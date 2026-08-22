#!/usr/bin/env python
"""Anti-theater lint: static detection of verification theater.

Permanent infrastructure for the Stage-3 quality gate (WP-1.4):
``docs/LAST200_STAGE3_QUALITY_REVIEW.md`` section 5.3 ("Anti-theater lint
rules (must never pass review)"), with runtime twins described in
``docs/LAST200_STAGE4_TESTING_STRATEGY.md`` section 5.

Rules implemented (AST-based; Python stdlib only):

R1  Verifier returns literal bool -- functions named ``verify_*`` /
    ``check_*`` / ``prove_*`` / ``is_*`` whose returns are all constant
    ``True``/``False`` (Stage-3 rule 2).
R2  Hardcoded verdict literals -- ``"verified": True`` / ``"passed": True``
    / ``"agrees": ...`` / ``"ok": ...`` dict entries inside verifier bodies,
    and assignments of literal bools / verdict strings to verdict-named
    variables that are never recomputed (Stage-3 rule 1).  Pure early-exit
    guards (``if n == 0: return {...}`` whose branch body is only the
    return) are exempt.
R3  Agreement/score magic constants without provenance -- assignments or
    dict entries under ``*score*`` / ``*agreement*`` / ``*confidence*`` /
    ``*accuracy*`` names whose value is a bare numeric literal >= 0.8 with
    no ``# provenance:`` comment or citation within 3 lines (Stage-3
    rule 5).
R4  Self-referential verification -- inside ``verify_*`` / ``prove_*`` /
    ``check_*`` functions, a call-chain in which the output of one
    locally-defined method flows into the arguments of another, while the
    two direct call outputs are compared against each other in a single
    expression (the D-10 circular cross-check class; Stage-3 rule 4
    heuristic).  Deliberately narrow: consistency checks that compare
    B(A(x)) against an inline formula of A(x), or round trips against the
    input x, are legitimate and stay exempt.
R5  Tests asserting an implementation against itself -- ``assert f(...) ==
    f(...)`` style identical-call comparisons (Stage-3 rule 10 class).
R6  Constant-return stubs under ``@maxwell_cite`` -- decorated functions
    whose entire body is ``return <constant>`` (includes ``return True``
    and dicts/lists of bare literals; Stage-3 rules 2-3).
R7  Hardcoded physical constants -- numeric literals of the
    speed-of-light family {2.99792458e10, 2.9979e10, 2.99792e10, 3.0e10}
    anywhere in ``maxwell/`` outside ``maxwell/config/constants.py``, and
    literal standard gravity 980.665 outside constants/data modules; all
    code must reference ``CONST.C`` / a pinned store value instead.  In
    ``tests/`` the finding is MEDIUM and suppressed entirely when a
    provenance comment (matching the R3 provenance regex) appears within
    2 lines, because test goldens may legitimately pin a number while the
    migration into ``tests/articles/reference_values.json`` proceeds.
    Historical anchors that merely LOOK similar (e.g. the Weber-Kohlrausch
    3.107e10 cm/s) are deliberately not in the family and stay exempt.
R8  Chapter drift -- ``@maxwell_cite(..., chapter="X")`` where ``X`` is
    not one of the chapter titles of the Treatise part tables in
    ``check_coverage.py`` (imported as the single source of truth;
    titles are normalized case-insensitively, stripping a leading
    ``Ch <roman>:`` / ``Preliminary:`` prefix, mapping ``&`` to `` and ``
    and collapsing whitespace).  Severity is MEDIUM everywhere: ~1.5k
    drifting call sites predate this rule and are unowned; promote to
    HIGH after a dedicated remediation wave.
R9  Out-of-range mixed citations -- a single function whose
    ``@maxwell_cite`` article list mixes at least one last-200 article
    (>= 667) with at least one article < 667.  Definition: the last-200
    program scope is Arts. 667-866; citing outside that scope from an
    in-scope function hides unimplemented or parked claims.  Such a
    citation is only legal when the decorator line carries a
    ``PARKING-LOT:`` comment within 2 lines (the explicit parking
    convention); otherwise HIGH.  Functions citing ONLY articles < 667
    are known pre-LAST200 backlog and are NOT flagged.
R10 Test theater -- ``tests/`` functions decorated with
    ``@pytest.mark.article(...)`` whose asserts contain no numeric
    comparison at all (only key-presence, ``in``, ``isinstance``,
    bare-bool or ``None`` checks, string/bool equality).  A qualifying
    article test must pin at least one number with a stated tolerance.
    Quarantine-marked tests and tests using ``pytest.raises`` are
    exempt.  HIGH everywhere.

Detector policy is conservative: false negatives are preferred over false
positives that would block CI on legitimate code.

Usage:
    python scripts/anti_theater_lint.py [paths ...] [--json] [--rules R1,R2]

Exit codes:
    0 -- no HIGH-severity findings
    1 -- at least one HIGH-severity finding
    2 -- configuration error (bad arguments, no scannable files)
"""
from __future__ import annotations

import argparse
import ast
import functools
import importlib.util
import json
import os
import re
import sys
from dataclasses import dataclass, asdict

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SCAN_DIRS = ("maxwell", "tests")

RULE_IDS = ("R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10")

# Severity levels.  Only HIGH findings flip the exit code to 1.
HIGH = "HIGH"
MEDIUM = "MEDIUM"

# Function-name prefixes treated as verifiers (Stage-3 rules 1-2).
_VERIFIER_PREFIXES = ("verify_", "check_", "prove_")
_BOOL_STUB_PREFIXES = ("verify_", "check_", "prove_", "is_")

# Dict keys that carry verification verdicts (Stage-3 rule 1).
_VERDICT_KEYS = frozenset({"verified", "agrees", "passed", "ok"})

# String literals that encode a verdict.
_VERDICT_STRINGS = frozenset(
    {"pass", "passed", "ok", "verified", "fail", "failed", "yes", "no"}
)

# Names that carry a verdict when assigned a literal (Stage-3 rule 1).
# Narrow to verdict semantics: property flags such as ``is_transverse``
# are physics attributes, not verification verdicts, and stay exempt.
_VERDICT_NAME_RE = re.compile(
    r"(?:^is_(?:verified|passed|ok|valid)$|_check$|^(?:verified|verdict|passed|ok)$)"
)

# Score/agreement/confidence/accuracy magic-constant detection (rule 5).
_SCORE_NAME_RE = re.compile(r"(?i)(score|agreement|confidence|accuracy)")
# 'accuracy_order' is a finite-difference order, not an agreement score.
_SCORE_NAME_EXCLUDE_RE = re.compile(r"(?i)(tolerance|threshold|order)")
_SCORE_THRESHOLD = 0.8

# Provenance escape hatch for R3: a comment/citation near the literal.
_PROVENANCE_RE = re.compile(
    r"(?i)provenance\s*:|\bart\.?\s*\d|\barticle\s+\d|\btreatise\b"
    r"|doi\s*:|https?://|reference_values"
)
_PROVENANCE_WINDOW = 3  # lines above/below the finding

# R7: hardcoded physical constants.  The speed-of-light family is exact-
# value membership: historical anchors such as the Weber-Kohlrausch
# 3.107e10 cm/s are deliberately NOT members and stay exempt.  Integer
# twins (e.g. 30000000000) compare equal to the float members.
_R7_LIGHT_FAMILY = frozenset({2.99792458e10, 2.9979e10, 2.99792e10, 3.0e10})
_R7_G_STANDARD = 980.665
_R7_CONSTANTS_FILE = "maxwell/config/constants.py"
# Literal 980.665 is additionally exempt in constants/data modules.
_R7_DATA_HINTS = ("constants", "data")
# In tests/ goldens are exempt when provenance appears within 2 lines.
_R7_TESTS_PROVENANCE_WINDOW = 2

# R9: the explicit parking convention for out-of-scope citations.
_PARKING_LOT_RE = re.compile(r"(?i)parking[- ]lot\s*:")
_PARKING_LOT_WINDOW = 2
_LAST200_FIRST_ARTICLE = 667

_SNIPPET_WIDTH = 110


@dataclass
class Finding:
    """One lint finding."""

    file: str
    line: int
    rule: str
    severity: str
    message: str
    snippet: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    def format_text(self) -> str:
        loc = f"{self.file}:{self.line}"
        text = f"{loc}: [{self.rule}|{self.severity}] {self.message}"
        if self.snippet:
            text += f"\n    | {self.snippet}"
        return text


@dataclass
class FileContext:
    """Everything the per-rule checkers need about one parsed file."""

    tree: ast.Module
    lines: list[str]
    relpath: str  # repo-relative, forward slashes
    in_tests: bool

    def snippet(self, lineno: int) -> str:
        if 1 <= lineno <= len(self.lines):
            return self.lines[lineno - 1].strip()[:_SNIPPET_WIDTH]
        return ""

    def severity_for_source(self) -> str:
        """Findings in the test tree are MEDIUM unless a rule says otherwise.

        Test files legitimately build expected-value fixtures, so source-
        pattern rules (R1-R3) are downgraded there; structural theater
        (R4-R6) stays HIGH everywhere.
        """
        return MEDIUM if self.in_tests else HIGH

    def has_provenance_near(self, lineno: int, window: int = _PROVENANCE_WINDOW) -> bool:
        return self.has_comment_near(lineno, _PROVENANCE_RE, window)

    def has_comment_near(self, lineno: int, pattern, window: int) -> bool:
        """True when ``pattern`` matches any source line within ``window``
        lines above or below ``lineno`` (1-based)."""
        lo = max(0, lineno - 1 - window)
        hi = min(len(self.lines), lineno + window)
        return any(pattern.search(line) for line in self.lines[lo:hi])


# ── small AST helpers ─────────────────────────────────────────────


def _is_scope_boundary(node: ast.AST) -> bool:
    return isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))


def walk_local(node: ast.AST):
    """ast.walk that does not descend into nested defs/classes.

    The starting node itself is always yielded.
    """
    stack = [node]
    while stack:
        current = stack.pop()
        yield current
        for child in ast.iter_child_nodes(current):
            if current is not node and _is_scope_boundary(current):
                continue
            if not (current is not node and _is_scope_boundary(child)):
                stack.append(child)


def _iter_stmts(body: list):
    """Yield statements in source order, recursing into compound blocks
    but never into nested function/class bodies."""
    for stmt in body:
        yield stmt
        if _is_scope_boundary(stmt):
            continue
        if isinstance(stmt, ast.Match):
            for case in stmt.cases:
                yield from _iter_stmts(case.body)
            continue
        if isinstance(stmt, ast.Try):
            for handler in stmt.handlers:
                yield from _iter_stmts(handler.body)
        for _field, value in ast.iter_fields(stmt):
            if isinstance(value, list) and value and isinstance(value[0], ast.stmt):
                yield from _iter_stmts(value)


def _function_defs(tree: ast.Module):
    """All FunctionDef/AsyncFunctionDef nodes including methods."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node


def _decorator_names(node) -> list[str]:
    names = []
    for deco in getattr(node, "decorator_list", []):
        target = deco.func if isinstance(deco, ast.Call) else deco
        if isinstance(target, ast.Name):
            names.append(target.id)
        elif isinstance(target, ast.Attribute):
            names.append(target.attr)
    return names


def _callee_name(call: ast.Call) -> str | None:
    func = call.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _strip_docstring(body: list) -> list:
    """Return body without a leading docstring statement."""
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        return body[1:]
    return body


def _enclosing_if_is_pure_guard(tree: ast.Module, target: ast.AST) -> bool:
    """True when ``target`` sits in an If whose branch body is exactly the
    enclosing Return -- the degenerate-input early-exit guard pattern:

        if n == 0:
            return {"verified": True, ...}
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            for branch in (node.body, node.orelse):
                if len(branch) == 1 and branch[0] is target:
                    return True
    return False


def _names_used(node: ast.AST) -> set[str]:
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


def _calls_in(node: ast.AST):
    return (n for n in ast.walk(node) if isinstance(n, ast.Call))


def _is_bool_constant(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and isinstance(node.value, bool)


def _is_constant_expr(node: ast.AST) -> bool:
    """Fully literal expression (constants, and dicts/lists/tuples/sets of
    them).  Used by R6 to recognize stub/prose returns."""
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return all(_is_constant_expr(elt) for elt in node.elts)
    if isinstance(node, ast.Dict):
        return all(
            _is_constant_expr(part)
            for pair in zip(node.keys, node.values)
            for part in pair
            if part is not None
        )
    return False


def _is_number_ge(node: ast.AST, threshold: float) -> bool:
    if not isinstance(node, ast.Constant) or isinstance(node.value, bool):
        return False
    if not isinstance(node.value, (int, float)):
        return False
    return node.value >= threshold


# ── R1: verifier returns only constant bools ─────────────────────


def _has_data_conditioned_bool_return(func) -> bool:
    """True when a literal-bool return sits under an If whose test refers
    to a name computed inside the function body -- the legitimate
    scan-and-bail pattern:

        for point in points:
            if np.linalg.norm(curl) > tolerance:
                return False
        return True
    """
    assigned = set()
    for stmt in _iter_stmts(func.body):
        if isinstance(stmt, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets = (
                stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
            )
            for target in targets:
                if isinstance(target, ast.Name):
                    assigned.add(target.id)

    def _conditioned(body: list) -> bool:
        for stmt in body:
            if _is_scope_boundary(stmt):
                continue
            if isinstance(stmt, ast.If):
                test_names = _names_used(stmt.test) & assigned
                branch_has_bool_return = any(
                    isinstance(n, ast.Return)
                    and n.value is not None
                    and _is_bool_constant(n.value)
                    for branch in (stmt.body, stmt.orelse)
                    for n in walk_local_list(branch)
                )
                if test_names and branch_has_bool_return:
                    return True
                if _conditioned(stmt.body) or _conditioned(stmt.orelse):
                    return True
            elif isinstance(stmt, (ast.For, ast.While, ast.With)):
                if _conditioned(stmt.body) or _conditioned(
                    getattr(stmt, "orelse", [])
                ):
                    return True
            elif isinstance(stmt, ast.Try):
                bodies = [stmt.body, stmt.orelse, stmt.finalbody] + [
                    handler.body for handler in stmt.handlers
                ]
                if any(_conditioned(b) for b in bodies):
                    return True
            elif isinstance(stmt, ast.Match):
                if any(_conditioned(case.body) for case in stmt.cases):
                    return True
        return False

    return _conditioned(func.body)


def walk_local_list(body: list):
    for stmt in body:
        yield from walk_local(stmt)


def _check_r1(ctx: FileContext) -> list[Finding]:
    findings = []
    for func in _function_defs(ctx.tree):
        name = func.name
        if not name.startswith(_BOOL_STUB_PREFIXES):
            continue
        returns = [
            n
            for n in walk_local(func)
            if isinstance(n, ast.Return) and n is not func
        ]
        if not returns:
            continue
        if not all(
            ret.value is not None and _is_bool_constant(ret.value)
            for ret in returns
        ):
            continue
        if _has_data_conditioned_bool_return(func):
            continue  # computed early-exit verdicts, not a stub
        findings.append(
            Finding(
                file=ctx.relpath,
                line=func.lineno,
                rule="R1",
                severity=ctx.severity_for_source(),
                message=(
                    f"verifier '{name}' returns only literal bools "
                    f"({len(returns)} return site(s)) -- verdicts must "
                    f"be computed from compared quantities"
                ),
                snippet=ctx.snippet(func.lineno),
            )
        )
    return findings


# ── R2: hardcoded verdict literals ───────────────────────────────


def _check_r2(ctx: FileContext) -> list[Finding]:
    findings = []

    # (a) verdict dict entries inside verifier-named functions.
    for func in _function_defs(ctx.tree):
        if not func.name.startswith(_VERIFIER_PREFIXES):
            continue
        for node in walk_local(func):
            if not isinstance(node, ast.Dict):
                continue
            for key, value in zip(node.keys, node.values):
                if (
                    isinstance(key, ast.Constant)
                    and isinstance(key.value, str)
                    and key.value in _VERDICT_KEYS
                    and _is_bool_constant(value)
                ):
                    ret = _enclosing_return(ctx.tree, node)
                    if ret is not None and _enclosing_if_is_pure_guard(
                        ctx.tree, ret
                    ):
                        continue  # degenerate-input early exit guard
                    findings.append(
                        Finding(
                            file=ctx.relpath,
                            line=value.lineno,
                            rule="R2",
                            severity=ctx.severity_for_source(),
                            message=(
                                f"hardcoded verdict '{key.value}: "
                                f"{value.value}' in verifier "
                                f"'{func.name}' -- verdicts must be "
                                f"expressions derived from compared "
                                f"quantities"
                            ),
                            snippet=ctx.snippet(value.lineno),
                        )
                    )

    # (b) verdict-named variables assigned a literal and never recomputed.
    for scope_body, scope_label in _scopes(ctx.tree):
        assigned: dict[str, int] = {}
        for stmt in _iter_stmts(scope_body):
            if isinstance(stmt, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                targets = (
                    stmt.targets
                    if isinstance(stmt, ast.Assign)
                    else [stmt.target]
                )
                for target in targets:
                    if isinstance(target, ast.Name):
                        assigned[target.id] = assigned.get(target.id, 0) + 1
        for stmt in _iter_stmts(scope_body):
            if not isinstance(stmt, ast.Assign):
                continue
            value = stmt.value
            literal = None
            if _is_bool_constant(value):
                literal = value.value
            elif (
                isinstance(value, ast.Constant)
                and isinstance(value.value, str)
                and value.value in _VERDICT_STRINGS
            ):
                literal = value.value
            if literal is None:
                continue
            for target in stmt.targets:
                if not isinstance(target, ast.Name):
                    continue
                name = target.id
                if not _VERDICT_NAME_RE.search(name):
                    continue
                if assigned.get(name, 0) != 1:
                    continue  # reassigned later: accumulator, not a verdict
                findings.append(
                    Finding(
                        file=ctx.relpath,
                        line=stmt.lineno,
                        rule="R2",
                        severity=ctx.severity_for_source(),
                        message=(
                            f"verdict variable '{name}' assigned literal "
                            f"{literal!r} and never recomputed -- "
                            f"compute the check instead of asserting it"
                        ),
                        snippet=ctx.snippet(stmt.lineno),
                    )
                )
    return findings


def _enclosing_return(tree: ast.Module, node: ast.AST) -> ast.Return | None:
    """Return the Return statement containing ``node``, if any."""
    for ret in (n for n in ast.walk(tree) if isinstance(n, ast.Return)):
        if ret.value is not None and node in ast.walk(ret.value):
            return ret
    return None


def _scopes(tree: ast.Module):
    """(body, label) pairs: the module body plus every function body."""
    yield tree.body, "<module>"
    for func in _function_defs(tree):
        yield func.body, func.name


# ── R3: agreement/score constants without provenance ─────────────


def _score_name(name: str) -> bool:
    return bool(_SCORE_NAME_RE.search(name)) and not _SCORE_NAME_EXCLUDE_RE.search(
        name
    )


def _check_r3(ctx: FileContext) -> list[Finding]:
    findings = []

    def maybe_add(lineno: int, label: str, value) -> None:
        if ctx.has_provenance_near(lineno):
            return
        findings.append(
            Finding(
                file=ctx.relpath,
                line=lineno,
                rule="R3",
                severity=ctx.severity_for_source(),
                message=(
                    f"agreement/score literal {value!r} for '{label}' "
                    f"without provenance -- compute the metric or add a "
                    f"'# provenance: ...' comment/citation within "
                    f"{_PROVENANCE_WINDOW} lines"
                ),
                snippet=ctx.snippet(lineno),
            )
        )

    # (a) assignments: score/agreement/... = <bare number >= threshold>
    for func_body in [ctx.tree.body] + [f.body for f in _function_defs(ctx.tree)]:
        for stmt in _iter_stmts(func_body):
            if isinstance(stmt, ast.Assign) and _is_number_ge(
                stmt.value, _SCORE_THRESHOLD
            ):
                for target in stmt.targets:
                    if isinstance(target, ast.Name) and _score_name(target.id):
                        maybe_add(stmt.lineno, target.id, stmt.value.value)

    # (b) dict entries under score-like keys (one nesting level included).
    for node in ast.walk(ctx.tree):
        if not isinstance(node, ast.Dict):
            continue
        for key, value in zip(node.keys, node.values):
            if not (
                isinstance(key, ast.Constant) and isinstance(key.value, str)
            ):
                continue
            if not _score_name(key.value):
                continue
            if _is_number_ge(value, _SCORE_THRESHOLD):
                maybe_add(value.lineno, key.value, value.value)
            elif isinstance(value, ast.Dict):
                for inner_key, inner_value in zip(value.keys, value.values):
                    if (
                        isinstance(inner_key, ast.Constant)
                        and isinstance(inner_key.value, str)
                        and _is_number_ge(inner_value, _SCORE_THRESHOLD)
                    ):
                        maybe_add(
                            inner_value.lineno,
                            f"{key.value}.{inner_key.value}",
                            inner_value.value,
                        )
    return findings


# ── R4: circular cross-checks (taint heuristic) ──────────────────


def _check_r4(ctx: FileContext) -> list[Finding]:
    findings = []
    # Callee set: functions/methods defined in this module.  Class names are
    # deliberately excluded: constructing an object is not computing a value
    # to be verified (EllipticIntegral(...), Quaternion(...) etc.), and
    # treating constructors as value origins produces false positives on
    # legitimate identity/orthogonality checks.
    local_funcs = _module_local_function_names(ctx.tree)

    for func in _function_defs(ctx.tree):
        if not func.name.startswith(_VERIFIER_PREFIXES):
            continue

        # 1) forward taint pass: name -> producing local callee.
        #    ``direct`` additionally records names assigned straight from a
        #    local call (R_energy = method(...)); names merely derived by
        #    arithmetic from tainted values stay in ``taint`` only.
        taint: dict[str, str] = {}
        direct: dict[str, str] = {}
        for stmt in _iter_stmts(func.body):
            if isinstance(stmt, ast.Assign):
                local_call = None
                for call in _calls_in(stmt.value):
                    callee = _callee_name(call)
                    if callee in local_funcs:
                        local_call = callee
                        break
                origin = local_call
                is_direct = local_call is not None
                if origin is None:
                    for used_name in sorted(_names_used(stmt.value)):
                        if used_name in taint:
                            origin = taint[used_name]
                            break
                if origin is None:
                    for target in stmt.targets:
                        if isinstance(target, ast.Name):
                            taint.pop(target.id, None)
                            direct.pop(target.id, None)
                    continue
                for target in stmt.targets:
                    if isinstance(target, ast.Name):
                        taint[target.id] = origin
                        if is_direct:
                            direct[target.id] = origin
                        else:
                            direct.pop(target.id, None)
            elif isinstance(stmt, ast.AugAssign) and isinstance(
                stmt.target, ast.Name
            ):
                taint.pop(stmt.target.id, None)
                direct.pop(stmt.target.id, None)

        # 2) feeding: a local call whose arguments use another local call's
        #    tainted output.
        feeding_pairs = []  # (origin_callee, fed_callee, line)
        for call in _calls_in(func):
            callee = _callee_name(call)
            if callee is None or callee not in local_funcs:
                continue
            arg_names = set()
            for arg in list(call.args) + [kw.value for kw in call.keywords]:
                arg_names |= _names_used(arg)
            for used_name in sorted(arg_names):
                origin = taint.get(used_name)
                if origin is not None and origin != callee:
                    feeding_pairs.append((origin, callee, call.lineno))
                    break

        if not feeding_pairs:
            continue

        # 3) circular combining: a single arithmetic/comparison expression
        #    that brings together the DIRECT outputs of both members of a
        #    feeding pair -- the check compares A's value to B(A)'s value.
        #    Conservatively restricted to direct call outputs on both sides
        #    (the D-10 signature): comparing B(A(x)) against an inline
        #    formula of A(x), or round trips against the input x, are
        #    legitimate consistency/identity checks and must not block CI.
        #    BoolOp conjunctions of error flags never count.
        hit_pair_index = None
        hit_line = None
        for node in walk_local(func):
            if not isinstance(node, (ast.BinOp, ast.Compare)):
                continue
            direct_origins = {
                direct[n.id]
                for n in ast.walk(node)
                if isinstance(n, ast.Name) and n.id in direct
            }
            if len(direct_origins) < 2:
                continue
            for index, (origin, callee, _line) in enumerate(feeding_pairs):
                if {origin, callee} <= direct_origins:
                    hit_pair_index = index
                    hit_line = node.lineno
                    break
            if hit_pair_index is not None:
                break

        if hit_pair_index is None:
            continue

        origin, callee, feed_line = feeding_pairs[hit_pair_index]
        findings.append(
            Finding(
                file=ctx.relpath,
                line=feed_line,
                rule="R4",
                severity=HIGH,
                message=(
                    f"self-referential cross-check in '{func.name}': output "
                    f"of '{origin}' feeds '{callee}' and both results are "
                    f"compared against each other (line {hit_line}) -- the "
                    f"check compares a value to itself; use independently "
                    f"sourced inputs"
                ),
                snippet=ctx.snippet(feed_line),
            )
        )
    return findings


def _module_local_function_names(tree: ast.Module) -> set[str]:
    """Function/method names defined in this module (no class names)."""
    names = set()
    for stmt in tree.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names.add(stmt.name)
    for cls in (n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)):
        for sub in cls.body:
            if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                names.add(sub.name)
    return names


# ── R5: identical-call self-comparisons in asserts ───────────────


def _unwrap_approx(node: ast.AST) -> ast.AST:
    if (
        isinstance(node, ast.Call)
        and _callee_name(node) == "approx"
        and node.args
    ):
        return node.args[0]
    return node


def _check_r5(ctx: FileContext) -> list[Finding]:
    findings = []
    for node in ast.walk(ctx.tree):
        if not isinstance(node, ast.Assert):
            continue
        test = node.test
        if (
            not isinstance(test, ast.Compare)
            or len(test.ops) != 1
            or not isinstance(test.ops[0], (ast.Eq, ast.Is))
        ):
            continue
        left = _unwrap_approx(test.left)
        right = _unwrap_approx(test.comparators[0])
        if ast.dump(left) != ast.dump(right):
            continue
        subtree_calls = [
            c
            for c in ast.walk(test)
            if isinstance(c, ast.Call) and _callee_name(c) != "approx"
        ]
        if not subtree_calls:
            continue
        findings.append(
            Finding(
                file=ctx.relpath,
                line=node.lineno,
                rule="R5",
                severity=HIGH,
                message=(
                    "assert compares a call to an identical call "
                    "(self-confirmation) -- assert against an independent "
                    "expected value"
                ),
                snippet=ctx.snippet(node.lineno),
            )
        )
    return findings


# ── R6: constant-return stubs under @maxwell_cite ────────────────


def _leaf_counts(node: ast.AST) -> tuple[int, int, bool]:
    """(prose_leaves, numeric_leaves, is_empty) for a constant expression.

    Prose leaves are bool/str/None constants (stub verdicts and prose);
    numeric leaves are int/float.  A constant return counts as theater when
    prose dominates (prose-as-implementation); reference-data tables that
    merely carry a few string annotations stay exempt (conservative policy).
    """
    if isinstance(node, ast.Constant):
        if node.value is None or isinstance(node.value, (bool, str)):
            return 1, 0, False
        return 0, 1, False
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        if not node.elts:
            return 0, 0, True
        prose = sum(_leaf_counts(elt)[0] for elt in node.elts)
        numeric = sum(_leaf_counts(elt)[1] for elt in node.elts)
        return prose, numeric, False
    if isinstance(node, ast.Dict):
        if not node.keys:
            return 0, 0, True
        # Only values carry semantics; string keys are labels, not prose.
        prose = sum(
            _leaf_counts(value)[0] for value in node.values if value is not None
        )
        numeric = sum(
            _leaf_counts(value)[1] for value in node.values if value is not None
        )
        return prose, numeric, False
    return 0, 0, False


def _check_r6(ctx: FileContext) -> list[Finding]:
    findings = []
    for func in _function_defs(ctx.tree):
        if "maxwell_cite" not in _decorator_names(func):
            continue
        body = _strip_docstring(func.body)
        if len(body) != 1 or not isinstance(body[0], ast.Return):
            continue
        value = body[0].value
        if value is None or not _is_constant_expr(value):
            continue
        prose, numeric, is_empty = _leaf_counts(value)
        if not is_empty and not (prose > numeric or (prose > 0 and numeric == 0)):
            continue  # numeric/data-table return, not prose-as-implementation
        label = ast.unparse(value)
        if len(label) > 60:
            label = label[:57] + "..."
        findings.append(
            Finding(
                file=ctx.relpath,
                line=func.lineno,
                rule="R6",
                severity=HIGH,
                message=(
                    f"@maxwell_cite function '{func.name}' body is the "
                    f"constant return `{label}` -- implement the article's "
                    f"computation instead of returning a verdict/prose"
                ),
                snippet=ctx.snippet(body[0].lineno),
            )
        )
    return findings


# ── R7: hardcoded physical constants ─────────────────────────────


def _r7_exempt_data_module(relpath: str) -> bool:
    """Constants/data modules may legitimately carry reference numbers."""
    parts = relpath.replace("\\", "/").split("/")
    for part in parts:
        stem = part[:-3] if part.endswith(".py") else part
        lowered = stem.lower()
        if any(hint in lowered for hint in _R7_DATA_HINTS):
            return True
    return False


def _check_r7(ctx: FileContext) -> list[Finding]:
    findings = []
    relpath = ctx.relpath
    if relpath == _R7_CONSTANTS_FILE:
        return findings  # the canonical home of the constants

    def maybe_add(node: ast.Constant, kind: str) -> None:
        if ctx.in_tests and ctx.has_provenance_near(
            node.lineno, _R7_TESTS_PROVENANCE_WINDOW
        ):
            return  # provenanced test golden during the store migration
        severity = MEDIUM if ctx.in_tests else HIGH
        findings.append(
            Finding(
                file=relpath,
                line=node.lineno,
                rule="R7",
                severity=severity,
                message=(
                    f"hardcoded physical constant {node.value!r} ({kind}) "
                    f"-- reference maxwell.config.constants.CONST or the "
                    f"central reference store instead of inlining"
                ),
                snippet=ctx.snippet(node.lineno),
            )
        )

    for node in ast.walk(ctx.tree):
        if not isinstance(node, ast.Constant) or isinstance(node.value, bool):
            continue
        if not isinstance(node.value, (int, float)):
            continue
        if node.value in _R7_LIGHT_FAMILY:
            maybe_add(node, "speed-of-light family; use CONST.C")
        elif node.value == _R7_G_STANDARD and not _r7_exempt_data_module(relpath):
            maybe_add(node, "standard gravity g; use a pinned store value")
    return findings


# ── R8: chapter drift against the PARTS table ────────────────────


_CHAPTER_PREFIX_RE = re.compile(
    r"^(?:ch(?:apter)?\s+[ivxlcdm]+\s*:\s*|preliminary\s*:\s*)"
)


def _normalize_chapter_title(title: str) -> str:
    text = title.strip().lower()
    text = _CHAPTER_PREFIX_RE.sub("", text)
    text = text.replace("&", " and ")
    return re.sub(r"\s+", " ", text).strip()


@functools.lru_cache(maxsize=1)
def _canonical_chapter_titles() -> frozenset[str]:
    """Chapter-title set from check_coverage.py's PARTS table (the single
    source of truth).  Empty frozenset if the table cannot be loaded --
    the R8 checker then degrades to no-op instead of crashing CI."""
    path = os.path.join(REPO_ROOT, "check_coverage.py")
    try:
        spec = importlib.util.spec_from_file_location(
            "_anti_theater_check_coverage", path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        parts = getattr(module, "PARTS", None)
        if not isinstance(parts, dict):
            return frozenset()
        titles = set()
        for part in parts.values():
            for chapter in part.get("chapters", []):
                if chapter and isinstance(chapter[0], str):
                    normalized = _normalize_chapter_title(chapter[0])
                    if normalized:
                        titles.add(normalized)
        return frozenset(titles)
    except Exception:  # noqa: BLE001 - lint must never crash the gate
        return frozenset()


def _check_r8(ctx: FileContext) -> list[Finding]:
    titles = _canonical_chapter_titles()
    if not titles:
        return []
    findings = []
    for func in _function_defs(ctx.tree):
        for deco in getattr(func, "decorator_list", []):
            if not isinstance(deco, ast.Call) or _callee_name(deco) != "maxwell_cite":
                continue
            for kw in deco.keywords:
                if kw.arg != "chapter":
                    continue
                if not (
                    isinstance(kw.value, ast.Constant)
                    and isinstance(kw.value.value, str)
                ):
                    continue
                given = _normalize_chapter_title(kw.value.value)
                if given and given not in titles:
                    findings.append(
                        Finding(
                            file=ctx.relpath,
                            line=kw.value.lineno,
                            rule="R8",
                            severity=MEDIUM,
                            message=(
                                f"@maxwell_cite chapter={kw.value.value!r} "
                                f"in '{func.name}' does not match any "
                                f"Treatise chapter title in the PARTS "
                                f"table (check_coverage.py)"
                            ),
                            snippet=ctx.snippet(kw.value.lineno),
                        )
                    )
    return findings


# ── R9: out-of-range mixed citations without parking ─────────────


def _maxwell_cite_calls(func):
    for deco in getattr(func, "decorator_list", []):
        if isinstance(deco, ast.Call) and _callee_name(deco) == "maxwell_cite":
            yield deco


def _check_r9(ctx: FileContext) -> list[Finding]:
    findings = []
    for func in _function_defs(ctx.tree):
        articles: list[int] = []
        cite_lines: list[int] = []
        for deco in _maxwell_cite_calls(func):
            cite_lines.append(deco.lineno)
            for arg in deco.args:
                if (
                    isinstance(arg, ast.Constant)
                    and isinstance(arg.value, int)
                    and not isinstance(arg.value, bool)
                ):
                    articles.append(arg.value)
        in_scope = [a for a in articles if a >= _LAST200_FIRST_ARTICLE]
        out_scope = [a for a in articles if a < _LAST200_FIRST_ARTICLE]
        if not in_scope or not out_scope:
            continue  # pure backlog files (only < 667) are not flagged
        parked = any(
            ctx.has_comment_near(line, _PARKING_LOT_RE, _PARKING_LOT_WINDOW)
            for line in cite_lines
        )
        if parked:
            continue
        findings.append(
            Finding(
                file=ctx.relpath,
                line=cite_lines[0],
                rule="R9",
                severity=HIGH,
                message=(
                    f"'{func.name}' mixes last-200 articles "
                    f"({', '.join(str(a) for a in sorted(set(in_scope)))}) "
                    f"with out-of-scope articles "
                    f"({', '.join(str(a) for a in sorted(set(out_scope)))}) "
                    f"without a 'PARKING-LOT:' comment on the decorator"
                ),
                snippet=ctx.snippet(cite_lines[0]),
            )
        )
    return findings


# ── R10: article-marked tests without numeric asserts ────────────

_NUMERIC_CALLEES = frozenset(
    {
        "approx",
        "allclose",
        "isclose",
        "assert_allclose",
        "assert_almost_equal",
        "isfinite",
        "isnan",
        "isinf",
    }
)

# Calls that build/inspect containers: an equality against them is a
# structural comparison, not a numeric pin (R10).
_NON_NUMERIC_CALLEES = frozenset(
    {
        "set",
        "list",
        "dict",
        "tuple",
        "sorted",
        "str",
        "isinstance",
        "keys",
        "values",
        "items",
        "len",
    }
)


def _contains_numeric_constant(node: ast.AST) -> bool:
    for sub in ast.walk(node):
        if (
            isinstance(sub, ast.Constant)
            and not isinstance(sub.value, bool)
            and isinstance(sub.value, (int, float))
        ):
            return True
    return False


def _assert_is_numeric(test: ast.AST) -> bool:
    """True when an assert test pins at least one number."""
    for sub in ast.walk(test):
        if isinstance(sub, ast.Call) and _callee_name(sub) in _NUMERIC_CALLEES:
            return True
    if isinstance(test, ast.Compare):
        if any(
            isinstance(op, (ast.Lt, ast.LtE, ast.Gt, ast.GtE)) for op in test.ops
        ):
            return True
        operands = [test.left] + list(test.comparators)
        if any(_contains_numeric_constant(op) for op in operands):
            return True
        if any(isinstance(op, (ast.Eq, ast.NotEq)) for op in test.ops):
            if any(_operand_is_computed(op) for op in operands):
                return True
    return False


def _operand_is_computed(node: ast.AST) -> bool:
    """Equality operand produced by a genuine computation (numeric pin),
    as opposed to a container construction like ``set(d.keys())``."""
    for sub in ast.walk(node):
        if isinstance(sub, ast.BinOp):
            return True
        if isinstance(sub, ast.Call):
            callee = _callee_name(sub)
            if callee is not None and callee not in _NON_NUMERIC_CALLEES:
                return True
    return False


def _has_article_mark(func) -> bool:
    for deco in getattr(func, "decorator_list", []):
        target = deco.func if isinstance(deco, ast.Call) else deco
        if isinstance(target, ast.Attribute) and target.attr == "article":
            return True
    return False


def _decorator_mentions(func, needle: str) -> bool:
    for deco in getattr(func, "decorator_list", []):
        for sub in ast.walk(deco):
            if isinstance(sub, ast.Name) and needle in sub.id:
                return True
            if isinstance(sub, ast.Attribute) and needle in sub.attr:
                return True
    return False


def _check_r10(ctx: FileContext) -> list[Finding]:
    if not ctx.in_tests:
        return []
    findings = []
    for func in _function_defs(ctx.tree):
        if not _has_article_mark(func):
            continue
        if _decorator_mentions(func, "quarantine"):
            continue
        uses_raises = any(
            isinstance(sub, ast.Call)
            and isinstance(sub.func, ast.Attribute)
            and sub.func.attr == "raises"
            for sub in walk_local(func)
        )
        if uses_raises:
            continue
        asserts = [
            node for node in walk_local(func) if isinstance(node, ast.Assert)
        ]
        if any(_assert_is_numeric(assert_node.test) for assert_node in asserts):
            continue
        if asserts:
            message = (
                f"article-marked test '{func.name}' has {len(asserts)} "
                f"assert(s) but no numeric comparison (structure/key/"
                f"bool checks only) -- qualifying tests must pin a "
                f"number with a stated tolerance"
            )
        else:
            message = (
                f"article-marked test '{func.name}' has no asserts at "
                f"all -- qualifying tests must pin a number with a "
                f"stated tolerance"
            )
        findings.append(
            Finding(
                file=ctx.relpath,
                line=func.lineno,
                rule="R10",
                severity=HIGH,
                message=message,
                snippet=ctx.snippet(func.lineno),
            )
        )
    return findings


_CHECKERS = {
    "R1": _check_r1,
    "R2": _check_r2,
    "R3": _check_r3,
    "R4": _check_r4,
    "R5": _check_r5,
    "R6": _check_r6,
    "R7": _check_r7,
    "R8": _check_r8,
    "R9": _check_r9,
    "R10": _check_r10,
}

RULE_DESCRIPTIONS = {
    "R1": "verifier returns literal True/False",
    "R2": "hardcoded verdict literals",
    "R3": "agreement/score magic constant without provenance",
    "R4": "self-referential (circular) verification",
    "R5": "test asserts a call against the identical call",
    "R6": "@maxwell_cite function whose body is a constant return",
    "R7": "hardcoded physical constant (speed-of-light family / g)",
    "R8": "@maxwell_cite chapter title drifts from the PARTS table",
    "R9": "mixed in-scope/out-of-scope citation without PARKING-LOT",
    "R10": "article-marked test without any numeric assert",
}


# ── driver ────────────────────────────────────────────────────────


def _in_tests_path(relpath: str) -> bool:
    parts = relpath.replace("\\", "/").split("/")
    return "tests" in parts or parts[-1].startswith("test_")


def lint_source(source: str, filename: str = "<string>", rules=None) -> list[Finding]:
    """Lint one source string.  Returns a list of Finding (sorted).

    Raises SyntaxError if the source does not parse.
    """
    tree = ast.parse(source, filename=filename)
    relpath = filename.replace("\\", "/")
    ctx = FileContext(
        tree=tree,
        lines=source.splitlines(),
        relpath=relpath,
        in_tests=_in_tests_path(relpath),
    )
    active = RULE_IDS if rules is None else tuple(rules)
    findings: list[Finding] = []
    for rule_id in active:
        findings.extend(_CHECKERS[rule_id](ctx))
    findings.sort(key=lambda f: (f.file, f.line, f.rule))
    return findings


def scan_file(path: str, relpath: str | None = None, rules=None) -> list[Finding]:
    """Lint one file.  Unparseable files warn on stderr and yield []."""
    if relpath is None:
        relpath = os.path.relpath(path, REPO_ROOT).replace(os.sep, "/")
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            source = handle.read()
    except OSError as exc:
        print(f"anti_theater_lint: cannot read {path}: {exc}", file=sys.stderr)
        return []
    try:
        return lint_source(source, filename=relpath, rules=rules)
    except SyntaxError as exc:
        print(
            f"anti_theater_lint: syntax error in {relpath}:{exc.lineno}: {exc.msg}",
            file=sys.stderr,
        )
        return []


def collect_python_files(paths: list[str]) -> list[str]:
    """Expand files/directories into a sorted list of .py files."""
    collected = []
    for path in paths:
        if os.path.isfile(path):
            if path.endswith(".py"):
                collected.append(path)
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if d != "__pycache__"]
                for name in files:
                    if name.endswith(".py"):
                        collected.append(os.path.join(root, name))
        else:
            print(f"anti_theater_lint: no such path: {path}", file=sys.stderr)
    return sorted(set(collected))


def scan_paths(paths: list[str], rules=None) -> tuple[list[Finding], int]:
    """Scan files/directories.  Returns (findings, files_scanned)."""
    findings: list[Finding] = []
    files = collect_python_files(paths)
    for path in files:
        findings.extend(scan_file(path, rules=rules))
    findings.sort(key=lambda f: (f.file, f.line, f.rule))
    return findings, len(files)


def _default_paths() -> list[str]:
    return [os.path.join(REPO_ROOT, name) for name in DEFAULT_SCAN_DIRS]


def main(argv=None) -> int:
    # Windows consoles default to a charmap codec; findings may quote
    # unicode source (Greek letters, operators).  Never crash on output.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass

    parser = argparse.ArgumentParser(
        prog="anti_theater_lint",
        description=(
            "Static anti-theater lint (Stage-3 quality review section 5.3): "
            "detects verification theater in maxwell/ and tests/."
        ),
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="files or directories to scan (default: maxwell/ and tests/)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON instead of text",
    )
    parser.add_argument(
        "--rules",
        default=None,
        help=f"comma-separated subset of rules to run (default: all of "
        f"{','.join(RULE_IDS)})",
    )
    args = parser.parse_args(argv)

    rules = list(RULE_IDS)
    if args.rules:
        requested = [r.strip().upper() for r in args.rules.split(",") if r.strip()]
        unknown = [r for r in requested if r not in RULE_IDS]
        if unknown:
            parser.error(
                f"unknown rule(s): {', '.join(unknown)} "
                f"(valid: {', '.join(RULE_IDS)})"
            )
        rules = requested

    paths = args.paths or _default_paths()
    findings, files_scanned = scan_paths(paths, rules=rules)

    high = [f for f in findings if f.severity == HIGH]
    by_rule = {rid: 0 for rid in rules}
    by_severity = {HIGH: 0, MEDIUM: 0}
    for finding in findings:
        by_rule[finding.rule] = by_rule.get(finding.rule, 0) + 1
        by_severity[finding.severity] = by_severity.get(finding.severity, 0) + 1

    if args.json:
        payload = {
            "tool": "anti_theater_lint",
            "rules_active": rules,
            "files_scanned": files_scanned,
            "total_findings": len(findings),
            "high_findings": len(high),
            "summary": {"by_rule": by_rule, "by_severity": by_severity},
            "findings": [f.to_dict() for f in findings],
        }
        print(json.dumps(payload, indent=1))
    else:
        for finding in findings:
            print(finding.format_text())
        print(
            f"\nanti_theater_lint: {files_scanned} files scanned, "
            f"{len(findings)} finding(s) "
            f"({len(high)} HIGH) [rules: {', '.join(rules)}]"
        )
        if findings:
            detail = ", ".join(
                f"{rid}={by_rule[rid]}" for rid in rules if by_rule.get(rid)
            )
            print(f"by rule: {detail}")

    return 1 if high else 0


if __name__ == "__main__":
    sys.exit(main())

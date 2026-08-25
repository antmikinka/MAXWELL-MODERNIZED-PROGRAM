"""Meta-tests for scripts/anti_theater_lint.py (Stage-3 section 5.3 gate).

Planted-violation fixtures (one per rule class) assert that every detector
catches the theater pattern it is defined against; canonical clean code must
produce zero findings; and a full-repo scan smoke test asserts the scanner
completes with structured results (it does NOT assert zero repo findings --
remediation of the baseline findings is concurrent work owned by other
agents, and this file is their measurement instrument).

Run: PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_anti_theater_lint.py
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LINT_PATH = REPO_ROOT / "scripts" / "anti_theater_lint.py"


def _load_lint():
    spec = importlib.util.spec_from_file_location("anti_theater_lint", LINT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["anti_theater_lint"] = module  # dataclasses needs module lookup
    spec.loader.exec_module(module)
    return module


lint = _load_lint()


def _findings(source, filename="maxwell/module_under_test.py", rules=None):
    return lint.lint_source(source, filename=filename, rules=rules)


# ── planted-violation fixtures ────────────────────────────────────

R1_BAD = '''
def verify_alignment(points):
    """Stub verifier: verdict is a literal, not a computation."""
    return True
'''

R1_GOOD = '''
def verify_bound(points):
    """Computed verifier with a data-conditioned early exit."""
    worst = 0.0
    for point in points:
        err = measure(point)
        worst = max(worst, err)
        if worst > 0.1:
            return False
    return True
'''

R2_DICT_BAD = '''
def verify_relation(data):
    """Hardcoded verdict literal in the return dict."""
    error = compute_error(data)
    return {"error": error, "verified": True}
'''

R2_ASSIGN_BAD = '''
def check_dimensions(quantity):
    """Hardcoded verdict variable, never recomputed."""
    velocity_check = True
    return {"velocity_dimensions": velocity_check}
'''

R2_GOOD = '''
def verify_all(rows):
    """Accumulator pattern: the literal is reassigned from data."""
    all_agree = True
    for row in rows:
        if not row_agrees(row):
            all_agree = False
    return {"all_agree": all_agree}


def verify_reassign(rows):
    """Verdict-named variable reassigned from data is not theater."""
    verified = True
    for row in rows:
        if not row_ok(row):
            verified = False
    return {"verified": verified}


def verify_empty(items):
    """Pure early-exit guard plus a computed final verdict."""
    if not items:
        return {"verified": True}
    error = compute(items)
    return {"verified": bool(error < 0.01)}
'''

R3_BAD = '''
def analyze_webers_theory():
    """Invented agreement scores without provenance."""
    agreement_score = 0.9
    return {
        "experimental_agreement": {
            "electrostatics": 1.0,
            "magnetostatics": 0.9,
            "waves": 0.0,
        },
    }
'''

R3_GOOD = '''
def analyze_amperes_theory():
    return {
        "experimental_agreement": {
            # provenance: computed residual vs reference_values.json art841
            "electrostatics": 0.95,
        },
    }


def set_thresholds():
    """Names outside the score class stay exempt."""
    tolerance_score = 0.99
    accuracy_order = 4
    return {"tolerance_score": tolerance_score, "accuracy_order": accuracy_order}
'''

R4_BAD = '''
def lenz_method(emf, current):
    return emf / current


def energy_dissipation_method(current, time, heat):
    return heat / (current * current * time)


def verify_absolute_resistance(emf, current):
    """D-10 shape: heat built from R_lenz, R_energy recovered from heat,
    then R_energy compared back to R_lenz -- a value compared to itself."""
    R_lenz = lenz_method(emf, current)
    time = 1.0
    heat = R_lenz * current * current * time
    R_energy = energy_dissipation_method(current, time, heat)
    consistency_error = abs(R_lenz - R_energy) / R_lenz
    return {"verified": consistency_error < 1e-10}
'''

R4_GOOD_ROUNDTRIP = '''
def forward(x):
    return 2.0 * x


def inverse(y):
    return y / 2.0


def verify_roundtrip(x):
    """Legitimate inverse round trip: compared against the input x."""
    y = forward(x)
    z = inverse(y)
    error = abs(z - x)
    return {"verified": error < 1e-12}
'''

R4_GOOD_INDEPENDENT = '''
def recoil_method(m, period):
    return m / period


def lenz_method(emf, current):
    return emf / current


def verify_cross_method(m, period, emf, current):
    """Legitimate cross-method check: independent inputs, no feeding."""
    R_recoil = recoil_method(m, period)
    R_lenz = lenz_method(emf, current)
    error = abs(R_recoil - R_lenz) / R_recoil
    return {"verified": error < 1e-6}
'''

R5_BAD = """
def test_field_identity():
    assert calc_field(1.0) == calc_field(1.0)
"""

R5_BAD_APPROX = """
def test_energy_identity():
    assert calc_energy(2.0) == pytest.approx(calc_energy(2.0))
"""

R5_GOOD = """
def test_field_value():
    expected = 2.5
    assert calc_field(1.0) == expected
    assert calc_field(1.0) == calc_field(2.0)
"""

R6_BAD = '''
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(820, part=4, theory_class="maxwell_original")
def prove_real_rotation_required():
    """Bare-bool stub under a citation."""
    return True


@maxwell_cite(821, part=4, theory_class="maxwell_original")
def summarize_results():
    """Prose dict as implementation."""
    return {
        "result_1": "The velocity is split",
        "result_2": "Rotation adds on the round trip",
    }
'''

R6_GOOD = '''
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(820, part=4)
def prove_real_rotation(theta):
    """Computed discriminant: not a constant return."""
    discriminant = theta + theta
    return {
        "discriminant": discriminant,
        "requires_real_rotation": bool(discriminant != 0.0),
    }


@maxwell_cite(46, part=1)
def table_specific_inductive_capacities():
    """Numeric reference-data table: exempt."""
    return {"vacuum": 1.0, "air": 1.00059, "water": 1.77}
'''

CLEAN_CANONICAL = '''
"""Canonical clean module: zero findings expected."""
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(676, part=4)
def calc_coil_field(current, radius):
    """On-axis field of a single circular coil."""
    return 2.0 * current / radius


def independent_reference(current, radius):
    """Independent expectation source."""
    return 2.0 * current / radius * (1.0 + 1e-15)


def verify_coil_field(current=1.0, radius=10.0, tolerance=1e-6):
    """Good verifier: verdict computed from compared quantities."""
    computed = calc_coil_field(current, radius)
    expected = independent_reference(current, radius)
    rel_error = abs(computed - expected) / expected
    return {
        "value": computed,
        "expected": expected,
        "rel_error": rel_error,
        "passed": bool(rel_error < tolerance),
    }
'''


# ── per-rule detector tests ───────────────────────────────────────


def test_r1_flags_constant_bool_verifier():
    findings = _findings(R1_BAD)
    assert [f.rule for f in findings] == ["R1"]
    assert findings[0].severity == lint.HIGH
    assert "verify_alignment" in findings[0].message


def test_r1_ignores_data_conditioned_returns():
    assert _findings(R1_GOOD) == []


def test_r2_flags_hardcoded_verdict_in_dict():
    findings = [f for f in _findings(R2_DICT_BAD) if f.rule == "R2"]
    assert len(findings) == 1
    assert "verified" in findings[0].message


def test_r2_flags_verdict_variable_assignment():
    findings = [f for f in _findings(R2_ASSIGN_BAD) if f.rule == "R2"]
    assert len(findings) == 1
    assert "velocity_check" in findings[0].message


def test_r2_ignores_accumulators_guards_and_computed_verdicts():
    assert _findings(R2_GOOD) == []


def test_r3_flags_score_literals_without_provenance():
    findings = [f for f in _findings(R3_BAD) if f.rule == "R3"]
    labels = sorted(f.message.split("'")[1] for f in findings)
    # assignment + two nested literals >= 0.8; the 0.0 entry is exempt
    assert len(findings) == 3
    assert "agreement_score" in labels
    assert "experimental_agreement.electrostatics" in labels
    assert "experimental_agreement.magnetostatics" in labels


def test_r3_ignores_provenanced_and_excluded_names():
    assert _findings(R3_GOOD) == []


def test_r4_flags_circular_cross_check():
    findings = [f for f in _findings(R4_BAD) if f.rule == "R4"]
    assert len(findings) == 1
    assert "lenz_method" in findings[0].message
    assert "energy_dissipation_method" in findings[0].message


def test_r4_ignores_round_trips_and_independent_routes():
    assert _findings(R4_GOOD_ROUNDTRIP) == []
    assert _findings(R4_GOOD_INDEPENDENT) == []


def test_r5_flags_identical_call_assertions():
    findings = _findings(R5_BAD)
    assert [f.rule for f in findings] == ["R5"]
    findings_approx = _findings(R5_BAD_APPROX)
    assert [f.rule for f in findings_approx] == ["R5"]


def test_r5_ignores_independent_expected_values():
    assert _findings(R5_GOOD) == []


def test_r6_flags_constant_return_stubs_under_maxwell_cite():
    findings = [f for f in _findings(R6_BAD) if f.rule == "R6"]
    assert len(findings) == 2
    names = " ".join(f.message for f in findings)
    assert "prove_real_rotation_required" in names
    assert "summarize_results" in names


def test_r6_ignores_computed_returns_and_numeric_tables():
    assert _findings(R6_GOOD) == []


def test_clean_canonical_code_produces_zero_findings():
    assert _findings(CLEAN_CANONICAL) == []


# ── R7-R10 fixtures (Stage-3 section 5.3 extension, G2 condition C4) ──

R7_BAD = '''
def calc_wave_speed(eps, mu):
    """Hardcoded speed-of-light and gravity literals."""
    c = 2.99792458e10
    g = 980.665
    return c * eps / mu, g
'''

R7_GOOD = '''
from maxwell.config.constants import CONST

def calc_wave_speed(eps, mu):
    """Constants referenced, not inlined."""
    return CONST.C * eps / mu


def historical_anchor():
    """Weber-Kohlrausch 1856 result: NOT in the speed-of-light family."""
    return {"v_cm_s": 3.107e10}
'''

R7_TESTS_PROVENANCED = """
def test_v_anchor():
    # provenance: Weber-Kohlrausch measurement quoted in Treatise Art. 775
    v = 3.0e10
    assert compute_v() > 0.5 * v
"""

R7_TESTS_UNPROVENANCED = """
def test_v_anchor_no_provenance():
    v = 3.0e10
    assert compute_v() > 0.5 * v
"""

R8_BAD = '''
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(781, part=4, chapter="Electromagnetic Theory of Light")
def calc_plane_wave():
    """Drifted chapter title (canonical: 'EM Theory of Light')."""
    return 2.0
'''

R8_GOOD = '''
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(781, part=4, chapter="EM Theory of Light")
def calc_plane_wave():
    """Exact canonical chapter title."""
    return 2.0


@maxwell_cite(768, part=4, chapter="Ch XIX: ESU vs EMU")
def calc_ratio():
    """Prefix form normalizes to the canonical title."""
    return 3.0
'''

R9_BAD = '''
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(700, 46, part=4)
def mixed_citation_unparked():
    """In-scope 700 mixed with out-of-scope 46, no parking comment."""
    return 2.0
'''

R9_GOOD_IN_SCOPE_ONLY = '''
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(700, 701, part=4)
def in_scope_only():
    """Pure last-200 citation: nothing to flag."""
    return 2.0
'''

R9_GOOD_BACKLOG_ONLY = '''
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(46, 47, part=1)
def backlog_only():
    """Known pre-LAST200 backlog file citing only < 667: exempt."""
    return 2.0
'''

R9_GOOD_PARKED = '''
from maxwell.meta.citation import maxwell_cite


# PARKING-LOT: art 46 (electrostatics) parked until Part I modernization
@maxwell_cite(700, 46, part=4)
def mixed_citation_parked():
    """Mixed citation with the explicit parking convention."""
    return 2.0
'''

R10_BAD = '''
import pytest


@pytest.mark.article(700)
def test_art700_structure_only():
    """Key-presence / isinstance / bare-bool asserts, no numbers."""
    result = analyze_instrument()
    assert "coil_constant" in result
    assert isinstance(result, dict)
    assert result["verified"]
    assert result["notes"] is not None
'''

R10_BAD_NO_ASSERTS = '''
import pytest


@pytest.mark.article(701)
def test_art701_smoke_only():
    """Calls the module but asserts nothing."""
    analyze_instrument()
'''

R10_GOOD = '''
import pytest


@pytest.mark.article(700)
def test_art700_numeric_approx():
    """Numeric golden via pytest.approx."""
    assert analyze_instrument()["coil_constant"] == pytest.approx(62.83, rel=1e-3)


@pytest.mark.article(701)
def test_art701_ordered_comparison():
    """Ordered comparison counts as numeric."""
    assert analyze_instrument()["error"] < 1e-6


@pytest.mark.article(702)
def test_art702_number_equality():
    """Equality against a numeric constant counts."""
    assert analyze_instrument()["turns"] == 100


@pytest.mark.quarantine
@pytest.mark.article(703)
def test_art703_quarantined():
    """Quarantine-marked: exempt from the numeric-assert requirement."""
    assert analyze_instrument()


@pytest.mark.article(704)
def test_art704_raises():
    """pytest.raises tests are exempt."""
    with pytest.raises(ValueError):
        analyze_instrument()


def test_not_article_marked():
    """No article mark: R10 does not apply."""
    assert analyze_instrument()
'''


def test_r7_flags_light_family_and_gravity_in_source():
    findings = _findings(R7_BAD)
    assert [f.rule for f in findings] == ["R7", "R7"]
    assert all(f.severity == lint.HIGH for f in findings)
    text = " ".join(f.message for f in findings)
    assert "speed-of-light" in text
    assert "gravity" in text


def test_r7_ignores_const_references_and_historical_anchors():
    assert _findings(R7_GOOD) == []


def test_r7_provenance_exempts_tests_tree_only():
    assert _findings(R7_TESTS_PROVENANCED, filename="tests/test_sample.py") == []
    findings = _findings(R7_TESTS_UNPROVENANCED, filename="tests/test_sample.py")
    assert len(findings) == 1
    assert findings[0].rule == "R7"
    assert findings[0].severity == lint.MEDIUM
    # the same unprovenanced code in maxwell/ is HIGH
    findings_src = _findings(R7_TESTS_UNPROVENANCED)
    assert findings_src[0].severity == lint.HIGH


def test_r8_flags_drifted_chapter_title():
    findings = _findings(R8_BAD)
    assert [f.rule for f in findings] == ["R8"]
    assert findings[0].severity == lint.MEDIUM
    assert "Electromagnetic Theory of Light" in findings[0].message


def test_r8_accepts_canonical_and_prefixed_titles():
    assert _findings(R8_GOOD) == []


def test_r9_flags_unparked_mixed_citation():
    findings = _findings(R9_BAD)
    assert [f.rule for f in findings] == ["R9"]
    assert findings[0].severity == lint.HIGH
    assert "46" in findings[0].message
    assert "700" in findings[0].message


def test_r9_ignores_pure_scope_and_parked_citations():
    assert _findings(R9_GOOD_IN_SCOPE_ONLY) == []
    assert _findings(R9_GOOD_BACKLOG_ONLY) == []
    assert _findings(R9_GOOD_PARKED) == []


def test_r10_flags_article_tests_without_numeric_asserts():
    findings = _findings(R10_BAD, filename="tests/test_sample.py")
    assert [f.rule for f in findings] == ["R10"]
    assert findings[0].severity == lint.HIGH
    assert "test_art700_structure_only" in findings[0].message
    findings_none = _findings(R10_BAD_NO_ASSERTS, filename="tests/test_sample.py")
    assert [f.rule for f in findings_none] == ["R10"]
    assert "no asserts" in findings_none[0].message


def test_r10_ignores_numeric_quarantined_and_unmarked_tests():
    assert _findings(R10_GOOD, filename="tests/test_sample.py") == []


def test_r10_skips_source_files():
    """R10 is a tests-tree rule: source modules are never scanned by it."""
    assert _findings(R10_BAD) == []


# ── contract, severity, filtering ─────────────────────────────────


def test_finding_to_dict_contract():
    findings = _findings(R1_BAD)
    assert findings, "planted R1 violation must be caught"
    payload = findings[0].to_dict()
    assert set(payload) == {"file", "line", "rule", "severity", "message", "snippet"}
    assert payload["line"] >= 1


def test_severity_downgraded_in_tests_tree():
    findings = _findings(R2_DICT_BAD, filename="tests/test_sample.py")
    assert findings and all(f.severity == lint.MEDIUM for f in findings)
    findings_r5 = _findings(R5_BAD, filename="tests/test_sample.py")
    assert any(f.rule == "R5" and f.severity == lint.HIGH for f in findings_r5)


def test_rules_filter_restricts_detectors():
    assert _findings(R6_BAD, rules=["R5"]) == []
    assert len(_findings(R6_BAD, rules=["R6"])) == 2
    both = _findings(R6_BAD, rules=["R1", "R6"])
    # R6 fires twice; R1 additionally flags the bare-bool prove_* stub.
    assert len([f for f in both if f.rule == "R6"]) == 2
    assert any(f.rule == "R1" for f in both)


# ── CLI behavior (subprocess) ─────────────────────────────────────


def _run_cli(args):
    return subprocess.run(
        [sys.executable, str(LINT_PATH), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(REPO_ROOT),
    )


def test_cli_exit_codes_and_json_output(tmp_path):
    bad = tmp_path / "maxwell" / "bad_verifier.py"
    bad.parent.mkdir(parents=True, exist_ok=True)
    bad.write_text(R1_BAD, encoding="utf-8")
    clean = tmp_path / "clean_module.py"
    clean.write_text("def calc_value(x):\n    return 2.0 * x\n", encoding="utf-8")

    proc_bad = _run_cli([str(bad), "--json"])
    assert proc_bad.returncode == 1, proc_bad.stdout + proc_bad.stderr
    # An empty stdout with rc=1 means the child crashed BEFORE printing the
    # JSON payload (e.g. an uncaught ValueError from os.path.relpath on
    # cross-drive paths -- the Windows GitHub Actions layout).  Surface the
    # child's stderr instead of a bare JSONDecodeError at char 0.
    assert proc_bad.stdout.strip(), (
        "lint CLI produced no stdout; child stderr tail: "
        f"{proc_bad.stderr[-2000:]!r}"
    )
    payload = json.loads(proc_bad.stdout)
    assert payload["high_findings"] >= 1
    assert payload["findings"][0]["rule"] == "R1"
    assert payload["summary"]["by_rule"]["R1"] >= 1

    proc_clean = _run_cli([str(clean)])
    assert proc_clean.returncode == 0, proc_clean.stdout + proc_clean.stderr

    # rule filter suppresses findings of other rules -> exit 0
    proc_filtered = _run_cli([str(bad), "--rules", "R5"])
    assert proc_filtered.returncode == 0, proc_filtered.stdout


def test_cli_unknown_rule_is_usage_error():
    proc = _run_cli(["--rules", "R11"])
    assert proc.returncode == 2
    assert "unknown rule" in proc.stderr.lower()


# ── full-repo smoke test (measurement baseline, not a green assert) ──


def test_full_repo_scan_completes_with_structured_results():
    """The scanner must run over the whole tree without crashing.

    Finding counts are deliberately NOT asserted: the baseline shrinks as
    concurrent remediation lands (see docs/LAST200_STAGE3_QUALITY_REVIEW.md
    defect register).  This test only guarantees the instrument works.
    """
    findings, files_scanned = lint.scan_paths(
        [str(REPO_ROOT / "maxwell"), str(REPO_ROOT / "tests")]
    )
    assert files_scanned > 100
    assert isinstance(findings, list)
    for finding in findings:
        assert finding.rule in lint.RULE_IDS
        assert finding.severity in (lint.HIGH, lint.MEDIUM)
        assert finding.file
        assert finding.line >= 1
        assert finding.message


# ── regression: cross-drive paths must not crash the scanner ──────


def test_scan_file_survives_cross_drive_relpath_failure(monkeypatch, tmp_path):
    """Regression for the Windows GitHub Actions layout.

    On the runner the checkout lives on ``D:\\a\\...`` while pytest's
    ``tmp_path`` lives on ``C:\\...``; ``os.path.relpath`` then raises
    ``ValueError: path is on mount 'C:', start on mount 'D:'``.  The scanner
    must degrade to absolute-path findings, never crash (which previously
    emptied the CLI's stdout and broke ``--json`` consumers).
    """
    bad = tmp_path / "maxwell" / "bad_verifier.py"
    bad.parent.mkdir(parents=True, exist_ok=True)
    bad.write_text(R1_BAD, encoding="utf-8")

    def exploding_relpath(path, start=None):
        raise ValueError("path is on mount 'C:', start on mount 'D:'")

    monkeypatch.setattr(os.path, "relpath", exploding_relpath)
    findings = lint.scan_file(str(bad))

    assert findings, "scan_file must still return findings on foreign mounts"
    assert all(f.rule == "R1" for f in findings)
    assert all(f.severity == lint.HIGH for f in findings)
    # Location must remain usable even when relpath is unavailable.
    assert all(f.file for f in findings)
    assert all(f.line >= 1 for f in findings)

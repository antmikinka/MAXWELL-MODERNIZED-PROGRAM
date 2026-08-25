"""
Pytest fixtures for Maxwell project testing.

Provides fixtures for:
- CGS unit tolerance testing
- Citation decorator validation
- Common test utilities
"""

from __future__ import annotations

from typing import Any, Callable

import numpy as np
import pytest

from maxwell.meta.citation import MaxwellCitation, get_citation

# ── CGS Unit Tolerances ────────────────────────────────────────────


@pytest.fixture
def cgs_tolerance() -> float:
    """Default tolerance for CGS numerical comparisons.

    CGS calculations often involve very small or very large numbers.
    This tolerance accounts for floating-point precision limits.

    Returns:
        Relative tolerance for numerical comparisons (1e-10).
    """
    return 1e-10


@pytest.fixture
def cgs_coarse_tolerance() -> float:
    """Coarse tolerance for derived CGS calculations.

    For calculations involving multiple steps or empirical formulas.

    Returns:
        Relative tolerance for coarse comparisons (1e-6).
    """
    return 1e-6


@pytest.fixture
def cgs_length_scale() -> float:
    """Characteristic length scale for CGS calculations (1 cm).

    Returns:
        Reference length in cm.
    """
    return 1.0


@pytest.fixture
def cgs_current_scale() -> float:
    """Characteristic current scale for CGS calculations (1 abampere).

    In CGS-EMU, 1 abampere = 10 amperes (SI).

    Returns:
        Reference current in abamperes.
    """
    return 1.0


@pytest.fixture
def cgs_distance_range() -> list[float]:
    """Range of distances for testing inverse-distance laws.

    Returns:
        List of distances in cm: [0.1, 0.5, 1.0, 2.0, 5.0, 10.0].
    """
    return [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]


# ── Citation Validation Fixtures ──────────────────────────────────


@pytest.fixture
def require_citation() -> Callable[[Callable], MaxwellCitation]:
    """Fixture that validates a function has a @maxwell_cite decorator.

    Usage:
        def test_something(require_citation):
            citation = require_citation(my_function)
            assert citation.part == 4

    Returns:
        Function that takes a callable and returns its citation.

    Raises:
        AssertionError: If function lacks citation decorator.
    """

    def _validate(func: Callable) -> MaxwellCitation:
        citation = get_citation(func)
        assert citation is not None, (
            f"Function {func.__module__}.{func.__qualname__} "
            f"must have @maxwell_cite decorator"
        )
        return citation

    return _validate


@pytest.fixture
def validate_citation_articles() -> Callable[[Callable, int, list[int]], None]:
    """Fixture that validates citation has correct article numbers.

    Usage:
        def test_oersted(validate_citation_articles):
            validate_citation_articles(
                calc_oersted_field,
                part=4,
                articles=[475, 476, 477]
            )

    Args:
        func: Function to validate.
        part: Expected Part number.
        articles: Expected article numbers.

    Raises:
        AssertionError: If citation doesn't match expected values.
    """

    def _validate(func: Callable, part: int, articles: list[int]) -> None:
        citation = get_citation(func)
        assert citation is not None, (
            f"Function {func.__module__}.{func.__qualname__} "
            f"must have @maxwell_cite decorator"
        )
        assert citation.part == part, f"Expected Part {part}, got Part {citation.part}"
        for art in articles:
            assert (
                art in citation.articles
            ), f"Article {art} not found in citation: {citation.articles}"

    return _validate


# ── Numerical Testing Utilities ───────────────────────────────────


@pytest.fixture
def assert_cgs_close() -> Callable[[float, float, float], None]:
    """Fixture for CGS-aware numerical assertions.

    Usage:
        def test_field(assert_cgs_close, cgs_tolerance):
            result = calc_oersted_field(1.0, 1.0)
            assert_cgs_close(result, 2.0, cgs_tolerance)

    Returns:
        Function that asserts two floats are close within tolerance.
    """

    def _assert_close(
        actual: float | np.ndarray,
        expected: float | np.ndarray,
        tolerance: float,
        msg: str | None = None,
    ) -> None:
        actual = np.asarray(actual)
        expected = np.asarray(expected)
        diff = np.abs(actual - expected)
        scale = np.maximum(np.abs(actual), np.abs(expected))
        scale = np.maximum(scale, 1.0)
        rel_err = diff / scale
        if not np.all(rel_err < tolerance) and not np.all(diff < tolerance * 1e-6):
            raise AssertionError(
                f"{msg or ''} Expected {expected}, got {actual} "
                f"(relative error: {rel_err:.2e}, tolerance: {tolerance})"
            )

    return _assert_close


@pytest.fixture
def assert_vectors_close() -> Callable[[np.ndarray, np.ndarray, float], None]:
    """Fixture for CGS vector assertions.

    Usage:
        def test_direction(assert_vectors_close, cgs_tolerance):
            result = calc_circular_field_direction(1.0, [1, 0, 0])
            assert_vectors_close(result, [0, 1, 0], cgs_tolerance)

    Returns:
        Function that asserts two vectors are close within tolerance.
    """

    def _assert_close(
        actual: np.ndarray, expected: np.ndarray, tolerance: float
    ) -> None:
        actual = np.asarray(actual)
        expected = np.asarray(expected)
        assert (
            actual.shape == expected.shape
        ), f"Shape mismatch: {actual.shape} vs {expected.shape}"
        diff = np.linalg.norm(actual - expected)
        expected_mag = np.linalg.norm(expected)
        if expected_mag == 0:
            assert diff < tolerance, f"Expected zero vector, got norm={diff}"
        else:
            relative_error = diff / expected_mag
            assert relative_error < tolerance, (
                f"Vector mismatch: expected {expected}, got {actual} "
                f"(relative error: {relative_error:.2e})"
            )

    return _assert_close


# ── Common Test Data ──────────────────────────────────────────────


@pytest.fixture
def sample_point_charge() -> Any:
    """Create a sample point charge for testing.

    Returns:
        PointCharge object with q=1 esu at origin.
    """
    from maxwell.core.charge import PointCharge

    return PointCharge(q=1.0, position=np.array([0.0, 0.0, 0.0]))


@pytest.fixture
def sample_test_positions() -> list[np.ndarray]:
    """Standard test positions for field calculations.

    Returns:
        List of position vectors for testing.
    """
    return [
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([0.0, 0.0, 1.0]),
        np.array([1.0, 1.0, 0.0]),
        np.array([1.0, 1.0, 1.0]),
    ]


# ── Article-evidence plugin (LAST200 Stage 4 §2.1-2.2) ─────────────
#
# Registers the article/regression/quarantine markers, validates every
# ``@pytest.mark.article`` usage at collection time, builds the
# article -> [test nodeid] evidence map, and emits the G3 evidence artifact
# to ``docs/reports/article_evidence_report.json``.
#
# Adapted from docs/LAST200_STAGE4_TESTING_STRATEGY.md §2.2. Deviations:
#   * Installed in the root ``tests/conftest.py`` (the ``tests/articles/``
#     tree does not exist yet), so the plugin covers the whole suite.
#   * Validation errors are collected across all items and reported in a
#     single failure (rather than raising on the first offender).
#   * The report path is anchored to this file's location instead of the
#     process CWD so the artifact lands in the project tree regardless of
#     where pytest is invoked.

import json
import pathlib
import sys
from datetime import datetime, timezone

# LAST200 scope fence (R13): articles 667-866.
_ARTICLE_RANGE = range(667, 867)
_ARTICLE_MIN, _ARTICLE_MAX = 1, 866
_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_ARTICLE_REPORT = _PROJECT_ROOT / "docs" / "reports" / "article_evidence_report.json"
# G3-R6: partial (subset) runs write here and NEVER touch the canonical
# report, so a `-k foo` or single-file run cannot clobber the full-run
# gate_G3 verdict (mechanism documented in G3_GATE_REVIEW §7.3).
_ARTICLE_REPORT_PARTIAL = (
    _PROJECT_ROOT / "docs" / "reports" / "article_evidence_report_partial.json"
)
_TESTS_ROOT = pathlib.Path(__file__).resolve().parent


def _invocation_info(config) -> dict[str, Any]:
    """Record how pytest was invoked, embedded in the emitted artifact.

    G3 recommendation R6: an artifact must carry its own provenance so a
    stale or partial report can never be mistaken for a full-run verdict.
    """
    return {
        "argv": list(sys.argv),
        "args": list(getattr(config, "args", []) or []),
        "keyword": getattr(config.option, "keyword", None) or None,
        "markexpr": getattr(config.option, "markexpr", None) or None,
        "cwd": str(pathlib.Path.cwd()),
    }


def _is_partial_collection(config) -> bool:
    """Detect subset/deselected runs that must not write the canonical report.

    A run is partial when any pytest feature selects a SUBSET of the
    suite: ``-k``/``--keyword``, ``-m``/``--markexpr``, cache-based
    selection (``--lf``/``--nf``), ``--ignore``/``--deselect``, explicit
    node-id arguments (containing ``::``), or path arguments that do not
    resolve to the whole tests tree.  Bare invocations (no args, with
    ``testpaths = ["tests"]``) and invocations pointing at the entire
    tests directory collect the full universe and are full runs.

    Deliberately NOT based on the size of the collected article map: a
    genuine full run that has lost an article's qualifying tests is
    exactly the regression the canonical ``gate_G3: FAIL`` must expose.
    """
    opts = config.option
    if getattr(opts, "keyword", None):
        return True
    if getattr(opts, "markexpr", None):
        return True
    if getattr(opts, "ignore", None):
        return True
    if getattr(opts, "deselect", None):
        return True
    # cacheprovider selections (--lf/--nf; builtin plugin, so present
    # even under PYTEST_DISABLE_PLUGIN_AUTOLOAD — getattr guards either way)
    for flag in ("lf", "last_failed", "nf", "new_first", "ff", "failed_first"):
        if getattr(opts, flag, False):
            return True
    base = pathlib.Path.cwd()
    inv_dir = getattr(getattr(config, "invocation_params", None), "dir", None)
    if inv_dir is not None:
        base = pathlib.Path(inv_dir)
    for arg in list(getattr(config, "args", []) or []):
        if "::" in arg:
            return True  # node-id selection is always a subset
        p = pathlib.Path(arg)
        if not p.is_absolute():
            p = base / p
        try:
            p = p.resolve()
        except OSError:
            return True
        if p != _TESTS_ROOT:
            return True
    return False


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "article(N): test provides evidence for Treatise article N (int, 1-866)",
    )
    config.addinivalue_line(
        "markers",
        "regression(defect): failing-before/passing-after test for a defect register ID",
    )
    config.addinivalue_line(
        "markers",
        "quarantine: enshrines unadjudicated content; excluded from the G3 count",
    )
    # article number -> list of test nodeids (populated during collection)
    config._article_map = {}


def pytest_collection_modifyitems(config, items):
    amap = config._article_map
    errors = []
    for item in items:
        for mark in item.iter_markers(name="article"):
            if not mark.args:
                errors.append(
                    f"{item.nodeid}: article marker needs an article number N"
                )
                continue
            n = mark.args[0]
            if (
                isinstance(n, bool)
                or not isinstance(n, int)
                or not (_ARTICLE_MIN <= n <= _ARTICLE_MAX)
            ):
                errors.append(
                    f"{item.nodeid}: bad article number {n!r} (must be an int in 1..866)"
                )
                continue
            if n in _ARTICLE_RANGE and "quarantine" not in [
                m.name for m in item.iter_markers()
            ]:
                amap.setdefault(n, []).append(item.nodeid)
    if errors:
        # Collected across all items above, then raised once (Stage 4 §2.2
        # raises pytest.UsageError at collection; pytest.fail here surfaces as
        # an INTERNALERROR, so UsageError is used for a clean hard failure).
        raise pytest.UsageError(
            "Invalid @pytest.mark.article usage detected:\n  " + "\n  ".join(errors)
        )


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Emit the article -> test evidence map (G3 evidence artifact).

    G3-R6 guard (2026-08-22): a SUBSET run (``-k``, ``-m``, ``--lf``,
    explicit paths/node-ids, ...) must never overwrite the canonical
    ``gate_G3`` verdict with its inherently incomplete coverage.  Partial
    runs write a distinctly-named artifact
    (``article_evidence_report_partial.json``) carrying ``"partial": true``
    and full invocation provenance; the canonical file is written ONLY by
    full-suite runs, preserving the pre-R6 format exactly (plus the
    additive ``"partial": false`` and ``"invocation"`` keys).
    """
    # Never clobber a good report on an aborted session (usage/collection
    # errors, internal crashes) — the map would be empty or partial.
    if exitstatus in (pytest.ExitCode.USAGE_ERROR, pytest.ExitCode.INTERNAL_ERROR):
        return
    amap = getattr(config, "_article_map", {})
    missing = [n for n in _ARTICLE_RANGE if n not in amap]
    total_marked = sum(len(v) for v in amap.values())
    tr = terminalreporter
    if _is_partial_collection(config):
        # Partial run: side artifact only, canonical gate_G3 untouched.
        report = {
            "partial": True,
            "gate_G3": "NOT_EVALUATED_PARTIAL_RUN",
            "range": [_ARTICLE_RANGE[0], _ARTICLE_RANGE[-1]],
            "generated": datetime.now(timezone.utc).isoformat(),
            "articles_covered": len(amap),
            "total_marked_tests": total_marked,
            "articles_missing": missing,
            "invocation": _invocation_info(config),
            "evidence": {str(n): amap[n] for n in sorted(amap)},
        }
        _ARTICLE_REPORT_PARTIAL.parent.mkdir(parents=True, exist_ok=True)
        _ARTICLE_REPORT_PARTIAL.write_text(json.dumps(report, indent=1))
        tr.write_sep("=", "ARTICLE EVIDENCE MAP (667-866) — PARTIAL RUN")
        tr.write_line(
            f"covered {len(amap)}/200  missing {len(missing)}  "
            f"marked tests {total_marked}"
        )
        tr.write_line(
            "partial run: wrote "
            f"{_ARTICLE_REPORT_PARTIAL.name}; canonical "
            f"{_ARTICLE_REPORT.name} left untouched (gate_G3 not evaluated)"
        )
        return
    report = {
        "range": [_ARTICLE_RANGE[0], _ARTICLE_RANGE[-1]],
        "generated": datetime.now(timezone.utc).isoformat(),
        "articles_covered": len(amap),
        "total_marked_tests": total_marked,
        "articles_missing": missing,
        "gate_G3": "PASS" if not missing else "FAIL",
        "evidence": {str(n): amap[n] for n in sorted(amap)},
        "partial": False,
        "invocation": _invocation_info(config),
    }
    _ARTICLE_REPORT.parent.mkdir(parents=True, exist_ok=True)
    _ARTICLE_REPORT.write_text(json.dumps(report, indent=1))
    tr.write_sep("=", "ARTICLE EVIDENCE MAP (667-866)")
    tr.write_line(
        f"covered {len(amap)}/200  missing {len(missing)}  marked tests {total_marked}"
    )
    if missing:
        tr.write_line(
            "missing: "
            + " ".join(map(str, missing[:50]))
            + (" ..." if len(missing) > 50 else "")
        )

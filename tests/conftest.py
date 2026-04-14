"""
Pytest fixtures for Maxwell project testing.

Provides fixtures for:
- CGS unit tolerance testing
- Citation decorator validation
- Common test utilities
"""

from __future__ import annotations
import pytest
import numpy as np
from typing import Any, Callable
from maxwell.meta.citation import get_citation, MaxwellCitation


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
        assert citation.part == part, (
            f"Expected Part {part}, got Part {citation.part}"
        )
        for art in articles:
            assert art in citation.articles, (
                f"Article {art} not found in citation: {citation.articles}"
            )
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
        msg: str | None = None
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
        actual: np.ndarray,
        expected: np.ndarray,
        tolerance: float
    ) -> None:
        actual = np.asarray(actual)
        expected = np.asarray(expected)
        assert actual.shape == expected.shape, (
            f"Shape mismatch: {actual.shape} vs {expected.shape}"
        )
        diff = np.linalg.norm(actual - expected)
        expected_mag = np.linalg.norm(expected)
        if expected_mag == 0:
            assert diff < tolerance, (
                f"Expected zero vector, got norm={diff}"
            )
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

"""maxwell.verification.convergence -- Convergence rate testing.

Measures how numerical errors decrease as resolution increases,
verifying that implementations converge to analytical solutions.
"""

from __future__ import annotations

from typing import Callable

import numpy as np

from maxwell.verification.framework import VerificationResult


def measure_spherical_harmonic_convergence(
    l_max_sequence: tuple[int, ...] = (1, 2, 4, 8, 16),
    n_grid_points: int = 100,
) -> dict:
    """Measure convergence rate of spherical harmonic expansion.

    Tests that the expansion of f(theta) = cos(theta) converges
    to the known solution with increasing l_max.

    Args:
        l_max_sequence: Sequence of max_l values to test.
        n_grid_points: Grid points for coefficient computation.

    Returns:
        Dictionary with convergence data including error at each l_max
        and measured convergence rate.
    """
    from maxwell.math.spherical_harmonics import SphericalHarmonicExpansion

    def f_theta(theta):
        return np.cos(theta)

    errors = []
    test_theta = np.pi / 3
    expected = float(np.cos(test_theta))

    for l_max in l_max_sequence:
        expansion = SphericalHarmonicExpansion(max_l=l_max)
        expansion.expand_axisymmetric(f_theta, n_theta=n_grid_points)
        approx = expansion.reconstruct(test_theta, 0)
        # Handle both complex scalar and numpy array returns
        if isinstance(approx, np.ndarray):
            approx_val = float(approx.real.item())
        else:
            approx_val = float(np.real(complex(approx)))
        error = abs(approx_val - expected)
        errors.append({"l_max": l_max, "error": float(error)})

    # Compute convergence rate from last two points
    if len(errors) >= 2 and errors[-1]["error"] > 1e-15 and errors[-2]["error"] > 1e-15:
        log_ratio = np.log(errors[-1]["error"] / errors[-2]["error"])
        l_ratio = np.log(l_max_sequence[-1] / l_max_sequence[-2])
        rate = float(log_ratio / l_ratio) if l_ratio != 0 else float("inf")
    else:
        rate = float("inf")  # Already converged to machine precision

    return {
        "function": "cos(theta)",
        "test_point": float(test_theta),
        "expected": expected,
        "convergence_data": errors,
        "convergence_rate": rate,
        "final_error": errors[-1]["error"] if errors else float("inf"),
    }


def measure_grid_convergence(
    field_func: Callable[[np.ndarray], np.ndarray],
    reference_value: float,
    name: str = "grid_convergence",
    grid_sequence: tuple[int, ...] = (10, 20, 40, 80),
) -> dict:
    """Measure error decrease with grid resolution for numerical integration.

    Args:
        field_func: Function that takes n_points and returns a scalar value
                    (e.g., numerical integral result).
        reference_value: Known analytical result to compare against.
        name: Human-readable test name.
        grid_sequence: Sequence of grid sizes to test.

    Returns:
        Dictionary with error at each grid size and convergence rate.
    """
    errors = []

    for n in grid_sequence:
        value = field_func(n)
        ref = abs(reference_value) if reference_value != 0 else 1.0
        error = abs(value - reference_value) / ref
        errors.append({"n": n, "value": float(value), "relative_error": float(error)})

    # Compute convergence rate
    if (
        len(errors) >= 2
        and errors[-1]["relative_error"] > 1e-15
        and errors[-2]["relative_error"] > 1e-15
    ):
        log_ratio = np.log(errors[-1]["relative_error"] / errors[-2]["relative_error"])
        n_ratio = np.log(grid_sequence[-1] / grid_sequence[-2])
        rate = float(log_ratio / n_ratio) if n_ratio != 0 else float("inf")
    else:
        rate = float("inf")

    return {
        "name": name,
        "reference_value": reference_value,
        "convergence_data": errors,
        "convergence_rate": rate,
        "final_error": errors[-1]["relative_error"] if errors else float("inf"),
    }


def verify_convergence_results(
    convergence_data: dict, max_error: float = 0.01
) -> VerificationResult:
    """Wrap convergence test results into a VerificationResult.

    Args:
        convergence_data: Output from test_spherical_harmonic_convergence or
                          test_grid_convergence.
        max_error: Maximum acceptable final relative error.

    Returns:
        VerificationResult indicating pass/fail.
    """
    final_error = convergence_data.get("final_error", float("inf"))
    passed = final_error <= max_error

    return VerificationResult(
        module_name="maxwell.verification.convergence",
        article_refs=(),
        test_name=f"Convergence: {convergence_data.get('name', 'spherical_harmonic')}",
        expected=0.0,
        actual=float(final_error),
        relative_error=float(final_error),
        tolerance=max_error,
        passed=passed,
        details=f"Rate: {convergence_data.get('convergence_rate', 'N/A'):.2f}, "
        f"Final error: {final_error:.2e}",
    )

"""maxwell.electromagnetism.fields.curl_relation — Curl relations (Arts. 590-592).

Implements Maxwell's verification that the magnetic field is the curl of
the vector potential, and related field identities.

Maxwell's CGS formulation (Arts. 590-592):
    The fundamental curl relations are:

        B = curl(A)           (magnetic field from vector potential)
        H = curl(A)           (in CGS-EMU, B = H since mu_0 = 1)
        curl(E) = -dB/dt      (Faraday's law in differential form)
        div(B) = 0            (no magnetic monopoles)

    The identity curl(grad(phi)) = 0 ensures gauge invariance:
        A' = A + grad(chi) gives the same B field.

    The identity div(curl(A)) = 0 ensures div(B) = 0 automatically.

where:
    A = vector potential (gauss*cm)
    B = magnetic field (gauss)
    E = electric field (statvolts/cm)
    phi = scalar potential (statvolts)

Category: A (maxwell_original) — Maxwell's curl relation theory.

References:
    Part IV, Arts. 590-592: Curl relations and field identities.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


def _numerical_curl(F_func: callable, position: np.ndarray, delta: float) -> np.ndarray:
    """Calculate numerical curl of vector field F.

    curl F = [dFz/dy - dFy/dz, dFx/dz - dFz/dx, dFy/dx - dFx/dy]
    """
    curl = np.zeros(3)

    # curl_x = dFz/dy - dFy/dz
    Fz_y_plus = F_func(position + np.array([0, delta, 0]))[2]
    Fz_y_minus = F_func(position - np.array([0, delta, 0]))[2]
    dFz_dy = (Fz_y_plus - Fz_y_minus) / (2 * delta)

    Fy_z_plus = F_func(position + np.array([0, 0, delta]))[1]
    Fy_z_minus = F_func(position - np.array([0, 0, delta]))[1]
    dFy_dz = (Fy_z_plus - Fy_z_minus) / (2 * delta)

    curl[0] = dFz_dy - dFy_dz

    # curl_y = dFx/dz - dFz/dx
    Fx_z_plus = F_func(position + np.array([0, 0, delta]))[0]
    Fx_z_minus = F_func(position - np.array([0, 0, delta]))[0]
    dFx_dz = (Fx_z_plus - Fx_z_minus) / (2 * delta)

    Fz_x_plus = F_func(position + np.array([delta, 0, 0]))[2]
    Fz_x_minus = F_func(position - np.array([delta, 0, 0]))[2]
    dFz_dx = (Fz_x_plus - Fz_x_minus) / (2 * delta)

    curl[1] = dFx_dz - dFz_dx

    # curl_z = dFy/dx - dFx/dy
    Fy_x_plus = F_func(position + np.array([delta, 0, 0]))[1]
    Fy_x_minus = F_func(position - np.array([delta, 0, 0]))[1]
    dFy_dx = (Fy_x_plus - Fy_x_minus) / (2 * delta)

    Fx_y_plus = F_func(position + np.array([0, delta, 0]))[0]
    Fx_y_minus = F_func(position - np.array([0, delta, 0]))[0]
    dFx_dy = (Fx_y_plus - Fx_y_minus) / (2 * delta)

    curl[2] = dFy_dx - dFx_dy

    return curl


def _numerical_divergence(F_func: callable, position: np.ndarray, delta: float) -> float:
    """Calculate numerical divergence of vector field F.

    div F = dFx/dx + dFy/dy + dFz/dz
    """
    div = 0.0

    for i in range(3):
        pos_plus = position.copy()
        pos_plus[i] += delta
        pos_minus = position.copy()
        pos_minus[i] -= delta

        dF_i = (F_func(pos_plus)[i] - F_func(pos_minus)[i]) / (2 * delta)
        div += dF_i

    return div


def _numerical_gradient(f_func: callable, position: np.ndarray, delta: float) -> np.ndarray:
    """Calculate numerical gradient of scalar field f."""
    grad = np.zeros(3)

    for i in range(3):
        pos_plus = position.copy()
        pos_plus[i] += delta
        pos_minus = position.copy()
        pos_minus[i] -= delta

        grad[i] = (f_func(pos_plus) - f_func(pos_minus)) / (2 * delta)

    return grad


@dataclass
class CurlRelations:
    """
    Curl relation calculator for electromagnetic fields.

    Art. 590-592: These relations connect the vector potential A
    to the physical fields B and E through differential operators.

    Key identities:
    - curl(grad(phi)) = 0 (gauge invariance)
    - div(curl(A)) = 0 (no magnetic monopoles)
    - curl(curl(A)) = grad(div(A)) - laplacian(A)

    Attributes:
        A_function: Function returning A at position.
        delta: Finite difference step for numerical derivatives.
    """

    A_function: callable = None
    delta: float = 1e-6

    @maxwell_cite(
        590, 591,
        part=4, chapter="Curl Relations",
        theory_class="maxwell_original",
        description="Calculate B = curl(A)",
    )
    def magnetic_field(self, position: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic field from curl of vector potential.

        Art. 590-591: B = curl(A)

        Args:
            position: Position (cm).

        Returns:
            Magnetic field B (gauss).
        """
        if self.A_function is None:
            return np.zeros(3)
        return _numerical_curl(self.A_function, np.asarray(position, dtype=np.float64), self.delta)

    @maxwell_cite(
        590,
        part=4, chapter="Curl Relations",
        theory_class="maxwell_original",
        description="Verify div(B) = 0",
    )
    def verify_divergence_free(self, position: np.ndarray) -> dict[str, float | bool]:
        """
        Verify that B = curl(A) is divergence-free.

        Art. 590: The identity div(curl(A)) = 0 guarantees that
        there are no magnetic monopoles.

        Args:
            position: Position (cm).

        Returns:
            Dictionary with divergence verification results.
        """
        position = np.asarray(position, dtype=np.float64)

        if self.A_function is None:
            return {"divergence": 0.0, "verified": True}

        def B_func(r):
            return _numerical_curl(self.A_function, r, self.delta)

        div_B = _numerical_divergence(B_func, position, self.delta)

        return {
            "position": position,
            "divergence": div_B,
            "verified": bool(abs(div_B) < 1e-4),
        }


@maxwell_cite(
    590, 591,
    part=4, chapter="Curl Relations",
    theory_class="maxwell_original",
    description="Verify B = curl(A) relation",
)
def verify_curl_relation(
    A_function: callable,
    B_expected: callable,
    test_positions: list[np.ndarray] = None,
    tolerance: float = 1e-5,
) -> dict[str, float | bool | list]:
    """
    Verify that B = curl(A) at test positions.

    Art. 590-591: This function computes curl(A) numerically and
    compares it with the expected B field.

    Args:
        A_function: Function returning A at position.
        B_expected: Function returning expected B at position.
        test_positions: Positions to test (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if test_positions is None:
        test_positions = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([1.0, 1.0, 0.0]),
            np.array([0.5, 0.5, 0.5]),
        ]

    errors = []
    results = []

    for pos in test_positions:
        pos = np.asarray(pos, dtype=np.float64)

        B_calc = _numerical_curl(A_function, pos, 1e-6)
        B_exp = np.asarray(B_expected(pos), dtype=np.float64)

        error = np.linalg.norm(B_calc - B_exp)
        B_mag = np.linalg.norm(B_exp)
        rel_error = error / B_mag if B_mag > 1e-15 else error

        errors.append(rel_error)
        results.append({
            "position": pos,
            "B_calculated": B_calc,
            "B_expected": B_exp,
            "relative_error": rel_error,
        })

    max_error = max(errors) if errors else 0

    return {
        "test_positions": test_positions,
        "max_relative_error": max_error,
        "errors": errors,
        "results": results,
        "verified": bool(max_error < tolerance),
    }


@maxwell_cite(
    590,
    part=4, chapter="Curl Relations",
    theory_class="maxwell_original",
    description="Verify curl(grad(phi)) = 0",
)
def verify_curl_gradient_identity(
    phi_function: callable = None,
    test_positions: list[np.ndarray] = None,
    tolerance: float = 1e-5,
) -> dict[str, float | bool]:
    """
    Verify that curl of gradient is zero.

    Art. 590: The identity curl(grad(phi)) = 0 is fundamental to
    gauge invariance. Adding grad(chi) to A does not change B.

    Args:
        phi_function: Scalar potential function phi(r).
        test_positions: Positions to test.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with identity verification results.
    """
    if phi_function is None:
        # Default: phi = x^2 + y^2 + z^2
        def phi_function(r):
            return r[0] ** 2 + r[1] ** 2 + r[2] ** 2

    if test_positions is None:
        test_positions = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([1.0, 1.0, 1.0]),
        ]

    max_norm = 0.0

    for pos in test_positions:
        pos = np.asarray(pos, dtype=np.float64)
        grad_phi = _numerical_gradient(phi_function, pos, 1e-6)

        def grad_func(r):
            return _numerical_gradient(phi_function, r, 1e-6)

        curl_grad = _numerical_curl(grad_func, pos, 1e-4)
        norm = np.linalg.norm(curl_grad)
        max_norm = max(max_norm, norm)

    return {
        "max_curl_grad_norm": max_norm,
        "test_positions": test_positions,
        "identity_verified": bool(max_norm < tolerance),
    }


@maxwell_cite(
    591, 592,
    part=4, chapter="Curl Relations",
    theory_class="maxwell_original",
    description="Verify div(B) = 0 for vector potential",
)
def verify_divergence_free_B(
    A_function: callable,
    test_positions: list[np.ndarray] = None,
    tolerance: float = 1e-4,
) -> dict[str, float | bool]:
    """
    Verify that B = curl(A) is divergence-free.

    Art. 591-592: The identity div(curl(A)) = 0 is a mathematical
    identity that guarantees no magnetic monopoles exist.

    Args:
        A_function: Function returning A at position.
        test_positions: Positions to test.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with divergence-free verification results.
    """
    if test_positions is None:
        test_positions = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([1.0, 1.0, 0.0]),
        ]

    max_div = 0.0

    for pos in test_positions:
        pos = np.asarray(pos, dtype=np.float64)

        def B_func(r):
            return _numerical_curl(A_function, r, 1e-6)

        div_B = _numerical_divergence(B_func, pos, 1e-4)
        max_div = max(max_div, abs(div_B))

    return {
        "max_divergence": max_div,
        "test_positions": test_positions,
        "divergence_free": bool(max_div < tolerance),
    }


@maxwell_cite(
    590, 591, 592,
    part=4, chapter="Curl Relations",
    theory_class="maxwell_original",
    description="Calculate curl of vector field",
)
def calc_curl(
    F_function: callable,
    position: np.ndarray,
    delta: float = 1e-6,
) -> np.ndarray:
    """
    Calculate curl of a vector field at a position.

    Art. 590-592: The curl operator measures the circulation density
    of a vector field.

    Args:
        F_function: Vector field function F(r).
        position: Position (cm).
        delta: Finite difference step.

    Returns:
        curl F at position.
    """
    position = np.asarray(position, dtype=np.float64)
    return _numerical_curl(F_function, position, delta)


@maxwell_cite(
    590, 591,
    part=4, chapter="Curl Relations",
    theory_class="maxwell_original",
    description="Calculate divergence of vector field",
)
def calc_divergence(
    F_function: callable,
    position: np.ndarray,
    delta: float = 1e-6,
) -> float:
    """
    Calculate divergence of a vector field at a position.

    Art. 590-591: The divergence operator measures the source/sink
    strength of a vector field.

    Args:
        F_function: Vector field function F(r).
        position: Position (cm).
        delta: Finite difference step.

    Returns:
        div F at position.
    """
    position = np.asarray(position, dtype=np.float64)
    return _numerical_divergence(F_function, position, delta)


@maxwell_cite(
    591, 592,
    part=4, chapter="Curl Relations",
    theory_class="maxwell_original",
    description="Verify gauge invariance of B field",
)
def verify_gauge_invariance(
    A_function: callable,
    chi_function: callable,
    test_positions: list[np.ndarray] = None,
    tolerance: float = 1e-5,
) -> dict[str, float | bool]:
    """
    Verify that B is invariant under gauge transformation.

    Art. 591-592: Under the gauge transformation:

        A' = A + grad(chi)

    the magnetic field B = curl(A') = curl(A) since curl(grad(chi)) = 0.

    Args:
        A_function: Original vector potential.
        chi_function: Gauge function chi(r).
        test_positions: Positions to test.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with gauge invariance verification results.
    """
    if test_positions is None:
        test_positions = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([1.0, 1.0, 0.0]),
        ]

    def A_prime(r):
        grad_chi = _numerical_gradient(chi_function, r, 1e-6)
        return np.asarray(A_function(r), dtype=np.float64) + grad_chi

    max_diff = 0.0

    for pos in test_positions:
        pos = np.asarray(pos, dtype=np.float64)

        B_original = _numerical_curl(A_function, pos, 1e-6)
        B_transformed = _numerical_curl(A_prime, pos, 1e-6)

        diff = np.linalg.norm(B_transformed - B_original)
        B_mag = np.linalg.norm(B_original)
        rel_diff = diff / B_mag if B_mag > 1e-15 else diff

        max_diff = max(max_diff, rel_diff)

    return {
        "max_relative_difference": max_diff,
        "test_positions": test_positions,
        "gauge_invariant": bool(max_diff < tolerance),
    }


@maxwell_cite(
    590, 591, 592,
    part=4, chapter="Curl Relations",
    theory_class="maxwell_original",
    description="Complete curl relation analysis",
)
def analyze_curl_relations(
    A_function: callable,
    B_function: callable = None,
    test_positions: list[np.ndarray] = None,
) -> dict[str, float | np.ndarray | list]:
    """
    Complete analysis of curl relations.

    Art. 590-592: Comprehensive analysis including:
    1. B = curl(A) verification
    2. div(B) = 0 verification
    3. Curl values at test positions

    Args:
        A_function: Vector potential function A(r).
        B_function: Expected B field function (for comparison).
        test_positions: Positions for evaluation.

    Returns:
        Dictionary with complete analysis results.
    """
    if test_positions is None:
        test_positions = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([1.0, 1.0, 0.0]),
            np.array([0.5, 0.5, 0.5]),
        ]

    results = {
        "test_positions": test_positions,
    }

    curl_values = []
    div_values = []

    for pos in test_positions:
        pos = np.asarray(pos, dtype=np.float64)

        curl_A = _numerical_curl(A_function, pos, 1e-6)
        curl_values.append(curl_A)

        def B_func(r):
            return _numerical_curl(A_function, r, 1e-6)

        div_B = _numerical_divergence(B_func, pos, 1e-4)
        div_values.append(div_B)

    results["curl_values"] = curl_values
    results["divergence_values"] = div_values

    # Verify B = curl(A) if B_function provided
    if B_function is not None:
        errors = []
        for pos in test_positions:
            pos = np.asarray(pos, dtype=np.float64)
            B_calc = _numerical_curl(A_function, pos, 1e-6)
            B_exp = np.asarray(B_function(pos), dtype=np.float64)
            error = np.linalg.norm(B_calc - B_exp)
            B_mag = np.linalg.norm(B_exp)
            rel_error = error / B_mag if B_mag > 1e-15 else error
            errors.append(rel_error)

        results["max_relative_error"] = max(errors)
        results["curl_verified"] = bool(max(errors) < 1e-5)

    # Verify div(B) = 0
    max_div = max(abs(d) for d in div_values)
    results["max_divergence"] = max_div
    results["divergence_free"] = bool(max_div < 1e-4)

    return results

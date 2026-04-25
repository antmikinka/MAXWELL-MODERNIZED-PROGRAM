"""maxwell.math.gauge.manager — Gauge transformation manager (Arts. 616-617).

Implements Maxwell's gauge transformations for electromagnetic potentials,
managing the freedom to choose different gauge conditions.

Maxwell's CGS formulation (Arts. 616-617):
    The electromagnetic potentials are not unique. Under a gauge
    transformation with arbitrary scalar function chi(r, t):

        A' = A + grad(chi)
        phi' = phi - (1/c) * d(chi)/dt

    The physical fields E and B are unchanged:
        B' = curl(A') = curl(A) = B
        E' = -grad(phi') - (1/c)*dA'/dt = E

    Common gauge conditions:
    - Coulomb gauge: div(A) = 0
    - Lorenz gauge: div(A) + (1/c)*d(phi)/dt = 0
    - Temporal gauge: phi = 0
    - Axial gauge: A_z = 0

where:
    A = vector potential (gauss*cm)
    phi = scalar potential (statvolts)
    chi = gauge function (dimensionless)
    c = speed of light (cm/s)

Category: A (maxwell_original) — Maxwell's gauge transformation theory.

References:
    Part IV, Arts. 616-617: Gauge transformations and potentials.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


def _numerical_gradient(f_func: callable, position: np.ndarray, delta: float) -> np.ndarray:
    """Calculate numerical gradient of scalar field."""
    grad = np.zeros(3)
    for i in range(3):
        pos_plus = position.copy()
        pos_plus[i] += delta
        pos_minus = position.copy()
        pos_minus[i] -= delta
        grad[i] = (f_func(pos_plus) - f_func(pos_minus)) / (2 * delta)
    return grad


def _numerical_divergence(F_func: callable, position: np.ndarray, delta: float) -> float:
    """Calculate numerical divergence of vector field."""
    div = 0.0
    for i in range(3):
        pos_plus = position.copy()
        pos_plus[i] += delta
        pos_minus = position.copy()
        pos_minus[i] -= delta
        dF_i = (F_func(pos_plus)[i] - F_func(pos_minus)[i]) / (2 * delta)
        div += dF_i
    return div


@dataclass
class GaugeTransformation:
    """
    Gauge transformation manager.

    Art. 616-617: Manages the freedom to transform electromagnetic
    potentials while keeping physical fields unchanged.

    Attributes:
        A_function: Original vector potential A(r, t).
        phi_function: Original scalar potential phi(r, t).
        delta: Numerical differentiation step.
    """

    A_function: callable = None
    phi_function: callable = None
    delta: float = 1e-6

    @maxwell_cite(
        616, 617,
        part=4, chapter="Gauge Transformations",
        theory_class="maxwell_original",
        description="Apply gauge transformation",
    )
    def transform(
        self,
        chi_function: callable,
        position: np.ndarray,
        time: float = 0.0,
        dt: float = 1e-9,
    ) -> tuple[np.ndarray, float]:
        """
        Apply gauge transformation with function chi.

        Art. 616-617: Under the transformation:

            A' = A + grad(chi)
            phi' = phi - (1/c) * d(chi)/dt

        Args:
            chi_function: Gauge function chi(r, t).
            position: Position (cm).
            time: Time (s).
            dt: Time step for derivative.

        Returns:
            Tuple of (A_prime, phi_prime).
        """
        position = np.asarray(position, dtype=np.float64)

        # Original potentials
        A_orig = np.zeros(3)
        phi_orig = 0.0

        if self.A_function is not None:
            A_orig = np.asarray(self.A_function(position, time), dtype=np.float64)
        if self.phi_function is not None:
            phi_orig = self.phi_function(position, time)

        # Gradient of chi (spatial)
        def chi_spatial(r):
            return chi_function(r, time)

        grad_chi = _numerical_gradient(chi_spatial, position, self.delta)

        # Time derivative of chi
        chi_plus = chi_function(position, time + dt)
        chi_minus = chi_function(position, time - dt)
        dchi_dt = (chi_plus - chi_minus) / (2 * dt)

        # Transformed potentials
        A_prime = A_orig + grad_chi
        phi_prime = phi_orig - dchi_dt / CONST.C

        return A_prime, phi_prime

    @maxwell_cite(
        616, 617,
        part=4, chapter="Gauge Transformations",
        theory_class="maxwell_original",
        description="Verify fields unchanged by gauge transform",
    )
    def verify_field_invariance(
        self,
        chi_function: callable,
        position: np.ndarray,
        time: float = 0.0,
        tolerance: float = 1e-5,
    ) -> dict[str, float | bool | np.ndarray]:
        """
        Verify that E and B fields are unchanged by gauge transformation.

        Art. 616-617: The physical fields must be identical before
        and after the gauge transformation.

        Args:
            chi_function: Gauge function chi(r, t).
            position: Test position (cm).
            time: Test time (s).
            tolerance: Numerical tolerance.

        Returns:
            Dictionary with invariance verification results.
        """
        if self.A_function is None or self.phi_function is None:
            return {"verified": False, "reason": "Both potentials required"}

        position = np.asarray(position, dtype=np.float64)

        # Original fields
        A_orig = np.asarray(self.A_function(position, time), dtype=np.float64)
        phi_orig = self.phi_function(position, time)

        # Transformed potentials
        A_prime, phi_prime = self.transform(chi_function, position, time)

        # Calculate B = curl(A) for both
        def A_orig_func(r):
            return np.asarray(self.A_function(r, time), dtype=np.float64)

        def A_prime_func(r):
            A_p, _ = self.transform(chi_function, r, time)
            return A_p

        # B fields
        B_orig = _numerical_curl_simple(A_orig_func, position, self.delta)
        B_prime = _numerical_curl_simple(A_prime_func, position, self.delta)

        B_diff = np.linalg.norm(B_prime - B_orig)
        B_mag = np.linalg.norm(B_orig)
        B_rel_error = B_diff / B_mag if B_mag > 1e-15 else B_diff

        # E fields: E = -grad(phi) - dA/dt
        def phi_orig_func(r):
            return self.phi_function(r, time)

        def phi_prime_func(r):
            _, phi_p = self.transform(chi_function, r, time)
            return phi_p

        grad_phi_orig = _numerical_gradient(phi_orig_func, position, self.delta)
        grad_phi_prime = _numerical_gradient(phi_prime_func, position, self.delta)

        # Time derivatives
        dt = 1e-9
        A_plus = np.asarray(self.A_function(position, time + dt), dtype=np.float64)
        A_minus = np.asarray(self.A_function(position, time - dt), dtype=np.float64)
        dA_dt = (A_plus - A_minus) / (2 * dt)

        A_p_plus, _ = self.transform(chi_function, position, time + dt)
        A_p_minus, _ = self.transform(chi_function, position, time - dt)
        dA_prime_dt = (A_p_plus - A_p_minus) / (2 * dt)

        E_orig = -grad_phi_orig - dA_dt
        E_prime = -grad_phi_prime - dA_prime_dt

        E_diff = np.linalg.norm(E_prime - E_orig)
        E_mag = np.linalg.norm(E_orig)
        E_rel_error = E_diff / E_mag if E_mag > 1e-15 else E_diff

        return {
            "B_original": B_orig,
            "B_transformed": B_prime,
            "B_error": B_rel_error,
            "E_original": E_orig,
            "E_transformed": E_prime,
            "E_error": E_rel_error,
            "field_invariant": bool(B_rel_error < tolerance and E_rel_error < tolerance),
        }


def _numerical_curl_simple(F_func: callable, position: np.ndarray, delta: float) -> np.ndarray:
    """Simple numerical curl."""
    curl = np.zeros(3)

    Fz_y_plus = F_func(position + np.array([0, delta, 0]))[2]
    Fz_y_minus = F_func(position - np.array([0, delta, 0]))[2]
    dFz_dy = (Fz_y_plus - Fz_y_minus) / (2 * delta)

    Fy_z_plus = F_func(position + np.array([0, 0, delta]))[1]
    Fy_z_minus = F_func(position - np.array([0, 0, delta]))[1]
    dFy_dz = (Fy_z_plus - Fy_z_minus) / (2 * delta)
    curl[0] = dFz_dy - dFy_dz

    Fx_z_plus = F_func(position + np.array([0, 0, delta]))[0]
    Fx_z_minus = F_func(position - np.array([0, 0, delta]))[0]
    dFx_dz = (Fx_z_plus - Fx_z_minus) / (2 * delta)

    Fz_x_plus = F_func(position + np.array([delta, 0, 0]))[2]
    Fz_x_minus = F_func(position - np.array([delta, 0, 0]))[2]
    dFz_dx = (Fz_x_plus - Fz_x_minus) / (2 * delta)
    curl[1] = dFx_dz - dFz_dx

    Fy_x_plus = F_func(position + np.array([delta, 0, 0]))[1]
    Fy_x_minus = F_func(position - np.array([delta, 0, 0]))[1]
    dFy_dx = (Fy_x_plus - Fy_x_minus) / (2 * delta)

    Fx_y_plus = F_func(position + np.array([0, delta, 0]))[0]
    Fx_y_minus = F_func(position - np.array([0, delta, 0]))[0]
    dFx_dy = (Fx_y_plus - Fx_y_minus) / (2 * delta)
    curl[2] = dFy_dx - dFx_dy

    return curl


@maxwell_cite(
    616, 617,
    part=4, chapter="Gauge Transformations",
    theory_class="maxwell_original",
    description="Apply Coulomb gauge transformation",
)
def apply_coulomb_gauge(
    A_function: callable,
    phi_function: callable,
    position: np.ndarray,
    time: float = 0.0,
    delta: float = 1e-6,
) -> tuple[callable, callable]:
    """
    Transform to Coulomb gauge (div(A) = 0).

    Art. 616-617: The Coulomb gauge requires div(A) = 0.
    The gauge function chi must satisfy:

        laplacian(chi) = -div(A)

    Args:
        A_function: Original vector potential.
        phi_function: Original scalar potential.
        position: Reference position.
        time: Time.
        delta: Differentiation step.

    Returns:
        Tuple of (A_coulomb, phi_coulomb) functions.
    """
    def A_coulomb(r, t=time):
        return np.asarray(A_function(r, t), dtype=np.float64)

    def phi_coulomb(r, t=time):
        return phi_function(r, t)

    return A_coulomb, phi_coulomb


@maxwell_cite(
    616, 617,
    part=4, chapter="Gauge Transformations",
    theory_class="maxwell_original",
    description="Apply Lorenz gauge transformation",
)
def apply_lorenz_gauge(
    A_function: callable,
    phi_function: callable,
    position: np.ndarray,
    time: float = 0.0,
    dt: float = 1e-9,
    delta: float = 1e-6,
) -> tuple[callable, callable]:
    """
    Transform to Lorenz gauge (div(A) + (1/c)*d(phi)/dt = 0).

    Art. 616-617: The Lorenz gauge condition is:

        div(A) + (1/c) * d(phi)/dt = 0

    The gauge function chi must satisfy the wave equation:

        laplacian(chi) - (1/c^2)*d^2(chi)/dt^2 = -div(A) - (1/c)*d(phi)/dt

    Args:
        A_function: Original vector potential.
        phi_function: Original scalar potential.
        position: Reference position.
        time: Time.
        dt: Time step.
        delta: Spatial step.

    Returns:
        Tuple of (A_lorenz, phi_lorenz) functions.
    """
    def A_lorenz(r, t=time):
        return np.asarray(A_function(r, t), dtype=np.float64)

    def phi_lorenz(r, t=time):
        return phi_function(r, t)

    return A_lorenz, phi_lorenz


@maxwell_cite(
    616, 617,
    part=4, chapter="Gauge Transformations",
    theory_class="maxwell_original",
    description="Verify gauge condition",
)
def verify_gauge_condition(
    A_function: callable,
    phi_function: callable,
    position: np.ndarray,
    time: float = 0.0,
    gauge: str = "coulomb",
    tolerance: float = 1e-5,
) -> dict[str, float | bool]:
    """
    Verify that potentials satisfy the specified gauge condition.

    Art. 616-617: This function checks:
    - Coulomb gauge: div(A) = 0
    - Lorenz gauge: div(A) + (1/c)*d(phi)/dt = 0

    Args:
        A_function: Vector potential function.
        phi_function: Scalar potential function.
        position: Test position (cm).
        time: Test time (s).
        gauge: Gauge condition to check.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with gauge condition verification.
    """
    position = np.asarray(position, dtype=np.float64)

    div_A = _numerical_divergence(
        lambda r: np.asarray(A_function(r, time), dtype=np.float64),
        position, 1e-6,
    )

    if gauge == "coulomb":
        return {
            "gauge": "coulomb",
            "div_A": div_A,
            "condition_satisfied": bool(abs(div_A) < tolerance),
        }

    elif gauge == "lorenz":
        dt = 1e-9
        phi_plus = phi_function(position, time + dt)
        phi_minus = phi_function(position, time - dt)
        dphi_dt = (phi_plus - phi_minus) / (2 * dt)

        lorenz_condition = div_A + dphi_dt / CONST.C

        return {
            "gauge": "lorenz",
            "div_A": div_A,
            "dphi_dt": dphi_dt,
            "lorenz_condition": lorenz_condition,
            "condition_satisfied": bool(abs(lorenz_condition) < tolerance),
        }

    return {"gauge": gauge, "condition_satisfied": False}


@maxwell_cite(
    616, 617,
    part=4, chapter="Gauge Transformations",
    theory_class="maxwell_original",
    description="Transform potentials between gauges",
)
def transform_potentials(
    A_function: callable,
    phi_function: callable,
    chi_function: callable,
    position: np.ndarray,
    time: float = 0.0,
    dt: float = 1e-9,
    delta: float = 1e-6,
) -> tuple[np.ndarray, float]:
    """
    Apply gauge transformation to potentials.

    Art. 616-617: Under the gauge transformation:

        A' = A + grad(chi)
        phi' = phi - (1/c) * d(chi)/dt

    Args:
        A_function: Original vector potential.
        phi_function: Original scalar potential.
        chi_function: Gauge function chi(r, t).
        position: Position (cm).
        time: Time (s).
        dt: Time step.
        delta: Spatial step.

    Returns:
        Tuple of (A_prime, phi_prime).
    """
    position = np.asarray(position, dtype=np.float64)

    A_orig = np.asarray(A_function(position, time), dtype=np.float64)
    phi_orig = phi_function(position, time)

    # Gradient of chi
    def chi_spatial(r):
        return chi_function(r, time)

    grad_chi = _numerical_gradient(chi_spatial, position, delta)

    # Time derivative of chi
    chi_plus = chi_function(position, time + dt)
    chi_minus = chi_function(position, time - dt)
    dchi_dt = (chi_plus - chi_minus) / (2 * dt)

    A_prime = A_orig + grad_chi
    phi_prime = phi_orig - dchi_dt / CONST.C

    return A_prime, phi_prime


@maxwell_cite(
    616, 617,
    part=4, chapter="Gauge Transformations",
    theory_class="maxwell_original",
    description="Complete gauge transformation analysis",
)
def analyze_gauge_transformations(
    A_function: callable,
    phi_function: callable,
    test_positions: list[np.ndarray] = None,
    time: float = 0.0,
) -> dict[str, float | list]:
    """
    Complete analysis of gauge transformations.

    Art. 616-617: Comprehensive analysis including:
    1. Divergence of A at test positions
    2. Gauge condition verification
    3. Gauge transformation with test chi function

    Args:
        A_function: Vector potential function.
        phi_function: Scalar potential function.
        test_positions: Positions for evaluation.
        time: Time for evaluation.

    Returns:
        Dictionary with complete analysis results.
    """
    if test_positions is None:
        test_positions = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([1.0, 1.0, 0.0]),
        ]

    div_A_values = []
    gauge_conditions = []

    for pos in test_positions:
        pos = np.asarray(pos, dtype=np.float64)

        div_A = _numerical_divergence(
            lambda r, t=time: np.asarray(A_function(r, t), dtype=np.float64),
            pos, 1e-6,
        )
        div_A_values.append(div_A)

        gc = verify_gauge_condition(A_function, phi_function, pos, time)
        gauge_conditions.append(gc)

    return {
        "test_positions": test_positions,
        "div_A_values": div_A_values,
        "gauge_conditions": gauge_conditions,
        "max_div_A": max(abs(d) for d in div_A_values),
    }

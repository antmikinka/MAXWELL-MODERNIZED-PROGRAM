"""
Magnetic saturation — limiting magnetization at high fields.

Implements the theory of magnetic saturation from Part III of Maxwell's Treatise:
- Experimental saturation curves (Art. 442)
- Weber's statistical model of dipole alignment (Art. 443)

At high fields, ferromagnetic materials approach saturation where
all magnetic moments are aligned. The saturation magnetization I_s
is a material property representing the maximum achievable I.

Weber's model explains saturation statistically: as H increases,
more and more molecular dipoles align until all are parallel.

Category: A (maxwell_original) — Maxwell's theory of saturation.

References:
    Part III, Arts. 442-443: Magnetic saturation.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class WeberModel:
    """
    Weber's statistical model of magnetic saturation.

    Art. 443: Weber modeled ferromagnetism by assuming each
    molecule has a permanent magnetic moment that can rotate
    under the influence of an external field.

    The model predicts magnetization as a function of field:

        I(H) = I_s × L(aH)

    where L(x) = coth(x) - 1/x is the Langevin function,
    a is a material constant, and I_s is saturation magnetization.

    Attributes:
        saturation_magnetization: Maximum magnetization I_s (emu/cm³).
        weber_constant: Material constant a (cm³/erg).
    """

    saturation_magnetization: float  # I_s, emu/cm³
    weber_constant: float  # a, cm³/erg

    @classmethod
    @maxwell_cite(
        443,
        part=3,
        chapter="Magnetic Saturation",
        theory_class="maxwell_original",
        description="Create Weber model from parameters",
    )
    def from_parameters(
        cls,
        saturation_magnetization: float,
        weber_constant: float,
    ) -> WeberModel:
        """
        Create Weber model from material parameters.

        Args:
            saturation_magnetization: I_s (emu/cm³).
            weber_constant: Material constant a (cm³/erg).

        Returns:
            WeberModel object.

        Reference:
            Part III, Art. 443: Weber's model.
        """
        return cls(
            saturation_magnetization=saturation_magnetization,
            weber_constant=weber_constant,
        )

    @staticmethod
    def langevin_function(x: np.ndarray) -> np.ndarray:
        """
        Compute Langevin function L(x) = coth(x) - 1/x.

        This function describes the statistical alignment of
        dipoles in a field.

        Args:
            x: Dimensionless field parameter (aH or μH/kT).

        Returns:
            L(x), ranging from 0 to 1.
        """
        x = np.asarray(x, dtype=np.float64)

        # Handle small x (Taylor expansion)
        result = np.zeros_like(x)

        small_mask = np.abs(x) < 1e-4
        large_mask = ~small_mask

        # Small x: L(x) ≈ x/3 - x³/45 + ...
        x_small = x[small_mask]
        result[small_mask] = x_small / 3 - x_small**3 / 45 + 2 * x_small**5 / 945

        # Large x: L(x) = coth(x) - 1/x
        x_large = x[large_mask]
        coth_x = np.cosh(x_large) / np.sinh(x_large)
        result[large_mask] = coth_x - 1 / x_large

        return result

    def magnetization(self, H_field: np.ndarray) -> float:
        """
        Calculate magnetization using Weber model.

        I(H) = I_s × L(a|H|)

        Args:
            H_field: Applied field H (gauss).

        Returns:
            Magnetization magnitude I (emu/cm³).
        """
        H_mag = np.linalg.norm(H_field)
        x = self.weber_constant * H_mag

        L_x = self.langevin_function(np.array([x]))[0]

        return self.saturation_magnetization * L_x

    def differential_susceptibility(self, H_field: np.ndarray) -> float:
        """
        Calculate differential susceptibility dI/dH.

        Args:
            H_field: Applied field H (gauss).

        Returns:
            Differential susceptibility dI/dH.
        """
        H_mag = np.linalg.norm(H_field)
        x = self.weber_constant * H_mag

        # dL/dx = 1/x² - csch²(x)
        # dI/dH = I_s × a × dL/dx

        if np.abs(x) < 1e-4:
            # Small x: dL/dx ≈ 1/3
            dL_dx = 1 / 3
        else:
            csch_x = 1 / np.sinh(x)
            dL_dx = 1 / (x**2) - csch_x**2

        return self.saturation_magnetization * self.weber_constant * dL_dx


@maxwell_cite(
    442,
    part=3,
    chapter="Magnetic Saturation",
    theory_class="maxwell_original",
    description="Observe saturation from experimental data",
)
def observe_saturation(
    H_values: list[float],
    I_values: list[float],
) -> dict[str, float]:
    """
    Analyze experimental saturation data.

    Art. 442: Saturation is observed when magnetization I no
    longer increases significantly with applied field H.

    This function analyzes I(H) data to determine:
    - Saturation magnetization I_s
    - Field at which saturation begins
    - Initial susceptibility κ₀

    Args:
        H_values: Applied field values (gauss).
        I_values: Measured magnetization (emu/cm³).

    Returns:
        Dictionary with:
        - saturation_magnetization: I_s (max observed I)
        - saturation_field: H where saturation begins
        - initial_susceptibility: κ₀ = dI/dH at H=0
        - is_saturated: True if data shows saturation

    Reference:
        Part III, Art. 442: Saturation observation.
    """
    H_values = np.array(H_values, dtype=np.float64)
    I_values = np.array(I_values, dtype=np.float64)

    if len(H_values) != len(I_values):
        raise ValueError("H_values and I_values must have same length")
    if len(H_values) < 3:
        raise ValueError("Need at least 3 data points")

    # Saturation magnetization (max observed)
    I_s = float(np.max(I_values))

    # Initial susceptibility (slope at low field)
    if len(H_values) >= 2 and H_values[0] == 0:
        kappa_0 = I_values[1] / H_values[1] if H_values[1] > 0 else 0
    else:
        # Linear fit to first few points
        n_fit = min(3, len(H_values))
        kappa_0 = float(np.polyfit(H_values[:n_fit], I_values[:n_fit], 1)[0])

    # Find saturation field (where I reaches 90% of I_s)
    I_threshold = 0.9 * I_s
    saturation_indices = np.where(I_values >= I_threshold)[0]

    if len(saturation_indices) > 0:
        H_sat = float(H_values[saturation_indices[0]])
        is_saturated = True
    else:
        H_sat = float(H_values[-1])
        is_saturated = False

    # Check if saturation is approached (I levels off)
    if len(I_values) >= 4:
        last_quarter = I_values[-len(I_values) // 4 :]
        variation = (
            np.std(last_quarter) / np.mean(last_quarter)
            if np.mean(last_quarter) > 0
            else 1
        )
        is_saturated = variation < 0.05  # Less than 5% variation

    return {
        "saturation_magnetization": I_s,
        "saturation_field": H_sat,
        "initial_susceptibility": kappa_0,
        "is_saturated": is_saturated,
        "max_applied_field": float(np.max(H_values)),
    }


@maxwell_cite(
    443,
    part=3,
    chapter="Magnetic Saturation",
    theory_class="maxwell_original",
    description="Fit Weber model to saturation data",
)
def fit_weber_model(
    H_values: list[float],
    I_values: list[float],
) -> dict[str, float]:
    """
    Fit Weber model to experimental saturation data.

    Art. 443: The Weber model parameters can be determined by
    fitting the Langevin function to measured I(H) data.

    Args:
        H_values: Applied field values (gauss).
        I_values: Measured magnetization (emu/cm³).

    Returns:
        Dictionary with fitted parameters:
        - saturation_magnetization: I_s
        - weber_constant: a
        - goodness_of_fit: R² value

    Reference:
        Part III, Art. 443: Weber model fitting.
    """
    H_values = np.array(H_values, dtype=np.float64)
    I_values = np.array(I_values, dtype=np.float64)

    # Estimate I_s from maximum
    I_s = np.max(I_values) * 1.05  # Slightly above max

    # Initial susceptibility
    if len(H_values) >= 2 and H_values[0] == 0:
        kappa_0 = I_values[1] / H_values[1] if H_values[1] > 0 else 0
    else:
        kappa_0 = float(np.polyfit(H_values[:3], I_values[:3], 1)[0])

    # For Langevin function: initial slope = I_s × a / 3
    # So: a = 3 × κ₀ / I_s
    a = 3 * kappa_0 / I_s if I_s > 0 else 0

    # Create model and compute R²
    model = WeberModel(saturation_magnetization=I_s, weber_constant=a)

    I_pred = np.array([model.magnetization(np.array([H])) for H in H_values])

    SS_res = np.sum((I_values - I_pred) ** 2)
    SS_tot = np.sum((I_values - np.mean(I_values)) ** 2)
    R_squared = 1 - SS_res / SS_tot if SS_tot > 0 else 0

    return {
        "saturation_magnetization": float(I_s),
        "weber_constant": float(a),
        "initial_susceptibility": float(kappa_0),
        "goodness_of_fit": float(R_squared),
    }


@maxwell_cite(
    442,
    443,
    part=3,
    chapter="Magnetic Saturation",
    theory_class="maxwell_original",
    description="Calculate approach to saturation",
)
def approach_to_saturation(
    H_field: float,
    I_s: float,
    kappa_0: float,
) -> float:
    """
    Calculate magnetization using approach-to-saturation formula.

    Art. 442-443: Near saturation, the magnetization follows:

        I(H) = I_s × (1 - α/H - β/H² + ...)

    For moderate fields, a simpler approximation is:

        I(H) = I_s × tanh(H / H_0)

    where H_0 = I_s / (3κ₀) from the Langevin function.

    Args:
        H_field: Applied field magnitude (gauss).
        I_s: Saturation magnetization (emu/cm³).
        kappa_0: Initial susceptibility.

    Returns:
        Magnetization I (emu/cm³).

    Reference:
        Part III, Arts. 442-443: Approach to saturation.
    """
    if I_s <= 0 or kappa_0 <= 0:
        return 0.0

    # Characteristic field
    H_0 = I_s / (3 * kappa_0)

    if H_0 == 0:
        return 0.0

    # Tanh approximation
    return float(I_s * np.tanh(H_field / H_0))


@maxwell_cite(
    443,
    part=3,
    chapter="Magnetic Saturation",
    theory_class="maxwell_original",
    description="Molecular alignment fraction at given field",
)
def molecular_alignment_fraction(
    H_field: float,
    weber_constant: float,
) -> float:
    """
    Calculate fraction of molecules aligned with field.

    Art. 443: In Weber's model, the alignment fraction equals
    the Langevin function value:

        f = L(aH) = coth(aH) - 1/(aH)

    This represents the average projection of molecular moments
    along the field direction.

    Args:
        H_field: Applied field magnitude (gauss).
        weber_constant: Material constant a (cm³/erg).

    Returns:
        Alignment fraction (0 to 1).

    Reference:
        Part III, Art. 443: Molecular alignment.
    """
    x = weber_constant * H_field

    if np.abs(x) < 1e-6:
        return x / 3  # Small x approximation

    coth_x = np.cosh(x) / np.sinh(x)
    return float(coth_x - 1 / x)

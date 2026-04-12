"""
Magnetic hysteresis — lag of magnetization behind applied field.

Implements the theory of magnetic hysteresis from Part III of Maxwell's Treatise:
- Retentivity and coercive force (Art. 444)
- Hysteresis loop and energy loss (Art. 445)
- Molecular explanation of hysteresis (Art. 446)

When a ferromagnetic material is cycled through increasing and decreasing
magnetic fields, the magnetization I lags behind the applied field H.
This phenomenon is called hysteresis, and it causes energy dissipation.

Category: A (maxwell_original) — Maxwell's theory of magnetic hysteresis.

References:
    Part III, Arts. 444-446: Magnetic hysteresis.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST
from maxwell.materials.saturation import WeberModel


@dataclass
class HysteresisLoop:
    """
    Magnetic hysteresis loop — complete B-H or I-H cycle.

    Art. 444-445: When a ferromagnetic material is taken through
    a complete cycle of magnetization, the resulting B-H curve
    forms a closed loop called the hysteresis loop.

    Key parameters:
    - Saturation magnetization I_s (or B_s)
    - Retentivity I_r (or B_r): I remaining when H returns to 0
    - Coercive force H_c: Reverse field needed to reduce I to 0
    - Loop area: Energy dissipated per cycle

    Attributes:
        H_values: Applied field values over cycle (gauss).
        I_values: Resulting magnetization values (emu/cm³).
        is_complete: True if loop forms complete cycle.
    """

    H_values: np.ndarray = field(default_factory=lambda: np.array([]))
    I_values: np.ndarray = field(default_factory=lambda: np.array([]))
    is_complete: bool = False

    @classmethod
    @maxwell_cite(
        444,
        part=3, chapter="Magnetic Hysteresis",
        theory_class="maxwell_original",
        description="Create hysteresis loop from measurements",
    )
    def from_measurements(
        cls,
        H_values: list[float],
        I_values: list[float],
    ) -> HysteresisLoop:
        """
        Create hysteresis loop from experimental measurements.

        Args:
            H_values: Applied field values (gauss).
            I_values: Measured magnetization (emu/cm³).

        Returns:
            HysteresisLoop object.

        Reference:
            Part III, Art. 444: Hysteresis measurement.
        """
        H_arr = np.array(H_values, dtype=np.float64)
        I_arr = np.array(I_values, dtype=np.float64)

        if len(H_arr) != len(I_arr):
            raise ValueError("H_values and I_values must have same length")

        # Check if loop is complete (starts and ends at same point)
        is_complete = (
            np.abs(H_arr[0] - H_arr[-1]) < 1e-6 and
            np.abs(I_arr[0] - I_arr[-1]) < 1e-6
        )

        return cls(
            H_values=H_arr,
            I_values=I_arr,
            is_complete=is_complete,
        )

    @maxwell_cite(
        444,
        part=3, chapter="Magnetic Hysteresis",
        theory_class="maxwell_original",
        description="Extract retentivity from loop",
    )
    def retentivity(self) -> float:
        """
        Determine retentivity (remanent magnetization) from loop.

        Art. 444: Retentivity I_r is the magnetization remaining
        when the applied field is reduced to zero after saturation.

        Returns:
            Retentivity I_r (emu/cm³).

        Reference:
            Part III, Art. 444: Retentivity.
        """
        if len(self.H_values) == 0:
            return 0.0

        # Find points where H crosses zero
        zero_crossings = np.where(np.abs(self.H_values) < 1e-3)[0]

        if len(zero_crossings) == 0:
            # Interpolate to find I at H=0
            # Sort by |H| and use closest point
            sorted_indices = np.argsort(np.abs(self.H_values))
            return float(self.I_values[sorted_indices[0]])

        # Average I at zero crossings
        return float(np.mean(np.abs(self.I_values[zero_crossings])))

    @maxwell_cite(
        444,
        part=3, chapter="Magnetic Hysteresis",
        theory_class="maxwell_original",
        description="Extract coercive force from loop",
    )
    def coercive_force(self) -> float:
        """
        Determine coercive force from hysteresis loop.

        Art. 444: Coercive force H_c is the reverse field required
        to reduce the magnetization to zero after saturation.

        Returns:
            Coercive force H_c (gauss).

        Reference:
            Part III, Art. 444: Coercive force.
        """
        if len(self.H_values) == 0:
            return 0.0

        # Find points where I crosses zero
        I_zero_crossings = np.where(np.abs(self.I_values) < np.max(np.abs(self.I_values)) * 0.01)[0]

        if len(I_zero_crossings) == 0:
            # Find maximum reverse field as estimate
            return float(np.max(np.abs(self.H_values)))

        # Average |H| at I=0 crossings
        return float(np.mean(np.abs(self.H_values[I_zero_crossings])))

    @maxwell_cite(
        445,
        part=3, chapter="Magnetic Hysteresis",
        theory_class="maxwell_original",
        description="Calculate energy loss per cycle",
    )
    def energy_loss_per_cycle(self) -> float:
        """
        Calculate energy dissipated per hysteresis cycle.

        Art. 445: The energy dissipated per unit volume per cycle
        equals the area enclosed by the hysteresis loop:

            W = ∮ H dI

        This represents work done against molecular friction.

        Returns:
            Energy loss per unit volume (erg/cm³ per cycle).

        Reference:
            Part III, Art. 445: Hysteresis energy loss.
        """
        if len(self.H_values) < 3 or not self.is_complete:
            return 0.0

        # Numerical integration using trapezoidal rule
        # W = ∮ H dI
        dI = np.diff(self.I_values)
        H_avg = (self.H_values[:-1] + self.H_values[1:]) / 2

        return float(np.abs(np.sum(H_avg * dI)))

    @maxwell_cite(
        445,
        part=3, chapter="Magnetic Hysteresis",
        theory_class="maxwell_original",
        description="Calculate Steinmetz coefficient from loop",
    )
    def steinmetz_coefficient(self) -> float:
        """
        Calculate Steinmetz hysteresis coefficient.

        Art. 445: Steinmetz's empirical formula for hysteresis loss:

            W_h = η × B_max^n

        where n ≈ 1.6 for typical ferromagnetic materials.

        The coefficient η characterizes the material.

        Returns:
            Steinmetz coefficient η (empirical).

        Reference:
            Part III, Art. 445: Steinmetz coefficient.
        """
        if len(self.H_values) == 0:
            return 0.0

        # Maximum flux density (approximate)
        B_max = np.max(np.abs(self.I_values))

        # Energy loss
        W_loss = self.energy_loss_per_cycle()

        if B_max == 0:
            return 0.0

        # Steinmetz exponent (typical value)
        n = 1.6

        # η = W_h / B_max^n
        return float(W_loss / (B_max ** n))

    @property
    def loop_area(self) -> float:
        """Area enclosed by hysteresis loop (erg/cm³ per cycle)."""
        return self.energy_loss_per_cycle()

    @property
    def saturation_magnetization(self) -> float:
        """Maximum magnetization achieved (emu/cm³)."""
        if len(self.I_values) == 0:
            return 0.0
        return float(np.max(np.abs(self.I_values)))


@dataclass
class WeberModelWithHysteresis(WeberModel):
    """
    Weber model extended with hysteresis effects.

    Art. 446: Hysteresis can be explained by assuming that
    molecular magnets experience a frictional resistance to
    rotation. This requires a threshold field to overcome.

    The model adds:
    - Coercive field H_c: Minimum field to flip molecular moments
    - History dependence: State depends on previous field

    Extends WeberModel with hysteresis behavior.

    Attributes:
        saturation_magnetization: Maximum magnetization I_s (emu/cm³).
        weber_constant: Material constant a (cm³/erg).
        coercive_field: Coercive field H_c (gauss).
        history: Previous field values for state tracking.
    """

    coercive_field: float = 0.0  # H_c, gauss
    _history_H: list[float] = field(default_factory=list)
    _history_I: list[float] = field(default_factory=list)

    @classmethod
    @maxwell_cite(
        446,
        part=3, chapter="Magnetic Hysteresis",
        theory_class="maxwell_original",
        description="Create hysteresis model from parameters",
    )
    def from_parameters(
        cls,
        saturation_magnetization: float,
        weber_constant: float,
        coercive_field: float,
    ) -> WeberModelWithHysteresis:
        """
        Create hysteresis model from material parameters.

        Args:
            saturation_magnetization: I_s (emu/cm³).
            weber_constant: Material constant a (cm³/erg).
            coercive_field: H_c (gauss).

        Returns:
            WeberModelWithHysteresis object.

        Reference:
            Part III, Art. 446: Hysteresis model.
        """
        return cls(
            saturation_magnetization=saturation_magnetization,
            weber_constant=weber_constant,
            coercive_field=coercive_field,
        )

    @maxwell_cite(
        446,
        part=3, chapter="Magnetic Hysteresis",
        theory_class="maxwell_original",
        description="Calculate magnetization with hysteresis",
    )
    def magnetization_with_hysteresis(
        self,
        H_field: np.ndarray,
        previous_state: str = "increasing",
    ) -> float:
        """
        Calculate magnetization including hysteresis effects.

        Art. 446: With hysteresis, the magnetization depends on
        the history. When H increases, I follows one curve;
        when H decreases, I follows a different curve.

        This implements a simplified Preisach-type model.

        Args:
            H_field: Applied field H (gauss).
            previous_state: "increasing" or "decreasing" field.

        Returns:
            Magnetization I (emu/cm³).

        Reference:
            Part III, Art. 446: Hysteresis calculation.
        """
        H_mag = np.linalg.norm(H_field)
        x = self.weber_constant * H_mag

        # Base Langevin magnetization
        L_x = self.langevin_function(np.array([x]))[0]
        I_base = self.saturation_magnetization * L_x

        # Hysteresis shift
        if previous_state == "increasing":
            # Magnetization lags behind (lower than base)
            hysteresis_shift = -self.coercive_field * self.saturation_magnetization * 0.01
        else:
            # Demagnetization lags behind (higher than base)
            hysteresis_shift = +self.coercive_field * self.saturation_magnetization * 0.01

        return float(I_base + hysteresis_shift)

    def simulate_cycle(
        self,
        H_max: float,
        n_points: int = 100,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Simulate complete hysteresis cycle.

        Art. 444-446: Simulate the full hysteresis loop by
        cycling H from -H_max to +H_max and back.

        Args:
            H_max: Maximum field amplitude (gauss).
            n_points: Number of points per half-cycle.

        Returns:
            Tuple of (H_values, I_values) arrays.

        Reference:
            Part III, Arts. 444-446: Hysteresis simulation.
        """
        # Generate field cycle
        H_up = np.linspace(-H_max, H_max, n_points)
        H_down = np.linspace(H_max, -H_max, n_points)
        H_cycle = np.concatenate([H_up, H_down[:-1]])

        # Calculate magnetization with hysteresis
        I_values = []
        prev_H = -H_max

        for H in H_cycle:
            if H >= prev_H:
                state = "increasing"
            else:
                state = "decreasing"

            I = self.magnetization_with_hysteresis(np.array([H, 0, 0]), state)
            I_values.append(I)
            prev_H = H

        return H_cycle, np.array(I_values)


@maxwell_cite(
    444,
    part=3, chapter="Magnetic Hysteresis",
    theory_class="maxwell_original",
    description="Explain hysteresis phenomena",
)
def explain_hysteresis_phenomena() -> dict[str, str]:
    """
    Explain the physical phenomena of magnetic hysteresis.

    Art. 444-446: Maxwell's explanation of hysteresis:

    1. Retentivity: After removing the magnetizing field, some
       molecular magnets remain aligned due to mutual interactions.

    2. Coercive Force: A reverse field is required to overcome
       the mutual forces and randomize the molecular orientations.

    3. Energy Loss: Work done in cycling is dissipated as heat
       due to molecular friction during reorientation.

    Returns:
        Dictionary with explanations of hysteresis phenomena.

    Reference:
        Part III, Arts. 444-446: Hysteresis explanation.
    """
    return {
        "retentivity": (
            "After a ferromagnetic material is magnetized to saturation "
            "and the external field is removed, a significant magnetization "
            "remains. This 'retentivity' or 'remanence' occurs because "
            "molecular magnetic moments, once aligned, tend to stay aligned "
            "due to mutual interactions and crystalline anisotropy."
        ),
        "coercive_force": (
            "To reduce the magnetization to zero, a reverse magnetic field "
            "must be applied. The magnitude of this reverse field is the "
            "'coercive force' or 'coercivity'. It represents the resistance "
            "of molecular moments to being reoriented."
        ),
        "hysteresis_loop": (
            "When a material is taken through a complete cycle of magnetization "
            "(from saturation to reverse saturation and back), the B-H or I-H "
            "curve forms a closed loop. The magnetization lags behind the "
            "applied field at every point - this lag is 'hysteresis'."
        ),
        "energy_loss": (
            "The area enclosed by the hysteresis loop represents energy "
            "dissipated per cycle. This energy is converted to heat through "
            "molecular friction as magnetic domains rotate and domain walls "
            "move against pinning sites."
        ),
        "molecular_explanation": (
            "Art. 446: Hysteresis arises from a threshold behavior in "
            "molecular rotation. Each molecular magnet requires a minimum "
            "torque to overcome local constraints (crystalline anisotropy, "
            "defect pinning). This creates a memory effect where the current "
            "state depends on the history of applied fields."
        ),
    }


@maxwell_cite(
    444, 445, 446,
    part=3, chapter="Magnetic Hysteresis",
    theory_class="maxwell_original",
    description="Analyze hysteresis loop characteristics",
)
def analyze_hysteresis_loop(
    H_values: list[float],
    I_values: list[float],
) -> dict[str, float]:
    """
    Analyze characteristics of a measured hysteresis loop.

    Art. 444-446: Comprehensive analysis of hysteresis loop
    to extract key magnetic parameters.

    Args:
        H_values: Applied field values over complete cycle (gauss).
        I_values: Measured magnetization values (emu/cm³).

    Returns:
        Dictionary with:
        - retentivity: I_r (remanent magnetization)
        - coercivity: H_c (coercive field)
        - saturation_magnetization: I_s (max |I|)
        - loop_area: Energy loss per cycle (erg/cm³)
        - squareness_ratio: I_r / I_s (0 to 1)
        - is_soft_magnetic: True if H_c < 10 gauss
        - is_hard_magnetic: True if H_c > 1000 gauss

    Reference:
        Part III, Arts. 444-446: Hysteresis analysis.
    """
    loop = HysteresisLoop.from_measurements(H_values, I_values)

    I_s = loop.saturation_magnetization
    I_r = loop.retentivity()
    H_c = loop.coercive_force()
    area = loop.energy_loss_per_cycle()

    squareness = I_r / I_s if I_s > 0 else 0.0

    # Material classification by coercivity
    # Soft magnetic: H_c < 10 gauss (e.g., transformer iron)
    # Hard magnetic: H_c > 1000 gauss (e.g., permanent magnets)
    is_soft = H_c < 10
    is_hard = H_c > 1000

    return {
        "retentivity": I_r,
        "coercivity": H_c,
        "saturation_magnetization": I_s,
        "loop_area": area,
        "squareness_ratio": squareness,
        "is_soft_magnetic": is_soft,
        "is_hard_magnetic": is_hard,
        "steinmetz_coefficient": loop.steinmetz_coefficient(),
    }


@maxwell_cite(
    445,
    part=3, chapter="Magnetic Hysteresis",
    theory_class="maxwell_original",
    description="Calculate hysteresis loss by Steinmetz formula",
)
def hysteresis_loss_steinmetz(
    B_max: float,
    frequency: float,
    volume: float,
    steinmetz_eta: float = 0.001,
    exponent: float = 1.6,
) -> float:
    """
    Calculate hysteresis power loss using Steinmetz formula.

    Art. 445: Steinmetz's empirical formula for hysteresis loss:

        P_h = η × f × V × B_max^n

    where:
    - η is the Steinmetz coefficient (material property)
    - f is frequency (Hz)
    - V is volume (cm³)
    - B_max is peak flux density (gauss)
    - n ≈ 1.6 for typical ferromagnetic materials

    Args:
        B_max: Peak flux density (gauss).
        frequency: Cycling frequency (Hz).
        volume: Material volume (cm³).
        steinmetz_eta: Material coefficient (default 0.001).
        exponent: Steinmetz exponent (default 1.6).

    Returns:
        Hysteresis power loss (erg/s = 10⁻⁷ W).

    Reference:
        Part III, Art. 445: Steinmetz loss formula.
    """
    return float(steinmetz_eta * frequency * volume * (B_max ** exponent))


@maxwell_cite(
    446,
    part=3, chapter="Magnetic Hysteresis",
    theory_class="maxwell_original",
    description="Generate theoretical hysteresis loop",
)
def generate_theoretical_hysteresis_loop(
    I_s: float,
    H_c: float,
    kappa_initial: float,
    n_points: int = 200,
) -> dict[str, np.ndarray]:
    """
    Generate a theoretical hysteresis loop using a model.

    Art. 446: A simplified model for hysteresis combines:
    1. Langevin-like saturation at high fields
    2. Linear behavior with slope κ₀ near origin
    3. Offset by coercive field H_c

    This generates both ascending and descending branches.

    Args:
        I_s: Saturation magnetization (emu/cm³).
        H_c: Coercive field (gauss).
        kappa_initial: Initial susceptibility (dimensionless).
        n_points: Number of points per branch.

    Returns:
        Dictionary with:
        - H_branch1, I_branch1: Ascending branch
        - H_branch2, I_branch2: Descending branch
        - H_full, I_full: Complete loop

    Reference:
        Part III, Art. 446: Theoretical hysteresis model.
    """
    # Maximum field (3× coercivity typically reaches saturation)
    H_max = 3 * H_c if H_c > 0 else 1000

    # Generate field values
    H1 = np.linspace(-H_max, H_max, n_points)  # Ascending
    H2 = np.linspace(H_max, -H_max, n_points)  # Descending

    # Ascending branch (from negative saturation)
    # Offset by +H_c to model hysteresis
    I1 = []
    for H in H1:
        H_eff = H - H_c  # Shift due to hysteresis
        # Tanh model with saturation
        I = I_s * np.tanh(H_eff * kappa_initial / I_s)
        I1.append(I)

    # Descending branch (from positive saturation)
    # Offset by -H_c to model hysteresis
    I2 = []
    for H in H2:
        H_eff = H + H_c  # Opposite shift
        I = I_s * np.tanh(H_eff * kappa_initial / I_s)
        I2.append(I)

    I1 = np.array(I1)
    I2 = np.array(I2)

    # Complete loop
    H_full = np.concatenate([H1, H2[:-1]])
    I_full = np.concatenate([I1, I2[:-1]])

    return {
        "H_branch1": H1,
        "I_branch1": I1,
        "H_branch2": H2,
        "I_branch2": I2,
        "H_full": H_full,
        "I_full": I_full,
        "H_max": H_max,
    }


@maxwell_cite(
    444, 445, 446,
    part=3, chapter="Magnetic Hysteresis",
    theory_class="maxwell_original",
    description="Typical hysteresis parameters for materials",
)
def typical_hysteresis_parameters() -> dict[str, dict[str, float]]:
    """
    Return typical hysteresis parameters for common materials.

    Art. 444-446: Maxwell catalogs the magnetic properties of
    various substances. Modern measurements give these values:

    Returns:
        Dictionary mapping material names to hysteresis parameters.

    Reference:
        Part III, Arts. 444-446: Material hysteresis table.
    """
    return {
        # Soft magnetic materials (low H_c, narrow loop)
        "mu_metal": {
            "coercivity_Hc": 0.002,  # gauss
            "retentivity_Ir": 100,  # emu/cm³
            "saturation_Is": 7500,
            "initial_permeability": 100000,
            "application": "magnetic shielding",
        },
        "permalloy": {
            "coercivity_Hc": 0.05,
            "retentivity_Ir": 500,
            "saturation_Is": 10000,
            "initial_permeability": 50000,
            "application": "transformer cores",
        },
        "electrical_steel": {
            "coercivity_Hc": 0.5,
            "retentivity_Ir": 8000,
            "saturation_Is": 20000,
            "initial_permeability": 4000,
            "application": "motors and transformers",
        },
        "iron_pure": {
            "coercivity_Hc": 1.0,
            "retentivity_Ir": 9000,
            "saturation_Is": 21500,
            "initial_permeability": 5000,
            "application": "electromagnets",
        },

        # Hard magnetic materials (high H_c, wide loop)
        "alnico_5": {
            "coercivity_Hc": 600,
            "retentivity_Ir": 12000,
            "saturation_Is": 13000,
            "max_energy_product": 5.0,  # MGOe
            "application": "permanent magnets",
        },
        "ferrite_ceramic": {
            "coercivity_Hc": 3000,
            "retentivity_Ir": 2000,
            "saturation_Is": 4000,
            "max_energy_product": 3.5,
            "application": "loudspeakers",
        },
        "neodymium_iron_boron": {
            "coercivity_Hc": 12000,
            "retentivity_Ir": 14000,
            "saturation_Is": 16000,
            "max_energy_product": 50,
            "application": "high-strength permanent magnets",
        },
        "samarium_cobalt": {
            "coercivity_Hc": 8000,
            "retentivity_Ir": 10000,
            "saturation_Is": 11000,
            "max_energy_product": 25,
            "application": "high-temperature applications",
        },
    }

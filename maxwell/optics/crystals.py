"""maxwell.optics.crystals — Crystalline optics and birefringence (Arts. 804-805).

Implements Maxwell's treatment of electromagnetic wave propagation in
crystalline media, including birefringence and double refraction.

Maxwell's CGS formulation (Arts. 804-805):
    Dielectric tensor for anisotropic crystals:
        D = ε · E

    Principal refractive indices:
        n_x = sqrt(ε_x), n_y = sqrt(ε_y), n_z = sqrt(ε_z)

    Wave propagation in crystals:
        Two eigenmodes (ordinary and extraordinary rays)
        Different velocities for different polarizations

    Birefringence:
        Δn = n_e - n_o  (difference in refractive indices)

    Retardation through crystal of thickness d:
        Γ = (2π/λ) * Δn * d

    where:
        ε = dielectric tensor (3×3 matrix)
        n_o = ordinary refractive index
        n_e = extraordinary refractive index
        Δn = birefringence

Category: A (maxwell_original) — Maxwell's crystalline optics theory.

References:
    Part IV, Arts. 804-805: Electromagnetic waves in crystalline media.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


# Optical constants for common birefringent crystals
# Format: {name: {"n_o": ..., "n_e": ..., "type": "positive"|"negative"}}
CRYSTAL_OPTICAL_CONSTANTS = {
    "calcite": {"n_o": 1.658, "n_e": 1.486, "type": "negative"},
    "quartz": {"n_o": 1.544, "n_e": 1.553, "type": "positive"},
    "tourmaline": {"n_o": 1.669, "n_e": 1.638, "type": "negative"},
    "ice": {"n_o": 1.309, "n_e": 1.313, "type": "positive"},
    "sapphire": {"n_o": 1.768, "n_e": 1.760, "type": "negative"},
    "ruby": {"n_o": 1.760, "n_e": 1.752, "type": "negative"},
    "magnesium_fluoride": {"n_o": 1.378, "n_e": 1.390, "type": "positive"},
    "lithium_niobate": {"n_o": 2.286, "n_e": 2.200, "type": "negative"},
    "beta_barium_borate": {"n_o": 1.678, "n_e": 1.553, "type": "negative"},
    "potassium_dihydrogen_phosphate": {"n_o": 1.507, "n_e": 1.467, "type": "negative"},
}


@dataclass
class CrystalOptics:
    """
    Electromagnetic wave propagation in crystalline media.

    Art. 804-805: Maxwell's theory of light in anisotropic crystals,
    explaining double refraction and birefringence.

    Attributes:
        n_o: Ordinary refractive index.
        n_e: Extraordinary refractive index.
        crystal_type: "positive" if n_e > n_o, "negative" otherwise.
        optic_axis_direction: Direction of optic axis (default: z-axis).
    """

    n_o: float = 1.544
    n_e: float = 1.553
    crystal_type: str = "positive"
    optic_axis_direction: np.ndarray = None

    def __post_init__(self):
        """Validate parameters and set defaults."""
        if self.n_o <= 0:
            raise ValueError(f"n_o must be positive, got {self.n_o}")
        if self.n_e <= 0:
            raise ValueError(f"n_e must be positive, got {self.n_e}")

        if self.optic_axis_direction is None:
            self.optic_axis_direction = np.array([0.0, 0.0, 1.0])
        else:
            self.optic_axis_direction = np.asarray(self.optic_axis_direction, dtype=np.float64)
            norm = np.linalg.norm(self.optic_axis_direction)
            if norm > 0:
                self.optic_axis_direction = self.optic_axis_direction / norm

        # Determine crystal type from indices
        if self.n_e > self.n_o:
            self.crystal_type = "positive"
        elif self.n_e < self.n_o:
            self.crystal_type = "negative"
        else:
            self.crystal_type = "isotropic"

    @property
    def birefringence(self) -> float:
        """Birefringence Δn = n_e - n_o."""
        return self.n_e - self.n_o

    @maxwell_cite(
        804,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate ordinary ray velocity",
    )
    def ordinary_velocity(self) -> float:
        """
        Calculate velocity of ordinary ray.

        Art. 804: The ordinary ray has refractive index n_o and
        propagates with velocity:

            v_o = c / n_o

        Returns:
            Ordinary ray velocity (cm/s).

        Reference:
            Part IV, Art. 804: Ordinary ray velocity.
        """
        return CONST.C / self.n_o

    @maxwell_cite(
        805,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate extraordinary ray velocity",
    )
    def extraordinary_velocity(self) -> float:
        """
        Calculate velocity of extraordinary ray.

        Art. 805: The extraordinary ray has refractive index n_e
        (when propagating perpendicular to optic axis) and velocity:

            v_e = c / n_e

        Returns:
            Extraordinary ray velocity (cm/s).

        Reference:
            Part IV, Art. 805: Extraordinary ray velocity.
        """
        return CONST.C / self.n_e

    @maxwell_cite(
        804, 805,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate retardation through crystal",
    )
    def retardation(self, thickness: float, wavelength: float) -> float:
        """
        Calculate phase retardation between o-ray and e-ray.

        Art. 804-805: The phase retardation after passing through
        crystal thickness d is:

            Γ = (2π / λ) * |Δn| * d

        Args:
            thickness: Crystal thickness d (cm).
            wavelength: Vacuum wavelength λ (cm).

        Returns:
            Phase retardation Γ (radians).

        Reference:
            Part IV, Arts. 804-805: Retardation.
        """
        if thickness <= 0:
            raise ValueError(f"Thickness must be positive")
        if wavelength <= 0:
            raise ValueError(f"Wavelength must be positive")

        return (2.0 * np.pi / wavelength) * abs(self.birefringence) * thickness

    @maxwell_cite(
        804,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate path difference",
    )
    def path_difference(self, thickness: float) -> float:
        """
        Calculate optical path difference between o-ray and e-ray.

        Art. 804: The path difference is:

            OPD = |Δn| * d

        Args:
            thickness: Crystal thickness (cm).

        Returns:
            Optical path difference (cm).

        Reference:
            Part IV, Art. 804: Path difference.
        """
        if thickness <= 0:
            raise ValueError(f"Thickness must be positive")

        return abs(self.birefringence) * thickness

    @maxwell_cite(
        804, 805,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate effective refractive index at angle",
    )
    def effective_index_at_angle(self, angle_from_optic_axis: float) -> float:
        """
        Calculate effective refractive index for e-ray at angle θ.

        Art. 805: For the extraordinary ray propagating at angle θ
        from the optic axis:

            1/n_eff(θ)² = cos²(θ)/n_o² + sin²(θ)/n_e²

        Args:
            angle_from_optic_axis: Angle θ (radians).

        Returns:
            Effective refractive index n_eff.

        Reference:
            Part IV, Art. 805: Angle-dependent refractive index.
        """
        theta = angle_from_optic_axis
        cos_sq = np.cos(theta) ** 2
        sin_sq = np.sin(theta) ** 2

        inv_n_sq = cos_sq / (self.n_o ** 2) + sin_sq / (self.n_e ** 2)

        return 1.0 / np.sqrt(inv_n_sq)

    @maxwell_cite(
        804,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate quarter-wave plate thickness",
    )
    def quarter_wave_thickness(self, wavelength: float) -> float:
        """
        Calculate thickness for quarter-wave plate.

        Art. 804: A quarter-wave plate produces Γ = π/2 retardation:

            d_λ/4 = λ / (4 * |Δn|)

        Args:
            wavelength: Design wavelength λ (cm).

        Returns:
            Quarter-wave plate thickness (cm).

        Reference:
            Part IV, Art. 804: Quarter-wave plate.
        """
        if wavelength <= 0:
            raise ValueError(f"Wavelength must be positive")
        if abs(self.birefringence) < 1e-15:
            raise ValueError("Crystal must be birefringent")

        return wavelength / (4.0 * abs(self.birefringence))

    @maxwell_cite(
        804,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate half-wave plate thickness",
    )
    def half_wave_thickness(self, wavelength: float) -> float:
        """
        Calculate thickness for half-wave plate.

        Art. 804: A half-wave plate produces Γ = π retardation:

            d_λ/2 = λ / (2 * |Δn|)

        Args:
            wavelength: Design wavelength λ (cm).

        Returns:
            Half-wave plate thickness (cm).

        Reference:
            Part IV, Art. 804: Half-wave plate.
        """
        if wavelength <= 0:
            raise ValueError(f"Wavelength must be positive")
        if abs(self.birefringence) < 1e-15:
            raise ValueError("Crystal must be birefringent")

        return wavelength / (2.0 * abs(self.birefringence))


@maxwell_cite(
    804,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Get crystal optical constants",
)
def get_crystal_constants(crystal_name: str) -> dict[str, float | str]:
    """
    Get optical constants for a birefringent crystal.

    Art. 804-805: Lookup table of refractive indices for common
    birefringent crystals.

    Args:
        crystal_name: Name of crystal (case-insensitive).

    Returns:
        Dictionary with:
        - n_o: Ordinary refractive index
        - n_e: Extraordinary refractive index
        - type: "positive" or "negative"
        - birefringence: Δn

    Raises:
        KeyError: If crystal not found.

    Reference:
        Part IV, Arts. 804-805: Crystal optical constants.

    Example:
        >>> constants = get_crystal_constants("calcite")
        >>> print(f"n_o = {constants['n_o']}, n_e = {constants['n_e']}")
        >>> print(f"Birefringence = {constants['birefringence']:.3f}")
    """
    crystal_key = crystal_name.lower().replace(" ", "_")
    if crystal_key not in CRYSTAL_OPTICAL_CONSTANTS:
        available = list(CRYSTAL_OPTICAL_CONSTANTS.keys())
        raise KeyError(f"Crystal '{crystal_name}' not found. Available: {available}")

    data = CRYSTAL_OPTICAL_CONSTANTS[crystal_key]
    return {
        "n_o": data["n_o"],
        "n_e": data["n_e"],
        "type": data["type"],
        "birefringence": data["n_e"] - data["n_o"],
    }


@maxwell_cite(
    804, 805,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate birefringence",
)
def calc_birefringence(n_o: float, n_e: float) -> float:
    """
    Calculate birefringence of crystal.

    Art. 804-805: Birefringence is the difference between
    extraordinary and ordinary refractive indices:

        Δn = n_e - n_o

    Positive crystals: Δn > 0 (n_e > n_o)
    Negative crystals: Δn < 0 (n_e < n_o)

    Args:
        n_o: Ordinary refractive index.
        n_e: Extraordinary refractive index.

    Returns:
        Birefringence Δn.

    Reference:
        Part IV, Arts. 804-805: Birefringence.

    Example:
        >>> # Calcite (negative crystal)
        >>> delta_n = calc_birefringence(1.658, 1.486)
        >>> print(f"Δn = {delta_n:.3f}")  # Δn = -0.172
    """
    return n_e - n_o


@maxwell_cite(
    804, 805,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate velocity difference between rays",
)
def calc_velocity_difference(n_o: float, n_e: float) -> float:
    """
    Calculate velocity difference between ordinary and extraordinary rays.

    Art. 804-805: The velocity difference is:

        Δv = v_o - v_e = c * (1/n_o - 1/n_e)

    Args:
        n_o: Ordinary refractive index.
        n_e: Extraordinary refractive index.

    Returns:
        Velocity difference Δv (cm/s).

    Reference:
        Part IV, Arts. 804-805: Velocity difference.
    """
    return CONST.C * (1.0 / n_o - 1.0 / n_e)


@maxwell_cite(
    804,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate retardation in waves",
)
def calc_retardation_waves(
    thickness: float,
    birefringence: float,
    wavelength: float,
) -> float:
    """
    Calculate retardation in number of waves.

    Art. 804: The retardation expressed in waves is:

        N = |Δn| * d / λ

    This is useful for counting interference fringes.

    Args:
        thickness: Crystal thickness (cm).
        birefringence: Δn (dimensionless).
        wavelength: Vacuum wavelength (cm).

    Returns:
        Retardation in waves (dimensionless).

    Reference:
        Part IV, Art. 804: Retardation in waves.
    """
    if thickness <= 0:
        raise ValueError(f"Thickness must be positive")
    if wavelength <= 0:
        raise ValueError(f"Wavelength must be positive")

    return abs(birefringence) * thickness / wavelength


@maxwell_cite(
    804, 805,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Verify crystal optics relations",
)
def verify_crystal_optics(
    n_o: float = 1.544,
    n_e: float = 1.553,
    wavelength: float = 589e-7,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify crystalline optics relationships.

    Art. 804-805: This function verifies:
    1. v = c/n for both rays
    2. Retardation formula
    3. Wave plate thickness formulas

    Args:
        n_o: Ordinary refractive index.
        n_e: Extraordinary refractive index.
        wavelength: Test wavelength (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 804-805: Crystal optics verification.
    """
    co = CrystalOptics(n_o=n_o, n_e=n_e)

    # Verify velocities
    v_o_expected = CONST.C / n_o
    v_e_expected = CONST.C / n_e

    v_o_error = abs(co.ordinary_velocity() - v_o_expected) / v_o_expected
    v_e_error = abs(co.extraordinary_velocity() - v_e_expected) / v_e_expected

    # Verify quarter-wave plate
    d_qwp = co.quarter_wave_thickness(wavelength)
    Gamma_qwp = co.retardation(d_qwp, wavelength)
    qwp_error = abs(Gamma_qwp - np.pi / 2) / (np.pi / 2)

    # Verify half-wave plate
    d_hwp = co.half_wave_thickness(wavelength)
    Gamma_hwp = co.retardation(d_hwp, wavelength)
    hwp_error = abs(Gamma_hwp - np.pi) / np.pi

    return {
        "n_o": n_o,
        "n_e": n_e,
        "birefringence": co.birefringence,
        "crystal_type": co.crystal_type,
        "v_ordinary": co.ordinary_velocity(),
        "v_extraordinary": co.extraordinary_velocity(),
        "v_o_error": v_o_error,
        "v_e_error": v_e_error,
        "quarter_wave_thickness": d_qwp,
        "quarter_wave_retardation": Gamma_qwp,
        "qwp_error": qwp_error,
        "half_wave_thickness": d_hwp,
        "half_wave_retardation": Gamma_hwp,
        "hwp_error": hwp_error,
        "verified": all([
            v_o_error < tolerance,
            v_e_error < tolerance,
            qwp_error < tolerance,
            hwp_error < tolerance,
        ]),
    }


@maxwell_cite(
    804, 805,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Complete crystal optics analysis",
)
def analyze_crystal_optics(
    crystal_name: str = None,
    n_o: float = None,
    n_e: float = None,
    wavelength: float = 589e-7,
    thickness: float = 0.01,
) -> dict[str, float | str]:
    """
    Complete analysis of crystal optical properties.

    Art. 804-805: Comprehensive analysis including:
    1. Refractive indices and birefringence
    2. Ray velocities
    3. Retardation for given thickness
    4. Quarter-wave and half-wave plate thicknesses
    5. Effective index vs angle

    Args:
        crystal_name: Optional crystal name for lookup.
        n_o: Ordinary refractive index (if not using crystal_name).
        n_e: Extraordinary refractive index (if not using crystal_name).
        wavelength: Wavelength for calculations (cm).
        thickness: Crystal thickness for retardation (cm).

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 804-805: Complete crystal optics analysis.

    Example:
        >>> # Analyze calcite at visible wavelengths
        >>> result = analyze_crystal_optics("calcite", wavelength=589e-7)
        >>> print(f"Δn = {result['birefringence']:.3f}")
        >>> print(f"v_o = {result['v_ordinary']:.4e} cm/s")
    """
    # Get crystal constants
    if crystal_name is not None:
        constants = get_crystal_constants(crystal_name)
        n_o = constants["n_o"]
        n_e = constants["n_e"]
    else:
        if n_o is None:
            n_o = 1.544
        if n_e is None:
            n_e = 1.553

    co = CrystalOptics(n_o=n_o, n_e=n_e)

    # Calculate angle-dependent effective index
    angles = np.linspace(0, np.pi / 2, 10)
    n_eff_values = [co.effective_index_at_angle(a) for a in angles]

    return {
        "crystal": crystal_name if crystal_name else "custom",
        "n_o": n_o,
        "n_e": n_e,
        "birefringence": co.birefringence,
        "crystal_type": co.crystal_type,
        "v_ordinary": co.ordinary_velocity(),
        "v_extraordinary": co.extraordinary_velocity(),
        "velocity_difference": calc_velocity_difference(n_o, n_e),
        "wavelength_cm": wavelength,
        "wavelength_nm": wavelength * 1e7,
        "thickness_cm": thickness,
        "retardation_radians": co.retardation(thickness, wavelength),
        "retardation_degrees": np.degrees(co.retardation(thickness, wavelength)),
        "retardation_waves": calc_retardation_waves(thickness, co.birefringence, wavelength),
        "quarter_wave_thickness_cm": co.quarter_wave_thickness(wavelength),
        "half_wave_thickness_cm": co.half_wave_thickness(wavelength),
        "n_eff_min": min(n_eff_values),
        "n_eff_max": max(n_eff_values),
        "n_eff_range": max(n_eff_values) - min(n_eff_values),
    }

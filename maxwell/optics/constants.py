"""maxwell.optics.constants — Optical constants and properties (Arts. 788-790).

Implements Maxwell's treatment of optical constants including refractive indices,
dispersion relations, and material optical properties.

Maxwell's CGS formulation (Arts. 788-790):
    Refractive index:
        n = c / v = sqrt(ε_r * μ_r)

    Dispersion (wavelength-dependent refractive index):
        n(λ) varies with wavelength due to material response

    Optical density:
        Related to refractive index by n = c / v

    Specific inductive capacity (dielectric constant):
        K = ε_r ≈ n² (for non-magnetic materials)

where:
    n = refractive index (dimensionless)
    c = speed of light in vacuum (cm/s)
    v = wave velocity in medium (cm/s)
    ε_r = relative permittivity
    μ_r = relative permeability
    K = specific inductive capacity

Category: A (maxwell_original) — Maxwell's optical constants theory.

References:
    Part IV, Arts. 788-790: Optical constants and material properties.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite

# Standard optical constants for common materials (at visible wavelengths)
# Refractive indices at λ ≈ 589 nm (sodium D line)
OPTICAL_CONSTANTS = {
    # Vacuum and gases
    "vacuum": {"n": 1.0, "eps_r": 1.0, "mu_r": 1.0},
    "air": {"n": 1.000293, "eps_r": 1.000586, "mu_r": 1.0},
    # Liquids
    "water": {"n": 1.333, "eps_r": 1.777, "mu_r": 1.0},
    "ethanol": {"n": 1.361, "eps_r": 1.852, "mu_r": 1.0},
    "benzene": {"n": 1.501, "eps_r": 2.253, "mu_r": 1.0},
    "carbon_disulfide": {"n": 1.628, "eps_r": 2.650, "mu_r": 1.0},
    # Solids (optical glasses)
    "crown_glass": {"n": 1.52, "eps_r": 2.31, "mu_r": 1.0},
    "flint_glass": {"n": 1.66, "eps_r": 2.76, "mu_r": 1.0},
    "fused_silica": {"n": 1.458, "eps_r": 2.13, "mu_r": 1.0},
    # Crystals
    "quartz": {"n": 1.544, "eps_r": 2.38, "mu_r": 1.0},
    "calcite": {"n_o": 1.658, "n_e": 1.486, "eps_r": 2.75, "mu_r": 1.0},
    "diamond": {"n": 2.417, "eps_r": 5.84, "mu_r": 1.0},
    # Semiconductors
    "silicon": {"n": 3.48, "eps_r": 12.1, "mu_r": 1.0},
    "germanium": {"n": 4.0, "eps_r": 16.0, "mu_r": 1.0},
}

# Wavelength ranges for optical spectrum (in cm, CGS)
WAVELENGTH_RANGES = {
    "ultraviolet": (1e-7, 4e-7),  # 100-400 nm
    "visible": (4e-7, 7e-7),  # 400-700 nm
    "infrared": (7e-7, 1e-3),  # 700 nm - 1 mm
    "near_ir": (7e-7, 2.5e-4),  # 700 nm - 2.5 μm
    "mid_ir": (2.5e-4, 2.5e-3),  # 2.5-25 μm
    "far_ir": (2.5e-3, 1e-3),  # 25 μm - 1 mm
}


@maxwell_cite(
    788,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate refractive index from dielectric constant",
)
def calc_refractive_from_dielectric(K: float) -> float:
    """
    Calculate refractive index from dielectric constant.

    Art. 788: Maxwell's relation:

        n = sqrt(K)

    where K is the specific inductive capacity (dielectric constant).

    Args:
        K: Dielectric constant (dimensionless).

    Returns:
        Refractive index n (dimensionless).

    Reference:
        Part IV, Art. 788: Refractive from dielectric.

    Example:
        >>> n = calc_refractive_from_dielectric(2.25)
        >>> print(f"n = {n:.2f}")  # n = 1.5
    """
    if K <= 0:
        raise ValueError(f"Dielectric constant must be positive, got {K}")
    return np.sqrt(K)


@maxwell_cite(
    788,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate dielectric constant from refractive index",
)
def calc_dielectric_from_refractive(n: float) -> float:
    """
    Calculate dielectric constant from refractive index.

    Art. 788: Inverse of Maxwell's relation:

        K = n²

    Args:
        n: Refractive index (dimensionless).

    Returns:
        Dielectric constant K (dimensionless).

    Reference:
        Part IV, Art. 788: Dielectric from refractive.

    Example:
        >>> K = calc_dielectric_from_refractive(1.5)
        >>> print(f"K = {K:.2f}")  # K = 2.25
    """
    if n <= 0:
        raise ValueError(f"Refractive index must be positive, got {n}")
    return n**2


@maxwell_cite(
    789,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate dispersion (wavelength-dependent n)",
)
def calc_dispersion(omega: float, omega_0: float) -> float:
    """
    Calculate refractive index with simple dispersion model.

    Art. 789: Simple dispersion model (normal dispersion):

        n(omega) = n_base + A * (omega / omega_0)^2

    For omega < omega_0, n increases with frequency (normal dispersion).

    Args:
        omega: Angular frequency of light (rad/s).
        omega_0: Reference frequency for normalization (rad/s).

    Returns:
        Refractive index n at frequency omega (dimensionless).

    Reference:
        Part IV, Art. 789: Dispersion relation.

    Example:
        >>> n1 = calc_dispersion(5e14, 6e14)
        >>> n2 = calc_dispersion(7e14, 6e14)
        >>> print(f"n2 > n1: {n2 > n1}")  # True (normal dispersion)
    """
    if omega_0 <= 0:
        raise ValueError(f"Resonant frequency must be positive")

    # Simple normal dispersion model: n increases with frequency
    # n = n_base + A * (omega / omega_0)^2
    n_base = 1.0
    A = 0.1

    return n_base + A * (omega / omega_0) ** 2


@dataclass
class OpticalConstants:
    """
    Optical constants calculator for materials.

    Art. 788-790: Maxwell established the connection between optical
    and electromagnetic properties of materials.

    Attributes:
        refractive_index: Refractive index n (dimensionless).
        permittivity: Relative permittivity ε_r.
        permeability: Relative permeability μ_r.
        material_name: Optional material name for lookup.
    """

    refractive_index: Optional[float] = None
    permittivity: Optional[float] = None
    permeability: Optional[float] = None
    material_name: Optional[str] = None

    def __post_init__(self):
        """Initialize from material name or validate parameters."""
        if (
            self.material_name is not None
            and self.material_name.lower() in OPTICAL_CONSTANTS
        ):
            constants = OPTICAL_CONSTANTS[self.material_name.lower()]
            if self.refractive_index is None:
                self.refractive_index = constants.get("n", 1.0)
            if self.permittivity is None:
                self.permittivity = constants.get("eps_r", 1.0)
            if self.permeability is None:
                self.permeability = constants.get("mu_r", 1.0)

        # Calculate missing values from n = sqrt(ε_r * μ_r)
        if (
            self.refractive_index is None
            and self.permittivity is not None
            and self.permeability is not None
        ):
            self.refractive_index = np.sqrt(self.permittivity * self.permeability)

        if (
            self.permittivity is None
            and self.refractive_index is not None
            and self.permeability is not None
        ):
            self.permittivity = (self.refractive_index**2) / self.permeability

        # Validate
        if self.refractive_index is not None and self.refractive_index <= 0:
            raise ValueError(
                f"Refractive index must be positive, got {self.refractive_index}"
            )
        if self.permittivity is not None and self.permittivity <= 0:
            raise ValueError(f"Permittivity must be positive, got {self.permittivity}")
        if self.permeability is not None and self.permeability <= 0:
            raise ValueError(f"Permeability must be positive, got {self.permeability}")

        # Set defaults
        if self.refractive_index is None:
            self.refractive_index = 1.0
        if self.permittivity is None:
            self.permittivity = 1.0
        if self.permeability is None:
            self.permeability = 1.0

    @maxwell_cite(
        788,
        part=4,
        chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate wave velocity in material",
    )
    def wave_velocity(self) -> float:
        """
        Calculate wave propagation velocity.

        Art. 788: v = c / n

        Returns:
            Wave velocity (cm/s).

        Reference:
            Part IV, Art. 788: Wave velocity.
        """
        return CONST.C / self.refractive_index

    @maxwell_cite(
        789,
        part=4,
        chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate optical path length",
    )
    def optical_path_length(self, physical_length: float) -> float:
        """
        Calculate optical path length.

        Art. 789: The optical path length is:

            OPL = n * L

        where L is the physical path length.

        Args:
            physical_length: Physical distance (cm).

        Returns:
            Optical path length (cm).

        Reference:
            Part IV, Art. 789: Optical path length.
        """
        if physical_length < 0:
            raise ValueError(f"Physical length must be non-negative")
        return self.refractive_index * physical_length

    @maxwell_cite(
        790,
        part=4,
        chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate wavelength in material",
    )
    def wavelength_in_material(self, vacuum_wavelength: float) -> float:
        """
        Calculate wavelength inside the material.

        Art. 790: λ = λ_0 / n

        Args:
            vacuum_wavelength: Wavelength in vacuum (cm).

        Returns:
            Wavelength in material (cm).

        Reference:
            Part IV, Art. 790: Wavelength in medium.
        """
        if vacuum_wavelength <= 0:
            raise ValueError(f"Wavelength must be positive")
        return vacuum_wavelength / self.refractive_index

    @maxwell_cite(
        788,
        part=4,
        chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate specific inductive capacity",
    )
    def specific_inductive_capacity(self) -> float:
        """
        Calculate Maxwell's specific inductive capacity (dielectric constant).

        Art. 788: For non-magnetic materials:

            K = ε_r = n²

        Returns:
            Specific inductive capacity K (dimensionless).

        Reference:
            Part IV, Art. 788: Specific inductive capacity.
        """
        return self.permittivity

    @maxwell_cite(
        788,
        part=4,
        chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate refractive index from dielectric constant",
    )
    def refractive_from_dielectric(self, K: float) -> float:
        """
        Calculate refractive index from dielectric constant.

        Art. 788: n = sqrt(K)

        Args:
            K: Dielectric constant (dimensionless).

        Returns:
            Refractive index n (dimensionless).

        Reference:
            Part IV, Art. 788: Refractive from dielectric.
        """
        return calc_refractive_from_dielectric(K)

    @maxwell_cite(
        788,
        part=4,
        chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate dielectric constant from refractive index",
    )
    def dielectric_from_refractive(self, n: float) -> float:
        """
        Calculate dielectric constant from refractive index.

        Art. 788: K = n²

        Args:
            n: Refractive index (dimensionless).

        Returns:
            Dielectric constant K (dimensionless).

        Reference:
            Part IV, Art. 788: Dielectric from refractive.
        """
        return calc_dielectric_from_refractive(n)


@maxwell_cite(
    788,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Get optical constants for material",
)
def get_optical_constants(material_name: str) -> dict[str, float]:
    """
    Get optical constants for a known material.

    Art. 788: Lookup table of refractive indices and related properties
    for common optical materials at visible wavelengths.

    Args:
        material_name: Name of material (case-insensitive).

    Returns:
        Dictionary with optical constants:
        - n: Refractive index
        - eps_r: Relative permittivity
        - mu_r: Relative permeability
        - v: Wave velocity (cm/s)

    Raises:
        KeyError: If material is not found.

    Reference:
        Part IV, Art. 788: Optical constants.

    Example:
        >>> constants = get_optical_constants("water")
        >>> print(f"n = {constants['n']:.3f}")  # n = 1.333
        >>> print(f"v = {constants['v']:.4e} cm/s")
    """
    material_key = material_name.lower()
    if material_key not in OPTICAL_CONSTANTS:
        available = list(OPTICAL_CONSTANTS.keys())
        raise KeyError(f"Material '{material_name}' not found. Available: {available}")

    constants = OPTICAL_CONSTANTS[material_key].copy()
    constants["v"] = CONST.C / constants["n"]

    return constants


@maxwell_cite(
    788,
    789,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate refractive index from electromagnetic properties",
)
def calc_refractive_index_from_EM(
    permittivity: float,
    permeability: float = 1.0,
) -> float:
    """
    Calculate refractive index from electromagnetic properties.

    Art. 788-789: Maxwell's fundamental relation:

        n = sqrt(ε_r * μ_r)

    For non-magnetic materials (μ_r ≈ 1):

        n ≈ sqrt(ε_r)

    This connects optics with electromagnetism.

    Args:
        permittivity: Relative permittivity ε_r.
        permeability: Relative permeability μ_r (default: 1.0).

    Returns:
        Refractive index n (dimensionless).

    Reference:
        Part IV, Arts. 788-789: Refractive index from EM properties.

    Example:
        >>> # Water: ε_r ≈ 1.777 at optical frequencies
        >>> n = calc_refractive_index_from_EM(1.777)
        >>> print(f"n = {n:.3f}")  # n ≈ 1.333
    """
    if permittivity <= 0:
        raise ValueError(f"Permittivity must be positive, got {permittivity}")
    if permeability <= 0:
        raise ValueError(f"Permeability must be positive, got {permeability}")

    return np.sqrt(permittivity * permeability)


@maxwell_cite(
    790,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate frequency from wavelength",
)
def calc_frequency_from_wavelength(
    vacuum_wavelength: float,
) -> float:
    """
    Calculate frequency from vacuum wavelength.

    Art. 790: The frequency is:

        ν = c / λ_0

    Frequency is invariant across media boundaries.

    Args:
        vacuum_wavelength: Wavelength in vacuum (cm).

    Returns:
        Frequency ν (Hz).

    Reference:
        Part IV, Art. 790: Frequency-wavelength relation.

    Example:
        >>> # Green light: λ = 530 nm
        >>> nu = calc_frequency_from_wavelength(530e-7)
        >>> print(f"ν = {nu:.2e} Hz")
    """
    if vacuum_wavelength <= 0:
        raise ValueError(f"Wavelength must be positive")

    return CONST.C / vacuum_wavelength


@maxwell_cite(
    790,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate wavelength from frequency",
)
def calc_wavelength_from_frequency(
    frequency: float,
    refractive_index: float = 1.0,
) -> float:
    """
    Calculate wavelength from frequency.

    Art. 790: The wavelength in a medium is:

        λ = v / ν = c / (n * ν)

    In vacuum (n = 1):

        λ_0 = c / ν

    Args:
        frequency: Frequency ν (Hz).
        refractive_index: Refractive index n (default: 1.0).

    Returns:
        Wavelength λ (cm).

    Reference:
        Part IV, Art. 790: Wavelength from frequency.

    Example:
        >>> # Green light: ν = 5.66e14 Hz
        >>> lambda_0 = calc_wavelength_from_frequency(5.66e14)
        >>> print(f"λ_0 = {lambda_0*1e7:.1f} nm")
    """
    if frequency <= 0:
        raise ValueError(f"Frequency must be positive")
    if refractive_index <= 0:
        raise ValueError(f"Refractive index must be positive")

    return CONST.C / (refractive_index * frequency)


@maxwell_cite(
    789,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate optical path difference",
)
def calc_optical_path_difference(
    n1: float,
    n2: float,
    physical_thickness: float,
) -> float:
    """
    Calculate optical path difference between two media.

    Art. 789: For light passing through thickness L in two different media:

        OPD = (n2 - n1) * L

    This is fundamental to interference phenomena.

    Args:
        n1: Refractive index of first medium.
        n2: Refractive index of second medium.
        physical_thickness: Physical thickness (cm).

    Returns:
        Optical path difference (cm).

    Reference:
        Part IV, Art. 789: Optical path difference.

    Example:
        >>> # Thin film: glass (n=1.5) in air (n=1.0), thickness 1 μm
        >>> OPD = calc_optical_path_difference(1.0, 1.5, 1e-4)
        >>> print(f"OPD = {OPD*1e7:.1f} nm")  # OPD = 500 nm
    """
    if physical_thickness < 0:
        raise ValueError(f"Thickness must be non-negative")

    return (n2 - n1) * physical_thickness


@maxwell_cite(
    788,
    789,
    790,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Classify spectral region from wavelength",
)
def classify_spectral_region(wavelength: float) -> str:
    """
    Classify wavelength into spectral region.

    Art. 788-790: Classification of electromagnetic spectrum:
    - Ultraviolet: 100-400 nm
    - Visible: 400-700 nm
    - Infrared: 700 nm - 1 mm
      - Near IR: 700 nm - 2.5 μm
      - Mid IR: 2.5-25 μm
      - Far IR: 25 μm - 1 mm

    Args:
        wavelength: Wavelength in vacuum (cm).

    Returns:
        Spectral region classification string.

    Reference:
        Part IV, Arts. 788-790: Spectral classification.

    Example:
        >>> region = classify_spectral_region(550e-7)  # 550 nm
        >>> print(region)  # "visible"
    """
    if wavelength <= 0:
        return "invalid"

    wavelength_nm = wavelength * 1e7  # Convert to nm

    if wavelength_nm < 100:
        return "extreme_ultraviolet"
    elif wavelength_nm < 400:
        return "ultraviolet"
    elif wavelength_nm < 700:
        return "visible"
    elif wavelength_nm < 2500:
        return "near_infrared"
    elif wavelength_nm < 25000:
        return "mid_infrared"
    elif wavelength_nm < 1000000:
        return "far_infrared"
    else:
        return "terahertz_microwave"


@maxwell_cite(
    788,
    789,
    790,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Verify optical constant relations",
)
def verify_optical_constants(
    refractive_index: float = 1.5,
    permittivity: float = None,
    permeability: float = 1.0,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify optical constant relationships.

    Art. 788-790: This function verifies:
    1. n = sqrt(ε_r * μ_r)
    2. v = c / n
    3. λ = λ_0 / n
    4. ε_r = n² (for μ_r = 1)

    Args:
        refractive_index: Refractive index n.
        permittivity: Relative permittivity ε_r (default: n²).
        permeability: Relative permeability μ_r (default: 1.0).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 788-790: Optical constant verification.
    """
    if permittivity is None:
        permittivity = refractive_index**2

    # Calculate expected values
    n_expected = np.sqrt(permittivity * permeability)
    v = CONST.C / refractive_index
    eps_from_n = (refractive_index**2) / permeability

    # Calculate errors
    n_error = (
        abs(n_expected - refractive_index) / refractive_index
        if refractive_index > 0
        else 0
    )
    eps_error = abs(eps_from_n - permittivity) / permittivity if permittivity > 0 else 0

    # Velocity verification
    v_check = CONST.C / n_expected
    v_error = abs(v - v_check) / v if v > 0 else 0

    return {
        "refractive_index": refractive_index,
        "permittivity": permittivity,
        "permeability": permeability,
        "n_from_formula": n_expected,
        "velocity": v,
        "eps_from_n": eps_from_n,
        "n_error": n_error,
        "eps_error": eps_error,
        "v_error": v_error,
        "verified": all(
            [
                n_error < tolerance,
                eps_error < tolerance,
                v_error < tolerance,
            ]
        ),
    }


@maxwell_cite(
    788,
    789,
    790,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Complete optical constants analysis",
)
def analyze_optical_constants(
    material_name: str = None,
    refractive_index: float = None,
    wavelength_vacuum: float = None,
) -> dict[str, float]:
    """
    Complete analysis of optical constants.

    Art. 788-790: Comprehensive analysis including:
    1. Refractive index and related properties
    2. Wave velocity
    3. Wavelength in material
    4. Optical path length per cm
    5. Spectral region classification

    Args:
        material_name: Optional material name for lookup.
        refractive_index: Refractive index (default: 1.0 or from material).
        wavelength_vacuum: Optional vacuum wavelength (cm).

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 788-790: Complete optical analysis.

    Example:
        >>> # Analyze water at green light
        >>> result = analyze_optical_constants("water", wavelength_vacuum=530e-7)
        >>> print(f"λ_water = {result['wavelength_in_material']*1e7:.1f} nm")
    """
    # Get refractive index
    if material_name is not None and material_name.lower() in OPTICAL_CONSTANTS:
        constants = get_optical_constants(material_name)
        n = constants["n"]
        eps_r = constants["eps_r"]
        mu_r = constants["mu_r"]
    else:
        n = refractive_index if refractive_index is not None else 1.0
        eps_r = n**2
        mu_r = 1.0

    # Calculate properties
    velocity = CONST.C / n
    specific_inductive_capacity = eps_r

    result = {
        "material": material_name if material_name else "custom",
        "refractive_index": n,
        "permittivity": eps_r,
        "permeability": mu_r,
        "wave_velocity": velocity,
        "velocity_ratio_to_c": velocity / CONST.C,
        "specific_inductive_capacity": specific_inductive_capacity,
        "spectral_region": None,
    }

    if wavelength_vacuum is not None:
        wavelength_material = wavelength_vacuum / n
        frequency = CONST.C / wavelength_vacuum

        result["wavelength_vacuum"] = wavelength_vacuum
        result["wavelength_in_material"] = wavelength_material
        result["frequency"] = frequency
        result["spectral_region"] = classify_spectral_region(wavelength_vacuum)
        result["wavelength_shift"] = wavelength_vacuum - wavelength_material

    return result

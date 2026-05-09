"""
Dielectrics and Electrification — Maxwell's Part I, Chapters VII–VIII.

This module implements Maxwell's theory of dielectrics and electrification:

1. **Dielectric Theory** (Arts. 157–164):
   - Specific inductive capacity (dielectric constant / relative permittivity)
   - Dielectric polarization and electric susceptibility
   - Bound charge density and surface bound charge
   - Electric displacement (dielectric displacement)

2. **Electrification Theory** (Arts. 165–170):
   - Electrification by friction (triboelectric effect)
   - Electrification by contact (contact potential)
   - Electrification by induction (charging by induction)
   - Charge distribution on conductors

Maxwell's key insight (Art. 164): The electric displacement D is the
fundamental field in dielectrics, related to the electric field E by
the specific inductive capacity K (relative permittivity ε_r):

    D = ε_0 * K * E = ε_0 * E + P

where P is the polarization vector.

CGS-ESU units are used throughout, following Maxwell's conventions:
    - Electric field: statvolts/cm (dyne/statcoulomb)
    - Electric displacement: statcoulombs/cm²
    - Polarization: statcoulombs/cm²
    - Permittivity: dimensionless (relative to vacuum)
    - Charge: statcoulombs (esu)

Category: A (maxwell_original) — Maxwell's theory of dielectrics.

References:
    Part I, Chapter VII: Theory of Dielectrics (Arts. 157–164).
    Part I, Chapter VIII: Electrification (Arts. 165–170).
    Part II, Chapter X: Conduction in Dielectric Media (Arts. 325–334).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from maxwell.config.constants import CONST, C
from maxwell.meta.citation import maxwell_cite

# =============================================================================
# SPECIFIC INDUCTIVE CAPACITY (Arts. 157–159)
# =============================================================================


@maxwell_cite(
    157,
    158,
    159,
    part=1,
    chapter="Theory of Dielectrics",
    theory_class="maxwell_original",
    description="Specific inductive capacity (dielectric constant)",
)
def specific_inductive_capacity(
    material: str = None,
    relative_permittivity: float = None,
    temperature: float = 293.15,
    frequency: float = None,
) -> dict[str, float]:
    """
    Specific inductive capacity — Maxwell's term for relative permittivity.

    Arts. 157–159: Maxwell introduced the concept of specific inductive
    capacity (K), now called relative permittivity (ε_r). This is the
    ratio of the capacitance of a capacitor filled with the dielectric
    to the capacitance of the same capacitor with vacuum.

        K = ε_r = ε / ε_0

    Maxwell's key discovery: K > 1 for all material dielectrics,
    typically ranging from ~2 for paraffin to ~80 for water.

    The specific inductive capacity depends on:
        - Material composition and molecular structure
        - Temperature (generally decreases with increasing T)
        - Frequency (decreases at high frequency as polarization lags)
        - Moisture content and impurities

    Args:
        material: Optional material name for lookup (e.g., "glass", "water").
        relative_permittivity: K value (dimensionless). If None, looked up.
        temperature: Temperature in Kelvin (default: 293.15 K = 20°C).
        frequency: Optional frequency in Hz (for dispersion).

    Returns:
        Dictionary with:
        - specific_inductive_capacity: K = ε_r (dimensionless)
        - absolute_permittivity: ε = K * ε_0 (in CGS-ESU: statfarad/cm)
        - material: Material name if provided
        - temperature: Temperature (K)
        - frequency: Frequency if provided (Hz)

    Raises:
        ValueError: If material not found and no K provided.

    References:
        Part I, Art. 157: Definition of specific inductive capacity.
        Part I, Art. 158: Experimental determination.
        Part I, Art. 159: Values for various substances.

    Example:
        >>> result = specific_inductive_capacity(material="glass")
        >>> print(f"K = {result['specific_inductive_capacity']}")

        >>> result = specific_inductive_capacity(relative_permittivity=2.5)
        >>> print(f"ε = {result['absolute_permittivity']:.4e} statF/cm")
    """
    # Material property database (values at 20°C, low frequency)
    # Sources: Maxwell's experimental data, modern handbooks
    material_database = {
        # Solids
        "glass": {"K": 5.0, "temp_coeff": -0.001},
        "mica": {"K": 6.0, "temp_coeff": 0.0005},
        "quartz": {"K": 4.5, "temp_coeff": 0.0001},
        "fused_quartz": {"K": 3.78, "temp_coeff": 0.0001},
        "paraffin": {"K": 2.2, "temp_coeff": -0.002},
        "ebonite": {"K": 2.7, "temp_coeff": -0.001},
        "gutta_percha": {"K": 2.5, "temp_coeff": -0.002},
        "shellac": {"K": 3.0, "temp_coeff": -0.001},
        "sulfur": {"K": 4.0, "temp_coeff": 0.001},
        "resin": {"K": 2.5, "temp_coeff": -0.001},
        "wax": {"K": 2.3, "temp_coeff": -0.002},
        "ivory": {"K": 3.5, "temp_coeff": -0.001},
        "diamond": {"K": 5.7, "temp_coeff": 0.0001},
        "amber": {"K": 2.8, "temp_coeff": -0.001},
        "gutta_percha": {"K": 2.5, "temp_coeff": -0.002},
        "paper": {"K": 3.5, "temp_coeff": -0.001},
        "silk": {"K": 4.0, "temp_coeff": -0.001},
        "wood_dry": {"K": 2.5, "temp_coeff": -0.001},
        "porcelain": {"K": 6.0, "temp_coeff": 0.001},
        "ceramic": {"K": 7.0, "temp_coeff": 0.002},
        # Liquids
        "water": {"K": 80.4, "temp_coeff": -0.004},  # At 20°C
        "alcohol_ethanol": {"K": 24.3, "temp_coeff": -0.003},
        "alcohol_methanol": {"K": 32.7, "temp_coeff": -0.003},
        "benzene": {"K": 2.28, "temp_coeff": -0.002},
        "turpentine": {"K": 2.23, "temp_coeff": -0.002},
        "olive_oil": {"K": 3.1, "temp_coeff": -0.002},
        "castor_oil": {"K": 4.8, "temp_coeff": -0.002},
        "petroleum": {"K": 2.1, "temp_coeff": -0.002},
        "kerosene": {"K": 2.1, "temp_coeff": -0.002},
        # Gases (at STP)
        "air": {"K": 1.00059, "temp_coeff": 0},
        "nitrogen": {"K": 1.00058, "temp_coeff": 0},
        "oxygen": {"K": 1.00050, "temp_coeff": 0},
        "hydrogen": {"K": 1.00026, "temp_coeff": 0},
        "carbon_dioxide": {"K": 1.00092, "temp_coeff": 0},
        "helium": {"K": 1.00007, "temp_coeff": 0},
        # Vacuum
        "vacuum": {"K": 1.0, "temp_coeff": 0},
    }

    result = {
        "temperature": temperature,
        "frequency": frequency,
        "material": material,
    }

    # Lookup material
    if material and material.lower() in material_database:
        props = material_database[material.lower()]
        if relative_permittivity is None:
            relative_permittivity = props["K"]
        # Temperature correction (linear approximation)
        delta_T = temperature - 293.15  # Deviation from 20°C
        if "temp_coeff" in props:
            relative_permittivity *= 1 + props["temp_coeff"] * delta_T
        result["temp_correction"] = delta_T * props.get("temp_coeff", 0)

    if relative_permittivity is None:
        raise ValueError(
            "Either material name or relative_permittivity must be provided"
        )

    # Absolute permittivity in CGS-ESU (ε_0 = 1/4π in ESU, but often normalized to 1)
    # In Maxwell's convention, ε_0 = 1 for ESU
    epsilon_0_esu = 1.0  # In statfarad/cm
    absolute_permittivity = epsilon_0_esu * relative_permittivity

    result["specific_inductive_capacity"] = relative_permittivity
    result["absolute_permittivity"] = absolute_permittivity
    result["epsilon_0"] = epsilon_0_esu

    return result


@maxwell_cite(
    157,
    158,
    159,
    part=1,
    chapter="Theory of Dielectrics",
    theory_class="maxwell_original",
    description="Table of specific inductive capacities",
)
def table_specific_inductive_capacities() -> dict[str, float]:
    """
    Return a table of specific inductive capacities for common materials.

    Arts. 157–159: Maxwell compiled experimental values of K for
    numerous substances, establishing that:
        - All material dielectrics have K > 1
        - Values range from ~1 (gases) to ~80 (water)
        - K is approximately constant for moderate field strengths

    Returns:
        Dictionary mapping material names to their K values at 20°C.

    References:
        Part I, Art. 159: Table of specific inductive capacities.
    """
    return {
        # Gases (K ≈ 1)
        "vacuum": 1.0,
        "air": 1.00059,
        "helium": 1.00007,
        "hydrogen": 1.00026,
        "nitrogen": 1.00058,
        "oxygen": 1.00050,
        "carbon_dioxide": 1.00092,
        # Solids (2 < K < 10)
        "paraffin": 2.2,
        "wax": 2.3,
        "ebonite": 2.7,
        "amber": 2.8,
        "shellac": 3.0,
        "sulfur": 4.0,
        "quartz": 4.5,
        "glass": 5.0,
        "diamond": 5.7,
        "mica": 6.0,
        "porcelain": 6.0,
        # Liquids
        "benzene": 2.28,
        "turpentine": 2.23,
        "olive_oil": 3.1,
        "castor_oil": 4.8,
        "alcohol_ethanol": 24.3,
        "alcohol_methanol": 32.7,
        "water": 80.4,
    }


# =============================================================================
# DIELECTRIC POLARIZATION (Arts. 160–161)
# =============================================================================


@maxwell_cite(
    160,
    161,
    part=1,
    chapter="Theory of Dielectrics",
    theory_class="maxwell_original",
    description="Dielectric polarization P = χ_e * E",
)
def dielectric_polarization(
    electric_field: np.ndarray,
    susceptibility: float = None,
    relative_permittivity: float = None,
) -> dict[str, np.ndarray | float]:
    """
    Calculate dielectric polarization from electric field.

    Arts. 160–161: Maxwell defined polarization as the electric dipole
    moment per unit volume induced in a dielectric by an applied field.

    For linear isotropic dielectrics:

        P = χ_e * ε_0 * E

    where χ_e is the electric susceptibility, related to K by:

        K = 1 + χ_e  (in SI)
        K = 1 + 4π * χ_e  (in CGS-ESU with Gaussian convention)

    In the Heaviside-Lorentz convention used here:

        P = (K - 1) * E  (CGS-ESU, with ε_0 = 1)

    Maxwell described polarization as an "electric strain" in the
    dielectric medium, analogous to elastic deformation.

    Args:
        electric_field: Electric field vector E (statvolts/cm).
        susceptibility: Electric susceptibility χ_e (dimensionless).
        relative_permittivity: K (alternative to susceptibility).

    Returns:
        Dictionary with:
        - polarization: P vector (statcoulombs/cm²)
        - polarization_magnitude: |P| (statcoulombs/cm²)
        - electric_field: Input E field
        - susceptibility: χ_e used
        - relative_permittivity: K used

    Raises:
        ValueError: If neither susceptibility nor K provided.

    References:
        Part I, Art. 160: Theory of polarization.
        Part I, Art. 161: Relation to electric displacement.

    Example:
        >>> E = np.array([100, 0, 0])  # 100 statV/cm
        >>> result = dielectric_polarization(E, relative_permittivity=2.5)
        >>> print(f"P = {result['polarization']} statC/cm²")
    """
    electric_field = np.asarray(electric_field, dtype=np.float64)

    if susceptibility is None and relative_permittivity is None:
        raise ValueError("Either susceptibility or relative_permittivity required")

    if susceptibility is None:
        # χ_e = K - 1 (in this convention)
        susceptibility = relative_permittivity - 1

    # P = χ_e * E (in CGS-ESU with ε_0 = 1)
    polarization = susceptibility * electric_field
    polarization_magnitude = np.linalg.norm(polarization)

    return {
        "polarization": polarization,
        "polarization_magnitude": polarization_magnitude,
        "electric_field": electric_field,
        "susceptibility": susceptibility,
        "relative_permittivity": (
            susceptibility + 1 if susceptibility is not None else None
        ),
    }


@maxwell_cite(
    160,
    161,
    162,
    part=1,
    chapter="Theory of Dielectrics",
    theory_class="maxwell_original",
    description="Electric susceptibility χ_e",
)
def electric_susceptibility(
    relative_permittivity: float = None,
    material: str = None,
) -> dict[str, float]:
    """
    Calculate electric susceptibility from specific inductive capacity.

    Arts. 160–162: The electric susceptibility χ_e measures how easily
    a dielectric polarizes in response to an electric field.

    Relation to specific inductive capacity:

        χ_e = K - 1  (in CGS-ESU with ε_0 = 1)

    For vacuum: K = 1, so χ_e = 0 (no polarization).
    For air: K ≈ 1.0006, so χ_e ≈ 0.0006 (very weak polarization).
    For water: K ≈ 80, so χ_e ≈ 79 (strong polarization).

    Args:
        relative_permittivity: K value (dimensionless).
        material: Material name for lookup.

    Returns:
        Dictionary with:
        - susceptibility: χ_e (dimensionless)
        - relative_permittivity: K
        - material: Material name if provided

    References:
        Part I, Art. 160: Definition of susceptibility.
        Part I, Art. 162: Relation to bound charge.
    """
    if material is not None:
        result = specific_inductive_capacity(material=material)
        relative_permittivity = result["specific_inductive_capacity"]

    if relative_permittivity is None:
        raise ValueError("Either relative_permittivity or material required")

    susceptibility = relative_permittivity - 1

    return {
        "susceptibility": susceptibility,
        "relative_permittivity": relative_permittivity,
        "material": material,
    }


# =============================================================================
# BOUND CHARGE (Arts. 162–163)
# =============================================================================


@maxwell_cite(
    162,
    part=1,
    chapter="Theory of Dielectrics",
    theory_class="maxwell_original",
    description="Bound charge density ρ_bound = -∇·P",
)
def bound_charge_density(
    polarization_field: callable,
    position: np.ndarray,
    h: float = 1e-5,
) -> dict[str, float | np.ndarray]:
    """
    Calculate bound (polarization) charge density from polarization.

    Art. 162: Maxwell showed that a non-uniform polarization produces
    a volume density of bound charge:

        ρ_bound = -∇ · P = -(∂P_x/∂x + ∂P_y/∂y + ∂P_z/∂z)

    This "bound" charge is not free to move; it arises from the
    divergence of the polarization field. Positive divergence
    corresponds to a net negative bound charge (excess of - ends).

    The bound charge density is computed numerically using finite
    differences for the divergence.

    Args:
        polarization_field: Function P(r) returning polarization vector
                          at position r (statcoulombs/cm²).
        position: Position vector r (cm) where ρ_bound is computed.
        h: Finite difference step size (cm).

    Returns:
        Dictionary with:
        - bound_charge_density: ρ_bound (statcoulombs/cm³)
        - position: Position where computed
        - divergence_P: ∇ · P at the position

    Raises:
        ValueError: If polarization field returns invalid shape.

    References:
        Part I, Art. 162: Bound charge from polarization divergence.

    Example:
        >>> # Uniform polarization (should give ρ_bound = 0)
        >>> def P_uniform(r):
        ...     return np.array([1, 0, 0])
        >>> result = bound_charge_density(P_uniform, np.array([0, 0, 0]))
        >>> print(f"ρ_bound = {result['bound_charge_density']:.2e}")
    """
    position = np.asarray(position, dtype=np.float64)

    # Compute divergence using central finite differences
    P0 = polarization_field(position)
    if P0.shape != (3,):
        raise ValueError(f"Polarization must return 3D vector, got {P0.shape}")

    div_P = 0.0
    for i in range(3):
        pos_plus = position.copy()
        pos_minus = position.copy()
        pos_plus[i] += h
        pos_minus[i] -= h

        P_plus = polarization_field(pos_plus)
        P_minus = polarization_field(pos_minus)

        dP_i = (P_plus[i] - P_minus[i]) / (2 * h)
        div_P += dP_i

    # ρ_bound = -∇ · P
    rho_bound = -div_P

    return {
        "bound_charge_density": rho_bound,
        "position": position,
        "divergence_P": div_P,
    }


@maxwell_cite(
    162,
    part=1,
    chapter="Theory of Dielectrics",
    theory_class="maxwell_original",
    description="Bound charge density for linear dielectric",
)
def bound_charge_density_linear(
    electric_field_divergence: float,
    susceptibility: float,
) -> dict[str, float]:
    """
    Bound charge density for a linear homogeneous dielectric.

    Art. 162: For a linear dielectric with P = χ_e * E, the bound
    charge density is:

        ρ_bound = -∇ · P = -χ_e * (∇ · E)

    Using Gauss's law ∇ · E = 4π * ρ_free (in CGS-ESU):

        ρ_bound = -χ_e * 4π * ρ_free = -(K - 1) * 4π * ρ_free

    This shows that bound charge opposes free charge, reducing the
    net field inside the dielectric.

    Args:
        electric_field_divergence: ∇ · E (statvolts/cm²).
        susceptibility: χ_e (dimensionless).

    Returns:
        Dictionary with:
        - bound_charge_density: ρ_bound (statcoulombs/cm³)
        - free_charge_equivalent: ρ_free that would produce ∇ · E
        - susceptibility: χ_e used

    References:
        Part I, Art. 162: Bound charge in linear dielectrics.
    """
    # ρ_bound = -χ_e * (∇ · E) / (4π) * 4π = -χ_e * (∇ · E) in our convention
    rho_bound = -susceptibility * electric_field_divergence

    # Free charge that would produce this field divergence
    # ∇ · E = 4π * ρ_free in CGS-ESU
    rho_free = electric_field_divergence / (4 * np.pi)

    return {
        "bound_charge_density": rho_bound,
        "free_charge_equivalent": rho_free,
        "susceptibility": susceptibility,
        "electric_field_divergence": electric_field_divergence,
    }


@maxwell_cite(
    163,
    part=1,
    chapter="Theory of Dielectrics",
    theory_class="maxwell_original",
    description="Surface bound charge σ_bound = P · n",
)
def surface_bound_charge(
    polarization: np.ndarray,
    surface_normal: np.ndarray,
) -> dict[str, float | np.ndarray]:
    """
    Calculate surface bound charge density at a dielectric boundary.

    Art. 163: At the surface of a polarized dielectric, bound charge
    appears with surface density:

        σ_bound = P · n

    where n is the outward unit normal to the surface.

    This surface charge arises because the polarization terminates
    at the boundary, leaving uncompensated bound charge on the surface.

    For a dielectric in an external field:
        - σ_bound > 0 where P points outward (n · P > 0)
        - σ_bound < 0 where P points inward (n · P < 0)

    Args:
        polarization: Polarization vector P at the surface (statC/cm²).
        surface_normal: Outward unit normal vector n (dimensionless).

    Returns:
        Dictionary with:
        - surface_bound_charge: σ_bound (statcoulombs/cm²)
        - polarization: Input P vector
        - surface_normal: Input n vector
        - polarization_angle: Angle between P and n (radians)

    References:
        Part I, Art. 163: Surface bound charge at dielectric boundary.

    Example:
        >>> P = np.array([1, 0, 0])  # Polarization in +x
        >>> n = np.array([1, 0, 0])  # Normal also in +x
        >>> result = surface_bound_charge(P, n)
        >>> print(f"σ_bound = {result['surface_bound_charge']} statC/cm²")
    """
    polarization = np.asarray(polarization, dtype=np.float64)
    surface_normal = np.asarray(surface_normal, dtype=np.float64)

    # Normalize surface normal
    n_norm = np.linalg.norm(surface_normal)
    if n_norm > 0:
        surface_normal = surface_normal / n_norm

    # σ_bound = P · n
    sigma_bound = np.dot(polarization, surface_normal)

    # Angle between P and n
    P_norm = np.linalg.norm(polarization)
    if P_norm > 0 and n_norm > 0:
        cos_theta = sigma_bound / (P_norm * n_norm)
        cos_theta = np.clip(cos_theta, -1, 1)
        angle = np.arccos(cos_theta)
    else:
        angle = 0.0

    return {
        "surface_bound_charge": sigma_bound,
        "polarization": polarization,
        "surface_normal": surface_normal,
        "polarization_angle": angle,
        "polarization_magnitude": P_norm,
    }


# =============================================================================
# DIELECTRIC DISPLACEMENT (Art. 164)
# =============================================================================


@maxwell_cite(
    164,
    part=1,
    chapter="Theory of Dielectrics",
    theory_class="maxwell_original",
    description="Electric displacement D = ε_0*E + P",
)
def dielectric_displacement(
    electric_field: np.ndarray,
    polarization: np.ndarray = None,
    relative_permittivity: float = None,
    susceptibility: float = None,
) -> dict[str, np.ndarray | float]:
    """
    Calculate electric displacement (dielectric displacement).

    Art. 164: Maxwell introduced the electric displacement D as the
    fundamental field in dielectrics. It combines the electric field
    and the polarization response:

        D = ε_0 * E + P

    In CGS-ESU (with ε_0 = 1):

        D = E + P = E + χ_e * E = (1 + χ_e) * E = K * E

    The key property of D is that its divergence gives only the
    free charge density (not bound charge):

        ∇ · D = 4π * ρ_free  (in CGS-ESU)

    This makes D the natural field to use when free charges are known.

    Args:
        electric_field: Electric field E (statvolts/cm).
        polarization: Polarization P (statcoulombs/cm²). Optional.
        relative_permittivity: K (alternative to providing P).
        susceptibility: χ_e (alternative to providing P).

    Returns:
        Dictionary with:
        - displacement: D vector (statcoulombs/cm²)
        - displacement_magnitude: |D| (statcoulombs/cm²)
        - electric_field: Input E
        - polarization: P used (computed if not provided)
        - relative_permittivity: K used

    Raises:
        ValueError: If insufficient parameters for calculation.

    References:
        Part I, Art. 164: Definition of electric displacement.

    Example:
        >>> E = np.array([100, 0, 0])
        >>> result = dielectric_displacement(E, relative_permittivity=2.5)
        >>> print(f"D = {result['displacement']} statC/cm²")
        >>> print(f"|D| = {result['displacement_magnitude']:.2f}")
    """
    electric_field = np.asarray(electric_field, dtype=np.float64)

    if polarization is None:
        if relative_permittivity is None and susceptibility is None:
            raise ValueError(
                "Either polarization or (relative_permittivity/susceptibility) required"
            )

        if susceptibility is None:
            susceptibility = relative_permittivity - 1

        # P = χ_e * E (in CGS-ESU with ε_0 = 1)
        polarization = susceptibility * electric_field

    polarization = np.asarray(polarization, dtype=np.float64)

    # D = E + P (in CGS-ESU with ε_0 = 1)
    displacement = electric_field + polarization
    displacement_magnitude = np.linalg.norm(displacement)

    return {
        "displacement": displacement,
        "displacement_magnitude": displacement_magnitude,
        "electric_field": electric_field,
        "polarization": polarization,
        "relative_permittivity": (
            1 + np.linalg.norm(polarization) / np.linalg.norm(electric_field)
            if np.linalg.norm(electric_field) > 0
            else None
        ),
    }


@maxwell_cite(
    164,
    part=1,
    chapter="Theory of Dielectrics",
    theory_class="maxwell_original",
    description="Gauss's law for D: ∇ · D = 4πρ_free",
)
def gauss_law_dielectric(
    free_charge_density: float,
) -> dict[str, float]:
    """
    Gauss's law in dielectric media.

    Art. 164: Maxwell showed that the divergence of D equals the free
    charge density (times 4π in CGS-ESU):

        ∇ · D = 4π * ρ_free

    This is the fundamental advantage of D: it depends only on free
    charges, not on bound charges from polarization.

    Args:
        free_charge_density: ρ_free (statcoulombs/cm³).

    Returns:
        Dictionary with:
        - divergence_D: ∇ · D (statcoulombs/cm³)
        - free_charge_density: Input ρ_free
        - bound_charge_factor: Factor by which bound charge reduces field

    References:
        Part I, Art. 164: Gauss's law for dielectrics.

    Example:
        >>> result = gauss_law_dielectric(free_charge_density=1.0)
        >>> print(f"∇ · D = {result['divergence_D']:.2f}")
    """
    # ∇ · D = 4π * ρ_free in CGS-ESU
    divergence_D = 4 * np.pi * free_charge_density

    return {
        "divergence_D": divergence_D,
        "free_charge_density": free_charge_density,
    }


# =============================================================================
# ELECTRIFICATION BY FRICTION (Arts. 165–166)
# =============================================================================


@maxwell_cite(
    165,
    166,
    part=1,
    chapter="Electrification",
    theory_class="maxwell_original",
    description="Electrification by friction (triboelectric effect)",
)
def electrification_by_friction(
    material_1: str,
    material_2: str,
    contact_area: float,
    pressure: float = None,
    temperature: float = 293.15,
) -> dict[str, float]:
    """
    Model electrification by friction (triboelectric effect).

    Arts. 165–166: Maxwell described the phenomenon where two
    dissimilar materials become oppositely charged when rubbed
    together (triboelectric effect).

    The triboelectric series ranks materials by their tendency to
    gain or lose electrons:
        + (loses electrons, becomes +): air, glass, mica, wool, fur
        ... (middle): paper, cotton, wood, amber
        - (gains electrons, becomes -): rubber, ebonite, resin, sulfur

    The charge transferred depends on:
        - Position in triboelectric series (work function difference)
        - Contact area and pressure
        - Surface roughness and cleanliness
        - Temperature and humidity

    Args:
        material_1: First material name.
        material_2: Second material name.
        contact_area: Contact area (cm²).
        pressure: Contact pressure (dynes/cm²). Optional.
        temperature: Temperature (K).

    Returns:
        Dictionary with:
        - charge_transferred: Q transferred (statcoulombs)
        - material_1_charge: Charge on material_1
        - material_2_charge: Charge on material_2
        - triboelectric_series: Position of each material

    References:
        Part I, Art. 165: Electrification by friction.
        Part I, Art. 166: Triboelectric series.

    Example:
        >>> result = electrification_by_friction(
        ...     "glass", "silk", contact_area=10.0
        ... )
        >>> print(f"Q = {result['charge_transferred']:.2e} statC")
    """
    # Triboelectric series (approximate work function in eV)
    # Higher value = more likely to gain electrons (become negative)
    triboelectric_series = {
        # Positive end (loses electrons)
        "air": 0.0,
        "glass": 4.5,
        "mica": 4.7,
        "wool": 4.8,
        "fur": 4.9,
        "silk": 5.0,
        "paper": 5.1,
        "cotton": 5.2,
        "wood": 5.3,
        "amber": 5.4,
        "resin": 5.5,
        "ebonite": 5.6,
        "sulfur": 5.7,
        "rubber": 5.8,
        # Negative end (gains electrons)
    }

    # Get positions in series
    pos_1 = triboelectric_series.get(material_1.lower(), 5.0)
    pos_2 = triboelectric_series.get(material_2.lower(), 5.0)

    # Work function difference (eV)
    delta_phi = abs(pos_2 - pos_1)

    # Charge transfer coefficient (statC/cm² per eV difference)
    # This is an empirical parameter
    charge_coefficient = 1e-9  # statC/cm² per eV

    # Pressure factor (increases contact, more charge)
    pressure_factor = 1.0
    if pressure is not None and pressure > 0:
        pressure_factor = 1.0 + 0.1 * np.log10(max(pressure, 1) / 1000)

    # Charge transferred
    charge_transferred = (
        charge_coefficient
        * delta_phi
        * contact_area
        * pressure_factor
        * (293.15 / temperature)  # Temperature reduces charge
    )

    # Determine polarity
    if pos_1 < pos_2:
        # Material 1 loses electrons (becomes +)
        charge_1 = charge_transferred
        charge_2 = -charge_transferred
    else:
        charge_1 = -charge_transferred
        charge_2 = charge_transferred

    return {
        "charge_transferred": abs(charge_transferred),
        "material_1_charge": charge_1,
        "material_2_charge": charge_2,
        "material_1": material_1,
        "material_2": material_2,
        "material_1_series_position": pos_1,
        "material_2_series_position": pos_2,
        "triboelectric_difference": delta_phi,
        "contact_area": contact_area,
        "temperature": temperature,
    }


# =============================================================================
# ELECTRIFICATION BY CONTACT (Arts. 167–168)
# =============================================================================


@maxwell_cite(
    167,
    168,
    part=1,
    chapter="Electrification",
    theory_class="maxwell_original",
    description="Electrification by contact (contact potential)",
)
def electrification_by_contact(
    material_1: str,
    material_2: str,
    contact_time: float,
    separation_velocity: float = None,
    temperature: float = 293.15,
) -> dict[str, float]:
    """
    Model electrification by contact (contact potential difference).

    Arts. 167–168: Maxwell showed that when two dissimilar conductors
    are brought into contact, a potential difference (contact potential)
    develops between them due to the difference in work functions.

    The Volta contact potential is:

        V_contact = (Φ_1 - Φ_2) / e

    where Φ is the work function. For conductors, this leads to
    charge transfer until equilibrium.

    Upon rapid separation, some charge may be retained, leading to
    electrification.

    Args:
        material_1: First conductor material.
        material_2: Second conductor material.
        contact_time: Time in contact (seconds).
        separation_velocity: Velocity of separation (cm/s).
        temperature: Temperature (K).

    Returns:
        Dictionary with:
        - contact_potential: V_contact (statvolts)
        - charge_transferred: Q (statcoulombs)
        - retained_charge: Q retained after separation
        - work_functions: Work functions of materials

    References:
        Part I, Art. 167: Contact electrification theory.
        Part I, Art. 168: Contact potential difference.

    Example:
        >>> result = electrification_by_contact("zinc", "copper", contact_time=1.0)
        >>> print(f"V_contact = {result['contact_potential']:.4f} statV")
    """
    # Work functions (eV) for common metals
    work_functions = {
        "zinc": 4.3,
        "aluminum": 4.1,
        "magnesium": 3.7,
        "calcium": 2.9,
        "sodium": 2.8,
        "potassium": 2.3,
        "lithium": 2.9,
        "iron": 4.5,
        "nickel": 5.0,
        "cobalt": 5.0,
        "copper": 4.7,
        "silver": 4.7,
        "gold": 5.1,
        "platinum": 5.6,
        "tungsten": 4.5,
        "mercury": 4.5,
        "lead": 4.1,
        "tin": 4.4,
    }

    # Get work functions (default to 4.5 eV if unknown)
    phi_1 = work_functions.get(material_1.lower(), 4.5)
    phi_2 = work_functions.get(material_2.lower(), 4.5)

    # Contact potential (eV)
    delta_phi = phi_1 - phi_2

    # Convert to statvolts (1 eV/e = 1 V = 1/299.79 statV)
    contact_potential = delta_phi / 299.792458

    # Charge transfer depends on capacitance and contact time
    # Typical contact capacitance ~ 1 pF = 1e-12 F = 0.9 cm in CGS
    contact_capacitance = 1.0  # cm (statfarads)

    # Equilibrium charge
    Q_equilibrium = contact_capacitance * abs(contact_potential)

    # Charge retention factor (depends on separation speed)
    retention = 0.5  # Default: 50% retained
    if separation_velocity is not None:
        # Faster separation retains more charge
        retention = min(0.9, 0.3 + 0.1 * np.log10(max(separation_velocity, 0.1)))

    # Contact time factor (longer contact approaches equilibrium)
    time_constant = 0.1  # seconds
    time_factor = 1 - np.exp(-contact_time / time_constant)

    retained_charge = Q_equilibrium * retention * time_factor

    return {
        "contact_potential": contact_potential,
        "charge_transferred": Q_equilibrium * time_factor,
        "retained_charge": retained_charge,
        "material_1": material_1,
        "material_2": material_2,
        "work_function_1": phi_1,
        "work_function_2": phi_2,
        "work_function_difference": delta_phi,
        "contact_time": contact_time,
        "temperature": temperature,
    }


@maxwell_cite(
    168,
    part=1,
    chapter="Electrification",
    theory_class="maxwell_original",
    description="Charge distribution on conductor after contact",
)
def charge_distribution_conductor(
    total_charge: float,
    conductor_shape: str,
    dimensions: dict[str, float],
) -> dict[str, float | np.ndarray]:
    """
    Calculate charge distribution on a charged conductor.

    Art. 168: Maxwell analyzed how charge distributes itself on the
    surface of a conductor. For an isolated conductor:
        - Charge resides entirely on the surface (electrostatic equilibrium)
        - Surface charge density σ is proportional to curvature
        - Sharp points have highest σ (corona discharge)

    For common shapes:
        - Sphere: σ = Q / (4πa²) uniform
        - Ellipsoid: σ ∝ 1/radius of curvature
        - Disk: σ ∝ 1/√(a² - r²) diverges at edge

    Args:
        total_charge: Total charge Q (statcoulombs).
        conductor_shape: Shape type ("sphere", "ellipsoid", "disk", "wire").
        dimensions: Shape parameters (e.g., {"radius": a} for sphere).

    Returns:
        Dictionary with:
        - surface_charge_density: σ (function of position or average)
        - total_charge: Q
        - conductor_shape: Shape type
        - capacitance: Self-capacitance (statfarads)

    References:
        Part I, Art. 168: Charge distribution on conductors.

    Example:
        >>> result = charge_distribution_conductor(
        ...     total_charge=100,
        ...     conductor_shape="sphere",
        ...     dimensions={"radius": 5.0}
        ... )
        >>> print(f"σ = {result['surface_charge_density']:.4f} statC/cm²")
    """
    total_charge = float(total_charge)

    if conductor_shape == "sphere":
        radius = dimensions.get("radius", 1.0)
        # Sphere: uniform charge distribution
        surface_area = 4 * np.pi * radius**2
        sigma = total_charge / surface_area
        capacitance = radius  # Self-capacitance of sphere in CGS-ESU

        return {
            "surface_charge_density": sigma,
            "surface_charge_density_function": lambda r: sigma,
            "total_charge": total_charge,
            "conductor_shape": "sphere",
            "capacitance": capacitance,
            "radius": radius,
            "surface_area": surface_area,
        }

    elif conductor_shape == "ellipsoid":
        # Prolate ellipsoid (a > b = c)
        a = dimensions.get("a", 2.0)
        b = dimensions.get("b", 1.0)
        c = dimensions.get("c", b)

        # Eccentricity
        e = np.sqrt(1 - (b / a) ** 2) if a > b else 0

        # Surface charge density at pole (highest)
        sigma_pole = total_charge / (4 * np.pi * a * b)

        # Average surface charge density
        surface_area_approx = 4 * np.pi * ((a * b + b * c + c * a) / 3) ** 0.5
        sigma_avg = total_charge / surface_area_approx

        # Capacitance of ellipsoid (approximate)
        if a > b:
            capacitance = 2 * a * e / np.log((1 + e) / (1 - e))
        else:
            capacitance = a  # Sphere limit

        return {
            "surface_charge_density": sigma_avg,
            "sigma_at_pole": sigma_pole,
            "sigma_at_equator": sigma_pole * (b / a),
            "total_charge": total_charge,
            "conductor_shape": "ellipsoid",
            "capacitance": capacitance,
            "eccentricity": e,
            "dimensions": dimensions,
        }

    elif conductor_shape == "disk":
        radius = dimensions.get("radius", 1.0)
        thickness = dimensions.get("thickness", 0.01)

        # Disk has charge concentrating at edges
        # Average on each face
        face_area = np.pi * radius**2
        sigma_avg = total_charge / (2 * face_area)  # Both faces

        # Edge charge density (higher)
        sigma_edge = sigma_avg * (radius / thickness) ** 0.5

        # Capacitance of disk (isolated)
        capacitance = 2 * radius / np.pi

        return {
            "surface_charge_density": sigma_avg,
            "edge_charge_density": sigma_edge,
            "total_charge": total_charge,
            "conductor_shape": "disk",
            "capacitance": capacitance,
            "radius": radius,
        }

    elif conductor_shape == "wire":
        length = dimensions.get("length", 10.0)
        radius = dimensions.get("radius", 0.1)

        # Wire has charge concentrating at ends
        surface_area = 2 * np.pi * radius * length
        sigma_avg = total_charge / surface_area

        # End charge density (higher)
        sigma_end = sigma_avg * (length / radius) ** 0.5

        # Capacitance of thin wire (approximate)
        capacitance = length / (2 * np.log(length / radius))

        return {
            "surface_charge_density": sigma_avg,
            "end_charge_density": sigma_end,
            "total_charge": total_charge,
            "conductor_shape": "wire",
            "capacitance": capacitance,
            "length": length,
            "radius": radius,
        }

    else:
        raise ValueError(f"Unknown conductor_shape: {conductor_shape}")


# =============================================================================
# ELECTRIFICATION BY INDUCTION (Arts. 169–170)
# =============================================================================


@maxwell_cite(
    169,
    170,
    part=1,
    chapter="Electrification",
    theory_class="maxwell_original",
    description="Electrification by induction (charging by induction)",
)
def electrification_by_induction(
    inducing_charge: float,
    inducing_position: np.ndarray,
    conductor_position: np.ndarray,
    conductor_radius: float,
    grounding: bool = False,
) -> dict[str, float | np.ndarray]:
    """
    Model electrification by induction (charging by induction).

    Arts. 169–170: Maxwell described induction: when a charged body
    is brought near a neutral conductor, it induces opposite charges
    on the near side and like charges on the far side.

    If the conductor is momentarily grounded while the inducing
    charge is present, the like charges flow to ground, and the
    conductor retains a net opposite charge after the ground is
    removed and the inducing charge is taken away.

    This is the principle of the electrophorus and electrostatic
    induction machines.

    Args:
        inducing_charge: Q_inducing (statcoulombs).
        inducing_position: Position of inducing charge (cm).
        conductor_position: Center of conductor (cm).
        conductor_radius: Radius of spherical conductor (cm).
        grounding: If True, model complete induction charging.

    Returns:
        Dictionary with:
        - induced_dipole: p (statC·cm)
        - near_side_charge: Induced charge on near side
        - far_side_charge: Induced charge on far side
        - net_induced_charge: Net charge if grounded
        - inducing_position: Input position
        - inducing_charge: Input charge

    References:
        Part I, Art. 169: Induction theory.
        Part I, Art. 170: Induction charging process.

    Example:
        >>> result = electrification_by_induction(
        ...     inducing_charge=100,
        ...     inducing_position=np.array([0, 0, 10]),
        ...     conductor_position=np.array([0, 0, 0]),
        ...     conductor_radius=1.0,
        ...     grounding=True
        ... )
        >>> print(f"Q_induced = {result['net_induced_charge']:.2f} statC")
    """
    inducing_position = np.asarray(inducing_position, dtype=np.float64)
    conductor_position = np.asarray(conductor_position, dtype=np.float64)

    # Vector from conductor to inducing charge
    r_vec = inducing_position - conductor_position
    r_mag = np.linalg.norm(r_vec)

    if r_mag <= conductor_radius:
        raise ValueError("Inducing charge must be outside the conductor")

    # Electric field at conductor due to inducing charge
    E_mag = inducing_charge / r_mag**2  # In CGS-ESU

    # Induced dipole moment (for spherical conductor)
    # p = a³ * E_0 (where a is radius)
    induced_dipole_magnitude = conductor_radius**3 * E_mag
    induced_dipole = induced_dipole_magnitude * r_vec / r_mag

    # Induced surface charge distribution
    # σ(θ) = σ_0 * cos(θ) where θ is angle from field direction
    sigma_0 = 3 * E_mag / (4 * np.pi)  # Maximum surface charge density

    # Charge on near side (hemisphere facing inducing charge)
    near_side_charge = -(conductor_radius**2) * E_mag * (inducing_charge > 0)
    if inducing_charge < 0:
        near_side_charge = abs(near_side_charge)

    # Charge on far side
    far_side_charge = -near_side_charge

    # Net induced charge (if grounded)
    # For a grounded sphere: Q_induced = -a * V_0 = -a² * E_0
    if grounding:
        net_induced_charge = -conductor_radius * (inducing_charge / r_mag)
    else:
        net_induced_charge = 0.0

    return {
        "induced_dipole": induced_dipole,
        "induced_dipole_magnitude": induced_dipole_magnitude,
        "near_side_charge": near_side_charge,
        "far_side_charge": far_side_charge,
        "net_induced_charge": net_induced_charge,
        "inducing_charge": inducing_charge,
        "inducing_position": inducing_position,
        "conductor_position": conductor_position,
        "conductor_radius": conductor_radius,
        "separation_distance": r_mag,
        "electric_field_at_conductor": E_mag,
        "grounding": grounding,
    }


@maxwell_cite(
    169,
    170,
    part=1,
    chapter="Electrification",
    theory_class="maxwell_original",
    description="Image charge method for induction",
)
def image_charge_induction(
    point_charge: float,
    point_position: np.ndarray,
    sphere_center: np.ndarray,
    sphere_radius: float,
    sphere_potential: float = 0,
) -> dict[str, float | np.ndarray]:
    """
    Calculate image charge for a point charge near a conducting sphere.

    Arts. 169–170: Maxwell used the method of images to solve
    induction problems. For a point charge q at distance d from
    the center of a grounded conducting sphere of radius a:

    The image charge q' is located at distance d' = a²/d from center:

        q' = -q * (a / d)
        d' = a² / d

    This image charge reproduces the boundary condition (V = 0 on
    sphere surface).

    Args:
        point_charge: q (statcoulombs).
        point_position: Position of point charge (cm).
        sphere_center: Center of sphere (cm).
        sphere_radius: Radius a (cm).
        sphere_potential: V on sphere (default 0 = grounded).

    Returns:
        Dictionary with:
        - image_charge: q' (statcoulombs)
        - image_position: Position of image charge (cm)
        - force: Force on point charge (dynes)
        - potential_on_sphere: V (should match input)

    References:
        Part I, Art. 169: Image charge theory.
        Part I, Art. 170: Method of images for spheres.

    Example:
        >>> result = image_charge_induction(
        ...     point_charge=100,
        ...     point_position=np.array([0, 0, 10]),
        ...     sphere_center=np.array([0, 0, 0]),
        ...     sphere_radius=1.0
        ... )
        >>> print(f"q' = {result['image_charge']:.2f} statC")
        >>> print(f"r' = {result['image_position']}")
    """
    point_position = np.asarray(point_position, dtype=np.float64)
    sphere_center = np.asarray(sphere_center, dtype=np.float64)

    # Vector from sphere center to point charge
    r_vec = point_position - sphere_center
    r_mag = np.linalg.norm(r_vec)

    if r_mag <= sphere_radius:
        raise ValueError("Point charge must be outside the sphere")

    # Image charge position: d' = a²/d
    image_distance = sphere_radius**2 / r_mag
    image_position = sphere_center + (image_distance / r_mag) * r_vec

    # Image charge: q' = -q * (a/d) for grounded sphere
    image_charge = -point_charge * (sphere_radius / r_mag)

    # For non-zero potential, add central charge Q_center = V * a
    central_charge = sphere_potential * sphere_radius

    # Force on point charge
    # Distance between charge and image
    d_image = r_mag - image_distance
    force_magnitude = point_charge * image_charge / d_image**2

    # Force direction (attractive if charges opposite)
    force = -force_magnitude * r_vec / r_mag
    if force_magnitude < 0:
        force = -force

    return {
        "image_charge": image_charge,
        "image_position": image_position,
        "central_charge": central_charge if sphere_potential != 0 else 0,
        "force_on_charge": force,
        "force_magnitude": abs(force_magnitude),
        "point_charge": point_charge,
        "point_position": point_position,
        "sphere_center": sphere_center,
        "sphere_radius": sphere_radius,
        "sphere_potential": sphere_potential,
    }


# =============================================================================
# DIELECTRIC MATERIAL CLASS
# =============================================================================


@dataclass
class DielectricMaterial:
    """
    Dielectric material with Maxwell's specific inductive capacity.

    This class encapsulates the dielectric properties of a material
    as described in Part I, Chapter VII:

        - Specific inductive capacity K (relative permittivity ε_r)
        - Electric susceptibility χ_e
        - Dielectric breakdown field strength
        - Temperature and frequency dependence

    Attributes:
        name: Material name.
        relative_permittivity: K = ε_r (dimensionless).
        susceptibility: χ_e = K - 1 (dimensionless).
        breakdown_field: Dielectric strength (statvolts/cm).
        temperature: Operating temperature (K).
        frequency: Operating frequency (Hz), None for DC.
    """

    name: str
    relative_permittivity: float
    susceptibility: float = None
    breakdown_field: float = None
    temperature: float = 293.15
    frequency: float = None

    def __post_init__(self):
        """Initialize derived properties."""
        if self.susceptibility is None:
            self.susceptibility = self.relative_permittivity - 1

    @classmethod
    def from_name(
        cls,
        name: str,
        temperature: float = 293.15,
        frequency: float = None,
    ) -> "DielectricMaterial":
        """
        Create a DielectricMaterial from a material name.

        Args:
            name: Material name (e.g., "glass", "water", "air").
            temperature: Temperature (K).
            frequency: Frequency (Hz).

        Returns:
            DielectricMaterial instance.

        Raises:
            ValueError: If material not found in database.

        References:
            Part I, Art. 159: Table of specific inductive capacities.
        """
        # Material database with breakdown fields
        materials = {
            "vacuum": {"K": 1.0, "E_break": float("inf")},
            "air": {"K": 1.00059, "E_break": 30000},  # ~100 statV/cm = 30 kV/cm
            "glass": {"K": 5.0, "E_break": 300000},
            "mica": {"K": 6.0, "E_break": 1000000},
            "quartz": {"K": 4.5, "E_break": 800000},
            "paraffin": {"K": 2.2, "E_break": 50000},
            "ebonite": {"K": 2.7, "E_break": 150000},
            "water": {"K": 80.4, "E_break": 650000},
            "paper": {"K": 3.5, "E_break": 150000},
            "porcelain": {"K": 6.0, "E_break": 200000},
            "polyethylene": {"K": 2.25, "E_break": 450000},
            "teflon": {"K": 2.1, "E_break": 600000},
            "bakelite": {"K": 5.0, "E_break": 200000},
            "rubber": {"K": 2.8, "E_break": 250000},
        }

        name_lower = name.lower()
        if name_lower not in materials:
            raise ValueError(
                f"Material '{name}' not found. " f"Available: {list(materials.keys())}"
            )

        props = materials[name_lower]
        return cls(
            name=name,
            relative_permittivity=props["K"],
            breakdown_field=props["E_break"],
            temperature=temperature,
            frequency=frequency,
        )

    @maxwell_cite(
        160,
        161,
        part=1,
        chapter="Theory of Dielectrics",
        theory_class="maxwell_original",
        description="Calculate polarization for given field",
    )
    def polarization(self, electric_field: np.ndarray) -> np.ndarray:
        """
        Calculate polarization induced by electric field.

        P = χ_e * E (in CGS-ESU with ε_0 = 1)

        Args:
            electric_field: E vector (statvolts/cm).

        Returns:
            Polarization P (statcoulombs/cm²).
        """
        return self.susceptibility * np.asarray(electric_field)

    @maxwell_cite(
        164,
        part=1,
        chapter="Theory of Dielectrics",
        theory_class="maxwell_original",
        description="Calculate displacement for given field",
    )
    def displacement(self, electric_field: np.ndarray) -> np.ndarray:
        """
        Calculate electric displacement.

        D = K * E = E + P (in CGS-ESU)

        Args:
            electric_field: E vector (statvolts/cm).

        Returns:
            Displacement D (statcoulombs/cm²).
        """
        return self.relative_permittivity * np.asarray(electric_field)

    @property
    def permittivity(self) -> float:
        """
        Absolute permittivity ε = K * ε_0.

        In CGS-ESU, ε_0 = 1, so ε = K.

        Reference: Part I, Arts. 157–159: Specific inductive capacity.
        """
        return self.relative_permittivity

    def check_breakdown(self, electric_field: float) -> bool:
        """
        Check if electric field exceeds dielectric strength.

        Args:
            electric_field: Field magnitude (statvolts/cm).

        Returns:
            True if breakdown would occur.

        Reference: Part I, Arts. 157–159: Dielectric breakdown.
        """
        if self.breakdown_field is None:
            return False
        return electric_field >= self.breakdown_field

    def __repr__(self) -> str:
        return (
            f"DielectricMaterial({self.name!r}, K={self.relative_permittivity}, "
            f"chi_e={self.susceptibility})"
        )


# =============================================================================
# MAIN: Module verification
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DIELECTRICS AND ELECTRIFICATION")
    print("Maxwell's Treatise, Part I, Chapters VII-VIII (Arts. 157-170)")
    print("=" * 70)

    # Test specific inductive capacity
    print("\n--- Specific Inductive Capacity (Arts. 157-159) ---")
    result = specific_inductive_capacity(material="glass")
    print(f"  Glass: K = {result['specific_inductive_capacity']}")
    result = specific_inductive_capacity(material="water")
    print(f"  Water: K = {result['specific_inductive_capacity']}")

    # Test dielectric polarization
    print("\n--- Dielectric Polarization (Arts. 160-161) ---")
    E = np.array([100.0, 0.0, 0.0])
    result = dielectric_polarization(E, relative_permittivity=2.5)
    print(f"  E = {E[0]} statV/cm, K = 2.5")
    print(f"  P = {result['polarization']} statC/cm^2")
    print(f"  chi_e = {result['susceptibility']}")

    # Test electric susceptibility
    print("\n--- Electric Susceptibility (Arts. 160-162) ---")
    result = electric_susceptibility(relative_permittivity=5.0)
    print(f"  K = 5.0 -> chi_e = {result['susceptibility']}")

    # Test bound charge density
    print("\n--- Bound Charge Density (Art. 162) ---")

    def P_uniform(r):
        return np.array([1.0, 0.0, 0.0])

    result = bound_charge_density(P_uniform, np.array([0.0, 0.0, 0.0]))
    print(f"  Uniform P: rho_bound = {result['bound_charge_density']:.2e} statC/cm^3")

    # Test surface bound charge
    print("\n--- Surface Bound Charge (Art. 163) ---")
    P = np.array([1.0, 0.0, 0.0])
    n = np.array([1.0, 0.0, 0.0])
    result = surface_bound_charge(P, n)
    print(f"  P . n = {result['surface_bound_charge']} statC/cm^2")

    # Test dielectric displacement
    print("\n--- Dielectric Displacement (Art. 164) ---")
    E = np.array([100.0, 0.0, 0.0])
    result = dielectric_displacement(E, relative_permittivity=2.5)
    print(f"  E = {E[0]} statV/cm, K = 2.5")
    print(f"  D = {result['displacement']} statC/cm^2")
    print(f"  |D| = {result['displacement_magnitude']:.2f}")

    # Test electrification by friction
    print("\n--- Electrification by Friction (Arts. 165-166) ---")
    result = electrification_by_friction("glass", "silk", contact_area=10.0)
    print(f"  Glass rubbed with silk:")
    print(f"    Q_transferred = {result['charge_transferred']:.2e} statC")
    print(f"    Glass charge = {result['material_1_charge']:.2e} statC")
    print(f"    Silk charge = {result['material_2_charge']:.2e} statC")

    # Test electrification by contact
    print("\n--- Electrification by Contact (Arts. 167-168) ---")
    result = electrification_by_contact("zinc", "copper", contact_time=1.0)
    print(f"  Zinc-Copper contact:")
    print(f"    V_contact = {result['contact_potential']:.4f} statV")
    print(f"    Q_retained = {result['retained_charge']:.2e} statC")

    # Test charge distribution
    print("\n--- Charge Distribution on Conductor (Art. 168) ---")
    result = charge_distribution_conductor(
        total_charge=100.0, conductor_shape="sphere", dimensions={"radius": 5.0}
    )
    print(f"  Sphere (r=5cm, Q=100 statC):")
    print(f"    sigma = {result['surface_charge_density']:.4f} statC/cm^2")
    print(f"    Capacitance = {result['capacitance']} cm")

    # Test electrification by induction
    print("\n--- Electrification by Induction (Arts. 169-170) ---")
    result = electrification_by_induction(
        inducing_charge=100.0,
        inducing_position=np.array([0.0, 0.0, 10.0]),
        conductor_position=np.array([0.0, 0.0, 0.0]),
        conductor_radius=1.0,
        grounding=True,
    )
    print(f"  Induction with grounding:")
    print(f"    Q_induced = {result['net_induced_charge']:.2f} statC")
    print(f"    Dipole moment = {result['induced_dipole_magnitude']:.2f} statC.cm")

    # Test image charge
    print("\n--- Image Charge Method (Arts. 169-170) ---")
    result = image_charge_induction(
        point_charge=100.0,
        point_position=np.array([0.0, 0.0, 10.0]),
        sphere_center=np.array([0.0, 0.0, 0.0]),
        sphere_radius=1.0,
    )
    print(f"  Point charge near grounded sphere:")
    print(f"    q' = {result['image_charge']:.2f} statC")
    print(f"    r' = {result['image_position']} cm")
    print(f"    Force = {result['force_magnitude']:.4f} dynes")

    # Test DielectricMaterial class
    print("\n--- DielectricMaterial Class ---")
    mica = DielectricMaterial.from_name("mica")
    print(f"  {mica}")
    E_test = np.array([1000.0, 0.0, 0.0])
    print(f"  P = {mica.polarization(E_test)} statC/cm^2")
    print(f"  D = {mica.displacement(E_test)} statC/cm^2")
    print(f"  Breakdown at {mica.breakdown_field} statV/cm")

    print("\n" + "=" * 70)
    print("Module verification complete.")
    print("=" * 70)

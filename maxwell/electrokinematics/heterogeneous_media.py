"""
Conduction in Heterogeneous Media — Maxwell's Part II, Chapter IX (Arts. 310-324).

This module implements Maxwell's theory of conduction through heterogeneous
and composite media:

1. **Series and Parallel Combinations** (Arts. 310-318): Effective conductivity
   of layered and composite structures.
   - Layers in series (Arts. 310-314)
   - Layers in parallel (Arts. 315-318)
   - Maxwell-Garnett effective medium theory

2. **Interface Effects** (Arts. 319-321): Contact resistance and boundary layers
   - Interface resistance
   - Transition layers

3. **Stratified Media** (Arts. 322-324): General anisotropic treatment
   - Stratified conductor analysis
   - Mixed conductor modeling

Maxwell's key insight: The effective properties of heterogeneous media depend
on both the constituent properties and their geometric arrangement. His
effective medium theory remains foundational for composite material science.

CGS-EMU units are used throughout:
    - Conductivity: siemens/cm
    - Resistance: abohms
    - Dimensions: cm

Category: A (maxwell_original) — Maxwell's theory of heterogeneous conduction.

References:
    Part II, Chapter IX: Conduction in Heterogeneous Media (Arts. 310-324).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional, Union, List
import numpy as np
from functools import wraps

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST, C, C_APPROX


# =============================================================================
# SERIES COMBINATIONS (Arts. 310-314)
# =============================================================================

@maxwell_cite(
    310, 311, 312, 313, 314,
    part=2, chapter="Conduction in Heterogeneous Media",
    theory_class="maxwell_original",
    description="Calculate effective conductivity of layers in series"
)
def effective_conductivity_series(
    layer_conductivities: list[float],
    layer_thicknesses: list[float],
) -> dict[str, float]:
    """
    Calculate the effective conductivity of layers arranged in series.

    Arts. 310-314: Maxwell analyzed conduction perpendicular to the plane
    of stratification. For N layers with conductivities sigma_i and
    thicknesses d_i:

    The effective conductivity for current flowing perpendicular to the
    layers is:

        sigma_eff_perp = D / sum(d_i / sigma_i)

    where D = sum(d_i) is the total thickness.

    This is equivalent to resistors in series:

        R_total = sum(R_i) = sum(d_i / (sigma_i * A))
        sigma_eff = D / (R_total * A)

    The effective resistivity is the thickness-weighted average:

        rho_eff = sum(f_i * rho_i)

    where f_i = d_i / D is the volume fraction of layer i.

    Args:
        layer_conductivities: List of layer conductivities [sigma_1, sigma_2, ...].
        layer_thicknesses: List of layer thicknesses [d_1, d_2, ...].

    Returns:
        Dictionary with:
        - effective_conductivity: sigma_eff perpendicular to layers
        - effective_resistivity: rho_eff = 1/sigma_eff
        - total_thickness: D = sum(d_i)
        - layer_resistances: R_i proportional terms
        - volume_fractions: f_i = d_i/D for each layer

    Raises:
        ValueError: If lists have different lengths or contain invalid values.

    References:
        Part II, Arts. 310-314: Series combination of layers.

    Example:
        >>> # Alternating layers: sigma=[1, 0.1, 1] S/cm, d=[1, 1, 1] cm
        >>> result = effective_conductivity_series([1, 0.1, 1], [1, 1, 1])
        >>> print(f"sigma_eff = {result['effective_conductivity']:.4f} S/cm")
    """
    if len(layer_conductivities) != len(layer_thicknesses):
        raise ValueError("layer_conductivities and layer_thicknesses must have same length")

    if len(layer_conductivities) == 0:
        raise ValueError("At least one layer required")

    n_layers = len(layer_conductivities)
    layer_conductivities = np.asarray(layer_conductivities, dtype=np.float64)
    layer_thicknesses = np.asarray(layer_thicknesses, dtype=np.float64)

    if np.any(layer_conductivities <= 0):
        raise ValueError("All conductivities must be positive")
    if np.any(layer_thicknesses <= 0):
        raise ValueError("All thicknesses must be positive")

    # Total thickness
    total_thickness = np.sum(layer_thicknesses)

    # Volume fractions
    volume_fractions = layer_thicknesses / total_thickness

    # Layer resistance terms (proportional to d/sigma)
    layer_resistance_terms = layer_thicknesses / layer_conductivities

    # Effective conductivity (perpendicular to layers)
    # sigma_eff = D / sum(d_i / sigma_i)
    effective_conductivity = total_thickness / np.sum(layer_resistance_terms)

    # Effective resistivity
    layer_resistivities = 1.0 / layer_conductivities
    effective_resistivity = np.sum(volume_fractions * layer_resistivities)

    return {
        "effective_conductivity": effective_conductivity,
        "effective_resistivity": effective_resistivity,
        "total_thickness": total_thickness,
        "layer_resistance_terms": layer_resistance_terms.tolist(),
        "volume_fractions": volume_fractions.tolist(),
        "n_layers": n_layers,
        "conductivity_perpendicular": effective_conductivity,
    }


@maxwell_cite(
    310, 311, 312, 313, 314,
    part=2, chapter="Conduction in Heterogeneous Media",
    theory_class="maxwell_original",
    description="Calculate anisotropic effective conductivity of stratified medium"
)
def stratified_conductor_effective(
    layer_conductivities: list[float],
    layer_thicknesses: list[float],
) -> dict[str, float]:
    """
    Calculate both parallel and perpendicular effective conductivities of a
    stratified medium.

    Arts. 310-314: A stratified medium (layered structure) is anisotropic.
    Maxwell showed that the effective conductivity depends on the direction
    of current flow relative to the layering.

    For current flowing PARALLEL to the layers:

        sigma_eff_parallel = sum(f_i * sigma_i)

    For current flowing PERPENDICULAR to the layers:

        sigma_eff_perpendicular = 1 / sum(f_i / sigma_i)

    where f_i = d_i / D is the volume fraction of layer i.

    The stratified medium behaves as an anisotropic conductor with:
        - Higher conductivity parallel to layers
        - Lower conductivity perpendicular to layers

    The anisotropy ratio is:

        ratio = sigma_parallel / sigma_perpendicular >= 1

    Args:
        layer_conductivities: List of layer conductivities.
        layer_thicknesses: List of layer thicknesses.

    Returns:
        Dictionary with:
        - sigma_parallel: Effective conductivity parallel to layers
        - sigma_perpendicular: Effective conductivity perpendicular to layers
        - anisotropy_ratio: sigma_parallel / sigma_perpendicular
        - volume_fractions: f_i for each layer
        - is_isotropic: True if ratio ≈ 1

    References:
        Part II, Arts. 310-314: Stratified medium anisotropy.

    Example:
        >>> # Two-layer structure: sigma=[1, 0.01] S/cm, equal thickness
        >>> result = stratified_conductor_effective([1, 0.01], [1, 1])
        >>> print(f"sigma_parallel = {result['sigma_parallel']:.4f} S/cm")
        >>> print(f"sigma_perp = {result['sigma_perpendicular']:.4f} S/cm")
        >>> print(f"Anisotropy = {result['anisotropy_ratio']:.1f}x")
    """
    if len(layer_conductivities) != len(layer_thicknesses):
        raise ValueError("layer_conductivities and layer_thicknesses must have same length")

    n_layers = len(layer_conductivities)
    layer_conductivities = np.asarray(layer_conductivities, dtype=np.float64)
    layer_thicknesses = np.asarray(layer_thicknesses, dtype=np.float64)

    if np.any(layer_conductivities <= 0):
        raise ValueError("All conductivities must be positive")
    if np.any(layer_thicknesses <= 0):
        raise ValueError("All thicknesses must be positive")

    # Total thickness and volume fractions
    total_thickness = np.sum(layer_thicknesses)
    volume_fractions = layer_thicknesses / total_thickness

    # Parallel conductivity: sigma_eff = sum(f_i * sigma_i)
    sigma_parallel = np.sum(volume_fractions * layer_conductivities)

    # Perpendicular conductivity: sigma_eff = 1 / sum(f_i / sigma_i)
    sigma_perpendicular = 1.0 / np.sum(volume_fractions / layer_conductivities)

    # Anisotropy ratio
    anisotropy_ratio = sigma_parallel / sigma_perpendicular if sigma_perpendicular > 0 else float('inf')

    # Isotropy check
    is_isotropic = np.allclose(layer_conductivities, layer_conductivities[0])

    return {
        "sigma_parallel": sigma_parallel,
        "sigma_perpendicular": sigma_perpendicular,
        "anisotropy_ratio": anisotropy_ratio,
        "volume_fractions": volume_fractions.tolist(),
        "n_layers": n_layers,
        "is_isotropic": is_isotropic,
        "conductivity_tensor_principal": np.array([sigma_parallel, sigma_parallel, sigma_perpendicular]),
    }


# =============================================================================
# PARALLEL COMBINATIONS (Arts. 315-318)
# =============================================================================

@maxwell_cite(
    315, 316, 317, 318,
    part=2, chapter="Conduction in Heterogeneous Media",
    theory_class="maxwell_original",
    description="Calculate effective conductivity of layers in parallel"
)
def effective_conductivity_parallel(
    layer_conductivities: list[float],
    layer_areas: list[float],
    layer_thickness: float = None,
) -> dict[str, float]:
    """
    Calculate the effective conductivity of layers arranged in parallel.

    Arts. 315-318: Maxwell analyzed conduction parallel to the plane of
    stratification. For N layers with conductivities sigma_i and
    cross-sectional areas A_i:

    The effective conductivity for current flowing parallel to the layers is:

        sigma_eff_parallel = sum(A_i * sigma_i) / sum(A_i)

    This is equivalent to resistors in parallel:

        1/R_total = sum(1/R_i) = sum(sigma_i * A_i / L)
        sigma_eff = (L / A_total) * (1/R_total) = sum(A_i * sigma_i) / A_total

    If all layers have the same thickness t and width w_i:

        A_i = t * w_i
        sigma_eff = sum(w_i * sigma_i) / sum(w_i)

    Args:
        layer_conductivities: List of layer conductivities [sigma_1, sigma_2, ...].
        layer_areas: List of cross-sectional areas [A_1, A_2, ...].
        layer_thickness: Optional common thickness for calculating conductance.

    Returns:
        Dictionary with:
        - effective_conductivity: sigma_eff parallel to layers
        - total_area: A_total = sum(A_i)
        - area_fractions: A_i/A_total for each layer
        - layer_conductances: G_i = sigma_i * A_i (if thickness not given)

    Raises:
        ValueError: If lists have different lengths or contain invalid values.

    References:
        Part II, Arts. 315-318: Parallel combination of layers.

    Example:
        >>> # Three wires in parallel: sigma=[1, 2, 3] S/cm, A=[1, 1, 1] cm²
        >>> result = effective_conductivity_parallel([1, 2, 3], [1, 1, 1])
        >>> print(f"sigma_eff = {result['effective_conductivity']:.2f} S/cm")
    """
    if len(layer_conductivities) != len(layer_areas):
        raise ValueError("layer_conductivities and layer_areas must have same length")

    if len(layer_conductivities) == 0:
        raise ValueError("At least one layer required")

    n_layers = len(layer_conductivities)
    layer_conductivities = np.asarray(layer_conductivities, dtype=np.float64)
    layer_areas = np.asarray(layer_areas, dtype=np.float64)

    if np.any(layer_conductivities <= 0):
        raise ValueError("All conductivities must be positive")
    if np.any(layer_areas <= 0):
        raise ValueError("All areas must be positive")

    # Total area
    total_area = np.sum(layer_areas)

    # Area fractions
    area_fractions = layer_areas / total_area

    # Effective conductivity: sigma_eff = sum(A_i * sigma_i) / sum(A_i)
    effective_conductivity = np.sum(layer_areas * layer_conductivities) / total_area

    # Layer conductances (per unit length)
    layer_conductances = layer_conductivities * layer_areas

    return {
        "effective_conductivity": effective_conductivity,
        "total_area": total_area,
        "area_fractions": area_fractions.tolist(),
        "layer_conductances": layer_conductances.tolist(),
        "n_layers": n_layers,
        "conductivity_parallel": effective_conductivity,
    }


@maxwell_cite(
    315, 316, 317, 318,
    part=2, chapter="Conduction in Heterogeneous Media",
    theory_class="maxwell_original",
    description="Maxwell-Garnett effective medium theory for inclusions"
)
def maxwell_garnett_conductivity(
    matrix_conductivity: float,
    inclusion_conductivity: float,
    volume_fraction: float,
    inclusion_shape: str = "sphere",
) -> dict[str, float]:
    """
    Calculate effective conductivity using Maxwell-Garnett effective medium theory.

    Arts. 315-318: Maxwell derived the effective conductivity of a composite
    material consisting of a matrix with embedded inclusions. This is the
    famous Maxwell-Garnett formula.

    For SPHERICAL inclusions at volume fraction f:

        sigma_eff = sigma_m * [2(1-f)*sigma_m + (1+2f)*sigma_i] / [(2+f)*sigma_m + (1-f)*sigma_i]

    For DILUTE suspensions (f << 1):

        sigma_eff ≈ sigma_m * [1 + 3f * (sigma_i - sigma_m)/(sigma_i + 2*sigma_m)]

    Maxwell also derived formulas for other inclusion shapes:

    - Needles (parallel to field):
        sigma_eff = (1-f)*sigma_m + f*sigma_i  (simple rule of mixtures)

    - Disks (perpendicular to field):
        1/sigma_eff = (1-f)/sigma_m + f/sigma_i  (series combination)

    - Randomly oriented ellipsoids (Bruggeman symmetric):
        f*(sigma_i - sigma_eff)/(sigma_i + 2*sigma_eff) + (1-f)*(sigma_m - sigma_eff)/(sigma_m + 2*sigma_eff) = 0

    Args:
        matrix_conductivity: Conductivity of matrix sigma_m (siemens/cm).
        inclusion_conductivity: Conductivity of inclusions sigma_i (siemens/cm).
        volume_fraction: Volume fraction f of inclusions (0 to 1).
        inclusion_shape: Shape of inclusions. Options:
                        - "sphere" (default): Spherical inclusions
                        - "needle": Needle-like inclusions (parallel)
                        - "disk": Disk-like inclusions (perpendicular)
                        - "random": Randomly oriented ellipsoids (Bruggeman)

    Returns:
        Dictionary with:
        - effective_conductivity: sigma_eff of the composite
        - conductivity_ratio: sigma_i / sigma_m
        - enhancement_factor: sigma_eff / sigma_m
        - volume_fraction: Input volume fraction
        - inclusion_shape: Shape used

    Raises:
        ValueError: If volume_fraction not in [0, 1] or invalid shape.

    References:
        Part II, Arts. 315-318: Maxwell-Garnett effective medium theory.

    Example:
        >>> # Spherical inclusions (f=0.3) with sigma_i=10*sigma_m
        >>> result = maxwell_garnett_conductivity(1.0, 10.0, 0.3)
        >>> print(f"sigma_eff = {result['effective_conductivity']:.3f} S/cm")
        >>> print(f"Enhancement = {result['enhancement_factor']:.2f}x")
    """
    if not 0 <= volume_fraction <= 1:
        raise ValueError(f"Volume fraction must be between 0 and 1, got {volume_fraction}")

    if matrix_conductivity <= 0:
        raise ValueError(f"matrix_conductivity must be positive")
    if inclusion_conductivity < 0:
        raise ValueError(f"inclusion_conductivity must be non-negative")

    # Conductivity ratio
    cond_ratio = inclusion_conductivity / matrix_conductivity if matrix_conductivity > 0 else float('inf')

    if inclusion_shape == "sphere":
        # Maxwell-Garnett formula for spherical inclusions
        numerator = 2 * (1 - volume_fraction) * matrix_conductivity + (1 + 2 * volume_fraction) * inclusion_conductivity
        denominator = (2 + volume_fraction) * matrix_conductivity + (1 - volume_fraction) * inclusion_conductivity

        if abs(denominator) > 1e-15:
            effective_conductivity = matrix_conductivity * numerator / denominator
        else:
            effective_conductivity = inclusion_conductivity

    elif inclusion_shape == "needle":
        # Parallel (Voigt) model: rule of mixtures
        effective_conductivity = (1 - volume_fraction) * matrix_conductivity + volume_fraction * inclusion_conductivity

    elif inclusion_shape == "disk":
        # Perpendicular (Reuss) model: series combination
        inv_sigma_eff = (1 - volume_fraction) / matrix_conductivity + volume_fraction / inclusion_conductivity
        effective_conductivity = 1.0 / inv_sigma_eff if inv_sigma_eff > 0 else 0.0

    elif inclusion_shape == "random":
        # Bruggeman symmetric effective medium theory
        if matrix_conductivity > 0 and inclusion_conductivity > 0:
            # Solve the Bruggeman equation iteratively or analytically
            # Quadratic form: 2*sigma_eff² + B*sigma_eff + C = 0
            a = 2
            b = matrix_conductivity + inclusion_conductivity - 3 * volume_fraction * (inclusion_conductivity - matrix_conductivity) - 2 * matrix_conductivity
            c = -matrix_conductivity * inclusion_conductivity

            discriminant = b ** 2 - 4 * a * c
            if discriminant >= 0:
                sigma_eff1 = (-b + np.sqrt(discriminant)) / (2 * a)
                sigma_eff2 = (-b - np.sqrt(discriminant)) / (2 * a)
                effective_conductivity = max(sigma_eff1, sigma_eff2)
            else:
                # Fallback to matrix conductivity
                effective_conductivity = matrix_conductivity
        else:
            effective_conductivity = max(matrix_conductivity, inclusion_conductivity)

    else:
        raise ValueError(f"Unknown inclusion_shape: {inclusion_shape}. "
                        f"Options: sphere, needle, disk, random")

    enhancement_factor = effective_conductivity / matrix_conductivity if matrix_conductivity > 0 else float('inf')

    return {
        "effective_conductivity": effective_conductivity,
        "conductivity_ratio": cond_ratio,
        "enhancement_factor": enhancement_factor,
        "volume_fraction": volume_fraction,
        "inclusion_shape": inclusion_shape,
        "matrix_conductivity": matrix_conductivity,
        "inclusion_conductivity": inclusion_conductivity,
    }


# =============================================================================
# INTERFACE RESISTANCE (Arts. 319-321)
# =============================================================================

@maxwell_cite(
    319, 320, 321,
    part=2, chapter="Conduction in Heterogeneous Media",
    theory_class="maxwell_original",
    description="Calculate interface (contact) resistance between materials"
)
def interface_resistance(
    material_1_conductivity: float,
    material_2_conductivity: float,
    contact_area: float,
    interface_quality: str = "ideal",
    interface_thickness: float = None,
    interface_conductivity: float = None,
) -> dict[str, float]:
    """
    Calculate the resistance at an interface between two different materials.

    Arts. 319-321: Maxwell analyzed the additional resistance arising at
    the interface between two conducting materials. This "contact resistance"
    or "interface resistance" has several contributions:

    1. **Constriction resistance** (Maxwell's contribution):
       Current constricts at the interface due to mismatch in conductivity.

        R_constriction = (1/sigma_1 + 1/sigma_2) / (4 * a)

       where a is the characteristic size of the contact region.

    2. **Interface layer resistance**:
       If there is a thin layer of different material at the interface:

        R_interface = d_interface / (sigma_interface * A)

    3. **Boundary scattering** (not in Maxwell's original theory):
       Additional resistance from electron scattering at the interface.

    For an IDEAL interface (perfect contact):

        R_interface = 0

    Args:
        material_1_conductivity: Conductivity sigma_1 of material 1.
        material_2_conductivity: Conductivity sigma_2 of material 2.
        contact_area: Cross-sectional area A of the contact (cm²).
        interface_quality: "ideal", "poor", or "quantified".
        interface_thickness: Thickness d of interface layer (cm).
        interface_conductivity: Conductivity of interface layer.

    Returns:
        Dictionary with:
        - interface_resistance: R_interface (abohms)
        - constriction_resistance: R_constriction component
        - layer_resistance: R_layer component (if applicable)
        - total_resistance: Sum of all contributions

    Raises:
        ValueError: If conductivities or area invalid.

    References:
        Part II, Arts. 319-321: Interface resistance theory.

    Example:
        >>> # Copper-aluminum joint: sigma_Cu=5.96e5, sigma_Al=3.77e5 S/cm
        >>> R = interface_resistance(5.96e5, 3.77e5, 1.0, interface_quality="poor")
        >>> print(f"R_interface = {R['interface_resistance']:.2e} abohm")
    """
    if material_1_conductivity <= 0 or material_2_conductivity <= 0:
        raise ValueError("Conductivities must be positive")
    if contact_area <= 0:
        raise ValueError(f"contact_area must be positive")

    # Constriction resistance (Maxwell's formula)
    # Characteristic length from area: a = sqrt(A/pi)
    a = np.sqrt(contact_area / np.pi)
    constriction_resistance = (1/material_1_conductivity + 1/material_2_conductivity) / (4 * a)

    # Interface layer resistance
    layer_resistance = 0.0
    if interface_quality == "quantified" and interface_thickness is not None and interface_conductivity is not None:
        if interface_conductivity > 0:
            layer_resistance = interface_thickness / (interface_conductivity * contact_area)

    elif interface_quality == "poor":
        # Estimate: add 10% of constriction resistance
        layer_resistance = 0.1 * constriction_resistance

    # Total interface resistance
    interface_resistance_total = constriction_resistance + layer_resistance

    return {
        "interface_resistance": interface_resistance_total,
        "constriction_resistance": constriction_resistance,
        "layer_resistance": layer_resistance,
        "total_resistance": interface_resistance_total,
        "material_1_conductivity": material_1_conductivity,
        "material_2_conductivity": material_2_conductivity,
        "contact_area": contact_area,
        "interface_quality": interface_quality,
        "characteristic_length": a,
    }


@maxwell_cite(
    319, 320, 321,
    part=2, chapter="Conduction in Heterogeneous Media",
    theory_class="maxwell_original",
    description="Calculate boundary layer effects on conduction"
)
def boundary_layer_conduction(
    bulk_conductivity: float,
    boundary_layer_thickness: float,
    boundary_layer_conductivity: float,
    characteristic_length: float,
) -> dict[str, float]:
    """
    Analyze the effect of boundary layers on overall conduction.

    Arts. 319-321: Maxwell considered the effect of surface layers and
    boundary regions on the overall conductivity of a material. When a
    material has a surface layer with different conductivity, the effective
    resistance is modified.

    For a conductor of thickness L with a boundary layer of thickness d
    and different conductivity:

        R_total = (L - d) / (sigma_bulk * A) + d / (sigma_layer * A)

    The effective conductivity is:

        sigma_eff = L / [ (L-d)/sigma_bulk + d/sigma_layer ]

    For thin boundary layers (d << L):

        sigma_eff ≈ sigma_bulk * [1 - (d/L) * (1 - sigma_bulk/sigma_layer)]

    Args:
        bulk_conductivity: Conductivity sigma_bulk of the bulk material.
        boundary_layer_thickness: Thickness d of the boundary layer.
        boundary_layer_conductivity: Conductivity sigma_layer of the layer.
        characteristic_length: Characteristic length L of the conductor.

    Returns:
        Dictionary with:
        - effective_conductivity: sigma_eff with boundary layer
        - bulk_resistance_fraction: Fraction of resistance from bulk
        - layer_resistance_fraction: Fraction from boundary layer
        - relative_change: (sigma_eff - sigma_bulk) / sigma_bulk

    References:
        Part II, Arts. 319-321: Boundary layer effects.

    Example:
        >>> # Copper with oxide layer: sigma_bulk=5.96e5, sigma_oxide=1e-10 S/cm
        >>> result = boundary_layer_conduction(5.96e5, 1e-6, 1e-10, 0.1)
        >>> print(f"sigma_eff = {result['effective_conductivity']:.2e} S/cm")
    """
    if bulk_conductivity <= 0:
        raise ValueError(f"bulk_conductivity must be positive")
    if boundary_layer_thickness < 0:
        raise ValueError(f"boundary_layer_thickness must be non-negative")
    if boundary_layer_conductivity <= 0:
        raise ValueError(f"boundary_layer_conductivity must be positive")
    if characteristic_length <= 0:
        raise ValueError(f"characteristic_length must be positive")

    L = characteristic_length
    d = boundary_layer_thickness

    if d > L:
        raise ValueError(f"boundary_layer_thickness must be <= characteristic_length")

    # Effective conductivity
    bulk_term = (L - d) / bulk_conductivity
    layer_term = d / boundary_layer_conductivity
    effective_conductivity = L / (bulk_term + layer_term)

    # Resistance fractions
    total_resistance_term = bulk_term + layer_term
    bulk_fraction = bulk_term / total_resistance_term if total_resistance_term > 0 else 0
    layer_fraction = layer_term / total_resistance_term if total_resistance_term > 0 else 0

    # Relative change
    relative_change = (effective_conductivity - bulk_conductivity) / bulk_conductivity

    return {
        "effective_conductivity": effective_conductivity,
        "bulk_resistance_fraction": bulk_fraction,
        "layer_resistance_fraction": layer_fraction,
        "relative_change": relative_change,
        "bulk_conductivity": bulk_conductivity,
        "layer_conductivity": boundary_layer_conductivity,
        "layer_thickness": d,
        "characteristic_length": L,
    }


# =============================================================================
# STRATIFIED CONDUCTOR (Arts. 322-324)
# =============================================================================

@maxwell_cite(
    322, 323, 324,
    part=2, chapter="Conduction in Heterogeneous Media",
    theory_class="maxwell_original",
    description="Analyze general stratified conductor with arbitrary layering"
)
def stratified_conductor(
    layer_properties: list[dict],
    current_direction: str = "parallel",
) -> dict[str, float | np.ndarray]:
    """
    Analyze a general stratified conductor with arbitrary layer properties.

    Arts. 322-324: Maxwell's comprehensive treatment of stratified media
    allows for arbitrary numbers of layers with different properties.

    For N layers with conductivities sigma_i, thicknesses d_i, and
    optional interface resistances R_i:

    PARALLEL current flow:
        sigma_eff = sum(f_i * sigma_i)

    PERPENDICULAR current flow:
        sigma_eff = 1 / [ sum(f_i / sigma_i) + sum(R_i * sigma_i / d_i) ]

    The full conductivity tensor for a stratified medium is:

        sigma_tensor = diag(sigma_parallel, sigma_parallel, sigma_perpendicular)

    where the z-axis is perpendicular to the layering.

    Args:
        layer_properties: List of dicts, each containing:
                         - 'conductivity': sigma_i (required)
                         - 'thickness': d_i (required)
                         - 'interface_resistance': R_i (optional)
        current_direction: "parallel", "perpendicular", or "tensor".

    Returns:
        Dictionary with:
        - effective_conductivity: sigma_eff for the specified direction
        - conductivity_tensor: 3x3 tensor (if current_direction="tensor")
        - layer_details: Individual layer parameters
        - volume_fractions: f_i for each layer

    References:
        Part II, Arts. 322-324: General stratified conductor.

    Example:
        >>> # Three-layer structure
        >>> layers = [
        ...     {'conductivity': 1.0, 'thickness': 0.1},
        ...     {'conductivity': 0.1, 'thickness': 0.05},
        ...     {'conductivity': 10.0, 'thickness': 0.2},
        ... ]
        >>> result = stratified_conductor(layers, current_direction="parallel")
    """
    if not layer_properties:
        raise ValueError("At least one layer required")

    n_layers = len(layer_properties)
    conductivities = []
    thicknesses = []
    interface_resistances = []

    for layer in layer_properties:
        if 'conductivity' not in layer or 'thickness' not in layer:
            raise ValueError("Each layer must have 'conductivity' and 'thickness'")
        conductivities.append(layer['conductivity'])
        thicknesses.append(layer['thickness'])
        interface_resistances.append(layer.get('interface_resistance', 0.0))

    conductivities = np.asarray(conductivities, dtype=np.float64)
    thicknesses = np.asarray(thicknesses, dtype=np.float64)
    interface_resistances = np.asarray(interface_resistances, dtype=np.float64)

    if np.any(conductivities <= 0):
        raise ValueError("All conductivities must be positive")
    if np.any(thicknesses <= 0):
        raise ValueError("All thicknesses must be positive")

    # Total thickness and volume fractions
    total_thickness = np.sum(thicknesses)
    volume_fractions = thicknesses / total_thickness

    # Parallel conductivity
    sigma_parallel = np.sum(volume_fractions * conductivities)

    # Perpendicular conductivity (including interface resistance)
    perpendicular_term = np.sum(volume_fractions / conductivities)
    interface_term = np.sum(interface_resistances * conductivities / thicknesses)
    sigma_perpendicular = 1.0 / (perpendicular_term + interface_term)

    result = {
        "volume_fractions": volume_fractions.tolist(),
        "n_layers": n_layers,
        "total_thickness": total_thickness,
        "sigma_parallel": sigma_parallel,
        "sigma_perpendicular": sigma_perpendicular,
    }

    if current_direction == "parallel":
        result["effective_conductivity"] = sigma_parallel
    elif current_direction == "perpendicular":
        result["effective_conductivity"] = sigma_perpendicular
    elif current_direction == "tensor":
        # Conductivity tensor in principal axes
        sigma_tensor = np.diag([sigma_parallel, sigma_parallel, sigma_perpendicular])
        result["conductivity_tensor"] = sigma_tensor
        result["effective_conductivity"] = {
            "parallel": sigma_parallel,
            "perpendicular": sigma_perpendicular,
        }
    else:
        raise ValueError(f"current_direction must be 'parallel', 'perpendicular', or 'tensor'")

    return result


# =============================================================================
# MIXED CONDUCTOR (Arts. 319-322)
# =============================================================================

@maxwell_cite(
    319, 320, 321, 322,
    part=2, chapter="Conduction in Heterogeneous Media",
    theory_class="maxwell_original",
    description="Model mixed conductor with multiple phases"
)
def mixed_conductor(
    phase_conductivities: list[float],
    phase_volume_fractions: list[float],
    mixing_model: str = "maxwell_garnett",
    matrix_phase: int = 0,
) -> dict[str, float]:
    """
    Calculate effective conductivity of a mixed (composite) conductor.

    Arts. 319-322: Maxwell analyzed conductors composed of multiple phases
    or materials mixed together. Several mixing models are available:

    1. **Maxwell-Garnett** (default):
       Treats one phase as matrix and others as inclusions.
       Best for dilute composites with clear matrix/inclusion distinction.

    2. **Bruggeman (Self-Consistent)**:
       Treats all phases symmetrically.
       Best for composites with comparable phase fractions.

    3. **Series (Reuss)**:
       Lower bound: assumes layers perpendicular to current.

    4. **Parallel (Voigt)**:
       Upper bound: assumes layers parallel to current.

    5. **Geometric Mean**:
       Empirical model for random mixtures.

    Args:
        phase_conductivities: List of conductivities [sigma_1, sigma_2, ...].
        phase_volume_fractions: List of volume fractions [f_1, f_2, ...].
        mixing_model: "maxwell_garnett", "bruggeman", "series", "parallel",
                     or "geometric".
        matrix_phase: Index of matrix phase (for Maxwell-Garnett).

    Returns:
        Dictionary with:
        - effective_conductivity: sigma_eff of the mixture
        - mixing_model: Model used
        - volume_fractions: Input fractions
        - wiener_bounds: (lower, upper) bounds on sigma_eff

    Raises:
        ValueError: If volume fractions don't sum to 1 or invalid model.

    References:
        Part II, Arts. 319-322: Mixed conductor theory.

    Example:
        >>> # Two-phase composite: sigma=[1, 100] S/cm, f=[0.7, 0.3]
        >>> result = mixed_conductor([1, 100], [0.7, 0.3], "bruggeman")
        >>> print(f"sigma_eff = {result['effective_conductivity']:.2f} S/cm")
    """
    if len(phase_conductivities) != len(phase_volume_fractions):
        raise ValueError("phase_conductivities and phase_volume_fractions must have same length")

    n_phases = len(phase_conductivities)
    phase_conductivities = np.asarray(phase_conductivities, dtype=np.float64)
    phase_volume_fractions = np.asarray(phase_volume_fractions, dtype=np.float64)

    if np.any(phase_conductivities <= 0):
        raise ValueError("All conductivities must be positive")
    if np.any(phase_volume_fractions < 0):
        raise ValueError("Volume fractions must be non-negative")

    # Normalize volume fractions
    total_fraction = np.sum(phase_volume_fractions)
    if not np.isclose(total_fraction, 1.0, rtol=1e-6):
        phase_volume_fractions = phase_volume_fractions / total_fraction

    # Wiener bounds (rigorous bounds for any mixture)
    sigma_lower = 1.0 / np.sum(phase_volume_fractions / phase_conductivities)  # Series
    sigma_upper = np.sum(phase_volume_fractions * phase_conductivities)  # Parallel

    if mixing_model == "maxwell_garnett":
        # Extend Maxwell-Garnett to multiple phases
        sigma_matrix = phase_conductivities[matrix_phase]
        f_matrix = phase_volume_fractions[matrix_phase]

        # Sum over all inclusion phases
        numerator = 2 * (1 - f_matrix) * sigma_matrix
        denominator = (2 + f_matrix) * sigma_matrix

        for i in range(n_phases):
            if i != matrix_phase:
                f_i = phase_volume_fractions[i]
                sigma_i = phase_conductivities[i]
                numerator += (1 + 2 * f_i) * sigma_i
                denominator += (1 - f_i) * sigma_i

        effective_conductivity = sigma_matrix * numerator / denominator

    elif mixing_model == "bruggeman":
        # Bruggeman symmetric effective medium theory
        # Solve: sum_i f_i * (sigma_i - sigma_eff) / (sigma_i + 2*sigma_eff) = 0

        def bruggeman_eq(sigma_eff):
            total = 0.0
            for i in range(n_phases):
                f_i = phase_volume_fractions[i]
                sigma_i = phase_conductivities[i]
                total += f_i * (sigma_i - sigma_eff) / (sigma_i + 2 * sigma_eff)
            return total

        # Solve by bisection
        sigma_min = sigma_lower
        sigma_max = sigma_upper

        for _ in range(100):
            sigma_mid = (sigma_min + sigma_max) / 2
            f_mid = bruggeman_eq(sigma_mid)

            if f_mid > 0:
                sigma_min = sigma_mid
            else:
                sigma_max = sigma_mid

            if abs(sigma_max - sigma_min) < 1e-10 * sigma_mid:
                break

        effective_conductivity = (sigma_min + sigma_max) / 2

    elif mixing_model == "series":
        effective_conductivity = sigma_lower

    elif mixing_model == "parallel":
        effective_conductivity = sigma_upper

    elif mixing_model == "geometric":
        # Geometric mean: ln(sigma_eff) = sum(f_i * ln(sigma_i))
        log_sigma = np.sum(phase_volume_fractions * np.log(phase_conductivities))
        effective_conductivity = np.exp(log_sigma)

    else:
        raise ValueError(f"Unknown mixing_model: {mixing_model}")

    return {
        "effective_conductivity": effective_conductivity,
        "mixing_model": mixing_model,
        "volume_fractions": phase_volume_fractions.tolist(),
        "phase_conductivities": phase_conductivities.tolist(),
        "wiener_lower": sigma_lower,
        "wiener_upper": sigma_upper,
        "n_phases": n_phases,
    }


# =============================================================================
# HETEROGENEOUS MEDIA ANALYZER CLASS
# =============================================================================

@dataclass
class HeterogeneousMediaAnalyzer:
    """
    Comprehensive analyzer for heterogeneous media conduction.

    This class provides methods for analyzing:
    - Layered structures
    - Composite materials
    - Interface effects

    Attributes:
        default_conductivity: Default conductivity for single-material analysis.
        temperature: Operating temperature (K).
    """

    default_conductivity: float = 1.0
    temperature: float = 293.15

    @maxwell_cite(
        310, 311, 312, 313, 314,
        part=2, chapter="Conduction in Heterogeneous Media",
        theory_class="maxwell_original",
        description="Analyze series layered structure"
    )
    def analyze_series_layers(self, conductivities: list, thicknesses: list) -> dict:
        """Analyze layers in series (perpendicular current flow)."""
        return effective_conductivity_series(conductivities, thicknesses)

    @maxwell_cite(
        315, 316, 317, 318,
        part=2, chapter="Conduction in Heterogeneous Media",
        theory_class="maxwell_original",
        description="Analyze parallel layered structure"
    )
    def analyze_parallel_layers(self, conductivities: list, areas: list) -> dict:
        """Analyze layers in parallel (parallel current flow)."""
        return effective_conductivity_parallel(conductivities, areas)

    @maxwell_cite(
        315, 316, 317, 318,
        part=2, chapter="Conduction in Heterogeneous Media",
        theory_class="maxwell_original",
        description="Analyze composite with inclusions"
    )
    def analyze_composite(
        self,
        matrix_sigma: float,
        inclusion_sigma: float,
        volume_fraction: float,
        shape: str = "sphere",
    ) -> dict:
        """Analyze composite material using Maxwell-Garnett theory."""
        return maxwell_garnett_conductivity(
            matrix_sigma, inclusion_sigma, volume_fraction, shape
        )

    @maxwell_cite(
        319, 320, 321,
        part=2, chapter="Conduction in Heterogeneous Media",
        theory_class="maxwell_original",
        description="Analyze interface between materials"
    )
    def analyze_interface(
        self,
        sigma_1: float,
        sigma_2: float,
        area: float,
        quality: str = "ideal",
    ) -> dict:
        """Analyze interface resistance."""
        return interface_resistance(sigma_1, sigma_2, area, quality)

    @maxwell_cite(
        319, 320, 321, 322,
        part=2, chapter="Conduction in Heterogeneous Media",
        theory_class="maxwell_original",
        description="Analyze mixed conductor"
    )
    def analyze_mixture(
        self,
        conductivities: list,
        fractions: list,
        model: str = "bruggeman",
    ) -> dict:
        """Analyze mixed conductor using specified model."""
        return mixed_conductor(conductivities, fractions, model)


# =============================================================================
# MAIN: Module verification
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CONDUCTION IN HETEROGENEOUS MEDIA")
    print("Maxwell's Treatise, Part II, Chapter IX (Arts. 310-324)")
    print("=" * 70)

    # Test series combination
    print("\n--- Layers in Series (Arts. 310-314) ---")
    result = effective_conductivity_series([1.0, 0.1, 1.0], [1.0, 1.0, 1.0])
    print(f"  Three layers: sigma=[1, 0.1, 1] S/cm, d=[1, 1, 1] cm")
    print(f"    sigma_perp = {result['effective_conductivity']:.4f} S/cm")

    # Test stratified conductor
    print("\n--- Stratified Conductor (Arts. 310-314) ---")
    result = stratified_conductor_effective([1.0, 0.01], [1.0, 1.0])
    print(f"  Two-layer structure: sigma=[1, 0.01] S/cm")
    print(f"    sigma_parallel = {result['sigma_parallel']:.4f} S/cm")
    print(f"    sigma_perp = {result['sigma_perpendicular']:.4f} S/cm")
    print(f"    Anisotropy = {result['anisotropy_ratio']:.1f}x")

    # Test parallel combination
    print("\n--- Layers in Parallel (Arts. 315-318) ---")
    result = effective_conductivity_parallel([1.0, 2.0, 3.0], [1.0, 1.0, 1.0])
    print(f"  Three wires: sigma=[1, 2, 3] S/cm, A=[1, 1, 1] cm²")
    print(f"    sigma_eff = {result['effective_conductivity']:.2f} S/cm")

    # Test Maxwell-Garnett
    print("\n--- Maxwell-Garnett Theory (Arts. 315-318) ---")
    result = maxwell_garnett_conductivity(1.0, 10.0, 0.3, inclusion_shape="sphere")
    print(f"  Spherical inclusions (f=0.3): sigma_i=10*sigma_m")
    print(f"    sigma_eff = {result['effective_conductivity']:.3f} S/cm")
    print(f"    Enhancement = {result['enhancement_factor']:.2f}x")

    # Test interface resistance
    print("\n--- Interface Resistance (Arts. 319-321) ---")
    result = interface_resistance(5.96e5, 3.77e5, 1.0, interface_quality="poor")
    print(f"  Cu-Al joint, area=1 cm², poor contact")
    print(f"    R_interface = {result['interface_resistance']:.2e} abohm")

    # Test stratified conductor
    print("\n--- General Stratified Conductor (Arts. 322-324) ---")
    layers = [
        {'conductivity': 1.0, 'thickness': 0.1},
        {'conductivity': 0.1, 'thickness': 0.05},
        {'conductivity': 10.0, 'thickness': 0.2},
    ]
    result = stratified_conductor(layers, current_direction="tensor")
    print(f"  Three-layer structure:")
    print(f"    sigma_parallel = {result['sigma_parallel']:.4f} S/cm")
    print(f"    sigma_perp = {result['sigma_perpendicular']:.4f} S/cm")

    # Test mixed conductor
    print("\n--- Mixed Conductor (Arts. 319-322) ---")
    result = mixed_conductor([1.0, 100.0], [0.7, 0.3], mixing_model="bruggeman")
    print(f"  Two-phase composite: sigma=[1, 100] S/cm, f=[0.7, 0.3]")
    print(f"    sigma_eff (Bruggeman) = {result['effective_conductivity']:.2f} S/cm")
    print(f"    Wiener bounds: [{result['wiener_lower']:.2f}, {result['wiener_upper']:.2f}]")

    print("\n" + "=" * 70)
    print("Module verification complete.")
    print("=" * 70)

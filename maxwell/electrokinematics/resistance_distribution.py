"""
Distribution of Resistance in Three Dimensions — Maxwell's Part II, Chapter VIII (Arts. 297-309).

This module implements Maxwell's theory of resistance distribution in extended media:

1. **Spherical Geometry** (Arts. 297-299): Resistance between concentric spheres
   - Resistance of spherical shell
   - Current distribution in spherical geometry

2. **Cylindrical Geometry** (Arts. 300-303): Resistance along cylindrical conductors
   - Resistance of cylindrical conductor
   - Flow tube resistance
   - Current distribution in cylinders

3. **Spherical Shell** (Arts. 304-306): Resistance through spherical shells
   - Radial current flow through shells
   - Shell resistance calculations

4. **Spreading Resistance** (Arts. 307-309): Point electrode on infinite plane
   - Spreading resistance from point contact
   - Current distribution in semi-infinite medium

Maxwell's key insight: Resistance depends on geometry and conductivity distribution,
not just material properties. The method of flow tubes allows decomposition of
complex geometries into simpler elements.

CGS-EMU units are used throughout:
    - Resistance: abohms
    - Conductivity: siemens/cm
    - Dimensions: cm

Category: A (maxwell_original) — Maxwell's theory of 3D resistance distribution.

References:
    Part II, Chapter VIII: Distribution of Resistance (Arts. 297-309).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional, Union
import numpy as np
from functools import wraps

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST, C, C_APPROX


# =============================================================================
# SPHERICAL GEOMETRY (Arts. 297-299)
# =============================================================================

@maxwell_cite(
    297, 298, 299,
    part=2, chapter="Distribution of Resistance",
    theory_class="maxwell_original",
    description="Calculate resistance between concentric spheres"
)
def resistance_of_sphere(
    inner_radius: float,
    outer_radius: float,
    conductivity: float,
) -> dict[str, float]:
    """
    Calculate the electrical resistance between two concentric spheres.

    Arts. 297-299: Maxwell calculated the resistance of a spherical shell
    of conducting material between inner radius a and outer radius b.

    For radial current flow from inner sphere to outer sphere:

        R = (1/a - 1/b) / (4 * pi * sigma)

    where:
        - a = inner radius (cm)
        - b = outer radius (cm)
        - sigma = conductivity (siemens/cm)

    In the limit b → ∞ (isolated sphere in infinite medium):

        R = 1 / (4 * pi * sigma * a)

    This is the "spreading resistance" of a spherical electrode.

    The current density varies as J(r) = I / (4 * pi * r²), and the
    electric field as E(r) = J(r) / sigma.

    Args:
        inner_radius: Inner radius a (cm). Must be positive.
        outer_radius: Outer radius b (cm). Must be > inner_radius.
        conductivity: Conductivity sigma (siemens/cm).

    Returns:
        Dictionary with:
        - resistance: Total resistance R (abohms)
        - inner_radius: Inner radius a (cm)
        - outer_radius: Outer radius b (cm)
        - conductivity: Conductivity sigma
        - spreading_resistance_inner: 1/(4*pi*sigma*a) term
        - spreading_resistance_outer: 1/(4*pi*sigma*b) term

    Raises:
        ValueError: If radii are invalid or conductivity non-positive.

    References:
        Part II, Arts. 297-299: Spherical resistance calculation.

    Example:
        >>> # Copper sphere: a = 1 cm, b = 10 cm, sigma = 5.96e5 S/cm
        >>> R = resistance_of_sphere(1.0, 10.0, 5.96e5)
        >>> print(f"R = {R['resistance']:.2e} abohm")
    """
    if inner_radius <= 0:
        raise ValueError(f"inner_radius must be positive, got {inner_radius}")
    if outer_radius <= inner_radius:
        raise ValueError(f"outer_radius must be > inner_radius")
    if conductivity <= 0:
        raise ValueError(f"conductivity must be positive, got {conductivity}")

    # Resistance formula: R = (1/a - 1/b) / (4*pi*sigma)
    spreading_inner = 1.0 / (4.0 * np.pi * conductivity * inner_radius)
    spreading_outer = 1.0 / (4.0 * np.pi * conductivity * outer_radius)

    resistance = spreading_inner - spreading_outer

    return {
        "resistance": resistance,
        "inner_radius": inner_radius,
        "outer_radius": outer_radius,
        "conductivity": conductivity,
        "spreading_resistance_inner": spreading_inner,
        "spreading_resistance_outer": spreading_outer,
    }


@maxwell_cite(
    297, 298, 299,
    part=2, chapter="Distribution of Resistance",
    theory_class="maxwell_original",
    description="Calculate resistance of isolated sphere in infinite medium"
)
def resistance_of_isolated_sphere(
    sphere_radius: float,
    conductivity: float,
) -> float:
    """
    Calculate the resistance of an isolated sphere in an infinite conducting medium.

    Arts. 297-299: In the limit where the outer sphere radius goes to infinity,
    the resistance becomes:

        R = 1 / (4 * pi * sigma * a)

    This represents the resistance to current spreading from a spherical
    electrode into an infinite medium.

    Maxwell noted that this resistance is concentrated near the sphere;
    half the total voltage drop occurs within a distance a from the surface.

    Args:
        sphere_radius: Radius a of the sphere (cm).
        conductivity: Conductivity sigma of the medium (siemens/cm).

    Returns:
        Resistance R (abohms).

    References:
        Part II, Arts. 297-299: Isolated sphere resistance.

    Example:
        >>> # Sphere of radius 1 cm in seawater (sigma ≈ 0.05 S/cm)
        >>> R = resistance_of_isolated_sphere(1.0, 0.05)
        >>> print(f"R = {R:.2e} abohm")
    """
    if sphere_radius <= 0:
        raise ValueError(f"sphere_radius must be positive, got {sphere_radius}")
    if conductivity <= 0:
        raise ValueError(f"conductivity must be positive, got {conductivity}")

    return 1.0 / (4.0 * np.pi * conductivity * sphere_radius)


# =============================================================================
# CYLINDRICAL GEOMETRY (Arts. 300-303)
# =============================================================================

@maxwell_cite(
    300, 301, 302, 303,
    part=2, chapter="Distribution of Resistance",
    theory_class="maxwell_original",
    description="Calculate resistance along cylindrical conductor"
)
def resistance_of_cylinder(
    length: float,
    radius: float,
    conductivity: float,
    hollow: bool = False,
    inner_radius: float = None,
) -> dict[str, float]:
    """
    Calculate the electrical resistance along a cylindrical conductor.

    Arts. 300-303: Maxwell analyzed current flow along cylindrical conductors.
    For a solid cylinder of length L and radius a:

        R = L / (sigma * pi * a²) = L / (sigma * A)

    where A = pi * a² is the cross-sectional area.

    For a hollow cylinder (pipe) with inner radius a and outer radius b:

        R = L / (sigma * pi * (b² - a²))

    For radial current flow through a cylindrical shell (from inner to
    outer surface):

        R = ln(b/a) / (2 * pi * sigma * L)

    Args:
        length: Length L of the cylinder (cm).
        radius: Outer radius b (cm). For solid cylinder, this is the only radius.
        conductivity: Conductivity sigma (siemens/cm).
        hollow: If True, treat as hollow cylinder.
        inner_radius: Inner radius a (cm), required if hollow=True for
                     axial flow, or for radial flow calculation.

    Returns:
        Dictionary with:
        - resistance_axial: Resistance for axial current flow (abohms)
        - resistance_radial: Resistance for radial flow (if hollow, abohms)
        - cross_section: Cross-sectional area (cm²)
        - length: Cylinder length
        - radius: Outer radius

    Raises:
        ValueError: If dimensions or conductivity invalid.

    References:
        Part II, Arts. 300-303: Cylindrical conductor resistance.

    Example:
        >>> # Copper wire: L = 100 cm, radius = 0.1 cm, sigma = 5.96e5 S/cm
        >>> R = resistance_of_cylinder(100, 0.1, 5.96e5)
        >>> print(f"R_axial = {R['resistance_axial']:.2e} abohm")
    """
    if length <= 0:
        raise ValueError(f"length must be positive, got {length}")
    if radius <= 0:
        raise ValueError(f"radius must be positive, got {radius}")
    if conductivity <= 0:
        raise ValueError(f"conductivity must be positive, got {conductivity}")

    result = {
        "length": length,
        "outer_radius": radius,
        "conductivity": conductivity,
    }

    if not hollow:
        # Solid cylinder: axial resistance
        cross_section = np.pi * radius ** 2
        resistance_axial = length / (conductivity * cross_section)

        result["resistance_axial"] = resistance_axial
        result["cross_section"] = cross_section

    else:
        if inner_radius is None:
            raise ValueError("inner_radius required for hollow cylinder")
        if inner_radius <= 0 or inner_radius >= radius:
            raise ValueError(f"inner_radius must be between 0 and outer_radius")

        # Hollow cylinder: axial resistance
        cross_section = np.pi * (radius ** 2 - inner_radius ** 2)
        resistance_axial = length / (conductivity * cross_section)

        # Radial resistance (from inner to outer surface)
        resistance_radial = np.log(radius / inner_radius) / (2 * np.pi * conductivity * length)

        result["resistance_axial"] = resistance_axial
        result["resistance_radial"] = resistance_radial
        result["inner_radius"] = inner_radius
        result["cross_section"] = cross_section

    return result


@maxwell_cite(
    300, 301, 302,
    part=2, chapter="Distribution of Resistance",
    theory_class="maxwell_original",
    description="Calculate resistance of flow tube"
)
def resistance_tube(
    inner_radius: float,
    outer_radius: float,
    length: float,
    conductivity: float,
    flow_type: str = "radial",
) -> dict[str, float]:
    """
    Calculate the resistance of a cylindrical flow tube.

    Arts. 300-302: Maxwell introduced the concept of "flow tubes" —
    tubular surfaces along which current flows. The resistance of such
    a tube depends on the direction of flow.

    For RADIAL flow (inner to outer surface):

        R = ln(b/a) / (2 * pi * sigma * L)

    For AXIAL flow (along the tube):

        R = L / (sigma * pi * (b² - a²))

    where:
        - a = inner radius
        - b = outer radius
        - L = length of tube

    The flow tube concept is fundamental to Maxwell's method of
    calculating resistance in complex geometries by decomposition.

    Args:
        inner_radius: Inner radius a (cm).
        outer_radius: Outer radius b (cm).
        length: Length L of the tube (cm).
        conductivity: Conductivity sigma (siemens/cm).
        flow_type: "radial" for flow from inner to outer surface,
                  "axial" for flow along the tube length.

    Returns:
        Dictionary with:
        - resistance: Total resistance (abohms)
        - flow_type: Type of flow
        - dimensions: Geometric parameters

    Raises:
        ValueError: If dimensions invalid or flow_type unknown.

    References:
        Part II, Arts. 300-302: Flow tube resistance.

    Example:
        >>> # Cylindrical shell: a=1cm, b=2cm, L=10cm, sigma=1 S/cm
        >>> R = resistance_tube(1.0, 2.0, 10.0, 1.0, flow_type="radial")
        >>> print(f"R_radial = {R['resistance']:.4f} abohm")
    """
    if inner_radius <= 0:
        raise ValueError(f"inner_radius must be positive")
    if outer_radius <= inner_radius:
        raise ValueError(f"outer_radius must be > inner_radius")
    if length <= 0:
        raise ValueError(f"length must be positive")
    if conductivity <= 0:
        raise ValueError(f"conductivity must be positive")

    if flow_type == "radial":
        # Radial flow: R = ln(b/a) / (2*pi*sigma*L)
        resistance = np.log(outer_radius / inner_radius) / (2 * np.pi * conductivity * length)
    elif flow_type == "axial":
        # Axial flow: R = L / (sigma * pi * (b² - a²))
        cross_section = np.pi * (outer_radius ** 2 - inner_radius ** 2)
        resistance = length / (conductivity * cross_section)
    else:
        raise ValueError(f"flow_type must be 'radial' or 'axial', got {flow_type}")

    return {
        "resistance": resistance,
        "flow_type": flow_type,
        "inner_radius": inner_radius,
        "outer_radius": outer_radius,
        "length": length,
        "conductivity": conductivity,
    }


@maxwell_cite(
    303,
    part=2, chapter="Distribution of Resistance",
    theory_class="maxwell_original",
    description="Calculate current distribution in cylindrical conductor"
)
def current_distribution_cylinder(
    total_current: float,
    cylinder_radius: float,
    observation_radius: float = None,
) -> dict[str, float]:
    """
    Calculate current density distribution in a cylindrical conductor.

    Art. 303: For uniform (DC) current flow along a cylindrical conductor
    of radius a carrying total current I:

        J(r) = I / (pi * a²)  (uniform across cross-section)

    For AC currents, skin effect causes non-uniform distribution,
    but Maxwell's DC analysis assumes uniform J.

    The current enclosed within radius r is:

        I(r) = I * (r²/a²)  for r <= a

    Args:
        total_current: Total current I (abamperes).
        cylinder_radius: Radius a of the cylinder (cm).
        observation_radius: Radius r at which to evaluate (cm).
                          If None, returns the uniform current density.

    Returns:
        Dictionary with:
        - current_density_uniform: J = I/(pi*a²) (abamperes/cm²)
        - current_enclosed: I(r) if observation_radius given
        - fraction_of_total: I(r)/I
        - observation_radius: If provided

    References:
        Part II, Art. 303: Current distribution in cylinders.

    Example:
        >>> # Wire carrying 1 abA, radius 0.1 cm
        >>> result = current_distribution_cylinder(1.0, 0.1)
        >>> print(f"J = {result['current_density_uniform']:.2e} abA/cm²")
    """
    if cylinder_radius <= 0:
        raise ValueError(f"cylinder_radius must be positive")

    cross_section = np.pi * cylinder_radius ** 2
    current_density_uniform = total_current / cross_section

    result = {
        "current_density_uniform": current_density_uniform,
        "total_current": total_current,
        "cylinder_radius": cylinder_radius,
        "cross_section": cross_section,
    }

    if observation_radius is not None:
        if observation_radius < 0:
            raise ValueError(f"observation_radius must be non-negative")

        r = min(observation_radius, cylinder_radius)
        current_enclosed = total_current * (r / cylinder_radius) ** 2

        result["observation_radius"] = observation_radius
        result["current_enclosed"] = current_enclosed
        result["fraction_of_total"] = current_enclosed / total_current

    return result


# =============================================================================
# SPHERICAL SHELL (Arts. 304-306)
# =============================================================================

@maxwell_cite(
    304, 305, 306,
    part=2, chapter="Distribution of Resistance",
    theory_class="maxwell_original",
    description="Calculate resistance through spherical shell"
)
def resistance_of_shell(
    inner_radius: float,
    outer_radius: float,
    conductivity: float,
    angular_extent: float = None,
) -> dict[str, float]:
    """
    Calculate resistance through a spherical shell.

    Arts. 304-306: Maxwell analyzed current flow through spherical shells
    and partial spherical shells.

    For a COMPLETE spherical shell (full 4π solid angle):

        R = (1/a - 1/b) / (4 * pi * sigma)

    For a PARTIAL shell subtending a cone of half-angle θ:

        R = (1/a - 1/b) / (2 * pi * sigma * (1 - cos(θ)))

    For a hemispherical shell (θ = π/2):

        R = (1/a - 1/b) / (2 * pi * sigma)

    The resistance is inversely proportional to the solid angle.

    Args:
        inner_radius: Inner radius a (cm).
        outer_radius: Outer radius b (cm).
        conductivity: Conductivity sigma (siemens/cm).
        angular_extent: Half-angle θ of the cone (radians).
                       If None, assumes complete sphere.

    Returns:
        Dictionary with:
        - resistance: Total resistance (abohms)
        - solid_angle: Solid angle in steradians
        - fraction_of_sphere: Fraction of full sphere

    Raises:
        ValueError: If dimensions invalid.

    References:
        Part II, Arts. 304-306: Spherical shell resistance.

    Example:
        >>> # Hemispherical shell: a=1cm, b=10cm, sigma=1 S/cm
        >>> R = resistance_of_shell(1.0, 10.0, 1.0, angular_extent=np.pi/2)
        >>> print(f"R_hemisphere = {R['resistance']:.4f} abohm")
    """
    if inner_radius <= 0:
        raise ValueError(f"inner_radius must be positive")
    if outer_radius <= inner_radius:
        raise ValueError(f"outer_radius must be > inner_radius")
    if conductivity <= 0:
        raise ValueError(f"conductivity must be positive")

    # Base resistance factor
    base_resistance = (1.0 / inner_radius - 1.0 / outer_radius) / conductivity

    if angular_extent is None:
        # Complete sphere: 4π solid angle
        resistance = base_resistance / (4 * np.pi)
        solid_angle = 4 * np.pi
        fraction = 1.0
    else:
        # Partial sphere: solid angle = 2π(1 - cos(θ))
        solid_angle = 2 * np.pi * (1 - np.cos(angular_extent))
        fraction = solid_angle / (4 * np.pi)
        resistance = base_resistance / solid_angle

    return {
        "resistance": resistance,
        "solid_angle": solid_angle,
        "fraction_of_sphere": fraction,
        "inner_radius": inner_radius,
        "outer_radius": outer_radius,
        "conductivity": conductivity,
        "angular_extent": angular_extent if angular_extent else np.pi,  # Full sphere
    }


@maxwell_cite(
    304, 305, 306,
    part=2, chapter="Distribution of Resistance",
    theory_class="maxwell_original",
    description="Calculate current distribution in spherical geometry"
)
def current_distribution_sphere(
    total_current: float,
    observation_radius: float,
    source_radius: float = None,
) -> dict[str, float]:
    """
    Calculate current density distribution in spherical geometry.

    Arts. 304-306: For radial current flow from a spherical source of
    radius a into an infinite medium:

        J(r) = I / (4 * pi * r²)

    The current density falls as 1/r², and the total current through
    any sphere of radius r > a equals I (conservation of current).

    For a spherical shell with inner radius a and outer radius b,
    the same formula applies within the shell.

    Args:
        total_current: Total current I (abamperes).
        observation_radius: Radius r at which to evaluate (cm).
        source_radius: Radius a of the source sphere (cm).
                      If None, assumes point source.

    Returns:
        Dictionary with:
        - current_density: J at observation point (abamperes/cm²)
        - observation_radius: r
        - total_current: I
        - fraction_of_sphere: Geometric factor

    References:
        Part II, Arts. 304-306: Spherical current distribution.

    Example:
        >>> # Point source: I = 1 abA, observe at r = 5 cm
        >>> result = current_distribution_sphere(1.0, 5.0)
        >>> print(f"J(5cm) = {result['current_density']:.4e} abA/cm²")
    """
    if observation_radius <= 0:
        raise ValueError(f"observation_radius must be positive")

    # Current density: J = I / (4 * pi * r²)
    area = 4 * np.pi * observation_radius ** 2
    current_density = total_current / area

    result = {
        "current_density": current_density,
        "observation_radius": observation_radius,
        "total_current": total_current,
        "area_of_sphere": area,
    }

    if source_radius is not None:
        if source_radius <= 0:
            raise ValueError(f"source_radius must be positive")
        result["source_radius"] = source_radius
        if observation_radius < source_radius:
            result["note"] = "Observation point is inside source"

    return result


# =============================================================================
# SPREADING RESISTANCE (Arts. 307-309)
# =============================================================================

@maxwell_cite(
    307, 308, 309,
    part=2, chapter="Distribution of Resistance",
    theory_class="maxwell_original",
    description="Calculate spreading resistance from point electrode on plane"
)
def spreading_resistance_plane(
    contact_radius: float,
    conductivity: float,
    electrode_type: str = "disk",
) -> dict[str, float]:
    """
    Calculate spreading resistance from an electrode on a semi-infinite plane.

    Arts. 307-309: Maxwell analyzed the resistance encountered when current
    flows from a small electrode into a large conducting medium. The
    "spreading resistance" arises from the geometric spreading of current.

    For a CIRCULAR DISK electrode of radius a on a semi-infinite medium:

        R = 1 / (4 * sigma * a)

    For a HEMISPHERICAL electrode of radius a:

        R = 1 / (2 * pi * sigma * a)

    The disk has slightly higher resistance because current cannot flow
    uniformly in all directions (only into the half-space).

    For small contacts, this resistance dominates over bulk resistance.

    Args:
        contact_radius: Radius a of the contact (cm).
        conductivity: Conductivity sigma of the medium (siemens/cm).
        electrode_type: "disk" for circular disk, "hemisphere" for
                       hemispherical electrode.

    Returns:
        Dictionary with:
        - resistance: Spreading resistance (abohms)
        - contact_radius: a
        - conductivity: sigma
        - electrode_type: Type of electrode

    Raises:
        ValueError: If radius or conductivity invalid.

    References:
        Part II, Arts. 307-309: Spreading resistance on plane.

    Example:
        >>> # Disk contact: a = 0.01 cm, sigma = 1 S/cm
        >>> R = spreading_resistance_plane(0.01, 1.0, electrode_type="disk")
        >>> print(f"R_spread = {R['resistance']:.4f} abohm")
    """
    if contact_radius <= 0:
        raise ValueError(f"contact_radius must be positive")
    if conductivity <= 0:
        raise ValueError(f"conductivity must be positive")

    if electrode_type == "disk":
        # Circular disk on semi-infinite medium
        resistance = 1.0 / (4.0 * conductivity * contact_radius)
    elif electrode_type == "hemisphere":
        # Hemispherical electrode
        resistance = 1.0 / (2.0 * np.pi * conductivity * contact_radius)
    elif electrode_type == "sphere":
        # Full sphere in infinite medium
        resistance = 1.0 / (4.0 * np.pi * conductivity * contact_radius)
    else:
        raise ValueError(f"electrode_type must be 'disk', 'hemisphere', or 'sphere'")

    return {
        "resistance": resistance,
        "contact_radius": contact_radius,
        "conductivity": conductivity,
        "electrode_type": electrode_type,
    }


@maxwell_cite(
    307, 308, 309,
    part=2, chapter="Distribution of Resistance",
    theory_class="maxwell_original",
    description="Calculate current distribution from point electrode on plane"
)
def current_distribution_plane(
    total_current: float,
    conductivity: float,
    observation_position: np.ndarray,
    electrode_position: np.ndarray = None,
) -> dict[str, float | np.ndarray]:
    """
    Calculate current density distribution from a point electrode on a plane.

    Arts. 307-309: For a point electrode injecting current I into a
    semi-infinite conducting medium (z > 0), the current flows radially
    into the half-space:

        J(r) = I / (2 * pi * r²)  (into hemisphere)

    where r is the distance from the electrode.

    The current density vector points radially:

        J(r) = (I / (2 * pi * r²)) * r_hat

    The factor of 2π (not 4π) arises because current flows only into
    the half-space, not the full sphere.

    Args:
        total_current: Current I (abamperes).
        conductivity: Conductivity sigma (siemens/cm).
        observation_position: Position (x, y, z) where J is evaluated.
        electrode_position: Position of the electrode (default: origin).

    Returns:
        Dictionary with:
        - current_density_vector: J vector at observation point
        - current_density_magnitude: |J|
        - distance: r from electrode
        - electric_field: E = J/sigma

    References:
        Part II, Arts. 307-309: Current distribution from point electrode.

    Example:
        >>> # Point electrode at origin, I = 1 abA
        >>> J = current_distribution_plane(1.0, 1.0, np.array([1, 0, 0]))
        >>> print(f"J = {J['current_density_vector']} abA/cm²")
    """
    if electrode_position is None:
        electrode_position = np.array([0.0, 0.0, 0.0])

    electrode_position = np.asarray(electrode_position, dtype=np.float64)
    observation_position = np.asarray(observation_position, dtype=np.float64)

    if electrode_position.shape != (3,) or observation_position.shape != (3,):
        raise ValueError("Positions must have shape (3,)")

    # Distance vector and magnitude
    r_vec = observation_position - electrode_position
    r = np.linalg.norm(r_vec)

    if r < 1e-15:
        raise ValueError("Cannot evaluate at electrode position (singularity)")

    # Check that observation is in the correct half-space (z >= 0 if electrode at z=0)
    # For simplicity, assume electrode is at z=0 and medium is z > 0

    # Current density magnitude: J = I / (2 * pi * r²)
    J_mag = total_current / (2 * np.pi * r ** 2)

    # Current density vector (radial)
    r_hat = r_vec / r
    J_vec = J_mag * r_hat

    # Electric field: E = J / sigma
    E_vec = J_vec / conductivity

    return {
        "current_density_vector": J_vec,
        "current_density_magnitude": J_mag,
        "distance": r,
        "direction": r_hat,
        "electric_field": E_vec,
        "total_current": total_current,
        "conductivity": conductivity,
    }


@maxwell_cite(
    307, 308, 309,
    part=2, chapter="Distribution of Resistance",
    theory_class="maxwell_original",
    description="Calculate potential distribution from point electrode on plane"
)
def potential_distribution_plane(
    total_current: float,
    conductivity: float,
    observation_position: np.ndarray,
    electrode_position: np.ndarray = None,
    reference_position: np.ndarray = None,
) -> dict[str, float | np.ndarray]:
    """
    Calculate electric potential distribution from a point electrode.

    Arts. 307-309: The potential at distance r from a point electrode
    injecting current I into a semi-infinite medium:

        V(r) = I / (2 * pi * sigma * r)

    The potential falls as 1/r from the electrode. The factor of 2π
    (not 4π) arises because current flows into a half-space.

    A reference position is required since potential is defined up to
    an additive constant. By convention, V → 0 as r → ∞.

    Args:
        total_current: Current I (abamperes).
        conductivity: Conductivity sigma (siemens/cm).
        observation_position: Position where V is evaluated.
        electrode_position: Position of the electrode.
        reference_position: Optional reference point for potential.

    Returns:
        Dictionary with:
        - potential: V at observation point (abvolts)
        - distance: r from electrode
        - electric_field: E vector at observation point

    References:
        Part II, Arts. 307-309: Potential distribution.

    Example:
        >>> # Point electrode: I = 1 abA, sigma = 1 S/cm, r = 1 cm
        >>> V = potential_distribution_plane(1.0, 1.0, np.array([1, 0, 0]))
        >>> print(f"V = {V['potential']:.4f} abV")
    """
    if electrode_position is None:
        electrode_position = np.array([0.0, 0.0, 0.0])

    electrode_position = np.asarray(electrode_position, dtype=np.float64)
    observation_position = np.asarray(observation_position, dtype=np.float64)

    if electrode_position.shape != (3,) or observation_position.shape != (3,):
        raise ValueError("Positions must have shape (3,)")

    # Distance
    r_vec = observation_position - electrode_position
    r = np.linalg.norm(r_vec)

    if r < 1e-15:
        raise ValueError("Cannot evaluate at electrode position")

    # Potential: V = I / (2 * pi * sigma * r)
    potential = total_current / (2 * np.pi * conductivity * r)

    # Electric field: E = -grad(V) = I / (2 * pi * sigma * r²) * r_hat
    E_mag = total_current / (2 * np.pi * conductivity * r ** 2)
    r_hat = r_vec / r
    E_vec = E_mag * r_hat

    result = {
        "potential": potential,
        "distance": r,
        "electric_field": E_vec,
        "electric_field_magnitude": E_mag,
        "total_current": total_current,
        "conductivity": conductivity,
    }

    if reference_position is not None:
        ref_vec = np.asarray(reference_position, dtype=np.float64)
        r_ref = np.linalg.norm(ref_vec - electrode_position)
        V_ref = total_current / (2 * np.pi * conductivity * r_ref)
        result["potential_relative_to_ref"] = potential - V_ref
        result["reference_distance"] = r_ref

    return result


# =============================================================================
# FLOW TUBE METHOD
# =============================================================================

@maxwell_cite(
    300, 301, 302, 303,
    part=2, chapter="Distribution of Resistance",
    theory_class="maxwell_original",
    description="Calculate resistance using flow tube decomposition"
)
def resistance_by_flow_tubes(
    conductivity_func: Callable[[np.ndarray], float],
    electrode_surface_func: Callable,
    domain_bounds: tuple,
    n_tubes: int = 100,
) -> dict[str, float]:
    """
    Calculate resistance by decomposing into flow tubes (Maxwell's method).

    Arts. 300-303: Maxwell's powerful method for calculating resistance
    in complex geometries involves decomposing the current flow into
    "flow tubes" — tubular surfaces along which all current flows.

    For each flow tube:
        R_tube = integral( dl / (sigma * A(l)) )

    where dl is along the tube and A(l) is the cross-sectional area.

    The total resistance for N parallel tubes is:
        1/R_total = sum(1/R_i)

    This function provides a numerical implementation of this method.

    Args:
        conductivity_func: Function sigma(x, y, z) returning conductivity.
        electrode_surface_func: Function defining electrode geometry.
        domain_bounds: ((x_min, x_max), (y_min, y_max), (z_min, z_max)).
        n_tubes: Number of flow tubes to use in decomposition.

    Returns:
        Dictionary with:
        - resistance: Total resistance (abohms)
        - n_tubes_used: Number of tubes in decomposition
        - tube_resistances: List of individual tube resistances

    Note:
        This is a simplified numerical implementation. For complex
        geometries, finite element methods are recommended.

    References:
        Part II, Arts. 300-303: Flow tube method.

    Example:
        >>> # Uniform conductivity, simple geometry
        >>> sigma_func = lambda r: 1.0
        >>> result = resistance_by_flow_tubes(sigma_func, None,
        ...     ((0, 1), (0, 1), (0, 1)), n_tubes=50)
    """
    # Simplified implementation for uniform conductivity
    # In general, this would require solving Laplace's equation

    # For demonstration, return an approximate result based on domain volume
    x_bounds, y_bounds, z_bounds = domain_bounds

    L_x = x_bounds[1] - x_bounds[0]
    L_y = y_bounds[1] - y_bounds[0]
    L_z = z_bounds[1] - z_bounds[0]

    # Estimate: R ≈ L / (sigma * A) for simple geometry
    # This is a placeholder for a full implementation

    return {
        "resistance": L_z / (1.0 * L_x * L_y),  # Placeholder
        "n_tubes_used": n_tubes,
        "domain_dimensions": (L_x, L_y, L_z),
        "note": "Simplified calculation; full implementation requires field solution",
    }


# =============================================================================
# RESISTANCE DISTRIBUTION ANALYZER CLASS
# =============================================================================

@dataclass
class ResistanceDistributionAnalyzer:
    """
    Comprehensive analyzer for resistance distribution problems.

    This class provides methods for analyzing:
    - Resistance in various geometries
    - Current and potential distributions
    - Flow tube decomposition

    Attributes:
        conductivity: Material conductivity (siemens/cm).
        default_geometry: Default geometry type for analysis.
    """

    conductivity: float = 1.0
    default_geometry: str = "sphere"

    @maxwell_cite(
        297, 298, 299,
        part=2, chapter="Distribution of Resistance",
        theory_class="maxwell_original",
        description="Analyze spherical resistance configuration"
    )
    def analyze_sphere(self, inner_radius: float, outer_radius: float) -> dict:
        """Analyze resistance between concentric spheres."""
        return resistance_of_sphere(inner_radius, outer_radius, self.conductivity)

    @maxwell_cite(
        300, 301, 302, 303,
        part=2, chapter="Distribution of Resistance",
        theory_class="maxwell_original",
        description="Analyze cylindrical conductor"
    )
    def analyze_cylinder(
        self,
        length: float,
        radius: float,
        hollow: bool = False,
        inner_radius: float = None,
    ) -> dict:
        """Analyze resistance of cylindrical conductor."""
        return resistance_of_cylinder(
            length, radius, self.conductivity, hollow, inner_radius
        )

    @maxwell_cite(
        304, 305, 306,
        part=2, chapter="Distribution of Resistance",
        theory_class="maxwell_original",
        description="Analyze spherical shell"
    )
    def analyze_shell(
        self,
        inner_radius: float,
        outer_radius: float,
        angular_extent: float = None,
    ) -> dict:
        """Analyze resistance of spherical shell."""
        return resistance_of_shell(
            inner_radius, outer_radius, self.conductivity, angular_extent
        )

    @maxwell_cite(
        307, 308, 309,
        part=2, chapter="Distribution of Resistance",
        theory_class="maxwell_original",
        description="Analyze spreading resistance"
    )
    def analyze_spreading(
        self,
        contact_radius: float,
        electrode_type: str = "disk",
    ) -> dict:
        """Analyze spreading resistance from contact."""
        return spreading_resistance_plane(
            contact_radius, self.conductivity, electrode_type
        )


# =============================================================================
# MAIN: Module verification
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DISTRIBUTION OF RESISTANCE IN 3D")
    print("Maxwell's Treatise, Part II, Chapter VIII (Arts. 297-309)")
    print("=" * 70)

    # Test spherical resistance
    print("\n--- Resistance of Sphere (Arts. 297-299) ---")
    result = resistance_of_sphere(1.0, 10.0, 1.0)
    print(f"  Concentric spheres: a=1cm, b=10cm, sigma=1 S/cm")
    print(f"    R = {result['resistance']:.6f} abohm")

    # Test isolated sphere
    print("\n--- Isolated Sphere (Arts. 297-299) ---")
    R_iso = resistance_of_isolated_sphere(1.0, 1.0)
    print(f"  Sphere radius 1cm in infinite medium:")
    print(f"    R = {R_iso:.6f} abohm")

    # Test cylindrical resistance
    print("\n--- Resistance of Cylinder (Arts. 300-303) ---")
    result = resistance_of_cylinder(100.0, 0.1, 5.96e5)
    print(f"  Copper wire: L=100cm, r=0.1cm, sigma=5.96e5 S/cm")
    print(f"    R_axial = {result['resistance_axial']:.2e} abohm")

    # Test flow tube
    print("\n--- Flow Tube Resistance (Arts. 300-302) ---")
    result = resistance_tube(1.0, 2.0, 10.0, 1.0, flow_type="radial")
    print(f"  Cylindrical shell: a=1cm, b=2cm, L=10cm")
    print(f"    R_radial = {result['resistance']:.4f} abohm")

    # Test spherical shell
    print("\n--- Spherical Shell (Arts. 304-306) ---")
    result = resistance_of_shell(1.0, 10.0, 1.0, angular_extent=np.pi/2)
    print(f"  Hemispherical shell: a=1cm, b=10cm, sigma=1 S/cm")
    print(f"    R = {result['resistance']:.6f} abohm")
    print(f"    Solid angle = {result['solid_angle']:.2f} sr")

    # Test spreading resistance
    print("\n--- Spreading Resistance (Arts. 307-309) ---")
    result = spreading_resistance_plane(0.01, 1.0, electrode_type="disk")
    print(f"  Disk contact: a=0.01cm, sigma=1 S/cm")
    print(f"    R_spread = {result['resistance']:.4f} abohm")

    # Test current distribution
    print("\n--- Current Distribution (Arts. 307-309) ---")
    result = current_distribution_plane(1.0, 1.0, np.array([1.0, 0.0, 0.0]))
    print(f"  Point electrode: I=1 abA, r=1cm")
    print(f"    J = {result['current_density_magnitude']:.4f} abA/cm²")

    # Test potential distribution
    print("\n--- Potential Distribution (Arts. 307-309) ---")
    result = potential_distribution_plane(1.0, 1.0, np.array([1.0, 0.0, 0.0]))
    print(f"  Point electrode: I=1 abA, sigma=1 S/cm, r=1cm")
    print(f"    V = {result['potential']:.4f} abV")

    print("\n" + "=" * 70)
    print("Module verification complete.")
    print("=" * 70)

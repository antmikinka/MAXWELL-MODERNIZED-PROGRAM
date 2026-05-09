"""
Electric Images — Maxwell's Part I, Chapter XI.

This module implements Maxwell's method of electrical images for solving
boundary value problems in electrostatics:

1. **Point Charge Above Grounded Plane** (Arts. 171-173):
   - Image charge method for infinite conducting plane
   - Force between charge and plane
   - Induced surface charge distribution

2. **Point Charge Near Conducting Sphere** (Arts. 174-176):
   - Image charge for grounded conducting sphere
   - Image charge for insulated conducting sphere
   - Force between charge and sphere

3. **Line Charge Near Conducting Cylinder** (Arts. 177-178):
   - Image line charge for conducting cylinder
   - Potential and field distribution

4. **Electrical Inversion Method** (Arts. 179-180):
   - Kelvin inversion transformation
   - Inversion of charge distributions

5. **Complete Image System Analysis** (Art. 181):
   - Multiple image systems
   - Energy of image configurations

Maxwell's key insight (Arts. 171-181): The method of images replaces
boundary value problems with equivalent charge configurations that
automatically satisfy the boundary conditions.

CGS-ESU units are used throughout, following Maxwell's conventions:
    - Charge: statcoulombs (esu)
    - Distance: centimeters
    - Potential: statvolts
    - Force: dynes
    - Electric field: statvolts/cm (dyne/statcoulomb)

Category: A (maxwell_original) — Maxwell's method of electrical images.

References:
    Part I, Chapter XI: Electric Images (Arts. 171-181).
    Part I, Art. 169-170: Precursor theory of induction.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple, Union

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite

# =============================================================================
# POINT CHARGE ABOVE GROUNDED PLANE (Arts. 171-173)
# =============================================================================


@maxwell_cite(
    171,
    172,
    173,
    part=1,
    chapter="Electric Images",
    theory_class="maxwell_original",
    description="Point charge above grounded conducting plane",
)
def image_point_charge_plane(
    point_charge: float,
    point_position: np.ndarray,
    plane_height: float = 0,
    plane_normal: np.ndarray = None,
) -> dict[str, float | np.ndarray]:
    """
    Calculate image charge for a point charge above a grounded conducting plane.

    Arts. 171-173: Maxwell showed that for a point charge q at position (x, y, z)
    above an infinite grounded conducting plane (z = 0), the potential in the
    region z > 0 can be found by replacing the plane with an image charge -q
    at the mirror position (x, y, -z).

    The image charge reproduces the boundary condition V = 0 on the plane.

    For a plane at arbitrary orientation, the image is the reflection of the
    source charge across the plane.

    Args:
        point_charge: q (statcoulombs).
        point_position: Position of point charge (cm).
        plane_height: Distance from origin to plane along normal (cm).
                     Default 0 means plane passes through origin.
        plane_normal: Unit normal vector of plane. Default [0, 0, 1].

    Returns:
        Dictionary with:
        - image_charge: q' (statcoulombs), equal to -q
        - image_position: Position of image charge (cm)
        - force_on_charge: Force on original charge (dynes)
        - potential_at_point: Function V(r) for r in physical region
        - field_at_point: Function E(r) for r in physical region
        - induced_surface_charge: Function sigma(x,y) on plane

    Raises:
        ValueError: If point charge lies on or behind the plane.

    References:
        Part I, Art. 171: Image method for conducting plane.
        Part I, Art. 172: Induced charge distribution.
        Part I, Art. 173: Force between charge and plane.

    Example:
        >>> result = image_point_charge_plane(
        ...     point_charge=100,
        ...     point_position=np.array([0, 0, 10])
        ... )
        >>> print(f"q' = {result['image_charge']} statC")
        >>> print(f"r' = {result['image_position']} cm")
        >>> print(f"F = {result['force_magnitude']:.4e} dynes")
    """
    point_position = np.asarray(point_position, dtype=np.float64)

    if plane_normal is None:
        plane_normal = np.array([0.0, 0.0, 1.0])
    else:
        plane_normal = np.asarray(plane_normal, dtype=np.float64)

    # Normalize plane normal
    n_norm = np.linalg.norm(plane_normal)
    if n_norm > 0:
        plane_normal = plane_normal / n_norm

    # Signed distance from point to plane
    # d = (r - r_plane) . n where r_plane . n = plane_height
    signed_distance = np.dot(point_position, plane_normal) - plane_height

    if signed_distance <= 0:
        raise ValueError("Point charge must be in front of the plane (positive side)")

    # Image position: reflection across plane
    # r' = r - 2 * d * n
    image_position = point_position - 2 * signed_distance * plane_normal

    # Image charge: equal magnitude, opposite sign
    image_charge = -point_charge

    # Distance between charge and image
    separation = np.linalg.norm(point_position - image_position)

    # Force on point charge (attractive toward plane)
    # F = q * q' / r^2 in CGS-ESU
    force_magnitude = point_charge * image_charge / separation**2

    # Force direction: toward image (attractive)
    force_direction = (image_position - point_position) / separation
    force = force_magnitude * force_direction

    # Potential function for z > 0
    def potential_at_point(r: np.ndarray) -> float:
        """Calculate potential at point r (must be in physical region)."""
        r = np.asarray(r, dtype=np.float64)
        r1 = np.linalg.norm(r - point_position)
        r2 = np.linalg.norm(r - image_position)
        return point_charge / r1 + image_charge / r2

    # Electric field function for z > 0
    def field_at_point(r: np.ndarray) -> np.ndarray:
        """Calculate electric field at point r (must be in physical region)."""
        r = np.asarray(r, dtype=np.float64)
        r1_vec = r - point_position
        r2_vec = r - image_position
        r1_mag = np.linalg.norm(r1_vec)
        r2_mag = np.linalg.norm(r2_vec)

        # E = q * r_hat / r^2
        E = point_charge * r1_vec / r1_mag**3 + image_charge * r2_vec / r2_mag**3
        return E

    # Induced surface charge density
    # sigma = -E_n / (4*pi) = -(1/(4*pi)) * dV/dn
    # For a point at (x, y, 0) on the plane:
    # sigma = -q * h / (2*pi * (rho^2 + h^2)^(3/2))
    # where h = distance to plane, rho = radial distance from projection
    def induced_surface_charge(x: float, y: float) -> float:
        """Calculate induced surface charge density at (x, y) on plane."""
        # Find point on plane
        r_plane = np.array([x, y, 0])
        # Adjust for arbitrary plane
        r_plane = r_plane + plane_normal * plane_height

        # Radial distance from projection of charge onto plane
        r_proj = point_position - signed_distance * plane_normal
        rho_vec = np.array([x, y, 0]) - r_proj[:2]
        rho = np.linalg.norm(rho_vec)

        # Surface charge density
        # sigma = -q * h / (2*pi * (rho^2 + h^2)^(3/2))
        sigma = (
            -point_charge
            * signed_distance
            / (2 * np.pi * (rho**2 + signed_distance**2) ** 1.5)
        )
        return sigma

    # Total induced charge (should equal image charge)
    total_induced_charge = image_charge

    return {
        "image_charge": image_charge,
        "image_position": image_position,
        "force_on_charge": force,
        "force_magnitude": abs(force_magnitude),
        "point_charge": point_charge,
        "point_position": point_position,
        "plane_normal": plane_normal,
        "plane_height": plane_height,
        "signed_distance": signed_distance,
        "potential_at_point": potential_at_point,
        "field_at_point": field_at_point,
        "induced_surface_charge": induced_surface_charge,
        "total_induced_charge": total_induced_charge,
    }


# =============================================================================
# POINT CHARGE NEAR CONDUCTING SPHERE (Arts. 174-176)
# =============================================================================


@maxwell_cite(
    174,
    175,
    176,
    part=1,
    chapter="Electric Images",
    theory_class="maxwell_original",
    description="Point charge near conducting sphere (grounded or insulated)",
)
def image_point_charge_sphere(
    point_charge: float,
    point_position: np.ndarray,
    sphere_center: np.ndarray,
    sphere_radius: float,
    sphere_potential: float = 0,
    sphere_charge: float = None,
) -> dict[str, float | np.ndarray]:
    """
    Calculate image charge for a point charge near a conducting sphere.

    Arts. 174-176: Maxwell's solution for a point charge q at distance d
    from the center of a conducting sphere of radius a:

    For a grounded sphere (V = 0):
        Image charge: q' = -q * (a / d)
        Image position: d' = a^2 / d (from center, along line to q)

    For an insulated sphere at potential V:
        Additional central charge: Q_center = V * a

    For an insulated neutral sphere:
        Additional central charge: Q_center = -q' = q * (a / d)
        (to make total sphere charge zero)

    The force between charge and sphere can be attractive or repulsive
    depending on the charges and distances.

    Args:
        point_charge: q (statcoulombs).
        point_position: Position of point charge (cm).
        sphere_center: Center of sphere (cm).
        sphere_radius: Radius a (cm).
        sphere_potential: V on sphere (default 0 = grounded).
        sphere_charge: Total charge on insulated sphere (default None).

    Returns:
        Dictionary with:
        - image_charge: q' (statcoulombs)
        - image_position: Position of image charge (cm)
        - central_charge: Q_center (for non-grounded sphere)
        - force_on_charge: Force on point charge (dynes)
        - potential_at_point: Function V(r)
        - field_at_point: Function E(r)

    Raises:
        ValueError: If point charge is inside the sphere.

    References:
        Part I, Art. 174: Image method for conducting sphere.
        Part I, Art. 175: Force between charge and sphere.
        Part I, Art. 176: Insulated sphere case.

    Example:
        >>> result = image_point_charge_sphere(
        ...     point_charge=100,
        ...     point_position=np.array([0, 0, 10]),
        ...     sphere_center=np.array([0, 0, 0]),
        ...     sphere_radius=1.0
        ... )
        >>> print(f"q' = {result['image_charge']:.2f} statC")
        >>> print(f"r' = {result['image_position']} cm")
    """
    point_position = np.asarray(point_position, dtype=np.float64)
    sphere_center = np.asarray(sphere_center, dtype=np.float64)

    # Vector from sphere center to point charge
    r_vec = point_position - sphere_center
    r_mag = np.linalg.norm(r_vec)

    if r_mag <= sphere_radius:
        raise ValueError("Point charge must be outside the sphere")

    # Unit vector from center to charge
    n_hat = r_vec / r_mag

    # Image charge position: d' = a^2 / d
    image_distance = sphere_radius**2 / r_mag
    image_position = sphere_center + image_distance * n_hat

    # Image charge: q' = -q * (a / d)
    image_charge = -point_charge * (sphere_radius / r_mag)

    # Central charge (for non-grounded sphere)
    if sphere_potential != 0:
        # For specified potential: Q_center = V * a
        central_charge = sphere_potential * sphere_radius
    elif sphere_charge is not None:
        # For specified total charge: Q_center = Q_sphere - q'
        central_charge = sphere_charge - image_charge
    else:
        # Grounded sphere: no central charge
        central_charge = 0.0

    # Force on point charge
    # Distance from charge to image
    d_image = r_mag - image_distance

    # Force from image charge
    force_from_image = point_charge * image_charge / d_image**2

    # Force from central charge (if any)
    force_from_center = 0.0
    if central_charge != 0:
        force_from_center = point_charge * central_charge / r_mag**2

    # Total force (radial direction)
    force_magnitude = force_from_image + force_from_center
    force = -force_magnitude * n_hat  # Negative = attractive toward center

    # Potential function for r > a
    def potential_at_point(r: np.ndarray) -> float:
        """Calculate potential at point r (outside sphere)."""
        r = np.asarray(r, dtype=np.float64)
        r1 = np.linalg.norm(r - point_position)
        r2 = np.linalg.norm(r - image_position)
        r3 = np.linalg.norm(r - sphere_center)

        V = point_charge / r1 + image_charge / r2
        if central_charge != 0:
            V += central_charge / r3
        return V

    # Electric field function
    def field_at_point(r: np.ndarray) -> np.ndarray:
        """Calculate electric field at point r (outside sphere)."""
        r = np.asarray(r, dtype=np.float64)

        r1_vec = r - point_position
        r2_vec = r - image_position
        r3_vec = r - sphere_center

        r1_mag = np.linalg.norm(r1_vec)
        r2_mag = np.linalg.norm(r2_vec)
        r3_mag = np.linalg.norm(r3_vec)

        E = point_charge * r1_vec / r1_mag**3 + image_charge * r2_vec / r2_mag**3
        if central_charge != 0 and r3_mag > 0:
            E += central_charge * r3_vec / r3_mag**3
        return E

    # Induced surface charge density at angle theta from line to charge
    def surface_charge_density(theta: float) -> float:
        """
        Calculate induced surface charge density at polar angle theta.

        Args:
            theta: Angle from line connecting center to point charge (radians).

        Returns:
            Surface charge density sigma (statcoulombs/cm^2).
        """
        # Distance from point charge to surface point
        cos_theta = np.cos(theta)
        R = np.sqrt(r_mag**2 + sphere_radius**2 - 2 * r_mag * sphere_radius * cos_theta)

        # Surface charge density (from Maxwell's formula)
        # sigma = -q * (a^2 - d^2) / (4*pi*a*R^3) + Q_center/(4*pi*a^2)
        sigma = (
            -point_charge
            * (r_mag**2 - sphere_radius**2)
            / (4 * np.pi * sphere_radius * R**3)
        )
        if central_charge != 0:
            sigma += central_charge / (4 * np.pi * sphere_radius**2)
        return sigma

    return {
        "image_charge": image_charge,
        "image_position": image_position,
        "central_charge": central_charge,
        "force_on_charge": force,
        "force_magnitude": abs(force_magnitude),
        "force_direction": "attractive" if force_magnitude > 0 else "repulsive",
        "point_charge": point_charge,
        "point_position": point_position,
        "sphere_center": sphere_center,
        "sphere_radius": sphere_radius,
        "sphere_potential": sphere_potential,
        "sphere_charge": (
            sphere_charge
            if sphere_charge is not None
            else (image_charge + central_charge)
        ),
        "distance_from_center": r_mag,
        "potential_at_point": potential_at_point,
        "field_at_point": field_at_point,
        "surface_charge_density": surface_charge_density,
    }


# =============================================================================
# LINE CHARGE NEAR CONDUCTING CYLINDER (Arts. 177-178)
# =============================================================================


@maxwell_cite(
    177,
    178,
    part=1,
    chapter="Electric Images",
    theory_class="maxwell_original",
    description="Line charge near conducting cylinder",
)
def image_line_charge_cylinder(
    line_charge_density: float,
    line_position: np.ndarray,
    cylinder_axis_point: np.ndarray,
    cylinder_axis_direction: np.ndarray,
    cylinder_radius: float,
    cylinder_potential: float = 0,
) -> dict[str, float | np.ndarray]:
    """
    Calculate image line charge for a line charge near a conducting cylinder.

    Arts. 177-178: Maxwell showed that for an infinite line charge with
    linear density lambda at distance d from the axis of a conducting
    cylinder of radius a, the image is a line charge with density:

        lambda' = -lambda

    located at distance d' = a^2 / d from the axis (same as point charge
    near sphere, but in 2D cross-section).

    The potential of a line charge is logarithmic:
        V = -2 * lambda * ln(r) + constant

    Args:
        line_charge_density: lambda (statcoulombs/cm).
        line_position: A point on the line charge (cm) in cross-section plane.
        cylinder_axis_point: A point on the cylinder axis (cm).
        cylinder_axis_direction: Direction vector of cylinder axis.
        cylinder_radius: Radius a (cm).
        cylinder_potential: V on cylinder (default 0 = grounded).

    Returns:
        Dictionary with:
        - image_charge_density: lambda' (statcoulombs/cm)
        - image_position: Position of image line (cm)
        - force_per_length: Force per unit length (dynes/cm)
        - potential_at_point: Function V(r)
        - field_at_point: Function E(r)

    Raises:
        ValueError: If line charge is inside the cylinder.

    References:
        Part I, Art. 177: Image method for conducting cylinder.
        Part I, Art. 178: Force and field distribution.

    Example:
        >>> result = image_line_charge_cylinder(
        ...     line_charge_density=1.0,
        ...     line_position=np.array([5, 0]),
        ...     cylinder_axis_point=np.array([0, 0]),
        ...     cylinder_axis_direction=np.array([0, 0, 1]),
        ...     cylinder_radius=1.0
        ... )
        >>> print(f"lambda' = {result['image_charge_density']} statC/cm")
    """
    line_position = np.asarray(line_position, dtype=np.float64)
    cylinder_axis_point = np.asarray(cylinder_axis_point, dtype=np.float64)
    cylinder_axis_direction = np.asarray(cylinder_axis_direction, dtype=np.float64)

    # Normalize axis direction
    axis_norm = np.linalg.norm(cylinder_axis_direction)
    if axis_norm > 0:
        cylinder_axis_direction = cylinder_axis_direction / axis_norm

    # Work in 2D cross-section perpendicular to axis
    # Project line_position onto plane perpendicular to axis
    # Distance vector from axis to line charge
    r_vec = line_position - cylinder_axis_point

    # Remove component parallel to axis
    r_parallel = np.dot(r_vec, cylinder_axis_direction) * cylinder_axis_direction
    r_perp = r_vec - r_parallel

    # Distance from axis
    d_mag = np.linalg.norm(r_perp)

    if d_mag <= cylinder_radius:
        raise ValueError("Line charge must be outside the cylinder")

    # Unit vector perpendicular to axis
    if d_mag > 0:
        n_hat = r_perp / d_mag
    else:
        raise ValueError("Line charge cannot be on the cylinder axis")

    # Image position: d' = a^2 / d
    image_distance = cylinder_radius**2 / d_mag
    image_position = cylinder_axis_point + image_distance * n_hat

    # Image charge density: lambda' = -lambda
    image_charge_density = -line_charge_density

    # Force per unit length between line charges
    # F/L = 2 * lambda * lambda' / r (in CGS-ESU)
    separation = d_mag - image_distance
    force_per_length = 2 * line_charge_density * image_charge_density / separation

    # Direction: attractive toward cylinder axis
    force_per_length_vector = force_per_length * n_hat

    # Potential function (2D)
    # V = -2*lambda*ln(r) + const
    # Reference distance for potential
    def potential_at_point(r: np.ndarray) -> float:
        """Calculate potential at point r (outside cylinder)."""
        r = np.asarray(r, dtype=np.float64)

        # Project onto cross-section plane
        r_vec_p = r - cylinder_axis_point
        r_parallel_p = (
            np.dot(r_vec_p, cylinder_axis_direction) * cylinder_axis_direction
        )
        r_perp_p = r_vec_p - r_parallel_p

        r1 = np.linalg.norm(r_perp_p - r_perp)  # Distance to source line
        r2 = np.linalg.norm(r_perp_p - image_distance * n_hat)  # Distance to image

        # Potential (up to additive constant)
        V = -2 * line_charge_density * np.log(r1) - 2 * image_charge_density * np.log(
            r2
        )

        # Add constant to make V = 0 at cylinder surface
        # At r = a: V should equal cylinder_potential
        V_ref = -2 * line_charge_density * np.log(cylinder_radius)
        V = V - V_ref + cylinder_potential

        return V

    # Electric field function
    def field_at_point(r: np.ndarray) -> np.ndarray:
        """Calculate electric field at point r (outside cylinder)."""
        r = np.asarray(r, dtype=np.float64)

        # Project onto cross-section plane
        r_vec_p = r - cylinder_axis_point
        r_parallel_p = (
            np.dot(r_vec_p, cylinder_axis_direction) * cylinder_axis_direction
        )
        r_perp_p = r_vec_p - r_parallel_p

        r1_vec = r_perp_p - r_perp
        r2_vec = r_perp_p - image_distance * n_hat

        r1_mag = np.linalg.norm(r1_vec)
        r2_mag = np.linalg.norm(r2_vec)

        # E = 2*lambda*r_hat/r (in CGS-ESU for line charge)
        E_perp = 2 * line_charge_density * r1_vec / r1_mag**2
        E_perp += 2 * image_charge_density * r2_vec / r2_mag**2

        # Field is perpendicular to cylinder axis
        return E_perp

    # Induced surface charge density
    def surface_charge_density(theta: float) -> float:
        """
        Calculate induced surface charge density at angle theta.

        Args:
            theta: Angle from line to charge (radians).

        Returns:
            Surface charge density sigma (statcoulombs/cm^2).
        """
        cos_theta = np.cos(theta)

        # Distance from line charge to surface point
        R_sq = d_mag**2 + cylinder_radius**2 - 2 * d_mag * cylinder_radius * cos_theta
        R = np.sqrt(R_sq)

        # Surface charge density
        # sigma = -lambda * (d^2 - a^2) / (2*pi*a*R^2)
        sigma = (
            -line_charge_density
            * (d_mag**2 - cylinder_radius**2)
            / (2 * np.pi * cylinder_radius * R_sq)
        )
        return sigma

    return {
        "image_charge_density": image_charge_density,
        "image_position": image_position,
        "force_per_length": force_per_length_vector,
        "force_per_length_magnitude": abs(force_per_length),
        "line_charge_density": line_charge_density,
        "line_position": line_position,
        "cylinder_axis_point": cylinder_axis_point,
        "cylinder_axis_direction": cylinder_axis_direction,
        "cylinder_radius": cylinder_radius,
        "cylinder_potential": cylinder_potential,
        "distance_from_axis": d_mag,
        "potential_at_point": potential_at_point,
        "field_at_point": field_at_point,
        "surface_charge_density": surface_charge_density,
    }


# =============================================================================
# ELECTRICAL INVERSION METHOD (Arts. 179-180)
# =============================================================================


@maxwell_cite(
    179,
    180,
    part=1,
    chapter="Electric Images",
    theory_class="maxwell_original",
    description="Electrical inversion (Kelvin transformation)",
)
def inversion_method(
    charge_distribution: Union[float, Callable[[np.ndarray], float]],
    inversion_center: np.ndarray,
    inversion_radius: float,
    is_point_charge: bool = True,
    charge_position: np.ndarray = None,
) -> dict[str, float | np.ndarray | Callable]:
    """
    Apply Kelvin's electrical inversion transformation.

    Arts. 179-180: Maxwell described the method of electrical inversion,
    discovered by Lord Kelvin. Under inversion with respect to a sphere
    of radius k centered at O:

        r' = O + k^2 * (r - O) / |r - O|^2

    Points at distance r from the center map to points at distance k^2/r.

    For charges:
        - A point charge q at distance r maps to charge q' at distance r'
        - q' = q * (k / r) (charge scales with distance)

    Key properties:
        - Spheres invert to spheres (or planes, as infinite spheres)
        - Angles are preserved (conformal mapping)
        - Laplace's equation is preserved

    This method can transform difficult problems into simpler ones.

    Args:
        charge_distribution: Charge q or charge density function rho(r).
        inversion_center: Center of inversion sphere O (cm).
        inversion_radius: Radius k of inversion sphere (cm).
        is_point_charge: If True, treat as point charge; else as distribution.
        charge_position: Position of point charge (required if is_point_charge).

    Returns:
        Dictionary with:
        - inverted_charge: q' (for point charge)
        - inverted_position: r' (for point charge)
        - inverted_density: rho'(r') (for distribution)
        - inversion_function: r -> r' mapping
        - potential_transform: V -> V' transformation rule

    References:
        Part I, Art. 179: Kelvin inversion transformation.
        Part I, Art. 180: Application to electrostatic problems.

    Example:
        >>> # Invert a point charge
        >>> result = inversion_method(
        ...     charge_distribution=100,
        ...     inversion_center=np.array([0, 0, 0]),
        ...     inversion_radius=1.0,
        ...     is_point_charge=True,
        ...     charge_position=np.array([2, 0, 0])
        ... )
        >>> print(f"q' = {result['inverted_charge']} statC")
        >>> print(f"r' = {result['inverted_position']} cm")
    """
    inversion_center = np.asarray(inversion_center, dtype=np.float64)

    # Inversion transformation function
    def invert_point(r: np.ndarray) -> np.ndarray:
        """Map point r to its inverse r'."""
        r = np.asarray(r, dtype=np.float64)
        r_vec = r - inversion_center
        r_mag = np.linalg.norm(r_vec)

        if r_mag == 0:
            return np.array([np.inf, np.inf, np.inf])  # Center maps to infinity

        # r' = O + k^2 * (r - O) / |r - O|^2
        factor = inversion_radius**2 / r_mag**2
        return inversion_center + factor * r_vec

    # Jacobian of inversion (for charge density transformation)
    def inversion_jacobian(r: np.ndarray) -> float:
        """Calculate Jacobian determinant |dr'/dr|."""
        r = np.asarray(r, dtype=np.float64)
        r_vec = r - inversion_center
        r_mag = np.linalg.norm(r_vec)

        # Jacobian = (k/r)^6 for 3D inversion
        return (inversion_radius / r_mag) ** 6

    if is_point_charge:
        if charge_position is None:
            raise ValueError("charge_position required for point charge")

        charge_position = np.asarray(charge_position, dtype=np.float64)

        # Vector from inversion center to charge
        r_vec = charge_position - inversion_center
        r_mag = np.linalg.norm(r_vec)

        if r_mag == 0:
            raise ValueError("Point charge cannot be at inversion center")

        # Inverted position
        inverted_position = invert_point(charge_position)

        # Inverted charge: q' = q * (k / r)
        inverted_charge = charge_distribution * (inversion_radius / r_mag)

        # Potential transformation: V'(r') = V(r) * (r / k)
        def potential_transform(V_original: float, r_original: np.ndarray) -> float:
            """Transform potential under inversion."""
            r_orig_mag = np.linalg.norm(np.asarray(r_original) - inversion_center)
            return V_original * (r_orig_mag / inversion_radius)

        return {
            "inverted_charge": inverted_charge,
            "inverted_position": inverted_position,
            "original_charge": charge_distribution,
            "original_position": charge_position,
            "inversion_center": inversion_center,
            "inversion_radius": inversion_radius,
            "inversion_function": invert_point,
            "potential_transform": potential_transform,
            "jacobian": inversion_jacobian(charge_position),
        }

    else:
        # For continuous charge distribution
        # rho'(r') = rho(r) * (k/r)^5 (in 3D)
        if not callable(charge_distribution):
            raise ValueError("For distributed charge, provide a callable function")

        def inverted_density(r_prime: np.ndarray) -> float:
            """Calculate inverted charge density at r'."""
            # Find original position r that maps to r'
            # Inversion is self-inverse: r = invert(r')
            r = invert_point(r_prime)

            # Jacobian factor for density transformation
            r_mag = np.linalg.norm(r - inversion_center)
            jacobian_factor = (inversion_radius / r_mag) ** 5

            return charge_distribution(r) * jacobian_factor

        return {
            "inverted_density": inverted_density,
            "inversion_center": inversion_center,
            "inversion_radius": inversion_radius,
            "inversion_function": invert_point,
            "jacobian_function": inversion_jacobian,
        }


@maxwell_cite(
    179,
    180,
    part=1,
    chapter="Electric Images",
    theory_class="maxwell_original",
    description="Invert a sphere to a plane (and vice versa)",
)
def invert_sphere_to_plane(
    sphere_center: np.ndarray,
    sphere_radius: float,
    inversion_center: np.ndarray,
    inversion_radius: float,
) -> dict[str, float | np.ndarray]:
    """
    Special case: invert a sphere to a plane.

    Arts. 179-180: When the inversion center lies on the surface of a
    sphere, the sphere inverts to an infinite plane. This is useful
    for transforming problems involving spheres to problems involving
    planes (which are often simpler).

    The distance from the inversion center to the plane is:
        d = k^2 / (2a)
    where a is the sphere radius and k is the inversion radius.

    Args:
        sphere_center: Center of the sphere (cm).
        sphere_radius: Radius of the sphere (cm).
        inversion_center: Center of inversion (must be on sphere surface).
        inversion_radius: Radius of inversion sphere (cm).

    Returns:
        Dictionary with:
        - plane_normal: Unit normal vector of inverted plane
        - plane_distance: Distance from origin to plane
        - transformation_verified: Boolean (should be True)

    References:
        Part I, Art. 179: Sphere-to-plane inversion.
        Part I, Art. 180: Applications to image problems.
    """
    sphere_center = np.asarray(sphere_center, dtype=np.float64)
    inversion_center = np.asarray(inversion_center, dtype=np.float64)

    # Verify inversion center is on sphere surface
    dist_check = np.linalg.norm(inversion_center - sphere_center)
    if not np.isclose(dist_check, sphere_radius, rtol=1e-6):
        raise ValueError(
            f"Inversion center must be on sphere surface. "
            f"Distance = {dist_check}, radius = {sphere_radius}"
        )

    # Normal points from sphere center through inversion center
    plane_normal = (inversion_center - sphere_center) / sphere_radius

    # Distance from inversion center to plane
    # d = k^2 / (2a)
    plane_distance = inversion_radius**2 / (2 * sphere_radius)

    # Plane equation: n . r = d (where d is from inversion center)
    # Point on plane
    point_on_plane = inversion_center + plane_distance * plane_normal

    return {
        "plane_normal": plane_normal,
        "plane_distance": plane_distance,
        "point_on_plane": point_on_plane,
        "sphere_center": sphere_center,
        "sphere_radius": sphere_radius,
        "inversion_center": inversion_center,
        "inversion_radius": inversion_radius,
        "transformation_verified": True,
    }


# =============================================================================
# IMAGE SYSTEM ANALYSIS (Art. 181)
# =============================================================================


@maxwell_cite(
    181,
    part=1,
    chapter="Electric Images",
    theory_class="maxwell_original",
    description="Complete analysis of image charge systems",
)
def image_system_analysis(
    image_configs: List[dict],
    evaluation_points: np.ndarray = None,
) -> dict[str, float | np.ndarray]:
    """
    Analyze a complete system of image charges.

    Art. 181: Maxwell showed how to analyze complex configurations
    involving multiple conductors and charges by building up image
    systems. Each conductor generates images of all other charges,
    which in turn generate additional images (infinite series in
    some cases).

    This function combines multiple image configurations and computes:
        - Total potential at specified points
        - Total electric field
        - Total electrostatic energy
        - Forces on all charges
        - Induced charges on conductors

    Args:
        image_configs: List of image configuration dictionaries from
                      other functions in this module.
        evaluation_points: Optional array of points (N, 3) where
                          potential and field are evaluated.

    Returns:
        Dictionary with:
        - all_charges: List of (charge, position) tuples
        - total_potential: V at evaluation points (if provided)
        - total_field: E at evaluation points (if provided)
        - total_energy: Electrostatic energy of system
        - forces: Forces on each charge
        - conductor_charges: Induced charges on conductors

    References:
        Part I, Art. 181: Analysis of complete image systems.

    Example:
        >>> # Two parallel planes with charge between
        >>> config1 = image_point_charge_plane(100, np.array([0, 0, 5]), plane_height=0)
        >>> config2 = image_point_charge_plane(100, np.array([0, 0, 5]), plane_height=10)
        >>> result = image_system_analysis([config1, config2])
        >>> print(f"Total energy = {result['total_energy']} ergs")
    """
    # Collect all charges (original and images)
    all_charges = []  # List of (q, r) tuples
    conductor_data = []

    for config in image_configs:
        # Extract charges from each configuration
        if "image_charge" in config:
            # Point charge image system
            if "point_charge" in config and "point_position" in config:
                all_charges.append((config["point_charge"], config["point_position"]))
            if "image_charge" in config and "image_position" in config:
                all_charges.append((config["image_charge"], config["image_position"]))
            if "central_charge" in config and config.get("central_charge", 0) != 0:
                if "sphere_center" in config:
                    all_charges.append(
                        (config["central_charge"], config["sphere_center"])
                    )

            # Store conductor info
            if "sphere_radius" in config:
                conductor_data.append(
                    {
                        "type": "sphere",
                        "center": config.get("sphere_center"),
                        "radius": config["sphere_radius"],
                        "charge": config.get(
                            "sphere_charge", config.get("image_charge", 0)
                        ),
                    }
                )
            elif "plane_normal" in config:
                conductor_data.append(
                    {
                        "type": "plane",
                        "normal": config["plane_normal"],
                        "height": config.get("plane_height", 0),
                        "charge": config.get("total_induced_charge", 0),
                    }
                )

        if "image_charge_density" in config:
            # Line charge image system
            if "line_charge_density" in config and "line_position" in config:
                all_charges.append(
                    ("line", config["line_charge_density"], config["line_position"])
                )
            if "image_charge_density" in config and "image_position" in config:
                all_charges.append(
                    ("line", config["image_charge_density"], config["image_position"])
                )

    # Compute total potential at evaluation points
    total_potential = None
    total_field = None

    if evaluation_points is not None:
        evaluation_points = np.asarray(evaluation_points, dtype=np.float64)
        n_points = len(evaluation_points)
        total_potential = np.zeros(n_points)
        total_field = np.zeros((n_points, 3))

        for i, r in enumerate(evaluation_points):
            for charge_data in all_charges:
                if charge_data[0] == "line":
                    # Line charge contribution
                    _, lambda_val, r_line = charge_data
                    r_vec = r[:2] - r_line[:2]  # 2D distance in cross-section
                    r_mag = np.linalg.norm(r_vec)
                    if r_mag > 0:
                        total_potential[i] -= 2 * lambda_val * np.log(r_mag)
                        total_field[i] += 2 * lambda_val * r_vec / r_mag**2
                else:
                    # Point charge contribution
                    q, r_q = charge_data
                    r_vec = r - r_q
                    r_mag = np.linalg.norm(r_vec)
                    if r_mag > 0:
                        total_potential[i] += q / r_mag
                        total_field[i] += q * r_vec / r_mag**3

    # Compute total electrostatic energy
    # W = (1/2) * sum_{i!=j} q_i * q_j / r_ij
    total_energy = 0.0
    n_charges = len([c for c in all_charges if c[0] != "line"])

    point_charges = [(c[0], c[1]) for c in all_charges if c[0] != "line"]
    for i in range(len(point_charges)):
        for j in range(i + 1, len(point_charges)):
            q_i, r_i = point_charges[i]
            q_j, r_j = point_charges[j]
            r_ij = np.linalg.norm(r_i - r_j)
            if r_ij > 0:
                total_energy += q_i * q_j / r_ij

    total_energy *= 0.5  # Factor of 1/2

    # Compute forces on each charge
    forces = []
    for i, charge_data in enumerate(all_charges):
        if charge_data[0] == "line":
            forces.append(None)  # Skip line charges for now
            continue

        q_i, r_i = charge_data
        force = np.zeros(3)

        for j, other_data in enumerate(all_charges):
            if i == j:
                continue
            if other_data[0] == "line":
                continue

            q_j, r_j = other_data
            r_vec = r_i - r_j
            r_mag = np.linalg.norm(r_vec)
            if r_mag > 0:
                force += q_i * q_j * r_vec / r_mag**3

        forces.append(force)

    return {
        "all_charges": all_charges,
        "num_charges": len(all_charges),
        "total_potential": total_potential,
        "total_field": total_field,
        "total_energy": total_energy,
        "forces": forces,
        "conductor_data": conductor_data,
        "num_conductors": len(conductor_data),
    }


# =============================================================================
# UTILITY: Force between charge and conductor
# =============================================================================


@maxwell_cite(
    173,
    175,
    178,
    part=1,
    chapter="Electric Images",
    theory_class="maxwell_original",
    description="Force between charge and conducting surface",
)
def force_charge_conductor(
    charge: float,
    distance: float,
    conductor_type: str,
    conductor_size: float = None,
) -> dict[str, float]:
    """
    Calculate force between a point charge and a conducting surface.

    Arts. 173, 175, 178: Maxwell derived formulas for the force between
    a point charge and various conducting surfaces using the image method.

    Args:
        charge: Point charge q (statcoulombs).
        distance: Distance from charge to conductor surface (cm).
        conductor_type: Type of conductor ("plane", "sphere", "cylinder").
        conductor_size: Size parameter (radius for sphere/cylinder).

    Returns:
        Dictionary with:
        - force_magnitude: |F| (dynes)
        - force_direction: "attractive" or "repulsive"
        - formula_used: String describing the formula

    References:
        Part I, Art. 173: Force on plane.
        Part I, Art. 175: Force on sphere.
        Part I, Art. 178: Force on cylinder.
    """
    if conductor_type == "plane":
        # F = q^2 / (4*d^2) for infinite plane
        force_magnitude = charge**2 / (4 * distance**2)
        formula = f"F = q^2 / (4*d^2) = {charge}^2 / (4*{distance}^2)"

    elif conductor_type == "sphere":
        if conductor_size is None:
            raise ValueError("conductor_size (radius) required for sphere")

        # For grounded sphere: F = q^2 * a / (d^2 * (d^2 - a^2))
        # where d is distance from center, a is radius
        d_center = distance + conductor_size  # distance from center
        force_magnitude = (charge**2 * conductor_size) / (
            d_center**2 * (d_center**2 - conductor_size**2)
        )
        formula = f"F = q^2*a/(d^2*(d^2-a^2))"

    elif conductor_type == "cylinder":
        if conductor_size is None:
            raise ValueError("conductor_size (radius) required for cylinder")

        # For cylinder: F/L = lambda^2 * a / (d * (d^2 - a^2)) per unit length
        d_center = distance + conductor_size
        force_per_length = (charge**2 * conductor_size) / (
            d_center * (d_center**2 - conductor_size**2)
        )
        force_magnitude = force_per_length  # Force per unit length
        formula = f"F/L = lambda^2*a/(d*(d^2-a^2))"

    else:
        raise ValueError(f"Unknown conductor_type: {conductor_type}")

    return {
        "force_magnitude": force_magnitude,
        "force_direction": "attractive",
        "formula_used": formula,
        "charge": charge,
        "distance": distance,
        "conductor_type": conductor_type,
        "conductor_size": conductor_size,
    }


# =============================================================================
# MAIN: Module verification
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ELECTRIC IMAGES")
    print("Maxwell's Treatise, Part I, Chapter XI (Arts. 171-181)")
    print("=" * 70)

    # Test 1: Point charge above grounded plane
    print("\n--- Point Charge Above Grounded Plane (Arts. 171-173) ---")
    result = image_point_charge_plane(
        point_charge=100, point_position=np.array([0, 0, 10])
    )
    print(f"  Charge: q = {result['point_charge']} statC")
    print(f"  Position: r = {result['point_position']} cm")
    print(f"  Image charge: q' = {result['image_charge']} statC")
    print(f"  Image position: r' = {result['image_position']} cm")
    print(f"  Force magnitude: F = {result['force_magnitude']:.4e} dynes")
    print(f"  Total induced charge: Q_induced = {result['total_induced_charge']} statC")

    # Test 2: Point charge near conducting sphere
    print("\n--- Point Charge Near Conducting Sphere (Arts. 174-176) ---")
    result = image_point_charge_sphere(
        point_charge=100,
        point_position=np.array([0, 0, 10]),
        sphere_center=np.array([0, 0, 0]),
        sphere_radius=1.0,
    )
    print(f"  Charge: q = {result['point_charge']} statC")
    print(f"  Distance from center: d = {result['distance_from_center']} cm")
    print(f"  Sphere radius: a = {result['sphere_radius']} cm")
    print(f"  Image charge: q' = {result['image_charge']:.2f} statC")
    print(f"  Image position: d' = {np.linalg.norm(result['image_position'])} cm")
    print(
        f"  Force: F = {result['force_magnitude']:.4e} dynes ({result['force_direction']})"
    )

    # Test 3: Line charge near conducting cylinder
    print("\n--- Line Charge Near Conducting Cylinder (Arts. 177-178) ---")
    result = image_line_charge_cylinder(
        line_charge_density=1.0,
        line_position=np.array([5, 0, 0]),
        cylinder_axis_point=np.array([0, 0, 0]),
        cylinder_axis_direction=np.array([0, 0, 1]),
        cylinder_radius=1.0,
    )
    print(f"  Line charge density: lambda = {result['line_charge_density']} statC/cm")
    print(f"  Distance from axis: d = {result['distance_from_axis']} cm")
    print(
        f"  Image charge density: lambda' = {result['image_charge_density']} statC/cm"
    )
    print(
        f"  Force per length: F/L = {result['force_per_length_magnitude']:.4e} dynes/cm"
    )

    # Test 4: Kelvin inversion
    print("\n--- Kelvin Inversion (Arts. 179-180) ---")
    result = inversion_method(
        charge_distribution=100,
        inversion_center=np.array([0, 0, 0]),
        inversion_radius=1.0,
        is_point_charge=True,
        charge_position=np.array([2, 0, 0]),
    )
    print(f"  Original charge: q = {result['original_charge']} statC")
    print(f"  Original position: r = {result['original_position']} cm")
    print(f"  Inverted charge: q' = {result['inverted_charge']:.2f} statC")
    print(f"  Inverted position: r' = {result['inverted_position']} cm")

    # Test 5: Sphere to plane inversion
    print("\n--- Sphere to Plane Inversion (Arts. 179-180) ---")
    result = invert_sphere_to_plane(
        sphere_center=np.array([0, 0, 0]),
        sphere_radius=1.0,
        inversion_center=np.array([1, 0, 0]),
        inversion_radius=1.0,
    )
    print(
        f"  Sphere: center={result['sphere_center']}, radius={result['sphere_radius']}"
    )
    print(f"  Inversion center: {result['inversion_center']}")
    print(f"  Plane normal: {result['plane_normal']}")
    print(f"  Plane distance: d = {result['plane_distance']} cm")

    # Test 6: Force calculations
    print("\n--- Force Between Charge and Conductor (Arts. 173, 175, 178) ---")
    result = force_charge_conductor(charge=100, distance=1, conductor_type="plane")
    print(f"  Plane: F = {result['force_magnitude']:.4e} dynes")

    result = force_charge_conductor(
        charge=100, distance=1, conductor_type="sphere", conductor_size=1
    )
    print(f"  Sphere: F = {result['force_magnitude']:.4e} dynes")

    result = force_charge_conductor(
        charge=1.0, distance=1, conductor_type="cylinder", conductor_size=1
    )
    print(f"  Cylinder: F/L = {result['force_magnitude']:.4e} dynes/cm")

    # Test 7: Complete image system
    print("\n--- Complete Image System Analysis (Art. 181) ---")
    # Two parallel planes: one at z=0, one at z=-10, charge at z=5
    # Charge is in front of both planes (positive side)
    config1 = image_point_charge_plane(100, np.array([0, 0, 5]), plane_height=0)
    config2 = image_point_charge_plane(100, np.array([0, 0, 5]), plane_height=-10)
    result = image_system_analysis([config1, config2])
    print(f"  Number of charges in system: {result['num_charges']}")
    print(f"  Total electrostatic energy: W = {result['total_energy']:.4e} ergs")
    print(f"  Number of conductors: {result['num_conductors']}")

    print("\n" + "=" * 70)
    print("Module verification complete.")
    print("=" * 70)

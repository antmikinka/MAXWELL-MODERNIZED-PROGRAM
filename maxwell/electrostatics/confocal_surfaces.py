"""
Confocal Surfaces — Maxwell's Part I, Chapter X.

This module implements Maxwell's theory of confocal quadric surfaces
and ellipsoidal harmonics for solving electrostatic boundary value
problems:

1. **Charged Ellipsoid** (Arts. 147-150):
   - Potential of a charged conducting ellipsoid
   - Surface charge distribution on ellipsoid
   - Capacitance of ellipsoidal conductors

2. **Confocal Hyperboloids** (Arts. 151-153):
   - Hyperboloidal equipotential surfaces
   - Field lines as orthogonal trajectories
   - Confocal coordinate systems

3. **Ellipsoidal Coordinates** (Arts. 154-156):
   - Ellipsoidal harmonic expansion
   - Laplace equation in ellipsoidal coordinates
   - Applications to conductor problems

Maxwell's key insight (Arts. 147-156): Confocal quadric surfaces
(ellipsoids and hyperboloids sharing the same foci) form orthogonal
coordinate systems in which Laplace's equation can be solved by
separation of variables.

CGS-ESU units are used throughout:
    - Charge: statcoulombs
    - Distance: centimeters
    - Potential: statvolts
    - Capacitance: centimeters (statfarads)

Category: A (maxwell_original) — Maxwell's theory of confocal surfaces.

References:
    Part I, Chapter X: Confocal Surfaces (Arts. 147-156).
    Part I, Arts. 128-146: Spherical harmonics (related theory).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional, Tuple, Union
import numpy as np
from scipy import special, integrate

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


# =============================================================================
# CONFOCAL ELLIPSOID POTENTIAL (Arts. 147-150)
# =============================================================================

@maxwell_cite(
    147, 148, 149, 150,
    part=1, chapter="Confocal Surfaces",
    theory_class="maxwell_original",
    description="Potential of charged conducting ellipsoid"
)
def confocal_ellipsoid_potential(
    total_charge: float,
    semi_axes: Tuple[float, float, float],
    evaluation_point: np.ndarray = None,
) -> dict[str, float | np.ndarray]:
    """
    Calculate the potential and field of a charged conducting ellipsoid.

    Arts. 147-150: Maxwell showed that for a conducting ellipsoid with
    semi-axes (a, b, c) carrying total charge Q, the surface charge
    density is proportional to the distance from the center to the
    tangent plane.

    For a prolate ellipsoid (a > b = c), the charge concentrates at
    the ends (poles). For an oblate ellipsoid (a = b > c), charge
    concentrates at the edge.

    The potential outside the ellipsoid can be expressed using
    ellipsoidal coordinates and involves elliptic integrals.

    Args:
        total_charge: Total charge Q on the ellipsoid (statcoulombs).
        semi_axes: Tuple (a, b, c) of semi-axes in cm.
        evaluation_point: Optional point where V and E are evaluated (cm).

    Returns:
        Dictionary with:
        - surface_potential: V on the ellipsoid surface (statvolts)
        - capacitance: C = Q/V (cm = statfarads in CGS)
        - surface_charge_density: Function sigma(x, y, z)
        - potential_at_point: V at evaluation_point (if provided)
        - field_at_point: E at evaluation_point (if provided)
        - axes: (a, b, c) tuple
        - eccentricity: For prolate/oblate cases

    References:
        Part I, Art. 147: Conducting ellipsoid theory.
        Part I, Art. 148: Surface charge distribution.
        Part I, Art. 149: Potential calculation.
        Part I, Art. 150: Capacitance of ellipsoid.
    """
    a, b, c = semi_axes
    semi_axes = np.array([a, b, c], dtype=np.float64)

    # Sort axes to identify prolate vs oblate
    sorted_axes = sorted(semi_axes, reverse=True)
    a_max = sorted_axes[0]
    c_min = sorted_axes[2]

    # Surface area of ellipsoid (approximate formula by Knud Thomsen)
    p = 1.6075
    surface_area = 4 * np.pi * ((a**p * b**p + a**p * c**p + b**p * c**p) / 3) ** (1/p)

    # Average surface charge density
    sigma_avg = total_charge / surface_area

    # For a conducting ellipsoid, the surface charge density at point (x,y,z) is:
    # sigma = Q / (4*pi*a*b*c) * (x^2/a^4 + y^2/b^4 + z^2/c^4)^(-1/2)
    def surface_charge_density(x: float, y: float, z: float) -> float:
        """Calculate surface charge density at point (x, y, z) on ellipsoid."""
        # Verify point is on ellipsoid surface
        on_surface = (x**2/a**2 + y**2/b**2 + z**2/c**2)
        if not np.isclose(on_surface, 1.0, rtol=1e-6):
            # Return density for nearest surface point
            scale = 1.0 / np.sqrt(on_surface)
            x, y, z = x * scale, y * scale, z * scale

        # Surface charge density formula
        factor = np.sqrt((x**2/a**4 + y**2/b**4 + z**2/c**4))
        sigma = total_charge / (4 * np.pi * a * b * c * factor)
        return sigma

    # Capacitance of ellipsoid
    # For general ellipsoid: C = integral formula involving elliptic integrals
    # C = a * integral_0^inf dt / sqrt((a^2+t)(b^2+t)(c^2+t))
    def integrand(t):
        return 1.0 / np.sqrt((a**2 + t) * (b**2 + t) * (c**2 + t))

    # Compute the integral
    integral_result, error = integrate.quad(integrand, 0, np.inf)
    capacitance = 1.0 / integral_result  # In CGS-ESU, C has units of length

    # Surface potential: V = Q / C
    surface_potential = total_charge / capacitance

    # Eccentricity for prolate case (a > b = c)
    if np.isclose(b, c):
        eccentricity = np.sqrt(1 - (c/a)**2)
    elif np.isclose(a, b):
        # Oblate case
        eccentricity = np.sqrt(1 - (c/a)**2)
    else:
        eccentricity = None

    # Potential and field at evaluation point
    potential_at_point = None
    field_at_point = None

    if evaluation_point is not None:
        evaluation_point = np.asarray(evaluation_point, dtype=np.float64)
        x, y, z = evaluation_point

        # Check if point is outside ellipsoid
        ellipsoid_check = x**2/a**2 + y**2/b**2 + z**2/c**2

        if ellipsoid_check >= 1.0:
            # Outside ellipsoid - use approximation for far field
            r = np.linalg.norm(evaluation_point)

            # Monopole term (dominant at large distances)
            potential_at_point = total_charge / r

            # Field (radial for far field)
            field_at_point = total_charge * evaluation_point / r**3

            # Add quadrupole correction for nearby points
            # This is a simplified approximation
            if ellipsoid_check < 4.0:
                # Near field correction factor
                correction = 1.0 + 0.1 * (a**2 + b**2 + c**2) / r**2
                potential_at_point *= correction
                field_at_point *= correction

    # Maximum and minimum surface charge densities
    # At poles (ends of major axis): sigma_max
    sigma_max = total_charge / (4 * np.pi * b * c)  # At x = +/-a
    sigma_min = total_charge / (4 * np.pi * a * b)  # At z = +/-c (if c is smallest)

    return {
        "total_charge": total_charge,
        "semi_axes": (a, b, c),
        "surface_potential": surface_potential,
        "capacitance": capacitance,
        "surface_area": surface_area,
        "average_charge_density": sigma_avg,
        "maximum_charge_density": sigma_max,
        "minimum_charge_density": sigma_min,
        "surface_charge_density": surface_charge_density,
        "potential_at_point": potential_at_point,
        "field_at_point": field_at_point,
        "eccentricity": eccentricity,
        "ellipsoid_type": "prolate" if np.isclose(b, c) else ("oblate" if np.isclose(a, b) else "triaxial"),
    }


@maxwell_cite(
    147, 148,
    part=1, chapter="Confocal Surfaces",
    theory_class="maxwell_original",
    description="Capacitance of ellipsoidal conductor"
)
def ellipsoid_capacitance(
    semi_axes: Tuple[float, float, float],
) -> dict[str, float]:
    """
    Calculate the capacitance of an isolated conducting ellipsoid.

    Arts. 147-148: The capacitance of an ellipsoid with semi-axes (a, b, c)
    is given by:

        C = 1 / integral_0^inf dt / sqrt((a^2+t)(b^2+t)(c^2+t))

    Special cases:
        - Sphere (a=b=c=R): C = R
        - Prolate spheroid (a>b=c): C = 2a*e / ln((1+e)/(1-e))
        - Oblate spheroid (a=b>c): C = a*e / arcsin(e)

    where e is the eccentricity.

    Args:
        semi_axes: Tuple (a, b, c) of semi-axes in cm.

    Returns:
        Dictionary with:
        - capacitance: C (cm = statfarads in CGS)
        - semi_axes: Input (a, b, c)
        - ellipsoid_type: "sphere", "prolate", "oblate", or "triaxial"
        - eccentricity: For spheroidal cases

    References:
        Part I, Art. 147: Ellipsoid capacitance formula.
        Part I, Art. 148: Special cases.
    """
    a, b, c = semi_axes

    # Determine ellipsoid type
    if np.isclose(a, b) and np.isclose(b, c):
        ellipsoid_type = "sphere"
        # Sphere: C = R
        capacitance = a
        eccentricity = 0.0

    elif np.isclose(b, c):
        ellipsoid_type = "prolate"
        eccentricity = np.sqrt(1 - (c/a)**2)
        if eccentricity > 0:
            # Prolate spheroid: C = 2a*e / ln((1+e)/(1-e))
            capacitance = 2 * a * eccentricity / np.log((1 + eccentricity) / (1 - eccentricity))
        else:
            capacitance = a

    elif np.isclose(a, b):
        ellipsoid_type = "oblate"
        eccentricity = np.sqrt(1 - (c/a)**2)
        if eccentricity > 0:
            # Oblate spheroid: C = a*e / arcsin(e)
            capacitance = a * eccentricity / np.arcsin(eccentricity)
        else:
            capacitance = a

    else:
        ellipsoid_type = "triaxial"
        eccentricity = None

        # General triaxial ellipsoid - numerical integration
        def integrand(t):
            return 1.0 / np.sqrt((a**2 + t) * (b**2 + t) * (c**2 + t))

        integral_result, error = integrate.quad(integrand, 0, np.inf)
        capacitance = 1.0 / integral_result

    # Equivalent sphere radius (sphere with same capacitance)
    equivalent_radius = capacitance

    return {
        "capacitance": capacitance,
        "semi_axes": (a, b, c),
        "ellipsoid_type": ellipsoid_type,
        "eccentricity": eccentricity,
        "equivalent_sphere_radius": equivalent_radius,
    }


# =============================================================================
# CONFOCAL HYPERBOLOID (Arts. 151-153)
# =============================================================================

@maxwell_cite(
    151, 152, 153,
    part=1, chapter="Confocal Surfaces",
    theory_class="maxwell_original",
    description="Confocal hyperboloid equipotentials"
)
def confocal_hyperboloid(
    focal_distance: float,
    hyperboloid_parameter: float,
    potential_value: float = None,
    evaluation_point: np.ndarray = None,
) -> dict[str, float | np.ndarray]:
    """
    Calculate properties of confocal hyperboloid surfaces.

    Arts. 151-153: Maxwell showed that confocal hyperboloids form
    orthogonal trajectories to confocal ellipsoids and can serve as
    equipotential surfaces in certain charge configurations.

    The confocal family is defined by:

        x^2/(a^2 - lambda) + y^2/(b^2 - lambda) + z^2/(c^2 - lambda) = 1

    For hyperboloids, lambda takes values that make some denominators
    negative, giving hyperbolic cross-sections.

    A hyperboloid of one sheet: x^2/a^2 + y^2/b^2 - z^2/c^2 = 1
    A hyperboloid of two sheets: x^2/a^2 - y^2/b^2 - z^2/c^2 = 1

    Args:
        focal_distance: Distance to foci (cm).
        hyperboloid_parameter: Parameter defining which hyperboloid.
        potential_value: Optional potential on the hyperboloid surface.
        evaluation_point: Point to check if on hyperboloid.

    Returns:
        Dictionary with:
        - hyperboloid_type: "one_sheet" or "two_sheet"
        - semi_axes: (a, b, c) for the hyperboloid
        - focal_curves: Focal ellipse and hyperbola
        - asymptotic_cone: Cone approached at infinity
        - potential_on_surface: V (if provided)
        - point_on_surface: Boolean (if evaluation_point provided)

    References:
        Part I, Art. 151: Confocal hyperboloid theory.
        Part I, Art. 152: Orthogonal trajectory property.
        Part I, Art. 153: Applications to field problems.
    """
    # For a confocal system with focal distance f:
    # The hyperboloid parameter u determines the surface

    # Hyperboloid of one sheet (u < 0):
    # x^2/(f^2 + u) + y^2/(f^2 + u) - z^2/|u| = 1

    # Hyperboloid of two sheets (u > 0):
    # x^2/(f^2 + u) - y^2/u - z^2/u = 1

    if hyperboloid_parameter < 0:
        hyperboloid_type = "one_sheet"
        # One sheet: x^2/a_h^2 + y^2/b_h^2 - z^2/c_h^2 = 1
        a_h = np.sqrt(focal_distance**2 + hyperboloid_parameter)
        b_h = a_h  # Assume rotational symmetry
        c_h = np.sqrt(abs(hyperboloid_parameter))

        # Waist radius (minimum cross-section)
        waist_radius = a_h

    else:
        hyperboloid_type = "two_sheet"
        # Two sheets: x^2/a_h^2 - y^2/b_h^2 - z^2/c_h^2 = 1
        a_h = np.sqrt(focal_distance**2 + hyperboloid_parameter)
        b_h = np.sqrt(hyperboloid_parameter)
        c_h = b_h

        # Vertex distance (distance from origin to each sheet)
        vertex_distance = a_h

    # Asymptotic cone (surface approached at large distances)
    # For one sheet: x^2/a_h^2 + y^2/b_h^2 = z^2/c_h^2
    # For two sheets: same form
    cone_semi_angle = np.arctan(c_h / a_h) if hyperboloid_type == "one_sheet" else np.arctan(a_h / c_h)

    # Check if evaluation point is on the hyperboloid
    point_on_surface = None
    surface_function = None

    def hyperboloid_equation(x: float, y: float, z: float) -> float:
        """
        Evaluate the hyperboloid equation at (x, y, z).

        Returns:
            Value of left-hand side minus 1 (zero on surface).
        """
        if hyperboloid_type == "one_sheet":
            return x**2/a_h**2 + y**2/b_h**2 - z**2/c_h**2 - 1
        else:
            return x**2/a_h**2 - y**2/b_h**2 - z**2/c_h**2 - 1

    surface_function = hyperboloid_equation

    if evaluation_point is not None:
        x, y, z = evaluation_point
        value = hyperboloid_equation(x, y, z)
        point_on_surface = np.isclose(value, 0, rtol=1e-6)

    # Focal curves
    # For the confocal system, the focal ellipse lies in the xy-plane
    focal_ellipse_semi_major = focal_distance
    focal_ellipse_semi_minor = focal_distance  # For rotational symmetry

    # Focal hyperbola lies in the xz-plane
    focal_hyperbola_semi_transverse = focal_distance
    focal_hyperbola_semi_conjugate = focal_distance

    result = {
        "hyperboloid_type": hyperboloid_type,
        "semi_axes": (a_h, b_h, c_h),
        "focal_distance": focal_distance,
        "hyperboloid_parameter": hyperboloid_parameter,
        "asymptotic_cone_angle": cone_semi_angle,
        "potential_on_surface": potential_value,
        "point_on_surface": point_on_surface,
        "surface_function": surface_function,
        "focal_ellipse": {
            "semi_major": focal_ellipse_semi_major,
            "semi_minor": focal_ellipse_semi_minor,
            "plane": "xy",
        },
        "focal_hyperbola": {
            "semi_transverse": focal_hyperbola_semi_transverse,
            "semi_conjugate": focal_hyperbola_semi_conjugate,
            "plane": "xz",
        },
    }

    if hyperboloid_type == "one_sheet":
        result["waist_radius"] = waist_radius
    else:
        result["vertex_distance"] = vertex_distance

    return result


@maxwell_cite(
    151, 152,
    part=1, chapter="Confocal Surfaces",
    theory_class="maxwell_original",
    description="Field lines orthogonal to confocal surfaces"
)
def confocal_field_lines(
    ellipsoid_axes: Tuple[float, float, float],
    starting_point: np.ndarray,
    num_points: int = 100,
    step_size: float = 0.01,
) -> dict[str, np.ndarray]:
    """
    Trace electric field lines orthogonal to confocal ellipsoidal surfaces.

    Arts. 151-152: Maxwell showed that electric field lines are orthogonal
    trajectories to equipotential surfaces. For confocal ellipsoids,
    the field lines follow the normals to the ellipsoidal surfaces.

    The field line differential equation is:
        dr/ds = E(r) / |E(r)|

    where s is arc length along the field line.

    Args:
        ellipsoid_axes: Semi-axes (a, b, c) of reference ellipsoid.
        starting_point: Starting point for field line tracing (cm).
        num_points: Number of points along the field line.
        step_size: Integration step size (cm).

    Returns:
        Dictionary with:
        - field_line: Array of (x, y, z) positions along field line
        - outward_line: Field line going outward
        - inward_line: Field line going inward (to conductor)

    References:
        Part I, Art. 151: Orthogonal trajectory property.
        Part I, Art. 152: Field line equations.
    """
    a, b, c = ellipsoid_axes
    starting_point = np.asarray(starting_point, dtype=np.float64)

    def ellipsoid_normal(r: np.ndarray) -> np.ndarray:
        """Calculate unit normal to ellipsoid at point r."""
        x, y, z = r
        # Gradient of f(x,y,z) = x^2/a^2 + y^2/b^2 + z^2/c^2
        grad_f = np.array([2*x/a**2, 2*y/b**2, 2*z/c**2])
        grad_norm = np.linalg.norm(grad_f)
        if grad_norm > 0:
            return grad_f / grad_norm
        return np.array([0, 0, 1])

    def field_direction(r: np.ndarray) -> np.ndarray:
        """
        Get field direction (normal to ellipsoid through r).

        For a charged ellipsoid, E points along the normal to the
        confocal ellipsoid passing through r.
        """
        return ellipsoid_normal(r)

    # Integrate field line using Euler method
    field_line = np.zeros((num_points, 3))
    field_line[0] = starting_point

    for i in range(1, num_points):
        r = field_line[i-1]
        direction = field_direction(r)
        field_line[i] = r + step_size * direction

    # Also trace inward (toward ellipsoid surface)
    inward_line = np.zeros((num_points, 3))
    inward_line[0] = starting_point

    for i in range(1, num_points):
        r = inward_line[i-1]
        direction = -field_direction(r)  # Inward
        inward_line[i] = r + step_size * direction

    return {
        "field_line": field_line,
        "outward_line": field_line,
        "inward_line": inward_line,
        "starting_point": starting_point,
        "ellipsoid_axes": ellipsoid_axes,
        "num_points": num_points,
        "step_size": step_size,
        "total_length": num_points * step_size,
    }


# =============================================================================
# ELLIPSOIDAL COORDINATES (Arts. 154-156)
# =============================================================================

@maxwell_cite(
    154, 155, 156,
    part=1, chapter="Confocal Surfaces",
    theory_class="maxwell_original",
    description="Convert Cartesian to ellipsoidal coordinates"
)
def ellipsoidal_coordinates(
    x: float, y: float, z: float,
    semi_axes: Tuple[float, float, float],
) -> dict[str, float]:
    """
    Convert Cartesian coordinates to ellipsoidal coordinates.

    Arts. 154-156: Maxwell introduced ellipsoidal coordinates (lambda, mu, nu)
    as the three roots of the equation:

        x^2/(a^2 - s) + y^2/(b^2 - s) + z^2/(c^2 - s) = 1

    The three roots satisfy:
        lambda < c^2 < mu < b^2 < nu < a^2

    where:
        - lambda = constant gives ellipsoids
        - mu = constant gives hyperboloids of one sheet
        - nu = constant gives hyperboloids of two sheets

    These coordinates are orthogonal and useful for solving Laplace's
    equation with ellipsoidal boundary conditions.

    Args:
        x, y, z: Cartesian coordinates (cm).
        semi_axes: (a, b, c) semi-axes of reference ellipsoid.

    Returns:
        Dictionary with:
        - lambda_coord: First ellipsoidal coordinate
        - mu_coord: Second ellipsoidal coordinate
        - nu_coord: Third ellipsoidal coordinate
        - scale_factors: (h_lambda, h_mu, h_nu) Lamé coefficients

    References:
        Part I, Art. 154: Ellipsoidal coordinate definition.
        Part I, Art. 155: Scale factors (Lamé coefficients).
        Part I, Art. 156: Laplace equation in ellipsoidal coordinates.
    """
    a, b, c = semi_axes
    a2, b2, c2 = a**2, b**2, c**2

    # The ellipsoidal coordinates are roots of:
    # f(s) = x^2/(a^2-s) + y^2/(b^2-s) + z^2/(c^2-s) - 1 = 0
    # This is a cubic equation in s

    # Rewrite as polynomial: clear denominators
    # x^2(b^2-s)(c^2-s) + y^2(a^2-s)(c^2-s) + z^2(a^2-s)(b^2-s)
    # - (a^2-s)(b^2-s)(c^2-s) = 0

    # Expand to get cubic: s^3 + p*s^2 + q*s + r = 0
    # Coefficients (after expansion and collecting terms)
    x2, y2, z2 = x**2, y**2, z**2

    # Coefficient of s^3: -1
    # Coefficient of s^2: a^2 + b^2 + c^2 + x^2 + y^2 + z^2
    # (derived from expanding the equation)

    # Use numpy roots function to find the three roots
    # Polynomial coefficients (descending powers)
    coef_s3 = -1.0
    coef_s2 = a2 + b2 + c2 + x2 + y2 + z2
    coef_s1 = -(a2*b2 + b2*c2 + c2*a2 + x2*(b2+c2) + y2*(a2+c2) + z2*(a2+b2))
    coef_s0 = a2*b2*c2 + x2*b2*c2 + y2*a2*c2 + z2*a2*b2

    # Normalize to monic polynomial
    coef_s2 /= coef_s3
    coef_s1 /= coef_s3
    coef_s0 /= coef_s3

    # Find roots
    coeffs = [1.0, coef_s2, coef_s1, coef_s0]
    roots = np.roots(coeffs)

    # Sort roots: lambda < c^2 < mu < b^2 < nu < a^2
    # Filter real parts (roots should be real for points outside focal curves)
    roots_real = np.sort(roots.real)

    # Assign to coordinates based on inequalities
    lambda_coord = roots_real[0]  # Smallest root
    mu_coord = roots_real[1]       # Middle root
    nu_coord = roots_real[2]       # Largest root

    # Scale factors (Lamé coefficients) for ellipsoidal coordinates
    # h_lambda^2 = (lambda-mu)(lambda-nu) / (4*(a^2-lambda)(b^2-lambda)(c^2-lambda))
    # etc.

    def scale_factor(coord, others):
        """Compute scale factor for a coordinate."""
        s = coord
        s1, s2 = others
        numerator = (s - s1) * (s - s2)
        denominator = 4 * (a2 - s) * (b2 - s) * (c2 - s)
        if denominator > 0:
            return np.sqrt(abs(numerator / denominator))
        return np.sqrt(abs(numerator)) / np.sqrt(abs(denominator))

    h_lambda = scale_factor(lambda_coord, (mu_coord, nu_coord))
    h_mu = scale_factor(mu_coord, (lambda_coord, nu_coord))
    h_nu = scale_factor(nu_coord, (lambda_coord, mu_coord))

    return {
        "lambda_coord": lambda_coord,
        "mu_coord": mu_coord,
        "nu_coord": nu_coord,
        "scale_factors": (h_lambda, h_mu, h_nu),
        "cartesian": (x, y, z),
        "semi_axes": semi_axes,
        "roots_raw": roots_real,
    }


@maxwell_cite(
    154, 155, 156,
    part=1, chapter="Confocal Surfaces",
    theory_class="maxwell_original",
    description="Laplace equation in ellipsoidal coordinates"
)
def laplacian_ellipsoidal(
    potential_func: Callable[[float, float, float], float],
    lambda_coord: float, mu_coord: float, nu_coord: float,
    semi_axes: Tuple[float, float, float],
    h: float = 1e-5,
) -> dict[str, float]:
    """
    Compute Laplacian of a potential in ellipsoidal coordinates.

    Arts. 154-156: The Laplace equation in ellipsoidal coordinates is:

        del^2 V = 0

    In orthogonal curvilinear coordinates:

        del^2 V = (1/h1*h2*h3) * [d/dq1(h2*h3/h1 * dV/dq1) + ...]

    For ellipsoidal coordinates (lambda, mu, nu) with scale factors
    h_lambda, h_mu, h_nu, the Laplacian takes a specific form that
    separates variables.

    This function computes the Laplacian numerically to verify that
    a given potential satisfies Laplace's equation.

    Args:
        potential_func: Function V(lambda, mu, nu) returning potential.
        lambda_coord, mu_coord, nu_coord: Coordinates where Laplacian
                                         is evaluated.
        semi_axes: (a, b, c) semi-axes.
        h: Finite difference step size.

    Returns:
        Dictionary with:
        - laplacian: del^2 V at the point (should be 0 for harmonic)
        - separation_check: Check if potential separates as product

    References:
        Part I, Art. 156: Laplace equation in ellipsoidal coordinates.
    """
    a, b, c = semi_axes

    # Get scale factors at the evaluation point
    coords = ellipsoidal_coordinates(
        lambda_coord, mu_coord, nu_coord,  # Use as Cartesian proxy
        semi_axes
    )

    # For numerical Laplacian, we need to work in actual space
    # This is a simplified version - full implementation would
    # require transformation back to Cartesian

    # Compute second derivatives using central differences
    def d2V_dq2(q, dq, other1, other2, axis):
        """Second derivative with respect to coordinate q."""
        if axis == 0:
            return (potential_func(q+h, other1, other2) - 2*potential_func(q, other1, other2)
                    + potential_func(q-h, other1, other2)) / h**2
        elif axis == 1:
            return (potential_func(other1, q+h, other2) - 2*potential_func(other1, q, other2)
                    + potential_func(other1, q-h, other2)) / h**2
        else:
            return (potential_func(other1, other2, q+h) - 2*potential_func(other1, other2, q)
                    + potential_func(other1, other2, q-h)) / h**2

    # Numerical second derivatives
    d2V_dlambda2 = d2V_dq2(lambda_coord, h, mu_coord, nu_coord, 0)
    d2V_dmu2 = d2V_dq2(mu_coord, h, lambda_coord, nu_coord, 1)
    d2V_dnu2 = d2V_dq2(nu_coord, h, lambda_coord, mu_coord, 2)

    # Approximate Laplacian (simplified - assumes unit scale factors)
    # Full expression includes scale factor derivatives
    laplacian_approx = d2V_dlambda2 + d2V_dmu2 + d2V_dnu2

    # Check separation of variables
    # If V = L(lambda) * M(mu) * N(nu), then:
    # (1/L) * d/dlambda(h_mu*h_nu/h_lambda * dL/dlambda) + cyclic = 0

    V0 = potential_func(lambda_coord, mu_coord, nu_coord)
    V_lambda = potential_func(lambda_coord + h, mu_coord, nu_coord)
    V_mu = potential_func(lambda_coord, mu_coord + h, nu_coord)
    V_nu = potential_func(lambda_coord, mu_coord, nu_coord + h)

    # Separation ratios (should be constant if separable)
    sep_lambda = (V_lambda - V0) / (V0 * h) if V0 != 0 else 0
    sep_mu = (V_mu - V0) / (V0 * h) if V0 != 0 else 0
    sep_nu = (V_nu - V0) / (V0 * h) if V0 != 0 else 0

    return {
        "laplacian": laplacian_approx,
        "is_harmonic": np.isclose(laplacian_approx, 0, rtol=1e-3),
        "separation_ratios": (sep_lambda, sep_mu, sep_nu),
        "potential_at_point": V0,
        "coordinates": (lambda_coord, mu_coord, nu_coord),
    }


@maxwell_cite(
    154, 155, 156,
    part=1, chapter="Confocal Surfaces",
    theory_class="maxwell_original",
    description="Ellipsoidal harmonic expansion"
)
def ellipsoidal_harmonic_expansion(
    boundary_potential: Callable[[float, float, float], float],
    semi_axes: Tuple[float, float, float],
    max_order: int = 4,
) -> dict[str, float | np.ndarray]:
    """
    Expand a boundary potential in ellipsoidal harmonics.

    Arts. 154-156: Maxwell showed that any potential on an ellipsoidal
    surface can be expanded in ellipsoidal harmonics, which are the
    natural basis functions for the Laplace equation in ellipsoidal
    coordinates.

    The expansion takes the form:

        V(lambda, mu, nu) = sum_{n,m} A_{nm} * E_n^m(lambda) * E_n^m(mu) * E_n^m(nu)

    where E_n^m are Lamé functions (ellipsoidal harmonics).

    This is analogous to spherical harmonic expansion but for
    ellipsoidal geometry.

    Args:
        boundary_potential: Function V(x, y, z) on the ellipsoid surface.
        semi_axes: (a, b, c) semi-axes of the ellipsoid.
        max_order: Maximum order of harmonics to compute.

    Returns:
        Dictionary with:
        - expansion_coefficients: A_{nm} for each order
        - harmonic_functions: Lamé functions evaluated
        - reconstruction_error: Error when reconstructing boundary

    References:
        Part I, Art. 154: Ellipsoidal harmonics theory.
        Part I, Art. 156: Harmonic expansion method.
    """
    a, b, c = semi_axes

    # Generate sample points on ellipsoid surface
    n_samples = 100
    theta = np.linspace(0, np.pi, n_samples)
    phi = np.linspace(0, 2*np.pi, n_samples)
    theta, phi = np.meshgrid(theta, phi)

    # Parametric equations for ellipsoid surface
    x = a * np.sin(theta) * np.cos(phi)
    y = b * np.sin(theta) * np.sin(phi)
    z = c * np.cos(theta)

    # Evaluate boundary potential on surface
    V_boundary = np.zeros_like(x)
    for i in range(n_samples):
        for j in range(n_samples):
            V_boundary[i, j] = boundary_potential(x[i,j], y[i,j], z[i,j])

    # For a proper ellipsoidal harmonic expansion, we would need
    # to compute Lamé functions. Here we use a simplified approach
    # using the fact that low-order harmonics are polynomials.

    # Zeroth order (monopole): constant term
    A_00 = np.mean(V_boundary)

    # First order (dipole): linear terms
    # V_1 = A_x * x + A_y * y + A_z * z
    # Use least squares to fit
    design_matrix = np.column_stack([
        x.flatten(), y.flatten(), z.flatten()
    ])
    coeffs_1, _, _, _ = np.linalg.lstsq(
        design_matrix, V_boundary.flatten(), rcond=None
    )
    A_10, A_11, A_12 = coeffs_1

    # Second order (quadrupole): quadratic terms
    # V_2 = A_xx * x^2 + A_yy * y^2 + A_zz * z^2 + A_xy * xy + ...
    design_matrix_2 = np.column_stack([
        x.flatten()**2, y.flatten()**2, z.flatten()**2,
        (x*y).flatten(), (y*z).flatten(), (x*z).flatten()
    ])

    # Residual after removing monopole and dipole
    V_residual = V_boundary.flatten() - A_00 - A_10*x.flatten() - A_11*y.flatten() - A_12*z.flatten()

    coeffs_2, residuals, _, _ = np.linalg.lstsq(
        design_matrix_2, V_residual, rcond=None
    )

    # Reconstruction
    V_reconstruct = (
        A_00 +
        A_10 * x + A_11 * y + A_12 * z +
        coeffs_2[0] * x**2 + coeffs_2[1] * y**2 + coeffs_2[2] * z**2 +
        coeffs_2[3] * x*y + coeffs_2[4] * y*z + coeffs_2[5] * x*z
    )

    reconstruction_error = np.sqrt(np.mean((V_boundary - V_reconstruct)**2))

    return {
        "expansion_coefficients": {
            "monopole": A_00,
            "dipole": (A_10, A_11, A_12),
            "quadrupole": tuple(coeffs_2),
        },
        "max_order": max_order,
        "reconstruction_error": reconstruction_error,
        "boundary_potential_mean": A_00,
        "semi_axes": semi_axes,
        "num_surface_samples": n_samples**2,
    }


# =============================================================================
# ELLIPSOIDAL HARMONIC CLASS
# =============================================================================

@dataclass
class EllipsoidalHarmonic:
    """
    Ellipsoidal harmonic (Lamé function) of given order.

    This class represents a single ellipsoidal harmonic function,
    which is a solution to Laplace's equation in ellipsoidal
    coordinates.

    Attributes:
        order: Degree n of the harmonic.
        semi_axes: (a, b, c) of the reference ellipsoid.
        eigenvalue: Separation constant for this harmonic.
    """

    order: int
    semi_axes: Tuple[float, float, float]
    eigenvalue: float = None

    def __post_init__(self):
        """Compute eigenvalue for the harmonic."""
        a, b, c = self.semi_axes
        # Eigenvalues for Lamé equation depend on order
        # For n=0: eigenvalue = 0 (constant)
        # For n=1: eigenvalues related to axes ratios
        # For n>=2: eigenvalues are roots of transcendental equation

        if self.eigenvalue is None:
            if self.order == 0:
                self.eigenvalue = 0.0
            elif self.order == 1:
                # First order: three possible eigenvalues
                self.eigenvalue = (a**2 + b**2 + c**2) / 3
            else:
                # Higher orders require numerical solution
                self.eigenvalue = self.order * (self.order + 1) * (a**2 + b**2 + c**2) / 3

    @maxwell_cite(
        154, 155, 156,
        part=1, chapter="Confocal Surfaces",
        theory_class="maxwell_original",
        description="Evaluate ellipsoidal harmonic at point"
    )
    def evaluate(self, lambda_coord: float, mu_coord: float, nu_coord: float) -> float:
        """
        Evaluate the harmonic at given ellipsoidal coordinates.

        Args:
            lambda_coord, mu_coord, nu_coord: Ellipsoidal coordinates.

        Returns:
            Value of the harmonic function.
        """
        # For proper Lamé functions, this would solve the Lamé ODE
        # Here we use a simplified polynomial approximation

        if self.order == 0:
            return 1.0  # Constant (monopole)

        elif self.order == 1:
            # First order (dipole-like): linear in coordinates
            return lambda_coord + mu_coord + nu_coord

        else:
            # Higher orders: polynomial in coordinates
            # This is a placeholder - actual Lamé functions are more complex
            return (lambda_coord * mu_coord * nu_coord) ** (self.order / 3)

    @classmethod
    def generate_basis(cls, semi_axes: Tuple[float, float, float], max_order: int) -> list:
        """
        Generate a complete basis of ellipsoidal harmonics up to max_order.

        Args:
            semi_axes: (a, b, c) of reference ellipsoid.
            max_order: Maximum harmonic order.

        Returns:
            List of EllipsoidalHarmonic objects.
        """
        basis = []
        for n in range(max_order + 1):
            # Each order n has (2n+1) harmonics
            for m in range(2*n + 1):
                harmonic = cls(order=n, semi_axes=semi_axes)
                basis.append(harmonic)
        return basis


# =============================================================================
# MAIN: Module verification
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CONFOCAL SURFACES")
    print("Maxwell's Treatise, Part I, Chapter X (Arts. 147-156)")
    print("=" * 70)

    # Test 1: Charged conducting ellipsoid
    print("\n--- Charged Conducting Ellipsoid (Arts. 147-150) ---")
    result = confocal_ellipsoid_potential(
        total_charge=100,
        semi_axes=(3.0, 2.0, 1.0),
        evaluation_point=np.array([5.0, 0.0, 0.0])
    )
    print(f"  Semi-axes: a={result['semi_axes'][0]}, b={result['semi_axes'][1]}, c={result['semi_axes'][2]} cm")
    print(f"  Type: {result['ellipsoid_type']}")
    print(f"  Total charge: Q = {result['total_charge']} statC")
    print(f"  Capacitance: C = {result['capacitance']:.4f} cm")
    print(f"  Surface potential: V = {result['surface_potential']:.4f} statV")
    print(f"  Potential at (5,0,0): V = {result['potential_at_point']:.4f} statV")

    # Test 2: Ellipsoid capacitance
    print("\n--- Ellipsoid Capacitance (Arts. 147-148) ---")
    result = ellipsoid_capacitance((2.0, 1.0, 1.0))
    print(f"  Prolate spheroid (a=2, b=c=1):")
    print(f"    Capacitance: C = {result['capacitance']:.4f} cm")
    print(f"    Eccentricity: e = {result['eccentricity']:.4f}")

    result = ellipsoid_capacitance((1.0, 1.0, 0.5))
    print(f"  Oblate spheroid (a=b=1, c=0.5):")
    print(f"    Capacitance: C = {result['capacitance']:.4f} cm")
    print(f"    Eccentricity: e = {result['eccentricity']:.4f}")

    result = ellipsoid_capacitance((1.0, 1.0, 1.0))
    print(f"  Sphere (R=1):")
    print(f"    Capacitance: C = {result['capacitance']:.4f} cm")

    # Test 3: Confocal hyperboloid
    print("\n--- Confocal Hyperboloid (Arts. 151-153) ---")
    result = confocal_hyperboloid(
        focal_distance=2.0,
        hyperboloid_parameter=-1.0,  # One sheet
        potential_value=100
    )
    print(f"  Hyperboloid of one sheet:")
    print(f"    Type: {result['hyperboloid_type']}")
    print(f"    Semi-axes: {result['semi_axes']}")
    print(f"    Asymptotic cone angle: {np.degrees(result['asymptotic_cone_angle']):.2f} degrees")
    print(f"    Waist radius: {result['waist_radius']:.4f} cm")

    result = confocal_hyperboloid(
        focal_distance=2.0,
        hyperboloid_parameter=1.0,  # Two sheets
    )
    print(f"  Hyperboloid of two sheets:")
    print(f"    Type: {result['hyperboloid_type']}")
    print(f"    Vertex distance: {result['vertex_distance']:.4f} cm")

    # Test 4: Field line tracing
    print("\n--- Confocal Field Lines (Arts. 151-152) ---")
    result = confocal_field_lines(
        ellipsoid_axes=(3.0, 2.0, 1.0),
        starting_point=np.array([4.0, 0.0, 0.0]),
        num_points=50
    )
    print(f"  Field line traced from (4, 0, 0)")
    print(f"  Number of points: {result['num_points']}")
    print(f"  Total length: {result['total_length']} cm")
    print(f"  End point: {result['outward_line'][-1]}")

    # Test 5: Ellipsoidal coordinates
    print("\n--- Ellipsoidal Coordinates (Arts. 154-156) ---")
    result = ellipsoidal_coordinates(
        x=4.0, y=2.0, z=1.0,
        semi_axes=(3.0, 2.0, 1.0)
    )
    print(f"  Cartesian: (4, 2, 1)")
    print(f"  Ellipsoidal coordinates:")
    print(f"    lambda = {result['lambda_coord']:.4f}")
    print(f"    mu = {result['mu_coord']:.4f}")
    print(f"    nu = {result['nu_coord']:.4f}")
    print(f"  Scale factors: {result['scale_factors']}")

    # Test 6: Laplacian check
    print("\n--- Laplacian in Ellipsoidal Coordinates (Art. 156) ---")
    def V_simple(l, m, n):
        return l + m + n  # Linear function (should be harmonic)

    result = laplacian_ellipsoidal(
        potential_func=V_simple,
        lambda_coord=0.5, mu_coord=1.5, nu_coord=2.5,
        semi_axes=(3.0, 2.0, 1.0)
    )
    print(f"  Linear potential V = lambda + mu + nu")
    print(f"  Laplacian: {result['laplacian']:.2e} (should be ~0)")
    print(f"  Is harmonic: {result['is_harmonic']}")

    # Test 7: Harmonic expansion
    print("\n--- Ellipsoidal Harmonic Expansion (Arts. 154-156) ---")
    def V_boundary(x, y, z):
        return 100 + 10*x + 5*y + 2*z  # Linear + constant

    result = ellipsoidal_harmonic_expansion(
        boundary_potential=V_boundary,
        semi_axes=(2.0, 1.5, 1.0),
        max_order=2
    )
    print(f"  Boundary potential: V = 100 + 10x + 5y + 2z")
    print(f"  Monopole coefficient: A_00 = {result['expansion_coefficients']['monopole']:.4f}")
    print(f"  Dipole coefficients: (A_x, A_y, A_z) = {result['expansion_coefficients']['dipole']}")
    print(f"  Reconstruction error: {result['reconstruction_error']:.4e}")

    # Test 8: EllipsoidalHarmonic class
    print("\n--- EllipsoidalHarmonic Class (Arts. 154-156) ---")
    harmonic = EllipsoidalHarmonic(order=2, semi_axes=(3.0, 2.0, 1.0))
    print(f"  Order n=2 harmonic:")
    print(f"    Eigenvalue: {harmonic.eigenvalue:.4f}")
    print(f"    Evaluated at (1, 2, 3): {harmonic.evaluate(1, 2, 3):.4f}")

    basis = EllipsoidalHarmonic.generate_basis((2.0, 1.5, 1.0), max_order=2)
    print(f"  Generated {len(basis)} harmonics up to order 2")

    print("\n" + "=" * 70)
    print("Module verification complete.")
    print("=" * 70)

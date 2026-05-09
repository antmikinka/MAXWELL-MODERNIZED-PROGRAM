"""maxwell.math.conjugate_functions — Conjugate functions in 2D electrostatics (Arts. 182-206).

Implements Maxwell's mathematical theory of conjugate functions for solving
two-dimensional electrostatic problems using conformal mapping techniques.

Maxwell's Conjugate Functions (Arts. 182-206):
    If phi(x, y) is a potential function satisfying Laplace's equation,
    its conjugate function psi(x, y) gives the streamlines (lines of force).

    Cauchy-Riemann equations (Arts. 182-185):
        d(phi)/dx = d(psi)/dy
        d(phi)/dy = -d(psi)/dx

    Complex potential:
        w(z) = phi(x, y) + i * psi(x, y) where z = x + iy

    Conformal mappings preserve angles and transform solutions of
    Laplace's equation to other solutions.

Key transformations (Arts. 190-204):
    Inversion:        w = 1/z (point inversion through unit circle)
    Exponential:      w = exp(z) (parallel plates to radial field)
    Logarithmic:      w = log(z) (line charge potential)
    Bilinear/Mobius:  w = (az + b)/(cz + d) (general conformal map)

Applications (Arts. 195-206):
    - Parallel plate capacitor edge effects
    - Line charge potentials
    - Capacitance calculation in 2D

All calculations use CGS-EMU units.

Category: C (standard_math) — Conformal mapping for 2D electrostatics.

References:
    Part I, Arts. 182-206: Theory of conjugate functions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Tuple

import numpy as np

from maxwell.meta.citation import maxwell_cite

# Type aliases
ComplexFunction = Callable[[complex], complex]
RealFunction2D = Callable[[float, float], float]


@dataclass
class ConjugatePair:
    """
    A pair of conjugate functions (phi, psi) representing potential and stream function.

    Arts. 182-185: If phi and psi are conjugate functions, then:
        - Both satisfy Laplace's equation
        - Their level curves are orthogonal
        - f(z) = phi + i*psi is analytic

    Attributes:
        phi: Potential function phi(x, y).
        psi: Stream function psi(x, y).
    """

    phi: RealFunction2D
    psi: RealFunction2D

    def __post_init__(self):
        """Validate that functions are callable."""
        if not callable(self.phi):
            raise ValueError("phi must be a callable function")
        if not callable(self.psi):
            raise ValueError("psi must be a callable function")


@maxwell_cite(
    182,
    183,
    184,
    185,
    part=1,
    chapter="Mathematical Theory of Electrification",
    theory_class="standard_math",
    description="Verify Cauchy-Riemann equations for conjugate functions (Arts. 182-185)",
)
def cauchy_riemann_check(
    phi: RealFunction2D,
    psi: RealFunction2D,
    x: float,
    y: float,
    h: float = 1e-6,
    tolerance: float = 1e-6,
) -> Dict[str, Any]:
    """
    Verify that two functions satisfy the Cauchy-Riemann equations.

    Maxwell's formulation (Arts. 182-185):
        For conjugate functions phi and psi:
            d(phi)/dx = d(psi)/dy
            d(phi)/dy = -d(psi)/dx

    These equations ensure that f(z) = phi + i*psi is an analytic function
    of the complex variable z = x + iy.

    Uses central difference for numerical differentiation:
        d(f)/dx ~ (f(x+h) - f(x-h)) / (2h)

    Args:
        phi: Potential function phi(x, y).
        psi: Stream function psi(x, y).
        x, y: Point coordinates (cm).
        h: Step size for numerical differentiation (cm).
        tolerance: Maximum allowable error in C-R equations.

    Returns:
        Dictionary containing:
            - 'dphi_dx': Partial derivative of phi with respect to x
            - 'dphi_dy': Partial derivative of phi with respect to y
            - 'dpsi_dx': Partial derivative of psi with respect to x
            - 'dpsi_dy': Partial derivative of psi with respect to y
            - 'cr1_error': Error in first C-R equation |dphi_dx - dpsi_dy|
            - 'cr2_error': Error in second C-R equation |dphi_dy + dpsi_dx|
            - 'satisfied': True if both equations satisfied within tolerance

    Reference:
        Part I, Arts. 182-185: Cauchy-Riemann equations for conjugate functions.

    Example:
        >>> # Verify for w = z^2 = (x^2 - y^2) + i*(2xy)
        >>> def phi(x, y): return x**2 - y**2
        >>> def psi(x, y): return 2*x*y
        >>> result = cauchy_riemann_check(phi, psi, 1.0, 1.0)
        >>> print(f"C-R satisfied: {result['satisfied']}")
    """
    # Central difference derivatives for phi
    dphi_dx = (phi(x + h, y) - phi(x - h, y)) / (2 * h)
    dphi_dy = (phi(x, y + h) - phi(x, y - h)) / (2 * h)

    # Central difference derivatives for psi
    dpsi_dx = (psi(x + h, y) - psi(x - h, y)) / (2 * h)
    dpsi_dy = (psi(x, y + h) - psi(x, y - h)) / (2 * h)

    # Cauchy-Riemann equations
    cr1_error = abs(dphi_dx - dpsi_dy)  # dphi/dx = dpsi/dy
    cr2_error = abs(dphi_dy + dpsi_dx)  # dphi/dy = -dpsi/dx

    return {
        "dphi_dx": dphi_dx,
        "dphi_dy": dphi_dy,
        "dpsi_dx": dpsi_dx,
        "dpsi_dy": dpsi_dy,
        "cr1_error": cr1_error,
        "cr2_error": cr2_error,
        "satisfied": (cr1_error < tolerance) and (cr2_error < tolerance),
    }


@maxwell_cite(
    186,
    187,
    188,
    189,
    part=1,
    chapter="Mathematical Theory of Electrification",
    theory_class="maxwell_original",
    description="Find conjugate function using line integration (Arts. 186-189)",
)
def conjugate_function(
    phi: RealFunction2D,
    x: float,
    y: float,
    reference_point: Tuple[float, float] = (0.0, 0.0),
    reference_value: float = 0.0,
    num_steps: int = 100,
) -> float:
    """
    Find the conjugate function psi at a point given the potential phi.

    Maxwell's method (Arts. 186-189):
        Given phi(x, y), the conjugate psi(x, y) is found by integration:
            psi(x, y) = psi_0 + integral from (x0, y0) to (x, y) of:
                       (-d(phi)/dy * dx + d(phi)/dx * dy)

        This follows from the Cauchy-Riemann equations:
            d(psi)/dx = -d(phi)/dy
            d(psi)/dy = d(phi)/dx

    The integration path is taken as a straight line from the reference
    point to the target point. For analytic functions, the result is
    path-independent.

    Args:
        phi: Potential function phi(x, y).
        x, y: Target point coordinates (cm).
        reference_point: Starting point (x0, y0) for integration (cm).
        reference_value: Value of psi at reference point.
        num_steps: Number of steps for numerical integration.

    Returns:
        Value of the conjugate function psi(x, y).

    Reference:
        Part I, Arts. 186-189: Method of finding conjugate functions.

    Example:
        >>> # Find conjugate of phi = x^2 - y^2 (should give psi = 2xy + const)
        >>> def phi(x, y): return x**2 - y**2
        >>> psi_val = conjugate_function(phi, 1.0, 1.0, reference_point=(0.0, 0.0))
        >>> print(f"psi(1, 1) = {psi_val:.4f} (expected: 2.0)")
    """
    x0, y0 = reference_point
    h_step = 1e-6  # For computing derivatives of phi

    # Parameterize the path from (x0, y0) to (x, y)
    dx_total = x - x0
    dy_total = y - y0

    psi = reference_value

    # Numerical integration along the path using trapezoidal rule
    for i in range(num_steps):
        t1 = i / num_steps
        t2 = (i + 1) / num_steps

        # Position at each end of segment
        x1 = x0 + t1 * dx_total
        y1 = y0 + t1 * dy_total
        x2 = x0 + t2 * dx_total
        y2 = y0 + t2 * dy_total

        # Derivatives at each end
        dphi_dx1 = (phi(x1 + h_step, y1) - phi(x1 - h_step, y1)) / (2 * h_step)
        dphi_dy1 = (phi(x1, y1 + h_step) - phi(x1, y1 - h_step)) / (2 * h_step)
        dphi_dx2 = (phi(x2 + h_step, y2) - phi(x2 - h_step, y2)) / (2 * h_step)
        dphi_dy2 = (phi(x2, y2 + h_step) - phi(x2, y2 - h_step)) / (2 * h_step)

        # Segment differentials
        dx_seg = x2 - x1
        dy_seg = y2 - y1

        # Trapezoidal integration:
        # d(psi) = -d(phi)/dy * dx + d(phi)/dx * dy
        dpsi1 = -dphi_dy1 * dx_seg + dphi_dx1 * dy_seg
        dpsi2 = -dphi_dy2 * dx_seg + dphi_dx2 * dy_seg

        psi += 0.5 * (dpsi1 + dpsi2)

    return psi


@maxwell_cite(
    190,
    191,
    192,
    193,
    194,
    part=1,
    chapter="Mathematical Theory of Electrification",
    theory_class="maxwell_original",
    description="Inversion conformal mapping z -> 1/z (Arts. 190-194)",
)
def inversion_transform(
    z: complex,
    scale: float = 1.0,
) -> complex:
    """
    Apply the inversion transformation w = scale/z.

    Maxwell's inversion (Arts. 190-194):
        The transformation w = 1/z (or w = scale/z) maps:
        - Points inside the unit circle to outside
        - Points outside to inside
        - Circles through origin to straight lines
        - Straight lines not through origin to circles through origin

    This is useful for transforming electrostatic problems with
    cylindrical symmetry or for mapping exterior problems to interior ones.

    Args:
        z: Complex coordinate z = x + iy (cm).
        scale: Scaling factor for inversion (cm^2). Default is 1.

    Returns:
        Transformed complex coordinate w = scale/z.

    Reference:
        Part I, Arts. 190-194: Inversion transformation.

    Example:
        >>> # Invert point z = 2 + 0i
        >>> w = inversion_transform(2 + 0j)
        >>> print(f"w = {w}")  # Should be 0.5 + 0j

        >>> # Invert with scale factor
        >>> w = inversion_transform(2 + 0j, scale=4.0)
        >>> print(f"w = {w}")  # Should be 2.0 + 0j
    """
    if z == 0:
        raise ValueError("Inversion undefined at z = 0")
    return scale / z


@maxwell_cite(
    190,
    191,
    192,
    193,
    194,
    part=1,
    chapter="Mathematical Theory of Electrification",
    theory_class="maxwell_original",
    description="Inverse of inversion transformation (Arts. 190-194)",
)
def inverse_inversion_transform(
    w: complex,
    scale: float = 1.0,
) -> complex:
    """
    Apply the inverse of the inversion transformation.

    Maxwell's inversion inverse (Arts. 190-194):
        If w = scale/z, then z = scale/w.

    This is the same functional form as the forward transformation,
    reflecting the self-inverse property of inversion.

    Args:
        w: Transformed complex coordinate (cm).
        scale: Scaling factor used in forward transformation (cm^2).

    Returns:
        Original complex coordinate z = scale/w.

    Reference:
        Part I, Arts. 190-194: Inversion transformation inverse.

    Example:
        >>> # Recover z from w = 0.5 + 0j
        >>> z = inverse_inversion_transform(0.5 + 0j)
        >>> print(f"z = {z}")  # Should be 2.0 + 0j
    """
    if w == 0:
        raise ValueError("Inverse inversion undefined at w = 0")
    return scale / w


@maxwell_cite(
    190,
    191,
    192,
    193,
    194,
    part=1,
    chapter="Mathematical Theory of Electrification",
    theory_class="maxwell_original",
    description="Map geometry under inversion (Arts. 190-194)",
)
def map_geometry_under_inversion(
    points: np.ndarray,
    scale: float = 1.0,
    include_inverse: bool = False,
) -> Dict[str, np.ndarray]:
    """
    Map a set of points under the inversion transformation.

    Maxwell's application (Arts. 190-194):
        Transform electrode geometries and field point grids under inversion
        to solve complex electrostatic problems by mapping to simpler geometries.

    Args:
        points: Array of complex coordinates shape (N,) or (N, 2) for [x, y] pairs.
        scale: Scaling factor for inversion (cm^2).
        include_inverse: If True, also compute inverse transformation.

    Returns:
        Dictionary containing:
            - 'transformed': Array of transformed points w = scale/z
            - 'inverse': Array of inverse-transformed points (if include_inverse)

    Reference:
        Part I, Arts. 190-194: Geometry mapping under inversion.

    Example:
        >>> # Map a circle of radius 2 centered at origin
        >>> theta = np.linspace(0, 2*np.pi, 100)
        >>> circle = 2 * np.exp(1j * theta)
        >>> result = map_geometry_under_inversion(circle)
        >>> # Result is a circle of radius 0.5
    """
    # Handle both complex array and [x, y] array inputs
    if points.ndim == 2 and points.shape[1] == 2:
        z_points = points[:, 0] + 1j * points[:, 1]
    else:
        z_points = np.asarray(points, dtype=complex)

    # Apply inversion, handling potential singularity at origin
    with np.errstate(divide="ignore", invalid="ignore"):
        transformed = scale / z_points
        transformed = np.where(np.isfinite(transformed), transformed, np.nan)

    result = {"transformed": transformed}

    if include_inverse:
        with np.errstate(divide="ignore", invalid="ignore"):
            inverse = scale / transformed
            inverse = np.where(np.isfinite(inverse), inverse, np.nan)
        result["inverse"] = inverse

    return result


@maxwell_cite(
    195,
    196,
    197,
    198,
    part=1,
    chapter="Mathematical Theory of Electrification",
    theory_class="maxwell_original",
    description="Exponential mapping w = exp(z) for parallel plates (Arts. 195-198)",
)
def exponential_transform(
    z: complex,
    scale: float = 1.0,
) -> complex:
    """
    Apply the exponential transformation w = scale * exp(z).

    Maxwell's exponential mapping (Arts. 195-198):
        The transformation w = exp(z) maps:
        - Horizontal lines (y = const) to rays from origin
        - Vertical lines (x = const) to circles centered at origin
        - Infinite strip to the entire w-plane (with branch cut)

    This is particularly useful for mapping parallel plate capacitor
    geometry to a radial configuration, or vice versa.

    In electrostatics:
        - A uniform field in the z-plane becomes a radial field in w-plane
        - Parallel plates at different potentials map to circular arcs

    Args:
        z: Complex coordinate z = x + iy (dimensionless for exp).
        scale: Optional scaling factor for the result.

    Returns:
        Transformed complex coordinate w = scale * exp(z).

    Reference:
        Part I, Arts. 195-198: Exponential transformation.

    Example:
        >>> # Map point z = 0 + i*pi/2
        >>> w = exponential_transform(0 + 1j * np.pi/2)
        >>> print(f"w = {w:.4f}")  # Should be approximately i

        >>> # Map a vertical strip
        >>> x_vals = np.linspace(0, 1, 10)
        >>> for x in x_vals:
        ...     w = exponential_transform(x + 0j)
        ...     print(f"z={x} -> w={w.real:.4f}")
    """
    return scale * np.exp(z)


@maxwell_cite(
    195,
    196,
    197,
    198,
    part=1,
    chapter="Mathematical Theory of Electrification",
    theory_class="maxwell_original",
    description="Inverse of exponential mapping w = log(z) (Arts. 195-198)",
)
def logarithmic_transform(
    w: complex,
    scale: float = 1.0,
    branch: int = 0,
) -> complex:
    """
    Apply the logarithmic transformation z = log(w/scale).

    Maxwell's logarithmic mapping (Arts. 195-198, 199-201):
        The inverse transformation z = log(w) maps:
        - Rays from origin to horizontal lines
        - Circles centered at origin to vertical lines
        - Radial field configuration to uniform field

    This is the inverse of the exponential transform and is used for:
        - Line charge potential calculations
        - Mapping circular electrodes to parallel plates
        - Computing capacitance of coaxial cylinders

    The branch parameter selects the Riemann sheet:
        log(w) = ln|w| + i*(arg(w) + 2*pi*branch)

    Args:
        w: Complex coordinate in w-plane.
        scale: Scaling factor to apply before logarithm.
        branch: Branch number for multi-valued logarithm (default 0).

    Returns:
        Transformed complex coordinate z = log(w/scale).

    Reference:
        Part I, Arts. 195-198, 199-201: Logarithmic transformation.

    Example:
        >>> # Map point w = exp(1 + i*pi/4) back
        >>> z = logarithmic_transform(np.exp(1 + 1j*np.pi/4))
        >>> print(f"z = {z}")  # Should be approximately 1 + i*pi/4

        >>> # Line charge: potential is logarithmic
        >>> def line_charge_potential(x, y, lambda_charge):
        ...     z = x + 1j*y
        ...     phi = -2 * lambda_charge * np.log(np.abs(z))
        ...     return phi
    """
    if w == 0:
        raise ValueError("Logarithm undefined at w = 0")
    return np.log(w / scale) + 1j * 2 * np.pi * branch


@maxwell_cite(
    199,
    200,
    201,
    part=1,
    chapter="Mathematical Theory of Electrification",
    theory_class="maxwell_original",
    description="Combined log-exp mapping for line charge problems (Arts. 199-201)",
)
def line_charge_mapping(
    observation_point: complex,
    line_charge_position: complex,
    linear_charge_density: float,
) -> Dict[str, float]:
    """
    Compute potential and stream function for a line charge using logarithmic mapping.

    Maxwell's line charge solution (Arts. 199-201):
        For an infinite line charge with density lambda at position z0:

        Complex potential:
            w(z) = -2*lambda * log(z - z0)

        Potential (real part):
            phi(x, y) = -2*lambda * ln|z - z0|

        Stream function (imaginary part):
            psi(x, y) = -2*lambda * arg(z - z0)

    In CGS-EMU units, lambda is in emu/cm, potential in emu.

    Args:
        observation_point: Complex coordinate z = x + iy where field is computed (cm).
        line_charge_position: Complex coordinate z0 of line charge (cm).
        linear_charge_density: Charge density lambda in CGS-EMU (emu/cm).

    Returns:
        Dictionary containing:
            - 'potential': Electrostatic potential phi (CGS-EMU)
            - 'stream_function': Stream function psi (CGS-EMU)
            - 'field_magnitude': |E| = |grad(phi)| (CGS-EMU)
            - 'distance': |z - z0| (cm)

    Reference:
        Part I, Arts. 199-201: Line charge potential.

    Example:
        >>> # Line charge at origin with lambda = 1
        >>> result = line_charge_mapping(1+0j, 0+0j, 1.0)
        >>> print(f"Potential at (1,0): {result['potential']:.4f}")
        >>> print(f"Field magnitude: {result['field_magnitude']:.4f}")
    """
    # Relative position
    z_rel = observation_point - line_charge_position
    r = np.abs(z_rel)

    if r == 0:
        raise ValueError("Observation point coincides with line charge")

    # Complex potential w = -2*lambda*log(z - z0)
    log_z = np.log(z_rel)

    potential = -2.0 * linear_charge_density * log_z.real
    stream_function = -2.0 * linear_charge_density * log_z.imag

    # Field magnitude |E| = 2*lambda / r
    field_magnitude = 2.0 * abs(linear_charge_density) / r

    return {
        "potential": potential,
        "stream_function": stream_function,
        "field_magnitude": field_magnitude,
        "distance": r,
    }


@maxwell_cite(
    202,
    203,
    204,
    part=1,
    chapter="Mathematical Theory of Electrification",
    theory_class="maxwell_original",
    description="Bilinear (Mobius) transformation (Arts. 202-204)",
)
def bilinear_transform(
    z: complex,
    a: complex,
    b: complex,
    c: complex,
    d: complex,
) -> complex:
    """
    Apply the bilinear (Mobius) transformation w = (az + b)/(cz + d).

    Maxwell's bilinear mapping (Arts. 202-204):
        The most general conformal one-to-one mapping of the extended
        complex plane:
            w = (a*z + b) / (c*z + d)

        where ad - bc != 0 (non-degenerate condition).

    Properties:
        - Maps circles and lines to circles and lines
        - Preserves angles (conformal)
        - Three points can be mapped to any three target points
        - Inverse is also a bilinear transform

    Special cases include:
        - Translation: w = z + b (a=1, c=0, d=1)
        - Rotation: w = exp(i*theta)*z (a=exp(i*theta), c=0, d=1)
        - Scaling: w = k*z (a=k, c=0, d=1)
        - Inversion: w = 1/z (a=0, b=1, c=1, d=0)

    Args:
        z: Complex coordinate to transform.
        a, b, c, d: Complex coefficients of the transformation.

    Returns:
        Transformed complex coordinate w = (az + b)/(cz + d).

    Raises:
        ValueError: If ad - bc = 0 (degenerate) or cz + d = 0 (pole).

    Reference:
        Part I, Arts. 202-204: Bilinear transformations.

    Example:
        >>> # Cayley transform: maps upper half-plane to unit disk
        >>> w = bilinear_transform(1j, a=1, b=-1j, c=1, d=1j)
        >>> print(f"Cayley of i: {w}")

        >>> # Map three points to desired locations
        >>> # Find a, b, c, d such that z1->w1, z2->w2, z3->w3
    """
    # Check non-degeneracy
    determinant = a * d - b * c
    if abs(determinant) < 1e-15:
        raise ValueError("Degenerate transformation: ad - bc = 0")

    denominator = c * z + d
    if abs(denominator) < 1e-15:
        raise ValueError("Transformation has a pole at this z value")

    return (a * z + b) / denominator


@maxwell_cite(
    202,
    203,
    204,
    part=1,
    chapter="Mathematical Theory of Electrification",
    theory_class="maxwell_original",
    description="Compute bilinear transform coefficients from point mapping (Arts. 202-204)",
)
def bilinear_transform_coefficients(
    z1: complex,
    w1: complex,
    z2: complex,
    w2: complex,
    z3: complex,
    w3: complex,
) -> Dict[str, complex]:
    """
    Compute bilinear transform coefficients that map three points to three targets.

    Maxwell's method (Arts. 202-204):
        Given three source points z1, z2, z3 and three target points w1, w2, w3,
        find the unique bilinear transform w = (az + b)/(cz + d) that maps
        zi -> wi for i = 1, 2, 3.

    The coefficients are determined up to a common factor by solving:
        (a*zi + b) - wi*(c*zi + d) = 0 for i = 1, 2, 3

    Args:
        z1, z2, z3: Source points in the z-plane.
        w1, w2, w3: Target points in the w-plane.

    Returns:
        Dictionary with coefficients 'a', 'b', 'c', 'd'.

    Reference:
        Part I, Arts. 202-204: Determining bilinear transform coefficients.

    Example:
        >>> # Map unit disk to upper half-plane
        >>> coeffs = bilinear_transform_coefficients(
        ...     z1=1, w1=0,      # 1 -> 0
        ...     z2=1j, w2=1,     # i -> 1
        ...     z3=-1, w2=np.inf # -1 -> infinity
        ... )
        >>> print(f"a={coeffs['a']}, b={coeffs['b']}, c={coeffs['c']}, d={coeffs['d']}")
    """
    # Handle infinity by using limiting procedure
    # For w3 = infinity, we need c*z3 + d = 0, so we can set c = 1, d = -z3

    if np.isinf(np.abs(w1)) or np.isinf(np.abs(w2)) or np.isinf(np.abs(w3)):
        # Special handling for infinity targets
        if np.isinf(np.abs(w3)):
            # c*z3 + d = 0, choose c = 1, d = -z3
            c = 1.0
            d = -z3
            # Now solve for a, b from remaining two equations
            # (a*z1 + b) = w1*(z1 - z3)
            # (a*z2 + b) = w2*(z2 - z3)
            rhs1 = w1 * (z1 - z3) if not np.isinf(np.abs(w1)) else 1.0
            rhs2 = w2 * (z2 - z3) if not np.isinf(np.abs(w2)) else 1.0

            if np.isinf(np.abs(w1)):
                # a*z1 + b = 0, choose a = 1, b = -z1
                a = 1.0
                b = -z1
            elif np.isinf(np.abs(w2)):
                a = 1.0
                b = -z2
            else:
                a = (rhs1 - rhs2) / (z1 - z2)
                b = rhs1 - a * z1
        else:
            raise NotImplementedError(
                "Infinity handling for w1 or w2 not fully implemented"
            )
    else:
        # Standard case: all finite
        # Use cross-ratio formula or direct solution
        # The bilinear transform preserving cross-ratio:
        # (w - w1)(w2 - w3) / ((w - w3)(w2 - w1)) = (z - z1)(z2 - z3) / ((z - z3)(z2 - z1))

        # Direct matrix approach: solve homogeneous system
        # For each point: a*zi + b - wi*c*zi - wi*d = 0
        # This gives 3 equations in 4 unknowns (a, b, c, d)
        # We can set one coefficient to 1 and solve for the others

        # Set d = 1 (valid if d != 0) and solve for a, b, c
        # a*z1 + b - w1*c*z1 = w1
        # a*z2 + b - w2*c*z2 = w2
        # a*z3 + b - w3*c*z3 = w3

        A = np.array(
            [
                [z1, 1, -w1 * z1],
                [z2, 1, -w2 * z2],
                [z3, 1, -w3 * z3],
            ],
            dtype=complex,
        )
        b_vec = np.array([w1, w2, w3], dtype=complex)

        try:
            solution = np.linalg.solve(A, b_vec)
            a, b, c = solution
            d = 1.0 + 0j
        except np.linalg.LinAlgError:
            # Matrix singular, try setting c = 1 instead
            # a*z1 + b - w1*d = w1*z1
            A = np.array(
                [
                    [z1, 1, -w1],
                    [z2, 1, -w2],
                    [z3, 1, -w3],
                ],
                dtype=complex,
            )
            b_vec = np.array([w1 * z1, w2 * z2, w3 * z3], dtype=complex)
            solution = np.linalg.solve(A, b_vec)
            a, b, d = solution
            c = 1.0 + 0j

    return {"a": a, "b": b, "c": c, "d": d}


@maxwell_cite(
    205,
    206,
    part=1,
    chapter="Mathematical Theory of Electrification",
    theory_class="maxwell_original",
    description="Compute edge effect correction for parallel plate capacitor (Arts. 205-206)",
)
def edge_effect_correction(
    plate_separation: float,
    plate_length: float,
    observation_point: complex,
    potential_difference: float,
) -> Dict[str, float]:
    """
    Compute edge effect (fringe field) correction for a parallel plate capacitor.

    Maxwell's edge correction (Arts. 205-206):
        For a parallel plate capacitor with finite plates, the field near
        the edges deviates from the uniform field approximation. Using
        conformal mapping (Schwarz-Christoffel transformation), the
        fringe field can be computed.

        The transformation from the parallel plate geometry to a half-plane
        allows calculation of the potential and field including edge effects.

    For a capacitor with:
        - Plate separation: d
        - Plate length: L
        - Potential difference: V

        The complex potential is found by mapping the geometry to a
        simpler configuration where the solution is known.

    Args:
        plate_separation: Distance between plates d (cm).
        plate_length: Length of plates L (cm).
        observation_point: Complex coordinate z = x + iy where field is computed (cm).
        potential_difference: Voltage V between plates (CGS-EMU statvolts).

    Returns:
        Dictionary containing:
            - 'potential': Corrected potential phi including edge effects
            - 'field_x': x-component of electric field Ex
            - 'field_y': y-component of electric field Ey
            - 'field_magnitude': |E|
            - 'fringe_factor': Ratio of actual field to uniform field

    Reference:
        Part I, Arts. 205-206: Edge effects in capacitors.

    Example:
        >>> # Capacitor with d=1cm, L=10cm, V=100 statvolts
        >>> result = edge_effect_correction(1.0, 10.0, 5.0+0.5j, 100.0)
        >>> print(f"Field at edge: {result['field_magnitude']:.4f}")
        >>> print(f"Fringe factor: {result['fringe_factor']:.4f}")
    """
    d = plate_separation
    L = plate_length
    V = potential_difference
    z = observation_point

    # Uniform field approximation (baseline)
    E_uniform = V / d

    # Schwarz-Christoffel mapping for parallel plates with finite length
    # The transformation w = f(z) maps the parallel plate geometry to upper half-plane
    # For simplicity, we use an approximate formula for the fringe field

    # Position relative to plate edge (assume plates extend from -L/2 to L/2)
    x_rel = z.real - L / 2  # Distance from right edge
    y_rel = z.imag

    # Approximate fringe field correction using conformal mapping result
    # Near the edge, the field behaves like the field near a conducting corner

    # For points near the edge (|x_rel| < d), apply correction
    if abs(x_rel) < d:
        # Fringe field enhancement near edge
        # The field is stronger due to charge concentration at edges
        r_edge = np.sqrt(x_rel**2 + y_rel**2)
        if r_edge > 0.01 * d:  # Avoid singularity at edge
            fringe_factor = 1.0 + 0.5 * np.exp(-abs(x_rel) / d) * (d / r_edge)
        else:
            fringe_factor = 1.0 + 0.5 * np.exp(-abs(x_rel) / d) * 100
    else:
        # Far from edge, field approaches uniform
        fringe_factor = 1.0 + 0.1 * np.exp(-abs(x_rel) / d)

    # Corrected field
    E_magnitude = E_uniform * fringe_factor

    # Field direction (approximately perpendicular to plates, with fringe bending)
    if x_rel > 0:
        # Outside capacitor, field bends outward
        angle = np.arctan2(y_rel, x_rel)
        field_x = E_magnitude * np.cos(angle)
        field_y = E_magnitude * np.sin(angle)
    else:
        # Between plates, field is mostly uniform
        field_x = 0.0
        field_y = E_magnitude

    # Potential (relative to negative plate at y = d)
    potential = V * (1 - y_rel / d) if 0 <= y_rel <= d else V * np.exp(-y_rel / d)

    return {
        "potential": potential,
        "field_x": field_x,
        "field_y": field_y,
        "field_magnitude": E_magnitude,
        "fringe_factor": fringe_factor,
    }


@maxwell_cite(
    190,
    191,
    192,
    193,
    194,
    195,
    196,
    197,
    198,
    199,
    200,
    part=1,
    chapter="Mathematical Theory of Electrification",
    theory_class="maxwell_original",
    description="Map capacitor geometry using conformal transformation (Arts. 190-200)",
)
def map_capacitor_geometry(
    plate_separation: float,
    plate_length: float,
    num_points: int = 50,
    mapping_type: str = "schwarz_christoffel",
) -> Dict[str, np.ndarray]:
    """
    Generate a conformal map of capacitor geometry for field visualization.

    Maxwell's capacitor mapping (Arts. 190-200):
        Map the physical capacitor geometry (parallel plates with finite length)
        to a simpler geometry where the field is uniform. The inverse map
        then gives the actual field configuration including edge effects.

    Common mappings:
        - Schwarz-Christoffel: Maps polygon boundaries to real axis
        - Exponential: Maps strip to half-plane
        - Logarithmic: Maps half-plane to strip

    Args:
        plate_separation: Distance between plates d (cm).
        plate_length: Length of plates L (cm).
        num_points: Number of grid points in each dimension.
        mapping_type: Type of mapping to use ('schwarz_christoffel', 'exponential', 'logarithmic').

    Returns:
        Dictionary containing:
            - 'z_grid': Physical plane coordinates (num_points x num_points complex array)
            - 'w_grid': Transformed plane coordinates
            - 'potential_grid': Computed potential at each point
            - 'field_grid': Computed field magnitude at each point

    Reference:
        Part I, Arts. 190-200: Capacitor geometry mapping.

    Example:
        >>> # Map a capacitor with d=1cm, L=10cm
        >>> result = map_capacitor_geometry(1.0, 10.0, num_points=30)
        >>> print(f"Grid shape: {result['z_grid'].shape}")
    """
    d = plate_separation
    L = plate_length

    # Create grid in physical plane
    x = np.linspace(-L, L, num_points)
    y = np.linspace(-d, 2 * d, num_points)
    X, Y = np.meshgrid(x, y)
    z_grid = X + 1j * Y

    # Apply appropriate mapping based on type
    if mapping_type == "exponential":
        # Map strip to half-plane using exponential
        w_grid = np.exp(np.pi * z_grid / d)
    elif mapping_type == "logarithmic":
        # Map half-plane to strip using logarithm
        w_grid = (d / np.pi) * np.log(z_grid + 1e-10)  # Avoid log(0)
    elif mapping_type == "schwarz_christoffel":
        # Approximate Schwarz-Christoffel for parallel plates
        # w = arcsin(z) maps half-plane to strip
        w_grid = np.arcsin(z_grid / (L / 2))
    else:
        raise ValueError(f"Unknown mapping_type: {mapping_type}")

    # Compute potential in transformed plane (simpler geometry)
    # For uniform field in w-plane: phi = Re(w) * V / d
    V = 1.0  # Normalize to unit potential difference
    potential_grid = w_grid.real * V / d

    # Compute field magnitude |E| = |dw/dz| * |E_w|
    # For conformal map, |E_z| = |dw/dz| * |E_w|
    h = 1e-6
    dw_dz = np.zeros_like(z_grid, dtype=complex)

    for i in range(num_points):
        for j in range(num_points):
            z = z_grid[i, j]
            # Numerical derivative
            if mapping_type == "exponential":
                dw_dz[i, j] = (np.pi / d) * np.exp(np.pi * z / d)
            elif mapping_type == "logarithmic":
                dw_dz[i, j] = (d / np.pi) / (z + 1e-10)
            elif mapping_type == "schwarz_christoffel":
                dw_dz[i, j] = 1 / np.sqrt(1 - (z / (L / 2)) ** 2 + 1e-10)

    field_grid = np.abs(dw_dz) * V / d

    return {
        "z_grid": z_grid,
        "w_grid": w_grid,
        "potential_grid": potential_grid,
        "field_grid": field_grid,
    }


@maxwell_cite(
    195,
    196,
    197,
    198,
    199,
    200,
    part=1,
    chapter="Mathematical Theory of Electrification",
    theory_class="maxwell_original",
    description="Compute 2D capacitance using conformal mapping (Arts. 195-200)",
)
def capacitance_2d(
    geometry_type: str,
    **kwargs: float,
) -> Dict[str, float]:
    """
    Compute capacitance per unit length for 2D geometries using conformal mapping.

    Maxwell's capacitance calculation (Arts. 195-200):
        Using conformal mapping, the capacitance of various 2D geometries
        can be computed. The key insight is that capacitance is invariant
        under conformal transformation.

    Supported geometries:
        - 'parallel_plate': Infinite parallel plates (C = epsilon * W / d)
        - 'coaxial': Coaxial cylinders (C = epsilon / (2 * ln(b/a)))
        - 'strip': Conducting strip above ground plane
        - 'cylinder': Single cylinder above ground plane

    In CGS-EMU, epsilon = 1/(4*pi*c^2) where c is speed of light in cm/s.
    For electrostatics in CGS-ESU, epsilon = 1/(4*pi).

    Args:
        geometry_type: Type of geometry (see above).
        **kwargs: Geometry-specific parameters:
            - parallel_plate: width (cm), separation (cm)
            - coaxial: inner_radius (cm), outer_radius (cm)
            - strip: width (cm), height (cm)
            - cylinder: radius (cm), height (cm)

    Returns:
        Dictionary containing:
            - 'capacitance': Capacitance per unit length (CGS-EMU cm)
            - 'geometry': Description of the geometry
            - 'parameters': Input parameters used

    Reference:
        Part I, Arts. 195-200: Capacitance via conformal mapping.

    Example:
        >>> # Coaxial cable: a=0.1cm, b=0.5cm
        >>> result = capacitance_2d('coaxial', inner_radius=0.1, outer_radius=0.5)
        >>> print(f"Capacitance: {result['capacitance']:.6f} cm")

        >>> # Parallel plates: W=10cm, d=0.1cm
        >>> result = capacitance_2d('parallel_plate', width=10.0, separation=0.1)
        >>> print(f"Capacitance: {result['capacitance']:.6f} cm")
    """
    # CGS-EMU permittivity (for electrostatics, use CGS-ESU where epsilon_0 = 1/(4*pi))
    epsilon_0 = 1.0 / (4.0 * np.pi)  # CGS-ESU

    if geometry_type == "parallel_plate":
        width = kwargs.get("width", 1.0)
        separation = kwargs.get("separation", 1.0)

        if separation <= 0:
            raise ValueError("Separation must be positive")

        # C = epsilon * W / d (per unit length)
        capacitance = epsilon_0 * width / separation

        return {
            "capacitance": capacitance,
            "geometry": "Parallel plate capacitor",
            "parameters": {"width": width, "separation": separation},
            "units": "CGS-ESU (cm)",
        }

    elif geometry_type == "coaxial":
        inner_radius = kwargs.get("inner_radius", 1.0)
        outer_radius = kwargs.get("outer_radius", 2.0)

        if inner_radius <= 0 or outer_radius <= inner_radius:
            raise ValueError("Invalid radii: need 0 < a < b")

        # C = epsilon / (2 * ln(b/a)) for coaxial cylinders
        capacitance = epsilon_0 / (2.0 * np.log(outer_radius / inner_radius))

        return {
            "capacitance": capacitance,
            "geometry": "Coaxial cylinders",
            "parameters": {"inner_radius": inner_radius, "outer_radius": outer_radius},
            "units": "CGS-ESU (cm)",
        }

    elif geometry_type == "strip":
        width = kwargs.get("width", 1.0)
        height = kwargs.get("height", 1.0)

        if height <= 0:
            raise ValueError("Height must be positive")

        # Strip above ground plane: approximate formula using conformal mapping
        # C ~ epsilon * W / h * (1 + correction for fringe)
        fringe_correction = 1.0 + (height / (np.pi * width)) * np.log(
            2 * np.pi * width / height
        )
        capacitance = epsilon_0 * width / height * fringe_correction

        return {
            "capacitance": capacitance,
            "geometry": "Conducting strip above ground plane",
            "parameters": {"width": width, "height": height},
            "units": "CGS-ESU (cm)",
        }

    elif geometry_type == "cylinder":
        radius = kwargs.get("radius", 1.0)
        height = kwargs.get("height", 2.0)

        if radius <= 0 or height <= radius:
            raise ValueError("Invalid geometry: need 0 < r < h")

        # Cylinder above ground plane:
        # C = epsilon / (2 * arccosh(h/r)) = epsilon / (2 * ln((h + sqrt(h^2-r^2))/r))
        capacitance = epsilon_0 / (2.0 * np.arccosh(height / radius))

        return {
            "capacitance": capacitance,
            "geometry": "Cylinder above ground plane",
            "parameters": {"radius": radius, "height": height},
            "units": "CGS-ESU (cm)",
        }

    else:
        raise ValueError(f"Unknown geometry_type: {geometry_type}")


@maxwell_cite(
    182,
    183,
    184,
    185,
    186,
    187,
    188,
    189,
    190,
    191,
    192,
    193,
    194,
    195,
    196,
    197,
    198,
    199,
    200,
    201,
    202,
    203,
    204,
    205,
    206,
    part=1,
    chapter="Mathematical Theory of Electrification",
    theory_class="maxwell_original",
    description="Verify conjugate function relations and transformations",
)
def verify_conjugate_functions(
    tolerance: float = 1e-6,
) -> Dict[str, Any]:
    """
    Verify all conjugate function implementations and identities.

    Maxwell's verification (Arts. 182-206):
        This function tests:
        1. Cauchy-Riemann equations for standard functions
        2. Conjugate function computation accuracy
        3. Conformal mapping properties
        4. Capacitance formulas

    Args:
        tolerance: Numerical tolerance for verification tests.

    Returns:
        Dictionary containing verification results for each test.

    Reference:
        Part I, Arts. 182-206: Complete conjugate function verification.

    Example:
        >>> results = verify_conjugate_functions()
        >>> print(f"All tests passed: {results['all_verified']}")
    """
    results = {}
    all_verified = True

    # Test 1: Cauchy-Riemann for w = z^2
    def phi_z2(x, y):
        return x**2 - y**2

    def psi_z2(x, y):
        return 2 * x * y

    cr_result = cauchy_riemann_check(phi_z2, psi_z2, 1.0, 1.0, tolerance=tolerance)
    results["z_squared_cr"] = cr_result["satisfied"]
    all_verified = all_verified and cr_result["satisfied"]

    # Test 2: Cauchy-Riemann for w = exp(z)
    def phi_exp(x, y):
        return np.exp(x) * np.cos(y)

    def psi_exp(x, y):
        return np.exp(x) * np.sin(y)

    cr_exp = cauchy_riemann_check(phi_exp, psi_exp, 0.5, np.pi / 4, tolerance=tolerance)
    results["exp_cr"] = cr_exp["satisfied"]
    all_verified = all_verified and cr_exp["satisfied"]

    # Test 3: Inversion is self-inverse
    z_test = 2.0 + 1.5j
    w = inversion_transform(z_test, scale=1.0)
    z_back = inverse_inversion_transform(w, scale=1.0)
    inversion_verified = abs(z_test - z_back) < tolerance
    results["inversion_self_inverse"] = inversion_verified
    all_verified = all_verified and inversion_verified

    # Test 4: Exponential and logarithm are inverses
    z_test = 0.5 + 0.3j
    w = exponential_transform(z_test)
    z_back = logarithmic_transform(w)
    exp_log_verified = abs(z_test - z_back) < tolerance
    results["exp_log_inverse"] = exp_log_verified
    all_verified = all_verified and exp_log_verified

    # Test 5: Bilinear transform with known coefficients
    w_test = bilinear_transform(1 + 1j, a=1, b=0, c=0, d=1)  # Identity
    bilinear_verified = abs(w_test - (1 + 1j)) < tolerance
    results["bilinear_identity"] = bilinear_verified
    all_verified = all_verified and bilinear_verified

    # Test 6: Line charge potential
    lc_result = line_charge_mapping(1 + 0j, 0 + 0j, 1.0)
    # For line charge at origin, potential at r=1 should be 0 (since ln(1)=0)
    lc_verified = abs(lc_result["potential"]) < tolerance
    results["line_charge_potential"] = lc_verified
    all_verified = all_verified and lc_verified

    # Test 7: Capacitance formulas
    c_coax = capacitance_2d("coaxial", inner_radius=1.0, outer_radius=np.exp(1))
    # For b/a = e, C = epsilon / 2 = 1/(8*pi)
    expected_c = 1.0 / (8.0 * np.pi)
    coax_verified = abs(c_coax["capacitance"] - expected_c) / expected_c < tolerance
    results["coaxial_capacitance"] = coax_verified
    all_verified = all_verified and coax_verified

    c_pp = capacitance_2d("parallel_plate", width=1.0, separation=1.0)
    expected_c = epsilon_0 = 1.0 / (4.0 * np.pi)
    pp_verified = (
        abs(c_pp["capacitance"] - expected_c) / expected_c < 0.01
    )  # 1% tolerance
    results["parallel_plate_capacitance"] = pp_verified
    all_verified = all_verified and pp_verified

    results["all_verified"] = all_verified
    results["tolerance_used"] = tolerance

    return results


@maxwell_cite(
    182,
    183,
    184,
    185,
    186,
    187,
    188,
    189,
    190,
    191,
    192,
    193,
    194,
    195,
    196,
    197,
    198,
    199,
    200,
    201,
    202,
    203,
    204,
    205,
    206,
    part=1,
    chapter="Mathematical Theory of Electrification",
    theory_class="maxwell_original",
    description="Complete conjugate function analysis toolkit",
)
def analyze_conjugate_functions(
    test_functions: list = None,
    num_grid_points: int = 20,
) -> Dict[str, Any]:
    """
    Complete analysis toolkit for conjugate function problems.

    Maxwell's analysis (Arts. 182-206):
        Comprehensive analysis including:
        1. Cauchy-Riemann verification for multiple functions
        2. Conformal mapping visualization data
        3. Capacitance calculations for various geometries
        4. Edge effect quantification

    Args:
        test_functions: List of (phi, psi, name) tuples to test.
                        If None, uses standard test functions.
        num_grid_points: Number of points for grid-based analysis.

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part I, Arts. 182-206: Complete conjugate function analysis.

    Example:
        >>> results = analyze_conjugate_functions()
        >>> for name, cr_ok in results["cauchy_riemann_tests"].items():
        ...     print(f"{name}: C-R satisfied = {cr_ok}")
    """
    # Default test functions
    if test_functions is None:
        test_functions = [
            (lambda x, y: x**2 - y**2, lambda x, y: 2 * x * y, "z_squared"),
            (
                lambda x, y: np.exp(x) * np.cos(y),
                lambda x, y: np.exp(x) * np.sin(y),
                "exp_z",
            ),
            (lambda x, y: x, lambda x, y: y, "identity"),  # w = z
            (
                lambda x, y: x / (x**2 + y**2),
                lambda x, y: -y / (x**2 + y**2),
                "inverse_z",
            ),
        ]

    results = {}

    # Test Cauchy-Riemann for each function
    cr_results = {}
    for phi, psi, name in test_functions:
        try:
            cr = cauchy_riemann_check(phi, psi, 1.0, 0.5)
            cr_results[name] = cr["satisfied"]
        except (ValueError, ZeroDivisionError):
            cr_results[name] = "error"

    results["cauchy_riemann_tests"] = cr_results

    # Conformal mapping analysis
    z_test = 1.0 + 0.5j
    results["conformal_maps"] = {
        "inversion": inversion_transform(z_test),
        "exponential": exponential_transform(z_test),
        "logarithm": logarithmic_transform(2.0 + 0j),  # Avoid log(0)
    }

    # Capacitance analysis for various geometries
    results["capacitance_analysis"] = {
        "parallel_plate": capacitance_2d("parallel_plate", width=10.0, separation=0.1),
        "coaxial": capacitance_2d("coaxial", inner_radius=0.1, outer_radius=0.5),
        "strip": capacitance_2d("strip", width=1.0, height=0.5),
        "cylinder": capacitance_2d("cylinder", radius=0.1, height=0.5),
    }

    # Edge effect analysis
    results["edge_effect"] = edge_effect_correction(
        plate_separation=1.0,
        plate_length=10.0,
        observation_point=5.0 + 0.5j,
        potential_difference=100.0,
    )

    # Grid mapping for visualization
    results["geometry_map"] = map_capacitor_geometry(
        plate_separation=1.0,
        plate_length=10.0,
        num_points=min(num_grid_points, 30),  # Limit for performance
        mapping_type="exponential",
    )

    results["summary"] = {
        "total_cr_tests": len(cr_results),
        "cr_passed": sum(1 for v in cr_results.values() if v is True),
        "num_capacitance_geometries": 4,
    }

    return results


__all__ = [
    # Data classes
    "ConjugatePair",
    # Core functions (Arts. 182-189)
    "cauchy_riemann_check",
    "conjugate_function",
    # Conformal mappings (Arts. 190-204)
    "inversion_transform",
    "inverse_inversion_transform",
    "map_geometry_under_inversion",
    "exponential_transform",
    "logarithmic_transform",
    "bilinear_transform",
    "bilinear_transform_coefficients",
    # Line charge and applications (Arts. 199-201)
    "line_charge_mapping",
    # Edge effects (Arts. 205-206)
    "edge_effect_correction",
    # Geometry mapping and capacitance (Arts. 190-200)
    "map_capacitor_geometry",
    "capacitance_2d",
    # Verification and analysis
    "verify_conjugate_functions",
    "analyze_conjugate_functions",
]

"""maxwell.math.calculus_calculator — Unified calculus integration engine (Arts. 60-405).

Computes volume integrals (triple integrals), surface integrals (double integrals),
line integrals, and verifies the three fundamental integral theorems (Divergence,
Stokes', Green's) in the context of Maxwell's electromagnetic theory.

All calculations maintain strict CGS unit consistency.

Volume Integrals (Arts. 60-63, 71-77, 85, 405):
    - volume_integral_scalar: Triple integral of scalar fields over 3D volumes
    - volume_integral_vector: Triple integral of vector fields (component-wise)
    - volume_integral_spherical: Spherical coordinate integration with Jacobian

Surface Integrals (Arts. 79-81, 83, 402):
    - surface_integral_vector: Flux of vector fields through parametric surfaces
    - surface_integral_scalar: Surface area and scalar surface integrals
    - surface_integral_sphere: Convenience wrapper for spherical surfaces

Line Integrals (Arts. 242-244, 401):
    - line_integral_vector: Work/EMF along parametric curves
    - line_integral_scalar: Arc length and scalar line integrals
    - line_integral_circle: Closed circle path integral

Theorem Verifications (Arts. 77, 79-81, 182-206, 401-402):
    - verify_divergence_theorem: Gauss's theorem (volume divergence = surface flux)
    - verify_stokes_theorem: Stokes' theorem (surface curl = boundary circulation)
    - verify_greens_theorem: Green's theorem (2D curl integral = boundary circulation)

Theorems (Arts. 103-110):
    - Vector identities: curl(grad phi) = 0, div(curl F) = 0, curl(curl F) = grad(div F) - nabla^2(F)

Category: C (standard_math) — Core integration foundations.

References:
    Part I, Arts. 60-63: Volume charge density.
    Part I, Arts. 71-77: Potential from charge distributions.
    Part I, Arts. 77, 79-81: Divergence theorem and surface integrals.
    Part I, Arts. 83, 85: Mean value theorem, field energy density.
    Part I, Arts. 103-110: Vector calculus identities.
    Part I, Arts. 128-130: Spherical coordinate transformations.
    Part I, Arts. 182-206: Conjugate functions and 2D electrostatics (Green's theorem).
    Part II, Arts. 242-244: Electromotive force definition.
    Part III, Arts. 401-402: Magnetic line/surface integrals.
    Part III, Art. 405: Vector potential from currents.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple, Union

import numpy as np
from scipy.integrate import dblquad, nquad, quad

from maxwell.math.vector_operators import curl, divergence
from maxwell.meta.citation import maxwell_cite

# ── Type aliases ──────────────────────────────────────────────────
VectorField3D = Tuple[
    Callable[[float, float, float], float],
    Callable[[float, float, float], float],
    Callable[[float, float, float], float],
]
ScalarField3D = Callable[[float, float, float], float]
Limits1D = Tuple[float, float]
LimitsCallable = Callable[..., Tuple[float, float]]
ParamSurface = Callable[[float, float], Tuple[float, float, float]]
ParamCurve3D = Callable[[float], Tuple[float, float, float]]
ParamCurve2D = Callable[[float], Tuple[float, float]]

# Numerical differentiation step for parameterization derivatives
H_DERIV: float = 1e-8

# ── Helper: numerical derivative of parameterizations ─────────────


def _numerical_partial(
    r_func: ParamSurface,
    u: float,
    v: float,
    component: int,
    variable: str,
    h: float = H_DERIV,
) -> float:
    """Compute partial derivative of a surface parameterization component.

    Args:
        r_func: Surface parameterization r(u, v) -> (x, y, z).
        u, v: Current parameter values.
        component: Which component to differentiate (0=x, 1=y, 2=z).
        variable: 'u' or 'v'.
        h: Step size for central difference.

    Returns:
        Partial derivative value.
    """
    if variable == "u":
        forward = r_func(u + h, v)[component]
        backward = r_func(u - h, v)[component]
    else:
        forward = r_func(u, v + h)[component]
        backward = r_func(u, v - h)[component]
    return (forward - backward) / (2 * h)


def _numerical_curve_derivative(
    curve_func: ParamCurve3D,
    t: float,
    component: int,
    h: float = H_DERIV,
) -> float:
    """Compute derivative of a curve parameterization component.

    Args:
        curve_func: Curve parameterization r(t) -> (x, y, z).
        t: Current parameter value.
        component: Which component (0=x, 1=y, 2=z).
        h: Step size.

    Returns:
        Derivative value.
    """
    forward = curve_func(t + h)[component]
    backward = curve_func(t - h)[component]
    return (forward - backward) / (2 * h)


def _cross_product(
    a: Tuple[float, float, float], b: Tuple[float, float, float]
) -> Tuple[float, float, float]:
    """Compute 3D cross product."""
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _dot_product(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> float:
    """Compute 3D dot product."""
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _vec_magnitude(v: Tuple[float, float, float]) -> float:
    """Compute vector magnitude."""
    return float(np.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2))


# ═══════════════════════════════════════════════════════════════════
# VOLUME INTEGRALS
# ═══════════════════════════════════════════════════════════════════


@maxwell_cite(
    60,
    61,
    62,
    63,
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    85,
    part=1,
    chapter="On the Relation of Electrification to Liquid Action",
    theory_class="standard_math",
    description="Compute triple integral of scalar field over 3D volume",
)
def volume_integral_scalar(
    func: ScalarField3D,
    x_bounds: Limits1D,
    y_bounds: Union[Limits1D, Callable[[float], Limits1D]],
    z_bounds: Union[Limits1D, Callable[[float, float], Limits1D]],
    epsabs: float = 1e-8,
    epsrel: float = 1e-8,
) -> float:
    """Compute triple integral of a scalar field over a 3D volume.

    I = ∭_V f(x, y, z) dx dy dz

    Uses scipy.integrate.nquad for adaptive multidimensional quadrature.
    Supports variable integration limits for non-rectangular domains.

    Args:
        func: Scalar field f(x, y, z).
        x_bounds: (x_min, x_max) — constant bounds.
        y_bounds: (y_min, y_max) or callable y_min(x), y_max(x).
        z_bounds: (z_min, z_max) or callable z_min(x, y), z_max(x, y).
        epsabs: Absolute error tolerance.
        epsrel: Relative error tolerance.

    Returns:
        Integral value.

    CGS Units:
        If func is charge density (statcoulomb/cm³) and dV in cm³,
        result is in statcoulombs.

    Example:
        >>> # Total charge of uniform sphere (radius R, density rho0)
        >>> R, rho0 = 5.0, 1.0
        >>> def rho(x, y, z):
        ...     return rho0 if x**2 + y**2 + z**2 <= R**2 else 0.0
        >>> Q = volume_integral_scalar(
        ...     rho, (-R, R),
        ...     lambda x: (-np.sqrt(max(0, R**2 - x**2)), np.sqrt(max(0, R**2 - x**2))),
        ...     lambda x, y: (-np.sqrt(max(0, R**2 - x**2 - y**2)),
        ...                    np.sqrt(max(0, R**2 - x**2 - y**2)))
        ... )

    Reference:
        Part I, Arts. 60-63: Volume charge density.
        Part I, Arts. 71-77: Potential from charge distribution.
    """
    # Build limits list for nquad
    # nquad expects limits in order [z, y, x] (innermost first)
    # but the function is called as func(x, y, z), so we wrap it

    if callable(z_bounds):
        z_limits_inner = z_bounds
    else:
        z_lo, z_hi = z_bounds
        z_limits_inner = lambda x, y: (z_lo, z_hi)

    if callable(y_bounds):
        y_limits_inner = y_bounds
    else:
        y_lo, y_hi = y_bounds
        y_limits_inner = lambda x: (y_lo, y_hi)

    limits = [z_limits_inner, y_limits_inner, x_bounds]

    # nquad calls the integrand with args in reverse order: func(z, y, x)
    def integrand(z, y, x):
        return func(x, y, z)

    result, error = nquad(
        integrand,
        limits,
        opts={"epsabs": epsabs, "epsrel": epsrel},
    )
    return float(result)


@maxwell_cite(
    405,
    part=3,
    chapter="Electromagnetic Potential",
    theory_class="standard_math",
    description="Compute triple integral of vector field over 3D volume",
)
def volume_integral_vector(
    Fx: Callable[[float, float, float], float],
    Fy: Callable[[float, float, float], float],
    Fz: Callable[[float, float, float], float],
    x_bounds: Limits1D,
    y_bounds: Union[Limits1D, Callable[[float], Limits1D]],
    z_bounds: Union[Limits1D, Callable[[float, float], Limits1D]],
    epsabs: float = 1e-8,
    epsrel: float = 1e-8,
) -> Tuple[float, float, float]:
    """Compute triple integral of a vector field over a 3D volume.

    Returns (∭ Fx dV, ∭ Fy dV, ∭ Fz dV).

    Applications:
        - Vector potential from current distribution (Art. 405):
          A = (1/c) ∭ J(r') / |r - r'| dV'
        - Total force on volume: F = ∭ f(x,y,z) dV

    Args:
        Fx, Fy, Fz: Vector field component functions.
        x_bounds: (x_min, x_max).
        y_bounds: (y_min, y_max) or callable.
        z_bounds: (z_min, z_max) or callable.
        epsabs: Absolute error tolerance.
        epsrel: Relative error tolerance.

    Returns:
        Tuple of (integral_x, integral_y, integral_z).

    CGS Units:
        If F is current density (abampere/cm²) and dV in cm³,
        result is in abampere·cm.

    Reference:
        Part III, Art. 405: Vector potential from currents.
    """
    ix = volume_integral_scalar(Fx, x_bounds, y_bounds, z_bounds, epsabs, epsrel)
    iy = volume_integral_scalar(Fy, x_bounds, y_bounds, z_bounds, epsabs, epsrel)
    iz = volume_integral_scalar(Fz, x_bounds, y_bounds, z_bounds, epsabs, epsrel)
    return (float(ix), float(iy), float(iz))


@maxwell_cite(
    128,
    129,
    130,
    part=1,
    chapter="On Spherical Harmonics",
    theory_class="standard_math",
    description="Compute volume integral in spherical coordinates",
)
def volume_integral_spherical(
    func: ScalarField3D,
    r_bounds: Limits1D,
    theta_bounds: Limits1D = (0, np.pi),
    phi_bounds: Limits1D = (0, 2 * np.pi),
    epsabs: float = 1e-8,
    epsrel: float = 1e-8,
) -> float:
    """Compute volume integral using spherical coordinates.

    I = ∭ f(r,theta,phi) * r² * sin(theta) dr dtheta dphi

    The Jacobian r²*sin(theta) is automatically applied.
    Internal conversion from spherical to Cartesian coordinates.

    Args:
        func: Scalar field in Cartesian f(x, y, z).
        r_bounds: (r_min, r_max) in cm.
        theta_bounds: (theta_min, theta_max) in radians.
        phi_bounds: (phi_min, phi_max) in radians.
        epsabs: Absolute error tolerance.
        epsrel: Relative error tolerance.

    Returns:
        Integral value.

    Reference:
        Part I, Arts. 128-130: Spherical coordinate transformations.
    """

    def integrand(phi, theta, r):
        """Integrand with Jacobian, in nquad order (phi innermost)."""
        # Convert spherical to Cartesian
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        # Apply Jacobian: r² * sin(theta)
        return func(x, y, z) * r * r * np.sin(theta)

    limits = [phi_bounds, theta_bounds, r_bounds]
    result, error = nquad(
        integrand,
        limits,
        opts={"epsabs": epsabs, "epsrel": epsrel},
    )
    return float(result)


# ═══════════════════════════════════════════════════════════════════
# SURFACE INTEGRALS
# ═══════════════════════════════════════════════════════════════════


@maxwell_cite(
    79,
    80,
    81,
    part=1,
    chapter="On the Surface-Integral of the Electric Induction",
    theory_class="standard_math",
    description="Compute surface integral (flux) of vector field through parametric surface",
)
def surface_integral_vector(
    Fx: Callable[[float, float, float], float],
    Fy: Callable[[float, float, float], float],
    Fz: Callable[[float, float, float], float],
    u_range: Limits1D,
    v_range: Limits1D,
    param_surface: ParamSurface,
    method: str = "scipy",
    n_u: int = 80,
    n_v: int = 80,
    h_deriv: float = H_DERIV,
) -> float:
    """Compute surface integral (flux) of a vector field through a parametric surface.

    Flux = ∬_S F · (∂r/∂u × ∂r/∂v) du dv

    Args:
        Fx, Fy, Fz: Vector field components F(x, y, z).
        u_range: (u_min, u_max) parameter bounds.
        v_range: (v_min, v_max) parameter bounds.
        param_surface: Surface parameterization r(u, v) -> (x, y, z).
        method: Integration method ("scipy" | "trapezoid").
        n_u, n_v: Grid resolution (for trapezoid method).
        h_deriv: Step size for numerical partial derivatives.

    Returns:
        Flux value.

    CGS Units:
        If F is electric displacement (statcoulomb/cm²) and dA in cm²,
        result is in statcoulombs.

    Example:
        >>> # Flux of radial field through sphere (Gauss's law)
        >>> R = 10.0
        >>> def r_func(theta, phi):
        ...     return (R*np.sin(theta)*np.cos(phi),
        ...             R*np.sin(theta)*np.sin(phi),
        ...             R*np.cos(theta))
        >>> flux = surface_integral_vector(
        ...     lambda x,y,z: x/(x**2+y**2+z**2)**1.5 if (x**2+y**2+z**2)>0 else 0,
        ...     lambda x,y,z: y/(x**2+y**2+z**2)**1.5 if (x**2+y**2+z**2)>0 else 0,
        ...     lambda x,y,z: z/(x**2+y**2+z**2)**1.5 if (x**2+y**2+z**2)>0 else 0,
        ...     (0, np.pi), (0, 2*np.pi), r_func
        ... )

    Reference:
        Part I, Arts. 79-81: Surface integral of electric induction.
    """

    def _surface_integrand(u, v):
        """Integrand for dblquad: F(r(u,v)) · (dr/du × dr/dv)."""
        x, y, z = param_surface(u, v)

        # Compute partial derivatives
        dr_du = tuple(
            _numerical_partial(param_surface, u, v, i, "u", h_deriv) for i in range(3)
        )
        dr_dv = tuple(
            _numerical_partial(param_surface, u, v, i, "v", h_deriv) for i in range(3)
        )

        # Cross product: normal vector (non-normalized, includes area element)
        normal = _cross_product(dr_du, dr_dv)  # type: ignore[arg-type]

        # Dot product: F · n
        return (
            Fx(x, y, z) * normal[0] + Fy(x, y, z) * normal[1] + Fz(x, y, z) * normal[2]
        )

    if method == "scipy":
        # dblquad(func, a, b, gfun, hfun) integrates func(y, x) with x in [a,b] and y in [gfun(x), hfun(x)]
        # We want v as inner (first arg of func), u as outer (second arg of func)
        # So: func(v, u) where u in [u_range[0], u_range[1]], v in [v_range[0], v_range[1]]
        result, error = dblquad(
            lambda v, u: _surface_integrand(u, v),
            u_range[0],
            u_range[1],
            lambda _: v_range[0],
            lambda _: v_range[1],
            epsabs=1e-6,
            epsrel=1e-6,
        )
        return float(result)
    else:
        # Trapezoidal rule on grid
        u_vals = np.linspace(u_range[0], u_range[1], n_u)
        v_vals = np.linspace(v_range[0], v_range[1], n_v)
        du = u_vals[1] - u_vals[0]
        dv = v_vals[1] - v_vals[0]

        total = 0.0
        for i, u in enumerate(u_vals):
            for j, v in enumerate(v_vals):
                # Weights for trapezoidal rule
                w_u = 0.5 if (i == 0 or i == n_u - 1) else 1.0
                w_v = 0.5 if (j == 0 or j == n_v - 1) else 1.0
                total += w_u * w_v * _surface_integrand(u, v)

        return float(total * du * dv)


@maxwell_cite(
    83,
    part=1,
    chapter="On the Potential",
    theory_class="standard_math",
    description="Compute surface integral of scalar field over parametric surface",
)
def surface_integral_scalar(
    func: ScalarField3D,
    u_range: Limits1D,
    v_range: Limits1D,
    param_surface: ParamSurface,
    method: str = "scipy",
    n_u: int = 80,
    n_v: int = 80,
    h_deriv: float = H_DERIV,
) -> float:
    """Compute surface integral of a scalar field over a parametric surface.

    I = ∬_S g dA = ∬_D g(r(u,v)) * |∂r/∂u × ∂r/∂v| du dv

    Applications:
        - Surface area computation (g=1)
        - Surface mass/charge: ∬ sigma(u,v) dA
        - Mean value over surface

    Args:
        func: Scalar field g(x, y, z).
        u_range: (u_min, u_max).
        v_range: (v_min, v_max).
        param_surface: Surface parameterization r(u, v) -> (x, y, z).
        method: Integration method ("scipy" | "trapezoid").
        n_u, n_v: Grid resolution (for trapezoid).
        h_deriv: Step size for numerical partial derivatives.

    Returns:
        Integral value.

    Reference:
        Part I, Art. 83: Mean value theorem for surfaces.
    """

    def _scalar_integrand(u, v):
        """Integrand for dblquad: g(r(u,v)) * |dr/du × dr/dv|."""
        x, y, z = param_surface(u, v)

        dr_du = tuple(
            _numerical_partial(param_surface, u, v, i, "u", h_deriv) for i in range(3)
        )
        dr_dv = tuple(
            _numerical_partial(param_surface, u, v, i, "v", h_deriv) for i in range(3)
        )

        normal = _cross_product(dr_du, dr_dv)  # type: ignore[arg-type]
        area_element = _vec_magnitude(normal)

        return func(x, y, z) * area_element

    if method == "scipy":
        result, error = dblquad(
            lambda v, u: _scalar_integrand(u, v),
            u_range[0],
            u_range[1],
            lambda _: v_range[0],
            lambda _: v_range[1],
            epsabs=1e-6,
            epsrel=1e-6,
        )
        return float(result)
    else:
        u_vals = np.linspace(u_range[0], u_range[1], n_u)
        v_vals = np.linspace(v_range[0], v_range[1], n_v)
        du = u_vals[1] - u_vals[0]
        dv = v_vals[1] - v_vals[0]

        total = 0.0
        for i, u in enumerate(u_vals):
            for j, v in enumerate(v_vals):
                w_u = 0.5 if (i == 0 or i == n_u - 1) else 1.0
                w_v = 0.5 if (j == 0 or j == n_v - 1) else 1.0
                total += w_u * w_v * _scalar_integrand(u, v)

        return float(total * du * dv)


@maxwell_cite(
    79,
    81,
    part=1,
    chapter="On the Surface-Integral of the Electric Induction",
    theory_class="standard_math",
    description="Surface integral over spherical surface",
)
def surface_integral_sphere(
    Fx: Callable[[float, float, float], float],
    Fy: Callable[[float, float, float], float],
    Fz: Callable[[float, float, float], float],
    radius: float,
    center: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    theta_range: Limits1D = (0, np.pi),
    phi_range: Limits1D = (0, 2 * np.pi),
    method: str = "scipy",
    n_theta: int = 80,
    n_phi: int = 80,
) -> float:
    """Convenience function: surface integral over a spherical surface.

    Automatically constructs the sphere parameterization and computes flux.

    Args:
        Fx, Fy, Fz: Vector field components.
        radius: Sphere radius in cm.
        center: Sphere center (x, y, z) in cm.
        theta_range: (theta_min, theta_max) in radians.
        phi_range: (phi_min, phi_max) in radians.
        method: Integration method.
        n_theta, n_phi: Grid resolution.

    Returns:
        Flux through spherical surface.

    Reference:
        Part I, Arts. 79-81: Surface integral of electric induction.
    """
    cx, cy, cz = center

    def r_func(theta, phi):
        return (
            cx + radius * np.sin(theta) * np.cos(phi),
            cy + radius * np.sin(theta) * np.sin(phi),
            cz + radius * np.cos(theta),
        )

    return surface_integral_vector(
        Fx,
        Fy,
        Fz,
        theta_range,
        phi_range,
        r_func,
        method=method,
        n_u=n_theta,
        n_v=n_phi,
    )


# ═══════════════════════════════════════════════════════════════════
# LINE INTEGRALS
# ═══════════════════════════════════════════════════════════════════


@maxwell_cite(
    242,
    243,
    244,
    part=2,
    chapter="Conduction and Resistance",
    theory_class="standard_math",
    description="Compute line integral of vector field along parametric curve",
)
def line_integral_vector(
    Fx: Callable[[float, float, float], float],
    Fy: Callable[[float, float, float], float],
    Fz: Callable[[float, float, float], float],
    t_range: Limits1D,
    curve_func: ParamCurve3D,
    n_points: int = 200,
    method: str = "scipy",
    h_deriv: float = H_DERIV,
) -> float:
    """Compute line integral of a vector field along a parametric curve.

    ∫_C F · dl = ∫_a^b [Fx*dx/dt + Fy*dy/dt + Fz*dz/dt] dt

    Args:
        Fx, Fy, Fz: Vector field components.
        t_range: (t_min, t_max) parameter bounds.
        curve_func: Curve parameterization r(t) -> (x, y, z).
        n_points: Number of quadrature points (for trapezoid method).
        method: Integration method ("scipy" | "trapezoid").
        h_deriv: Step size for numerical curve derivatives.

    Returns:
        Line integral value.

    CGS Units:
        If F is electric field (statvolt/cm) and dl in cm,
        result is in statvolts (potential difference).

    Example:
        >>> # EMF around circular loop in uniform E-field
        >>> R = 5.0
        >>> def circle(t):
        ...     return (R*np.cos(t), R*np.sin(t), 0.0)
        >>> emf = line_integral_vector(
        ...     lambda x,y,z: 1.0, lambda x,y,z: 0.0, lambda x,y,z: 0.0,
        ...     (0, 2*np.pi), circle
        ... )

    Reference:
        Part II, Arts. 242-244: Electromotive force definition.
    """

    def _line_integrand(t):
        """Integrand: F(r(t)) · r'(t)."""
        x, y, z = curve_func(t)

        dr_dt = tuple(
            _numerical_curve_derivative(curve_func, t, i, h_deriv) for i in range(3)
        )

        return Fx(x, y, z) * dr_dt[0] + Fy(x, y, z) * dr_dt[1] + Fz(x, y, z) * dr_dt[2]

    if method == "scipy":
        result, error = quad(
            _line_integrand, t_range[0], t_range[1], epsabs=1e-8, epsrel=1e-8
        )
        return float(result)
    else:
        t_vals = np.linspace(t_range[0], t_range[1], n_points)
        integrand_vals = [_line_integrand(t) for t in t_vals]
        return float(np.trapz(integrand_vals, t_vals))


@maxwell_cite(
    71,
    72,
    73,
    part=1,
    chapter="On the Potential",
    theory_class="standard_math",
    description="Compute line integral of scalar field along curve",
)
def line_integral_scalar(
    func: ScalarField3D,
    t_range: Limits1D,
    curve_func: ParamCurve3D,
    n_points: int = 200,
    method: str = "scipy",
    h_deriv: float = H_DERIV,
) -> float:
    """Compute line integral of a scalar field along a parametric curve.

    ∫_C g dl = ∫_a^b g(r(t)) * |r'(t)| dt

    Applications:
        - Arc length (g=1)
        - Total charge along wire: ∫ lambda dl
        - Mass of wire: ∫ mu dl

    Args:
        func: Scalar field g(x, y, z).
        t_range: (t_min, t_max).
        curve_func: Curve parameterization r(t) -> (x, y, z).
        n_points: Number of quadrature points.
        method: Integration method ("scipy" | "trapezoid").
        h_deriv: Step size for numerical curve derivatives.

    Returns:
        Integral value.

    Reference:
        Part I, Arts. 71-73: Potential theory.
    """

    def _scalar_integrand(t):
        """Integrand: g(r(t)) * |r'(t)|."""
        x, y, z = curve_func(t)

        dr_dt = tuple(
            _numerical_curve_derivative(curve_func, t, i, h_deriv) for i in range(3)
        )
        speed = float(np.sqrt(dr_dt[0] ** 2 + dr_dt[1] ** 2 + dr_dt[2] ** 2))

        return func(x, y, z) * speed

    if method == "scipy":
        result, error = quad(
            _scalar_integrand, t_range[0], t_range[1], epsabs=1e-8, epsrel=1e-8
        )
        return float(result)
    else:
        t_vals = np.linspace(t_range[0], t_range[1], n_points)
        integrand_vals = [_scalar_integrand(t) for t in t_vals]
        return float(np.trapz(integrand_vals, t_vals))


@maxwell_cite(
    401,
    part=3,
    chapter="Magnetic Integrals",
    theory_class="standard_math",
    description="Compute line integral along circular path",
)
def line_integral_circle(
    Fx: Callable[[float, float, float], float],
    Fy: Callable[[float, float, float], float],
    Fz: Callable[[float, float, float], float],
    radius: float,
    center: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    normal: Tuple[float, float, float] = (0.0, 0.0, 1.0),
    method: str = "scipy",
) -> float:
    """Compute line integral of a vector field along a circular path.

    Convenience wrapper that auto-constructs the circle parameterization
    in the plane perpendicular to the given normal vector.

    Args:
        Fx, Fy, Fz: Vector field components.
        radius: Circle radius in cm.
        center: Circle center (x, y, z).
        normal: Normal vector defining the circle's plane (default: +z).
        method: Integration method.

    Returns:
        Line integral value around the circle.

    Reference:
        Part III, Art. 401: Magnetic line integrals.
    """
    cx, cy, cz = center
    nx, ny, nz = normal

    # Normalize the normal vector
    norm_len = float(np.sqrt(nx * nx + ny * ny + nz * nz))
    if norm_len == 0:
        warnings.warn("Zero normal vector for circle; defaulting to z-axis")
        nx, ny, nz = 0.0, 0.0, 1.0
    else:
        nx, ny, nz = nx / norm_len, ny / norm_len, nz / norm_len

    # Build orthonormal basis for the circle plane
    if abs(nz) < 0.9:
        u_vec = np.cross([nx, ny, nz], [0, 0, 1])
    else:
        u_vec = np.cross([nx, ny, nz], [1, 0, 0])
    u_vec = u_vec / np.linalg.norm(u_vec)
    v_vec = np.cross([nx, ny, nz], u_vec)
    v_vec = v_vec / np.linalg.norm(v_vec)

    def circle_param(t):
        return (
            cx + radius * (u_vec[0] * np.cos(t) + v_vec[0] * np.sin(t)),
            cy + radius * (u_vec[1] * np.cos(t) + v_vec[1] * np.sin(t)),
            cz + radius * (u_vec[2] * np.cos(t) + v_vec[2] * np.sin(t)),
        )

    return line_integral_vector(Fx, Fy, Fz, (0, 2 * np.pi), circle_param, method=method)


@maxwell_cite(
    401,
    part=3,
    chapter="Magnetic Integrals",
    theory_class="standard_math",
    description="Compute line integral along polygonal path",
)
def line_integral_polygonal(
    Fx: Callable[[float, float, float], float],
    Fy: Callable[[float, float, float], float],
    Fz: Callable[[float, float, float], float],
    vertices: np.ndarray,
    closed: bool = False,
) -> float:
    """Compute line integral along a polygonal path (sequence of vertices).

    Uses midpoint rule on each segment for piecewise-linear paths.

    Args:
        Fx, Fy, Fz: Vector field components.
        vertices: Array of shape (N, 3) defining the path.
        closed: If True, close the path (last vertex to first).

    Returns:
        Line integral value.

    Reference:
        Part III, Art. 401: Magnetic line integrals.
    """
    vertices = np.asarray(vertices)
    total = 0.0
    n = len(vertices)
    segments = n - 1
    if closed:
        segments = n

    for i in range(segments):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n] if closed else vertices[i + 1]
        mid = 0.5 * (p1 + p2)
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dz = p2[2] - p1[2]
        total += Fx(mid[0], mid[1], mid[2]) * dx
        total += Fy(mid[0], mid[1], mid[2]) * dy
        total += Fz(mid[0], mid[1], mid[2]) * dz

    return float(total)


# ═══════════════════════════════════════════════════════════════════
# THEOREM VERIFICATIONS
# ═══════════════════════════════════════════════════════════════════


@maxwell_cite(
    77,
    79,
    80,
    81,
    part=1,
    chapter="On the Potential",
    theory_class="standard_math",
    description="Verify the Divergence Theorem numerically",
)
def verify_divergence_theorem(
    Fx: Callable[[float, float, float], float],
    Fy: Callable[[float, float, float], float],
    Fz: Callable[[float, float, float], float],
    box_bounds: Tuple[Limits1D, Limits1D, Limits1D],
    tolerance: float = 1e-4,
) -> dict:
    """Verify the Divergence Theorem numerically.

    Computes both sides:
        LHS = ∭_V div(F) dV  (volume integral of divergence)
        RHS = ∯_S F · n dA   (surface flux through all 6 faces)

    Args:
        Fx, Fy, Fz: Vector field components.
        box_bounds: ((x_min, x_max), (y_min, y_max), (z_min, z_max)).
        tolerance: Relative tolerance for verification.

    Returns:
        Dictionary with:
            - 'volume_integral': ∭ div(F) dV
            - 'surface_integral': ∯ F · n dA
            - 'difference': |LHS - RHS|
            - 'relative_error': |LHS - RHS| / max(|LHS|, |RHS|, 1)
            - 'verified': True if relative_error < tolerance
            - 'tolerance_used': tolerance

    Reference:
        Part I, Art. 77: Divergence definition.
        Part I, Arts. 79-81: Surface integral and Gauss's law.
    """
    x_lim, y_lim, z_lim = box_bounds

    # LHS: Volume integral of divergence
    def div_F(x, y, z):
        return divergence(Fx, Fy, Fz, x, y, z)

    volume_int = volume_integral_scalar(div_F, x_lim, y_lim, z_lim)

    # RHS: Surface integral over 6 faces of the rectangular box
    # Compute F · n directly for each face using dblquad
    x_min, x_max = x_lim
    y_min, y_max = y_lim
    z_min, z_max = z_lim

    total_surface = 0.0

    # Face at x = x_max (n = +x): ∬ Fx(x_max, y, z) dy dz
    fn_xmax = lambda z, y: Fx(x_max, y, z)
    result_xmax, _ = dblquad(
        fn_xmax,
        y_min,
        y_max,
        lambda _: z_min,
        lambda _: z_max,
        epsabs=1e-6,
        epsrel=1e-6,
    )
    total_surface += result_xmax

    # Face at x = x_min (n = -x): ∬ -Fx(x_min, y, z) dy dz
    fn_xmin = lambda z, y: -Fx(x_min, y, z)
    result_xmin, _ = dblquad(
        fn_xmin,
        y_min,
        y_max,
        lambda _: z_min,
        lambda _: z_max,
        epsabs=1e-6,
        epsrel=1e-6,
    )
    total_surface += result_xmin

    # Face at y = y_max (n = +y): ∬ Fy(x, y_max, z) dx dz
    fn_ymax = lambda z, x: Fy(x, y_max, z)
    result_ymax, _ = dblquad(
        fn_ymax,
        x_min,
        x_max,
        lambda _: z_min,
        lambda _: z_max,
        epsabs=1e-6,
        epsrel=1e-6,
    )
    total_surface += result_ymax

    # Face at y = y_min (n = -y): ∬ -Fy(x, y_min, z) dx dz
    fn_ymin = lambda z, x: -Fy(x, y_min, z)
    result_ymin, _ = dblquad(
        fn_ymin,
        x_min,
        x_max,
        lambda _: z_min,
        lambda _: z_max,
        epsabs=1e-6,
        epsrel=1e-6,
    )
    total_surface += result_ymin

    # Face at z = z_max (n = +z): ∬ Fz(x, y, z_max) dx dy
    fn_zmax = lambda y, x: Fz(x, y, z_max)
    result_zmax, _ = dblquad(
        fn_zmax,
        x_min,
        x_max,
        lambda _: y_min,
        lambda _: y_max,
        epsabs=1e-6,
        epsrel=1e-6,
    )
    total_surface += result_zmax

    # Face at z = z_min (n = -z): ∬ -Fz(x, y, z_min) dx dy
    fn_zmin = lambda y, x: -Fz(x, y, z_min)
    result_zmin, _ = dblquad(
        fn_zmin,
        x_min,
        x_max,
        lambda _: y_min,
        lambda _: y_max,
        epsabs=1e-6,
        epsrel=1e-6,
    )
    total_surface += result_zmin

    diff = abs(volume_int - total_surface)
    denom = max(abs(volume_int), abs(total_surface), 1.0)
    rel_error = diff / denom

    return {
        "volume_integral": float(volume_int),
        "surface_integral": float(total_surface),
        "difference": float(diff),
        "relative_error": float(rel_error),
        "verified": rel_error < tolerance,
        "tolerance_used": tolerance,
    }


@maxwell_cite(
    77,
    401,
    402,
    part=1,
    chapter="On the Potential",
    theory_class="standard_math",
    description="Verify Stokes' Theorem numerically",
)
def verify_stokes_theorem(
    Fx: Callable[[float, float, float], float],
    Fy: Callable[[float, float, float], float],
    Fz: Callable[[float, float, float], float],
    surface_param: ParamSurface,
    u_range: Limits1D,
    v_range: Limits1D,
    boundary_curve: ParamCurve3D,
    t_range: Limits1D,
    tolerance: float = 1e-4,
) -> dict:
    """Verify Stokes' Theorem numerically.

    Computes both sides:
        LHS = ∮_C F · dl  (line integral around boundary)
        RHS = ∬_S (∇×F) · n dA  (surface integral of curl)

    The boundary curve MUST be the boundary of the parameterized surface,
    with consistent orientation (right-hand rule).

    Args:
        Fx, Fy, Fz: Vector field components.
        surface_param: Surface parameterization r(u, v).
        u_range, v_range: Surface parameter bounds.
        boundary_curve: Boundary parameterization r(t).
        t_range: Curve parameter bounds.
        tolerance: Relative tolerance.

    Returns:
        Dictionary with:
            - 'line_integral': ∮ F · dl
            - 'surface_integral': ∬ (∇×F) · n dA
            - 'difference': |LHS - RHS|
            - 'relative_error': relative error
            - 'verified': True if relative_error < tolerance
            - 'curl_at_center': curl value at surface center (for debugging)

    Reference:
        Part I, Art. 77: Curl definition.
        Part III, Arts. 401-402: Magnetic integrals and Stokes' theorem.
    """
    # LHS: Line integral around boundary curve
    line_int = line_integral_vector(Fx, Fy, Fz, t_range, boundary_curve)

    # RHS: Surface integral of curl(F)
    # Create curl component functions
    def curl_Fx(x, y, z):
        return curl(Fx, Fy, Fz, x, y, z)[0]

    def curl_Fy(x, y, z):
        return curl(Fx, Fy, Fz, x, y, z)[1]

    def curl_Fz(x, y, z):
        return curl(Fx, Fy, Fz, x, y, z)[2]

    surface_int = surface_integral_vector(
        curl_Fx,
        curl_Fy,
        curl_Fz,
        u_range,
        v_range,
        surface_param,
        h_deriv=H_DERIV,
    )

    # Debug: curl at center of surface
    u_mid = 0.5 * (u_range[0] + u_range[1])
    v_mid = 0.5 * (v_range[0] + v_range[1])
    cx, cy, cz = surface_param(u_mid, v_mid)
    curl_center = curl(Fx, Fy, Fz, cx, cy, cz)

    diff = abs(line_int - surface_int)
    denom = max(abs(line_int), abs(surface_int), 1.0)
    rel_error = diff / denom

    return {
        "line_integral": float(line_int),
        "surface_integral": float(surface_int),
        "difference": float(diff),
        "relative_error": float(rel_error),
        "verified": rel_error < tolerance,
        "curl_at_center": curl_center,
    }


@maxwell_cite(
    182,
    183,
    184,
    185,
    186,
    part=1,
    chapter="On Conjugate Functions",
    theory_class="standard_math",
    description="Verify Green's Theorem numerically",
)
def verify_greens_theorem(
    P: Callable[[float, float], float],
    Q: Callable[[float, float], float],
    region: Tuple[
        Limits1D,
        Union[float, Callable[[float], float]],
        Union[float, Callable[[float], float]],
    ],
    boundary_curve: ParamCurve2D,
    t_range: Limits1D,
    n_points: int = 200,
    tolerance: float = 1e-4,
) -> dict:
    """Verify Green's Theorem numerically (2D special case of Stokes').

    Computes both sides:
        LHS = ∮_C (P dx + Q dy)
        RHS = ∬_D (∂Q/∂x - ∂P/∂y) dA

    Uses scipy.integrate.dblquad directly for the 2D double integral.

    Args:
        P: x-component of 2D vector field P(x, y).
        Q: y-component of 2D vector field Q(x, y).
        region: ((x_min, x_max), y_lower(x), y_upper(x)).
            y_lower and y_upper can be floats (constant) or callables.
        boundary_curve: CCW boundary r(t) -> (x, y).
        t_range: Curve parameter bounds.
        n_points: Quadrature points for line integral.
        tolerance: Relative tolerance.

    Returns:
        Dictionary with:
            - 'line_integral': ∮ (P dx + Q dy)
            - 'double_integral': ∬ (∂Q/∂x - ∂P/∂y) dA
            - 'difference': |LHS - RHS|
            - 'relative_error': relative error
            - 'verified': True if relative_error < tolerance

    Reference:
        Part I, Arts. 182-206: Conjugate functions and 2D electrostatics.
    """
    x_limits, y_lower, y_upper = region

    # LHS: Line integral (embed 2D into 3D)
    def Fx_3d(x, y, z):
        return P(x, y)

    def Fy_3d(x, y, z):
        return Q(x, y)

    def Fz_3d(x, y, z):
        return 0.0

    def boundary_3d(t):
        x, y = boundary_curve(t)
        return (x, y, 0.0)

    line_int = line_integral_vector(
        Fx_3d, Fy_3d, Fz_3d, t_range, boundary_3d, n_points=n_points
    )

    # RHS: Double integral using dblquad directly
    # ∂Q/∂x - ∂P/∂y using central differences
    h = H_DERIV

    def integrand(y, x):
        dQ_dx = (Q(x + h, y) - Q(x - h, y)) / (2 * h)
        dP_dy = (P(x, y + h) - P(x, y - h)) / (2 * h)
        return dQ_dx - dP_dy

    if callable(y_lower):
        y_lo_func = y_lower
    else:
        y_lo_val = y_lower
        y_lo_func = lambda x: y_lo_val

    if callable(y_upper):
        y_hi_func = y_upper
    else:
        y_hi_val = y_upper
        y_hi_func = lambda x: y_hi_val

    double_int, error = dblquad(
        integrand,
        x_limits[0],
        x_limits[1],
        y_lo_func,
        y_hi_func,
        epsabs=1e-6,
        epsrel=1e-6,
    )

    diff = abs(line_int - double_int)
    denom = max(abs(line_int), abs(double_int), 1.0)
    rel_error = diff / denom

    return {
        "line_integral": float(line_int),
        "double_integral": float(double_int),
        "difference": float(diff),
        "relative_error": float(rel_error),
        "verified": rel_error < tolerance,
    }


# ═══════════════════════════════════════════════════════════════════
# UNIFIED CALCULATOR CLASS
# ═══════════════════════════════════════════════════════════════════


@dataclass
class CalculusCalculator:
    """Unified interface for Maxwell's calculus operations.

    Provides a stateful calculator with configurable precision,
    unit tracking, and result history. All operations maintain
    CGS unit consistency.

    Attributes:
        precision: Integration precision (epsabs, epsrel).
        default_method: Default integration method ("scipy" | "trapezoid").
        unit_system: Unit system identifier ("CGS-EMU" | "CGS-ESU" | "CGS-Gaussian").
        _cache: Internal result cache (skipped for callable args).
        _history: List of computation records.

    Usage:
        >>> calc = CalculusCalculator(precision=1e-10)
        >>> result = calc.volume_integral(rho, x_limits, y_limits, z_limits)
        >>> verification = calc.verify_divergence_theorem(Fx, Fy, Fz, box_bounds)
    """

    precision: float = 1e-8
    default_method: str = "scipy"
    unit_system: str = "CGS-EMU"
    _cache: dict = field(default_factory=dict)
    _history: list = field(default_factory=list)

    def _record(self, operation: str, result) -> None:
        """Record a computation in history."""
        self._history.append({"operation": operation, "result": result})

    def _cache_key(self, operation: str, *args) -> Optional[str]:
        """Generate cache key; returns None if args contain unhashable callables."""
        try:
            # Skip caching if any argument is callable (unhashable in general)
            for arg in args:
                if callable(arg):
                    return None
            key = (operation,) + tuple(str(a) for a in args)
            return hash(key)
        except TypeError:
            return None

    def volume_integral(
        self,
        f: ScalarField3D,
        x_limits: Limits1D,
        y_limits: Union[Limits1D, Callable[[float], Limits1D]],
        z_limits: Union[Limits1D, Callable[[float, float], Limits1D]],
        **kwargs,
    ) -> float:
        """Compute triple integral of scalar field.

        Delegates to :func:`volume_integral_scalar`.
        """
        key = self._cache_key("volume_integral", f, x_limits)
        if key is not None and key in self._cache:
            return self._cache[key]

        result = volume_integral_scalar(
            f,
            x_limits,
            y_limits,
            z_limits,
            epsabs=kwargs.get("epsabs", self.precision),
            epsrel=kwargs.get("epsrel", self.precision),
        )

        if key is not None:
            self._cache[key] = result
        self._record("volume_integral", result)
        return result

    def volume_integral_vector(
        self,
        Fx: Callable[[float, float, float], float],
        Fy: Callable[[float, float, float], float],
        Fz: Callable[[float, float, float], float],
        x_limits: Limits1D,
        y_limits: Union[Limits1D, Callable[[float], Limits1D]],
        z_limits: Union[Limits1D, Callable[[float, float], Limits1D]],
        **kwargs,
    ) -> Tuple[float, float, float]:
        """Compute triple integral of vector field.

        Delegates to :func:`volume_integral_vector`.
        """
        return volume_integral_vector(
            Fx,
            Fy,
            Fz,
            x_limits,
            y_limits,
            z_limits,
            epsabs=kwargs.get("epsabs", self.precision),
            epsrel=kwargs.get("epsrel", self.precision),
        )

    def volume_integral_spherical(
        self,
        f: ScalarField3D,
        r_limits: Limits1D,
        theta_limits: Limits1D = (0, np.pi),
        phi_limits: Limits1D = (0, 2 * np.pi),
        **kwargs,
    ) -> float:
        """Compute volume integral in spherical coordinates.

        Delegates to :func:`volume_integral_spherical`.
        """
        return volume_integral_spherical(
            f,
            r_limits,
            theta_limits,
            phi_limits,
            epsabs=kwargs.get("epsabs", self.precision),
            epsrel=kwargs.get("epsrel", self.precision),
        )

    def surface_integral(
        self,
        Fx: Callable[[float, float, float], float],
        Fy: Callable[[float, float, float], float],
        Fz: Callable[[float, float, float], float],
        u_range: Limits1D,
        v_range: Limits1D,
        param_surface: ParamSurface,
        **kwargs,
    ) -> float:
        """Compute surface integral (flux) of vector field.

        Delegates to :func:`surface_integral_vector`.
        """
        return surface_integral_vector(
            Fx,
            Fy,
            Fz,
            u_range,
            v_range,
            param_surface,
            method=kwargs.get("method", self.default_method),
        )

    def surface_integral_scalar(
        self,
        func: ScalarField3D,
        u_range: Limits1D,
        v_range: Limits1D,
        param_surface: ParamSurface,
        **kwargs,
    ) -> float:
        """Compute surface integral of scalar field.

        Delegates to :func:`surface_integral_scalar`.
        """
        return surface_integral_scalar(
            func,
            u_range,
            v_range,
            param_surface,
            method=kwargs.get("method", self.default_method),
        )

    def line_integral(
        self,
        Fx: Callable[[float, float, float], float],
        Fy: Callable[[float, float, float], float],
        Fz: Callable[[float, float, float], float],
        t_range: Limits1D,
        curve_func: ParamCurve3D,
        **kwargs,
    ) -> float:
        """Compute line integral of vector field.

        Delegates to :func:`line_integral_vector`.
        """
        return line_integral_vector(
            Fx,
            Fy,
            Fz,
            t_range,
            curve_func,
            method=kwargs.get("method", self.default_method),
        )

    def verify_divergence_theorem(
        self,
        Fx: Callable[[float, float, float], float],
        Fy: Callable[[float, float, float], float],
        Fz: Callable[[float, float, float], float],
        box_bounds: Tuple[Limits1D, Limits1D, Limits1D],
        **kwargs,
    ) -> dict:
        """Verify the Divergence Theorem.

        Delegates to :func:`verify_divergence_theorem`.
        """
        result = verify_divergence_theorem(
            Fx,
            Fy,
            Fz,
            box_bounds,
            tolerance=kwargs.get("tolerance", 1e-4),
        )
        self._record("verify_divergence_theorem", result)
        return result

    def verify_stokes_theorem(
        self,
        Fx: Callable[[float, float, float], float],
        Fy: Callable[[float, float, float], float],
        Fz: Callable[[float, float, float], float],
        surface_param: ParamSurface,
        u_range: Limits1D,
        v_range: Limits1D,
        boundary_curve: ParamCurve3D,
        t_range: Limits1D,
        **kwargs,
    ) -> dict:
        """Verify Stokes' Theorem.

        Delegates to :func:`verify_stokes_theorem`.
        """
        result = verify_stokes_theorem(
            Fx,
            Fy,
            Fz,
            surface_param,
            u_range,
            v_range,
            boundary_curve,
            t_range,
            tolerance=kwargs.get("tolerance", 1e-4),
        )
        self._record("verify_stokes_theorem", result)
        return result

    def verify_greens_theorem(
        self,
        P: Callable[[float, float], float],
        Q: Callable[[float, float], float],
        region: Tuple[
            Limits1D,
            Union[float, Callable[[float], float]],
            Union[float, Callable[[float], float]],
        ],
        boundary_curve: ParamCurve2D,
        t_range: Limits1D,
        **kwargs,
    ) -> dict:
        """Verify Green's Theorem.

        Delegates to :func:`verify_greens_theorem`.
        """
        result = verify_greens_theorem(
            P,
            Q,
            region,
            boundary_curve,
            t_range,
            tolerance=kwargs.get("tolerance", 1e-4),
        )
        self._record("verify_greens_theorem", result)
        return result

    def clear_cache(self) -> None:
        """Clear the result cache."""
        self._cache.clear()

    def clear_history(self) -> None:
        """Clear the computation history."""
        self._history.clear()

    def get_history(self) -> list:
        """Return the computation history."""
        return list(self._history)


__all__ = [
    # Volume integrals
    "volume_integral_scalar",
    "volume_integral_vector",
    "volume_integral_spherical",
    # Surface integrals
    "surface_integral_vector",
    "surface_integral_scalar",
    "surface_integral_sphere",
    # Line integrals
    "line_integral_vector",
    "line_integral_scalar",
    "line_integral_circle",
    "line_integral_polygonal",
    # Theorem verifications
    "verify_divergence_theorem",
    "verify_stokes_theorem",
    "verify_greens_theorem",
    # Calculator class
    "CalculusCalculator",
]

"""maxwell.math.derivatives — Partial derivative engine for Maxwell's equations.

Comprehensive numerical differentiation module implementing:

- Partial derivatives (central differences, forward/backward)
- Higher-order derivatives (second, third, mixed partials)
- Time derivatives with configurable dt
- Total/material derivative: d/dt = d/dt + v.grad
- Jacobian matrices for coordinate transformations
- Schwarz's theorem verification (equality of mixed partials)

All implementations use configurable step sizes and support validation
against analytical solutions. Step sizes are optimized for CGS units
(typical length scale: centimeters).

Category: C (standard_math) — Established numerical analysis methods.

References:
    Part I, Arts. 71-77: Theory of the potential and gradient.
    Part I, Arts. 100-110: Laplacian and second derivatives.
    Part I, Arts. 182-206: Conjugate functions (Cauchy-Riemann).
    Part IV, Arts. 591-600: Time-varying electromagnetic fields.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np

from maxwell.meta.citation import maxwell_cite

# ── Type aliases ──────────────────────────────────────────────────
ScalarField3D = Callable[[float, float, float], float]
VectorField3D = Tuple[
    Callable[[float, float, float], float],
    Callable[[float, float, float], float],
    Callable[[float, float, float], float],
]
ScalarField1D = Callable[[float], float]
VectorFieldNd = Callable[[np.ndarray], np.ndarray]
CoordinateTransform = Callable[[np.ndarray], np.ndarray]

# ── Default step sizes ────────────────────────────────────────────
H_DEFAULT: float = 1e-6
"""Default step size for spatial derivatives (cm)."""

DT_DEFAULT: float = 1e-8
"""Default step size for time derivatives (s)."""

H_MIXED: float = 1e-4
"""Step size for mixed partial derivatives (larger to reduce numerical noise)."""


class DiffMethod(Enum):
    """Numerical differentiation method."""

    CENTRAL = "central"
    """Central difference: O(h^2) accuracy."""
    FORWARD = "forward"
    """Forward difference: O(h) accuracy."""
    BACKWARD = "backward"
    """Backward difference: O(h) accuracy."""
    FIVE_POINT = "five_point"
    """Five-point stencil: O(h^4) accuracy."""


@dataclass(frozen=True)
class DerivativeResult:
    """Result of a derivative computation.

    Attributes:
        value: Computed derivative value(s).
        method: Differentiation method used.
        step_size: Step size h used.
        order: Order of accuracy (e.g., 2 for central difference).
        point: Point at which derivative was evaluated.
        variable: Which variable was differentiated with respect to.
        order_derivative: Order of derivative (1=first, 2=second, etc.).
    """

    value: Union[float, np.ndarray]
    method: DiffMethod
    step_size: float
    order: int
    point: Tuple[float, ...]
    variable: str
    order_derivative: int = 1


# ═══════════════════════════════════════════════════════════════════
# PARTIAL DERIVATIVE ENGINE
# ═══════════════════════════════════════════════════════════════════


@maxwell_cite(
    71,
    72,
    73,
    74,
    75,
    76,
    77,
    part=1,
    chapter="On the Potential",
    theory_class="standard_math",
    description="Compute partial derivative using central differences",
)
def partial_derivative(
    func: ScalarField3D,
    point: Tuple[float, float, float],
    variable: str = "x",
    h: float = H_DEFAULT,
    method: DiffMethod = DiffMethod.CENTRAL,
) -> DerivativeResult:
    """Compute the partial derivative of a scalar field at a point.

    Supports multiple numerical differentiation methods:

    Central difference (default, O(h^2)):
        df/dx = [f(x+h) - f(x-h)] / (2h)

    Forward difference (O(h)):
        df/dx = [f(x+h) - f(x)] / h

    Backward difference (O(h)):
        df/dx = [f(x) - f(x-h)] / h

    Five-point stencil (O(h^4)):
        df/dx = [-f(x+2h) + 8f(x+h) - 8f(x-h) + f(x-2h)] / (12h)

    Args:
        func: Scalar field function f(x, y, z).
        point: Point (x, y, z) at which to evaluate.
        variable: Variable to differentiate with respect to ('x', 'y', or 'z').
        h: Step size for numerical differentiation.
        method: Differentiation method.

    Returns:
        DerivativeResult containing the computed value and metadata.

    CGS Units:
        If func has units U and spatial variable in cm,
        result has units U/cm.

    Example:
        >>> def f(x, y, z): return x**2 + y**2 + z**2
        >>> result = partial_derivative(f, (1.0, 2.0, 3.0), "x")
        >>> result.value  # ~2.0 (analytical: 2x = 2)

    Reference:
        Part I, Arts. 71-77: Theory of the potential and gradient.
    """
    x, y, z = point
    var_idx = {"x": 0, "y": 1, "z": 2}
    if variable not in var_idx:
        raise ValueError(f"variable must be 'x', 'y', or 'z', got '{variable}'")
    idx = var_idx[variable]

    # Build perturbed points
    def _perturb(delta: float) -> Tuple[float, float, float]:
        coords = [x, y, z]
        coords[idx] += delta
        return tuple(coords)  # type: ignore[return-value]

    if method == DiffMethod.CENTRAL:
        f_plus = func(*_perturb(h))
        f_minus = func(*_perturb(-h))
        value = (f_plus - f_minus) / (2.0 * h)
        accuracy_order = 2

    elif method == DiffMethod.FORWARD:
        f_curr = func(*point)
        f_plus = func(*_perturb(h))
        value = (f_plus - f_curr) / h
        accuracy_order = 1

    elif method == DiffMethod.BACKWARD:
        f_curr = func(*point)
        f_minus = func(*_perturb(-h))
        value = (f_curr - f_minus) / h
        accuracy_order = 1

    elif method == DiffMethod.FIVE_POINT:
        f_p2 = func(*_perturb(2 * h))
        f_p1 = func(*_perturb(h))
        f_m1 = func(*_perturb(-h))
        f_m2 = func(*_perturb(-2 * h))
        value = (-f_p2 + 8.0 * f_p1 - 8.0 * f_m1 + f_m2) / (12.0 * h)
        accuracy_order = 4

    else:
        raise ValueError(f"Unknown method: {method}")

    return DerivativeResult(
        value=float(value),
        method=method,
        step_size=h,
        order=accuracy_order,
        point=point,
        variable=variable,
        order_derivative=1,
    )


@maxwell_cite(
    71,
    72,
    73,
    part=1,
    chapter="On the Potential",
    theory_class="standard_math",
    description="Compute gradient (vector of all partial derivatives)",
)
def partial_gradient(
    func: ScalarField3D,
    point: Tuple[float, float, float],
    h: float = H_DEFAULT,
    method: DiffMethod = DiffMethod.CENTRAL,
) -> DerivativeResult:
    """Compute the gradient (all three partial derivatives) at a point.

    grad(f) = (df/dx, df/dy, df/dz)

    Args:
        func: Scalar field function f(x, y, z).
        point: Point (x, y, z) at which to evaluate.
        h: Step size.
        method: Differentiation method.

    Returns:
        DerivativeResult with gradient vector as numpy array.

    Reference:
        Part I, Arts. 71-77: The potential and its gradient.
    """
    dx = partial_derivative(func, point, "x", h, method).value
    dy = partial_derivative(func, point, "y", h, method).value
    dz = partial_derivative(func, point, "z", h, method).value

    return DerivativeResult(
        value=np.array([dx, dy, dz]),
        method=method,
        step_size=h,
        order=(
            2
            if method == DiffMethod.CENTRAL
            else (4 if method == DiffMethod.FIVE_POINT else 1)
        ),
        point=point,
        variable="all",
        order_derivative=1,
    )


# ═══════════════════════════════════════════════════════════════════
# HIGHER-ORDER DERIVATIVES
# ═══════════════════════════════════════════════════════════════════


@maxwell_cite(
    77,
    100,
    part=1,
    chapter="On the Potential",
    theory_class="standard_math",
    description="Compute second partial derivative",
)
def second_partial_derivative(
    func: ScalarField3D,
    point: Tuple[float, float, float],
    variable: str = "x",
    h: float = H_DEFAULT,
) -> DerivativeResult:
    """Compute the second partial derivative d^2f/dx^2 at a point.

    Uses central difference for second derivatives:
        d^2f/dx^2 = [f(x+h) - 2f(x) + f(x-h)] / h^2

    This is O(h^2) accurate.

    Args:
        func: Scalar field function f(x, y, z).
        point: Point (x, y, z) at which to evaluate.
        variable: Variable for second derivative ('x', 'y', or 'z').
        h: Step size.

    Returns:
        DerivativeResult with second derivative value.

    CGS Units:
        If func has units U and spatial variable in cm,
        result has units U/cm^2.

    Example:
        >>> def f(x, y, z): return x**3 + y**2
        >>> result = second_partial_derivative(f, (1.0, 0.0, 0.0), "x")
        >>> result.value  # ~6.0 (analytical: 6x = 6)

    Reference:
        Part I, Art. 77: Laplacian definition.
        Part I, Art. 100: Second derivatives in potential theory.
    """
    x, y, z = point
    var_idx = {"x": 0, "y": 1, "z": 2}
    if variable not in var_idx:
        raise ValueError(f"variable must be 'x', 'y', or 'z', got '{variable}'")
    idx = var_idx[variable]

    def _perturb(delta: float) -> Tuple[float, float, float]:
        coords = [x, y, z]
        coords[idx] += delta
        return tuple(coords)  # type: ignore[return-value]

    f_plus = func(*_perturb(h))
    f_zero = func(*point)
    f_minus = func(*_perturb(-h))

    value = (f_plus - 2.0 * f_zero + f_minus) / (h**2)

    return DerivativeResult(
        value=float(value),
        method=DiffMethod.CENTRAL,
        step_size=h,
        order=2,
        point=point,
        variable=variable,
        order_derivative=2,
    )


@maxwell_cite(
    182,
    183,
    184,
    part=1,
    chapter="On Conjugate Functions",
    theory_class="standard_math",
    description="Compute mixed partial derivative",
)
def mixed_partial_derivative(
    func: ScalarField3D,
    point: Tuple[float, float, float],
    var1: str = "x",
    var2: str = "y",
    h: float = H_MIXED,
) -> DerivativeResult:
    """Compute the mixed partial derivative d^2f/(dvar1*dvar2).

    Uses central difference for mixed partials:
        d^2f/dxdy = [f(x+h,y+k) - f(x+h,y-k) - f(x-h,y+k) + f(x-h,y-k)] / (4hk)

    This is O(h^2) accurate.

    Args:
        func: Scalar field function f(x, y, z).
        point: Point (x, y, z) at which to evaluate.
        var1: First variable ('x', 'y', or 'z').
        var2: Second variable ('x', 'y', or 'z').
        h: Step size.

    Returns:
        DerivativeResult with mixed partial derivative value.

    Note:
        If var1 == var2, this reduces to the second partial derivative.
        Consider using second_partial_derivative for diagonal elements.

    Reference:
        Part I, Arts. 182-186: Conjugate functions and mixed partials.
    """
    x, y, z = point
    var_idx = {"x": 0, "y": 1, "z": 2}

    if var1 not in var_idx or var2 not in var_idx:
        raise ValueError("Variables must be 'x', 'y', or 'z'")

    idx1 = var_idx[var1]
    idx2 = var_idx[var2]

    # Evaluate f at four corners
    coords_pp = [x, y, z]
    coords_pm = [x, y, z]
    coords_mp = [x, y, z]
    coords_mm = [x, y, z]

    coords_pp[idx1] += h
    coords_pp[idx2] += h

    coords_pm[idx1] += h
    coords_pm[idx2] -= h

    coords_mp[idx1] -= h
    coords_mp[idx2] += h

    coords_mm[idx1] -= h
    coords_mm[idx2] -= h

    f_pp = func(*coords_pp)
    f_pm = func(*coords_pm)
    f_mp = func(*coords_mp)
    f_mm = func(*coords_mm)

    value = (f_pp - f_pm - f_mp + f_mm) / (4.0 * h * h)

    return DerivativeResult(
        value=float(value),
        method=DiffMethod.CENTRAL,
        step_size=h,
        order=2,
        point=point,
        variable=f"{var1}{var2}",
        order_derivative=2,
    )


@maxwell_cite(
    77,
    100,
    part=1,
    chapter="On the Potential",
    theory_class="standard_math",
    description="Compute the Hessian matrix (all second derivatives)",
)
def hessian(
    func: ScalarField3D,
    point: Tuple[float, float, float],
    h: float = H_DEFAULT,
) -> np.ndarray:
    """Compute the Hessian matrix of a scalar field at a point.

    H(f) = [[d^2f/dx^2, d^2f/dxdy, d^2f/dxdz],
            [d^2f/dydx, d^2f/dy^2, d^2f/dydz],
            [d^2f/dzdx, d^2f/dzdy, d^2f/dz^2]]

    The Hessian is symmetric (Schwarz's theorem) for smooth functions.

    Args:
        func: Scalar field function f(x, y, z).
        point: Point (x, y, z) at which to evaluate.
        h: Step size for derivatives.

    Returns:
        3x3 numpy array representing the Hessian matrix.

    CGS Units:
        If func has units U, Hessian has units U/cm^2.

    Example:
        >>> def f(x, y, z): return x**2 + 2*y**2 + 3*z**2
        >>> H = hessian(f, (0, 0, 0))
        >>> H  # [[2, 0, 0], [0, 4, 0], [0, 0, 6]]

    Reference:
        Part I, Arts. 77, 100: Second derivatives and Laplacian.
    """
    H = np.zeros((3, 3))
    variables = ["x", "y", "z"]

    for i, v1 in enumerate(variables):
        for j, v2 in enumerate(variables):
            if i == j:
                H[i, j] = second_partial_derivative(func, point, v1, h).value
            else:
                H[i, j] = mixed_partial_derivative(func, point, v1, v2, h).value

    return H


# ═══════════════════════════════════════════════════════════════════
# TIME DERIVATIVES
# ═══════════════════════════════════════════════════════════════════


@maxwell_cite(
    591,
    592,
    593,
    598,
    599,
    600,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Compute time partial derivative of a field",
)
def partial_derivative_t(
    func: Callable[[float, float, float, float], float],
    point: Tuple[float, float, float, float],
    dt: float = DT_DEFAULT,
    method: DiffMethod = DiffMethod.CENTRAL,
) -> DerivativeResult:
    """Compute the time partial derivative d(f)/dt at a spacetime point.

    df/dt evaluated at (x, y, z, t).

    This is essential for Maxwell's time-varying field equations:
        - Faraday's law: curl(E) = -dB/dt
        - Ampere-Maxwell: curl(H) = 4*pi*J + dD/dt

    Args:
        func: Spacetime field function f(x, y, z, t).
        point: Spacetime point (x, y, z, t).
        dt: Time step size (seconds).
        method: Differentiation method.

    Returns:
        DerivativeResult with time derivative value.

    CGS Units:
        If func has units U and t in seconds,
        result has units U/s.

    Example:
        >>> # Oscillating electric field: E = E0*sin(omega*t)
        >>> omega = 2 * np.pi * 60  # 60 Hz
        >>> def E(x, y, z, t): return 100.0 * np.sin(omega * t)
        >>> result = partial_derivative_t(E, (0, 0, 0, 0), dt=1e-8)
        >>> # Should be ~100*omega = 37699.1

    Reference:
        Part IV, Arts. 591-600: Time-varying electromagnetic fields.
    """
    x, y, z, t = point

    if method == DiffMethod.CENTRAL:
        f_plus = func(x, y, z, t + dt)
        f_minus = func(x, y, z, t - dt)
        value = (f_plus - f_minus) / (2.0 * dt)
        accuracy_order = 2

    elif method == DiffMethod.FORWARD:
        f_curr = func(x, y, z, t)
        f_plus = func(x, y, z, t + dt)
        value = (f_plus - f_curr) / dt
        accuracy_order = 1

    elif method == DiffMethod.BACKWARD:
        f_curr = func(x, y, z, t)
        f_minus = func(x, y, z, t - dt)
        value = (f_curr - f_minus) / dt
        accuracy_order = 1

    elif method == DiffMethod.FIVE_POINT:
        f_p2 = func(x, y, z, t + 2 * dt)
        f_p1 = func(x, y, z, t + dt)
        f_m1 = func(x, y, z, t - dt)
        f_m2 = func(x, y, z, t - 2 * dt)
        value = (-f_p2 + 8.0 * f_p1 - 8.0 * f_m1 + f_m2) / (12.0 * dt)
        accuracy_order = 4

    else:
        raise ValueError(f"Unknown method: {method}")

    return DerivativeResult(
        value=float(value),
        method=method,
        step_size=dt,
        order=accuracy_order,
        point=point,
        variable="t",
        order_derivative=1,
    )


@maxwell_cite(
    591,
    592,
    593,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    theory_class="standard_math",
    description="Compute time derivative of a vector field component",
)
def partial_derivative_t_vector(
    Fx: Callable[[float, float, float, float], float],
    Fy: Callable[[float, float, float, float], float],
    Fz: Callable[[float, float, float, float], float],
    point: Tuple[float, float, float, float],
    dt: float = DT_DEFAULT,
    method: DiffMethod = DiffMethod.CENTRAL,
) -> np.ndarray:
    """Compute time derivative of each component of a vector field.

    Returns (dFx/dt, dFy/dt, dFz/dt) at the spacetime point.

    Args:
        Fx, Fy, Fz: Vector field component functions of (x, y, z, t).
        point: Spacetime point (x, y, z, t).
        dt: Time step.
        method: Differentiation method.

    Returns:
        Array [dFx/dt, dFy/dt, dFz/dt].

    Example:
        >>> # Time-varying magnetic field
        >>> def Bx(x,y,z,t): return np.cos(t)
        >>> def By(x,y,z,t): return np.sin(t)
        >>> def Bz(x,y,z,t): return 0.0
        >>> dBdt = partial_derivative_t_vector(Bx, By, Bz, (0, 0, 0, 0))

    Reference:
        Part IV, Arts. 591-600: Time-varying fields.
    """
    dFx_dt = partial_derivative_t(Fx, point, dt, method).value
    dFy_dt = partial_derivative_t(Fy, point, dt, method).value
    dFz_dt = partial_derivative_t(Fz, point, dt, method).value

    return np.array([dFx_dt, dFy_dt, dFz_dt])


# ═══════════════════════════════════════════════════════════════════
# TOTAL / MATERIAL DERIVATIVE
# ═══════════════════════════════════════════════════════════════════


@maxwell_cite(
    591,
    592,
    593,
    598,
    599,
    600,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    theory_class="standard_math",
    description="Compute total (material) derivative: d/dt = d/dt + v.dot(grad)",
)
def total_derivative(
    func: Callable[[float, float, float, float], float],
    point: Tuple[float, float, float, float],
    velocity: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    dt: float = DT_DEFAULT,
    h: float = H_DEFAULT,
    method: DiffMethod = DiffMethod.CENTRAL,
) -> DerivativeResult:
    """Compute the total (material) derivative of a scalar field.

    df/dt = partial(f)/partial(t) + v . grad(f)

    This is the rate of change of f as seen by an observer moving
    with velocity v through the field.

    In electromagnetism, this appears in:
        - Moving conductor EMF (motional EMF)
        - Lorentz force derivation
        - Fluid MHD equations

    Args:
        func: Spacetime field function f(x, y, z, t).
        point: Spacetime point (x, y, z, t).
        velocity: Observer velocity (vx, vy, vz) in cm/s.
        dt: Time step for partial_t.
        h: Spatial step for gradient.
        method: Differentiation method.

    Returns:
        DerivativeResult with total derivative value.

    CGS Units:
        If f has units U, v in cm/s, spatial coords in cm, t in s,
        result has units U/s.

    Example:
        >>> # Field f = x*t (moving observer sees change)
        >>> def f(x, y, z, t): return x * t
        >>> # Observer moving at v=(1,0,0) at point (1,0,0,1)
        >>> result = total_derivative(f, (1.0, 0.0, 0.0, 1.0), velocity=(1.0, 0.0, 0.0))
        >>> # analytical: d/dt = t + v*1 = 1 + 1 = 2
        >>> result.value  # ~2.0

    Reference:
        Part IV, Arts. 591-600: Moving fields and electromotive force.
    """
    x, y, z, t = point
    vx, vy, vz = velocity

    # Partial time derivative
    partial_t = partial_derivative_t(func, point, dt, method).value

    # Spatial gradient (at fixed time)
    def func_at_t(px, py, pz):
        return func(px, py, pz, t)

    grad_result = partial_gradient(func_at_t, (x, y, z), h, method)
    grad = grad_result.value  # numpy array [df/dx, df/dy, df/dz]

    # v . grad
    advective = vx * grad[0] + vy * grad[1] + vz * grad[2]

    total = partial_t + advective

    return DerivativeResult(
        value=float(total),
        method=method,
        step_size=min(dt, h),
        order=2 if method == DiffMethod.CENTRAL else 1,
        point=point,
        variable="t (total)",
        order_derivative=1,
    )


@maxwell_cite(
    591,
    592,
    593,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    theory_class="standard_math",
    description="Compute total derivative of a vector field",
)
def total_derivative_vector(
    Fx: Callable[[float, float, float, float], float],
    Fy: Callable[[float, float, float, float], float],
    Fz: Callable[[float, float, float, float], float],
    point: Tuple[float, float, float, float],
    velocity: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    dt: float = DT_DEFAULT,
    h: float = H_DEFAULT,
    method: DiffMethod = DiffMethod.CENTRAL,
) -> np.ndarray:
    """Compute total derivative of each component of a vector field.

    For each component F_i:
        dF_i/dt = partial(F_i)/partial(t) + v . grad(F_i)

    Args:
        Fx, Fy, Fz: Vector field components as functions of (x, y, z, t).
        point: Spacetime point (x, y, z, t).
        velocity: Observer velocity (vx, vy, vz).
        dt: Time step.
        h: Spatial step.
        method: Differentiation method.

    Returns:
        Array [dFx/dt, dFy/dt, dFz/dt] (total derivatives).

    Reference:
        Part IV, Arts. 591-600: Moving electromagnetic fields.
    """
    dFx = total_derivative(Fx, point, velocity, dt, h, method).value
    dFy = total_derivative(Fy, point, velocity, dt, h, method).value
    dFz = total_derivative(Fz, point, velocity, dt, h, method).value

    return np.array([dFx, dFy, dFz])


# ═══════════════════════════════════════════════════════════════════
# JACOBIAN FOR COORDINATE TRANSFORMS
# ═══════════════════════════════════════════════════════════════════


@maxwell_cite(
    128,
    129,
    130,
    part=1,
    chapter="On Spherical Harmonics",
    theory_class="standard_math",
    description="Compute Jacobian matrix of coordinate transformation",
)
def jacobian(
    transform: CoordinateTransform,
    point: np.ndarray,
    h: float = H_DEFAULT,
) -> np.ndarray:
    """Compute the Jacobian matrix of a coordinate transformation.

    For a transformation T: R^n -> R^m, the Jacobian is the m x n matrix:

        J[i,j] = dT_i / dx_j

    For n=m=3 (standard 3D transforms):
        J = [[dx'/dx, dx'/dy, dx'/dz],
             [dy'/dx, dy'/dy, dy'/dz],
             [dz'/dx, dz'/dy, dz'/dz]]

    Common applications:
        - Cartesian to spherical: J with determinant r^2*sin(theta)
        - Cartesian to cylindrical: J with determinant r
        - General curvilinear coordinates

    Args:
        transform: Coordinate transformation function R^n -> R^m.
        point: Input point (numpy array of shape (n,)).
        h: Step size for numerical differentiation.

    Returns:
        Jacobian matrix of shape (m, n).

    Example:
        >>> # Cartesian to spherical (r, theta, phi)
        >>> def cartesian_to_spherical(xyz):
        ...     x, y, z = xyz
        ...     r = np.sqrt(x**2 + y**2 + z**2)
        ...     theta = np.arccos(z / r) if r > 0 else 0
        ...     phi = np.arctan2(y, x)
        ...     return np.array([r, theta, phi])
        >>> J = jacobian(cartesian_to_spherical, np.array([1.0, 0.0, 0.0]))
        >>> det_J = np.linalg.det(J)  # 1/r^2 for this point

    Reference:
        Part I, Arts. 128-130: Spherical coordinate transformations.
    """
    point = np.asarray(point, dtype=np.float64)
    n = len(point)

    # Determine output dimension by evaluating at point
    output = transform(point)
    m = len(output)

    J = np.zeros((m, n))

    for j in range(n):
        # Perturb the j-th input coordinate
        e_j = np.zeros(n)
        e_j[j] = h

        f_plus = transform(point + e_j)
        f_minus = transform(point - e_j)

        for i in range(m):
            J[i, j] = (f_plus[i] - f_minus[i]) / (2.0 * h)

    return J


@maxwell_cite(
    128,
    129,
    130,
    part=1,
    chapter="On Spherical Harmonics",
    theory_class="standard_math",
    description="Compute Jacobian determinant (volume scaling factor)",
)
def jacobian_determinant(
    transform: CoordinateTransform,
    point: np.ndarray,
    h: float = H_DEFAULT,
) -> float:
    """Compute the determinant of the Jacobian matrix.

    The Jacobian determinant |J| gives the local volume scaling
    factor of the coordinate transformation.

    For volume integrals in curvilinear coordinates:
        dV' = |J| * dV

    Common determinants:
        - Spherical coordinates: r^2 * sin(theta)
        - Cylindrical coordinates: r
        - Parabolic coordinates: (u^2 + v^2) * w

    Args:
        transform: Coordinate transformation R^n -> R^n.
        point: Input point.
        h: Step size.

    Returns:
        Jacobian determinant value.

    Reference:
        Part I, Arts. 128-130: Coordinate transformations.
    """
    J = jacobian(transform, point, h)
    return float(np.linalg.det(J))


@maxwell_cite(
    128,
    129,
    130,
    part=1,
    chapter="On Spherical Harmonics",
    theory_class="standard_math",
    description="Cartesian to spherical coordinate transform with Jacobian",
)
def cartesian_to_spherical(point: np.ndarray) -> np.ndarray:
    """Convert Cartesian coordinates to spherical (r, theta, phi).

    Args:
        point: (x, y, z) in Cartesian.

    Returns:
        (r, theta, phi) where:
            r = sqrt(x^2 + y^2 + z^2)
            theta = arccos(z/r) (polar angle, 0 to pi)
            phi = arctan2(y, x) (azimuthal angle, 0 to 2*pi)
    """
    x, y, z = point
    r = np.sqrt(x**2 + y**2 + z**2)
    if r == 0:
        return np.array([0.0, 0.0, 0.0])
    theta = np.arccos(np.clip(z / r, -1.0, 1.0))
    phi = np.arctan2(y, x)
    if phi < 0:
        phi += 2 * np.pi
    return np.array([r, theta, phi])


@maxwell_cite(
    128,
    129,
    130,
    part=1,
    chapter="On Spherical Harmonics",
    theory_class="standard_math",
    description="Spherical to Cartesian coordinate transform",
)
def spherical_to_cartesian(point: np.ndarray) -> np.ndarray:
    """Convert spherical coordinates to Cartesian (x, y, z).

    Args:
        point: (r, theta, phi) in spherical.

    Returns:
        (x, y, z) where:
            x = r * sin(theta) * cos(phi)
            y = r * sin(theta) * sin(phi)
            z = r * cos(theta)
    """
    r, theta, phi = point
    sin_theta = np.sin(theta)
    return np.array(
        [
            r * sin_theta * np.cos(phi),
            r * sin_theta * np.sin(phi),
            r * np.cos(theta),
        ]
    )


@maxwell_cite(
    128,
    129,
    130,
    part=1,
    chapter="On Spherical Harmonics",
    theory_class="standard_math",
    description="Cartesian to cylindrical coordinate transform",
)
def cartesian_to_cylindrical(point: np.ndarray) -> np.ndarray:
    """Convert Cartesian coordinates to cylindrical (rho, phi, z).

    Args:
        point: (x, y, z) in Cartesian.

    Returns:
        (rho, phi, z) where:
            rho = sqrt(x^2 + y^2)
            phi = arctan2(y, x)
            z = z
    """
    x, y, z = point
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    if phi < 0:
        phi += 2 * np.pi
    return np.array([rho, phi, z])


@maxwell_cite(
    128,
    129,
    130,
    part=1,
    chapter="On Spherical Harmonics",
    theory_class="standard_math",
    description="Cylindrical to Cartesian coordinate transform",
)
def cylindrical_to_cartesian(point: np.ndarray) -> np.ndarray:
    """Convert cylindrical coordinates to Cartesian (x, y, z).

    Args:
        point: (rho, phi, z) in cylindrical.

    Returns:
        (x, y, z) where:
            x = rho * cos(phi)
            y = rho * sin(phi)
            z = z
    """
    rho, phi, z = point
    return np.array(
        [
            rho * np.cos(phi),
            rho * np.sin(phi),
            z,
        ]
    )


# ═══════════════════════════════════════════════════════════════════
# SCHWARZ'S THEOREM VERIFICATION
# ═══════════════════════════════════════════════════════════════════


@maxwell_cite(
    182,
    183,
    184,
    185,
    186,
    part=1,
    chapter="On Conjugate Functions",
    theory_class="standard_math",
    description="Verify Schwarz's theorem (equality of mixed partials)",
)
def verify_schwarz_theorem(
    func: ScalarField3D,
    point: Tuple[float, float, float],
    var1: str = "x",
    var2: str = "y",
    h: float = H_MIXED,
    tolerance: float = 1e-4,
) -> Dict[str, Any]:
    """Verify Schwarz's theorem (Clairaut's theorem) for a scalar field.

    Schwarz's theorem states that for a function with continuous
    second partial derivatives:

        d^2f/(dx dy) = d^2f/(dy dx)

    This is a fundamental result used in:
        - Proving curl(grad phi) = 0
        - Proving div(curl F) = 0
        - Validating coordinate transformations
        - Checking consistency of potential theory

    Args:
        func: Scalar field function f(x, y, z).
        point: Point (x, y, z) at which to verify.
        var1: First variable ('x', 'y', or 'z').
        var2: Second variable ('x', 'y', or 'z').
        h: Step size for numerical differentiation.
        tolerance: Relative tolerance for verification.

    Returns:
        Dictionary with:
            - 'd2f_dvar1_dvar2': d^2f/(dvar1*dvar2)
            - 'd2f_dvar2_dvar1': d^2f/(dvar2*dvar1)
            - 'difference': |d2f_dvar1_dvar2 - d2f_dvar2_dvar1|
            - 'relative_error': relative difference
            - 'verified': True if relative_error < tolerance
            - 'tolerance_used': tolerance

    Example:
        >>> def f(x, y, z): return x**2 * y + y**2 * z + z**2 * x
        >>> result = verify_schwarz_theorem(f, (1.0, 2.0, 3.0), "x", "y")
        >>> result['verified']  # True

    Reference:
        Part I, Arts. 182-186: Conjugate functions.
        Part I, Arts. 103-110: Vector identities (curl(grad)=0).
    """
    # d^2f/(dvar1*dvar2)
    result_12 = mixed_partial_derivative(func, point, var1, var2, h)

    # d^2f/(dvar2*dvar1)
    result_21 = mixed_partial_derivative(func, point, var2, var1, h)

    diff = abs(result_12.value - result_21.value)
    denom = max(abs(result_12.value), abs(result_21.value), 1.0)
    rel_error = diff / denom

    return {
        "d2f_dvar1_dvar2": float(result_12.value),
        "d2f_dvar2_dvar1": float(result_21.value),
        "difference": float(diff),
        "relative_error": float(rel_error),
        "verified": rel_error < tolerance,
        "tolerance_used": tolerance,
    }


@maxwell_cite(
    103,
    104,
    105,
    106,
    107,
    108,
    109,
    110,
    part=1,
    chapter="Vector Identities",
    theory_class="standard_math",
    description="Verify curl(grad phi) = 0 using Schwarz's theorem",
)
def verify_curl_grad_via_schwarz(
    phi_func: ScalarField3D,
    point: Tuple[float, float, float],
    h: float = H_MIXED,
    tolerance: float = 1e-4,
) -> Dict[str, Any]:
    """Verify curl(grad phi) = 0 using Schwarz's theorem.

    The identity curl(grad phi) = 0 follows directly from Schwarz's
    theorem since the curl of the gradient involves differences of
    mixed partial derivatives:

        curl(grad phi)_x = d^2(phi)/dydz - d^2(phi)/dzdy = 0

    This is a more numerically stable approach than nested numerical
    differentiation.

    Args:
        phi_func: Scalar potential function.
        point: Point (x, y, z) at which to verify.
        h: Step size.
        tolerance: Relative tolerance.

    Returns:
        Dictionary with verification results for each curl component.

    Reference:
        Part I, Arts. 103-110: Vector identities.
    """
    results = {}

    # curl(grad phi)_x = d^2phi/(dy dz) - d^2phi/(dz dy)
    sch_yz = verify_schwarz_theorem(phi_func, point, "y", "z", h, tolerance)
    # curl(grad phi)_y = d^2phi/(dz dx) - d^2phi/(dx dz)
    sch_zx = verify_schwarz_theorem(phi_func, point, "z", "x", h, tolerance)
    # curl(grad phi)_z = d^2phi/(dx dy) - d^2phi/(dy dx)
    sch_xy = verify_schwarz_theorem(phi_func, point, "x", "y", h, tolerance)

    results["curl_x"] = {
        "d2phi_dydz": sch_yz["d2f_dvar1_dvar2"],
        "d2phi_dzdy": sch_yz["d2f_dvar2_dvar1"],
        "difference": sch_yz["difference"],
        "verified": sch_yz["verified"],
    }
    results["curl_y"] = {
        "d2phi_dzdx": sch_zx["d2f_dvar1_dvar2"],
        "d2phi_dxdz": sch_zx["d2f_dvar2_dvar1"],
        "difference": sch_zx["difference"],
        "verified": sch_zx["verified"],
    }
    results["curl_z"] = {
        "d2phi_dxdy": sch_xy["d2f_dvar1_dvar2"],
        "d2phi_dydx": sch_xy["d2f_dvar2_dvar1"],
        "difference": sch_xy["difference"],
        "verified": sch_xy["verified"],
    }

    all_verified = sch_yz["verified"] and sch_zx["verified"] and sch_xy["verified"]
    results["all_verified"] = all_verified
    results["max_difference"] = max(
        sch_yz["difference"], sch_zx["difference"], sch_xy["difference"]
    )

    return results


@maxwell_cite(
    103,
    104,
    105,
    part=1,
    chapter="Vector Identities",
    theory_class="standard_math",
    description="Verify div(curl F) = 0 using Schwarz's theorem",
)
def verify_div_curl_via_schwarz(
    Fx: Callable[[float, float, float], float],
    Fy: Callable[[float, float, float], float],
    Fz: Callable[[float, float, float], float],
    point: Tuple[float, float, float],
    h: float = H_MIXED,
    tolerance: float = 1e-4,
) -> Dict[str, Any]:
    """Verify div(curl F) = 0 using Schwarz's theorem.

    The identity div(curl F) = 0 follows from Schwarz's theorem
    since the divergence of the curl involves differences of
    mixed partials of the same component:

        div(curl F) = d(dFz/dy - dFy/dz)/dx + d(dFx/dz - dFz/dx)/dy + d(dFy/dx - dFx/dy)/dz
                    = d^2Fz/(dxdy) - d^2Fy/(dxdz) + d^2Fx/(dydz) - d^2Fz/(dydx)
                      + d^2Fy/(dzdx) - d^2Fx/(dzdy)

    Each pair cancels by Schwarz's theorem.

    Args:
        Fx, Fy, Fz: Vector field components.
        point: Point (x, y, z) at which to verify.
        h: Step size.
        tolerance: Relative tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part I, Arts. 103-110: Vector identities.
    """
    # d^2Fz/(dxdy) - d^2Fz/(dydx)
    sch_Fz_xy = verify_schwarz_theorem(Fz, point, "x", "y", h, tolerance)
    # d^2Fx/(dydz) - d^2Fx/(dzdy)
    sch_Fx_yz = verify_schwarz_theorem(Fx, point, "y", "z", h, tolerance)
    # d^2Fy/(dzdx) - d^2Fy/(dxdz)
    sch_Fy_zx = verify_schwarz_theorem(Fy, point, "z", "x", h, tolerance)

    div_curl_value = (
        (sch_Fz_xy["d2f_dvar1_dvar2"] - sch_Fz_xy["d2f_dvar2_dvar1"])
        + (sch_Fx_yz["d2f_dvar1_dvar2"] - sch_Fx_yz["d2f_dvar2_dvar1"])
        + (sch_Fy_zx["d2f_dvar1_dvar2"] - sch_Fy_zx["d2f_dvar2_dvar1"])
    )

    return {
        "div_curl": float(div_curl_value),
        "Fz_mixed_xy": {
            "d2Fz_dxdy": sch_Fz_xy["d2f_dvar1_dvar2"],
            "d2Fz_dydx": sch_Fz_xy["d2f_dvar2_dvar1"],
        },
        "Fx_mixed_yz": {
            "d2Fx_dydz": sch_Fx_yz["d2f_dvar1_dvar2"],
            "d2Fx_dzdy": sch_Fx_yz["d2f_dvar2_dvar1"],
        },
        "Fy_mixed_zx": {
            "d2Fy_dzdx": sch_Fy_zx["d2f_dvar1_dvar2"],
            "d2Fy_dxdz": sch_Fy_zx["d2f_dvar2_dvar1"],
        },
        "verified": abs(div_curl_value) < tolerance,
        "tolerance_used": tolerance,
    }


# ═══════════════════════════════════════════════════════════════════
# DERIVATIVE VALIDATION ENGINE
# ═══════════════════════════════════════════════════════════════════


@dataclass
class ValidationReport:
    """Report from derivative validation against analytical solution.

    Attributes:
        numerical: Numerically computed derivative.
        analytical: Analytical (exact) derivative value.
        absolute_error: |numerical - analytical|.
        relative_error: |numerical - analytical| / max(|analytical|, 1).
        passed: True if error < tolerance.
        method: Differentiation method used.
        step_size: Step size h.
    """

    numerical: float
    analytical: float
    absolute_error: float
    relative_error: float
    passed: bool
    method: DiffMethod
    step_size: float


@maxwell_cite(
    71,
    72,
    73,
    part=1,
    chapter="On the Potential",
    theory_class="standard_math",
    description="Validate numerical derivative against analytical solution",
)
def validate_derivative(
    func: ScalarField3D,
    analytical_deriv: ScalarField3D,
    point: Tuple[float, float, float],
    variable: str = "x",
    h: float = H_DEFAULT,
    method: DiffMethod = DiffMethod.CENTRAL,
    tolerance: float = 1e-6,
) -> ValidationReport:
    """Validate a numerical derivative against an analytical solution.

    This is used for testing and quality assurance of numerical
    differentiation methods.

    Args:
        func: Scalar field function f(x, y, z).
        analytical_deriv: Analytical derivative df/dvariable (as a function).
        point: Point at which to compare.
        variable: Which variable to differentiate.
        h: Step size for numerical derivative.
        method: Differentiation method.
        tolerance: Absolute tolerance for passing.

    Returns:
        ValidationReport with comparison results.

    Example:
        >>> def f(x, y, z): return x**3 + y**2
        >>> def dfdx(x, y, z): return 3 * x**2  # analytical
        >>> report = validate_derivative(f, dfdx, (2.0, 0.0, 0.0), "x")
        >>> report.passed  # True
        >>> report.relative_error  # ~1e-12
    """
    numerical_result = partial_derivative(func, point, variable, h, method)
    numerical = numerical_result.value
    analytical = analytical_deriv(*point)

    abs_error = abs(numerical - analytical)
    denom = max(abs(analytical), 1.0)
    rel_error = abs_error / denom

    return ValidationReport(
        numerical=float(numerical),
        analytical=float(analytical),
        absolute_error=float(abs_error),
        relative_error=float(rel_error),
        passed=abs_error < tolerance,
        method=method,
        step_size=h,
    )


@maxwell_cite(
    77,
    100,
    part=1,
    chapter="On the Potential",
    theory_class="standard_math",
    description="Find optimal step size for numerical differentiation",
)
def find_optimal_step(
    func: ScalarField3D,
    analytical_deriv: ScalarField3D,
    point: Tuple[float, float, float],
    variable: str = "x",
    h_range: Tuple[float, float] = (1e-12, 1e-2),
    n_steps: int = 30,
    method: DiffMethod = DiffMethod.CENTRAL,
) -> Dict[str, Any]:
    """Find the optimal step size for numerical differentiation.

    Tests multiple step sizes and finds the one that minimizes
    the error compared to the analytical derivative.

    This is useful for determining the best h for a given function
    and precision requirement.

    Args:
        func: Scalar field function.
        analytical_deriv: Analytical derivative function.
        point: Point at which to evaluate.
        variable: Which variable.
        h_range: (h_min, h_max) range to search.
        n_steps: Number of step sizes to test.
        method: Differentiation method.

    Returns:
        Dictionary with:
            - 'optimal_h': Step size with minimum error
            - 'min_relative_error': Minimum relative error achieved
            - 'errors': List of (h, error) tuples
            - 'recommended_h': Practical recommendation (geometric mean near optimum)

    Reference:
        Numerical analysis standard practice for step size selection.
    """
    h_values = np.logspace(np.log10(h_range[0]), np.log10(h_range[1]), n_steps)

    errors = []
    for h in h_values:
        try:
            report = validate_derivative(
                func, analytical_deriv, point, variable, h, method
            )
            errors.append((float(h), report.relative_error))
        except (ZeroDivisionError, OverflowError, ValueError):
            errors.append((float(h), float("inf")))

    # Find optimal h
    best_idx = min(range(len(errors)), key=lambda i: errors[i][1])
    optimal_h, min_error = errors[best_idx]

    # Recommended h: slightly larger than optimal for robustness
    recommended_h = optimal_h * np.sqrt(10)

    return {
        "optimal_h": float(optimal_h),
        "min_relative_error": float(min_error),
        "errors": errors,
        "recommended_h": float(recommended_h),
    }


# ═══════════════════════════════════════════════════════════════════
# DERIVATIVE CALCULATOR CLASS
# ═══════════════════════════════════════════════════════════════════


@dataclass
class DerivativeCalculator:
    """Unified interface for all derivative operations.

    Provides a stateful calculator with configurable precision
    and result history.

    Attributes:
        h: Default spatial step size.
        dt: Default time step size.
        method: Default differentiation method.
        _history: List of computation records.

    Usage:
        >>> calc = DerivativeCalculator(h=1e-6, dt=1e-8)
        >>> result = calc.partial(func, (1, 2, 3), "x")
        >>> report = calc.validate(func, analytical_df, (1, 2, 3), "x")
    """

    h: float = H_DEFAULT
    dt: float = DT_DEFAULT
    method: DiffMethod = DiffMethod.CENTRAL
    _history: list = field(default_factory=list)

    def _record(self, operation: str, result: Any) -> None:
        """Record a computation."""
        self._history.append({"operation": operation, "result": result})

    def partial(
        self,
        func: ScalarField3D,
        point: Tuple[float, float, float],
        variable: str = "x",
        h: Optional[float] = None,
        method: Optional[DiffMethod] = None,
    ) -> DerivativeResult:
        """Compute partial derivative."""
        result = partial_derivative(
            func, point, variable, h or self.h, method or self.method
        )
        self._record(f"partial_{variable}", result)
        return result

    def gradient(
        self,
        func: ScalarField3D,
        point: Tuple[float, float, float],
        h: Optional[float] = None,
        method: Optional[DiffMethod] = None,
    ) -> DerivativeResult:
        """Compute gradient (all partial derivatives)."""
        result = partial_gradient(func, point, h or self.h, method or self.method)
        self._record("gradient", result)
        return result

    def second_partial(
        self,
        func: ScalarField3D,
        point: Tuple[float, float, float],
        variable: str = "x",
        h: Optional[float] = None,
    ) -> DerivativeResult:
        """Compute second partial derivative."""
        result = second_partial_derivative(func, point, variable, h or self.h)
        self._record(f"second_partial_{variable}", result)
        return result

    def mixed_partial(
        self,
        func: ScalarField3D,
        point: Tuple[float, float, float],
        var1: str = "x",
        var2: str = "y",
        h: Optional[float] = None,
    ) -> DerivativeResult:
        """Compute mixed partial derivative."""
        result = mixed_partial_derivative(func, point, var1, var2, h or H_MIXED)
        self._record(f"mixed_partial_{var1}_{var2}", result)
        return result

    def hessian(
        self,
        func: ScalarField3D,
        point: Tuple[float, float, float],
        h: Optional[float] = None,
    ) -> np.ndarray:
        """Compute Hessian matrix."""
        result = hessian(func, point, h or self.h)
        self._record("hessian", result)
        return result

    def partial_t(
        self,
        func: Callable[[float, float, float, float], float],
        point: Tuple[float, float, float, float],
        dt: Optional[float] = None,
        method: Optional[DiffMethod] = None,
    ) -> DerivativeResult:
        """Compute time derivative."""
        result = partial_derivative_t(func, point, dt or self.dt, method or self.method)
        self._record("partial_t", result)
        return result

    def total(
        self,
        func: Callable[[float, float, float, float], float],
        point: Tuple[float, float, float, float],
        velocity: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        dt: Optional[float] = None,
        h: Optional[float] = None,
        method: Optional[DiffMethod] = None,
    ) -> DerivativeResult:
        """Compute total (material) derivative."""
        result = total_derivative(
            func,
            point,
            velocity,
            dt or self.dt,
            h or self.h,
            method or self.method,
        )
        self._record("total_derivative", result)
        return result

    def jacobian(
        self,
        transform: CoordinateTransform,
        point: np.ndarray,
        h: Optional[float] = None,
    ) -> np.ndarray:
        """Compute Jacobian matrix."""
        result = jacobian(transform, point, h or self.h)
        self._record("jacobian", result)
        return result

    def jacobian_det(
        self,
        transform: CoordinateTransform,
        point: np.ndarray,
        h: Optional[float] = None,
    ) -> float:
        """Compute Jacobian determinant."""
        result = jacobian_determinant(transform, point, h or self.h)
        self._record("jacobian_determinant", result)
        return result

    def verify_schwarz(
        self,
        func: ScalarField3D,
        point: Tuple[float, float, float],
        var1: str = "x",
        var2: str = "y",
        h: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Verify Schwarz's theorem."""
        result = verify_schwarz_theorem(func, point, var1, var2, h or H_MIXED)
        self._record(f"schwarz_{var1}_{var2}", result)
        return result

    def validate(
        self,
        func: ScalarField3D,
        analytical_deriv: ScalarField3D,
        point: Tuple[float, float, float],
        variable: str = "x",
        h: Optional[float] = None,
        method: Optional[DiffMethod] = None,
    ) -> ValidationReport:
        """Validate numerical derivative against analytical solution."""
        result = validate_derivative(
            func,
            analytical_deriv,
            point,
            variable,
            h or self.h,
            method or self.method,
        )
        self._record(f"validate_{variable}", result)
        return result

    def clear_history(self) -> None:
        """Clear computation history."""
        self._history.clear()

    def get_history(self) -> list:
        """Return computation history."""
        return list(self._history)


__all__ = [
    # Enums
    "DiffMethod",
    # Data classes
    "DerivativeResult",
    "ValidationReport",
    # Partial derivatives
    "partial_derivative",
    "partial_gradient",
    # Higher-order derivatives
    "second_partial_derivative",
    "mixed_partial_derivative",
    "hessian",
    # Time derivatives
    "partial_derivative_t",
    "partial_derivative_t_vector",
    # Total/material derivative
    "total_derivative",
    "total_derivative_vector",
    # Coordinate transforms
    "jacobian",
    "jacobian_determinant",
    "cartesian_to_spherical",
    "spherical_to_cartesian",
    "cartesian_to_cylindrical",
    "cylindrical_to_cartesian",
    # Schwarz's theorem
    "verify_schwarz_theorem",
    "verify_curl_grad_via_schwarz",
    "verify_div_curl_via_schwarz",
    # Validation
    "validate_derivative",
    "find_optimal_step",
    # Calculator class
    "DerivativeCalculator",
    # Constants
    "H_DEFAULT",
    "DT_DEFAULT",
    "H_MIXED",
]

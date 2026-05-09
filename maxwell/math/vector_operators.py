"""maxwell.math.vector_operators — Core vector calculus operators (Arts. 71-110).

Implements Maxwell's vector calculus foundations used throughout
Part I (Electrostatics) and Part II (Electrokinematics).

Maxwell's Vector Calculus (Arts. 71-110):
    Gradient (Arts. 71-77): V = -grad(phi)
        The force is the negative gradient of the potential.

    Divergence (Art. 77): div(F) = dFx/dx + dFy/dy + dFz/dz
        The convergence or divergence of a vector field.

    Curl (Art. 77): curl(F) = (dFz/dy - dFy/dz, dFx/dz - dFz/dx, dFy/dx - dFx/dy)
        The rotation of a vector field.

    Laplacian (Arts. 77, 100): nabla^2(phi) = div(grad phi)
        Second derivative operator for potential theory.

Vector Identities (Arts. 103-110):
    - div(grad phi) = nabla^2(phi)
    - curl(grad phi) = 0
    - div(curl F) = 0
    - curl(curl F) = grad(div F) - nabla^2(F)

All calculations use numerical differentiation with configurable step size.
The default step size h=1e-6 is suitable for CGS units (centimeters).

Category: C (standard_math) — Vector calculus foundations.

References:
    Part I, Arts. 71-77: Theory of the potential and gradient.
    Part I, Art. 77: Definition of divergence and curl.
    Part I, Arts. 100-110: Vector identities and Laplacian.
"""

from __future__ import annotations

from typing import Callable, Tuple

import numpy as np

from maxwell.meta.citation import maxwell_cite

# Type alias for 3D vector field components
VectorField = Tuple[float, float, float]
ScalarFieldResult = float


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
    description="Compute gradient of scalar potential (Art. 71-77)",
)
def gradient(
    phi_func: Callable[[float, float, float], float],
    x: float,
    y: float,
    z: float,
    h: float = 1e-6,
) -> Tuple[float, float, float]:
    """
    Compute the gradient of a scalar potential field.

    Maxwell's formulation (Arts. 71-77):
        The force components are:
            Ex = -d(phi)/dx, Ey = -d(phi)/dy, Ez = -d(phi)/dz

        Therefore: grad(phi) = (d(phi)/dx, d(phi)/dy, d(phi)/dz)

    Uses central difference for numerical differentiation:
        d(f)/dx ≈ (f(x+h) - f(x-h)) / (2h)

    Args:
        phi_func: Scalar potential function phi(x, y, z).
        x, y, z: Point coordinates (cm).
        h: Step size for numerical differentiation (cm).

    Returns:
        Gradient vector (d(phi)/dx, d(phi)/dy, d(phi)/dz).

    Reference:
        Part I, Arts. 71-77: The potential and its gradient.

    Example:
        >>> # Potential of a point charge at origin
        >>> def phi(x, y, z): return 1.0 / np.sqrt(x**2 + y**2 + z**2)
        >>> Ex, Ey, Ez = gradient(phi, 1.0, 0.0, 0.0)
        >>> print(f"Gradient at (1,0,0): ({Ex:.4f}, {Ey:.4f}, {Ez:.4f})")
    """
    # Central difference for each component
    dphi_dx = (phi_func(x + h, y, z) - phi_func(x - h, y, z)) / (2 * h)
    dphi_dy = (phi_func(x, y + h, z) - phi_func(x, y - h, z)) / (2 * h)
    dphi_dz = (phi_func(x, y, z + h) - phi_func(x, y, z - h)) / (2 * h)

    return (dphi_dx, dphi_dy, dphi_dz)


@maxwell_cite(
    77,
    part=1,
    chapter="On the Potential",
    theory_class="standard_math",
    description="Compute divergence of vector field (Art. 77)",
)
def divergence(
    Fx: Callable[[float, float, float], float],
    Fy: Callable[[float, float, float], float],
    Fz: Callable[[float, float, float], float],
    x: float,
    y: float,
    z: float,
    h: float = 1e-6,
) -> float:
    """
    Compute the divergence of a vector field.

    Maxwell's definition (Art. 77):
        div(F) = dFx/dx + dFy/dy + dFz/dz

    The divergence measures the "convergence" or "divergence" of the field
    at a point. In electrostatics, div(E) = 4*pi*rho (Gauss's law in CGS).

    Uses central difference for numerical differentiation.

    Args:
        Fx, Fy, Fz: Vector field component functions.
        x, y, z: Point coordinates (cm).
        h: Step size for numerical differentiation (cm).

    Returns:
        Divergence value div(F) at the point.

    Reference:
        Part I, Art. 77: Definition of divergence.

    Example:
        >>> # Inverse square field: F = r/|r|^3
        >>> def Fx(x,y,z): return x / (x**2 + y**2 + z**2)**1.5
        >>> def Fy(x,y,z): return y / (x**2 + y**2 + z**2)**1.5
        >>> def Fz(x,y,z): return z / (x**2 + y**2 + z**2)**1.5
        >>> div_F = divergence(Fx, Fy, Fz, 2.0, 0.0, 0.0)
    """
    dFx_dx = (Fx(x + h, y, z) - Fx(x - h, y, z)) / (2 * h)
    dFy_dy = (Fy(x, y + h, z) - Fy(x, y - h, z)) / (2 * h)
    dFz_dz = (Fz(x, y, z + h) - Fz(x, y, z - h)) / (2 * h)

    return dFx_dx + dFy_dy + dFz_dz


@maxwell_cite(
    77,
    part=1,
    chapter="On the Potential",
    theory_class="standard_math",
    description="Compute curl of vector field (Art. 77)",
)
def curl(
    Fx: Callable[[float, float, float], float],
    Fy: Callable[[float, float, float], float],
    Fz: Callable[[float, float, float], float],
    x: float,
    y: float,
    z: float,
    h: float = 1e-6,
) -> Tuple[float, float, float]:
    """
    Compute the curl of a vector field.

    Maxwell's definition (Art. 77):
        curl(F) = (dFz/dy - dFy/dz, dFx/dz - dFz/dx, dFy/dx - dFx/dy)

    In electromagnetism:
        - Electrostatics: curl(E) = 0 (conservative field)
        - Magnetostatics: curl(H) = 4*pi*C (Ampere's law in CGS)

    Uses central difference for numerical differentiation.

    Args:
        Fx, Fy, Fz: Vector field component functions.
        x, y, z: Point coordinates (cm).
        h: Step size for numerical differentiation (cm).

    Returns:
        Curl vector (cx, cy, cz) at the point.

    Reference:
        Part I, Art. 77: Definition of curl.

    Example:
        >>> # Rotational field: F = (-y, x, 0)
        >>> def Fx(x,y,z): return -y
        >>> def Fy(x,y,z): return x
        >>> def Fz(x,y,z): return 0.0
        >>> curl_F = curl(Fx, Fy, Fz, 1.0, 0.0, 0.0)
        >>> print(f"Curl: {curl_F}")  # Should be (0, 0, 2)
    """
    # curl_x = dFz/dy - dFy/dz
    dFz_dy = (Fz(x, y + h, z) - Fz(x, y - h, z)) / (2 * h)
    dFy_dz = (Fy(x, y, z + h) - Fy(x, y, z - h)) / (2 * h)
    cx = dFz_dy - dFy_dz

    # curl_y = dFx/dz - dFz/dx
    dFx_dz = (Fx(x, y, z + h) - Fx(x, y, z - h)) / (2 * h)
    dFz_dx = (Fz(x + h, y, z) - Fz(x - h, y, z)) / (2 * h)
    cy = dFx_dz - dFz_dx

    # curl_z = dFy/dx - dFx/dy
    dFy_dx = (Fy(x + h, y, z) - Fy(x - h, y, z)) / (2 * h)
    dFx_dy = (Fx(x, y + h, z) - Fx(x, y - h, z)) / (2 * h)
    cz = dFy_dx - dFx_dy

    return (cx, cy, cz)


@maxwell_cite(
    77,
    100,
    part=1,
    chapter="On the Potential",
    theory_class="standard_math",
    description="Compute Laplacian of scalar field (Arts. 77, 100)",
)
def laplacian(
    phi_func: Callable[[float, float, float], float],
    x: float,
    y: float,
    z: float,
    h: float = 1e-6,
) -> float:
    """
    Compute the Laplacian of a scalar field.

    Maxwell's formulation (Arts. 77, 100):
        nabla^2(phi) = d^2(phi)/dx^2 + d^2(phi)/dy^2 + d^2(phi)/dz^2

    Equivalently: nabla^2(phi) = div(grad(phi))

    In electrostatics (Poisson's equation):
        nabla^2(phi) = -4*pi*rho

    Uses central difference for second derivatives:
        d^2(f)/dx^2 ≈ (f(x+h) - 2f(x) + f(x-h)) / h^2

    Args:
        phi_func: Scalar field function phi(x, y, z).
        x, y, z: Point coordinates (cm).
        h: Step size for numerical differentiation (cm).

    Returns:
        Laplacian value nabla^2(phi) at the point.

    Reference:
        Part I, Art. 77: Laplacian definition.
        Part I, Art. 100: Application to potential theory.

    Example:
        >>> # Potential satisfying Laplace's equation (away from origin)
        >>> def phi(x, y, z): return 1.0 / np.sqrt(x**2 + y**2 + z**2)
        >>> lap = laplacian(phi, 2.0, 0.0, 0.0)
        >>> print(f"Laplacian (should be ~0): {lap:.2e}")
    """
    # Second derivatives using central difference
    d2phi_dx2 = (
        phi_func(x + h, y, z) - 2 * phi_func(x, y, z) + phi_func(x - h, y, z)
    ) / (h**2)
    d2phi_dy2 = (
        phi_func(x, y + h, z) - 2 * phi_func(x, y, z) + phi_func(x, y - h, z)
    ) / (h**2)
    d2phi_dz2 = (
        phi_func(x, y, z + h) - 2 * phi_func(x, y, z) + phi_func(x, y, z - h)
    ) / (h**2)

    return d2phi_dx2 + d2phi_dy2 + d2phi_dz2


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
    description="Compute vector Laplacian (Arts. 103-110)",
)
def vector_laplacian(
    Fx: Callable[[float, float, float], float],
    Fy: Callable[[float, float, float], float],
    Fz: Callable[[float, float, float], float],
    x: float,
    y: float,
    z: float,
    h: float = 1e-6,
) -> Tuple[float, float, float]:
    """
    Compute the vector Laplacian of a vector field.

    Maxwell's vector identity (Arts. 103-110):
        nabla^2(F) = grad(div F) - curl(curl F)

    Component-wise definition:
        nabla^2(F) = (nabla^2(Fx), nabla^2(Fy), nabla^2(Fz))

    This function computes the component-wise Laplacian.

    Args:
        Fx, Fy, Fz: Vector field component functions.
        x, y, z: Point coordinates (cm).
        h: Step size for numerical differentiation (cm).

    Returns:
        Vector Laplacian (lx, ly, lz) at the point.

    Reference:
        Part I, Arts. 103-110: Vector calculus identities.

    Example:
        >>> # Solenoidal field
        >>> def Fx(x,y,z): return y * z
        >>> def Fy(x,y,z): return x * z
        >>> def Fz(x,y,z): return x * y
        >>> lap_F = vector_laplacian(Fx, Fy, Fz, 1.0, 1.0, 1.0)
    """
    # Compute scalar Laplacian for each component
    lx = laplacian(Fx, x, y, z, h)
    ly = laplacian(Fy, x, y, z, h)
    lz = laplacian(Fz, x, y, z, h)

    return (lx, ly, lz)


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
    description="Verify curl(grad phi) = 0 identity (Arts. 103-110)",
)
def identity_curl_grad_zero(
    phi_func: Callable[[float, float, float], float],
    x: float,
    y: float,
    z: float,
    h: float = 1e-6,
) -> bool:
    """
    Verify the vector identity: curl(grad phi) = 0.

    Maxwell's identity (Arts. 103-110):
        The curl of a gradient is always zero.

    This is a fundamental identity expressing that gradient fields
    are irrotational (conservative). In electrostatics, this means
    curl(E) = 0 since E = -grad(phi).

    Args:
        phi_func: Scalar potential function phi(x, y, z).
        x, y, z: Point coordinates (cm).
        h: Step size for numerical differentiation (cm).

    Returns:
        True if |curl(grad phi)| < tolerance (numerical precision).

    Reference:
        Part I, Arts. 103-110: Vector identities.

    Example:
        >>> def phi(x,y,z): return x**2 + y**2 + z**2
        >>> verified = identity_curl_grad_zero(phi, 1.0, 1.0, 1.0)
        >>> print(f"Identity verified: {verified}")
    """
    # First compute gradient
    grad_x, grad_y, grad_z = gradient(phi_func, x, y, z, h)

    # Create functions for the gradient components
    def Gx(px, py, pz):
        return gradient(phi_func, px, py, pz, h)[0]

    def Gy(px, py, pz):
        return gradient(phi_func, px, py, pz, h)[1]

    def Gz(px, py, pz):
        return gradient(phi_func, px, py, pz, h)[2]

    # Compute curl of gradient
    curl_g = curl(Gx, Gy, Gz, x, y, z, h * 10)  # Larger h for nested derivatives

    # Check if magnitude is near zero
    magnitude = np.sqrt(curl_g[0] ** 2 + curl_g[1] ** 2 + curl_g[2] ** 2)
    tolerance = 1e-3  # Relaxed tolerance for nested numerical differentiation

    return magnitude < tolerance


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
    description="Verify div(curl F) = 0 identity (Arts. 103-110)",
)
def identity_div_curl_zero(
    Fx: Callable[[float, float, float], float],
    Fy: Callable[[float, float, float], float],
    Fz: Callable[[float, float, float], float],
    x: float,
    y: float,
    z: float,
    h: float = 1e-6,
) -> bool:
    """
    Verify the vector identity: div(curl F) = 0.

    Maxwell's identity (Arts. 103-110):
        The divergence of a curl is always zero.

    This identity expresses that solenoidal (divergence-free) fields
    can be written as curls. In magnetostatics, since div(B) = 0,
    we can write B = curl(A) for some vector potential A.

    Args:
        Fx, Fy, Fz: Vector field component functions.
        x, y, z: Point coordinates (cm).
        h: Step size for numerical differentiation (cm).

    Returns:
        True if |div(curl F)| < tolerance (numerical precision).

    Reference:
        Part I, Arts. 103-110: Vector identities.

    Example:
        >>> def Fx(x,y,z): return y * z
        >>> def Fy(x,y,z): return x * z
        >>> def Fz(x,y,z): return x * y
        >>> verified = identity_div_curl_zero(Fx, Fy, Fz, 1.0, 1.0, 1.0)
    """
    # First compute curl
    curl_x, curl_y, curl_z = curl(Fx, Fy, Fz, x, y, z, h)

    # Create functions for curl components
    def Cx(px, py, pz):
        return curl(Fx, Fy, Fz, px, py, pz, h)[0]

    def Cy(px, py, pz):
        return curl(Fx, Fy, Fz, px, py, pz, h)[1]

    def Cz(px, py, pz):
        return curl(Fx, Fy, Fz, px, py, pz, h)[2]

    # Compute divergence of curl
    div_curl = divergence(
        Cx, Cy, Cz, x, y, z, h * 10
    )  # Larger h for nested derivatives

    # Check if near zero
    tolerance = 1e-3  # Relaxed tolerance for nested numerical differentiation

    return abs(div_curl) < tolerance


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
    description="Verify curl(curl F) identity (Arts. 103-110)",
)
def identity_curl_curl(
    Fx: Callable[[float, float, float], float],
    Fy: Callable[[float, float, float], float],
    Fz: Callable[[float, float, float], float],
    x: float,
    y: float,
    z: float,
    h: float = 1e-6,
) -> dict[str, float | bool | Tuple[float, float, float]]:
    """
    Verify the vector identity: curl(curl F) = grad(div F) - nabla^2(F).

    Maxwell's identity (Arts. 103-110):
        curl(curl F) = grad(div F) - nabla^2(F)

    This is one of the most important vector identities in electromagnetism.
    It is used in deriving the wave equation from Maxwell's equations.

    In wave propagation (Part IV):
        curl(curl E) = -d(curl B)/dt = -d^2(E)/dt^2 (in vacuum)
        leading to: nabla^2(E) - (1/c^2) * d^2(E)/dt^2 = 0

    Args:
        Fx, Fy, Fz: Vector field component functions.
        x, y, z: Point coordinates (cm).
        h: Step size for numerical differentiation (cm).

    Returns:
        Dictionary containing:
            - 'curl_curl': curl(curl F) vector
            - 'grad_div': grad(div F) vector
            - 'vec_laplacian': nabla^2(F) vector
            - 'rhs': grad(div F) - nabla^2(F) (should equal curl(curl F))
            - 'error': Maximum absolute error between LHS and RHS
            - 'verified': True if identity holds within tolerance

    Reference:
        Part I, Arts. 103-110: Vector calculus identities.

    Example:
        >>> def Fx(x,y,z): return x**2 - y**2
        >>> def Fy(x,y,z): return 2*x*y
        >>> def Fz(x,y,z): return 0.0
        >>> result = identity_curl_curl(Fx, Fy, Fz, 1.0, 1.0, 0.0)
        >>> print(f"Verified: {result['verified']}")
    """
    # Compute curl of F
    curl_x, curl_y, curl_z = curl(Fx, Fy, Fz, x, y, z, h)

    # Create functions for curl components
    def Cx(px, py, pz):
        return curl(Fx, Fy, Fz, px, py, pz, h)[0]

    def Cy(px, py, pz):
        return curl(Fx, Fy, Fz, px, py, pz, h)[1]

    def Cz(px, py, pz):
        return curl(Fx, Fy, Fz, px, py, pz, h)[2]

    # LHS: curl(curl F)
    curl_curl = curl(Cx, Cy, Cz, x, y, z, h * 10)

    # Compute divergence of F
    div_F = divergence(Fx, Fy, Fz, x, y, z, h)

    # Create function for divergence
    def div_func(px, py, pz):
        return divergence(Fx, Fy, Fz, px, py, pz, h)

    # RHS term 1: grad(div F)
    grad_div = gradient(div_func, x, y, z, h * 10)

    # RHS term 2: vector Laplacian
    vec_laplacian = vector_laplacian(Fx, Fy, Fz, x, y, z, h)

    # RHS: grad(div F) - nabla^2(F)
    rhs = (
        grad_div[0] - vec_laplacian[0],
        grad_div[1] - vec_laplacian[1],
        grad_div[2] - vec_laplacian[2],
    )

    # Compute error
    error = max(
        abs(curl_curl[0] - rhs[0]),
        abs(curl_curl[1] - rhs[1]),
        abs(curl_curl[2] - rhs[2]),
    )

    tolerance = 1e-2  # Relaxed tolerance for nested numerical differentiation

    return {
        "curl_curl": curl_curl,
        "grad_div": grad_div,
        "vec_laplacian": vec_laplacian,
        "rhs": rhs,
        "error": error,
        "verified": error < tolerance,
    }


__all__ = [
    # Core operators
    "gradient",
    "divergence",
    "curl",
    "laplacian",
    "vector_laplacian",
    # Vector identity verifications
    "identity_curl_grad_zero",
    "identity_div_curl_zero",
    "identity_curl_curl",
]

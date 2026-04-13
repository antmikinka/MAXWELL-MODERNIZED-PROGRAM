"""maxwell.math.potential_theorems — Surface integrals and potential theorems (Arts. 79-81, 83, 111).

Implements Maxwell's surface integral formulations and potential theory
foundations used throughout Part I (Electrostatics) and Part II (Electrokinematics).

Surface Integrals (Arts. 79-81):
    Maxwell introduces the surface integral as the foundation for understanding
    electric induction through surfaces. The surface integral of electric induction
    is central to Gauss's law and the characterization of fields at boundaries.

    - Art. 79-80: Definition and computation of surface integral of induction
    - Art. 81: Characteristic equation at a surface (Gauss's law form)

Potential Mean Value Theorem (Art. 83):
    For a charge-free region, the potential at the center of a sphere equals
    the mean value of the potential over the sphere's surface. This is a
    consequence of Laplace's equation.

Field Line Mechanics (Art. 111):
    Maxwell's mechanical interpretation of field lines, where tension along
    lines of force and pressure perpendicular to them explain electrostatic
    and magnetic forces through the stress tensor.

Electric Current Theory (Arts. 231-240, 242-244):
    Fundamental definitions and properties of electric current, including
    direction conventions, magnetic/chemical/thermal effects, and EMF.

    - Arts. 231-233: Definition and measurement of current
    - Arts. 234-236: Direction and properties of current flow
    - Arts. 237-240: Effects of current (magnetic, chemical, thermal)
    - Arts. 242-243: Electromotive force definition
    - Art. 244: Methods of measuring EMF

All calculations use CGS units by default.

Category: B (user_original) — Maxwell's theoretical formulations with modern implementation.

References:
    Part I, Arts. 79-81: Surface integrals and Gauss's law.
    Part I, Art. 83: Mean value theorem for potential.
    Part I, Art. 111: Field line mechanics and stress.
    Part II, Arts. 231-240: Electric current theory.
    Part II, Arts. 242-244: Electromotive force.
"""

from __future__ import annotations

from typing import Callable, Tuple, Optional, Union
import numpy as np
from numpy.typing import ArrayLike

from maxwell.meta.citation import maxwell_cite


# Type aliases
VectorField = Tuple[Callable[[float, float, float], float],
                    Callable[[float, float, float], float],
                    Callable[[float, float, float], float]]
ScalarField = Callable[[float, float, float], float]


@maxwell_cite(
    79, 80,
    part=1, chapter="On the Surface-Integral of the Electric Induction",
    theory_class="maxwell_original",
    description="Compute surface integral of electric induction (Arts. 79-80)",
)
def surface_integral_flux(
    Dx: Callable[[float, float, float], float],
    Dy: Callable[[float, float, float], float],
    Dz: Callable[[float, float, float], float],
    r_func: Callable[[float, float], Tuple[float, float, float]],
    theta_range: Tuple[float, float],
    phi_range: Tuple[float, float],
    n_theta: int = 50,
    n_phi: int = 50,
) -> float:
    """
    Compute the surface integral of electric induction (electric displacement).

    Maxwell's formulation (Arts. 79-80):
        The surface integral of electric induction is:
            Q = ∬(D · n) dS = ∬(Dx·dy·dz + Dy·dz·dx + Dz·dx·dy)

        In parametric form with parameters (u, v):
            Q = ∬ D(r(u,v)) · (∂r/∂u × ∂r/∂v) du dv

        For a sphere parameterized by (θ, φ):
            dS = R² sin(θ) dθ dφ
            n = (sin(θ)cos(φ), sin(θ)sin(φ), cos(θ))

    Args:
        Dx, Dy, Dz: Components of electric displacement D (statcoulombs/cm²).
        r_func: Parameterization r(theta, phi) -> (x, y, z) in cm.
        theta_range: Range of theta parameter (radians), e.g., (0, π).
        phi_range: Range of phi parameter (radians), e.g., (0, 2π).
        n_theta: Number of discretization points in theta direction.
        n_phi: Number of discretization points in phi direction.

    Returns:
        Surface integral value Q (statcoulombs).

    Reference:
        Part I, Arts. 79-80: Definition of surface integral of induction.

    Example:
        >>> # Flux through sphere of radius R centered at origin
        >>> R = 10.0  # cm
        >>> def r(theta, phi):
        ...     return (R * np.sin(theta) * np.cos(phi),
        ...             R * np.sin(theta) * np.sin(phi),
        ...             R * np.cos(theta))
        >>> # Radial field from point charge at origin
        >>> def Dx(x,y,z): r3 = (x**2+y**2+z**2)**1.5; return x / r3 if r3 > 0 else 0
        >>> def Dy(x,y,z): r3 = (x**2+y**2+z**2)**1.5; return y / r3 if r3 > 0 else 0
        >>> def Dz(x,y,z): r3 = (x**2+y**2+z**2)**1.5; return z / r3 if r3 > 0 else 0
        >>> Q = surface_integral_flux(Dx, Dy, Dz, r, (0, np.pi), (0, 2*np.pi))
        >>> print(f"Total flux: {Q:.4f} (should equal 4π for unit charge)")
    """
    theta_min, theta_max = theta_range
    phi_min, phi_max = phi_range

    # Discretize parameters
    theta_vals = np.linspace(theta_min, theta_max, n_theta)
    phi_vals = np.linspace(phi_min, phi_max, n_phi)
    dtheta = (theta_max - theta_min) / (n_theta - 1)
    dphi = (phi_max - phi_min) / (n_phi - 1)

    total_flux = 0.0

    for i in range(n_theta):
        for j in range(n_phi):
            theta = theta_vals[i]
            phi = phi_vals[j]

            # Get position on surface
            x, y, z = r_func(theta, phi)

            # Compute tangent vectors ∂r/∂theta and ∂r/∂phi
            h = 1e-8  # Small step for numerical differentiation
            x_t, y_t, z_t = r_func(theta + h, phi)
            x_p, y_p, z_p = r_func(theta, phi + h)

            # Tangent vectors
            dr_dtheta = ((x_t - x) / h, (y_t - y) / h, (z_t - z) / h)
            dr_dphi = ((x_p - x) / h, (y_p - y) / h, (z_p - z) / h)

            # Normal vector dS = (∂r/∂theta × ∂r/∂phi) dtheta dphi
            # Cross product gives unnormalized normal times area element
            nx = dr_dtheta[1] * dr_dphi[2] - dr_dtheta[2] * dr_dphi[1]
            ny = dr_dtheta[2] * dr_dphi[0] - dr_dtheta[0] * dr_dphi[2]
            nz = dr_dtheta[0] * dr_dphi[1] - dr_dtheta[1] * dr_dphi[0]

            # D · dS
            D_dot_n = Dx(x, y, z) * nx + Dy(x, y, z) * ny + Dz(x, y, z) * nz

            total_flux += D_dot_n * dtheta * dphi

    return total_flux


@maxwell_cite(
    81,
    part=1, chapter="On the Surface-Integral of the Electric Induction",
    theory_class="maxwell_original",
    description="Characteristic equation at a surface - Gauss's law (Art. 81)",
)
def gauss_law_surface(
    Dx: Callable[[float, float, float], float],
    Dy: Callable[[float, float, float], float],
    Dz: Callable[[float, float, float], float],
    surface_type: str,
    surface_params: dict,
    n_points: int = 100,
) -> dict:
    """
    Compute the characteristic equation at a surface (Gauss's law).

    Maxwell's formulation (Art. 81):
        The surface integral of electric induction over a closed surface
        equals 4π times the total charge enclosed (in CGS units):
            ∯ D · n dS = 4π Q_enclosed

        For a surface with surface charge density sigma:
            D_above · n - D_below · n = 4π sigma

    Args:
        Dx, Dy, Dz: Components of electric displacement D (statcoulombs/cm²).
        surface_type: Type of surface ('sphere', 'cylinder', 'plane').
        surface_params: Parameters for the surface:
            - sphere: {'center': (x,y,z), 'radius': R}
            - cylinder: {'axis': 'x'|'y'|'z', 'center': (y,z)|etc, 'radius': R, 'length': L}
            - plane: {'normal': (nx,ny,nz), 'point': (x0,y0,z0), 'size': L}
        n_points: Number of discretization points for integration.

    Returns:
        Dictionary containing:
            - 'flux': Total surface integral value
            - 'enclosed_charge': Q_enclosed = flux / (4π)
            - 'surface_type': Type of surface computed
            - 'surface_area': Computed surface area

    Reference:
        Part I, Art. 81: Characteristic equation at a surface.

    Example:
        >>> # Point charge at origin, compute flux through sphere
        >>> def Dx(x,y,z):
        ...     r2 = x**2 + y**2 + z**2
        ...     return x / r2**1.5 if r2 > 0 else 0
        >>> def Dy(x,y,z):
        ...     r2 = x**2 + y**2 + z**2
        ...     return y / r2**1.5 if r2 > 0 else 0
        >>> def Dz(x,y,z):
        ...     r2 = x**2 + y**2 + z**2
        ...     return z / r2**1.5 if r2 > 0 else 0
        >>> result = gauss_law_surface(Dx, Dy, Dz, 'sphere', {'center': (0,0,0), 'radius': 10.0})
        >>> print(f"Enclosed charge: {result['enclosed_charge']:.4f}")
    """
    from maxwell.math.vector_operators import divergence

    if surface_type == 'sphere':
        center = surface_params.get('center', (0.0, 0.0, 0.0))
        R = surface_params['radius']
        cx, cy, cz = center

        def r_func(theta, phi):
            return (
                cx + R * np.sin(theta) * np.cos(phi),
                cy + R * np.sin(theta) * np.sin(phi),
                cz + R * np.cos(theta)
            )

        # For sphere: dS = R² sin(θ) dθ dφ, n = (sin(θ)cos(φ), sin(θ)sin(φ), cos(θ))
        flux = surface_integral_flux(
            Dx, Dy, Dz, r_func,
            (0, np.pi), (0, 2 * np.pi),
            n_theta=n_points, n_phi=n_points
        )
        area = 4 * np.pi * R**2

    elif surface_type == 'cylinder':
        axis = surface_params.get('axis', 'z')
        center = surface_params.get('center', (0.0, 0.0))
        R = surface_params['radius']
        L = surface_params.get('length', 10.0)

        # Cylinder along z-axis
        if axis == 'z':
            cy, cz = center

            def r_side(phi, z_param):
                return (
                    cy[0] + R * np.cos(phi),
                    cy[1] + R * np.sin(phi),
                    z_param
                )

            # Side surface
            flux_side = 0.0
            n_phi = n_points
            n_z = n_points

            for i in range(n_z):
                z_val = -L/2 + (L / (n_z - 1)) * i
                for j in range(n_phi):
                    phi = 2 * np.pi * j / (n_phi - 1)
                    x, y, z = r_side(phi, z_val)

                    # Normal is radial in xy plane
                    nx = np.cos(phi)
                    ny = np.sin(phi)
                    nz = 0.0

                    # dS = R dphi dz
                    dS = R * (2 * np.pi / (n_phi - 1)) * (L / (n_z - 1))
                    flux_side += (Dx(x, y, z) * nx + Dy(x, y, z) * ny) * dS

            # Top and bottom caps
            flux_top = 0.0
            flux_bottom = 0.0

            # Top cap at z = +L/2
            for i in range(n_points):
                r_val = R * i / (n_points - 1)
                for j in range(n_points):
                    phi = 2 * np.pi * j / (n_points - 1)
                    x = cy[0] + r_val * np.cos(phi)
                    y = cy[1] + r_val * np.sin(phi)
                    z = L / 2

                    dS = r_val * (2 * np.pi / (n_points - 1)) * (R / (n_points - 1))
                    flux_top += Dz(x, y, z) * dS

            # Bottom cap at z = -L/2 (normal points in -z direction)
            for i in range(n_points):
                r_val = R * i / (n_points - 1)
                for j in range(n_points):
                    phi = 2 * np.pi * j / (n_points - 1)
                    x = cy[0] + r_val * np.cos(phi)
                    y = cy[1] + r_val * np.sin(phi)
                    z = -L / 2

                    dS = r_val * (2 * np.pi / (n_points - 1)) * (R / (n_points - 1))
                    flux_bottom += -Dz(x, y, z) * dS

            flux = flux_side + flux_top + flux_bottom
            area = 2 * np.pi * R * L + 2 * np.pi * R**2

        else:
            raise NotImplementedError(f"Cylinder along {axis} axis not yet implemented")

    elif surface_type == 'plane':
        normal = np.array(surface_params['normal'])
        normal = normal / np.linalg.norm(normal)
        point = np.array(surface_params['point'])
        size = surface_params['size']

        # Create orthonormal basis on plane
        if abs(normal[2]) < 0.9:
            u = np.cross(normal, [0, 0, 1])
        else:
            u = np.cross(normal, [1, 0, 0])
        u = u / np.linalg.norm(u)
        v = np.cross(normal, u)

        flux = 0.0
        n_u = n_points
        n_v = n_points

        for i in range(n_u):
            for j in range(n_v):
                u_val = -size/2 + (size / (n_u - 1)) * i
                v_val = -size/2 + (size / (n_v - 1)) * j

                pos = point + u_val * u + v_val * v
                x, y, z = pos

                dS = (size / (n_u - 1)) * (size / (n_v - 1))
                flux += (Dx(x, y, z) * normal[0] +
                         Dy(x, y, z) * normal[1] +
                         Dz(x, y, z) * normal[2]) * dS

        area = size**2

    else:
        raise ValueError(f"Unknown surface type: {surface_type}")

    # Gauss's law: Q_enclosed = flux / (4π) in CGS
    enclosed_charge = flux / (4 * np.pi)

    return {
        'flux': flux,
        'enclosed_charge': enclosed_charge,
        'surface_type': surface_type,
        'surface_area': area,
    }


@maxwell_cite(
    83,
    part=1, chapter="On the Potential",
    theory_class="maxwell_original",
    description="Mean value theorem for potential over a sphere (Art. 83)",
)
def potential_mean_value(
    phi_func: Callable[[float, float, float], float],
    center: Tuple[float, float, float],
    radius: float,
    n_points: int = 100,
) -> dict:
    """
    Compute the mean value of potential over a spherical surface.

    Maxwell's theorem (Art. 83):
        If the potential satisfies Laplace's equation in a charge-free region,
        then the value of the potential at any point equals the mean value of
        the potential over any sphere centered at that point:
            phi(center) = (1 / 4πR²) ∯ phi dS

        This is a consequence of the harmonic property of solutions to
        Laplace's equation: nabla²phi = 0.

    Args:
        phi_func: Scalar potential function phi(x, y, z) (statvolts).
        center: Center of sphere (x, y, z) in cm.
        radius: Radius of sphere in cm.
        n_points: Number of discretization points for integration.

    Returns:
        Dictionary containing:
            - 'center_potential': phi(center)
            - 'surface_mean': Mean value of phi over sphere surface
            - 'difference': |phi(center) - surface_mean|
            - 'verified': True if mean value theorem holds (within tolerance)
            - 'sphere_surface_values': Array of phi values on surface

    Reference:
        Part I, Art. 83: Mean value of potential over a sphere.

    Example:
        >>> # Potential satisfying Laplace's equation (away from origin)
        >>> def phi(x, y, z):
        ...     return 1.0 / np.sqrt(x**2 + y**2 + z**2 + 0.01)
        >>> result = potential_mean_value(phi, (2.0, 0.0, 0.0), 0.5)
        >>> print(f"Center potential: {result['center_potential']:.6f}")
        >>> print(f"Surface mean: {result['surface_mean']:.6f}")
        >>> print(f"Verified: {result['verified']}")
    """
    cx, cy, cz = center
    R = radius

    # Compute potential at center
    center_potential = phi_func(cx, cy, cz)

    # Compute surface integral of potential using proper spherical integration
    # with midpoint rule for better accuracy
    total_potential = 0.0
    total_weight = 0.0
    surface_values = []

    n_theta = max(20, int(np.sqrt(n_points)))
    n_phi = max(20, n_points // n_theta)

    # Use midpoint rule for integration
    dtheta = np.pi / n_theta
    dphi = 2 * np.pi / n_phi

    for i in range(n_theta):
        # Midpoint of each theta cell
        theta = (i + 0.5) * dtheta
        sin_theta = np.sin(theta)

        for j in range(n_phi):
            # Midpoint of each phi cell
            phi = (j + 0.5) * dphi

            # Position on sphere surface
            x = cx + R * sin_theta * np.cos(phi)
            y = cy + R * sin_theta * np.sin(phi)
            z = cz + R * np.cos(theta)

            phi_val = phi_func(x, y, z)
            surface_values.append(phi_val)

            # dS = R² sin(θ) dθ dφ
            dS = R**2 * sin_theta * dtheta * dphi
            total_potential += phi_val * dS
            total_weight += dS

    # Surface area of sphere (for verification)
    surface_area = 4 * np.pi * R**2

    # Mean value = integral / area
    # Use computed weight for numerical robustness
    surface_mean = total_potential / total_weight if total_weight > 0 else 0.0

    # Difference
    difference = abs(center_potential - surface_mean)
    # Use relative tolerance based on magnitude
    tolerance = 1e-2 * max(abs(center_potential), abs(surface_mean), 1.0)

    verified = difference < tolerance

    return {
        'center_potential': center_potential,
        'surface_mean': surface_mean,
        'difference': difference,
        'verified': verified,
        'surface_area': surface_area,
        'surface_area_computed': total_weight,
        'sphere_surface_values': np.array(surface_values),
    }


@maxwell_cite(
    111,
    part=1, chapter="On the Action at a Distance Between Two Electrified Bodies",
    theory_class="maxwell_original",
    description="Mechanical action along lines of force (Art. 111)",
)
def field_line_mechanics(
    Ex: Callable[[float, float, float], float],
    Ey: Callable[[float, float, float], float],
    Ez: Callable[[float, float, float], float],
    point: Tuple[float, float, float],
    h: float = 1e-6,
) -> dict:
    """
    Compute mechanical properties of the field at a point (stress tensor).

    Maxwell's mechanical interpretation (Art. 111):
        Maxwell introduced the concept that electric field lines are under
        tension along their length and exert pressure perpendicular to them.
        This mechanical stress explains the forces between charged bodies.

        The Maxwell stress tensor components:
            T_ij = (1/4π) [E_i E_j - (1/2) δ_ij E²]

        Tension along field lines:
            T_parallel = E² / (8π)  (tension, pulling along field lines)

        Pressure perpendicular to field lines:
            T_perp = -E² / (8π)  (pressure, pushing perpendicular)

        Force density (from divergence of stress tensor):
            f = div(T) = rho E (force per unit volume)

    Args:
        Ex, Ey, Ez: Components of electric field E (statvolts/cm).
        point: Point (x, y, z) at which to compute stress.
        h: Step size for numerical differentiation (cm).

    Returns:
        Dictionary containing:
            - 'field_magnitude': |E| at the point
            - 'field_direction': Unit vector in direction of E
            - 'stress_tensor': 3x3 Maxwell stress tensor T_ij
            - 'tension_parallel': Tension along field lines (= E²/8π)
            - 'pressure_perp': Pressure perpendicular to field lines (= E²/8π)
            - 'force_density': div(T) = force per unit volume
            - 'energy_density': E²/(8π) energy per unit volume

    Reference:
        Part I, Art. 111: Mechanical action along lines of force.
        See also: Part I, Arts. 103-110 (stress tensor theory).

    Example:
        >>> # Field of point charge at origin
        >>> def Ex(x, y, z):
        ...     r2 = x**2 + y**2 + z**2
        ...     return x / r2**1.5 if r2 > 0 else 0
        >>> def Ey(x, y, z):
        ...     r2 = x**2 + y**2 + z**2
        ...     return y / r2**1.5 if r2 > 0 else 0
        >>> def Ez(x, y, z):
        ...     r2 = x**2 + y**2 + z**2
        ...     return z / r2**1.5 if r2 > 0 else 0
        >>> result = field_line_mechanics(Ex, Ey, Ez, (1.0, 0.0, 0.0))
        >>> print(f"Field magnitude: {result['field_magnitude']:.4f}")
        >>> print(f"Tension: {result['tension_parallel']:.4f}")
    """
    x, y, z = point

    # Compute field components at point
    Ex_val = Ex(x, y, z)
    Ey_val = Ey(x, y, z)
    Ez_val = Ez(x, y, z)

    # Field magnitude
    E_mag = np.sqrt(Ex_val**2 + Ey_val**2 + Ez_val**2)

    # Field direction (unit vector)
    if E_mag > 0:
        n = np.array([Ex_val / E_mag, Ey_val / E_mag, Ez_val / E_mag])
    else:
        n = np.array([0.0, 0.0, 0.0])

    # Energy density: u = E² / (8π)
    energy_density = E_mag**2 / (8 * np.pi)

    # Tension along field lines = energy density
    tension_parallel = energy_density

    # Pressure perpendicular = energy density (but opposite sign)
    pressure_perp = energy_density

    # Maxwell stress tensor: T_ij = (1/4π)[E_i E_j - (1/2)δ_ij E²]
    # Note: In CGS Gaussian units
    E_squared = E_mag**2
    factor = 1.0 / (4 * np.pi)

    stress_tensor = np.zeros((3, 3))

    # Diagonal components: T_ii = (1/4π)[E_i² - (1/2)E²]
    stress_tensor[0, 0] = factor * (Ex_val**2 - 0.5 * E_squared)
    stress_tensor[1, 1] = factor * (Ey_val**2 - 0.5 * E_squared)
    stress_tensor[2, 2] = factor * (Ez_val**2 - 0.5 * E_squared)

    # Off-diagonal components: T_ij = (1/4π) E_i E_j (for i != j)
    stress_tensor[0, 1] = stress_tensor[1, 0] = factor * Ex_val * Ey_val
    stress_tensor[0, 2] = stress_tensor[2, 0] = factor * Ex_val * Ez_val
    stress_tensor[1, 2] = stress_tensor[2, 1] = factor * Ey_val * Ez_val

    # Force density: f_i = ∂T_ij/∂x_j (Einstein summation)
    # Compute divergence of stress tensor numerically

    def Txx(px, py, pz):
        Ex_p = Ex(px, py, pz)
        Ey_p = Ey(px, py, pz)
        Ez_p = Ez(px, py, pz)
        E2 = Ex_p**2 + Ey_p**2 + Ez_p**2
        return factor * (Ex_p**2 - 0.5 * E2)

    def Txy(px, py, pz):
        return factor * Ex(px, py, pz) * Ey(px, py, pz)

    def Txz(px, py, pz):
        return factor * Ex(px, py, pz) * Ez(px, py, pz)

    def Tyx(px, py, pz):
        return factor * Ey(px, py, pz) * Ex(px, py, pz)

    def Tyy(px, py, pz):
        Ex_p = Ex(px, py, pz)
        Ey_p = Ey(px, py, pz)
        Ez_p = Ez(px, py, pz)
        E2 = Ex_p**2 + Ey_p**2 + Ez_p**2
        return factor * (Ey_p**2 - 0.5 * E2)

    def Tyz(px, py, pz):
        return factor * Ey(px, py, pz) * Ez(px, py, pz)

    def Tzx(px, py, pz):
        return factor * Ez(px, py, pz) * Ex(px, py, pz)

    def Tzy(px, py, pz):
        return factor * Ez(px, py, pz) * Ey(px, py, pz)

    def Tzz(px, py, pz):
        Ex_p = Ex(px, py, pz)
        Ey_p = Ey(px, py, pz)
        Ez_p = Ez(px, py, pz)
        E2 = Ex_p**2 + Ey_p**2 + Ez_p**2
        return factor * (Ez_p**2 - 0.5 * E2)

    # dfx/dx = dTxx/dx + dTxy/dy + dTxz/dz
    dTxx_dx = (Txx(x + h, y, z) - Txx(x - h, y, z)) / (2 * h)
    dTxy_dy = (Txy(x, y + h, z) - Txy(x, y - h, z)) / (2 * h)
    dTxz_dz = (Txz(x, y, z + h) - Txz(x, y, z - h)) / (2 * h)
    fx = dTxx_dx + dTxy_dy + dTxz_dz

    # dfy/dy = dTyx/dx + dTyy/dy + dTyz/dz
    dTyx_dx = (Tyx(x + h, y, z) - Tyx(x - h, y, z)) / (2 * h)
    dTyy_dy = (Tyy(x, y + h, z) - Tyy(x, y - h, z)) / (2 * h)
    dTyz_dz = (Tyz(x, y, z + h) - Tyz(x, y, z - h)) / (2 * h)
    fy = dTyx_dx + dTyy_dy + dTyz_dz

    # dfz/dz = dTzx/dx + dTzy/dy + dTzz/dz
    dTzx_dx = (Tzx(x + h, y, z) - Tzx(x - h, y, z)) / (2 * h)
    dTzy_dy = (Tzy(x, y + h, z) - Tzy(x, y - h, z)) / (2 * h)
    dTzz_dz = (Tzz(x, y, z + h) - Tzz(x, y, z - h)) / (2 * h)
    fz = dTzx_dx + dTzy_dy + dTzz_dz

    force_density = np.array([fx, fy, fz])

    return {
        'field_magnitude': E_mag,
        'field_direction': n,
        'stress_tensor': stress_tensor,
        'tension_parallel': tension_parallel,
        'pressure_perp': pressure_perp,
        'force_density': force_density,
        'energy_density': energy_density,
    }


@maxwell_cite(
    231, 232, 233,
    part=2, chapter="The Electric Current",
    theory_class="maxwell_original",
    description="Definition and measurement of electric current (Arts. 231-233)",
)
def current_definition(
    charge_func: Optional[Callable[[float], float]] = None,
    current_magnitude: Optional[float] = None,
    direction: Optional[Tuple[float, float, float]] = None,
    conductor_type: str = "metallic",
) -> dict:
    """
    Define and characterize an electric current.

    Maxwell's definition (Arts. 231-233):
        Electric current is the rate of transfer of electric charge:
            I = dQ/dt

        In CGS electromagnetic (emu) units:
            1 emu of current = 1 abcoulomb/second = 10 amperes

        In CGS electrostatic (esu) units:
            1 esu of current = 1 statcoulomb/second
            1 esu current = c CGS emu current (where c = speed of light)

        Maxwell describes the voltaic battery as producing a continuous
        current through the transference of electrification.

    Args:
        charge_func: Function Q(t) giving charge transferred vs time (statcoulombs).
        current_magnitude: Constant current value (esu: statcoulombs/second).
        direction: Direction of current flow as unit vector (dx, dy, dz).
        conductor_type: Type of conductor ('metallic', 'electrolytic', 'gaseous').

    Returns:
        Dictionary containing:
            - 'current_type': 'constant' | 'time_varying'
            - 'magnitude': Current magnitude I
            - 'magnitude_emu': Current in electromagnetic units
            - 'direction': Unit vector in direction of flow
            - 'conductor_type': Type of conductor
            - 'charge_transferred': Q(t) function or total charge
            - 'maxwell_description': Text describing the current per Maxwell

    Reference:
        Part II, Arts. 231-233: Definition of electric current.

    Example:
        >>> # Constant current of 1 esu/s in x-direction
        >>> result = current_definition(
        ...     current_magnitude=1.0,
        ...     direction=(1.0, 0.0, 0.0),
        ...     conductor_type="metallic"
        ... )
        >>> print(f"Current: {result['magnitude']} esu/s")
        >>> print(f"Current (emu): {result['magnitude_emu']} emu")
    """
    from scipy import constants as sci_const

    # Speed of light for unit conversion (cm/s)
    c_cgs = 2.99792458e10  # cm/s

    if current_magnitude is not None:
        # Constant current case
        current_type = "constant"
        magnitude = current_magnitude
        magnitude_emu = current_magnitude / c_cgs  # Convert esu to emu

        def charge_transferred(t):
            return magnitude * t

    elif charge_func is not None:
        # Time-varying current case
        current_type = "time_varying"

        def current_at_time(t):
            # Numerical derivative of charge
            h = 1e-9
            return (charge_func(t + h) - charge_func(t - h)) / (2 * h)

        magnitude = None  # Function of time
        magnitude_emu = None

        def charge_transferred(t):
            return charge_func(t)

    else:
        raise ValueError("Either current_magnitude or charge_func must be provided")

    # Normalize direction
    if direction is not None:
        dir_array = np.array(direction)
        dir_norm = np.linalg.norm(dir_array)
        if dir_norm > 0:
            direction_unit = dir_array / dir_norm
        else:
            direction_unit = None
    else:
        direction_unit = None

    # Maxwell's description based on conductor type
    descriptions = {
        "metallic": "Metallic conduction: Current flows through metal by movement of electric fluid",
        "electrolytic": "Electrolytic conduction: Current flows through liquid by ion transport (Art. 236)",
        "gaseous": "Gaseous conduction: Current flows through gas by ion and electron movement",
    }

    return {
        'current_type': current_type,
        'magnitude': magnitude,
        'magnitude_emu': magnitude_emu,
        'direction': direction_unit,
        'conductor_type': conductor_type,
        'charge_transferred': charge_transferred,
        'maxwell_description': descriptions.get(conductor_type, "Unknown conductor type"),
    }


@maxwell_cite(
    234, 235, 236,
    part=2, chapter="The Electric Current",
    theory_class="maxwell_original",
    description="Direction of current flow (Arts. 234-236)",
)
def current_direction(
    current_density: Callable[[float, float, float], Tuple[float, float, float]],
    surface_normal: Callable[[float, float, float], Tuple[float, float, float]],
    surface_params: dict,
    n_points: int = 50,
) -> dict:
    """
    Determine the direction and properties of current flow through a surface.

    Maxwell's analysis (Arts. 234-236):
        The direction of current flow is defined by the motion of positive
        electrification. In a conductor:

        - Current density J = (Jx, Jy, Jz) gives magnitude and direction
        - Total current I through surface S: I = ∬ J · n dS
        - Current flows from higher to lower potential in passive conductors

        Maxwell establishes that current is continuous in steady state and
        that its direction can be determined by the galvanometer.

    Args:
        current_density: Function J(x,y,z) -> (Jx, Jy, Jz) (esu/cm²/s).
        surface_normal: Function n(x,y,z) -> (nx, ny, nz) giving surface normal.
        surface_params: Parameters defining the integration surface.
        n_points: Number of discretization points.

    Returns:
        Dictionary containing:
            - 'total_current': Total current I through surface
            - 'current_density_field': Sample of J values
            - 'net_direction': Average direction of current flow
            - 'surface_integral': J · n integrated over surface
            - 'continuity_check': True if div(J) ≈ 0 (steady state)

    Reference:
        Part II, Arts. 234-236: Direction and properties of current.

    Example:
        >>> # Uniform current density through circular disk
        >>> def J(x, y, z): return (1.0, 0.0, 0.0)
        >>> def normal(x, y, z): return (1.0, 0.0, 0.0)
        >>> result = current_direction(J, normal, {'type': 'disk', 'radius': 1.0})
    """
    # Get surface type and parameters
    surface_type = surface_params.get('type', 'plane')

    if surface_type == 'plane':
        point = np.array(surface_params.get('point', [0.0, 0.0, 0.0]))
        size = surface_params.get('size', 1.0)

        # Create orthonormal basis on plane
        n0 = np.array(surface_normal(point[0], point[1], point[2]))
        n0 = n0 / np.linalg.norm(n0)

        if abs(n0[2]) < 0.9:
            u = np.cross(n0, [0, 0, 1])
        else:
            u = np.cross(n0, [1, 0, 0])
        u = u / np.linalg.norm(u)
        v = np.cross(n0, u)

        total_current = 0.0
        j_samples = []

        for i in range(n_points):
            for j in range(n_points):
                u_val = -size/2 + (size / (n_points - 1)) * i
                v_val = -size/2 + (size / (n_points - 1)) * j

                pos = point + u_val * u + v_val * v
                x, y, z = pos

                J_vec = np.array(current_density(x, y, z))
                n_vec = np.array(surface_normal(x, y, z))
                n_vec = n_vec / np.linalg.norm(n_vec)

                j_samples.append(J_vec)
                dS = (size / (n_points - 1))**2
                total_current += np.dot(J_vec, n_vec) * dS

    elif surface_type == 'disk':
        radius = surface_params.get('radius', 1.0)
        center = np.array(surface_params.get('center', [0.0, 0.0, 0.0]))
        normal_vec = np.array(surface_params.get('normal', [0.0, 0.0, 1.0]))
        normal_vec = normal_vec / np.linalg.norm(normal_vec)

        # Orthonormal basis
        if abs(normal_vec[2]) < 0.9:
            u = np.cross(normal_vec, [0, 0, 1])
        else:
            u = np.cross(normal_vec, [1, 0, 0])
        u = u / np.linalg.norm(u)
        v = np.cross(normal_vec, u)

        total_current = 0.0
        j_samples = []

        n_radial = n_points
        n_angular = n_points

        for i in range(n_radial):
            r = radius * i / (n_radial - 1)
            for j in range(n_angular):
                theta = 2 * np.pi * j / (n_angular - 1)

                pos = center + r * np.cos(theta) * u + r * np.sin(theta) * v
                x, y, z = pos

                J_vec = np.array(current_density(x, y, z))
                j_samples.append(J_vec)

                dS = r * (2 * np.pi / (n_angular - 1)) * (radius / (n_radial - 1))
                total_current += np.dot(J_vec, normal_vec) * dS
    else:
        raise NotImplementedError(f"Surface type {surface_type} not implemented")

    # Compute average direction
    if j_samples:
        j_array = np.array(j_samples)
        avg_direction = np.mean(j_array, axis=0)
        avg_norm = np.linalg.norm(avg_direction)
        if avg_norm > 0:
            net_direction = avg_direction / avg_norm
        else:
            net_direction = None
    else:
        net_direction = None

    # Continuity check (div J ≈ 0 for steady state)
    h = 1e-6
    J0 = current_density(0, 0, 0)

    Jx_h = current_density(h, 0, 0)[0]
    Jx_mh = current_density(-h, 0, 0)[0]
    dJx_dx = (Jx_h - Jx_mh) / (2 * h)

    Jy_h = current_density(0, h, 0)[1]
    Jy_mh = current_density(0, -h, 0)[1]
    dJy_dy = (Jy_h - Jy_mh) / (2 * h)

    Jz_h = current_density(0, 0, h)[2]
    Jz_mh = current_density(0, 0, -h)[2]
    dJz_dz = (Jz_h - Jz_mh) / (2 * h)

    div_J = dJx_dx + dJy_dy + dJz_dz
    continuity_holds = abs(div_J) < 1e-6

    return {
        'total_current': total_current,
        'current_density_sample': j_samples[:10] if j_samples else [],
        'net_direction': net_direction,
        'surface_integral': total_current,
        'divergence_J': div_J,
        'continuity_check': continuity_holds,
    }


@maxwell_cite(
    237, 238, 239, 240,
    part=2, chapter="The Electric Current",
    theory_class="maxwell_original",
    description="Magnetic, chemical, thermal effects of current (Arts. 237-240)",
)
def current_effects(
    current: float,
    resistance: Optional[float] = None,
    time: Optional[float] = None,
    electrolyte_params: Optional[dict] = None,
    coil_params: Optional[dict] = None,
) -> dict:
    """
    Compute the various effects of electric current.

    Maxwell's analysis (Arts. 237-240):

    1. Magnetic Effect (Art. 239):
        A current produces a magnetic field that acts on magnets.
        This is the principle of the galvanometer.

    2. Chemical Effect (Arts. 237-238):
        In electrolytes, current causes chemical decomposition.
        Different modes of current passage in solids vs liquids.

    3. Thermal Effect (implied by later articles):
        Current generates heat according to Joule's law (developed later).

    Args:
        current: Current magnitude I (esu/s or emu/s as specified).
        resistance: Resistance R for thermal effect calculation (CGS ohms).
        time: Duration for integrated effects (seconds).
        electrolyte_params: Parameters for electrolysis:
            - 'equivalent_weight': Chemical equivalent of substance
            - 'valence': Number of electrons in reaction
        coil_params: Parameters for magnetic effect:
            - 'n_turns': Number of turns in galvanometer coil
            - 'radius': Radius of coil (cm)
            - 'current_unit': 'esu' or 'emu'

    Returns:
        Dictionary containing:
            - 'magnetic_effect': Magnetic field produced / galvanometer deflection
            - 'chemical_effect': Mass of substance deposited/decomposed
            - 'thermal_effect': Heat generated (if resistance given)
            - 'maxwell_analysis': Text description of effects

    Reference:
        Part II, Arts. 237-240: Effects of electric current.

    Example:
        >>> # Galvanometer with 100 turns, radius 5 cm, current 0.01 emu
        >>> result = current_effects(
        ...     current=0.01,
        ...     coil_params={'n_turns': 100, 'radius': 5.0, 'current_unit': 'emu'}
        ... )
        >>> print(f"Magnetic field at center: {result['magnetic_effect']['B_center']}")
    """
    from scipy import constants as sci_const

    results = {}

    # Magnetic effect (Art. 239)
    if coil_params is not None:
        n_turns = coil_params.get('n_turns', 1)
        radius = coil_params.get('radius', 1.0)
        current_unit = coil_params.get('current_unit', 'emu')

        # Convert to emu if necessary
        if current_unit == 'esu':
            c_cgs = 2.99792458e10
            I_emu = current / c_cgs
        else:
            I_emu = current

        # Magnetic field at center of circular coil (in emu):
        # B = (2π n I) / R for single loop at center
        # For coil with n turns: B = (2π n N I) / R
        B_center = (2 * np.pi * n_turns * I_emu) / radius

        results['magnetic_effect'] = {
            'B_center': B_center,  # in gauss (emu)
            'n_turns': n_turns,
            'coil_radius': radius,
            'description': 'Magnetic field at center of galvanometer coil',
        }

        # Galvanometer deflection (simplified model)
        # Assuming Earth's horizontal field H ≈ 0.2 gauss
        H_earth = 0.2  # gauss
        if 'B_center' in results['magnetic_effect']:
            tan_theta = B_center / H_earth
            theta_rad = np.arctan(tan_theta)
            theta_deg = np.degrees(theta_rad)
            results['magnetic_effect']['deflection_deg'] = theta_deg

    # Chemical effect (Arts. 237-238)
    if electrolyte_params is not None and time is not None:
        eq_weight = electrolyte_params.get('equivalent_weight', 1.0)
        valence = electrolyte_params.get('valence', 1)

        # Faraday's law of electrolysis:
        # m = (I t M) / (n F)
        # In CGS: m = z Q where z is electrochemical equivalent

        # Faraday constant in CGS (abcoulombs per mole of electrons)
        F_emu = 96485.3329  # C/mol = 9648.5 abcoulomb/mol

        # Charge passed (convert to abcoulombs if current is in esu)
        Q_total = current * time  # statcoulomb-seconds if current in esu/s

        # Convert to emu (abcoulombs)
        c_cgs = 2.99792458e10
        Q_emu = Q_total / c_cgs

        # Mass deposited
        mass_deposited = (eq_weight * Q_emu) / F_emu

        results['chemical_effect'] = {
            'mass_deposited': mass_deposited,  # grams
            'equivalent_weight': eq_weight,
            'charge_passed': Q_emu,  # abcoulombs
            'description': 'Mass of substance deposited by electrolysis',
        }
    else:
        results['chemical_effect'] = {
            'description': 'No electrolysis parameters provided',
        }

    # Thermal effect (Joule heating)
    if resistance is not None and time is not None:
        # Joule's law: H = I² R t
        # In CGS, need to be careful about units

        # If current is in emu (abcoulombs/s = abamperes)
        # and resistance is in CGS electromagnetic units (abohms)
        # then heat is in ergs

        # Conversion: 1 joule = 10^7 ergs
        heat_emu = current**2 * resistance * time  # ergs if I in abamperes, R in abohms

        # Convert to joules for reference
        heat_joules = heat_emu / 1e7

        results['thermal_effect'] = {
            'heat_ergs': heat_emu,
            'heat_joules': heat_joules,
            'resistance': resistance,
            'time': time,
            'description': 'Heat generated by Joule heating (I²R)',
        }
    else:
        results['thermal_effect'] = {
            'description': 'No resistance or time provided for thermal calculation',
        }

    # Maxwell's synthesis
    results['maxwell_analysis'] = (
        f"Current of {current} produces:\n"
        f"  - Magnetic field detectable by galvanometer (Art. 239)\n"
        f"  - Chemical decomposition in electrolytes (Arts. 237-238)\n"
        f"  - Heat generation proportional to I²R (Joule's law)"
    )

    return results


@maxwell_cite(
    242, 243,
    part=2, chapter="Conduction and Resistance",
    theory_class="maxwell_original",
    description="Electromotive force definition (Arts. 242-243)",
)
def emf_definition(
    potential_high: float,
    potential_low: float,
    source_type: str = "voltaic",
    internal_resistance: Optional[float] = None,
    temperature_gradient: Optional[float] = None,
    contact_materials: Optional[Tuple[str, str]] = None,
) -> dict:
    """
    Define and compute electromotive force (EMF).

    Maxwell's definition (Arts. 242-243):
        Electromotive force (EMF) is the force that produces and maintains
        electric current. It is measured by the difference of potential
        between the terminals when no current flows:
            E = V_high - V_low

        EMF can arise from:
        - Voltaic cells (chemical action)
        - Thermoelectric effects (temperature differences)
        - Contact potentials (dissimilar materials)
        - Induction (changing magnetic fields, discussed later)

        Joule's law (Art. 242): The heat generated by current is
            H = I² R t = E I t (when E drives current through R)

    Args:
        potential_high: Higher electric potential (statvolts).
        potential_low: Lower electric potential (statvolts).
        source_type: Type of EMF source:
            - 'voltaic': Chemical battery
            - 'thermoelectric': Seebeck effect
            - 'contact': Contact potential
            - 'induced': Electromagnetic induction
        internal_resistance: Internal resistance of source (CGS ohms).
        temperature_gradient: Temperature difference for thermoelectric sources (K).
        contact_materials: Tuple of material names for contact potential.

    Returns:
        Dictionary containing:
            - 'emf': Electromotive force E (statvolts)
            - 'emf_emu': EMF in electromagnetic units (abvolts)
            - 'source_type': Type of EMF source
            - 'open_circuit_voltage': Voltage with no load
            - 'short_circuit_current': Current if terminals shorted
            - 'max_power': Maximum power deliverable
            - 'maxwell_description': Text description per Maxwell

    Reference:
        Part II, Arts. 242-243: Definition of electromotive force.

    Example:
        >>> # Voltaic cell with 1.5 V potential difference
        >>> result = emf_definition(
        ...     potential_high=1.5 / 299.792458,  # Convert V to statvolts
        ...     potential_low=0.0,
        ...     source_type="voltaic",
        ...     internal_resistance=0.1
        ... )
        >>> print(f"EMF: {result['emf']} statvolts = {result['emf_emu']} abvolts")
    """
    # Basic EMF
    emf = potential_high - potential_low

    # Convert to electromagnetic units (abvolts)
    # 1 statvolt = c abvolts where c = speed of light in cm/s
    c_cgs = 2.99792458e10  # cm/s
    emf_emu = emf * c_cgs  # abvolts

    # Open circuit voltage equals EMF
    open_circuit_voltage = emf

    # Short circuit current (if internal resistance known)
    if internal_resistance is not None and internal_resistance > 0:
        short_circuit_current = emf / internal_resistance
        max_power = emf**2 / (4 * internal_resistance)  # Max power transfer theorem
    else:
        short_circuit_current = None
        max_power = None

    # Source-specific analysis
    if source_type == "voltaic":
        description = (
            "Voltaic cell: EMF arises from chemical action in the battery. "
            "Maxwell describes the voltaic battery as maintaining a continuous "
            "current by transference of electrification (Arts. 232-233)."
        )
    elif source_type == "thermoelectric":
        if temperature_gradient is not None:
            # Seebeck coefficient (typical values ~10-100 microvolts/K)
            # In CGS: 1 microvolt/K = 1e-6 / 299.792458 statvolts/K
            seebeck_approx = 50e-6 / 299.792458  # statvolts/K
            estimated_emf = seebeck_approx * temperature_gradient
            description = (
                f"Thermoelectric source: EMF from Seebeck effect. "
                f"Temperature difference: {temperature_gradient} K. "
                f"Estimated Seebeck EMF: {estimated_emf:.2e} statvolts."
            )
        else:
            description = "Thermoelectric source: EMF from temperature gradient (Seebeck effect)."
    elif source_type == "contact":
        if contact_materials is not None:
            description = (
                f"Contact potential between {contact_materials[0]} and {contact_materials[1]}. "
                "Volta's law governs the contact force between different metals (Art. 246)."
            )
        else:
            description = "Contact potential: EMF from dissimilar materials in contact."
    elif source_type == "induced":
        description = (
            "Induced EMF: From changing magnetic flux (Faraday's law). "
            "E = -d(Phi)/dt (discussed in Part IV on Electromagnetism)."
        )
    else:
        description = "General EMF source."

    return {
        'emf': emf,
        'emf_emu': emf_emu,
        'emf_volts': emf * 299.792458,  # Convert statvolts to volts
        'source_type': source_type,
        'open_circuit_voltage': open_circuit_voltage,
        'short_circuit_current': short_circuit_current,
        'max_power': max_power,
        'internal_resistance': internal_resistance,
        'maxwell_description': description,
    }


@maxwell_cite(
    244,
    part=2, chapter="Conduction and Resistance",
    theory_class="maxwell_original",
    description="Methods of measuring electromotive force (Art. 244)",
)
def emf_measurement(
    measured_emf: float,
    measurement_method: str = "potentiometer",
    galvanometer_params: Optional[dict] = None,
    standard_cell_emf: Optional[float] = None,
    comparison_readings: Optional[list] = None,
) -> dict:
    """
    Methods for measuring electromotive force.

    Maxwell's methods (Art. 244):
        EMF can be measured by several methods:

        1. Potentiometer Method (preferred):
            Compare unknown EMF with a standard cell using a
            uniform resistance wire. At balance (null deflection):
                E_unknown / E_standard = L_unknown / L_standard

        2. Galvanometer Method:
            Pass current through known resistance and measure
            deflection. Requires knowledge of galvanometer constant.

        3. Electrometer Method:
            Direct measurement of potential difference using
            an absolute electrometer (Kelvin type).

    Args:
        measured_emf: The measured or nominal EMF value (statvolts).
        measurement_method: One of 'potentiometer', 'galvanometer', 'electrometer'.
        galvanometer_params: Parameters for galvanometer method:
            - 'resistance': Total circuit resistance
            - 'sensitivity': Deflection per unit current
        standard_cell_emf: Known standard cell EMF for comparison (statvolts).
        comparison_readings: List of readings for comparison method:
            [(length_std, deflection_std), (length_unknown, deflection_unknown)]

    Returns:
        Dictionary containing:
            - 'measured_emf': The EMF value
            - 'measurement_method': Method used
            - 'accuracy_estimate': Estimated measurement accuracy
            - 'method_description': Description of the method
            - 'calculated_emf': EMF calculated from readings (if provided)

    Reference:
        Part II, Art. 244: Methods of measuring electromotive force.

    Example:
        >>> # Potentiometer measurement with standard cell
        >>> result = emf_measurement(
        ...     measured_emf=1.018 / 299.792458,  # Weston cell ~1.018 V
        ...     measurement_method="potentiometer",
        ...     standard_cell_emf=1.018 / 299.792458,
        ...     comparison_readings=[(50.0, 0), (52.3, 0)]  # cm readings at null
        ... )
        >>> print(f"Unknown EMF: {result['calculated_emf']} statvolts")
    """
    results = {
        'measured_emf': measured_emf,
        'measurement_method': measurement_method,
    }

    if measurement_method == "potentiometer":
        results['method_description'] = (
            "Potentiometer method: Compare unknown EMF with standard cell "
            "using a uniform resistance wire. At balance, no current flows "
            "and the ratio of EMFs equals the ratio of lengths."
        )

        if comparison_readings is not None and len(comparison_readings) >= 2:
            L_std = comparison_readings[0][0]
            L_unknown = comparison_readings[1][0]

            if standard_cell_emf is not None:
                # E_unknown = E_standard * (L_unknown / L_std)
                calculated_emf = standard_cell_emf * (L_unknown / L_std)
                results['calculated_emf'] = calculated_emf

                # Potentiometer accuracy: typically 0.01% to 0.1%
                results['accuracy_estimate'] = "0.01% to 0.1% (high precision)"
                results['potentiometer_ratio'] = L_unknown / L_std

        else:
            results['accuracy_estimate'] = "0.01% to 0.1% (high precision)"

    elif measurement_method == "galvanometer":
        results['method_description'] = (
            "Galvanometer method: Pass current through known resistance "
            "and measure deflection. Requires calibration of galvanometer "
            "constant and knowledge of circuit resistance."
        )

        if galvanometer_params is not None:
            R_total = galvanometer_params.get('resistance', 1.0)
            sensitivity = galvanometer_params.get('sensitivity', 1.0)

            # I = E / R, deflection = sensitivity * I
            # So E = deflection * R / sensitivity
            results['galvanometer_formula'] = "E = theta * R / k"
            results['circuit_resistance'] = R_total
            results['sensitivity'] = sensitivity

        # Galvanometer accuracy: typically 1% to 5%
        results['accuracy_estimate'] = "1% to 5% (moderate precision)"

    elif measurement_method == "electrometer":
        results['method_description'] = (
            "Electrometer method: Direct measurement using an absolute "
            "electrometer (Kelvin type). Measures force between charged "
            "plates to determine potential difference absolutely."
        )

        # Electrometer accuracy: typically 0.1% to 1%
        results['accuracy_estimate'] = "0.1% to 1% (good precision)"

    else:
        results['method_description'] = "Unknown measurement method."
        results['accuracy_estimate'] = "Unknown"

    # Convert to practical units
    results['emf_volts'] = measured_emf * 299.792458
    results['emf_abvolts'] = measured_emf * 2.99792458e10

    return results


__all__ = [
    # Surface integrals and potential theorems (Arts. 79-81, 83, 111)
    "surface_integral_flux",
    "gauss_law_surface",
    "potential_mean_value",
    "field_line_mechanics",

    # Electric current theory (Arts. 231-240, 242-244)
    "current_definition",
    "current_direction",
    "current_effects",
    "emf_definition",
    "emf_measurement",
]

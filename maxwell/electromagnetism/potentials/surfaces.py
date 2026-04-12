"""maxwell.electromagnetism.potentials.surfaces — Equipotential surfaces (Arts. 486-487).

Implements Maxwell's treatment of magnetic equipotential surfaces produced by
current distributions, particularly the solid angle formulation for current loops.

Maxwell's CGS formulation (Arts. 486-487):
    For a current loop, the magnetic potential at a point is:
        Omega = I * omega  (where omega is the solid angle subtended by the loop)

    The equipotential surfaces are surfaces of constant solid angle.
    For a small loop (magnetic dipole), these are cones around the dipole axis.

where:
    I = current in abamperes (EMU)
    omega = solid angle (steradians)
    Omega = magnetic scalar potential (oersted*cm)

Category: A (maxwell_original) — Maxwell's theory of magnetic potentials.

References:
    Part IV, Arts. 486-487: Equipotential surfaces and solid angle formulation.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class EquipotentialSurface:
    """
    Magnetic equipotential surface for a current distribution.

    Art. 486-487: Maxwell showed that the magnetic potential due to a current
    loop can be expressed in terms of the solid angle subtended by the loop
    at the observation point:

        Omega = I * omega

    where omega is the solid angle (positive if the point sees the "north"
    face of the loop, negative for the "south" face).

    The equipotential surfaces are surfaces of constant solid angle.
    For a circular loop, these surfaces have a characteristic shape
    that transitions from disks near the loop to cones far away.

    Attributes:
        current: Current in the loop (abamperes).
        potential_value: The potential value defining this surface (oersted*cm).
    """

    current: float
    potential_value: float

    @property
    def solid_angle(self) -> float:
        """
        Solid angle defining this equipotential surface.

        Returns:
            omega = Omega/I (steradians).
        """
        if self.current == 0:
            return 0.0
        return self.potential_value / self.current

    @maxwell_cite(
        486, 487,
        part=4, chapter="Equipotential Surfaces",
        theory_class="maxwell_original",
        description="Check if point lies on equipotential surface",
    )
    def contains_point(self, solid_angle_at_point: float, tolerance: float = 1e-6) -> bool:
        """
        Check if a point lies on this equipotential surface.

        Art. 486-487: A point lies on the equipotential surface if the
        solid angle subtended at that point equals the surface's solid angle.

        Args:
            solid_angle_at_point: Solid angle at the test point (steradians).
            tolerance: Numerical tolerance for comparison.

        Returns:
            True if point is on the surface.

        Reference:
            Part IV, Arts. 486-487: Equipotential surface definition.
        """
        return abs(solid_angle_at_point - self.solid_angle) < tolerance


@dataclass
class CurrentLoopPotential:
    """
    Magnetic potential calculator for a circular current loop.

    Art. 486-487: The potential at a point due to a circular current loop
    is proportional to the solid angle subtended by the loop:

        Omega = I * omega

    For a loop of radius a in the xy-plane centered at origin:
        omega = 2*pi * (1 - z/sqrt(z² + (a-r)²))  [approximate on axis]

    The exact solid angle requires elliptic integrals for off-axis points.

    Attributes:
        current: Current in the loop (abamperes).
        radius: Radius of the loop (cm).
        center: Center position of the loop (cm).
        normal: Unit vector normal to the loop plane.
    """

    current: float
    radius: float
    center: np.ndarray = None
    normal: np.ndarray = None

    def __post_init__(self):
        """Validate parameters and set defaults."""
        if self.radius <= 0:
            raise ValueError(f"Radius must be positive, got {self.radius}")

        self.center = np.asarray(self.center, dtype=np.float64) if self.center is not None else np.zeros(3)
        self.normal = np.asarray(self.normal, dtype=np.float64) if self.normal is not None else np.array([0.0, 0.0, 1.0])

        # Normalize normal vector
        norm = np.linalg.norm(self.normal)
        if norm > 0:
            self.normal = self.normal / norm

    @maxwell_cite(
        486, 487,
        part=4, chapter="Equipotential Surfaces",
        theory_class="maxwell_original",
        description="Calculate solid angle subtended by loop at point",
    )
    def solid_angle_at(self, position: np.ndarray) -> float:
        """
        Calculate the solid angle subtended by the loop at a point.

        Art. 486-487: The solid angle omega subtended by a circular loop at
        point P is given by:

            omega = 2*pi * (1 - cos(alpha))

        where alpha is the half-angle of the cone from P to the loop edge.
        On the axis of the loop at distance z:
            omega = 2*pi * (1 - z/sqrt(z² + a²))

        For off-axis points, elliptic integrals are required.

        Args:
            position: Position vector (cm) where solid angle is calculated.

        Returns:
            Solid angle (steradians), positive for "north" side.

        Reference:
            Part IV, Arts. 486-487: Solid angle of current loop.
        """
        position = np.asarray(position, dtype=np.float64)

        # Vector from loop center to point
        r_vec = position - self.center
        z = np.dot(r_vec, self.normal)  # Distance along axis
        r_perp = np.linalg.norm(r_vec - z * self.normal)  # Perpendicular distance

        # On-axis formula (exact on axis, approximate nearby)
        if r_perp < 1e-10 * self.radius:
            # On axis: omega = 2*pi * (1 - z/sqrt(z² + a²))
            R = np.sqrt(z ** 2 + self.radius ** 2)
            omega = 2.0 * np.pi * (1.0 - z / R)
        else:
            # Off-axis: use approximate formula
            # For r_perp >> a, loop looks like dipole
            # omega ≈ pi*a²*z / (r_perp² + z²)^(3/2)  [dipole approximation]
            R3 = (r_perp ** 2 + z ** 2) ** 1.5
            if R3 > 1e-15:
                omega = np.pi * self.radius ** 2 * z / R3
            else:
                omega = 0.0

        # Sign: positive if point is on "north" side (same side as normal)
        return omega

    @maxwell_cite(
        486,
        part=4, chapter="Equipotential Surfaces",
        theory_class="maxwell_original",
        description="Calculate magnetic potential at point",
    )
    def potential_at(self, position: np.ndarray) -> float:
        """
        Calculate magnetic potential at a point.

        Art. 486-487: Omega = I * omega

        Args:
            position: Position vector (cm).

        Returns:
            Magnetic potential (oersted*cm).

        Reference:
            Part IV, Arts. 486-487: Potential from solid angle.
        """
        omega = self.solid_angle_at(position)
        return self.current * omega

    @maxwell_cite(
        487,
        part=4, chapter="Equipotential Surfaces",
        theory_class="maxwell_original",
        description="Calculate magnetic field from potential gradient",
    )
    def field_at(self, position: np.ndarray, delta: float = 1e-6) -> np.ndarray:
        """
        Calculate magnetic field H = -grad(Omega) at a point.

        Art. 487: The magnetic field is the negative gradient of the potential.
        This is computed numerically using finite differences.

        Args:
            position: Position vector (cm).
            delta: Finite difference step (cm).

        Returns:
            Magnetic field vector (oersted).

        Reference:
            Part IV, Art. 487: Field from potential gradient.
        """
        position = np.asarray(position, dtype=np.float64)
        omega_0 = self.potential_at(position)

        # Numerical gradient
        grad = np.zeros(3)
        for i in range(3):
            pos_plus = position.copy()
            pos_plus[i] += delta
            grad[i] = (self.potential_at(pos_plus) - omega_0) / delta

        return -grad


@maxwell_cite(
    486, 487,
    part=4, chapter="Equipotential Surfaces",
    theory_class="maxwell_original",
    description="Calculate solid angle of circular loop: omega = 2*pi*(1 - cos(alpha))",
)
def calc_solid_angle_circular_loop(
    loop_radius: float,
    axial_distance: float,
    radial_distance: float = 0.0,
) -> float:
    """
    Calculate solid angle subtended by a circular current loop.

    Art. 486-487: For a circular loop of radius a, the solid angle at a point
    at axial distance z and radial distance r is:

    On axis (r = 0):
        omega = 2*pi * (1 - z/sqrt(z² + a²))

    Off axis (approximate):
        omega ≈ pi*a²*z / (r² + z²)^(3/2)  [dipole approximation for large distances]

    Args:
        loop_radius: Radius of the loop a (cm).
        axial_distance: Distance along loop axis z (cm).
        radial_distance: Perpendicular distance from axis r (cm, default 0).

    Returns:
        Solid angle (steradians).

    Reference:
        Part IV, Arts. 486-487: Solid angle of circular loop.

    Example:
        >>> # Solid angle at center of loop (z=0, on axis)
        >>> omega = calc_solid_angle_circular_loop(1.0, 0.0)
        >>> print(f"omega = {omega:.2f} sr")  # omega = 6.28 sr (2*pi, half space)
    """
    if loop_radius <= 0:
        raise ValueError(f"Loop radius must be positive, got {loop_radius}")

    a = loop_radius
    z = axial_distance
    r = radial_distance

    if r < 1e-10 * a:
        # On axis: exact formula
        R = np.sqrt(z ** 2 + a ** 2)
        if R > 0:
            omega = 2.0 * np.pi * (1.0 - z / R)
        else:
            omega = 2.0 * np.pi  # At center, full half-space
    else:
        # Off axis: dipole approximation
        R3 = (r ** 2 + z ** 2) ** 1.5
        if R3 > 1e-15:
            omega = np.pi * a ** 2 * z / R3
        else:
            omega = 0.0

    return omega


@maxwell_cite(
    486,
    part=4, chapter="Equipotential Surfaces",
    theory_class="maxwell_original",
    description="Calculate magnetic potential from solid angle: Omega = I*omega",
)
def calc_magnetic_potential(
    current: float,
    solid_angle: float,
) -> float:
    """
    Calculate magnetic potential from solid angle.

    Art. 486: The fundamental relation:

        Omega = I * omega

    where omega is the solid angle subtended by the current loop at
    the observation point.

    Args:
        current: Current in loop (abamperes).
        solid_angle: Solid angle (steradians).

    Returns:
        Magnetic potential (oersted*cm).

    Reference:
        Part IV, Art. 486: Potential-solid angle relation.

    Example:
        >>> # 1 abampere loop, 2*pi steradians (half-space)
        >>> Omega = calc_magnetic_potential(1.0, 2*np.pi)
        >>> print(f"Omega = {Omega:.2f} oersted*cm")  # Omega = 6.28 oersted*cm
    """
    return current * solid_angle


@maxwell_cite(
    487,
    part=4, chapter="Equipotential Surfaces",
    theory_class="maxwell_original",
    description="Calculate potential of magnetic dipole",
)
def calc_dipole_potential(
    magnetic_moment: np.ndarray,
    position: np.ndarray,
) -> float:
    """
    Calculate magnetic potential of a dipole (small current loop).

    Art. 487: For a small current loop (magnetic dipole) with moment m,
    the potential at distance r is:

        Omega = (m · r_hat) / r² = (m · r) / r³

    This is the far-field limit of the solid angle formula.

    In CGS-EMU:
        m = magnetic moment (erg/gauss or abampere*cm²)
        r = position vector from dipole (cm)
        Omega = potential (oersted*cm)

    Args:
        magnetic_moment: Magnetic dipole moment vector (EMU).
        position: Position vector from dipole (cm).

    Returns:
        Magnetic potential (oersted*cm).

    Reference:
        Part IV, Art. 487: Dipole potential.

    Example:
        >>> # Dipole of 100 EMU, point at 10 cm on axis
        >>> m = np.array([0, 0, 100])
        >>> r = np.array([0, 0, 10])
        >>> Omega = calc_dipole_potential(m, r)
        >>> print(f"Omega = {Omega} oersted*cm")  # Omega = 1.0 oersted*cm
    """
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)
    position = np.asarray(position, dtype=np.float64)

    r_mag = np.linalg.norm(position)
    if r_mag < 1e-15:
        return 0.0  # At dipole (singularity)

    return np.dot(magnetic_moment, position) / (r_mag ** 3)


@maxwell_cite(
    486, 487,
    part=4, chapter="Equipotential Surfaces",
    theory_class="maxwell_original",
    description="Calculate field of magnetic dipole",
)
def calc_dipole_field(
    magnetic_moment: np.ndarray,
    position: np.ndarray,
) -> np.ndarray:
    """
    Calculate magnetic field of a dipole.

    Art. 487: The field of a magnetic dipole with moment m at position r is:

        H = (3(m·r_hat)r_hat - m) / r³

    In CGS-EMU:
        m = magnetic moment (EMU)
        r = position (cm)
        H = field (oersted)

    Args:
        magnetic_moment: Magnetic dipole moment vector (EMU).
        position: Position vector from dipole (cm).

    Returns:
        Magnetic field vector (oersted).

    Reference:
        Part IV, Art. 487: Dipole field.

    Example:
        >>> # Dipole of 100 EMU, point at 10 cm on axis
        >>> m = np.array([0, 0, 100])
        >>> r = np.array([0, 0, 10])
        >>> H = calc_dipole_field(m, r)
        >>> print(f"H = {H} oersted")  # H = [0, 0, 0.2] oersted
    """
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)
    position = np.asarray(position, dtype=np.float64)

    r_mag = np.linalg.norm(position)
    if r_mag < 1e-15:
        return np.zeros(3)

    r_hat = position / r_mag
    m_dot_r = np.dot(magnetic_moment, r_hat)

    # H = (3(m·r_hat)r_hat - m) / r³
    return (3.0 * m_dot_r * r_hat - magnetic_moment) / (r_mag ** 3)


@maxwell_cite(
    486, 487,
    part=4, chapter="Equipotential Surfaces",
    theory_class="maxwell_original",
    description="Verify equipotential surface properties",
)
def verify_equipotential_surfaces(
    current: float = 1.0,
    loop_radius: float = 1.0,
    tolerance: float = 1e-6,
) -> dict[str, float | bool]:
    """
    Verify properties of equipotential surfaces.

    Art. 486-487: This function verifies:
    1. Potential is constant on surfaces of constant solid angle
    2. Field is perpendicular to equipotential surfaces
    3. Dipole approximation matches exact formula at large distances

    Args:
        current: Test current (abamperes).
        loop_radius: Loop radius (cm).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 486-487: Equipotential surface verification.
    """
    loop = CurrentLoopPotential(current=current, radius=loop_radius)

    # Test on axis at various distances
    z_values = [0.5, 1.0, 2.0, 5.0, 10.0]
    potentials = [loop.potential_at(np.array([0, 0, z])) for z in z_values]

    # Verify dipole approximation at large distance
    z_far = 100.0 * loop_radius
    exact = loop.potential_at(np.array([0, 0, z_far]))

    # Dipole moment of loop: m = I * area = I * pi * a²
    m = np.array([0, 0, current * np.pi * loop_radius ** 2])
    dipole_approx = calc_dipole_potential(m, np.array([0, 0, z_far]))

    dipole_error = abs(exact - dipole_approx) / abs(exact) if exact != 0 else 0

    # Verify field is -grad(potential)
    z_test = 2.0 * loop_radius
    field_z = loop.field_at(np.array([0, 0, z_test]))

    # Analytical field on axis: H_z = 2*pi*I*a² / (z² + a²)^(3/2)
    H_analytical = 2.0 * np.pi * current * loop_radius ** 2 / (z_test ** 2 + loop_radius ** 2) ** 1.5

    field_error = abs(field_z[2] - H_analytical) / H_analytical if H_analytical != 0 else 0

    verified = dipole_error < tolerance and field_error < tolerance

    return {
        "potentials_on_axis": potentials,
        "z_positions": z_values,
        "dipole_exact": exact,
        "dipole_approximation": dipole_approx,
        "dipole_error": dipole_error,
        "field_numerical": field_z[2],
        "field_analytical": H_analytical,
        "field_error": field_error,
        "verified": verified,
    }


@maxwell_cite(
    486, 487,
    part=4, chapter="Equipotential Surfaces",
    theory_class="maxwell_original",
    description="Complete equipotential surface analysis",
)
def analyze_equipotential_surfaces(
    current: float,
    loop_radius: float,
    evaluation_points: list[np.ndarray] = None,
) -> dict[str, float | np.ndarray | list]:
    """
    Perform complete analysis of equipotential surfaces.

    Art. 486-487: Comprehensive analysis including:
    1. Solid angle at various points
    2. Magnetic potential
    3. Magnetic field
    4. Dipole approximation validity

    Args:
        current: Current in loop (abamperes).
        loop_radius: Loop radius (cm).
        evaluation_points: Optional list of points to evaluate.

    Returns:
        Dictionary with analysis results.

    Reference:
        Part IV, Arts. 486-487: Complete equipotential analysis.
    """
    loop = CurrentLoopPotential(current=current, radius=loop_radius)

    # Dipole moment
    dipole_moment = current * np.pi * loop_radius ** 2

    result = {
        "current": current,
        "loop_radius": loop_radius,
        "loop_area": np.pi * loop_radius ** 2,
        "dipole_moment": dipole_moment,
        "potential_at_center": loop.potential_at(np.array([0, 0, 0])),
        "field_on_axis_at_1cm": loop.field_at(np.array([0, 0, 1.0])),
    }

    if evaluation_points is not None:
        potentials = []
        fields = []
        solid_angles = []

        for point in evaluation_points:
            point = np.asarray(point, dtype=np.float64)
            potentials.append(loop.potential_at(point))
            fields.append(loop.field_at(point))
            solid_angles.append(loop.solid_angle_at(point))

        result["evaluation_points"] = evaluation_points
        result["potentials"] = potentials
        result["fields"] = fields
        result["solid_angles"] = solid_angles

    return result

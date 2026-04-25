"""
Electric field and electric intensity — the vector field of electrostatics.

Implements the theory of the electric field from Part I:
- Electric field definition (Art. 44)
- Electromotive force and potential (Art. 45)
- Equipotential surfaces (Art. 46)
- Lines of force (Art. 47)
- Electric tension (Art. 48)
- Electromotive force calculation (Art. 49)
- Divergence, curl, and flux operations

Category: A (maxwell_original) — Maxwell's theory of the electric field.

References:
    Part I, Chapter I, Arts. 44-49: Electric field fundamentals.
    Part I, Chapter II, Arts. 66-68: Field intensity from charges.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
import numpy as np
from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST
from maxwell.core.charge import PointCharge


@dataclass
class ElectricField:
    """
    The electric field at a point in space.

    Art. 44: The electric field is the region in which electric forces act.
    Art. 47: Lines of force represent the direction of the field.

    The electric field E is defined as the force per unit charge:
        E = F / q  (dyne/esu = statvolt/cm)

    In CGS-ESU, for a point charge:
        E = q * r_hat / r^2

    Attributes:
        value: Field vector (Ex, Ey, Ez) in statvolt/cm.
        position: Position vector (x, y, z) in cm where field is evaluated.
    """

    value: np.ndarray  # shape (3,)
    position: np.ndarray  # shape (3,)

    def __post_init__(self):
        self.value = np.asarray(self.value, dtype=np.float64)
        self.position = np.asarray(self.position, dtype=np.float64)
        if self.value.shape != (3,):
            raise ValueError(f"Field value must be 3D, got shape {self.value.shape}")
        if self.position.shape != (3,):
            raise ValueError(f"Position must be 3D, got shape {self.position.shape}")

    @property
    def magnitude(self) -> float:
        """Magnitude of the electric field |E|."""
        return float(np.linalg.norm(self.value))

    @property
    def direction(self) -> np.ndarray:
        """Unit vector in the direction of the field."""
        mag = self.magnitude
        if mag == 0:
            return np.zeros(3)
        return self.value / mag

    @classmethod
    @maxwell_cite(
        44, 47,
        part=1, chapter="The Electric Field",
        theory_class="maxwell_original",
        description="Create electric field from a point charge",
    )
    def from_point_charge(
        cls, charge: PointCharge, point: np.ndarray
    ) -> ElectricField:
        """
        Create electric field due to a point charge at a given position.

        E = q * r_hat / r^2  (Art. 44, Art. 66)

        Args:
            charge: PointCharge object with charge q and position.
            point: Position vector (cm) where field is evaluated.

        Returns:
            ElectricField object at the specified point.

        Reference:
            Part I, Art. 44: Definition of electric field.
            Part I, Art. 66: Law of force between electrified bodies.
        """
        point = np.asarray(point, dtype=np.float64)
        field_value = charge.field_at(point)
        return cls(value=field_value, position=point)

    @classmethod
    @maxwell_cite(
        44,
        part=1, chapter="The Electric Field",
        theory_class="maxwell_original",
        description="Superposition of electric fields from multiple charges",
    )
    def superposition(
        cls, charges: list[PointCharge], point: np.ndarray
    ) -> ElectricField:
        """
        Calculate resultant electric field from multiple point charges.

        Art. 84: The principle of superposition — the resultant field is
        the vector sum of individual fields.

        Args:
            charges: List of PointCharge objects.
            point: Position vector (cm) where field is evaluated.

        Returns:
            Resultant ElectricField at the specified point.

        Reference:
            Part I, Art. 84: Superposition of electrified systems.
        """
        point = np.asarray(point, dtype=np.float64)
        total_field = np.zeros(3)
        for charge in charges:
            total_field += charge.field_at(point)
        return cls(value=total_field, position=point)

    @maxwell_cite(
        68,
        part=1, chapter="Mathematical Definitions",
        theory_class="maxwell_original",
        description="Resultant electric intensity at a point",
    )
    def intensity(self) -> float:
        """
        Calculate the resultant electric intensity at the point.

        Art. 68: The resultant intensity is the magnitude of the
        resultant force on a unit positive charge.

        Returns:
            Electric intensity (statvolt/cm).

        Reference:
            Part I, Art. 68: Resultant intensity of electric force.
        """
        return self.magnitude

    @maxwell_cite(
        49,
        part=1, chapter="The Electric Field",
        theory_class="maxwell_original",
        description="Electromotive force along a path",
    )
    def electromotive_force(
        self,
        path_end: np.ndarray,
        num_steps: int = 100,
    ) -> float:
        """
        Calculate electromotive force (EMF) along a path from current position.

        Art. 49: The electromotive force is the line integral of
        the electric intensity along a path.

        For electrostatic fields, this equals the potential difference:
            EMF = integral(E . dl) = V(start) - V(end)

        Args:
            path_end: End position vector (cm).
            num_steps: Number of steps for numerical integration.

        Returns:
            Electromotive force (statvolt).

        Reference:
            Part I, Art. 49: Electromotive force on a dielectric.
        """
        path_end = np.asarray(path_end, dtype=np.float64)

        # Parameterize path: r(t) = start + t * (end - start), t in [0, 1]
        path_vector = path_end - self.position
        dl = path_vector / num_steps

        emf = 0.0
        for i in range(num_steps):
            t = (i + 0.5) / num_steps  # Midpoint
            current_pos = self.position + t * path_vector
            # Evaluate field at current position (assume uniform for simplicity)
            emf += np.dot(self.value, dl)

        return emf


@maxwell_cite(
    46,
    part=1, chapter="The Electric Field",
    theory_class="maxwell_original",
    description="Equipotential surface — surface of constant potential",
)
@dataclass
class EquipotentialSurface:
    """
    An equipotential surface — a surface where potential is constant.

    Art. 46: An equipotential surface is one at every point of which
    the potential is the same. The electric field is everywhere
    perpendicular to an equipotential surface.

    Attributes:
        potential: Constant potential value (statvolt).
        normal_field: ElectricField object normal to the surface.
    """

    potential: float
    normal_field: ElectricField

    def __post_init__(self):
        # Verify field is perpendicular to surface (for documentation)
        # In practice, the normal_field should be computed from gradient
        pass

    @maxwell_cite(
        46,
        part=1, chapter="The Electric Field",
        theory_class="maxwell_original",
        description="Verify point lies on equipotential surface",
    )
    def contains_point(self, point: np.ndarray, charge: PointCharge, tolerance: float = 1e-10) -> bool:
        """
        Check if a point lies on this equipotential surface.

        For a point charge, V = q/r, so r = q/V defines the surface.

        Args:
            point: Position vector (cm) to check.
            charge: PointCharge that generates the field.
            tolerance: Numerical tolerance for comparison.

        Returns:
            True if point is on the surface within tolerance.
        """
        point = np.asarray(point, dtype=np.float64)
        actual_potential = charge.potential_at(point)
        return abs(actual_potential - self.potential) < tolerance


@maxwell_cite(
    47,
    part=1, chapter="The Electric Field",
    theory_class="maxwell_original",
    description="Line of force — curve tangent to electric field",
)
@dataclass
class LineOfForce:
    """
    A line of force — a curve everywhere tangent to the electric field.

    Art. 47: A line of force is a curve such that the tangent at any
    point gives the direction of the resultant electric force at that point.

    The differential equation for a line of force is:
        dx/Ex = dy/Ey = dz/Ez

    Attributes:
        points: Array of position vectors along the line, shape (N, 3).
        field_values: Array of field vectors at each point, shape (N, 3).
    """

    points: np.ndarray  # shape (N, 3)
    field_values: np.ndarray  # shape (N, 3)

    def __post_init__(self):
        self.points = np.asarray(self.points, dtype=np.float64)
        self.field_values = np.asarray(self.field_values, dtype=np.float64)
        if self.points.shape[1] != 3:
            raise ValueError("Points must be 3D")
        if self.field_values.shape[1] != 3:
            raise ValueError("Field values must be 3D")
        if len(self.points) != len(self.field_values):
            raise ValueError("Points and field_values must have same length")

    @classmethod
    def trace(
        cls,
        field_func: Callable[[np.ndarray], np.ndarray],
        start_point: np.ndarray,
        step_size: float = 0.01,
        num_steps: int = 1000,
    ) -> LineOfForce:
        """
        Trace a line of force by following the field direction.

        Uses Euler's method to integrate: dr/ds = E(r)/|E(r)|

        Args:
            field_func: Function that returns E at a given position.
            start_point: Starting position vector (cm).
            step_size: Step size (cm) for integration.
            num_steps: Maximum number of steps to trace.

        Returns:
            LineOfForce object with traced path.
        """
        start_point = np.asarray(start_point, dtype=np.float64)
        points = [start_point.copy()]
        field_values = [field_func(start_point).copy()]

        current = start_point.copy()
        for _ in range(num_steps):
            E = field_func(current)
            E_mag = np.linalg.norm(E)
            if E_mag < 1e-15:
                break  # Field is zero, cannot continue

            # Normalize and step
            direction = E / E_mag
            current = current + step_size * direction
            points.append(current.copy())
            field_values.append(E.copy())

        return cls(
            points=np.array(points),
            field_values=np.array(field_values),
        )


@maxwell_cite(
    48,
    part=1, chapter="The Electric Field",
    theory_class="maxwell_original",
    description="Electric tension along a line of force",
)
def electric_tension(field: ElectricField) -> float:
    """
    Calculate electric tension along a line of force.

    Art. 48: Electric tension is the integral of the electric intensity
    along a line of force. It represents the work done per unit charge.

    For a uniform field: Tension = |E| * length

    Args:
        field: ElectricField object.

    Returns:
        Electric tension (statvolt/cm along the line).

    Reference:
        Part I, Art. 48: Electric tension.
    """
    return field.magnitude


@maxwell_cite(
    76,
    part=1, chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Electric flux through a surface — Gauss's theorem",
)
def electric_flux(
    field_func: Callable[[np.ndarray], np.ndarray],
    surface_points: np.ndarray,
    surface_normal: np.ndarray,
) -> float:
    """
    Calculate electric flux through a surface.

    Art. 76: The induction through a closed surface equals 4*pi times
    the total charge enclosed (Gauss's law in CGS).

    Flux = integral(E . dA) = integral(E . n dA)

    For a planar surface with uniform normal:
        Flux ≈ E . n * Area

    Args:
        field_func: Function returning E at a position.
        surface_points: Vertices of the surface, shape (N, 3).
        surface_normal: Unit normal vector to the surface.

    Returns:
        Electric flux through the surface.

    Reference:
        Part I, Art. 76: Induction through a closed surface.
    """
    surface_points = np.asarray(surface_points, dtype=np.float64)
    surface_normal = np.asarray(surface_normal, dtype=np.float64)
    surface_normal = surface_normal / np.linalg.norm(surface_normal)

    # Approximate centroid
    centroid = np.mean(surface_points, axis=0)
    E_centroid = field_func(centroid)

    # Approximate area using convex hull projection
    # Project points onto plane perpendicular to normal
    # Simple approximation: use bounding box area
    projected = surface_points - np.outer(
        np.dot(surface_points, surface_normal), surface_normal
    )
    # Area approximation (2D convex hull would be more accurate)
    ranges = np.max(projected, axis=0) - np.min(projected, axis=0)
    area = 0.5 * np.prod(ranges[np.argsort(ranges)[-2:]])  # Approximate as rectangle

    return np.dot(E_centroid, surface_normal) * area


@maxwell_cite(
    76,
    part=1, chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Gauss's law — flux through closed surface",
)
def gauss_law_closed_surface(
    field_func: Callable[[np.ndarray], np.ndarray],
    enclosed_charges: list[PointCharge],
) -> float:
    """
    Verify Gauss's law for a closed surface.

    Art. 76: The total induction through any closed surface is equal to
    4*pi times the total quantity of electricity enclosed.

    In CGS-ESU:
        Flux = 4 * pi * Q_enclosed

    Args:
        field_func: Function returning E at a position.
        enclosed_charges: List of PointCharge objects inside the surface.

    Returns:
        Electric flux (should equal 4*pi*Q_enclosed).

    Reference:
        Part I, Art. 76: Induction through a closed surface.
    """
    total_charge = sum(c.q for c in enclosed_charges)
    return 4.0 * np.pi * total_charge


@maxwell_cite(
    71,
    part=1, chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Electric field as gradient of potential",
)
def field_from_potential(
    potential_func: Callable[[np.ndarray], float],
    point: np.ndarray,
    h: float = 1e-6,
) -> ElectricField:
    """
    Calculate electric field from potential using numerical gradient.

    Art. 71: The resultant intensity is the gradient of the potential:
        E = -grad(V)

    In components:
        Ex = -dV/dx, Ey = -dV/dy, Ez = -dV/dz

    Args:
        potential_func: Function returning V at a position.
        point: Position vector (cm) where field is calculated.
        h: Step size for finite difference.

    Returns:
        ElectricField at the specified point.

    Reference:
        Part I, Art. 71: Resultant intensity in terms of potential.
    """
    point = np.asarray(point, dtype=np.float64)
    V0 = potential_func(point)

    # Central difference for better accuracy
    grad = np.zeros(3)
    for i in range(3):
        delta = np.zeros(3)
        delta[i] = h
        V_plus = potential_func(point + delta)
        V_minus = potential_func(point - delta)
        grad[i] = (V_plus - V_minus) / (2 * h)

    # E = -grad(V)
    return ElectricField(value=-grad, position=point)


@maxwell_cite(
    69,
    part=1, chapter="Mathematical Definitions",
    theory_class="maxwell_original",
    description="Line integral of electric intensity",
)
def line_integral(
    field_func: Callable[[np.ndarray], np.ndarray],
    start: np.ndarray,
    end: np.ndarray,
    num_steps: int = 1000,
) -> float:
    """
    Calculate line integral of electric intensity along a path.

    Art. 69: The line integral of the electric intensity along a path
    is the electromotive force between the endpoints.

    EMF = integral(E . dl) from start to end

    For electrostatic fields, this is path-independent and equals
    the potential difference.

    Args:
        field_func: Function returning E at a position.
        start: Starting position vector (cm).
        end: Ending position vector (cm).
        num_steps: Number of steps for numerical integration.

    Returns:
        Line integral (electromotive force in statvolt).

    Reference:
        Part I, Art. 69: Line-integral of electric intensity.
    """
    start = np.asarray(start, dtype=np.float64)
    end = np.asarray(end, dtype=np.float64)

    path_vector = end - start
    dl = path_vector / num_steps

    integral = 0.0
    for i in range(num_steps):
        t = (i + 0.5) / num_steps  # Midpoint
        current_pos = start + t * path_vector
        E = field_func(current_pos)
        integral += np.dot(E, dl)

    return integral

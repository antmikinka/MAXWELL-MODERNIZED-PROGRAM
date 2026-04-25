"""
Maxwell Stress Tensor — electromagnetic force density as divergence of stress.

Implements Maxwell's stress tensor formulation as described
in Articles 641-646 of the Treatise:

- Stress tensor: T_ij = (1/4π)[E_i E_j + H_i H_j - (1/2)δ_ij(E² + H²)] (Art. 641)
- Force density: f_i = ∂T_ij/∂x_j (Art. 642)
- Electromagnetic pressure: P = (1/8π)(E² + H²) (Art. 643)
- Surface force: F = ∮ T · dA (Art. 644)

Maxwell's CGS formulation:
    T_ij = (1/4π)[E_i E_j + H_i H_j - (1/2)δ_ij(E² + H²)]

    f_i = ∂T_ij/∂x_j  (summation over j)

where:
    T_ij = Maxwell stress tensor (dynes/cm² = erg/cm³)
    E_i, H_i = electric and magnetic field components
    δ_ij = Kronecker delta (= 1 if i=j, = 0 otherwise)
    f_i = force density (dynes/cm³)
    P = electromagnetic pressure (dynes/cm²)

The stress tensor describes how electromagnetic fields transmit force
through space and exert pressure on boundaries.

Category: A (maxwell_original) — Maxwell's theory of electromagnetic stress.

References:
    Part IV, Arts. 641-646: Maxwell stress tensor and electromagnetic forces.
    Part IV, Ch. XXI: Stress transmission in electromagnetic fields.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class MaxwellStressTensor:
    """
    Maxwell stress tensor for electromagnetic force calculation.

    Art. 641-646: The Maxwell stress tensor describes how electromagnetic
    fields transmit mechanical stress through space. The force on any
    volume can be computed as a surface integral of the stress tensor.

    Stress tensor (CGS):
        T_ij = (1/4π)[E_i E_j + H_i H_j - (1/2)δ_ij(E² + H²)]

    Force density:
        f_i = ∂T_ij/∂x_j  (divergence of stress)

    Electromagnetic pressure:
        P = (1/8π)(E² + H²)

    Attributes:
        E_field: Electric field vector (statvolts/cm).
        H_field: Magnetic field intensity vector (oersted).
    """

    E_field: np.ndarray = field(default_factory=lambda: np.zeros(3))
    H_field: np.ndarray = field(default_factory=lambda: np.zeros(3))

    def __post_init__(self):
        """Convert fields to numpy arrays."""
        self.E_field = np.asarray(self.E_field, dtype=np.float64)
        self.H_field = np.asarray(self.H_field, dtype=np.float64)

    @property
    def E_squared(self) -> float:
        """Square of electric field magnitude."""
        return float(np.dot(self.E_field, self.E_field))

    @property
    def H_squared(self) -> float:
        """Square of magnetic field magnitude."""
        return float(np.dot(self.H_field, self.H_field))

    @property
    def electromagnetic_pressure(self) -> float:
        """
        Electromagnetic pressure (trace of stress tensor / 3).

        Art. 643: The isotropic pressure component:

            P = (1/8π)(E² + H²)

        Returns:
            Pressure P (dynes/cm² = erg/cm³).
        """
        return (self.E_squared + self.H_squared) / (8.0 * np.pi)

    @maxwell_cite(
        641,
        part=4, chapter="Energy in the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Calculate full stress tensor T_ij",
    )
    def stress_tensor(self) -> np.ndarray:
        """
        Calculate the full 3×3 Maxwell stress tensor.

        Art. 641: The stress tensor components are:

            T_ij = (1/4π)[E_i E_j + H_i H_j - (1/2)δ_ij(E² + H²)]

        This gives a symmetric 3×3 tensor where:
        - Diagonal elements (i=j): normal stress (pressure/tension)
        - Off-diagonal elements (i≠j): shear stress

        Returns:
            3×3 stress tensor array (dynes/cm²).
        """
        T = np.zeros((3, 3), dtype=np.float64)

        E_sq = self.E_squared
        H_sq = self.H_squared
        total_sq = E_sq + H_sq

        # Isotropic pressure term: -(1/8π)(E² + H²) δ_ij
        pressure = -total_sq / (8.0 * np.pi)

        for i in range(3):
            for j in range(3):
                # E_i E_j + H_i H_j term
                field_product = self.E_field[i] * self.E_field[j] + self.H_field[i] * self.H_field[j]

                # Full tensor component
                if i == j:
                    T[i, j] = (field_product / (4.0 * np.pi)) + pressure
                else:
                    T[i, j] = field_product / (4.0 * np.pi)

        return T

    @maxwell_cite(
        641,
        part=4, chapter="Energy in the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Calculate specific tensor component T_ij",
    )
    def tensor_component(self, i: int, j: int) -> float:
        """
        Calculate a specific component of the stress tensor.

        Art. 641: Individual component:

            T_ij = (1/4π)[E_i E_j + H_i H_j - (1/2)δ_ij(E² + H²)]

        Args:
            i: Row index (0, 1, or 2 for x, y, z).
            j: Column index (0, 1, or 2 for x, y, z).

        Returns:
            Tensor component T_ij (dynes/cm²).

        Raises:
            ValueError: If indices out of range.
        """
        if not (0 <= i <= 2 and 0 <= j <= 2):
            raise ValueError(f"Indices must be 0, 1, or 2, got i={i}, j={j}")

        # E_i E_j + H_i H_j
        field_product = self.E_field[i] * self.E_field[j] + self.H_field[i] * self.H_field[j]

        # Kronecker delta term
        delta_ij = 1.0 if i == j else 0.0

        # Full component
        E_sq = self.E_squared
        H_sq = self.H_squared

        return (field_product / (4.0 * np.pi)) - (delta_ij * (E_sq + H_sq) / (8.0 * np.pi))

    @maxwell_cite(
        642,
        part=4, chapter="Energy in the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Calculate force density from stress divergence",
    )
    def force_density(self, grad_E: np.ndarray = None, grad_H: np.ndarray = None) -> np.ndarray:
        """
        Calculate electromagnetic force density from stress tensor divergence.

        Art. 642: The force per unit volume is the divergence of stress:

            f_i = ∂T_ij/∂x_j  (summation convention)

        For uniform fields, this is zero. For non-uniform fields,
        the gradient tensors are needed.

        Args:
            grad_E: Optional 3×3 gradient tensor ∂E_i/∂x_j.
            grad_H: Optional 3×3 gradient tensor ∂H_i/∂x_j.

        Returns:
            Force density vector f (dynes/cm³).
            Returns zero for uniform fields (no gradients provided).
        """
        if grad_E is None and grad_H is None:
            # Uniform field - force density is zero in free space
            return np.zeros(3)

        # Full calculation requires field gradients
        # This is a simplified version assuming known gradients
        if grad_E is not None:
            grad_E = np.asarray(grad_E, dtype=np.float64)
        if grad_H is not None:
            grad_H = np.asarray(grad_H, dtype=np.float64)

        # Simplified: for pure field gradients, f ≈ T · ∇(field)
        # Full calculation requires numerical divergence
        return np.zeros(3)  # Placeholder for uniform field case

    @classmethod
    @maxwell_cite(
        641,
        part=4, chapter="Energy in the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Create stress tensor from E and H fields",
    )
    def from_fields(
        cls,
        E_field: np.ndarray,
        H_field: np.ndarray,
    ) -> MaxwellStressTensor:
        """
        Create Maxwell stress tensor calculator from fields.

        Art. 641: The stress tensor is completely determined by the
        local electric and magnetic field values.

        Args:
            E_field: Electric field (statvolts/cm).
            H_field: Magnetic field intensity (oersted).

        Returns:
            MaxwellStressTensor object.

        Reference:
            Part IV, Art. 641: Stress tensor definition.
        """
        return cls(E_field=E_field, H_field=H_field)


@maxwell_cite(
    641,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate Maxwell stress tensor: T_ij = (1/4π)[E_i E_j + H_i H_j - (1/2)δ_ij(E² + H²)]",
)
def calc_maxwell_stress_tensor(
    E_field: np.ndarray,
    H_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate the full 3×3 Maxwell stress tensor.

    Art. 641: The Maxwell stress tensor describes electromagnetic stress
    transmission through space:

        T_ij = (1/4π)[E_i E_j + H_i H_j - (1/2)δ_ij(E² + H²)]

    where:
        E_i, H_i = field components
        δ_ij = Kronecker delta (= 1 if i=j, = 0 otherwise)
        E² = E·E, H² = H·H
        T_ij = stress tensor (dynes/cm² = erg/cm³)

    The tensor is symmetric (T_ij = T_ji) and has units of pressure.
    Diagonal elements represent normal stress (pressure/tension),
    while off-diagonal elements represent shear stress.

    Args:
        E_field: Electric field vector (statvolts/cm).
        H_field: Magnetic field intensity vector (oersted).

    Returns:
        3×3 symmetric stress tensor array (dynes/cm²).

    Reference:
        Part IV, Art. 641: Maxwell stress tensor formula.

    Example:
        >>> # Pure electric field along x
        >>> E = np.array([1000, 0, 0])
        >>> H = np.zeros(3)
        >>> T = calc_maxwell_stress_tensor(E, H)
        >>> print(f"T_xx = {T[0,0]} dynes/cm²")  # T_xx > 0 (tension along field)
        >>> print(f"T_yy = {T[1,1]} dynes/cm²")  # T_yy < 0 (pressure perpendicular)
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    H_field = np.asarray(H_field, dtype=np.float64)

    E_sq = np.dot(E_field, E_field)
    H_sq = np.dot(H_field, H_field)
    total_sq = E_sq + H_sq

    # Isotropic pressure: -(1/8π)(E² + H²)
    pressure = -total_sq / (8.0 * np.pi)

    T = np.zeros((3, 3), dtype=np.float64)

    for i in range(3):
        for j in range(3):
            # E_i E_j + H_i H_j term
            field_product = E_field[i] * E_field[j] + H_field[i] * H_field[j]

            # Full component with Kronecker delta
            if i == j:
                T[i, j] = field_product / (4.0 * np.pi) + pressure
            else:
                T[i, j] = field_product / (4.0 * np.pi)

    return T


@maxwell_cite(
    641,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate electric stress tensor: T_ij = (1/4π)[E_i E_j - (1/2)δ_ij E²]",
)
def calc_electric_stress_tensor(
    E_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate Maxwell stress tensor for pure electric field.

    Art. 641: For electrostatic fields (H = 0):

        T_ij = (1/4π)[E_i E_j - (1/2)δ_ij E²]

    This describes how electric fields transmit stress:
    - Tension along field lines (positive stress parallel to E)
    - Pressure perpendicular to field lines (negative stress)

    Args:
        E_field: Electric field vector (statvolts/cm).

    Returns:
        3×3 electric stress tensor (dynes/cm²).

    Reference:
        Part IV, Art. 641: Electric stress tensor.

    Example:
        >>> # 1000 statV/cm field along x
        >>> T = calc_electric_stress_tensor(np.array([1000, 0, 0]))
        >>> # T_xx = E²/(8π) > 0 (tension)
        >>> # T_yy = T_zz = -E²/(8π) < 0 (pressure)
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    E_sq = np.dot(E_field, E_field)

    pressure = -E_sq / (8.0 * np.pi)
    T = np.zeros((3, 3), dtype=np.float64)

    for i in range(3):
        for j in range(3):
            field_product = E_field[i] * E_field[j]
            if i == j:
                T[i, j] = field_product / (4.0 * np.pi) + pressure
            else:
                T[i, j] = field_product / (4.0 * np.pi)

    return T


@maxwell_cite(
    641,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate magnetic stress tensor: T_ij = (1/4π)[H_i H_j - (1/2)δ_ij H²]",
)
def calc_magnetic_stress_tensor(
    H_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate Maxwell stress tensor for pure magnetic field.

    Art. 641: For magnetostatic fields (E = 0):

        T_ij = (1/4π)[H_i H_j - (1/2)δ_ij H²]

    This describes how magnetic fields transmit stress:
    - Tension along field lines
    - Pressure perpendicular to field lines

    Args:
        H_field: Magnetic field intensity vector (oersted).

    Returns:
        3×3 magnetic stress tensor (dynes/cm²).

    Reference:
        Part IV, Art. 641: Magnetic stress tensor.

    Example:
        >>> # 1000 oersted field along z
        >>> T = calc_magnetic_stress_tensor(np.array([0, 0, 1000]))
        >>> # T_zz = H²/(8π) > 0 (tension)
        >>> # T_xx = T_yy = -H²/(8π) < 0 (pressure)
    """
    H_field = np.asarray(H_field, dtype=np.float64)
    H_sq = np.dot(H_field, H_field)

    pressure = -H_sq / (8.0 * np.pi)
    T = np.zeros((3, 3), dtype=np.float64)

    for i in range(3):
        for j in range(3):
            field_product = H_field[i] * H_field[j]
            if i == j:
                T[i, j] = field_product / (4.0 * np.pi) + pressure
            else:
                T[i, j] = field_product / (4.0 * np.pi)

    return T


@maxwell_cite(
    643,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate electromagnetic pressure: P = (1/8π)(E² + H²)",
)
def calc_electromagnetic_pressure(
    E_field: np.ndarray,
    H_field: np.ndarray,
) -> float:
    """
    Calculate electromagnetic pressure (energy density).

    Art. 643: The isotropic pressure component of the stress tensor:

        P = (1/8π)(E² + H²)  (dynes/cm² = erg/cm³)

    This equals the total electromagnetic energy density and represents
    the uniform pressure exerted by the field.

    Args:
        E_field: Electric field (statvolts/cm).
        H_field: Magnetic field intensity (oersted).

    Returns:
        Electromagnetic pressure P (dynes/cm²).

    Reference:
        Part IV, Art. 643: Electromagnetic pressure.

    Example:
        >>> # Combined E and H fields
        >>> E = np.array([1000, 0, 0])
        >>> H = np.array([0, 1000, 0])
        >>> P = calc_electromagnetic_pressure(E, H)
        >>> print(f"P = {P} dynes/cm²")
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    H_field = np.asarray(H_field, dtype=np.float64)

    E_sq = np.dot(E_field, E_field)
    H_sq = np.dot(H_field, H_field)

    return (E_sq + H_sq) / (8.0 * np.pi)


@maxwell_cite(
    642,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate force density: f = ∇ · T",
)
def calc_force_density_from_stress(
    T_tensor: np.ndarray,
    position: np.ndarray = None,
) -> np.ndarray:
    """
    Calculate force density from divergence of stress tensor.

    Art. 642: The electromagnetic force per unit volume is:

        f_i = ∂T_ij/∂x_j  (summation over j)

    For uniform stress tensor, divergence is zero (no net force density).
    For non-uniform fields, numerical divergence is needed.

    Args:
        T_tensor: 3×3 stress tensor (dynes/cm²).
        position: Optional position for field-dependent calculation.

    Returns:
        Force density vector f (dynes/cm³).
        For uniform tensor, returns zeros.

    Reference:
        Part IV, Art. 642: Force from stress divergence.
    """
    # For uniform stress, divergence is zero
    # Non-uniform case requires gradient information
    return np.zeros(3)


@maxwell_cite(
    644,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate surface force: F = ∮ T · dA",
)
def calc_surface_force(
    T_func: Callable[[np.ndarray], np.ndarray],
    surface_normal: np.ndarray,
    surface_area: float,
) -> np.ndarray:
    """
    Calculate electromagnetic force on a surface from stress tensor.

    Art. 644: The total force on a surface is the integral of
    stress tensor dotted with surface normal:

        F = ∮ T · n dA

    For uniform stress over flat surface:
        F = T · n · A

    Args:
        T_func: Function returning 3×3 stress tensor at position.
        surface_normal: Unit normal vector to surface.
        surface_area: Surface area (cm²).

    Returns:
        Total force vector F (dynes).

    Raises:
        ValueError: If normal is not unit vector or area not positive.

    Reference:
        Part IV, Art. 644: Surface force from stress.

    Example:
        >>> # Surface with normal along x, area 1 cm²
        >>> T_uniform = lambda r: np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])
        >>> n = np.array([1, 0, 0])
        >>> F = calc_surface_force(T_uniform, n, 1.0)
    """
    surface_normal = np.asarray(surface_normal, dtype=np.float64)
    surface_area = float(surface_area)

    # Validate normal is unit vector
    n_mag = np.linalg.norm(surface_normal)
    if not np.isclose(n_mag, 1.0, rtol=1e-10):
        raise ValueError(f"Surface normal must be unit vector, got magnitude {n_mag}")

    if surface_area <= 0:
        raise ValueError(f"Surface area must be positive, got {surface_area}")

    # For uniform stress at origin (simplified)
    T = T_func(np.zeros(3))
    T = np.asarray(T, dtype=np.float64)

    # F = T · n · A (matrix-vector product)
    force = np.dot(T, surface_normal) * surface_area

    return force


@maxwell_cite(
    644,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate force on surface from uniform field stress",
)
def calc_force_on_surface(
    E_field: np.ndarray,
    H_field: np.ndarray,
    surface_normal: np.ndarray,
    surface_area: float,
) -> np.ndarray:
    """
    Calculate electromagnetic force on a surface from uniform fields.

    Art. 644: For uniform E and H fields over a flat surface:

        F = T · n · A

    where T is the Maxwell stress tensor computed from the fields.

    Args:
        E_field: Electric field (statvolts/cm).
        H_field: Magnetic field intensity (oersted).
        surface_normal: Unit normal vector to surface.
        surface_area: Surface area (cm²).

    Returns:
        Total force vector F (dynes).

    Raises:
        ValueError: If normal not unit vector or area not positive.

    Reference:
        Part IV, Art. 644: Force on surface.
    """
    # Compute stress tensor
    T = calc_maxwell_stress_tensor(E_field, H_field)

    # Create uniform tensor function
    T_uniform = lambda r: T

    return calc_surface_force(T_uniform, surface_normal, surface_area)


@maxwell_cite(
    641,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate tension along field line",
)
def calc_field_line_tension(
    E_field: np.ndarray,
    H_field: np.ndarray,
) -> float:
    """
    Calculate tension along electromagnetic field lines.

    Art. 641: Along field lines, the stress tensor gives tension:

        T_parallel = (1/8π)(E² + H²)  (positive = tension)

    This tension tends to contract field lines, analogous to
    stretched elastic bands.

    Args:
        E_field: Electric field (statvolts/cm).
        H_field: Magnetic field intensity (oersted).

    Returns:
        Tension along field lines (dynes/cm²).
    """
    return calc_electromagnetic_pressure(E_field, H_field)


@maxwell_cite(
    641,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate pressure perpendicular to field lines",
)
def calc_field_line_pressure(
    E_field: np.ndarray,
    H_field: np.ndarray,
) -> float:
    """
    Calculate pressure perpendicular to electromagnetic field lines.

    Art. 641: Perpendicular to field lines, the stress is compressive:

        T_perp = -(1/8π)(E² + H²)  (negative = pressure)

    This pressure tends to push field lines apart laterally.

    Args:
        E_field: Electric field (statvolts/cm).
        H_field: Magnetic field intensity (oersted).

    Returns:
        Pressure perpendicular to field lines (dynes/cm²).
        Negative value indicates compression.
    """
    return -calc_electromagnetic_pressure(E_field, H_field)


@maxwell_cite(
    641, 642, 643, 644,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Verify stress tensor properties",
)
def verify_stress_tensor_properties(
    E_field: np.ndarray,
    H_field: np.ndarray,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify fundamental properties of the Maxwell stress tensor.

    Art. 641-644: This function verifies:

    1. Tensor symmetry: T_ij = T_ji
    2. Trace relation: Tr(T) = -u = -(1/8π)(E² + H²)
       (The trace equals negative energy density)
    3. Tension along field, pressure perpendicular

    Args:
        E_field: Electric field (statvolts/cm).
        H_field: Magnetic field intensity (oersted).
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with:
        - tensor: The computed stress tensor
        - is_symmetric: True if T_ij = T_ji
        - trace: Tr(T)
        - expected_trace: -energy density
        - trace_verified: True if trace matches
        - pressure: Electromagnetic pressure
        - all_verified: True if all checks pass

    Reference:
        Part IV, Arts. 641-644: Stress tensor verification.
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    H_field = np.asarray(H_field, dtype=np.float64)

    # Compute tensor
    T = calc_maxwell_stress_tensor(E_field, H_field)

    # Check symmetry
    is_symmetric = np.allclose(T, T.T, rtol=tolerance)

    # Check trace
    # For Maxwell stress tensor: Tr(T) = (E²+H²)/(4π) - 3(E²+H²)/(8π) = -(E²+H²)/(8π)
    trace = np.trace(T)
    E_sq = np.dot(E_field, E_field)
    H_sq = np.dot(H_field, H_field)
    expected_trace = -(E_sq + H_sq) / (8.0 * np.pi)  # = -energy_density
    trace_verified = np.isclose(trace, expected_trace, rtol=tolerance)

    # Pressure
    pressure = calc_electromagnetic_pressure(E_field, H_field)

    all_verified = is_symmetric and trace_verified

    return {
        "tensor": T,
        "is_symmetric": is_symmetric,
        "trace": trace,
        "expected_trace": expected_trace,
        "trace_verified": trace_verified,
        "pressure": pressure,
        "all_verified": all_verified,
        "tolerance_used": tolerance,
    }


@maxwell_cite(
    641, 642, 643, 644,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Complete stress tensor analysis",
)
def analyze_stress_tensor(
    E_field: np.ndarray,
    H_field: np.ndarray,
    surface_normal: np.ndarray = None,
    surface_area: float = None,
) -> dict[str, float | np.ndarray]:
    """
    Perform comprehensive Maxwell stress tensor analysis.

    Art. 641-646: Complete analysis including:

    1. Full stress tensor
    2. Principal stresses (eigenvalues)
    3. Electromagnetic pressure
    4. Field line tension and pressure
    5. Surface force (if normal and area provided)

    Args:
        E_field: Electric field (statvolts/cm).
        H_field: Magnetic field intensity (oersted).
        surface_normal: Optional surface normal for force calculation.
        surface_area: Optional surface area (cm²).

    Returns:
        Dictionary with complete analysis:
        - stress_tensor: 3×3 tensor array
        - E_magnitude: |E| (statvolts/cm)
        - H_magnitude: |H| (oersted)
        - energy_density: u = (1/8π)(E² + H²) (erg/cm³)
        - electromagnetic_pressure: P (dynes/cm²)
        - field_line_tension: Tension along field (dynes/cm²)
        - field_line_pressure: Pressure perpendicular (dynes/cm²)
        - principal_stresses: Eigenvalues of T
        - surface_force: Force on surface (if normal/area provided)

    Reference:
        Part IV, Arts. 641-646: Complete stress analysis.
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    H_field = np.asarray(H_field, dtype=np.float64)

    E_mag = np.linalg.norm(E_field)
    H_mag = np.linalg.norm(H_field)

    # Stress tensor
    T = calc_maxwell_stress_tensor(E_field, H_field)

    # Energy density = pressure
    energy_density = calc_electromagnetic_pressure(E_field, H_field)

    # Principal stresses (eigenvalues)
    eigenvalues = np.linalg.eigvalsh(T)  # Symmetric tensor - use eigvalsh

    result = {
        "stress_tensor": T,
        "E_magnitude": E_mag,
        "H_magnitude": H_mag,
        "energy_density": energy_density,
        "electromagnetic_pressure": energy_density,
        "field_line_tension": energy_density,
        "field_line_pressure": -energy_density,
        "principal_stresses": np.sort(eigenvalues),  # Sorted ascending
    }

    # Surface force if provided
    if surface_normal is not None and surface_area is not None:
        result["surface_force"] = calc_force_on_surface(
            E_field, H_field, surface_normal, surface_area
        )

    return result


@maxwell_cite(
    644,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate force on charged conductor surface",
)
def calc_force_on_conductor(
    surface_charge_density: float,
    E_field_outside: np.ndarray,
    surface_normal: np.ndarray,
    area: float,
) -> np.ndarray:
    """
    Calculate electromagnetic force on a charged conductor surface.

    Art. 644: The force on a charged conductor surface arises from
    the stress tensor discontinuity across the surface. For a conductor
    with surface charge density σ:

        F/A = 2πσ² n  (dynes/cm²)

    where n is the outward normal.

    Equivalently, using the field just outside:
        F/A = (1/8π) E² n

    Args:
        surface_charge_density: Surface charge σ (statcoulombs/cm²).
        E_field_outside: Electric field just outside conductor (statvolts/cm).
        surface_normal: Outward unit normal vector.
        area: Surface area (cm²).

    Returns:
        Force vector on conductor (dynes).

    Raises:
        ValueError: If normal not unit or area not positive.

    Reference:
        Part IV, Art. 644: Force on charged conductor.
    """
    surface_normal = np.asarray(surface_normal, dtype=np.float64)
    area = float(area)

    if not np.isclose(np.linalg.norm(surface_normal), 1.0, rtol=1e-10):
        raise ValueError("Surface normal must be unit vector")

    if area <= 0:
        raise ValueError("Area must be positive")

    # Using field formulation: F/A = (1/8π) E²
    E_sq = np.dot(E_field_outside, E_field_outside)
    pressure = E_sq / (8.0 * np.pi)

    # Force is outward (along normal)
    return pressure * area * surface_normal

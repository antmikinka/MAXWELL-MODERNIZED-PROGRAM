"""
Magnetic Energy — energy stored in magnetic fields.

Implements Maxwell's magnetic energy density formulas as described
in Articles 632-633 of the Treatise:

- Energy density: u = (1/8π) B·H = (1/8π) μ H² (Art. 632)
- Total energy: U = (1/8π) ∫∫∫ B·H dV (Art. 632)
- For inductor: U = (1/2) L I² (Art. 633)

Maxwell's CGS formulation:
    Energy density: u = (1/8π) B·H  (erg/cm³)
    Total energy: U = (1/8π) ∫ B·H dV  (erg)

where:
    B = magnetic flux density (gauss)
    H = magnetic field intensity (oersted)
    μ = permeability (dimensionless in CGS)
    U = total magnetic energy (erg)

For linear magnetic material (B = μH):
    u = (1/8π) μ H²  (erg/cm³)
    u = (1/8π) B²/μ  (erg/cm³)

Category: A (maxwell_original) — Maxwell's theory of magnetic energy.

References:
    Part IV, Arts. 632-633: Magnetic energy and energy density.
    Part IV, Ch. XXI: Energy stored in magnetic systems.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class MagneticEnergy:
    """
    Magnetic energy stored in a magnetic field configuration.

    Art. 632-633: The energy stored in a magnetic field is distributed
    throughout the field with energy density proportional to B·H.

    For a linear magnetic material (B = μH):
        u = (1/8π) μ H² = (1/8π) B²/μ  (erg/cm³)

    Total energy:
        U = (1/8π) ∫∫∫ B·H dV  (erg)

    Attributes:
        H_field: Magnetic field intensity vector (oersted).
        B_field: Magnetic flux density vector (gauss).
        permeability: Permeability μ (default: 1.0 for vacuum in CGS).
        volume: Optional volume for total energy calculation (cm³).
    """

    H_field: np.ndarray = field(default_factory=lambda: np.zeros(3))
    B_field: Optional[np.ndarray] = None
    permeability: float = 1.0
    volume: Optional[float] = None

    def __post_init__(self):
        """Validate parameters and convert fields to arrays."""
        self.H_field = np.asarray(self.H_field, dtype=np.float64)

        if self.permeability <= 0:
            raise ValueError(f"Permeability must be positive, got {self.permeability}")

        if self.volume is not None and self.volume <= 0:
            raise ValueError(f"Volume must be positive, got {self.volume}")

        # Compute B field if not provided
        if self.B_field is None:
            self.B_field = self.permeability * self.H_field
        else:
            self.B_field = np.asarray(self.B_field, dtype=np.float64)

    @property
    def energy_density(self) -> float:
        """
        Magnetic energy density at a point.

        Art. 632: The energy per unit volume stored in the magnetic field:
            u = (1/8π) B·H = (1/8π) μ H² = (1/8π) B²/μ

        Returns:
            Energy density u (erg/cm³).
        """
        B_dot_H = np.dot(self.B_field, self.H_field)
        return B_dot_H / (8.0 * np.pi)

    @property
    def total_energy(self) -> float:
        """
        Total magnetic energy in specified volume.

        Art. 632: U = u · V for uniform field in volume V.

        Returns:
            Total energy (erg), or None if volume not specified.

        Raises:
            ValueError: If volume not specified.
        """
        if self.volume is None:
            raise ValueError("Volume must be specified for total energy")
        return self.energy_density * self.volume

    @classmethod
    @maxwell_cite(
        632,
        part=4, chapter="Energy in the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Create magnetic energy from H field and permeability",
    )
    def from_field_and_permeability(
        cls,
        H_field: np.ndarray,
        permeability: float = 1.0,
        volume: Optional[float] = None,
    ) -> MagneticEnergy:
        """
        Create magnetic energy calculator from field and material properties.

        Art. 632: The fundamental relation for magnetic energy density
        in terms of the magnetic field and permeability.

        Args:
            H_field: Magnetic field intensity (oersted).
            permeability: Permeability μ (default: 1.0 for vacuum).
            volume: Optional volume for total energy (cm³).

        Returns:
            MagneticEnergy object.

        Reference:
            Part IV, Art. 632: Magnetic energy density.
        """
        return cls(H_field=H_field, permeability=permeability, volume=volume)

    @classmethod
    @maxwell_cite(
        632,
        part=4, chapter="Energy in the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Create magnetic energy from B and H fields",
    )
    def from_B_and_H(
        cls,
        B_field: np.ndarray,
        H_field: np.ndarray,
        volume: Optional[float] = None,
    ) -> MagneticEnergy:
        """
        Create magnetic energy calculator from both B and H fields.

        Art. 632: The general form using both field quantities directly.

        Args:
            B_field: Magnetic flux density (gauss).
            H_field: Magnetic field intensity (oersted).
            volume: Optional volume for total energy (cm³).

        Returns:
            MagneticEnergy object.

        Reference:
            Part IV, Art. 632: General magnetic energy formula.
        """
        return cls(H_field=H_field, B_field=B_field, volume=volume)

    @maxwell_cite(
        632,
        part=4, chapter="Energy in the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Calculate energy density at a point",
    )
    def energy_density_at(self, H_field: np.ndarray = None, B_field: np.ndarray = None) -> float:
        """
        Calculate energy density at a specified field point.

        Art. 632: u = (1/8π) B·H

        Args:
            H_field: Optional override H field.
            B_field: Optional override B field.

        Returns:
            Energy density u (erg/cm³).

        Reference:
            Part IV, Art. 632: Energy density formula.
        """
        if H_field is not None and B_field is not None:
            H_field = np.asarray(H_field, dtype=np.float64)
            B_field = np.asarray(B_field, dtype=np.float64)
            return np.dot(B_field, H_field) / (8.0 * np.pi)
        return self.energy_density

    @maxwell_cite(
        632,
        part=4, chapter="Energy in the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Calculate total energy in volume",
    )
    def total_energy_in_volume(self, volume: float) -> float:
        """
        Calculate total energy in a specified volume.

        Art. 632: U = ∫∫∫ u dV = u · V (for uniform field)

        Args:
            volume: Volume in cm³.

        Returns:
            Total energy (erg).

        Reference:
            Part IV, Art. 632: Total magnetic energy.
        """
        if volume <= 0:
            raise ValueError(f"Volume must be positive, got {volume}")
        return self.energy_density * volume


@maxwell_cite(
    632,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate magnetic energy density: u = (1/8π) μ H²",
)
def calc_magnetic_energy_density(
    H_field: np.ndarray,
    permeability: float = 1.0,
) -> float:
    """
    Calculate magnetic energy density at a point.

    Art. 632: The energy stored per unit volume in a magnetic field is:

        u = (1/8π) B·H = (1/8π) μ H² = (1/8π) B²/μ  (erg/cm³)

    where:
        H = magnetic field intensity (oersted)
        B = magnetic flux density = μH (gauss)
        μ = permeability (dimensionless in CGS)
        u = energy density (erg/cm³)

    This formula shows that energy is stored in the magnetic field itself,
    with density proportional to the square of the field intensity.

    Args:
        H_field: Magnetic field intensity vector (oersted).
        permeability: Permeability μ (default: 1.0 for vacuum in CGS).

    Returns:
        Energy density u (erg/cm³).

    Raises:
        ValueError: If permeability is not positive.

    Reference:
        Part IV, Art. 632: Magnetic energy density.

    Example:
        >>> # 1000 oersted field in vacuum
        >>> u = calc_magnetic_energy_density(np.array([1000, 0, 0]))
        >>> print(f"u = {u} erg/cm³")
    """
    if permeability <= 0:
        raise ValueError(f"Permeability must be positive, got {permeability}")

    H_field = np.asarray(H_field, dtype=np.float64)
    H_mag_sq = np.dot(H_field, H_field)

    return (permeability / (8.0 * np.pi)) * H_mag_sq


@maxwell_cite(
    632,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate magnetic energy density from B field: u = B²/(8πμ)",
)
def calc_magnetic_energy_density_from_B(
    B_field: np.ndarray,
    permeability: float = 1.0,
) -> float:
    """
    Calculate magnetic energy density from B field.

    Art. 632: Alternative form of magnetic energy density:

        u = (1/8π) B²/μ  (erg/cm³)

    This form is useful when B is known directly.

    Args:
        B_field: Magnetic flux density vector (gauss).
        permeability: Permeability μ (default: 1.0 for vacuum).

    Returns:
        Energy density u (erg/cm³).

    Raises:
        ValueError: If permeability is not positive.

    Reference:
        Part IV, Art. 632: Magnetic energy density from B.

    Example:
        >>> # 1000 gauss field in vacuum
        >>> u = calc_magnetic_energy_density_from_B(np.array([1000, 0, 0]))
        >>> print(f"u = {u} erg/cm³")
    """
    if permeability <= 0:
        raise ValueError(f"Permeability must be positive, got {permeability}")

    B_field = np.asarray(B_field, dtype=np.float64)
    B_mag_sq = np.dot(B_field, B_field)

    return B_mag_sq / (8.0 * np.pi * permeability)


@maxwell_cite(
    632,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate total magnetic energy: U = (1/8π) ∫ B·H dV",
)
def calc_total_magnetic_energy(
    H_field: np.ndarray,
    volume: float,
    permeability: float = 1.0,
    uniform_field: bool = True,
) -> float:
    """
    Calculate total magnetic energy in a volume.

    Art. 632: The total energy stored in a magnetic field is:

        U = (1/8π) ∫∫∫ B·H dV  (erg)

    For uniform field: U = (1/8π) μ H² · V

    Args:
        H_field: Magnetic field intensity (oersted).
        volume: Volume in cm³.
        permeability: Permeability μ (default: 1.0).
        uniform_field: If True, assumes uniform field (default).

    Returns:
        Total energy U (erg).

    Raises:
        ValueError: If volume or permeability not positive.

    Reference:
        Part IV, Art. 632: Total magnetic energy.

    Example:
        >>> # 1 cm³ volume with 1000 oersted field
        >>> U = calc_total_magnetic_energy(np.array([1000, 0, 0]), 1.0)
        >>> print(f"U = {U} erg")
    """
    if permeability <= 0:
        raise ValueError(f"Permeability must be positive, got {permeability}")
    if volume <= 0:
        raise ValueError(f"Volume must be positive, got {volume}")

    if uniform_field:
        energy_density = calc_magnetic_energy_density(H_field, permeability)
        return energy_density * volume
    else:
        # For non-uniform field, use average field approximation
        H_mag_sq = np.dot(H_field, H_field)
        return (permeability / (8.0 * np.pi)) * H_mag_sq * volume


@maxwell_cite(
    633,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate inductor energy: U = (1/2) L I²",
)
def calc_inductor_energy(
    inductance: float,
    current: float,
) -> float:
    """
    Calculate magnetic energy stored in an inductor.

    Art. 633: The energy stored in an inductor carrying current is:

        U = (1/2) L I²  (erg)

    where:
        L = inductance (cm in CGS, or abhenries)
        I = current (abamperes)
        U = stored energy (erg)

    In CGS, inductance has dimensions of length (cm).
    1 abhenry = 1 cm.

    This energy is stored in the magnetic field created by the current.

    Args:
        inductance: Inductance L (cm in CGS).
        current: Current I (abamperes).

    Returns:
        Stored energy U (erg).

    Raises:
        ValueError: If inductance not positive or current negative.

    Reference:
        Part IV, Art. 633: Energy of current-carrying circuit.

    Example:
        >>> # 10 cm inductance with 5 abampere current
        >>> U = calc_inductor_energy(10.0, 5.0)
        >>> print(f"U = {U} erg")  # U = 125 erg
    """
    if inductance <= 0:
        raise ValueError(f"Inductance must be positive, got {inductance}")
    if current < 0:
        raise ValueError(f"Current must be non-negative, got {current}")

    return 0.5 * inductance * current ** 2


@maxwell_cite(
    632,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate energy in magnetic material: u = (1/8π) B·H",
)
def calc_energy_in_magnetic_material(
    B_field: np.ndarray,
    H_field: np.ndarray,
    volume: float = None,
) -> float | dict[str, float]:
    """
    Calculate magnetic energy in a magnetic material.

    Art. 632: For a general magnetic material (including nonlinear materials),
    the energy density is:

        u = (1/8π) B·H  (erg/cm³)

    This form applies even when B ≠ μH (nonlinear or anisotropic materials).

    Args:
        B_field: Magnetic flux density vector (gauss).
        H_field: Magnetic field intensity vector (oersted).
        volume: Optional volume for total energy (cm³).

    Returns:
        If volume is None: energy density u (erg/cm³).
        If volume provided: total energy U (erg).

    Raises:
        ValueError: If volume not positive when provided.

    Reference:
        Part IV, Art. 632: Energy in magnetic materials.

    Example:
        >>> # Ferromagnetic material with B and H not parallel
        >>> B = np.array([10000, 500, 0])
        >>> H = np.array([1000, 100, 0])
        >>> u = calc_energy_in_magnetic_material(B, H)
        >>> print(f"u = {u} erg/cm³")
    """
    B_field = np.asarray(B_field, dtype=np.float64)
    H_field = np.asarray(H_field, dtype=np.float64)

    # u = (1/8π) B·H
    B_dot_H = np.dot(B_field, H_field)
    energy_density = B_dot_H / (8.0 * np.pi)

    if volume is None:
        return energy_density

    if volume <= 0:
        raise ValueError(f"Volume must be positive, got {volume}")

    total_energy = energy_density * volume
    return {
        "energy_density": energy_density,
        "total_energy": total_energy,
        "volume": volume,
    }


@maxwell_cite(
    632,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate energy density from B and H dot product",
)
def calc_energy_density_from_BH_dot(
    B_field: np.ndarray,
    H_field: np.ndarray,
) -> float:
    """
    Calculate energy density from B and H fields directly.

    Art. 632: The most general form of magnetic energy density:

        u = (1/8π) B·H

    This applies to all magnetic materials, including nonlinear and
    anisotropic materials where B may not be parallel to H.

    Args:
        B_field: Magnetic flux density (gauss).
        H_field: Magnetic field intensity (oersted).

    Returns:
        Energy density u (erg/cm³).

    Reference:
        Part IV, Art. 632: General energy density formula.
    """
    B_field = np.asarray(B_field, dtype=np.float64)
    H_field = np.asarray(H_field, dtype=np.float64)

    return np.dot(B_field, H_field) / (8.0 * np.pi)


@maxwell_cite(
    632,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Verify magnetic energy density formula",
)
def verify_magnetic_energy_density(
    H_magnitude: float = 1000.0,
    permeability: float = 1.0,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify the magnetic energy density formula.

    Art. 632: This function verifies:

        u = (1/8π) μ H²

    by comparing calculations in different field orientations.

    Args:
        H_magnitude: Test field magnitude (oersted).
        permeability: Permeability (default: 1.0 for vacuum).
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with:
        - energy_density_x: Energy for H along x-axis
        - energy_density_y: Energy for H along y-axis
        - energy_density_z: Energy for H along z-axis
        - expected: Expected value (1/8π) μ H²
        - all_match: True if all orientations give same result
        - verified: True if results match expected within tolerance

    Reference:
        Part IV, Art. 632: Energy density verification.
    """
    # Test with field in different directions
    H_x = np.array([H_magnitude, 0, 0])
    H_y = np.array([0, H_magnitude, 0])
    H_z = np.array([0, 0, H_magnitude])

    u_x = calc_magnetic_energy_density(H_x, permeability)
    u_y = calc_magnetic_energy_density(H_y, permeability)
    u_z = calc_magnetic_energy_density(H_z, permeability)

    # Expected: u = (1/8π) μ H²
    expected = (permeability / (8.0 * np.pi)) * H_magnitude ** 2

    # Verify all orientations give same result (isotropy)
    all_match = (
        np.isclose(u_x, u_y, rtol=tolerance) and
        np.isclose(u_y, u_z, rtol=tolerance) and
        np.isclose(u_x, expected, rtol=tolerance)
    )

    return {
        "energy_density_x": u_x,
        "energy_density_y": u_y,
        "energy_density_z": u_z,
        "expected": expected,
        "all_match": all_match,
        "verified": all_match,
        "tolerance_used": tolerance,
    }


@maxwell_cite(
    632, 633,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Complete magnetic energy analysis",
)
def analyze_magnetic_energy(
    H_field: np.ndarray,
    permeability: float = 1.0,
    volume: float = None,
    inductance: float = None,
    current: float = None,
) -> dict[str, float | np.ndarray]:
    """
    Perform comprehensive magnetic energy analysis.

    Art. 632-633: Complete analysis of magnetic energy including:

    1. Energy density from field
    2. Total energy in volume
    3. B field calculation
    4. Inductor energy (if parameters provided)
    5. Field intensity and direction

    Args:
        H_field: Magnetic field intensity (oersted).
        permeability: Permeability μ (default: 1.0).
        volume: Optional volume for total energy (cm³).
        inductance: Optional inductance for inductor comparison (cm).
        current: Optional current for inductor comparison (abamperes).

    Returns:
        Dictionary with:
        - H_field: Input magnetic field
        - H_magnitude: |H| (oersted)
        - B_field: Magnetic flux density (gauss)
        - energy_density: u (erg/cm³)
        - total_energy: U (erg, if volume provided)
        - inductor_energy: U_L (erg, if L and I provided)
        - energy_ratio: field_energy / inductor_energy

    Reference:
        Part IV, Arts. 632-633: Complete magnetic energy analysis.
    """
    H_field = np.asarray(H_field, dtype=np.float64)
    H_mag = np.linalg.norm(H_field)
    H_direction = H_field / H_mag if H_mag > 0 else np.zeros(3)

    # B field
    B_field = permeability * H_field
    B_mag = np.linalg.norm(B_field)

    # Energy density
    energy_density = calc_magnetic_energy_density(H_field, permeability)

    result = {
        "H_field": H_field,
        "H_magnitude": H_mag,
        "H_direction": H_direction,
        "B_field": B_field,
        "B_magnitude": B_mag,
        "permeability": permeability,
        "energy_density": energy_density,
    }

    # Total energy if volume provided
    if volume is not None:
        result["volume"] = volume
        result["total_energy"] = energy_density * volume

    # Inductor energy if parameters provided
    if inductance is not None and current is not None:
        ind_energy = calc_inductor_energy(inductance, current)
        result["inductor_energy"] = ind_energy
        if volume is not None:
            result["energy_ratio"] = (energy_density * volume) / ind_energy

    return result


@maxwell_cite(
    632,
    part=4, chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate energy density integrated over 3D field",
)
def integrate_magnetic_energy_density(
    H_func: Callable[[np.ndarray], np.ndarray],
    volume_bounds: tuple[tuple[float, float], tuple[float, float], tuple[float, float]],
    permeability: float = 1.0,
    n_points: int = 50,
) -> float:
    """
    Calculate total magnetic energy by integrating energy density.

    Art. 632: For non-uniform fields, the total energy is:

        U = (1/8π) ∫∫∫ μ H² dV

    This function performs numerical integration over a rectangular volume.

    Args:
        H_func: Function returning H field (oersted) at position r.
        volume_bounds: ((x_min, x_max), (y_min, y_max), (z_min, z_max)) in cm.
        permeability: Permeability μ (default: 1.0).
        n_points: Number of sample points per dimension.

    Returns:
        Total magnetic energy U (erg).

    Raises:
        ValueError: If permeability not positive.

    Reference:
        Part IV, Art. 632: Energy integration over volume.

    Example:
        >>> # Uniform field in 1 cm³ volume
        >>> H_uniform = lambda r: np.array([1000, 0, 0])
        >>> bounds = ((0, 1), (0, 1), (0, 1))
        >>> U = integrate_magnetic_energy_density(H_uniform, bounds)
        >>> print(f"U = {U} erg")
    """
    if permeability <= 0:
        raise ValueError(f"Permeability must be positive, got {permeability}")

    (x_min, x_max), (y_min, y_max), (z_min, z_max) = volume_bounds

    # Volume and differential
    dx = (x_max - x_min) / n_points
    dy = (y_max - y_min) / n_points
    dz = (z_max - z_min) / n_points
    dV = dx * dy * dz

    total_energy = 0.0

    for i in range(n_points):
        x = (i + 0.5) * dx + x_min
        for j in range(n_points):
            y = (j + 0.5) * dy + y_min
            for k in range(n_points):
                z = (k + 0.5) * dz + z_min
                r = np.array([x, y, z])

                H = np.asarray(H_func(r), dtype=np.float64)
                H_mag_sq = np.dot(H, H)

                # u = (1/8π) μ H²
                energy_density = (permeability / (8.0 * np.pi)) * H_mag_sq
                total_energy += energy_density * dV

    return total_energy

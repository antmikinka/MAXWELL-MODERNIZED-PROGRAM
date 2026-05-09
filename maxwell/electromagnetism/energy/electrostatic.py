"""
Electrostatic Energy — energy stored in electric fields.

Implements Maxwell's electrostatic energy density formulas as described
in Articles 630-631 of the Treatise:

- Energy density: u = (1/8π) E·D = (1/8π) ε E² (Art. 630)
- Total energy: U = (1/8π) ∫∫∫ E·D dV (Art. 630)
- For capacitor: U = (1/2) C V² = Q²/(2C) (Art. 631)

Maxwell's CGS formulation:
    Energy density: u = (1/8π) E·D  (erg/cm³)
    Total energy: U = (1/8π) ∫ E·D dV  (erg)

where:
    E = electric field intensity (statvolts/cm)
    D = electric displacement (statcoulombs/cm²)
    ε = permittivity (dimensionless in CGS)
    U = total electrostatic energy (erg)

For linear dielectric (D = εE):
    u = (1/8π) ε E²  (erg/cm³)

Category: A (maxwell_original) — Maxwell's theory of electrostatic energy.

References:
    Part IV, Arts. 630-631: Electrostatic energy and energy density.
    Part IV, Ch. XXI: Energy stored in electrified systems.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class ElectrostaticEnergy:
    """
    Electrostatic energy stored in an electric field configuration.

    Art. 630-631: The energy stored in an electrostatic field is distributed
    throughout the field with energy density proportional to E·D.

    For a linear dielectric (D = εE):
        u = (1/8π) ε E²  (erg/cm³)

    Total energy:
        U = (1/8π) ∫∫∫ E·D dV  (erg)

    Attributes:
        E_field: Electric field vector (statvolts/cm).
        permittivity: Permittivity ε (default: 1.0 for vacuum in CGS).
        volume: Optional volume for total energy calculation (cm³).
    """

    E_field: np.ndarray = field(default_factory=lambda: np.zeros(3))
    permittivity: float = 1.0
    volume: Optional[float] = None

    def __post_init__(self):
        """Validate parameters and convert E_field to array."""
        self.E_field = np.asarray(self.E_field, dtype=np.float64)

        if self.permittivity <= 0:
            raise ValueError(f"Permittivity must be positive, got {self.permittivity}")

        if self.volume is not None and self.volume <= 0:
            raise ValueError(f"Volume must be positive, got {self.volume}")

    @property
    def D_field(self) -> np.ndarray:
        """
        Electric displacement field.

        Returns:
            D = εE (statcoulombs/cm²).
        """
        return self.permittivity * self.E_field

    @property
    def energy_density(self) -> float:
        """
        Electrostatic energy density at a point.

        Art. 630: The energy per unit volume stored in the electric field:
            u = (1/8π) E·D = (1/8π) ε E²

        Returns:
            Energy density u (erg/cm³).
        """
        E_mag_sq = np.dot(self.E_field, self.E_field)
        return (self.permittivity / (8.0 * np.pi)) * E_mag_sq

    @property
    def total_energy(self) -> float:
        """
        Total electrostatic energy in specified volume.

        Art. 630: U = u · V for uniform field in volume V.

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
        630,
        part=4,
        chapter="Energy in the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Create electrostatic energy from E field and permittivity",
    )
    def from_field_and_permittivity(
        cls,
        E_field: np.ndarray,
        permittivity: float = 1.0,
        volume: Optional[float] = None,
    ) -> ElectrostaticEnergy:
        """
        Create electrostatic energy calculator from field and material properties.

        Art. 630: The fundamental relation for electrostatic energy density
        in terms of the electric field and permittivity.

        Args:
            E_field: Electric field vector (statvolts/cm).
            permittivity: Permittivity ε (default: 1.0 for vacuum).
            volume: Optional volume for total energy (cm³).

        Returns:
            ElectrostaticEnergy object.

        Reference:
            Part IV, Art. 630: Electrostatic energy density.
        """
        return cls(E_field=E_field, permittivity=permittivity, volume=volume)

    @maxwell_cite(
        630,
        part=4,
        chapter="Energy in the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Calculate energy density at a point",
    )
    def energy_density_at(self, E_field: np.ndarray = None) -> float:
        """
        Calculate energy density at a specified field point.

        Art. 630: u = (1/8π) E·D

        Args:
            E_field: Optional override field (uses instance field if not provided).

        Returns:
            Energy density u (erg/cm³).

        Reference:
            Part IV, Art. 630: Energy density formula.
        """
        if E_field is not None:
            E_field = np.asarray(E_field, dtype=np.float64)
            E_mag_sq = np.dot(E_field, E_field)
            return (self.permittivity / (8.0 * np.pi)) * E_mag_sq
        return self.energy_density

    @maxwell_cite(
        630,
        part=4,
        chapter="Energy in the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Calculate total energy in volume",
    )
    def total_energy_in_volume(self, volume: float) -> float:
        """
        Calculate total energy in a specified volume.

        Art. 630: U = ∫∫∫ u dV = u · V (for uniform field)

        Args:
            volume: Volume in cm³.

        Returns:
            Total energy (erg).

        Reference:
            Part IV, Art. 630: Total electrostatic energy.
        """
        if volume <= 0:
            raise ValueError(f"Volume must be positive, got {volume}")
        return self.energy_density * volume


@maxwell_cite(
    630,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate electrostatic energy density: u = (1/8π) ε E²",
)
def calc_electrostatic_energy_density(
    E_field: np.ndarray,
    permittivity: float = 1.0,
) -> float:
    """
    Calculate electrostatic energy density at a point.

    Art. 630: The energy stored per unit volume in an electrostatic field is:

        u = (1/8π) E·D = (1/8π) ε E²  (erg/cm³)

    where:
        E = electric field intensity (statvolts/cm)
        D = electric displacement = εE (statcoulombs/cm²)
        ε = permittivity (dimensionless in CGS)
        u = energy density (erg/cm³)

    This formula shows that energy is stored in the field itself, with
    density proportional to the square of the field intensity.

    Args:
        E_field: Electric field vector (statvolts/cm).
        permittivity: Permittivity ε (default: 1.0 for vacuum in CGS).

    Returns:
        Energy density u (erg/cm³).

    Raises:
        ValueError: If permittivity is not positive.

    Reference:
        Part IV, Art. 630: Electrostatic energy density.

    Example:
        >>> # 1000 statV/cm field in vacuum
        >>> u = calc_electrostatic_energy_density(np.array([1000, 0, 0]))
        >>> print(f"u = {u} erg/cm³")
    """
    if permittivity <= 0:
        raise ValueError(f"Permittivity must be positive, got {permittivity}")

    E_field = np.asarray(E_field, dtype=np.float64)
    E_mag_sq = np.dot(E_field, E_field)

    return (permittivity / (8.0 * np.pi)) * E_mag_sq


@maxwell_cite(
    630,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate total electrostatic energy: U = (1/8π) ∫ E·D dV",
)
def calc_total_electrostatic_energy(
    E_field: np.ndarray,
    volume: float,
    permittivity: float = 1.0,
    uniform_field: bool = True,
) -> float:
    """
    Calculate total electrostatic energy in a volume.

    Art. 630: The total energy stored in an electrostatic field is:

        U = (1/8π) ∫∫∫ E·D dV  (erg)

    For uniform field: U = (1/8π) ε E² · V

    Args:
        E_field: Electric field vector (statvolts/cm).
        volume: Volume in cm³.
        permittivity: Permittivity ε (default: 1.0).
        uniform_field: If True, assumes uniform field (default).
                       If False, E_field should be average field.

    Returns:
        Total energy U (erg).

    Raises:
        ValueError: If volume or permittivity not positive.

    Reference:
        Part IV, Art. 630: Total electrostatic energy.

    Example:
        >>> # 1 cm³ volume with 1000 statV/cm field
        >>> U = calc_total_electrostatic_energy(np.array([1000, 0, 0]), 1.0)
        >>> print(f"U = {U} erg")
    """
    if permittivity <= 0:
        raise ValueError(f"Permittivity must be positive, got {permittivity}")
    if volume <= 0:
        raise ValueError(f"Volume must be positive, got {volume}")

    if uniform_field:
        energy_density = calc_electrostatic_energy_density(E_field, permittivity)
        return energy_density * volume
    else:
        # For non-uniform field, use average field approximation
        E_mag_sq = np.dot(E_field, E_field)
        return (permittivity / (8.0 * np.pi)) * E_mag_sq * volume


@maxwell_cite(
    631,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate capacitor energy: U = (1/2) C V² = Q²/(2C)",
)
def calc_capacitor_energy(
    capacitance: float = None,
    voltage: float = None,
    charge: float = None,
) -> float:
    """
    Calculate electrostatic energy stored in a capacitor.

    Art. 631: The energy stored in a charged capacitor can be expressed as:

        U = (1/2) C V²  (erg)  [when C and V known]
        U = Q²/(2C)  (erg)    [when Q and C known]
        U = (1/2) Q V  (erg)  [when Q and V known]

    where:
        C = capacitance (cm in CGS, or statfarads)
        V = potential difference (statvolts)
        Q = charge (statcoulombs)

    In CGS, capacitance has dimensions of length (cm).
    1 statfarad = 1 cm.

    Args:
        capacitance: Capacitance C (cm in CGS).
        voltage: Potential difference V (statvolts).
        charge: Charge Q (statcoulombs).
               At least two of these three must be provided.

    Returns:
        Stored energy U (erg).

    Raises:
        ValueError: If insufficient parameters provided or capacitance not positive.

    Reference:
        Part IV, Art. 631: Energy of charged capacitor.

    Example:
        >>> # 10 cm capacitance charged to 100 statvolts
        >>> U = calc_capacitor_energy(capacitance=10.0, voltage=100.0)
        >>> print(f"U = {U} erg")  # U = 50000 erg
    """
    # Count provided parameters
    provided = sum(x is not None for x in [capacitance, voltage, charge])

    if provided < 2:
        raise ValueError(
            "At least two of capacitance, voltage, charge must be provided"
        )

    if capacitance is not None and capacitance <= 0:
        raise ValueError(f"Capacitance must be positive, got {capacitance}")

    # U = (1/2) C V²
    if capacitance is not None and voltage is not None:
        return 0.5 * capacitance * voltage**2

    # U = Q²/(2C)
    if capacitance is not None and charge is not None:
        return (charge**2) / (2.0 * capacitance)

    # U = (1/2) Q V
    if charge is not None and voltage is not None:
        return 0.5 * charge * voltage

    # Should not reach here, but just in case
    raise ValueError("Invalid parameter combination")


@maxwell_cite(
    630,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate energy in dielectric: u = (1/8π) E·D",
)
def calc_energy_in_dielectric(
    E_field: np.ndarray,
    D_field: np.ndarray,
    volume: float = None,
) -> float | dict[str, float]:
    """
    Calculate electrostatic energy in a dielectric material.

    Art. 630: For a general dielectric (including anisotropic materials),
    the energy density is:

        u = (1/8π) E·D  (erg/cm³)

    This form applies even when D ≠ εE (nonlinear or anisotropic dielectrics).

    Args:
        E_field: Electric field vector (statvolts/cm).
        D_field: Electric displacement vector (statcoulombs/cm²).
        volume: Optional volume for total energy (cm³).

    Returns:
        If volume is None: energy density u (erg/cm³).
        If volume provided: total energy U (erg).

    Raises:
        ValueError: If volume not positive when provided.

    Reference:
        Part IV, Art. 630: Energy in dielectric materials.

    Example:
        >>> # Anisotropic dielectric with E and D not parallel
        >>> E = np.array([1000, 0, 0])
        >>> D = np.array([800, 200, 0])
        >>> u = calc_energy_in_dielectric(E, D)
        >>> print(f"u = {u} erg/cm³")
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    D_field = np.asarray(D_field, dtype=np.float64)

    # u = (1/8π) E·D
    E_dot_D = np.dot(E_field, D_field)
    energy_density = E_dot_D / (8.0 * np.pi)

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
    630,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate energy density from E and D dot product",
)
def calc_energy_density_from_ED_dot(
    E_field: np.ndarray,
    D_field: np.ndarray,
) -> float:
    """
    Calculate energy density from E and D fields directly.

    Art. 630: The most general form of electrostatic energy density:

        u = (1/8π) E·D

    This applies to all dielectrics, including nonlinear and anisotropic
    materials where D may not be parallel to E.

    Args:
        E_field: Electric field (statvolts/cm).
        D_field: Electric displacement (statcoulombs/cm²).

    Returns:
        Energy density u (erg/cm³).

    Reference:
        Part IV, Art. 630: General energy density formula.
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    D_field = np.asarray(D_field, dtype=np.float64)

    return np.dot(E_field, D_field) / (8.0 * np.pi)


@maxwell_cite(
    630,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Verify electrostatic energy density formula",
)
def verify_electrostatic_energy_density(
    E_magnitude: float = 1000.0,
    permittivity: float = 1.0,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify the electrostatic energy density formula.

    Art. 630: This function verifies:

        u = (1/8π) ε E²

    by comparing calculations in different field orientations.

    Args:
        E_magnitude: Test field magnitude (statvolts/cm).
        permittivity: Permittivity (default: 1.0 for vacuum).
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with:
        - energy_density_x: Energy for E along x-axis
        - energy_density_y: Energy for E along y-axis
        - energy_density_z: Energy for E along z-axis
        - expected: Expected value (1/8π) ε E²
        - all_match: True if all orientations give same result
        - verified: True if results match expected within tolerance

    Reference:
        Part IV, Art. 630: Energy density verification.
    """
    # Test with field in different directions
    E_x = np.array([E_magnitude, 0, 0])
    E_y = np.array([0, E_magnitude, 0])
    E_z = np.array([0, 0, E_magnitude])

    u_x = calc_electrostatic_energy_density(E_x, permittivity)
    u_y = calc_electrostatic_energy_density(E_y, permittivity)
    u_z = calc_electrostatic_energy_density(E_z, permittivity)

    # Expected: u = (1/8π) ε E²
    expected = (permittivity / (8.0 * np.pi)) * E_magnitude**2

    # Verify all orientations give same result (isotropy)
    all_match = (
        np.isclose(u_x, u_y, rtol=tolerance)
        and np.isclose(u_y, u_z, rtol=tolerance)
        and np.isclose(u_x, expected, rtol=tolerance)
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
    630,
    631,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Complete electrostatic energy analysis",
)
def analyze_electrostatic_energy(
    E_field: np.ndarray,
    permittivity: float = 1.0,
    volume: float = None,
    capacitance: float = None,
    voltage: float = None,
) -> dict[str, float | np.ndarray]:
    """
    Perform comprehensive electrostatic energy analysis.

    Art. 630-631: Complete analysis of electrostatic energy including:

    1. Energy density from field
    2. Total energy in volume
    3. D field calculation
    4. Capacitor energy (if parameters provided)
    5. Field intensity and direction

    Args:
        E_field: Electric field vector (statvolts/cm).
        permittivity: Permittivity ε (default: 1.0).
        volume: Optional volume for total energy (cm³).
        capacitance: Optional capacitance for capacitor comparison (cm).
        voltage: Optional voltage for capacitor comparison (statvolts).

    Returns:
        Dictionary with:
        - E_field: Input electric field
        - E_magnitude: |E| (statvolts/cm)
        - D_field: Electric displacement (statcoulombs/cm²)
        - energy_density: u (erg/cm³)
        - total_energy: U (erg, if volume provided)
        - capacitor_energy: U_cap (erg, if C and V provided)
        - energy_ratio: E_field_energy / capacitor_energy

    Reference:
        Part IV, Arts. 630-631: Complete electrostatic energy analysis.
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    E_mag = np.linalg.norm(E_field)
    E_direction = E_field / E_mag if E_mag > 0 else np.zeros(3)

    # D field
    D_field = permittivity * E_field

    # Energy density
    energy_density = calc_electrostatic_energy_density(E_field, permittivity)

    result = {
        "E_field": E_field,
        "E_magnitude": E_mag,
        "E_direction": E_direction,
        "D_field": D_field,
        "permittivity": permittivity,
        "energy_density": energy_density,
    }

    # Total energy if volume provided
    if volume is not None:
        result["volume"] = volume
        result["total_energy"] = energy_density * volume

    # Capacitor energy if parameters provided
    if capacitance is not None and voltage is not None:
        cap_energy = calc_capacitor_energy(capacitance, voltage)
        result["capacitor_energy"] = cap_energy
        if volume is not None:
            result["energy_ratio"] = (energy_density * volume) / cap_energy

    return result


@maxwell_cite(
    630,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate energy density integrated over 3D field",
)
def integrate_energy_density(
    E_func: Callable[[np.ndarray], np.ndarray],
    volume_bounds: tuple[tuple[float, float], tuple[float, float], tuple[float, float]],
    permittivity: float = 1.0,
    n_points: int = 50,
) -> float:
    """
    Calculate total electrostatic energy by integrating energy density.

    Art. 630: For non-uniform fields, the total energy is:

        U = (1/8π) ∫∫∫ ε E² dV

    This function performs numerical integration over a rectangular volume.

    Args:
        E_func: Function returning E field (statvolts/cm) at position r.
        volume_bounds: ((x_min, x_max), (y_min, y_max), (z_min, z_max)) in cm.
        permittivity: Permittivity ε (default: 1.0).
        n_points: Number of sample points per dimension.

    Returns:
        Total electrostatic energy U (erg).

    Raises:
        ValueError: If permittivity not positive.

    Reference:
        Part IV, Art. 630: Energy integration over volume.

    Example:
        >>> # Uniform field in 1 cm³ volume
        >>> E_uniform = lambda r: np.array([1000, 0, 0])
        >>> bounds = ((0, 1), (0, 1), (0, 1))
        >>> U = integrate_energy_density(E_uniform, bounds)
        >>> print(f"U = {U} erg")
    """
    if permittivity <= 0:
        raise ValueError(f"Permittivity must be positive, got {permittivity}")

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

                E = np.asarray(E_func(r), dtype=np.float64)
                E_mag_sq = np.dot(E, E)

                # u = (1/8π) ε E²
                energy_density = (permittivity / (8.0 * np.pi)) * E_mag_sq
                total_energy += energy_density * dV

    return total_energy

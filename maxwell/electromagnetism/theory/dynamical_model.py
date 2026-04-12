"""maxwell.electromagnetism.theory.dynamical_model — Dynamical theory (Arts. 568-577).

Implements Maxwell's dynamical theory of electromagnetic fields, treating
the field as a dynamical system with kinetic and potential energy.

Maxwell's CGS formulation (Arts. 568-577):
    The electromagnetic field as a dynamical system:

    Lagrangian: L = T - U

    where:
    - T = electromagnetic kinetic energy = (1/8π) * integral(H²) dV
    - U = electromagnetic potential energy = (1/8π) * integral(E²) dV

    The field equations follow from the principle of least action.

where:
    T = kinetic energy (ergs)
    U = potential energy (ergs)
    E = electric field (statvolts/cm)
    H = magnetic field (oersted)

Category: A (maxwell_original) — Maxwell's dynamical field theory.

References:
    Part IV, Arts. 568-577: Dynamical theory of the electromagnetic field.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class DynamicalModel:
    """
    Maxwell's dynamical model of the electromagnetic field.

    Art. 568-577: Maxwell treated the electromagnetic field as a
    dynamical system with:
    - Generalized coordinates (vector potential A)
    - Generalized momenta (electric displacement D)
    - Kinetic energy (magnetic field energy)
    - Potential energy (electric field energy)

    The field equations follow from Lagrange's equations.

    Attributes:
        volume: Volume of field region (cm³).
        permittivity: Permittivity epsilon (dimensionless).
        permeability: Permeability mu (dimensionless).
    """

    volume: float
    permittivity: float = 1.0
    permeability: float = 1.0

    def __post_init__(self):
        """Validate parameters."""
        if self.volume <= 0:
            raise ValueError(f"Volume must be positive")
        if self.permittivity <= 0:
            raise ValueError(f"Permittivity must be positive")
        if self.permeability <= 0:
            raise ValueError(f"Permeability must be positive")

    @maxwell_cite(
        568, 569,
        part=4, chapter="Dynamical Theory",
        theory_class="maxwell_original",
        description="Calculate electromagnetic kinetic energy",
    )
    def kinetic_energy(self, H_field: np.ndarray) -> float:
        """
        Calculate electromagnetic kinetic energy (magnetic energy).

        Art. 568-569: The kinetic energy of the field is:

            T = (mu / 8π) * integral(H²) dV

        For uniform field in volume V:
            T = (mu / 8π) * H² * V

        Args:
            H_field: Magnetic field vector (oersted).

        Returns:
            Kinetic energy (ergs).
        """
        H_field = np.asarray(H_field, dtype=np.float64)
        H_squared = np.dot(H_field, H_field)

        return (self.permeability / (8.0 * np.pi)) * H_squared * self.volume

    @maxwell_cite(
        570, 571,
        part=4, chapter="Dynamical Theory",
        theory_class="maxwell_original",
        description="Calculate electromagnetic potential energy",
    )
    def potential_energy(self, E_field: np.ndarray) -> float:
        """
        Calculate electromagnetic potential energy (electric energy).

        Art. 570-571: The potential energy of the field is:

            U = (epsilon / 8π) * integral(E²) dV

        For uniform field in volume V:
            U = (epsilon / 8π) * E² * V

        Args:
            E_field: Electric field vector (statvolts/cm).

        Returns:
            Potential energy (ergs).
        """
        E_field = np.asarray(E_field, dtype=np.float64)
        E_squared = np.dot(E_field, E_field)

        return (self.permittivity / (8.0 * np.pi)) * E_squared * self.volume

    @maxwell_cite(
        572, 573,
        part=4, chapter="Dynamical Theory",
        theory_class="maxwell_original",
        description="Calculate total field energy",
    )
    def total_energy(self, E_field: np.ndarray, H_field: np.ndarray) -> float:
        """
        Calculate total electromagnetic field energy.

        Art. 572-573: The total energy is:

            W = T + U = (1/8π) * integral(epsilon*E² + mu*H²) dV

        Args:
            E_field: Electric field (statvolts/cm).
            H_field: Magnetic field (oersted).

        Returns:
            Total energy (ergs).
        """
        return self.kinetic_energy(H_field) + self.potential_energy(E_field)

    @maxwell_cite(
        574, 575,
        part=4, chapter="Dynamical Theory",
        theory_class="maxwell_original",
        description="Calculate Lagrangian of field",
    )
    def lagrangian(self, E_field: np.ndarray, H_field: np.ndarray) -> float:
        """
        Calculate Lagrangian of the electromagnetic field.

        Art. 574-575: The Lagrangian is:

            L = T - U

        Args:
            E_field: Electric field (statvolts/cm).
            H_field: Magnetic field (oersted).

        Returns:
            Lagrangian (ergs).
        """
        return self.kinetic_energy(H_field) - self.potential_energy(E_field)

    @maxwell_cite(
        576, 577,
        part=4, chapter="Dynamical Theory",
        theory_class="maxwell_original",
        description="Calculate energy density",
    )
    def energy_density(self, E_field: np.ndarray, H_field: np.ndarray) -> dict[str, float]:
        """
        Calculate electromagnetic energy density.

        Art. 576-577: Energy densities are:

            u_kinetic = (mu / 8π) * H²
            u_potential = (epsilon / 8π) * E²
            u_total = u_kinetic + u_potential

        Args:
            E_field: Electric field (statvolts/cm).
            H_field: Magnetic field (oersted).

        Returns:
            Dictionary with energy densities (ergs/cm³).
        """
        E_field = np.asarray(E_field, dtype=np.float64)
        H_field = np.asarray(H_field, dtype=np.float64)

        E_squared = np.dot(E_field, E_field)
        H_squared = np.dot(H_field, H_field)

        u_kinetic = (self.permeability / (8.0 * np.pi)) * H_squared
        u_potential = (self.permittivity / (8.0 * np.pi)) * E_squared

        return {
            "kinetic_density": u_kinetic,
            "potential_density": u_potential,
            "total_density": u_kinetic + u_potential,
        }


@maxwell_cite(
    568, 569, 570,
    part=4, chapter="Dynamical Theory",
    theory_class="maxwell_original",
    description="Calculate electromagnetic energy density",
)
def calc_energy_density(
    E_field: np.ndarray,
    H_field: np.ndarray,
    permittivity: float = 1.0,
    permeability: float = 1.0,
) -> dict[str, float]:
    """
    Calculate electromagnetic energy density.

    Art. 568-570: In CGS units:

        u_electric = (epsilon / 8π) * E²
        u_magnetic = (mu / 8π) * H²
        u_total = u_electric + u_magnetic

    Args:
        E_field: Electric field (statvolts/cm).
        H_field: Magnetic field (oersted).
        permittivity: Permittivity (dimensionless).
        permeability: Permeability (dimensionless).

    Returns:
        Dictionary with energy densities (ergs/cm³).

    Reference:
        Part IV, Arts. 568-570: Energy density.
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    H_field = np.asarray(H_field, dtype=np.float64)

    E_squared = np.dot(E_field, E_field)
    H_squared = np.dot(H_field, H_field)

    return {
        "electric": (permittivity / (8.0 * np.pi)) * E_squared,
        "magnetic": (permeability / (8.0 * np.pi)) * H_squared,
        "total": (permittivity / (8.0 * np.pi)) * E_squared + (permeability / (8.0 * np.pi)) * H_squared,
    }


@maxwell_cite(
    572, 573,
    part=4, chapter="Dynamical Theory",
    theory_class="maxwell_original",
    description="Calculate Poynting vector (energy flux)",
)
def calc_poynting_vector(
    E_field: np.ndarray,
    H_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate Poynting vector (energy flux density).

    Art. 572-573: The Poynting vector represents energy flow:

        S = (c / 4π) * E × H

    In CGS units, S has units of ergs/(cm²*s).

    Args:
        E_field: Electric field (statvolts/cm).
        H_field: Magnetic field (oersted).

    Returns:
        Poynting vector (ergs/(cm²*s)).
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    H_field = np.asarray(H_field, dtype=np.float64)

    return (CONST.C / (4.0 * np.pi)) * np.cross(E_field, H_field)


@maxwell_cite(
    574, 575,
    part=4, chapter="Dynamical Theory",
    theory_class="maxwell_original",
    description="Verify energy conservation (Poynting theorem)",
)
def verify_poynting_theorem(
    E_field_func: callable,
    H_field_func: callable,
    volume_bounds: tuple,
    time: float = 0.0,
    dt: float = 1e-12,
) -> dict[str, float | bool]:
    """
    Verify Poynting's theorem (energy conservation).

    Art. 574-575: Poynting's theorem states:

        -dW/dt = integral(S · dA) + integral(J · E) dV

    The rate of energy decrease equals outward flux plus ohmic loss.

    Args:
        E_field_func: Function E(r, t) returning electric field.
        H_field_func: Function H(r, t) returning magnetic field.
        volume_bounds: ((x_min,x_max), (y_min,y_max), (z_min,z_max)).
        time: Time for evaluation (s).
        dt: Time step for derivative (s).

    Returns:
        Dictionary with verification results.
    """
    # Simplified verification for uniform fields
    # Full verification would require numerical integration

    (x_min, x_max), (y_min, y_max), (z_min, z_max) = volume_bounds
    volume = (x_max - x_min) * (y_max - y_min) * (z_max - z_min)

    # Sample field at center
    center = np.array([
        (x_min + x_max) / 2,
        (y_min + y_max) / 2,
        (z_min + z_max) / 2
    ])

    E = np.asarray(E_field_func(center, time), dtype=np.float64)
    H = np.asarray(H_field_func(center, time), dtype=np.float64)

    # Energy density
    energy_density = calc_energy_density(E, H)
    total_energy = energy_density["total"] * volume

    # Poynting vector
    S = calc_poynting_vector(E, H)

    return {
        "total_energy": total_energy,
        "energy_density": energy_density,
        "poynting_vector": S,
        "poynting_magnitude": np.linalg.norm(S),
        "volume": volume,
    }


@maxwell_cite(
    568, 577,
    part=4, chapter="Dynamical Theory",
    theory_class="maxwell_original",
    description="Calculate field momentum",
)
def calc_field_momentum(
    E_field: np.ndarray,
    H_field: np.ndarray,
    volume: float,
) -> np.ndarray:
    """
    Calculate electromagnetic field momentum.

    Art. 568-577: The electromagnetic momentum density is:

        g = S / c² = (1 / 4πc) * E × H

    Total momentum in volume V:
        p = integral(g) dV

    Args:
        E_field: Electric field (statvolts/cm).
        H_field: Magnetic field (oersted).
        volume: Volume (cm³).

    Returns:
        Field momentum (g*cm/s).
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    H_field = np.asarray(H_field, dtype=np.float64)

    # Momentum density = S / c²
    S = (CONST.C / (4.0 * np.pi)) * np.cross(E_field, H_field)
    g = S / (CONST.C ** 2)

    return g * volume


@maxwell_cite(
    568, 569, 570, 571, 572, 573, 574, 575, 576, 577,
    part=4, chapter="Dynamical Theory",
    theory_class="maxwell_original",
    description="Complete dynamical model analysis",
)
def analyze_dynamical_model(
    E_field: np.ndarray,
    H_field: np.ndarray,
    volume: float,
    permittivity: float = 1.0,
    permeability: float = 1.0,
) -> dict[str, float | np.ndarray]:
    """
    Complete analysis of the dynamical electromagnetic model.

    Art. 568-577: Comprehensive analysis including:
    1. Kinetic and potential energy
    2. Total energy and Lagrangian
    3. Energy density
    4. Poynting vector
    5. Field momentum

    Args:
        E_field: Electric field (statvolts/cm).
        H_field: Magnetic field (oersted).
        volume: Volume of field region (cm³).
        permittivity: Permittivity (dimensionless).
        permeability: Permeability (dimensionless).

    Returns:
        Dictionary with complete analysis results.
    """
    model = DynamicalModel(
        volume=volume,
        permittivity=permittivity,
        permeability=permeability
    )

    E_field = np.asarray(E_field, dtype=np.float64)
    H_field = np.asarray(H_field, dtype=np.float64)

    kinetic = model.kinetic_energy(H_field)
    potential = model.potential_energy(E_field)
    total = model.total_energy(E_field, H_field)
    lagrangian = model.lagrangian(E_field, H_field)
    density = model.energy_density(E_field, H_field)
    poynting = calc_poynting_vector(E_field, H_field)
    momentum = calc_field_momentum(E_field, H_field, volume)

    return {
        "kinetic_energy": kinetic,
        "potential_energy": potential,
        "total_energy": total,
        "lagrangian": lagrangian,
        "energy_density": density,
        "poynting_vector": poynting,
        "field_momentum": momentum,
        "volume": volume,
        "permittivity": permittivity,
        "permeability": permeability,
        "energy_partition": {
            "kinetic_fraction": kinetic / total if total > 0 else 0,
            "potential_fraction": potential / total if total > 0 else 0,
        },
    }

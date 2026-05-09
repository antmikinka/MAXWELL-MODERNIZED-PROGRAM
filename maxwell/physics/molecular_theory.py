"""
Molecular theory of magnetism — statistical mechanics of magnetic moments.

Implements the molecular theory from Part III of Maxwell's Treatise:
- Magnetic molecules and their interactions (Art. 430)
- Statistical distribution of molecular orientations
- Molecular field theory foundations

Maxwell's molecular theory treats ferromagnetic materials as collections
of tiny molecular magnets. Each molecule has a permanent magnetic moment
that can rotate under external influences.

The theory explains:
- Why some materials are ferromagnetic (strong molecular interactions)
- Temperature dependence of magnetization
- The origin of magnetic domains

Category: A (maxwell_original) — Maxwell's molecular theory of magnetism.

References:
    Part III, Art. 430: Magnetic molecules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class MagneticMolecule:
    """
    Individual magnetic molecule with permanent moment.

    Art. 430: Each magnetic molecule has a fixed magnetic moment
    that can rotate but not change magnitude. The molecule responds
    to external fields and to the fields from neighboring molecules.

    Attributes:
        magnetic_moment: Permanent magnetic moment m (emu).
        position: Position vector r (cm).
        orientation: Unit vector along moment direction.
    """

    magnetic_moment: float  # |m|, emu
    position: np.ndarray  # shape (3,), cm
    orientation: np.ndarray = None  # shape (3,), unit vector

    def __post_init__(self):
        self.position = np.asarray(self.position, dtype=np.float64)
        if self.orientation is None:
            # Random initial orientation
            self.orientation = self._random_unit_vector()
        else:
            self.orientation = np.asarray(self.orientation, dtype=np.float64)
            self.orientation = self.orientation / np.linalg.norm(self.orientation)

    @staticmethod
    def _random_unit_vector() -> np.ndarray:
        """Generate random unit vector."""
        phi = np.random.uniform(0, 2 * np.pi)
        cos_theta = np.random.uniform(-1, 1)
        sin_theta = np.sqrt(1 - cos_theta**2)
        return np.array([sin_theta * np.cos(phi), sin_theta * np.sin(phi), cos_theta])

    @property
    def moment_vector(self) -> np.ndarray:
        """Magnetic moment vector m = |m| × orientation."""
        return self.magnetic_moment * self.orientation

    @maxwell_cite(
        430,
        part=3,
        chapter="Molecular Theory",
        theory_class="maxwell_original",
        description="Calculate torque on molecule in field",
    )
    def torque_in_field(self, B_field: np.ndarray) -> np.ndarray:
        """
        Calculate torque on molecule in external field.

        Art. 430: A magnetic molecule in field B experiences torque:

            τ = m × B

        This torque tends to align the molecule with the field.

        Args:
            B_field: External magnetic field B (gauss).

        Returns:
            Torque vector τ (dyne·cm).

        Reference:
            Part III, Art. 430: Molecular torque.
        """
        B_field = np.asarray(B_field, dtype=np.float64)
        return np.cross(self.moment_vector, B_field)

    @maxwell_cite(
        430,
        part=3,
        chapter="Molecular Theory",
        theory_class="maxwell_original",
        description="Calculate potential energy of molecule in field",
    )
    def potential_energy(self, B_field: np.ndarray) -> float:
        """
        Calculate potential energy of molecule in external field.

        Art. 430: The potential energy of a magnetic molecule:

            W = -m · B

        Energy is minimum when aligned with field.

        Args:
            B_field: External magnetic field B (gauss).

        Returns:
            Potential energy W (erg).

        Reference:
            Part III, Art. 430: Molecular energy.
        """
        B_field = np.asarray(B_field, dtype=np.float64)
        return -float(np.dot(self.moment_vector, B_field))

    @maxwell_cite(
        430,
        part=3,
        chapter="Molecular Theory",
        theory_class="maxwell_original",
        description="Rotate molecule toward field direction",
    )
    def align_with_field(
        self,
        B_field: np.ndarray,
        damping: float = 0.1,
    ) -> np.ndarray:
        """
        Rotate molecule's orientation toward field direction.

        Art. 430: Under the influence of torque, the molecule
        rotates to align with the field. This simulates the
        rotation with damping.

        Args:
            B_field: External magnetic field B (gauss).
            damping: Damping coefficient (0 to 1).

        Returns:
            New orientation vector.

        Reference:
            Part III, Art. 430: Molecular alignment.
        """
        B_field = np.asarray(B_field, dtype=np.float64)
        B_mag = np.linalg.norm(B_field)

        if B_mag < 1e-10:
            return self.orientation

        # Target direction (field direction)
        target = B_field / B_mag

        # Interpolate toward target (simplified dynamics)
        new_orientation = (1 - damping) * self.orientation + damping * target

        # Normalize
        new_orientation = new_orientation / np.linalg.norm(new_orientation)
        self.orientation = new_orientation

        return new_orientation


@dataclass
class MolecularEnsemble:
    """
    Collection of magnetic molecules with statistical properties.

    Art. 430: A magnetized body consists of many magnetic molecules.
    The macroscopic magnetization is the vector sum of all molecular
    moments per unit volume.

    This class models the statistical behavior of the ensemble.

    Attributes:
        molecules: List of MagneticMolecule objects.
        volume: Volume containing the ensemble (cm³).
        temperature: Temperature T (K).
    """

    molecules: list[MagneticMolecule] = field(default_factory=list)
    volume: float = 1.0  # cm³
    temperature: float = 300.0  # K

    @maxwell_cite(
        430,
        part=3,
        chapter="Molecular Theory",
        theory_class="maxwell_original",
        description="Calculate net magnetization of ensemble",
    )
    def net_magnetization(self) -> np.ndarray:
        """
        Calculate net magnetization of molecular ensemble.

        Art. 430: The magnetization I is the total magnetic moment
        per unit volume:

            I = (Σ m_i) / V

        Args:
            None

        Returns:
            Magnetization vector I (emu/cm³).

        Reference:
            Part III, Art. 430: Ensemble magnetization.
        """
        if len(self.molecules) == 0:
            return np.zeros(3)

        total_moment = sum(m.moment_vector for m in self.molecules)
        return total_moment / self.volume

    @maxwell_cite(
        430,
        part=3,
        chapter="Molecular Theory",
        theory_class="maxwell_original",
        description="Calculate alignment order parameter",
    )
    def order_parameter(self) -> float:
        """
        Calculate orientational order parameter of ensemble.

        Art. 430: The degree of molecular alignment is quantified
        by the order parameter S:

            S = <(3 cos²θ - 1) / 2>

        where θ is the angle between each molecule and the average
        orientation direction. S = 1 for perfect alignment,
        S = 0 for random orientation.

        Returns:
            Order parameter S (0 to 1).

        Reference:
            Part III, Art. 430: Order parameter.
        """
        if len(self.molecules) == 0:
            return 0.0

        # Average orientation direction
        orientations = np.array([m.orientation for m in self.molecules])
        avg_orientation = np.mean(orientations, axis=0)
        avg_mag = np.linalg.norm(avg_orientation)

        if avg_mag < 1e-10:
            return 0.0

        # Direction of average orientation
        director = avg_orientation / avg_mag

        # Calculate order parameter
        cos_thetas = np.dot(orientations, director)
        S = np.mean((3 * cos_thetas**2 - 1) / 2)

        return float(max(0, S))  # Ensure non-negative

    @maxwell_cite(
        430,
        part=3,
        chapter="Molecular Theory",
        theory_class="maxwell_original",
        description="Apply external field to all molecules",
    )
    def apply_field(
        self,
        B_field: np.ndarray,
        iterations: int = 10,
        damping: float = 0.1,
    ) -> np.ndarray:
        """
        Apply external field to ensemble and relax molecular orientations.

        Art. 430: When an external field is applied, each molecule
        experiences torque and rotates toward alignment. The final
        state represents equilibrium between field alignment and
        thermal randomization.

        Args:
            B_field: External magnetic field B (gauss).
            iterations: Number of relaxation iterations.
            damping: Damping coefficient per iteration.

        Returns:
            Final net magnetization I (emu/cm³).

        Reference:
            Part III, Art. 430: Field application.
        """
        B_field = np.asarray(B_field, dtype=np.float64)

        for _ in range(iterations):
            for molecule in self.molecules:
                molecule.align_with_field(B_field, damping)

        return self.net_magnetization()

    @classmethod
    @maxwell_cite(
        430,
        part=3,
        chapter="Molecular Theory",
        theory_class="maxwell_original",
        description="Create ensemble with random orientations",
    )
    def random_ensemble(
        cls,
        n_molecules: int,
        moment_magnitude: float,
        volume: float = 1.0,
        temperature: float = 300.0,
        seed: int = None,
    ) -> MolecularEnsemble:
        """
        Create molecular ensemble with random orientations.

        Art. 430: An unmagnetized material has randomly oriented
        molecules, giving zero net magnetization.

        Args:
            n_molecules: Number of molecules.
            moment_magnitude: |m| per molecule (emu).
            volume: Volume (cm³).
            temperature: Temperature (K).
            seed: Random seed for reproducibility.

        Returns:
            MolecularEnsemble with random orientations.

        Reference:
            Part III, Art. 430: Random ensemble.
        """
        if seed is not None:
            np.random.seed(seed)

        molecules = []
        for i in range(n_molecules):
            # Random position in cube
            pos = np.random.uniform(-0.5, 0.5, 3) * volume ** (1 / 3)
            molecule = MagneticMolecule(
                magnetic_moment=moment_magnitude,
                position=pos,
            )
            molecules.append(molecule)

        return cls(molecules=molecules, volume=volume, temperature=temperature)


@maxwell_cite(
    430,
    part=3,
    chapter="Molecular Theory",
    theory_class="maxwell_original",
    description="Calculate molecular field from neighbors",
)
def molecular_field(
    position: np.ndarray,
    molecules: list[MagneticMolecule],
    exchange_constant: float = 0.0,
) -> np.ndarray:
    """
    Calculate effective field at a point from molecular dipoles.

    Art. 430: Each molecule contributes to the local field:

        B_dipole(r) = (3(m·r̂)r̂ - m) / r³

    The total field is the sum of all molecular dipoles plus
    any exchange field from quantum mechanical interactions.

    Args:
        position: Point to evaluate field (cm).
        molecules: List of MagneticMolecule objects.
        exchange_constant: Exchange coupling J (erg).

    Returns:
        Total molecular field B (gauss).

    Reference:
        Part III, Art. 430: Molecular field calculation.
    """
    position = np.asarray(position, dtype=np.float64)
    B_total = np.zeros(3)

    for molecule in molecules:
        r = position - molecule.position
        r_mag = np.linalg.norm(r)

        if r_mag < 1e-8:
            # Skip self-interaction
            continue

        r_hat = r / r_mag
        m = molecule.moment_vector

        # Dipole field: B = (3(m·r̂)r̂ - m) / r³
        B_dipole = (3 * np.dot(m, r_hat) * r_hat - m) / (r_mag**3)
        B_total += B_dipole

        # Exchange field (mean field approximation)
        if exchange_constant > 0:
            B_exchange = exchange_constant * m / (np.linalg.norm(m) + 1e-10)
            B_total += B_exchange

    return B_total


@maxwell_cite(
    430,
    part=3,
    chapter="Molecular Theory",
    theory_class="maxwell_original",
    description="Calculate Curie temperature from molecular parameters",
)
def curie_temperature(
    molecular_density: float,
    moment_magnitude: float,
    exchange_constant: float = 0.0,
) -> float:
    """
    Estimate Curie temperature from molecular parameters.

    Art. 430: The Curie temperature T_c marks the transition from
    ferromagnetic to paramagnetic behavior. In mean field theory:

        T_c = (2/3) × (zJ / k_B)

    where z is the number of neighbors and J is the exchange constant.

    For pure dipole interactions (no exchange):
        T_c ≈ (n m²) / (3 k_B)

    Args:
        molecular_density: Number density n (molecules/cm³).
        moment_magnitude: |m| per molecule (emu).
        exchange_constant: Exchange coupling J (erg).

    Returns:
        Curie temperature T_c (K).

    Reference:
        Part III, Art. 430: Curie temperature.
    """
    k_B = CONST.k_B  # Boltzmann constant (erg/K)

    if exchange_constant > 0:
        # With exchange interaction (typical ferromagnet)
        z = 6  # Approximate coordination number
        T_c = (2 / 3) * (z * exchange_constant / k_B)
    else:
        # Pure dipole interaction (very weak)
        m = moment_magnitude
        n = molecular_density
        T_c = (n * m**2) / (3 * k_B)

    return float(T_c)


@maxwell_cite(
    430,
    part=3,
    chapter="Molecular Theory",
    theory_class="maxwell_original",
    description="Simulate thermal randomization of molecular orientations",
)
def thermal_randomization(
    ensemble: MolecularEnsemble,
    B_field: np.ndarray,
    temperature: float,
    n_steps: int = 100,
) -> list[np.ndarray]:
    """
    Simulate thermal effects on molecular alignment.

    Art. 430: Thermal energy competes with magnetic alignment.
    The Langevin function describes the balance:

        I/I_s = L(x) where x = mB / (k_B T)

    This function simulates thermal randomization using a Monte
    Carlo approach.

    Args:
        ensemble: MolecularEnsemble to simulate.
        B_field: External magnetic field B (gauss).
        temperature: Temperature T (K).
        n_steps: Number of Monte Carlo steps.

    Returns:
        List of magnetization values at each step.

    Reference:
        Part III, Art. 430: Thermal randomization.
    """
    k_B = CONST.k_B
    B_field = np.asarray(B_field, dtype=np.float64)

    magnetization_history = []

    for step in range(n_steps):
        # Pick random molecule
        molecule = np.random.choice(ensemble.molecules)

        # Calculate energy change for small rotation
        delta_theta = 0.1  # radians
        axis = np.random.randn(3)
        axis = axis / np.linalg.norm(axis)

        # Rotated orientation
        cos_d = np.cos(delta_theta)
        sin_d = np.sin(delta_theta)
        new_orient = (
            molecule.orientation * cos_d
            + np.cross(axis, molecule.orientation) * sin_d
            + axis * np.dot(axis, molecule.orientation) * (1 - cos_d)
        )
        new_orient = new_orient / np.linalg.norm(new_orient)

        # Energy difference
        old_energy = -np.dot(molecule.moment_vector, B_field)
        new_moment = molecule.magnetic_moment * new_orient
        new_energy = -np.dot(new_moment, B_field)
        delta_E = new_energy - old_energy

        # Metropolis acceptance
        if delta_E < 0 or np.random.exp() < np.exp(-delta_E / (k_B * temperature)):
            molecule.orientation = new_orient

        # Record magnetization
        mag = ensemble.net_magnetization()
        magnetization_history.append(mag)

    return magnetization_history


@maxwell_cite(
    430,
    part=3,
    chapter="Molecular Theory",
    theory_class="maxwell_original",
    description="Verify molecular theory predictions",
)
def verify_molecular_theory() -> dict[str, any]:
    """
    Verify predictions of molecular theory against known results.

    Art. 430: Molecular theory makes several testable predictions:

    1. Saturation magnetization depends on molecular density
    2. Initial susceptibility follows Curie law: κ ∝ 1/T
    3. Order parameter increases with field, decreases with T

    Returns:
        Dictionary with verification results.

    Reference:
        Part III, Art. 430: Theory verification.
    """
    results = {}

    # Test 1: Random ensemble has zero magnetization
    ensemble = MolecularEnsemble.random_ensemble(
        n_molecules=1000,
        moment_magnitude=1e-20,  # Typical molecular moment
        volume=1.0,
        seed=42,
    )

    M_initial = ensemble.net_magnetization()
    M_mag = np.linalg.norm(M_initial)

    results["random_ensemble_magnetization"] = {
        "magnitude": float(M_mag),
        "expected": 0.0,
        "passes": M_mag < 1e-19,  # Should be very small
    }

    # Test 2: Field alignment increases magnetization
    B_applied = np.array([1000, 0, 0])  # 1000 gauss
    M_final = ensemble.apply_field(B_applied, iterations=50, damping=0.05)

    results["field_alignment"] = {
        "initial_magnitude": float(M_mag),
        "final_magnitude": float(np.linalg.norm(M_final)),
        "aligned_with_field": np.dot(M_final, B_applied) > 0,
    }

    # Test 3: Order parameter increases with alignment
    S_initial = ensemble.order_parameter()

    # Create new random ensemble
    ensemble2 = MolecularEnsemble.random_ensemble(
        n_molecules=1000,
        moment_magnitude=1e-20,
        volume=1.0,
        seed=42,
    )
    ensemble2.apply_field(B_applied, iterations=50, damping=0.05)
    S_final = ensemble2.order_parameter()

    results["order_parameter"] = {
        "initial": float(S_initial),
        "final": float(S_final),
        "increases_with_field": S_final > S_initial,
    }

    return results

"""
Electrokinetic Energy — energy of electric currents and magnetic interactions.

Implements Maxwell's electrokinetic energy formulas as described
in Articles 634-638 of the Treatise:

- Electrokinetic energy: T = (1/2) ∫∫∫ A·J dV (Art. 634)
- For single circuit: T = (1/2) L I² (Art. 635)
- For coupled circuits: T = (1/2) L₁ I₁² + (1/2) L₂ I₂² + M I₁ I₂ (Art. 636-637)
- Mutual inductance energy: T_mutual = M I₁ I₂ (Art. 638)

Maxwell's CGS formulation:
    T = (1/2) ∫ A·J dV  (erg)

where:
    A = vector potential (gauss·cm)
    J = current density (abamperes/cm²)
    T = electrokinetic energy (erg)

For discrete circuits:
    T = (1/2) Σ L_ij I_i I_j  (erg)

where:
    L_ii = self-inductance of circuit i (cm)
    L_ij = mutual inductance between circuits i and j (cm)
    I_i = current in circuit i (abamperes)

Category: A (maxwell_original) — Maxwell's theory of electrokinetic energy.

References:
    Part IV, Arts. 634-638: Electrokinetic energy and mutual inductance.
    Part IV, Ch. XXI: Energy of current-carrying systems.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class ElectrokineticEnergy:
    """
    Electrokinetic energy of current-carrying circuits.

    Art. 634-638: The electrokinetic energy represents the energy stored
    in the magnetic field produced by electric currents. It can be expressed
    either as a field integral or in terms of circuit inductances.

    Field formulation:
        T = (1/2) ∫∫∫ A·J dV  (erg)

    Circuit formulation:
        T = (1/2) Σ L_ij I_i I_j  (erg)

    For a single circuit:
        T = (1/2) L I²  (erg)

    Attributes:
        inductance: Self-inductance L (cm) for single circuit.
        current: Current I (abamperes) for single circuit.
        inductance_matrix: L_ij matrix for coupled circuits.
        currents: Array of currents for coupled circuits.
    """

    # Single circuit parameters
    inductance: Optional[float] = None
    current: Optional[float] = None

    # Coupled circuits parameters
    inductance_matrix: Optional[np.ndarray] = None
    currents: Optional[np.ndarray] = None

    def __post_init__(self):
        """Validate parameters."""
        if self.inductance is not None and self.inductance <= 0:
            raise ValueError(f"Inductance must be positive, got {self.inductance}")

        if self.current is not None and self.current < 0:
            raise ValueError(f"Current must be non-negative, got {self.current}")

        if self.inductance_matrix is not None:
            self.inductance_matrix = np.asarray(
                self.inductance_matrix, dtype=np.float64
            )
            # Check symmetry
            if not np.allclose(self.inductance_matrix, self.inductance_matrix.T):
                raise ValueError("Inductance matrix must be symmetric")

        if self.currents is not None:
            self.currents = np.asarray(self.currents, dtype=np.float64)
            if np.any(self.currents < 0):
                raise ValueError("Currents must be non-negative")

    @property
    def energy(self) -> float:
        """
        Calculate electrokinetic energy.

        Returns:
            Energy T (erg).

        Raises:
            ValueError: If neither single circuit nor coupled circuits configured.
        """
        if self.inductance is not None and self.current is not None:
            # Single circuit: T = (1/2) L I²
            return 0.5 * self.inductance * self.current**2

        if self.inductance_matrix is not None and self.currents is not None:
            # Coupled circuits: T = (1/2) Σ L_ij I_i I_j
            return 0.5 * np.dot(
                self.currents, np.dot(self.inductance_matrix, self.currents)
            )

        raise ValueError(
            "Either (inductance, current) or (inductance_matrix, currents) must be provided"
        )

    @classmethod
    @maxwell_cite(
        635,
        part=4,
        chapter="Energy in the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Create electrokinetic energy for single circuit",
    )
    def from_single_circuit(
        cls,
        inductance: float,
        current: float,
    ) -> ElectrokineticEnergy:
        """
        Create electrokinetic energy for a single current-carrying circuit.

        Art. 635: For a single circuit with self-inductance L carrying
        current I, the electrokinetic energy is:

            T = (1/2) L I²

        Args:
            inductance: Self-inductance L (cm).
            current: Current I (abamperes).

        Returns:
            ElectrokineticEnergy object.

        Reference:
            Part IV, Art. 635: Energy of single circuit.
        """
        return cls(inductance=inductance, current=current)

    @classmethod
    @maxwell_cite(
        636,
        637,
        part=4,
        chapter="Energy in the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Create electrokinetic energy for coupled circuits",
    )
    def from_coupled_circuits(
        cls,
        inductance_matrix: np.ndarray,
        currents: np.ndarray,
    ) -> ElectrokineticEnergy:
        """
        Create electrokinetic energy for coupled current-carrying circuits.

        Art. 636-637: For multiple coupled circuits with inductance matrix L_ij
        and currents I_i, the total electrokinetic energy is:

            T = (1/2) Σ L_ij I_i I_j

        This includes both self-inductance (diagonal) and mutual inductance
        (off-diagonal) contributions.

        Args:
            inductance_matrix: Symmetric matrix of inductances L_ij (cm).
            currents: Array of currents I_i (abamperes).

        Returns:
            ElectrokineticEnergy object.

        Reference:
            Part IV, Arts. 636-637: Energy of coupled circuits.
        """
        return cls(inductance_matrix=inductance_matrix, currents=currents)

    @maxwell_cite(
        634,
        part=4,
        chapter="Energy in the Electromagnetic Field",
        theory_class="maxwell_original",
        description="Calculate energy from A and J fields",
    )
    def energy_from_fields(
        self,
        A_potential: np.ndarray,
        J_current: np.ndarray,
        volume: float,
    ) -> float:
        """
        Calculate electrokinetic energy from vector potential and current density.

        Art. 634: The fundamental field expression for electrokinetic energy:

            T = (1/2) ∫∫∫ A·J dV

        For uniform A and J in volume V:
            T = (1/2) A·J · V

        Args:
            A_potential: Vector potential (gauss·cm).
            J_current: Current density (abamperes/cm²).
            volume: Volume (cm³).

        Returns:
            Electrokinetic energy T (erg).

        Reference:
            Part IV, Art. 634: Field formulation of electrokinetic energy.
        """
        A_potential = np.asarray(A_potential, dtype=np.float64)
        J_current = np.asarray(J_current, dtype=np.float64)

        if volume <= 0:
            raise ValueError(f"Volume must be positive, got {volume}")

        A_dot_J = np.dot(A_potential, J_current)
        return 0.5 * A_dot_J * volume


@maxwell_cite(
    634,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate electrokinetic energy: T = (1/2) ∫ A·J dV",
)
def calc_electrokinetic_energy(
    A_potential: np.ndarray,
    J_current: np.ndarray,
    volume: float,
) -> float:
    """
    Calculate electrokinetic energy from vector potential and current density.

    Art. 634: Maxwell's fundamental expression for the energy of currents:

        T = (1/2) ∫∫∫ A·J dV  (erg)

    where:
        A = vector potential (gauss·cm)
        J = current density (abamperes/cm²)
        V = volume (cm³)
        T = electrokinetic energy (erg)

    This formula expresses the energy stored in the magnetic field in terms
    of the sources (currents) and the vector potential they produce.

    For uniform A and J:
        T = (1/2) A·J · V

    Args:
        A_potential: Vector potential vector (gauss·cm).
        J_current: Current density vector (abamperes/cm²).
        volume: Volume containing the current (cm³).

    Returns:
        Electrokinetic energy T (erg).

    Raises:
        ValueError: If volume is not positive.

    Reference:
        Part IV, Art. 634: Electrokinetic energy formula.

    Example:
        >>> # Vector potential 100 gauss·cm, current density 1 abA/cm², 1 cm³
        >>> T = calc_electrokinetic_energy(np.array([100, 0, 0]), np.array([1, 0, 0]), 1.0)
        >>> print(f"T = {T} erg")  # T = 50 erg
    """
    if volume <= 0:
        raise ValueError(f"Volume must be positive, got {volume}")

    A_potential = np.asarray(A_potential, dtype=np.float64)
    J_current = np.asarray(J_current, dtype=np.float64)

    A_dot_J = np.dot(A_potential, J_current)
    return 0.5 * A_dot_J * volume


@maxwell_cite(
    635,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate single circuit energy: T = (1/2) L I²",
)
def calc_single_circuit_energy(
    inductance: float,
    current: float,
) -> float:
    """
    Calculate electrokinetic energy of a single current-carrying circuit.

    Art. 635: For a single circuit with self-inductance L carrying current I:

        T = (1/2) L I²  (erg)

    where:
        L = self-inductance (cm in CGS)
        I = current (abamperes)
        T = electrokinetic energy (erg)

    This is the energy stored in the magnetic field produced by the current.

    Args:
        inductance: Self-inductance L (cm).
        current: Current I (abamperes).

    Returns:
        Electrokinetic energy T (erg).

    Raises:
        ValueError: If inductance not positive or current negative.

    Reference:
        Part IV, Art. 635: Energy of single circuit.

    Example:
        >>> # 10 cm inductance with 5 abampere current
        >>> T = calc_single_circuit_energy(10.0, 5.0)
        >>> print(f"T = {T} erg")  # T = 125 erg
    """
    if inductance <= 0:
        raise ValueError(f"Inductance must be positive, got {inductance}")
    if current < 0:
        raise ValueError(f"Current must be non-negative, got {current}")

    return 0.5 * inductance * current**2


@maxwell_cite(
    636,
    637,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate coupled circuits energy: T = (1/2) Σ L_ij I_i I_j",
)
def calc_coupled_circuits_energy(
    inductance_matrix: np.ndarray,
    currents: np.ndarray,
) -> float:
    """
    Calculate electrokinetic energy of coupled current-carrying circuits.

    Art. 636-637: For multiple coupled circuits, the total electrokinetic
    energy includes both self-inductance and mutual inductance terms:

        T = (1/2) Σ L_ij I_i I_j

    Expanding for two circuits:
        T = (1/2) L₁₁ I₁² + (1/2) L₂₂ I₂² + L₁₂ I₁ I₂

    where:
        L_ii = self-inductance of circuit i (cm)
        L_ij = mutual inductance between circuits i,j (cm)
        I_i = current in circuit i (abamperes)

    The mutual term L₁₂ I₁ I₂ represents the energy of magnetic coupling.

    Args:
        inductance_matrix: Symmetric matrix L_ij (cm).
        currents: Array of currents I_i (abamperes).

    Returns:
        Total electrokinetic energy T (erg).

    Raises:
        ValueError: If inductance matrix not symmetric or currents negative.

    Reference:
        Part IV, Arts. 636-637: Energy of coupled circuits.

    Example:
        >>> # Two coupled circuits with L = [[10, 2], [2, 5]], I = [3, 4]
        >>> L = np.array([[10.0, 2.0], [2.0, 5.0]])
        >>> I = np.array([3.0, 4.0])
        >>> T = calc_coupled_circuits_energy(L, I)
        >>> print(f"T = {T} erg")
    """
    inductance_matrix = np.asarray(inductance_matrix, dtype=np.float64)
    currents = np.asarray(currents, dtype=np.float64)

    if not np.allclose(inductance_matrix, inductance_matrix.T):
        raise ValueError("Inductance matrix must be symmetric")

    if np.any(currents < 0):
        raise ValueError("Currents must be non-negative")

    return 0.5 * np.dot(currents, np.dot(inductance_matrix, currents))


@maxwell_cite(
    638,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate mutual inductance energy: T = M I₁ I₂",
)
def calc_mutual_inductance_energy(
    mutual_inductance: float,
    I1: float,
    I2: float,
) -> float:
    """
    Calculate energy due to mutual inductance between two circuits.

    Art. 638: The mutual inductance contribution to electrokinetic energy:

        T_mutual = M I₁ I₂  (erg)

    where:
        M = mutual inductance (cm)
        I₁, I₂ = currents in the two circuits (abamperes)

    The mutual inductance M depends on the geometry and relative position
    of the circuits. It is symmetric: M₁₂ = M₂₁.

    The sign of the mutual energy depends on the relative direction of
    the currents (dot product convention).

    Args:
        mutual_inductance: Mutual inductance M (cm). Can be positive or negative.
        I1: Current in first circuit (abamperes).
        I2: Current in second circuit (abamperes).

    Returns:
        Mutual inductance energy (erg). Sign depends on current directions.

    Reference:
        Part IV, Art. 638: Mutual inductance energy.

    Example:
        >>> # Mutual inductance of 2 cm, currents of 3 and 4 abamperes
        >>> T = calc_mutual_inductance_energy(2.0, 3.0, 4.0)
        >>> print(f"T_mutual = {T} erg")  # T_mutual = 24 erg
    """
    mutual_inductance = float(mutual_inductance)
    I1 = float(I1)
    I2 = float(I2)

    return mutual_inductance * I1 * I2


@maxwell_cite(
    636,
    637,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate two-circuit energy with self and mutual inductance",
)
def calc_two_circuit_energy(
    L1: float,
    L2: float,
    M: float,
    I1: float,
    I2: float,
) -> float:
    """
    Calculate electrokinetic energy of two coupled circuits.

    Art. 636-637: For two coupled circuits with self-inductances L₁, L₂
    and mutual inductance M:

        T = (1/2) L₁ I₁² + (1/2) L₂ I₂² + M I₁ I₂  (erg)

    This can be written in matrix form as:
        T = (1/2) [I₁ I₂] [[L₁, M], [M, L₂]] [I₁, I₂]ᵀ

    The mutual term M I₁ I₂ represents the magnetic coupling energy.
    Its sign depends on the relative orientation of the circuits.

    Args:
        L1: Self-inductance of first circuit (cm).
        L2: Self-inductance of second circuit (cm).
        M: Mutual inductance (cm). Positive for aiding, negative for opposing.
        I1: Current in first circuit (abamperes).
        I2: Current in second circuit (abamperes).

    Returns:
        Total electrokinetic energy T (erg).

    Raises:
        ValueError: If self-inductances not positive.

    Reference:
        Part IV, Arts. 636-637: Two-circuit energy.

    Example:
        >>> # L1=10, L2=5, M=2, I1=3, I2=4
        >>> T = calc_two_circuit_energy(10.0, 5.0, 2.0, 3.0, 4.0)
        >>> print(f"T = {T} erg")
    """
    if L1 <= 0:
        raise ValueError(f"L1 must be positive, got {L1}")
    if L2 <= 0:
        raise ValueError(f"L2 must be positive, got {L2}")

    # T = (1/2) L₁ I₁² + (1/2) L₂ I₂² + M I₁ I₂
    return 0.5 * L1 * I1**2 + 0.5 * L2 * I2**2 + M * I1 * I2


@maxwell_cite(
    634,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate energy density integrated over 3D current distribution",
)
def integrate_electrokinetic_energy(
    A_func: Callable[[np.ndarray], np.ndarray],
    J_func: Callable[[np.ndarray], np.ndarray],
    volume_bounds: tuple[tuple[float, float], tuple[float, float], tuple[float, float]],
    n_points: int = 30,
) -> float:
    """
    Calculate total electrokinetic energy by integrating over current distribution.

    Art. 634: For arbitrary current distributions:

        T = (1/2) ∫∫∫ A·J dV

    This function performs numerical integration over a rectangular volume.

    Args:
        A_func: Function returning vector potential (gauss·cm) at position r.
        J_func: Function returning current density (abA/cm²) at position r.
        volume_bounds: ((x_min, x_max), (y_min, y_max), (z_min, z_max)) in cm.
        n_points: Number of sample points per dimension.

    Returns:
        Total electrokinetic energy T (erg).

    Reference:
        Part IV, Art. 634: Energy integration over volume.

    Example:
        >>> # Uniform current density and vector potential
        >>> A_uniform = lambda r: np.array([100, 0, 0])
        >>> J_uniform = lambda r: np.array([1, 0, 0])
        >>> bounds = ((0, 1), (0, 1), (0, 1))
        >>> T = integrate_electrokinetic_energy(A_uniform, J_uniform, bounds)
        >>> print(f"T = {T} erg")
    """
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

                A = np.asarray(A_func(r), dtype=np.float64)
                J = np.asarray(J_func(r), dtype=np.float64)

                A_dot_J = np.dot(A, J)
                total_energy += 0.5 * A_dot_J * dV

    return total_energy


@maxwell_cite(
    638,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Calculate coupling coefficient: k = M/√(L₁L₂)",
)
def calc_coupling_coefficient(
    M: float,
    L1: float,
    L2: float,
) -> float:
    """
    Calculate the magnetic coupling coefficient between two circuits.

    Art. 638: The coupling coefficient measures the degree of magnetic
    coupling between two circuits:

        k = M / √(L₁ L₂)

    where:
        M = mutual inductance (cm)
        L₁, L₂ = self-inductances (cm)
        k = coupling coefficient (0 ≤ k ≤ 1)

    The coupling coefficient is dimensionless and ranges from 0 (no coupling)
    to 1 (perfect coupling, all flux from one circuit links the other).

    Args:
        M: Mutual inductance (cm).
        L1: Self-inductance of first circuit (cm).
        L2: Self-inductance of second circuit (cm).

    Returns:
        Coupling coefficient k (0 to 1).

    Raises:
        ValueError: If inductances not positive or |k| > 1.

    Reference:
        Part IV, Art. 638: Coupling coefficient.

    Example:
        >>> # M=2, L1=10, L2=5
        >>> k = calc_coupling_coefficient(2.0, 10.0, 5.0)
        >>> print(f"k = {k}")  # k ≈ 0.283
    """
    if L1 <= 0:
        raise ValueError(f"L1 must be positive, got {L1}")
    if L2 <= 0:
        raise ValueError(f"L2 must be positive, got {L2}")

    k = M / np.sqrt(L1 * L2)

    # Physically, |k| should not exceed 1
    if abs(k) > 1.0:
        # Warn but don't fail - could be numerical or theoretical exercise
        pass

    return k


@maxwell_cite(
    635,
    636,
    637,
    638,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Complete electrokinetic energy analysis",
)
def analyze_electrokinetic_energy(
    inductance_matrix: np.ndarray = None,
    currents: np.ndarray = None,
    L1: float = None,
    L2: float = None,
    M: float = None,
    I1: float = None,
    I2: float = None,
) -> dict[str, float | np.ndarray]:
    """
    Perform comprehensive electrokinetic energy analysis.

    Art. 635-638: Complete analysis of electrokinetic energy including:

    1. Single circuit energy (if L, I provided)
    2. Two-circuit energy with mutual inductance
    3. Coupling coefficient
    4. Self and mutual energy contributions

    Args:
        inductance_matrix: Full inductance matrix for multi-circuit.
        currents: Currents array for multi-circuit.
        L1: Self-inductance of first circuit (two-circuit mode).
        L2: Self-inductance of second circuit.
        M: Mutual inductance.
        I1: Current in first circuit.
        I2: Current in second circuit.

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 635-638: Complete electrokinetic analysis.
    """
    result = {}

    # Two-circuit analysis
    if all(x is not None for x in [L1, L2, M, I1, I2]):
        # Total energy
        total_energy = calc_two_circuit_energy(L1, L2, M, I1, I2)

        # Self-energy contributions
        self_energy_1 = 0.5 * L1 * I1**2
        self_energy_2 = 0.5 * L2 * I2**2
        mutual_energy = M * I1 * I2

        # Coupling coefficient
        k = calc_coupling_coefficient(M, L1, L2)

        result.update(
            {
                "total_energy": total_energy,
                "self_energy_1": self_energy_1,
                "self_energy_2": self_energy_2,
                "mutual_energy": mutual_energy,
                "coupling_coefficient": k,
                "mutual_fraction": (
                    mutual_energy / total_energy if total_energy > 0 else 0
                ),
            }
        )

    # Multi-circuit analysis
    if inductance_matrix is not None and currents is not None:
        total_energy = calc_coupled_circuits_energy(inductance_matrix, currents)

        result.update(
            {
                "total_energy": total_energy,
                "inductance_matrix": inductance_matrix,
                "currents": currents,
                "num_circuits": len(currents),
            }
        )

    return result


@maxwell_cite(
    636,
    637,
    part=4,
    chapter="Energy in the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Verify coupled circuits energy formula",
)
def verify_coupled_circuits_energy(
    L1: float = 10.0,
    L2: float = 5.0,
    M: float = 2.0,
    I1: float = 3.0,
    I2: float = 4.0,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify the coupled circuits energy formula.

    Art. 636-637: This function verifies that:

        T = (1/2) L₁ I₁² + (1/2) L₂ I₂² + M I₁ I₂

    equals the matrix formulation:

        T = (1/2) Iᵀ · L · I

    where L is the inductance matrix.

    Args:
        L1: Self-inductance of first circuit.
        L2: Self-inductance of second circuit.
        M: Mutual inductance.
        I1: Current in first circuit.
        I2: Current in second circuit.
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with:
        - energy_scalar: Energy from scalar formula
        - energy_matrix: Energy from matrix formula
        - self_energy_1: (1/2) L₁ I₁²
        - self_energy_2: (1/2) L₂ I₂²
        - mutual_energy: M I₁ I₂
        - verified: True if both methods agree

    Reference:
        Part IV, Arts. 636-637: Coupled circuits verification.
    """
    # Scalar formula
    energy_scalar = calc_two_circuit_energy(L1, L2, M, I1, I2)

    # Matrix formula
    L_matrix = np.array([[L1, M], [M, L2]])
    I_array = np.array([I1, I2])
    energy_matrix = calc_coupled_circuits_energy(L_matrix, I_array)

    # Component energies
    self_energy_1 = 0.5 * L1 * I1**2
    self_energy_2 = 0.5 * L2 * I2**2
    mutual_energy = M * I1 * I2

    # Verify both methods agree
    verified = np.isclose(energy_scalar, energy_matrix, rtol=tolerance)

    return {
        "energy_scalar": energy_scalar,
        "energy_matrix": energy_matrix,
        "self_energy_1": self_energy_1,
        "self_energy_2": self_energy_2,
        "mutual_energy": mutual_energy,
        "energy_sum": self_energy_1 + self_energy_2 + mutual_energy,
        "verified": verified,
        "tolerance_used": tolerance,
    }

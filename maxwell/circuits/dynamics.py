"""
Circuit Dynamics and Mutual Induction — how circuits interact through electromagnetic fields.

Implements Maxwell's theory of circuit dynamics, self and mutual induction
as described in Articles 578-584 of the Treatise:

- Self-inductance and magnetic energy: T = (1/2) L I² (Arts. 578-580)
- Induced EMF from self-induction: E_induced = -L dI/dt (Art. 579)
- Self-inductance of solenoid: L = 4πn²A/l (Art. 580)
- Mutual inductance energy: T = (1/2)L₁I₁² + (1/2)L₂I₂² + M·I₁·I₂ (Arts. 581-582)
- Mutual induction EMF: EMF₁ = -M·dI₂/dt, EMF₂ = -M·dI₁/dt (Art. 583)
- Coupling coefficient: k = M/√(L₁L₂), 0 ≤ k ≤ 1 (Art. 584)
- Force between circuits: F = I₁I₂ ∂M/∂x (Art. 584)
- Torque between circuits: τ = I₁I₂ ∂M/∂θ (Art. 584)

Maxwell's CGS-EMU formulation:
    Self-inductance energy: T = (1/2) L I²
    Mutual inductance energy: T_mutual = M I₁ I₂
    Total energy: T = (1/2) L₁ I₁² + (1/2) L₂ I₂² + M I₁ I₂
    Induced EMF: E = -L dI/dt (self), E = -M dI/dt (mutual)
    Force: F = I₁I₂ ∂M/∂x
    Torque: τ = I₁I₂ ∂M/∂θ

where:
    L = self-inductance (cm in CGS)
    M = mutual inductance (cm in CGS)
    I = current (abamperes)
    T = energy (ergs)
    E = EMF (abvolts)
    F = force (dynes)
    τ = torque (dyne·cm)

Category: A (maxwell_original) — Maxwell's theory of circuit dynamics and mutual induction.

References:
    Part IV, Arts. 578-584: Circuit dynamics and mutual induction.
    Part IV, Ch. V-VI: Self and mutual inductance, electromagnetic forces.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class Circuit:
    """
    A single electrical circuit with self-inductance and resistance.

    Arts. 578-580: A circuit carrying current possesses self-inductance,
    which determines the magnetic energy stored and the induced EMF when
    current changes.

    Properties:
        Self-inductance L depends only on circuit geometry (Art. 580)
        For a solenoid: L = 4πn²A/l where n = turns, A = area, l = length
        Magnetic energy: T = (1/2) L I²
        Time constant: τ = L/R

    Attributes:
        self_inductance: Self-inductance L (cm in CGS).
        resistance: Resistance R (cm/s in CGS).
        current: Current I (abamperes).
    """

    self_inductance: float
    resistance: float
    current: float = 0.0

    def __post_init__(self):
        """Validate parameters."""
        if self.self_inductance < 0:
            raise ValueError(f"Self-inductance must be non-negative, got {self.self_inductance}")
        if self.resistance < 0:
            raise ValueError(f"Resistance must be non-negative, got {self.resistance}")

    @classmethod
    @maxwell_cite(
        578, 579, 580,
        part=4, chapter="Circuit Dynamics and Mutual Induction",
        theory_class="maxwell_original",
        description="Create circuit from self-inductance and resistance",
    )
    def from_inductance_and_resistance(
        cls,
        self_inductance: float,
        resistance: float,
        initial_current: float = 0.0,
    ) -> Circuit:
        """
        Create a circuit from its inductance and resistance.

        Arts. 578-580: A circuit is characterized by its self-inductance L
        (a geometric property) and resistance R (a material property).

        Args:
            self_inductance: Self-inductance L (cm in CGS).
            resistance: Resistance R (cm/s in CGS).
            initial_current: Initial current I (abamperes, default 0).

        Returns:
            Circuit object.

        Reference:
            Part IV, Arts. 578-580: Circuit parameters and properties.
        """
        return cls(
            self_inductance=self_inductance,
            resistance=resistance,
            current=initial_current,
        )

    @maxwell_cite(
        578,
        part=4, chapter="Circuit Dynamics and Mutual Induction",
        theory_class="maxwell_original",
        description="Calculate magnetic energy stored in circuit",
    )
    def energy(self) -> float:
        """
        Calculate magnetic energy stored in the circuit.

        Art. 578: The magnetic energy of a circuit carrying current I
        with self-inductance L is:

            T = (1/2) L I²  (erg)

        Returns:
            Magnetic energy T (erg).

        Reference:
            Part IV, Art. 578: Magnetic energy of a circuit.

        Example:
            >>> circuit = Circuit(self_inductance=10.0, resistance=1.0, current=5.0)
            >>> energy = circuit.energy()
            >>> print(f"T = {energy} erg")  # T = 125.0 erg
        """
        return 0.5 * self.self_inductance * self.current ** 2

    @maxwell_cite(
        579,
        part=4, chapter="Circuit Dynamics and Mutual Induction",
        theory_class="maxwell_original",
        description="Calculate induced EMF from changing current",
    )
    def induced_emf(self, dI_dt: float) -> float:
        """
        Calculate EMF induced by changing current (self-induction).

        Art. 579: When the current in a circuit changes, the self-inductance
        produces an opposing EMF (Lenz's law):

            E_induced = -L · dI/dt  (abvolts)

        where:
            L = self-inductance (cm)
            dI_dt = rate of current change (abamperes/s)

        Args:
            dI_dt: Rate of current change dI/dt (abamperes/s).
                   Positive = increasing current, negative = decreasing.

        Returns:
            Induced EMF (abvolts). Negative sign indicates opposition to change.

        Reference:
            Part IV, Art. 579: Self-induction EMF.

        Example:
            >>> circuit = Circuit(self_inductance=1000.0, resistance=1.0, current=5.0)
            >>> emf = circuit.induced_emf(10.0)  # Current increasing at 10 A/s
            >>> print(f"EMF = {emf} abvolts")  # EMF = -10000.0 abvolts
        """
        return -self.self_inductance * dI_dt

    @maxwell_cite(
        578, 579,
        part=4, chapter="Circuit Dynamics and Mutual Induction",
        theory_class="maxwell_original",
        description="Calculate circuit time constant τ = L/R",
    )
    def time_constant(self) -> float:
        """
        Calculate the circuit time constant.

        Arts. 578-579: The time constant τ = L/R characterizes the rate
        at which current builds up or decays in an RL circuit:

            I(t) = I₀(1 - e^(-t/τ))  (rising)
            I(t) = I₀ e^(-t/τ)        (decaying)

        In CGS:
            L in cm
            R in cm/s
            τ in seconds

        Returns:
            Time constant τ (seconds). Returns 0 if R = 0.

        Reference:
            Part IV, Arts. 578-579: RL circuit dynamics.

        Example:
            >>> circuit = Circuit(self_inductance=10.0, resistance=2.0)
            >>> tau = circuit.time_constant()
            >>> print(f"τ = {tau} s")  # τ = 5.0 s
        """
        if self.resistance == 0:
            return float('inf')  # Pure inductance, current never decays
        return self.self_inductance / self.resistance


@dataclass
class CoupledCircuits:
    """
    Two magnetically coupled circuits with mutual inductance.

    Arts. 581-584: When two circuits are magnetically coupled, the total
    electrokinetic energy includes both self-inductance and mutual inductance
    terms. The mutual inductance M depends on the geometry and relative
    position of the circuits.

    Total energy:
        T = (1/2) L₁ I₁² + (1/2) L₂ I₂² + M I₁ I₂

    Mutual induction:
        EMF₁ = -M · dI₂/dt  (EMF induced in circuit 1 by circuit 2)
        EMF₂ = -M · dI₁/dt  (EMF induced in circuit 2 by circuit 1)

    Coupling coefficient:
        k = M / √(L₁ L₂), where 0 ≤ k ≤ 1

    Attributes:
        circuit1: First circuit object.
        circuit2: Second circuit object.
        mutual_inductance: Mutual inductance M (cm in CGS).
    """

    circuit1: Circuit
    circuit2: Circuit
    mutual_inductance: float

    def __post_init__(self):
        """Validate parameters."""
        # Check physical constraint on mutual inductance
        L1 = self.circuit1.self_inductance
        L2 = self.circuit2.self_inductance
        M_max = np.sqrt(L1 * L2)

        if abs(self.mutual_inductance) > M_max * (1 + 1e-10):
            # Allow small numerical tolerance
            raise ValueError(
                f"|M| cannot exceed √(L₁L₂) = {M_max:.6f} cm, got |M| = {abs(self.mutual_inductance):.6f} cm"
            )

    @classmethod
    @maxwell_cite(
        581, 582,
        part=4, chapter="Circuit Dynamics and Mutual Induction",
        theory_class="maxwell_original",
        description="Create coupled circuits from two circuits and mutual inductance",
    )
    def from_circuits_and_mutual_inductance(
        cls,
        circuit1: Circuit,
        circuit2: Circuit,
        mutual_inductance: float,
    ) -> CoupledCircuits:
        """
        Create a coupled circuit system from two circuits and their mutual inductance.

        Arts. 581-582: Two circuits are magnetically coupled when the magnetic
        field of one links with the other, characterized by mutual inductance M.

        Args:
            circuit1: First circuit.
            circuit2: Second circuit.
            mutual_inductance: Mutual inductance M (cm).

        Returns:
            CoupledCircuits object.

        Reference:
            Part IV, Arts. 581-582: Coupled circuit systems.
        """
        return cls(
            circuit1=circuit1,
            circuit2=circuit2,
            mutual_inductance=mutual_inductance,
        )

    @property
    def coupling_coefficient(self) -> float:
        """
        Calculate the coupling coefficient k.

        Art. 584: The coupling coefficient measures the degree of magnetic
        coupling between circuits:

            k = M / √(L₁ L₂)

        where:
            0 ≤ |k| ≤ 1 (perfect coupling when |k| = 1)
            k > 0 for aiding coupling, k < 0 for opposing

        Returns:
            Coupling coefficient k (-1 to 1).

        Reference:
            Part IV, Art. 584: Coupling coefficient.

        Example:
            >>> c1 = Circuit(self_inductance=10.0, resistance=1.0, current=5.0)
            >>> c2 = Circuit(self_inductance=5.0, resistance=1.0, current=3.0)
            >>> coupled = CoupledCircuits(c1, c2, mutual_inductance=2.0)
            >>> k = coupled.coupling_coefficient
            >>> print(f"k = {k:.4f}")  # k ≈ 0.2828
        """
        L1 = self.circuit1.self_inductance
        L2 = self.circuit2.self_inductance

        if L1 <= 0 or L2 <= 0:
            return 0.0

        return self.mutual_inductance / np.sqrt(L1 * L2)

    @maxwell_cite(
        581, 582,
        part=4, chapter="Circuit Dynamics and Mutual Induction",
        theory_class="maxwell_original",
        description="Calculate total energy of coupled circuits",
    )
    def total_energy(self) -> float:
        """
        Calculate total electrokinetic energy of coupled circuits.

        Arts. 581-582: The total energy includes self-inductance energy
        of each circuit plus the mutual inductance energy:

            T = (1/2) L₁ I₁² + (1/2) L₂ I₂² + M I₁ I₂  (erg)

        The mutual term M I₁ I₂ represents the magnetic coupling energy.
        Its sign depends on the relative orientation of the circuits.

        Returns:
            Total electrokinetic energy T (erg).

        Reference:
            Part IV, Arts. 581-582: Energy of coupled circuits.

        Example:
            >>> c1 = Circuit(self_inductance=10.0, resistance=1.0, current=5.0)
            >>> c2 = Circuit(self_inductance=5.0, resistance=1.0, current=3.0)
            >>> coupled = CoupledCircuits(c1, c2, mutual_inductance=2.0)
            >>> T = coupled.total_energy()
            >>> print(f"T = {T} erg")
        """
        L1 = self.circuit1.self_inductance
        L2 = self.circuit2.self_inductance
        I1 = self.circuit1.current
        I2 = self.circuit2.current
        M = self.mutual_inductance

        # T = (1/2) L₁ I₁² + (1/2) L₂ I₂² + M I₁ I₂
        return 0.5 * L1 * I1 ** 2 + 0.5 * L2 * I2 ** 2 + M * I1 * I2

    @maxwell_cite(
        583,
        part=4, chapter="Circuit Dynamics and Mutual Induction",
        theory_class="maxwell_original",
        description="Calculate EMF induced in circuit 1 by circuit 2",
    )
    def emf_on_1(self, dI2_dt: float) -> float:
        """
        Calculate EMF induced in circuit 1 by changing current in circuit 2.

        Art. 583: Mutual induction — when current in circuit 2 changes,
        it induces an EMF in circuit 1:

            EMF₁ = -M · dI₂/dt  (abvolts)

        The negative sign (Lenz's law) indicates the induced EMF opposes
        the change in current.

        Args:
            dI2_dt: Rate of change of current in circuit 2 (abamperes/s).

        Returns:
            Induced EMF in circuit 1 (abvolts).

        Reference:
            Part IV, Art. 583: Mutual induction EMF.

        Example:
            >>> c1 = Circuit(self_inductance=10.0, resistance=1.0, current=5.0)
            >>> c2 = Circuit(self_inductance=5.0, resistance=1.0, current=3.0)
            >>> coupled = CoupledCircuits(c1, c2, mutual_inductance=2.0)
            >>> emf = coupled.emf_on_1(10.0)  # I2 increasing at 10 A/s
            >>> print(f"EMF₁ = {emf} abvolts")  # EMF₁ = -20.0 abvolts
        """
        return -self.mutual_inductance * dI2_dt

    @maxwell_cite(
        583,
        part=4, chapter="Circuit Dynamics and Mutual Induction",
        theory_class="maxwell_original",
        description="Calculate EMF induced in circuit 2 by circuit 1",
    )
    def emf_on_2(self, dI1_dt: float) -> float:
        """
        Calculate EMF induced in circuit 2 by changing current in circuit 1.

        Art. 583: Mutual induction is symmetric — when current in circuit 1
        changes, it induces an EMF in circuit 2:

            EMF₂ = -M · dI₁/dt  (abvolts)

        The mutual inductance M is the same in both directions: M₁₂ = M₂₁.

        Args:
            dI1_dt: Rate of change of current in circuit 1 (abamperes/s).

        Returns:
            Induced EMF in circuit 2 (abvolts).

        Reference:
            Part IV, Art. 583: Mutual induction symmetry.

        Example:
            >>> c1 = Circuit(self_inductance=10.0, resistance=1.0, current=5.0)
            >>> c2 = Circuit(self_inductance=5.0, resistance=1.0, current=3.0)
            >>> coupled = CoupledCircuits(c1, c2, mutual_inductance=2.0)
            >>> emf = coupled.emf_on_2(10.0)  # I1 increasing at 10 A/s
            >>> print(f"EMF₂ = {emf} abvolts")  # EMF₂ = -20.0 abvolts
        """
        return -self.mutual_inductance * dI1_dt


@maxwell_cite(
    580,
    part=4, chapter="Circuit Dynamics and Mutual Induction",
    theory_class="maxwell_original",
    description="Calculate self-inductance of a solenoid: L = 4πn²A/l",
)
def calc_solenoid_inductance(
    turns: int,
    area: float,
    length: float,
) -> float:
    """
    Calculate self-inductance of a long solenoid.

    Art. 580: For a long solenoid (length >> radius) with uniform winding,
    the self-inductance is:

        L = 4π n² A / l  (cm in CGS)

    where:
        n = total number of turns
        A = cross-sectional area (cm²)
        l = length of solenoid (cm)

    This formula assumes the solenoid is sufficiently long that end effects
    are negligible and the field is uniform inside.

    Args:
        turns: Total number of turns N (dimensionless).
        area: Cross-sectional area A (cm²).
        length: Length of solenoid l (cm).

    Returns:
        Self-inductance L (cm in CGS).

    Raises:
        ValueError: If area or length is not positive, or turns is not positive.

    Reference:
        Part IV, Art. 580: Self-inductance of solenoid.

    Example:
        >>> # Solenoid with 100 turns, 1 cm² area, 10 cm length
        >>> L = calc_solenoid_inductance(100, 1.0, 10.0)
        >>> print(f"L = {L:.2f} cm")  # L ≈ 12566.37 cm
    """
    if turns <= 0:
        raise ValueError(f"Number of turns must be positive, got {turns}")
    if area <= 0:
        raise ValueError(f"Area must be positive, got {area}")
    if length <= 0:
        raise ValueError(f"Length must be positive, got {length}")

    # n = turns per unit length = N/l
    # L = 4π n² A l = 4π (N/l)² A l = 4π N² A / l
    return 4.0 * np.pi * (turns ** 2) * area / length


@maxwell_cite(
    578, 579, 580,
    part=4, chapter="Circuit Dynamics and Mutual Induction",
    theory_class="maxwell_original",
    description="Calculate self-inductance from geometry parameters",
)
def calc_self_inductance(
    geometry_type: str,
    **kwargs: float,
) -> float:
    """
    Calculate self-inductance from circuit geometry.

    Arts. 578-580: Self-inductance is a purely geometric property of a circuit.
    This function provides calculations for common circuit geometries.

    Supported geometries:
    - "solenoid": L = 4πn²A/l (requires: turns, area, length)
    - "toroid": L = 2πn²h·ln(b/a) (requires: turns, height, inner_radius, outer_radius)
    - "circular_loop": L ≈ μ₀R[ln(8R/a) - 2] (requires: radius, wire_radius)

    Args:
        geometry_type: Type of circuit geometry ("solenoid", "toroid", "circular_loop").
        **kwargs: Geometry-specific parameters.

    Returns:
        Self-inductance L (cm in CGS).

    Raises:
        ValueError: If geometry_type is unknown or required parameters missing.

    Reference:
        Part IV, Arts. 578-580: Self-inductance from geometry.

    Example:
        >>> # Solenoid inductance
        >>> L = calc_self_inductance("solenoid", turns=100, area=1.0, length=10.0)
        >>> print(f"L = {L:.2f} cm")
    """
    geometry_type = geometry_type.lower()

    if geometry_type == "solenoid":
        required = ["turns", "area", "length"]
        if not all(k in kwargs for k in required):
            raise ValueError(f"Solenoid requires parameters: {required}")
        return calc_solenoid_inductance(
            turns=int(kwargs["turns"]),
            area=kwargs["area"],
            length=kwargs["length"],
        )

    elif geometry_type == "toroid":
        # L = 2πn²h·ln(b/a) for rectangular cross-section toroid
        required = ["turns", "height", "inner_radius", "outer_radius"]
        if not all(k in kwargs for k in required):
            raise ValueError(f"Toroid requires parameters: {required}")

        n = kwargs["turns"]
        h = kwargs["height"]
        a = kwargs["inner_radius"]
        b = kwargs["outer_radius"]

        if a <= 0 or b <= 0 or h <= 0:
            raise ValueError("Radii and height must be positive")
        if a >= b:
            raise ValueError("Inner radius must be less than outer radius")

        return 2.0 * np.pi * (n ** 2) * h * np.log(b / a)

    elif geometry_type == "circular_loop":
        # Approximate formula for circular loop of wire
        # L ≈ R[ln(8R/a) - 2] where R = loop radius, a = wire radius
        required = ["radius", "wire_radius"]
        if not all(k in kwargs for k in required):
            raise ValueError(f"Circular loop requires parameters: {required}")

        R = kwargs["radius"]
        a = kwargs["wire_radius"]

        if R <= 0 or a <= 0:
            raise ValueError("Radii must be positive")
        if a >= R:
            raise ValueError("Wire radius must be less than loop radius")

        return R * (np.log(8.0 * R / a) - 2.0)

    else:
        raise ValueError(f"Unknown geometry type: {geometry_type}")


@maxwell_cite(
    581, 582,
    part=4, chapter="Circuit Dynamics and Mutual Induction",
    theory_class="maxwell_original",
    description="Calculate mutual inductance between two circuits",
)
def calc_mutual_inductance(
    circuit1_type: str,
    circuit2_type: str,
    separation: float,
    **kwargs: float,
) -> float:
    """
    Calculate mutual inductance between two circuits.

    Arts. 581-582: Mutual inductance depends on the geometry of both circuits
    and their relative position. This function provides calculations for
    common circuit configurations.

    Supported configurations:
    - "coaxial_loops": Two coaxial circular loops (requires: r1, r2, separation)
    - "parallel_wires": Two parallel wires of length l (requires: length, wire_spacing)
    - "solenoid_coils": Two coaxial solenoids (requires: n1, n2, area, length)

    Args:
        circuit1_type: Type of first circuit.
        circuit2_type: Type of second circuit.
        separation: Distance between circuits (cm).
        **kwargs: Geometry-specific parameters.

    Returns:
        Mutual inductance M (cm in CGS).

    Raises:
        ValueError: If configuration is unsupported or parameters missing.

    Reference:
        Part IV, Arts. 581-582: Mutual inductance calculation.

    Example:
        >>> # Two coaxial solenoids
        >>> M = calc_mutual_inductance(
        ...     "solenoid_coils", "solenoid_coils",
        ...     separation=0.0,  # Perfectly coupled
        ...     n1=100, n2=50, area=1.0, length=10.0
        ... )
    """
    circuit1_type = circuit1_type.lower()
    circuit2_type = circuit2_type.lower()

    if circuit1_type == "solenoid_coils" and circuit2_type == "solenoid_coils":
        # Two coaxial solenoids sharing the same axis
        # M = 4π n1 n2 A / l (for perfect coupling, k = 1)
        # With coupling factor that decreases with separation
        required = ["n1", "n2", "area", "length"]
        if not all(k in kwargs for k in required):
            raise ValueError(f"Coaxial solenoids require: {required}")

        n1 = kwargs["n1"]
        n2 = kwargs["n2"]
        A = kwargs["area"]
        l = kwargs["length"]
        d = separation

        if l <= 0 or A <= 0:
            raise ValueError("Length and area must be positive")

        # Base mutual inductance (perfect coupling)
        M_base = 4.0 * np.pi * n1 * n2 * A / l

        # Coupling decreases with separation (simplified model)
        # k ≈ l / sqrt(l² + d²) for coaxial solenoids
        if d > 0:
            coupling = l / np.sqrt(l ** 2 + d ** 2)
        else:
            coupling = 1.0

        return M_base * coupling

    elif circuit1_type == "coaxial_loops" and circuit2_type == "coaxial_loops":
        # Two coaxial circular loops
        # Approximate formula using elliptic integrals simplified
        required = ["r1", "r2"]
        if not all(k in required for k in ["r1", "r2"]):
            raise ValueError("Coaxial loops require: r1, r2, separation")

        r1 = kwargs["r1"]
        r2 = kwargs["r2"]
        d = separation

        if r1 <= 0 or r2 <= 0:
            raise ValueError("Radii must be positive")

        # Simplified formula for mutual inductance of coaxial loops
        # M ≈ (2π/c²) * (r1² r2²) / (r1² + r2² + d²)^(3/2)
        # In CGS, this becomes (simplified):
        denom = (r1 ** 2 + r2 ** 2 + d ** 2) ** 1.5
        if denom == 0:
            return float('inf')  # Loops coincident

        return 2.0 * np.pi * (r1 ** 2) * (r2 ** 2) / denom

    elif circuit1_type == "parallel_wires" and circuit2_type == "parallel_wires":
        # Two parallel wires (mutual inductance per unit length)
        # M = 2l [ln(2l/d) - 1] for length l, spacing d
        required = ["length", "wire_spacing"]
        if not all(k in kwargs for k in required):
            raise ValueError("Parallel wires require: length, wire_spacing")

        l = kwargs["length"]
        d = kwargs["wire_spacing"]

        if l <= 0 or d <= 0:
            raise ValueError("Length and spacing must be positive")

        return 2.0 * l * (np.log(2.0 * l / d) - 1.0)

    else:
        raise ValueError(
            f"Unsupported configuration: {circuit1_type} and {circuit2_type}"
        )


@maxwell_cite(
    584,
    part=4, chapter="Circuit Dynamics and Mutual Induction",
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

    Art. 584: The coupling coefficient measures the degree of magnetic
    coupling between two circuits:

        k = M / √(L₁ L₂)

    where:
        M = mutual inductance (cm)
        L₁, L₂ = self-inductances (cm)
        k = coupling coefficient

    Properties:
        0 ≤ |k| ≤ 1 (physically realizable coupling)
        k = 0: No coupling (circuits far apart or orthogonal)
        |k| = 1: Perfect coupling (all flux from one links the other)
        k > 0: Aiding coupling (fluxes reinforce)
        k < 0: Opposing coupling (fluxes oppose)

    Args:
        M: Mutual inductance (cm).
        L1: Self-inductance of first circuit (cm).
        L2: Self-inductance of second circuit (cm).

    Returns:
        Coupling coefficient k (-1 to 1).

    Raises:
        ValueError: If L1 or L2 is not positive.

    Reference:
        Part IV, Art. 584: Coupling coefficient.

    Example:
        >>> k = calc_coupling_coefficient(M=2.0, L1=10.0, L2=5.0)
        >>> print(f"k = {k:.4f}")  # k ≈ 0.2828
    """
    if L1 <= 0:
        raise ValueError(f"L1 must be positive, got {L1}")
    if L2 <= 0:
        raise ValueError(f"L2 must be positive, got {L2}")

    return M / np.sqrt(L1 * L2)


@maxwell_cite(
    583,
    part=4, chapter="Circuit Dynamics and Mutual Induction",
    theory_class="maxwell_original",
    description="Calculate EMF from mutual inductance: EMF = -M·dI/dt",
)
def calc_emf_from_mutual_inductance(
    M: float,
    dI_dt: float,
) -> float:
    """
    Calculate EMF induced by mutual inductance.

    Art. 583: When current in one circuit changes, it induces an EMF
    in a nearby circuit through mutual induction:

        EMF = -M · dI/dt  (abvolts)

    where:
        M = mutual inductance (cm)
        dI_dt = rate of current change in the source circuit (abamperes/s)

    The negative sign (Lenz's law) indicates the induced EMF opposes
    the change in flux.

    Args:
        M: Mutual inductance (cm).
        dI_dt: Rate of current change dI/dt (abamperes/s).

    Returns:
        Induced EMF (abvolts).

    Raises:
        ValueError: If M is negative.

    Reference:
        Part IV, Art. 583: Mutual induction EMF.

    Example:
        >>> emf = calc_emf_from_mutual_inductance(M=2.0, dI_dt=10.0)
        >>> print(f"EMF = {emf} abvolts")  # EMF = -20.0 abvolts
    """
    if M < 0:
        raise ValueError(f"Mutual inductance must be non-negative, got {M}")

    return -M * dI_dt


@maxwell_cite(
    584,
    part=4, chapter="Circuit Dynamics and Mutual Induction",
    theory_class="maxwell_original",
    description="Calculate force between circuits: F = I₁I₂ ∂M/∂x",
)
def calc_force_between_circuits(
    I1: float,
    I2: float,
    dM_dx: float,
) -> float:
    """
    Calculate force between two current-carrying circuits.

    Art. 584: When two circuits carry currents and their mutual inductance
    varies with position, a mechanical force acts between them:

        F = I₁ I₂ (∂M/∂x)  (dynes)

    where:
        I₁, I₂ = currents in the circuits (abamperes)
        ∂M/∂x = rate of change of mutual inductance with position (cm)

    The force direction is such that it increases the mutual inductance
    (circuits tend to move toward maximum coupling).

    Args:
        I1: Current in first circuit (abamperes).
        I2: Current in second circuit (abamperes).
        dM_dx: Gradient of mutual inductance with respect to position (cm).

    Returns:
        Force F (dynes). Positive = attractive (increasing M).

    Reference:
        Part IV, Art. 584: Force between circuits.

    Example:
        >>> # Two circuits with 5A and 3A, dM/dx = 0.1 cm/cm
        >>> F = calc_force_between_circuits(5.0, 3.0, 0.1)
        >>> print(f"F = {F} dynes")  # F = 1.5 dynes
    """
    return I1 * I2 * dM_dx


@maxwell_cite(
    584,
    part=4, chapter="Circuit Dynamics and Mutual Induction",
    theory_class="maxwell_original",
    description="Calculate torque between circuits: τ = I₁I₂ ∂M/∂θ",
)
def calc_torque_between_circuits(
    I1: float,
    I2: float,
    dM_dtheta: float,
) -> float:
    """
    Calculate torque between two current-carrying circuits.

    Art. 584: When two circuits can rotate relative to each other,
    the variation of mutual inductance with angle produces a torque:

        τ = I₁ I₂ (∂M/∂θ)  (dyne·cm)

    where:
        I₁, I₂ = currents in the circuits (abamperes)
        ∂M/∂θ = rate of change of mutual inductance with angle (cm/radian)

    The torque acts to rotate the circuits toward maximum coupling
    (parallel alignment for positive M).

    Args:
        I1: Current in first circuit (abamperes).
        I2: Current in second circuit (abamperes).
        dM_dtheta: Gradient of mutual inductance with respect to angle (cm/rad).

    Returns:
        Torque τ (dyne·cm). Positive = toward increasing M.

    Reference:
        Part IV, Art. 584: Torque between circuits.

    Example:
        >>> # Two coils at angle, dM/dθ = -0.5 cm/rad at current orientation
        >>> tau = calc_torque_between_circuits(5.0, 3.0, -0.5)
        >>> print(f"τ = {tau} dyne·cm")  # τ = -7.5 dyne·cm
    """
    return I1 * I2 * dM_dtheta


@maxwell_cite(
    578, 579, 580, 581, 582, 583, 584,
    part=4, chapter="Circuit Dynamics and Mutual Induction",
    theory_class="maxwell_original",
    description="Complete analysis of circuit system with mutual inductances",
)
def analyze_circuit_system(
    circuits: list[Circuit],
    mutual_inductances: dict[tuple[int, int], float],
) -> dict[str, float | list[float] | np.ndarray]:
    """
    Perform comprehensive analysis of a system of coupled circuits.

    Arts. 578-584: Complete analysis of multiple coupled circuits including:
    - Individual circuit energies
    - Mutual inductance energies
    - Total system energy
    - Coupling coefficients
    - Inductance matrix

    For N circuits:
        T_total = (1/2) Σᵢ Lᵢᵢ Iᵢ² + Σᵢ<ⱼ Mᵢⱼ Iᵢ Iⱼ

    Args:
        circuits: List of Circuit objects.
        mutual_inductances: Dict mapping (i,j) circuit pairs to mutual inductance M_ij.

    Returns:
        Dictionary with:
        - total_energy: Total electrokinetic energy (erg)
        - self_energies: List of individual circuit energies (erg)
        - mutual_energies: Dict of mutual energy contributions (erg)
        - coupling_coefficients: Dict of k values for each pair
        - inductance_matrix: Full L_ij matrix (cm)
        - current_vector: Array of currents (abamperes)
        - num_circuits: Number of circuits

    Reference:
        Part IV, Arts. 578-584: Complete circuit system analysis.

    Example:
        >>> c1 = Circuit(self_inductance=10.0, resistance=1.0, current=5.0)
        >>> c2 = Circuit(self_inductance=5.0, resistance=1.0, current=3.0)
        >>> M = {(0, 1): 2.0}  # Mutual inductance between c1 and c2
        >>> result = analyze_circuit_system([c1, c2], M)
        >>> print(f"Total energy: {result['total_energy']} erg")
    """
    n = len(circuits)
    if n == 0:
        return {
            "total_energy": 0.0,
            "self_energies": [],
            "mutual_energies": {},
            "coupling_coefficients": {},
            "inductance_matrix": np.array([]),
            "current_vector": np.array([]),
            "num_circuits": 0,
        }

    # Build inductance matrix
    L_matrix = np.zeros((n, n))
    for i, circuit in enumerate(circuits):
        L_matrix[i, i] = circuit.self_inductance

    # Fill mutual inductances (symmetric matrix)
    for (i, j), M in mutual_inductances.items():
        if 0 <= i < n and 0 <= j < n:
            L_matrix[i, j] = M
            L_matrix[j, i] = M  # Symmetry: M_ij = M_ji

    # Current vector
    I_vector = np.array([c.current for c in circuits])

    # Calculate energies
    # Self energies: T_i = (1/2) L_i I_i²
    self_energies = [0.5 * c.self_inductance * c.current ** 2 for c in circuits]

    # Mutual energies: T_ij = M_ij I_i I_j
    mutual_energies = {}
    for (i, j), M in mutual_inductances.items():
        if 0 <= i < n and 0 <= j < n:
            mutual_energies[(i, j)] = M * circuits[i].current * circuits[j].current

    # Total energy: T = Σ T_self + Σ T_mutual
    total_energy = sum(self_energies) + sum(mutual_energies.values())

    # Coupling coefficients
    coupling_coefficients = {}
    for (i, j), M in mutual_inductances.items():
        if 0 <= i < n and 0 <= j < n:
            L_i = circuits[i].self_inductance
            L_j = circuits[j].self_inductance
            if L_i > 0 and L_j > 0:
                coupling_coefficients[(i, j)] = M / np.sqrt(L_i * L_j)

    return {
        "total_energy": total_energy,
        "self_energies": self_energies,
        "mutual_energies": mutual_energies,
        "coupling_coefficients": coupling_coefficients,
        "inductance_matrix": L_matrix,
        "current_vector": I_vector,
        "num_circuits": n,
    }


@maxwell_cite(
    578, 581, 582,
    part=4, chapter="Circuit Dynamics and Mutual Induction",
    theory_class="maxwell_original",
    description="Verify energy conservation in coupled circuit system",
)
def verify_energy_conservation(
    circuits: list[Circuit],
    mutual_inductances: dict[tuple[int, int], float],
    tolerance: float = 1e-10,
) -> dict[str, float | bool | np.ndarray]:
    """
    Verify energy conservation in a coupled circuit system.

    Arts. 578, 581-582: The total electrokinetic energy can be computed
    two equivalent ways:

    1. Sum of individual contributions:
       T = Σ (1/2) Lᵢᵢ Iᵢ² + Σ Mᵢⱼ Iᵢ Iⱼ

    2. Matrix formulation:
       T = (1/2) Iᵀ · L · I

    This function verifies both methods give identical results,
    confirming energy conservation and correct implementation.

    Args:
        circuits: List of Circuit objects.
        mutual_inductances: Dict mapping (i,j) to mutual inductance M_ij.
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with:
        - energy_sum: Energy from summing contributions
        - energy_matrix: Energy from matrix formulation
        - self_energy_total: Total self-inductance energy
        - mutual_energy_total: Total mutual inductance energy
        - relative_error: |E_sum - E_matrix| / E_sum
        - verified: True if energies match within tolerance

    Reference:
        Part IV, Arts. 578, 581-582: Energy conservation verification.

    Example:
        >>> c1 = Circuit(self_inductance=10.0, resistance=1.0, current=5.0)
        >>> c2 = Circuit(self_inductance=5.0, resistance=1.0, current=3.0)
        >>> result = verify_energy_conservation([c1, c2], {(0, 1): 2.0})
        >>> assert result["verified"]
    """
    n = len(circuits)
    if n == 0:
        return {
            "energy_sum": 0.0,
            "energy_matrix": 0.0,
            "self_energy_total": 0.0,
            "mutual_energy_total": 0.0,
            "relative_error": 0.0,
            "verified": True,
        }

    # Method 1: Sum of contributions
    self_energy_total = sum(0.5 * c.self_inductance * c.current ** 2 for c in circuits)

    mutual_energy_total = 0.0
    for (i, j), M in mutual_inductances.items():
        if 0 <= i < n and 0 <= j < n:
            mutual_energy_total += M * circuits[i].current * circuits[j].current

    energy_sum = self_energy_total + mutual_energy_total

    # Method 2: Matrix formulation T = (1/2) Iᵀ · L · I
    L_matrix = np.zeros((n, n))
    for i, circuit in enumerate(circuits):
        L_matrix[i, i] = circuit.self_inductance

    for (i, j), M in mutual_inductances.items():
        if 0 <= i < n and 0 <= j < n:
            L_matrix[i, j] = M
            L_matrix[j, i] = M

    I_vector = np.array([c.current for c in circuits])
    energy_matrix = 0.5 * np.dot(I_vector, np.dot(L_matrix, I_vector))

    # Verify equality
    if energy_sum != 0:
        relative_error = abs(energy_sum - energy_matrix) / abs(energy_sum)
    else:
        relative_error = 0.0 if energy_matrix == 0 else float('inf')

    verified = relative_error <= tolerance

    return {
        "energy_sum": energy_sum,
        "energy_matrix": energy_matrix,
        "self_energy_total": self_energy_total,
        "mutual_energy_total": mutual_energy_total,
        "relative_error": relative_error,
        "verified": verified,
        "tolerance_used": tolerance,
    }


@maxwell_cite(
    578, 579, 580, 581, 582, 583, 584,
    part=4, chapter="Circuit Dynamics and Mutual Induction",
    theory_class="maxwell_original",
    description="Verify complete circuit dynamics theory",
)
def verify_circuit_dynamics(
    tolerance: float = 1e-10,
) -> dict[str, bool | dict]:
    """
    Comprehensive verification of circuit dynamics theory.

    Arts. 578-584: This function verifies the complete theory of
    self and mutual induction through numerical experiments:

    1. Self-inductance energy formula: T = (1/2) L I²
    2. Mutual inductance energy: T = (1/2) L₁ I₁² + (1/2) L₂ I₂² + M I₁ I₂
    3. Energy conservation between formulations
    4. Coupling coefficient bounds: 0 ≤ |k| ≤ 1
    5. Symmetry of mutual inductance: M₁₂ = M₂₁

    Args:
        tolerance: Numerical tolerance for all verifications.

    Returns:
        Dictionary with verification results for each aspect.

    Reference:
        Part IV, Arts. 578-584: Complete circuit dynamics verification.
    """
    results = {}

    # Test 1: Self-inductance energy
    L = 10.0
    I = 5.0
    expected_energy = 0.5 * L * I ** 2

    circuit = Circuit(self_inductance=L, resistance=1.0, current=I)
    computed_energy = circuit.energy()

    results["self_inductance_energy"] = {
        "expected": expected_energy,
        "computed": computed_energy,
        "verified": abs(expected_energy - computed_energy) <= tolerance * expected_energy,
    }

    # Test 2: Mutual inductance energy (two circuits)
    L1, L2 = 10.0, 5.0
    I1, I2 = 3.0, 4.0
    M = 2.0

    c1 = Circuit(self_inductance=L1, resistance=1.0, current=I1)
    c2 = Circuit(self_inductance=L2, resistance=1.0, current=I2)
    coupled = CoupledCircuits(c1, c2, mutual_inductance=M)

    # Scalar formula
    expected_total = 0.5 * L1 * I1 ** 2 + 0.5 * L2 * I2 ** 2 + M * I1 * I2
    computed_total = coupled.total_energy()

    results["mutual_inductance_energy"] = {
        "expected": expected_total,
        "computed": computed_total,
        "verified": abs(expected_total - computed_total) <= tolerance * expected_total,
    }

    # Test 3: Coupling coefficient bounds
    k = coupled.coupling_coefficient
    results["coupling_coefficient"] = {
        "value": k,
        "in_bounds": 0 <= abs(k) <= 1,
        "verified": 0 <= abs(k) <= 1,
    }

    # Test 4: Energy conservation (matrix vs scalar)
    energy_result = verify_energy_conservation([c1, c2], {(0, 1): M}, tolerance)
    results["energy_conservation"] = {
        "energy_sum": energy_result["energy_sum"],
        "energy_matrix": energy_result["energy_matrix"],
        "relative_error": energy_result["relative_error"],
        "verified": energy_result["verified"],
    }

    # Test 5: Induced EMF (self and mutual)
    dI_dt = 10.0
    expected_self_emf = -L * dI_dt
    computed_self_emf = circuit.induced_emf(dI_dt)

    expected_mutual_emf = -M * dI_dt
    computed_mutual_emf_1 = coupled.emf_on_1(dI_dt)
    computed_mutual_emf_2 = coupled.emf_on_2(dI_dt)

    results["induced_emf"] = {
        "self_expected": expected_self_emf,
        "self_computed": computed_self_emf,
        "self_verified": abs(expected_self_emf - computed_self_emf) <= tolerance * abs(expected_self_emf),
        "mutual_expected": expected_mutual_emf,
        "mutual_computed_1": computed_mutual_emf_1,
        "mutual_computed_2": computed_mutual_emf_2,
        "mutual_symmetric": abs(computed_mutual_emf_1 - computed_mutual_emf_2) <= tolerance,
        "verified": (
            abs(expected_self_emf - computed_self_emf) <= tolerance * abs(expected_self_emf) and
            abs(expected_mutual_emf - computed_mutual_emf_1) <= tolerance * abs(expected_mutual_emf) and
            abs(computed_mutual_emf_1 - computed_mutual_emf_2) <= tolerance
        ),
    }

    # Overall verification
    all_verified = all(
        test.get("verified", False) if isinstance(test, dict) else test
        for test in results.values()
    )
    results["all_verified"] = all_verified

    return results

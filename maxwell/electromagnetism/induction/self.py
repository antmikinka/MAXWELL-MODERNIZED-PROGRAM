"""maxwell.electromagnetism.induction.self — Self-induction (Arts. 546-551).

Implements Maxwell's treatment of self-induction, where a changing current
in a circuit induces an EMF in the same circuit.

Maxwell's CGS formulation (Arts. 546-551):
    Self-inductance L relates flux to current:
        Phi = L * I

    Self-induced EMF:
        EMF = -L * dI/dt

    Energy stored in inductor:
        W = (1/2) * L * I²

where:
    L = self-inductance (cm in CGS-EMU)
    I = current (abamperes)
    Phi = magnetic flux (maxwells)
    EMF = electromotive force (abvolts)

Category: A (maxwell_original) — Maxwell's theory of self-induction.

References:
    Part IV, Arts. 546-551: Self-induction and inductance.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class SelfInductance:
    """
    Self-inductance calculator for various geometries.

    Art. 546-551: Self-inductance L is the ratio of magnetic flux
    through a circuit to the current producing it:

        L = Phi / I

    The self-induced EMF opposes changes in current:

        EMF = -L * dI/dt

    Attributes:
        inductance: Self-inductance value (cm).
        geometry: Description of the geometry.
    """

    inductance: float
    geometry: str = "unknown"

    def __post_init__(self):
        """Validate inductance."""
        if self.inductance < 0:
            raise ValueError(f"Inductance must be non-negative, got {self.inductance}")

    @maxwell_cite(
        546, 547,
        part=4, chapter="Self-Induction",
        theory_class="maxwell_original",
        description="Calculate self-induced EMF",
    )
    def induced_emf(self, dI_dt: float) -> float:
        """
        Calculate self-induced EMF.

        Art. 546-547: The self-induced EMF is:

            EMF = -L * dI/dt

        The negative sign indicates opposition to current change.

        Args:
            dI_dt: Rate of change of current (abamperes/s).

        Returns:
            Self-induced EMF (abvolts).
        """
        return -self.inductance * dI_dt

    @maxwell_cite(
        548, 549,
        part=4, chapter="Self-Induction",
        theory_class="maxwell_original",
        description="Calculate energy stored in inductor",
    )
    def stored_energy(self, current: float) -> float:
        """
        Calculate energy stored in the inductor.

        Art. 548-549: The energy stored in an inductor is:

            W = (1/2) * L * I²

        Args:
            current: Current through inductor (abamperes).

        Returns:
            Stored energy (ergs).
        """
        return 0.5 * self.inductance * current ** 2

    @maxwell_cite(
        550, 551,
        part=4, chapter="Self-Induction",
        theory_class="maxwell_original",
        description="Calculate magnetic flux from current",
    )
    def flux(self, current: float) -> float:
        """
        Calculate magnetic flux through the circuit.

        Art. 550-551: The flux is:

            Phi = L * I

        Args:
            current: Current (abamperes).

        Returns:
            Magnetic flux (maxwells).
        """
        return self.inductance * current


@maxwell_cite(
    546, 547, 548,
    part=4, chapter="Self-Induction",
    theory_class="maxwell_original",
    description="Calculate self-inductance of solenoid",
)
def calc_solenoid_inductance(
    n_turns: int,
    radius: float,
    length: float,
    mu_r: float = 1.0,
) -> float:
    """
    Calculate self-inductance of a solenoid.

    Art. 546-548: For a long solenoid (length >> radius):

        L = 4*pi² * n² * r² * mu_r / l

    where:
        n = number of turns
        r = radius (cm)
        l = length (cm)
        mu_r = relative permeability

    In CGS-EMU, L is in centimeters.

    Args:
        n_turns: Number of turns.
        radius: Solenoid radius (cm).
        length: Solenoid length (cm).
        mu_r: Relative permeability (default 1.0 for air).

    Returns:
        Self-inductance (cm).

    Reference:
        Part IV, Arts. 546-548: Solenoid inductance.
    """
    if length <= 0 or radius <= 0:
        raise ValueError("Dimensions must be positive")

    n = n_turns
    r = radius
    l = length

    # L = 4*pi² * n² * r² * mu_r / l
    return 4.0 * np.pi ** 2 * n ** 2 * r ** 2 * mu_r / l


@maxwell_cite(
    546, 547,
    part=4, chapter="Self-Induction",
    theory_class="maxwell_original",
    description="Calculate self-inductance of circular loop",
)
def calc_loop_inductance(
    radius: float,
    wire_radius: float = None,
) -> float:
    """
    Calculate self-inductance of a circular loop.

    Art. 546-547: For a circular loop of radius R made from wire
    of radius a:

        L = 4*pi*R * (ln(8R/a) - 7/4)  (approximate)

    This formula assumes R >> a.

    Args:
        radius: Loop radius R (cm).
        wire_radius: Wire radius a (cm, default R/100).

    Returns:
        Self-inductance (cm).

    Reference:
        Part IV, Arts. 546-547: Circular loop inductance.
    """
    if radius <= 0:
        raise ValueError("Radius must be positive")

    R = radius
    a = wire_radius if wire_radius is not None else R / 100.0

    if a <= 0 or a >= R:
        raise ValueError("Wire radius must be positive and less than loop radius")

    # L = 4*pi*R * (ln(8R/a) - 7/4)
    return 4.0 * np.pi * R * (np.log(8.0 * R / a) - 1.75)


@maxwell_cite(
    546, 547,
    part=4, chapter="Self-Induction",
    theory_class="maxwell_original",
    description="Calculate self-induced EMF: EMF = -L*dI/dt",
)
def calc_self_induced_emf(
    inductance: float,
    dI_dt: float,
) -> float:
    """
    Calculate self-induced electromotive force.

    Art. 546-547: The self-induced EMF is:

        EMF = -L * dI/dt

    The negative sign (Lenz's law) indicates the EMF opposes
    the change in current.

    Args:
        inductance: Self-inductance L (cm).
        dI_dt: Rate of change of current (abamperes/s).

    Returns:
        Self-induced EMF (abvolts).

    Reference:
        Part IV, Arts. 546-547: Self-induced EMF.
    """
    return -inductance * dI_dt


@maxwell_cite(
    548, 549,
    part=4, chapter="Self-Induction",
    theory_class="maxwell_original",
    description="Calculate energy stored in inductor: W = (1/2)*L*I²",
)
def calc_inductor_energy(
    inductance: float,
    current: float,
) -> float:
    """
    Calculate energy stored in an inductor.

    Art. 548-549: The magnetic energy stored in an inductor is:

        W = (1/2) * L * I²

    Args:
        inductance: Self-inductance L (cm).
        current: Current I (abamperes).

    Returns:
        Stored energy (ergs).

    Reference:
        Part IV, Arts. 548-549: Inductor energy.
    """
    return 0.5 * inductance * current ** 2


@maxwell_cite(
    550, 551,
    part=4, chapter="Self-Induction",
    theory_class="maxwell_original",
    description="Calculate current rise in RL circuit",
)
def calc_rl_current_rise(
    voltage: float,
    resistance: float,
    inductance: float,
    time: float,
) -> float:
    """
    Calculate current in an RL circuit after voltage is applied.

    Art. 550-551: For an RL circuit with applied voltage V:

        I(t) = (V/R) * (1 - exp(-R*t/L))

    The time constant is tau = L/R.

    Args:
        voltage: Applied voltage (abvolts).
        resistance: Resistance (abohms).
        inductance: Inductance (cm).
        time: Time after voltage applied (s).

    Returns:
        Current at time t (abamperes).

    Reference:
        Part IV, Arts. 550-551: RL circuit response.
    """
    if resistance <= 0 or inductance <= 0:
        raise ValueError("R and L must be positive")

    tau = inductance / resistance  # Time constant
    I_final = voltage / resistance

    return I_final * (1.0 - np.exp(-time / tau))


@maxwell_cite(
    550, 551,
    part=4, chapter="Self-Induction",
    theory_class="maxwell_original",
    description="Calculate current decay in RL circuit",
)
def calc_rl_current_decay(
    initial_current: float,
    resistance: float,
    inductance: float,
    time: float,
) -> float:
    """
    Calculate current decay in an RL circuit.

    Art. 550-551: For an RL circuit with initial current I0:

        I(t) = I0 * exp(-R*t/L)

    Args:
        initial_current: Initial current I0 (abamperes).
        resistance: Resistance (abohms).
        inductance: Inductance (cm).
        time: Time (s).

    Returns:
        Current at time t (abamperes).

    Reference:
        Part IV, Arts. 550-551: RL circuit decay.
    """
    if resistance <= 0 or inductance <= 0:
        raise ValueError("R and L must be positive")

    tau = inductance / resistance

    return initial_current * np.exp(-time / tau)


@maxwell_cite(
    546, 551,
    part=4, chapter="Self-Induction",
    theory_class="maxwell_original",
    description="Verify self-induction energy relations",
)
def verify_self_induction(
    inductance: float = 100.0,
    resistance: float = 1.0,
    voltage: float = 1.0,
    test_times: list[float] = None,
    tolerance: float = 1e-6,
) -> dict[str, float | bool | list]:
    """
    Verify self-induction energy relations.

    Art. 546-551: This function verifies:
    1. W = (1/2)*L*I²
    2. Energy conservation in RL circuit
    3. Time constant tau = L/R

    Args:
        inductance: Test inductance (cm).
        resistance: Test resistance (abohms).
        voltage: Test voltage (abvolts).
        test_times: Times to evaluate.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if test_times is None:
        tau = inductance / resistance
        test_times = [0.1*tau, 0.5*tau, tau, 2*tau, 5*tau]

    I_final = voltage / resistance
    tau = inductance / resistance

    energies = []
    currents = []

    for t in test_times:
        I = calc_rl_current_rise(voltage, resistance, inductance, t)
        W = calc_inductor_energy(inductance, I)
        currents.append(I)
        energies.append(W)

    # Verify final energy = (1/2)*L*I_final²
    W_final_expected = 0.5 * inductance * I_final ** 2
    W_final_actual = energies[-1] if currents[-1] > 0.99 * I_final else energies[-1]

    # Time constant verification
    I_at_tau = calc_rl_current_rise(voltage, resistance, inductance, tau)
    expected_at_tau = I_final * (1.0 - np.exp(-1))
    tau_error = abs(I_at_tau - expected_at_tau) / I_final

    energy_verified = abs(W_final_actual - W_final_expected) / W_final_expected < tolerance if W_final_expected > 0 else True
    tau_verified = tau_error < tolerance

    return {
        "inductance": inductance,
        "resistance": resistance,
        "voltage": voltage,
        "time_constant": tau,
        "test_times": test_times,
        "currents": currents,
        "energies": energies,
        "final_current": currents[-1] if currents else 0,
        "expected_final_current": I_final,
        "final_energy": energies[-1] if energies else 0,
        "expected_final_energy": W_final_expected,
        "tau_verified": tau_verified,
        "energy_verified": energy_verified,
        "verified": tau_verified and energy_verified,
    }


@maxwell_cite(
    546, 547, 548, 549, 550, 551,
    part=4, chapter="Self-Induction",
    theory_class="maxwell_original",
    description="Complete self-induction analysis",
)
def analyze_self_induction(
    inductance: float,
    initial_current: float = 0.0,
    applied_voltage: float = 0.0,
    resistance: float = 1.0,
    time_range: tuple[float, float] = None,
) -> dict[str, float | list]:
    """
    Complete analysis of self-induction phenomena.

    Art. 546-551: Comprehensive analysis including:
    1. Time-dependent current
    2. Self-induced EMF
    3. Stored energy
    4. Time constant

    Args:
        inductance: Self-inductance (cm).
        initial_current: Initial current (abamperes).
        applied_voltage: Applied voltage (abvolts).
        resistance: Circuit resistance (abohms).
        time_range: (t_min, t_max) in seconds.

    Returns:
        Dictionary with complete analysis results.
    """
    tau = inductance / resistance

    if time_range is None:
        time_range = (0.0, 5.0 * tau)

    n_points = 100
    times = np.linspace(time_range[0], time_range[1], n_points)

    currents = []
    emfs = []
    energies = []

    for t in times:
        if applied_voltage != 0:
            # Rising current with applied voltage
            I = calc_rl_current_rise(applied_voltage, resistance, inductance, t)
            I = I + initial_current * np.exp(-t / tau)
        else:
            # Decaying current
            I = initial_current * np.exp(-t / tau)

        dI_dt = -I / tau if applied_voltage == 0 else (applied_voltage - I * resistance) / inductance

        emf = calc_self_induced_emf(inductance, dI_dt)
        W = calc_inductor_energy(inductance, I)

        currents.append(I)
        emfs.append(emf)
        energies.append(W)

    return {
        "inductance": inductance,
        "resistance": resistance,
        "time_constant": tau,
        "initial_current": initial_current,
        "applied_voltage": applied_voltage,
        "times": times,
        "currents": currents,
        "self_induced_emfs": emfs,
        "stored_energies": energies,
        "max_current": max(currents),
        "max_emf": max(abs(e) for e in emfs),
        "max_energy": max(energies),
    }

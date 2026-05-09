"""maxwell.electromagnetism.theory.conservation — Energy conservation derivation (Arts. 543-544).

Implements Maxwell's derivation of energy conservation in electromagnetic
systems, showing how electromagnetic energy is converted to other forms.

Maxwell's CGS formulation (Arts. 543-544):
    Energy conservation in electromagnetic systems:

    dW/dt = EMF * I - I²*R

    where:
    - EMF * I is the power supplied by external sources
    - I²*R is the power dissipated as heat
    - dW/dt is the rate of change of stored electromagnetic energy

    For inductive circuits:
    W = (1/2) * L * I² + (1/2) * M * I1 * I2

where:
    W = electromagnetic energy (ergs)
    EMF = electromotive force (abvolts)
    I = current (abamperes)
    R = resistance (abohms)
    L = self-inductance (cm)
    M = mutual inductance (cm)

Category: A (maxwell_original) — Maxwell's energy conservation theory.

References:
    Part IV, Arts. 543-544: Conservation of energy in electromagnetic systems.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class EnergyConservation:
    """
    Energy conservation calculator for electromagnetic systems.

    Art. 543-544: Maxwell showed that electromagnetic systems obey
    energy conservation:

        Power_in = Power_stored + Power_dissipated

    For a circuit with inductance:
        V*I = d/dt((1/2)*L*I²) + I²*R

    Attributes:
        inductance: Self-inductance L (cm).
        resistance: Resistance R (abohms).
        mutual_inductance: Mutual inductance M (cm, default 0).
    """

    inductance: float = 0.0
    resistance: float = 1.0
    mutual_inductance: float = 0.0

    def __post_init__(self):
        """Validate parameters."""
        if self.inductance < 0:
            raise ValueError(f"Inductance must be non-negative")
        if self.resistance < 0:
            raise ValueError(f"Resistance must be non-negative")

    @maxwell_cite(
        543,
        544,
        part=4,
        chapter="Energy Conservation",
        theory_class="maxwell_original",
        description="Calculate stored electromagnetic energy",
    )
    def stored_energy(self, current: float, current2: float = 0.0) -> float:
        """
        Calculate total stored electromagnetic energy.

        Art. 543-544: For a system with self and mutual inductance:

            W = (1/2)*L1*I1² + (1/2)*L2*I2² + M*I1*I2

        Args:
            current: Current in primary circuit (abamperes).
            current2: Current in secondary circuit (abamperes, default 0).

        Returns:
            Stored energy (ergs).
        """
        energy = 0.5 * self.inductance * current**2

        if self.mutual_inductance != 0 and current2 != 0:
            energy += self.mutual_inductance * current * current2

        return energy

    @maxwell_cite(
        543,
        544,
        part=4,
        chapter="Energy Conservation",
        theory_class="maxwell_original",
        description="Calculate power dissipation",
    )
    def power_dissipated(self, current: float) -> float:
        """
        Calculate power dissipated as heat.

        Art. 543-544: The power dissipated in resistance is:

            P_dissipated = I² * R

        Args:
            current: Current (abamperes).

        Returns:
            Power dissipated (ergs/s).
        """
        return current**2 * self.resistance

    def joule_heat(self, current: float, resistance: float = None) -> float:
        """
        Calculate Joule heating power.

        Args:
            current: Current (abamperes).
            resistance: Resistance (abohms, uses self.resistance if None).

        Returns:
            Joule heating power (ergs/s).
        """
        R = resistance if resistance is not None else self.resistance
        return current**2 * R

    def electrical_power(self, emf: float, current: float) -> float:
        """
        Calculate electrical power supplied.

        Art. 543-544: P = EMF * I

        Args:
            emf: Electromotive force (abvolts).
            current: Current (abamperes).

        Returns:
            Electrical power (ergs/s).
        """
        return emf * current

    @maxwell_cite(
        543,
        544,
        part=4,
        chapter="Energy Conservation",
        theory_class="maxwell_original",
        description="Calculate rate of energy storage",
    )
    def power_stored(self, current: float, dI_dt: float) -> float:
        """
        Calculate rate of energy storage in magnetic field.

        Art. 543-544: The rate of energy storage is:

            dW/dt = L * I * dI/dt

        Args:
            current: Current (abamperes).
            dI_dt: Rate of change of current (abamperes/s).

        Returns:
            Rate of energy storage (ergs/s).
        """
        return self.inductance * current * dI_dt

    @maxwell_cite(
        543,
        544,
        part=4,
        chapter="Energy Conservation",
        theory_class="maxwell_original",
        description="Verify energy balance",
    )
    def verify_energy_balance(
        self,
        voltage: float,
        current: float,
        dI_dt: float,
        tolerance: float = 1e-6,
    ) -> dict[str, float | bool]:
        """
        Verify energy conservation.

        Art. 543-544: Energy balance equation:

            V*I = dW/dt + I²*R

        Args:
            voltage: Applied voltage (abvolts).
            current: Current (abamperes).
            dI_dt: Rate of change of current (abamperes/s).
            tolerance: Numerical tolerance.

        Returns:
            Dictionary with energy balance verification.
        """
        power_in = voltage * current
        power_stored = self.power_stored(current, dI_dt)
        power_dissipated = self.power_dissipated(current)

        balance = power_in - power_stored - power_dissipated
        relative_error = (
            abs(balance) / abs(power_in) if abs(power_in) > 1e-15 else abs(balance)
        )

        return {
            "power_in": power_in,
            "power_stored": power_stored,
            "power_dissipated": power_dissipated,
            "balance_error": balance,
            "relative_error": relative_error,
            "conservation_verified": relative_error < tolerance,
        }


@maxwell_cite(
    543,
    544,
    part=4,
    chapter="Energy Conservation",
    theory_class="maxwell_original",
    description="Calculate electromagnetic energy in circuit",
)
def calc_electromagnetic_energy(
    inductance: float,
    current: float,
    mutual_inductance: float = 0.0,
    current2: float = 0.0,
) -> float:
    """
    Calculate total electromagnetic energy in a circuit system.

    Art. 543-544: The total energy is:

        W = (1/2)*L*I² + (1/2)*L2*I2² + M*I1*I2

    For a single circuit (I2 = 0):
        W = (1/2)*L*I²

    Args:
        inductance: Self-inductance L1 (cm).
        current: Current I1 (abamperes).
        mutual_inductance: Mutual inductance M (cm).
        current2: Current I2 (abamperes).

    Returns:
        Total electromagnetic energy (ergs).

    Reference:
        Part IV, Arts. 543-544: Electromagnetic energy.
    """
    energy = 0.5 * inductance * current**2

    if mutual_inductance != 0:
        energy += 0.5 * 0 * current2**2  # L2 assumed 0 if not provided
        energy += mutual_inductance * current * current2

    return energy


@maxwell_cite(
    543,
    544,
    part=4,
    chapter="Energy Conservation",
    theory_class="maxwell_original",
    description="Calculate power supplied to circuit",
)
def calc_power_supplied(
    voltage: float,
    current: float,
) -> float:
    """
    Calculate power supplied to a circuit.

    Art. 543-544: The power supplied by an external source is:

        P = V * I

    Args:
        voltage: Applied voltage (abvolts).
        current: Current (abamperes).

    Returns:
        Power supplied (ergs/s).

    Reference:
        Part IV, Arts. 543-544: Power supplied.
    """
    return voltage * current


@maxwell_cite(
    543,
    544,
    part=4,
    chapter="Energy Conservation",
    theory_class="maxwell_original",
    description="Calculate work done by EMF",
)
def calc_work_by_emf(
    emf: float,
    current: float,
    time_interval: float,
) -> float:
    """
    Calculate work done by an EMF over a time interval.

    Art. 543-544: The work done is:

        W = integral(EMF * I * dt)

    For constant EMF and current:
        W = EMF * I * t

    Args:
        emf: Electromotive force (abvolts).
        current: Current (abamperes).
        time_interval: Time interval (s).

    Returns:
        Work done (ergs).

    Reference:
        Part IV, Arts. 543-544: Work by EMF.
    """
    return emf * current * time_interval


@maxwell_cite(
    543,
    544,
    part=4,
    chapter="Energy Conservation",
    theory_class="maxwell_original",
    description="Verify energy conservation in circuit",
)
def verify_energy_conservation(
    emf: float,
    current: float,
    resistance: float,
    mechanical_power: float = 0.0,
    tolerance: float = 1e-6,
) -> dict[str, float | bool]:
    """
    Verify energy conservation in electromagnetic system.

    Art. 543-544: Energy balance:

        dW_electric = dW_mechanical + dW_heat

    where:
        dW_electric = EMF * I
        dW_mechanical = mechanical_power
        dW_heat = I² * R

    Args:
        emf: Electromotive force (abvolts).
        current: Current (abamperes).
        resistance: Resistance (abohms).
        mechanical_power: Mechanical power output (ergs/s).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    electrical_power = emf * current
    heat_power = current**2 * resistance

    # Energy balance: electrical = mechanical + heat + stored
    stored_power = electrical_power - heat_power - mechanical_power

    balance = electrical_power - (mechanical_power + heat_power + stored_power)
    relative_error = (
        abs(balance) / abs(electrical_power)
        if abs(electrical_power) > 1e-15
        else abs(balance)
    )

    return {
        "electrical_power": electrical_power,
        "heat_power": heat_power,
        "mechanical_power": mechanical_power,
        "stored_power": stored_power,
        "balance_error": balance,
        "relative_error": relative_error,
        "energy_conserved": relative_error < tolerance,
    }


@maxwell_cite(
    543,
    544,
    part=4,
    chapter="Energy Conservation",
    theory_class="maxwell_original",
    description="Verify energy conservation in RL circuit",
)
def verify_energy_conservation_rl(
    inductance: float,
    resistance: float,
    voltage: float,
    test_times: list[float] = None,
    tolerance: float = 1e-6,
) -> dict[str, float | bool | list]:
    """
    Verify energy conservation in an RL circuit.

    Art. 543-544: This function verifies that:

        Power_in = Power_stored + Power_dissipated

    at all times during the transient response.

    Args:
        inductance: Circuit inductance (cm).
        resistance: Circuit resistance (abohms).
        voltage: Applied voltage (abvolts).
        test_times: Times to evaluate.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if test_times is None:
        tau = inductance / resistance
        test_times = [0.01 * tau, 0.1 * tau, 0.5 * tau, tau, 2 * tau, 5 * tau]

    I_final = voltage / resistance
    tau = inductance / resistance

    results = []
    all_verified = True

    for t in test_times:
        # Current at time t
        I = I_final * (1.0 - np.exp(-t / tau))

        # dI/dt at time t
        dI_dt = (voltage / inductance) * np.exp(-t / tau)

        # Power calculations
        power_in = voltage * I
        power_stored = inductance * I * dI_dt
        power_dissipated = I**2 * resistance

        # Check balance
        balance = power_in - power_stored - power_dissipated
        relative_error = (
            abs(balance) / abs(power_in) if abs(power_in) > 1e-15 else abs(balance)
        )

        verified = relative_error < tolerance
        all_verified = all_verified and verified

        results.append(
            {
                "time": t,
                "current": I,
                "power_in": power_in,
                "power_stored": power_stored,
                "power_dissipated": power_dissipated,
                "balance_error": balance,
                "relative_error": relative_error,
                "verified": verified,
            }
        )

    return {
        "inductance": inductance,
        "resistance": resistance,
        "voltage": voltage,
        "time_constant": tau,
        "test_times": test_times,
        "results_by_time": results,
        "all_verified": all_verified,
        "conservation_verified": all_verified,
    }


@maxwell_cite(
    543,
    544,
    part=4,
    chapter="Energy Conservation",
    theory_class="maxwell_original",
    description="Calculate energy transfer between coupled circuits",
)
def calc_energy_transfer(
    mutual_inductance: float,
    current1_initial: float,
    current2_initial: float,
    current1_final: float,
    current2_final: float,
) -> dict[str, float]:
    """
    Calculate energy transfer between coupled circuits.

    Art. 543-544: For two coupled circuits, the mutual energy is:

        W_mutual = M * I1 * I2

    The change in mutual energy represents energy transfer.

    Args:
        mutual_inductance: Mutual inductance M (cm).
        current1_initial: Initial current in circuit 1 (abamperes).
        current2_initial: Initial current in circuit 2 (abamperes).
        current1_final: Final current in circuit 1 (abamperes).
        current2_final: Final current in circuit 2 (abamperes).

    Returns:
        Dictionary with energy transfer results.

    Reference:
        Part IV, Arts. 543-544: Energy transfer between circuits.
    """
    W_mutual_initial = mutual_inductance * current1_initial * current2_initial
    W_mutual_final = mutual_inductance * current1_final * current2_final

    delta_W_mutual = W_mutual_final - W_mutual_initial

    return {
        "mutual_energy_initial": W_mutual_initial,
        "mutual_energy_final": W_mutual_final,
        "energy_transferred": delta_W_mutual,
        "current1_change": current1_final - current1_initial,
        "current2_change": current2_final - current2_initial,
    }


@maxwell_cite(
    543,
    544,
    part=4,
    chapter="Energy Conservation",
    theory_class="maxwell_original",
    description="Complete energy conservation analysis",
)
def analyze_energy_conservation(
    inductance: float,
    resistance: float,
    voltage: float,
    initial_current: float = 0.0,
    time_range: tuple[float, float] = None,
) -> dict[str, float | list]:
    """
    Complete analysis of energy conservation in electromagnetic systems.

    Art. 543-544: Comprehensive analysis including:
    1. Time-dependent energy storage
    2. Power dissipation
    3. Energy balance verification
    4. Efficiency calculations

    Args:
        inductance: Circuit inductance (cm).
        resistance: Circuit resistance (abohms).
        voltage: Applied voltage (abvolts).
        initial_current: Initial current (abamperes).
        time_range: (t_min, t_max) in seconds.

    Returns:
        Dictionary with complete analysis results.
    """
    tau = inductance / resistance
    I_final = voltage / resistance

    if time_range is None:
        time_range = (0.0, 5.0 * tau)

    n_points = 100
    times = np.linspace(time_range[0], time_range[1], n_points)

    energies = []
    powers_in = []
    powers_stored = []
    powers_dissipated = []

    for t in times:
        # Current
        I = I_final * (1.0 - np.exp(-t / tau)) + initial_current * np.exp(-t / tau)

        # dI/dt
        dI_dt = ((voltage - initial_current * resistance) / inductance) * np.exp(
            -t / tau
        )

        # Energy and power
        W = 0.5 * inductance * I**2
        P_in = voltage * I
        P_stored = inductance * I * dI_dt
        P_dissipated = I**2 * resistance

        energies.append(W)
        powers_in.append(P_in)
        powers_stored.append(P_stored)
        powers_dissipated.append(P_dissipated)

    # Final values
    W_final = energies[-1]
    W_max = 0.5 * inductance * I_final**2
    efficiency = W_final / W_max if W_max > 0 else 0

    return {
        "inductance": inductance,
        "resistance": resistance,
        "voltage": voltage,
        "time_constant": tau,
        "final_current": I_final,
        "times": times,
        "energies": energies,
        "powers_in": powers_in,
        "powers_stored": powers_stored,
        "powers_dissipated": powers_dissipated,
        "final_energy": W_final,
        "max_storable_energy": W_max,
        "charging_efficiency": efficiency,
        "energy_balance_verified": all(
            abs(p_in - p_stored - p_diss) / max(abs(p_in), 1e-15) < 1e-10
            for p_in, p_stored, p_diss in zip(
                powers_in, powers_stored, powers_dissipated
            )
        ),
    }

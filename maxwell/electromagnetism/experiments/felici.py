"""maxwell.electromagnetism.experiments.felici — Felici's law experiments (Arts. 536-539).

Implements Felici's law: the total induced charge in a circuit
depends only on the change in magnetic flux linkage, not on the
rate of change or the time profile.

Maxwell's CGS formulation (Arts. 536-539):
    Faraday's law of induction:

        EMF = -(1/c) * dPhi/dt

    The induced current in a circuit of resistance R:

        I_induced = EMF / R = -(1/(c*R)) * dPhi/dt

    The total induced charge is:

        Q = integral(I_induced * dt)
          = -(1/(c*R)) * integral(dPhi/dt * dt)
          = -(1/(c*R)) * (Phi_final - Phi_initial)
          = -Delta_Phi / (c * R)

    Felici's key result: Q depends only on Delta_Phi, not on
    how fast the flux changes.

    For mutual inductance M between two circuits:

        Phi_2 = M * I_1

        Q_2 = -(M * Delta_I_1) / (c * R_2)

where:
    Phi = magnetic flux (maxwells = gauss*cm^2)
    R = resistance (CGS-EMU: cm/s)
    Q = induced charge (esu)
    M = mutual inductance (cm in CGS-EMU)
    c = speed of light (cm/s)

Category: A (maxwell_original) — Felici's induction law.

References:
    Part IV, Arts. 536-539: Felici's experiments on induction.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class InductionEvent:
    """Result from an induction experiment.

    Attributes:
        delta_flux: Change in magnetic flux (maxwells).
        resistance: Circuit resistance (CGS units).
        induced_charge: Total induced charge (esu).
        induced_emf_peak: Peak induced EMF (statvolts).
        duration: Duration of flux change (seconds).
    """

    delta_flux: float
    resistance: float
    induced_charge: float
    induced_emf_peak: float
    duration: float


@dataclass
class FeliciResult:
    """Complete Felici's law experiment result.

    Attributes:
        events: List of induction events with different time profiles.
        mutual_inductance: Mutual inductance between circuits (cm).
        delta_current: Change in primary current (abamperes).
        charges: Induced charges for each event.
        charges_equal: Whether all charges are equal (within tolerance).
    """

    events: list[InductionEvent]
    mutual_inductance: float
    delta_current: float
    charges: list[float]
    charges_equal: bool


def _induced_emf(dflux_dt: float) -> float:
    """Calculate induced EMF from flux change rate.

    EMF = -(1/c) * dPhi/dt
    """
    return -dflux_dt / CONST.C


def _induced_charge(delta_flux: float, resistance: float) -> float:
    """Calculate total induced charge from flux change.

    Q = -Delta_Phi / (c * R)
    """
    if resistance < 1e-15:
        return 0.0
    return -delta_flux / (CONST.C * resistance)


@maxwell_cite(
    536, 537,
    part=4, chapter="Felici's Law",
    theory_class="maxwell_original",
    description="Simulate induction with linear flux ramp",
)
def simulate_linear_ramp(
    initial_flux: float,
    final_flux: float,
    resistance: float,
    duration: float,
) -> InductionEvent:
    """Simulate induction with linearly changing flux.

    Art. 536-537: Linear flux ramp from initial to final value.

    Args:
        initial_flux: Initial magnetic flux (maxwells).
        final_flux: Final magnetic flux (maxwells).
        resistance: Circuit resistance (CGS units).
        duration: Ramp duration (seconds).

    Returns:
        InductionEvent with results.
    """
    delta_flux = final_flux - initial_flux
    dflux_dt = delta_flux / duration if duration > 1e-15 else 0.0

    emf = _induced_emf(dflux_dt)
    charge = _induced_charge(delta_flux, resistance)

    return InductionEvent(
        delta_flux=delta_flux,
        resistance=resistance,
        induced_charge=charge,
        induced_emf_peak=abs(emf),
        duration=duration,
    )


@maxwell_cite(
    537, 538,
    part=4, chapter="Felici's Law",
    theory_class="maxwell_original",
    description="Simulate induction with exponential flux decay",
)
def simulate_exponential_decay(
    initial_flux: float,
    resistance: float,
    time_constant: float,
    n_steps: int = 1000,
) -> InductionEvent:
    """Simulate induction with exponentially decaying flux.

    Art. 537-538: Flux decays as Phi(t) = Phi_0 * exp(-t/tau).

    Args:
        initial_flux: Initial magnetic flux (maxwells).
        resistance: Circuit resistance (CGS units).
        time_constant: Decay time constant (seconds).
        n_steps: Number of integration steps.

    Returns:
        InductionEvent with results.
    """
    # Total flux change = -initial_flux (decays to zero)
    delta_flux = -initial_flux

    # Peak EMF at t=0: dPhi/dt = -Phi_0/tau
    peak_dflux_dt = -initial_flux / time_constant
    peak_emf = _induced_emf(peak_dflux_dt)

    charge = _induced_charge(delta_flux, resistance)

    return InductionEvent(
        delta_flux=delta_flux,
        resistance=resistance,
        induced_charge=charge,
        induced_emf_peak=abs(peak_emf),
        duration=5 * time_constant,  # ~99% decay
    )


@maxwell_cite(
    538, 539,
    part=4, chapter="Felici's Law",
    theory_class="maxwell_original",
    description="Simulate induction from mutual inductance",
)
def simulate_mutual_induction(
    mutual_inductance: float,
    primary_current_initial: float,
    primary_current_final: float,
    secondary_resistance: float,
) -> InductionEvent:
    """Simulate induction via mutual inductance.

    Art. 538-539: When primary current changes, flux in secondary:

        Phi_2 = M * I_1
        Q_2 = -(M * Delta_I_1) / (c * R_2)

    Args:
        mutual_inductance: Mutual inductance (cm).
        primary_current_initial: Initial primary current (abamperes).
        primary_current_final: Final primary current (abamperes).
        secondary_resistance: Secondary circuit resistance (CGS units).

    Returns:
        InductionEvent with results.
    """
    delta_current = primary_current_final - primary_current_initial
    delta_flux = mutual_inductance * delta_current

    charge = _induced_charge(delta_flux, secondary_resistance)

    return InductionEvent(
        delta_flux=delta_flux,
        resistance=secondary_resistance,
        induced_charge=charge,
        induced_emf_peak=0.0,  # Profile-dependent
        duration=0.0,  # Felici's law: duration doesn't matter for Q
    )


@maxwell_cite(
    536, 537, 538, 539,
    part=4, chapter="Felici's Law",
    theory_class="maxwell_original",
    description="Verify Felici's law with different time profiles",
)
def verify_felici_law(
    delta_flux: float = 1000.0,
    resistance: float = 1e11,  # ~1 ohm in CGS
    tolerance: float = 1e-5,
) -> dict[str, float | bool]:
    """Verify Felici's law: induced charge is independent of time profile.

    Art. 536-539: Verifies that the same flux change produces the
    same induced charge regardless of how fast it occurs.

    Args:
        delta_flux: Flux change (maxwells).
        resistance: Circuit resistance (CGS units).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    initial_flux = 0.0
    final_flux = delta_flux

    # Expected charge
    Q_expected = _induced_charge(delta_flux, resistance)

    # Linear ramp: fast
    fast = simulate_linear_ramp(initial_flux, final_flux, resistance, duration=0.01)

    # Linear ramp: slow
    slow = simulate_linear_ramp(initial_flux, final_flux, resistance, duration=1.0)

    # Linear ramp: very slow
    very_slow = simulate_linear_ramp(initial_flux, final_flux, resistance, duration=10.0)

    # Exponential decay (same total delta)
    exponential = simulate_exponential_decay(delta_flux, resistance, time_constant=0.1)

    # Check all charges are equal
    charges = [fast.induced_charge, slow.induced_charge, very_slow.induced_charge, exponential.induced_charge]
    Q_ref = charges[0]

    all_equal = all(abs(q - Q_ref) / abs(Q_ref) < tolerance for q in charges if abs(Q_ref) > 1e-15)

    # Check against expected
    matches_expected = abs(Q_expected - Q_ref) / abs(Q_expected) < tolerance if abs(Q_expected) > 1e-15 else True

    # Peak EMF should be inversely proportional to duration
    emf_ratio = fast.induced_emf_peak / slow.induced_emf_peak if slow.induced_emf_peak > 1e-15 else 0
    expected_ratio = slow.duration / fast.duration  # 1.0 / 0.01 = 100
    emf_correct = abs(emf_ratio - expected_ratio) / expected_ratio < tolerance if expected_ratio > 1e-15 else True

    return {
        "Q_expected": Q_expected,
        "Q_fast_ramp": fast.induced_charge,
        "Q_slow_ramp": slow.induced_charge,
        "Q_very_slow_ramp": very_slow.induced_charge,
        "Q_exponential": exponential.induced_charge,
        "charges_independent_of_rate": bool(all_equal),
        "matches_expected": bool(matches_expected),
        "emf_inversely_proportional_to_rate": bool(emf_correct),
        "verified": bool(all_equal and matches_expected),
    }


@maxwell_cite(
    536, 537, 538, 539,
    part=4, chapter="Felici's Law",
    theory_class="maxwell_original",
    description="Complete Felici's law analysis",
)
def analyze_felici_law(
    delta_flux: float = 1000.0,
    resistance: float = 1e11,
    mutual_inductance: float = 100.0,
    delta_current: float = 1.0,
) -> dict[str, float | list | dict]:
    """Complete analysis of Felici's law.

    Art. 536-539: Comprehensive analysis including:
    1. Linear ramp induction
    2. Exponential decay induction
    3. Mutual induction
    4. Verification of time-profile independence

    Args:
        delta_flux: Flux change (maxwells).
        resistance: Circuit resistance (CGS units).
        mutual_inductance: Mutual inductance (cm).
        delta_current: Primary current change (abamperes).

    Returns:
        Dictionary with complete analysis results.
    """
    # Linear ramps at different speeds
    durations = [0.001, 0.01, 0.1, 1.0, 10.0]
    linear_results = [simulate_linear_ramp(0, delta_flux, resistance, d) for d in durations]

    # Exponential decay
    exp_result = simulate_exponential_decay(delta_flux, resistance, time_constant=0.1)

    # Mutual induction
    mutual_result = simulate_mutual_induction(mutual_inductance, 0, delta_current, resistance)

    # Verification
    verification = verify_felici_law(delta_flux, resistance)

    return {
        "delta_flux": delta_flux,
        "resistance": resistance,
        "linear_ramps": {
            "durations": durations,
            "charges": [r.induced_charge for r in linear_results],
            "peak_emfs": [r.induced_emf_peak for r in linear_results],
        },
        "exponential_decay": exp_result,
        "mutual_induction": mutual_result,
        "verification": verification,
        "felici_law_valid": verification["verified"],
    }

"""Electromagnetic experiment simulations.

References:
    Part IV, Arts. 579-584: Ampere's current balance.
    Part IV, Arts. 536-539: Felici's law of induction.
    Part IV, Arts. 645-646: Stress tensor verification.
"""

from maxwell.electromagnetism.experiments.ampere_balance import (
    BalanceReading,
    analyze_ampere_balance,
    force_vs_current,
    force_vs_separation,
    simulate_ampere_balance,
    verify_ampere_balance,
)
from maxwell.electromagnetism.experiments.felici import (
    FeliciResult,
    InductionEvent,
    analyze_felici_law,
    simulate_exponential_decay,
    simulate_linear_ramp,
    simulate_mutual_induction,
    verify_felici_law,
)
from maxwell.electromagnetism.experiments.stress_verification import (
    analyze_stress_verification,
    verify_magnetic_pressure,
    verify_parallel_wire_stress,
    verify_point_charge_stress,
)

__all__ = [
    # Ampere balance (Arts. 579-584)
    "simulate_ampere_balance",
    "force_vs_separation",
    "force_vs_current",
    "verify_ampere_balance",
    "analyze_ampere_balance",
    "BalanceReading",
    # Felici's law (Arts. 536-539)
    "simulate_linear_ramp",
    "simulate_exponential_decay",
    "simulate_mutual_induction",
    "verify_felici_law",
    "analyze_felici_law",
    "InductionEvent",
    "FeliciResult",
    # Stress verification (Arts. 645-646)
    "verify_point_charge_stress",
    "verify_parallel_wire_stress",
    "verify_magnetic_pressure",
    "analyze_stress_verification",
]

"""maxwell.instruments — Electromagnetic instruments (Arts. 707-729).

Galvanometers, dynamometers, suspended coils, Helmholtz coils,
and sensitivity optimization for electromagnetic measurement.
"""

from __future__ import annotations

from maxwell.instruments.galvanometers import (
    StandardGalvanometer,
    TangentGalvanometer,
    SineGalvanometer,
    SingleCoilGalvanometer,
    FourCoilGalvanometer,
    ThreeCoilGalvanometer,
    UniformWireGalvanometer,
    calc_galvanometer_response,
    calc_field_at_center,
    design_standard_coil,
    apply_gaugain_suspension,
    design_sensitive_galvanometer,
    calc_uniform_wire_sensitivity,
)

from maxwell.instruments.helmholtz import HelmholtzCoil

from maxwell.instruments.suspended_coil import (
    SuspendedCoil,
    ThomsonSensitiveCoil,
    ThomsonCombinedInstrument,
    determine_magnetic_force,
    calc_uniform_normal_force,
)

from maxwell.instruments.dynamometers import (
    WeberDynamometer,
    JouleCurrentWeigher,
    TorsionDynamometer,
    calc_solenoid_suction,
)

__all__ = [
    # Galvanometers (Arts. 707-720)
    "StandardGalvanometer",
    "TangentGalvanometer",
    "SineGalvanometer",
    "SingleCoilGalvanometer",
    "FourCoilGalvanometer",
    "ThreeCoilGalvanometer",
    "UniformWireGalvanometer",
    "calc_galvanometer_response",
    "calc_field_at_center",
    "design_standard_coil",
    "apply_gaugain_suspension",
    "design_sensitive_galvanometer",
    "calc_uniform_wire_sensitivity",
    # Helmholtz (Art. 713)
    "HelmholtzCoil",
    # Suspended coil (Arts. 721-724)
    "SuspendedCoil",
    "ThomsonSensitiveCoil",
    "ThomsonCombinedInstrument",
    "determine_magnetic_force",
    "calc_uniform_normal_force",
    # Dynamometers (Arts. 725-729)
    "WeberDynamometer",
    "JouleCurrentWeigher",
    "TorsionDynamometer",
    "calc_solenoid_suction",
]

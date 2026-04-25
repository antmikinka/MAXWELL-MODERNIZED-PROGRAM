"""maxwell.electromagnetism.charges — Charge density equations (Arts. 612-613).

Package for Maxwell's charge density equations including volume and
surface charge distributions.
"""

from maxwell.electromagnetism.charges.volume import (
    VolumeCharge,
    calc_volume_charge_density,
    calc_charge_density_from_E,
    calc_total_charge_uniform,
    calc_charge_in_sphere,
    calc_field_from_charged_sphere,
    verify_gauss_law_volume,
    analyze_volume_charge,
)

from maxwell.electromagnetism.charges.surface import (
    SurfaceCharge,
    calc_surface_charge_density,
    calc_surface_charge_from_E,
    calc_conductor_surface_charge,
    calc_total_surface_charge,
    calc_field_near_charged_plane,
    calc_parallel_plate_capacitance,
    verify_surface_charge_boundary,
    analyze_surface_charge,
)

__all__ = [
    # Volume charge (Art. 612)
    "VolumeCharge",
    "calc_volume_charge_density",
    "calc_charge_density_from_E",
    "calc_total_charge_uniform",
    "calc_charge_in_sphere",
    "calc_field_from_charged_sphere",
    "verify_gauss_law_volume",
    "analyze_volume_charge",
    # Surface charge (Art. 613)
    "SurfaceCharge",
    "calc_surface_charge_density",
    "calc_surface_charge_from_E",
    "calc_conductor_surface_charge",
    "calc_total_surface_charge",
    "calc_field_near_charged_plane",
    "calc_parallel_plate_capacitance",
    "verify_surface_charge_boundary",
    "analyze_surface_charge",
]

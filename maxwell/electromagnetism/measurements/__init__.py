"""maxwell.electromagnetism.measurements — Electrical measurement instruments (Arts. 736-757).

Galvanometers, wattmeters, electrodynamometers, and absolute current
measurement methods from Maxwell's Part IV.

Modules:
    galvanometers_extended: Tangent, sine, Helmholtz galvanometers,
                           wattmeters, electrodynamometers, current
                           weighers, and Joule balances.
"""

from maxwell.electromagnetism.measurements.galvanometers_extended import (
    # Tangent galvanometer (Arts. 736-738)
    TangentGalvanometer,
    tangent_galvanometer,
    # Sine galvanometer (Art. 739)
    SineGalvanometer,
    sine_galvanometer,
    # Helmholtz galvanometer (Arts. 741-743)
    HelmholtzGalvanometer,
    helmholtz_galvanometer,
    # Wattmeter (Arts. 744, 746)
    wattmeter,
    # Electrodynamometer (Arts. 747-749)
    Electrodynamometer,
    electrodynamometer,
    # Current weigher (Arts. 751-754)
    current_weigher,
    # Joule balance (Arts. 755-757)
    joule_balance,
    # Complete analysis
    analyze_galvanometers,
)

__all__ = [
    # Tangent galvanometer (Arts. 736-738)
    "TangentGalvanometer",
    "tangent_galvanometer",
    # Sine galvanometer (Art. 739)
    "SineGalvanometer",
    "sine_galvanometer",
    # Helmholtz galvanometer (Arts. 741-743)
    "HelmholtzGalvanometer",
    "helmholtz_galvanometer",
    # Wattmeter (Arts. 744, 746)
    "wattmeter",
    # Electrodynamometer (Arts. 747-749)
    "Electrodynamometer",
    "electrodynamometer",
    # Current weigher (Arts. 751-754)
    "current_weigher",
    # Joule balance (Arts. 755-757)
    "joule_balance",
    # Complete analysis
    "analyze_galvanometers",
]

"""maxwell.experiments.ratio_v.condensers — Condenser methods (Arts. 771-774).

Experimental methods using condenser (capacitor) charge and discharge to
determine the ratio of ESU to EMU units:

* Weber and Kohlrausch's method (Art. 771)
* Thomson's electrometer method (Art. 772)
* Maxwell's combined method — see ``combined.py`` (Art. 773)
* Jenkin's method by intermittent condenser discharge (Art. 774)

Dimensional bookkeeping for capacitance (explicit)
==================================================

The two systems attach different dimensions to capacitance:

* ESU: ``C = q/V`` with ``[q] = M^1/2 L^3/2 T^-1`` and
  ``[V] = M^1/2 L^1/2 T^-1``  ->  ``[C_ESU] = L`` (the centimetre; an
  isolated sphere of radius ``a`` has ``C = a`` cm).
* EMU: ``[q] = M^1/2 L^1/2`` and ``[V] = M^1/2 L^3/2 T^-2``  ->
  ``[C_EMU] = L^-1 T^2`` (seconds squared per centimetre).

Their dimensional ratio is ``L^2 T^-2 = (velocity)^2``; numerically the
readings for one and the same condenser obey

    C_ESU / C_EMU = v^2          (v in cm/s)

so every capacitance-based reduction recovers v as a square root of a
ratio of capacitances, or as the velocity that converts one system into
the other (``C_EMU = C_ESU / v^2``).  Series/parallel composition
identities are linear/rational in C, so they hold in *either* system and
commute with the ``v^2`` conversion (see ``capacity_parallel`` /
``capacity_series`` / ``convert_capacity``).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite

PI = np.pi

#: Speed of light in CGS (cm/s) — single source of truth (D-33 guardrail).
C_CGS = CONST.C


@maxwell_cite(
    771,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="ESU capacitance of an isolated sphere from its geometry",
)
def sphere_capacity_esu(
    radius_cm: float, specific_inductive_capacity: float = 1.0
) -> float:
    """Capacitance of an isolated sphere in electrostatic measure.

    Art. 771 programme: the ESU capacitance is obtained by geometric
    measurement and calculation.  For an isolated sphere of radius ``a``
    in a medium of specific inductive capacity ``K``,

        C_ESU = K a        (centimetres)

    so ESU capacitance is literally a length.

    Args:
        radius_cm: Sphere radius (cm).
        specific_inductive_capacity: Dielectric constant K (>= 1; air ~ 1).

    Returns:
        Capacitance in ESU (cm).

    Raises:
        ValueError: If the radius or K is not positive.
    """
    if radius_cm <= 0:
        raise ValueError(f"radius must be positive, got {radius_cm}")
    if specific_inductive_capacity <= 0:
        raise ValueError(
            f"specific inductive capacity must be positive, "
            f"got {specific_inductive_capacity}"
        )
    return specific_inductive_capacity * radius_cm


@maxwell_cite(
    771,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Weber-Kohlrausch determination of v from a capacitance ratio",
)
def method_weber_kohlrausch(
    capacity_esu_cm: float,
    capacity_emu_s2_per_cm: float,
) -> float:
    """Weber and Kohlrausch's method (1856).

    The first measurement of the ratio v.  The capacitance of the same
    condenser is determined twice:

    * in ESU (cm) by geometric measurement and calculation,
    * in EMU (s^2/cm) by an electrical (discharge) measurement.

    Since ``C_ESU / C_EMU = v^2``,

        v = sqrt(C_ESU / C_EMU)        (cm/s)

    Dimensional check: ``L / (L^-1 T^2) = L^2 T^-2``; the square root
    carries ``L T^-1`` — a velocity.

    Args:
        capacity_esu_cm: Capacitance in electrostatic measure (cm).
        capacity_emu_s2_per_cm: Capacitance in electromagnetic measure
            (s^2/cm).

    Returns:
        The velocity v (cm/s).

    Raises:
        ValueError: If either capacitance is not positive.
    """
    if capacity_esu_cm <= 0 or capacity_emu_s2_per_cm <= 0:
        raise ValueError(
            f"capacitances must be positive, got esu={capacity_esu_cm}, "
            f"emu={capacity_emu_s2_per_cm}"
        )
    return float(np.sqrt(capacity_esu_cm / capacity_emu_s2_per_cm))


@dataclass
class CondenserMeasurement:
    """A single condenser-based measurement of the ratio v.

    Attributes:
        geometry_capacitance: Capacitance from dimensions (ESU, cm).
        measured_capacitance: Capacitance measured electrically
            (EMU, s^2/cm).
        method: Name of the experimental method.
    """

    geometry_capacitance: float  # ESU, cm
    measured_capacitance: float  # EMU, s^2/cm
    method: str

    @maxwell_cite(771, part=4, theory_class="standard_math")
    def calculate_v(self) -> float:
        """Calculate v = sqrt(C_ESU / C_EMU) (cm/s)."""
        return method_weber_kohlrausch(
            self.geometry_capacitance, self.measured_capacitance
        )

    @maxwell_cite(771, part=4, theory_class="standard_math")
    def deviation_from_c(self) -> float:
        """Percentage deviation of the recovered v from the speed of light."""
        v = self.calculate_v()
        return abs(v - C_CGS) / C_CGS * 100


@maxwell_cite(
    772,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Thomson's electrometer method: ESU potential vs EMU current x resistance",
)
def method_thomson_electrometer(
    voltage_esu_statvolt: float,
    current_emu_abampere: float,
    resistance_emu_abohm: float,
) -> float:
    """Thomson's method by electrometer (1860).

    The same potential difference is read twice:

    * ``V_ESU`` by an electrometer (statvolts),
    * ``V_EMU = I_EMU R_EMU`` from the circuit current (abamperes)
      through a known resistance (abohms), giving abvolts.

    Potential readings obey ``n_esu / n_emu = 1/v`` (p = -1), so

        v = V_EMU / V_ESU = I_EMU R_EMU / V_ESU        (cm/s)

    Dimensional check: ``[I_EMU R_EMU] = M^1/2 L^3/2 T^-2`` (abvolt) and
    ``[V_ESU] = M^1/2 L^1/2 T^-1`` (statvolt); the quotient has
    dimensions ``L T^-1``.

    Args:
        voltage_esu_statvolt: Electrometer reading (statvolts).
        current_emu_abampere: Circuit current (abamperes).
        resistance_emu_abohm: Circuit resistance (abohms).

    Returns:
        The velocity v (cm/s).

    Raises:
        ValueError: If the ESU voltage is not positive.
    """
    if voltage_esu_statvolt <= 0:
        raise ValueError(f"ESU voltage must be positive, got {voltage_esu_statvolt}")
    voltage_emu_abvolt = current_emu_abampere * resistance_emu_abohm
    return float(voltage_emu_abvolt / voltage_esu_statvolt)


@maxwell_cite(
    774,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Jenkin's method: intermittent condenser discharge current",
)
def method_jenkin(
    capacity_esu_cm: float,
    voltage_esu_statvolt: float,
    discharge_frequency_hz: float,
    measured_current_emu_abampere: float,
) -> float:
    """Jenkin's method by condenser capacity.

    A condenser is charged and discharged ``f`` times per second.  Each
    cycle transports the charge ``Q = C V``; the charge is known in ESU
    (statcoulombs) while the *average* current is measured in EMU
    (abamperes) by a galvanometer:

        I_ESU = C_ESU V_ESU f        (statamperes)
        I_EMU = I_ESU / v            (abamperes, since n_esu/n_emu = v)

    hence

        v = C_ESU V_ESU f / I_EMU        (cm/s)

    Dimensional check: the quotient is a ratio of two currents, whose
    unit sizes differ by one power of velocity, so the result carries
    ``L T^-1``.

    Args:
        capacity_esu_cm: Condenser capacity in ESU (cm).
        voltage_esu_statvolt: Charging voltage (statvolts).
        discharge_frequency_hz: Charge/discharge frequency (Hz).
        measured_current_emu_abampere: Average current (abamperes).

    Returns:
        The velocity v (cm/s).

    Raises:
        ValueError: If any input is not positive.
    """
    if (
        min(
            capacity_esu_cm,
            voltage_esu_statvolt,
            discharge_frequency_hz,
            measured_current_emu_abampere,
        )
        <= 0
    ):
        raise ValueError(
            "all inputs must be positive, got "
            f"C={capacity_esu_cm}, V={voltage_esu_statvolt}, "
            f"f={discharge_frequency_hz}, I={measured_current_emu_abampere}"
        )
    charge_per_cycle_esu = capacity_esu_cm * voltage_esu_statvolt
    current_esu_statampere = charge_per_cycle_esu * discharge_frequency_hz
    return float(current_esu_statampere / measured_current_emu_abampere)


@maxwell_cite(
    771,
    772,
    773,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Convert a capacitance reading between ESU and EMU via v^2",
)
def convert_capacity(capacity: float, direction: str, v: float | None = None) -> float:
    """Convert a capacitance reading between the two systems.

    Since ``C_ESU / C_EMU = v^2`` for the same condenser:

    * ``to_emu``: ``C_EMU = C_ESU / v^2``  (cm -> s^2/cm)
    * ``to_esu``: ``C_ESU = C_EMU v^2``    (s^2/cm -> cm)

    Args:
        capacity: The reading to convert (positive).
        direction: ``"to_emu"`` or ``"to_esu"``.
        v: Ratio of units (cm/s); defaults to ``CONST.C``.

    Returns:
        The converted reading.

    Raises:
        ValueError: If the capacity is not positive or direction unknown.
    """
    if capacity <= 0:
        raise ValueError(f"capacity must be positive, got {capacity}")
    if v is None:
        v = C_CGS
    if direction == "to_emu":
        return capacity / (v * v)
    if direction == "to_esu":
        return capacity * (v * v)
    raise ValueError(f"direction must be 'to_emu' or 'to_esu', got {direction!r}")


@maxwell_cite(
    771,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Parallel composition of condensers (valid in either unit system)",
)
def capacity_parallel(*capacities: float) -> float:
    """Total capacitance of condensers in parallel: ``C = sum(C_i)``.

    Valid in any consistent unit system (ESU cm or EMU s^2/cm); being
    linear, it commutes with the ``v^2`` system conversion.

    Args:
        *capacities: Individual capacitances (all positive, one system).

    Returns:
        Combined capacitance (same system as the inputs).

    Raises:
        ValueError: If fewer than one capacitance or any is non-positive.
    """
    if len(capacities) < 1:
        raise ValueError("at least one capacitance is required")
    if any(c <= 0 for c in capacities):
        raise ValueError(f"all capacitances must be positive, got {capacities}")
    return float(sum(capacities))


@maxwell_cite(
    771,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Series composition of condensers (valid in either unit system)",
)
def capacity_series(*capacities: float) -> float:
    """Total capacitance of condensers in series: ``1/C = sum(1/C_i)``.

    Valid in any consistent unit system; being rational-homogeneous, it
    commutes with the ``v^2`` system conversion.

    Args:
        *capacities: Individual capacitances (all positive, one system).

    Returns:
        Combined capacitance (same system as the inputs).

    Raises:
        ValueError: If fewer than one capacitance or any is non-positive.
    """
    if len(capacities) < 1:
        raise ValueError("at least one capacitance is required")
    if any(c <= 0 for c in capacities):
        raise ValueError(f"all capacitances must be positive, got {capacities}")
    return float(1.0 / sum(1.0 / c for c in capacities))

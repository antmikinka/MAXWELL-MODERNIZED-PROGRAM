"""maxwell.experiments.ratio_v.theory — Unit ratio theory (Arts. 768-770, 780).

Theoretical foundation of Part IV Chapter XIX: the ratio of electrostatic
to electromagnetic units is a velocity, experimentally determined to be of
the order of the speed of light.

Dimensional bookkeeping (explicit, per the Chapter XIX programme)
==================================================================

The two CGS systems define electrical units from different mechanical
force laws:

* ESU from Coulomb's law ``F = q1 q2 / r^2``  ->  [q_ESU] = M^1/2 L^3/2 T^-1
* EMU from Ampere's force law between current elements
  ``F ~ I1 I2 dl1 dl2 / r^2``  ->  [I_EMU] = M^1/2 L^1/2 T^-1

whence (see ``derive_unit_ratio_dimension``):

    quantity      [.]_ESU                [.]_EMU              ratio dims
    charge        M^1/2 L^3/2 T^-1       M^1/2 L^1/2          L T^-1
    current       M^1/2 L^3/2 T^-2       M^1/2 L^1/2 T^-1     L T^-1
    potential     M^1/2 L^1/2 T^-1       M^1/2 L^3/2 T^-2     L^-1 T
    resistance    L^-1 T (s/cm)          L T^-1 (cm/s)        L^-2 T^2
    capacitance   L (cm)                 L^-1 T^2 (s^2/cm)    L^2 T^-2
    inductance    L^-1 T^2               L (cm)               L^-2 T^2

Numeric-value convention (Maxwell, Treatise Arts. 768-770): for the *same
physical quantity* let ``n_esu`` and ``n_emu`` be the measured numbers in
ESU and EMU.  Then

    n_esu / n_emu = v**p

where ``v`` is a velocity (dimensionally ``L T^-1``, numerically
~3.1e10 cm/s) and ``p`` is the power of velocity in the dimensional ratio
above:

    p = +1  charge, current        n_esu = v   * n_emu
    p = -1  potential              n_esu = n_emu / v
    p = +2  capacitance            n_esu = v^2 * n_emu   (cm vs s^2/cm)
    p = -2  resistance, inductance n_esu = n_emu / v^2

Because ``n_esu * unit_esu = n_emu * unit_emu`` for one and the same
physical quantity, the numeric ratio equals the *unit-size* ratio
``unit_emu / unit_esu``; e.g. one abcoulomb contains v statcoulombs, one
statohm contains v^2 abohms, and one centimetre of ESU capacitance equals
v^2 units of EMU capacitance.  ``v`` therefore carries dimensions cm/s in
every reduction of this package.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite

PI = np.pi

#: Speed of light in CGS (cm/s) — single source of truth (D-33 guardrail).
C_CGS = CONST.C

#: Historical anchor for the ratio v (cm/s).
#: Provenance: Treatise Arts. 775-778 report determinations of
#: v ~ 3.1 x 10^10 cm/s; the anchor value 3.107 x 10^10 cm/s is the
#: Weber-Kohlrausch (1856) result (310,740,000 m/s) quoted in the chapter
#: (Stage 4 reference store entry ``art768_weber_kohlrausch_v``,
#: EMPIRICAL tolerance class, rel_tol = 5e-2).
V_HISTORICAL = 3.107e10
V_HISTORICAL_TOL = 5e-2

#: Numeric power p of v in the ratio n_ESU/n_EMU = v^p for each quantity
#: (hand-derived from the dimensional table in the module docstring).
UNIT_RATIO_POWERS: dict[str, int] = {
    "charge": 1,
    "current": 1,
    "potential": -1,
    "resistance": -2,
    "capacitance": 2,
    "inductance": -2,
}


def _dims_to_string(m2: int, l2: int, t2: int) -> str:
    """Format doubled (M, L, T) exponents as Maxwell's M^a L^b T^c string."""
    parts = []
    for name, e2 in (("M", m2), ("L", l2), ("T", t2)):
        if e2 == 0:
            continue
        if e2 % 2 == 0:
            e = e2 // 2
            parts.append(name if e == 1 else f"{name}^{e}")
        else:
            parts.append(f"{name}^({e2}/2)")
    return " ".join(parts) if parts else "dimensionless"


@maxwell_cite(
    768,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="maxwell_original",
    description="Statement and significance of the ratio-of-units investigation",
)
def motivate_ratio_investigation() -> dict[str, object]:
    """State the nature and importance of the ratio investigation.

    Art. 768: determining the ratio between the electrostatic and the
    electromagnetic units connects the two systems of electrical
    measurement; the result is a velocity comparable with the speed of
    light, which is the experimental root of the electromagnetic theory
    of light.

    Returns:
        Motivation dictionary including the quantitative historical
        anchor (value + tolerance + provenance) so that downstream
        reductions can be pinned to the reported value.
    """
    return {
        "significance": "The ratio v between ESU and EMU units is "
        "found to be a velocity of the same order as "
        "the speed of light",
        "implication": "This suggests that light itself may be an "
        "electromagnetic phenomenon",
        "method": "Compare the same physical quantity (charge, "
        "current, resistance, capacitance) measured in both "
        "systems; the numeric ratios are powers of one velocity v",
        "reported_v_cm_s": V_HISTORICAL,
        "reported_v_rel_tol": V_HISTORICAL_TOL,
        "provenance": "Treatise Arts. 775-778 reported value "
        "~3.1 x 10^10 cm/s; anchor 3.107 x 10^10 cm/s is the "
        "Weber-Kohlrausch (1856) result quoted in the chapter",
    }


@maxwell_cite(
    769,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="maxwell_original",
    description="Derive the dimensions of the ESU/EMU ratio from the two force laws",
)
def derive_unit_ratio_dimension(quantity: str = "charge") -> dict[str, object]:
    """Derive the dimensions of the ESU/EMU ratio of a quantity.

    Art. 769: the ratio of the electrostatic to the electromagnetic unit
    is *derived here from the defining force laws*, not returned as a
    constant (Stage 3 defect D-19 closure):

    * ESU charge from Coulomb: ``[q^2] = [F][L^2] = M L^3 T^-2``
      -> ``[q_ESU] = M^1/2 L^3/2 T^-1``.
    * EMU current from Ampere's force between current elements:
      ``[I^2] = [F][L^2]/[L^2] = M L T^-2``
      -> ``[I_EMU] = M^1/2 L^1/2 T^-1``, so ``[q_EMU] = M^1/2 L^1/2``.

    The remaining quantities follow from ``current = charge/time``,
    ``potential = energy/charge``, ``resistance = potential/current``,
    ``capacitance = charge/potential``, ``inductance = potential*time/current``.
    All exponents are carried as *doubled integers* so that the
    half-integer CGS dimensions are exact.

    Args:
        quantity: One of ``UNIT_RATIO_POWERS`` (charge, current,
            potential, resistance, capacitance, inductance).

    Returns:
        Dictionary with the derived ESU/EMU dimensional formulae, the
        dimensional formula of their ratio, the integer velocity power
        ``p`` such that ``[Q]_ESU/[Q]_EMU = (L T^-1)^p``, and a boolean
        ``is_velocity_power`` (True when the ratio is a pure power of
        velocity, i.e. zero mass exponent and ``L``-exponent = minus
        ``T``-exponent).

    Raises:
        KeyError: If the quantity is unknown.
    """
    if quantity not in UNIT_RATIO_POWERS:
        raise KeyError(
            f"Unknown quantity: {quantity!r}. "
            f"Available: {sorted(UNIT_RATIO_POWERS)}"
        )

    # Doubled exponent vectors (m2, l2, t2): exact integer arithmetic.
    force = (2, 2, -4)  # F = M L T^-2
    length = (0, 2, 0)
    time = (0, 0, 2)
    energy = (2, 4, -4)  # M L^2 T^-2

    def add(a, b):
        return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

    def sub(a, b):
        return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

    def half(a):
        return (a[0] // 2, a[1] // 2, a[2] // 2)

    # ESU charge: [q^2] = [F][L^2]  (Coulomb F = q1 q2 / r^2)
    q_esu = half(add(force, add(length, length)))  # (1, 3, -2)
    # EMU current: [I^2] = [F][L^2]/[L^2]  (Ampere element force)
    i_emu = half(sub(add(force, add(length, length)), add(length, length)))
    q_emu = add(i_emu, time)  # (1, 1, 0)

    # ESU system
    i_esu = sub(q_esu, time)  # charge / time
    pot_esu = sub(energy, q_esu)  # energy / charge
    r_esu = sub(pot_esu, i_esu)  # potential / current
    c_esu = sub(q_esu, pot_esu)  # charge / potential
    l_esu = sub(add(pot_esu, time), i_esu)  # potential * time / current

    # EMU system
    pot_emu = sub(energy, q_emu)  # energy / charge
    r_emu = sub(pot_emu, i_emu)  # potential / current
    c_emu = sub(q_emu, pot_emu)  # charge / potential
    l_emu = sub(add(pot_emu, time), i_emu)  # potential * time / current

    table = {
        "charge": (q_esu, q_emu),
        "current": (i_esu, i_emu),
        "potential": (pot_esu, pot_emu),
        "resistance": (r_esu, r_emu),
        "capacitance": (c_esu, c_emu),
        "inductance": (l_esu, l_emu),
    }
    esu_dims, emu_dims = table[quantity]
    ratio_dims = sub(esu_dims, emu_dims)

    # Pure power of velocity iff mass-free and l2 == -t2 (doubled).
    is_velocity_power = ratio_dims[0] == 0 and ratio_dims[1] == -ratio_dims[2]
    velocity_power = ratio_dims[1] // 2 if is_velocity_power else None

    derivation = [
        "ESU: F = q1 q2 / r^2  =>  [q_ESU]^2 = [F][L]^2 = M L^3 T^-2",
        "EMU: F ~ I1 I2 dl1 dl2 / r^2  =>  [I_EMU]^2 = M L T^-2",
        f"[{quantity}]_ESU = {_dims_to_string(*esu_dims)}",
        f"[{quantity}]_EMU = {_dims_to_string(*emu_dims)}",
        f"ratio dimensions = {_dims_to_string(*ratio_dims)}",
    ]
    if is_velocity_power:
        derivation.append(
            f"ratio = (L T^-1)^{velocity_power}: a power of a velocity"
        )

    return {
        "quantity": quantity,
        "esu_dimensions": _dims_to_string(*esu_dims),
        "emu_dimensions": _dims_to_string(*emu_dims),
        "ratio_dimensions": _dims_to_string(*ratio_dims),
        "ratio_exponents": (ratio_dims[0] // 2, ratio_dims[1] / 2, ratio_dims[2] / 2),
        "velocity_power": velocity_power,
        "is_velocity_power": is_velocity_power,
        "numeric_power": UNIT_RATIO_POWERS[quantity],
        "derivation": derivation,
    }


@maxwell_cite(
    769,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="maxwell_original",
    description="The ESU/EMU ratio has the dimensions of a velocity (derived)",
)
def prove_ratio_is_velocity(quantity: str = "charge") -> dict[str, object]:
    """Prove that the ratio of units is dimensionally a velocity.

    Art. 769: ``[q_ESU]/[q_EMU] = L T^-1`` (and analogues for the other
    quantities) is *derived* from the defining force laws by
    :func:`derive_unit_ratio_dimension`; no measured value is returned
    here (the measured value lives in :func:`historical_v_anchor`,
    per the D-19 separation of derivation and measurement).

    Args:
        quantity: Quantity whose unit ratio is analysed (default charge).

    Returns:
        The derivation dictionary, which is guaranteed to carry
        ``is_velocity_power == True`` for every supported quantity.

    Raises:
        KeyError: If the quantity is unknown.
    """
    result = derive_unit_ratio_dimension(quantity)
    if not result["is_velocity_power"]:
        raise AssertionError(  # pragma: no cover - guarded by table
            f"ratio of units for {quantity!r} is not a power of velocity"
        )
    return result


@maxwell_cite(
    768,
    775,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Experimental anchor value for the ratio v with provenance",
)
def historical_v_anchor() -> dict[str, object]:
    """Return the experimental anchor for v (separate from the derivation).

    The derivation (Art. 769) fixes only the *dimensions* of the ratio;
    the *value* is an experimental result.  This function carries the
    anchor used to validate the Chapter XIX reductions:

    Returns:
        Dictionary with ``v_cm_s`` (= 3.107 x 10^10), ``rel_tol`` (= 5e-2,
        the EMPIRICAL tolerance class of the Stage 4 testing strategy)
        and ``provenance``.
    """
    return {
        "v_cm_s": V_HISTORICAL,
        "rel_tol": V_HISTORICAL_TOL,
        "unit": "cm/s",
        "provenance": "Treatise Arts. 775-778 reported value "
        "~3.1 x 10^10 cm/s; anchor 3.107 x 10^10 cm/s is the "
        "Weber-Kohlrausch (1856) result quoted in the chapter",
    }


@maxwell_cite(
    770,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Convection current of a rotating charged ring and its magnetic field",
)
def calc_convection_current(
    charge_esu: float,
    radius_cm: float,
    angular_velocity: float,
    v: float | None = None,
) -> dict[str, float]:
    """Convection current of charge in motion (rotating charged ring).

    Art. 770: a moving charged body is an electric current.  For a ring
    carrying total charge ``q`` (statcoulombs) rotating with angular
    velocity ``omega`` (rad/s), one revolution of period ``T = 2 pi /
    omega`` transports the whole charge past any section, so

        I_ESU = q omega / (2 pi)            (statamperes)
        I_EMU = I_ESU / v = q omega / (2 pi v)   (abamperes)

    where ``v`` is the ratio of units (the ESU charge converts to EMU by
    division by v since n_esu/n_emu = v for charge).  The ring's magnetic
    field at its centre (EMU, gauss) is ``H = 2 pi I_EMU / a``, i.e.

        H = q omega / (v a)

    which is the basis of the convection method of measuring v (Rowland's
    programme): measuring H gives ``v = q omega / (a H)``.

    Args:
        charge_esu: Total charge on the ring (statcoulombs).
        radius_cm: Radius of the ring (cm).
        angular_velocity: Angular velocity (rad/s).
        v: Ratio of units used for the ESU->EMU conversion (cm/s).
            Defaults to ``CONST.C`` (prediction mode).

    Returns:
        Dictionary with period (s), current_esu (statamperes),
        current_emu (abamperes), and field_at_center (gauss).

    Raises:
        ValueError: If the radius is not positive.
    """
    if radius_cm <= 0:
        raise ValueError(f"radius must be positive, got {radius_cm}")
    if v is None:
        v = C_CGS
    period = 2.0 * PI / angular_velocity
    current_esu = charge_esu / period
    current_emu = current_esu / v
    field_at_center = 2.0 * PI * current_emu / radius_cm
    return {
        "period_s": period,
        "current_esu": current_esu,
        "current_emu": current_emu,
        "field_at_center": field_at_center,
        "v_used": v,
    }


@maxwell_cite(
    770,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Ratio of units from the magnetic field of a convection current",
)
def v_from_convection_field(
    charge_esu: float,
    radius_cm: float,
    angular_velocity: float,
    field_gauss: float,
) -> float:
    """Invert the convection-current field to determine v.

    Art. 770: with ``H = q omega / (v a)`` the measured centre field of
    the rotating charged ring gives

        v = q omega / (a H)        (cm/s)

    Args:
        charge_esu: Charge on the ring (statcoulombs).
        radius_cm: Ring radius (cm).
        angular_velocity: Angular velocity (rad/s).
        field_gauss: Measured centre field (gauss, EMU).

    Returns:
        The ratio v (cm/s).

    Raises:
        ZeroDivisionError: If the measured field is zero.
    """
    return charge_esu * angular_velocity / (radius_cm * field_gauss)


@maxwell_cite(
    780,
    part=4,
    chapter="Comparison of Electrostatic and Electromagnetic Units",
    theory_class="standard_math",
    description="Ratio of units from the same resistance measured in both systems",
)
def compare_resistance_systems(
    resistance_esu: float,
    resistance_emu: float,
) -> dict[str, float]:
    """Compare ESU and EMU values of the same resistance.

    Art. 780: for one and the same conductor the numeric readings obey
    ``n_esu / n_emu = 1/v^2`` (resistance power p = -2: the statohm is a
    huge unit, ``1 statohm = v^2 abohm``), hence

        v = sqrt(R_EMU / R_ESU)        (cm/s)

    Dimensional check: R_EMU has dimensions L T^-1 (cm/s) and R_ESU has
    L^-1 T (s/cm), so ``R_EMU / R_ESU`` has dimensions L^2 T^-2 and its
    square root is a velocity.

    Args:
        resistance_esu: The conductor's resistance in statohms (s/cm).
        resistance_emu: The same resistance in abohms (cm/s).

    Returns:
        Dictionary with the two readings, their ratio, the calculated
        v (cm/s) and its deviation from the accepted speed of light.

    Raises:
        ValueError: If either resistance is non-positive.
    """
    if resistance_esu <= 0 or resistance_emu <= 0:
        raise ValueError(
            f"resistances must be positive, got esu={resistance_esu}, "
            f"emu={resistance_emu}"
        )
    ratio = resistance_emu / resistance_esu
    calculated_v = float(np.sqrt(ratio))
    return {
        "resistance_esu": resistance_esu,
        "resistance_emu": resistance_emu,
        "ratio_emu_esu": ratio,
        "calculated_v": calculated_v,
        "speed_of_light": C_CGS,
        "deviation_pct": abs(calculated_v - C_CGS) / C_CGS * 100,
    }


@dataclass
class UnitRatioExperiment:
    """Framework for measuring the ESU/EMU ratio of any quantity.

    Base class for all experimental methods (Weber-Kohlrausch, Thomson,
    Maxwell's combined method, etc.).  The two readings are the *numeric
    values* of one and the same physical quantity in ESU and EMU.

    The power ``p`` with ``n_esu/n_emu = v^p`` depends on the quantity
    (see ``UNIT_RATIO_POWERS``), so the velocity is recovered as

        v = (n_esu / n_emu)^(1/p)

    e.g. directly for charge (p = 1), by square root for capacitance
    (p = 2), by reciprocal square root for resistance (p = -2).
    """

    measured_quantity_esu: float
    measured_quantity_emu: float
    quantity_name: str
    quantity_kind: str = "charge"

    @maxwell_cite(769, part=4, theory_class="standard_math")
    def calculate_ratio(self) -> float:
        """Calculate the velocity v = (n_ESU / n_EMU)^(1/p) in cm/s."""
        if self.measured_quantity_emu == 0:
            return float("inf")
        p = UNIT_RATIO_POWERS[self.quantity_kind]
        ratio = abs(self.measured_quantity_esu / self.measured_quantity_emu)
        return float(ratio ** (1.0 / p))

    @maxwell_cite(769, part=4, theory_class="standard_math")
    def verify_equals_c(self, tolerance: float = 0.05) -> bool:
        """Verify that the recovered velocity equals the speed of light.

        Args:
            tolerance: Acceptable fractional deviation (default 5%).

        Returns:
            True if v is within tolerance of c.
        """
        v = self.calculate_ratio()
        return abs(v - C_CGS) / C_CGS < tolerance

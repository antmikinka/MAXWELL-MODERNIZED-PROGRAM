"""maxwell.electromagnetism.coil_comparison — Comparison of Coils (Arts. 752-757).

Genuine implementation of Part IV, Ch XVII "Comparison of Coils"
(Treatise 3rd edition, Vol. II, printed pp. 392-398; PDF pp. 419-425).
Implements the Stage-3 register's remedy for defect D-17 (the former
anachronistic ``joule_balance`` citation of 755-757 was re-mapped in
Wave 6; this package supplies the real coil-comparison methods).

Placement rationale: Ch XVII sits between the instrument/observation
chapters (XV-XVI, held by ``electromagnetism/measurements/``) and the
absolute-resistance chapters (XVIII-XIX, held by ``calibration/`` and
``experiments/ratio_v/``).  It is a self-contained comparison-methods
cluster, so it gets its own subpackage of ``electromagnetism`` rather
than extending a file owned by a concurrent work package.

Unit convention: pure CGS-EMU, as the Treatise uses throughout Part IV
("currents being estimated in electromagnetic units", Art. 846):

    G1    magnetic force at a coil's centre per unit current
          (gauss per abampere; a single circular turn of radius a
          gives G1 = 2 pi / a)
    g1    magnetic moment of a coil per unit current (cm^2)
    M, L  coefficients of mutual / self-induction (centimetres)
    R     resistance (abohm)

No factor of c appears anywhere in this module; inductance has the
dimension of length and the force/field constants carry no 1/c.

References:
    Part IV, Ch XVII, Arts. 752-757: Comparison of Coils.
    Part IV, Arts. 700, 703-704: coil-constant expansions and the
    elliptic-integral formula for the mutual induction of two coaxial
    circles (evaluated here via ``maxwell.math.elliptic_integrals``,
    the Landen/AGM machinery of Arts. 696-705).
"""

from __future__ import annotations

from maxwell.electromagnetism.coil_comparison.coil_comparison import (
    axis_field_series,
    calc_comparison_advantage,
    calc_g3_correction,
    calc_standard_coil_g1,
    compare_mutual_by_null,
    compare_self_inductions,
    deflection_residual,
    determine_g1_by_null,
    determine_g1_by_shunt,
    determine_small_coil_moment,
    full_null_residual,
    integral_induction_current,
    self_induction_from_mutual,
    self_induction_from_mutual_with_w,
    self_induction_ratio_from_bridge,
    standard_pair_mutual_inductance,
    steady_balance_residual,
)

__all__ = [
    # Art. 752 — standard coil and the case for electrical comparison
    "calc_standard_coil_g1",
    "calc_comparison_advantage",
    # Art. 753 — determination of G1
    "determine_g1_by_null",
    "determine_g1_by_shunt",
    "deflection_residual",
    # Art. 754 — determination of g1
    "axis_field_series",
    "calc_g3_correction",
    "determine_small_coil_moment",
    # Art. 755 — comparison of coefficients of mutual induction
    "standard_pair_mutual_inductance",
    "integral_induction_current",
    "compare_mutual_by_null",
    "full_null_residual",
    # Art. 756 — self-induction compared with mutual induction
    "self_induction_from_mutual",
    "self_induction_from_mutual_with_w",
    "steady_balance_residual",
    # Art. 757 — comparison of two self-inductions
    "compare_self_inductions",
    "self_induction_ratio_from_bridge",
]

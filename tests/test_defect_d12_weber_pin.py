"""Defect D-12 (Stage-2, severity S2): Weber force coefficient pin.

Adjudication (CIRCUITUS, Wave 7, 2026-08-21), from the printed 3rd-edition
text of the Treatise (Vol. II, Part IV, Ch. XXIII "Action at a Distance",
pp. 482-484):

* Art. 850, eq. (19) gives Weber's repulsion of two electrical particles as

      F = (e e' / r^2) [ 1 + (1/c^2) ( r d^2r/dt^2 - (1/2) (dr/dt)^2 ) ],

  i.e. coefficient 1/2 on the r_dot^2 term and coefficient 1 on the
  r*r_ddot term, with c the ESU/EMU ratio (= speed of light, Art. 849).
* Art. 853, eq. (20) gives the Weber potential
  psi = (e e'/r) [ 1 - (1/(2 c^2)) (dr/dt)^2 ], whose -d/dr (with the
  chain rule d(r_dot^2)/dr = 2 r_dot r_ddot) reproduces exactly that force.
* Weber's original 1846 form (Elektrodynamische Maassbestimmungen) uses
  his own constant c_W:  F = (ee'/r^2)[1 - r_dot^2/c_W^2 + 2 r r_ddot/c_W^2],
  and the Treatise (Arts. 848/855) records c_W = sqrt(2) c; substituting
  gives the 1/2 and 1 coefficients above.

Both implementation sites (maxwell/molecular/webers_theory.py WeberForce
and maxwell/theories/failure_modes.py _weber_force) use the adjudicated
(1/2, 1) convention with c = CONST.C.  This file pins that convention
numerically: the coefficients are EXTRACTED from computed forces (never
read from the code) and compared against the store's goldens, and the two
files are checked against each other and against Weber's original c_W form.
"""

from __future__ import annotations

import pytest

from maxwell.config.constants import CONST
from maxwell.molecular.webers_theory import WeberForce, weber_constant
from maxwell.theories.failure_modes import _weber_force

from articles import ref_value, tolerance_of

C = CONST.C

# Golden kinematics of the store's Art. 841 Coulomb case.
Q1, Q2, R_SEP = 2.0, 3.0, 4.0
F_COULOMB = Q1 * Q2 / R_SEP**2  # 0.375, the Art. 841 golden


@pytest.mark.article(845)
def test_d12_velocity_squared_coefficient_pin():
    """D-12 pin, r_dot^2 term only (r_ddot = 0): the extracted
    coefficient of (r_dot/c)^2 must equal the adjudicated 1/2.

    kappa = (F_Coulomb - F) c^2 / (F_Coulomb r_dot^2); any other
    convention (e.g. coefficient 1, or c_W = sqrt(2) c used WITH the
    1/2) would shift kappa away from 1/2 and fail this pin.
    """
    r_dot = 0.1 * C
    force = WeberForce(
        q1=Q1, q2=Q2, separation=R_SEP,
        relative_velocity=r_dot, relative_acceleration=0.0,
    ).force()
    kappa = (F_COULOMB - force) * C**2 / (F_COULOMB * r_dot**2)
    assert kappa == pytest.approx(
        ref_value(845, "weber_velocity_squared_coefficient"),
        **tolerance_of(845, "weber_velocity_squared_coefficient"),
    )


@pytest.mark.article(845)
def test_d12_acceleration_coefficient_pin():
    """Companion pin, r*r_ddot term only (r_dot = 0): the extracted
    coefficient of r*r_ddot/c^2 must equal the adjudicated 1."""
    r_ddot = 1.0e16
    force = WeberForce(
        q1=Q1, q2=Q2, separation=R_SEP,
        relative_velocity=0.0, relative_acceleration=r_ddot,
    ).force()
    kappa_a = (force - F_COULOMB) * C**2 / (F_COULOMB * R_SEP * r_ddot)
    assert kappa_a == pytest.approx(
        ref_value(845, "weber_acceleration_coefficient"),
        **tolerance_of(845, "weber_acceleration_coefficient"),
    )


@pytest.mark.article(845)
def test_d12_both_implementation_sites_one_convention():
    """D-12 requires ONE convention across the codebase: the force from
    maxwell.theories.failure_modes must equal the force from
    maxwell.molecular.webers_theory at the same kinematics."""
    kinematics = [
        (0.1 * C, 0.0),
        (0.0, 1.0e16),
        (0.05 * C, -2.0e16),
    ]
    for r_dot, r_ddot in kinematics:
        molecular = WeberForce(
            q1=Q1, q2=Q2, separation=R_SEP,
            relative_velocity=r_dot, relative_acceleration=r_ddot,
        ).force()
        failure = _weber_force(R_SEP, r_dot, r_ddot, Q1, Q2)
        assert failure == pytest.approx(molecular, rel=1e-14)


@pytest.mark.article(845)
def test_d12_equivalence_with_weber_1846_c_w_form():
    """The adjudicated (1/2, 1, c) convention must equal Weber's original
    1846 form with c_W = sqrt(2) c, evaluated independently."""
    c_w = weber_constant()
    r_dot, r_ddot = 0.05 * C, -2.0e16
    original_form = (Q1 * Q2 / R_SEP**2) * (
        1.0 - r_dot**2 / c_w**2 + 2.0 * R_SEP * r_ddot / c_w**2
    )
    adjudicated = WeberForce(
        q1=Q1, q2=Q2, separation=R_SEP,
        relative_velocity=r_dot, relative_acceleration=r_ddot,
    ).force()
    assert original_form == pytest.approx(adjudicated, rel=1e-13)

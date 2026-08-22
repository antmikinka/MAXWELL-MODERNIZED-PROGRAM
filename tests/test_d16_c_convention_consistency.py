"""D-16 cross-module c-convention consistency tests.

Stage-3 defect D-16 (S2): ``maxwell/instruments/galvanometers.py`` computed
the centre field of a circular coil as 2.pi.n.I/R (CGS-EMU, no factor of c,
current in abamperes) while ``maxwell/electromagnetism/components/
circular_coils.py`` computed the same physical field as
2.pi.n.I*a^2/(c*(a^2+z^2)^(3/2)) (explicit c, current in statamperes).
For identical numeric inputs the two modules disagreed by a factor of
CONST.C ~ 3e10.

Resolution (this wave): the repo convention is Gaussian CGS with explicit c
via ``maxwell.config.constants.CONST.C`` (the dominant family per Stage-3
section 4.1). ``galvanometers.py`` has been converted: all coil constants
and fields carry CONST.C in the denominator and currents are statamperes.

These tests pin the direct agreement of the two modules for the same
physical coil, and both against an independent statampere Biot-Savart
vector quadrature of the loop:

    dB = (I/c) dl x r_hat / r^2  (Gaussian law; c = CONST.C).

Provenance: Stage-3 defect register D-16 (docs/LAST200_STAGE3_QUALITY_REVIEW.md);
repo-convention decision per Stage-5 orchestration (Wave 7, INSTRUMENTUM).
"""

from __future__ import annotations

import numpy as np
import pytest

from maxwell.config.constants import CONST
from maxwell.electromagnetism.components.circular_coils import calc_coil_on_axis
from maxwell.instruments.galvanometers import (
    StandardGalvanometer,
    apply_gaugain_suspension,
    calc_field_at_center,
)


def _biot_savart_center_field_stat(
    current_stat: float,
    n_turns: int,
    radius: float,
    n_segments: int = 20000,
) -> float:
    """Independent oracle: direct vector line integral around the loop.

    Discretizes the circular loop into ``n_segments`` straight chords and
    sums dB = (I/c) dl x r_hat / r^2 at the centre with numpy cross
    products. By symmetry only the axial component survives; the chord
    discretization error is O((2*pi/N)^2) ~ 8e-9 at N = 20000. The
    quadrature shares no code or closed form with either module under
    test (it is the defining integral, not 2*pi*n*I/(c*R)).
    """
    phi = np.linspace(0.0, 2.0 * np.pi, n_segments + 1)
    pts = radius * np.stack([np.cos(phi), np.sin(phi), 0.0 * phi], axis=-1)
    dl = np.diff(pts, axis=0)  # (N, 3) chord vectors
    mid = 0.5 * (pts[:-1] + pts[1:])  # (N, 3) segment midpoints
    r_vec = -mid  # from wire element to the centre (origin)
    r = np.linalg.norm(r_vec, axis=1, keepdims=True)
    db = (current_stat / CONST.C) * np.cross(dl, r_vec) / r**3
    return float(n_turns * db[:, 2].sum())


class TestD16DirectModuleAgreement:
    """The two modules must agree numerically for the same physical coil."""

    @pytest.mark.parametrize(
        ("current", "n_turns", "radius"),
        [
            (1.0e-3, 100, 10.0),
            (2.5e-4, 250, 15.0),
            (7.0e-5, 4, 2.5),
            (1.0, 1, 1.0),
        ],
    )
    def test_centre_field_agrees_with_circular_coils(
        self, current, n_turns, radius
    ) -> None:
        """calc_field_at_center == calc_coil_on_axis(z=0) to machine precision.

        Both are closed forms of the same Gaussian integral
        B = 2.pi.n.I/(c.R); any deviation beyond roundoff means one of the
        modules has reverted to the EMU (no-c) convention.
        """
        g_field = calc_field_at_center(current, n_turns, radius)
        cc_field = calc_coil_on_axis(current, radius, 0.0, n_turns=n_turns)
        assert g_field == pytest.approx(cc_field, rel=1e-13, abs=0.0), (
            f"D-16 regression: galvanometers gives {g_field}, circular_coils "
            f"gives {cc_field}; ratio {g_field / cc_field} (should be 1, not c)"
        )

    @pytest.mark.parametrize(
        ("current", "n_turns", "radius"),
        [(1.0e-3, 100, 10.0), (3.0e-4, 60, 8.0)],
    )
    def test_gaugain_axial_field_agrees_with_circular_coils(
        self, current, n_turns, radius
    ) -> None:
        """apply_gaugain_suspension == calc_coil_on_axis at z = R/2.

        The Gaugain eccentric point (Art. 712) sits at half the radius;
        the axial-field formulas of the two modules must coincide there
        as well, not only at the centre.
        """
        z = 0.5 * radius
        g_field = apply_gaugain_suspension(radius, z, n_turns, current)
        cc_field = calc_coil_on_axis(current, radius, z, n_turns=n_turns)
        assert g_field == pytest.approx(cc_field, rel=1e-13, abs=0.0)


class TestD16IndependentOracle:
    """Both modules must match the defining Gaussian Biot-Savart integral."""

    def test_both_modules_match_vector_quadrature(self) -> None:
        """Centre field vs direct dB = (I/c) dl x r_hat / r^2 summation.

        Tolerance rel 1e-6 covers the O(N^-2) chord discretization error
        (N = 20000 gives ~8e-9, so the bound is ~100x loose, still far
        below the factor-c ~ 3e10 that D-16 produced).
        Provenance: Gaussian Biot-Savart law, direct quadrature (this file);
        agreement at this tolerance excludes both the EMU-no-c form and any
        missing/extra factor of c.
        """
        current, n_turns, radius = 5.0e-3, 120, 12.0
        oracle = _biot_savart_center_field_stat(current, n_turns, radius)

        g_field = calc_field_at_center(current, n_turns, radius)
        cc_field = calc_coil_on_axis(current, radius, 0.0, n_turns=n_turns)

        assert g_field == pytest.approx(oracle, rel=1e-6), (
            "galvanometers.py disagrees with the Gaussian Biot-Savart integral"
        )
        assert cc_field == pytest.approx(oracle, rel=1e-6), (
            "circular_coils.py disagrees with the Gaussian Biot-Savart integral"
        )

    def test_standard_galvanometer_constant_is_gaussian(self) -> None:
        """G = 2.pi.n/(c.R): galvanometer constant in gauss per statampere.

        Recomputed here from first principles (CONST.C from the repo's
        constants module — no bare literals per R7) and compared at machine
        precision; this is the quantity every tangent-law measurement in
        Arts. 707-720 multiplies the current by.
        """
        n_turns, radius = 100, 10.0
        expected = 2.0 * np.pi * n_turns / (CONST.C * radius)
        galvanometer = StandardGalvanometer(
            n_turns=n_turns,
            mean_radius=radius,
            wire_radius=0.05,
            coil_depth=0.5,
        )
        assert galvanometer.coil_constant == pytest.approx(expected, rel=1e-13)

    def test_ratio_is_c_not_unity_if_conventions_mixed(self) -> None:
        """Guard orientation: an EMU-style no-c field is larger by exactly c.

        This documents the discriminating power of the test: the former
        buggy value 2.pi.n.I/R equals CONST.C times the correct Gaussian
        value. The assert computes the ratio from the two closed forms
        (nothing hardcoded) and checks it is CONST.C, so any future
        convention drift is caught with the correct expectation in the
        failure message.
        """
        current, n_turns, radius = 1.0e-3, 100, 10.0
        emu_style = 2.0 * np.pi * n_turns * current / radius  # former bug
        gaussian = calc_field_at_center(current, n_turns, radius)
        ratio = emu_style / gaussian
        assert ratio == pytest.approx(CONST.C, rel=1e-13)
        assert gaussian == pytest.approx(emu_style / CONST.C, rel=1e-13)

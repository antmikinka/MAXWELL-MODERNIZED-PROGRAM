"""Qualifying tests for the anti-theater lint remediation of in-scope findings.

Remediates the Stage-3 quality-review defect D-10 class (verification
theater) in the last-200 program scope (Arts. 667-866):

* ``calibration/absolute_resistance.py`` -- the circular cross-check in
  ``verify_absolute_resistance`` (heat derived from R_lenz, then R_energy
  recovered from that heat and compared back to R_lenz) is replaced by a
  comparison of INDEPENDENT determinations, and the hardcoded
  ``velocity_check = True`` is replaced by a computed dimensional-
  homogeneity check (anti-theater lint findings R4 at :567 and R2 at :571).
* ``electromagnetism/theory/em_light_theory.py`` -- the hardcoded
  ``"verified": True`` in the capacitor case of ``verify_poynting_theorem``
  (finding R2 at :626) is replaced by a verdict computed from the actual
  finite-difference residuals of the Poynting identity
  du/dt + div S = -J.E on the module's own field solution.

Test patterns follow docs/LAST200_STAGE4_TESTING_STRATEGY.md:
section 5.1 (perturbation oracle for circularity, S2-8) and section 5.2
(known-bad dataset must flip the verdict).  All asserts are numeric with
stated tolerances (REQ-T rubric); no key-presence-only or bare-bool-only
assertions.

Run: PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_lint_remediation_last200.py
"""
from __future__ import annotations

import math

import numpy as np
import pytest

from articles import ref_value, tolerance_of
from maxwell.calibration.absolute_resistance import (
    analyze_absolute_resistance,
    verify_absolute_resistance,
)
from maxwell.electromagnetism.theory.em_light_theory import verify_poynting_theorem

# Electromagnetic determination shared by the resistance tests:
# R_lenz = EMF / I = 1.0 / 0.1 = 10 abohms (Arts. 759-760).
EMF = 1.0  # abvolt
CURRENT = 0.1  # abampere
R_LENZ = EMF / CURRENT  # 10 abohms


class TestAbsoluteResistanceIndependence:
    """The cross-check must use independent determinations (D-10, S2-8)."""

    @pytest.mark.regression("D-10")
    @pytest.mark.article(762)
    def test_verify_absolute_resistance_independence(self) -> None:
        """Perturbation oracle (Stage-4 section 5.1, test S2-8).

        Perturb the Lenz method's independent input (EMF) by +1% while the
        calorimetric heat stays fixed: a circular check would propagate the
        perturbation 1:1 into R_energy; an independent determination must
        not move at all (propagation < 0.1, here exactly 0).
        """
        heat = 0.2  # erg, independently measured over t = 2 s
        base = verify_absolute_resistance(
            induced_emf=EMF,
            induced_current=CURRENT,
            heat_generated=heat,
            dissipation_time=2.0,
        )
        perturbed = verify_absolute_resistance(
            induced_emf=EMF * 1.01,
            induced_current=CURRENT,
            heat_generated=heat,
            dissipation_time=2.0,
        )

        propagation = abs(perturbed["R_energy"] - base["R_energy"]) / (
            0.01 * abs(base["R_energy"])
        )
        assert propagation < 0.1, "cross-check propagates perturbations => circular"
        assert propagation == pytest.approx(0.0, abs=1e-15)

        # The perturbed input must still be live (the wiring was not simply
        # severed): R_lenz moves by exactly the imposed 1%.
        assert perturbed["R_lenz"] == pytest.approx(1.01 * base["R_lenz"], rel=1e-12)

    @pytest.mark.article(762)
    def test_calorimetric_cross_check_consistent_heat_passes(self) -> None:
        """An independent calorimetric measurement agreeing with the Lenz
        determination yields zero residual and a passing verdict."""
        heat = R_LENZ * CURRENT**2 * 2.0  # 0.2 erg over 2 s
        result = verify_absolute_resistance(
            induced_emf=EMF,
            induced_current=CURRENT,
            heat_generated=heat,
            dissipation_time=2.0,
        )

        assert result["calorimetric_cross_check"] is True
        assert result["R_energy"] == pytest.approx(R_LENZ, rel=1e-12)
        assert result["consistency_error"] == pytest.approx(0.0, abs=1e-12)
        assert result["verified"] is True

    @pytest.mark.article(762)
    def test_known_bad_heat_flips_verdict(self) -> None:
        """Known-bad dataset (Stage-4 section 5.2 runtime twin): heat 50%
        too large must flip the verdict, proving it is computed."""
        heat_bad = 1.5 * R_LENZ * CURRENT**2 * 2.0  # 0.3 erg over 2 s
        result = verify_absolute_resistance(
            induced_emf=EMF,
            induced_current=CURRENT,
            heat_generated=heat_bad,
            dissipation_time=2.0,
        )

        assert result["R_energy"] == pytest.approx(
            ref_value(762, "R_energy_known_bad"),
            **tolerance_of(762, "R_energy_known_bad"),
        )
        assert result["consistency_error"] == pytest.approx(
            ref_value(762, "consistency_error_known_bad"),
            **tolerance_of(762, "consistency_error_known_bad"),
        )
        assert result["verified"] is False

    @pytest.mark.article(759)
    def test_no_heat_reports_cross_check_not_performed(self) -> None:
        """Without an independent calorimetric measurement the function
        reports honestly instead of fabricating a comparison."""
        result = verify_absolute_resistance(
            induced_emf=EMF, induced_current=CURRENT
        )

        assert result["calorimetric_cross_check"] is False
        assert math.isnan(result["R_energy"])
        assert math.isnan(result["consistency_error"])
        # Verdict rests on the computed dimensional-homogeneity check only.
        assert result["R_lenz"] == pytest.approx(R_LENZ, rel=1e-12)
        assert result["verified"] is True


class TestVelocityDimensionCheck:
    """[R] = LT^-1 must be verified numerically, not asserted by comment."""

    @pytest.mark.article(767)
    def test_velocity_dimensions_exponents_computed(self) -> None:
        """The recoil formula's dimensional exponents are measured as
        (+1, -1): one power of length, minus one power of time -- the
        signature of a velocity (1 abohm = 1 cm/s in CGS-EMU)."""
        result = verify_absolute_resistance(
            mutual_inductance=1000.0,
            period=2.0,
            deflection_ratio=1.25,
        )

        exponents = result["dimension_exponents"]
        assert exponents["length"] == pytest.approx(
            ref_value(767, "velocity_dimension_length_exponent"),
            **tolerance_of(767, "velocity_dimension_length_exponent"),
        )
        assert exponents["time"] == pytest.approx(
            ref_value(767, "velocity_dimension_time_exponent"),
            **tolerance_of(767, "velocity_dimension_time_exponent"),
        )
        assert result["velocity_dimensions"] is True

    @pytest.mark.article(767)
    def test_degenerate_measurement_fails_dimension_check(self) -> None:
        """A zero-resistance (M = 0) measurement cannot establish the
        dimensional claim: the check must compute False, not default True."""
        result = verify_absolute_resistance(mutual_inductance=0.0)

        assert math.isnan(result["dimension_exponents"]["length"])
        assert math.isnan(result["dimension_exponents"]["time"])
        assert result["velocity_dimensions"] is False
        assert result["verified"] is False


class TestAnalyzeAbsoluteResistanceHonesty:
    """analyze_absolute_resistance must not synthesize a third method."""

    @pytest.mark.article(762)
    def test_no_heat_average_uses_existing_determinations_only(self) -> None:
        """Without independent heat, R_energy is NaN and the average is the
        mean of the two determinations that actually exist."""
        result = analyze_absolute_resistance(
            mutual_inductance=1000.0,
            period=2.0,
            deflection_ratio=1.25,
            induced_emf=EMF,
            induced_current=CURRENT,
        )

        assert math.isnan(result["R_energy"])
        expected_average = 0.5 * (result["R_recoil"] + result["R_lenz"])
        assert result["R_average"] == pytest.approx(expected_average, rel=1e-12)
        assert result["R_spread"] == pytest.approx(
            result["R_recoil"] - result["R_lenz"], rel=1e-12
        )

    @pytest.mark.article(762)
    def test_independent_heat_enters_average(self) -> None:
        """An independently supplied heat measurement contributes a genuine
        third determination to the average."""
        heat = R_LENZ * CURRENT**2 * 2.0
        result = analyze_absolute_resistance(
            mutual_inductance=1000.0,
            period=2.0,
            deflection_ratio=1.25,
            induced_emf=EMF,
            induced_current=CURRENT,
            heat_generated=heat,
            dissipation_time=2.0,
        )

        assert result["R_energy"] == pytest.approx(R_LENZ, rel=1e-12)
        expected_average = (
            result["R_recoil"] + result["R_lenz"] + result["R_energy"]
        ) / 3.0
        assert result["R_average"] == pytest.approx(expected_average, rel=1e-12)


class TestPoyntingIdentityResidual:
    """The capacitor-case verdict must come from the identity residual."""

    @pytest.mark.article(624)
    def test_capacitor_identity_residual_computed(self) -> None:
        """du/dt + div S = -J.E with J = 0: the finite-difference residual
        on the charging-capacitor field solution is reported and bounded by
        tolerance * scale; energy flows radially inward while charging."""
        result = verify_poynting_theorem("capacitor")

        assert result["poynting_residual"] >= 0.0
        assert result["residual_scale"] > 0.0
        relative = result["poynting_residual"] / result["residual_scale"]
        assert relative == pytest.approx(0.0, abs=1e-6)
        assert result["verified"] is True
        # Interior grid over (r, t): (21 - 2) x (21 - 2) points.
        assert result["grid_points"] == int(
            ref_value(624, "poynting_grid_interior_points")
        )
        # E along z, B along +y (local phi direction) => S = -x: inward.
        direction = np.asarray(result["energy_flow_direction"])
        assert direction == pytest.approx([-1.0, 0.0, 0.0], abs=1e-12)

    @pytest.mark.article(623)
    def test_capacitor_verdict_responds_to_tolerance(self) -> None:
        """A hardcoded verdict could never flip: tightening the tolerance
        below the residual magnitude must turn the verdict False."""
        strict = verify_poynting_theorem("capacitor", tolerance=0.0)
        assert strict["verified"] is False
        # the flip is only possible because the residual is a computed,
        # strictly positive number (REQ-T numeric pin for this test)
        assert strict["poynting_residual"] > 0.0

        loose = verify_poynting_theorem("capacitor", tolerance=1e-6)
        assert loose["verified"] is True
        assert loose["residual_scale"] > 0.0

        # If the reported residual is nonzero, straddling tolerances must
        # flip the verdict both ways around it.
        max_residual = loose["poynting_residual"]
        scale = loose["residual_scale"]
        if max_residual > 0.0:
            below = verify_poynting_theorem(
                "capacitor", tolerance=max_residual / (2.0 * scale)
            )
            above = verify_poynting_theorem(
                "capacitor", tolerance=2.0 * max_residual / scale
            )
            assert below["verified"] is False
            assert above["verified"] is True

    @pytest.mark.article(625)
    def test_other_cases_still_compute_their_verdicts(self) -> None:
        """The plane-wave and resistor cases keep their computed verdicts
        and numeric error reports."""
        plane = verify_poynting_theorem("plane_wave")
        assert plane["relative_error"] == pytest.approx(0.0, abs=1e-9)
        assert plane["verified"] is True

        resistor = verify_poynting_theorem("resistor")
        assert resistor["work_rate_density"] == pytest.approx(
            ref_value(625, "resistor_work_rate_density"),
            **tolerance_of(625, "resistor_work_rate_density"),
        )
        # The resistor branch returns a numpy bool (pre-existing behavior).
        assert resistor["verified"] is True or resistor["verified"] is np.True_

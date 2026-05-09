"""
Test suite for Magnetic Measurements module (Arts. 449-464).

This module tests Maxwell's magnetic measurement instruments from
Part III, Chapter VII:

1. Deflection Magnetometer (Arts. 449-452)
2. Suspension Systems (Arts. 453-456)
3. Kew Magnetometer (Arts. 457-459)
4. Dip Circle (Arts. 460-462)
5. Balance Magnetometer (Arts. 463-464)

All tests verify:
- Correct implementation of Maxwell's formulas
- CGS unit consistency
- Citation decorator compliance
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pytest

from maxwell.meta.citation import MaxwellCitation, get_citation

# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def earth_field_H() -> float:
    """Typical horizontal Earth field strength.

    Returns:
        H = 0.18 gauss (mid-latitude typical value).
    """
    return 0.18


@pytest.fixture
def sample_magnetic_moment() -> float:
    """Typical magnetic moment for test magnets.

    Returns:
        M = 100 emu.
    """
    return 100.0


@pytest.fixture
def sample_distance() -> float:
    """Typical distance for deflection measurements.

    Returns:
        r = 20.0 cm.
    """
    return 20.0


@pytest.fixture
def sample_deflection_angle() -> float:
    """Typical deflection angle.

    Returns:
        theta = 30 degrees in radians.
    """
    return np.radians(30)


@pytest.fixture
def sample_vibration_period() -> float:
    """Typical vibration period.

    Returns:
        T = 10.0 seconds.
    """
    return 10.0


@pytest.fixture
def sample_moment_of_inertia() -> float:
    """Typical moment of inertia for suspended magnet.

    Returns:
        I = 100.0 g*cm^2.
    """
    return 100.0


# =============================================================================
# CITATION TESTS
# =============================================================================


class TestMagneticMeasurementsCitations:
    """Test citation decorator compliance for magnetic measurements."""

    @pytest.fixture(autouse=True)
    def setup_magnetic_measurements(self) -> None:
        """Import the magnetic measurements module."""
        from maxwell.magnetism import magnetic_measurements

        self.module = magnetic_measurements

    def test_deflection_magnetometer_class_has_citations(
        self, require_citation
    ) -> None:
        """Verify DeflectionMagnetometer methods have citations."""
        from maxwell.magnetism import DeflectionMagnetometer

        citation = require_citation(DeflectionMagnetometer.measure_magnetic_moment)
        assert 449 in citation.articles
        assert 450 in citation.articles
        assert citation.part == 3

    def test_magnetometer_tan_position_has_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify magnetometer_tan_position has correct citation."""
        validate_citation_articles(
            self.module.magnetometer_tan_position, part=3, articles=[451]
        )

    def test_magnetometer_sine_position_has_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify magnetometer_sine_position has correct citation."""
        validate_citation_articles(
            self.module.magnetometer_sine_position, part=3, articles=[452]
        )

    def test_magnetometer_gauss_method_has_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify magnetometer_gauss_method has correct citation."""
        validate_citation_articles(
            self.module.magnetometer_gauss_method, part=3, articles=[451, 452]
        )

    def test_unifilar_suspension_class_has_citations(self, require_citation) -> None:
        """Verify UnifilarSuspension methods have citations."""
        from maxwell.magnetism import UnifilarSuspension

        citation = require_citation(UnifilarSuspension.oscillation_period)
        assert 453 in citation.articles
        assert 454 in citation.articles

    def test_torsion_constant_has_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify torsion_constant has correct citation."""
        validate_citation_articles(
            self.module.torsion_constant, part=3, articles=[453, 454]
        )

    def test_bifilar_suspension_class_has_citations(self, require_citation) -> None:
        """Verify BifilarSuspension methods have citations."""
        from maxwell.magnetism import BifilarSuspension

        citation = require_citation(BifilarSuspension.measure_horizontal_force)
        assert 455 in citation.articles
        assert 456 in citation.articles

    def test_magnetic_declination_has_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify magnetic_declination has correct citation."""
        validate_citation_articles(
            self.module.magnetic_declination, part=3, articles=[455]
        )

    def test_kew_magnetometer_class_has_citations(self, require_citation) -> None:
        """Verify KewMagnetometer methods have citations."""
        from maxwell.magnetism import KewMagnetometer

        citation = require_citation(KewMagnetometer.measure_absolute_H)
        assert 457 in citation.articles
        assert 458 in citation.articles

    def test_vibration_magnetometer_has_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify vibration_magnetometer has correct citation."""
        validate_citation_articles(
            self.module.vibration_magnetometer, part=3, articles=[459]
        )

    def test_dip_circle_class_has_citations(self, require_citation) -> None:
        """Verify DipCircle methods have citations."""
        from maxwell.magnetism import DipCircle

        citation = require_citation(DipCircle.measure_dip)
        assert 460 in citation.articles
        assert 461 in citation.articles

    def test_dip_correction_has_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify dip_correction has correct citation."""
        validate_citation_articles(self.module.dip_correction, part=3, articles=[462])

    def test_balance_magnetometer_class_has_citations(self, require_citation) -> None:
        """Verify BalanceMagnetometer methods have citations."""
        from maxwell.magnetism import BalanceMagnetometer

        citation = require_citation(BalanceMagnetometer.measure_vertical_force)
        assert 463 in citation.articles

    def test_vertical_intensity_has_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify vertical_intensity has correct citation."""
        validate_citation_articles(
            self.module.vertical_intensity, part=3, articles=[464]
        )

    def test_magnetic_survey_class_has_citations(self, require_citation) -> None:
        """Verify MagneticSurvey covers all articles 449-464."""
        from maxwell.magnetism import MagneticSurvey

        citation = require_citation(MagneticSurvey.complete_survey)
        assert citation.part == 3
        # Should cover all articles from 449 to 464
        for art in range(449, 465):
            assert (
                art in citation.articles
            ), f"Article {art} missing from survey citation"


# =============================================================================
# DEFLECTION MAGNETOMETER TESTS (Arts. 449-452)
# =============================================================================


class TestDeflectionMagnetometer:
    """Tests for DeflectionMagnetometer class (Arts. 449-450)."""

    def test_measure_magnetic_moment_end_on(
        self, earth_field_H, sample_distance, sample_deflection_angle
    ) -> None:
        """Test magnetic moment measurement in end-on position."""
        from maxwell.magnetism import DeflectionMagnetometer

        dm = DeflectionMagnetometer(
            earth_field_H=earth_field_H,
            needle_distance=sample_distance,
            position="end_on",
        )

        result = dm.measure_magnetic_moment(sample_deflection_angle)

        # M = (H * r^3 / 2) * tan(theta)
        expected_M = (earth_field_H * sample_distance**3 / 2) * np.tan(
            sample_deflection_angle
        )

        assert abs(result["magnetic_moment"] - expected_M) < 1e-10
        assert result["position"] == "end_on"
        assert abs(result["deflection_degrees"] - 30.0) < 1e-10

    def test_measure_magnetic_moment_broadside(
        self, earth_field_H, sample_distance, sample_deflection_angle
    ) -> None:
        """Test magnetic moment measurement in broadside position."""
        from maxwell.magnetism import DeflectionMagnetometer

        dm = DeflectionMagnetometer(
            earth_field_H=earth_field_H,
            needle_distance=sample_distance,
            position="broadside",
        )

        result = dm.measure_magnetic_moment(sample_deflection_angle)

        # M = (H * r^3) * tan(theta) for broadside
        expected_M = (
            earth_field_H * sample_distance**3 * np.tan(sample_deflection_angle)
        )

        assert abs(result["magnetic_moment"] - expected_M) < 1e-10
        assert result["position"] == "broadside"

    def test_predict_deflection(
        self, earth_field_H, sample_distance, sample_magnetic_moment
    ) -> None:
        """Test deflection prediction from known moment."""
        from maxwell.magnetism import DeflectionMagnetometer

        dm = DeflectionMagnetometer(
            earth_field_H=earth_field_H,
            needle_distance=sample_distance,
            position="end_on",
        )

        result = dm.predict_deflection(sample_magnetic_moment)

        # tan(theta) = 2*M / (H * r^3)
        expected_tan = 2 * sample_magnetic_moment / (earth_field_H * sample_distance**3)

        assert abs(result["tan_theta"] - expected_tan) < 1e-10
        assert "deflection_radians" in result
        assert "deflection_degrees" in result

    def test_invalid_position_raises_error(self) -> None:
        """Test that invalid position raises ValueError."""
        from maxwell.magnetism import DeflectionMagnetometer

        dm = DeflectionMagnetometer(position="invalid")

        with pytest.raises(ValueError):
            dm.measure_magnetic_moment(np.radians(30))


class TestMagnetometerTanPosition:
    """Tests for magnetometer_tan_position function (Art. 451)."""

    def test_tan_a_position_basic(
        self,
        sample_magnetic_moment,
        earth_field_H,
        sample_distance,
        sample_deflection_angle,
    ) -> None:
        """Test Tan-A position measurement."""
        from maxwell.magnetism import magnetometer_tan_position

        result = magnetometer_tan_position(
            magnetic_moment=sample_magnetic_moment,
            earth_field_H=earth_field_H,
            distance=sample_distance,
            deflection=sample_deflection_angle,
        )

        # M/H = (r^3 / 2) * tan(theta)
        expected_M_over_H = (sample_distance**3 / 2) * np.tan(sample_deflection_angle)

        assert abs(result["M_over_H"] - expected_M_over_H) < 1e-10
        assert result["gauss_constant"] == sample_distance**3 / 2


class TestMagnetometerSinePosition:
    """Tests for magnetometer_sine_position function (Art. 452)."""

    def test_sine_position_basic(
        self,
        sample_magnetic_moment,
        earth_field_H,
        sample_distance,
        sample_deflection_angle,
    ) -> None:
        """Test Sin-A position measurement."""
        from maxwell.magnetism import magnetometer_sine_position

        result = magnetometer_sine_position(
            magnetic_moment=sample_magnetic_moment,
            earth_field_H=earth_field_H,
            distance=sample_distance,
            deflection=sample_deflection_angle,
        )

        # M/H = r^3 * sin(theta) for sine method
        expected_M_over_H = (sample_distance**3 / 2) * np.sin(sample_deflection_angle)

        assert abs(result["M_over_H"] - expected_M_over_H) < 1e-10
        assert result["sin_deflection"] == np.sin(sample_deflection_angle)

    def test_tan_sin_difference(self) -> None:
        """Test that tan and sin differ for large angles."""
        from maxwell.magnetism import magnetometer_sine_position

        result = magnetometer_sine_position(
            magnetic_moment=100,
            earth_field_H=0.18,
            distance=20.0,
            deflection=np.radians(45),
        )

        # For 45 degrees, tan and sin differ significantly
        assert result["tan_deflection"] > result["sin_deflection"]


class TestMagnetometerGaussMethod:
    """Tests for magnetometer_gauss_method function (Arts. 451-452)."""

    def test_gauss_method_tan_a(
        self, sample_vibration_period, sample_distance, sample_moment_of_inertia
    ) -> None:
        """Test Gauss's method in Tan-A position."""
        from maxwell.magnetism import magnetometer_gauss_method

        tan_theta = np.tan(np.radians(30))

        result = magnetometer_gauss_method(
            tan_deflection=tan_theta,
            vibration_period=sample_vibration_period,
            distance=sample_distance,
            moment_of_inertia=sample_moment_of_inertia,
            position="tan_a",
        )

        # Verify M*H from vibration
        expected_MH = (
            4 * np.pi**2 * sample_moment_of_inertia / sample_vibration_period**2
        )
        assert abs(result["MH_product"] - expected_MH) < 1e-10

        # Verify M/H from deflection
        expected_M_over_H = (sample_distance**3 / 2) * tan_theta
        assert abs(result["M_over_H"] - expected_M_over_H) < 1e-10

        # Verify H and M are positive
        assert result["earth_field_H"] > 0
        assert result["magnetic_moment"] > 0

    def test_gauss_method_tan_b(self) -> None:
        """Test Gauss's method in Tan-B position."""
        from maxwell.magnetism import magnetometer_gauss_method

        result = magnetometer_gauss_method(
            tan_deflection=0.5,
            vibration_period=10.0,
            distance=20.0,
            moment_of_inertia=100.0,
            position="tan_b",
        )

        # Tan-B has different geometric factor (r^3 instead of r^3/2)
        assert result["M_over_H"] > 0

    def test_gauss_method_invalid_position(self) -> None:
        """Test that invalid position raises ValueError."""
        from maxwell.magnetism import magnetometer_gauss_method

        with pytest.raises(ValueError):
            magnetometer_gauss_method(
                tan_deflection=0.5,
                vibration_period=10.0,
                distance=20.0,
                moment_of_inertia=100.0,
                position="invalid",
            )


# =============================================================================
# SUSPENSION SYSTEMS TESTS (Arts. 453-456)
# =============================================================================


class TestUnifilarSuspension:
    """Tests for UnifilarSuspension class (Arts. 453-454)."""

    def test_torsion_constant_calculation(self) -> None:
        """Test torsion constant from fiber properties."""
        from maxwell.magnetism import UnifilarSuspension

        uf = UnifilarSuspension(
            fiber_length=30.0, fiber_radius=0.005, shear_modulus=3e11
        )

        # kappa = (pi * G * r^4) / (2 * l)
        expected_kappa = (np.pi * 3e11 * 0.005**4) / (2 * 30.0)

        assert abs(uf.torsion_constant - expected_kappa) < 1e-6

    def test_oscillation_period_zero_field(self) -> None:
        """Test oscillation period without magnetic field."""
        from maxwell.magnetism import UnifilarSuspension

        uf = UnifilarSuspension(
            fiber_length=30.0,
            fiber_radius=0.005,
            shear_modulus=3e11,
            moment_of_inertia=100.0,
        )

        result = uf.oscillation_period(magnetic_moment=0, earth_field_H=0)

        # T_0 = 2*pi * sqrt(I / kappa)
        expected_T = 2 * np.pi * np.sqrt(uf.moment_of_inertia / uf.torsion_constant)

        assert abs(result["period_zero_field"] - expected_T) < 1e-10

    def test_oscillation_period_with_field(self) -> None:
        """Test oscillation period with magnetic field."""
        from maxwell.magnetism import UnifilarSuspension

        uf = UnifilarSuspension(
            fiber_length=30.0,
            fiber_radius=0.005,
            shear_modulus=3e11,
            moment_of_inertia=100.0,
        )

        result = uf.oscillation_period(magnetic_moment=100, earth_field_H=0.18)

        # Field should reduce period (increase restoring torque)
        assert result["period"] < result["period_zero_field"]


class TestTorsionConstant:
    """Tests for torsion_constant function (Arts. 453-454)."""

    def test_theoretical_torsion_constant(self) -> None:
        """Test theoretical calculation of torsion constant."""
        from maxwell.magnetism import torsion_constant

        result = torsion_constant(
            fiber_length=30.0, fiber_radius=0.005, shear_modulus=3e11
        )

        expected = (np.pi * 3e11 * 0.005**4) / (2 * 30.0)

        assert abs(result["torsion_constant"] - expected) < 1e-6
        assert result["fiber_length"] == 30.0
        assert result["fiber_radius"] == 0.005

    def test_experimental_torsion_constant(self) -> None:
        """Test experimental determination from period."""
        from maxwell.magnetism import torsion_constant

        # Given period and inertia, compute kappa
        T = 11.91
        I = 100.0

        result = torsion_constant(
            fiber_length=30.0,
            fiber_radius=0.005,
            shear_modulus=3e11,
            measured_period=T,
            suspended_inertia=I,
        )

        expected_exp = 4 * np.pi**2 * I / T**2

        assert abs(result["experimental_kappa"] - expected_exp) < 1e-6
        assert "discrepancy" in result
        assert "discrepancy_percent" in result


class TestBifilarSuspension:
    """Tests for BifilarSuspension class (Arts. 455-456)."""

    def test_bifilar_constant(self) -> None:
        """Test bifilar constant calculation."""
        from maxwell.magnetism import BifilarSuspension

        bf = BifilarSuspension(
            fiber_length=30.0,
            top_separation=2.0,
            bottom_separation=2.0,
            suspended_mass=50.0,
        )

        # D = (m * g * a * b) / l
        expected_D = (50.0 * 980 * 2.0 * 2.0) / 30.0

        assert abs(bf.bifilar_constant - expected_D) < 1e-6

    def test_measure_horizontal_force(self) -> None:
        """Test horizontal force measurement."""
        from maxwell.magnetism import BifilarSuspension

        bf = BifilarSuspension(fiber_length=30.0, suspended_mass=50.0)

        result = bf.measure_horizontal_force(
            equilibrium_angle=np.radians(30), magnetic_moment=100
        )

        assert result["earth_field_H"] > 0
        assert "restoring_torque" in result
        assert "magnetic_torque" in result


class TestMagneticDeclination:
    """Tests for magnetic_declination function (Art. 455)."""

    def test_declination_east(self) -> None:
        """Test east declination (positive)."""
        from maxwell.magnetism import magnetic_declination

        result = magnetic_declination(
            astronomical_azimuth=0, magnetic_azimuth=np.radians(5)
        )

        assert result["declination_degrees"] > 0
        assert result["east_positive"] == True
        assert abs(result["declination_degrees"] - 5.0) < 1e-10

    def test_declination_west(self) -> None:
        """Test west declination (negative)."""
        from maxwell.magnetism import magnetic_declination

        result = magnetic_declination(
            astronomical_azimuth=0, magnetic_azimuth=np.radians(-5)
        )

        assert result["declination_degrees"] < 0
        assert result["east_positive"] == False

    def test_declination_normalization(self) -> None:
        """Test declination is normalized to [-180, 180]."""
        from maxwell.magnetism import magnetic_declination

        result = magnetic_declination(
            astronomical_azimuth=0, magnetic_azimuth=np.radians(370)  # Should normalize
        )

        assert -180 <= result["declination_degrees"] <= 180


# =============================================================================
# KEW MAGNETOMETER TESTS (Arts. 457-459)
# =============================================================================


class TestKewMagnetometer:
    """Tests for KewMagnetometer class (Arts. 457-458)."""

    def test_moment_of_inertia(self) -> None:
        """Test moment of inertia calculation."""
        from maxwell.magnetism import KewMagnetometer

        km = KewMagnetometer(magnet_length=10.0, magnet_mass=50.0)

        # I = (1/12) * m * L^2 for thin rod
        expected_I = (1 / 12) * 50.0 * 10.0**2

        assert abs(km.moment_of_inertia - expected_I) < 1e-10

    def test_measure_absolute_H(self) -> None:
        """Test absolute H measurement."""
        from maxwell.magnetism import KewMagnetometer

        km = KewMagnetometer()

        result = km.measure_absolute_H(
            deflection_angle=np.radians(30),
            vibration_period=10.0,
            deflecting_moment=100,
            deflection_distance=30.0,
        )

        assert result["earth_field_H"] > 0
        assert result["magnet_moment"] > 0
        assert "MH_product" in result
        assert "M_over_H" in result
        assert "measurement_quality" in result


class TestVibrationMagnetometer:
    """Tests for vibration_magnetometer function (Art. 459)."""

    def test_MH_product(
        self, sample_vibration_period, sample_moment_of_inertia
    ) -> None:
        """Test M*H product from vibration."""
        from maxwell.magnetism import vibration_magnetometer

        result = vibration_magnetometer(
            vibration_period=sample_vibration_period,
            moment_of_inertia=sample_moment_of_inertia,
        )

        expected_MH = (
            4 * np.pi**2 * sample_moment_of_inertia / sample_vibration_period**2
        )

        assert abs(result["MH_product"] - expected_MH) < 1e-10

    def test_derive_M_from_H(
        self, sample_vibration_period, sample_moment_of_inertia
    ) -> None:
        """Test deriving M when H is known."""
        from maxwell.magnetism import vibration_magnetometer

        H = 0.18

        result = vibration_magnetometer(
            vibration_period=sample_vibration_period,
            moment_of_inertia=sample_moment_of_inertia,
            earth_field_H=H,
        )

        assert result["derived_M"] is not None
        assert result["derived_M"] > 0

    def test_derive_H_from_M(
        self, sample_vibration_period, sample_moment_of_inertia
    ) -> None:
        """Test deriving H when M is known."""
        from maxwell.magnetism import vibration_magnetometer

        M = 100.0

        result = vibration_magnetometer(
            vibration_period=sample_vibration_period,
            moment_of_inertia=sample_moment_of_inertia,
            magnetic_moment=M,
        )

        assert result["derived_H"] is not None
        assert result["derived_H"] > 0


# =============================================================================
# DIP CIRCLE TESTS (Arts. 460-462)
# =============================================================================


class TestDipCircle:
    """Tests for DipCircle class (Arts. 460-461)."""

    def test_measure_dip_basic(self) -> None:
        """Test basic dip measurement."""
        from maxwell.magnetism import DipCircle

        dc = DipCircle()

        result = dc.measure_dip(np.radians(60))

        assert abs(result["true_dip_degrees"] - 60.0) < 1e-10
        assert result["vertical_component_Z"] > 0
        assert result["total_field_F"] > 0

    def test_dip_azimuth_correction(self) -> None:
        """Test dip measurement with azimuth correction."""
        from maxwell.magnetism import DipCircle

        dc = DipCircle()

        # When dip circle is rotated from meridian, apparent dip increases
        result = dc.measure_dip(
            observed_dip=np.radians(60), azimuth_from_meridian=np.radians(10)
        )

        # True dip should be less than observed when not in meridian
        assert result["true_dip"] < result["observed_dip"]


class TestDipCorrection:
    """Tests for dip_correction function (Art. 462)."""

    def test_reversal_correction(self) -> None:
        """Test reversal correction."""
        from maxwell.magnetism import dip_correction

        result = dip_correction(
            observed_dip=np.radians(60), needle_reversed_dip=np.radians(59.5)
        )

        # Corrected dip should be average
        expected = (np.radians(60) + np.radians(59.5)) / 2

        assert abs(result["corrected_dip"] - expected) < 1e-10
        assert result["reversal_correction"] != 0

    def test_azimuth_correction(self) -> None:
        """Test azimuth correction."""
        from maxwell.magnetism import dip_correction

        result = dip_correction(
            observed_dip=np.radians(60), azimuth_error=np.radians(5)
        )

        assert result["azimuth_correction"] != 0

    def test_no_corrections(self) -> None:
        """Test with no corrections needed."""
        from maxwell.magnetism import dip_correction

        result = dip_correction(
            observed_dip=np.radians(60),
            needle_reversed_dip=np.radians(60),
            azimuth_error=0,
            eccentricity_error=0,
        )

        # No corrections should mean output equals input
        assert abs(result["corrected_dip"] - np.radians(60)) < 1e-10


# =============================================================================
# BALANCE MAGNETOMETER TESTS (Arts. 463-464)
# =============================================================================


class TestBalanceMagnetometer:
    """Tests for BalanceMagnetometer class (Arts. 463-464)."""

    def test_measure_vertical_force(self) -> None:
        """Test vertical force measurement."""
        from maxwell.magnetism import BalanceMagnetometer

        bm = BalanceMagnetometer()

        result = bm.measure_vertical_force(np.radians(5))

        assert result["vertical_component_Z"] > 0
        assert "magnetic_torque" in result
        assert "gravitational_torque" in result

    def test_small_angle_approximation(self) -> None:
        """Test small angle behavior."""
        from maxwell.magnetism import BalanceMagnetometer

        bm = BalanceMagnetometer()

        result_small = bm.measure_vertical_force(np.radians(1))
        result_large = bm.measure_vertical_force(np.radians(10))

        # Z should scale approximately with tan(theta)
        ratio = (
            result_large["vertical_component_Z"] / result_small["vertical_component_Z"]
        )
        expected_ratio = np.tan(np.radians(10)) / np.tan(np.radians(1))

        assert abs(ratio - expected_ratio) < 1e-6


class TestVerticalIntensity:
    """Tests for vertical_intensity function (Art. 464)."""

    def test_basic_measurement(self) -> None:
        """Test basic vertical intensity measurement."""
        from maxwell.magnetism import vertical_intensity

        result = vertical_intensity(balance_reading=0.42, calibration_constant=1.0)

        assert result["vertical_intensity_Z"] == 0.42
        assert result["total_field_F"] > 0
        assert result["dip_degrees"] > 0

    def test_temperature_correction(self) -> None:
        """Test temperature correction."""
        from maxwell.magnetism import vertical_intensity

        result = vertical_intensity(
            balance_reading=0.42,
            calibration_constant=1.0,
            temperature=298.15,  # 5 degrees above reference
        )

        assert result["temperature_corrected_Z"] != result["vertical_intensity_Z"]
        assert result["temperature_correction_factor"] != 1.0


# =============================================================================
# MAGNETIC SURVEY TESTS (Arts. 449-464)
# =============================================================================


class TestMagneticSurvey:
    """Tests for MagneticSurvey class (complete survey Arts. 449-464)."""

    def test_complete_survey(self) -> None:
        """Test complete magnetic survey."""
        from maxwell.magnetism import MagneticSurvey

        survey = MagneticSurvey(observatory_name="Test Observatory")

        result = survey.complete_survey(
            deflection_angle=np.radians(30),
            deflection_distance=20.0,
            vibration_period=10.0,
            magnet_inertia=100.0,
            observed_dip=np.radians(60),
            astronomical_azimuth=0,
            magnetic_azimuth=np.radians(5),
            balance_reading=0.42,
            balance_constant=1.0,
        )

        # Verify all seven elements are present
        assert "H" in result
        assert "Z" in result
        assert "F" in result
        assert "X" in result
        assert "Y" in result
        assert "dip_degrees" in result
        assert "declination_degrees" in result

        # Verify physical consistency
        assert result["H"] > 0
        assert result["Z"] > 0
        assert result["F"] > 0

        # F = sqrt(H^2 + Z^2)
        expected_F = np.sqrt(result["H"] ** 2 + result["Z"] ** 2)
        assert abs(result["F"] - expected_F) < 1e-10

    def test_survey_with_reversed_dip(self) -> None:
        """Test survey with reversed dip reading."""
        from maxwell.magnetism import MagneticSurvey

        survey = MagneticSurvey()

        result = survey.complete_survey(
            deflection_angle=np.radians(30),
            deflection_distance=20.0,
            vibration_period=10.0,
            magnet_inertia=100.0,
            observed_dip=np.radians(60),
            astronomical_azimuth=0,
            magnetic_azimuth=np.radians(5),
            balance_reading=0.42,
            balance_constant=1.0,
            dip_reversed=np.radians(59.8),
        )

        # Dip should be average of observed and reversed
        expected_dip = (np.radians(60) + np.radians(59.8)) / 2

        assert abs(result["dip_I"] - expected_dip) < 1e-10


# =============================================================================
# INTEGRATION TESTS
# =============================================================================


class TestMagneticMeasurementsIntegration:
    """Integration tests for complete magnetic measurements workflow."""

    def test_full_measurement_chain(self) -> None:
        """Test complete chain from raw measurements to field elements."""
        from maxwell.magnetism import (
            BalanceMagnetometer,
            DeflectionMagnetometer,
            DipCircle,
            MagneticSurvey,
            magnetometer_gauss_method,
        )

        # Step 1: Deflection measurement
        dm = DeflectionMagnetometer(earth_field_H=0.18, needle_distance=20.0)
        moment_result = dm.measure_magnetic_moment(np.radians(30))

        # Step 2: Gauss method for H and M
        gauss_result = magnetometer_gauss_method(
            tan_deflection=np.tan(np.radians(30)),
            vibration_period=10.0,
            distance=20.0,
            moment_of_inertia=100.0,
        )

        # Step 3: Dip measurement
        dc = DipCircle()
        dip_result = dc.measure_dip(np.radians(60))

        # Step 4: Vertical intensity
        bm = BalanceMagnetometer()
        vertical_result = bm.measure_vertical_force(np.radians(5))

        # All results should be consistent
        assert gauss_result["earth_field_H"] > 0
        assert dip_result["true_dip_degrees"] > 0
        assert vertical_result["vertical_component_Z"] > 0

    def test_export_completeness(self) -> None:
        """Verify all expected functions are exported."""
        from maxwell import magnetism

        expected_exports = [
            "DeflectionMagnetometer",
            "magnetometer_tan_position",
            "magnetometer_sine_position",
            "magnetometer_gauss_method",
            "UnifilarSuspension",
            "torsion_constant",
            "BifilarSuspension",
            "magnetic_declination",
            "KewMagnetometer",
            "vibration_magnetometer",
            "DipCircle",
            "dip_correction",
            "BalanceMagnetometer",
            "vertical_intensity",
            "MagneticSurvey",
        ]

        for name in expected_exports:
            assert hasattr(magnetism, name), f"Missing export: {name}"


# =============================================================================
# MAIN: Run tests with pytest
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

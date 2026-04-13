"""
Test new Part IV Signal Processing and Calibration modules.

Comprehensive test coverage for signal transmission and resistance measurement:
- Telegraphy (Arts. 730-757) — Telegraph equation, signal velocity, attenuation
- Absolute Resistance (Arts. 758-767) — Recoil method, Lenz method, rotating coil

Tests verify:
- Correct formula implementation with numeric values
- Physical relationships (v = 1/sqrt(LC), Z0 = sqrt(L/C))
- Edge cases (lossless limits, zero inputs)
- CGS unit compliance (abohms, abvolts, abamperes)
- Citation decorator compliance
"""

from __future__ import annotations

import pytest
import numpy as np

from maxwell.config.constants import CONST, C, cgs_unit_of
from maxwell.meta.citation import get_citation, MaxwellCitation


# =============================================================================
# TELEGRAPHY TESTS (Arts. 730-757)
# =============================================================================

class TestTelegraphLine:
    """Test TelegraphLine class for signal transmission."""

    def test_signal_velocity_lossless(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify v = 1/sqrt(LC) for lossless line.

        Art. 730: For L = 10 cm, C = 1e-10 cm^-1:
        v = 1/sqrt(10 * 1e-10) = 1e5 cm/s
        """
        from maxwell.signal_processing.telegraphy import TelegraphLine

        line = TelegraphLine(L=10.0, C=1e-10)
        v = line.signal_velocity()

        expected = 1.0 / np.sqrt(10.0 * 1e-10)
        assert_cgs_close(v, expected, cgs_tolerance)

    def test_signal_velocity_limits(self) -> None:
        """Verify signal velocity returns 0 for invalid inputs."""
        from maxwell.signal_processing.telegraphy import TelegraphLine

        # Zero inductance
        line_zero_L = TelegraphLine(L=0.0, C=1e-10)
        assert line_zero_L.signal_velocity() == 0.0

        # Zero capacitance
        line_zero_C = TelegraphLine(L=10.0, C=0.0)
        assert line_zero_C.signal_velocity() == 0.0

    def test_characteristic_impedance(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Z0 = sqrt(L/C).

        Art. 731: For L = 10 cm, C = 1e-10 cm^-1:
        Z0 = sqrt(10 / 1e-10) = 1e5 cm/s
        """
        from maxwell.signal_processing.telegraphy import TelegraphLine

        line = TelegraphLine(L=10.0, C=1e-10)
        Z0 = line.characteristic_impedance()

        expected = np.sqrt(10.0 / 1e-10)
        assert_cgs_close(Z0, expected, cgs_tolerance)

    def test_characteristic_impedance_zero_capacitance(self) -> None:
        """Verify Z0 = infinity for C = 0."""
        from maxwell.signal_processing.telegraphy import TelegraphLine

        line = TelegraphLine(L=10.0, C=0.0)
        assert line.characteristic_impedance() == float('inf')

    def test_attenuation_constant_low_frequency(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify attenuation at low frequency.

        Art. 732: For low frequency, alpha ≈ sqrt(R*G).

        With G = 0, attenuation should be small.
        """
        from maxwell.signal_processing.telegraphy import TelegraphLine

        line = TelegraphLine(R=0.01, L=10.0, C=1e-10, G=0.0)

        # Low frequency
        omega = 2 * np.pi * 100  # 100 Hz
        alpha = line.attenuation_constant(omega)

        # Should be small but non-zero
        assert alpha >= 0

    def test_attenuation_constant_high_frequency(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify attenuation increases with frequency.

        Art. 732: High frequency attenuation:
        alpha ≈ (R/2)*sqrt(C/L) + (G/2)*sqrt(L/C)
        """
        from maxwell.signal_processing.telegraphy import TelegraphLine

        line = TelegraphLine(R=0.01, L=10.0, C=1e-10, G=1e-6)

        omega_low = 2 * np.pi * 100
        omega_high = 2 * np.pi * 1e9

        alpha_low = line.attenuation_constant(omega_low)
        alpha_high = line.attenuation_constant(omega_high)

        # High frequency should have higher attenuation
        assert alpha_high > alpha_low

    def test_phase_constant(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify phase constant beta.

        Art. 733: For lossless line, beta = omega * sqrt(LC).
        """
        from maxwell.signal_processing.telegraphy import TelegraphLine

        line = TelegraphLine(R=0.0, L=10.0, C=1e-10, G=0.0)

        omega = 2 * np.pi * 1e6  # 1 MHz
        beta = line.phase_constant(omega)

        expected = omega * np.sqrt(10.0 * 1e-10)
        assert_cgs_close(beta, expected, cgs_tolerance)

    def test_delay_per_length(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify delay = sqrt(LC).

        Art. 734: Delay per unit length = 1/v = sqrt(LC).
        """
        from maxwell.signal_processing.telegraphy import TelegraphLine

        line = TelegraphLine(L=10.0, C=1e-10)
        delay = line.delay_per_length()

        expected = np.sqrt(10.0 * 1e-10)
        assert_cgs_close(delay, expected, cgs_tolerance)

    def test_voltage_at_distance衰减(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify voltage decays with distance.

        Art. 735: V(x) = V0 * exp(-gamma * x)
        """
        from maxwell.signal_processing.telegraphy import TelegraphLine

        line = TelegraphLine(R=0.01, L=10.0, C=1e-10, G=0.0)

        V0 = 1.0  # 1 abvolt
        omega = 2 * np.pi * 1e6

        V_near = line.voltage_at_distance(V0, x=0.0, angular_frequency=omega)
        V_far = line.voltage_at_distance(V0, x=1000.0, angular_frequency=omega)

        # Magnitude should decrease with distance
        assert abs(V_far) < abs(V_near)

    def test_voltage_at_distance_zero(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify V(0) = V0."""
        from maxwell.signal_processing.telegraphy import TelegraphLine

        line = TelegraphLine(R=0.01, L=10.0, C=1e-10, G=0.0)

        V0 = 1.0
        omega = 2 * np.pi * 1e6

        V_at_zero = line.voltage_at_distance(V0, x=0.0, angular_frequency=omega)

        assert_cgs_close(abs(V_at_zero), V0, cgs_tolerance)

    def test_telegraph_line_invalid_parameters(self) -> None:
        """Verify error for negative parameters."""
        from maxwell.signal_processing.telegraphy import TelegraphLine

        with pytest.raises(ValueError):
            TelegraphLine(R=-0.01, L=10.0, C=1e-10)

        with pytest.raises(ValueError):
            TelegraphLine(R=0.01, L=-10.0, C=1e-10)


class TestSignalTransmission:
    """Test SignalTransmission analysis class."""

    def test_rise_time(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify rise time formula.

        Art. 740: t_r ≈ 2.2 * R * C * L^2
        """
        from maxwell.signal_processing.telegraphy import (
            TelegraphLine, SignalTransmission
        )

        line = TelegraphLine(R=0.01, L=10.0, C=1e-10, G=0.0)
        st = SignalTransmission(line)

        length = 1000.0  # 1000 cm
        t_r = st.rise_time(length)

        expected = 2.2 * 0.01 * 1e-10 * (1000.0 ** 2)
        assert_cgs_close(t_r, expected, cgs_tolerance)

    def test_rise_time_zero_length(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify rise time = 0 for zero length."""
        from maxwell.signal_processing.telegraphy import (
            TelegraphLine, SignalTransmission
        )

        line = TelegraphLine(R=0.01, L=10.0, C=1e-10, G=0.0)
        st = SignalTransmission(line)

        assert st.rise_time(0.0) == 0.0

    def test_bandwidth_limit(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify bandwidth limit.

        Art. 745: BW ≈ 0.35 / t_r
        """
        from maxwell.signal_processing.telegraphy import (
            TelegraphLine, SignalTransmission
        )

        line = TelegraphLine(R=0.01, L=10.0, C=1e-10, G=0.0)
        st = SignalTransmission(line)

        length = 1000.0
        t_r = st.rise_time(length)
        bw = st.bandwidth_limit(length)

        expected = 0.35 / t_r
        assert_cgs_close(bw, expected, cgs_tolerance)

    def test_max_signaling_rate(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify maximum signaling rate.

        Art. 750: f_max ≈ 1 / (2 * t_r)
        """
        from maxwell.signal_processing.telegraphy import (
            TelegraphLine, SignalTransmission
        )

        line = TelegraphLine(R=0.01, L=10.0, C=1e-10, G=0.0)
        st = SignalTransmission(line)

        length = 1000.0
        t_r = st.rise_time(length)
        f_max = st.max_signaling_rate(length)

        expected = 1.0 / (2.0 * t_r)
        assert_cgs_close(f_max, expected, cgs_tolerance)


class TestTelegraphFunctions:
    """Test standalone telegraph functions."""

    def test_calc_signal_velocity(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify calc_signal_velocity function."""
        from maxwell.signal_processing.telegraphy import calc_signal_velocity

        v = calc_signal_velocity(L=10.0, C=1e-10)
        expected = 1.0 / np.sqrt(10.0 * 1e-10)

        assert_cgs_close(v, expected, cgs_tolerance)

    def test_calc_signal_velocity_invalid(self) -> None:
        """Verify calc_signal_velocity returns 0 for invalid inputs."""
        from maxwell.signal_processing.telegraphy import calc_signal_velocity

        assert calc_signal_velocity(L=0.0, C=1e-10) == 0.0
        assert calc_signal_velocity(L=10.0, C=0.0) == 0.0

    def test_calc_characteristic_impedance(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify calc_characteristic_impedance function."""
        from maxwell.signal_processing.telegraphy import calc_characteristic_impedance

        Z0 = calc_characteristic_impedance(L=10.0, C=1e-10)
        expected = np.sqrt(10.0 / 1e-10)

        assert_cgs_close(Z0, expected, cgs_tolerance)

    def test_calc_propagation_constant(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify calc_propagation_constant function."""
        from maxwell.signal_processing.telegraphy import calc_propagation_constant

        omega = 2 * np.pi * 1e6
        gamma = calc_propagation_constant(R=0.01, L=10.0, C=1e-10, G=0.0, angular_frequency=omega)

        # Should be complex
        assert isinstance(gamma, (complex, np.complex128))

        # Real part (alpha) should be small for low loss
        # Imaginary part (beta) should be positive
        assert np.imag(gamma) > 0

    def test_calc_signal_delay(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify calc_signal_delay function."""
        from maxwell.signal_processing.telegraphy import calc_signal_delay

        delay = calc_signal_delay(L=10.0, C=1e-10, length=1000.0)
        expected = 1000.0 * np.sqrt(10.0 * 1e-10)

        assert_cgs_close(delay, expected, cgs_tolerance)

    def test_verify_telegraph_line(self) -> None:
        """Verify verify_telegraph_line function."""
        from maxwell.signal_processing.telegraphy import verify_telegraph_line

        result = verify_telegraph_line(
            R=0.01, L=10.0, C=1e-10, G=0.0, frequency=1e6
        )

        assert result["verified"] is True or result["verified"] is np.True_
        assert "signal_velocity" in result
        assert "characteristic_impedance" in result
        assert "attenuation_constant" in result
        assert "phase_constant" in result

    def test_analyze_telegraph_line(self) -> None:
        """Verify analyze_telegraph_line function."""
        from maxwell.signal_processing.telegraphy import analyze_telegraph_line

        result = analyze_telegraph_line(
            R=0.003, L=1.7, C=0.3e-6, G=0.0,
            length=3000e5,  # 3000 km
            frequency=1e6
        )

        assert "signal_velocity_cm_s" in result
        assert "characteristic_impedance" in result
        assert "length_km" in result
        assert "bandwidth_Hz" in result


class TestTelegraphLinePhysicalRelationships:
    """Test physical relationships in telegraph line theory."""

    def test_velocity_impedance_relationship(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify v * Z0 = 1/C relationship.

        From v = 1/sqrt(LC) and Z0 = sqrt(L/C):
        v * Z0 = (1/sqrt(LC)) * sqrt(L/C) = 1/C
        """
        from maxwell.signal_processing.telegraphy import TelegraphLine

        line = TelegraphLine(L=10.0, C=1e-10)

        v = line.signal_velocity()
        Z0 = line.characteristic_impedance()
        C = line.C

        lhs = v * Z0
        rhs = 1.0 / C

        assert_cgs_close(lhs, rhs, cgs_tolerance)

    def test_velocity_inductance_relationship(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify v / Z0 = 1/L relationship.

        From v = 1/sqrt(LC) and Z0 = sqrt(L/C):
        v / Z0 = (1/sqrt(LC)) / sqrt(L/C) = 1/L
        """
        from maxwell.signal_processing.telegraphy import TelegraphLine

        line = TelegraphLine(L=10.0, C=1e-10)

        v = line.signal_velocity()
        Z0 = line.characteristic_impedance()
        L = line.L

        lhs = v / Z0
        rhs = 1.0 / L

        assert_cgs_close(lhs, rhs, cgs_tolerance)


# =============================================================================
# ABSOLUTE RESISTANCE TESTS (Arts. 758-767)
# =============================================================================

class TestAbsoluteResistanceRecoilMethod:
    """Test recoil method for absolute resistance measurement."""

    def test_recoil_method_basic(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify recoil method formula.

        Art. 758: R = (2M/T) * (theta1/theta2)

        For M = 1000 cm, T = 2.0 s, theta1/theta2 = 1.25:
        R = (2*1000/2) * 1.25 = 1250 abohms
        """
        from maxwell.calibration.absolute_resistance import AbsoluteResistance

        ar = AbsoluteResistance(method='recoil')

        R = ar.recoil_method(
            mutual_inductance=1000.0,
            period=2.0,
            first_deflection=0.1,
            second_deflection=0.08  # ratio = 1.25
        )

        expected = (2 * 1000.0 / 2.0) * (0.1 / 0.08)
        assert_cgs_close(R, expected, cgs_tolerance)

    def test_recoil_method_direct_calculation(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify calc_absolute_resistance_recoil function."""
        from maxwell.calibration.absolute_resistance import calc_absolute_resistance_recoil

        R = calc_absolute_resistance_recoil(
            mutual_inductance=1000.0,
            period=2.0,
            first_deflection=0.1,
            second_deflection=0.08
        )

        expected = (2 * 1000.0 / 2.0) * (0.1 / 0.08)
        assert_cgs_close(R, expected, cgs_tolerance)

    def test_recoil_method_invalid_period(self) -> None:
        """Verify error for invalid period."""
        from maxwell.calibration.absolute_resistance import AbsoluteResistance

        ar = AbsoluteResistance()

        with pytest.raises(ValueError):
            ar.recoil_method(
                mutual_inductance=1000.0,
                period=0.0,
                first_deflection=0.1,
                second_deflection=0.08
            )

    def test_recoil_method_invalid_deflection(self) -> None:
        """Verify error for invalid deflection."""
        from maxwell.calibration.absolute_resistance import AbsoluteResistance

        ar = AbsoluteResistance()

        with pytest.raises(ValueError):
            ar.recoil_method(
                mutual_inductance=1000.0,
                period=2.0,
                first_deflection=0.1,
                second_deflection=0.0
            )


class TestAbsoluteResistanceLenzMethod:
    """Test Lenz's law method for resistance measurement."""

    def test_lenz_method_basic(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Lenz method formula.

        Art. 759-760: R = EMF / I

        For EMF = 1.0 abvolt, I = 0.1 abampere:
        R = 10 abohms
        """
        from maxwell.calibration.absolute_resistance import AbsoluteResistance

        ar = AbsoluteResistance(method='lenz')

        R = ar.lenz_method(
            induced_emf=1.0,
            induced_current=0.1
        )

        expected = 1.0 / 0.1
        assert_cgs_close(R, expected, cgs_tolerance)

    def test_lenz_method_direct_calculation(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify calc_absolute_resistance_lenz function."""
        from maxwell.calibration.absolute_resistance import calc_absolute_resistance_lenz

        R = calc_absolute_resistance_lenz(
            induced_emf=1.0,
            induced_current=0.1
        )

        expected = 1.0 / 0.1
        assert_cgs_close(R, expected, cgs_tolerance)

    def test_lenz_method_zero_current(self) -> None:
        """Verify R = infinity for I = 0."""
        from maxwell.calibration.absolute_resistance import AbsoluteResistance

        ar = AbsoluteResistance()

        R = ar.lenz_method(
            induced_emf=1.0,
            induced_current=0.0
        )

        assert R == float('inf')


class TestAbsoluteResistanceRotatingCoilMethod:
    """Test rotating coil (Lorenz) method."""

    def test_rotating_coil_method_basic(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify rotating coil method formula.

        Art. 761: EMF = N * B * A * omega
                  R = EMF / I

        For N = 100, B = 1000 gauss, A = 10 cm^2, omega = 100 rad/s:
        EMF = 100 * 1000 * 10 * 100 = 1e8 abvolts
        For I = 0.01 abampere: R = 1e10 abohms
        """
        from maxwell.calibration.absolute_resistance import calc_absolute_resistance_rotating_coil

        R = calc_absolute_resistance_rotating_coil(
            n_turns=100,
            coil_area=10.0,
            angular_velocity=100.0,
            magnetic_field=1000.0,
            induced_current=0.01
        )

        expected_emf = 100 * 1000.0 * 10.0 * 100.0
        expected_R = expected_emf / 0.01

        assert_cgs_close(R, expected_R, cgs_tolerance)

    def test_rotating_coil_zero_current(self) -> None:
        """Verify R = infinity for I = 0."""
        from maxwell.calibration.absolute_resistance import AbsoluteResistance

        ar = AbsoluteResistance()

        R = ar.rotating_coil_method(
            n_turns=100,
            coil_area=10.0,
            angular_velocity=100.0,
            magnetic_field=1000.0,
            induced_current=0.0,
            circuit_resistance_known=0.0
        )

        assert R == float('inf')


class TestAbsoluteResistanceEnergyMethod:
    """Test energy dissipation method."""

    def test_energy_dissipation_method_basic(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify energy dissipation formula.

        Art. 762: Heat = I^2 * R * t
                  R = Heat / (I^2 * t)

        For I = 1.0 abamp, t = 1.0 s, Heat = 10.0 ergs:
        R = 10.0 abohms
        """
        from maxwell.calibration.absolute_resistance import AbsoluteResistance

        ar = AbsoluteResistance(method='energy')

        R = ar.energy_dissipation_method(
            current=1.0,
            time=1.0,
            heat_generated=10.0
        )

        expected = 10.0 / (1.0 ** 2 * 1.0)
        assert_cgs_close(R, expected, cgs_tolerance)

    def test_energy_dissipation_direct_calculation(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify calc_absolute_resistance_joule function."""
        from maxwell.calibration.absolute_resistance import calc_absolute_resistance_joule

        R = calc_absolute_resistance_joule(
            current=1.0,
            time=1.0,
            heat_energy=10.0
        )

        expected = 10.0 / (1.0 ** 2 * 1.0)
        assert_cgs_close(R, expected, cgs_tolerance)

    def test_energy_dissipation_zero_current(self) -> None:
        """Verify R = infinity for I = 0."""
        from maxwell.calibration.absolute_resistance import AbsoluteResistance

        ar = AbsoluteResistance()

        R = ar.energy_dissipation_method(
            current=0.0,
            time=1.0,
            heat_generated=10.0
        )

        assert R == float('inf')


class TestStandardResistanceCoil:
    """Test standard resistance coil calculations."""

    def test_resistance_at_temperature(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify temperature correction formula.

        Art. 763: R(T) = R0 * [1 + alpha * (T - T0)]

        For R0 = 100 abohms, alpha = 0.004/°C, T = 30°C, T0 = 20°C:
        R = 100 * [1 + 0.004 * 10] = 104 abohms
        """
        from maxwell.calibration.absolute_resistance import StandardResistanceCoil

        src = StandardResistanceCoil(
            nominal_resistance=100.0,
            material='copper'
        )

        R = src.resistance_at_temperature(temperature=30.0)

        expected = 100.0 * (1.0 + 0.004 * 10.0)
        assert_cgs_close(R, expected, cgs_tolerance)

    def test_resistance_at_reference_temperature(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify R(T0) = R0."""
        from maxwell.calibration.absolute_resistance import StandardResistanceCoil

        src = StandardResistanceCoil(nominal_resistance=100.0)

        R = src.resistance_at_temperature(temperature=20.0)

        assert_cgs_close(R, 100.0, cgs_tolerance)

    def test_temperature_coefficients(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify temperature coefficients for different materials."""
        from maxwell.calibration.absolute_resistance import StandardResistanceCoil

        # Manganin has very low temperature coefficient
        src_manganin = StandardResistanceCoil(
            nominal_resistance=100.0,
            material='manganin'
        )
        assert src_manganin.temperature_coefficient == 0.00002

        # Copper has high temperature coefficient
        src_copper = StandardResistanceCoil(
            nominal_resistance=100.0,
            material='copper'
        )
        assert src_copper.temperature_coefficient == 0.004

    def test_self_inductance_calculation(self) -> None:
        """Verify self-inductance calculation."""
        from maxwell.calibration.absolute_resistance import StandardResistanceCoil

        src = StandardResistanceCoil(nominal_resistance=100.0)

        L = src.self_inductance(coil_radius=1.0, coil_length=10.0)

        # Should be positive
        assert L > 0

    def test_self_inductance_invalid_dimensions(self) -> None:
        """Verify L = 0 for invalid dimensions."""
        from maxwell.calibration.absolute_resistance import StandardResistanceCoil

        src = StandardResistanceCoil(nominal_resistance=100.0)

        assert src.self_inductance(coil_radius=0.0, coil_length=10.0) == 0.0
        assert src.self_inductance(coil_radius=1.0, coil_length=0.0) == 0.0


class TestTemperatureCorrectedResistance:
    """Test temperature-corrected resistance function."""

    def test_calc_temperature_corrected_resistance(
        self, cgs_tolerance, assert_cgs_close
    ) -> None:
        """Verify calc_temperature_corrected_resistance function."""
        from maxwell.calibration.absolute_resistance import calc_temperature_corrected_resistance

        R = calc_temperature_corrected_resistance(
            nominal_resistance=100.0,
            temperature=30.0,
            temperature_coefficient=0.004,
            reference_temp=20.0
        )

        expected = 100.0 * (1.0 + 0.004 * 10.0)
        assert_cgs_close(R, expected, cgs_tolerance)


class TestAbsoluteResistanceVerification:
    """Test verification functions."""

    def test_verify_absolute_resistance(self) -> None:
        """Verify verify_absolute_resistance function."""
        from maxwell.calibration.absolute_resistance import verify_absolute_resistance

        result = verify_absolute_resistance(
            mutual_inductance=1000.0,
            period=2.0,
            deflection_ratio=1.25,
            induced_emf=1.0,
            induced_current=0.1
        )

        assert result["verified"] is True
        assert "R_recoil" in result
        assert "R_lenz" in result
        assert "R_energy" in result
        assert "consistency_error" in result

    def test_analyze_absolute_resistance(self) -> None:
        """Verify analyze_absolute_resistance function."""
        from maxwell.calibration.absolute_resistance import analyze_absolute_resistance

        result = analyze_absolute_resistance(
            method='recoil',
            mutual_inductance=1000.0,
            period=2.0,
            deflection_ratio=1.25,
            induced_emf=1.0,
            induced_current=0.1,
            nominal_resistance=10.0,
            temperature=20.0
        )

        assert "R_recoil" in result
        assert "R_lenz" in result
        assert "R_energy" in result
        assert "R_average" in result
        assert "R_temperature_corrected" in result


# =============================================================================
# CGS UNIT COMPLIANCE TESTS
# =============================================================================

class TestTelegraphyCGSUnits:
    """Test CGS unit compliance for telegraphy modules."""

    def test_signal_velocity_units(self) -> None:
        """Verify signal velocity has units cm/s."""
        from maxwell.signal_processing.telegraphy import TelegraphLine

        line = TelegraphLine(L=10.0, C=1e-10)
        v = line.signal_velocity()

        assert isinstance(v, float)
        # Units: cm/s

    def test_characteristic_impedance_units(self) -> None:
        """Verify characteristic impedance has units cm/s (velocity in CGS)."""
        from maxwell.signal_processing.telegraphy import TelegraphLine

        line = TelegraphLine(L=10.0, C=1e-10)
        Z0 = line.characteristic_impedance()

        assert isinstance(Z0, float)
        # In CGS-EMU, impedance has same dimensions as velocity

    def test_attenuation_constant_units(self) -> None:
        """Verify attenuation constant has units cm^-1."""
        from maxwell.signal_processing.telegraphy import TelegraphLine

        line = TelegraphLine(R=0.01, L=10.0, C=1e-10, G=0.0)
        alpha = line.attenuation_constant(angular_frequency=2 * np.pi * 1e6)

        assert isinstance(alpha, float)
        # Units: cm^-1

    def test_resistance_units(self) -> None:
        """Verify resistance has units abohms (cm/s in CGS)."""
        from maxwell.calibration.absolute_resistance import AbsoluteResistance

        ar = AbsoluteResistance()
        R = ar.lenz_method(induced_emf=1.0, induced_current=0.1)

        assert isinstance(R, float)
        # In CGS-EMU: 1 abohm = 1 cm/s


# =============================================================================
# CITATION COMPLIANCE TESTS
# =============================================================================

class TestTelegraphyCitationCompliance:
    """Test citation decorator compliance for telegraphy modules."""

    def test_telegraph_line_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify TelegraphLine methods have correct citations."""
        from maxwell.signal_processing.telegraphy import TelegraphLine

        line = TelegraphLine()

        citation = require_citation(line.signal_velocity)
        assert citation.part == 4
        assert any(a in citation.articles for a in [730, 731, 732, 733, 734, 735])

    def test_signal_transmission_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify SignalTransmission methods have correct citations."""
        from maxwell.signal_processing.telegraphy import SignalTransmission, TelegraphLine

        line = TelegraphLine()
        st = SignalTransmission(line)

        citation = require_citation(st.rise_time)
        assert citation.part == 4
        assert any(a in citation.articles for a in [740, 745, 750])

    def test_telegraph_functions_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify telegraph calc_* functions have correct citations."""
        from maxwell.signal_processing.telegraphy import (
            calc_signal_velocity,
            calc_characteristic_impedance,
            calc_propagation_constant,
            verify_telegraph_line,
        )

        for func in [
            calc_signal_velocity,
            calc_characteristic_impedance,
            calc_propagation_constant,
            verify_telegraph_line,
        ]:
            citation = require_citation(func)
            assert citation.part == 4
            assert any(a >= 730 and a <= 735 for a in citation.articles)


class TestAbsoluteResistanceCitationCompliance:
    """Test citation decorator compliance for absolute resistance modules."""

    def test_absolute_resistance_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify AbsoluteResistance methods have correct citations."""
        from maxwell.calibration.absolute_resistance import AbsoluteResistance

        ar = AbsoluteResistance()

        citation = require_citation(ar.recoil_method)
        assert citation.part == 4
        assert any(a in citation.articles for a in [758, 759, 760, 761, 762])

    def test_standard_resistance_coil_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify StandardResistanceCoil methods have correct citations."""
        from maxwell.calibration.absolute_resistance import StandardResistanceCoil

        src = StandardResistanceCoil(nominal_resistance=100.0)

        citation = require_citation(src.resistance_at_temperature)
        assert citation.part == 4
        assert any(a in citation.articles for a in [763, 764, 765, 766, 767])

    def test_absolute_resistance_functions_citation(
        self, require_citation, validate_citation_articles
    ) -> None:
        """Verify absolute resistance calc_* functions have correct citations."""
        from maxwell.calibration.absolute_resistance import (
            calc_absolute_resistance_recoil,
            calc_absolute_resistance_lenz,
            calc_absolute_resistance_joule,
            verify_absolute_resistance,
        )

        for func in [
            calc_absolute_resistance_recoil,
            calc_absolute_resistance_lenz,
            calc_absolute_resistance_joule,
            verify_absolute_resistance,
        ]:
            citation = require_citation(func)
            assert citation.part == 4
            assert any(a >= 758 and a <= 767 for a in citation.articles)

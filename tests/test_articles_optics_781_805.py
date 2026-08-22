"""Article-evidence tests for Part IV, Chapter XX — Arts. 781-805.

LAST200 Stage 4 (Cluster E): qualifying ``@pytest.mark.article(N)`` tests
for Maxwell's electromagnetic theory of light:

* Arts. 781-785: wave equation, dispersion relation, plane-wave solution
* Arts. 786-790: transversality, E/B relation, Poynting flux, energy
* Arts. 791-795: polarization states, Jones/Stokes calculus, wave plates
* Arts. 795-800: metallic reflection, skin depth, Hagen-Rubens limit
* Arts. 801-803: polarization classification, Stokes completeness,
  interference
* Arts. 804-805: crystal optics, uniaxial index identities

Every numerical expectation below is derived independently in the test
(hand algebra from Maxwell's CGS-Gaussian formulas) and never copied from
the implementation under test.  Tolerance classes follow Stage 4 sec. 2.5:
TIGHT 1e-10, STANDARD 1e-8, NUMERIC 1e-6, EMPIRICAL 1e-2.
"""

from __future__ import annotations

import numpy as np
import pytest

from maxwell.config.constants import CONST
from maxwell.electromagnetism.waves import plane_wave as em_pw
from maxwell.electromagnetism.waves import polarization as em_pol
from maxwell.electromagnetism.waves import wave_equation as em_we
from maxwell.optics import constants as optics_const
from maxwell.optics import crystals as optics_crystals
from maxwell.optics import metals as optics_metals
from maxwell.optics import plane_waves as optics_pw
from maxwell.optics import radiation_pressure as optics_rp
from maxwell.optics import velocity as optics_vel
from maxwell.optics import wave_equation as optics_we

from articles import ref_value, tolerance_of

# Tolerance classes (LAST200 Stage 4 sec. 2.5)
TIGHT = 1e-10
STANDARD = 1e-8
NUMERIC = 1e-6
EMPIRICAL = 1e-2


# =============================================================================
# Arts. 781-785: WAVE EQUATION AND DISPERSION RELATION
# =============================================================================


class TestWaveEquation781to785:
    """Wave equation derivation and vacuum plane-wave solution."""

    @pytest.mark.article(781)
    def test_781_vacuum_dispersion_relation(self) -> None:
        """Art. 781: vacuum waves obey omega = c|k|, i.e. v_phase = c.

        Independent oracle: omega/k must equal CONST.C, and a second
        implementation path (optics calc_wave_speed) must agree.
        """
        wave = em_we.ElectromagneticWave.from_frequency(5e14, 100.0)

        omega_over_k = wave.angular_frequency / wave.wave_number
        assert omega_over_k == pytest.approx(CONST.C, rel=STANDARD)
        assert wave.phase_velocity == pytest.approx(CONST.C, rel=STANDARD)

        # Cross-check with the independent optics-module code path
        v_optics = optics_we.calc_wave_speed(1.0, 1.0)
        assert v_optics == pytest.approx(omega_over_k, rel=TIGHT)

    @pytest.mark.article(782)
    def test_782_wave_satisfies_maxwell_equations(self) -> None:
        """Art. 782: plane wave satisfies all four Maxwell equations.

        Oracle: with B0 = (1/omega) k x E0 the Faraday/Ampere residuals
        vanish analytically; the Gauss-law residuals vanish because the
        construction is exactly transverse.  Residuals are asserted on
        their absolute magnitude, not just a boolean verdict.
        """
        wave = em_we.ElectromagneticWave.from_frequency(5e14, 100.0)
        result = em_we.verify_wave_equation(wave, test_points=12)

        assert result["all_verified"]
        # Divergence residuals: k.E0 = 0 by construction -> exactly 0
        assert result["divergence_E"]["max_residual"] < 1e-12
        assert result["divergence_B"]["max_residual"] < 1e-12
        # Curl residuals: analytic cancellation, ~ floating-point noise.
        # Term scale is E0*k ~ 1e7, so < 1e-6 is a ~1e-13 relative check.
        assert result["faraday"]["max_residual"] < 1e-6
        assert result["ampere_maxwell"]["max_residual"] < 1e-6

    @pytest.mark.article(783)
    def test_783_vacuum_speed_identity_from_emu_constants(self) -> None:
        """Art. 783 (required anchor): v = 1/sqrt(mu0*eps0) -> c.

        In CGS-EMU, eps0 = 1/c^2 and mu0 = 1, so the electromagnetic wave
        speed 1/sqrt(eps0*mu0) reproduces c identically.  Hand-derived,
        independent of any optics code path.
        """
        v_from_constants = 1.0 / np.sqrt(CONST.EPS0_EMU * CONST.MU0_EMU)
        assert v_from_constants == pytest.approx(CONST.C, rel=1e-12)

        # ESU convention from first principles: in CGS-ESU Coulomb's law
        # F = q1 q2 / r^2 fixes eps0 = 1, and the wave speed 1/sqrt(eps0
        # mu0) = c then fixes mu0 = 1/c^2.  (Derived independently; note
        # CONST.MU0_ESU stores the reciprocal convention c^2 — see report.)
        eps0_esu, mu0_esu = 1.0, 1.0 / CONST.C**2
        v_esu = 1.0 / np.sqrt(eps0_esu * mu0_esu)
        assert v_esu == pytest.approx(CONST.C, rel=1e-12)

    @pytest.mark.article(783)
    def test_783_vacuum_wave_speed_equals_c(self) -> None:
        """Art. 783: computed vacuum wave speed equals c (STANDARD tol)."""
        v = optics_we.calc_wave_speed(1.0, 1.0)
        assert v == pytest.approx(CONST.C, rel=STANDARD)

        result = optics_we.verify_speed_equals_c(tolerance=STANDARD)
        assert result["theoretical_speed"] == pytest.approx(CONST.C, rel=STANDARD)
        assert result["E0_B0_ratio_c"] == pytest.approx(CONST.C, rel=STANDARD)

    @pytest.mark.article(784)
    def test_784_medium_wave_speed(self) -> None:
        """Art. 784: v = c/sqrt(eps*mu) in a medium.

        Oracle: eps = 2.25 = (3/2)^2, mu = 1  =>  v = c / 1.5 exactly.
        """
        eps_r = 2.25
        v = optics_we.calc_wave_speed(eps_r, 1.0)
        assert v == pytest.approx(CONST.C / 1.5, rel=TIGHT)

        # Same relation via the velocity module (independent code path)
        v2 = optics_vel.calc_wave_velocity(eps_r, 1.0)
        assert v2 == pytest.approx(v, rel=TIGHT)

    @pytest.mark.article(784)
    def test_784_dispersionless_vacuum_and_medium(self) -> None:
        """Art. 784 (required anchor): dispersion-free limit.

        In a non-dispersive medium v = c/sqrt(eps*mu) is independent of
        frequency: two waves differing by 20% in frequency must travel
        at the same speed.
        """
        eps_r = 2.25
        expected_v = CONST.C / 1.5  # hand-derived

        wave1 = em_we.ElectromagneticWave.from_frequency(5e14, 100.0, epsilon=eps_r)
        wave2 = em_we.ElectromagneticWave.from_frequency(6e14, 100.0, epsilon=eps_r)

        assert wave1.phase_velocity == pytest.approx(expected_v, rel=STANDARD)
        assert wave2.phase_velocity == pytest.approx(expected_v, rel=STANDARD)
        # Frequency independence directly
        assert wave1.phase_velocity == pytest.approx(wave2.phase_velocity, rel=TIGHT)

        # Vacuum limit: same statement with eps = mu = 1
        w_red = em_we.ElectromagneticWave.from_frequency(4e14, 1.0)
        w_blue = em_we.ElectromagneticWave.from_frequency(7e14, 1.0)
        assert w_red.phase_velocity == pytest.approx(w_blue.phase_velocity, rel=TIGHT)
        assert w_red.phase_velocity == pytest.approx(CONST.C, rel=STANDARD)

    @pytest.mark.article(785)
    def test_785_plane_wave_fields_golden(self) -> None:
        """Art. 785: E(r,t) = E0 cos(k.r - omega t), B = (1/omega) k x E.

        Golden case, hand-derived: lambda = 1 cm (kz = 2*pi), r = lambda/8
        => phase = pi/4 at t = 0, so E_x = cos(pi/4); and
        B_y = kz/omega = 1/c when omega = c*kz.
        """
        lambda_cm = 1.0
        kz = 2.0 * np.pi / lambda_cm
        omega = CONST.C * kz
        E0 = np.array([1.0, 0.0, 0.0])

        E = optics_we.calc_plane_wave_E(
            np.array([0.0, 0.0, lambda_cm / 8.0]), 0.0, np.array([0.0, 0.0, kz]),
            omega, E0,
        )
        assert E[0] == pytest.approx(
            ref_value(785, "plane_wave_E_x_phase_pi4"),
            **tolerance_of(785, "plane_wave_E_x_phase_pi4"),
        )
        assert E[1] == pytest.approx(0.0, abs=1e-15)

        B = optics_we.calc_plane_wave_B_from_E(E0, np.array([0.0, 0.0, kz]), omega)
        assert B[1] == pytest.approx(
            ref_value(785, "plane_wave_B_y_amplitude"),
            **tolerance_of(785, "plane_wave_B_y_amplitude"),
        )
        assert B[0] == pytest.approx(0.0, abs=1e-25)
        assert B[2] == pytest.approx(0.0, abs=1e-25)

        # Same B from the wave-constructor path (independent code route)
        wave = optics_we.ElectromagneticWave.from_E_k_omega(
            E0, np.array([0.0, 0.0, kz]), omega
        )
        assert wave.amplitude_B[1] == pytest.approx(1.0 / CONST.C, rel=TIGHT)


# =============================================================================
# Arts. 786-790: TRANSVERSALITY, E/B RATIO, ENERGY AND POYNTING FLUX
# =============================================================================


class TestPlaneWaveProperties786to790:
    """Transverse structure and energetics of plane waves."""

    @pytest.mark.article(786)
    def test_786_transversality_k_dot_E(self) -> None:
        """Art. 786: k . E = 0 and k . B = 0 for EM plane waves.

        Oracle: an exactly orthogonal (k along z, E along x) construction
        must give a zero dot product and a 90-degree angle; a longitudinal
        field must be flagged non-transverse.
        """
        k = np.array([0.0, 0.0, 1e-4])
        E_trans = np.array([1000.0, 0.0, 0.0])

        result = optics_we.verify_transversality(k, E_trans)
        assert result["dot_product"] == pytest.approx(0.0, abs=1e-20)
        assert result["angle_degrees"] == pytest.approx(90.0, abs=1e-8)
        assert result["verified"]

        # Longitudinal field must fail the transversality check
        E_long = np.array([0.0, 0.0, 1000.0])
        result_long = optics_we.verify_transversality(k, E_long)
        assert not result_long["is_transverse"]

    @pytest.mark.article(786)
    def test_786_transversality_full_wave(self) -> None:
        """Art. 786: constructed plane wave is transverse in E and B."""
        wave = em_pw.PlaneWave.linearly_polarized(
            angular_frequency=2 * np.pi * 5e14,
            E0_magnitude=100.0,
            propagation_direction=np.array([0.0, 0.0, 1.0]),
            polarization_direction=np.array([1.0, 0.0, 0.0]),
        )
        result = em_pw.verify_transversality(wave)
        assert result["transverse_verified"]
        k_scale = wave.wave_number * 100.0
        assert abs(result["k_dot_E_real"]) < 1e-10 * k_scale
        assert abs(result["k_dot_B_real"]) < 1e-10 * k_scale

    @pytest.mark.article(787)
    def test_787_E_over_B_equals_c(self) -> None:
        """Art. 787: in vacuum |E|/|B| = c for a plane wave (TIGHT)."""
        wave = em_pw.PlaneWave.linearly_polarized(
            angular_frequency=2 * np.pi * 5e14,
            E0_magnitude=100.0,
            propagation_direction=np.array([0.0, 0.0, 1.0]),
            polarization_direction=np.array([1.0, 0.0, 0.0]),
        )
        fields = wave.fields_at(np.zeros(3), 0.0)
        ratio = fields["E_magnitude"] / fields["B_magnitude"]
        assert ratio == pytest.approx(CONST.C, rel=TIGHT)

        # Velocity-module statement of the same law (independent path)
        assert optics_vel.calc_E_B_ratio(1.0, 1.0) == pytest.approx(CONST.C, rel=TIGHT)

    @pytest.mark.article(787)
    def test_787_E_B_ratio_in_medium(self) -> None:
        """Art. 787: in a medium |E|/|B| = v = c/n, n = sqrt(eps*mu).

        Oracle: eps = 4, mu = 1 => n = 2 => |E|/|B| = c/2.
        """
        ratio = optics_vel.calc_E_B_ratio(4.0, 1.0)
        assert ratio == pytest.approx(CONST.C / 2.0, rel=TIGHT)
        assert optics_vel.calc_refractive_index(4.0, 1.0) == pytest.approx(2.0, rel=TIGHT)

    @pytest.mark.article(788)
    def test_788_poynting_vector_golden(self) -> None:
        """Art. 788: S = (c/4pi) E x B.

        Golden case: E = x_hat, B = y_hat  =>  S = (c/4pi) z_hat, derived
        directly from the definition (no implementation constants reused).
        """
        S = optics_we.calc_poynting_vector(
            np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0])
        )
        expected_mag = ref_value(788, "poynting_flux_unit_fields")
        assert S[2] == pytest.approx(
            expected_mag, **tolerance_of(788, "poynting_flux_unit_fields")
        )
        assert S[0] == pytest.approx(0.0, abs=1e-20)
        assert S[1] == pytest.approx(0.0, abs=1e-20)

    @pytest.mark.article(788)
    def test_788_intensity_golden(self) -> None:
        """Art. 788-789: I = <S> = (c/8pi) E0^2 (cycle average of cos^2).

        Oracle: the time average of cos^2 is 1/2, so I is exactly half the
        peak flux (c/4pi) E0^2.
        """
        E0 = np.array([1000.0, 0.0, 0.0])
        I = optics_we.calc_wave_intensity(E0)
        assert I == pytest.approx(CONST.C * 1e6 / (8.0 * np.pi), rel=TIGHT)

        peak_flux = CONST.C * 1e6 / (4.0 * np.pi)
        assert I == pytest.approx(0.5 * peak_flux, rel=TIGHT)

        # Same law through the wave object (independent code path)
        wave = optics_we.ElectromagneticWave.from_E_k_omega(
            E0, np.array([0.0, 0.0, 1e-4]), CONST.C * 1e-4
        )
        assert wave.intensity() == pytest.approx(I, rel=TIGHT)

    @pytest.mark.article(789)
    def test_789_energy_density_golden(self) -> None:
        """Art. 789: u = (E^2 + B^2)/(8pi).

        Golden case: unit orthogonal fields give u = 2/(8pi) = 1/(4pi).
        For a vacuum plane wave |E| = |B|, hence u = E0^2/(4pi).
        """
        u = optics_we.calc_energy_density(
            np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0])
        )
        assert u == pytest.approx(
            ref_value(789, "energy_density_unit_fields"),
            **tolerance_of(789, "energy_density_unit_fields"),
        )

        E0 = 100.0
        wave = optics_we.ElectromagneticWave.from_E_k_omega(
            np.array([E0, 0.0, 0.0]),
            np.array([0.0, 0.0, 1e-4]),
            CONST.C * 1e-4,
        )
        # With stored B = E0/c and physical B_gauss = c*B, the peak energy
        # is u = (E0^2 + c^2 (E0/c)^2)/(8pi) = E0^2/(4pi) exactly.
        u_peak = wave.energy_density()
        assert u_peak == pytest.approx(E0**2 / (4.0 * np.pi), rel=STANDARD)

        # Art. 788-789 consistency: energy flows at speed c, so the
        # cycle-averaged density <u> = u_peak/2 obeys I = c <u>.
        assert wave.intensity() == pytest.approx(
            CONST.C * 0.5 * u_peak, rel=STANDARD
        )

    @pytest.mark.article(790)
    def test_790_wavelength_frequency_relations(self) -> None:
        """Art. 790: lambda = v/nu, lambda_medium = lambda0/n, nu invariant.

        Oracle: a vacuum/medium round trip must return the original
        frequency, and the medium wavelength is shorter by exactly n.
        """
        nu = 5e14
        n = 1.5

        lambda0 = optics_const.calc_wavelength_from_frequency(nu)
        assert lambda0 == pytest.approx(CONST.C / nu, rel=TIGHT)

        nu_back = optics_const.calc_frequency_from_wavelength(lambda0)
        assert nu_back == pytest.approx(nu, rel=TIGHT)  # frequency invariant

        lambda_med = optics_vel.calc_wavelength_in_medium(lambda0, n)
        assert lambda_med == pytest.approx(lambda0 / n, rel=TIGHT)

        # Wavelength from (frequency, speed) — independent route
        lambda_from_speed = optics_we.calc_wavelength(nu, CONST.C / n)
        assert lambda_from_speed == pytest.approx(lambda_med, rel=TIGHT)


# =============================================================================
# Arts. 791-795: POLARIZATION, JONES AND STOKES CALCULUS
# =============================================================================


class TestPolarization791to795:
    """Jones/Stokes polarization calculus and wave plates."""

    @pytest.mark.article(791)
    def test_791_linear_polarization_malus(self) -> None:
        """Art. 791: linear polarization and Malus's law via Jones matrices.

        Oracle: x-polarized unit light through a polarizer at theta = pi/3
        transmits cos^2(pi/3) = 1/4 of the intensity.
        """
        P = em_pol.Jones_linear_polarizer(np.pi / 3)
        J_in = np.array([1.0, 0.0], dtype=complex)
        J_out = P @ J_in

        transmitted = float(np.vdot(J_out, J_out).real)
        assert transmitted == pytest.approx(np.cos(np.pi / 3) ** 2, rel=TIGHT)
        assert transmitted == pytest.approx(
            ref_value(791, "malus_transmission_pi_over_3"),
            **tolerance_of(791, "malus_transmission_pi_over_3"),
        )

        # Jones vector of a linear state at angle theta
        st = em_pol.PolarizationState.linear(np.pi / 6, amplitude=1.0)
        J = st.Jones_vector
        assert abs(J[0]) == pytest.approx(np.cos(np.pi / 6), rel=TIGHT)
        assert abs(J[1]) == pytest.approx(np.sin(np.pi / 6), rel=TIGHT)
        assert st.polarization_type == "linear"

    @pytest.mark.article(792)
    def test_792_circular_polarization_stokes(self) -> None:
        """Art. 792: circular polarization has Stokes [2, 0, 0, +/-2].

        Hand-derived: E1 = E2 = 1, delta = +/-pi/2 gives
        S0 = 2, S1 = 0, S2 = 2cos(+/-pi/2) = 0, S3 = 2sin(+/-pi/2) = +/-2.
        """
        right = em_pol.PolarizationState.circular("right", amplitude=1.0)
        S_r = right.Stokes_parameters
        assert S_r[0] == pytest.approx(2.0, rel=TIGHT)
        assert S_r[1] == pytest.approx(0.0, abs=1e-12)
        assert S_r[2] == pytest.approx(0.0, abs=1e-12)
        assert S_r[3] == pytest.approx(2.0, rel=TIGHT)
        assert right.polarization_type == "circular"
        assert right.handedness == "right"

        left = em_pol.PolarizationState.circular("left", amplitude=1.0)
        assert left.Stokes_parameters[3] == pytest.approx(-2.0, rel=TIGHT)
        assert left.handedness == "left"

    @pytest.mark.article(793)
    def test_793_elliptical_polarization_stokes_identity(self) -> None:
        """Art. 793: elliptical state (E1, E2, delta) = (2, 1, pi/2).

        Hand-derived Stokes: S0 = 5, S1 = 3, S2 = 0, S3 = 4, which
        satisfies the pure-state identity 5^2 = 3^2 + 0^2 + 4^2.
        """
        st = em_pol.PolarizationState.elliptical(2.0, 1.0, np.pi / 2)
        S = st.Stokes_parameters
        assert S[0] == pytest.approx(5.0, rel=TIGHT)
        assert S[1] == pytest.approx(3.0, rel=TIGHT)
        assert S[2] == pytest.approx(0.0, abs=1e-12)
        assert S[3] == pytest.approx(4.0, rel=TIGHT)
        assert S[0] ** 2 == pytest.approx(S[1] ** 2 + S[2] ** 2 + S[3] ** 2, rel=TIGHT)
        assert st.polarization_type == "elliptical"

    @pytest.mark.article(794)
    def test_794_half_wave_plate_flips_polarization(self) -> None:
        """Art. 794: HWP at fast axis 45 deg maps x -> y polarization.

        Hand-derived via rotation matrices:
        M = R(-pi/4) diag(1, e^{-i pi}) R(pi/4), M [1,0]^T = [0,1]^T.
        """
        M = em_pol.Jones_wave_plate(np.pi, fast_axis=np.pi / 4)
        J_out = M @ np.array([1.0, 0.0], dtype=complex)

        assert abs(J_out[0]) < 1e-10
        assert abs(abs(J_out[1]) - 1.0) < 1e-10

        # Ellipse parameters of a linear state: infinite axial ratio
        # (pytest.approx cannot wrap inf, so assert equality directly)
        st = em_pol.PolarizationState.linear(0.3, amplitude=1.0)
        ell = st.ellipse_parameters()
        assert ell["axial_ratio"] == float("inf")
        assert ell["minor_axis"] == pytest.approx(0.0, abs=1e-10)

    @pytest.mark.article(794)
    def test_794_snell_refraction_golden(self) -> None:
        """Art. 794: Snell's law theta2 = arcsin(sin(theta1)/n).

        Golden case: 30-degree incidence into n = 1.5 gives
        theta2 = arcsin(1/3), derived independently.
        """
        theta2 = optics_crystals.calc_refraction_angle(np.pi / 6, 1.5)
        assert theta2 == pytest.approx(np.arcsin(1.0 / 3.0), rel=TIGHT)
        assert theta2 < np.pi / 6  # refraction bends toward the normal

    @pytest.mark.article(795)
    def test_795_quarter_wave_plate_makes_circular(self) -> None:
        """Art. 795: QWP converts 45-deg linear light to circular.

        Hand-derived: M = diag(1, e^{-i pi/2}) sends [1,1]/sqrt(2) to
        [1, -i]/sqrt(2), whose Stokes vector has |S3| = S0 and S1=S2=0.
        Also checks wave-plate unitarity M^dag M = I (energy conservation).
        """
        M = em_pol.Jones_wave_plate(np.pi / 2, fast_axis=0.0)
        J_in = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2)
        J_out = M @ J_in

        E1 = abs(J_out[0])
        E2 = abs(J_out[1])
        delta = np.angle(J_out[1]) - np.angle(J_out[0])
        S = em_pol.calc_Stokes_parameters(E1, E2, delta)
        assert S["S0"] == pytest.approx(1.0, rel=TIGHT)
        assert S["S1"] == pytest.approx(0.0, abs=1e-12)
        assert S["S2"] == pytest.approx(0.0, abs=1e-12)
        assert abs(S["S3"]) == pytest.approx(1.0, rel=TIGHT)  # fully circular

        # Unitarity for an arbitrary retardance and fast-axis angle
        M2 = em_pol.Jones_wave_plate(1.234, fast_axis=0.7)
        product = M2.conj().T @ M2
        np.testing.assert_allclose(product, np.eye(2), atol=1e-12)


# =============================================================================
# Arts. 795-800: METALLIC REFLECTION, SKIN DEPTH, HAGEN-RUBENS
# =============================================================================


class TestMetalOptics795to800:
    """Optical behavior of metals from finite conductivity."""

    @pytest.mark.article(796)
    def test_796_fresnel_normal_incidence_equality(self) -> None:
        """Art. 796: at normal incidence r_p = -r_s, so R_s = R_p.

        Oracle: with cos(theta1) = cos(theta2) = 1 the complex Fresnel
        formulas reduce to r_s = (n1 - n2)/(n1 + n2), r_p = -r_s.
        """
        mr = optics_metals.MetallicReflection(n1=1.0, n2_real=0.05, kappa=3.88)
        r_s = mr.reflection_perpendicular(0.0)
        r_p = mr.reflection_parallel(0.0)

        assert r_p == pytest.approx(-r_s, rel=TIGHT)
        assert abs(r_s) ** 2 == pytest.approx(abs(r_p) ** 2, rel=TIGHT)

    @pytest.mark.article(797)
    def test_797_normal_reflectance_golden(self) -> None:
        """Art. 797: R = [(n1-n)^2 + kappa^2] / [(n1+n)^2 + kappa^2].

        Golden case derived in-test for silver (n, kappa) = (0.05, 3.88):
        numerator = 0.95^2 + 3.88^2, denominator = 1.05^2 + 3.88^2.
        """
        n, kappa = 0.05, 3.88
        # Golden pinned in the reference store: numerator 0.95^2 + 3.88^2,
        # denominator 1.05^2 + 3.88^2 (hand arithmetic).
        expected = ref_value(797, "silver_normal_reflectance")

        R = optics_metals.calc_metal_reflectance_normal(1.0, n, kappa)
        assert R == pytest.approx(
            expected, **tolerance_of(797, "silver_normal_reflectance")
        )
        assert R > 0.95  # silver is highly reflective

        # Same value from the class interface (independent code path)
        mr = optics_metals.MetallicReflection(n1=1.0, n2_real=n, kappa=kappa)
        assert mr.normal_reflectance() == pytest.approx(R, rel=TIGHT)
        assert mr.reflectance(0.0, "unpolarized") == pytest.approx(R, rel=NUMERIC)

    @pytest.mark.article(798)
    def test_798_skin_depth_conductivity_golden(self) -> None:
        """Art. 798: delta = c / sqrt(2 pi sigma omega).

        Independent oracle: the kappa-based optical formula
        delta = lambda0/(2 pi kappa) with the good-conductor extinction
        kappa = sqrt(2 pi sigma / omega) and lambda0 = 2 pi c / omega
        reduces algebraically to c/sqrt(2 pi sigma omega).  The two
        independent implementations must therefore agree exactly.
        """
        sigma = optics_metals.COPPER_CONDUCTIVITY_CGS
        omega = 2.0 * np.pi * 1e6

        delta_sigma = optics_metals.calc_skin_depth(sigma, omega)
        expected = CONST.C / np.sqrt(2.0 * np.pi * sigma * omega)
        assert delta_sigma == pytest.approx(expected, rel=TIGHT)

        kappa_good = np.sqrt(2.0 * np.pi * sigma / omega)
        lambda0 = 2.0 * np.pi * CONST.C / omega
        delta_kappa = optics_metals.calc_skin_depth_from_kappa(lambda0, kappa_good)
        assert delta_kappa == pytest.approx(delta_sigma, rel=STANDARD)

    @pytest.mark.article(798)
    def test_798_skin_depth_limit_behavior(self) -> None:
        """Art. 798 (required anchor): skin-depth limit behavior.

        From delta = c/sqrt(2 pi sigma omega): quadrupling omega halves
        delta (1/sqrt(omega) scaling), and delta -> 0 as sigma -> infinity
        (perfect conductor excludes the field).
        """
        sigma = optics_metals.COPPER_CONDUCTIVITY_CGS
        omega = 2.0 * np.pi * 1e6

        delta1 = optics_metals.calc_skin_depth(sigma, omega)
        delta4 = optics_metals.calc_skin_depth(sigma, 4.0 * omega)
        assert delta1 / delta4 == pytest.approx(2.0, rel=STANDARD)

        delta_high_sigma = optics_metals.calc_skin_depth(1e6 * sigma, omega)
        assert delta_high_sigma / delta1 == pytest.approx(1e-3, rel=STANDARD)
        assert delta_high_sigma < delta1

    @pytest.mark.article(799)
    def test_799_absorption_coefficient_identities(self) -> None:
        """Art. 799 (required anchor): absorption limit behaviors.

        Hand-derived identities: the intensity absorption coefficient
        alpha = 4 pi kappa / lambda0 satisfies alpha * delta = 2 when
        delta = lambda0/(2 pi kappa) is the field-amplitude 1/e depth;
        the amplitude coefficient is alpha_amp = 1/delta.
        """
        sigma = optics_metals.COPPER_CONDUCTIVITY_CGS
        omega = 2.0 * np.pi * 1e14
        kappa_good = np.sqrt(2.0 * np.pi * sigma / omega)
        lambda0 = 2.0 * np.pi * CONST.C / omega

        delta = optics_metals.calc_skin_depth_from_kappa(lambda0, kappa_good)
        alpha_int = optics_metals.calc_absorption_coefficient_from_kappa(
            lambda0, kappa_good
        )
        assert alpha_int * delta == pytest.approx(2.0, rel=TIGHT)
        assert alpha_int == pytest.approx(4.0 * np.pi * kappa_good / lambda0, rel=TIGHT)

        delta_sigma = optics_metals.calc_skin_depth(sigma, omega)
        alpha_amp = optics_metals.calc_absorption_coefficient(delta_sigma)
        assert alpha_amp == pytest.approx(1.0 / delta_sigma, rel=TIGHT)

    @pytest.mark.article(800)
    def test_800_hagen_rubens_against_fresnel_oracle(self) -> None:
        """Art. 800: Hagen-Rubens reflectivity.

        Independent oracle: in the good-conductor limit the complex index
        is n2~ = (1+i) sqrt(2 pi sigma / omega) (from n2~^2 = 4 pi i sigma
        / omega), and exact normal-incidence Fresnel reflection off that
        index gives R = [(1-n)^2 + n^2]/[(1+n)^2 + n^2], which expands to
        1 - 2 sqrt(omega/(2 pi sigma)) + O(omega/sigma).  The two routes
        must agree at optical frequencies for copper.
        """
        sigma = optics_metals.COPPER_CONDUCTIVITY_CGS
        omega = 2.0 * np.pi * 1e14

        R_hr = optics_metals.calc_metal_reflectivity(sigma, omega)

        n_good = np.sqrt(2.0 * np.pi * sigma / omega)
        R_fresnel = ((1.0 - n_good) ** 2 + n_good**2) / (
            (1.0 + n_good) ** 2 + n_good**2
        )
        assert R_hr == pytest.approx(R_fresnel, abs=EMPIRICAL / 2)
        assert 0.9 < R_hr < 1.0

    @pytest.mark.article(800)
    def test_800_hagen_rubens_limit_behavior(self) -> None:
        """Art. 800 (required anchor): R -> 1 as sigma -> infinity.

        Hand-derived: 1 - R = 2 sqrt(omega/(2 pi sigma)) scales as
        sigma^{-1/2}, so raising sigma by 100x shrinks (1 - R) by 10x.
        """
        omega = 2.0 * np.pi * 1e14
        sigma = optics_metals.COPPER_CONDUCTIVITY_CGS

        deficit = 1.0 - optics_metals.calc_metal_reflectivity(sigma, omega)
        deficit_100 = 1.0 - optics_metals.calc_metal_reflectivity(100.0 * sigma, omega)
        assert deficit_100 / deficit == pytest.approx(
            ref_value(800, "hagen_rubens_deficit_ratio_100x_sigma"),
            **tolerance_of(800, "hagen_rubens_deficit_ratio_100x_sigma"),
        )
        assert deficit_100 < deficit  # better conductor reflects more


# =============================================================================
# Arts. 791-794 (RADIATION PRESSURE): MECHANICAL ACTION OF LIGHT
# =============================================================================


class TestRadiationPressure791to794:
    """Radiation pressure golden cases (independent in-test derivations)."""

    @pytest.mark.article(791)
    def test_791_radiation_pressure_absorber_golden(self) -> None:
        """Art. 791: P = u = I/c on an absorbing surface.

        Golden case: I = c erg/(cm^2 s) gives P = 1 dyne/cm^2 exactly
        (1 erg/cm^3 = 1 dyne/cm^2).  Also cross-checks the two
        independent code paths P = u and u = I/c.
        """
        P = optics_rp.calc_pressure_from_intensity(CONST.C)
        assert P == pytest.approx(
            ref_value(791, "radiation_pressure_absorber_I_eq_c"),
            **tolerance_of(791, "radiation_pressure_absorber_I_eq_c"),
        )
        assert optics_rp.calc_radiation_pressure(1.0) == pytest.approx(1.0, rel=TIGHT)

        I = 1e6
        u = optics_rp.calc_energy_density_from_intensity(I)
        P_abs = optics_rp.calc_pressure_from_intensity(I)
        # Two independent routes both yield I/c
        assert u == pytest.approx(I / CONST.C, rel=TIGHT)
        assert P_abs == pytest.approx(u, rel=TIGHT)
        assert optics_rp.calc_radiation_pressure(u) == pytest.approx(P_abs, rel=TIGHT)

    @pytest.mark.article(792)
    def test_792_radiation_pressure_reflector_golden(self) -> None:
        """Art. 792: perfect reflection doubles the pressure, P = 2u.

        Hand-derived: reversing the momentum of the reflected wave
        transfers twice the momentum flux, hence P_refl = 2 P_abs.
        """
        u = 1.0
        assert optics_rp.calc_radiation_pressure_reflection(u) == pytest.approx(
            ref_value(792, "radiation_pressure_reflector_unit_u"),
            **tolerance_of(792, "radiation_pressure_reflector_unit_u"),
        )

        I = 1e6
        u_wave = optics_rp.calc_energy_density_from_intensity(I)
        P_abs = optics_rp.calc_radiation_pressure(u_wave)
        P_refl = optics_rp.calc_radiation_pressure_reflection(u_wave)
        assert P_refl == pytest.approx(2.0 * P_abs, rel=TIGHT)
        assert P_refl == pytest.approx(2.0 * I / CONST.C, rel=TIGHT)

    @pytest.mark.article(793)
    def test_793_radiation_pressure_oblique_golden(self) -> None:
        """Art. 793: oblique incidence carries a cos^2(theta) factor.

        Golden case: theta = pi/3 gives cos^2 = 1/4, so the pressure is
        one quarter of the normal-incidence value.  Limits: full pressure
        at theta = 0, zero pressure at grazing incidence.
        """
        I = 1e6
        P_normal = I / CONST.C  # hand-derived

        P_60 = optics_rp.calc_radiation_pressure_oblique(I, np.pi / 3)
        assert P_60 == pytest.approx(
            ref_value(793, "oblique_pressure_cos2_pi_over_3") * P_normal,
            **tolerance_of(793, "oblique_pressure_cos2_pi_over_3"),
        )

        P_0 = optics_rp.calc_radiation_pressure_oblique(I, 0.0)
        assert P_0 == pytest.approx(P_normal, rel=TIGHT)

        P_grazing = optics_rp.calc_radiation_pressure_oblique(I, np.pi / 2)
        assert P_grazing == pytest.approx(0.0, abs=1e-25)

    @pytest.mark.article(794)
    def test_794_radiation_force_and_momentum_golden(self) -> None:
        """Arts. 791-794: F = P A and p = E/c.

        Golden cases, hand-derived:
        - F = 2 I A / c for a perfect reflector at normal incidence;
        - p = E/c gives p = 1 g.cm/s for E = c ergs.
        """
        I, A = 1e6, 10.0
        F_refl = optics_rp.calc_radiation_force(I, A, reflecting=True)
        assert F_refl == pytest.approx(2.0 * I * A / CONST.C, rel=TIGHT)

        F_abs = optics_rp.calc_radiation_force(I, A, reflecting=False)
        assert F_abs == pytest.approx(I * A / CONST.C, rel=TIGHT)
        assert F_refl == pytest.approx(2.0 * F_abs, rel=TIGHT)

        assert optics_rp.calc_radiation_momentum(CONST.C) == pytest.approx(
            ref_value(794, "radiation_momentum_E_eq_c"),
            **tolerance_of(794, "radiation_momentum_E_eq_c"),
        )
        # Consistency with the pressure calculator dataclass route
        rp = optics_rp.RadiationPressure()
        u = optics_rp.calc_energy_density_from_intensity(I)
        assert rp.force_on_area(optics_rp.calc_radiation_pressure_reflection(u), A) \
            == pytest.approx(F_refl, rel=TIGHT)


# =============================================================================
# Arts. 801-803: POLARIZATION CLASSIFICATION, STOKES, INTERFERENCE
# =============================================================================


class TestPolarizationStates801to803:
    """Polarization classification, completeness, and interference."""

    @pytest.mark.article(801)
    def test_801_polarization_classification(self) -> None:
        """Art. 801: linear / circular / elliptical classification.

        Hand-derived cases: delta = 0 is linear; E0x = E0y with
        delta = pi/2 is circular; unequal amplitudes with generic delta
        is elliptical.  Intensity is (c/8pi)(E0x^2 + E0y^2).
        """
        lin = optics_pw.PolarizationState.linear_polarization(1.0, np.pi / 6)
        assert lin.polarization_type() == "linear"

        circ = optics_pw.PolarizationState.circular_polarization(1.0, "right")
        assert circ.polarization_type().startswith("circular")

        ell = optics_pw.PolarizationState.elliptical_polarization(2.0, 1.0, np.pi / 3)
        assert ell.polarization_type() == "elliptical"

        I = optics_pw.calc_polarized_wave_intensity(3.0, 4.0)
        assert I == pytest.approx(CONST.C * 25.0 / (8.0 * np.pi), rel=TIGHT)

    @pytest.mark.article(802)
    def test_802_polarization_ellipse_limits(self) -> None:
        """Art. 802: polarization ellipse in the linear and circular limits.

        Hand-derived: linear light has zero ellipticity; circular light has
        |ellipticity| = 1 with equal axes; in general a^2 + b^2 = E0x^2 +
        E0y^2 (energy conservation across the ellipse axes).
        """
        lin = optics_pw.calc_polarization_ellipse(1.0, 0.0, 0.0)
        assert lin["ellipticity"] == pytest.approx(0.0, abs=1e-12)
        assert lin["handedness"] == "none"

        circ = optics_pw.calc_polarization_ellipse(1.0, 1.0, np.pi / 2)
        assert abs(circ["ellipticity"]) == pytest.approx(1.0, rel=TIGHT)
        assert circ["semi_major_axis"] == pytest.approx(
            circ["semi_minor_axis"], rel=TIGHT
        )
        assert circ["handedness"] == "right"

        gen = optics_pw.calc_polarization_ellipse(2.0, 1.0, np.pi / 6)
        a, b = gen["semi_major_axis"], gen["semi_minor_axis"]
        assert a**2 + b**2 == pytest.approx(2.0**2 + 1.0**2, rel=STANDARD)

    @pytest.mark.article(803)
    def test_803_stokes_completeness_identity(self) -> None:
        """Art. 803 (required anchor): S0^2 = S1^2 + S2^2 + S3^2.

        Hand-derived for (E0x, E0y, delta) = (3, 4, pi/7):
        I = 25, Q = -7, and U^2 + V^2 = (2 E0x E0y)^2 = 576 exactly,
        so I^2 = 49 + 576 = 625.  Checked in two independent modules.
        """
        delta = np.pi / 7
        ps = optics_pw.PolarizationState(
            Ex_amplitude=3.0, Ey_amplitude=4.0, phase_difference=delta
        )
        I, Q, U, V = ps.stokes_parameters()
        assert I == pytest.approx(
            ref_value(803, "stokes_I_3_4_pi7"),
            **tolerance_of(803, "stokes_I_3_4_pi7"),
        )
        assert Q == pytest.approx(
            ref_value(803, "stokes_Q_3_4_pi7"),
            **tolerance_of(803, "stokes_Q_3_4_pi7"),
        )
        assert U**2 + V**2 == pytest.approx(
            ref_value(803, "stokes_U2_plus_V2_3_4_pi7"),
            **tolerance_of(803, "stokes_U2_plus_V2_3_4_pi7"),
        )
        assert I**2 == pytest.approx(Q**2 + U**2 + V**2, rel=TIGHT)

        # Same statement through the waves-module Stokes calculator
        S = em_pol.calc_Stokes_parameters(3.0, 4.0, delta)
        assert S["S0"] == pytest.approx(I, rel=TIGHT)
        assert S["degree_of_polarization"] == pytest.approx(1.0, rel=TIGHT)

    @pytest.mark.article(803)
    def test_803_interference_limits_and_visibility(self) -> None:
        """Art. 803: interference and fringe visibility.

        Hand-derived: I = I1 + I2 + 2 sqrt(I1 I2) cos(dphi) gives
        I_max = (sqrt(I1) + sqrt(I2))^2 and I_min = (sqrt(I1) - sqrt(I2))^2;
        for I1 = 4 I2 the visibility is (9-1)/(9+1) = 0.8.
        """
        I1, I2 = 4.0, 1.0
        I_max = optics_pw.calc_wave_interference(I1, I2, 0.0)
        I_min = optics_pw.calc_wave_interference(I1, I2, np.pi)
        assert I_max == pytest.approx((2.0 + 1.0) ** 2, rel=TIGHT)
        assert I_min == pytest.approx((2.0 - 1.0) ** 2, rel=TIGHT)

        V = optics_pw.calc_fringe_visibility(I_max, I_min)
        assert V == pytest.approx(
            ref_value(803, "fringe_visibility_4_to_1"),
            **tolerance_of(803, "fringe_visibility_4_to_1"),
        )

        # Equal beams: perfect constructive/destructive limits
        assert optics_pw.calc_wave_interference(1.0, 1.0, 0.0) == pytest.approx(
            4.0, rel=TIGHT
        )
        assert optics_pw.calc_wave_interference(1.0, 1.0, np.pi) == pytest.approx(
            0.0, abs=1e-12
        )
        assert optics_pw.calc_fringe_visibility(4.0, 0.0) == pytest.approx(1.0, rel=TIGHT)


# =============================================================================
# Arts. 804-805: CRYSTAL OPTICS, UNIAXIAL INDICES, FRESNEL NORMALS
# =============================================================================


class TestCrystalOptics804to805:
    """Birefringence and uniaxial wave-normal propagation."""

    @pytest.mark.article(804)
    def test_804_ordinary_extraordinary_velocities(self) -> None:
        """Art. 804 (required anchor): uniaxial o/e identities.

        Hand-derived for calcite (n_o, n_e) = (1.658, 1.486):
        v_o = c/n_o, v_e = c/n_e, Delta n = n_e - n_o = -0.172, and the
        optical path difference is |Delta n| d.
        """
        n_o, n_e = 1.658, 1.486
        co = optics_crystals.CrystalOptics(n_o=n_o, n_e=n_e)

        assert co.ordinary_velocity() == pytest.approx(CONST.C / n_o, rel=TIGHT)
        assert co.extraordinary_velocity() == pytest.approx(CONST.C / n_e, rel=TIGHT)
        assert co.birefringence() == pytest.approx(n_e - n_o, rel=TIGHT)
        assert co.crystal_type == "negative"  # calcite: n_e < n_o

        d = 1e-3
        assert co.path_difference(d) == pytest.approx(abs(n_e - n_o) * d, rel=TIGHT)
        lam = optics_crystals.SODIUM_D_LINE_CM
        Gamma = co.retardation(d, lam)
        assert Gamma == pytest.approx(
            2.0 * np.pi * abs(n_e - n_o) * d / lam, rel=TIGHT
        )

    @pytest.mark.article(804)
    def test_804_wave_plate_thickness_round_trip(self) -> None:
        """Art. 804: quarter/half-wave plate thicknesses.

        Hand-derived round trip: d_{lambda/4} = lambda/(4|Delta n|) must
        produce retardation Gamma = pi/2 when substituted back into
        Gamma = (2pi/lambda)|Delta n| d; likewise pi for the half-wave
        plate.  Also N = |Delta n| d / lambda retardation in waves.
        """
        n_o, n_e = 1.544, 1.553
        lam = optics_crystals.SODIUM_D_LINE_CM
        co = optics_crystals.CrystalOptics(n_o=n_o, n_e=n_e)

        d_qwp = co.quarter_wave_thickness(lam)
        assert d_qwp == pytest.approx(lam / (4.0 * abs(n_e - n_o)), rel=TIGHT)
        assert co.retardation(d_qwp, lam) == pytest.approx(np.pi / 2, rel=STANDARD)

        d_hwp = co.half_wave_thickness(lam)
        assert d_hwp == pytest.approx(2.0 * d_qwp, rel=TIGHT)
        assert co.retardation(d_hwp, lam) == pytest.approx(np.pi, rel=STANDARD)

        d = 1e-3
        N = optics_crystals.calc_retardation_waves(d, n_e - n_o, lam)
        assert N == pytest.approx(abs(n_e - n_o) * d / lam, rel=TIGHT)

    @pytest.mark.article(805)
    def test_805_uniaxial_index_identities(self) -> None:
        """Art. 805 (required anchor): n_eff(0) = n_o, n_eff(pi/2) = n_e.

        Along the optic axis the extraordinary wave sees the ordinary
        index; perpendicular to it, the principal extraordinary index.
        """
        n_o, n_e = 1.658, 1.486

        assert optics_crystals.calc_effective_index(n_o, n_e, 0.0) == pytest.approx(
            n_o, rel=TIGHT
        )
        assert optics_crystals.calc_effective_index(
            n_o, n_e, np.pi / 2
        ) == pytest.approx(n_e, rel=STANDARD)

        co = optics_crystals.CrystalOptics(n_o=n_o, n_e=n_e)
        assert co.effective_index_at_angle(0.0) == pytest.approx(n_o, rel=TIGHT)

    @pytest.mark.article(805)
    def test_805_fresnel_normal_equation(self) -> None:
        """Art. 805 (required anchor): Fresnel wave-normal equation.

        For a uniaxial crystal the wave-normal index satisfies
            1/n(theta)^2 = cos^2(theta)/n_o^2 + sin^2(theta)/n_e^2.
        Verified at theta = pi/4 against a hand-evaluated oracle, and at
        the two principal directions (covered by the identity test).
        """
        n_o, n_e = 1.658, 1.486
        theta = np.pi / 4

        expected = 1.0 / np.sqrt(
            np.cos(theta) ** 2 / n_o**2 + np.sin(theta) ** 2 / n_e**2
        )
        n_eff = optics_crystals.calc_effective_index(n_o, n_e, theta)
        assert n_eff == pytest.approx(expected, rel=TIGHT)

        # For a negative crystal n_e < n_eff(theta) < n_o off-axis
        assert n_e < n_eff < n_o

    @pytest.mark.article(805)
    def test_805_crystal_sign_and_velocity_ordering(self) -> None:
        """Art. 805: positive vs negative crystals order the ray speeds.

        Hand-derived: v = c/n, so a negative crystal (n_e < n_o) has the
        extraordinary ray faster (v_e > v_o), and a positive crystal the
        reverse.  Uses the provenance table entries directly.
        """
        calcite = optics_crystals.get_crystal_constants("calcite")
        quartz = optics_crystals.get_crystal_constants("quartz")

        assert calcite["type"] == "negative"
        assert quartz["type"] == "positive"

        v_o_cal = optics_crystals.calc_velocity_difference(
            calcite["n_o"], calcite["n_e"]
        )
        # v_o - v_e < 0 for a negative crystal (e-ray is faster)
        assert v_o_cal < 0

        v_o_qtz = optics_crystals.calc_velocity_difference(
            quartz["n_o"], quartz["n_e"]
        )
        assert v_o_qtz > 0

        # Magnitude oracle for calcite: c(1/n_o - 1/n_e), hand formula
        expected = CONST.C * (1.0 / calcite["n_o"] - 1.0 / calcite["n_e"])
        assert v_o_cal == pytest.approx(expected, rel=TIGHT)

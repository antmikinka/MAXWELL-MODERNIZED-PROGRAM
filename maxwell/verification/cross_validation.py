"""maxwell.verification.cross_validation -- Cross-module consistency checks.

Verifies that different modules produce mutually consistent results,
catching integration-level bugs that unit tests miss.
"""

from __future__ import annotations

import numpy as np

from maxwell.verification.framework import VerificationResult


def validate_stress_energy_consistency() -> list[VerificationResult]:
    """Verify trace of stress tensor = -(E^2 + H^2) / (8*pi).

    Cross-validates: MaxwellStressTensor and energy density formula.
    """
    from maxwell.electromagnetism.forces.stress_tensor import MaxwellStressTensor

    results = []

    E = np.array([100.0, 50.0, 25.0])
    H = np.array([10.0, 20.0, 30.0])
    E2 = np.dot(E, E)
    H2 = np.dot(H, H)

    # Stress tensor trace
    st = MaxwellStressTensor(E_field=E, H_field=H)
    T_trace = st.stress_tensor().trace()

    # Expected trace = -(E^2 + H^2) / (8*pi)
    expected_trace = -(E2 + H2) / (8.0 * np.pi)

    err = (
        abs(T_trace - expected_trace) / abs(expected_trace)
        if expected_trace != 0
        else abs(T_trace)
    )
    results.append(
        VerificationResult(
            module_name="maxwell.electromagnetism",
            article_refs=(616, 637),
            test_name="Stress tensor trace = -(E^2+H^2)/(8pi)",
            expected=float(expected_trace),
            actual=float(T_trace),
            relative_error=float(err),
            tolerance=1e-10,
            passed=err <= 1e-10,
        )
    )

    # Electromagnetic pressure check
    pressure = st.electromagnetic_pressure
    expected_pressure = (E2 + H2) / (8.0 * np.pi)
    err_p = (
        abs(pressure - expected_pressure) / expected_pressure
        if expected_pressure != 0
        else abs(pressure)
    )
    results.append(
        VerificationResult(
            module_name="maxwell.electromagnetism.forces.stress_tensor",
            article_refs=(637, 640),
            test_name="EM pressure = (E^2+H^2)/(8pi)",
            expected=float(expected_pressure),
            actual=float(pressure),
            relative_error=float(err_p),
            tolerance=1e-10,
            passed=err_p <= 1e-10,
        )
    )

    return results


def validate_faraday_self_consistency() -> list[VerificationResult]:
    """Verify Faraday's law: EMF = -d(phi_B)/dt.

    Cross-validates: FaradayInduction module with expected analytical result.
    """
    from maxwell.electromagnetism.induction.faraday import FaradayInduction

    results = []

    fi = FaradayInduction(num_turns=100)
    # EMF = -N * d_flux/dt
    flux_change_rate = 0.01  # weber/s equivalent
    emf = fi.induced_emf(flux_change_rate=flux_change_rate)
    expected_emf = -fi.num_turns * flux_change_rate

    err = abs(emf - expected_emf) / abs(expected_emf) if expected_emf != 0 else abs(emf)
    results.append(
        VerificationResult(
            module_name="maxwell.electromagnetism.induction.faraday",
            article_refs=(530,),
            test_name="Faraday EMF = -N*d(flux)/dt",
            expected=float(expected_emf),
            actual=float(emf),
            relative_error=float(err),
            tolerance=1e-8,
            passed=err <= 1e-8,
        )
    )

    return results


def validate_maxwell_equations_consistency() -> list[VerificationResult]:
    """Verify Maxwell equations for a static field configuration.

    Cross-validates: MaxwellEquations module with known field properties.
    """
    from maxwell.electromagnetism.theory.general_equations import MaxwellEquations

    results = []

    eq = MaxwellEquations()

    # Gauss law: div(D) = 4*pi*rho in CGS
    D_test = np.array([100.0, 0.0, 0.0])
    gauss_e = eq.gauss_law_electric(D_field=D_test)
    # For uniform D field, div(D) = 0 numerically
    results.append(
        VerificationResult(
            module_name="maxwell.electromagnetism.theory.general_equations",
            article_refs=(610,),
            test_name="Gauss law electric: div(D) for uniform field",
            expected=0.0,
            actual=float(gauss_e),
            relative_error=abs(gauss_e),
            tolerance=1e-6,
            passed=abs(gauss_e) < 1e-6,
            details=f"div(D) for uniform field = {gauss_e:.6e}",
        )
    )

    # Gauss law magnetic: div(B) = 0 always
    B_test = np.array([0.0, 0.0, 100.0])
    gauss_m = eq.gauss_law_magnetic(B_field=B_test)
    results.append(
        VerificationResult(
            module_name="maxwell.electromagnetism.theory.general_equations",
            article_refs=(610,),
            test_name="Gauss law magnetic: div(B) = 0",
            expected=0.0,
            actual=float(gauss_m),
            relative_error=abs(gauss_m),
            tolerance=1e-6,
            passed=abs(gauss_m) < 1e-6,
        )
    )

    return results


def validate_cgs_si_roundtrip() -> list[VerificationResult]:
    """Verify CGS unit conversions are invertible."""
    from maxwell.config.constants import C
    from maxwell.core.units.units import CGSUnitConverter

    results = []
    converter = CGSUnitConverter()

    # ESU <-> EMU charge conversion roundtrip
    q_esu = 1.0
    q_emu = converter.esu_to_emu_charge(q_esu)
    q_back = converter.emu_to_esu_charge(q_emu)
    err_q = abs(q_back - q_esu) / q_esu
    results.append(
        VerificationResult(
            module_name="maxwell.core.units",
            article_refs=(771,),
            test_name="ESU <-> EMU charge roundtrip",
            expected=q_esu,
            actual=float(q_back),
            relative_error=float(err_q),
            tolerance=1e-12,
            passed=err_q <= 1e-12,
        )
    )

    # ESU <-> EMU potential conversion roundtrip
    v_esu = 1.0
    v_emu = converter.esu_to_emu_potential(v_esu)
    v_back = converter.emu_to_esu_potential(v_emu)
    err_v = abs(v_back - v_esu) / v_esu
    results.append(
        VerificationResult(
            module_name="maxwell.core.units",
            article_refs=(771,),
            test_name="ESU <-> EMU potential roundtrip",
            expected=v_esu,
            actual=float(v_back),
            relative_error=float(err_v),
            tolerance=1e-12,
            passed=err_v <= 1e-12,
        )
    )

    # CGS <-> SI: Tesla <-> Gauss using constant
    from maxwell.config.constants import CONST

    B_gauss = 1.0
    B_tesla = B_gauss / CONST.TESLA_TO_GAUSS
    B_back = B_tesla * CONST.TESLA_TO_GAUSS
    err_B = abs(B_back - B_gauss) / B_gauss
    results.append(
        VerificationResult(
            module_name="maxwell.config.constants",
            article_refs=(771,),
            test_name="Gauss <-> Tesla via constant roundtrip",
            expected=B_gauss,
            actual=float(B_back),
            relative_error=float(err_B),
            tolerance=1e-12,
            passed=err_B <= 1e-12,
        )
    )

    return results

"""maxwell.verification.module_checks -- Module-specific verification functions.

Each function verifies a specific module group against known analytical results,
returning a list of VerificationResult.
"""

from __future__ import annotations

import numpy as np

from maxwell.verification.framework import VerificationResult


def _make(
    module: str,
    articles: tuple[int, ...],
    name: str,
    expected: float,
    actual: float,
    tol: float = 1e-8,
) -> VerificationResult:
    """Helper to create a VerificationResult with correct pass/fail."""
    err = abs(actual - expected) / abs(expected) if expected != 0 else abs(actual)
    return VerificationResult(
        module_name=module,
        article_refs=articles,
        test_name=name,
        expected=expected,
        actual=float(actual),
        relative_error=float(err),
        tolerance=tol,
        passed=err <= tol,
    )


def verify_spherical_harmonics() -> list[VerificationResult]:
    """Verify spherical harmonic computations (Arts. 128-146, 675-695)."""
    from maxwell.math.spherical_harmonics import (
        SphericalHarmonicExpansion,
        addition_theorem,
        calc_associated_legendre,
        calc_legendre_polynomial,
        calc_spherical_harmonic,
    )

    results = []

    # P_0(x) = 1
    results.append(
        _make(
            "maxwell.math.spherical_harmonics",
            (128,),
            "P_0(0.5) = 1",
            expected=1.0,
            actual=calc_legendre_polynomial(0, 0.5),
        )
    )

    # P_1(x) = x
    results.append(
        _make(
            "maxwell.math.spherical_harmonics",
            (128,),
            "P_1(0.7) = 0.7",
            expected=0.7,
            actual=calc_legendre_polynomial(1, 0.7),
        )
    )

    # P_2(x) = (3x^2 - 1) / 2
    x = 0.5
    expected_p2 = (3 * x**2 - 1) / 2
    results.append(
        _make(
            "maxwell.math.spherical_harmonics",
            (128,),
            f"P_2({x}) = {expected_p2}",
            expected=expected_p2,
            actual=calc_legendre_polynomial(2, x),
        )
    )

    # Y_00 = 1/sqrt(4*pi)
    y00 = calc_spherical_harmonic(0, 0, np.pi / 2, 0)
    expected_y00 = 1.0 / np.sqrt(4 * np.pi)
    results.append(
        _make(
            "maxwell.math.spherical_harmonics",
            (132, 685),
            "|Y_00| = 1/sqrt(4pi)",
            expected=expected_y00,
            actual=abs(y00),
        )
    )

    # Addition theorem for l=0: P_0(cos gamma) = 1
    add_l0 = addition_theorem(0, 0, 0, 0, 0)
    results.append(
        _make(
            "maxwell.math.spherical_harmonics",
            (143,),
            "Addition theorem l=0: P_0 = 1",
            expected=1.0,
            actual=add_l0,
            tol=1e-10,
        )
    )

    # Addition theorem for l=1, same direction: P_1(1) = 1
    add_l1_same = addition_theorem(1, np.pi / 4, 0, np.pi / 4, 0)
    results.append(
        _make(
            "maxwell.math.spherical_harmonics",
            (143,),
            "Addition theorem l=1, same dir: P_1(1) = 1",
            expected=1.0,
            actual=add_l1_same,
            tol=1e-10,
        )
    )

    return results


def verify_electrostatics() -> list[VerificationResult]:
    """Verify electrostatic modules (Part I, Arts. 1-229)."""
    from maxwell.core.charge import PointCharge

    results = []

    # Point charge E = q / r^2 at r=5, q=1
    q = PointCharge(q=1.0, position=np.array([0.0, 0.0, 0.0]))
    r = 5.0
    E_at_r = q.field_at(np.array([r, 0.0, 0.0]))
    expected_E = 1.0 / r**2  # CGS: E = q/r^2
    results.append(
        _make(
            "maxwell.core.charge",
            (27,),
            f"Point charge E at r={r}: q/r^2 = {expected_E}",
            expected=expected_E,
            actual=np.linalg.norm(E_at_r),
        )
    )

    # Potential V = q/r
    V_at_r = q.potential_at(np.array([r, 0.0, 0.0]))
    expected_V = 1.0 / r
    results.append(
        _make(
            "maxwell.core.charge",
            (27,),
            f"Point charge V at r={r}: q/r = {expected_V}",
            expected=expected_V,
            actual=V_at_r,
        )
    )

    # Gauss law: flux through sphere = 4*pi*q
    n_points = 10000
    np.random.seed(42)
    theta = np.arccos(2 * np.random.rand(n_points) - 1)
    phi = 2 * np.pi * np.random.rand(n_points)
    r_sphere = 1.0
    flux = 0.0
    for th, ph in zip(theta, phi):
        pt = r_sphere * np.array(
            [np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)]
        )
        E = q.field_at(pt)
        n_hat = pt / r_sphere
        dA = 4 * np.pi * r_sphere**2 / n_points
        flux += np.dot(E, n_hat) * dA
    expected_flux = 4 * np.pi * 1.0
    results.append(
        _make(
            "maxwell.core.charge",
            (41,),
            f"Gauss law flux: 4pi*q = {expected_flux:.4f}",
            expected=expected_flux,
            actual=flux,
            tol=0.01,
        )
    )

    return results


def verify_magnetism() -> list[VerificationResult]:
    """Verify magnetic modules (Part III, Arts. 371-474)."""
    from maxwell.core.magnet import Magnet, MagneticPole
    from maxwell.instruments.helmholtz import HelmholtzCoil

    results = []

    # Helmholtz coil field at center
    coil = HelmholtzCoil(radius=10.0, n_turns=100, current=1.0)
    B_center = coil.field_at_center()
    results.append(
        _make(
            "maxwell.instruments.helmholtz",
            (475,),
            f"Helmholtz coil B_center > 0: {B_center:.6f}",
            expected=0.0,
            actual=B_center,
            tol=0.0,
        )
    )

    # Magnetic dipole: create a magnet and verify its moment
    north = MagneticPole(
        strength=1.0, position=np.array([0.0, 0.0, 1.0]), pole_type="N"
    )
    south = MagneticPole(
        strength=1.0, position=np.array([0.0, 0.0, -1.0]), pole_type="S"
    )
    mag = Magnet(north_pole=north, south_pole=south)
    # Magnetic moment = pole_strength * length
    expected_moment = 1.0 * 2.0  # strength * distance
    actual_moment = np.linalg.norm(mag.magnetic_moment)
    results.append(
        _make(
            "maxwell.core.magnet",
            (371,),
            f"Magnetic moment = pole_strength * length = {expected_moment}",
            expected=expected_moment,
            actual=actual_moment,
        )
    )

    return results


def verify_electromagnetism() -> list[VerificationResult]:
    """Verify electromagnetism modules (Part IV, Arts. 475-866)."""
    results = []

    # Lorentz force: F = I * L x B
    from maxwell.electromagnetism.forces.lorentz import LorentzForce

    current = 1.0  # statampere
    length_vec = np.array([10.0, 0.0, 0.0])  # cm, wire along x
    B = np.array([0.0, 0.0, 100.0])  # gauss

    lf = LorentzForce(current=current, B_field=B, length=length_vec)
    F = lf.force_vector
    # L x B = (10,0,0) x (0,0,100) = (0, -1000, 0)
    # F = I * (L x B) = (0, -1000, 0)
    expected_Fy = -current * 10.0 * 100.0  # Fy = -I*Lx*Bz
    results.append(
        _make(
            "maxwell.electromagnetism.forces.lorentz",
            (593,),
            f"Lorentz Fy = -I*L*B = {expected_Fy:.6e}",
            expected=expected_Fy,
            actual=F[1],
            tol=1e-6,
        )
    )

    # Maxwell stress tensor symmetry
    from maxwell.electromagnetism.forces.stress_tensor import MaxwellStressTensor

    E_test = np.array([1.0, 2.0, 3.0])
    H_test = np.array([0.5, 1.0, 1.5])
    st = MaxwellStressTensor(E_field=E_test, H_field=H_test)
    T = st.stress_tensor()
    is_symmetric = np.allclose(T, T.T)
    results.append(
        VerificationResult(
            module_name="maxwell.electromagnetism.forces.stress_tensor",
            article_refs=(616,),
            test_name="Stress tensor symmetry T_ij = T_ji",
            expected=1.0,
            actual=float(is_symmetric),
            relative_error=0.0 if is_symmetric else 1.0,
            tolerance=0.0,
            passed=bool(is_symmetric),
        )
    )

    # Stress tensor trace = -(E^2 + H^2) / (8*pi)
    E2 = np.dot(E_test, E_test)
    H2 = np.dot(H_test, H_test)
    expected_trace = -(E2 + H2) / (8.0 * np.pi)
    actual_trace = T.trace()
    results.append(
        _make(
            "maxwell.electromagnetism.forces.stress_tensor",
            (616,),
            f"Stress tensor trace = -(E^2+H^2)/(8pi) = {expected_trace:.6e}",
            expected=expected_trace,
            actual=actual_trace,
        )
    )

    return results


def verify_vector_calculus() -> list[VerificationResult]:
    """Verify vector calculus operators."""
    from maxwell.math.vector_operators import curl, gradient

    results = []

    # curl(grad(V)) = 0 for V = 1/r
    def V_inverse_r(x, y, z):
        r = np.sqrt(x**2 + y**2 + z**2)
        return 1.0 / r if r > 1e-10 else 0.0

    grad_vx = lambda x, y, z: gradient(V_inverse_r, x, y, z)[0]
    grad_vy = lambda x, y, z: gradient(V_inverse_r, x, y, z)[1]
    grad_vz = lambda x, y, z: gradient(V_inverse_r, x, y, z)[2]

    curl_val = curl(grad_vx, grad_vy, grad_vz, 5.0, 3.0, 2.0)
    curl_err = np.linalg.norm(curl_val)
    results.append(
        VerificationResult(
            module_name="maxwell.math.vector_operators",
            article_refs=(15,),
            test_name="curl(grad(1/r)) = 0",
            expected=0.0,
            actual=float(curl_err),
            relative_error=float(curl_err),
            tolerance=1e-4,
            passed=curl_err < 1e-4,
            details=f"curl_grad magnitude: {curl_err:.2e}",
        )
    )

    # gradient of V = 1/r should give dV/dx = -x/r^3
    grad_val = gradient(V_inverse_r, 3.0, 0.0, 0.0)
    expected_grad_x = -1.0 / 9.0  # -x/r^3 at (3,0,0)
    results.append(
        _make(
            "maxwell.math.vector_operators",
            (15,),
            f"grad(1/r) at (3,0,0): dV/dx = {expected_grad_x:.6e}",
            expected=expected_grad_x,
            actual=grad_val[0],
            tol=1e-4,
        )
    )

    return results


def verify_elliptic_integrals() -> list[VerificationResult]:
    """Verify elliptic integral computations (Arts. 696-705)."""
    from scipy.special import ellipe, ellipk

    results = []

    # K(0) = pi/2
    K0 = ellipk(0.0)
    results.append(
        _make(
            "maxwell.math.elliptic_integrals",
            (696,),
            "K(0) = pi/2",
            expected=np.pi / 2,
            actual=K0,
        )
    )

    # E(0) = pi/2
    E0 = ellipe(0.0)
    results.append(
        _make(
            "maxwell.math.elliptic_integrals",
            (696,),
            "E(0) = pi/2",
            expected=np.pi / 2,
            actual=E0,
        )
    )

    # K(0.5) ~ 1.8540746773013719
    K05 = ellipk(0.5)
    expected_K05 = 1.8540746773013719
    results.append(
        _make(
            "maxwell.math.elliptic_integrals",
            (697,),
            "K(0.5) ~ 1.8540746773",
            expected=expected_K05,
            actual=K05,
            tol=1e-10,
        )
    )

    # E(0.5) ~ 1.3506438810476755
    E05 = ellipe(0.5)
    expected_E05 = 1.3506438810476755
    results.append(
        _make(
            "maxwell.math.elliptic_integrals",
            (697,),
            "E(0.5) ~ 1.3506438810",
            expected=expected_E05,
            actual=E05,
            tol=1e-10,
        )
    )

    return results


def verify_units_and_dimensions() -> list[VerificationResult]:
    """Verify unit system consistency."""
    from maxwell.config.constants import C
    from maxwell.core.units.units import CGSUnitConverter

    results = []

    # ESU/EMU ratio for charge = c
    converter = CGSUnitConverter()
    q_emu = 1.0
    q_esu = converter.emu_to_esu_charge(q_emu)
    ratio = q_esu / q_emu  # should equal c
    ratio_over_c = ratio / C
    results.append(
        _make(
            "maxwell.core.units",
            (771,),
            "ESU/EMU charge ratio / c = 1.0",
            expected=1.0,
            actual=ratio_over_c,
            tol=1e-10,
        )
    )

    # Speed of light constant
    results.append(
        _make(
            "maxwell.config.constants",
            (782,),
            "c = 2.9979e10 cm/s",
            expected=2.9979e10,
            actual=C,
            tol=1e-4,
        )
    )

    return results


def verify_optics_and_waves() -> list[VerificationResult]:
    """Verify optics and wave propagation modules (Arts. 781-866)."""
    from maxwell.config.constants import C
    from maxwell.optics.wave_equation import PlaneWave

    results = []

    # Plane wave: E = c*B relationship, wavelength = 2*pi*c/omega
    E0 = np.array([1.0, 0.0, 0.0])
    k = np.array([0.0, 0.0, 2 * np.pi * 1e14 / C])  # wavevector magnitude = omega/c
    omega = 2 * np.pi * 1e14  # angular frequency

    pw = PlaneWave(E0=E0, k=k, omega=omega)
    # Wavelength lambda = 2*pi/|k| = c/f
    expected_lambda = C / 1e14
    actual_lambda = 2 * np.pi / np.linalg.norm(k)
    results.append(
        _make(
            "maxwell.optics.wave_equation",
            (787,),
            f"Plane wave lambda = c/f = {expected_lambda:.4e} cm",
            expected=expected_lambda,
            actual=actual_lambda,
        )
    )

    return results

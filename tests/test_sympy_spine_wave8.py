"""Tests for the Wave 8a spine verifiers in maxwell.verification.sympy_verify.

Wave 8a (G4 criterion) requires at least 60 SymPy spine verifiers; this
file exercises the 56 verifiers added for the in-scope spine of Part IV
(Arts. 667-866): elliptic integrals and circular currents, the
zonal-harmonic potential spine, current sheets, electromagnetic waves and
magneto-optics, absolute resistance standards, action-at-distance
theories, CGS unit discipline, and the dipole vector-calculus spine.

Each case asserts:
  * the computed verdict passes (``passed is True``);
  * the computed residual is numerically negligible (numeric pin);
  * the VerificationResult contract holds and the article marking is
    consistent with the verifier's citation and article_refs.

Skips the whole module when SymPy is absent, like test_sympy_verify.py.
"""

from __future__ import annotations

import math
from typing import Callable

import pytest

# Skip entire module if SymPy is not available
sympy = pytest.importorskip("sympy")

from maxwell.meta.citation import get_citation
from maxwell.verification.framework import VerificationResult
from maxwell.verification.sympy_verify import (
    ALL_SYMBOLIC_VERIFIERS,
    verify_Y00_normalization,
    verify_addition_theorem_p1,
    verify_ampere_force_symmetry,
    verify_ampere_newton_third_law,
    verify_ampere_parallel_attraction,
    verify_ballistic_throw_charge,
    verify_capacitance_esu_length_dimension,
    verify_capacitor_energy,
    verify_circular_birefringence_rotation,
    verify_circular_current_center_field,
    verify_coil_comparison_modulus,
    verify_cylindrical_sheet_field,
    verify_dM_dd_dipole_relation,
    verify_dipole_vector_potential,
    verify_dispersion_relation,
    verify_div_B_dipole_zero,
    verify_elliptic_E_derivative_identity,
    verify_elliptic_E_small_k_series,
    verify_elliptic_K_AGM_identity,
    verify_elliptic_K_derivative_identity,
    verify_elliptic_K_small_k_series,
    verify_elliptic_landen_descent,
    verify_elliptic_legendre_relation,
    verify_esu_emu_charge_ratio_c,
    verify_esu_emu_resistance_ratio_c2,
    verify_legendre_differential_equation,
    verify_legendre_generating_function,
    verify_legendre_orthogonality,
    verify_legendre_parity,
    verify_legendre_recurrence,
    verify_legendre_value_at_one,
    verify_loop_axial_field_integral,
    verify_loop_far_field_dipole_limit,
    verify_medium_wave_velocity,
    verify_mutual_inductance_far_limit,
    verify_mutual_inductance_neumann_symmetry,
    verify_normal_B_continuous,
    verify_plane_wave_E_cB,
    verify_plane_wave_dalembert,
    verify_plane_wave_poynting,
    verify_rc_discharge_ode,
    verify_rc_time_constant,
    verify_recoil_method_structure,
    verify_resistance_emu_velocity_dimension,
    verify_sheet_potential_discontinuity,
    verify_sheet_toroidal_zero_exterior,
    verify_solenoid_inductance_structure,
    verify_surface_current_jump,
    verify_vector_potential_loop_structure,
    verify_verdet_path_linearity,
    verify_wave_transversality,
    verify_weber_coulomb_limit,
    verify_weber_potential_energy_identity,
    verify_weber_velocity_structure,
    verify_wheatstone_balance,
    verify_zonal_harmonic_laplace,
)


def _case(fn: Callable[[], VerificationResult], article: int):
    """Build a parametrized case carrying its article evidence mark."""
    return pytest.param(fn, article, id=fn.__name__, marks=pytest.mark.article(article))


# (verifier, primary article) for every Wave 8a verifier.  The article is
# always a member of the verifier's @maxwell_cite articles (checked below).
WAVE8_CASES = [
    # Cluster A: elliptic integrals (Arts. 696-706, 752-757)
    _case(verify_elliptic_K_AGM_identity, 696),
    _case(verify_elliptic_legendre_relation, 703),
    _case(verify_elliptic_K_small_k_series, 703),
    _case(verify_elliptic_E_small_k_series, 703),
    _case(verify_elliptic_K_derivative_identity, 704),
    _case(verify_elliptic_E_derivative_identity, 704),
    _case(verify_elliptic_landen_descent, 705),
    _case(verify_coil_comparison_modulus, 752),
    # Cluster B: circular currents (Arts. 694-706, 755-756)
    _case(verify_circular_current_center_field, 694),
    _case(verify_loop_axial_field_integral, 694),
    _case(verify_loop_far_field_dipole_limit, 694),
    _case(verify_vector_potential_loop_structure, 696),
    _case(verify_mutual_inductance_neumann_symmetry, 694),
    _case(verify_mutual_inductance_far_limit, 755),
    _case(verify_dM_dd_dipole_relation, 755),
    # Cluster C: zonal-harmonic spine (Arts. 675-677)
    _case(verify_legendre_value_at_one, 675),
    _case(verify_legendre_parity, 675),
    _case(verify_legendre_recurrence, 675),
    _case(verify_legendre_orthogonality, 675),
    _case(verify_legendre_generating_function, 676),
    _case(verify_addition_theorem_p1, 676),
    _case(verify_Y00_normalization, 676),
    _case(verify_zonal_harmonic_laplace, 677),
    _case(verify_legendre_differential_equation, 677),
    # Cluster D: current sheets (Arts. 667-671)
    _case(verify_surface_current_jump, 667),
    _case(verify_normal_B_continuous, 667),
    _case(verify_solenoid_inductance_structure, 668),
    _case(verify_sheet_potential_discontinuity, 669),
    _case(verify_cylindrical_sheet_field, 670),
    _case(verify_sheet_toroidal_zero_exterior, 671),
    # Cluster E: waves and magneto-optics (Arts. 783-813)
    _case(verify_plane_wave_dalembert, 787),
    _case(verify_plane_wave_E_cB, 785),
    _case(verify_dispersion_relation, 787),
    _case(verify_wave_transversality, 785),
    _case(verify_medium_wave_velocity, 783),
    _case(verify_plane_wave_poynting, 788),
    _case(verify_circular_birefringence_rotation, 808),
    _case(verify_verdet_path_linearity, 813),
    # Cluster F: absolute resistance standards (Arts. 758-763)
    _case(verify_rc_discharge_ode, 759),
    _case(verify_rc_time_constant, 759),
    _case(verify_ballistic_throw_charge, 760),
    _case(verify_recoil_method_structure, 761),
    _case(verify_resistance_emu_velocity_dimension, 763),
    _case(verify_wheatstone_balance, 758),
    _case(verify_capacitor_energy, 759),
    # Cluster G: action at distance (Arts. 846-852)
    _case(verify_weber_coulomb_limit, 846),
    _case(verify_weber_velocity_structure, 846),
    _case(verify_weber_potential_energy_identity, 847),
    _case(verify_ampere_force_symmetry, 851),
    _case(verify_ampere_parallel_attraction, 851),
    _case(verify_ampere_newton_third_law, 852),
    # Cluster H: CGS unit discipline (Arts. 772-774)
    _case(verify_esu_emu_charge_ratio_c, 772),
    _case(verify_esu_emu_resistance_ratio_c2, 773),
    _case(verify_capacitance_esu_length_dimension, 774),
    # Cluster I: dipole vector-calculus spine (Art. 833)
    _case(verify_div_B_dipole_zero, 833),
    _case(verify_dipole_vector_potential, 833),
]


# ── G4 count guard ───────────────────────────────────────────────


class TestG4VerifierCount:
    """G4 requires >= 60 SymPy spine verifiers registered."""

    def test_registry_meets_g4_threshold(self):
        assert len(ALL_SYMBOLIC_VERIFIERS) >= 60

    def test_registry_has_no_duplicates(self):
        names = [fn.__name__ for fn in ALL_SYMBOLIC_VERIFIERS]
        assert len(set(names)) == len(names)

    def test_wave8_verifiers_are_all_registered(self):
        registered = {case.values[0] for case in WAVE8_CASES}
        for fn in registered:
            assert fn in ALL_SYMBOLIC_VERIFIERS, f"{fn.__name__} not registered"
        assert len(registered) == 56

    def test_wave8_targets_in_scope_articles_only(self):
        for case in WAVE8_CASES:
            art = case.values[1]
            assert 667 <= art <= 866, f"article {art} outside LAST200 scope"


# ── Per-verifier verdict and residual tests ─────────────────────


@pytest.mark.parametrize("verifier, article", WAVE8_CASES)
class TestWave8VerifiersPass:
    """Every Wave 8a verifier must compute a passing verdict."""

    def test_verdict_passes(self, verifier, article):
        result = verifier()
        assert result.passed is True, (
            f"{verifier.__name__} (Art. {article}) failed: {result.details}"
        )
        # Numeric pin: a passing verifier reports a negligible residual.
        assert result.relative_error < 1e-6

    def test_result_contract(self, verifier, article):
        result = verifier()
        assert isinstance(result, VerificationResult)
        assert result.module_name == "maxwell.verification.sympy_verify"
        assert result.test_name
        assert isinstance(result.article_refs, tuple)
        assert len(result.article_refs) >= 1
        assert article in result.article_refs
        assert math.isfinite(result.expected)
        assert math.isfinite(result.actual)
        # Numeric pin: tolerance is positive and finite.
        assert result.tolerance > 0.0

    def test_citation_matches_marker(self, verifier, article):
        citation = get_citation(verifier)
        assert citation is not None, f"{verifier.__name__} lacks @maxwell_cite"
        assert article in citation.articles
        assert citation.part == 4

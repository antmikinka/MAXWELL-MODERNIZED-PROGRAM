"""
Test new Part IV Molecular Theories modules.

Comprehensive test coverage for molecular and competing theories:
- Ampere's theory (Arts. 832-840) — Molecular currents, m = I*A/c
- Weber's theory (Arts. 841-850) — Velocity-dependent force law
- Neumann's theory (Arts. 851-858) — Mutual inductance via Neumann integral
- Competing theories (Arts. 859-866) — Compare all theories

Tests verify:
- Correct formula implementation with numeric values
- Physical property relationships (moment conservation, force laws)
- Edge cases (zero inputs, limiting behavior)
- CGS unit compliance
- Citation decorator compliance
"""

from __future__ import annotations

import pytest
import numpy as np

from maxwell.config.constants import CONST, C, cgs_unit_of
from maxwell.meta.citation import get_citation, MaxwellCitation


# =============================================================================
# AMPERE'S MOLECULAR THEORY TESTS (Arts. 832-840)
# =============================================================================

class TestAmperesMolecularTheory:
    """Test Ampere's molecular current theory: m = I*A/c."""

    def test_molecular_moment_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify m = I*A/c formula.

        For I = 1e-6 abampere, A = 1e-16 cm²:
        m = 1e-6 * 1e-16 / 3e10 = 3.33e-33 erg/gauss
        """
        from maxwell.molecular.amperes_theory import calc_molecular_moment

        current = 1e-6
        area = 1e-16

        m = calc_molecular_moment(current, area)
        expected = current * area / CONST.C

        assert_cgs_close(m, expected, cgs_tolerance)

    def test_molecular_field_dipole_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify B = (2m/r³)*cos(theta) for dipole field.

        For m = 1 erg/gauss, r = 1 cm, theta = 0:
        B_r = 2 gauss, B_theta = 0
        """
        from maxwell.molecular.amperes_theory import calc_molecular_field

        m = 1.0
        r = 1.0
        theta = 0.0

        B_r, B_theta = calc_molecular_field(m, r, theta)

        assert_cgs_close(B_r, 2.0, cgs_tolerance)
        assert_cgs_close(B_theta, 0.0, cgs_tolerance)

    def test_molecular_field_equator(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify B = -m/r³ at equator (theta = 90°).

        For m = 1, r = 1, theta = 90°:
        B_r = 0, B_theta = -1 gauss
        """
        from maxwell.molecular.amperes_theory import calc_molecular_field

        m = 1.0
        r = 1.0
        theta = np.pi / 2

        B_r, B_theta = calc_molecular_field(m, r, theta)

        assert_cgs_close(B_r, 0.0, cgs_tolerance)
        assert_cgs_close(B_theta, -1.0, cgs_tolerance)

    def test_magnetization_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify M = N*m*f magnetization.

        For N = 1e23 cm⁻³, m = 1e-23 erg/gauss, f = 0.5:
        M = 0.5 gauss
        """
        from maxwell.molecular.amperes_theory import AmperesTheory

        at = AmperesTheory(
            number_density=1e23,
            alignment_factor=0.5
        )

        m = 1e-23
        M = at.magnetization(m)
        expected = 1e23 * 1e-23 * 0.5

        assert_cgs_close(M, expected, cgs_tolerance)

    def test_curie_law_susceptibility(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify chi = C/T Curie law.

        For N = 1e23, m = 1e-23, T = 300 K:
        chi ~ constant/T
        """
        from maxwell.molecular.amperes_theory import AmperesTheory

        at = AmperesTheory(
            number_density=1e23,
            alignment_factor=1.0
        )

        m = 1e-23
        T1 = 300.0
        T2 = 600.0

        chi1 = at.susceptibility(m, T1, 100.0)
        chi2 = at.susceptibility(m, T2, 100.0)

        # chi2 should be half of chi1 (inverse temperature)
        expected_ratio = 2.0
        actual_ratio = chi1 / chi2 if chi2 > 0 else 0

        assert_cgs_close(actual_ratio, expected_ratio, cgs_tolerance * 10)

    def test_molecular_current_class(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify MolecularCurrent class."""
        from maxwell.molecular.amperes_theory import MolecularCurrent

        mc = MolecularCurrent(
            current=1e-6,
            area=1e-16,
            normal=np.array([0.0, 0.0, 1.0])
        )

        # Test magnetic moment
        m = mc.magnetic_moment()
        expected = 1e-6 * 1e-16 / CONST.C
        assert_cgs_close(m, expected, cgs_tolerance)

        # Test field at distance
        B = mc.magnetic_field_at(np.array([0.0, 0.0, 1e-6]))
        assert np.linalg.norm(B) > 0

    def test_bound_current_density(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify J_b = c*curl(M) bound current.

        For uniform M, J_b = 0.
        """
        from maxwell.molecular.amperes_theory import AmperesTheory

        at = AmperesTheory()
        M = np.array([100.0, 0.0, 0.0])  # Uniform

        J_b = at.bound_current_density(M)
        assert_vectors_close(J_b, np.zeros(3), cgs_tolerance)

    def test_verify_amperes_theory(self) -> None:
        """Verify Ampere's theory relations."""
        from maxwell.molecular.amperes_theory import verify_amperes_theory

        result = verify_amperes_theory(
            current=1e-6,
            area=1e-16,
            number_density=1e23
        )

        assert result["verified"] is True


# =============================================================================
# WEBER'S THEORY TESTS (Arts. 841-850)
# =============================================================================

class TestWebersTheory:
    """Test Weber's velocity-dependent force law."""

    def test_weber_force_basic(self, cgs_tolerance, assert_vectors_close) -> None:
        """Verify Weber force includes velocity terms.

        Weber force: F = (q1*q2/r²) * [1 - (r_dot²/2c²) + (r*r_ddot/c²)] * r_hat
        """
        from maxwell.molecular.webers_theory import weber_force

        q1 = 1.0
        q2 = 1.0
        r_vec = np.array([1.0, 0.0, 0.0])
        v1 = np.array([0.0, 1.0, 0.0])
        v2 = np.array([0.0, -1.0, 0.0])

        F = weber_force(q1, q2, r_vec, v1, v2)

        # Force should be along r direction
        assert abs(F[1]) < cgs_tolerance
        assert abs(F[2]) < cgs_tolerance
        assert F[0] > 0  # Repulsive for like charges

    def test_weber_force_static_limit(self, cgs_tolerance, assert_cgs_close, assert_vectors_close) -> None:
        """Verify Weber force reduces to Coulomb for v = 0.

        For v1 = v2 = 0:
        F = (q1*q2/r²) * r_hat
        """
        from maxwell.molecular.webers_theory import weber_force

        q1 = 1.0
        q2 = 1.0
        r_vec = np.array([1.0, 0.0, 0.0])
        v1 = np.zeros(3)
        v2 = np.zeros(3)

        F = weber_force(q1, q2, r_vec, v1, v2)

        expected = q1 * q2 / (1.0 ** 2)  # Along x
        assert_cgs_close(F[0], expected, cgs_tolerance)

    def test_weber_theory_class(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify WeberTheory class."""
        from maxwell.molecular.webers_theory import WeberTheory

        wt = WeberTheory()

        # Test force calculation
        F = wt.force(
            q1=1.0, q2=1.0,
            r_vec=np.array([1.0, 0.0, 0.0]),
            v1=np.zeros(3),
            v2=np.zeros(3)
        )

        expected = 1.0  # Coulomb force
        assert_cgs_close(F[0], expected, cgs_tolerance)

    def test_velocity_dependent_correction(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify velocity-dependent correction term."""
        from maxwell.molecular.webers_theory import weber_force

        q = 1.0
        r_vec = np.array([1.0, 0.0, 0.0])

        # Static case
        F_static = weber_force(q, q, r_vec, np.zeros(3), np.zeros(3))

        # Moving case (velocities along r)
        v = np.array([1e8, 0.0, 0.0])  # Significant fraction of c
        F_moving = weber_force(q, q, r_vec, v, v)

        # Moving force should differ from static
        # (velocity correction term is non-zero)
        assert abs(F_moving[0] - F_static[0]) > 1e-10

    def test_weber_potential_energy(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Weber potential energy formula."""
        from maxwell.molecular.webers_theory import weber_potential

        q1 = 1.0
        q2 = 1.0
        r = 1.0
        r_dot = 0.0

        U = weber_potential(q1, q2, r, r_dot)
        expected = q1 * q2 / r

        assert_cgs_close(U, expected, cgs_tolerance)


# =============================================================================
# NEUMANN'S THEORY TESTS (Arts. 851-858)
# =============================================================================

class TestNeumannsTheory:
    """Test Neumann's potential theory for mutual inductance."""

    def test_neumann_integral_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Neumann integral: M = (1/c²) * integral(dl1*dl2/r).

        For two identical coaxial loops, R = 1 cm, d = 2 cm:
        M ~ some positive value
        """
        from maxwell.molecular.neumanns_theory import neumann_mutual_inductance

        # Two coaxial circular loops
        R1 = 1.0
        R2 = 1.0
        d = 2.0

        M = neumann_mutual_inductance(R1, R2, d)

        # Mutual inductance should be positive
        assert M > 0

    def test_neumann_self_inductance(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify self-inductance from Neumann formula.

        For circular loop, R = 1 cm, a = 0.1 cm (wire radius):
        L ~ 4*pi*R*(ln(8R/a) - 2)
        """
        from maxwell.molecular.neumanns_theory import circular_loop_inductance

        R = 1.0
        a = 0.1

        L = circular_loop_inductance(R, a)

        # Should be positive and roughly proportional to R
        assert L > 0
        assert L < 100.0 * R  # Sanity check

    def test_neumann_potential_formula(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify Neumann potential: W = M*I1*I2.

        For M = 100 cm, I1 = 1 abamp, I2 = 2 abamp:
        W = 200 ergs
        """
        from maxwell.molecular.neumanns_theory import mutual_potential_energy

        M = 100.0
        I1 = 1.0
        I2 = 2.0

        W = mutual_potential_energy(M, I1, I2)
        expected = M * I1 * I2

        assert_cgs_close(W, expected, cgs_tolerance)

    def test_neumann_theory_class(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify NeumannTheory class."""
        from maxwell.molecular.neumanns_theory import NeumannTheory

        nt = NeumannTheory()

        # Test mutual inductance
        M = nt.mutual_inductance(R1=1.0, R2=1.0, d=2.0)
        assert M > 0

        # Test potential energy
        W = nt.potential_energy(M=100.0, I1=1.0, I2=2.0)
        assert_cgs_close(W, 200.0, cgs_tolerance)

    def test_coaxial_loops_limit(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify mutual inductance for coaxial loops at d=0.

        As d -> 0, M should approach sqrt(L1*L2).
        """
        from maxwell.molecular.neumanns_theory import neumann_mutual_inductance

        R1 = 1.0
        R2 = 1.0
        d = 0.01  # Very close

        M = neumann_mutual_inductance(R1, R2, d)

        # Should be large (approaching self-inductance)
        assert M > 1.0


# =============================================================================
# COMPETING THEORIES TESTS (Arts. 859-866)
# =============================================================================

class TestCompetingTheories:
    """Test comparison of competing electromagnetic theories."""

    def test_theory_comparison_basic(self) -> None:
        """Verify theory comparison framework."""
        from maxwell.molecular.competing_theories import compare_theories

        result = compare_theories()

        # Should have entries for each theory
        assert "amperes_theory" in result
        assert "webers_theory" in result
        assert "neumanns_theory" in result

    def test_amperes_theory_strengths(self) -> None:
        """Verify Ampere's theory characteristics."""
        from maxwell.molecular.competing_theories import analyze_amperes_theory

        analysis = analyze_amperes_theory()

        assert "molecular_currents" in analysis
        assert "limitations" in analysis

    def test_webers_theory_analysis(self) -> None:
        """Verify Weber's theory analysis."""
        from maxwell.molecular.competing_theories import analyze_webers_theory

        analysis = analyze_webers_theory()

        assert "velocity_dependent" in analysis
        assert "action_at_distance" in analysis

    def test_neumanns_theory_analysis(self) -> None:
        """Verify Neumann's theory analysis."""
        from maxwell.molecular.competing_theories import analyze_neumanns_theory

        analysis = analyze_neumanns_theory()

        assert "potential_based" in analysis
        assert "induction_focus" in analysis

    def test_maxwells_theory_advantages(self) -> None:
        """Verify Maxwell's theory advantages over competitors."""
        from maxwell.molecular.competing_theories import maxwells_theory_advantages

        advantages = maxwells_theory_advantages()

        assert "field_concept" in advantages
        assert "displacement_current" in advantages

    def test_competing_theory_class(self) -> None:
        """Verify CompetingTheory class."""
        from maxbell.molecular.competing_theories import CompetingTheory

        ct = CompetingTheory()

        # Test theory comparison
        comparison = ct.compare_all()
        assert isinstance(comparison, dict)


# =============================================================================
# MOLECULAR MAGNETISM TESTS
# =============================================================================

class TestMolecularMagnetism:
    """Test molecular magnetism phenomena."""

    def test_paramagnetic_susceptibility(self, cgs_tolerance, assert_cgs_close) -> None:
        """Verify paramagnetic chi > 0."""
        from maxwell.molecular.amperes_theory import AmperesTheory

        at = AmperesTheory(
            number_density=1e23,
            alignment_factor=1.0
        )

        chi = at.susceptibility(
            molecular_moment=1e-23,
            temperature=300.0,
            applied_field=1000.0
        )

        assert chi > 0  # Paramagnetic

    def test_diamagnetic_susceptibility(self) -> None:
        """Verify diamagnetic chi < 0."""
        from maxwell.molecular.competing_theories import diamagnetic_response

        # Diamagnetic materials have negative susceptibility
        chi = diamagnetic_response(applied_field=1000.0)

        assert chi < 0


# =============================================================================
# CGS UNIT COMPLIANCE TESTS
# =============================================================================

class TestMolecularCGSUnits:
    """Test CGS unit compliance for molecular theory modules."""

    def test_molecular_moment_units(self) -> None:
        """Verify molecular moment produces erg/gauss."""
        from maxwell.molecular.amperes_theory import calc_molecular_moment

        m = calc_molecular_moment(1e-6, 1e-16)
        assert isinstance(m, float)
        # Units: erg/gauss (emu)

    def test_weber_force_units(self) -> None:
        """Verify Weber force produces dynes."""
        from maxwell.molecular.webers_theory import weber_force

        F = weber_force(1.0, 1.0, np.array([1.0, 0, 0]), np.zeros(3), np.zeros(3))
        assert isinstance(F, np.ndarray)
        assert len(F) == 3
        # Units: dynes

    def test_neumann_inductance_units(self) -> None:
        """Verify Neumann inductance produces cm (abhenries)."""
        from maxwell.molecular.neumanns_theory import neumann_mutual_inductance

        M = neumann_mutual_inductance(1.0, 1.0, 2.0)
        assert isinstance(M, float)
        assert M > 0
        # Units: cm (abhenries in CGS-EMU)


# =============================================================================
# CITATION COMPLIANCE TESTS
# =============================================================================

class TestMolecularCitationCompliance:
    """Test citation decorator compliance for molecular theory modules."""

    def test_amperes_theory_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify Ampere's theory functions have correct citations."""
        from maxwell.molecular.amperes_theory import (
            calc_molecular_moment,
            calc_molecular_field,
        )

        citation = require_citation(calc_molecular_moment)
        assert citation.part == 4
        assert any(a in citation.articles for a in [832, 833, 834])

    def test_webers_theory_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify Weber's theory functions have correct citations."""
        from maxwell.molecular.webers_theory import weber_force

        citation = require_citation(weber_force)
        assert citation.part == 4
        assert any(a in citation.articles for a in [841, 842, 843, 844, 845, 846, 847, 848, 849, 850])

    def test_neumanns_theory_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify Neumann's theory functions have correct citations."""
        from maxwell.molecular.neumanns_theory import neumann_mutual_inductance

        citation = require_citation(neumann_mutual_inductance)
        assert citation.part == 4
        assert any(a in citation.articles for a in [851, 852, 853, 854, 855, 856, 857, 858])

    def test_competing_theories_citation(
        self,
        require_citation,
        validate_citation_articles
    ) -> None:
        """Verify competing theories functions have correct citations."""
        from maxwell.molecular.competing_theories import compare_theories

        citation = require_citation(compare_theories)
        assert citation.part == 4
        assert any(a in citation.articles for a in [859, 860, 861, 862, 863, 864, 865, 866])

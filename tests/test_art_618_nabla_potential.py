"""Arts. 618-619: nabla of the vector potential is one quaternion.

Wilhelm's test is representational. ∇A must be one object with two
visible parts. S∇A = 0 is not required to construct ∇A.
"""

from __future__ import annotations

import numpy as np
import pytest

from maxwell.electromagnetism.theory.quaternion_expressions import (
    Quaternion,
    impose_s_nabla_A_zero,
    magnetic_induction_from_potential,
    nabla_of_vector,
    scalar_part_of_potential,
    verify_nabla_quaternion_parts,
)
from maxwell.math.quaternion import Quaternion as MathQuaternion
from maxwell.meta.citation import get_citation


def _A_solenoidal(x, y, z):
    """A = (-y, x, 0). curl A = (0, 0, 2), div A = 0."""
    return np.array([-y, x, 0.0], dtype=np.float64)


def _A_unconstrained(x, y, z):
    """A = (x, 0, 0). curl A = 0, div A = 1, so S∇A ≠ 0."""
    return np.array([x, 0.0, 0.0], dtype=np.float64)


class TestNablaAsOneQuaternion:
    """∇A is one object; both parts remain readable."""

    def test_solenoidal_potential_both_parts_from_same_object(
        self, cgs_tolerance, assert_cgs_close, assert_vectors_close
    ) -> None:
        point = np.array([1.0, 2.0, 3.0])
        q = nabla_of_vector(_A_solenoidal, point)

        assert isinstance(q, Quaternion)
        assert Quaternion is MathQuaternion
        assert_vectors_close(q.vector, np.array([0.0, 0.0, 2.0]), cgs_tolerance)
        assert_cgs_close(q.scalar, 0.0, cgs_tolerance)
        assert q.S == q.scalar
        np.testing.assert_array_equal(q.V, q.vector)

        B = magnetic_induction_from_potential(_A_solenoidal, point)
        S = scalar_part_of_potential(_A_solenoidal, point)
        assert_vectors_close(B, q.vector, cgs_tolerance)
        assert_cgs_close(S, q.scalar, cgs_tolerance)
        assert_vectors_close(magnetic_induction_from_potential(q), q.vector, cgs_tolerance)
        assert_cgs_close(scalar_part_of_potential(q), q.scalar, cgs_tolerance)

    def test_nonzero_scalar_part_is_constructible(
        self, cgs_tolerance, assert_cgs_close, assert_vectors_close
    ) -> None:
        """The four-equation teaching has no slot for this case."""
        point = np.array([0.5, -1.0, 2.0])
        q = nabla_of_vector(_A_unconstrained, point)

        assert isinstance(q, Quaternion)
        assert q.scalar != 0.0
        assert_cgs_close(q.scalar, -1.0, cgs_tolerance)
        assert_vectors_close(q.vector, np.array([0.0, 0.0, 0.0]), cgs_tolerance)
        assert scalar_part_of_potential(_A_unconstrained, point) != 0.0

    def test_constructing_nabla_does_not_require_s_zero(self) -> None:
        q = nabla_of_vector(_A_unconstrained, (0.0, 0.0, 0.0))
        assert abs(q.S) > 0.0
        impose_s_nabla_A_zero(nabla_of_vector(_A_solenoidal, (0.0, 0.0, 0.0)))
        with pytest.raises(ValueError, match="later constraint"):
            impose_s_nabla_A_zero(q)

    def test_accepts_point_callable_and_xyz_callable(
        self, cgs_tolerance, assert_vectors_close, assert_cgs_close
    ) -> None:
        def A_xyz(x, y, z):
            return np.array([-y, x, 0.0], dtype=np.float64)

        def A_point(point):
            x, y, z = np.asarray(point, dtype=np.float64)
            return np.array([-y, x, 0.0], dtype=np.float64)

        p = (1.0, 2.0, 3.0)
        q_xyz = nabla_of_vector(A_xyz, p)
        q_point = nabla_of_vector(A_point, p)
        assert_cgs_close(q_xyz.S, q_point.S, cgs_tolerance)
        assert_vectors_close(q_xyz.V, q_point.V, cgs_tolerance)

    def test_bad_vector_part_shape_raises(self) -> None:
        with pytest.raises(ValueError, match="shape"):
            Quaternion(S=0.0, V=np.array([1.0, 2.0]))

    def test_verify_helper_matches_classical_cases(self) -> None:
        result = verify_nabla_quaternion_parts()
        assert result["verified"] is True
        assert result["solenoidal"]["ok"] is True
        assert result["unconstrained"]["ok"] is True


class TestArt618Citation:
    def test_nabla_of_vector_cites_618_619_part_iv(
        self, require_citation, validate_citation_articles
    ) -> None:
        citation = require_citation(nabla_of_vector)
        validate_citation_articles(nabla_of_vector, part=4, articles=[618, 619])
        retrieved = get_citation(nabla_of_vector)
        assert retrieved is not None
        assert retrieved.articles == (618, 619)
        assert retrieved.part == 4
        assert retrieved.chapter == "General Equations of the Electromagnetic Field"

    def test_impose_cites_617_and_619(
        self, require_citation, validate_citation_articles
    ) -> None:
        require_citation(impose_s_nabla_A_zero)
        validate_citation_articles(impose_s_nabla_A_zero, part=4, articles=[617, 619])

    def test_verify_helper_is_cited(
        self, require_citation, validate_citation_articles
    ) -> None:
        require_citation(verify_nabla_quaternion_parts)
        validate_citation_articles(
            verify_nabla_quaternion_parts, part=4, articles=[618, 619]
        )

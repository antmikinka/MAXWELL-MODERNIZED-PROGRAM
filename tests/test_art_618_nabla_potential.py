"""Arts. 618–619: ∇𝔄 is one quaternion. The scalar is not cut at ingest."""

from __future__ import annotations

import numpy as np
import pytest

from maxwell.electromagnetism.theory.quaternion_expressions import (
    impose_s_nabla_A_zero,
    magnetic_induction_from_potential,
    scalar_part_of_potential,
)
from maxwell.math.quaternion import Quaternion, nabla_of_vector
from maxwell.meta.citation import get_citation


def _A_circulating(point) -> np.ndarray:
    """A = (-y, x, 0)."""
    x, y, z = np.asarray(point, dtype=np.float64)
    return np.array([-y, x, 0.0], dtype=np.float64)


def _A_radial_x(point) -> np.ndarray:
    """A = (x, 0, 0)."""
    x, y, z = np.asarray(point, dtype=np.float64)
    return np.array([x, 0.0, 0.0], dtype=np.float64)


class TestUnsplitNablaObject:
    def test_circulating_potential_both_parts_on_one_object(self) -> None:
        """A = (-y, x, 0): V∇A = (0,0,2), S∇A = 0, same Quaternion."""
        point = np.array([1.0, 2.0, 3.0])
        q = nabla_of_vector(_A_circulating, point)
        assert isinstance(q, Quaternion)
        assert q.S == pytest.approx(0.0, abs=1e-8)
        assert q.scalar == pytest.approx(0.0, abs=1e-8)
        np.testing.assert_allclose(q.V, [0.0, 0.0, 2.0], atol=1e-8)
        np.testing.assert_allclose(q.vector, [0.0, 0.0, 2.0], atol=1e-8)
        np.testing.assert_allclose(
            magnetic_induction_from_potential(_A_circulating, point),
            [0.0, 0.0, 2.0],
            atol=1e-8,
        )
        assert scalar_part_of_potential(_A_circulating, point) == pytest.approx(
            0.0, abs=1e-8
        )
        impose_s_nabla_A_zero(q)

    def test_nonzero_scalar_is_constructible(self) -> None:
        """A = (x, 0, 0): S∇A ≠ 0, V∇A = 0. The four-equation slot that was cut."""
        point = np.array([0.4, -1.2, 2.5])
        q = nabla_of_vector(_A_radial_x, point)
        assert isinstance(q, Quaternion)
        assert q.S != pytest.approx(0.0, abs=1e-8)
        assert q.scalar == pytest.approx(-1.0, abs=1e-8)
        np.testing.assert_allclose(q.V, [0.0, 0.0, 0.0], atol=1e-8)
        np.testing.assert_allclose(q.vector, [0.0, 0.0, 0.0], atol=1e-8)
        assert scalar_part_of_potential(_A_radial_x, point) != pytest.approx(
            0.0, abs=1e-8
        )
        with pytest.raises(ValueError, match="not zero"):
            impose_s_nabla_A_zero(q)

    def test_nabla_citation_arts_618_619_part_iv(self) -> None:
        citation = get_citation(nabla_of_vector)
        assert citation is not None
        assert 618 in citation.articles
        assert 619 in citation.articles
        assert citation.part == 4

    def test_constructing_nabla_does_not_require_coulomb_gauge(self) -> None:
        """No test path may require S∇A = 0 in order to construct ∇A."""
        q = nabla_of_vector(_A_radial_x, (0.0, 0.0, 0.0))
        assert q.S != 0.0
        assert q.S == q.scalar

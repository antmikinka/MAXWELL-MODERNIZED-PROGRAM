"""Chapter IX quaternion expressions (Arts. 618-619).

Sibling of ``general_equations.py`` (Arts. 594-603, split form).
Source: Vol. II Ch. IX OCR catalog pages 274-289.

Art. 618 (OCR p284 / printed 257) — "Quaternion Expressions for
the Electromagnetic Equations." German letters are Hamiltonian
vectors. 𝔄 is electromagnetic momentum (F, G, H).

Art. 619 (OCR p285 / printed 258):

    𝔅 = V . ∇ 𝔄
    ∇ = i d/dx + j d/dy + k d/dz
    V = vector part of that one operation.

Then: "Since 𝔄 is subject to the condition S.∇𝔄 = 0, ∇𝔄 is a
pure vector, and the symbol V is unnecessary." The condition
is uniqueness of 𝔄 in Art. 617, not the definition of ∇.
``impose_s_nabla_A_zero`` is that later step.

The rest of 619 restates (B)-(E), e = S.∇𝔇, m = S.∇𝔍. Those
are not this module. The object Wilhelm asked to read is ∇𝔄
with both parts visible.

CGS-EMU. Operator in ``maxwell.math.quaternion``.

Category: A (maxwell_original) — Part IV, Chapter IX.
"""

from __future__ import annotations

from typing import Union

import numpy as np

from maxwell.math.quaternion import Quaternion
from maxwell.math.quaternion import nabla_of_vector as _math_nabla_of_vector
from maxwell.meta.citation import maxwell_cite

PointLike = Union[np.ndarray, tuple[float, float, float], list[float]]

__all__ = [
    "Quaternion",
    "impose_s_nabla_A_zero",
    "magnetic_induction_from_potential",
    "nabla_of_vector",
    "scalar_part_of_potential",
    "verify_nabla_quaternion_parts",
]


def _as_quaternion(A_or_q, point: PointLike | None, h: float) -> Quaternion:
    if isinstance(A_or_q, Quaternion):
        return A_or_q
    if point is None:
        raise TypeError("point is required when the first argument is a vector field")
    return nabla_of_vector(A_or_q, point, h)


@maxwell_cite(
    618,
    619,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Nabla applied to a vector returns one quaternion, not a pre-split div/curl pair.",
)
def nabla_of_vector(A, point: PointLike, h: float = 1e-6) -> Quaternion:
    """∇𝔄 = S∇𝔄 + V∇𝔄 as one object. Scalar is kept.

    Art. 618-619, CGS-EMU. S∇A = −div A (Hamilton/Tait); V∇A = curl A.
    Construction does not require S = 0.

    Args:
        A: Vector potential A(x, y, z) or A(point).
        point: Evaluation point (cm).
        h: Central-difference step (cm).

    Returns:
        Quaternion holding both S∇𝔄 and V∇𝔄.
    """
    return _math_nabla_of_vector(A, point, h)


@maxwell_cite(
    618,
    619,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Magnetic induction is the vector part of ∇A: 𝔅 = V∇𝔄.",
)
def magnetic_induction_from_potential(
    A_or_q,
    point: PointLike | None = None,
    h: float = 1e-6,
) -> np.ndarray:
    """𝔅 = V∇𝔄. Reads ``q.vector`` of the nabla quaternion.

    Args:
        A_or_q: ∇A quaternion, or vector potential A(x, y, z).
        point: Required when ``A_or_q`` is a field (cm).
        h: Central-difference step (cm).

    Returns:
        Magnetic induction (gauss), the vector slot of ∇A.
    """
    return _as_quaternion(A_or_q, point, h).vector


@maxwell_cite(
    618,
    619,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Scalar part of ∇A; kept, not assumed zero at ingest.",
)
def scalar_part_of_potential(
    A_or_q,
    point: PointLike | None = None,
    h: float = 1e-6,
) -> float:
    """S∇𝔄 from the same quaternion. Not assumed zero.

    Args:
        A_or_q: ∇A quaternion, or vector potential A(x, y, z).
        point: Required when ``A_or_q`` is a field (cm).
        h: Central-difference step (cm).

    Returns:
        Scalar slot of ∇A (Hamilton/Tait −div A).
    """
    return _as_quaternion(A_or_q, point, h).scalar


@maxwell_cite(
    617,
    619,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    theory_class="maxwell_original",
    description="S.∇A = 0 is Art. 617 uniqueness of A; Art. 619 then calls V unnecessary. Later constraint, not ingest.",
)
def impose_s_nabla_A_zero(q: Quaternion, tol: float = 1e-12) -> Quaternion:
    """S.∇A = 0 after nabla exists.

    Art. 617 uniquely fixes 𝔄 by S.∇𝔄 = 0. Art. 619 then says that
    because of that condition, ∇𝔄 is a pure vector and V is
    unnecessary. This function is that later step, not ingest.

    Does not silently drop the scalar. If |S| exceeds ``tol``, raise
    so the leftover degree of freedom stays visible. If |S| is within
    tolerance, return the same quaternion (S slot still readable).
    """
    if abs(q.S) > tol:
        raise ValueError(
            "Art. 617 uniquely fixes 𝔄 by S.∇𝔄 = 0; Art. 619 then "
            "calls V unnecessary. That is a later constraint, not ingest. "
            f"Got S={q.S}. Choose a potential whose scalar nabla already "
            "vanishes; this function will not delete S from the quaternion."
        )
    return q


@maxwell_cite(
    618,
    619,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Verify ∇A is one quaternion: V∇A = curl A, S∇A = −div A, S kept when nonzero.",
)
def verify_nabla_quaternion_parts(tolerance: float = 1e-8) -> dict:
    """Check the two classical fields on one Quaternion object.

    Solenoidal A = (−y, x, 0): V∇A = (0, 0, 2), S∇A = 0 (both readable).
    Unconstrained A = (x, 0, 0): S∇A = −1, V∇A = 0 (constructible).

    Args:
        tolerance: Absolute tolerance on S and V (CGS, linear fields).

    Returns:
        Dict with both cases and ``verified``.
    """

    def A_solenoidal(x: float, y: float, z: float) -> np.ndarray:
        return np.array([-y, x, 0.0], dtype=np.float64)

    def A_unconstrained(x: float, y: float, z: float) -> np.ndarray:
        return np.array([x, 0.0, 0.0], dtype=np.float64)

    point = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    q0 = nabla_of_vector(A_solenoidal, point)
    q1 = nabla_of_vector(A_unconstrained, point)

    solenoidal_ok = abs(q0.S) <= tolerance and bool(
        np.allclose(q0.V, (0.0, 0.0, 2.0), atol=tolerance)
    )
    unconstrained_ok = abs(q1.S + 1.0) <= tolerance and bool(
        np.allclose(q1.V, (0.0, 0.0, 0.0), atol=tolerance)
    )
    return {
        "solenoidal": {
            "S": q0.S,
            "V": q0.V,
            "expected_S": 0.0,
            "expected_V": (0.0, 0.0, 2.0),
            "ok": solenoidal_ok,
        },
        "unconstrained": {
            "S": q1.S,
            "V": q1.V,
            "expected_S": -1.0,
            "expected_V": (0.0, 0.0, 0.0),
            "ok": unconstrained_ok,
        },
        "verified": solenoidal_ok and unconstrained_ok,
        "tolerance_used": tolerance,
    }

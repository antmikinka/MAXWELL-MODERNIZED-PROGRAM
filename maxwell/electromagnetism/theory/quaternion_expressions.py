"""Arts. 618–619 written on the unsplit nabla quaternion.

``general_equations.py`` remains the Heaviside/Gibbs split form (Arts. 594–603).
This sibling keeps ∇𝔄 as one object: 𝔅 is the vector part, and S∇𝔄 still
has a slot.

Category: A (maxwell_original) — Treatise Part IV, Arts. 618–619.
"""

from __future__ import annotations

import numpy as np

from maxwell.math.quaternion import NablaInput, Quaternion, nabla_of_vector
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(
    618,
    619,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    description="𝔅 = V∇𝔄, read from the quaternion returned by nabla.",
)
def magnetic_induction_from_potential(A: NablaInput, point, h: float = 1e-6) -> np.ndarray:
    """𝔅 = V∇𝔄. Vector part of one quaternion, not a pre-split curl."""
    q = nabla_of_vector(A, point, h)
    return q.vector


@maxwell_cite(
    618,
    619,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    description="S∇𝔄 kept on the quaternion; not assumed zero at ingest.",
)
def scalar_part_of_potential(A: NablaInput, point, h: float = 1e-6) -> float:
    """S∇𝔄 — kept, not assumed zero."""
    q = nabla_of_vector(A, point, h)
    return q.scalar


@maxwell_cite(
    618,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    description="Maxwell's Art. 618 remark: he sets S∇A = 0. Explicit later step.",
)
def impose_s_nabla_A_zero(q: Quaternion, tol: float = 1e-12) -> Quaternion:
    """Maxwell's Art. 618 remark: he sets S∇A = 0.

    This is a later constraint, not ingest. A nonzero scalar is not dropped.
    """
    if abs(q.S) > tol:
        raise ValueError(
            f"S∇𝔄 = {q.S} is not zero; Art. 618's remark is an explicit "
            "step, not a silent ingest cut. Original scalar is recorded on q.S."
        )
    return q

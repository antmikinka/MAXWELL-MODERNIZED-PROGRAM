"""maxwell.math.quaternion — nabla as one quaternion (Arts. 618-619).

Source: Third Edition Vol. II Chapter IX, Mathpix OCR catalog
pages 274-289 (printed 257-258 for Arts. 618-619). Not Art. 522
algebra in ``maxwell.math.algebra.quaternions``.

Art. 619 (OCR p285 / printed 258):

    𝔅 = V . ∇ 𝔄

    ∇ = i d/dx + j d/dy + k d/dz

    V = the vector part of the result of this operation.

Cartesian (A) in Art. 616 is the same curl of (F, G, H).
Hamilton/Tait scalar of ∇𝔄 is −div 𝔄. Art. 616 footnote
(OCR p282): ∇² carries a minus "in order to make our
expressions consistent with those in which Quaternions are
employed."

Art. 617 (OCR p283) uniquely fixes 𝔄 by ∇²𝔄 = 4πμ𝔠 and
S.∇𝔄 = 0. Art. 619 then says: "Since 𝔄 is subject to the
condition S.∇𝔄 = 0, ∇𝔄 is a pure vector, and the symbol V
is unnecessary." That is a constraint on 𝔄, not ingest of ∇.
This module always returns both parts.

Numerical derivatives reuse ``maxwell.math.vector_operators``.

CGS-EMU:
    A = electromagnetic momentum / vector potential (gauss·cm)
    V.∇A = magnetic induction 𝔅 (gauss)
    S.∇A = −div A (1/cm when A is gauss·cm)
    point, h in cm (default h = 1e-6)

Category: A (maxwell_original) — Part IV, Chapter IX.

References:
    Part IV, Art. 616: Cartesian (A); ∇² minus sign for quaternions.
    Part IV, Art. 617: Unique 𝔄 with S.∇𝔄 = 0.
    Part IV, Art. 618: Quaternion expressions; German letters as Hamiltonian vectors.
    Part IV, Art. 619: 𝔅 = V.∇𝔄; ∇ = i d/dx + j d/dy + k d/dz.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Union

import numpy as np

from maxwell.math.vector_operators import curl, divergence
from maxwell.meta.citation import maxwell_cite

VectorField = Callable[..., np.ndarray | tuple[float, float, float] | list[float]]
PointLike = Union[np.ndarray, tuple[float, float, float], list[float]]


@dataclass(frozen=True, eq=False)
class Quaternion:
    """Hamilton/Tait quaternion: scalar part S plus vector part V.

    Arts. 618-619: both parts exist even when a part is zero. S∇A = 0
    is not applied at construction.

    Attributes:
        S: Scalar part (S∇).
        V: Vector part (V∇), shape (3,).
    """

    S: float
    V: np.ndarray

    def __post_init__(self) -> None:
        v = np.asarray(self.V, dtype=np.float64).reshape(-1)
        if v.size != 3:
            raise ValueError(f"V must have shape (3,), got {np.shape(self.V)}")
        v = np.array(v, dtype=np.float64, copy=True)
        v.setflags(write=False)
        object.__setattr__(self, "V", v)
        object.__setattr__(self, "S", float(self.S))

    @property
    def scalar(self) -> float:
        return self.S

    @property
    def vector(self) -> np.ndarray:
        return self.V

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Quaternion):
            return NotImplemented
        return float(self.S) == float(other.S) and bool(np.array_equal(self.V, other.V))


def _xyz(point: PointLike) -> tuple[float, float, float]:
    p = np.asarray(point, dtype=np.float64).reshape(3)
    return float(p[0]), float(p[1]), float(p[2])


def _eval_vector_field(A: VectorField, x: float, y: float, z: float) -> np.ndarray:
    """Evaluate A at (x, y, z). Accepts A(point) or A(x, y, z)."""
    point = np.array([x, y, z], dtype=np.float64)
    try:
        out = A(point)
    except TypeError:
        out = A(x, y, z)
    return np.asarray(out, dtype=np.float64).reshape(3)


def _component_functions(A: VectorField):
    def Fx(x: float, y: float, z: float) -> float:
        return float(_eval_vector_field(A, x, y, z)[0])

    def Fy(x: float, y: float, z: float) -> float:
        return float(_eval_vector_field(A, x, y, z)[1])

    def Fz(x: float, y: float, z: float) -> float:
        return float(_eval_vector_field(A, x, y, z)[2])

    return Fx, Fy, Fz


@maxwell_cite(
    618,
    619,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Hamilton/Tait scalar nabla S∇A = −div A; scalar is kept.",
)
def scalar_nabla(A: VectorField, point: PointLike, h: float = 1e-6) -> float:
    """S∇A at ``point``. Hamilton/Tait: −(∂Ax/∂x + ∂Ay/∂y + ∂Az/∂z).

    Args:
        A: Vector field A(x, y, z) or A(point), CGS-EMU.
        point: Evaluation point (cm).
        h: Central-difference step (cm).

    Returns:
        Scalar part of ∇A. Zero is a value, not a missing slot.
    """
    x, y, z = _xyz(point)
    Fx, Fy, Fz = _component_functions(A)
    return -float(divergence(Fx, Fy, Fz, x, y, z, h))


@maxwell_cite(
    618,
    619,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Hamilton/Tait vector nabla V∇A = curl A.",
)
def vector_nabla(A: VectorField, point: PointLike, h: float = 1e-6) -> np.ndarray:
    """V∇A at ``point``: curl A, shape (3,).

    Args:
        A: Vector field A(x, y, z) or A(point), CGS-EMU.
        point: Evaluation point (cm).
        h: Central-difference step (cm).

    Returns:
        Vector part of ∇A (gauss when A is the EMU vector potential).
    """
    x, y, z = _xyz(point)
    Fx, Fy, Fz = _component_functions(A)
    return np.asarray(curl(Fx, Fy, Fz, x, y, z, h), dtype=np.float64)


@maxwell_cite(
    618,
    619,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Nabla applied to a vector returns one quaternion, not a pre-split div/curl pair.",
)
def nabla_of_vector(A: VectorField, point: PointLike, h: float = 1e-6) -> Quaternion:
    """∇A as one quaternion. The scalar part is never discarded.

    ∇ = S∇ + V∇ with S∇A = −div A and V∇A = curl A.

    Args:
        A: Vector field A(x, y, z) or A(point), CGS-EMU.
        point: Evaluation point (cm).
        h: Central-difference step (cm).

    Returns:
        Quaternion with both S and V filled. S = 0 is still stored.
    """
    return Quaternion(S=scalar_nabla(A, point, h), V=vector_nabla(A, point, h))


__all__ = [
    "Quaternion",
    "nabla_of_vector",
    "scalar_nabla",
    "vector_nabla",
]

"""Hamilton/Tait quaternion type and nabla as one operator (Arts. 618–619).

This is a representation, not a quaternion CAS. Maxwell writes ∇𝔄 as one
object whose scalar and vector parts remain visible. The Art. 618 remark
S∇𝔄 = 0 is a later constraint, not an ingest law.

Category: A (maxwell_original) — Treatise Part IV, Arts. 618–619.

References:
    Part IV, Art. 618: 𝔅 = V∇𝔄; Maxwell then sets S∇𝔄 = 0.
    Part IV, Art. 619: the same quaternion written with both parts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence, Union

import numpy as np

from maxwell.math.vector_operators import curl, divergence
from maxwell.meta.citation import maxwell_cite

VectorField = Callable[[np.ndarray], np.ndarray]
ComponentField = Callable[[float, float, float], float]
NablaInput = Union[VectorField, tuple[ComponentField, ComponentField, ComponentField]]


@dataclass(frozen=True)
class Quaternion:
    """Hamilton/Tait quaternion: scalar part + vector part.

    Both parts exist. Callers can read ``q.S`` even when it is zero.
    The constructor never forces the scalar to zero.
    """

    S: float
    V: np.ndarray  # shape (3,)

    def __post_init__(self) -> None:
        object.__setattr__(self, "S", float(self.S))
        object.__setattr__(
            self, "V", np.asarray(self.V, dtype=np.float64).reshape(3)
        )

    @property
    def scalar(self) -> float:
        return self.S

    @property
    def vector(self) -> np.ndarray:
        return self.V


def _as_point(point: Sequence[float] | np.ndarray) -> tuple[float, float, float]:
    p = np.asarray(point, dtype=np.float64).reshape(3)
    return float(p[0]), float(p[1]), float(p[2])


def _as_components(
    A: NablaInput,
) -> tuple[ComponentField, ComponentField, ComponentField]:
    if isinstance(A, tuple) and len(A) == 3:
        return A[0], A[1], A[2]

    def eval_at(x: float, y: float, z: float) -> np.ndarray:
        return np.asarray(A(np.array([x, y, z], dtype=np.float64)), dtype=np.float64).reshape(3)

    def Fx(x: float, y: float, z: float) -> float:
        return float(eval_at(x, y, z)[0])

    def Fy(x: float, y: float, z: float) -> float:
        return float(eval_at(x, y, z)[1])

    def Fz(x: float, y: float, z: float) -> float:
        return float(eval_at(x, y, z)[2])

    return Fx, Fy, Fz


@maxwell_cite(
    618,
    619,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    description="Scalar part of nabla on a vector: S∇𝔄 ~ -div A (Hamilton/Tait).",
)
def scalar_nabla(A: NablaInput, point, h: float = 1e-6) -> float:
    """S∇𝔄 ~ -(∂Fx/∂x + ∂Fy/∂y + ∂Fz/∂z). The scalar is not discarded."""
    Fx, Fy, Fz = _as_components(A)
    x, y, z = _as_point(point)
    return -float(divergence(Fx, Fy, Fz, x, y, z, h))


@maxwell_cite(
    618,
    619,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    description="Vector part of nabla on a vector: V∇𝔄 ~ curl A.",
)
def vector_nabla(A: NablaInput, point, h: float = 1e-6) -> np.ndarray:
    """V∇𝔄 ~ curl A."""
    Fx, Fy, Fz = _as_components(A)
    x, y, z = _as_point(point)
    return np.asarray(curl(Fx, Fy, Fz, x, y, z, h), dtype=np.float64).reshape(3)


@maxwell_cite(
    618,
    619,
    part=4,
    chapter="General Equations of the Electromagnetic Field",
    description="Nabla applied to a vector returns one quaternion, not a pre-split div/curl pair.",
)
def nabla_of_vector(A: NablaInput, point, h: float = 1e-6) -> Quaternion:
    """∇𝔄 = S∇𝔄 + V∇𝔄.

    S∇𝔄  ~  -(∂Fx/∂x + ∂Fy/∂y + ∂Fz/∂z)   (Hamilton/Tait sign)
    V∇𝔄  ~   curl A

    The scalar is not discarded.
    """
    return Quaternion(S=scalar_nabla(A, point, h), V=vector_nabla(A, point, h))

"""
Electric charge and electrification — the fundamental scalar quantity.

Implements the theory of electrification from Part I:
- Point charge and its field
- Faraday's doctrine: no absolute isolated charge exists (Art. 45)
- Charge conservation

Category: A (maxwell_original) — Maxwell's theory of electrification.

References:
    Part I, Arts. 29–32: Electrification by friction.
    Part I, Art. 45: Faraday's doctrine of no absolute charge.
    Part II, Art. 245: Faraday's doctrine restated.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class PointCharge:
    """A point charge in the electrostatic field.

    Art. 29: The quantity of electrification of a body.

    Attributes:
        q: Charge in esu (statcoulombs). Positive = vitreous, negative = resinous.
        position: Position vector (x, y, z) in cm.
    """

    q: float
    position: np.ndarray  # shape (3,)

    def __post_init__(self):
        self.position = np.asarray(self.position, dtype=np.float64)
        if self.position.shape != (3,):
            raise ValueError(f"Position must be 3D, got shape {self.position.shape}")

    @maxwell_cite(
        29,
        30,
        part=1,
        chapter="Electrification",
        theory_class="maxwell_original",
        description="Electric field of a point charge: E = q/r^2",
    )
    def field_at(self, point: np.ndarray) -> np.ndarray:
        """Electric field at a point due to this charge.

        E = q * r_hat / r^2  (Coulomb's law in CGS-ESU)

        Args:
            point: Position vector (cm).

        Returns:
            Electric field vector (dyne/esu = statvolt/cm).

        Reference:
            Part I, Arts. 29–30: Inverse square law of electrification.
        """
        r_vec = point - self.position
        r_mag = np.linalg.norm(r_vec)
        if r_mag == 0:
            return np.zeros(3)
        r_hat = r_vec / r_mag
        return self.q * r_hat / r_mag**2

    @maxwell_cite(
        30,
        part=1,
        chapter="Electrification",
        theory_class="maxwell_original",
        description="Potential of a point charge: V = q/r",
    )
    def potential_at(self, point: np.ndarray) -> float:
        """Electric potential at a point.

        V = q / r  (CGS-ESU)

        Reference:
            Part I, Art. 30: Resultant force and potential.
        """
        r_vec = point - self.position
        r_mag = np.linalg.norm(r_vec)
        if r_mag == 0:
            return float("inf")
        return self.q / r_mag


@maxwell_cite(
    45,
    part=1,
    chapter="Electrical Work and Energy",
    theory_class="maxwell_original",
    description="Faraday's proof: no absolute isolated charge",
)
def faraday_isolation_proof() -> str:
    """Faraday's doctrine: an absolute charge cannot exist in isolation.

    Every electrification is relative: if one body is +charged,
    another must be -charged by an equal amount.

    Returns:
        Statement of the doctrine.

    Reference:
        Part I, Art. 45: Faraday's doctrine.
        Part II, Art. 245: Restatement in electrokinematic context.
    """
    return (
        "Faraday's Doctrine (Art. 45): Electrification always occurs in "
        "equal and opposite quantities. The algebraic sum of all charges "
        "in a closed system is zero. No absolute charge can exist; "
        "every charge is relative to an equal opposite charge."
    )


@maxwell_cite(
    245,
    part=2,
    chapter="Conduction and Resistance",
    theory_class="maxwell_original",
    description="No isolated absolute charge in electrokinematics",
)
def verify_charge_conservation(charges: list[PointCharge]) -> bool:
    """Verify that total charge is conserved (Faraday's doctrine in practice).

    In a truly isolated system, the net charge should be zero.
    This function checks whether the sum of all charges equals zero
    within numerical tolerance.

    Args:
        charges: List of point charges in the system.

    Returns:
        True if total charge is approximately zero.
    """
    total = sum(c.q for c in charges)
    return abs(total) < 1e-10

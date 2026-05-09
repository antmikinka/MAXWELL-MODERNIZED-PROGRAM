"""
Magnetic conventions — polarity and force direction standards.

Implements the convention definitions from Part III of Maxwell's Treatise:
- Austral (positive) vs Boreal (negative) polarity (Art. 393)
- Positive force direction: South to North (Art. 394)

These conventions establish the sign conventions used throughout
magnetic calculations in the CGS-EMU system.

Category: A (maxwell_original) — Maxwell's convention definitions.

References:
    Part III, Arts. 393-394: Magnetic polarity and force conventions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


class PolarityConvention(Enum):
    """
    Magnetic polarity convention — Austral vs Boreal.

    Art. 393: Maxwell establishes that:
    - Austral magnetism (N-seeking, north pole) is POSITIVE (+)
    - Boreal magnetism (S-seeking, south pole) is NEGATIVE (-)

    This follows from the analogy with electric charge, where
    vitreous electricity is positive and resinous is negative.

    Members:
        AUSTRAL: North pole, positive magnetic charge (+m)
        BOREAL: South pole, negative magnetic charge (-m)
    """

    AUSTRAL = +1  # North pole, positive
    BOREAL = -1  # South pole, negative

    @property
    def sign(self) -> int:
        """Return +1 for Austral, -1 for Boreal."""
        return self.value

    @property
    def pole_name(self) -> str:
        """Return 'N' for Austral, 'S' for Boreal."""
        return "N" if self == PolarityConvention.AUSTRAL else "S"

    @classmethod
    @maxwell_cite(
        393,
        part=3,
        chapter="Magnetic Conventions",
        theory_class="maxwell_original",
        description="Polarity convention: Austral positive, Boreal negative",
    )
    def from_pole_type(cls, pole_type: str) -> PolarityConvention:
        """
        Get polarity convention from pole type string.

        Args:
            pole_type: 'N' or 'S' (or 'north', 'south').

        Returns:
            PolarityConvention member.

        Reference:
            Part III, Art. 393: Polarity convention.
        """
        pole_type = pole_type.upper()
        if pole_type in ("N", "NORTH"):
            return cls.AUSTRAL
        elif pole_type in ("S", "SOUTH"):
            return cls.BOREAL
        else:
            raise ValueError(f"Unknown pole type: {pole_type}")


class ForceDirectionConvention(Enum):
    """
    Convention for positive direction of magnetic force.

    Art. 394: The positive direction of magnetic force is defined as
    the direction from South to North pole — the direction in which
    the north pole of a magnet is urged by the field.

    This means:
    - Magnetic field lines point from N to S outside a magnet
    - But the positive force direction is S to N (the direction a
      free N pole would move)

    Members:
        SOUTH_TO_NORTH: Positive direction (field acts S→N on N pole)
        NORTH_TO_SOUTH: Negative direction (opposite)
    """

    SOUTH_TO_NORTH = +1  # Positive direction
    NORTH_TO_SOUTH = -1  # Negative direction

    @property
    def sign(self) -> int:
        """Return +1 for S→N, -1 for N→S."""
        return self.value

    @classmethod
    @maxwell_cite(
        394,
        part=3,
        chapter="Magnetic Conventions",
        theory_class="maxwell_original",
        description="Force direction convention: positive is S to N",
    )
    def positive_direction(cls) -> ForceDirectionConvention:
        """
        Return the positive direction convention.

        Art. 394: The positive direction of magnetic force is from
        South to North — the direction in which a free north pole
        would be urged by the field.

        Returns:
            ForceDirectionConvention.SOUTH_TO_NORTH

        Reference:
            Part III, Art. 394: Force direction convention.
        """
        return cls.SOUTH_TO_NORTH


@dataclass
class MagneticDirection:
    """
    Direction in magnetic space — combines polarity and force conventions.

    This dataclass provides utilities for converting between different
    directional representations in magnetism.

    Attributes:
        polarity: PolarityConvention (Austral/BOREAL).
        force_direction: ForceDirectionConvention (S→N or N→S).
    """

    polarity: PolarityConvention
    force_direction: ForceDirectionConvention = ForceDirectionConvention.SOUTH_TO_NORTH

    @classmethod
    @maxwell_cite(
        393,
        394,
        part=3,
        chapter="Magnetic Conventions",
        theory_class="maxwell_original",
        description="Create magnetic direction from conventions",
    )
    def from_conventions(
        cls,
        pole_type: str,
        force_direction: str = "south_to_north",
    ) -> MagneticDirection:
        """
        Create magnetic direction from string specifications.

        Args:
            pole_type: 'N' or 'S' for pole type.
            force_direction: 'south_to_north' or 'north_to_south'.

        Returns:
            MagneticDirection object.

        Reference:
            Part III, Arts. 393-394: Magnetic conventions.
        """
        polarity = PolarityConvention.from_pole_type(pole_type)

        if force_direction.lower() == "south_to_north":
            force_dir = ForceDirectionConvention.SOUTH_TO_NORTH
        elif force_direction.lower() == "north_to_south":
            force_dir = ForceDirectionConvention.NORTH_TO_SOUTH
        else:
            raise ValueError(f"Unknown force direction: {force_direction}")

        return cls(polarity=polarity, force_direction=force_dir)

    @property
    def signed_scalar(self) -> float:
        """
        Combined signed scalar for calculations.

        Returns:
            Product of polarity and force direction signs.
        """
        return float(self.polarity.sign * self.force_direction.sign)


@maxwell_cite(
    393,
    part=3,
    chapter="Magnetic Conventions",
    theory_class="maxwell_original",
    description="Verify austral magnetism is positive",
)
def verify_austral_positive(pole_strength: float, pole_type: str) -> dict[str, any]:
    """
    Verify and apply the Austral-positive convention.

    Art. 393: By convention, Austral (N) magnetism is assigned a
    positive sign, while Boreal (S) magnetism is negative.

    This function ensures that pole strengths are assigned the
    correct sign according to Maxwell's convention.

    Args:
        pole_strength: Magnitude of pole strength (always positive).
        pole_type: 'N' (Austral) or 'S' (Boreal).

    Returns:
        Dictionary with:
        - signed_strength: Pole strength with correct sign
        - polarity: PolarityConvention member
        - convention_statement: Description of the convention

    Reference:
        Part III, Art. 393: Austral-positive convention.
    """
    if pole_strength < 0:
        raise ValueError("Pole strength magnitude must be non-negative")

    polarity = PolarityConvention.from_pole_type(pole_type)
    signed_strength = polarity.sign * abs(pole_strength)

    return {
        "signed_strength": signed_strength,
        "polarity": polarity,
        "pole_type": polarity.pole_name,
        "convention_statement": "Austral (N) magnetism is positive; Boreal (S) is negative",
        "reference": "Part III, Art. 393",
    }


@maxwell_cite(
    394,
    part=3,
    chapter="Magnetic Conventions",
    theory_class="maxwell_original",
    description="Apply force direction convention to field calculation",
)
def apply_force_direction(
    field_magnitude: float,
    direction: np.ndarray,
) -> np.ndarray:
    """
    Apply force direction convention to field vector.

    Art. 394: The positive direction of magnetic force is from
    South to North. This function ensures field vectors are
    oriented according to this convention.

    The magnetic field H points in the direction that a free
    north pole would be urged — from S to N inside a magnet,
    from N to S outside.

    Args:
        field_magnitude: Magnitude of H field (gauss).
        direction: Unit vector indicating field direction.

    Returns:
        Magnetic field vector H with correct convention (gauss).

    Reference:
        Part III, Art. 394: Force direction convention.
    """
    direction = np.asarray(direction, dtype=np.float64)
    dir_mag = np.linalg.norm(direction)

    if dir_mag == 0:
        return np.zeros(3)

    direction = direction / dir_mag

    # H vector points in the direction of force on a N pole
    return field_magnitude * direction


@maxwell_cite(
    393,
    394,
    part=3,
    chapter="Magnetic Conventions",
    theory_class="maxwell_original",
    description="Complete convention summary for magnetic calculations",
)
def magnetic_convention_summary() -> dict[str, str]:
    """
    Summary of all magnetic conventions used in this implementation.

    Art. 393-394: Maxwell establishes consistent conventions for:
    1. Polarity signs (Austral = +, Boreal = -)
    2. Force direction (positive = S→N)
    3. Field line direction (N→S outside magnet)
    4. Magnetic moment direction (S→N)

    Returns:
        Dictionary summarizing all conventions.

    Reference:
        Part III, Arts. 393-394: Magnetic conventions.
    """
    return {
        "polarity": "Austral (N) = positive (+), Boreal (S) = negative (-)",
        "force_direction": "Positive direction is South to North",
        "field_lines": "Outside magnet: N to S; Inside magnet: S to N",
        "magnetic_moment": "Direction from South pole to North pole",
        "potential": "H = -∇Ω (negative gradient of scalar potential)",
        "pole_force": "F = mH (force on pole of strength m in field H)",
        "reference": "Part III, Arts. 393-394",
    }


@maxwell_cite(
    393,
    part=3,
    chapter="Magnetic Conventions",
    theory_class="maxwell_original",
    description="Convert between modern and Maxwell pole naming",
)
def convert_pole_naming(modern_name: str) -> dict[str, str]:
    """
    Convert between modern and Maxwell-era pole naming conventions.

    Art. 393: Maxwell uses the terms "Austral" and "Boreal" for the
    two polarities, while modern usage prefers "North" and "South".

    Historical note:
    - "Austral" (from Latin 'australis' = southern) refers to the
      pole that seeks the south — i.e., the north-seeking pole
    - "Boreal" (from Latin 'borealis' = northern) refers to the
      pole that seeks the north — i.e., the south-seeking pole

    Args:
        modern_name: Modern pole name ('North', 'South', 'N', 'S').

    Returns:
        Dictionary with all naming conventions for the pole.

    Reference:
        Part III, Art. 393: Pole naming.
    """
    modern_name = modern_name.upper()

    if modern_name in ("N", "NORTH", "NORTH-SEEKING"):
        return {
            "modern": "North pole",
            "maxwell": "Austral magnetism",
            "symbol": "N",
            "sign": "+",
            "description": "North-seeking pole, positive magnetic charge",
        }
    elif modern_name in ("S", "SOUTH", "SOUTH-SEEKING"):
        return {
            "modern": "South pole",
            "maxwell": "Boreal magnetism",
            "symbol": "S",
            "sign": "-",
            "description": "South-seeking pole, negative magnetic charge",
        }
    else:
        raise ValueError(f"Unknown pole name: {modern_name}")


@maxwell_cite(
    394,
    part=3,
    chapter="Magnetic Conventions",
    theory_class="maxwell_original",
    description="Right-hand rule for magnetic field direction",
)
def right_hand_rule_direction(
    current_direction: np.ndarray,
    position: np.ndarray,
) -> np.ndarray:
    """
    Apply right-hand rule for magnetic field from current.

    Art. 394: The direction of magnetic field around a current-carrying
    conductor follows the right-hand rule: if the thumb points in the
    direction of current, the fingers curl in the direction of H.

    For a straight wire:
        H = (2I/cr) × r̂  (in azimuthal direction)

    where the direction is given by the right-hand rule.

    Args:
        current_direction: Unit vector along current direction.
        position: Position vector from wire to field point.

    Returns:
        Unit vector in magnetic field direction.

    Reference:
        Part III, Art. 394: Field direction conventions.

    Note:
        This uses the CGS convention where c appears in the formula.
    """
    current_direction = np.asarray(current_direction, dtype=np.float64)
    position = np.asarray(position, dtype=np.float64)

    # Unit vector from wire to point
    r_mag = np.linalg.norm(position)
    if r_mag == 0:
        return np.zeros(3)

    r_hat = position / r_mag

    # H direction is azimuthal: Î × r̂
    H_direction = np.cross(current_direction, r_hat)

    H_dir_mag = np.linalg.norm(H_direction)
    if H_dir_mag > 0:
        H_direction = H_direction / H_dir_mag

    return H_direction

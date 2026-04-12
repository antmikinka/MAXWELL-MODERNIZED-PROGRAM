"""
Magnetic matter — molecular theory of magnetism.

Implements the theory of magnetic matter from Part III of Maxwell's Treatise:
- Each particle of a magnet is itself a complete magnet (Art. 377)
- Magnetic matter as a fictitious abstraction (Art. 378)
- Proof that north and south quantities are always equal (Art. 379)
- Breaking a magnet — each fragment remains complete (Art. 380)

Maxwell explains that magnetism is not a fluid that can be separated,
but rather each elementary particle contains both N and S poles.

Category: A (maxwell_original) — Maxwell's molecular theory of magnetism.

References:
    Part III, Arts. 377-380: Magnetic matter and molecular theory.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST
from maxwell.core.magnet import Magnet, MagneticPole


@dataclass
class MolecularMagnet:
    """
    An elementary molecular magnet — the fundamental unit of magnetism.

    Art. 377: Each particle of a magnet is itself a complete magnet,
    with both north and south poles. Magnetism is not a separable fluid
    but an intrinsic property of matter at the molecular level.

    Attributes:
        magnetic_moment: Molecular magnetic moment vector (emu).
        position: Position of molecule center (cm).
        orientation: Unit vector along molecular axis (S to N direction).
        is_aligned: Whether molecule is aligned with external field.
    """

    magnetic_moment: np.ndarray  # shape (3,)
    position: np.ndarray  # shape (3,)
    orientation: Optional[np.ndarray] = None  # shape (3,), unit vector
    is_aligned: bool = False

    def __post_init__(self):
        self.magnetic_moment = np.asarray(self.magnetic_moment, dtype=np.float64)
        self.position = np.asarray(self.position, dtype=np.float64)

        if self.orientation is not None:
            self.orientation = np.asarray(self.orientation, dtype=np.float64)
            orient_mag = np.linalg.norm(self.orientation)
            if orient_mag > 0:
                self.orientation = self.orientation / orient_mag

        # Derive orientation from moment if not provided
        if self.orientation is None:
            moment_mag = np.linalg.norm(self.magnetic_moment)
            if moment_mag > 0:
                self.orientation = self.magnetic_moment / moment_mag
            else:
                self.orientation = np.zeros(3)

    @property
    def moment_magnitude(self) -> float:
        """Magnitude of molecular magnetic moment."""
        return float(np.linalg.norm(self.magnetic_moment))

    @classmethod
    @maxwell_cite(
        377,
        part=3, chapter="Magnetic Matter",
        theory_class="maxwell_original",
        description="Create molecular magnet from moment and position",
    )
    def from_moment(
        cls,
        magnetic_moment: np.ndarray,
        position: np.ndarray,
    ) -> MolecularMagnet:
        """
        Create a molecular magnet from its magnetic moment.

        Art. 377: Every molecule that participates in magnetization
        is itself a complete magnet with definite moment.

        Args:
            magnetic_moment: Molecular magnetic moment vector (emu).
            position: Position of molecule (cm).

        Returns:
            MolecularMagnet object.

        Reference:
            Part III, Art. 377: Molecular magnets.
        """
        return cls(magnetic_moment=magnetic_moment, position=position)

    @classmethod
    @maxwell_cite(
        377,
        part=3, chapter="Magnetic Matter",
        theory_class="maxwell_original",
        description="Create molecular magnet with specified orientation",
    )
    def from_orientation(
        cls,
        moment_magnitude: float,
        orientation: np.ndarray,
        position: np.ndarray,
    ) -> MolecularMagnet:
        """
        Create a molecular magnet from moment magnitude and orientation.

        Art. 377: The magnetic properties of a molecule are defined
        by its magnetic moment magnitude and its orientation in space.

        Args:
            moment_magnitude: Magnitude of magnetic moment (emu).
            orientation: Unit vector along molecular axis (S to N).
            position: Position of molecule (cm).

        Returns:
            MolecularMagnet object.

        Reference:
            Part III, Art. 377: Molecular magnetic orientation.
        """
        orientation = np.asarray(orientation, dtype=np.float64)
        orient_mag = np.linalg.norm(orientation)

        if orient_mag == 0:
            raise ValueError("Orientation cannot be zero vector")

        orientation = orientation / orient_mag
        magnetic_moment = moment_magnitude * orientation

        return cls(
            magnetic_moment=magnetic_moment,
            position=position,
            orientation=orientation,
        )

    @maxwell_cite(
        377,
        part=3, chapter="Magnetic Matter",
        theory_class="maxwell_original",
        description="Molecular magnet energy in external field",
    )
    def energy_in_field(self, field: np.ndarray) -> float:
        """
        Calculate potential energy of molecular magnet in field.

        Art. 377: A molecular magnet has minimum energy when aligned
        with the external field.

        W = -m · H

        Args:
            field: External H field vector (gauss).

        Returns:
            Potential energy (erg).

        Reference:
            Part III, Art. 377: Molecular magnet energy.
        """
        return -np.dot(self.magnetic_moment, field)

    @maxwell_cite(
        377,
        part=3, chapter="Magnetic Matter",
        theory_class="maxwell_original",
        description="Torque on molecular magnet",
    )
    def torque_in_field(self, field: np.ndarray) -> np.ndarray:
        """
        Calculate torque on molecular magnet in external field.

        Art. 377: The field exerts a torque trying to align the
        molecular magnet with the field direction.

        τ = m × H

        Args:
            field: External H field vector (gauss).

        Returns:
            Torque vector (dyne·cm).

        Reference:
            Part III, Art. 377: Molecular magnet torque.
        """
        return np.cross(self.magnetic_moment, field)


@dataclass
class MagneticMatterTheory:
    """
    Theory of magnetic matter — collection of molecular magnets.

    Art. 378: Magnetic matter is a fictitious abstraction used to
    simplify calculations. In reality, magnetism exists only as a
    property of elementary particles, each being a complete magnet.

    This class models a volume of magnetic material as a collection
    of molecular magnets, providing macroscopic properties through
    statistical aggregation.

    Attributes:
        molecules: List of molecular magnets in the volume.
        volume: Volume containing the molecules (cm³).
    """

    molecules: list[MolecularMagnet] = field(default_factory=list)
    volume: float = 1.0  # cm³

    @classmethod
    @maxwell_cite(
        378,
        part=3, chapter="Magnetic Matter",
        theory_class="maxwell_original",
        description="Create magnetic matter from molecular ensemble",
    )
    def from_molecules(
        cls,
        molecules: list[MolecularMagnet],
        volume: float = 1.0,
    ) -> MagneticMatterTheory:
        """
        Create magnetic matter theory from ensemble of molecules.

        Art. 378: The magnetic properties of bulk matter emerge from
        the collective behavior of its molecular magnets.

        Args:
            molecules: List of MolecularMagnet objects.
            volume: Volume containing molecules (cm³).

        Returns:
            MagneticMatterTheory object.

        Reference:
            Part III, Art. 378: Magnetic matter theory.
        """
        return cls(molecules=molecules, volume=volume)

    @property
    def number_density(self) -> float:
        """Number of molecules per unit volume."""
        if self.volume <= 0:
            return 0.0
        return len(self.molecules) / self.volume

    @property
    def total_magnetic_moment(self) -> np.ndarray:
        """Vector sum of all molecular moments."""
        if not self.molecules:
            return np.zeros(3)
        return sum(m.magnetic_moment for m in self.molecules)

    @property
    def magnetization(self) -> np.ndarray:
        """
        Magnetization (magnetic moment per unit volume).

        I = (sum of moments) / volume

        Returns:
            Magnetization vector (emu/cm³).
        """
        if self.volume <= 0:
            return np.zeros(3)
        return self.total_magnetic_moment / self.volume

    @maxwell_cite(
        378,
        part=3, chapter="Magnetic Matter",
        theory_class="maxwell_original",
        description="Calculate magnetization from molecular ensemble",
    )
    def calc_magnetization(self) -> np.ndarray:
        """
        Calculate the magnetization vector.

        Art. 378: The resultant magnetization is the vector sum of
        all molecular moments divided by the volume.

        Returns:
            Magnetization vector I (emu/cm³).

        Reference:
            Part III, Art. 378: Magnetization calculation.
        """
        return self.magnetization

    @maxwell_cite(
        378,
        part=3, chapter="Magnetic Matter",
        theory_class="maxwell_original",
        description="Alignment fraction in external field",
    )
    def alignment_fraction(self, field: np.ndarray, tolerance: float = 0.1) -> float:
        """
        Calculate fraction of molecules aligned with external field.

        Art. 378: In a magnetized body, a certain fraction of
        molecular magnets are aligned with the field direction.

        A molecule is considered "aligned" if its orientation is
        within `tolerance` radians of the field direction.

        Args:
            field: External H field vector (gauss).
            tolerance: Maximum angle for alignment (radians).

        Returns:
            Fraction of molecules aligned (0 to 1).

        Reference:
            Part III, Art. 378: Molecular alignment.
        """
        if not self.molecules:
            return 0.0

        field = np.asarray(field, dtype=np.float64)
        field_mag = np.linalg.norm(field)

        if field_mag == 0:
            return 0.0

        field_direction = field / field_mag

        aligned_count = 0
        for mol in self.molecules:
            if np.linalg.norm(mol.orientation) > 0:
                cos_theta = np.dot(mol.orientation, field_direction)
                cos_theta = np.clip(cos_theta, -1.0, 1.0)
                angle = np.arccos(cos_theta)
                if angle <= tolerance:
                    aligned_count += 1

        return aligned_count / len(self.molecules)


@maxwell_cite(
    379,
    part=3, chapter="Magnetic Matter",
    theory_class="maxwell_original",
    description="Proof that north and south magnetic quantities are equal",
)
def verify_equal_opposite(magnets: list[Magnet], tolerance: float = 1e-10) -> dict[str, float]:
    """
    Verify that total north and south magnetic quantities are equal.

    Art. 379: In any magnet or system of magnets, the total quantity
    of north magnetism exactly equals the total quantity of south
    magnetism. This is a fundamental law — magnetic poles always
    occur in equal and opposite pairs.

    This function proves that the algebraic sum of all pole strengths
    in a closed system is zero.

    Args:
        magnets: List of Magnet objects to analyze.
        tolerance: Numerical tolerance for equality check.

    Returns:
        Dictionary with:
        - total_north: Sum of all N pole strengths
        - total_south: Sum of all S pole strengths (absolute value)
        - net_magnetic_charge: Algebraic sum (should be ~0)
        - verified: True if equal within tolerance
        - imbalance_fraction: Fractional imbalance if any

    Reference:
        Part III, Art. 379: Equality of N and S quantities.
    """
    total_north = 0.0
    total_south = 0.0

    for magnet in magnets:
        total_north += abs(magnet.north_pole.strength)
        total_south += abs(magnet.south_pole.strength)

    net_charge = total_north - total_south
    total_magnitude = total_north + total_south

    if total_magnitude > 0:
        imbalance_fraction = abs(net_charge) / total_magnitude
    else:
        imbalance_fraction = 0.0

    verified = abs(net_charge) <= tolerance

    return {
        "total_north": total_north,
        "total_south": total_south,
        "net_magnetic_charge": net_charge,
        "verified": verified,
        "imbalance_fraction": imbalance_fraction,
        "tolerance_used": tolerance,
    }


@maxwell_cite(
    380,
    part=3, chapter="Magnetic Matter",
    theory_class="maxwell_original",
    description="Breaking a magnet produces complete smaller magnets",
)
def break_magnet(
    original_magnet: Magnet,
    break_positions: list[float],
) -> list[Magnet]:
    """
    Simulate breaking a magnet into fragments.

    Art. 380: When a magnet is broken, each fragment becomes a
    complete magnet with its own north and south poles. The break
    itself creates new poles of opposite polarity on each fragment.

    This demonstrates that magnetism is not a fluid that flows from
    one end to another, but rather each part of the magnet contains
    both polarities inherently.

    Args:
        original_magnet: The original magnet to break.
        break_positions: List of fractional positions (0 to 1) along
                        the magnet axis where breaks occur.

    Returns:
        List of new Magnet objects representing fragments.

    Reference:
        Part III, Art. 380: Breaking magnets.

    Example:
        Breaking a bar magnet at its center produces two smaller
        magnets, each with N and S poles — not isolated poles.
    """
    # Get magnet axis information
    axis_vector = original_magnet.magnetic_axis_vector
    axis_length = original_magnetic_length
    pole_strength = original_magnet.pole_strength

    # Sort break positions
    breaks = sorted([0.0] + break_positions + [1.0])

    fragments = []

    for i in range(len(breaks) - 1):
        start_frac = breaks[i]
        end_frac = breaks[i + 1]

        if end_frac - start_frac < 1e-6:
            continue  # Skip degenerate fragments

        # Calculate fragment pole positions along original axis
        frag_start = original_magnet.south_pole.position + start_frac * axis_vector
        frag_end = original_magnet.south_pole.position + end_frac * axis_vector

        # Fragment length
        frag_length = np.linalg.norm(frag_end - frag_start)

        # Fragment retains same pole strength (surface pole density unchanged)
        # New poles appear at break faces with opposite polarity
        fragments.append(
            Magnet.from_pole_data(
                pole_strength=pole_strength,
                north_position=frag_end,
                south_position=frag_start,
            )
        )

    return fragments


@maxwell_cite(
    380,
    part=3, chapter="Magnetic Matter",
    theory_class="maxwell_original",
    description="Verify broken magnet fragments are complete magnets",
)
def verify_fragments_complete(
    fragments: list[Magnet],
    tolerance: float = 1e-10,
) -> dict[str, any]:
    """
    Verify that all fragments from a broken magnet are complete.

    Art. 380: Every fragment, no matter how small, must have both
    N and S poles of equal strength.

    Args:
        fragments: List of fragment magnets.
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with:
        - all_complete: True if all fragments have both poles
        - fragment_count: Number of fragments
        - pole_imbalances: List of N-S imbalance for each fragment
        - verified: True if all fragments are complete magnets

    Reference:
        Part III, Art. 380: Fragment completeness.
    """
    if not fragments:
        return {
            "all_complete": False,
            "fragment_count": 0,
            "pole_imbalances": [],
            "verified": False,
        }

    pole_imbalances = []
    all_complete = True

    for frag in fragments:
        n_strength = abs(frag.north_pole.strength)
        s_strength = abs(frag.south_pole.strength)
        imbalance = abs(n_strength - s_strength)
        pole_imbalances.append(imbalance)

        if imbalance > tolerance:
            all_complete = False

    return {
        "all_complete": all_complete,
        "fragment_count": len(fragments),
        "pole_imbalances": pole_imbalances,
        "verified": all_complete,
        "tolerance_used": tolerance,
    }


@maxwell_cite(
    377, 378, 379, 380,
    part=3, chapter="Magnetic Matter",
    theory_class="maxwell_original",
    description="Molecular theory explanation of magnetization",
)
def molecular_magnetization_model(
    initial_molecules: list[MolecularMagnet],
    applied_field: np.ndarray,
    volume: float = 1.0,
) -> dict[str, np.ndarray | float]:
    """
    Model magnetization process using molecular theory.

    Art. 377-380: Magnetization is the process of aligning molecular
    magnets that were previously randomly oriented. The degree of
    alignment determines the macroscopic magnetization.

    This model simulates how an applied field causes molecular
    reorientation, computing the resulting bulk magnetization.

    Args:
        initial_molecules: Initial molecular magnets (may be random).
        applied_field: External H field causing alignment (gauss).
        volume: Volume containing molecules (cm³).

    Returns:
        Dictionary with:
        - initial_magnetization: Magnetization before field applied
        - final_magnetization: Magnetization after alignment
        - alignment_fraction: Fraction of aligned molecules
        - susceptibility_estimate: κ = |I|/|H| estimate

    Reference:
        Part III, Arts. 377-380: Molecular theory of magnetization.
    """
    applied_field = np.asarray(applied_field, dtype=np.float64)

    # Create matter theory object
    matter = MagneticMatterTheory.from_molecules(initial_molecules, volume)

    # Initial magnetization (before field)
    initial_I = matter.calc_magnetization()
    initial_mag = np.linalg.norm(initial_I)

    # Simulate alignment: each molecule experiences torque
    # Simplified model: molecules rotate toward field direction
    field_mag = np.linalg.norm(applied_field)

    if field_mag > 0:
        field_direction = applied_field / field_mag

        # Create aligned molecules
        aligned_molecules = []
        for mol in initial_molecules:
            # Simplified: partial alignment based on moment preservation
            # In reality, thermal agitation opposes complete alignment
            aligned_mol = MolecularMagnet(
                magnetic_moment=mol.magnetic_moment,
                position=mol.position,
                orientation=field_direction.copy(),
                is_aligned=True,
            )
            aligned_molecules.append(aligned_mol)
    else:
        aligned_molecules = initial_molecules

    # Final magnetization
    aligned_matter = MagneticMatterTheory.from_molecules(aligned_molecules, volume)
    final_I = aligned_matter.calc_magnetization()
    final_mag = np.linalg.norm(final_I)

    # Alignment fraction (all aligned in this simplified model)
    alignment = 1.0 if field_mag > 0 else 0.0

    # Estimate susceptibility
    if field_mag > 0:
        susceptibility = final_mag / field_mag
    else:
        susceptibility = 0.0

    return {
        "initial_magnetization": initial_I,
        "final_magnetization": final_I,
        "initial_magnitude": initial_mag,
        "final_magnitude": final_mag,
        "alignment_fraction": alignment,
        "susceptibility_estimate": susceptibility,
        "applied_field_magnitude": field_mag,
    }

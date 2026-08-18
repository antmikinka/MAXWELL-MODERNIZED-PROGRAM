"""maxwell.vortex_engine.vortex_lattice — Molecular vortices (Arts. 822-824, 831).

Maxwell's mechanical model of the ether: a lattice of molecular
vortices whose rotation produces magnetic phenomena and whose
disturbances propagate as electromagnetic waves.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi


@dataclass
class MolecularVortex:
    """Single molecular vortex (Arts. 822-823).

    Maxwell's hypothesis: magnetic fields are produced by
    rotating vortices in the ether. Each vortex has:
    - Angular velocity omega (proportional to magnetic field)
    - Density rho (ether density)
    - Radius r (molecular scale)

    The magnetic field H is related to the vortex parameters by:
        H ~ rho * omega * r^2

    Attributes:
        angular_velocity: Angular velocity of vortex rotation.
        density: Density of the ether medium.
        radius: Vortex radius.
        axis: Unit vector along vortex rotation axis.
    """

    angular_velocity: float
    density: float
    radius: float
    axis: np.ndarray = field(default_factory=lambda: np.array([0.0, 0.0, 1.0]))

    @maxwell_cite(822, part=4, theory_class="maxwell_original")
    def kinetic_energy(self) -> float:
        """Kinetic energy of a single vortex.

        T = (1/4) * rho * omega^2 * r^4 * L
        (for a cylindrical vortex of length L)

        For unit length:
        T = (1/4) * rho * omega^2 * r^4

        Returns:
            Kinetic energy per unit length.
        """
        return 0.25 * self.density * self.angular_velocity**2 * self.radius**4

    @maxwell_cite(822, part=4, theory_class="maxwell_original")
    def magnetic_field_equivalent(self) -> float:
        """Calculate the equivalent magnetic field of this vortex.

        H = (1/2) * rho * omega * r^2

        This is Maxwell's key insight: the magnetic field is
        proportional to the angular momentum of the vortex.

        Returns:
            Equivalent magnetic field H.
        """
        return 0.5 * self.density * self.angular_velocity * self.radius**2

    @maxwell_cite(822, part=4, theory_class="maxwell_original")
    def angular_momentum(self) -> np.ndarray:
        """Angular momentum of the vortex.

        L = I * omega = (1/2) * m * r^2 * omega
        For unit length: m = rho * pi * r^2

        Returns:
            Angular momentum vector.
        """
        mass_per_length = self.density * PI * self.radius**2
        moment_of_inertia = 0.5 * mass_per_length * self.radius**2
        return moment_of_inertia * self.angular_velocity * self.axis


@dataclass
class VortexLattice:
    """Lattice of molecular vortices (Arts. 822-824).

    A regular array of vortices filling space, with adjacent
    vortices rotating in opposite directions (like gears).
    The collective behavior of the lattice produces the
    macroscopic magnetic field.
    """

    vortices: list[MolecularVortex] = field(default_factory=list)
    lattice_spacing: float = 1.0e-8  # ~molecular scale, cm

    @maxwell_cite(822, part=4, theory_class="maxwell_original")
    def add_vortex(self, vortex: MolecularVortex) -> None:
        """Add a vortex to the lattice."""
        self.vortices.append(vortex)

    @maxwell_cite(822, part=4, theory_class="maxwell_original")
    def total_magnetic_field(self) -> np.ndarray:
        """Calculate the net magnetic field from all vortices.

        The superposition of all vortex contributions.

        Returns:
            Net magnetic field vector.
        """
        H_total = np.zeros(3)
        for v in self.vortices:
            H_total += v.magnetic_field_equivalent() * v.axis
        return H_total

    @maxwell_cite(822, part=4, theory_class="maxwell_original")
    def total_kinetic_energy(self) -> float:
        """Total kinetic energy of the vortex lattice.

        Returns:
            Sum of kinetic energies of all vortices.
        """
        return sum(v.kinetic_energy() for v in self.vortices)

    @maxwell_cite(822, part=4, theory_class="maxwell_original")
    def verify_vortex_gear_condition(self) -> bool:
        """Verify adjacent vortices rotate in opposite directions.

        For the lattice to be mechanically stable, adjacent
        vortices must rotate in opposite directions (like
        meshing gears). Maxwell introduced idle wheels
        (small particles) between vortices to achieve this.

        Returns:
            True if the gear condition is satisfied.
        """
        if len(self.vortices) < 2:
            return True
        # Check that vortices have alternating rotation sense
        # For a simple 1D chain, omega should alternate sign
        for i in range(len(self.vortices) - 1):
            w1 = self.vortices[i].angular_velocity
            w2 = self.vortices[i + 1].angular_velocity
            if w1 * w2 > 0:
                return False
        return True


@maxwell_cite(831, part=4, theory_class="maxwell_original")
def append_mechanical_theory_notes() -> dict[str, str]:
    """Notes on the mechanical theory of vortices.

    Art. 831: Maxwell's notes on the limitations and
    implications of the molecular vortex hypothesis.

    Returns:
        Notes dictionary.
    """
    return {
        "note_1": "The vortex model provides a mechanical picture of "
        "magnetic phenomena, but the exact nature of the "
        "ether remains speculative.",
        "note_2": "The idle-wheel particles between vortices serve as "
        "electricity -- their motion constitutes electric current.",
        "note_3": "The model successfully explains Faraday rotation as a "
        "modification of vortex speeds by the applied field.",
        "note_4": "The wave speed in the vortex lattice equals the "
        "speed of light, confirming the electromagnetic "
        "theory of light.",
        "note_5": "Maxwell does not claim the vortex model is literally "
        "true -- it is a working hypothesis that connects "
        "diverse phenomena.",
    }

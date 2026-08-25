"""maxwell.vortex_engine.vortex_lattice — Molecular vortices (Arts. 822-824, 831).

Maxwell's mechanical model of the medium: a lattice of molecular
vortices whose angular velocity is connected with magnetic force and
whose disturbances propagate as waves (Maxwell 1873, Part IV, Ch. XXI,
"Molecular Vortices", Arts. 822-824; Note, Art. 831).

Modelling caveat (documented for Stage-3 defect D-08): Art. 822 states
only that the magnetic action is connected with the angular velocity of
the vortices — it fixes no calibration constant carrying gauss
dimensions.  :meth:`MolecularVortex.magnetic_field_equivalent` is
therefore a constitutive assumption of this mechanical model
(H = (1/2) rho omega r^2, proportional to the angular momentum per unit
length), and its output is a model quantity, not a calibrated CGS field;
tests assert proportionality and internal consistency only.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite

PI = np.pi


@dataclass
class MolecularVortex:
    """Single molecular vortex (Arts. 822-823).

    Maxwell's hypothesis (Art. 822): the magnetic action in the medium
    is connected with the rotation of vortices; each vortex has angular
    velocity omega, density rho, radius r, and an axis.

    Attributes:
        angular_velocity: Angular velocity of vortex rotation (rad/s).
        density: Density of the medium carried by the vortex (g/cm^3).
        radius: Vortex radius (cm).
        axis: Unit vector along the vortex rotation axis.
    """

    angular_velocity: float
    density: float
    radius: float
    axis: np.ndarray = field(default_factory=lambda: np.array([0.0, 0.0, 1.0]))

    @maxwell_cite(822, part=4, theory_class="standard_math")
    def kinetic_energy(self) -> float:
        """Kinetic energy of a single vortex per unit length (Art. 822).

        A cylindrical vortex of unit length has mass m = rho pi r^2 and
        moment of inertia I = (1/2) m r^2 = (pi/2) rho r^4, hence

            T = (1/2) I omega^2 = (pi/4) rho omega^2 r^4.

        The factor pi makes this consistent with T = (1/2) L omega using
        :meth:`angular_momentum` (pre-fix code dropped the pi).

        Returns:
            Kinetic energy per unit length (erg/cm).
        """
        return (PI / 4.0) * self.density * self.angular_velocity**2 * self.radius**4

    @maxwell_cite(822, part=4, theory_class="maxwell_original")
    def magnetic_field_equivalent(self) -> float:
        """Equivalent magnetic quantity of this vortex (Art. 822, model).

        Constitutive assumption of the mechanical model: the magnetic
        quantity carried by the vortex is taken proportional to its
        angular momentum per unit length,

            H_model = (1/2) rho omega r^2.

        Art. 822 asserts the connection between magnetic action and
        vortex rotation without fixing the calibration constant, so this
        value is a model quantity (consistent in proportionality), not a
        CGS-gauss-calibrated field.

        Returns:
            Model magnetic quantity of the vortex.
        """
        return 0.5 * self.density * self.angular_velocity * self.radius**2

    @maxwell_cite(822, part=4, theory_class="standard_math")
    def angular_momentum(self) -> np.ndarray:
        """Angular momentum of the vortex per unit length.

        L = I omega = (1/2) m r^2 omega, with m = rho pi r^2 per unit
        length, directed along the vortex axis.  Satisfies
        T = (1/2) |L| omega with :meth:`kinetic_energy`.

        Returns:
            Angular momentum vector (per unit length).
        """
        mass_per_length = self.density * PI * self.radius**2
        moment_of_inertia = 0.5 * mass_per_length * self.radius**2
        return moment_of_inertia * self.angular_velocity * self.axis


@dataclass
class VortexLattice:
    """Lattice of molecular vortices (Arts. 822-824).

    A regular array of vortices filling the medium, with adjacent
    vortices rotating in opposite directions (like meshing gears);
    Maxwell introduced idle-wheel particles between vortices to permit
    this.  The collective behaviour of the lattice produces the
    macroscopic magnetic action.
    """

    vortices: list[MolecularVortex] = field(default_factory=list)
    lattice_spacing: float = 1.0e-8  # ~molecular scale, cm

    @maxwell_cite(822, part=4, theory_class="standard_math")
    def add_vortex(self, vortex: MolecularVortex) -> None:
        """Add a vortex to the lattice."""
        self.vortices.append(vortex)

    @maxwell_cite(822, part=4, theory_class="standard_math")
    def total_magnetic_field(self) -> np.ndarray:
        """Net model magnetic quantity of all vortices (superposition).

        Returns:
            Vector sum of each vortex's magnetic_field_equivalent along
            its axis.
        """
        H_total = np.zeros(3)
        for v in self.vortices:
            H_total += v.magnetic_field_equivalent() * v.axis
        return H_total

    @maxwell_cite(822, part=4, theory_class="standard_math")
    def total_kinetic_energy(self) -> float:
        """Total kinetic energy of the vortex lattice (per unit length).

        Returns:
            Sum of kinetic energies of all vortices.
        """
        return sum(v.kinetic_energy() for v in self.vortices)

    @maxwell_cite(822, part=4, theory_class="standard_math")
    def total_angular_momentum(self) -> np.ndarray:
        """Total angular momentum of the lattice (per unit length).

        Returns:
            Vector sum of the vortices' angular momenta.
        """
        L_total = np.zeros(3)
        for v in self.vortices:
            L_total += v.angular_momentum()
        return L_total

    @maxwell_cite(822, part=4, theory_class="maxwell_original")
    def verify_vortex_gear_condition(self) -> bool:
        """Verify adjacent vortices rotate in opposite directions.

        For the lattice to be mechanically consistent, adjacent vortices
        must rotate in opposite directions (like meshing gears); Maxwell
        introduced idle-wheel particles between vortices to achieve this.
        In a 1D chain the signed angular velocities must therefore
        alternate.

        Returns:
            True if every adjacent pair has opposite rotation sense.

        Raises:
            ValueError: If the lattice contains fewer than two vortices,
                since no adjacency exists to test (pre-fix code returned
                a vacuous True, masking the undefined case).
        """
        if len(self.vortices) < 2:
            raise ValueError(
                "the gear condition relates adjacent vortices; at least "
                "two vortices are required to test it"
            )
        for i in range(len(self.vortices) - 1):
            w1 = self.vortices[i].angular_velocity
            w2 = self.vortices[i + 1].angular_velocity
            if w1 * w2 >= 0:  # same sign, or a stationary vortex: not gears
                return False
        return True


@maxwell_cite(
    831,
    part=4,
    theory_class="maxwell_original",
    description="Computed mechanical state of the vortex medium: energies, "
    "angular momentum, net model field, wave speed, and the gear condition.",
)
def append_mechanical_theory_notes(
    lattice: VortexLattice,
    elastic_constant: float,
) -> dict:
    """Computed summary of the mechanical theory of vortices (Art. 831).

    Maxwell 1873, Art. 831 (Note): the whole chapter expands Sir William
    Thomson's 1856 remark — in a magnetized medium "a motion exists when
    transmitting no light", the luminiferous motion is only a component
    of the whole motion, and the elastic reaction being the same for the
    same displacements while the luminiferous motions are unequal is the
    dynamical explanation of the different propagation rates of right-
    and left-circularly polarized light.  The theory is expressly
    provisional ("resting... on unproved hypotheses relating to the
    nature of molecular vortices", Art. 830).

    Every entry below is computed from the lattice (no prose results):

    Args:
        lattice: The vortex lattice whose mechanical state is summarized.
        elastic_constant: Elastic constant of the medium (so that the
            transverse wave speed is sqrt(elastic_constant / density)).

    Returns:
        Dictionary with computed entries:
            vortex_count: Number of vortices.
            total_kinetic_energy: Sum of vortex kinetic energies.
            total_angular_momentum: Vector sum of angular momenta (the
                "motion existing when transmitting no light").
            net_magnetic_field: Superposed model magnetic quantity.
            mean_density: Mean medium density of the vortices.
            wave_speed: sqrt(elastic_constant / mean_density) (cm/s).
            wave_speed_over_light: wave_speed / c (equals 1 when the
                lattice is calibrated to the electromagnetic theory of
                light, elastic_constant = rho c^2).
            gear_condition_satisfied: Result of
                VortexLattice.verify_vortex_gear_condition().

    Raises:
        ValueError: If the lattice is empty (density undefined) or has
            fewer than two vortices (gear condition undefined).
    """
    if not lattice.vortices:
        raise ValueError("cannot summarize an empty lattice")
    kinetic = lattice.total_kinetic_energy()
    angular_momentum = lattice.total_angular_momentum()
    net_field = lattice.total_magnetic_field()
    mean_density = float(np.mean([v.density for v in lattice.vortices]))
    wave_speed = float(np.sqrt(elastic_constant / mean_density))
    return {
        "vortex_count": len(lattice.vortices),
        "total_kinetic_energy": kinetic,
        "total_angular_momentum": angular_momentum,
        "net_magnetic_field": net_field,
        "mean_density": mean_density,
        "wave_speed": wave_speed,
        "wave_speed_over_light": wave_speed / CONST.C,
        "gear_condition_satisfied": lattice.verify_vortex_gear_condition(),
    }

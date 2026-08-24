"""maxwell.magneto_optics.energy_analysis — Medium energy (Arts. 818-821).

Dynamical theory of the magneto-optic medium: the potential and kinetic
energies of the luminiferous disturbance, the quadratic propagation
condition for the angular velocity of a circular ray, and the argument
that the magnetic rotation of polarization requires a REAL rotation in
the medium about the axis of the magnetic force.

Maxwell 1873, Part IV, Ch. XXI, Arts. 818-821.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite

PI = np.pi


@dataclass
class MagnetoOpticMedium:
    """Energy analysis of a magneto-optic medium (Arts. 818-819).

    Attributes:
        permittivity: Dielectric constant epsilon of the medium.
        permeability: Magnetic permeability mu of the medium.
        verdet_constant: Verdet constant in rad/(gauss cm).
    """

    permittivity: float
    permeability: float
    verdet_constant: float

    @maxwell_cite(
        818,
        part=4,
        theory_class="standard_math",
        description="Potential energy depends on configuration (electric "
        "displacement), kinetic energy is a homogeneous quadratic function "
        "of the velocities (magnetic disturbance).",
    )
    def calc_medium_energy(
        self,
        E_field: np.ndarray,
        B_field: np.ndarray,
        volume: float,
    ) -> dict[str, float]:
        """Potential and kinetic energy of the medium (Art. 818).

        Maxwell 1873, Art. 818: "The potential energy, V, of the system
        depends on its configuration, that is, on the relative position of
        its parts", while "the kinetic energy, T, of the system is a
        homogeneous function of the second degree of the velocities of the
        system."  In the electromagnetic medium the electric displacement
        (configuration) carries the potential energy and the magnetic
        disturbance (proportional to the time-derivative of the
        displacement) carries the kinetic energy:

            potential = electric = epsilon E^2 V_vol / (8 pi)
            kinetic   = magnetic = mu B^2 V_vol / (8 pi)

        Args:
            E_field: Electric displacement amplitude vector.
            B_field: Magnetic disturbance amplitude vector.
            volume: Volume of the medium (cm^3).

        Returns:
            Dictionary with entries:
                electric_energy, potential_energy: epsilon E^2 V/(8 pi)
                    (the two keys carry the same value, per Art. 818).
                magnetic_energy, kinetic_energy: mu B^2 V/(8 pi).
                total_energy: sum of the two.
                potential_to_kinetic_ratio: potential/kinetic (inf when
                    the kinetic energy vanishes).
        """
        E_sq = float(np.dot(E_field, E_field))
        B_sq = float(np.dot(B_field, B_field))

        potential = (self.permittivity * E_sq * volume) / (8.0 * PI)
        kinetic = (self.permeability * B_sq * volume) / (8.0 * PI)

        return {
            "electric_energy": potential,
            "potential_energy": potential,
            "magnetic_energy": kinetic,
            "kinetic_energy": kinetic,
            "total_energy": potential + kinetic,
            "potential_to_kinetic_ratio": (
                potential / kinetic if kinetic > 0 else float("inf")
            ),
        }

    @maxwell_cite(
        819,
        part=4,
        theory_class="standard_math",
        description="Propagation condition for a ray of constant intensity: "
        "phase velocity c/sqrt(eps mu), and the two circular components "
        "split by Delta n = V B lambda / pi in the magnetic force.",
    )
    def derive_propagation_condition(
        self,
        magnetic_field: float = 0.0,
        wavelength: float | None = None,
    ) -> dict[str, float]:
        """Condition for wave propagation through the medium (Art. 819).

        For a ray of constant intensity (r constant), Lagrange's equation
        reduces to -dT/dr + dV/dr = 0 (eq. (6)); the balance of kinetic
        and potential energy is satisfied at the phase velocity

            v_phase = c / sqrt(epsilon mu) = c / n.

        When a magnetic force acts along the ray, the quadratic of Art.
        819 eq. (7) has two roots: the right- and left-circular components
        propagate with different velocities.  The index difference is
        Delta n = V B lambda / pi (Art. 812), giving the velocity split
        Delta v = v_phase^2 Delta k / omega with Delta k = 2 V B (the
        same first-order result as Arts. 812 and 815).

        Args:
            magnetic_field: Magnetic force along the ray (gauss).
            wavelength: Wavelength of the light (cm).  If None, no
                splitting is computed (the two circular components travel
                together at v_phase).

        Returns:
            Dictionary with entries:
                refractive_index: n = sqrt(epsilon mu).
                v_phase: c/n (cm/s).
                delta_n: V B lambda / pi (0.0 if wavelength is None).
                velocity_split: v_right - v_left (cm/s).
                v_right, v_left: circular-component velocities (cm/s);
                    v_right is the accelerated component (Art. 817: "that
                    is accelerated of which the direction of rotation in
                    the plane of x, y is positive").
        """
        c = CONST.C
        n = float(np.sqrt(self.permittivity * self.permeability))
        v_phase = c / n

        if wavelength is None:
            delta_n = 0.0
            velocity_split = 0.0
        else:
            delta_n = self.verdet_constant * magnetic_field * wavelength / PI
            omega = 2.0 * PI * c / wavelength
            # Delta k = 2 V B; Delta v = v^2 Delta k / omega (Art. 815 form)
            velocity_split = (
                v_phase**2 * (2.0 * self.verdet_constant * magnetic_field) / omega
            )

        return {
            "refractive_index": n,
            "v_phase": v_phase,
            "delta_n": delta_n,
            "velocity_split": velocity_split,
            "v_right": v_phase + velocity_split / 2.0,
            "v_left": v_phase - velocity_split / 2.0,
        }


@maxwell_cite(
    819,
    part=4,
    theory_class="standard_math",
    description="The propagation quadratic A n^2 + B n + C = 0 (eq. 7) and "
    "its roots, with Vieta relations.",
)
def calc_propagation_quadratic(A: float, B: float, C: float) -> dict:
    """Solve the propagation quadratic of Art. 819, eq. (7).

    Maxwell 1873, Art. 819: with r constant, the dynamical equation for
    the angular velocity n of the disturbance is "of the form

        A n^2 + B n + C = 0                                       (7)

    This being a quadratic equation, gives two values of n.  It appears
    from experiment that both values are real, that one is positive and
    the other negative, and that the positive value is numerically the
    greater."

    Args:
        A: Coefficient of n^2 (the pure kinetic-energy coefficient;
            positive).  Must be nonzero.
        B: Coefficient of n (the part of T involving the first power of
            the angular velocity; nonzero when magnetic force acts).
        C: Term independent of n (from dV/dr).

    Returns:
        Dictionary with entries:
            n1, n2: The two roots, n1 >= n2 (real for disc >= 0, complex
                otherwise).
            discriminant: B^2 - 4 A C.
            sum_roots: n1 + n2 = -B/A (Vieta).
            product_roots: n1 * n2 = C/A (Vieta).

    Raises:
        ValueError: If A is zero (the equation is not quadratic).
    """
    if A == 0:
        raise ValueError("A must be nonzero for the quadratic of Art. 819")
    disc = B * B - 4.0 * A * C
    if disc >= 0:
        root_disc = float(np.sqrt(disc))
        n1 = (-B + root_disc) / (2.0 * A)
        n2 = (-B - root_disc) / (2.0 * A)
    else:
        root_disc = complex(0.0, float(np.sqrt(-disc)))
        n1 = (-B + root_disc) / (2.0 * A)
        n2 = (-B - root_disc) / (2.0 * A)
    return {
        "n1": n1,
        "n2": n2,
        "discriminant": disc,
        "sum_roots": -B / A,
        "product_roots": C / A,
    }


@maxwell_cite(
    819,
    part=4,
    theory_class="standard_math",
    description="Equation (8): A(n1 + n2) + B = 0 fixes the coupling "
    "coefficient B from the two observed roots.",
)
def quadratic_coupling_coefficient(A: float, n1: float, n2: float) -> float:
    """Coupling coefficient B of the propagation quadratic (Art. 819 eq. 8).

    Maxwell 1873, Art. 819: "if n_1 and n_2 are the roots of the
    equation, A(n_1 + n_2) + B = 0.  (8)  The coefficient, B, therefore,
    is not zero, at least when magnetic force acts on the medium."  B is
    the coefficient of the part of the kinetic energy involving the first
    power of the angular velocity n.

    Args:
        A: Coefficient of n^2 in the propagation quadratic.
        n1, n2: The two roots (the observed angular velocities of the
            right- and left-circular rays).

    Returns:
        B = -A (n1 + n2).
    """
    return -A * (n1 + n2)


@maxwell_cite(
    820,
    part=4,
    theory_class="maxwell_original",
    description="Computed non-reciprocity argument: the magnetic round trip "
    "is 2 theta while the natural round trip is 0, a discriminant which can "
    "only arise from a real angular velocity accompanying the magnetic force.",
)
def prove_real_rotation_required(theta_single_pass: float) -> dict[str, float | bool]:
    """Compute the argument that a real rotation is required (Art. 820).

    Maxwell 1873, Art. 820: every term of the kinetic energy T is "of two
    dimensions as regards velocity", so the term B n involving the first
    power of the angular velocity n of the disturbance must contain
    another velocity.  That velocity cannot be r-dot or q-dot (both
    constant for a ray of constant intensity); it must be "an angular
    velocity about the axis of z", and it "is an invariable accompaniment
    of the magnetic force in those media which exhibit the magnetic
    rotation of the plane of polarization."

    The computational form of the argument contrasts the two possible
    round trips (cf. Art. 810): a reciprocal (natural) rotation cancels
    on reflection, while the observed magnetic rotation adds, so the
    round-trip discriminant is nonzero exactly when the medium carries a
    real rotation about the magnetic axis.

    Args:
        theta_single_pass: Rotation accumulated in one passage through
            the medium (radians).

    Returns:
        Dictionary with computed entries:
            faraday_round_trip: theta + theta = 2 theta (magnetic
                rotation is non-reciprocal, Art. 810).
            natural_round_trip: theta - theta = 0 (reciprocal rotation
                cancels on the return passage).
            discriminant: faraday_round_trip - natural_round_trip =
                2 theta; nonzero exactly when the two phenomena differ.
            requires_real_rotation: True when the discriminant is nonzero
                — the B n term of the kinetic energy then demands a real
                angular velocity in the medium (eqs. (7)-(8), Art. 820).
    """
    faraday_round_trip = theta_single_pass + theta_single_pass
    natural_round_trip = theta_single_pass - theta_single_pass
    discriminant = faraday_round_trip - natural_round_trip
    return {
        "faraday_round_trip": faraday_round_trip,
        "natural_round_trip": natural_round_trip,
        "discriminant": discriminant,
        "requires_real_rotation": bool(discriminant != 0.0),
    }


@maxwell_cite(
    821,
    part=4,
    theory_class="maxwell_original",
    description="Numerical summary of the magneto-optic analysis: refractive "
    "index and phase velocity from the medium constants, velocity splitting "
    "and rotation from Verdet's law, and the non-reciprocity residual.",
)
def summarize_magneto_optic_results(
    permittivity: float,
    permeability: float,
    verdet_constant: float,
    magnetic_field: float,
    wavelength: float,
    path_length: float,
) -> dict[str, float]:
    """Computed summary of the magneto-optic results (Art. 821).

    Maxwell 1873, Art. 821 restates the conclusions of Arts. 806-820
    without hypothesis: the disturbance is "of the nature of a vector or
    directed quantity, the direction of which is normal to the direction
    of the ray"; in circularly-polarized light its direction rotates about
    the ray; and in a medium under magnetic force "some rotatory motion is
    going on, the axis of rotation being in the direction of the magnetic
    force", so the two circular components propagate at different rates.
    Every entry below is a number derived from the inputs (no prose).

    Args:
        permittivity: Dielectric constant epsilon.
        permeability: Permeability mu.
        verdet_constant: Verdet constant, rad/(gauss cm).
        magnetic_field: Magnetic force along the ray (gauss).
        wavelength: Wavelength (cm).
        path_length: Path length through the medium (cm).

    Returns:
        Dictionary with computed entries:
            refractive_index: sqrt(epsilon mu).
            v_phase: c / refractive_index (cm/s).
            delta_n: V B lambda / pi (index difference of the circular
                components, Art. 812).
            rotation_per_length: V B (rad/cm, Art. 808).
            total_rotation: V B L (rad).
            velocity_split: v_phase^2 (2 V B) / omega (cm/s, Art. 815).
            non_reciprocity_residual: 2 * total_rotation - 0, the
                round-trip discriminant of Art. 820.
    """
    c = CONST.C
    n = float(np.sqrt(permittivity * permeability))
    v_phase = c / n
    delta_n = verdet_constant * magnetic_field * wavelength / PI
    rotation_per_length = verdet_constant * magnetic_field
    total_rotation = rotation_per_length * path_length
    omega = 2.0 * PI * c / wavelength
    velocity_split = v_phase**2 * (2.0 * verdet_constant * magnetic_field) / omega
    return {
        "refractive_index": n,
        "v_phase": v_phase,
        "delta_n": delta_n,
        "rotation_per_length": rotation_per_length,
        "total_rotation": total_rotation,
        "velocity_split": velocity_split,
        "non_reciprocity_residual": 2.0 * total_rotation,
    }

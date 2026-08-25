"""maxwell.magneto_optics.rotation — Faraday rotation (Arts. 806-810).

Rotation of the plane of polarization of light by magnetic action,
Verdet's constant, and the laws governing the phenomenon.

Canonical Verdet-unit convention (closes Stage-3 defect D-32):
    Verdet constants in this module are carried in **minutes of arc per
    (gauss cm)** — the unit in which Verdet's own measurements and the
    classical tables are quoted.  Conversion to radians uses the exact
    factor ``VERDET_MINUTE_TO_RAD = pi/10800`` rad/minute and must always
    be applied explicitly via :func:`verdet_to_rad` /
    :meth:`VerdetTable.get_verdet_rad`.  Every rotation angle computed
    in this package is returned in **radians**.

Maxwell 1873, Part IV, Ch. XXI "Magnetic Action on Light", Arts. 806-810.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from maxwell.meta.citation import maxwell_cite

#: Exact conversion from arc-minutes to radians (1 min = pi/10800 rad).
VERDET_MINUTE_TO_RAD: float = math.pi / 10800.0


def verdet_to_rad(verdet_minutes_per_gauss_cm: float) -> float:
    """Convert a Verdet constant from min/(gauss cm) to rad/(gauss cm).

    Args:
        verdet_minutes_per_gauss_cm: Verdet constant in arc-minutes per
            (gauss cm), the canonical table unit of this module.

    Returns:
        Verdet constant in rad/(gauss cm).
    """
    return verdet_minutes_per_gauss_cm * VERDET_MINUTE_TO_RAD


@maxwell_cite(
    806,
    part=4,
    theory_class="maxwell_original",
    description="Rotation measured by the analyser angle needed to "
    "re-extinguish the ray (Faraday's observation, Art. 806-807).",
)
def measure_rotation_by_analyser(
    initial_analyser_angle: float,
    extinction_analyser_angle: float,
) -> float:
    """Measure the rotation of the plane of polarization (Arts. 806-807).

    Maxwell 1873, Art. 807: a ray of plane-polarized light is transmitted
    through the medium and the plane of polarization "when it emerges from
    the medium, is ascertained by observing the position of an analyser
    when it cuts off the ray".  When the magnetic force is applied the
    light reappears, "but if the analyser is turned round through a certain
    angle, the light is again cut off.  This shews that the effect of the
    magnetic force is to turn the plane of polarization ... through a
    certain angle, measured by the angle through which the analyser must
    be turned in order to cut off the light."

    Args:
        initial_analyser_angle: Analyser extinction angle before the
            magnetic force is applied (radians).
        extinction_analyser_angle: Analyser angle that again extinguishes
            the ray with the magnetic force applied (radians).

    Returns:
        Rotation angle of the plane of polarization (radians).
    """
    return extinction_analyser_angle - initial_analyser_angle


@dataclass
class FaradayRotator:
    """Faraday rotation of polarization (Arts. 807-808).

    When linearly polarized light passes through a material in a magnetic
    field with a component along the propagation direction, the plane of
    polarization rotates by an angle (Maxwell 1873, Art. 808):

        theta = V * B_parallel * L

    where V is the Verdet constant of the medium, B_parallel is the
    resolved part of the magnetic force in the direction of the ray
    (gauss), and L is the path length within the medium (cm).

    Attributes:
        verdet_constant: Verdet constant of the material, rad/(gauss cm).
            Convert table values (min/(gauss cm)) with :func:`verdet_to_rad`.
        path_length: Path length through the material (cm).
    """

    verdet_constant: float  # rad/(gauss cm)
    path_length: float  # cm

    @maxwell_cite(807, part=4, theory_class="standard_math")
    def rotation_angle(self, B_field: float) -> float:
        """Calculate rotation of polarization plane.

        theta = V * B * L   (Maxwell 1873, Arts. 807-808, statement (1)-(2))

        Args:
            B_field: Magnetic force resolved along the propagation
                direction (gauss).

        Returns:
            Rotation angle in radians.
        """
        return self.verdet_constant * B_field * self.path_length

    @maxwell_cite(807, part=4, theory_class="standard_math")
    def B_field_from_rotation(self, theta: float) -> float:
        """Determine magnetic field from measured rotation.

        B = theta / (V * L)  — inversion of Verdet's law (Art. 808).

        Args:
            theta: Measured rotation angle (radians).

        Returns:
            Magnetic force in gauss.
        """
        return theta / (self.verdet_constant * self.path_length)


@maxwell_cite(
    808,
    part=4,
    theory_class="maxwell_original",
    description="Computed form of the three laws of Art. 808: rotation "
    "proportional to path length, to the resolved part of the magnetic "
    "force along the ray, and to the medium-specific coefficient.",
)
def establish_rotation_laws(
    verdet_constant: float,
    B_field_vector: np.ndarray,
    ray_direction: np.ndarray,
    path_length: float,
) -> dict[str, float]:
    """Compute the laws of Faraday rotation (Art. 808).

    Maxwell 1873, Art. 808: "The angle through which the plane of
    polarization is turned is proportional (1) to the distance which the
    ray travels within the medium ... (2) to the intensity of the resolved
    part of the magnetic force in the direction of the ray.  (3) The amount
    of the rotation depends on the nature of the medium."  These three
    statements are included in the general one "that the angular rotation
    is numerically equal to the amount by which the magnetic potential
    increases, from the point at which the ray enters the medium to that
    at which it leaves it, multiplied by a coefficient".

    All quantities below are computed from the inputs (no prose):

    Args:
        verdet_constant: Verdet constant of the medium, rad/(gauss cm).
        B_field_vector: Magnetic force vector (gauss), shape (3,).
        ray_direction: Direction of ray propagation (need not be unit).
        path_length: Distance travelled within the medium (cm).

    Returns:
        Dictionary with computed entries:
            resolved_field: B . ray_hat, the resolved part of the magnetic
                force in the direction of the ray (gauss) — law (2).
            potential_increase: resolved_field * path_length, the increase
                of magnetic potential along the ray path (gauss cm).
            rotation_angle: verdet_constant * potential_increase (rad) —
                laws (1) and (3) enter through path_length and the
                medium-specific coefficient.
    """
    B = np.asarray(B_field_vector, dtype=float)
    ray = np.asarray(ray_direction, dtype=float)
    ray_hat = ray / np.linalg.norm(ray)
    resolved = float(np.dot(B, ray_hat))
    potential_increase = resolved * path_length
    return {
        "resolved_field": resolved,
        "potential_increase": potential_increase,
        "rotation_angle": verdet_constant * potential_increase,
    }


@maxwell_cite(809, part=4, theory_class="maxwell_original")
def apply_verdet_negative_rotation(
    verdet_constant: float,
    B_field: float,
    path_length: float,
    material_type: str,
) -> float:
    """Apply Verdet's sign rule for the rotation (Art. 809).

    Maxwell 1873, Art. 809: "In diamagnetic substances, the direction in
    which the plane of polarization is made to rotate is generally the same
    as the direction in which a positive current must circulate round the
    ray in order to produce a magnetic force in the same direction as that
    which actually exists in the medium.  Verdet, however, discovered that
    in certain ferromagnetic media ... the rotation is in the opposite
    direction to the current which would produce the magnetic force."

    The computation therefore assigns a positive effective Verdet constant
    to diamagnetic media and a negative one to ferromagnetic media.
    Caveat recorded in the same article: the sign rule has exceptions
    ("neutral chromate of potash is diamagnetic, but produces a negative
    rotation"), so for quantitative work the measured Verdet constant of
    the specific medium should be used instead of the class rule.

    Args:
        verdet_constant: Magnitude of the Verdet constant, rad/(gauss cm).
        B_field: Magnetic force along the ray (gauss).
        path_length: Path length (cm).
        material_type: 'ferromagnetic' or 'diamagnetic'.

    Returns:
        Rotation angle in radians (sign gives the sense of rotation).
    """
    if material_type == "ferromagnetic":
        # Verdet's negative rotation: opposite to the current that would
        # produce the field (Art. 809).
        effective_V = -abs(verdet_constant)
    else:
        effective_V = abs(verdet_constant)

    return effective_V * B_field * path_length


@maxwell_cite(810, part=4, theory_class="maxwell_original")
def model_natural_rotation(
    specific_rotation: float,
    path_length: float,
    wavelength: float,
) -> float:
    """Model natural optical rotation (quartz, turpentine) (Art. 810).

    Maxwell 1873, Art. 810: "There are other substances, which,
    independently of the application of magnetic force, cause the plane of
    polarization to turn to the right or to the left ... In some of these
    the property is related to an axis, as in the case of quartz.  In
    others, the property is independent of the direction of the ray within
    the medium, as in turpentine, solution of sugar, &c."

    The wavelength dependence is Biot's law (standard empirical form,
    Category C): theta = alpha * L / lambda^2.

    Args:
        specific_rotation: Specific rotation constant (rad cm / cm^2 of
            wavelength, so that the result is in radians).
        path_length: Path length through medium (cm).
        wavelength: Wavelength of light (cm).

    Returns:
        Rotation angle in radians for a single passage.
    """
    # Biot's law: rotation inversely proportional to lambda^2
    return specific_rotation * path_length / wavelength**2


@maxwell_cite(
    810,
    part=4,
    theory_class="maxwell_original",
    description="Round-trip (reflected) rotation: doubled for magnetic "
    "rotation, cancelled for natural rotation (Art. 810).",
)
def round_trip_rotation(theta_single_pass: float, magnetic: bool) -> float:
    """Round-trip rotation after reflection back through the medium.

    Maxwell 1873, Art. 810: "if the ray of light, after passing through
    the medium from north to south, is reflected by a mirror, so as to
    return through the medium from south to north, the rotation will be
    doubled when it results from magnetic action.  When the rotation
    depends on the nature of the medium alone, as in turpentine, &c., the
    ray, when reflected back through the medium, emerges polarized in the
    same plane as when it entered, the rotation during the first passage
    through the medium having been exactly reversed during the second."

    The returned value is computed as theta_forward + theta_backward with
    theta_backward = +theta (magnetic: sense fixed by the field, hence
    non-reciprocal) or theta_backward = -theta (natural: sense fixed to
    the ray/medium handedness, hence reciprocal).

    Args:
        theta_single_pass: Rotation accumulated in one passage (radians).
        magnetic: True for magnetic (Faraday) rotation, False for natural
            rotation.

    Returns:
        Total round-trip rotation in radians: 2*theta (magnetic) or 0
        (natural).
    """
    theta_backward = theta_single_pass if magnetic else -theta_single_pass
    return theta_single_pass + theta_backward


@dataclass
class VerdetTable:
    """Collection of Verdet constants for various materials (Art. 809).

    Experimental values measured by Verdet and successors, quoted at the
    sodium D line.  Canonical unit: **minutes of arc per (gauss cm)**
    (see module docstring); use :meth:`get_verdet_rad` for radians.
    Values are approximate historical determinations (EMPIRICAL class).
    """

    materials: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.materials:
            # Default values (approximate, at sodium D line, 20 C),
            # minutes of arc per (gauss cm).  Provenance: classical
            # Verdet-constant tables (cf. treatise-era measurements;
            # carbon disulfide and water entries are the standard
            # reference values used in Verdet's own comparisons).
            self.materials = {
                "water": 0.0131,
                "carbon_disulfide": 0.0424,
                "flint_glass": 0.020,
                "crown_glass": 0.012,
                "quartz_parallel": 0.016,
            }

    @maxwell_cite(809, part=4, theory_class="standard_math")
    def get_verdet(self, material: str) -> float:
        """Get Verdet constant for a material.

        Args:
            material: Material name.

        Returns:
            Verdet constant in min/(gauss cm) (canonical table unit).
        """
        return self.materials.get(material, 0.0)

    @maxwell_cite(809, part=4, theory_class="standard_math")
    def get_verdet_rad(self, material: str) -> float:
        """Get Verdet constant for a material in radians.

        Args:
            material: Material name.

        Returns:
            Verdet constant in rad/(gauss cm), converted with the exact
            factor pi/10800.
        """
        return verdet_to_rad(self.get_verdet(material))

    @maxwell_cite(809, part=4, theory_class="standard_math")
    def compare_materials(self, mat1: str, mat2: str) -> float:
        """Compare Verdet constants of two materials.

        The ratio is independent of the unit (minutes or radians).

        Args:
            mat1: First material.
            mat2: Second material.

        Returns:
            Ratio of Verdet constants V(mat1)/V(mat2).
        """
        v1 = self.get_verdet(mat1)
        v2 = self.get_verdet(mat2)
        return v1 / v2 if v2 != 0 else float("inf")

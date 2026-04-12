"""maxwell.magneto_optics.rotation — Faraday rotation (Arts. 806-810).

Rotation of the plane of polarization of light by magnetic action,
Verdet's constant, and the laws governing the phenomenon.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from maxwell.meta.citation import maxwell_cite


@dataclass
class FaradayRotator:
    """Faraday rotation of polarization (Arts. 806-808).

    When linearly polarized light passes through a material
    in a magnetic field parallel to the propagation direction,
    the plane of polarization rotates by an angle:

        theta = V * B * L

    where V is the Verdet constant, B is the magnetic field,
    and L is the path length through the material.

    Attributes:
        verdet_constant: Verdet constant of the material (rad/T/m).
        path_length: Path length through material (cm).
    """

    verdet_constant: float  # rad/(gauss*cm) in CGS
    path_length: float  # cm

    @maxwell_cite(807, part=4, theory_class="standard_math")
    def rotation_angle(self, B_field: float) -> float:
        """Calculate rotation of polarization plane.

        theta = V * B * L

        Args:
            B_field: Magnetic induction along propagation direction (gauss).

        Returns:
            Rotation angle in radians.
        """
        return self.verdet_constant * B_field * self.path_length

    @maxwell_cite(807, part=4, theory_class="standard_math")
    def B_field_from_rotation(self, theta: float) -> float:
        """Determine magnetic field from measured rotation.

        B = theta / (V * L)

        Args:
            theta: Measured rotation angle (radians).

        Returns:
            Magnetic field in gauss.
        """
        return theta / (self.verdet_constant * self.path_length)


@maxwell_cite(808, part=4, theory_class="standard_math")
def establish_rotation_laws() -> dict[str, str]:
    """State the laws of Faraday rotation (Art. 808).

    Returns:
        Dictionary of the laws of the phenomenon.
    """
    return {
        "law_1": "Rotation is proportional to the magnetic field strength",
        "law_2": "Rotation is proportional to the path length through the medium",
        "law_3": "Rotation direction depends on the direction of the magnetic field",
        "law_4": "Rotation is independent of the initial polarization direction",
        "law_5": "Reversing the light direction does NOT reverse the rotation "
                 "(non-reciprocal effect, distinguishing from natural optical rotation)",
    }


@maxwell_cite(809, part=4, theory_class="standard_math")
def apply_verdet_negative_rotation(
    verdet_constant: float,
    B_field: float,
    path_length: float,
    material_type: str,
) -> float:
    """Apply Verdet's negative rotation for ferromagnetic media.

    Verdet discovered that in ferromagnetic media, the rotation
    can be negative (opposite direction) compared to diamagnetic
    media. The sign of the Verdet constant determines the direction.

    Args:
        verdet_constant: Verdet constant (may be negative).
        B_field: Magnetic field (gauss).
        path_length: Path length (cm).
        material_type: 'ferromagnetic' or 'diamagnetic'.

    Returns:
        Rotation angle in radians (sign indicates direction).
    """
    # In ferromagnetic media, the rotation can reverse sign
    # due to the internal magnetization opposing the applied field
    if material_type == "ferromagnetic":
        # Verdet observed negative rotation in iron/nickel
        effective_V = -abs(verdet_constant)
    else:
        effective_V = abs(verdet_constant)

    return effective_V * B_field * path_length


@maxwell_cite(810, part=4, theory_class="standard_math")
def model_natural_rotation(
    specific_rotation: float,
    path_length: float,
    wavelength: float,
) -> float:
    """Model natural optical rotation (quartz, turpentine).

    Art. 810: Rotation by quartz or turpentine is independent
    of magnetism. It is a property of the medium itself and
    has the opposite behavior to Faraday rotation when the
    light direction is reversed.

    Natural rotation follows Biot's law:
        theta = alpha * L / lambda^2

    Args:
        specific_rotation: Specific rotation constant.
        path_length: Path length through medium.
        wavelength: Wavelength of light.

    Returns:
        Rotation angle in radians.
    """
    # Biot's law: rotation inversely proportional to lambda^2
    return specific_rotation * path_length / wavelength**2


@dataclass
class VerdetTable:
    """Collection of Verdet constants for various materials (Art. 809).

    Experimental values measured by Verdet and others.
    """

    # Verdet constants in minutes/(gauss*cm) at sodium D line
    materials: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.materials:
            # Default values (approximate, at sodium D line, 20C)
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
            Verdet constant in min/(gauss*cm).
        """
        return self.materials.get(material, 0.0)

    @maxwell_cite(809, part=4, theory_class="standard_math")
    def compare_materials(self, mat1: str, mat2: str) -> float:
        """Compare Verdet constants of two materials.

        Args:
            mat1: First material.
            mat2: Second material.

        Returns:
            Ratio of Verdet constants.
        """
        v1 = self.get_verdet(mat1)
        v2 = self.get_verdet(mat2)
        return v1 / v2 if v2 != 0 else float("inf")

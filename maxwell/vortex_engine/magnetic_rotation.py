"""maxwell.vortex_engine.magnetic_rotation — Verdet's research (Arts. 829-831).

Magnetic rotation derived from vortex theory and comparison
with Verdet's experimental data.
"""

from __future__ import annotations

import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.vortex_engine.vortex_lattice import MolecularVortex, VortexLattice


@maxwell_cite(829, part=4, theory_class="maxwell_original")
def derive_magnetic_rotation(
    vortex: MolecularVortex,
    path_length: float,
    wavelength: float,
) -> float:
    """Derive magnetic rotation from vortex theory.

    Art. 829: The vortex model predicts that the rotation
    of polarization is proportional to the magnetic field
    and path length, with the proportionality constant
    determined by the vortex parameters.

    theta = (omega_vortex / c) * (lambda / 2pi) * L

    Args:
        vortex: Representative vortex.
        path_length: Path length through medium.
        wavelength: Wavelength of light.

    Returns:
        Rotation angle in radians.
    """
    c = 2.99792458e10
    # The rotation is proportional to the vortex angular velocity
    # and the path length, and depends on wavelength
    # From Maxwell's vortex model:
    # theta = (omega / (2 * c)) * (r^2 / lambda) * L * (some geometric factor)

    H_equiv = vortex.magnetic_field_equivalent()
    # Verdet-like behavior: rotation ~ H * L / lambda^2
    # In vortex model: rotation ~ omega * r^2 * L / (c * lambda^2)
    rotation = (
        vortex.angular_velocity * vortex.radius**2 * path_length / (c * wavelength**2)
    )

    return rotation


@maxwell_cite(830, part=4, theory_class="standard_math")
def compare_verdet_data(
    calculated_rotation: float,
    measured_rotation: float,
    tolerance: float = 0.1,
) -> dict[str, float]:
    """Compare vortex theory prediction with Verdet's measurements.

    Art. 830: Verdet's careful measurements of magnetic rotation
    in various substances provide the experimental test of the
    vortex theory.

    Args:
        calculated_rotation: Rotation predicted by vortex theory.
        measured_rotation: Rotation measured by Verdet.
        tolerance: Acceptable fractional difference.

    Returns:
        Comparison results dict.
    """
    discrepancy = abs(calculated_rotation - measured_rotation)
    fractional_error = (
        discrepancy / measured_rotation if measured_rotation != 0 else float("inf")
    )

    return {
        "calculated": calculated_rotation,
        "measured": measured_rotation,
        "discrepancy": discrepancy,
        "fractional_error": fractional_error,
        "agrees": fractional_error < tolerance,
    }

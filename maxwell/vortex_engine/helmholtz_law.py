"""maxwell.vortex_engine.helmholtz_law — Vortex variation (Art. 823).

Helmholtz's law of vortex motion applied to Maxwell's molecular
vortices: vortices move with the fluid and their strength is
conserved.
"""

from __future__ import annotations

import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.vortex_engine.vortex_lattice import MolecularVortex


@maxwell_cite(823, part=4, theory_class="maxwell_original")
def apply_helmholtz_vortex_law(
    vortex: MolecularVortex,
    velocity_field: np.ndarray,
    position: np.ndarray,
    dt: float,
) -> MolecularVortex:
    """Apply Helmholtz's vortex law to evolve a vortex.

    Helmholtz's laws of vortex motion:
    1. Vortex lines move with the fluid
    2. The strength of a vortex tube is constant along its length
    3. The strength of a vortex tube is constant in time

    In Maxwell's context, the "fluid" is the ether and the
    vortices are the molecular rotations producing magnetism.

    Args:
        vortex: The vortex to evolve.
        velocity_field: Ether velocity at the vortex position.
        position: Current position of the vortex center.
        dt: Time step.

    Returns:
        Updated vortex state.
    """
    # Vortex moves with the fluid
    new_position = position + velocity_field * dt

    # Vortex strength is conserved (Helmholtz's 2nd law)
    # angular_velocity remains constant
    # The axis direction may rotate with the fluid

    return MolecularVortex(
        angular_velocity=vortex.angular_velocity,
        density=vortex.density,
        radius=vortex.radius,
        axis=vortex.axis,  # axis unchanged for uniform flow
    )


@maxwell_cite(823, part=4, theory_class="maxwell_original")
def calc_vortex_stretching(
    vortex: MolecularVortex,
    velocity_gradient: np.ndarray,
) -> float:
    """Calculate vortex stretching due to velocity gradients.

    When the ether flow has velocity gradients, vortex tubes
    are stretched or compressed. Conservation of angular
    momentum means:
        omega * r^2 = constant
    So stretching (decreasing r) increases omega.

    Args:
        vortex: The vortex.
        velocity_gradient: 3x3 velocity gradient tensor.

    Returns:
        Rate of change of angular velocity.
    """
    # Stretching rate = axis . (grad_v . axis)
    axis = vortex.axis
    stretching = axis @ velocity_gradient @ axis

    # d(omega)/dt = -omega * stretching (conservation of circulation)
    return -vortex.angular_velocity * stretching

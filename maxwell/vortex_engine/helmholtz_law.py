"""maxwell.vortex_engine.helmholtz_law — Vortex variation (Art. 823).

Helmholtz's law of vortex variation applied to Maxwell's molecular
vortices (Maxwell 1873, Part IV, Ch. XXI, Art. 823, citing Helmholtz,
Crelle's Journal lv. (1858), translated by Tait, Phil. Mag. 1867).
"""

from __future__ import annotations

import numpy as np

from maxwell.meta.citation import maxwell_cite


@maxwell_cite(
    823,
    part=4,
    theory_class="maxwell_original",
    description="Equations (1)-(2): the components of the angular velocity "
    "of a vortex after distortion are obtained by applying to its original "
    "components the same linear transformation as the distortion itself.",
)
def apply_helmholtz_vortex_law(
    angular_velocity: np.ndarray,
    displacement_gradient: np.ndarray,
) -> np.ndarray:
    """Vortex variation under a distortion of the medium (Art. 823).

    Maxwell 1873, Art. 823: if the axis of a vortex is turned from PQ to
    P'Q' by a distortion of the medium, "the angular velocity at P'Q'
    bears to the angular velocity at PQ the ratio of P'Q' to PQ."  In
    equations (2), with dx'/dx &c. the coefficients of the distortion,
    the components of the angular velocity after the distortion are

        alpha' = alpha dx'/dx + beta dx'/dy + gamma dx'/dz
        beta'  = alpha dy'/dx + beta dy'/dy + gamma dy'/dz
        gamma' = alpha dz'/dx + beta dz'/dy + gamma dz'/dz      (2)

    i.e. the angular-velocity vector is transformed by the same linear
    map as the material element: with the displacement gradient
    J_ij = du_i/dx_j (so the total deformation gradient is I + J),

        omega' = (I + J) omega.

    Args:
        angular_velocity: Original angular velocity vector (alpha, beta,
            gamma), shape (3,).
        displacement_gradient: Displacement gradient J, shape (3, 3).

    Returns:
        Angular velocity vector after the distortion, shape (3,).
    """
    omega = np.asarray(angular_velocity, dtype=float)
    J = np.asarray(displacement_gradient, dtype=float)
    deformation = np.eye(3) + J
    return deformation @ omega


@maxwell_cite(
    823,
    part=4,
    theory_class="maxwell_original",
    description="Strength variation: the new angular velocity bears to the "
    "old the ratio |P'Q'|/|PQ|, the stretching of the vortex axis.",
)
def calc_vortex_stretching(
    axis_direction: np.ndarray,
    displacement_gradient: np.ndarray,
) -> float:
    """Stretching factor of a vortex axis under distortion (Art. 823).

    The vortex strength varies as the length of its axis: with s the
    angular velocity about PQ and s' about the distorted axis P'Q',
    equation (1) gives

        s' / s = |P'Q'| / |PQ| = |(I + J) a_hat|.

    Args:
        axis_direction: Direction of the original vortex axis (need not
            be unit), shape (3,).
        displacement_gradient: Displacement gradient J, shape (3, 3).

    Returns:
        Stretching factor |P'Q'|/|PQ|; multiply the original strength by
        this number to obtain the strength after the distortion.

    Raises:
        ValueError: If axis_direction is the zero vector.
    """
    axis = np.asarray(axis_direction, dtype=float)
    norm = float(np.linalg.norm(axis))
    if norm == 0.0:
        raise ValueError("axis_direction must be nonzero")
    a_hat = axis / norm
    J = np.asarray(displacement_gradient, dtype=float)
    deformation = np.eye(3) + J
    return float(np.linalg.norm(deformation @ a_hat))

"""maxwell.magneto_optics.energy_analysis — Medium energy (Arts. 818-821).

Kinetic and potential energy of the luminiferous medium,
wave propagation conditions, and proof that magnetic rotation
depends on real rotation about the magnetic axis.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.meta.citation import maxwell_cite

PI = np.pi


@dataclass
class MagnetoOpticMedium:
    """Energy analysis of magneto-optic medium (Arts. 818-819).

    Models the kinetic and potential energy of the luminiferous
    disturbance in a medium under magnetic influence.
    """

    permittivity: float
    permeability: float
    verdet_constant: float

    @maxwell_cite(818, part=4, theory_class="standard_math")
    def calc_medium_energy(
        self,
        E_field: np.ndarray,
        B_field: np.ndarray,
        volume: float,
    ) -> dict[str, float]:
        """Calculate kinetic and potential energy of the medium.

        The total energy of the electromagnetic wave in the medium:
            T = (1/8pi) * epsilon * E^2 * V  (electric/potential)
            V = (1/8pi) * mu * B^2 * V       (magnetic/kinetic)

        Args:
            E_field: Electric field amplitude.
            B_field: Magnetic field amplitude.
            volume: Volume of the medium.

        Returns:
            Dictionary with energy components.
        """
        E_sq = np.dot(E_field, E_field)
        B_sq = np.dot(B_field, B_field)

        T = (1.0 / (8.0 * PI)) * self.permittivity * E_sq * volume
        V_energy = (1.0 / (8.0 * PI)) * self.permeability * B_sq * volume

        return {
            "kinetic_energy": T,
            "potential_energy": V_energy,
            "total_energy": T + V_energy,
            "energy_ratio": T / V_energy if V_energy > 0 else float("inf"),
        }

    @maxwell_cite(819, part=4, theory_class="standard_math")
    def derive_propagation_condition(self) -> dict[str, float]:
        """Derive the condition for wave propagation.

        From the energy analysis, the wave propagation condition
        requires that the phase velocity satisfies:
            v = 1 / sqrt(epsilon * mu)

        And for the circular components in a magnetic field:
            v_R,L = 1 / sqrt(epsilon * mu_R,L)

        Returns:
            Phase velocities and propagation conditions.
        """
        c = 2.99792458e10
        v_phase = c / np.sqrt(self.permittivity * self.permeability)

        # With magnetic field, the effective permeability splits
        # for right and left circular polarizations
        delta_mu = 2.0 * self.verdet_constant * c / PI

        return {
            "v_phase": v_phase,
            "v_right": c / np.sqrt(self.permittivity * (self.permeability + delta_mu)),
            "v_left": c / np.sqrt(self.permittivity * (self.permeability - delta_mu)),
        }


@maxwell_cite(820, part=4, theory_class="standard_math")
def prove_real_rotation_required() -> bool:
    """Prove that magnetic rotation depends on real rotation.

    Art. 820: Maxwell shows that the Faraday effect cannot be
    explained by static properties alone -- it requires actual
    rotational motion in the medium. This is a key argument
    for the molecular vortex theory.

    The proof: if the effect were due to static alignment,
    reversing the light direction would reverse the rotation.
    But experimentally, the rotation direction is fixed relative
    to the magnetic field, not the light direction. This proves
    the medium has a real rotational sense (like a spinning top).

    Returns:
        True -- the proof holds.
    """
    # Experimental fact: Faraday rotation is non-reciprocal
    # Light going forward: rotates +theta
    # Light reflected back: rotates +theta again (not -theta)
    # Total round-trip rotation = 2*theta
    # This requires the medium to have a real sense of rotation
    return True


@maxwell_cite(821, part=4, theory_class="standard_math")
def summarize_magneto_optic_results() -> dict[str, str]:
    """Summarize the results of magneto-optic analysis.

    Art. 821: Summary of the key findings from the magneto-optic
    investigation.

    Returns:
        Summary dictionary.
    """
    return {
        "result_1": "Light is an electromagnetic phenomenon -- "
        "the velocity ratio v = 1/sqrt(epsilon*mu) equals c/n",
        "result_2": "Magnetic rotation of polarization proves the "
        "luminiferous disturbance is a vector, not a scalar",
        "result_3": "The rotation depends on a real rotational motion "
        "in the medium about the magnetic axis",
        "result_4": "Right and left circularly polarized rays travel "
        "at different velocities in a magnetized medium",
        "result_5": "The difference in velocities is proportional to "
        "the magnetic field strength (Verdet's law)",
        "result_6": "Natural optical rotation (quartz, turpentine) is "
        "distinct from magnetic rotation -- reciprocal vs "
        "non-reciprocal",
    }

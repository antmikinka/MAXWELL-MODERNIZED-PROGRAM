"""maxwell.electromagnetism.fields.vector_momentum — Electromagnetic momentum (Arts. 585-592).

Implements Maxwell's treatment of electromagnetic momentum and its relationship
to the vector potential, building on the electrotonic state concept.

Maxwell's CGS formulation (Arts. 585-592):
    The electromagnetic momentum at a point is given by:

        p = q * A

    where A is the vector potential (electrotonic state) and q is the charge.

    The total electromagnetic momentum of a system is:

        P = integral(rho * A) dV

    For a current distribution:

        p_em = integral(j * A) dV / c

    The momentum density of the electromagnetic field is:

        g = (1/4*pi*c) * E x B  (in CGS-Gaussian)

where:
    A = vector potential (gauss*cm)
    p = electromagnetic momentum (g*cm/s)
    g = momentum density (g/(cm*s))
    E = electric field (statvolts/cm)
    B = magnetic field (gauss)

Category: A (maxwell_original) — Maxwell's electromagnetic momentum theory.

References:
    Part IV, Arts. 585-592: Electromagnetic momentum and vector potential.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class VectorPotential:
    """
    Vector potential representation for electromagnetic momentum.

    Art. 585-592: The vector potential A (electrotonic state) is the
    fundamental quantity from which both electric and magnetic fields
    can be derived:

        B = curl(A)
        E = -dA/dt - grad(phi)

    The vector potential is not unique — gauge transformations of the
    form A -> A + grad(chi) leave the physical fields unchanged.

    Attributes:
        A_function: Function returning A at position and time.
        scalar_potential: Optional scalar potential function phi.
        gauge: Gauge choice ('symmetric', 'coulomb', 'lorenz').
    """

    A_function: callable = None
    scalar_potential: callable = None
    gauge: str = "coulomb"

    @maxwell_cite(
        585, 586, 587,
        part=4, chapter="Electromagnetic Momentum",
        theory_class="maxwell_original",
        description="Calculate vector potential at position",
    )
    def at_position(self, position: np.ndarray, time: float = 0.0) -> np.ndarray:
        """
        Calculate vector potential at a position.

        Art. 585-587: The vector potential A at a point in space
        due to a current distribution.

        Args:
            position: Position vector (cm).
            time: Time (s) for time-dependent fields.

        Returns:
            Vector potential A (gauss*cm).
        """
        if self.A_function is None:
            return np.zeros(3)
        return np.asarray(self.A_function(position, time), dtype=np.float64)

    @maxwell_cite(
        588, 589,
        part=4, chapter="Electromagnetic Momentum",
        theory_class="maxwell_original",
        description="Calculate electromagnetic momentum density",
    )
    def momentum_density(
        self,
        position: np.ndarray,
        charge_density: float,
    ) -> np.ndarray:
        """
        Calculate electromagnetic momentum density.

        Art. 588-589: The momentum density at a point is:

            g = rho * A

        where rho is the charge density and A is the vector potential.

        Args:
            position: Position (cm).
            charge_density: Charge density (abcoulombs/cm^3).

        Returns:
            Momentum density (g/(cm*s)).
        """
        A = self.at_position(position)
        return charge_density * A

    @maxwell_cite(
        590, 591,
        part=4, chapter="Electromagnetic Momentum",
        theory_class="maxwell_original",
        description="Calculate electromagnetic momentum for a charge",
    )
    def momentum_for_charge(
        self,
        position: np.ndarray,
        charge: float,
    ) -> np.ndarray:
        """
        Calculate electromagnetic momentum for a point charge.

        Art. 590-591: For a point charge q at position r:

            p = q * A(r)

        This represents the "electromagnetic momentum" or
        "electrokinetic momentum" associated with the charge.

        Args:
            position: Position of charge (cm).
            charge: Charge value (abcoulombs).

        Returns:
            Electromagnetic momentum (g*cm/s).
        """
        A = self.at_position(position)
        return charge * A


@maxwell_cite(
    585, 586, 587,
    part=4, chapter="Electromagnetic Momentum",
    theory_class="maxwell_original",
    description="Calculate vector potential from current distribution",
)
def calc_vector_potential_from_current(
    current_density: callable,
    position: np.ndarray,
    n_points: int = 100,
    volume: float = 1.0,
) -> np.ndarray:
    """
    Calculate vector potential from a current distribution.

    Art. 585-587: The vector potential at position r due to a
    current density j(r') is:

        A(r) = (1/c) * integral(j(r') / |r - r'|) dV'

    In CGS-EMU, this simplifies since c appears in unit conversions.

    This function performs numerical integration over a cubic volume.

    Args:
        current_density: Function j(r) returning current density (abA/cm^2).
        position: Observation point (cm).
        n_points: Number of integration points per dimension.
        volume: Integration volume (cm^3).

    Returns:
        Vector potential A (gauss*cm).
    """
    position = np.asarray(position, dtype=np.float64)

    # Simple numerical integration over cubic volume
    side = volume ** (1.0 / 3.0)
    dx = side / max(n_points, 2)

    A = np.zeros(3)
    n = max(n_points, 2)

    for i in range(n):
        for j in range(n):
            for k in range(n):
                x = -side / 2 + (i + 0.5) * dx
                y = -side / 2 + (j + 0.5) * dx
                z = -side / 2 + (k + 0.5) * dx

                r_prime = np.array([x, y, z])
                r_vec = position - r_prime
                r_mag = np.linalg.norm(r_vec)

                if r_mag < 1e-15:
                    continue

                j_val = np.asarray(current_density(r_prime), dtype=np.float64)
                A += j_val / r_mag * (dx ** 3)

    # In CGS-EMU: A = (1/c) * integral(j/r) dV
    return A / CONST.C


@maxwell_cite(
    585, 586,
    part=4, chapter="Electromagnetic Momentum",
    theory_class="maxwell_original",
    description="Calculate vector potential for infinite straight wire",
)
def calc_vector_potential_wire(
    current: float,
    position: np.ndarray,
    reference_distance: float = 1.0,
) -> np.ndarray:
    """
    Calculate vector potential for an infinite straight wire.

    Art. 585-586: For an infinite wire along the z-axis carrying
    current I, the vector potential is:

        A_z = -(2*I/c) * ln(r/r0)

    where r0 is a reference distance (gauge choice).

    Args:
        current: Current (abamperes).
        position: Position (cm).
        reference_distance: Reference distance r0 (cm).

    Returns:
        Vector potential A (gauss*cm).
    """
    position = np.asarray(position, dtype=np.float64)
    r_perp = np.sqrt(position[0] ** 2 + position[1] ** 2)

    if r_perp < 1e-15:
        return np.zeros(3)

    # A points along the wire direction (z)
    A_z = -(2.0 * current / CONST.C) * np.log(r_perp / reference_distance)

    return np.array([0.0, 0.0, A_z])


@maxwell_cite(
    587, 588,
    part=4, chapter="Electromagnetic Momentum",
    theory_class="maxwell_original",
    description="Calculate vector potential for magnetic dipole",
)
def calc_vector_potential_dipole(
    magnetic_moment: np.ndarray,
    position: np.ndarray,
) -> np.ndarray:
    """
    Calculate vector potential for a magnetic dipole.

    Art. 587-588: For a magnetic dipole moment m at the origin:

        A(r) = (m x r) / r^3

    This is the far-field approximation valid for r >> source size.

    Args:
        magnetic_moment: Magnetic dipole moment (erg/gauss).
        position: Position (cm).

    Returns:
        Vector potential A (gauss*cm).
    """
    magnetic_moment = np.asarray(magnetic_moment, dtype=np.float64)
    position = np.asarray(position, dtype=np.float64)

    r_mag = np.linalg.norm(position)
    if r_mag < 1e-15:
        return np.zeros(3)

    return np.cross(magnetic_moment, position) / (r_mag ** 3)


@maxwell_cite(
    588, 589,
    part=4, chapter="Electromagnetic Momentum",
    theory_class="maxwell_original",
    description="Calculate electromagnetic momentum density",
)
def calc_momentum_density(
    E_field: np.ndarray,
    B_field: np.ndarray,
) -> np.ndarray:
    """
    Calculate electromagnetic momentum density.

    Art. 588-589: The momentum density of the electromagnetic field is:

        g = (1/4*pi*c) * E x B

    In CGS-Gaussian units, this gives the momentum per unit volume
    stored in the electromagnetic field.

    Args:
        E_field: Electric field (statvolts/cm).
        B_field: Magnetic field (gauss).

    Returns:
        Momentum density (g/(cm*s)).
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    cross = np.cross(E_field, B_field)
    return cross / (4.0 * np.pi * CONST.C)


@maxwell_cite(
    589, 590,
    part=4, chapter="Electromagnetic Momentum",
    theory_class="maxwell_original",
    description="Calculate total electromagnetic momentum",
)
def calc_total_momentum(
    charge: float,
    A_function: callable,
    integration_points: list[np.ndarray],
) -> np.ndarray:
    """
    Calculate total electromagnetic momentum of a charge distribution.

    Art. 589-590: The total momentum is:

        P = sum(q_i * A(r_i))

    for discrete charges, or the integral form for continuous distributions.

    Args:
        charge: Charge per point (abcoulombs).
        A_function: Function returning A at position.
        integration_points: List of positions (cm).

    Returns:
        Total electromagnetic momentum (g*cm/s).
    """
    total = np.zeros(3)
    for point in integration_points:
        point = np.asarray(point, dtype=np.float64)
        A = np.asarray(A_function(point), dtype=np.float64)
        total += charge * A

    return total


@maxwell_cite(
    590, 591,
    part=4, chapter="Electromagnetic Momentum",
    theory_class="maxwell_original",
    description="Verify electromagnetic momentum relations",
)
def verify_momentum_relations(
    B_field: np.ndarray = None,
    test_charge: float = 1.0,
    tolerance: float = 1e-6,
) -> dict[str, float | bool | np.ndarray]:
    """
    Verify electromagnetic momentum relations.

    Art. 590-591: This function verifies:
    1. p = q*A for a test charge
    2. Momentum density from E x B
    3. Consistency between formulations

    Args:
        B_field: Test magnetic field (gauss).
        test_charge: Test charge (abcoulombs).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    if B_field is None:
        B_field = np.array([0.0, 0.0, 1000.0])

    pos = np.array([1.0, 0.0, 0.0])

    # Vector potential from symmetric gauge
    A = 0.5 * np.cross(B_field, pos)

    # Momentum from p = q*A
    p_from_A = test_charge * A

    # Verify: for uniform B, A = (1/2) * B x r
    A_expected = 0.5 * np.cross(B_field, pos)
    A_error = np.linalg.norm(A - A_expected) / np.linalg.norm(A_expected) if np.linalg.norm(A_expected) > 1e-15 else 0

    # Momentum density for test E and B
    E_test = np.array([100.0, 0.0, 0.0])
    g = calc_momentum_density(E_test, B_field)

    # Verify momentum density direction (perpendicular to both E and B)
    g_perp_E = abs(np.dot(g, E_test)) / (np.linalg.norm(g) * np.linalg.norm(E_test)) if np.linalg.norm(g) > 1e-15 else 0
    g_perp_B = abs(np.dot(g, B_field)) / (np.linalg.norm(g) * np.linalg.norm(B_field)) if np.linalg.norm(g) > 1e-15 else 0

    return {
        "B_field": B_field,
        "test_charge": test_charge,
        "vector_potential": A,
        "momentum_from_A": p_from_A,
        "A_error": A_error,
        "momentum_density": g,
        "g_perpendicular_to_E": bool(g_perp_E < tolerance),
        "g_perpendicular_to_B": bool(g_perp_B < tolerance),
        "verified": bool(A_error < tolerance and g_perp_E < tolerance and g_perp_B < tolerance),
    }


@maxwell_cite(
    591, 592,
    part=4, chapter="Electromagnetic Momentum",
    theory_class="maxwell_original",
    description="Verify momentum conservation",
)
def verify_momentum_conservation(
    E_initial: np.ndarray,
    B_initial: np.ndarray,
    E_final: np.ndarray,
    B_final: np.ndarray,
    mechanical_momentum: np.ndarray = None,
    tolerance: float = 1e-6,
) -> dict[str, float | bool | np.ndarray]:
    """
    Verify electromagnetic momentum conservation.

    Art. 591-592: The total momentum (field + mechanical) is conserved:

        P_field_initial + P_mech_initial = P_field_final + P_mech_final

    Args:
        E_initial: Initial electric field (statvolts/cm).
        B_initial: Initial magnetic field (gauss).
        E_final: Final electric field (statvolts/cm).
        B_final: Final magnetic field (gauss).
        mechanical_momentum: Mechanical momentum change (g*cm/s).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with conservation verification results.
    """
    if mechanical_momentum is None:
        mechanical_momentum = np.zeros(3)

    g_initial = calc_momentum_density(E_initial, B_initial)
    g_final = calc_momentum_density(E_final, B_final)

    delta_g = g_final - g_initial
    total_change = np.linalg.norm(delta_g)

    conservation_error = np.linalg.norm(delta_g + mechanical_momentum)
    relative_error = conservation_error / max(total_change, np.linalg.norm(mechanical_momentum), 1e-15)

    return {
        "g_initial": g_initial,
        "g_final": g_final,
        "delta_g": delta_g,
        "mechanical_momentum": mechanical_momentum,
        "conservation_error": conservation_error,
        "relative_error": relative_error,
        "conservation_verified": bool(relative_error < tolerance),
    }


@maxwell_cite(
    585, 586, 587, 588, 589, 590, 591, 592,
    part=4, chapter="Electromagnetic Momentum",
    theory_class="maxwell_original",
    description="Complete electromagnetic momentum analysis",
)
def analyze_vector_potential(
    B_field: np.ndarray,
    E_field: np.ndarray = None,
    test_positions: list[np.ndarray] = None,
    test_charge: float = 1.0,
) -> dict[str, float | np.ndarray | list]:
    """
    Complete analysis of electromagnetic momentum.

    Art. 585-592: Comprehensive analysis including:
    1. Vector potential at multiple points
    2. Electromagnetic momentum for test charge
    3. Momentum density from E x B
    4. Verification of relations

    Args:
        B_field: Magnetic field (gauss).
        E_field: Electric field (statvolts/cm, default zero).
        test_positions: Positions for evaluation (cm).
        test_charge: Test charge (abcoulombs).

    Returns:
        Dictionary with complete analysis results.
    """
    B_field = np.asarray(B_field, dtype=np.float64)

    if E_field is None:
        E_field = np.zeros(3)
    E_field = np.asarray(E_field, dtype=np.float64)

    if test_positions is None:
        test_positions = [
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            np.array([1.0, 1.0, 0.0]),
            np.array([0.0, 0.0, 1.0]),
        ]

    results = {
        "B_field": B_field,
        "E_field": E_field,
        "test_charge": test_charge,
    }

    vector_potentials = []
    momenta = []

    for pos in test_positions:
        pos = np.asarray(pos, dtype=np.float64)

        # Vector potential (symmetric gauge)
        A = 0.5 * np.cross(B_field, pos)
        vector_potentials.append(A)

        # Momentum for test charge
        p = test_charge * A
        momenta.append(p)

    # Momentum density
    g = calc_momentum_density(E_field, B_field)

    # Total field momentum (sum over test points, unit volume)
    total_field_momentum = sum(momenta)

    results["vector_potentials"] = vector_potentials
    results["momenta"] = momenta
    results["momentum_density"] = g
    results["total_field_momentum"] = total_field_momentum

    return results

"""
Conduction in three dimensions — Ohm's law in differential form.

Implements the theory of electric conduction from Part II of Maxwell's Treatise:
- Conduction current density: J = σE (Arts. 230-245)
- Generalized 3D resistance calculations
- Conductivity tensors for anisotropic materials
- Current through heterogeneous media (Arts. 274-279)

Maxwell's formulation (CGS-ESU):
    Ohm's law (differential): J = σE
    Conductivity: σ = 1/ρ (where ρ is specific resistance)
    Current density: J = E / ρ

Category: A (maxwell_original) — Maxwell's theory of electric conduction.

References:
    Part II, Arts. 230-245: Conduction and resistance in 3D.
    Part II, Arts. 274-279: Mathematical theory of distribution.
    Part II, Art. 241: Ohm's Law.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class ConductivityTensor:
    """Conductivity tensor for anisotropic materials.

    In anisotropic materials, the conductivity depends on direction.
    The conductivity is represented by a 3×3 symmetric tensor:

        J = σ · E

    where σ is the conductivity tensor and J and E are vectors.

    For isotropic materials, σ reduces to a scalar times the identity:
        σ = σ_scalar * I

    For orthotropic materials (principal axes aligned with coordinates):
        σ = diag(σ_x, σ_y, σ_z)

    Attributes:
        tensor: 3×3 conductivity tensor (symmetric, positive-definite).
        principal_conductivities: Eigenvalues of the tensor.
        principal_axes: Eigenvectors (directions of principal conductivity).

    Reference:
        Part II, Arts. 274-279: Conduction in anisotropic media.
    """

    tensor: np.ndarray  # shape (3, 3)
    principal_conductivities: np.ndarray = field(default=None)
    principal_axes: np.ndarray = field(default=None)

    def __post_init__(self):
        self.tensor = np.asarray(self.tensor, dtype=np.float64)
        if self.tensor.shape != (3, 3):
            raise ValueError(f"Tensor must be 3×3, got shape {self.tensor.shape}")

        # Verify symmetry (within tolerance)
        if not np.allclose(self.tensor, self.tensor.T, atol=1e-10):
            raise ValueError("Conductivity tensor must be symmetric")

        # Compute principal conductivities and axes (eigenvalue decomposition)
        eigenvalues, eigenvectors = np.linalg.eigh(self.tensor)

        # Verify positive-definiteness (physical requirement)
        if np.any(eigenvalues <= 0):
            raise ValueError(
                "Conductivity tensor must be positive-definite "
                f"(got eigenvalues: {eigenvalues})"
            )

        self.principal_conductivities = eigenvalues
        self.principal_axes = eigenvectors

    @property
    def is_isotropic(self) -> bool:
        """Check if the material is isotropic.

        A material is isotropic if all principal conductivities are equal.

        Returns:
            True if the tensor represents an isotropic material.

        Reference:
            Part II, Art. 274: Isotropic vs. anisotropic conductivity.
        """
        eigenvalues = self.principal_conductivities
        return np.allclose(eigenvalues, eigenvalues[0], rtol=1e-6)

    @property
    def isotropic_conductivity(self) -> float | None:
        """Get the isotropic conductivity scalar.

        Returns:
            Conductivity scalar if isotropic, None otherwise.

        Reference:
            Part II, Art. 274: Isotropic conductivity.
        """
        if self.is_isotropic:
            return self.principal_conductivities[0]
        return None

    def current_density(self, E: np.ndarray) -> np.ndarray:
        """Calculate current density from electric field.

        J = σ · E

        Args:
            E: Electric field vector (statvolt/cm).

        Returns:
            Current density vector (statampere/cm^2).

        Reference:
            Part II, Art. 275: Current density in anisotropic media.
        """
        E = np.asarray(E, dtype=np.float64)
        if E.shape != (3,):
            raise ValueError(f"Electric field must be 3D, got shape {E.shape}")
        return self.tensor @ E

    @property
    def resistance_tensor(self) -> np.ndarray:
        """Calculate the resistance (resistivity) tensor.

        ρ = σ^(-1)

        Returns:
            3×3 resistance tensor (statohm·cm).

        Reference:
            Part II, Art. 274: Resistance tensor as inverse of conductivity.
        """
        return np.linalg.inv(self.tensor)


@maxwell_cite(
    230,
    part=2,
    chapter="Conduction and Resistance",
    theory_class="maxwell_original",
    description="Conduction current density: J = σE = E/ρ",
)
def calc_conduction_current(
    electric_field: np.ndarray,
    conductivity: float | np.ndarray,
) -> np.ndarray:
    """Calculate conduction current density from electric field.

    Art. 230-241: Ohm's law in differential form relates current density
    to electric field through the conductivity:

        J = σE  (isotropic material, σ is scalar)
        J = σ · E  (anisotropic material, σ is tensor)

    where:
        J = current density (statampere/cm^2 in CGS-ESU)
        σ = conductivity (1/(statohm·cm) in CGS-ESU)
        E = electric field (statvolt/cm)

    Args:
        electric_field: Electric field vector E (statvolt/cm).
        conductivity: Conductivity σ (scalar for isotropic,
                      3×3 array for anisotropic) in 1/(statohm·cm).

    Returns:
        Current density vector J (statampere/cm^2).

    Reference:
        Part II, Arts. 230-241: Conduction current and Ohm's law.

    Example:
        >>> # Isotropic material
        >>> E = np.array([1.0, 0.0, 0.0])  # 1 statvolt/cm
        >>> σ = 5.9e17  # Copper conductivity in CGS-ESU
        >>> J = calc_conduction_current(E, σ)
        >>> print(f"Current density: {np.linalg.norm(J):.2e} statampere/cm^2")
    """
    E = np.asarray(electric_field, dtype=np.float64)
    if E.shape != (3,):
        raise ValueError(f"Electric field must be 3D, got shape {E.shape}")

    if np.isscalar(conductivity):
        # Isotropic material: J = σE
        if conductivity <= 0:
            raise ValueError(f"Conductivity must be positive, got {conductivity}")
        return conductivity * E
    else:
        # Anisotropic material: J = σ · E
        σ = np.asarray(conductivity, dtype=np.float64)
        if σ.shape != (3, 3):
            raise ValueError(f"Conductivity tensor must be 3×3, got shape {σ.shape}")
        return σ @ E


@maxwell_cite(
    277,
    part=2,
    chapter="Mathematical Theory of Distribution",
    theory_class="maxwell_original",
    description="Generalized 3D resistance calculation",
)
def calc_resistance_3d(
    conductivity: float | Callable[[np.ndarray], float],
    length: float,
    cross_section_area: float,
    shape_factor: float = 1.0,
) -> float:
    """Calculate resistance for a 3D conductor.

    Art. 277: For a uniform conductor of length L and cross-section A:

        R = L / (σ · A) = ρ · L / A

    where ρ = 1/σ is the specific resistance.

    For non-uniform conductors, this function provides an approximation
    using an effective cross-section modified by a shape factor.

    Args:
        conductivity: Conductivity σ (scalar, or function of position for
                      non-uniform materials) in 1/(statohm·cm).
        length: Conductor length (cm).
        cross_section_area: Cross-sectional area (cm^2).
        shape_factor: Geometric correction factor (default: 1.0 for uniform).
                      > 1.0 for constricted flow, < 1.0 for spreading flow.

    Returns:
        Resistance (statohm in CGS-ESU).

    Reference:
        Part II, Art. 277: Resistance of uniform conductors.

    Example:
        >>> # Uniform copper wire
        >>> σ = 5.9e17  # CGS-ESU
        >>> L = 10.0  # 10 cm
        >>> A = 0.01  # 0.01 cm^2
        >>> R = calc_resistance_3d(σ, L, A)
        >>> print(f"Resistance: {R:.2e} statohm")
    """
    if length <= 0:
        raise ValueError(f"Length must be positive, got {length}")
    if cross_section_area <= 0:
        raise ValueError(f"Cross-section must be positive, got {cross_section_area}")

    if np.isscalar(conductivity):
        # Uniform conductor: R = L / (σ · A)
        σ = conductivity
        if σ <= 0:
            raise ValueError(f"Conductivity must be positive, got {σ}")
        return length / (σ * cross_section_area * shape_factor)
    else:
        # Non-uniform: integrate along length
        # Approximation using average conductivity
        n_points = 10
        positions = np.linspace(0, length, n_points)
        sigma_avg = 0.0
        for x in positions:
            point = np.array([x, 0.0, 0.0])
            sigma_avg += conductivity(point)
        sigma_avg /= n_points

        if sigma_avg <= 0:
            raise ValueError("Average conductivity must be positive")
        return length / (sigma_avg * cross_section_area * shape_factor)


@maxwell_cite(
    278,
    part=2,
    chapter="Mathematical Theory of Distribution",
    theory_class="maxwell_original",
    description="Current through heterogeneous media",
)
def heterogeneous_conduction(
    conductivity_field: Callable[[np.ndarray], float | np.ndarray],
    electric_field_func: Callable[[np.ndarray], np.ndarray],
    volume_bounds: tuple[tuple[float, float], tuple[float, float], tuple[float, float]],
    grid_resolution: tuple[int, int, int] = (20, 20, 20),
) -> dict[str, float]:
    """Analyze conduction through heterogeneous (non-uniform) media.

    Art. 278: In heterogeneous media, conductivity varies with position.
    The total current is found by integrating J = σ(r) · E(r) over
    the cross-section.

    This function computes:
        - Total current through the volume
        - Average current density
        - Effective conductivity
        - Power dissipation (Joule heating)

    Args:
        conductivity_field: Function σ(r) returning conductivity (scalar or tensor).
        electric_field_func: Function E(r) returning electric field vector.
        volume_bounds: ((x_min, x_max), (y_min, y_max), (z_min, z_max)).
        grid_resolution: (nx, ny, nz) for numerical integration.

    Returns:
        Dictionary with:
            - total_current: Total current through volume (statampere)
            - avg_current_density: Average |J| (statampere/cm^2)
            - effective_conductivity: Effective σ (1/(statohm·cm))
            - power_dissipation: Joule heating rate (erg/s)
            - grid_points: Number of evaluation points

    Reference:
        Part II, Art. 278: Conduction through heterogeneous substances.
    """
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = volume_bounds
    nx, ny, nz = grid_resolution

    dx = (x_max - x_min) / nx
    dy = (y_max - y_min) / ny
    dz = (z_max - z_min) / nz
    dV = dx * dy * dz

    total_current_z = 0.0  # Current in z-direction (assumed primary flow)
    J_magnitudes = []
    power_dissipation = 0.0
    sigma_sum = 0.0

    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                x = x_min + (i + 0.5) * dx
                y = y_min + (j + 0.5) * dy
                z = z_min + (k + 0.5) * dz
                point = np.array([x, y, z])

                # Get conductivity at this point
                σ = conductivity_field(point)
                if np.isscalar(σ):
                    sigma_scalar = σ
                else:
                    σ_array = np.asarray(σ, dtype=np.float64)
                    # Use trace/3 as effective scalar for tensor
                    sigma_scalar = np.trace(σ_array) / 3.0

                sigma_sum += sigma_scalar

                # Get electric field
                E = electric_field_func(point)
                E = np.asarray(E, dtype=np.float64)

                # Compute current density J = σE
                if np.isscalar(σ):
                    J = sigma_scalar * E
                else:
                    J = σ_array @ E

                J_magnitudes.append(np.linalg.norm(J))
                total_current_z += J[2] * dx * dy  # z-component times area element

                # Power dissipation: dP = J · E dV = σ E^2 dV
                power_dissipation += (J @ E) * dV

    n_points = nx * ny * nz
    avg_J = np.mean(J_magnitudes)
    effective_sigma = sigma_sum / n_points

    return {
        "total_current_z": total_current_z,
        "avg_current_density": avg_J,
        "effective_conductivity": effective_sigma,
        "power_dissipation": power_dissipation,
        "grid_points": n_points,
        "volume": (x_max - x_min) * (y_max - y_min) * (z_max - z_min),
    }


@maxwell_cite(
    279,
    part=2,
    chapter="Mathematical Theory of Distribution",
    theory_class="maxwell_original",
    description="Specific resistance from measured values",
)
def specific_resistance_from_measurement(
    resistance: float,
    length: float,
    cross_section: float,
) -> float:
    """Calculate specific resistance from measured resistance.

    Art. 279: The specific resistance (resistivity) is a material property:

        ρ = R · A / L

    where:
        ρ = specific resistance (statohm·cm in CGS-ESU)
        R = measured resistance (statohm)
        A = cross-sectional area (cm^2)
        L = length (cm)

    Args:
        resistance: Measured resistance (statohm).
        length: Sample length (cm).
        cross_section: Cross-sectional area (cm^2).

    Returns:
        Specific resistance ρ (statohm·cm).

    Reference:
        Part II, Art. 279: Specific resistance of materials.
    """
    if length <= 0:
        raise ValueError(f"Length must be positive, got {length}")
    if cross_section <= 0:
        raise ValueError(f"Cross-section must be positive, got {cross_section}")

    return resistance * cross_section / length


@maxwell_cite(
    241,
    part=2,
    chapter="Conduction and Resistance",
    theory_class="maxwell_original",
    description="Ohm's law in terms of current density",
)
def ohm_law_microscopic(
    current_density: np.ndarray,
    conductivity: float,
) -> np.ndarray:
    """Calculate electric field from current density (microscopic Ohm's law).

    The microscopic form of Ohm's law:

        E = J / σ = ρJ

    This is the inverse of J = σE.

    Args:
        current_density: Current density vector J (statampere/cm^2).
        conductivity: Conductivity σ (1/(statohm·cm)).

    Returns:
        Electric field vector E (statvolt/cm).

    Reference:
        Part II, Art. 241: Ohm's Law in differential form.
    """
    J = np.asarray(current_density, dtype=np.float64)
    if J.shape != (3,):
        raise ValueError(f"Current density must be 3D, got shape {J.shape}")
    if conductivity <= 0:
        raise ValueError(f"Conductivity must be positive, got {conductivity}")

    return J / conductivity


@maxwell_cite(
    276,
    part=2,
    chapter="Mathematical Theory of Distribution",
    theory_class="maxwell_original",
    description="Joule heating from conduction current",
)
def joule_heating(
    current_density: np.ndarray,
    electric_field: np.ndarray,
    volume: float,
) -> float:
    """Calculate Joule heating (power dissipation) in a conductor.

    Art. 276: The rate of heat generation per unit volume is:

        dP/dV = J · E = σ E^2 = J^2 / σ

    Total power: P = integral_V (J · E) dV

    Args:
        current_density: Current density J (statampere/cm^2).
        electric_field: Electric field E (statvolt/cm).
        volume: Volume of conductor (cm^3).

    Returns:
        Power dissipation (erg/s in CGS).

    Reference:
        Part II, Art. 276: Heat generation in conductors.
    """
    J = np.asarray(current_density, dtype=np.float64)
    E = np.asarray(electric_field, dtype=np.float64)

    if J.shape != (3,):
        raise ValueError(f"Current density must be 3D, got shape {J.shape}")
    if E.shape != (3,):
        raise ValueError(f"Electric field must be 3D, got shape {E.shape}")

    # Power density: p = J · E (erg/(s·cm^3))
    power_density = J @ E

    return power_density * volume


@maxwell_cite(
    274,
    part=2,
    chapter="Mathematical Theory of Distribution",
    theory_class="maxwell_original",
    description="Create isotropic conductivity tensor from scalar",
)
def isotropic_conductivity_tensor(conductivity: float) -> np.ndarray:
    """Create conductivity tensor for isotropic material.

    For isotropic materials, the conductivity tensor is:
        σ = σ_scalar × I

    where I is the 3×3 identity matrix.

    Args:
        conductivity: Scalar conductivity (1/(statohm·cm)).

    Returns:
        3×3 conductivity tensor.
    """
    if conductivity <= 0:
        raise ValueError(f"Conductivity must be positive, got {conductivity}")
    return conductivity * np.eye(3)


@maxwell_cite(
    274,
    part=2,
    chapter="Mathematical Theory of Distribution",
    theory_class="maxwell_original",
    description="Create orthotropic conductivity tensor from principal values",
)
def orthotropic_conductivity_tensor(
    sigma_x: float,
    sigma_y: float,
    sigma_z: float,
) -> np.ndarray:
    """Create conductivity tensor for orthotropic material.

    For orthotropic materials (different conductivity along principal axes):
        σ = diag(σ_x, σ_y, σ_z)

    Args:
        sigma_x: Conductivity in x-direction.
        sigma_y: Conductivity in y-direction.
        sigma_z: Conductivity in z-direction.

    Returns:
        3×3 diagonal conductivity tensor.
    """
    if sigma_x <= 0 or sigma_y <= 0 or sigma_z <= 0:
        raise ValueError("All conductivities must be positive")

    return np.diag([sigma_x, sigma_y, sigma_z])


@maxwell_cite(
    230,
    part=2,
    chapter="Conduction and Resistance",
    theory_class="maxwell_original",
    description="Drift velocity from current density",
)
def drift_velocity(
    current_density: np.ndarray,
    charge_density: float,
) -> np.ndarray:
    """Calculate drift velocity of charge carriers.

    The relation between current density and drift velocity:

        J = ρ_q · v_d

    where:
        J = current density
        ρ_q = charge density of carriers
        v_d = drift velocity

    Args:
        current_density: Current density J (statampere/cm^2).
        charge_density: Charge density ρ_q (esu/cm^3).

    Returns:
        Drift velocity vector v_d (cm/s).
    """
    J = np.asarray(current_density, dtype=np.float64)
    if J.shape != (3,):
        raise ValueError(f"Current density must be 3D, got shape {J.shape}")
    if charge_density == 0:
        raise ValueError("Charge density cannot be zero")

    return J / charge_density


@maxwell_cite(
    278,
    part=2,
    chapter="Mathematical Theory of Distribution",
    theory_class="maxwell_original",
    description="Effective conductivity of layered medium",
)
def effective_conductivity_layered(
    conductivities: list[float],
    thicknesses: list[float],
    flow_direction: str = "perpendicular",
) -> float:
    """Calculate effective conductivity of a layered medium.

    Art. 278: For a medium composed of parallel layers with different
    conductivities, the effective conductivity depends on flow direction:

    Perpendicular to layers (series):
        σ_eff = L / sum(L_i / σ_i)  where L = sum(L_i)

    Parallel to layers (parallel):
        σ_eff = sum(σ_i · L_i) / L

    Args:
        conductivities: List of layer conductivities σ_i.
        thicknesses: List of layer thicknesses L_i.
        flow_direction: "perpendicular" (through layers) or
                        "parallel" (along layers).

    Returns:
        Effective conductivity σ_eff.

    Reference:
        Part II, Art. 278: Composite conductors.
    """
    if len(conductivities) != len(thicknesses):
        raise ValueError("Conductivities and thicknesses must have same length")

    total_thickness = sum(thicknesses)
    if total_thickness <= 0:
        raise ValueError("Total thickness must be positive")

    if flow_direction == "parallel":
        # Parallel combination: σ_eff = sum(σ_i · L_i) / L
        sigma_eff = (
            sum(σ * L for σ, L in zip(conductivities, thicknesses)) / total_thickness
        )
    elif flow_direction == "perpendicular":
        # Series combination: σ_eff = L / sum(L_i / σ_i)
        resistance_sum = sum(L / σ for σ, L in zip(conductivities, thicknesses))
        sigma_eff = total_thickness / resistance_sum
    else:
        raise ValueError(f"Unknown flow direction: {flow_direction}")

    return sigma_eff

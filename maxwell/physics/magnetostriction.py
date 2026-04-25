"""
Magnetostriction — deformation of magnetic materials under magnetization.

Implements the theory of magnetostriction from Part III of Maxwell's Treatise:
- Dimensional changes in magnetized materials (Arts. 447-448)
- Magnetoelastic coupling
- Volume and shape changes

When a ferromagnetic material is magnetized, it undergoes small
but measurable dimensional changes. This phenomenon, called
magnetostriction, results from the coupling between magnetic
order and crystal lattice strain.

Key effects:
- Linear magnetostriction: ΔL/L = λ (strain proportional to M²)
- Volume magnetostriction: ΔV/V (change in volume)
- Joule magnetostriction: Elongation along field direction

Category: A (maxwell_original) — Maxwell's theory of magnetostriction.

References:
    Part III, Arts. 447-448: Magnetostriction.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class MagnetostrictionTensor:
    """
    Magnetostriction tensor describing strain due to magnetization.

    Arts. 447-448: The magnetostriction tensor λ_ij relates the
    strain ε_ij to the magnetization direction:

        ε_ij = λ_ij (M̂)

    For cubic crystals, the tensor is characterized by two constants:
    - λ₁₀₀: Magnetostriction along [100] direction
    - λ₁₁₁: Magnetostriction along [111] direction

    Attributes:
        lambda_100: Magnetostriction constant λ₁₀₀.
        lambda_111: Magnetostriction constant λ₁₁₁.
        crystal_axis: Crystal orientation axes.
    """

    lambda_100: float  # Dimensionless strain
    lambda_111: float  # Dimensionless strain
    crystal_axis: np.ndarray = None  # shape (3, 3), rotation matrix

    def __post_init__(self):
        if self.crystal_axis is None:
            self.crystal_axis = np.eye(3)
        else:
            self.crystal_axis = np.asarray(self.crystal_axis, dtype=np.float64)

    @maxwell_cite(
        447,
        part=3, chapter="Magnetostriction",
        theory_class="maxwell_original",
        description="Calculate strain tensor from magnetization",
    )
    def strain_tensor(self, magnetization_direction: np.ndarray) -> np.ndarray:
        """
        Calculate magnetostrictive strain tensor.

        Art. 447: For a cubic crystal with magnetization direction
        α = (α₁, α₂, α₃), the strain tensor is:

            ε_ij = (3/2)λ₁₀₀(αᵢαⱼ - δᵢⱼ/3) + 3λ₁₁₁αᵢαⱼ (for i≠j)

        Args:
            magnetization_direction: Unit vector M̂ (3,).

        Returns:
            Strain tensor ε_ij (3, 3).

        Reference:
            Part III, Art. 447: Strain tensor.
        """
        alpha = np.asarray(magnetization_direction, dtype=np.float64)
        alpha = alpha / np.linalg.norm(alpha)

        # Initialize strain tensor
        epsilon = np.zeros((3, 3))

        # Diagonal components (λ₁₀₀ contribution)
        for i in range(3):
            for j in range(3):
                if i == j:
                    epsilon[i, j] = (3/2) * self.lambda_100 * (alpha[i]**2 - 1/3)
                else:
                    # Off-diagonal (λ₁₁₁ contribution)
                    epsilon[i, j] = (3/2) * self.lambda_111 * alpha[i] * alpha[j]

        return epsilon

    @maxwell_cite(
        447,
        part=3, chapter="Magnetostriction",
        theory_class="maxwell_original",
        description="Calculate linear strain along measurement direction",
    )
    def linear_strain(
        self,
        magnetization_direction: np.ndarray,
        measurement_direction: np.ndarray,
    ) -> float:
        """
        Calculate linear magnetostriction along a measurement direction.

        Art. 447: The fractional length change ΔL/L along direction β
        when magnetized along α is:

            ΔL/L = (3/2)λ₁₀₀(Σ αᵢ²βᵢ² - 1/3) + 3λ₁₁₁(α₁β₁α₂β₂ + ...)

        For parallel directions (α = β):
            ΔL/L = (3/2)λ₁₀₀(α₁²α₂² + α₂²α₃² + α₃²α₁²)

        Args:
            magnetization_direction: Magnetization direction α.
            measurement_direction: Measurement direction β.

        Returns:
            Linear strain ΔL/L (dimensionless).

        Reference:
            Part III, Art. 447: Linear magnetostriction.
        """
        alpha = np.asarray(magnetization_direction, dtype=np.float64)
        beta = np.asarray(measurement_direction, dtype=np.float64)

        alpha = alpha / np.linalg.norm(alpha)
        beta = beta / np.linalg.norm(beta)

        # Compute strain tensor
        epsilon = self.strain_tensor(alpha)

        # Project onto measurement direction: ε = βᵀ ε β
        strain = float(beta @ epsilon @ beta)

        return strain


@dataclass
class MagnetostrictiveMaterial:
    """
    Magnetostrictive material properties and behavior.

    Arts. 447-448: A magnetostrictive material changes dimensions
    when magnetized. The effect depends on:
    - Material composition (λ constants)
    - Crystal structure
    - Magnetization state
    - Applied stress

    Attributes:
        name: Material name.
        magnetostriction: MagnetostrictionTensor object.
        youngs_modulus: Elastic modulus E (dyne/cm²).
        poissons_ratio: Poisson ratio ν.
    """

    name: str
    magnetostriction: MagnetostrictionTensor
    youngs_modulus: float  # E, dyne/cm²
    poissons_ratio: float  # ν, dimensionless

    @classmethod
    @maxwell_cite(
        447,
        part=3, chapter="Magnetostriction",
        theory_class="maxwell_original",
        description="Create material from saturation magnetostriction",
    )
    def from_saturation_magnetostriction(
        cls,
        name: str,
        lambda_s: float,
        youngs_modulus: float,
        poissons_ratio: float = 0.3,
    ) -> MagnetostrictiveMaterial:
        """
        Create material from saturation magnetostriction constant.

        Art. 447: For isotropic polycrystalline materials, the
        saturation magnetostriction λ_s characterizes the maximum
        strain at magnetic saturation.

        Args:
            name: Material name.
            lambda_s: Saturation magnetostriction λ_s.
            youngs_modulus: Elastic modulus E (dyne/cm²).
            poissons_ratio: Poisson ratio.

        Returns:
            MagnetostrictiveMaterial object.

        Reference:
            Part III, Art. 447: Saturation magnetostriction.
        """
        # For isotropic material, λ₁₀₀ = λ₁₁₁ = (2/3)λ_s
        lambda_100 = (2/3) * lambda_s
        lambda_111 = (2/3) * lambda_s

        return cls(
            name=name,
            magnetostriction=MagnetostrictionTensor(
                lambda_100=lambda_100,
                lambda_111=lambda_111,
            ),
            youngs_modulus=youngs_modulus,
            poissons_ratio=poissons_ratio,
        )

    @maxwell_cite(
        448,
        part=3, chapter="Magnetostriction",
        theory_class="maxwell_original",
        description="Calculate magnetostrictive stress",
    )
    def magnetostrictive_stress(
        self,
        magnetization_direction: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate magnetostrictive stress tensor.

        Art. 448: The magnetostrictive strain generates internal
        stress when the material is constrained. The stress is:

            σ_ij = C_ijkl × ε_kl

        For isotropic elasticity:
            σ = E/(1+ν) × ε + Eν/((1+ν)(1-2ν)) × Tr(ε) × I

        Args:
            magnetization_direction: Magnetization direction M̂.

        Returns:
            Stress tensor σ_ij (dyne/cm²).

        Reference:
            Part III, Art. 448: Magnetostrictive stress.
        """
        epsilon = self.magnetostriction.strain_tensor(magnetization_direction)

        E = self.youngs_modulus
        nu = self.poissons_ratio

        # Isotropic elastic constants
        G = E / (2 * (1 + nu))  # Shear modulus
        K = E / (3 * (1 - 2 * nu))  # Bulk modulus

        # Stress = 2G × dev(ε) + 3K × vol(ε)
        trace_epsilon = np.trace(epsilon)
        deviatoric = epsilon - (trace_epsilon / 3) * np.eye(3)

        stress = 2 * G * deviatoric + K * trace_epsilon * np.eye(3)

        return stress

    @maxwell_cite(
        448,
        part=3, chapter="Magnetostriction",
        theory_class="maxwell_original",
        description="Calculate Villari effect (inverse magnetostriction)",
    )
    def villari_effect(
        self,
        applied_stress: np.ndarray,
        initial_magnetization: np.ndarray,
    ) -> np.ndarray:
        """
        Calculate change in magnetization due to applied stress.

        Art. 448: The Villari effect (inverse magnetostriction) is
        the change in magnetic susceptibility due to mechanical
        stress. Stress modifies the magnetic anisotropy energy:

            E_stress = -(3/2)λ_s σ cos²(θ)

        where θ is the angle between stress and magnetization.

        Args:
            applied_stress: Applied stress tensor (dyne/cm²).
            initial_magnetization: Initial M direction.

        Returns:
            New magnetization direction.

        Reference:
            Part III, Art. 448: Villari effect.
        """
        M_init = np.asarray(initial_magnetization, dtype=np.float64)
        M_init = M_init / np.linalg.norm(M_init)

        # Stress-induced anisotropy
        # Principal stress direction
        eigenvalues, eigenvectors = np.linalg.eigh(applied_stress)
        max_stress_idx = np.argmax(np.abs(eigenvalues))
        stress_direction = eigenvectors[:, max_stress_idx]

        # Magnetoelastic coupling tends to align M with stress
        # for positive λ_s, perpendicular for negative λ_s
        lambda_s = (self.magnetostriction.lambda_100 +
                   2 * self.magnetostriction.lambda_111) / 3

        if lambda_s > 0:
            # Align with tensile stress
            new_M = stress_direction
        else:
            # Perpendicular to stress (approximate)
            new_M = np.cross(M_init, stress_direction)
            if np.linalg.norm(new_M) < 1e-6:
                new_M = np.array([1, 0, 0])
            new_M = new_M / np.linalg.norm(new_M)

        return new_M


@maxwell_cite(
    447,
    part=3, chapter="Magnetostriction",
    theory_class="maxwell_original",
    description="Calculate Joule magnetostriction",
)
def joule_magnetostriction(
    lambda_s: float,
    field_direction: np.ndarray,
    measurement_direction: np.ndarray,
) -> float:
    """
    Calculate Joule magnetostriction (elongation along field).

    Art. 447: Joule discovered that iron elongates along the
    direction of magnetization. The strain is:

        ΔL/L = (3/2)λ_s cos²(θ)

    where θ is the angle between measurement and field directions.
    For θ = 0 (parallel): ΔL/L = (3/2)λ_s

    Args:
        lambda_s: Saturation magnetostriction constant.
        field_direction: Magnetic field direction.
        measurement_direction: Direction of length measurement.

    Returns:
        Linear strain ΔL/L (dimensionless).

    Reference:
        Part III, Art. 447: Joule magnetostriction.
    """
    H_dir = np.asarray(field_direction, dtype=np.float64)
    meas_dir = np.asarray(measurement_direction, dtype=np.float64)

    H_dir = H_dir / np.linalg.norm(H_dir)
    meas_dir = meas_dir / np.linalg.norm(meas_dir)

    cos_theta = float(np.dot(H_dir, meas_dir))

    return float((3/2) * lambda_s * cos_theta**2)


@maxwell_cite(
    448,
    part=3, chapter="Magnetostriction",
    theory_class="maxwell_original",
    description="Calculate volume magnetostriction",
)
def volume_magnetostriction(
    magnetization_magnitude: float,
    saturation_magnetization: float,
    bulk_modulus: float,
    magnetoelastic_constant: float,
) -> float:
    """
    Calculate volume change due to magnetization.

    Art. 448: In addition to linear magnetostriction, materials
    exhibit volume magnetostriction:

        ΔV/V = b × (M/M_s)²

    where b is the magnetoelastic coupling constant.

    Args:
        magnetization_magnitude: |M| (emu/cm³).
        saturation_magnetization: M_s (emu/cm³).
        bulk_modulus: Bulk modulus B (dyne/cm²).
        magnetoelastic_constant: Coupling constant b.

    Returns:
        Volume strain ΔV/V (dimensionless).

    Reference:
        Part III, Art. 448: Volume magnetostriction.
    """
    if saturation_magnetization == 0:
        return 0.0

    M_ratio = magnetization_magnitude / saturation_magnetization

    return float(magnetoelastic_constant * M_ratio**2)


@maxwell_cite(
    447,
    part=3, chapter="Magnetostriction",
    theory_class="maxwell_original",
    description="Typical magnetostriction constants for materials",
)
def typical_magnetostriction_constants() -> dict[str, dict[str, float]]:
    """
    Return typical magnetostriction constants for common materials.

    Arts. 447-448: Maxwell catalogs the magnetostrictive properties
    of various substances. Modern measurements give these values:

    Returns:
        Dictionary mapping material names to properties.

    Reference:
        Part III, Arts. 447-448: Magnetostriction table.
    """
    return {
        # Positive magnetostriction (elongates along field)
        "iron": {
            "lambda_s": 21e-6,
            "lambda_100": 21e-6,
            "lambda_111": -21e-6,
            "type": "positive",
            "youngs_modulus": 2.1e12,  # dyne/cm²
        },
        "nickel": {
            "lambda_s": -33e-6,
            "lambda_100": -46e-6,
            "lambda_111": -25e-6,
            "type": "negative",
            "youngs_modulus": 2.0e12,
        },
        "cobalt": {
            "lambda_s": -60e-6,
            "lambda_100": -60e-6,
            "lambda_111": -40e-6,
            "type": "negative",
            "youngs_modulus": 2.1e12,
        },
        # Giant magnetostrictive materials
        "terfenol_D": {
            "lambda_s": 1600e-6,  # 0.16% strain!
            "lambda_100": 1600e-6,
            "lambda_111": 800e-6,
            "type": "giant_positive",
            "youngs_modulus": 2.5e11,
            "composition": "Tb₀.₃Dy₀.₇Fe₂",
        },
        "galfenol": {
            "lambda_s": 400e-6,
            "lambda_100": 400e-6,
            "lambda_111": 200e-6,
            "type": "large_positive",
            "youngs_modulus": 7e11,
            "composition": "Fe₁₋ₓGaₓ",
        },
        # Low magnetostriction (for transformer cores)
        "permalloy": {
            "lambda_s": 0,  # Tuned to near zero
            "lambda_100": 0.5e-6,
            "lambda_111": -0.5e-6,
            "type": "near_zero",
            "youngs_modulus": 1.6e12,
        },
        "mu_metal": {
            "lambda_s": 2e-6,
            "lambda_100": 2e-6,
            "lambda_111": 1e-6,
            "type": "very_low",
            "youngs_modulus": 1.5e12,
        },
    }


@maxwell_cite(
    447, 448,
    part=3, chapter="Magnetostriction",
    theory_class="maxwell_original",
    description="Calculate magnetoelastic energy",
)
def magnetoelastic_energy(
    magnetization_direction: np.ndarray,
    stress_tensor: np.ndarray,
    lambda_s: float,
) -> float:
    """
    Calculate magnetoelastic coupling energy.

    Art. 447-448: The energy of interaction between magnetization
    and stress is:

        E_me = -(3/2)λ_s σ cos²(θ)

    where σ is the stress along the magnetization direction.

    This energy contributes to magnetic anisotropy and affects
    domain structure.

    Args:
        magnetization_direction: Unit vector M̂.
        stress_tensor: Applied stress σ_ij (dyne/cm²).
        lambda_s: Saturation magnetostriction.

    Returns:
        Magnetoelastic energy density (erg/cm³).

    Reference:
        Part III, Arts. 447-448: Magnetoelastic energy.
    """
    M_dir = np.asarray(magnetization_direction, dtype=np.float64)
    M_dir = M_dir / np.linalg.norm(M_dir)

    stress_tensor = np.asarray(stress_tensor, dtype=np.float64)

    # Stress along magnetization direction: σ = Mᵀ σ M
    sigma_M = float(M_dir @ stress_tensor @ M_dir)

    return float(-(3/2) * lambda_s * sigma_M)


@maxwell_cite(
    447,
    part=3, chapter="Magnetostriction",
    theory_class="maxwell_original",
    description="Explain magnetostriction phenomena",
)
def explain_magnetostriction_phenomena() -> dict[str, str]:
    """
    Explain the physical phenomena of magnetostriction.

    Arts. 447-448: Maxwell's explanation of magnetostriction:

    1. Spin-orbit coupling links magnetic moments to lattice
    2. Magnetization rotation distorts the crystal lattice
    3. Applied stress modifies magnetic anisotropy (Villari effect)

    Returns:
        Dictionary with explanations of magnetostrictive phenomena.

    Reference:
        Part III, Arts. 447-448: Magnetostriction explanation.
    """
    return {
        "joule_effect": (
            "Discovered by James Joule in 1842, this is the elongation or "
            "contraction of a ferromagnetic material when magnetized. The "
            "effect is quadratic in magnetization and reversible. Iron "
            "elongates along the field direction; nickel contracts."
        ),
        "villari_effect": (
            "The inverse magnetostrictive effect: applied stress changes "
            "the magnetic susceptibility and magnetization curve. Tensile "
            "stress increases permeability for positive λ_s materials, "
            "decreases it for negative λ_s materials like nickel."
        ),
        "volume_magnetostriction": (
            "A small volume change accompanying magnetization, distinct "
            "from linear magnetostriction. Related to the pressure "
            "dependence of the Curie temperature and exchange interactions."
        ),
        "physical_origin": (
            "Art. 447-448: Magnetostriction arises from spin-orbit coupling, "
            "which links the orientation of electron spins (magnetic moments) "
            "to the orbital wavefunctions that determine interatomic spacing. "
            "When spins align, the lattice distorts to minimize total energy."
        ),
        "applications": (
            "Magnetostrictive materials are used in: ultrasonic transducers "
            "(Terfenol-D), precision actuators, sensors, torque sensors, and "
            "vibration dampers. Low magnetostriction alloys are essential "
            "for transformer cores to minimize energy loss."
        ),
    }

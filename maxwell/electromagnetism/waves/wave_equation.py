"""
Electromagnetic Wave Equation — derivation and solutions of the 3D wave equation.

Implements Maxwell's electromagnetic theory of light from Articles 781-785:

- Wave equation derivation from field equations (Art. 781)
- Electromagnetic nature of light (Art. 782)
- Wave equation in homogeneous media (Art. 783)
- Three-dimensional wave propagation (Art. 784)
- Wave speed and permittivity/permeability (Art. 785)

Maxwell's great discovery: electromagnetic disturbances propagate as waves
with speed v = c/√(εμ), which for vacuum gives v = c, the speed of light.

The wave equation in vacuum:
    ∇²E - (1/c²) ∂²E/∂t² = 0
    ∇²B - (1/c²) ∂²B/∂t² = 0

In a medium with permittivity ε and permeability μ:
    ∇²E - (εμ/c²) ∂²E/∂t² = 0

Wave speed: v = c/√(εμ)
Refractive index: n = c/v = √(εμ)

CGS Units:
    E = electric field (statvolts/cm)
    B = magnetic flux density (gauss)
    c = speed of light = 2.99792458×10¹⁰ cm/s
    ε = permittivity (dimensionless in CGS)
    μ = permeability (dimensionless in CGS)

Category: A (maxwell_original) — Maxwell's electromagnetic theory of light.

References:
    Part IV, Ch XX: Electromagnetic Theory of Light (Arts. 781-805).
    Part IV, Arts. 781-785: Wave equation derivation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional, Tuple

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class ElectromagneticWave:
    """
    Electromagnetic wave solution to Maxwell's equations.

    Art. 781-785: An electromagnetic wave is characterized by:
    - Angular frequency ω = 2πf (rad/s)
    - Wave vector k (rad/cm), |k| = ω/v = 2π/λ
    - Electric field amplitude E₀
    - Magnetic field amplitude B₀
    - Polarization direction

    For a plane wave in vacuum:
        E(r,t) = E₀ cos(k·r - ωt + φ)
        B(r,t) = B₀ cos(k·r - ωt + φ)

    where:
        |B₀| = |E₀|/c (in vacuum)
        k·E₀ = 0 (transverse electric)
        k·B₀ = 0 (transverse magnetic)
        E₀ × B₀ points in propagation direction

    Attributes:
        frequency: f (Hz).
        wavelength: λ (cm).
        wave_vector: k vector (rad/cm).
        E_amplitude: Electric field amplitude E₀ (statvolts/cm).
        B_amplitude: Magnetic field amplitude B₀ (gauss).
        polarization: Unit vector in E-field direction.
        phase: Initial phase φ (radians).
    """

    frequency: float = 0.0
    wavelength: float = 0.0
    wave_vector: np.ndarray = field(default_factory=lambda: np.zeros(3))
    E_amplitude: float = 0.0
    B_amplitude: float = 0.0
    polarization: np.ndarray = field(default_factory=lambda: np.array([1.0, 0.0, 0.0]))
    phase: float = 0.0
    permittivity: float = 1.0
    permeability: float = 1.0

    def __post_init__(self):
        """Validate and compute derived quantities."""
        self.wave_vector = np.asarray(self.wave_vector, dtype=np.float64)
        self.polarization = np.asarray(self.polarization, dtype=np.float64)

        # Normalize polarization
        pol_norm = np.linalg.norm(self.polarization)
        if pol_norm > 0:
            self.polarization = self.polarization / pol_norm

        # Compute wave properties if frequency is given
        if self.frequency > 0 and self.wavelength == 0:
            # v = c/√(εμ)
            v = CONST.C / np.sqrt(self.permittivity * self.permeability)
            self.wavelength = v / self.frequency

            # |k| = 2π/λ = ω/v
            if np.allclose(self.wave_vector, 0):
                k_mag = 2.0 * np.pi / self.wavelength
                self.wave_vector = k_mag * np.array([0.0, 0.0, 1.0])  # Propagate in z

        # Compute B amplitude from E amplitude if not specified
        if self.E_amplitude > 0 and self.B_amplitude == 0:
            # In vacuum: B₀ = E₀/c
            # In medium: B₀ = E₀/v = E₀√(εμ)/c
            v = CONST.C / np.sqrt(self.permittivity * self.permeability)
            self.B_amplitude = self.E_amplitude / v

    @property
    def angular_frequency(self) -> float:
        """Angular frequency ω = 2πf (rad/s)."""
        return 2.0 * np.pi * self.frequency

    @property
    def wave_number(self) -> float:
        """Wave number |k| = 2π/λ (rad/cm)."""
        return np.linalg.norm(self.wave_vector)

    @property
    def phase_velocity(self) -> float:
        """Phase velocity v = ω/|k| = c/√(εμ) (cm/s)."""
        k_mag = self.wave_number
        if k_mag > 0:
            return self.angular_frequency / k_mag
        return CONST.C / np.sqrt(self.permittivity * self.permeability)

    @property
    def propagation_direction(self) -> np.ndarray:
        """Unit vector in propagation direction (k̂)."""
        k_mag = self.wave_number
        if k_mag > 0:
            return self.wave_vector / k_mag
        return np.array([0.0, 0.0, 1.0])

    @classmethod
    @maxwell_cite(
        781,
        782,
        part=4,
        chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Create EM wave from frequency and amplitude",
    )
    def from_frequency(
        cls,
        frequency: float,
        E_amplitude: float,
        propagation_direction: np.ndarray = None,
        polarization: np.ndarray = None,
        epsilon: float = 1.0,
        mu: float = 1.0,
    ) -> ElectromagneticWave:
        """
        Create an electromagnetic wave from frequency and amplitude.

        Art. 781-782: Specify an EM wave by its fundamental properties:
        frequency, amplitude, and propagation characteristics.

        Args:
            frequency: Wave frequency f (Hz).
            E_amplitude: Electric field amplitude E₀ (statvolts/cm).
            propagation_direction: Unit vector k̂ (default: z-axis).
            polarization: Unit vector for E-field (default: x-axis).
            epsilon: Permittivity ε (default: 1.0 for vacuum).
            mu: Permeability μ (default: 1.0 for vacuum).

        Returns:
            ElectromagneticWave object.

        Reference:
            Part IV, Arts. 781-782: EM wave specification.

        Example:
            >>> wave = ElectromagneticWave.from_frequency(
            ...     frequency=5e14,  # Green light
            ...     E_amplitude=100.0,
            ...     propagation_direction=np.array([0, 0, 1]),
            ...     polarization=np.array([1, 0, 0])
            ... )
        """
        if propagation_direction is None:
            propagation_direction = np.array([0.0, 0.0, 1.0])
        if polarization is None:
            polarization = np.array([1.0, 0.0, 0.0])

        propagation_direction = np.asarray(propagation_direction, dtype=np.float64)
        propagation_direction = propagation_direction / np.linalg.norm(
            propagation_direction
        )

        # Compute wavelength and wave vector
        v = CONST.C / np.sqrt(epsilon * mu)
        wavelength = v / frequency
        k_mag = 2.0 * np.pi / wavelength
        wave_vector = k_mag * propagation_direction

        return cls(
            frequency=frequency,
            wavelength=wavelength,
            wave_vector=wave_vector,
            E_amplitude=E_amplitude,
            polarization=polarization,
            permittivity=epsilon,
            permeability=mu,
        )


@maxwell_cite(
    781,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Derive wave equation from Maxwell's equations",
)
def derive_wave_equation(
    epsilon: float = 1.0,
    mu: float = 1.0,
    conductivity: float = 0.0,
) -> dict[str, float | str]:
    """
    Derive the electromagnetic wave equation from Maxwell's equations.

    Art. 781: Starting from Maxwell's equations in a homogeneous,
    isotropic medium with no free charges (ρ = 0):

    ∇ × E = -(1/c) ∂B/∂t          (Faraday's law)
    ∇ × H = (4π/c)J + (1/c) ∂D/∂t  (Ampere-Maxwell)

    With constitutive relations:
    D = εE, B = μH, J = σE

    Taking curl of Faraday's law:
    ∇ × (∇ × E) = -(1/c) ∂(∇ × B)/∂t

    Using vector identity ∇ × (∇ × E) = ∇(∇·E) - ∇²E
    and substituting Ampere-Maxwell for ∇ × B:

    For σ = 0 (non-conducting medium):
    ∇²E - (εμ/c²) ∂²E/∂t² = 0

    This is the wave equation with wave speed v = c/√(εμ).

    Args:
        epsilon: Permittivity ε (default: 1.0).
        mu: Permeability μ (default: 1.0).
        conductivity: σ (default: 0.0).

    Returns:
        Dictionary with:
        - wave_speed: v = c/√(εμ) (cm/s)
        - wave_equation: String form of the equation
        - refractive_index: n = √(εμ)
        - is_lossless: True if σ = 0

    Reference:
        Part IV, Art. 781: Wave equation derivation.

    Example:
        >>> result = derive_wave_equation()
        >>> print(f"Wave speed: {result['wave_speed']:.3e} cm/s")
        >>> print(f"Equation: {result['wave_equation']}")
    """
    # Wave speed
    v = CONST.C / np.sqrt(epsilon * mu)

    # Refractive index
    n = np.sqrt(epsilon * mu)

    # Lossless if no conductivity
    is_lossless = conductivity == 0.0

    # Wave equation string
    if is_lossless:
        wave_eq = f"∇²E - ({epsilon*mu}/{CONST.C**2:.2e}) ∂²E/∂t² = 0"
    else:
        wave_eq = f"∇²E - ({4*np.pi*conductivity}/{CONST.C}) ∂E/∂t - ({epsilon*mu}/{CONST.C**2:.2e}) ∂²E/∂t² = 0"

    return {
        "wave_speed": v,
        "refractive_index": n,
        "wave_equation": wave_eq,
        "is_lossless": is_lossless,
        "permittivity": epsilon,
        "permeability": mu,
        "conductivity": conductivity,
    }


@maxwell_cite(
    783,
    784,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate 3D wave equation solution",
)
def calc_wave_equation_3d(
    wave: ElectromagneticWave,
    position: np.ndarray,
    time: float,
) -> dict[str, np.ndarray | float]:
    """
    Calculate the 3D electromagnetic wave field at a point.

    Art. 783-784: For a plane electromagnetic wave, the fields are:

        E(r,t) = E₀ · ê_p · cos(k·r - ωt + φ)
        B(r,t) = B₀ · ê_b · cos(k·r - ωt + φ)

    where:
        ê_p = polarization direction (E-field direction)
        ê_b = k̂ × ê_p (B-field direction, perpendicular to both k and E)
        k·r = phase from position
        ωt = phase from time

    The fields satisfy:
    - E ⊥ k (transverse electric)
    - B ⊥ k (transverse magnetic)
    - E ⊥ B
    - |E|/|B| = v (wave speed)

    Args:
        wave: ElectromagneticWave object.
        position: Position r (cm).
        time: Time t (s).

    Returns:
        Dictionary with:
        - E_field: Electric field vector E(r,t) (statvolts/cm)
        - B_field: Magnetic flux density B(r,t) (gauss)
        - phase: Instantaneous phase k·r - ωt + φ
        - intensity: Proportional to |E|²

    Reference:
        Part IV, Arts. 783-784: 3D wave solution.

    Example:
        >>> wave = ElectromagneticWave.from_frequency(5e14, 100.0)
        >>> result = calc_wave_equation_3d(wave, np.array([0, 0, 0]), 0.0)
        >>> print(f"E = {result['E_field']} statvolts/cm")
    """
    position = np.asarray(position, dtype=np.float64)

    # Angular frequency and wave vector
    omega = wave.angular_frequency
    k = wave.wave_vector

    # Phase: k·r - ωt + φ
    phase = np.dot(k, position) - omega * time + wave.phase

    # Electric field: E = E₀ · ê_p · cos(phase)
    E_field = wave.E_amplitude * wave.polarization * np.cos(phase)

    # Magnetic field direction: ê_b = k̂ × ê_p
    k_hat = wave.propagation_direction
    B_direction = np.cross(k_hat, wave.polarization)
    B_direction = B_direction / np.linalg.norm(B_direction)

    # B field: B = B₀ · ê_b · cos(phase)
    B_field = wave.B_amplitude * B_direction * np.cos(phase)

    # Intensity (proportional to |E|²)
    intensity = np.dot(E_field, E_field)

    return {
        "E_field": E_field,
        "B_field": B_field,
        "phase": phase,
        "phase_degrees": np.degrees(phase) % 360,
        "intensity": intensity,
        "E_magnitude": np.linalg.norm(E_field),
        "B_magnitude": np.linalg.norm(B_field),
    }


@maxwell_cite(
    785,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate wave speed in medium",
)
def calc_wave_speed(
    epsilon: float = 1.0,
    mu: float = 1.0,
) -> dict[str, float]:
    """
    Calculate electromagnetic wave speed in a medium.

    Art. 785: Maxwell's prediction that the speed of electromagnetic
    waves in a medium is:

        v = c / √(εμ)

    where:
        c = speed of light in vacuum = 2.99792458×10¹⁰ cm/s
        ε = relative permittivity (dielectric constant)
        μ = relative permeability

    The refractive index is:
        n = c/v = √(εμ)

    For vacuum: ε = μ = 1, so v = c
    For air: ε ≈ 1.0006, μ ≈ 1, so v ≈ 0.9997c
    For water: ε ≈ 80 (static), μ = 1, so v ≈ c/9 (optical)

    Args:
        epsilon: Relative permittivity ε (dimensionless).
        mu: Relative permeability μ (dimensionless).

    Returns:
        Dictionary with:
        - wave_speed: v (cm/s)
        - refractive_index: n = c/v
        - vacuum_speed: c
        - speed_ratio: v/c

    Reference:
        Part IV, Art. 785: Wave speed in media.

    Example:
        >>> result = calc_wave_speed(epsilon=2.25)  # Glass
        >>> print(f"v = {result['wave_speed']:.3e} cm/s")
        >>> print(f"n = {result['refractive_index']}")
    """
    if epsilon <= 0 or mu <= 0:
        raise ValueError("Permittivity and permeability must be positive")

    # Wave speed
    v = CONST.C / np.sqrt(epsilon * mu)

    # Refractive index
    n = np.sqrt(epsilon * mu)

    return {
        "wave_speed": v,
        "refractive_index": n,
        "vacuum_speed": CONST.C,
        "speed_ratio": v / CONST.C,
        "permittivity": epsilon,
        "permeability": mu,
    }


@maxwell_cite(
    781,
    782,
    783,
    784,
    785,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Verify wave equation satisfies Maxwell's equations",
)
def verify_wave_equation(
    wave: ElectromagneticWave,
    test_points: int = 10,
    tolerance: float = 1e-10,
) -> dict[str, bool | float | dict]:
    """
    Verify that the electromagnetic wave satisfies Maxwell's equations.

    Art. 781-785: This function verifies that the plane wave solution
    satisfies all of Maxwell's equations:

    1. ∇ · E = 0 (no charge in vacuum)
    2. ∇ · B = 0 (no magnetic monopoles)
    3. ∇ × E = -(1/c) ∂B/∂t (Faraday's law)
    4. ∇ × B = (1/c) ∂E/∂t (Ampere-Maxwell in vacuum)

    For a plane wave E = E₀ cos(k·r - ωt), B = B₀ cos(k·r - ωt):
    - ∇ · E = -k·E₀ sin(k·r - ωt) = 0 if k ⊥ E₀ (transverse)
    - ∇ · B = -k·B₀ sin(k·r - ωt) = 0 if k ⊥ B₀ (transverse)
    - ∇ × E = k × E₀ sin(k·r - ωt)
    - ∂B/∂t = ω B₀ sin(k·r - ωt)
    - Faraday: k × E₀ = (ω/c) B₀ ✓

    Args:
        wave: ElectromagneticWave object.
        test_points: Number of test points in space-time.
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with:
        - all_verified: True if all equations satisfied
        - divergence_E: ∇ · E verification
        - divergence_B: ∇ · B verification
        - faraday: ∇ × E + (1/c)∂B/∂t verification
        - ampere_maxwell: ∇ × B - (1/c)∂E/∂t verification

    Reference:
        Part IV, Arts. 781-785: Wave equation verification.

    Example:
        >>> wave = ElectromagneticWave.from_frequency(5e14, 100.0)
        >>> result = verify_wave_equation(wave)
        >>> assert result['all_verified']
    """
    results = {}
    all_verified = True

    # Test at multiple points
    omega = wave.angular_frequency
    k = wave.wave_vector
    k_mag = wave.wave_number

    # Precompute directions
    k_hat = wave.propagation_direction
    p_hat = wave.polarization
    b_hat = np.cross(k_hat, p_hat)
    b_hat = b_hat / np.linalg.norm(b_hat)

    # E₀ and B₀ vectors
    E0_vec = wave.E_amplitude * p_hat
    B0_vec = wave.B_amplitude * b_hat

    # Test at random points
    max_div_E = 0.0
    max_div_B = 0.0
    max_faraday = 0.0
    max_ampere = 0.0

    for i in range(test_points):
        # Random position and time
        r = np.random.uniform(-wave.wavelength, wave.wavelength, 3)
        t = np.random.uniform(0, 1.0 / wave.frequency)

        phase = np.dot(k, r) - omega * t
        sin_phase = np.sin(phase)
        cos_phase = np.cos(phase)

        # Fields
        E = E0_vec * cos_phase
        B = B0_vec * cos_phase

        # ∇ · E = -k·E₀ sin(phase) = 0 for transverse wave
        div_E = -np.dot(k, E0_vec) * sin_phase
        max_div_E = max(max_div_E, abs(div_E))

        # ∇ · B = -k·B₀ sin(phase) = 0 for transverse wave
        div_B = -np.dot(k, B0_vec) * sin_phase
        max_div_B = max(max_div_B, abs(div_B))

        # ∇ × E = k × E₀ sin(phase)
        curl_E = np.cross(k, E0_vec) * sin_phase

        # ∂B/∂t = ω B₀ sin(phase)
        dB_dt = omega * B0_vec * sin_phase

        # Faraday: ∇ × E + (1/c) ∂B/∂t = 0
        faraday_residual = curl_E + (1.0 / CONST.C) * dB_dt
        max_faraday = max(max_faraday, np.linalg.norm(faraday_residual))

        # ∇ × B = k × B₀ sin(phase)
        curl_B = np.cross(k, B0_vec) * sin_phase

        # ∂E/∂t = ω E₀ sin(phase)
        dE_dt = omega * E0_vec * sin_phase

        # Ampere-Maxwell: ∇ × B - (1/c) ∂E/∂t = 0 (vacuum)
        ampere_residual = curl_B - (1.0 / CONST.C) * dE_dt
        max_ampere = max(max_ampere, np.linalg.norm(ampere_residual))

    # Check tolerances
    E0_scale = wave.E_amplitude * k_mag
    B0_scale = wave.B_amplitude * k_mag

    div_E_ok = max_div_E < tolerance * E0_scale
    div_B_ok = max_div_B < tolerance * B0_scale
    faraday_ok = max_faraday < tolerance * E0_scale * k_mag
    ampere_ok = max_ampere < tolerance * B0_scale * k_mag

    results["divergence_E"] = {"verified": div_E_ok, "max_residual": max_div_E}
    results["divergence_B"] = {"verified": div_B_ok, "max_residual": max_div_B}
    results["faraday"] = {"verified": faraday_ok, "max_residual": max_faraday}
    results["ampere_maxwell"] = {"verified": ampere_ok, "max_residual": max_ampere}
    results["all_verified"] = div_E_ok and div_B_ok and faraday_ok and ampere_ok

    return results


@maxwell_cite(
    781,
    782,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate wave impedance of medium",
)
def calc_wave_impedance(
    epsilon: float = 1.0,
    mu: float = 1.0,
) -> dict[str, float]:
    """
    Calculate the wave impedance (ratio of E to B fields).

    Art. 781-782: For a plane electromagnetic wave, the ratio of
    electric to magnetic field amplitudes is the wave impedance:

    In CGS-Gaussian units:
        Z = |E|/|H| = √(μ/ε) × (4π/c)

    But more commonly, we use the E/B ratio:
        |E|/|B| = v = c/√(εμ) (wave speed)

    In vacuum (ε = μ = 1):
        |E|/|B| = c = 2.99792458×10¹⁰ cm/s

    This is a fundamental property of electromagnetic waves:
    the electric and magnetic fields are related by the speed of light.

    Args:
        epsilon: Relative permittivity ε.
        mu: Relative permeability μ.

    Returns:
        Dictionary with:
        - E_over_B: |E|/|B| = v (cm/s)
        - E_over_H: |E|/|H| = Z (CGS impedance)
        - wave_speed: v = c/√(εμ) (cm/s)
        - intrinsic_impedance: Z₀ = √(μ/ε) (relative)

    Reference:
        Part IV, Arts. 781-782: Wave impedance.

    Example:
        >>> result = calc_wave_impedance()
        >>> print(f"|E|/|B| = {result['E_over_B']:.3e} cm/s")
    """
    if epsilon <= 0 or mu <= 0:
        raise ValueError("Permittivity and permeability must be positive")

    # Wave speed
    v = CONST.C / np.sqrt(epsilon * mu)

    # E/B ratio = v
    E_over_B = v

    # Intrinsic impedance (relative)
    Z_relative = np.sqrt(mu / epsilon)

    # E/H ratio in CGS
    # H = B/μ, so E/H = E·μ/B = μ·v = μ·c/√(εμ) = c√(μ/ε)
    E_over_H = CONST.C * Z_relative

    return {
        "E_over_B": E_over_B,
        "E_over_H": E_over_H,
        "wave_speed": v,
        "intrinsic_impedance": Z_relative,
        "permittivity": epsilon,
        "permeability": mu,
    }


@dataclass
class WaveEquationSolver:
    """
    Solver for the electromagnetic wave equation in various geometries.

    Art. 781-785: This class provides numerical and analytical solutions
    to the wave equation for different boundary conditions and media.

    The wave equation:
        ∇²ψ - (1/v²) ∂²ψ/∂t² = 0

    where ψ represents E or B field components.

    Attributes:
        epsilon: Permittivity of medium.
        mu: Permeability of medium.
        conductivity: Conductivity (for lossy media).
    """

    epsilon: float = 1.0
    mu: float = 1.0
    conductivity: float = 0.0

    @maxwell_cite(
        781,
        part=4,
        chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Get wave equation parameters",
    )
    def wave_parameters(self) -> dict:
        """Get wave equation parameters for this medium."""
        return derive_wave_equation(self.epsilon, self.mu, self.conductivity)

    @maxwell_cite(
        783,
        784,
        part=4,
        chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate plane wave field",
    )
    def plane_wave(
        self,
        frequency: float,
        E_amplitude: float,
        position: np.ndarray,
        time: float,
        propagation: np.ndarray = None,
        polarization: np.ndarray = None,
    ) -> dict:
        """Calculate plane wave fields at position and time."""
        wave = ElectromagneticWave.from_frequency(
            frequency=frequency,
            E_amplitude=E_amplitude,
            propagation_direction=propagation,
            polarization=polarization,
            epsilon=self.epsilon,
            mu=self.mu,
        )
        return calc_wave_equation_3d(wave, position, time)

    @maxwell_cite(
        785,
        part=4,
        chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Get wave speed in medium",
    )
    def wave_speed(self) -> float:
        """Calculate wave speed in this medium."""
        return calc_wave_speed(self.epsilon, self.mu)["wave_speed"]

    @maxwell_cite(
        781,
        782,
        part=4,
        chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Get wave impedance",
    )
    def impedance(self) -> dict:
        """Calculate wave impedance of this medium."""
        return calc_wave_impedance(self.epsilon, self.mu)


__all__ = [
    # Data class
    "ElectromagneticWave",
    # Wave equation functions
    "derive_wave_equation",
    "calc_wave_equation_3d",
    "calc_wave_speed",
    "calc_wave_impedance",
    "verify_wave_equation",
    # Solver class
    "WaveEquationSolver",
]

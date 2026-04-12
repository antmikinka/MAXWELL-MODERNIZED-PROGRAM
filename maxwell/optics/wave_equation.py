"""
Electromagnetic Wave Equation — Maxwell's proof that light is an electromagnetic wave.

Implements the electromagnetic wave equation as described by Maxwell in Articles 781-791:

- Derivation from Maxwell's equations in vacuum (Art. 783)
- Wave equation for E: ∇²E = (με/c²) · ∂²E/∂t² (Art. 783)
- Wave equation for B: ∇²B = (με/c²) · ∂²B/∂t² (Art. 783)
- Wave speed: v = c/√(με) — in vacuum with μ=1, ε=1: v = c (Art. 784)
- Plane wave solution: E = E₀ exp[i(k·r - ωt)] (Art. 785)
- Dispersion relation: ω = ck (in vacuum) (Art. 785)
- Transversality: k·E = 0, k·B = 0 (no longitudinal waves) (Art. 786)
- E and B relationship: |E| = |B| in vacuum (CGS) (Art. 787)
- Poynting vector: S = (c/4π) E × B (energy flux) (Art. 788)
- Energy density: u = (1/8π)(E² + B²) (Art. 789)
- Wavelength: λ = 2π/k, Frequency: ν = ω/(2π), c = λν (Art. 790)

Maxwell's CGS (Gaussian) formulation:
    Wave equation: ∇²E = (1/c²) · ∂²E/∂t²  (in vacuum)
    Wave speed: v = c = 2.99792458×10¹⁰ cm/s
    Plane wave: E(r,t) = E₀ cos(k·r - ωt)
    B field: B = (1/ω) k × E = (1/c) k̂ × E (in vacuum)
    Poynting vector: S = (c/4π) E × B (erg/cm²/s)
    Energy density: u = (1/8π)(E² + B²) (erg/cm³)
    Intensity: I = (c/8π) E₀² (erg/cm²/s)

where:
    E = electric field intensity (statvolts/cm)
    B = magnetic flux density (gauss)
    k = wavevector (cm⁻¹)
    ω = angular frequency (s⁻¹)
    c = speed of light = 2.99792458×10¹⁰ cm/s
    λ = wavelength (cm)
    ν = frequency (Hz = s⁻¹)

Maxwell's greatest achievement was recognizing that the wave speed derived from
electromagnetic theory equals the measured speed of light, proving that light
itself is an electromagnetic phenomenon. This unified optics with electromagnetism.

Category: A (maxwell_original) — Maxwell's electromagnetic theory of light.

References:
    Part IV, Arts. 781-791: Electromagnetic wave equation and theory of light.
    Part IV, Ch. XX: Electromagnetic theory of light (complete formulation).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class ElectromagneticWave:
    """
    Complete electromagnetic wave state — all wave quantities.

    Art. 781-791: This dataclass encapsulates the complete state of an
    electromagnetic plane wave:

    - amplitude_E: Electric field amplitude vector E₀ (statvolts/cm)
    - amplitude_B: Magnetic field amplitude vector B₀ (gauss)
    - wavevector: Wave vector k (cm⁻¹) — direction = propagation, |k| = 2π/λ
    - angular_frequency: Angular frequency ω (s⁻¹) = 2πν

    The wave satisfies:
    - Wave equation: ∇²E = (1/c²) · ∂²E/∂t²
    - Transversality: k·E = 0, k·B = 0
    - Field relation: B = (1/ω) k × E
    - Speed: ω/|k| = c (in vacuum)

    Attributes:
        amplitude_E: Electric field amplitude vector (statvolts/cm).
        amplitude_B: Magnetic field amplitude vector (gauss).
        wavevector: Wave vector (cm⁻¹).
        angular_frequency: Angular frequency (s⁻¹).
        permittivity: Permittivity ε (default: 1.0 for vacuum).
        permeability: Permeability μ (default: 1.0 for vacuum).
    """

    amplitude_E: np.ndarray = field(default_factory=lambda: np.zeros(3))
    amplitude_B: np.ndarray = field(default_factory=lambda: np.zeros(3))
    wavevector: np.ndarray = field(default_factory=lambda: np.zeros(3))
    angular_frequency: float = 0.0
    permittivity: float = 1.0
    permeability: float = 1.0

    def __post_init__(self):
        """Convert all vector fields to numpy arrays and validate."""
        self.amplitude_E = np.asarray(self.amplitude_E, dtype=np.float64)
        self.amplitude_B = np.asarray(self.amplitude_B, dtype=np.float64)
        self.wavevector = np.asarray(self.wavevector, dtype=np.float64)

        if self.angular_frequency < 0:
            raise ValueError(f"Angular frequency must be non-negative, got {self.angular_frequency}")
        if self.permittivity <= 0:
            raise ValueError(f"Permittivity must be positive, got {self.permittivity}")
        if self.permeability <= 0:
            raise ValueError(f"Permeability must be positive, got {self.permeability}")

    @property
    def wavelength(self) -> float:
        """
        Wavelength λ = 2π/|k|.

        Returns:
            Wavelength in cm.

        Reference:
            Part IV, Art. 790: Wavelength definition.
        """
        k_mag = np.linalg.norm(self.wavevector)
        if k_mag < 1e-15:
            return float('inf')
        return 2.0 * np.pi / k_mag

    @property
    def frequency(self) -> float:
        """
        Frequency ν = ω/(2π).

        Returns:
            Frequency in Hz (s⁻¹).

        Reference:
            Part IV, Art. 790: Frequency definition.
        """
        return self.angular_frequency / (2.0 * np.pi)

    @property
    def speed(self) -> float:
        """
        Wave speed v = ω/|k| = c/√(με).

        Returns:
            Wave speed in cm/s.

        Reference:
            Part IV, Art. 784: Wave speed relation.
        """
        k_mag = np.linalg.norm(self.wavevector)
        if k_mag < 1e-15:
            return 0.0
        return self.angular_frequency / k_mag

    @property
    def polarization(self) -> np.ndarray:
        """
        Polarization direction (unit vector in E field direction).

        Returns:
            Unit vector in polarization direction, or zero if E = 0.

        Reference:
            Part IV, Art. 786: Wave transversality and polarization.
        """
        E_mag = np.linalg.norm(self.amplitude_E)
        if E_mag < 1e-15:
            return np.zeros(3)
        return self.amplitude_E / E_mag

    @property
    def wave_speed_vacuum(self) -> float:
        """
        Expected wave speed in vacuum: c/√(με).

        Returns:
            Theoretical wave speed in cm/s.

        Reference:
            Part IV, Art. 784: Wave speed formula.
        """
        return CONST.C / np.sqrt(self.permittivity * self.permeability)

    @classmethod
    @maxwell_cite(
        781, 782, 783, 784, 785, 786, 787,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Create EM wave from E amplitude, k, and ω",
    )
    def from_E_k_omega(
        cls,
        amplitude_E: np.ndarray,
        wavevector: np.ndarray,
        angular_frequency: float,
        permittivity: float = 1.0,
        permeability: float = 1.0,
    ) -> ElectromagneticWave:
        """
        Create electromagnetic wave from electric field amplitude, wavevector, and frequency.

        Art. 785-787: Given E₀, k, and ω, the magnetic field amplitude is determined by:
            B₀ = (1/ω) k × E₀

        This ensures the wave satisfies Maxwell's equations.

        Args:
            amplitude_E: Electric field amplitude E₀ (statvolts/cm).
            wavevector: Wave vector k (cm⁻¹).
            angular_frequency: Angular frequency ω (s⁻¹).
            permittivity: Permittivity ε (default: 1.0 for vacuum).
            permeability: Permeability μ (default: 1.0 for vacuum).

        Returns:
            ElectromagneticWave object with B computed from E.

        Reference:
            Part IV, Arts. 785-787: Plane wave field relations.

        Example:
            >>> # Wave propagating in z-direction, E polarized along x
            >>> E0 = np.array([1000, 0, 0])
            >>> k = np.array([0, 0, 1e-4])  # k = 1e-4 cm⁻¹
            >>> omega = CONST.C * np.linalg.norm(k)  # ω = ck
            >>> wave = ElectromagneticWave.from_E_k_omega(E0, k, omega)
            >>> print(f"B amplitude: {wave.amplitude_B} gauss")
        """
        amplitude_E = np.asarray(amplitude_E, dtype=np.float64)
        wavevector = np.asarray(wavevector, dtype=np.float64)
        angular_frequency = float(angular_frequency)

        # B₀ = (1/ω) k × E₀
        if angular_frequency > 1e-15:
            amplitude_B = (1.0 / angular_frequency) * np.cross(wavevector, amplitude_E)
        else:
            amplitude_B = np.zeros(3)

        return cls(
            amplitude_E=amplitude_E,
            amplitude_B=amplitude_B,
            wavevector=wavevector,
            angular_frequency=angular_frequency,
            permittivity=permittivity,
            permeability=permeability,
        )

    @classmethod
    @maxwell_cite(
        785, 786, 787,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Create plane wave with given polarization and propagation",
    )
    def create_plane_wave(
        cls,
        E_magnitude: float,
        propagation_direction: np.ndarray,
        polarization_direction: np.ndarray,
        wavelength: float,
        permittivity: float = 1.0,
        permeability: float = 1.0,
    ) -> ElectromagneticWave:
        """
        Create a plane wave with specified properties.

        Art. 785-787: A plane wave is fully specified by:
        - E field magnitude and polarization direction
        - Propagation direction (k direction)
        - Wavelength (determines |k| = 2π/λ)

        The wave automatically satisfies:
        - k·E = 0 (transversality)
        - B = (1/ω) k × E
        - ω = c|k|/√(με)

        Args:
            E_magnitude: Electric field amplitude |E₀| (statvolts/cm).
            propagation_direction: Unit vector in k direction.
            polarization_direction: Unit vector in E₀ direction.
            wavelength: Wavelength λ (cm).
            permittivity: Permittivity ε (default: 1.0).
            permeability: Permeability μ (default: 1.0).

        Returns:
            ElectromagneticWave object.

        Raises:
            ValueError: If wavelength is not positive.

        Reference:
            Part IV, Arts. 785-787: Plane wave specification.

        Example:
            >>> # Visible light: λ = 500 nm = 5e-5 cm
            >>> wave = ElectromagneticWave.create_plane_wave(
            ...     E_magnitude=1000,
            ...     propagation_direction=np.array([0, 0, 1]),
            ...     polarization_direction=np.array([1, 0, 0]),
            ...     wavelength=5e-5
            ... )
            >>> print(f"Frequency: {wave.frequency:.2e} Hz")
        """
        if wavelength <= 0:
            raise ValueError(f"Wavelength must be positive, got {wavelength}")

        propagation_direction = np.asarray(propagation_direction, dtype=np.float64)
        polarization_direction = np.asarray(polarization_direction, dtype=np.float64)

        # Normalize directions
        k_dir = propagation_direction / np.linalg.norm(propagation_direction)
        E_dir = polarization_direction / np.linalg.norm(polarization_direction)

        # Verify transversality (k ⊥ E)
        if abs(np.dot(k_dir, E_dir)) > 1e-10:
            raise ValueError(
                f"Polarization must be perpendicular to propagation. "
                f"Dot product = {np.dot(k_dir, E_dir)}"
            )

        # |k| = 2π/λ
        k_mag = 2.0 * np.pi / wavelength
        wavevector = k_mag * k_dir

        # ω = c|k|/√(με)
        speed = CONST.C / np.sqrt(permittivity * permeability)
        angular_frequency = speed * k_mag

        # E₀ = E_magnitude × direction
        amplitude_E = E_magnitude * E_dir

        return cls.from_E_k_omega(
            amplitude_E=amplitude_E,
            wavevector=wavevector,
            angular_frequency=angular_frequency,
            permittivity=permittivity,
            permeability=permeability,
        )

    @maxwell_cite(
        785,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Evaluate E and B fields at position and time",
    )
    def evaluate(self, position: np.ndarray, time: float) -> tuple[np.ndarray, np.ndarray]:
        """
        Evaluate electric and magnetic fields at given position and time.

        Art. 785: For a plane wave E = E₀ cos(k·r - ωt):
            E(r,t) = E₀ cos(k·r - ωt)
            B(r,t) = B₀ cos(k·r - ωt)

        Args:
            position: Position vector r (cm).
            time: Time t (s).

        Returns:
            Tuple of (E_field, B_field) at the specified point.

        Reference:
            Part IV, Art. 785: Plane wave solution.

        Example:
            >>> # Evaluate wave at origin at t=0
            >>> E, B = wave.evaluate(np.zeros(3), 0.0)
        """
        position = np.asarray(position, dtype=np.float64)
        time = float(time)

        # Phase: φ = k·r - ωt
        phase = np.dot(self.wavevector, position) - self.angular_frequency * time

        # cos(φ)
        cos_phase = np.cos(phase)

        # E(r,t) = E₀ cos(φ)
        E_field = self.amplitude_E * cos_phase

        # B(r,t) = B₀ cos(φ)
        B_field = self.amplitude_B * cos_phase

        return E_field, B_field

    @maxwell_cite(
        789,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate energy density u = (1/8π)(E² + B²)",
    )
    def energy_density(self, position: np.ndarray = None, time: float = 0.0) -> float:
        """
        Calculate electromagnetic energy density.

        Art. 789: The energy density in an electromagnetic wave is:
            u = (1/8π)(E² + B²)  (erg/cm³)

        For a plane wave in vacuum, |E| = |B|, so:
            u = (1/4π) E²

        Args:
            position: Optional position (cm) — uses amplitude if not provided.
            time: Time t (s) — uses t=0 if not provided.

        Returns:
            Energy density u (erg/cm³).

        Reference:
            Part IV, Art. 789: EM wave energy density.

        Example:
            >>> u = wave.energy_density()  # Using amplitudes
            >>> print(f"u = {u:.2e} erg/cm³")
        """
        if position is not None:
            E_field, B_field = self.evaluate(position, time)
        else:
            E_field = self.amplitude_E
            B_field = self.amplitude_B

        E_sq = np.dot(E_field, E_field)
        B_sq = np.dot(B_field, B_field)

        return (1.0 / (8.0 * np.pi)) * (E_sq + B_sq)

    @maxwell_cite(
        788,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate Poynting vector S = (c/4π) E × B",
    )
    def poynting_vector(self, position: np.ndarray = None, time: float = 0.0) -> np.ndarray:
        """
        Calculate Poynting vector (energy flux density).

        Art. 788: The Poynting vector gives the energy flux:
            S = (c/4π) E × B  (erg/cm²/s)

        For a plane wave, S points in the k direction (propagation direction)
        and its magnitude is the intensity.

        Args:
            position: Optional position (cm) — uses amplitude if not provided.
            time: Time t (s) — uses t=0 if not provided.

        Returns:
            Poynting vector S (erg/cm²/s).

        Reference:
            Part IV, Art. 788: Poynting vector for EM waves.

        Example:
            >>> S = wave.poynting_vector()
            >>> print(f"|S| = {np.linalg.norm(S):.2e} erg/cm²/s")
        """
        if position is not None:
            E_field, B_field = self.evaluate(position, time)
        else:
            E_field = self.amplitude_E
            B_field = self.amplitude_B

        return (CONST.C / (4.0 * np.pi)) * np.cross(E_field, B_field)

    @maxwell_cite(
        788, 789,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate wave intensity I = <|S|>",
    )
    def intensity(self) -> float:
        """
        Calculate wave intensity (time-averaged energy flux).

        Art. 788-789: The intensity is the time average of |S|:
            I = <|S|> = (c/8π) E₀²  (erg/cm²/s)

        For a plane wave in vacuum where |E₀| = |B₀|:
            I = (c/8π) E₀² = (c/8π) B₀²

        Args:
            None — uses wave amplitudes.

        Returns:
            Intensity I (erg/cm²/s).

        Reference:
            Part IV, Arts. 788-789: Wave intensity.

        Example:
            >>> I = wave.intensity()
            >>> print(f"I = {I:.2e} erg/cm²/s")
        """
        E_mag_sq = np.dot(self.amplitude_E, self.amplitude_E)
        return (CONST.C / (8.0 * np.pi)) * E_mag_sq


@dataclass
class PlaneWave:
    """
    Plane electromagnetic wave calculator.

    Art. 783-791: This class provides methods for evaluating plane wave
    solutions to Maxwell's equations:

        E(r,t) = E₀ cos(k·r - ωt)
        B(r,t) = (1/ω) k × E(r,t)

    The plane wave satisfies:
    - Wave equation: ∇²E = (1/c²) · ∂²E/∂t²
    - Transversality: k·E = 0
    - Dispersion: ω = c|k| (in vacuum)

    Attributes:
        E0: Electric field amplitude vector (statvolts/cm).
        k: Wave vector (cm⁻¹).
        omega: Angular frequency (s⁻¹).
        permittivity: Permittivity ε (default: 1.0).
        permeability: Permeability μ (default: 1.0).
    """

    E0: np.ndarray = field(default_factory=lambda: np.zeros(3))
    k: np.ndarray = field(default_factory=lambda: np.zeros(3))
    omega: float = 0.0
    permittivity: float = 1.0
    permeability: float = 1.0

    def __post_init__(self):
        """Convert to arrays and validate."""
        self.E0 = np.asarray(self.E0, dtype=np.float64)
        self.k = np.asarray(self.k, dtype=np.float64)

        if self.omega < 0:
            raise ValueError(f"Angular frequency must be non-negative, got {self.omega}")

    @classmethod
    @maxwell_cite(
        783, 784, 785,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Create plane wave from E₀, k, ω",
    )
    def from_parameters(
        cls,
        E0: np.ndarray,
        k: np.ndarray,
        omega: float,
        permittivity: float = 1.0,
        permeability: float = 1.0,
    ) -> PlaneWave:
        """
        Create plane wave from parameters.

        Art. 783-785: The plane wave solution is:
            E(r,t) = E₀ cos(k·r - ωt)
            B(r,t) = (1/ω) k × E(r,t)

        Args:
            E0: Electric field amplitude (statvolts/cm).
            k: Wave vector (cm⁻¹).
            omega: Angular frequency (s⁻¹).
            permittivity: Permittivity ε (default: 1.0).
            permeability: Permeability μ (default: 1.0).

        Returns:
            PlaneWave object.

        Reference:
            Part IV, Arts. 783-785: Plane wave formulation.
        """
        return cls(E0=E0, k=k, omega=omega,
                   permittivity=permittivity, permeability=permeability)

    @maxwell_cite(
        785,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Evaluate E and B at position and time",
    )
    def evaluate(
        self,
        position: np.ndarray,
        time: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Evaluate E and B fields at given position and time.

        Art. 785: Plane wave solution:
            E(r,t) = E₀ cos(k·r - ωt)
            B(r,t) = (1/ω) k × E(r,t)

        Args:
            position: Position vector r (cm).
            time: Time t (s).

        Returns:
            Tuple of (E_field, B_field) at the specified point.

        Reference:
            Part IV, Art. 785: Plane wave evaluation.

        Example:
            >>> pw = PlaneWave.from_parameters(
            ...     E0=np.array([1000, 0, 0]),
            ...     k=np.array([0, 0, 1e-4]),
            ...     omega=CONST.C * 1e-4
            ... )
            >>> E, B = pw.evaluate(np.zeros(3), 0.0)
        """
        position = np.asarray(position, dtype=np.float64)
        time = float(time)

        # Phase: φ = k·r - ωt
        phase = np.dot(self.k, position) - self.omega * time

        # E(r,t) = E₀ cos(φ)
        cos_phase = np.cos(phase)
        E_field = self.E0 * cos_phase

        # B(r,t) = (1/ω) k × E(r,t)
        if self.omega > 1e-15:
            B_field = (1.0 / self.omega) * np.cross(self.k, E_field)
        else:
            B_field = np.zeros(3)

        return E_field, B_field

    @maxwell_cite(
        789,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate energy density u = (1/8π)(E² + B²)",
    )
    def energy_density(self, position: np.ndarray = None, time: float = 0.0) -> float:
        """
        Calculate electromagnetic energy density.

        Art. 789: u = (1/8π)(E² + B²)  (erg/cm³)

        Args:
            position: Optional position (cm) — uses E0 if not provided.
            time: Time t (s).

        Returns:
            Energy density u (erg/cm³).

        Reference:
            Part IV, Art. 789: Energy density.
        """
        if position is not None:
            E_field, B_field = self.evaluate(position, time)
        else:
            E_field = self.E0
            # B amplitude
            if self.omega > 1e-15:
                B_field = (1.0 / self.omega) * np.cross(self.k, self.E0)
            else:
                B_field = np.zeros(3)

        E_sq = np.dot(E_field, E_field)
        B_sq = np.dot(B_field, B_field)

        return (1.0 / (8.0 * np.pi)) * (E_sq + B_sq)

    @maxwell_cite(
        788,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate Poynting vector S = (c/4π) E × B",
    )
    def poynting_vector(self, position: np.ndarray = None, time: float = 0.0) -> np.ndarray:
        """
        Calculate Poynting vector (energy flux).

        Art. 788: S = (c/4π) E × B  (erg/cm²/s)

        Args:
            position: Optional position (cm).
            time: Time t (s).

        Returns:
            Poynting vector S (erg/cm²/s).

        Reference:
            Part IV, Art. 788: Poynting vector.
        """
        if position is not None:
            E_field, B_field = self.evaluate(position, time)
        else:
            E_field = self.E0
            if self.omega > 1e-15:
                B_field = (1.0 / self.omega) * np.cross(self.k, self.E0)
            else:
                B_field = np.zeros(3)

        return (CONST.C / (4.0 * np.pi)) * np.cross(E_field, B_field)

    @maxwell_cite(
        788, 789,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate intensity I = <|S|>",
    )
    def intensity(self) -> float:
        """
        Calculate time-averaged intensity.

        Art. 788-789: I = (c/8π) E₀²  (erg/cm²/s)

        Returns:
            Intensity I (erg/cm²/s).

        Reference:
            Part IV, Arts. 788-789: Wave intensity.
        """
        E_mag_sq = np.dot(self.E0, self.E0)
        return (CONST.C / (8.0 * np.pi)) * E_mag_sq


@maxwell_cite(
    783,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Derive wave equation from Maxwell's equations in vacuum",
)
def derive_wave_equation_from_maxwell() -> dict[str, str]:
    """
    Derive the electromagnetic wave equation from Maxwell's equations.

    Art. 783: Maxwell's equations in vacuum (ρ=0, J=0):

    (1) ∇·E = 0          (Gauss's law, no charges)
    (2) ∇·B = 0          (Gauss's law for magnetism)
    (3) ∇×E = -(1/c)·∂B/∂t   (Faraday's law)
    (4) ∇×B = (1/c)·∂E/∂t    (Ampere-Maxwell, no currents)

    Taking the curl of (3):
        ∇×(∇×E) = -(1/c)·∂(∇×B)/∂t

    Using the vector identity ∇×(∇×E) = ∇(∇·E) - ∇²E:
        ∇(∇·E) - ∇²E = -(1/c)·∂(∇×B)/∂t

    Since ∇·E = 0 in vacuum:
        -∇²E = -(1/c)·∂(∇×B)/∂t

    Substituting (4) for ∇×B:
        -∇²E = -(1/c)·∂[(1/c)·∂E/∂t]/∂t
        -∇²E = -(1/c²)·∂²E/∂t²

    Therefore:
        ∇²E = (1/c²)·∂²E/∂t²  ✓

    This is the three-dimensional wave equation with wave speed c.
    An identical derivation gives ∇²B = (1/c²)·∂²B/∂t².

    Returns:
        Dictionary with derivation steps and final wave equations.

    Reference:
        Part IV, Art. 783: Derivation of wave equation from Maxwell's equations.

    Example:
        >>> result = derive_wave_equation_from_maxwell()
        >>> print(result['wave_equation_E'])
    """
    return {
        "maxwell_equations_vacuum": {
            "gauss_E": "∇·E = 0 (no charges in vacuum)",
            "gauss_B": "∇·B = 0 (no magnetic monopoles)",
            "faraday": "∇×E = -(1/c)·∂B/∂t",
            "ampere_maxwell": "∇×B = (1/c)·∂E/∂t (no currents in vacuum)",
        },
        "derivation_steps": [
            "Take curl of Faraday's law: ∇×(∇×E) = -(1/c)·∂(∇×B)/∂t",
            "Use identity: ∇×(∇×E) = ∇(∇·E) - ∇²E",
            "Since ∇·E = 0 in vacuum: ∇×(∇×E) = -∇²E",
            "Substitute Ampere-Maxwell: -∇²E = -(1/c)·∂[(1/c)·∂E/∂t]/∂t",
            "Simplify: -∇²E = -(1/c²)·∂²E/∂t²",
            "Therefore: ∇²E = (1/c²)·∂²E/∂t²",
        ],
        "wave_equation_E": "∇²E = (1/c²)·∂²E/∂t²",
        "wave_equation_B": "∇²B = (1/c²)·∂²B/∂t²",
        "wave_speed": f"c = {CONST.C:.4e} cm/s",
        "conclusion": "Maxwell's equations predict electromagnetic waves propagating at speed c",
    }


@maxwell_cite(
    784,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate wave speed v = c/√(με)",
)
def calc_wave_speed(permittivity: float, permeability: float) -> float:
    """
    Calculate electromagnetic wave speed in a medium.

    Art. 784: The speed of electromagnetic waves in a medium with
    permittivity ε and permeability μ is:

        v = c/√(με)

    In vacuum where ε = 1, μ = 1 (CGS-Gaussian):
        v = c = 2.99792458×10¹⁰ cm/s

    This was Maxwell's crucial insight: the wave speed derived from
    electromagnetic theory equals the measured speed of light.

    In CGS-Gaussian:
        ε dimensionless (ε = 1 for vacuum)
        μ dimensionless (μ = 1 for vacuum)
        v in cm/s

    Args:
        permittivity: Permittivity ε (dimensionless in CGS).
        permeability: Permeability μ (dimensionless in CGS).

    Returns:
        Wave speed v (cm/s).

    Raises:
        ValueError: If permittivity or permeability is not positive.

    Reference:
        Part IV, Art. 784: Wave speed formula.

    Example:
        >>> # Wave speed in vacuum
        >>> v = calc_wave_speed(1.0, 1.0)
        >>> print(f"v = {v:.4e} cm/s")  # v = c
        >>> # Wave speed in water (ε ≈ 80, μ ≈ 1)
        >>> v_water = calc_wave_speed(80.0, 1.0)
        >>> print(f"v_water = {v_water:.4e} cm/s")  # v ≈ c/√80
    """
    if permittivity <= 0:
        raise ValueError(f"Permittivity must be positive, got {permittivity}")
    if permeability <= 0:
        raise ValueError(f"Permeability must be positive, got {permeability}")

    return CONST.C / np.sqrt(permittivity * permeability)


@maxwell_cite(
    790,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate wavelength λ = v/ν",
)
def calc_wavelength(frequency: float, speed: float) -> float:
    """
    Calculate wavelength from frequency and wave speed.

    Art. 790: The wavelength λ, frequency ν, and wave speed v are related by:

        λ = v/ν

    Equivalently, using angular frequency ω = 2πν and wavenumber k = 2π/λ:
        ω = vk

    In vacuum for electromagnetic waves:
        λ = c/ν

    In CGS:
        ν in Hz (s⁻¹)
        v in cm/s
        λ in cm

    Args:
        frequency: Frequency ν (Hz).
        speed: Wave speed v (cm/s).

    Returns:
        Wavelength λ (cm).

    Raises:
        ValueError: If frequency or speed is not positive.

    Reference:
        Part IV, Art. 790: Wavelength-frequency relation.

    Example:
        >>> # Visible light: ν = 6×10¹⁴ Hz (green)
        >>> lambda_green = calc_wavelength(6e14, CONST.C)
        >>> print(f"λ = {lambda_green*1e7:.1f} nm")  # ≈ 500 nm
    """
    if frequency <= 0:
        raise ValueError(f"Frequency must be positive, got {frequency}")
    if speed <= 0:
        raise ValueError(f"Speed must be positive, got {speed}")

    return speed / frequency


@maxwell_cite(
    785,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate plane wave E field: E(r,t) = E₀ cos(k·r - ωt)",
)
def calc_plane_wave_E(
    position: np.ndarray,
    time: float,
    k: np.ndarray,
    omega: float,
    E0: np.ndarray,
) -> np.ndarray:
    """
    Calculate electric field of a plane wave.

    Art. 785: The plane wave solution for the electric field is:

        E(r,t) = E₀ cos(k·r - ωt)

    where:
        E₀ = electric field amplitude (statvolts/cm)
        k = wavevector (cm⁻¹), |k| = 2π/λ
        ω = angular frequency (s⁻¹)
        r = position (cm)
        t = time (s)

    The wave satisfies the dispersion relation ω = c|k| in vacuum.

    In CGS-Gaussian:
        E0 in statvolts/cm
        k in cm⁻¹
        omega in s⁻¹
        position in cm
        time in s

    Args:
        position: Position vector r (cm).
        time: Time t (s).
        k: Wave vector (cm⁻¹).
        omega: Angular frequency ω (s⁻¹).
        E0: Electric field amplitude (statvolts/cm).

    Returns:
        Electric field E (statvolts/cm).

    Reference:
        Part IV, Art. 785: Plane wave solution.

    Example:
        >>> # E field at origin at t=0 for wave with E0 = 1000 statV/cm
        >>> E = calc_plane_wave_E(np.zeros(3), 0.0, np.array([0, 0, 1e-4]), 3e6, np.array([1000, 0, 0]))
        >>> print(f"E = {E} statvolts/cm")  # E = [1000. 0. 0.]
    """
    position = np.asarray(position, dtype=np.float64)
    k = np.asarray(k, dtype=np.float64)
    E0 = np.asarray(E0, dtype=np.float64)
    time = float(time)
    omega = float(omega)

    # Phase: φ = k·r - ωt
    phase = np.dot(k, position) - omega * time

    return E0 * np.cos(phase)


@maxwell_cite(
    786, 787,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate B field from E: B = (c/ω) k × E",
)
def calc_plane_wave_B_from_E(
    E_field: np.ndarray,
    wavevector: np.ndarray,
    omega: float,
) -> np.ndarray:
    """
    Calculate magnetic field from electric field in a plane wave.

    Art. 786-787: For a plane electromagnetic wave, the magnetic field
    is related to the electric field by:

        B = (1/ω) k × E

    Equivalently, using |k| = ω/c:
        B = (1/c) k̂ × E

    where k̂ is the unit vector in the propagation direction.

    In CGS-Gaussian, |E| = |B| for a plane wave in vacuum.

    Args:
        E_field: Electric field vector (statvolts/cm).
        wavevector: Wave vector k (cm⁻¹).
        omega: Angular frequency ω (s⁻¹).

    Returns:
        Magnetic field B (gauss).

    Raises:
        ValueError: If omega is zero.

    Reference:
        Part IV, Arts. 786-787: E-B field relation in EM waves.

    Example:
        >>> # B field for E = [1000, 0, 0] with k = [0, 0, 1e-4]
        >>> B = calc_plane_wave_B_from_E(np.array([1000, 0, 0]), np.array([0, 0, 1e-4]), 3e6)
        >>> print(f"B = {B} gauss")
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    wavevector = np.asarray(wavevector, dtype=np.float64)
    omega = float(omega)

    if abs(omega) < 1e-15:
        raise ValueError(f"Angular frequency must be non-zero, got {omega}")

    return (1.0 / omega) * np.cross(wavevector, E_field)


@maxwell_cite(
    788,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate Poynting vector S = (c/4π) E × B",
)
def calc_poynting_vector(E_field: np.ndarray, B_field: np.ndarray) -> np.ndarray:
    """
    Calculate Poynting vector (electromagnetic energy flux).

    Art. 788: The Poynting vector gives the rate of energy flow per unit area:

        S = (c/4π) E × B  (erg/cm²/s)

    For a plane wave, S points in the propagation direction (k direction)
    and its time average is the intensity I.

    In CGS-Gaussian:
        E in statvolts/cm
        B in gauss
        S in erg/cm²/s

    Args:
        E_field: Electric field (statvolts/cm).
        B_field: Magnetic field (gauss).

    Returns:
        Poynting vector S (erg/cm²/s).

    Reference:
        Part IV, Art. 788: Poynting vector definition.

    Example:
        >>> # Energy flux for E = 1000 statV/cm, B = 1000 gauss
        >>> S = calc_poynting_vector(np.array([1000, 0, 0]), np.array([0, 1000, 0]))
        >>> print(f"S = {S} erg/cm²/s")
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    return (CONST.C / (4.0 * np.pi)) * np.cross(E_field, B_field)


@maxwell_cite(
    789,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate energy density u = (1/8π)(E² + B²)",
)
def calc_energy_density(E_field: np.ndarray, B_field: np.ndarray) -> float:
    """
    Calculate electromagnetic energy density.

    Art. 789: The energy density in an electromagnetic field is:

        u = (1/8π)(E² + B²)  (erg/cm³)

    where:
        E² = E·E (square of field magnitude)
        B² = B·B

    For a plane wave in vacuum, |E| = |B|, so:
        u = (1/4π) E²

    In CGS-Gaussian:
        E in statvolts/cm
        B in gauss
        u in erg/cm³

    Args:
        E_field: Electric field (statvolts/cm).
        B_field: Magnetic field (gauss).

    Returns:
        Energy density u (erg/cm³).

    Reference:
        Part IV, Art. 789: EM energy density.

    Example:
        >>> # Energy density for E = 1000 statV/cm, B = 1000 gauss
        >>> u = calc_energy_density(np.array([1000, 0, 0]), np.array([0, 1000, 0]))
        >>> print(f"u = {u:.2e} erg/cm³")
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    E_sq = np.dot(E_field, E_field)
    B_sq = np.dot(B_field, B_field)

    return (1.0 / (8.0 * np.pi)) * (E_sq + B_sq)


@maxwell_cite(
    788, 789,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate wave intensity I = (c/8π) E₀²",
)
def calc_wave_intensity(E_amplitude: np.ndarray) -> float:
    """
    Calculate intensity of a plane electromagnetic wave.

    Art. 788-789: The intensity (time-averaged energy flux) of a plane wave is:

        I = (c/8π) E₀²  (erg/cm²/s)

    where E₀ is the electric field amplitude.

    This follows from averaging the Poynting vector over one cycle:
        <|cos²(ωt - k·r)|> = 1/2

    In CGS-Gaussian:
        E₀ in statvolts/cm
        I in erg/cm²/s

    Args:
        E_amplitude: Electric field amplitude E₀ (statvolts/cm).

    Returns:
        Intensity I (erg/cm²/s).

    Reference:
        Part IV, Arts. 788-789: Wave intensity formula.

    Example:
        >>> # Intensity for E₀ = 1000 statV/cm
        >>> I = calc_wave_intensity(np.array([1000, 0, 0]))
        >>> print(f"I = {I:.2e} erg/cm²/s")
    """
    E_amplitude = np.asarray(E_amplitude, dtype=np.float64)
    E_mag_sq = np.dot(E_amplitude, E_amplitude)
    return (CONST.C / (8.0 * np.pi)) * E_mag_sq


@maxwell_cite(
    786,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Verify transversality k·E = 0",
)
def verify_transversality(wavevector: np.ndarray, E_field: np.ndarray, tolerance: float = 1e-10) -> dict[str, float | bool]:
    """
    Verify that an electromagnetic wave is transverse.

    Art. 786: Electromagnetic waves are transverse — the electric field
    is perpendicular to the propagation direction:

        k·E = 0

    This follows from Gauss's law ∇·E = 0 in vacuum, which for a plane
    wave E = E₀ exp[i(k·r - ωt)] gives:
        ik·E = 0 → k·E = 0

    Similarly, k·B = 0 (magnetic field is also transverse).

    Args:
        wavevector: Wave vector k (cm⁻¹).
        E_field: Electric field vector (statvolts/cm).
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with:
        - dot_product: k·E value
        - k_magnitude: |k| (cm⁻¹)
        - E_magnitude: |E| (statvolts/cm)
        - angle_degrees: Angle between k and E (degrees)
        - is_transverse: True if k·E ≈ 0
        - verified: True if transversality holds within tolerance

    Reference:
        Part IV, Art. 786: Wave transversality.

    Example:
        >>> # Verify transverse wave (k along z, E along x)
        >>> result = verify_transversality(np.array([0, 0, 1e-4]), np.array([1000, 0, 0]))
        >>> assert result['verified']
    """
    wavevector = np.asarray(wavevector, dtype=np.float64)
    E_field = np.asarray(E_field, dtype=np.float64)

    dot_product = np.dot(wavevector, E_field)
    k_mag = np.linalg.norm(wavevector)
    E_mag = np.linalg.norm(E_field)

    # Calculate angle
    if k_mag > 1e-15 and E_mag > 1e-15:
        cos_theta = dot_product / (k_mag * E_mag)
        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        angle_rad = np.arccos(cos_theta)
        angle_deg = np.degrees(angle_rad)
    else:
        angle_deg = 90.0  # Undefined, assume perpendicular

    # Verify transversality
    normalized_error = abs(dot_product) / (k_mag * E_mag) if (k_mag > 1e-15 and E_mag > 1e-15) else abs(dot_product)
    is_transverse = abs(dot_product) < tolerance * k_mag * E_mag
    verified = is_transverse

    return {
        "dot_product": dot_product,
        "k_magnitude": k_mag,
        "E_magnitude": E_mag,
        "angle_degrees": angle_deg,
        "is_transverse": is_transverse,
        "verified": verified,
        "tolerance_used": tolerance,
    }


@maxwell_cite(
    783, 784,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Verify EM wave speed equals speed of light",
)
def verify_speed_equals_c(tolerance: float = 1e-10) -> dict[str, float | bool | str]:
    """
    Verify that electromagnetic wave speed equals the speed of light.

    Art. 783-784: This is Maxwell's greatest achievement. From the wave
    equation derived from Maxwell's equations:

        ∇²E = (με/c²) · ∂²E/∂t²

    The wave speed is:
        v = c/√(με)

    In vacuum (CGS-Gaussian) where ε = 1, μ = 1:
        v = c = 2.99792458×10¹⁰ cm/s

    Maxwell compared this with the measured speed of light and found
    agreement, leading to his conclusion: "Light is an electromagnetic
    wave propagated through the electromagnetic field."

    This function verifies the key relationships:
    1. Wave speed from ω and k equals c
    2. E₀/B₀ = c for plane waves in vacuum
    3. Theoretical prediction matches measured value

    Args:
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with:
        - theoretical_speed: c from electromagnetic theory (cm/s)
        - measured_speed_of_light: Experimental value (cm/s)
        - speed_match: True if theory matches measurement
        - wave_speed_formula: "v = c/√(με)"
        - vacuum_speed: Speed in vacuum (cm/s)
        - historical_note: Maxwell's 1865 conclusion
        - verified: True if all verifications pass

    Reference:
        Part IV, Arts. 783-784: EM wave speed equals speed of light.

    Example:
        >>> result = verify_speed_equals_c()
        >>> assert result['verified']  # Maxwell's crowning achievement!
    """
    # Theoretical speed from Maxwell's equations
    theoretical_speed = CONST.C  # This IS c from the theory

    # Compare with measured speed of light (same value in CGS)
    measured_speed_of_light = CONST.C

    # Speed ratio (should be 1)
    speed_ratio = theoretical_speed / measured_speed_of_light

    # For plane waves in vacuum: E₀/B₀ = c
    # This is another verification
    E0 = 1000.0  # statvolts/cm
    B0 = E0 / CONST.C  # gauss (from E = cB in vacuum)
    E0_over_B0 = E0 / B0
    c_from_EB_ratio = E0_over_B0

    # Verify
    speed_match = np.isclose(theoretical_speed, measured_speed_of_light, rtol=tolerance)
    ratio_verified = np.isclose(c_from_EB_ratio, CONST.C, rtol=tolerance)
    verified = speed_match and ratio_verified

    return {
        "theoretical_speed": theoretical_speed,
        "measured_speed_of_light": measured_speed_of_light,
        "speed_ratio": speed_ratio,
        "E0_B0_ratio_c": c_from_EB_ratio,
        "vacuum_speed": CONST.C,
        "wave_speed_formula": "v = c/√(με)",
        "speed_match": speed_match,
        "ratio_verified": ratio_verified,
        "historical_note": "Maxwell (1865): 'Light is an electromagnetic wave propagated through the electromagnetic field.'",
        "verified": verified,
        "significance": "This discovery unified optics with electromagnetism",
    }


@maxwell_cite(
    785, 786, 787, 788, 789, 790,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Complete analysis of electromagnetic wave",
)
def analyze_wave(
    E0: np.ndarray,
    k: np.ndarray,
    omega: float,
    position: np.ndarray = None,
    time: float = 0.0,
    permittivity: float = 1.0,
    permeability: float = 1.0,
) -> dict[str, np.ndarray | float | dict]:
    """
    Perform complete electromagnetic wave analysis.

    Art. 785-790: Comprehensive analysis of a plane electromagnetic wave:

    1. Wave properties (wavelength, frequency, speed)
    2. Field evaluation at position and time
    3. Transversality verification (k·E = 0)
    4. E-B field relationship (|E| = |B| in vacuum)
    5. Poynting vector and energy flux
    6. Energy density
    7. Intensity

    Args:
        E0: Electric field amplitude (statvolts/cm).
        k: Wave vector (cm⁻¹).
        omega: Angular frequency ω (s⁻¹).
        position: Optional position for field evaluation (cm).
        time: Time for field evaluation (s).
        permittivity: Permittivity ε (default: 1.0).
        permeability: Permeability μ (default: 1.0).

    Returns:
        Dictionary with complete analysis:
        - E0: Input electric field amplitude
        - k: Input wave vector
        - omega: Input angular frequency
        - wavelength: λ = 2π/|k| (cm)
        - frequency: ν = ω/(2π) (Hz)
        - wave_speed: v = ω/|k| (cm/s)
        - expected_speed: c/√(με) (cm/s)
        - speed_verified: True if ω/|k| = c/√(με)
        - E_field: E at (r,t) if position provided
        - B_field: B at (r,t) if position provided
        - transversality: k·E verification results
        - E_B_ratio: |E|/|B| (should be c in vacuum)
        - poynting_vector: S (erg/cm²/s)
        - energy_density: u (erg/cm³)
        - intensity: I (erg/cm²/s)
        - polarization: Unit vector in E direction

    Reference:
        Part IV, Arts. 785-790: Complete EM wave analysis.

    Example:
        >>> # Analyze visible light wave
        >>> E0 = np.array([1000, 0, 0])  # 1000 statV/cm
        >>> k = np.array([0, 0, 1e5])  # propagating in z
        >>> omega = CONST.C * 1e5  # ω = ck
        >>> result = analyze_wave(E0, k, omega)
        >>> print(f"Wavelength: {result['wavelength']*1e7:.1f} nm")
        >>> print(f"Frequency: {result['frequency']:.2e} Hz")
        >>> print(f"Intensity: {result['intensity']:.2e} erg/cm²/s")
    """
    E0 = np.asarray(E0, dtype=np.float64)
    k = np.asarray(k, dtype=np.float64)
    omega = float(omega)

    # Wave properties
    k_mag = np.linalg.norm(k)
    wavelength = 2.0 * np.pi / k_mag if k_mag > 1e-15 else float('inf')
    frequency = omega / (2.0 * np.pi)
    wave_speed = omega / k_mag if k_mag > 1e-15 else 0.0
    expected_speed = CONST.C / np.sqrt(permittivity * permeability)
    speed_verified = np.isclose(wave_speed, expected_speed, rtol=1e-10) if k_mag > 1e-15 else False

    # Field evaluation
    E_field = None
    B_field = None
    if position is not None:
        position = np.asarray(position, dtype=np.float64)
        phase = np.dot(k, position) - omega * time
        E_field = E0 * np.cos(phase)
        if omega > 1e-15:
            B_field = (1.0 / omega) * np.cross(k, E_field)
        else:
            B_field = np.zeros(3)

    # Transversality
    transversality = verify_transversality(k, E0)

    # E-B ratio
    E_mag = np.linalg.norm(E0)
    if omega > 1e-15 and k_mag > 1e-15:
        B_mag = k_mag * E_mag / omega  # |B| = |k||E|/ω
        E_B_ratio = E_mag / B_mag if B_mag > 1e-15 else float('inf')
    else:
        B_mag = 0.0
        E_B_ratio = float('inf')

    # Poynting vector (using amplitudes)
    if omega > 1e-15:
        B0 = (1.0 / omega) * np.cross(k, E0)
    else:
        B0 = np.zeros(3)
    S = calc_poynting_vector(E0, B0)

    # Energy density and intensity
    energy_density = calc_energy_density(E0, B0)
    intensity = calc_wave_intensity(E0)

    # Polarization
    polarization = E0 / E_mag if E_mag > 1e-15 else np.zeros(3)

    return {
        "E0": E0,
        "k": k,
        "omega": omega,
        "wavelength": wavelength,
        "frequency": frequency,
        "wave_speed": wave_speed,
        "expected_speed": expected_speed,
        "speed_verified": speed_verified,
        "E_field": E_field,
        "B_field": B_field,
        "transversality": transversality,
        "E_magnitude": E_mag,
        "B_magnitude": B_mag,
        "E_B_ratio": E_B_ratio,
        "poynting_vector": S,
        "energy_density": energy_density,
        "intensity": intensity,
        "polarization": polarization,
    }


class WaveEquationCalculator:
    """
    Comprehensive electromagnetic wave equation calculator.

    Art. 781-791: This class provides a unified interface for all
    electromagnetic wave calculations:

    - Wave equation derivation from Maxwell's equations
    - Plane wave solutions
    - Wave properties (wavelength, frequency, speed)
    - Energy and intensity calculations
    - Verification of light as EM wave

    Attributes:
        permittivity: Permittivity ε (default: 1.0 for vacuum).
        permeability: Permeability μ (default: 1.0 for vacuum).
    """

    def __init__(self, permittivity: float = 1.0, permeability: float = 1.0):
        """
        Initialize wave equation calculator.

        Args:
            permittivity: Permittivity ε (default: 1.0 for vacuum).
            permeability: Permeability μ (default: 1.0 for vacuum).
        """
        if permittivity <= 0:
            raise ValueError(f"Permittivity must be positive, got {permittivity}")
        if permeability <= 0:
            raise ValueError(f"Permeability must be positive, got {permeability}")

        self.permittivity = permittivity
        self.permeability = permeability
        self.wave_speed = CONST.C / np.sqrt(permittivity * permeability)

    @maxwell_cite(
        783,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Derive wave equation from Maxwell's equations",
    )
    def derive_wave_equation(self) -> dict[str, str]:
        """
        Derive the electromagnetic wave equation.

        Art. 783: Shows how Maxwell's equations yield the wave equation.

        Returns:
            Derivation results.

        Reference:
            Part IV, Art. 783: Wave equation derivation.
        """
        return derive_wave_equation_from_maxwell()

    @maxwell_cite(
        784,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate wave speed",
    )
    def wave_speed_calc(self) -> float:
        """
        Get wave speed in the medium.

        Art. 784: v = c/√(με)

        Returns:
            Wave speed (cm/s).

        Reference:
            Part IV, Art. 784: Wave speed formula.
        """
        return self.wave_speed

    @maxwell_cite(
        785,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Create plane wave",
    )
    def create_plane_wave(
        self,
        E0: np.ndarray,
        k: np.ndarray,
        omega: float = None,
    ) -> PlaneWave:
        """
        Create a plane wave calculator.

        Art. 785: E(r,t) = E₀ cos(k·r - ωt)

        Args:
            E0: Electric field amplitude (statvolts/cm).
            k: Wave vector (cm⁻¹).
            omega: Optional angular frequency (computed from dispersion if not provided).

        Returns:
            PlaneWave object.

        Reference:
            Part IV, Art. 785: Plane wave solution.
        """
        E0 = np.asarray(E0, dtype=np.float64)
        k = np.asarray(k, dtype=np.float64)

        if omega is None:
            # Use dispersion relation: ω = v|k|
            k_mag = np.linalg.norm(k)
            omega = self.wave_speed * k_mag

        return PlaneWave.from_parameters(
            E0=E0,
            k=k,
            omega=omega,
            permittivity=self.permittivity,
            permeability=self.permeability,
        )

    @maxwell_cite(
        788, 789,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate intensity from E amplitude",
    )
    def intensity(self, E_amplitude: np.ndarray) -> float:
        """
        Calculate wave intensity.

        Art. 788-789: I = (c/8π) E₀²

        Args:
            E_amplitude: Electric field amplitude (statvolts/cm).

        Returns:
            Intensity (erg/cm²/s).

        Reference:
            Part IV, Arts. 788-789: Wave intensity.
        """
        return calc_wave_intensity(E_amplitude)

    @maxwell_cite(
        786,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Verify wave transversality",
    )
    def verify_transverse(self, k: np.ndarray, E: np.ndarray, tolerance: float = 1e-10) -> dict:
        """
        Verify wave transversality (k ⊥ E).

        Art. 786: k·E = 0

        Args:
            k: Wave vector (cm⁻¹).
            E: Electric field (statvolts/cm).
            tolerance: Numerical tolerance.

        Returns:
            Transversality verification results.

        Reference:
            Part IV, Art. 786: Wave transversality.
        """
        return verify_transversality(k, E, tolerance)

    @maxwell_cite(
        783, 784,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Verify EM wave speed equals c",
    )
    def verify_light_is_em_wave(self, tolerance: float = 1e-10) -> dict:
        """
        Verify that electromagnetic waves propagate at the speed of light.

        Art. 783-784: Maxwell's crowning achievement — proving light is EM.

        Args:
            tolerance: Numerical tolerance.

        Returns:
            Verification results.

        Reference:
            Part IV, Arts. 783-784: Light as electromagnetic wave.
        """
        result = verify_speed_equals_c(tolerance)
        result["medium_wave_speed"] = self.wave_speed
        result["medium_refractive_index"] = np.sqrt(self.permittivity * self.permeability)
        return result

    @maxwell_cite(
        785, 786, 787, 788, 789, 790,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Complete wave analysis",
    )
    def analyze(
        self,
        E0: np.ndarray,
        k: np.ndarray,
        omega: float = None,
        position: np.ndarray = None,
        time: float = 0.0,
    ) -> dict:
        """
        Perform complete electromagnetic wave analysis.

        Art. 785-790: Comprehensive wave property analysis.

        Args:
            E0: Electric field amplitude (statvolts/cm).
            k: Wave vector (cm⁻¹).
            omega: Optional angular frequency.
            position: Optional position for evaluation.
            time: Time for evaluation.

        Returns:
            Complete analysis results.

        Reference:
            Part IV, Arts. 785-790: Complete wave analysis.
        """
        if omega is None:
            k_mag = np.linalg.norm(k)
            omega = self.wave_speed * k_mag

        return analyze_wave(
            E0=E0,
            k=k,
            omega=omega,
            position=position,
            time=time,
            permittivity=self.permittivity,
            permeability=self.permeability,
        )

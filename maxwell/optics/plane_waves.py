"""maxwell.optics.plane_waves — Advanced plane wave theory (Arts. 801-803).

Implements Maxwell's advanced treatment of plane electromagnetic waves,
including polarization states, elliptical polarization, and wave superposition.

Maxwell's CGS formulation (Arts. 801-803):
    General plane wave solution:
        E(r,t) = E₀ cos(k·r - ωt + φ)
        B(r,t) = (1/ω) k × E(r,t)

    Elliptical polarization:
        E_x = E₀x cos(ωt - kz)
        E_y = E₀y cos(ωt - kz + δ)

    Linear polarization: δ = 0 or π
    Circular polarization: E₀x = E₀y, δ = ±π/2

    Wave superposition (interference):
        E_total = E₁ + E₂
        I_total = I₁ + I₂ + 2√(I₁I₂)cos(Δφ)

where:
    E = electric field vector (statvolts/cm)
    B = magnetic field vector (gauss)
    k = wavevector (cm⁻¹)
    ω = angular frequency (s⁻¹)
    φ = phase (radians)
    δ = relative phase between components (radians)
    I = intensity (erg/cm²/s)

Category: A (maxwell_original) — Maxwell's advanced plane wave theory.

References:
    Part IV, Arts. 801-803: Advanced plane electromagnetic waves.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class PolarizationState:
    """
    Polarization state of electromagnetic wave.

    Art. 801-803: Maxwell's treatment of wave polarization including
    linear, circular, and elliptical polarization states.

    Attributes:
        Ex_amplitude: Amplitude of x-component E₀x (statvolts/cm).
        Ey_amplitude: Amplitude of y-component E₀y (statvolts/cm).
        phase_difference: Phase difference δ = φy - φx (radians).
        wavevector_magnitude: |k| (cm⁻¹).
        angular_frequency: ω (s⁻¹).
    """

    Ex_amplitude: float = 1.0
    Ey_amplitude: float = 0.0
    phase_difference: float = 0.0
    wavevector_magnitude: float = 1.0
    angular_frequency: float = CONST.C

    @maxwell_cite(
        801,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Determine polarization type",
    )
    def polarization_type(self) -> str:
        """
        Determine the type of polarization.

        Art. 801: Classification:
        - Linear: δ = 0 or π (or one component is zero)
        - Circular: E₀x = E₀y and δ = ±π/2
        - Elliptical: All other cases

        Returns:
            Polarization type string.

        Reference:
            Part IV, Art. 801: Polarization classification.
        """
        # Check for linear polarization
        if abs(self.Ey_amplitude) < 1e-15 or abs(self.Ex_amplitude) < 1e-15:
            return "linear"

        # Normalize phase to [-π, π]
        delta = np.mod(self.phase_difference + np.pi, 2 * np.pi) - np.pi

        # Check for circular polarization
        amplitude_ratio = self.Ey_amplitude / self.Ex_amplitude if self.Ex_amplitude > 0 else 0
        if abs(amplitude_ratio - 1.0) < 1e-10 and (abs(abs(delta) - np.pi/2) < 1e-10):
            handedness = "right" if delta > 0 else "left"
            return f"circular_{handedness}"

        # Check for linear with both components
        if abs(delta) < 1e-10 or abs(abs(delta) - np.pi) < 1e-10:
            return "linear"

        return "elliptical"

    @maxwell_cite(
        802,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate E field at position and time",
    )
    def electric_field(self, position: np.ndarray, time: float) -> np.ndarray:
        """
        Calculate electric field vector at given position and time.

        Art. 802: For a wave propagating in z-direction:

            E_x = E₀x cos(ωt - kz)
            E_y = E₀y cos(ωt - kz + δ)
            E_z = 0 (transverse wave)

        Args:
            position: Position vector r (cm).
            time: Time t (s).

        Returns:
            Electric field vector E (statvolts/cm).

        Reference:
            Part IV, Art. 802: E field calculation.
        """
        position = np.asarray(position, dtype=np.float64)
        z = position[2] if len(position) > 2 else 0.0

        # Phase: φ = ωt - kz
        phase = self.angular_frequency * time - self.wavevector_magnitude * z

        Ex = self.Ex_amplitude * np.cos(phase)
        Ey = self.Ey_amplitude * np.cos(phase + self.phase_difference)
        Ez = 0.0

        return np.array([Ex, Ey, Ez])

    @maxwell_cite(
        802,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate B field from E field",
    )
    def magnetic_field(self, position: np.ndarray, time: float) -> np.ndarray:
        """
        Calculate magnetic field vector from electric field.

        Art. 802: For a plane wave in vacuum:

            B = (1/c) k̂ × E

        where k̂ is the propagation direction unit vector.

        Args:
            position: Position vector (cm).
            time: Time t (s).

        Returns:
            Magnetic field vector B (gauss).

        Reference:
            Part IV, Art. 802: B field calculation.
        """
        E = self.electric_field(position, time)

        # Wave propagating in z-direction: k̂ = (0, 0, 1)
        # B = (1/c) k̂ × E
        # B_x = -(1/c) E_y
        # B_y = (1/c) E_x
        # B_z = 0

        return np.array([-E[1] / CONST.C, E[0] / CONST.C, 0.0])

    @maxwell_cite(
        803,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate Stokes parameters",
    )
    def stokes_parameters(self) -> Tuple[float, float, float, float]:
        """
        Calculate Stokes parameters for polarization state.

        Art. 803: The Stokes parameters describe polarization:

            I = E₀x² + E₀y²  (total intensity)
            Q = E₀x² - E₀y²  (linear H vs V)
            U = 2E₀xE₀y cos(δ)  (linear +45° vs -45°)
            V = 2E₀xE₀y sin(δ)  (circular R vs L)

        Returns:
            Tuple (I, Q, U, V) of Stokes parameters.

        Reference:
            Part IV, Art. 803: Stokes parameters.
        """
        Ex = self.Ex_amplitude
        Ey = self.Ey_amplitude
        delta = self.phase_difference

        I = Ex ** 2 + Ey ** 2
        Q = Ex ** 2 - Ey ** 2
        U = 2 * Ex * Ey * np.cos(delta)
        V = 2 * Ex * Ey * np.sin(delta)

        return (I, Q, U, V)

    @classmethod
    @maxwell_cite(
        801,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Create linear polarization state",
    )
    def linear_polarization(
        cls,
        amplitude: float,
        angle: float,
        **kwargs
    ) -> PolarizationState:
        """
        Create linear polarization at specified angle.

        Art. 801: Linear polarization at angle θ from x-axis:

            E₀x = E₀ cos(θ)
            E₀y = E₀ sin(θ)
            δ = 0

        Args:
            amplitude: Total amplitude E₀ (statvolts/cm).
            angle: Polarization angle θ (radians from x-axis).
            **kwargs: Additional parameters for PolarizationState.

        Returns:
            PolarizationState with linear polarization.

        Reference:
            Part IV, Art. 801: Linear polarization.
        """
        return cls(
            Ex_amplitude=amplitude * np.cos(angle),
            Ey_amplitude=amplitude * np.sin(angle),
            phase_difference=0.0,
            **kwargs
        )

    @classmethod
    @maxwell_cite(
        801,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Create circular polarization state",
    )
    def circular_polarization(
        cls,
        amplitude: float,
        handedness: str = "right",
        **kwargs
    ) -> PolarizationState:
        """
        Create circular polarization state.

        Art. 801: Circular polarization:

            E₀x = E₀y = E₀/√2
            δ = ±π/2 (right/left)

        Args:
            amplitude: Total amplitude (statvolts/cm).
            handedness: "right" or "left" circular.
            **kwargs: Additional parameters.

        Returns:
            PolarizationState with circular polarization.

        Reference:
            Part IV, Art. 801: Circular polarization.
        """
        amp = amplitude / np.sqrt(2)
        delta = np.pi / 2 if handedness.lower() == "right" else -np.pi / 2

        return cls(
            Ex_amplitude=amp,
            Ey_amplitude=amp,
            phase_difference=delta,
            **kwargs
        )

    @classmethod
    @maxwell_cite(
        801,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Create elliptical polarization state",
    )
    def elliptical_polarization(
        cls,
        Ex_amplitude: float,
        Ey_amplitude: float,
        phase_difference: float,
        **kwargs
    ) -> PolarizationState:
        """
        Create general elliptical polarization state.

        Art. 801: Elliptical polarization is the most general case,
        characterized by two amplitudes and a phase difference.

        Args:
            Ex_amplitude: X-component amplitude (statvolts/cm).
            Ey_amplitude: Y-component amplitude (statvolts/cm).
            phase_difference: Phase δ (radians).
            **kwargs: Additional parameters.

        Returns:
            PolarizationState with elliptical polarization.

        Reference:
            Part IV, Art. 801: Elliptical polarization.
        """
        return cls(
            Ex_amplitude=Ex_amplitude,
            Ey_amplitude=Ey_amplitude,
            phase_difference=phase_difference,
            **kwargs
        )


@maxwell_cite(
    801,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate intensity of polarized wave",
)
def calc_polarized_wave_intensity(
    Ex_amplitude: float,
    Ey_amplitude: float,
) -> float:
    """
    Calculate intensity of polarized electromagnetic wave.

    Art. 801: The intensity is:

        I = (c/8π) (E₀x² + E₀y²) = (c/8π) E₀²

    Args:
        Ex_amplitude: X-component amplitude (statvolts/cm).
        Ey_amplitude: Y-component amplitude (statvolts/cm).

    Returns:
        Intensity I (erg/cm²/s).

    Reference:
        Part IV, Art. 801: Polarized wave intensity.

    Example:
        >>> I = calc_polarized_wave_intensity(1000, 0)
        >>> print(f"I = {I:.2e} erg/cm²/s")
    """
    E_squared = Ex_amplitude ** 2 + Ey_amplitude ** 2
    return (CONST.C / (8.0 * np.pi)) * E_squared


@maxwell_cite(
    803,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate interference of two waves",
)
def calc_wave_interference(
    I1: float,
    I2: float,
    phase_difference: float,
) -> float:
    """
    Calculate intensity from interference of two coherent waves.

    Art. 803: The interference formula is:

        I_total = I₁ + I₂ + 2√(I₁I₂) cos(Δφ)

    Constructive interference: Δφ = 2πn → I_max = I₁ + I₂ + 2√(I₁I₂)
    Destructive interference: Δφ = (2n+1)π → I_min = I₁ + I₂ - 2√(I₁I₂)

    Args:
        I1: Intensity of first wave (erg/cm²/s).
        I2: Intensity of second wave (erg/cm²/s).
        phase_difference: Phase difference Δφ (radians).

    Returns:
        Total intensity I_total (erg/cm²/s).

    Reference:
        Part IV, Art. 803: Wave interference.

    Example:
        >>> # Constructive interference
        >>> I = calc_wave_interference(100, 100, 0)
        >>> print(f"I = {I}")  # I = 400
        >>> # Destructive interference
        >>> I = calc_wave_interference(100, 100, np.pi)
        >>> print(f"I = {I}")  # I = 0
    """
    return I1 + I2 + 2 * np.sqrt(I1 * I2) * np.cos(phase_difference)


@maxwell_cite(
    802,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate polarization ellipse parameters",
)
def calc_polarization_ellipse(
    Ex_amplitude: float,
    Ey_amplitude: float,
    phase_difference: float,
) -> dict[str, float]:
    """
    Calculate parameters of polarization ellipse.

    Art. 802: The polarization ellipse is characterized by:
    - Semi-major axis a
    - Semi-minor axis b
    - Ellipticity ε = b/a
    - Orientation angle ψ

    Args:
        Ex_amplitude: X-component amplitude.
        Ey_amplitude: Y-component amplitude.
        phase_difference: Phase difference δ (radians).

    Returns:
        Dictionary with ellipse parameters:
        - a: Semi-major axis (proportional)
        - b: Semi-minor axis (proportional)
        - ellipticity: b/a
        - orientation: Angle ψ (radians)
        - handedness: "right", "left", or "none"

    Reference:
        Part IV, Art. 802: Polarization ellipse.
    """
    Ex = Ex_amplitude
    Ey = Ey_amplitude
    delta = phase_difference

    # Auxiliary angle α
    tan_alpha = Ey / Ex if Ex > 0 else np.pi / 2
    alpha = np.arctan(tan_alpha)

    # Orientation angle ψ
    denom = Ex ** 2 - Ey ** 2
    tan_2psi = (2 * Ex * Ey * np.cos(delta)) / denom if abs(denom) > 1e-15 else np.inf
    psi = 0.5 * np.arctan(tan_2psi)

    # Ellipticity angle χ
    sin_2chi = (2 * Ex * Ey * np.sin(delta)) / (Ex ** 2 + Ey ** 2)
    sin_2chi = np.clip(sin_2chi, -1, 1)
    chi = 0.5 * np.arcsin(sin_2chi)

    # Ellipticity
    ellipticity = np.tan(chi)

    # Handedness
    if np.sin(delta) > 0:
        handedness = "right"
    elif np.sin(delta) < 0:
        handedness = "left"
    else:
        handedness = "none"  # Linear

    # Normalize axes (proportional to total amplitude)
    total_amp = np.sqrt(Ex ** 2 + Ey ** 2)
    a = total_amp * np.cos(chi)  # Semi-major
    b = total_amp * np.sin(chi)  # Semi-minor

    return {
        "semi_major_axis": a,
        "semi_minor_axis": b,
        "ellipticity": ellipticity,
        "orientation_angle": psi,
        "ellipticity_angle": chi,
        "handedness": handedness,
        "total_amplitude": total_amp,
    }


@maxwell_cite(
    803,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate fringe visibility",
)
def calc_fringe_visibility(
    I_max: float,
    I_min: float,
) -> float:
    """
    Calculate fringe visibility in interference pattern.

    Art. 803: The visibility (contrast) is:

        V = (I_max - I_min) / (I_max + I_min)

    V = 1: Perfect contrast (equal intensities)
    V = 0: No contrast (incoherent or very different intensities)

    Args:
        I_max: Maximum intensity in pattern.
        I_min: Minimum intensity in pattern.

    Returns:
        Visibility V (0 to 1).

    Reference:
        Part IV, Art. 803: Fringe visibility.

    Example:
        >>> V = calc_fringe_visibility(400, 0)
        >>> print(f"V = {V}")  # V = 1 (perfect)
    """
    if I_max + I_min <= 0:
        return 0.0
    return (I_max - I_min) / (I_max + I_min)


@maxwell_cite(
    801, 802, 803,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Verify polarization state relations",
)
def verify_polarization_relations(
    Ex_amplitude: float = 1.0,
    Ey_amplitude: float = 1.0,
    phase_difference: float = np.pi / 2,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify polarization state relationships.

    Art. 801-803: This function verifies:
    1. Stokes parameter relation: I² = Q² + U² + V² (for pure states)
    2. Circular polarization conditions
    3. Linear polarization conditions

    Args:
        Ex_amplitude: X-component amplitude.
        Ey_amplitude: Y-component amplitude.
        phase_difference: Phase difference δ (radians).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 801-803: Polarization verification.
    """
    ps = PolarizationState(
        Ex_amplitude=Ex_amplitude,
        Ey_amplitude=Ey_amplitude,
        phase_difference=phase_difference,
    )

    I, Q, U, V = ps.stokes_parameters()

    # Verify Stokes relation for pure states: I² = Q² + U² + V²
    lhs = I ** 2
    rhs = Q ** 2 + U ** 2 + V ** 2
    stokes_error = abs(lhs - rhs) / lhs if lhs > 0 else 0

    # Verify polarization type classification
    p_type = ps.polarization_type()

    # Check circular conditions
    is_circular = (
        abs(Ex_amplitude - Ey_amplitude) < tolerance * Ex_amplitude and
        abs(abs(phase_difference) - np.pi / 2) < tolerance
    )

    # Check linear conditions
    is_linear = (
        Ey_amplitude < tolerance or
        Ex_amplitude < tolerance or
        abs(phase_difference) < tolerance or
        abs(abs(phase_difference) - np.pi) < tolerance
    )

    return {
        "Ex_amplitude": Ex_amplitude,
        "Ey_amplitude": Ey_amplitude,
        "phase_difference": phase_difference,
        "stokes_I": I,
        "stokes_Q": Q,
        "stokes_U": U,
        "stokes_V": V,
        "stokes_relation_error": stokes_error,
        "polarization_type": p_type,
        "is_circular_condition": is_circular,
        "is_linear_condition": is_linear,
        "stokes_relation_verified": stokes_error < tolerance,
        "verified": stokes_error < tolerance,
    }


@maxwell_cite(
    801, 802, 803,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Complete plane wave polarization analysis",
)
def analyze_plane_wave_polarization(
    Ex_amplitude: float,
    Ey_amplitude: float,
    phase_difference: float,
    wavelength: float = 589e-7,
) -> dict[str, float | str]:
    """
    Complete analysis of plane wave polarization.

    Art. 801-803: Comprehensive analysis including:
    1. Polarization type classification
    2. Stokes parameters
    3. Polarization ellipse parameters
    4. Intensity
    5. Field expressions

    Args:
        Ex_amplitude: X-component amplitude (statvolts/cm).
        Ey_amplitude: Y-component amplitude (statvolts/cm).
        phase_difference: Phase difference δ (radians).
        wavelength: Wavelength λ (cm).

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 801-803: Complete polarization analysis.

    Example:
        >>> # Analyze right-circular polarization
        >>> result = analyze_plane_wave_polarization(1, 1, np.pi/2)
        >>> print(f"Type: {result['polarization_type']}")
        >>> print(f"Ellipticity: {result['ellipticity']}")
    """
    ps = PolarizationState(
        Ex_amplitude=Ex_amplitude,
        Ey_amplitude=Ey_amplitude,
        phase_difference=phase_difference,
        wavevector_magnitude=2 * np.pi / wavelength,
        angular_frequency=2 * np.pi * CONST.C / wavelength,
    )

    I, Q, U, V = ps.stokes_parameters()
    ellipse = calc_polarization_ellipse(Ex_amplitude, Ey_amplitude, phase_difference)
    intensity = calc_polarized_wave_intensity(Ex_amplitude, Ey_amplitude)

    return {
        "Ex_amplitude": Ex_amplitude,
        "Ey_amplitude": Ey_amplitude,
        "phase_difference": phase_difference,
        "phase_difference_degrees": np.degrees(phase_difference),
        "polarization_type": ps.polarization_type(),
        "stokes_I": I,
        "stokes_Q": Q,
        "stokes_U": U,
        "stokes_V": V,
        "degree_of_polarization": np.sqrt(Q ** 2 + U ** 2 + V ** 2) / I if I > 0 else 0,
        "intensity": intensity,
        "wavelength_cm": wavelength,
        "wavelength_nm": wavelength * 1e7,
        **ellipse,
    }

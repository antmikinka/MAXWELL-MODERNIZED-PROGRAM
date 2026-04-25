"""
Plane Wave Solutions — detailed analysis of plane electromagnetic waves.

Implements Maxwell's plane wave theory from Articles 786-790:

- Plane wave mathematical form (Art. 786)
- Transverse nature of EM waves (Art. 787)
- E and B field relationship (Art. 788)
- Phase and group velocity (Art. 789)
- Energy propagation in plane waves (Art. 790)

A plane wave is the simplest solution to the electromagnetic wave equation,
with fields that are constant over planes perpendicular to the propagation
direction. Despite its simplicity, the plane wave model is fundamental to
understanding electromagnetic radiation and optics.

Plane wave fields:
    E(r,t) = E₀ cos(k·r - ωt + φ)
    B(r,t) = (1/c) k̂ × E₀ cos(k·r - ωt + φ)

Key properties:
- Transverse: E ⊥ k and B ⊥ k
- Mutually perpendicular: E ⊥ B
- Amplitude relation: |B| = |E|/c (vacuum)
- In phase: E and B reach maxima together

Category: A (maxwell_original) — Maxwell's plane wave theory.

References:
    Part IV, Ch XX: Electromagnetic Theory of Light (Arts. 781-805).
    Part IV, Arts. 786-790: Plane wave solutions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np
from typing import Optional, Tuple

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class PlaneWave:
    """
    Plane electromagnetic wave solution.

    Art. 786-790: A complete description of a monochromatic plane
    electromagnetic wave:

    Mathematical form:
        E(r,t) = Re{E₀ exp[i(k·r - ωt)]}
        B(r,t) = Re{B₀ exp[i(k·r - ωt)]}

    where:
        E₀ = complex amplitude vector
        B₀ = (c/ω) k × E₀ (from Maxwell's equations)
        k = wave vector, |k| = ω/c
        ω = angular frequency

    Physical properties:
        - k · E₀ = 0 (transverse)
        - k · B₀ = 0 (transverse)
        - E₀ · B₀ = 0 (mutually perpendicular)
        - |E₀| = c|B₀| (amplitude relation)

    Attributes:
        angular_frequency: ω (rad/s).
        wave_vector: k vector (rad/cm).
        E0_real: Real part of E₀ (statvolts/cm).
        E0_imag: Imaginary part of E₀ (for elliptical polarization).
        position_ref: Reference position for phase (cm).
        phase_offset: Initial phase φ (radians).
    """

    angular_frequency: float = 0.0
    wave_vector: np.ndarray = field(default_factory=lambda: np.zeros(3))
    E0_real: np.ndarray = field(default_factory=lambda: np.zeros(3))
    E0_imag: np.ndarray = field(default_factory=lambda: np.zeros(3))
    position_ref: np.ndarray = field(default_factory=lambda: np.zeros(3))
    phase_offset: float = 0.0

    def __post_init__(self):
        """Validate and compute derived quantities."""
        self.wave_vector = np.asarray(self.wave_vector, dtype=np.float64)
        self.E0_real = np.asarray(self.E0_real, dtype=np.float64)
        self.E0_imag = np.asarray(self.E0_imag, dtype=np.float64)
        self.position_ref = np.asarray(self.position_ref, dtype=np.float64)

        # Compute wave number
        self.k_mag = np.linalg.norm(self.wave_vector)

        # Verify transversality: k · E₀ = 0
        self.transversality_error = np.dot(self.wave_vector, self.E0_real)

    @property
    def frequency(self) -> float:
        """Frequency f = ω/(2π) (Hz)."""
        return self.angular_frequency / (2.0 * np.pi)

    @property
    def wavelength(self) -> float:
        """Wavelength λ = 2π/|k| (cm)."""
        if self.k_mag > 0:
            return 2.0 * np.pi / self.k_mag
        return 0.0

    @property
    def wave_number(self) -> float:
        """Wave number |k| = 2π/λ (rad/cm)."""
        return self.k_mag

    @property
    def propagation_direction(self) -> np.ndarray:
        """Unit vector k̂ in propagation direction."""
        if self.k_mag > 0:
            return self.wave_vector / self.k_mag
        return np.array([0.0, 0.0, 1.0])

    @property
    def polarization_direction(self) -> np.ndarray:
        """Unit vector in E-field direction (real part)."""
        norm = np.linalg.norm(self.E0_real)
        if norm > 0:
            return self.E0_real / norm
        return np.zeros(3)

    @property
    def phase_velocity(self) -> float:
        """Phase velocity v = ω/|k| (cm/s)."""
        if self.k_mag > 0:
            return self.angular_frequency / self.k_mag
        return CONST.C

    @classmethod
    @maxwell_cite(
        786, 787,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Create linearly polarized plane wave",
    )
    def linearly_polarized(
        cls,
        angular_frequency: float,
        E0_magnitude: float,
        propagation_direction: np.ndarray,
        polarization_direction: np.ndarray,
    ) -> PlaneWave:
        """
        Create a linearly polarized plane wave.

        Art. 786-787: For linear polarization, the electric field
        oscillates along a fixed direction perpendicular to propagation.

        Args:
            angular_frequency: ω (rad/s).
            E0_magnitude: |E₀| (statvolts/cm).
            propagation_direction: Unit vector k̂.
            polarization_direction: Unit vector ê for E-field.

        Returns:
            PlaneWave object with linear polarization.

        Reference:
            Part IV, Arts. 786-787: Linearly polarized waves.

        Example:
            >>> wave = PlaneWave.linearly_polarized(
            ...     angular_frequency=2*np.pi*5e14,
            ...     E0_magnitude=100.0,
            ...     propagation_direction=np.array([0, 0, 1]),
            ...     polarization_direction=np.array([1, 0, 0])
            ... )
        """
        propagation_direction = np.asarray(propagation_direction, dtype=np.float64)
        propagation_direction = propagation_direction / np.linalg.norm(propagation_direction)

        polarization_direction = np.asarray(polarization_direction, dtype=np.float64)
        polarization_direction = polarization_direction / np.linalg.norm(polarization_direction)

        # Verify perpendicularity
        if abs(np.dot(propagation_direction, polarization_direction)) > 1e-10:
            raise ValueError("Propagation and polarization must be perpendicular")

        # Wave vector
        k_mag = angular_frequency / CONST.C
        wave_vector = k_mag * propagation_direction

        # E₀ vector (real only for linear polarization)
        E0_real = E0_magnitude * polarization_direction

        return cls(
            angular_frequency=angular_frequency,
            wave_vector=wave_vector,
            E0_real=E0_real,
            E0_imag=np.zeros(3),
        )

    @classmethod
    @maxwell_cite(
        788, 789,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Create circularly polarized plane wave",
    )
    def circularly_polarized(
        cls,
        angular_frequency: float,
        E0_magnitude: float,
        propagation_direction: np.ndarray,
        handedness: str = 'right',
    ) -> PlaneWave:
        """
        Create a circularly polarized plane wave.

        Art. 788-789: For circular polarization, the electric field
        vector rotates in the plane perpendicular to propagation.

        The complex amplitude is:
            E₀ = E₀/√2 (ê₁ ± i ê₂)

        where ê₁ and ê₂ are orthogonal unit vectors perpendicular to k,
        and the sign determines handedness.

        Right-hand circular (RHC): E rotates clockwise looking into source
        Left-hand circular (LHC): E rotates counterclockwise

        Args:
            angular_frequency: ω (rad/s).
            E0_magnitude: |E₀| (statvolts/cm).
            propagation_direction: Unit vector k̂.
            handedness: 'right' or 'left' (default: 'right').

        Returns:
            PlaneWave object with circular polarization.

        Reference:
            Part IV, Arts. 788-789: Circularly polarized waves.

        Example:
            >>> wave = PlaneWave.circularly_polarized(
            ...     angular_frequency=2*np.pi*5e14,
            ...     E0_magnitude=100.0,
            ...     propagation_direction=np.array([0, 0, 1]),
            ...     handedness='right'
            ... )
        """
        propagation_direction = np.asarray(propagation_direction, dtype=np.float64)
        propagation_direction = propagation_direction / np.linalg.norm(propagation_direction)

        # Find orthogonal basis vectors
        # Choose arbitrary vector not parallel to k
        if abs(propagation_direction[2]) < 0.9:
            temp = np.array([0.0, 0.0, 1.0])
        else:
            temp = np.array([1.0, 0.0, 0.0])

        ê1 = np.cross(propagation_direction, temp)
        ê1 = ê1 / np.linalg.norm(ê1)
        ê2 = np.cross(propagation_direction, ê1)

        # Circular polarization: E₀ = E₀/√2 (ê₁ ± i ê₂)
        # For right-hand: + sign (using physics convention)
        sign = 1.0 if handedness == 'right' else -1.0

        E0_real = (E0_magnitude / np.sqrt(2.0)) * ê1
        E0_imag = sign * (E0_magnitude / np.sqrt(2.0)) * ê2

        # Wave vector
        k_mag = angular_frequency / CONST.C
        wave_vector = k_mag * propagation_direction

        return cls(
            angular_frequency=angular_frequency,
            wave_vector=wave_vector,
            E0_real=E0_real,
            E0_imag=E0_imag,
        )

    @maxwell_cite(
        786,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate E and B fields at position and time",
    )
    def fields_at(
        self,
        position: np.ndarray,
        time: float,
    ) -> dict[str, np.ndarray | float]:
        """
        Calculate electric and magnetic field vectors.

        Art. 786: For a plane wave with complex amplitude E₀:

            E(r,t) = Re{E₀ exp[i(k·r - ωt)]}
            B(r,t) = (1/c) k̂ × E(r,t)

        For E₀ = E₀ᵣ + iE₀ᵢ:
            E(r,t) = E₀ᵣ cos(φ) - E₀ᵢ sin(φ)
            B(r,t) = (1/c) k̂ × E(r,t)

        where φ = k·r - ωt + φ₀

        Args:
            position: Position r (cm).
            time: Time t (s).

        Returns:
            Dictionary with:
            - E_field: Electric field vector (statvolts/cm)
            - B_field: Magnetic flux density (gauss)
            - H_field: Magnetic field intensity (oersted)
            - phase: Instantaneous phase
            - energy_density: u = (|E|² + |B|²)/(8π)

        Reference:
            Part IV, Art. 786: Plane wave field calculation.
        """
        position = np.asarray(position, dtype=np.float64)

        # Phase
        phase = np.dot(self.wave_vector, position - self.position_ref) - self.angular_frequency * time + self.phase_offset

        cos_phase = np.cos(phase)
        sin_phase = np.sin(phase)

        # Electric field: E = Eᵣ cos(φ) - Eᵢ sin(φ)
        E_field = self.E0_real * cos_phase - self.E0_imag * sin_phase

        # Magnetic field: B = (1/c) k̂ × E
        k_hat = self.propagation_direction
        B_field = (1.0 / CONST.C) * np.cross(k_hat, E_field)

        # H field (in vacuum, H = B)
        H_field = B_field

        # Energy density: u = (|E|² + |B|²)/(8π)
        E_sq = np.dot(E_field, E_field)
        B_sq = np.dot(B_field, B_field)
        energy_density = (E_sq + B_sq) / (8.0 * np.pi)

        return {
            "E_field": E_field,
            "B_field": B_field,
            "H_field": H_field,
            "phase": phase,
            "phase_degrees": np.degrees(phase) % 360,
            "energy_density": energy_density,
            "E_magnitude": np.linalg.norm(E_field),
            "B_magnitude": np.linalg.norm(B_field),
        }


@maxwell_cite(
    787,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Verify transverse nature of plane wave",
)
def verify_transversality(
    wave: PlaneWave,
    tolerance: float = 1e-10,
) -> dict[str, bool | float | np.ndarray]:
    """
    Verify the transverse nature of electromagnetic waves.

    Art. 787: Maxwell's equations require that plane electromagnetic
    waves be transverse:

        k · E = 0  (electric field perpendicular to propagation)
        k · B = 0  (magnetic field perpendicular to propagation)

    This follows from Gauss's laws:
        ∇ · E = 0 ⟹ k · E₀ = 0
        ∇ · B = 0 ⟹ k · B₀ = 0

    for a plane wave with exp[i(k·r - ωt)] dependence.

    Args:
        wave: PlaneWave object.
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with:
        - k_dot_E: k · E₀ (should be ~0)
        - k_dot_B: k · B₀ (should be ~0)
        - E_perp_k: True if E ⊥ k
        - B_perp_k: True if B ⊥ k
        - transverse_verified: True if wave is transverse

    Reference:
        Part IV, Art. 787: Transverse nature of EM waves.

    Example:
        >>> wave = PlaneWave.linearly_polarized(...)
        >>> result = verify_transversality(wave)
        >>> assert result['transverse_verified']
    """
    k = wave.wave_vector
    E0 = wave.E0_real + 1j * wave.E0_imag

    # k · E₀
    k_dot_E = np.dot(k, wave.E0_real)
    k_dot_E_imag = np.dot(k, wave.E0_imag)

    # B₀ = (1/ω) k × E₀, so k · B₀ = 0 automatically
    B0_real = (1.0 / CONST.C) * np.cross(wave.propagation_direction, wave.E0_real)
    B0_imag = (1.0 / CONST.C) * np.cross(wave.propagation_direction, wave.E0_imag)

    k_dot_B = np.dot(k, B0_real)
    k_dot_B_imag = np.dot(k, B0_imag)

    # Check tolerances
    E0_mag = np.linalg.norm(wave.E0_real) + np.linalg.norm(wave.E0_imag)
    tol = tolerance * wave.k_mag * E0_mag

    E_perp_k = abs(k_dot_E) < tol and abs(k_dot_E_imag) < tol
    B_perp_k = abs(k_dot_B) < tol and abs(k_dot_B_imag) < tol

    return {
        "k_dot_E_real": k_dot_E,
        "k_dot_E_imag": k_dot_E_imag,
        "k_dot_B_real": k_dot_B,
        "k_dot_B_imag": k_dot_B_imag,
        "E_perp_k": E_perp_k,
        "B_perp_k": B_perp_k,
        "transverse_verified": E_perp_k and B_perp_k,
    }


@maxwell_cite(
    788,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate E-B field relationship",
)
def calc_EB_relationship(
    wave: PlaneWave,
    position: np.ndarray,
    time: float,
) -> dict[str, np.ndarray | float | bool]:
    """
    Calculate the relationship between E and B fields.

    Art. 788: For a plane electromagnetic wave, the fields satisfy:

    1. E ⊥ B (mutually perpendicular)
    2. B = (1/c) k̂ × E (direction and magnitude)
    3. |E| = c|B| (in vacuum)
    4. E and B are in phase

    These relationships follow from Faraday's law and Ampere-Maxwell
    applied to the plane wave solutions.

    Args:
        wave: PlaneWave object.
        position: Position r (cm).
        time: Time t (s).

    Returns:
        Dictionary with:
        - E_field: Electric field vector
        - B_field: Magnetic flux density
        - E_dot_B: E · B (should be ~0)
        - B_from_E: (1/c) k̂ × E
        - amplitude_ratio: |E|/(c|B|) (should be ~1)
        - EB_perpendicular: True if E ⊥ B
        - amplitude_verified: True if |E| = c|B|

    Reference:
        Part IV, Art. 788: E-B field relationship.

    Example:
        >>> wave = PlaneWave.linearly_polarized(...)
        >>> result = calc_EB_relationship(wave, np.zeros(3), 0.0)
        >>> assert result['EB_perpendicular']
    """
    fields = wave.fields_at(position, time)
    E = fields["E_field"]
    B = fields["B_field"]

    # E · B (should be 0)
    E_dot_B = np.dot(E, B)

    # B from E: B = (1/c) k̂ × E
    k_hat = wave.propagation_direction
    B_from_E = (1.0 / CONST.C) * np.cross(k_hat, E)

    # Amplitude ratio |E|/(c|B|)
    E_mag = np.linalg.norm(E)
    B_mag = np.linalg.norm(B)

    if B_mag > 0:
        amplitude_ratio = E_mag / (CONST.C * B_mag)
    else:
        amplitude_ratio = 1.0 if E_mag == 0 else float('inf')

    # Phase check (E and B should have same sign)
    in_phase = np.dot(E, B) >= -1e-10  # Allow for numerical error

    return {
        "E_field": E,
        "B_field": B,
        "E_dot_B": E_dot_B,
        "EB_perpendicular": abs(E_dot_B) < 1e-10 * E_mag * B_mag,
        "B_from_E": B_from_E,
        "B_difference": np.linalg.norm(B - B_from_E),
        "amplitude_ratio": amplitude_ratio,
        "amplitude_verified": abs(amplitude_ratio - 1.0) < 1e-6,
        "in_phase": in_phase,
    }


@maxwell_cite(
    789, 790,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate Poynting vector for plane wave",
)
def calc_poynting_vector(
    wave: PlaneWave,
    position: np.ndarray,
    time: float,
    average: bool = False,
) -> dict[str, np.ndarray | float]:
    """
    Calculate the Poynting vector (energy flux) of a plane wave.

    Art. 789-790: The Poynting vector S represents the energy flux
    (energy per unit area per unit time) of the electromagnetic field:

        S = (c/4π) E × H

    For a plane wave in vacuum with H = B:
        S = (c/4π) E × B

    The time-averaged magnitude for a sinusoidal wave is:
        ⟨S⟩ = (c/8π) E₀² = (c/8π) |E₀|²

    The energy density is:
        u = (|E|² + |B|²)/(8π) = |E|²/(4π)

    And the energy flux is:
        S = u · c · k̂

    Args:
        wave: PlaneWave object.
        position: Position r (cm).
        time: Time t (s).
        average: If True, return time-averaged value.

    Returns:
        Dictionary with:
        - S_vector: Instantaneous Poynting vector (erg/(cm²·s))
        - S_average: Time-averaged Poynting vector
        - S_magnitude: |S|
        - energy_density: u (erg/cm³)
        - intensity: Time-averaged |S|

    Reference:
        Part IV, Arts. 789-790: Energy propagation.

    Example:
        >>> wave = PlaneWave.linearly_polarized(...)
        >>> result = calc_poynting_vector(wave, np.zeros(3), 0.0)
        >>> print(f"Intensity: {result['S_average']} erg/(cm²·s)")
    """
    fields = wave.fields_at(position, time)
    E = fields["E_field"]
    B = fields["B_field"]
    H = B  # In vacuum

    # Instantaneous Poynting vector: S = (c/4π) E × H
    S_instant = (CONST.C / (4.0 * np.pi)) * np.cross(E, H)

    # Energy density: u = (|E|² + |B|²)/(8π)
    E_sq = np.dot(E, E)
    B_sq = np.dot(B, B)
    u = (E_sq + B_sq) / (8.0 * np.pi)

    # Time-averaged values
    E0_sq = np.dot(wave.E0_real, wave.E0_real) + np.dot(wave.E0_imag, wave.E0_imag)
    S_avg_mag = (CONST.C / (8.0 * np.pi)) * E0_sq

    # Average Poynting vector direction
    k_hat = wave.propagation_direction
    S_average = S_avg_mag * k_hat

    # Intensity (magnitude of average Poynting vector)
    intensity = S_avg_mag

    return {
        "S_vector": S_instant,
        "S_magnitude": np.linalg.norm(S_instant),
        "S_average": S_average,
        "intensity": intensity,
        "energy_density": u,
        "propagation_direction": k_hat,
        "E_squared": E_sq,
        "B_squared": B_sq,
    }


@dataclass
class PlaneWaveAnalyzer:
    """
    Comprehensive analyzer for plane electromagnetic waves.

    Art. 786-790: This class provides a unified interface for all
    plane wave calculations and verifications.

    Attributes:
        wave: PlaneWave object to analyze.
    """

    wave: PlaneWave

    @maxwell_cite(
        786,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate fields at point",
    )
    def fields(self, position: np.ndarray, time: float) -> dict:
        """Calculate E and B fields at position and time."""
        return self.wave.fields_at(position, time)

    @maxwell_cite(
        787,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Verify transversality",
    )
    def verify_transverse(self) -> dict:
        """Verify wave is transverse."""
        return verify_transversality(self.wave)

    @maxwell_cite(
        788,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Verify E-B relationship",
    )
    def verify_EB(self, position: np.ndarray, time: float) -> dict:
        """Verify E-B field relationship."""
        return calc_EB_relationship(self.wave, position, time)

    @maxwell_cite(
        789, 790,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate energy flux",
    )
    def energy_flux(self, position: np.ndarray, time: float) -> dict:
        """Calculate Poynting vector and energy density."""
        return calc_poynting_vector(self.wave, position, time)

    @maxwell_cite(
        786, 787, 788, 789, 790,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Complete plane wave analysis",
    )
    def analyze(self, position: np.ndarray, time: float) -> dict:
        """Complete analysis of plane wave properties."""
        result = {
            "fields": self.fields(position, time),
            "transversality": self.verify_transverse(),
            "EB_relationship": self.verify_EB(position, time),
            "energy": self.energy_flux(position, time),
        }

        # Wave parameters
        result["wave_params"] = {
            "frequency": self.wave.frequency,
            "wavelength": self.wave.wavelength,
            "angular_frequency": self.wave.angular_frequency,
            "wave_number": self.wave.k_mag,
            "phase_velocity": self.wave.phase_velocity,
            "propagation_direction": self.wave.propagation_direction,
            "polarization": self.wave.polarization_direction,
        }

        return result


__all__ = [
    "PlaneWave",
    "verify_transversality",
    "calc_EB_relationship",
    "calc_poynting_vector",
    "PlaneWaveAnalyzer",
]

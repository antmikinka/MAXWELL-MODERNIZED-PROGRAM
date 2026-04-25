"""
Electromagnetic Wave Polarization — analysis of wave polarization states.

Implements Maxwell's polarization theory from Articles 791-795:

- Linear polarization (Art. 791)
- Circular polarization (Art. 792)
- Elliptical polarization (Art. 793)
- Polarization decomposition (Art. 794)
- Polarization transformation (Art. 795)

Polarization describes the time-varying direction of the electric field
vector at a fixed point in space. For a monochromatic plane wave, the
tip of the E-field vector traces an ellipse in the plane perpendicular
to propagation.

General elliptical polarization:
    E_x = E₁ cos(ωt - kz)
    E_y = E₂ cos(ωt - kz + δ)

where δ is the phase difference between orthogonal components.

Special cases:
- Linear: δ = 0 or π (ellipse collapses to line)
- Circular: E₁ = E₂ and δ = ±π/2 (circle)
- Elliptical: all other cases

Category: A (maxwell_original) — Maxwell's polarization theory.

References:
    Part IV, Ch XX: Electromagnetic Theory of Light (Arts. 781-805).
    Part IV, Arts. 791-795: Polarization of electromagnetic waves.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np
from typing import Optional, Tuple

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class PolarizationState:
    """
    Complete description of electromagnetic wave polarization.

    Art. 791-795: The polarization state is characterized by:

    Jones vector (complex amplitude):
        J = [E_x, E_y]ᵀ = [E₁, E₂·exp(iδ)]ᵀ

    Stokes parameters (real, measurable):
        S₀ = E₁² + E₂² (total intensity)
        S₁ = E₁² - E₂² (horizontal vs vertical)
        S₂ = 2E₁E₂ cos(δ) (+45° vs -45°)
        S₃ = 2E₁E₂ sin(δ) (right vs left circular)

    Ellipse parameters:
        ψ = orientation angle (0 to π)
        χ = ellipticity angle (-π/4 to π/4)
        ε = b/a = tan|χ| (axial ratio)

    Attributes:
        E1: Amplitude of x-component (statvolts/cm).
        E2: Amplitude of y-component (statvolts/cm).
        delta: Phase difference δ (radians).
        propagation_direction: Direction of wave travel.
    """

    E1: float = 1.0
    E2: float = 0.0
    delta: float = 0.0
    propagation_direction: np.ndarray = field(default_factory=lambda: np.array([0.0, 0.0, 1.0]))

    def __post_init__(self):
        """Validate and compute derived quantities."""
        self.propagation_direction = np.asarray(self.propagation_direction, dtype=np.float64)
        norm = np.linalg.norm(self.propagation_direction)
        if norm > 0:
            self.propagation_direction = self.propagation_direction / norm

        # Ensure amplitudes are non-negative
        self.E1 = abs(float(self.E1))
        self.E2 = abs(float(self.E2))

        # Normalize phase to [-π, π]
        self.delta = np.mod(self.delta + np.pi, 2 * np.pi) - np.pi

    @property
    def total_intensity(self) -> float:
        """Total intensity S₀ = E₁² + E₂²."""
        return self.E1 ** 2 + self.E2 ** 2

    @property
    def Jones_vector(self) -> np.ndarray:
        """Jones vector J = [E₁, E₂·exp(iδ)]ᵀ."""
        return np.array([self.E1, self.E2 * np.exp(1j * self.delta)])

    @property
    def Stokes_parameters(self) -> np.ndarray:
        """Stokes parameters [S₀, S₁, S₂, S₃]."""
        S0 = self.E1 ** 2 + self.E2 ** 2
        S1 = self.E1 ** 2 - self.E2 ** 2
        S2 = 2 * self.E1 * self.E2 * np.cos(self.delta)
        S3 = 2 * self.E1 * self.E2 * np.sin(self.delta)
        return np.array([S0, S1, S2, S3])

    @property
    def polarization_type(self) -> str:
        """Determine the polarization type."""
        if self.E2 == 0 or self.E1 == 0:
            return "linear"

        delta_normalized = np.mod(self.delta + np.pi, 2 * np.pi) - np.pi

        if abs(np.sin(self.delta)) < 1e-10:
            return "linear"
        elif abs(np.cos(self.delta)) < 1e-10 and abs(self.E1 - self.E2) < 0.01 * (self.E1 + self.E2):
            return "circular" if self.E1 > 0 and self.E2 > 0 else "linear"
        elif abs(self.E1 - self.E2) < 1e-10 and abs(abs(np.sin(self.delta)) - 1) < 0.01:
            return "circular"
        else:
            return "elliptical"

    @property
    def handedness(self) -> str:
        """Determine handedness for circular/elliptical polarization."""
        if np.sin(self.delta) > 0:
            return "right"  # Right-hand (clockwise looking into source)
        elif np.sin(self.delta) < 0:
            return "left"
        else:
            return "N/A"  # Linear

    @classmethod
    @maxwell_cite(
        791,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Create linear polarization state",
    )
    def linear(
        cls,
        angle: float,
        amplitude: float = 1.0,
        propagation_direction: np.ndarray = None,
    ) -> PolarizationState:
        """
        Create linear polarization at specified angle.

        Art. 791: Linear polarization occurs when the electric field
        oscillates along a fixed direction. The angle θ is measured
        from the x-axis in the xy-plane.

        For angle θ:
            E₁ = A cos(θ)
            E₂ = A sin(θ)
            δ = 0

        Args:
            angle: Polarization angle θ (radians) from x-axis.
            amplitude: Total amplitude A (default: 1.0).
            propagation_direction: Direction of propagation.

        Returns:
            PolarizationState object.

        Reference:
            Part IV, Art. 791: Linear polarization.

        Example:
            >>> # Horizontal polarization (along x)
            >>> p = PolarizationState.linear(0.0)
            >>> # 45-degree polarization
            >>> p = PolarizationState.linear(np.pi/4)
        """
        if propagation_direction is None:
            propagation_direction = np.array([0.0, 0.0, 1.0])

        E1 = amplitude * np.cos(angle)
        E2 = amplitude * np.sin(angle)

        return cls(E1=E1, E2=E2, delta=0.0, propagation_direction=propagation_direction)

    @classmethod
    @maxwell_cite(
        792,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Create circular polarization state",
    )
    def circular(
        cls,
        handedness: str = 'right',
        amplitude: float = 1.0,
        propagation_direction: np.ndarray = None,
    ) -> PolarizationState:
        """
        Create circular polarization.

        Art. 792: Circular polarization occurs when E₁ = E₂ and the
        phase difference is δ = ±π/2. The electric field vector
        rotates in a circle at frequency ω.

        Right-hand circular (RHC): δ = +π/2
        Left-hand circular (LHC): δ = -π/2

        Args:
            handedness: 'right' or 'left'.
            amplitude: Amplitude of each component (default: 1.0).
            propagation_direction: Direction of propagation.

        Returns:
            PolarizationState object.

        Reference:
            Part IV, Art. 792: Circular polarization.

        Example:
            >>> # Right-hand circular
            >>> p = PolarizationState.circular('right')
            >>> # Left-hand circular
            >>> p = PolarizationState.circular('left')
        """
        if propagation_direction is None:
            propagation_direction = np.array([0.0, 0.0, 1.0])

        delta = np.pi / 2 if handedness == 'right' else -np.pi / 2

        return cls(
            E1=amplitude,
            E2=amplitude,
            delta=delta,
            propagation_direction=propagation_direction,
        )

    @classmethod
    @maxwell_cite(
        793,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Create elliptical polarization state",
    )
    def elliptical(
        cls,
        E1: float,
        E2: float,
        delta: float,
        propagation_direction: np.ndarray = None,
    ) -> PolarizationState:
        """
        Create general elliptical polarization.

        Art. 793: Elliptical polarization is the most general form,
        where the electric field traces an ellipse. Special cases:
        - Linear: δ = 0 or π
        - Circular: E₁ = E₂, δ = ±π/2

        Args:
            E1: X-component amplitude.
            E2: Y-component amplitude.
            delta: Phase difference (radians).
            propagation_direction: Direction of propagation.

        Returns:
            PolarizationState object.

        Reference:
            Part IV, Art. 793: Elliptical polarization.

        Example:
            >>> # Elliptical with axial ratio 2:1
            >>> p = PolarizationState.elliptical(2.0, 1.0, np.pi/2)
        """
        return cls(E1=E1, E2=E2, delta=delta, propagation_direction=propagation_direction)

    @maxwell_cite(
        794,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate ellipse parameters",
    )
    def ellipse_parameters(self) -> dict[str, float]:
        """
        Calculate the polarization ellipse parameters.

        Art. 794: The polarization ellipse is characterized by:
        - Orientation angle ψ: Tilt of major axis from x-axis
        - Ellipticity angle χ: tan(χ) = b/a (axial ratio)
        - Axial ratio AR = a/b = 1/tan|χ|

        The ellipse equation is:
            (E_x/E₁)² + (E_y/E₂)² - 2(E_x/E₁)(E_y/E₂)cos(δ) = sin²(δ)

        Returns:
            Dictionary with:
            - orientation_angle: ψ (radians)
            - ellipticity_angle: χ (radians)
            - axial_ratio: a/b
            - major_axis: Length of major axis
            - minor_axis: Length of minor axis

        Reference:
            Part IV, Art. 794: Polarization ellipse.
        """
        # Orientation angle ψ
        if abs(self.E1) < 1e-10 and abs(self.E2) < 1e-10:
            psi = 0.0
        else:
            tan_2psi = (2 * self.E1 * self.E2 * np.cos(self.delta)) / (self.E1 ** 2 - self.E2 ** 2)
            psi = 0.5 * np.arctan2(tan_2psi * (self.E1 ** 2 - self.E2 ** 2), 2 * self.E1 * self.E2 * np.cos(self.delta))
            # Alternative formula
            psi = 0.5 * np.arctan2(2 * self.E1 * self.E2 * np.cos(self.delta),
                                    self.E1 ** 2 - self.E2 ** 2)

        # Ellipticity angle χ
        sin_2chi = (2 * self.E1 * self.E2 * np.sin(self.delta)) / (self.E1 ** 2 + self.E2 ** 2)
        sin_2chi = np.clip(sin_2chi, -1, 1)  # Numerical safety
        chi = 0.5 * np.arcsin(sin_2chi)

        # Axial ratio
        eps = np.tan(abs(chi))
        if eps > 1e-10:
            axial_ratio = 1.0 / eps
        else:
            axial_ratio = float('inf')  # Linear polarization

        # Semi-major and semi-minor axes
        I = self.E1 ** 2 + self.E2 ** 2
        a = np.sqrt(I / (1 + eps ** 2)) if eps < 1 else np.sqrt(I * eps ** 2 / (1 + eps ** 2))
        b = eps * a

        return {
            "orientation_angle": psi,
            "orientation_degrees": np.degrees(psi) % 180,
            "ellipticity_angle": chi,
            "ellipticity_degrees": np.degrees(chi),
            "axial_ratio": axial_ratio,
            "major_axis": a,
            "minor_axis": b,
            "handedness": self.handedness,
        }


@maxwell_cite(
    794,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate Stokes parameters from field amplitudes",
)
def calc_Stokes_parameters(
    E1: float,
    E2: float,
    delta: float,
) -> dict[str, float]:
    """
    Calculate Stokes parameters for characterizing polarization.

    Art. 794: The Stokes parameters provide a complete description
    of the polarization state using four real, measurable quantities:

        S₀ = E₁² + E₂²          (total intensity)
        S₁ = E₁² - E₂²          (horizontal vs vertical preference)
        S₂ = 2E₁E₂ cos(δ)       (+45° vs -45° preference)
        S₃ = 2E₁E₂ sin(δ)       (right vs left circular preference)

    Properties:
        - S₀ ≥ 0 (always non-negative)
        - S₁² + S₂² + S₃² = S₀² (fully polarized)
        - For partially polarized light: S₁² + S₂² + S₃² < S₀²

    The Poincaré sphere representation maps (S₁, S₂, S₃)/S₀ to a
    point on the unit sphere.

    Args:
        E1: X-component amplitude.
        E2: Y-component amplitude.
        delta: Phase difference (radians).

    Returns:
        Dictionary with Stokes parameters S₀, S₁, S₂, S₃ and derived quantities.

    Reference:
        Part IV, Art. 794: Stokes parameters.

    Example:
        >>> S = calc_Stokes_parameters(1.0, 1.0, np.pi/2)
        >>> print(f"Degree of polarization: {S['degree_of_polarization']}")
    """
    S0 = E1 ** 2 + E2 ** 2
    S1 = E1 ** 2 - E2 ** 2
    S2 = 2 * E1 * E2 * np.cos(delta)
    S3 = 2 * E1 * E2 * np.sin(delta)

    # Degree of polarization (1 for fully polarized)
    if S0 > 0:
        DOP = np.sqrt(S1 ** 2 + S2 ** 2 + S3 ** 2) / S0
    else:
        DOP = 0.0

    # Normalized Stokes parameters
    if S0 > 0:
        s1 = S1 / S0
        s2 = S2 / S0
        s3 = S3 / S0
    else:
        s1, s2, s3 = 0.0, 0.0, 0.0

    return {
        "S0": S0,
        "S1": S1,
        "S2": S2,
        "S3": S3,
        "Stokes_vector": np.array([S0, S1, S2, S3]),
        "normalized_Stokes": np.array([s1, s2, s3]),
        "degree_of_polarization": DOP,
        "polarization_type": _stokes_to_type(s1, s2, s3),
    }


def _stokes_to_type(s1: float, s2: float, s3: float) -> str:
    """Determine polarization type from normalized Stokes parameters."""
    if abs(s3) > 0.9:
        return "circular"
    elif abs(s3) < 0.1 and abs(s1) > 0.9 or abs(s2) > 0.9:
        return "linear"
    else:
        return "elliptical"


@maxwell_cite(
    794, 795,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Decompose polarization into orthogonal components",
)
def decompose_polarization(
    state: PolarizationState,
    basis_angle: float = 0.0,
) -> dict[str, np.ndarray | float]:
    """
    Decompose polarization state into orthogonal basis components.

    Art. 794-795: Any polarization state can be decomposed into
    orthogonal components in various bases:

    Linear basis (H/V at angle θ):
        E_H = E₁ cos(θ) + E₂ sin(θ)
        E_V = -E₁ sin(θ) + E₂ cos(θ)

    Circular basis (RHC/LHC):
        E_R = (E₁ - iE₂)/√2
        E_L = (E₁ + iE₂)/√2

    Args:
        state: PolarizationState object.
        basis_angle: Angle of linear basis from x-axis (radians).
                     Use 0 for H/V, π/4 for ±45°.
                     Use 'circular' for RHC/LHC basis.

    Returns:
        Dictionary with:
        - basis_type: 'linear' or 'circular'
        - components: Complex amplitude vector in new basis
        - intensities: Power in each component
        - projection_matrix: Transformation matrix

    Reference:
        Part IV, Arts. 794-795: Polarization decomposition.

    Example:
        >>> state = PolarizationState.linear(np.pi/4)
        >>> result = decompose_polarization(state, 0.0)  # H/V decomposition
    """
    J = state.Jones_vector  # [E₁, E₂·exp(iδ)]

    if basis_angle == 'circular':
        # Circular basis transformation
        # [E_R]   1     [1  -i] [E₁]
        # [E_L] = √2 ·  [1   i] [E₂]
        M = np.array([[1, -1j], [1, 1j]]) / np.sqrt(2)
        basis_type = 'circular'
        component_names = ['RHC', 'LHC']
    else:
        # Linear basis rotation by angle θ
        # [E_H]   [cos θ   sin θ] [E₁]
        # [E_V] = [-sin θ  cos θ] [E₂]
        c, s = np.cos(basis_angle), np.sin(basis_angle)
        M = np.array([[c, s], [-s, c]])
        basis_type = 'linear'
        component_names = [f'H@{np.degrees(basis_angle):.0f}°', f'V@{np.degrees(basis_angle):.0f}°']

    # Transform
    J_new = np.dot(M, J)

    # Intensities
    intensities = np.array([np.abs(J_new[0]) ** 2, np.abs(J_new[1]) ** 2])

    return {
        "basis_type": basis_type,
        "component_names": component_names,
        "components": J_new,
        "intensities": intensities,
        "projection_matrix": M,
        "original_Jones": J,
    }


@maxwell_cite(
    795,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Transform polarization through optical element",
)
def transform_polarization(
    state: PolarizationState,
    Jones_matrix: np.ndarray,
) -> dict[str, PolarizationState | np.ndarray]:
    """
    Transform polarization state through an optical element.

    Art. 795: The effect of an optical element (polarizer, waveplate,
    etc.) on the polarization state is described by Jones matrix
    multiplication:

        J_out = M · J_in

    Common Jones matrices:
    - Linear polarizer (horizontal): [[1, 0], [0, 0]]
    - Linear polarizer (vertical): [[0, 0], [0, 1]]
    - Quarter-wave plate: [[1, 0], [0, i]]
    - Half-wave plate: [[1, 0], [0, -1]]

    Args:
        state: Input PolarizationState.
        Jones_matrix: 2×2 Jones matrix of optical element.

    Returns:
        Dictionary with:
        - output_state: Transformed polarization state
        - input_Jones: Original Jones vector
        - output_Jones: Transformed Jones vector
        - transmission: Intensity ratio I_out/I_in

    Reference:
        Part IV, Art. 795: Polarization transformation.

    Example:
        >>> # Convert linear to circular with quarter-wave plate
        >>> state = PolarizationState.linear(np.pi/4)
        >>> QWP = np.array([[1, 0], [0, 1j]])
        >>> result = transform_polarization(state, QWP)
    """
    Jones_matrix = np.asarray(Jones_matrix, dtype=np.complex128)
    J_in = state.Jones_vector

    # Transform
    J_out = np.dot(Jones_matrix, J_in)

    # Output intensities
    I_in = np.dot(np.conj(J_in), J_in).real
    I_out = np.dot(np.conj(J_out), J_out).real

    transmission = I_out / I_in if I_in > 0 else 0.0

    # Create output state
    E1_out = np.abs(J_out[0])
    E2_out = np.abs(J_out[1])
    delta_out = np.angle(J_out[1]) - np.angle(J_out[0])

    output_state = PolarizationState(
        E1=E1_out,
        E2=E2_out,
        delta=delta_out,
        propagation_direction=state.propagation_direction,
    )

    return {
        "output_state": output_state,
        "input_Jones": J_in,
        "output_Jones": J_out,
        "input_intensity": I_in,
        "output_intensity": I_out,
        "transmission": transmission,
        "Jones_matrix": Jones_matrix,
    }


@maxwell_cite(
    791, 792, 793, 794, 795,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Analyze complete polarization state",
)
def analyze_polarization(
    state: PolarizationState,
) -> dict[str, float | np.ndarray | dict]:
    """
    Complete analysis of electromagnetic wave polarization.

    Art. 791-795: Comprehensive polarization analysis including:
    1. Polarization type identification
    2. Stokes parameters
    3. Ellipse parameters
    4. Decomposition in various bases
    5. Jones vector representation

    Args:
        state: PolarizationState object to analyze.

    Returns:
        Dictionary with complete polarization analysis.

    Reference:
        Part IV, Arts. 791-795: Complete polarization analysis.

    Example:
        >>> state = PolarizationState.circular('right')
        >>> result = analyze_polarization(state)
        >>> print(f"Type: {result['polarization_type']}")
    """
    # Basic properties
    result = {
        "polarization_type": state.polarization_type,
        "handedness": state.handedness,
        "total_intensity": state.total_intensity,
    }

    # Jones vector
    result["Jones_vector"] = state.Jones_vector

    # Stokes parameters
    Stokes = calc_Stokes_parameters(state.E1, state.E2, state.delta)
    result["Stokes_parameters"] = Stokes

    # Ellipse parameters
    ellipse = state.ellipse_parameters()
    result["ellipse"] = ellipse

    # Decomposition in H/V basis
    result["HV_decomposition"] = decompose_polarization(state, 0.0)

    # Decomposition in circular basis
    result["circular_decomposition"] = decompose_polarization(state, 'circular')

    # Poincaré sphere coordinates
    if state.total_intensity > 0:
        s = state.Stokes_parameters / state.total_intensity
        result["Poincare_sphere"] = {
            "s1": s[1],
            "s2": s[2],
            "s3": s[3],
        }
    else:
        result["Poincare_sphere"] = {"s1": 0, "s2": 0, "s3": 0}

    return result


@dataclass
class PolarizationAnalyzer:
    """
    Comprehensive analyzer for electromagnetic wave polarization.

    Art. 791-795: This class provides a unified interface for all
    polarization calculations and transformations.

    Attributes:
        state: PolarizationState object.
    """

    state: PolarizationState

    @maxwell_cite(
        791,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Get polarization type",
    )
    def polarization_type(self) -> str:
        """Get the polarization type."""
        return self.state.polarization_type

    @maxwell_cite(
        792, 793,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Get handedness",
    )
    def handedness(self) -> str:
        """Get polarization handedness."""
        return self.state.handedness

    @maxwell_cite(
        794,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Get Stokes parameters",
    )
    def Stokes(self) -> np.ndarray:
        """Get Stokes parameters."""
        return self.state.Stokes_parameters

    @maxwell_cite(
        794,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Get Jones vector",
    )
    def Jones(self) -> np.ndarray:
        """Get Jones vector."""
        return self.state.Jones_vector

    @maxwell_cite(
        794,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Get ellipse parameters",
    )
    def ellipse(self) -> dict:
        """Get polarization ellipse parameters."""
        return self.state.ellipse_parameters()

    @maxwell_cite(
        794, 795,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Decompose in basis",
    )
    def decompose(self, basis: float | str = 0.0) -> dict:
        """Decompose polarization in specified basis."""
        return decompose_polarization(self.state, basis)

    @maxwell_cite(
        795,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Transform through element",
    )
    def transform(self, Jones_matrix: np.ndarray) -> dict:
        """Transform polarization through optical element."""
        return transform_polarization(self.state, Jones_matrix)

    @maxwell_cite(
        791, 792, 793, 794, 795,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Complete polarization analysis",
    )
    def analyze(self) -> dict:
        """Complete polarization analysis."""
        return analyze_polarization(self.state)


# Common Jones matrices for optical elements
@maxwell_cite(
    795,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="standard_math",
    description="Jones matrix for linear polarizer",
)
def Jones_linear_polarizer(angle: float = 0.0) -> np.ndarray:
    """
    Jones matrix for linear polarizer at angle θ.

    Args:
        angle: Polarizer transmission axis angle from x-axis (radians).

    Returns:
        2×2 Jones matrix.
    """
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c ** 2, c * s], [c * s, s ** 2]])


@maxwell_cite(
    795,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="standard_math",
    description="Jones matrix for wave plate",
)
def Jones_wave_plate(retardance: float, fast_axis: float = 0.0) -> np.ndarray:
    """
    Jones matrix for wave plate with specified retardance.

    Args:
        retardance: Phase retardation δ (radians).
                    π/2 = quarter-wave, π = half-wave.
        fast_axis: Fast axis angle from x-axis (radians).

    Returns:
        2×2 Jones matrix.
    """
    c, s = np.cos(fast_axis), np.sin(fast_axis)
    exp_idelta = np.exp(-1j * retardance)

    # Rotation matrices and retardation
    R = np.array([[c, s], [-s, c]])
    R_inv = np.array([[c, -s], [s, c]])
    M_retard = np.array([[1, 0], [0, exp_idelta]])

    return np.dot(np.dot(R_inv, M_retard), R)


__all__ = [
    "PolarizationState",
    "calc_Stokes_parameters",
    "decompose_polarization",
    "transform_polarization",
    "analyze_polarization",
    "PolarizationAnalyzer",
    "Jones_linear_polarizer",
    "Jones_wave_plate",
]

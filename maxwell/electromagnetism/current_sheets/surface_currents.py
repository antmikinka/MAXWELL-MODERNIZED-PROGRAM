"""
Surface Currents — mathematical theory of current distributions on surfaces.

Implements Maxwell's theory of surface currents from Articles 656-662:

- Surface current density definition (Art. 656)
- Current continuity on surfaces (Art. 657)
- Field calculation from surface distributions (Art. 658)
- Surface current in conductors (Art. 659)
- Eddy currents and skin effect (Art. 660-661)
- Surface impedance (Art. 662)

Surface current density i (abamperes/cm in CGS) represents current
flowing in an infinitesimally thin layer. This is the limit of a
volume current J as thickness → 0 while I = ∫J·dz remains finite.

CGS Units:
    i = surface current density (abamperes/cm)
    J = volume current density (abamperes/cm²)
    σ = conductivity (s⁻¹ in CGS)
    δ = skin depth (cm)

Category: A (maxwell_original) — Maxwell's theory of surface currents.

References:
    Part IV, Ch XII: Current-Sheets (Arts. 647-674).
    Part IV, Arts. 656-662: Surface current distributions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class SurfaceCurrentDensity:
    """
    Surface current density — current per unit width on a surface.

    Art. 656: Surface current density i is defined as the limit of
    volume current density J integrated over thickness:

        i = lim(δ→0) ∫₀^δ J dz

    Units: abamperes/cm (CGS-EMU)

    For a surface parametrized by (u, v), the surface current is:
        i = i_u · ê_u + i_v · ê_v

    where ê_u and ê_v are tangent vectors to the surface.

    Attributes:
        i_x: Surface current density x-component (abamperes/cm).
        i_y: Surface current density y-component (abamperes/cm).
        surface_normal: Unit normal to the surface.
    """

    i_x: float = 0.0
    i_y: float = 0.0
    surface_normal: np.ndarray = field(
        default_factory=lambda: np.array([0.0, 0.0, 1.0])
    )

    def __post_init__(self):
        """Validate and compute derived quantities."""
        self.surface_normal = np.asarray(self.surface_normal, dtype=np.float64)
        norm = np.linalg.norm(self.surface_normal)
        if norm > 0:
            self.surface_normal = self.surface_normal / norm
        else:
            raise ValueError("Surface normal cannot be zero")

        # 3D current vector (in surface plane)
        self.current_3d = np.array([float(self.i_x), float(self.i_y), 0.0])

    @property
    def magnitude(self) -> float:
        """Magnitude of surface current density (abamperes/cm)."""
        return np.sqrt(self.i_x**2 + self.i_y**2)

    @property
    def direction(self) -> np.ndarray:
        """Unit vector in direction of current flow."""
        mag = self.magnitude
        if mag > 0:
            return np.array([self.i_x / mag, self.i_y / mag, 0.0])
        return np.zeros(3)

    @classmethod
    @maxwell_cite(
        656,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Create surface current from magnitude and direction",
    )
    def from_magnitude_direction(
        cls,
        magnitude: float,
        angle: float,
        normal: np.ndarray = None,
    ) -> SurfaceCurrentDensity:
        """
        Create surface current from magnitude and flow direction angle.

        Art. 656: Surface current density is specified by its magnitude
        and the direction of flow in the surface plane.

        Args:
            magnitude: Current density |i| (abamperes/cm).
            angle: Direction angle θ from x-axis (radians).
            normal: Surface normal (default: z-axis).

        Returns:
            SurfaceCurrentDensity object.

        Reference:
            Part IV, Art. 656: Surface current density definition.
        """
        if normal is None:
            normal = np.array([0.0, 0.0, 1.0])

        i_x = magnitude * np.cos(angle)
        i_y = magnitude * np.sin(angle)

        return cls(i_x=i_x, i_y=i_y, surface_normal=normal)

    @classmethod
    @maxwell_cite(
        656,
        657,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Create surface current from volume current and thickness",
    )
    def from_volume_current(
        cls,
        J: np.ndarray,
        thickness: float,
        normal: np.ndarray = None,
    ) -> SurfaceCurrentDensity:
        """
        Create equivalent surface current from volume current in thin layer.

        Art. 656-657: For a thin conducting layer of thickness δ with
        uniform volume current density J, the equivalent surface current is:

            i = J · δ

        Args:
            J: Volume current density (abamperes/cm²).
            thickness: Layer thickness δ (cm).
            normal: Surface normal (default: z-axis).

        Returns:
            SurfaceCurrentDensity object.

        Reference:
            Part IV, Arts. 656-657: Volume to surface current conversion.
        """
        if thickness <= 0:
            raise ValueError(f"Thickness must be positive, got {thickness}")

        J = np.asarray(J, dtype=np.float64)

        # Surface current = volume current × thickness
        i_x = J[0] * thickness if len(J) > 0 else 0.0
        i_y = J[1] * thickness if len(J) > 1 else 0.0

        return cls(i_x=i_x, i_y=i_y, surface_normal=normal)


@maxwell_cite(
    656,
    657,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Calculate surface current from total current and width",
)
def calc_surface_current(
    total_current: float,
    width: float,
    uniform: bool = True,
) -> dict[str, float]:
    """
    Calculate surface current density from total current and conductor width.

    Art. 656-657: For current I flowing uniformly across a conductor
    of width w, the surface current density is:

        i = I / w

    For non-uniform distributions, this gives the average value.

    Args:
        total_current: Total current I (abamperes).
        width: Conductor width w (cm).
        uniform: Assume uniform distribution (default: True).

    Returns:
        Dictionary with:
        - surface_current: Average i (abamperes/cm)
        - total_current: Input current (abamperes)
        - width: Conductor width (cm)
        - distribution: 'uniform' or 'estimated'

    Reference:
        Part IV, Arts. 656-657: Surface current calculation.

    Example:
        >>> result = calc_surface_current(100.0, 2.0)
        >>> print(f"i = {result['surface_current']} abamperes/cm")  # i = 50.0
    """
    if width <= 0:
        raise ValueError(f"Width must be positive, got {width}")

    i_avg = total_current / width

    return {
        "surface_current": i_avg,
        "total_current": total_current,
        "width": width,
        "distribution": "uniform" if uniform else "estimated",
    }


@maxwell_cite(
    658,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Calculate magnetic field from surface current element",
)
def calc_field_from_surface_current(
    surface_current: SurfaceCurrentDensity,
    observation_point: np.ndarray,
    source_point: np.ndarray = None,
) -> dict[str, np.ndarray | float]:
    """
    Calculate magnetic field from a surface current element.

    Art. 658: The magnetic field dB at a point due to a surface current
    element i dS is given by the Biot-Savart law:

        dB = (1/c) · (i × r̂) / r² · dS

    For a finite surface, integrate over the entire current distribution:

        B(r) = (1/c) · ∫∫ (i(r') × (r - r')) / |r - r'|³ dS'

    Args:
        surface_current: SurfaceCurrentDensity object.
        observation_point: Point where field is calculated (cm).
        source_point: Location of current element (cm, default: origin).

    Returns:
        Dictionary with:
        - field_B: Magnetic flux density (gauss)
        - distance: Distance from source (cm)
        - field_direction: Unit vector in field direction

    Reference:
        Part IV, Art. 658: Field from surface current.

    Example:
        >>> i = SurfaceCurrentDensity(i_x=100, i_y=0)
        >>> result = calc_field_from_surface_current(i, np.array([0, 0, 10]))
        >>> print(f"B = {result['field_B']} gauss")
    """
    obs = np.asarray(observation_point, dtype=np.float64)

    if source_point is None:
        source_point = np.zeros(3)
    else:
        source_point = np.asarray(source_point, dtype=np.float64)

    # Vector from source to observation point
    r_vec = obs - source_point
    r_mag = np.linalg.norm(r_vec)

    if r_mag < 1e-10:
        return {
            "field_B": np.zeros(3),
            "distance": 0.0,
            "warning": "At source point — singular",
        }

    r_hat = r_vec / r_mag

    # Surface current in 3D (rotated to surface plane)
    i_vec = surface_current.current_3d

    # Biot-Savart: dB = (1/c) · (i × r̂) / r²
    # For a unit area element
    factor = surface_current.magnitude / (CONST.C * r_mag**2)
    i_hat = surface_current.direction
    B_dir = np.cross(i_hat, r_hat)
    B = factor * B_dir

    return {
        "field_B": B,
        "distance": r_mag,
        "field_direction": (
            B_dir / np.linalg.norm(B_dir) if np.linalg.norm(B_dir) > 0 else np.zeros(3)
        ),
        "field_magnitude": np.linalg.norm(B),
    }


@maxwell_cite(
    657,
    658,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Calculate boundary condition for surface current sheet",
)
def calc_sheet_boundary_condition(
    surface_current: SurfaceCurrentDensity,
    H_above: np.ndarray = None,
    H_below: np.ndarray = None,
) -> dict[str, np.ndarray | float | bool]:
    """
    Calculate and verify the electromagnetic boundary condition at a current sheet.

    Art. 657-658: At a surface carrying current density i, the tangential
    component of H is discontinuous:

        n̂ × (H_above - H_below) = (4π/c) · i

    The normal component of B is always continuous:
        B_above · n̂ = B_below · n̂

    Args:
        surface_current: SurfaceCurrentDensity object.
        H_above: Magnetic field above the sheet (oersted).
        H_below: Magnetic field below the sheet (oersted).

    Returns:
        Dictionary with:
        - required_discontinuity: (4π/c) · i (oersted)
        - actual_discontinuity: n̂ × (H_above - H_below)
        - boundary_satisfied: True if boundary condition holds
        - normal_continuous: Whether normal B is continuous

    Reference:
        Part IV, Arts. 657-658: Surface current boundary conditions.

    Example:
        >>> i = SurfaceCurrentDensity(i_x=100, i_y=0)
        >>> H_above = np.array([0, 50, 0])
        >>> H_below = np.array([0, -50, 0])
        >>> result = calc_sheet_boundary_condition(i, H_above, H_below)
        >>> print(f"Boundary satisfied: {result['boundary_satisfied']}")
    """
    n = surface_current.surface_normal
    i_vec = surface_current.current_3d

    # Required discontinuity: (4π/c) · i
    required_discontinuity = (4.0 * np.pi / CONST.C) * i_vec

    if H_above is None or H_below is None:
        return {
            "required_discontinuity": required_discontinuity,
            "actual_discontinuity": None,
            "boundary_satisfied": None,
            "note": "Provide H fields to verify boundary condition",
        }

    H_above = np.asarray(H_above, dtype=np.float64)
    H_below = np.asarray(H_below, dtype=np.float64)

    # Actual discontinuity: n × (H_above - H_below)
    delta_H = H_above - H_below
    actual_discontinuity = np.cross(n, delta_H)

    # Check if boundary condition is satisfied
    diff = np.linalg.norm(actual_discontinuity - required_discontinuity)
    tolerance = 1e-8 * max(np.linalg.norm(required_discontinuity), 1.0)
    boundary_satisfied = diff < tolerance

    # Normal component check (B_normal continuous)
    B_normal_above = np.dot(H_above, n)  # In vacuum, B = H
    B_normal_below = np.dot(H_below, n)
    normal_continuous = abs(B_normal_above - B_normal_below) < tolerance

    return {
        "required_discontinuity": required_discontinuity,
        "actual_discontinuity": actual_discontinuity,
        "boundary_satisfied": boundary_satisfied,
        "difference": diff,
        "normal_continuous": normal_continuous,
        "B_normal_above": B_normal_above,
        "B_normal_below": B_normal_below,
    }


@maxwell_cite(
    659,
    660,
    661,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Analyze surface current distribution in conductor",
)
def analyze_surface_current_distribution(
    conductivity: float,
    frequency: float,
    thickness: float,
    applied_field: float,
) -> dict[str, float]:
    """
    Analyze surface current distribution including skin effect.

    Art. 659-661: In a conductor carrying alternating current, the
    current density is not uniform but concentrated near the surface
    (skin effect). The skin depth δ is:

        δ = c / √(2πσωμ)

    In CGS for non-magnetic conductors (μ = 1):
        δ = c / √(4π²σf)

    where σ is conductivity (s⁻¹) and f is frequency (Hz).

    The current distribution is:
        J(z) = J₀ · e^(-z/δ) · e^(iωt)

    Args:
        conductivity: σ (s⁻¹ in CGS).
        frequency: f (Hz).
        thickness: Conductor thickness (cm).
        applied_field: Applied electric field (statvolts/cm).

    Returns:
        Dictionary with:
        - skin_depth: δ (cm)
        - surface_current: i at surface (abamperes/cm)
        - penetration_ratio: thickness / δ
        - effective_resistance: AC resistance factor

    Reference:
        Part IV, Arts. 659-661: Skin effect and eddy currents.

    Example:
        >>> # Copper: σ ≈ 5e17 s⁻¹, f = 1 MHz
        >>> result = analyze_surface_current_distribution(5e17, 1e6, 0.1, 1.0)
        >>> print(f"Skin depth: {result['skin_depth']:.6f} cm")
    """
    if conductivity <= 0:
        raise ValueError(f"Conductivity must be positive")
    if frequency <= 0:
        raise ValueError(f"Frequency must be positive")
    if thickness <= 0:
        raise ValueError(f"Thickness must be positive")

    # Angular frequency
    omega = 2.0 * np.pi * frequency

    # Skin depth in CGS: δ = c / √(2πωσ)
    # For non-magnetic material (μ = 1 in CGS)
    skin_depth = CONST.C / np.sqrt(2.0 * omega * conductivity)

    # Surface current density (at z = 0)
    # J₀ = σE₀, i = J₀ · δ (integrated over skin depth)
    J_surface = conductivity * applied_field
    surface_current = J_surface * skin_depth

    # Penetration ratio
    penetration_ratio = thickness / skin_depth

    # AC resistance factor (approximate)
    # For thick conductor (t >> δ): R_AC / R_DC ≈ t / (2δ)
    # For thin conductor (t << δ): R_AC / R_DC ≈ 1
    if penetration_ratio > 3:
        resistance_factor = penetration_ratio / 2.0
    else:
        # Transition region approximation
        resistance_factor = 1.0 + (penetration_ratio**4) / 3.0

    return {
        "skin_depth": skin_depth,
        "surface_current": surface_current,
        "penetration_ratio": penetration_ratio,
        "ac_resistance_factor": resistance_factor,
        "conductivity": conductivity,
        "frequency": frequency,
        "wavelength": CONST.C / frequency,
    }


@maxwell_cite(
    662,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Calculate surface impedance of conductor",
)
def calc_surface_impedance(
    conductivity: float,
    frequency: float,
    permeability: float = 1.0,
) -> dict[str, float | complex]:
    """
    Calculate surface impedance of a conductor.

    Art. 662: The surface impedance Z_s relates the tangential electric
    field at a conductor surface to the surface current density:

        E_tangential = Z_s · i

    For a good conductor:
        Z_s = R_s + iX_s = (1 + i) / (σδ)

    where R_s = X_s = 1/(σδ) is the surface resistance and reactance.

    In CGS, surface impedance has units of statohm-cm (or s/cm).

    Args:
        conductivity: σ (s⁻¹ in CGS).
        frequency: f (Hz).
        permeability: μ (default: 1.0 for non-magnetic).

    Returns:
        Dictionary with:
        - surface_resistance: R_s (statohm-cm)
        - surface_reactance: X_s (statohm-cm)
        - surface_impedance: Z_s (complex, statohm-cm)
        - skin_depth: δ (cm)

    Reference:
        Part IV, Art. 662: Surface impedance.

    Example:
        >>> # Copper at 1 MHz
        >>> result = calc_surface_impedance(5e17, 1e6)
        >>> print(f"R_s = {result['surface_resistance']} statohm-cm")
    """
    if conductivity <= 0:
        raise ValueError(f"Conductivity must be positive")
    if frequency <= 0:
        raise ValueError(f"Frequency must be positive")

    omega = 2.0 * np.pi * frequency

    # Skin depth
    skin_depth = CONST.C / np.sqrt(2.0 * omega * conductivity * permeability)

    # Surface resistance and reactance (CGS)
    # R_s = X_s = 1 / (σδ)
    R_s = 1.0 / (conductivity * skin_depth)
    X_s = R_s  # For good conductor, R = X

    # Complex impedance
    Z_s = complex(R_s, X_s)

    # Magnitude
    Z_mag = np.sqrt(R_s**2 + X_s**2)

    return {
        "surface_resistance": R_s,
        "surface_reactance": X_s,
        "surface_impedance": Z_s,
        "impedance_magnitude": Z_mag,
        "skin_depth": skin_depth,
        "conductivity": conductivity,
        "frequency": frequency,
    }


@dataclass
class SurfaceCurrentAnalyzer:
    """
    Comprehensive analyzer for surface current phenomena.

    Art. 656-662: This class provides a unified interface for all
    surface current calculations including field computation,
    boundary conditions, skin effect, and impedance.

    Attributes:
        conductivity: Material conductivity σ (s⁻¹).
        permeability: Material permeability μ (default: 1.0).
    """

    conductivity: float = 0.0
    permeability: float = 1.0

    @maxwell_cite(
        656,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Create surface current density object",
    )
    def create_surface_current(
        self,
        i_x: float,
        i_y: float,
        normal: np.ndarray = None,
    ) -> SurfaceCurrentDensity:
        """Create a SurfaceCurrentDensity object."""
        return SurfaceCurrentDensity(i_x=i_x, i_y=i_y, surface_normal=normal)

    @maxwell_cite(
        656,
        657,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Calculate surface current from volume current",
    )
    def from_volume_current(
        self,
        J: np.ndarray,
        thickness: float,
    ) -> SurfaceCurrentDensity:
        """Convert volume current to surface current."""
        return SurfaceCurrentDensity.from_volume_current(J, thickness)

    @maxwell_cite(
        658,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Calculate magnetic field from surface current",
    )
    def calc_field(
        self,
        surface_current: SurfaceCurrentDensity,
        point: np.ndarray,
    ) -> dict:
        """Calculate B field at observation point."""
        return calc_field_from_surface_current(surface_current, point)

    @maxwell_cite(
        657,
        658,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Verify boundary condition",
    )
    def verify_boundary(
        self,
        surface_current: SurfaceCurrentDensity,
        H_above: np.ndarray,
        H_below: np.ndarray,
    ) -> dict:
        """Verify electromagnetic boundary condition."""
        return calc_sheet_boundary_condition(surface_current, H_above, H_below)

    @maxwell_cite(
        659,
        660,
        661,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Analyze skin effect",
    )
    def analyze_skin_effect(
        self,
        frequency: float,
        thickness: float,
        applied_field: float,
    ) -> dict:
        """Analyze skin effect in conductor."""
        if self.conductivity <= 0:
            raise ValueError("Conductivity must be set for skin effect analysis")

        return analyze_surface_current_distribution(
            conductivity=self.conductivity,
            frequency=frequency,
            thickness=thickness,
            applied_field=applied_field,
        )

    @maxwell_cite(
        662,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Calculate surface impedance",
    )
    def surface_impedance(self, frequency: float) -> dict:
        """Calculate surface impedance at given frequency."""
        if self.conductivity <= 0:
            raise ValueError("Conductivity must be set for impedance calculation")

        return calc_surface_impedance(
            conductivity=self.conductivity,
            frequency=frequency,
            permeability=self.permeability,
        )

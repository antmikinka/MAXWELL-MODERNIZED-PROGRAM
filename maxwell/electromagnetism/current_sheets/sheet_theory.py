"""
Current-Sheet Theory — Maxwell's mathematical theory of surface current distributions.

Implements Maxwell's theory of current-sheets from Articles 647-655:

- Current-sheet definition and properties (Art. 647)
- Magnetic shell equivalence (Art. 648-649)
- Vector potential of current-sheet (Art. 650)
- Field discontinuities across sheet (Art. 651)
- Self-induction of current-sheets (Art. 652-653)
- Interaction between current-sheets (Art. 654-655)

A current-sheet is a surface distribution of electric current, mathematically
treated as a surface current density i (current per unit width perpendicular
to flow direction). This idealization is useful for:

- Thin conducting films and foils
- Wound coils approximated as continuous distributions
- Magnetic materials modeled as bound surface currents
- Boundary condition analysis in electromagnetism

CGS Units:
    i = surface current density (abamperes/cm)
    A = vector potential (gauss-cm)
    B = magnetic flux density (gauss)
    L = inductance (cm in CGS)

Category: A (maxwell_original) — Maxwell's theory of current-sheets.

References:
    Part IV, Ch XII: Current-Sheets (Arts. 647-674).
    Part IV, Arts. 647-655: Mathematical theory of current-sheets.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class CurrentSheet:
    """
    Current-sheet — surface distribution of electric current.

    Art. 647: A current-sheet is a surface across which the tangential
    component of the magnetic field is discontinuous. The surface current
    density i (abamperes/cm) is related to this discontinuity by:

        n̂ × (H₂ - H₁) = 4πi/c

    where n̂ is the unit normal from side 1 to side 2.

    For a flat sheet in the xy-plane with current flowing in x-direction:
        i = (i_x, i_y) = surface current density vector
        B_z is continuous across the sheet
        B_x, B_y are discontinuous

    Attributes:
        surface_current: Surface current density vector i (abamperes/cm).
        surface_normal: Unit normal vector to the sheet.
        area: Total area of the sheet (cm²).
        position: Position of sheet center (cm).
    """

    surface_current: np.ndarray = field(default_factory=lambda: np.zeros(2))
    surface_normal: np.ndarray = field(
        default_factory=lambda: np.array([0.0, 0.0, 1.0])
    )
    area: float = 0.0
    position: np.ndarray = field(default_factory=lambda: np.zeros(3))

    def __post_init__(self):
        """Validate and normalize parameters."""
        self.surface_normal = np.asarray(self.surface_normal, dtype=np.float64)
        norm = np.linalg.norm(self.surface_normal)
        if norm > 0:
            self.surface_normal = self.surface_normal / norm
        else:
            raise ValueError("Surface normal cannot be zero")

        self.position = np.asarray(self.position, dtype=np.float64)

        if self.area <= 0:
            raise ValueError(f"Area must be positive, got {self.area}")

        # Extend 2D surface current to 3D (in sheet plane)
        if len(self.surface_current) == 2:
            # For xy-plane, current has x and y components
            self.current_3d = np.array(
                [float(self.surface_current[0]), float(self.surface_current[1]), 0.0]
            )
        else:
            self.current_3d = np.asarray(self.surface_current, dtype=np.float64)

    @property
    def current_magnitude(self) -> float:
        """Magnitude of surface current density (abamperes/cm)."""
        return float(np.linalg.norm(self.current_3d))

    @classmethod
    @maxwell_cite(
        647,
        648,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Create current-sheet from surface current density",
    )
    def from_surface_current(
        cls,
        current_x: float,
        current_y: float,
        normal: np.ndarray = None,
        area: float = 1.0,
        position: np.ndarray = None,
    ) -> CurrentSheet:
        """
        Create a current-sheet from surface current density components.

        Art. 647-648: A current-sheet is defined by its surface current
        density, which is the current per unit width perpendicular to
        the flow direction.

        Args:
            current_x: Surface current density in x-direction (abamperes/cm).
            current_y: Surface current density in y-direction (abamperes/cm).
            normal: Unit normal to sheet (default: z-axis).
            area: Sheet area (cm², default: 1).
            position: Center position (cm, default: origin).

        Returns:
            CurrentSheet object.

        Reference:
            Part IV, Arts. 647-648: Current-sheet definition.
        """
        if normal is None:
            normal = np.array([0.0, 0.0, 1.0])
        if position is None:
            position = np.zeros(3)

        return cls(
            surface_current=np.array([current_x, current_y]),
            surface_normal=normal,
            area=area,
            position=position,
        )


@dataclass
class MagneticShell:
    """
    Magnetic shell — equivalent to a current-sheet at the boundary.

    Art. 648-649: A magnetic shell is a surface distribution of magnetic
    matter that produces the same external field as a current-sheet.
    The strength of the shell φ (magnetic potential difference) is
    related to the current by:

        φ = i / c

    where i is the current per unit length and c is the speed of light.

    This equivalence allows magnetic problems to be solved using either
    current distributions or magnetic pole distributions.

    Attributes:
        shell_strength: Magnetic potential jump φ (gauss-cm).
        surface_normal: Unit normal to the shell surface.
        position: Position of shell center (cm).
    """

    shell_strength: float = 0.0
    surface_normal: np.ndarray = field(
        default_factory=lambda: np.array([0.0, 0.0, 1.0])
    )
    position: np.ndarray = field(default_factory=lambda: np.zeros(3))

    def __post_init__(self):
        """Validate and normalize."""
        self.surface_normal = np.asarray(self.surface_normal, dtype=np.float64)
        norm = np.linalg.norm(self.surface_normal)
        if norm > 0:
            self.surface_normal = self.surface_normal / norm
        self.position = np.asarray(self.position, dtype=np.float64)

    @classmethod
    @maxwell_cite(
        648,
        649,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Create magnetic shell equivalent to current-sheet",
    )
    def from_current_sheet(cls, sheet: CurrentSheet) -> MagneticShell:
        """
        Create magnetic shell equivalent to a current-sheet.

        Art. 648-649: Every current-sheet has an equivalent magnetic
        shell that produces identical external magnetic fields. The
        shell strength is:

            φ = I / c

        where I is the total current and c is the speed of light.

        Args:
            sheet: CurrentSheet object.

        Returns:
            MagneticShell object with equivalent field.

        Reference:
            Part IV, Arts. 648-649: Magnetic shell equivalence.
        """
        # Shell strength = current magnitude / c
        shell_strength = sheet.current_magnitude / CONST.C

        return cls(
            shell_strength=shell_strength,
            surface_normal=sheet.surface_normal,
            position=sheet.position,
        )

    @classmethod
    @maxwell_cite(
        648,
        649,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Create magnetic shell from current per unit length",
    )
    def from_current_per_length(
        cls,
        current_per_length: float,
        normal: np.ndarray = None,
        position: np.ndarray = None,
    ) -> MagneticShell:
        """
        Create magnetic shell from current per unit length.

        Art. 648: The strength of a magnetic shell is proportional to
        the current it replaces:

            φ = i / c

        Args:
            current_per_length: Current per unit length (abamperes).
            normal: Unit normal to shell (default: z-axis).
            position: Shell position (default: origin).

        Returns:
            MagneticShell object.

        Reference:
            Part IV, Art. 648: Shell strength from current.
        """
        if normal is None:
            normal = np.array([0.0, 0.0, 1.0])
        if position is None:
            position = np.zeros(3)

        shell_strength = current_per_length / CONST.C

        return cls(
            shell_strength=shell_strength,
            surface_normal=normal,
            position=position,
        )


@maxwell_cite(
    647,
    650,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Calculate magnetic field discontinuity across current-sheet",
)
def calc_sheet_field_discontinuity(
    sheet: CurrentSheet,
) -> dict[str, np.ndarray | float]:
    """
    Calculate the magnetic field discontinuity across a current-sheet.

    Art. 647, 650: The boundary condition at a current-sheet relates
    the discontinuity in tangential H to the surface current:

        n̂ × (H₂ - H₁) = (4π/c) · i

    For a sheet in xy-plane with current i = (i_x, i_y):
        H₂_x - H₁_x = -(4π/c) · i_y
        H₂_y - H₁_y = (4π/c) · i_x

    The normal component of B is continuous:
        B₂_z = B₁_z

    Args:
        sheet: CurrentSheet object.

    Returns:
        Dictionary with:
        - delta_H_tangential: Discontinuity in H (oersted)
        - delta_B_tangential: Discontinuity in B (gauss)
        - boundary_condition: The vector equation n̂ × ΔH = (4π/c)i

    Reference:
        Part IV, Arts. 647, 650: Field discontinuity at current-sheet.

    Example:
        >>> sheet = CurrentSheet.from_surface_current(100, 0, area=1.0)
        >>> result = calc_sheet_field_discontinuity(sheet)
        >>> print(f"ΔH_y = {result['delta_H_tangential'][1]} oersted")
    """
    n = sheet.surface_normal
    i = sheet.current_3d

    # Boundary condition: n × (H₂ - H₁) = (4π/c) · i
    # Solving for ΔH = H₂ - H₁:
    # ΔH_tangential = -(4π/c) · (n × i)

    factor = 4.0 * np.pi / CONST.C
    delta_H = -factor * np.cross(n, i)

    # For B field (in vacuum or non-magnetic media):
    delta_B = delta_H  # B = H in CGS-Gaussian vacuum

    return {
        "delta_H_tangential": delta_H,
        "delta_B_tangential": delta_B,
        "boundary_condition": n,
        "factor": factor,
        "current_magnitude": sheet.current_magnitude,
    }


@maxwell_cite(
    648,
    649,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Calculate magnetic scalar potential of magnetic shell",
)
def calc_magnetic_shell_potential(
    shell: MagneticShell,
    observation_point: np.ndarray,
) -> dict[str, float | np.ndarray]:
    """
    Calculate magnetic scalar potential of a magnetic shell.

    Art. 648-649: The magnetic scalar potential Ω at a point due to
    a magnetic shell of strength φ is:

        Ω = φ · ω / (4π)

    where ω is the solid angle subtended by the shell at the point.

    For a circular shell of radius a at distance z along axis:
        ω = 2π · (1 - z / √(z² + a²))

    The potential has a discontinuity of φ across the shell.

    Args:
        shell: MagneticShell object.
        observation_point: Point where potential is evaluated (cm).

    Returns:
        Dictionary with:
        - potential: Magnetic scalar potential Ω (gauss-cm)
        - solid_angle: Solid angle ω (steradians)
        - distance: Distance from shell (cm)
        - field: Magnetic field H = -∇Ω (oersted)

    Reference:
        Part IV, Arts. 648-649: Magnetic shell potential.

    Example:
        >>> shell = MagneticShell(shell_strength=1.0, position=np.zeros(3))
        >>> result = calc_magnetic_shell_potential(shell, np.array([0, 0, 10]))
        >>> print(f"Ω = {result['potential']} gauss-cm")
    """
    obs = np.asarray(observation_point, dtype=np.float64)
    pos = shell.position

    # Vector from shell to observation point
    r_vec = obs - pos
    r_mag = np.linalg.norm(r_vec)

    if r_mag < 1e-10:
        # At the shell itself — potential is discontinuous
        return {
            "potential": 0.0,
            "solid_angle": 2 * np.pi,  # Half the full solid angle
            "distance": 0.0,
            "field": np.zeros(3),
            "warning": "At shell position — potential discontinuous",
        }

    # Unit vector from shell to point
    r_hat = r_vec / r_mag

    # Solid angle (approximate for small shell or distant point)
    # For a flat shell of area A: ω ≈ A · cos(θ) / r²
    # where θ is angle between normal and line of sight
    cos_theta = np.dot(shell.surface_normal, r_hat)

    # For a shell of unit area (simplified model)
    area = 1.0  # Could be made into a parameter
    solid_angle = area * cos_theta / (r_mag**2)

    # Magnetic scalar potential
    potential = shell.shell_strength * solid_angle / (4.0 * np.pi)

    # Magnetic field H = -∇Ω
    # For a dipole-like shell: H ≈ (shell_strength / r³) · [3(n·r̂)r̂ - n]
    field_magnitude = shell.shell_strength / (r_mag**3)
    field = field_magnitude * (3 * cos_theta * r_hat - shell.surface_normal)

    return {
        "potential": potential,
        "solid_angle": solid_angle,
        "distance": r_mag,
        "field": field,
        "cos_theta": cos_theta,
    }


@maxwell_cite(
    650,
    651,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Calculate vector potential of current-sheet",
)
def calc_sheet_vector_potential(
    sheet: CurrentSheet,
    observation_point: np.ndarray,
) -> dict[str, np.ndarray | float]:
    """
    Calculate vector potential A of a current-sheet.

    Art. 650: The vector potential A at a point due to a current-sheet
    is given by the surface integral:

        A(r) = (1/c) · ∫∫ i(r') / |r - r'| dS'

    For a small sheet or distant point, this approximates to:

        A ≈ (I · area) / (c · r)

    where I is the total current and r is the distance.

    The magnetic field is obtained from: B = ∇ × A

    Args:
        sheet: CurrentSheet object.
        observation_point: Point where A is evaluated (cm).

    Returns:
        Dictionary with:
        - vector_potential: A (gauss-cm)
        - distance: Distance from sheet (cm)
        - field_B: Magnetic field B = ∇ × A (gauss)

    Reference:
        Part IV, Art. 650: Vector potential of current-sheet.

    Example:
        >>> sheet = CurrentSheet.from_surface_current(100, 0, area=1.0)
        >>> result = calc_sheet_vector_potential(sheet, np.array([0, 0, 10]))
        >>> print(f"A = {result['vector_potential']} gauss-cm")
    """
    obs = np.asarray(observation_point, dtype=np.float64)
    pos = sheet.position

    r_vec = obs - pos
    r_mag = np.linalg.norm(r_vec)

    if r_mag < 1e-10:
        return {
            "vector_potential": np.zeros(3),
            "distance": 0.0,
            "field_B": np.zeros(3),
            "warning": "At sheet position — singular",
        }

    r_hat = r_vec / r_mag

    # Vector potential (dipole approximation)
    # A = (μ₀/4π) · (m × r̂) / r² in SI
    # In CGS: A = (m × r̂) / (c · r²) where m = I·area/c

    # Magnetic moment of sheet
    moment_magnitude = sheet.current_magnitude * sheet.area / CONST.C

    # A = (m × r̂) / r²
    # For current in xy-plane, moment is in z-direction
    m_vec = moment_magnitude * sheet.surface_normal
    A = np.cross(m_vec, r_hat) / (r_mag**2)

    # Magnetic field from curl of A (dipole field)
    # B = (3(m·r̂)r̂ - m) / r³
    m_dot_r = np.dot(m_vec, r_hat)
    B = (3 * m_dot_r * r_hat - m_vec) / (r_mag**3)

    return {
        "vector_potential": A,
        "distance": r_mag,
        "field_B": B,
        "magnetic_moment": moment_magnitude,
    }


@maxwell_cite(
    652,
    653,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Calculate self-inductance of circular current-sheet",
)
def calc_sheet_inductance(
    radius: float,
    num_turns: int = 1,
) -> dict[str, float]:
    """
    Calculate self-inductance of a circular current-sheet.

    Art. 652-653: For a circular current-sheet (or coil) of radius a
    with N turns, the self-inductance is approximately:

        L ≈ 4π² · N² · a² / l

    where l is the effective length (for a thin sheet, l ≈ 2πa).

    For a single circular loop (N=1):
        L ≈ 4π · a · [ln(8a/r_wire) - 2]

    where r_wire is the wire radius (for finite thickness).

    In CGS, inductance has dimensions of length (centimeters).

    Args:
        radius: Radius of circular sheet (cm).
        num_turns: Number of equivalent turns (default: 1).

    Returns:
        Dictionary with:
        - inductance: Self-inductance L (cm in CGS)
        - radius: Sheet radius (cm)
        - num_turns: Number of turns

    Reference:
        Part IV, Arts. 652-653: Self-induction of current-sheets.

    Example:
        >>> result = calc_sheet_inductance(radius=10.0, num_turns=100)
        >>> print(f"L = {result['inductance']} cm")
    """
    if radius <= 0:
        raise ValueError(f"Radius must be positive, got {radius}")
    if num_turns <= 0:
        raise ValueError(f"Number of turns must be positive, got {num_turns}")

    # Approximate formula for circular current-sheet
    # L ≈ 4π² · N² · a (for a thin circular sheet)
    # More accurate: L ≈ 4π² · N² · a² / l where l is axial length

    # For a single loop, use the logarithmic formula
    if num_turns == 1:
        # Approximate wire radius as fraction of loop radius
        wire_radius = radius * 0.01  # Assume thin wire
        L = 4.0 * np.pi * radius * (np.log(8 * radius / wire_radius) - 2.0)
    else:
        # Multi-turn sheet (solenoid-like)
        # Assume sheet length ≈ 2πa (one layer)
        length = 2.0 * np.pi * radius
        L = 4.0 * np.pi * (num_turns**2) * (radius**2) / length

    return {
        "inductance": L,
        "radius": radius,
        "num_turns": num_turns,
        "formula": "circular_sheet_approximation",
    }


@maxwell_cite(
    648,
    649,
    650,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Verify magnetic shell equivalence to current-sheet",
)
def verify_shell_equivalence(
    sheet: CurrentSheet,
    observation_point: np.ndarray,
    tolerance: float = 1e-10,
) -> dict[str, bool | dict | float]:
    """
    Verify that a magnetic shell produces the same field as the equivalent current-sheet.

    Art. 648-650: A current-sheet and its equivalent magnetic shell should
    produce identical magnetic fields at all external points. This function
    verifies the equivalence by comparing:

    1. Vector potential from current-sheet
    2. Scalar potential gradient from magnetic shell

    The fields should match within numerical tolerance.

    Args:
        sheet: CurrentSheet object.
        observation_point: Point for field comparison (cm).
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with:
        - equivalent: True if fields match within tolerance
        - sheet_field: B field from current-sheet
        - shell_field: H field from magnetic shell
        - field_difference: Magnitude of difference
        - shell: The equivalent MagneticShell object

    Reference:
        Part IV, Arts. 648-650: Current-sheet / magnetic shell equivalence.

    Example:
        >>> sheet = CurrentSheet.from_surface_current(100, 0, area=1.0)
        >>> result = verify_shell_equivalence(sheet, np.array([0, 0, 10]))
        >>> assert result['equivalent']
    """
    obs = np.asarray(observation_point, dtype=np.float64)

    # Create equivalent shell
    shell = MagneticShell.from_current_sheet(sheet)

    # Calculate field from current-sheet (via vector potential)
    sheet_result = calc_sheet_vector_potential(sheet, obs)
    B_sheet = sheet_result["field_B"]

    # Calculate field from magnetic shell (via scalar potential)
    shell_result = calc_magnetic_shell_potential(shell, obs)
    H_shell = shell_result["field"]

    # In vacuum, B = H (CGS-Gaussian)
    field_diff = np.linalg.norm(B_sheet - H_shell)
    field_mag = max(np.linalg.norm(B_sheet), np.linalg.norm(H_shell), 1.0)

    equivalent = field_diff < tolerance * field_mag

    return {
        "equivalent": equivalent,
        "sheet_field": B_sheet,
        "shell_field": H_shell,
        "field_difference": field_diff,
        "relative_error": field_diff / field_mag,
        "shell": shell,
    }


@maxwell_cite(
    654,
    655,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="Calculate interaction between two current-sheets",
)
def calc_sheet_interaction(
    sheet1: CurrentSheet,
    sheet2: CurrentSheet,
) -> dict[str, float | np.ndarray]:
    """
    Calculate electromagnetic interaction between two current-sheets.

    Art. 654-655: The mutual inductance M between two current-sheets
    determines their electromagnetic coupling. The force between them
    is proportional to the product of currents and the gradient of M.

    For two parallel circular sheets of radius a, separated by distance d:
        M ≈ (4π² · a⁴) / (2 · d³)  (for d >> a)

    The potential energy of interaction is:
        U = -M · I₁ · I₂ / c²

    Args:
        sheet1: First CurrentSheet object.
        sheet2: Second CurrentSheet object.

    Returns:
        Dictionary with:
        - mutual_inductance: M (cm in CGS)
        - interaction_energy: U (ergs) for given currents
        - separation: Distance between sheets (cm)
        - force_estimate: Approximate force (dynes)

    Reference:
        Part IV, Arts. 654-655: Interaction between current-sheets.

    Example:
        >>> s1 = CurrentSheet.from_surface_current(100, 0, area=1.0,
        ...                                         position=np.zeros(3))
        >>> s2 = CurrentSheet.from_surface_current(100, 0, area=1.0,
        ...                                         position=np.array([0, 0, 10]))
        >>> result = calc_sheet_interaction(s1, s2)
        >>> print(f"M = {result['mutual_inductance']} cm")
    """
    r1 = sheet1.position
    r2 = sheet2.position

    # Separation vector and distance
    r_vec = r2 - r1
    d = np.linalg.norm(r_vec)

    if d < 1e-10:
        return {
            "mutual_inductance": 0.0,
            "interaction_energy": 0.0,
            "separation": 0.0,
            "warning": "Sheets at same position — undefined",
        }

    r_hat = r_vec / d

    # Mutual inductance (dipole approximation)
    # M ≈ (μ₀/4π) · (m₁ · m₂ - 3(m₁·r̂)(m₂·r̂)) / d³
    # In CGS: M ≈ (1/c²) · [m₁·m₂ - 3(m₁·r̂)(m₂·r̂)] / d³

    # Magnetic moments
    m1 = sheet1.current_magnitude * sheet1.area / CONST.C
    m2 = sheet2.current_magnitude * sheet2.area / CONST.C

    # Dot products with normal vectors
    n1 = sheet1.surface_normal
    n2 = sheet2.surface_normal

    n1_dot_n2 = np.dot(n1, n2)
    n1_dot_r = np.dot(n1, r_hat)
    n2_dot_r = np.dot(n2, r_hat)

    # Mutual inductance formula
    M = (m1 * m2 / (CONST.C * d**3)) * (n1_dot_n2 - 3 * n1_dot_r * n2_dot_r)

    # Interaction energy (for unit currents)
    I1 = sheet1.current_magnitude
    I2 = sheet2.current_magnitude
    U = -M * I1 * I2 / CONST.C

    # Force estimate (gradient of energy)
    # F ≈ dU/dd = 3M·I₁·I₂ / d
    F_mag = 3.0 * abs(M) * I1 * I2 / d if d > 0 else 0.0

    return {
        "mutual_inductance": M,
        "interaction_energy": U,
        "separation": d,
        "force_estimate": F_mag,
        "separation_direction": r_hat,
    }


@dataclass
class CurrentSheetCalculator:
    """
    Unified calculator for current-sheet electromagnetic problems.

    Art. 647-655: This class provides a complete interface for
    current-sheet calculations including field computation,
    inductance, and interactions.

    Attributes:
        default_normal: Default surface normal vector.
        default_area: Default sheet area (cm²).
    """

    default_normal: np.ndarray = field(
        default_factory=lambda: np.array([0.0, 0.0, 1.0])
    )
    default_area: float = 1.0

    @maxwell_cite(
        647,
        648,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Create current-sheet with specified parameters",
    )
    def create_sheet(
        self,
        current_x: float,
        current_y: float,
        normal: np.ndarray = None,
        area: float = None,
        position: np.ndarray = None,
    ) -> CurrentSheet:
        """Create a current-sheet with specified parameters."""
        return CurrentSheet.from_surface_current(
            current_x=current_x,
            current_y=current_y,
            normal=normal or self.default_normal,
            area=area or self.default_area,
            position=position if position is not None else np.zeros(3),
        )

    @maxwell_cite(
        648,
        649,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Create equivalent magnetic shell",
    )
    def create_shell(self, sheet: CurrentSheet) -> MagneticShell:
        """Create magnetic shell equivalent to current-sheet."""
        return MagneticShell.from_current_sheet(sheet)

    @maxwell_cite(
        647,
        650,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Calculate field discontinuity",
    )
    def field_discontinuity(self, sheet: CurrentSheet) -> dict:
        """Calculate field discontinuity across current-sheet."""
        return calc_sheet_field_discontinuity(sheet)

    @maxwell_cite(
        648,
        649,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Calculate shell potential",
    )
    def shell_potential(
        self,
        shell: MagneticShell,
        point: np.ndarray,
    ) -> dict:
        """Calculate magnetic scalar potential of shell."""
        return calc_magnetic_shell_potential(shell, point)

    @maxwell_cite(
        650,
        651,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Calculate vector potential",
    )
    def vector_potential(
        self,
        sheet: CurrentSheet,
        point: np.ndarray,
    ) -> dict:
        """Calculate vector potential of current-sheet."""
        return calc_sheet_vector_potential(sheet, point)

    @maxwell_cite(
        652,
        653,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Calculate self-inductance",
    )
    def self_inductance(self, radius: float, num_turns: int = 1) -> dict:
        """Calculate self-inductance of circular current-sheet."""
        return calc_sheet_inductance(radius, num_turns)

    @maxwell_cite(
        648,
        649,
        650,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Verify shell equivalence",
    )
    def verify_equivalence(
        self,
        sheet: CurrentSheet,
        point: np.ndarray,
    ) -> dict:
        """Verify magnetic shell equivalence."""
        return verify_shell_equivalence(sheet, point)

    @maxwell_cite(
        654,
        655,
        part=4,
        chapter="Current-Sheets",
        theory_class="maxwell_original",
        description="Calculate sheet interaction",
    )
    def interaction(self, sheet1: CurrentSheet, sheet2: CurrentSheet) -> dict:
        """Calculate interaction between two current-sheets."""
        return calc_sheet_interaction(sheet1, sheet2)

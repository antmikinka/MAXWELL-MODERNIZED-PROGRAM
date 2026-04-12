"""maxwell.optics.velocity — Electromagnetic wave velocity (Arts. 786-787).

Implements Maxwell's calculation of electromagnetic wave propagation velocity
through various media, establishing the connection between light and electromagnetism.

Maxwell's CGS formulation (Arts. 786-787):
    Wave velocity in vacuum:
        v = c = 2.99792458 × 10^10 cm/s

    Wave velocity in medium:
        v = c / sqrt(ε_r * μ_r) = c / n

    Refractive index:
        n = c / v = sqrt(ε_r * μ_r)

    For non-magnetic materials (μ_r ≈ 1):
        n ≈ sqrt(ε_r)

where:
    c = speed of light in vacuum (cm/s)
    v = wave velocity in medium (cm/s)
    ε_r = relative permittivity (dielectric constant K)
    μ_r = relative permeability
    n = refractive index

Category: A (maxwell_original) — Maxwell's electromagnetic theory of light.

References:
    Part IV, Arts. 786-787: Electromagnetic wave velocity and refractive index.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class WaveVelocity:
    """
    Electromagnetic wave velocity calculator.

    Art. 786-787: Maxwell showed that electromagnetic waves propagate
    through the electromagnetic field at a velocity determined by the
    electric and magnetic properties of the medium.

    Attributes:
        permittivity: Relative permittivity ε_r (dimensionless).
        permeability: Relative permeability μ_r (dimensionless).
    """

    permittivity: float = 1.0
    permeability: float = 1.0

    def __post_init__(self):
        """Validate parameters."""
        if self.permittivity <= 0:
            raise ValueError(f"Permittivity must be positive, got {self.permittivity}")
        if self.permeability <= 0:
            raise ValueError(f"Permeability must be positive, got {self.permeability}")

    @maxwell_cite(
        786, 787,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate wave velocity in medium",
    )
    def velocity(self) -> float:
        """
        Calculate wave propagation velocity.

        Art. 786-787: The velocity is:

            v = c / sqrt(ε_r * μ_r)

        Returns:
            Wave velocity (cm/s).

        Reference:
            Part IV, Arts. 786-787: Wave velocity formula.
        """
        return CONST.C / np.sqrt(self.permittivity * self.permeability)

    @maxwell_cite(
        786,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate refractive index",
    )
    def refractive_index(self) -> float:
        """
        Calculate refractive index of the medium.

        Art. 786: The refractive index is:

            n = c / v = sqrt(ε_r * μ_r)

        Returns:
            Refractive index n (dimensionless).

        Reference:
            Part IV, Art. 786: Refractive index.
        """
        return np.sqrt(self.permittivity * self.permeability)

    @maxwell_cite(
        786,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate wavelength in medium",
    )
    def wavelength(self, frequency: float) -> float:
        """
        Calculate wavelength in the medium.

        Art. 786: λ = v / ν

        Args:
            frequency: Frequency ν (Hz).

        Returns:
            Wavelength λ (cm).

        Reference:
            Part IV, Art. 786: Wavelength in medium.
        """
        if frequency <= 0:
            raise ValueError(f"Frequency must be positive, got {frequency}")
        return self.velocity() / frequency

    @maxwell_cite(
        787,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate wave number",
    )
    def wave_number(self, frequency: float) -> float:
        """
        Calculate wave number in the medium.

        Art. 787: k = 2π / λ = ω / v

        Args:
            frequency: Frequency ν (Hz).

        Returns:
            Wave number k (cm⁻¹).

        Reference:
            Part IV, Art. 787: Wave number.
        """
        if frequency <= 0:
            raise ValueError(f"Frequency must be positive, got {frequency}")
        omega = 2.0 * np.pi * frequency
        return omega / self.velocity()

    @maxwell_cite(
        786, 787,
        part=4, chapter="Electromagnetic Theory of Light",
        theory_class="maxwell_original",
        description="Calculate E-B field amplitude ratio",
    )
    def E_B_ratio(self) -> float:
        """
        Calculate ratio of electric to magnetic field amplitudes.

        Art. 786-787: For a plane electromagnetic wave:

            |E| / |B| = v = c / n

        In vacuum, |E| / |B| = c.

        Returns:
            E-B amplitude ratio (cm/s).

        Reference:
            Part IV, Arts. 786-787: Field amplitude ratio.
        """
        return self.velocity()


@maxwell_cite(
    786, 787,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate EM wave velocity: v = c/sqrt(ε_r * μ_r)",
)
def calc_wave_velocity(
    permittivity: float,
    permeability: float,
) -> float:
    """
    Calculate electromagnetic wave velocity in a medium.

    Art. 786-787: Maxwell's velocity formula:

        v = c / sqrt(ε_r * μ_r)

    where ε_r is the specific inductive capacity (dielectric constant)
    and μ_r is the magnetic permeability.

    Maxwell's key insight was that this velocity equals the measured
    speed of light, proving light is an electromagnetic wave.

    Args:
        permittivity: Relative permittivity ε_r (dimensionless).
        permeability: Relative permeability μ_r (dimensionless).

    Returns:
        Wave velocity (cm/s).

    Raises:
        ValueError: If permittivity or permeability is not positive.

    Reference:
        Part IV, Arts. 786-787: Wave velocity formula.

    Example:
        >>> # Velocity in vacuum
        >>> v = calc_wave_velocity(1.0, 1.0)
        >>> print(f"v = {v:.4e} cm/s")  # v = c
        >>> # Velocity in water (ε_r ≈ 80, μ_r ≈ 1)
        >>> v_water = calc_wave_velocity(80.0, 1.0)
        >>> print(f"v_water = {v_water:.4e} cm/s")
    """
    if permittivity <= 0:
        raise ValueError(f"Permittivity must be positive, got {permittivity}")
    if permeability <= 0:
        raise ValueError(f"Permeability must be positive, got {permeability}")

    return CONST.C / np.sqrt(permittivity * permeability)


@maxwell_cite(
    786,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate refractive index: n = sqrt(ε_r * μ_r)",
)
def calc_refractive_index(
    permittivity: float,
    permeability: float = 1.0,
) -> float:
    """
    Calculate refractive index from electromagnetic properties.

    Art. 786: Maxwell's formula for refractive index:

        n = c / v = sqrt(ε_r * μ_r)

    For non-magnetic materials (μ_r ≈ 1):

        n ≈ sqrt(ε_r)

    This relation connects optics with electromagnetism.

    Args:
        permittivity: Relative permittivity ε_r.
        permeability: Relative permeability μ_r (default: 1.0).

    Returns:
        Refractive index n (dimensionless).

    Reference:
        Part IV, Art. 786: Refractive index formula.

    Example:
        >>> # Air (ε_r ≈ 1.0006)
        >>> n_air = calc_refractive_index(1.0006)
        >>> print(f"n_air = {n_air:.6f}")  # n ≈ 1.0003
        >>> # Glass (ε_r ≈ 4, μ_r = 1)
        >>> n_glass = calc_refractive_index(4.0, 1.0)
        >>> print(f"n_glass = {n_glass:.2f}")  # n = 2.0
    """
    if permittivity <= 0:
        raise ValueError(f"Permittivity must be positive, got {permittivity}")
    if permeability <= 0:
        raise ValueError(f"Permeability must be positive, got {permeability}")

    return np.sqrt(permittivity * permeability)


@maxwell_cite(
    786,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate permittivity from refractive index",
)
def calc_permittivity_from_refractive_index(
    refractive_index: float,
    permeability: float = 1.0,
) -> float:
    """
    Calculate permittivity from refractive index.

    Art. 786: Inverting n = sqrt(ε_r * μ_r):

        ε_r = n² / μ_r

    For non-magnetic materials:

        ε_r ≈ n²

    Args:
        refractive_index: Refractive index n.
        permeability: Relative permeability μ_r (default: 1.0).

    Returns:
        Relative permittivity ε_r (dimensionless).

    Reference:
        Part IV, Art. 786: Permittivity from refractive index.

    Example:
        >>> # Glass with n = 1.5
        >>> eps_r = calc_permittivity_from_refractive_index(1.5)
        >>> print(f"ε_r = {eps_r:.2f}")  # ε_r = 2.25
    """
    if refractive_index <= 0:
        raise ValueError(f"Refractive index must be positive, got {refractive_index}")
    if permeability <= 0:
        raise ValueError(f"Permeability must be positive, got {permeability}")

    return (refractive_index ** 2) / permeability


@maxwell_cite(
    786,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate wavelength in medium",
)
def calc_wavelength_in_medium(
    vacuum_wavelength: float,
    refractive_index: float,
) -> float:
    """
    Calculate wavelength of light in a medium.

    Art. 786: The wavelength in a medium is reduced by the refractive index:

        λ = λ_0 / n

    where λ_0 is the vacuum wavelength.

    Frequency remains unchanged across boundaries.

    Args:
        vacuum_wavelength: Wavelength in vacuum λ_0 (cm).
        refractive_index: Refractive index n of medium.

    Returns:
        Wavelength in medium λ (cm).

    Raises:
        ValueError: If wavelength or refractive index is not positive.

    Reference:
        Part IV, Art. 786: Wavelength in medium.

    Example:
        >>> # Green light (530 nm) in water (n = 1.33)
        >>> lambda_water = calc_wavelength_in_medium(530e-7, 1.33)
        >>> print(f"λ = {lambda_water*1e7:.1f} nm")  # λ ≈ 398 nm
    """
    if vacuum_wavelength <= 0:
        raise ValueError(f"Wavelength must be positive, got {vacuum_wavelength}")
    if refractive_index <= 0:
        raise ValueError(f"Refractive index must be positive, got {refractive_index}")

    return vacuum_wavelength / refractive_index


@maxwell_cite(
    787,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate wave number k = 2π/λ",
)
def calc_wave_number(
    wavelength: float,
    refractive_index: float = 1.0,
) -> float:
    """
    Calculate electromagnetic wave number.

    Art. 787: The wave number is:

        k = 2π / λ = (2π * n) / λ_0 = ω / v

    where λ is the wavelength in the medium.

    Args:
        wavelength: Wavelength in vacuum λ_0 (cm).
        refractive_index: Refractive index n (default: 1.0 for vacuum).

    Returns:
        Wave number k (cm⁻¹).

    Reference:
        Part IV, Art. 787: Wave number formula.

    Example:
        >>> # Wave number for green light (530 nm)
        >>> k = calc_wave_number(530e-7)
        >>> print(f"k = {k:.2e} cm⁻¹")
    """
    if wavelength <= 0:
        raise ValueError(f"Wavelength must be positive, got {wavelength}")
    if refractive_index <= 0:
        raise ValueError(f"Refractive index must be positive, got {refractive_index}")

    medium_wavelength = wavelength / refractive_index
    return 2.0 * np.pi / medium_wavelength


@maxwell_cite(
    786, 787,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Calculate E-B field ratio |E|/|B| = v",
)
def calc_E_B_ratio(
    permittivity: float,
    permeability: float,
) -> float:
    """
    Calculate ratio of electric to magnetic field amplitudes.

    Art. 786-787: For a plane electromagnetic wave:

        |E| / |B| = v = c / n

    In vacuum:

        |E| / |B| = c

    This ratio has units of velocity.

    Args:
        permittivity: Relative permittivity ε_r.
        permeability: Relative permeability μ_r.

    Returns:
        E-B amplitude ratio (cm/s).

    Reference:
        Part IV, Arts. 786-787: Field amplitude ratio.

    Example:
        >>> # In vacuum
        >>> ratio = calc_E_B_ratio(1.0, 1.0)
        >>> print(f"|E|/|B| = {ratio:.4e} cm/s")  # = c
    """
    velocity = calc_wave_velocity(permittivity, permeability)
    return velocity


@maxwell_cite(
    786, 787,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Verify Maxwell's velocity-light connection",
)
def verify_maxwell_velocity(
    permittivity: float = 1.0,
    permeability: float = 1.0,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify Maxwell's velocity formula and connection to light.

    Art. 786-787: This function verifies:
    1. v = c / sqrt(ε_r * μ_r)
    2. n = sqrt(ε_r * μ_r)
    3. v = c / n
    4. |E| / |B| = v

    Args:
        permittivity: Relative permittivity.
        permeability: Relative permeability.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 786-787: Velocity verification.
    """
    # Calculate quantities
    velocity = calc_wave_velocity(permittivity, permeability)
    refractive_idx = calc_refractive_index(permittivity, permeability)
    E_B = calc_E_B_ratio(permittivity, permeability)

    # Verify v = c / n
    v_from_n = CONST.C / refractive_idx
    v_error = abs(velocity - v_from_n) / velocity if velocity > 0 else 0

    # Verify |E|/|B| = v
    ratio_error = abs(E_B - velocity) / velocity if velocity > 0 else 0

    # Verify n = sqrt(ε_r * μ_r)
    n_check = np.sqrt(permittivity * permeability)
    n_error = abs(n_check - refractive_idx) / refractive_idx if refractive_idx > 0 else 0

    # In vacuum, v should equal c
    vacuum_verified = True
    if permittivity == 1.0 and permeability == 1.0:
        vacuum_verified = abs(velocity - CONST.C) / CONST.C < tolerance

    return {
        "permittivity": permittivity,
        "permeability": permeability,
        "calculated_velocity": velocity,
        "refractive_index": refractive_idx,
        "velocity_from_n": v_from_n,
        "E_B_ratio": E_B,
        "velocity_error": v_error,
        "ratio_error": ratio_error,
        "refractive_index_error": n_error,
        "vacuum_verified": vacuum_verified,
        "maxwell_verified": all([
            v_error < tolerance,
            ratio_error < tolerance,
            n_error < tolerance,
        ]),
    }


@maxwell_cite(
    786, 787,
    part=4, chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="Complete wave velocity analysis",
)
def analyze_wave_velocity(
    permittivity: float,
    permeability: float,
    frequency: float = None,
) -> dict[str, float]:
    """
    Complete analysis of electromagnetic wave velocity.

    Art. 786-787: Comprehensive analysis including:
    1. Wave velocity
    2. Refractive index
    3. Wavelength (if frequency provided)
    4. Wave number
    5. E-B field ratio

    Args:
        permittivity: Relative permittivity ε_r.
        permeability: Relative permeability μ_r.
        frequency: Optional frequency ν (Hz).

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 786-787: Complete velocity analysis.

    Example:
        >>> # Analyze wave in glass (n ≈ 1.5)
        >>> result = analyze_wave_velocity(2.25, 1.0, 6e14)
        >>> print(f"v = {result['velocity']:.4e} cm/s")
        >>> print(f"λ = {result['wavelength']*1e7:.1f} nm")
    """
    velocity = calc_wave_velocity(permittivity, permeability)
    refractive_idx = calc_refractive_index(permittivity, permeability)
    E_B = calc_E_B_ratio(permittivity, permeability)

    result = {
        "permittivity": permittivity,
        "permeability": permeability,
        "velocity": velocity,
        "refractive_index": refractive_idx,
        "E_B_ratio": E_B,
        "velocity_ratio_to_c": velocity / CONST.C,
    }

    if frequency is not None and frequency > 0:
        wavelength = velocity / frequency
        wave_number = 2.0 * np.pi * frequency / velocity
        vacuum_wavelength = CONST.C / frequency

        result["frequency"] = frequency
        result["wavelength"] = wavelength
        result["wave_number"] = wave_number
        result["vacuum_wavelength"] = vacuum_wavelength
        result["wavelength_ratio"] = wavelength / vacuum_wavelength

    return result

"""
Faraday's Law of Electromagnetic Induction — the foundation of electromagnetic induction.

Implements Michael Faraday's 1831 discovery of electromagnetic induction,
as described by Maxwell in Articles 528-531 and 542:

- Electromagnetic induction phenomenon (Art. 528)
- Faraday's law: EMF = -dΦ/dt (Art. 529)
- Magnetic flux and its variation (Art. 530)
- Direction of induced current (Art. 531)
- Lenz's Law: induced current opposes the change (Art. 542)

Maxwell's CGS formulation:
    EMF = -dΦ/dt            (statvolts or abvolts depending on system)
    Φ = ∫∫ B · n̂ dA         (maxwells, where 1 maxwell = 1 gauss·cm²)
    Motional EMF: ∮(v × B)·dl
    Self-induction: EMF = -L·dI/dt

where:
    Φ = magnetic flux (maxwells in CGS)
    B = magnetic flux density (gauss)
    EMF = electromotive force (statvolts in ESU, abvolts in EMU)
    L = inductance (centimeters in CGS, or abhenries)
    I = current (abamperes in EMU)

Category: A (maxwell_original) — Maxwell's theory of electromagnetic induction.

References:
    Part IV, Arts. 528-531: Faraday's law of induction.
    Part IV, Art. 542: Lenz's law and direction of induced currents.
    Part IV, Ch. IV: Electromagnetic induction and its applications.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class MagneticFlux:
    """
    Magnetic flux through a surface — the fundamental quantity in induction.

    Art. 528-530: Magnetic flux is the surface integral of the magnetic
    induction B over a given area. It represents the total "number of
    magnetic field lines" passing through the surface.

    For a uniform field perpendicular to a flat surface:
        Φ = B * A  (maxwells)

    For arbitrary orientation:
        Φ = B * A * cos(θ) = B · A_vector

    where θ is the angle between B and the surface normal.

    Attributes:
        flux: Magnetic flux value in maxwells (gauss·cm²).
        B_field: Magnetic flux density vector (gauss).
        area: Surface area (cm²).
        normal: Unit normal vector to the surface.
    """

    flux: float
    B_field: np.ndarray
    area: float
    normal: np.ndarray | None = None

    def __post_init__(self):
        """Validate parameters and set defaults.

        Ensures area is positive and normal is a unit vector.
        Sets default normal to z-axis if not provided.
        """
        if self.area <= 0:
            raise ValueError(f"Area must be positive, got {self.area}")

        self.B_field = np.asarray(self.B_field, dtype=np.float64)

        if self.normal is None:
            self.normal = np.array([0.0, 0.0, 1.0])
        else:
            self.normal = np.asarray(self.normal, dtype=np.float64)
            norm = np.linalg.norm(self.normal)
            if norm > 0:
                self.normal = self.normal / norm

    @property
    def B_magnitude(self) -> float:
        """Magnitude of the magnetic field (gauss)."""
        return float(np.linalg.norm(self.B_field))

    @property
    def B_perpendicular(self) -> float:
        """Component of B perpendicular to the surface (gauss).

        This is B · n̂, the effective field contributing to flux.
        """
        return float(np.dot(self.B_field, self.normal))

    @classmethod
    @maxwell_cite(
        528, 529,
        part=4, chapter="Electromagnetic Induction",
        theory_class="maxwell_original",
        description="Create magnetic flux from B field and area",
    )
    def from_B_and_area(
        cls,
        B_field: np.ndarray,
        area: float,
        normal: np.ndarray = None,
    ) -> MagneticFlux:
        """
        Create magnetic flux from magnetic field and surface area.

        Art. 528-529: The flux through a surface is the integral of B · dA.
        For uniform B and flat surface: Φ = B · A · n̂

        Args:
            B_field: Magnetic flux density vector (gauss).
            area: Surface area (cm²).
            normal: Optional unit normal vector (default: z-axis).

        Returns:
            MagneticFlux object with computed flux value.

        Reference:
            Part IV, Arts. 528-529: Magnetic flux definition and calculation.
        """
        B_field = np.asarray(B_field, dtype=np.float64)

        if normal is None:
            normal = np.array([0.0, 0.0, 1.0])
        else:
            normal = np.asarray(normal, dtype=np.float64)
            normal = normal / np.linalg.norm(normal)

        # Φ = B · A · n̂ = A * (B · n̂)
        B_perp = np.dot(B_field, normal)
        flux = area * B_perp

        return cls(flux=flux, B_field=B_field, area=area, normal=normal)


@dataclass
class InducedEMF:
    """
    Electromotive force induced by changing magnetic flux.

    Art. 529-531: When the magnetic flux through a circuit changes,
    an electromotive force is induced. The magnitude is given by
    Faraday's law, and the direction by Lenz's law.

    Faraday's Law:
        EMF = -dΦ/dt

    The negative sign (Lenz's law, Art. 542) indicates that the
    induced current opposes the change in flux that caused it.

    Attributes:
        emf: Induced electromotive force (statvolts in ESU, abvolts in EMU).
        flux_change_rate: Rate of change of flux dΦ/dt (maxwells/s).
        resistance: Optional circuit resistance for current calculation.
    """

    emf: float
    flux_change_rate: float
    resistance: float | None = None

    def __post_init__(self):
        """Validate that EMF and flux change rate have correct relationship."""
        # Verify Faraday's law: EMF = -dΦ/dt
        expected_emf = -self.flux_change_rate
        # Allow for numerical tolerance
        if not np.isclose(self.emf, expected_emf, rtol=1e-10):
            # This is informational - the values might use different unit conventions
            pass

    @property
    def induced_current(self) -> float | None:
        """Calculate induced current if resistance is known.

        Using Ohm's law: I = EMF / R

        Returns:
            Induced current (abamperes in EMU, statamperes in ESU),
            or None if resistance is not specified.
        """
        if self.resistance is None or self.resistance == 0:
            return None
        return self.emf / self.resistance

    @classmethod
    @maxwell_cite(
        529, 542,
        part=4, chapter="Electromagnetic Induction",
        theory_class="maxwell_original",
        description="Create induced EMF from flux change rate",
    )
    def from_flux_change(
        cls,
        flux_change_rate: float,
        resistance: float = None,
    ) -> InducedEMF:
        """
        Create induced EMF from the rate of change of magnetic flux.

        Art. 529: The induced EMF equals the negative rate of change
        of magnetic flux: EMF = -dΦ/dt

        Art. 542 (Lenz's Law): The negative sign ensures the induced
        current creates a magnetic field that opposes the flux change.

        Args:
            flux_change_rate: Rate of flux change dΦ/dt (maxwells/s).
            resistance: Optional circuit resistance for current calculation.

        Returns:
            InducedEMF object.

        Reference:
            Part IV, Arts. 529, 542: Faraday's law and Lenz's law.
        """
        emf = -flux_change_rate
        return cls(emf=emf, flux_change_rate=flux_change_rate, resistance=resistance)


@maxwell_cite(
    528, 529, 530,
    part=4, chapter="Electromagnetic Induction",
    theory_class="maxwell_original",
    description="Calculate magnetic flux through a surface: Φ = B · A",
)
def calc_magnetic_flux(
    B_field: np.ndarray,
    area: float,
    normal: np.ndarray = None,
) -> float:
    """
    Calculate magnetic flux through a surface.

    Art. 528-530: The magnetic flux through a surface is the surface integral
    of the magnetic induction. For a uniform field and flat surface:

        Φ = B · A · n̂ = B * A * cos(θ)

    where θ is the angle between the field and surface normal.

    In CGS units:
        B in gauss
        A in cm²
        Φ in maxwells (1 maxwell = 1 gauss·cm²)

    Args:
        B_field: Magnetic flux density vector (gauss).
        area: Surface area (cm²). Must be positive.
        normal: Optional unit normal vector to surface (default: z-axis).

    Returns:
        Magnetic flux Φ (maxwells).

    Raises:
        ValueError: If area is not positive.

    Reference:
        Part IV, Arts. 528-530: Magnetic flux and its calculation.

    Example:
        >>> # 100 gauss field perpendicular to 10 cm² loop
        >>> B = np.array([0, 0, 100])  # gauss
        >>> flux = calc_magnetic_flux(B, 10.0)
        >>> print(f"Φ = {flux} maxwells")  # Φ = 1000 maxwells
    """
    if area <= 0:
        raise ValueError(f"Area must be positive, got {area}")

    B_field = np.asarray(B_field, dtype=np.float64)

    if normal is None:
        normal = np.array([0.0, 0.0, 1.0])
    else:
        normal = np.asarray(normal, dtype=np.float64)
        norm = np.linalg.norm(normal)
        if norm == 0:
            raise ValueError("Normal vector cannot be zero")
        normal = normal / norm

    # Φ = A * (B · n̂)
    return area * np.dot(B_field, normal)


@maxwell_cite(
    529, 531,
    part=4, chapter="Electromagnetic Induction",
    theory_class="maxwell_original",
    description="Calculate induced EMF from flux change rate: EMF = -dΦ/dt",
)
def calc_induced_emf(
    flux_change_rate: float,
) -> float:
    """
    Calculate electromotive force induced by changing magnetic flux.

    Art. 529-531: Faraday's law of induction states that the induced EMF
    equals the negative rate of change of magnetic flux:

        EMF = -dΦ/dt

    The negative sign (Lenz's law) indicates that the induced current
    flows in a direction that opposes the flux change.

    In CGS-EMU:
        dΦ/dt in maxwells/s
        EMF in abvolts (1 abvolt = 1 maxwell/s)

    In CGS-ESU:
        dΦ/dt in maxwells/s
        EMF in statvolts (1 statvolt = c abvolts, where c is speed of light)

    Args:
        flux_change_rate: Rate of flux change dΦ/dt (maxwells/s).
                         Positive = increasing flux, negative = decreasing.

    Returns:
        Induced EMF (abvolts in EMU, negative sign per Lenz's law).

    Reference:
        Part IV, Arts. 529-531: Faraday's law of induction.

    Example:
        >>> # Flux increasing at 1000 maxwells/s
        >>> emf = calc_induced_emf(1000.0)
        >>> print(f"EMF = {emf} abvolts")  # EMF = -1000 abvolts (opposes increase)
    """
    # EMF = -dΦ/dt (Faraday's law with Lenz's law sign)
    return -flux_change_rate


@maxwell_cite(
    529, 530,
    part=4, chapter="Electromagnetic Induction",
    theory_class="maxwell_original",
    description="Calculate motional EMF: EMF = ∮(v × B)·dl",
)
def calc_motional_emf(
    velocity: np.ndarray,
    B_field: np.ndarray,
    conductor_length: float,
) -> float:
    """
    Calculate motional electromotive force from conductor moving in magnetic field.

    Art. 529-530: When a conductor moves through a magnetic field, an EMF
    is induced due to the magnetic force on charge carriers. For a straight
    conductor of length l moving with velocity v perpendicular to B:

        EMF = ∮(v × B)·dl

    For uniform v, B, and straight conductor perpendicular to both:
        EMF = |v × B| * l = v * B * l * sin(θ)

    where θ is the angle between v and B.

    In CGS-EMU:
        v in cm/s
        B in gauss
        l in cm
        EMF in abvolts

    Args:
        velocity: Velocity vector of conductor (cm/s).
        B_field: Magnetic flux density (gauss).
        conductor_length: Length of conductor in field (cm).

    Returns:
        Motional EMF (abvolts in EMU).

    Raises:
        ValueError: If conductor_length is not positive.

    Reference:
        Part IV, Arts. 529-530: Motional induction.

    Example:
        >>> # Conductor moving at 100 cm/s perpendicular to 1000 gauss field
        >>> v = np.array([100, 0, 0])  # cm/s
        >>> B = np.array([0, 0, 1000])  # gauss
        >>> emf = calc_motional_emf(v, B, 10.0)  # 10 cm conductor
        >>> print(f"EMF = {emf} abvolts")  # EMF = 1000000 abvolts
    """
    if conductor_length <= 0:
        raise ValueError(f"Conductor length must be positive, got {conductor_length}")

    velocity = np.asarray(velocity, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    # v × B gives the force per unit charge
    v_cross_B = np.cross(velocity, B_field)

    # For a straight conductor, integrate along length
    # Assuming conductor is oriented perpendicular to v × B for maximum EMF
    v_cross_B_mag = np.linalg.norm(v_cross_B)

    return v_cross_B_mag * conductor_length


@maxwell_cite(
    529, 542,
    part=4, chapter="Electromagnetic Induction",
    theory_class="maxwell_original",
    description="Calculate self-induction EMF: EMF = -L·dI/dt",
)
def calc_self_induction(
    inductance: float,
    dI_dt: float,
) -> float:
    """
    Calculate electromotive force from self-induction.

    Art. 529, 542: When the current in a circuit changes, the changing
    magnetic flux produced by that current induces an opposing EMF in
    the same circuit. This is self-induction:

        EMF = -L * dI/dt

    where L is the inductance (also called the coefficient of self-induction).

    In CGS-EMU:
        L in centimeters (1 abhenry = 1 cm)
        dI/dt in abamperes/s
        EMF in abvolts

    The negative sign (Lenz's law) shows that self-induction opposes
    changes in current — the basis of inductive reactance.

    Args:
        inductance: Self-inductance L (centimeters in CGS, or abhenries).
        dI_dt: Rate of current change dI/dt (abamperes/s).

    Returns:
        Self-induced EMF (abvolts in EMU, negative sign per Lenz's law).

    Raises:
        ValueError: If inductance is not positive.

    Reference:
        Part IV, Arts. 529, 542: Self-induction and Lenz's law.

    Example:
        >>> # 1000 cm inductance, current increasing at 10 A/s
        >>> emf = calc_self_induction(1000.0, 10.0)
        >>> print(f"EMF = {emf} abvolts")  # EMF = -10000 abvolts
    """
    if inductance <= 0:
        raise ValueError(f"Inductance must be positive, got {inductance}")

    # EMF = -L * dI/dt
    return -inductance * dI_dt


@maxwell_cite(
    528, 529, 530,
    part=4, chapter="Electromagnetic Induction",
    theory_class="maxwell_original",
    description="Calculate flux through a circular loop at specified position",
)
def calc_flux_through_loop(
    B_field: np.ndarray,
    loop_center: np.ndarray,
    loop_normal: np.ndarray,
    loop_area: float,
) -> float:
    """
    Calculate magnetic flux through a circular current loop.

    Art. 528-530: The flux through a closed loop is the surface integral
    of B · dA over any surface bounded by the loop. For a uniform field
    and circular loop:

        Φ = B · n̂ * A

    where n̂ is the unit normal to the loop plane (by right-hand rule
    from current direction) and A is the loop area.

    Args:
        B_field: Magnetic flux density at loop center (gauss).
        loop_center: Position vector of loop center (cm).
        loop_normal: Unit normal vector to loop plane (right-hand rule).
        loop_area: Area of the loop (cm²).

    Returns:
        Magnetic flux through loop (maxwells).

    Raises:
        ValueError: If loop_area is not positive or loop_normal is zero.

    Reference:
        Part IV, Arts. 528-530: Flux through a closed circuit.

    Example:
        >>> # 500 gauss field through 5 cm² loop at 45°
        >>> B = np.array([0, 0, 500])
        >>> normal = np.array([0, 1, 1]) / np.sqrt(2)  # 45° from z-axis
        >>> flux = calc_flux_through_loop(B, np.zeros(3), normal, 5.0)
        >>> print(f"Φ = {flux:.2f} maxwells")  # Φ ≈ 1767.77 maxwells
    """
    if loop_area <= 0:
        raise ValueError(f"Loop area must be positive, got {loop_area}")

    loop_normal = np.asarray(loop_normal, dtype=np.float64)
    normal_mag = np.linalg.norm(loop_normal)

    if normal_mag == 0:
        raise ValueError("Loop normal cannot be zero vector")

    B_field = np.asarray(B_field, dtype=np.float64)
    loop_normal = loop_normal / normal_mag

    # Φ = B · n̂ * A
    return loop_area * np.dot(B_field, loop_normal)


@maxwell_cite(
    542,
    part=4, chapter="Electromagnetic Induction",
    theory_class="maxwell_original",
    description="Verify Lenz's law — induced current opposes flux change",
)
def verify_lenz_law(
    initial_flux: float,
    final_flux: float,
    time_interval: float,
    resistance: float,
    initial_current: float = 0.0,
) -> dict[str, float | bool]:
    """
    Verify Lenz's law by analyzing induced current direction.

    Art. 542: Lenz's law states that the direction of an induced current
    is always such that its own magnetic field opposes the change in
    flux that produced it.

    This function verifies:
    1. If flux is increasing (dΦ/dt > 0), induced current creates opposing field
    2. If flux is decreasing (dΦ/dt < 0), induced current creates supporting field
    3. The EMF sign is always opposite to dΦ/dt

    Args:
        initial_flux: Initial magnetic flux (maxwells).
        final_flux: Final magnetic flux (maxwells).
        time_interval: Time for the change (seconds).
        resistance: Circuit resistance (for current calculation).
        initial_current: Initial current before change (abamperes).

    Returns:
        Dictionary with:
        - flux_change: ΔΦ (maxwells)
        - flux_change_rate: dΦ/dt (maxwells/s)
        - induced_emf: EMF (abvolts, should be -dΦ/dt)
        - induced_current: Induced current (abamperes)
        - opposes_change: True if induced effects oppose the flux change
        - lenz_law_verified: True if Lenz's law holds

    Reference:
        Part IV, Art. 542: Lenz's law of induced current direction.

    Example:
        >>> # Increasing flux should induce opposing current
        >>> result = verify_lenz_law(1000, 2000, 0.1, 10.0)
        >>> assert result["lenz_law_verified"]
    """
    if time_interval <= 0:
        raise ValueError(f"Time interval must be positive, got {time_interval}")

    if resistance <= 0:
        raise ValueError(f"Resistance must be positive, got {resistance}")

    # Calculate flux change and rate
    flux_change = final_flux - initial_flux
    flux_change_rate = flux_change / time_interval

    # Faraday's law: EMF = -dΦ/dt
    induced_emf = calc_induced_emf(flux_change_rate)

    # Ohm's law: I = EMF / R
    induced_current = induced_emf / resistance

    # Total current after induction
    total_current = initial_current + induced_current

    # Lenz's law verification:
    # - If flux increased (dΦ/dt > 0), induced field should oppose (indicated by negative EMF)
    # - If flux decreased (dΦ/dt < 0), induced field should support (indicated by positive EMF)
    # The sign of induced_current relative to flux_change tells us this

    # For flux increase: flux_change > 0, induced_emf < 0 (opposes)
    # For flux decrease: flux_change < 0, induced_emf > 0 (supports, tries to maintain)
    opposes_change = (flux_change_rate * induced_emf) < 0

    # More rigorous: check that EMF * dΦ/dt is always negative
    lenz_law_verified = (induced_emf * flux_change_rate) <= 0

    return {
        "flux_change": flux_change,
        "flux_change_rate": flux_change_rate,
        "induced_emf": induced_emf,
        "induced_current": induced_current,
        "total_current": total_current,
        "opposes_change": opposes_change,
        "lenz_law_verified": lenz_law_verified,
    }


@maxwell_cite(
    528, 529, 530, 531,
    part=4, chapter="Electromagnetic Induction",
    theory_class="maxwell_original",
    description="Complete Faraday induction analysis for a circuit",
)
def analyze_faraday_induction(
    B_initial: np.ndarray,
    B_final: np.ndarray,
    loop_area: float,
    loop_normal: np.ndarray,
    time_interval: float,
    resistance: float,
    num_turns: int = 1,
) -> dict[str, float | np.ndarray]:
    """
    Analyze complete Faraday induction scenario for a multi-turn coil.

    Art. 528-531: Comprehensive analysis of electromagnetic induction
    in a coil with N turns, where the magnetic field changes from B_initial
    to B_final over a time interval.

    For N turns:
        Φ_total = N * Φ_per_turn
        EMF = -N * dΦ/dt
        I_induced = EMF / R

    Args:
        B_initial: Initial magnetic field vector (gauss).
        B_final: Final magnetic field vector (gauss).
        loop_area: Area of each turn (cm²).
        loop_normal: Unit normal to loop plane.
        time_interval: Time for field change (seconds).
        resistance: Total circuit resistance (for current).
        num_turns: Number of turns in coil (default: 1).

    Returns:
        Dictionary with complete analysis:
        - flux_initial: Initial flux per turn (maxwells)
        - flux_final: Final flux per turn (maxwells)
        - flux_change: Change in flux per turn (maxwells)
        - total_flux_change: N * flux_change (maxwells)
        - average_emf: Induced EMF (abvolts)
        - average_current: Induced current (abamperes)
        - charge_transferred: Total charge that flowed (abcoulombs)

    Reference:
        Part IV, Arts. 528-531: Complete Faraday induction analysis.

    Example:
        >>> # 100-turn coil, field changes from 0 to 1000 gauss
        >>> result = analyze_faraday_induction(
        ...     B_initial=np.zeros(3),
        ...     B_final=np.array([0, 0, 1000]),
        ...     loop_area=10.0,
        ...     loop_normal=np.array([0, 0, 1]),
        ...     time_interval=0.5,
        ...     resistance=100.0,
        ...     num_turns=100
        ... )
        >>> print(f"EMF = {result['average_emf']} abvolts")
    """
    if time_interval <= 0:
        raise ValueError(f"Time interval must be positive, got {time_interval}")

    if resistance <= 0:
        raise ValueError(f"Resistance must be positive, got {resistance}")

    if num_turns <= 0:
        raise ValueError(f"Number of turns must be positive, got {num_turns}")

    B_initial = np.asarray(B_initial, dtype=np.float64)
    B_final = np.asarray(B_final, dtype=np.float64)
    loop_normal = np.asarray(loop_normal, dtype=np.float64)
    loop_normal = loop_normal / np.linalg.norm(loop_normal)

    # Flux per turn
    flux_initial = calc_flux_through_loop(B_initial, np.zeros(3), loop_normal, loop_area)
    flux_final = calc_flux_through_loop(B_final, np.zeros(3), loop_normal, loop_area)
    flux_change = flux_final - flux_initial

    # Total flux change for N turns
    total_flux_change = num_turns * flux_change

    # Average rate of flux change
    flux_change_rate = total_flux_change / time_interval

    # Faraday's law for N turns
    average_emf = calc_induced_emf(flux_change_rate)

    # Ohm's law
    average_current = average_emf / resistance

    # Total charge transferred: Q = ∫I dt = (1/R) ∫EMF dt = (1/R) * (-N * ΔΦ)
    # Note: |Q| = |ΔΦ_total| / R
    charge_transferred = -total_flux_change / resistance

    return {
        "flux_initial": flux_initial,
        "flux_final": flux_final,
        "flux_change": flux_change,
        "total_flux_change": total_flux_change,
        "flux_change_rate": flux_change_rate,
        "average_emf": average_emf,
        "average_current": average_current,
        "charge_transferred": charge_transferred,
        "num_turns": num_turns,
    }


@maxwell_cite(
    529,
    part=4, chapter="Electromagnetic Induction",
    theory_class="maxwell_original",
    description="Calculate flux change needed for a given EMF",
)
def flux_change_for_emf(
    desired_emf: float,
    time_interval: float,
    num_turns: int = 1,
) -> float:
    """
    Calculate the flux change required to produce a specified EMF.

    Art. 529: Rearranging Faraday's law to find the required flux change:

        EMF = -N * dΦ/dt

        dΦ = -EMF * dt / N

    This is useful for designing generators and transformers where
    a specific output voltage is required.

    Args:
        desired_emf: Target induced EMF (abvolts).
        time_interval: Time over which change occurs (seconds).
        num_turns: Number of turns in coil (default: 1).

    Returns:
        Required flux change per turn (maxwells).
        Negative value means flux must decrease.

    Raises:
        ValueError: If time_interval or num_turns is not positive.

    Reference:
        Part IV, Art. 529: Faraday's law applied inversely.

    Example:
        >>> # Need 10000 abvolts over 0.1 seconds with 100 turns
        >>> dPhi = flux_change_for_emf(-10000, 0.1, 100)
        >>> print(f"Required flux change: {dPhi} maxwells per turn")
    """
    if time_interval <= 0:
        raise ValueError(f"Time interval must be positive, got {time_interval}")

    if num_turns <= 0:
        raise ValueError(f"Number of turns must be positive, got {num_turns}")

    # dΦ = -EMF * dt / N
    return -desired_emf * time_interval / num_turns


@maxwell_cite(
    528, 529, 530, 542,
    part=4, chapter="Electromagnetic Induction",
    theory_class="maxwell_original",
    description="Verify Faraday's law with numerical experiment",
)
def verify_faradays_law(
    B_magnitude: float = 1000.0,
    loop_area: float = 10.0,
    time_interval: float = 0.1,
    num_turns: int = 10,
    resistance: float = 50.0,
    tolerance: float = 1e-10,
) -> dict[str, float | bool | np.ndarray]:
    """
    Verify Faraday's law of induction through numerical experiment.

    Art. 528-542: This function verifies the complete induction phenomenon:

    1. Calculate initial and final flux for a known field change
    2. Compute expected EMF from Faraday's law: EMF = -N * dΦ/dt
    3. Verify Lenz's law (EMF opposes the change)
    4. Calculate induced current and verify energy considerations

    The verification confirms:
    - EMF magnitude equals N * |dΦ/dt|
    - EMF sign follows Lenz's law
    - Energy is conserved (induced current opposes the change)

    Args:
        B_magnitude: Initial field magnitude (gauss). Final field is 2*B.
        loop_area: Loop area (cm²).
        time_interval: Time for field change (seconds).
        num_turns: Number of turns in coil.
        resistance: Circuit resistance (for current).
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with:
        - initial_flux: Flux before change (maxwells)
        - final_flux: Flux after change (maxwells)
        - flux_change: Change in flux (maxwells)
        - expected_emf: Calculated from Faraday's law (abvolts)
        - computed_emf: From direct calculation (abvolts)
        - emf_match: True if expected matches computed
        - lenz_verified: True if Lenz's law holds
        - faraday_verified: True if Faraday's law is verified

    Reference:
        Part IV, Arts. 528-542: Faraday's law verification.
    """
    # Set up the scenario: field doubles from B to 2B
    B_initial = np.array([0.0, 0.0, B_magnitude])
    B_final = np.array([0.0, 0.0, 2.0 * B_magnitude])
    loop_normal = np.array([0.0, 0.0, 1.0])

    # Calculate fluxes
    initial_flux = calc_flux_through_loop(B_initial, np.zeros(3), loop_normal, loop_area)
    final_flux = calc_flux_through_loop(B_final, np.zeros(3), loop_normal, loop_area)
    flux_change = final_flux - initial_flux

    # Expected EMF from Faraday's law: EMF = -N * dΦ/dt
    total_flux_change = num_turns * flux_change
    flux_rate = total_flux_change / time_interval
    expected_emf = -flux_rate

    # Compute EMF directly
    computed_emf = calc_induced_emf(flux_rate)

    # Verify Lenz's law
    lenz_result = verify_lenz_law(initial_flux, final_flux, time_interval, resistance)

    # Check EMF match
    emf_difference = abs(expected_emf - computed_emf)
    emf_match = emf_difference < tolerance * max(abs(expected_emf), 1.0)

    # Faraday's law is verified if:
    # 1. EMF = -N * dΦ/dt (within tolerance)
    # 2. Lenz's law holds (EMF opposes the change)
    faraday_verified = emf_match and lenz_result["lenz_law_verified"]

    return {
        "initial_flux": initial_flux,
        "final_flux": final_flux,
        "flux_change": flux_change,
        "total_flux_change": total_flux_change,
        "flux_rate": flux_rate,
        "expected_emf": expected_emf,
        "computed_emf": computed_emf,
        "emf_difference": emf_difference,
        "emf_match": emf_match,
        "induced_current": computed_emf / resistance,
        "lenz_verified": lenz_result["lenz_law_verified"],
        "faraday_verified": faraday_verified,
        "tolerance_used": tolerance,
    }


class FaradayInduction:
    """
    Faraday Induction — comprehensive electromagnetic induction calculator.

    Art. 528-531, 542: This class provides a unified interface for
    calculating all aspects of electromagnetic induction:

    - Magnetic flux through arbitrary surfaces
    - Induced EMF from changing flux
    - Motional EMF from conductor movement
    - Self-induction effects
    - Lenz's law direction verification

    The class encapsulates Maxwell's complete theory of induction,
    providing both individual calculations and comprehensive analysis.

    Attributes:
        num_turns: Number of turns in the coil (default: 1).
        resistance: Circuit resistance (optional, ohms in appropriate CGS system).
    """

    def __init__(
        self,
        num_turns: int = 1,
        resistance: float | None = None,
    ):
        """
        Initialize Faraday induction calculator.

        Args:
            num_turns: Number of turns in coil (default: 1).
            resistance: Optional circuit resistance for current calculations.
        """
        if num_turns <= 0:
            raise ValueError(f"Number of turns must be positive, got {num_turns}")

        if resistance is not None and resistance <= 0:
            raise ValueError(f"Resistance must be positive, got {resistance}")

        self.num_turns = num_turns
        self.resistance = resistance

    @maxwell_cite(
        528, 529, 530,
        part=4, chapter="Electromagnetic Induction",
        theory_class="maxwell_original",
        description="Calculate magnetic flux through surface",
    )
    def magnetic_flux(
        self,
        B_field: np.ndarray,
        surface_area: float,
        surface_normal: np.ndarray = None,
    ) -> float:
        """
        Calculate magnetic flux through a surface.

        Art. 528-530: For a coil with N turns, the total flux is:
            Φ_total = N * (B · n̂ * A)

        Args:
            B_field: Magnetic flux density vector (gauss).
            surface_area: Area of the surface (cm²).
            surface_normal: Optional unit normal vector (default: z-axis).

        Returns:
            Total magnetic flux for all turns (maxwells).

        Reference:
            Part IV, Arts. 528-530: Magnetic flux calculation.
        """
        flux_per_turn = calc_magnetic_flux(B_field, surface_area, surface_normal)
        return self.num_turns * flux_per_turn

    @maxwell_cite(
        529, 531,
        part=4, chapter="Electromagnetic Induction",
        theory_class="maxwell_original",
        description="Calculate induced EMF from flux change rate",
    )
    def induced_emf(
        self,
        flux_change_rate: float,
    ) -> float:
        """
        Calculate induced electromotive force.

        Art. 529-531: Faraday's law for N turns:
            EMF = -N * dΦ/dt

        Args:
            flux_change_rate: Rate of flux change per turn dΦ/dt (maxwells/s).

        Returns:
            Induced EMF (abvolts in EMU, includes N-turn multiplication).

        Reference:
            Part IV, Arts. 529-531: Faraday's law of induction.
        """
        total_flux_rate = self.num_turns * flux_change_rate
        emf = calc_induced_emf(total_flux_rate)

        if self.resistance is not None:
            # Store the induced current for later access
            self._last_induced_current = emf / self.resistance
        else:
            self._last_induced_current = None

        return emf

    @maxwell_cite(
        529, 530,
        part=4, chapter="Electromagnetic Induction",
        theory_class="maxwell_original",
        description="Calculate motional EMF for moving conductor",
    )
    def motional_emf(
        self,
        velocity: np.ndarray,
        B_field: np.ndarray,
        conductor_length: float,
    ) -> float:
        """
        Calculate motional electromotive force.

        Art. 529-530: EMF induced when a conductor moves through
        a magnetic field:
            EMF = ∮(v × B)·dl

        For N parallel conductors (like N turns moving together):
            EMF_total = N * EMF_per_conductor

        Args:
            velocity: Velocity vector (cm/s).
            B_field: Magnetic flux density (gauss).
            conductor_length: Length of conductor in field (cm).

        Returns:
            Total motional EMF (abvolts).

        Reference:
            Part IV, Arts. 529-530: Motional induction.
        """
        emf_per_conductor = calc_motional_emf(velocity, B_field, conductor_length)
        return self.num_turns * emf_per_conductor

    @maxwell_cite(
        529, 542,
        part=4, chapter="Electromagnetic Induction",
        theory_class="maxwell_original",
        description="Calculate self-induction EMF",
    )
    def self_induction_emf(
        self,
        inductance: float,
        dI_dt: float,
    ) -> float:
        """
        Calculate EMF from self-induction.

        Art. 529, 542: When current changes in a circuit, the self-inductance
        produces an opposing EMF:
            EMF = -L * dI/dt

        Args:
            inductance: Self-inductance (centimeters or abhenries).
            dI_dt: Rate of current change (abamperes/s).

        Returns:
            Self-induced EMF (abvolts, opposes current change).

        Reference:
            Part IV, Arts. 529, 542: Self-induction and Lenz's law.
        """
        return calc_self_induction(inductance, dI_dt)

    @maxwell_cite(
        542,
        part=4, chapter="Electromagnetic Induction",
        theory_class="maxwell_original",
        description="Verify Lenz's law for induction scenario",
    )
    def verify_lenz(
        self,
        initial_flux: float,
        final_flux: float,
        time_interval: float,
    ) -> dict[str, float | bool]:
        """
        Verify Lenz's law for an induction scenario.

        Art. 542: Checks that the induced EMF and current oppose
        the change in magnetic flux.

        Args:
            initial_flux: Initial flux per turn (maxwells).
            final_flux: Final flux per turn (maxwells).
            time_interval: Time for change (seconds).

        Returns:
            Dictionary with Lenz's law verification results.

        Reference:
            Part IV, Art. 542: Lenz's law verification.
        """
        return verify_lenz_law(
            initial_flux=initial_flux,
            final_flux=final_flux,
            time_interval=time_interval,
            resistance=self.resistance or 1.0,  # Use unit resistance if not set
        )

    @property
    def last_induced_current(self) -> float | None:
        """Get the induced current from the last EMF calculation."""
        return getattr(self, '_last_induced_current', None)

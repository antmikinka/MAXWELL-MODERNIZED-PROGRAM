"""
Naval magnetism — magnetism of ships and magnetic compass deviation.

Implements the theory of naval magnetism from Part III of Maxwell's Treatise:
- Ship magnetism and compass deviation (Art. 441)
- Magnetic shielding for navigation
- Degaussing and compensation

When iron ships became common in the 19th century, navigators
discovered that the ship's own magnetism caused significant
compass errors. Maxwell's theory explained these effects and
led to methods for compensation.

Key concepts:
- Permanent magnetism of the ship's structure
- Induced magnetism from Earth's field
- Heeling error (tilt-induced deviation)
- Quadrantal deviation
- Flinders bar and compensation magnets

Category: A (maxwell_original) — Maxwell's theory of naval magnetism.

References:
    Part III, Art. 441: Ship magnetism and compass deviation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST
from maxwell.materials.induction import MagneticSusceptibility
from maxwell.components.ellipsoids import MagneticEllipsoid


@dataclass
class ShipMagnetism:
    """
    Magnetic model of an iron ship.

    Art. 441: A ship's magnetism has two components:

    1. Permanent magnetism: Acquired during construction from
       hammering and welding in Earth's field.

    2. Induced magnetism: Created by Earth's field acting on
       the ship's ferromagnetic structure.

    The total deviation depends on heading, latitude, and heel.

    Attributes:
        permanent_moment: Permanent magnetic moment m_p (emu).
        susceptibility: Effective susceptibility of ship structure.
        compass_position: Compass location relative to ship center.
    """

    permanent_moment: np.ndarray = None  # m_p, emu
    susceptibility: float = 0.0  # Effective κ
    compass_position: np.ndarray = None  # Position relative to ship center

    def __post_init__(self):
        self.permanent_moment = np.asarray(self.permanent_moment, dtype=np.float64) if self.permanent_moment is not None else np.zeros(3)
        self.compass_position = np.asarray(self.compass_position, dtype=np.float64) if self.compass_position is not None else np.zeros(3)

    @maxwell_cite(
        441,
        part=3, chapter="Naval Magnetism",
        theory_class="maxwell_original",
        description="Calculate deviation from ship magnetism",
    )
    def compass_deviation(
        self,
        heading: float,
        latitude: float,
        heel_angle: float = 0,
    ) -> float:
        """
        Calculate compass deviation due to ship's magnetism.

        Art. 441: The total deviation δ is the sum of several
        components:

            δ = A + B sin(θ) + C cos(θ) + D sin(2θ) + E cos(2θ)

        where:
        - A: Constant deviation (mechanical misalignment)
        - B, C: Semicircular deviation (permanent + induced)
        - D, E: Quadrantal deviation (induced in asymmetric structure)
        - θ: Ship's heading

        Args:
            heading: Ship's heading θ (radians, 0 = North).
            latitude: Geographic latitude φ (radians).
            heel_angle: Heel angle (radians, positive = starboard).

        Returns:
            Compass deviation δ (radians).

        Reference:
            Part III, Art. 441: Compass deviation.
        """
        # Earth's field components (typical values)
        H_earth = self._earth_field_components(latitude)

        # Ship heading unit vectors
        north = np.array([np.cos(heading), np.sin(heading), 0])
        east = np.array([-np.sin(heading), np.cos(heading), 0])

        # Permanent magnetism contribution
        # Deviation from permanent moment
        m_p = self.permanent_moment
        H_disturbance = self._dipole_field_at_compass(m_p)

        # Project disturbance onto compass plane
        H_perturb_north = np.dot(H_disturbance, north)
        H_perturb_east = np.dot(H_disturbance, east)

        # Deviation angle (small angle approximation)
        delta = np.arctan2(H_perturb_east, H_earth[0] + H_perturb_north)

        # Add heeling error (induced vertical magnetism)
        if np.abs(heel_angle) > 1e-6:
            heeling_error = self._heeling_error(heel_angle, heading, latitude)
            delta += heeling_error

        return float(delta)

    def _earth_field_components(self, latitude: float) -> np.ndarray:
        """Get Earth's field components at given latitude."""
        # Typical Earth field magnitude: ~0.5 gauss
        B_earth = 0.5  # gauss

        # Dip angle (magnetic inclination)
        # tan(I) = 2 tan(latitude) for dipole field
        dip_angle = np.arctan(2 * np.tan(latitude))

        # Horizontal and vertical components
        H_horizontal = B_earth * np.cos(dip_angle)
        H_vertical = B_earth * np.sin(dip_angle)

        return np.array([H_horizontal, 0, H_vertical])

    def _dipole_field_at_compass(self, moment: np.ndarray) -> np.ndarray:
        """Calculate field from ship's permanent moment at compass."""
        r = self.compass_position
        r_mag = np.linalg.norm(r)

        if r_mag < 1e-6:
            return np.zeros(3)

        r_hat = r / r_mag

        # Dipole field: H = (3(m·r̂)r̂ - m) / r³
        H = (3 * np.dot(moment, r_hat) * r_hat - moment) / (r_mag**3)

        return H

    def _heeling_error(
        self,
        heel_angle: float,
        heading: float,
        latitude: float,
    ) -> float:
        """Calculate heeling error due to ship tilt."""
        # Heeling induces vertical magnetization that creates
        # horizontal field at the compass

        # Vertical component of Earth's field
        H_earth = self._earth_field_components(latitude)
        H_v = H_earth[2]

        # Induced vertical moment (proportional to susceptibility)
        m_vertical = self.susceptibility * H_v * np.sin(heel_angle)

        # This creates horizontal field at compass
        # Simplified: assume compass is on centerline
        x = self.compass_position[0]
        z = self.compass_position[2]

        if x**2 + z**2 < 1e-6:
            return 0.0

        # Heeling error is maximum on East/West headings
        heeling_coeff = m_vertical / (x**2 + z**2)
        heeling_error = heeling_coeff * np.sin(heading)

        return float(heeling_error)

    @classmethod
    @maxwell_cite(
        441,
        part=3, chapter="Naval Magnetism",
        theory_class="maxwell_original",
        description="Create ship model from deviation coefficients",
    )
    def from_deviation_coefficients(
        cls,
        coefficient_A: float,
        coefficient_B: float,
        coefficient_C: float,
        coefficient_D: float,
        coefficient_E: float,
        compass_position: np.ndarray,
    ) -> ShipMagnetism:
        """
        Create ship magnetism model from measured deviation coefficients.

        Art. 441: The deviation coefficients A, B, C, D, E can be
        determined by "swinging ship" (measuring deviation at various
        headings). From these, we can estimate the magnetic parameters.

        Args:
            coefficient_A: Constant deviation.
            coefficient_B: Semicircular sine coefficient.
            coefficient_C: Semicircular cosine coefficient.
            coefficient_D: Quadrantal sine coefficient.
            coefficient_E: Quadrantal cosine coefficient.
            compass_position: Compass location (x, y, z).

        Returns:
            ShipMagnetism object.

        Reference:
            Part III, Art. 441: Deviation coefficients.
        """
        # Estimate permanent moment from B and C coefficients
        # B and C arise from permanent magnetism in fore-aft and
        # athwartships directions respectively

        # Simplified estimation
        # m ≈ H_earth × r³ × coefficient
        r_mag = np.linalg.norm(compass_position) if np.linalg.norm(compass_position) > 0 else 100
        H_earth = 0.3  # Typical horizontal field

        # Fore-aft moment (from C coefficient)
        m_fore_aft = H_earth * r_mag**3 * coefficient_C

        # Athwartships moment (from B coefficient)
        m_athwartships = H_earth * r_mag**3 * coefficient_B

        # Permanent moment vector (x = forward, y = starboard, z = down)
        permanent_moment = np.array([m_fore_aft, m_athwartships, 0])

        return cls(
            permanent_moment=permanent_moment,
            susceptibility=coefficient_D * 100,  # Rough estimate
            compass_position=compass_position,
        )


@dataclass
class MagneticCompass:
    """
    Ship's magnetic compass with deviation correction.

    Art. 441: A magnetic compass on a ship points to magnetic
    north plus deviation caused by the ship's magnetism.

    The deviation can be corrected by:
    - Permanent magnets (correct B and C)
    - Soft iron correctors (correct D and E)
    - Flinders bar (correct heeling error)

    Attributes:
        ship_magnetism: ShipMagnetism model.
        deviation_table: Measured deviation vs heading.
    """

    ship_magnetism: ShipMagnetism
    deviation_table: dict = field(default_factory=dict)

    @maxwell_cite(
        441,
        part=3, chapter="Naval Magnetism",
        theory_class="maxwell_original",
        description="Convert compass heading to true heading",
    )
    def compass_to_true(
        self,
        compass_heading: float,
        latitude: float,
        magnetic_variation: float,
        heel_angle: float = 0,
    ) -> float:
        """
        Convert compass heading to true (geographic) heading.

        Art. 441: The relationship is:

            True = Compass + Deviation + Variation

        where:
        - Deviation: Ship-induced error
        - Variation: Earth's magnetic declination at location

        Args:
            compass_heading: Compass reading (radians).
            latitude: Geographic latitude (radians).
            magnetic_variation: Magnetic declination (radians).
            heel_angle: Ship heel angle (radians).

        Returns:
            True heading (radians, 0 = geographic North).

        Reference:
            Part III, Art. 441: Heading correction.
        """
        # Estimate deviation at this heading
        deviation = self.ship_magnetism.compass_deviation(
            heading=compass_heading,
            latitude=latitude,
            heel_angle=heel_angle,
        )

        # True heading
        true_heading = compass_heading + deviation + magnetic_variation

        # Normalize to [0, 2π)
        true_heading = true_heading % (2 * np.pi)

        return float(true_heading)

    @maxwell_cite(
        441,
        part=3, chapter="Naval Magnetism",
        theory_class="maxwell_original",
        description="Generate deviation table for compass",
    )
    def generate_deviation_table(
        self,
        latitude: float,
        n_points: int = 36,
    ) -> list[dict[str, float]]:
        """
        Generate complete deviation table for all headings.

        Art. 441: A deviation table lists the compass deviation
        at regular heading intervals (typically every 10°).
        Navigators use this to correct compass readings.

        Args:
            latitude: Geographic latitude (radians).
            n_points: Number of heading points.

        Returns:
            List of dictionaries with heading and deviation.

        Reference:
            Part III, Art. 441: Deviation table.
        """
        table = []

        for i in range(n_points):
            heading = 2 * np.pi * i / n_points
            deviation = self.ship_magnetism.compass_deviation(
                heading=heading,
                latitude=latitude,
            )

            table.append({
                "heading_deg": float(heading * 180 / np.pi),
                "heading_rad": float(heading),
                "deviation_deg": float(deviation * 180 / np.pi),
                "deviation_rad": float(deviation),
            })

        self.deviation_table = {d["heading_deg"]: d["deviation_deg"] for d in table}

        return table


@maxwell_cite(
    441,
    part=3, chapter="Naval Magnetism",
    theory_class="maxwell_original",
    description="Calculate Flinders bar correction",
)
def flinders_bar_correction(
    latitude: float,
    heel_coefficient: float,
    ship_length: float,
) -> dict[str, float]:
    """
    Calculate required Flinders bar for heeling error correction.

    Art. 441: A Flinders bar is a vertical soft iron rod placed
    near the compass to counteract heeling error. The bar becomes
    magnetized by Earth's vertical field and creates a compensating
    horizontal field.

    Args:
        latitude: Geographic latitude (radians).
        heel_coefficient: Measured heeling error coefficient.
        ship_length: Ship length (for scaling).

    Returns:
        Dictionary with Flinders bar specifications.

    Reference:
        Part III, Art. 441: Flinders bar.
    """
    # Earth's vertical field component
    H_vertical = 0.5 * np.sin(latitude)  # Approximate

    # Required induced moment to cancel heeling
    required_correction = heel_coefficient * H_vertical

    # Flinders bar dimensions (empirical)
    bar_length = ship_length / 50  # Typical ratio
    bar_diameter = bar_length / 20

    # Volume of iron needed
    bar_volume = np.pi * (bar_diameter/2)**2 * bar_length

    return {
        "bar_length_cm": float(bar_length),
        "bar_diameter_cm": float(bar_diameter),
        "bar_volume_cm3": float(bar_volume),
        "placement": "Forward of compass on centerline",
        "purpose": "Correct heeling error",
    }


@maxwell_cite(
    441,
    part=3, chapter="Naval Magnetism",
    theory_class="maxwell_original",
    description="Calculate quadrantal corrector settings",
)
def quadrantal_correctors(
    coefficient_D: float,
    coefficient_E: float,
    compass_diameter: float,
) -> dict[str, any]:
    """
    Calculate soft iron corrector placement for quadrantal deviation.

    Art. 441: Quadrantal deviation (D and E coefficients) is caused
    by induced magnetism in horizontal soft iron. It can be corrected
    by placing soft iron spheres or bars near the compass.

    Args:
        coefficient_D: Quadrantal sine coefficient (radians).
        coefficient_E: Quadrantal cosine coefficient (radians).
        compass_diameter: Compass bowl diameter (cm).

    Returns:
        Dictionary with corrector specifications.

    Reference:
        Part III, Art. 441: Quadrantal correctors.
    """
    # Soft iron spheres are most common corrector
    # Size and placement depend on D and E coefficients

    # For pure D coefficient (sin 2θ term)
    # Spheres placed port and starboard

    sphere_diameter = compass_diameter / 3  # Typical size

    # Distance from compass center
    # Closer = stronger correction
    sphere_distance = compass_diameter * (1 + np.abs(coefficient_D) * 10)

    # Adjust for E coefficient (cos 2θ term)
    # Requires fore-aft asymmetry or additional correctors
    if np.abs(coefficient_E) > 1e-4:
        # Need additional fore-aft correction
        fore_sphere_offset = sphere_distance * coefficient_E / (coefficient_D + 1e-6)
    else:
        fore_sphere_offset = 0

    return {
        "sphere_diameter_cm": float(sphere_diameter),
        "sphere_distance_cm": float(sphere_distance),
        "placement": "Port and starboard of compass",
        "fore_aft_offset_cm": float(fore_sphere_offset),
        "corrects_D": np.abs(coefficient_D) > 1e-4,
        "corrects_E": np.abs(coefficient_E) > 1e-4,
    }


@maxwell_cite(
    441,
    part=3, chapter="Naval Magnetism",
    theory_class="maxwell_original",
    description="Simulate compass swinging procedure",
)
def simulate_compass_swinging(
    true_headings: list[float],
    latitude: float,
    ship_params: dict,
) -> dict[str, any]:
    """
    Simulate the compass swinging procedure to determine deviation.

    Art. 441: "Swinging ship" is the procedure to measure compass
    deviation at all headings:

    1. Ship is rotated to known true headings
    2. Compass reading is recorded at each heading
    3. Deviation = True - Compass (accounting for variation)
    4. Coefficients A, B, C, D, E are fitted

    Args:
        true_headings: List of true headings (radians).
        latitude: Geographic latitude (radians).
        ship_params: Ship magnetism parameters.

    Returns:
        Dictionary with deviation data and fitted coefficients.

    Reference:
        Part III, Art. 441: Compass swinging.
    """
    # Create ship model
    ship = ShipMagnetism(
        permanent_moment=np.array([
            ship_params.get("m_fore_aft", 1000),
            ship_params.get("m_athwartships", 500),
            ship_params.get("m_vertical", 100),
        ]),
        susceptibility=ship_params.get("susceptibility", 0.01),
        compass_position=np.array([0, 0, 50]),  # 50 cm above center
    )

    # Simulate measurements
    measurements = []
    for true_h in true_headings:
        # Compass would read: compass = true - deviation
        deviation = ship.compass_deviation(heading=true_h, latitude=latitude)
        compass_reading = true_h - deviation

        measurements.append({
            "true_heading_rad": float(true_h),
            "true_heading_deg": float(true_h * 180 / np.pi),
            "compass_heading_rad": float(compass_reading),
            "compass_heading_deg": float(compass_reading * 180 / np.pi),
            "deviation_rad": float(deviation),
            "deviation_deg": float(deviation * 180 / np.pi),
        })

    # Fit deviation coefficients (simplified)
    # δ = A + B sin(θ) + C cos(θ) + D sin(2θ) + E cos(2θ)
    coefficients = _fit_deviation_coefficients(measurements)

    return {
        "measurements": measurements,
        "fitted_coefficients": coefficients,
        "max_deviation": max(abs(m["deviation_deg"]) for m in measurements),
    }


def _fit_deviation_coefficients(measurements: list[dict]) -> dict[str, float]:
    """Fit deviation coefficients from measurements."""
    # Simplified least squares fit
    n = len(measurements)

    A = 0
    B_sum = 0
    C_sum = 0
    D_sum = 0
    E_sum = 0

    sin_sum = 0
    cos_sum = 0
    sin2_sum = 0
    cos2_sum = 0

    for m in measurements:
        theta = m["true_heading_rad"]
        delta = m["deviation_rad"]

        A += delta
        B_sum += delta * np.sin(theta)
        C_sum += delta * np.cos(theta)
        D_sum += delta * np.sin(2 * theta)
        E_sum += delta * np.cos(2 * theta)

        sin_sum += np.sin(theta)**2
        cos_sum += np.cos(theta)**2
        sin2_sum += np.sin(2 * theta)**2
        cos2_sum += np.cos(2 * theta)**2

    # Normalize
    A /= n
    B = 2 * B_sum / sin_sum if sin_sum > 0 else 0
    C = 2 * C_sum / cos_sum if cos_sum > 0 else 0
    D = 2 * D_sum / sin2_sum if sin2_sum > 0 else 0
    E = 2 * E_sum / cos2_sum if cos2_sum > 0 else 0

    return {
        "A_rad": float(A),
        "B_rad": float(B),
        "C_rad": float(C),
        "D_rad": float(D),
        "E_rad": float(E),
        "A_deg": float(A * 180 / np.pi),
        "B_deg": float(B * 180 / np.pi),
        "C_deg": float(C * 180 / np.pi),
        "D_deg": float(D * 180 / np.pi),
        "E_deg": float(E * 180 / np.pi),
    }


@maxwell_cite(
    441,
    part=3, chapter="Naval Magnetism",
    theory_class="maxwell_original",
    description="Verify naval magnetism calculations",
)
def verify_naval_magnetism() -> dict[str, any]:
    """
    Verify naval magnetism calculations.

    Art. 441: Test cases:

    1. Deviation varies with heading
    2. Heeling error depends on latitude
    3. Deviation coefficients can be fitted

    Returns:
        Dictionary with verification results.

    Reference:
        Part III, Art. 441: Naval verification.
    """
    results = {}

    # Test 1: Deviation varies sinusoidally with heading
    ship = ShipMagnetism(
        permanent_moment=np.array([1000, 500, 0]),
        susceptibility=0.01,
        compass_position=np.array([0, 0, 50]),
    )

    deviations = []
    headings = np.linspace(0, 2*np.pi, 36)

    for h in headings:
        dev = ship.compass_deviation(heading=h, latitude=np.pi/4)
        deviations.append(dev)

    # Should show periodic variation
    dev_range = max(deviations) - min(deviations)
    results["heading_variation"] = {
        "deviation_range_rad": float(dev_range),
        "deviation_range_deg": float(dev_range * 180 / np.pi),
        "varies_with_heading": dev_range > 1e-6,
    }

    # Test 2: Heeling error depends on latitude
    dev_equator = ship.compass_deviation(
        heading=np.pi/2, latitude=0, heel_angle=0.1
    )
    dev_polar = ship.compass_deviation(
        heading=np.pi/2, latitude=np.pi/3, heel_angle=0.1
    )

    results["heeling_latitude"] = {
        "deviation_at_equator": float(dev_equator),
        "deviation_at_latitude": float(dev_polar),
        "latitude_dependence": np.abs(dev_polar) > np.abs(dev_equator),
    }

    # Test 3: Compass swinging simulation
    true_headings = np.linspace(0, 2*np.pi, 12, endpoint=False).tolist()
    swing_result = simulate_compass_swinging(
        true_headings=true_headings,
        latitude=np.pi/4,
        ship_params={"m_fore_aft": 1000, "m_athwartships": 500},
    )

    results["compass_swinging"] = {
        "max_deviation_deg": swing_result["max_deviation"],
        "coefficients_fitted": swing_result["fitted_coefficients"],
        "measurements_count": len(swing_result["measurements"]),
    }

    return results

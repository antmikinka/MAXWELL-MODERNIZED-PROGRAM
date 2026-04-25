"""
Terrestrial Magnetism — Earth's magnetic field theory and measurement.

Implements Maxwell's theory of terrestrial magnetism from Part III, Chapter VIII:
- Earth's magnetic field components and elements (Arts. 465-468)
- Magnetic surveys and contour mapping (Arts. 469-471)
- Diurnal variation and magnetic storms (Arts. 472-473)
- Magnetic potential and spherical harmonic analysis (Art. 474)

Maxwell treats the Earth as a giant magnet whose field can be described
by a scalar potential expanded in spherical harmonics. The field is
characterized by seven elements that can be measured at observatories.

Category: A (maxwell_original) — Maxwell's theory of terrestrial magnetism.

References:
    Part III, Arts. 465-474: Terrestrial magnetism.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST, UniversalConstants


# =============================================================================
# EARTH'S MAGNETIC FIELD (Arts. 465-468)
# =============================================================================

@dataclass
class GeomagneticElements:
    """
    The seven elements that completely specify Earth's magnetic field at a location.

    Art. 467: The magnetic force at any point on Earth's surface is determined
    by seven elements, of which three are independent and four are derived:

    Independent elements (typically measured):
    - X: North component of H (gauss)
    - Y: East component of H (gauss)
    - Z: Vertical component (positive downward, gauss)

    Derived elements:
    - H: Horizontal intensity = sqrt(X^2 + Y^2) (gauss)
    - D: Declination = arctan(Y/X) (angle from true north, radians)
    - I: Inclination (dip) = arctan(Z/H) (angle below horizontal, radians)
    - F: Total intensity = sqrt(H^2 + Z^2) (gauss)

    Attributes:
        X: Northward component of horizontal field (gauss).
        Y: Eastward component of horizontal field (gauss).
        Z: Downward vertical component (gauss).
    """

    X: float  # North component
    Y: float  # East component
    Z: float  # Vertical component (positive down)

    @property
    def H(self) -> float:
        """Horizontal intensity H = sqrt(X^2 + Y^2)."""
        return float(np.sqrt(self.X ** 2 + self.Y ** 2))

    @property
    def D(self) -> float:
        """
        Declination (variation) — angle between magnetic and true north.

        D = arctan(Y/X)

        Positive D means magnetic north is east of true north.
        """
        return float(np.arctan2(self.Y, self.X))

    @property
    def I(self) -> float:
        """
        Inclination (dip) — angle the field makes with the horizontal.

        I = arctan(Z/H)

        Positive I means the field points downward (northern hemisphere).
        """
        H_mag = self.H
        if H_mag == 0:
            return np.pi / 2 if self.Z > 0 else -np.pi / 2
        return float(np.arctan2(self.Z, H_mag))

    @property
    def F(self) -> float:
        """Total intensity F = sqrt(H^2 + Z^2) = sqrt(X^2 + Y^2 + Z^2)."""
        return float(np.sqrt(self.X ** 2 + self.Y ** 2 + self.Z ** 2))

    @property
    def field_vector(self) -> np.ndarray:
        """Return the complete field vector (X, Y, Z)."""
        return np.array([self.X, self.Y, self.Z], dtype=np.float64)

    @classmethod
    @maxwell_cite(
        467,
        part=3, chapter="Terrestrial Magnetism",
        theory_class="maxwell_original",
        description="Create from horizontal intensity, declination, inclination",
    )
    def from_HDI(cls, H: float, D: float, I: float) -> GeomagneticElements:
        """
        Create geomagnetic elements from H, D, I.

        Art. 467: The field can be specified by the horizontal intensity,
        declination, and inclination, from which the components are derived:

            X = H * cos(D)
            Y = H * sin(D)
            Z = H * tan(I)

        Args:
            H: Horizontal intensity (gauss).
            D: Declination (radians, positive = east).
            I: Inclination (radians, positive = downward).

        Returns:
            GeomagneticElements object.

        Reference:
            Part III, Art. 467: Relations between magnetic elements.
        """
        if H < 0:
            raise ValueError("Horizontal intensity H must be non-negative")

        X = H * np.cos(D)
        Y = H * np.sin(D)
        Z = H * np.tan(I)

        return cls(X=X, Y=Y, Z=Z)

    @classmethod
    @maxwell_cite(
        467,
        part=3, chapter="Terrestrial Magnetism",
        theory_class="maxwell_original",
        description="Create from total intensity, declination, dip",
    )
    def from_FDI(cls, F: float, D: float, I: float) -> GeomagneticElements:
        """
        Create geomagnetic elements from F, D, I.

        Art. 467: Given total intensity and angles:

            H = F * cos(I)
            Z = F * sin(I)
            X = H * cos(D)
            Y = H * sin(D)

        Args:
            F: Total intensity (gauss).
            D: Declination (radians).
            I: Inclination (radians).

        Returns:
            GeomagneticElements object.

        Reference:
            Part III, Art. 467: Magnetic element relations.
        """
        if F < 0:
            raise ValueError("Total intensity F must be non-negative")

        H = F * np.cos(I)
        Z = F * np.sin(I)
        X = H * np.cos(D)
        Y = H * np.sin(D)

        return cls(X=X, Y=Y, Z=Z)

    @classmethod
    @maxwell_cite(
        465, 466,
        part=3, chapter="Terrestrial Magnetism",
        theory_class="maxwell_original",
        description="Create from direct component measurements",
    )
    def from_components(cls, X: float, Y: float, Z: float) -> GeomagneticElements:
        """
        Create geomagnetic elements from measured components.

        Art. 465-466: The Earth's magnetic force at any station is
        resolved into three rectangular components: X (north), Y (east),
        Z (vertical, positive downward).

        Args:
            X: Northward component (gauss).
            Y: Eastward component (gauss).
            Z: Downward vertical component (gauss).

        Returns:
            GeomagneticElements object.

        Reference:
            Part III, Arts. 465-466: Earth's magnetic field components.
        """
        return cls(X=X, Y=Y, Z=Z)

    @maxwell_cite(
        467,
        part=3, chapter="Terrestrial Magnetism",
        theory_class="maxwell_original",
        description="Convert all elements to dictionary",
    )
    def to_dict(self) -> Dict[str, float]:
        """
        Return all seven magnetic elements as a dictionary.

        Art. 467: The complete specification includes all seven elements.

        Returns:
            Dictionary with keys: X, Y, Z, H, D, I, F
            Angles in radians, intensities in gauss.

        Reference:
            Part III, Art. 467: Seven magnetic elements.
        """
        return {
            'X': self.X,
            'Y': self.Y,
            'Z': self.Z,
            'H': self.H,
            'D': self.D,
            'I': self.I,
            'F': self.F,
        }


@maxwell_cite(
    465, 466,
    part=3, chapter="Terrestrial Magnetism",
    theory_class="maxwell_original",
    description="Compute Earth's field components at a location",
)
def earth_field_components(
    latitude: float,
    longitude: float,
    dipole_moment: float = 8.0e25,
    dipole_latitude: float = 80.0,
    dipole_longitude: float = -72.0,
) -> Dict[str, float]:
    """
    Calculate Earth's magnetic field components using dipole approximation.

    Art. 465-466: The Earth acts as a giant magnet. To first approximation,
    its field is that of a magnetic dipole at Earth's center. The field
    components at any location are determined by the dipole orientation
    and moment.

    For a dipole field in spherical coordinates:
        B_r = -2 * (mu0/4pi) * m * cos(theta') / r^3
        B_theta = -(mu0/4pi) * m * sin(theta') / r^3

    where theta' is the angular distance from the dipole pole.

    Args:
        latitude: Geographic latitude (degrees, positive = north).
        longitude: Geographic longitude (degrees, positive = east).
        dipole_moment: Earth's magnetic dipole moment (emu, ~8e25 emu).
        dipole_latitude: Latitude of north dipole pole (degrees, ~80N).
        dipole_longitude: Longitude of north dipole pole (degrees, ~72W).

    Returns:
        Dictionary with:
        - X: North component (gauss)
        - Y: East component (gauss)
        - Z: Vertical component (gauss, positive down)
        - H: Horizontal intensity (gauss)
        - F: Total intensity (gauss)
        - D: Declination (radians)
        - I: Inclination (radians)

    Reference:
        Part III, Arts. 465-466: Earth's magnetic field components.

    Note:
        In CGS, the dipole field formulas simplify since mu0/4pi = 1.
        Earth radius ~6.37e8 cm.
    """
    # Convert to radians
    lat = np.radians(latitude)
    lon = np.radians(longitude)
    dipole_lat = np.radians(dipole_latitude)
    dipole_lon = np.radians(dipole_longitude)

    # Earth radius in cm
    R_EARTH = 6.371e8

    # Dipole moment (CGS-EMU)
    m = dipole_moment

    # Angular distance from dipole pole (spherical law of cosines)
    cos_theta_prime = (
        np.sin(lat) * np.sin(dipole_lat) +
        np.cos(lat) * np.cos(dipole_lat) * np.cos(lon - dipole_lon)
    )
    cos_theta_prime = np.clip(cos_theta_prime, -1.0, 1.0)
    theta_prime = np.arccos(cos_theta_prime)
    sin_theta_prime = np.sin(theta_prime)

    # Dipole field components in local spherical coordinates
    # B_r (radial, positive outward) and B_theta (southward)
    factor = m / (R_EARTH ** 3)

    B_r = -2 * factor * cos_theta_prime  # Negative = downward
    B_theta = -factor * sin_theta_prime  # Negative = northward

    # Convert to local coordinates:
    # Z (positive down) = -B_r
    # H (northward) = -B_theta
    Z = -B_r
    H_north = -B_theta

    # For declination, we need the east component
    # In centered dipole approximation, Y is small but not zero
    # due to the offset between geographic and magnetic poles

    # Azimuth from location to dipole pole
    sin_azimuth = (
        np.cos(dipole_lat) * np.sin(dipole_lon - lon) /
        np.sin(theta_prime) if sin_theta_prime > 1e-10 else 0.0
    )
    cos_azimuth = (
        (np.sin(dipole_lat) - np.sin(lat) * cos_theta_prime) /
        (np.cos(lat) * sin_theta_prime) if sin_theta_prime > 1e-10 and abs(np.cos(lat)) > 1e-10 else 1.0
    )
    cos_azimuth = np.clip(cos_azimuth, -1.0, 1.0)

    # East component from azimuth
    Y = H_north * sin_azimuth if abs(sin_azimuth) < 1 else 0.0
    X = H_north * np.sqrt(max(0, 1 - sin_azimuth**2))

    # Compute derived elements
    H = float(np.sqrt(X**2 + Y**2))
    F = float(np.sqrt(H**2 + Z**2))
    D = float(np.arctan2(Y, X)) if H > 1e-15 else 0.0
    I = float(np.arctan2(Z, H)) if H > 1e-15 else np.pi/2 * np.sign(Z)

    return {
        'X': float(X),
        'Y': float(Y),
        'Z': float(Z),
        'H': H,
        'F': F,
        'D': D,
        'I': I,
    }


@maxwell_cite(
    467,
    part=3, chapter="Terrestrial Magnetism",
    theory_class="maxwell_original",
    description="Calculate all seven magnetic elements and their relations",
)
def magnetic_elements(
    X: float = None, Y: float = None, Z: float = None,
    H: float = None, D: float = None, I: float = None,
    F: float = None,
) -> Dict[str, float]:
    """
    Calculate all seven magnetic elements from any independent set.

    Art. 467: The seven magnetic elements are related by the equations:

        H^2 = X^2 + Y^2
        F^2 = H^2 + Z^2 = X^2 + Y^2 + Z^2
        tan(D) = Y/X
        tan(I) = Z/H

        X = H * cos(D) = F * cos(I) * cos(D)
        Y = H * sin(D) = F * cos(I) * sin(D)
        Z = H * tan(I) = F * sin(I)

    Any three independent elements determine the rest.

    Args:
        X, Y, Z: Rectangular components (gauss).
        H: Horizontal intensity (gauss).
        D: Declination (radians or degrees, see below).
        I: Inclination (radians or degrees).
        F: Total intensity (gauss).

    Returns:
        Dictionary with all seven elements: X, Y, Z, H, D, I, F

    Reference:
        Part III, Art. 467: Relations between magnetic elements.

    Note:
        This function accepts various combinations of inputs and computes
        the complete set. Angles are assumed to be in radians unless
        the value exceeds 2*pi (then degrees are assumed).
    """
    # Helper to convert degrees to radians if needed
    def to_radians(angle, name):
        if angle is None:
            return None
        if abs(angle) > 2 * np.pi:  # Likely degrees
            return np.radians(angle)
        return angle

    # Convert angles
    D_rad = to_radians(D, 'D') if D is not None else None
    I_rad = to_radians(I, 'I') if I is not None else None

    # Strategy: first get X, Y, Z, then compute derived elements
    result = {}

    # Case 1: Given X, Y, Z directly
    if X is not None and Y is not None and Z is not None:
        result['X'] = X
        result['Y'] = Y
        result['Z'] = Z

    # Case 2: Given H, D, I
    elif H is not None and D_rad is not None and I_rad is not None:
        result['H'] = H
        result['X'] = H * np.cos(D_rad)
        result['Y'] = H * np.sin(D_rad)
        result['Z'] = H * np.tan(I_rad)

    # Case 3: Given F, D, I
    elif F is not None and D_rad is not None and I_rad is not None:
        H_calc = F * np.cos(I_rad)
        result['F'] = F
        result['H'] = H_calc
        result['X'] = H_calc * np.cos(D_rad)
        result['Y'] = H_calc * np.sin(D_rad)
        result['Z'] = F * np.sin(I_rad)

    # Case 4: Given H, D, Z
    elif H is not None and D_rad is not None and Z is not None:
        result['H'] = H
        result['X'] = H * np.cos(D_rad)
        result['Y'] = H * np.sin(D_rad)
        result['Z'] = Z

    # Case 5: Given F, I, D
    elif F is not None and I_rad is not None and D_rad is not None:
        H_calc = F * np.cos(I_rad)
        result['F'] = F
        result['H'] = H_calc
        result['X'] = H_calc * np.cos(D_rad)
        result['Y'] = H_calc * np.sin(D_rad)
        result['Z'] = F * np.sin(I_rad)

    else:
        raise ValueError(
            "Insufficient independent elements. Provide one of: "
            "(X, Y, Z), (H, D, I), (F, D, I), (H, D, Z), or (F, I, D)"
        )

    # Compute derived elements
    X_val = result.get('X', 0)
    Y_val = result.get('Y', 0)
    Z_val = result.get('Z', 0)

    if 'H' not in result:
        result['H'] = float(np.sqrt(X_val**2 + Y_val**2))
    if 'F' not in result:
        result['F'] = float(np.sqrt(X_val**2 + Y_val**2 + Z_val**2))
    if 'D' not in result:
        result['D'] = float(np.arctan2(Y_val, X_val))
    if 'I' not in result:
        H_val = result['H']
        result['I'] = float(np.arctan2(Z_val, H_val)) if H_val > 1e-15 else np.pi/2 * np.sign(Z_val)

    # Ensure D and I are in radians
    result['D'] = float(result['D'])
    result['I'] = float(result['I'])

    return result


@maxwell_cite(
    468,
    part=3, chapter="Terrestrial Magnetism",
    theory_class="maxwell_original",
    description="Magnetic observatory measurement protocol",
)
def magnetic_observatory_protocol(
    station_name: str,
    latitude: float,
    longitude: float,
    elevation: float = 0.0,
    measurements: Dict[str, float] = None,
) -> Dict[str, any]:
    """
    Process magnetic observatory measurements following Maxwell's protocol.

    Art. 468: Magnetic observatories are established at fixed locations
    to make continuous measurements of the Earth's field. The standard
    protocol includes:

    1. Determination of the magnetic meridian (plane of H)
    2. Measurement of declination D using a theodolite
    3. Measurement of inclination I using a dip circle
    4. Measurement of horizontal intensity H using oscillation method
    5. Computation of X, Y, Z, F from H, D, I

    Args:
        station_name: Name of the observatory station.
        latitude: Geographic latitude (degrees).
        longitude: Geographic longitude (degrees).
        elevation: Elevation above sea level (cm).
        measurements: Dictionary with measured values (H, D, I or X, Y, Z).

    Returns:
        Dictionary with:
        - station_info: Name, location, elevation
        - measured_elements: The input measurements
        - computed_elements: All seven elements
        - timestamp: When measurement was taken

    Reference:
        Part III, Art. 468: Magnetic observatory methods.

    Example:
        >>> result = magnetic_observatory_protocol(
        ...     "Kew Observatory",
        ...     latitude=51.4,
        ...     longitude=-0.3,
        ...     measurements={'H': 0.185, 'D': 0.02, 'I': 1.17}
        ... )
    """
    from datetime import datetime

    # Process measured elements
    if measurements is None:
        measurements = {}

    # Compute all seven elements
    try:
        computed = magnetic_elements(**measurements)
    except ValueError as e:
        computed = {'error': str(e)}

    return {
        'station_info': {
            'name': station_name,
            'latitude': latitude,
            'longitude': longitude,
            'elevation_cm': elevation,
        },
        'measured_elements': measurements,
        'computed_elements': computed,
        'timestamp': datetime.utcnow().isoformat(),
    }


# =============================================================================
# MAGNETIC SURVEYS (Arts. 469-471)
# =============================================================================

@maxwell_cite(
    469, 470,
    part=3, chapter="Terrestrial Magnetism",
    theory_class="maxwell_original",
    description="Regional magnetic survey method",
)
def magnetic_survey_method(
    survey_stations: List[Dict[str, float]],
    survey_name: str = "Unnamed Survey",
) -> Dict[str, any]:
    """
    Process data from a regional magnetic survey.

    Art. 469-470: Magnetic surveys involve measuring the Earth's field
    at multiple stations across a region. Each station records the
    magnetic elements, and the results are compiled into maps showing
    the spatial variation of the field.

    The survey method includes:
    1. Selection of stations distributed across the region
    2. Measurement of H, D, I (or X, Y, Z) at each station
    3. Reduction of observations to a common epoch
    4. Interpolation to create continuous field maps
    5. Drawing of isomagnetic lines (isogons, isoclines, isodynamics)

    Args:
        survey_stations: List of station dictionaries, each containing:
            - name: Station name
            - latitude: Geographic latitude (degrees)
            - longitude: Geographic longitude (degrees)
            - H, D, I or X, Y, Z: Magnetic elements
        survey_name: Name of the survey.

    Returns:
        Dictionary with:
        - survey_name: Name of the survey
        - num_stations: Number of stations
        - stations: List of processed station data
        - statistics: Mean, min, max of field elements
        - bounds: Geographic extent of survey

    Reference:
        Part III, Arts. 469-470: Magnetic survey methods.
    """
    if not survey_stations:
        raise ValueError("survey_stations cannot be empty")

    processed_stations = []
    all_H, all_D, all_I, all_F = [], [], [], []

    for station in survey_stations:
        # Extract location
        lat = station.get('latitude', 0)
        lon = station.get('longitude', 0)
        name = station.get('name', 'Unknown')

        # Extract measurements
        meas_keys = ['H', 'D', 'I', 'X', 'Y', 'Z', 'F']
        measurements = {k: v for k, v in station.items() if k in meas_keys}

        # Compute all elements
        try:
            elements = magnetic_elements(**measurements)
            all_H.append(elements['H'])
            all_D.append(elements['D'])
            all_I.append(elements['I'])
            all_F.append(elements['F'])
        except ValueError:
            elements = {'error': 'Insufficient measurements'}

        processed_stations.append({
            'name': name,
            'latitude': lat,
            'longitude': lon,
            'elements': elements,
        })

    # Compute statistics
    stats = {}
    if all_H:
        stats['H'] = {
            'mean': float(np.mean(all_H)),
            'min': float(np.min(all_H)),
            'max': float(np.max(all_H)),
        }
    if all_D:
        stats['D'] = {
            'mean': float(np.mean(all_D)),
            'min': float(np.min(all_D)),
            'max': float(np.max(all_D)),
        }
    if all_I:
        stats['I'] = {
            'mean': float(np.mean(all_I)),
            'min': float(np.min(all_I)),
            'max': float(np.max(all_I)),
        }
    if all_F:
        stats['F'] = {
            'mean': float(np.mean(all_F)),
            'min': float(np.min(all_F)),
            'max': float(np.max(all_F)),
        }

    # Geographic bounds
    lats = [s['latitude'] for s in processed_stations]
    lons = [s['longitude'] for s in processed_stations]

    return {
        'survey_name': survey_name,
        'num_stations': len(processed_stations),
        'stations': processed_stations,
        'statistics': stats,
        'bounds': {
            'lat_min': float(min(lats)),
            'lat_max': float(max(lats)),
            'lon_min': float(min(lons)),
            'lon_max': float(max(lons)),
        },
    }


@maxwell_cite(
    471,
    part=3, chapter="Terrestrial Magnetism",
    theory_class="maxwell_original",
    description="Lines of equal total force (isodynamic lines)",
)
def isodynamic_lines(
    survey_data: Dict[str, any],
    contour_levels: List[float] = None,
) -> Dict[str, any]:
    """
    Generate isodynamic lines (lines of equal total force F).

    Art. 471: Isodynamic lines connect points on the Earth's surface
    where the total intensity F has the same value. These lines form
    closed curves and never intersect.

    The distribution of isodynamic lines reveals:
    - Regions of maximum field intensity (near magnetic poles)
    - Regions of minimum field intensity (magnetic equator)
    - Anomalies due to crustal magnetization

    Args:
        survey_data: Output from magnetic_survey_method().
        contour_levels: Specific F values for contour lines (gauss).
                       If None, auto-generated from data.

    Returns:
        Dictionary with:
        - contour_levels: F values for each contour
        - stations_by_contour: Stations grouped by contour
        - intensity_range: Min and max F values

    Reference:
        Part III, Art. 471: Isodynamic, isoclinic, and isogonic lines.

    Note:
        This function computes the contour levels and groups stations.
        Actual line drawing requires interpolation and plotting.
    """
    if 'stations' not in survey_data:
        raise ValueError("Invalid survey data: missing 'stations'")

    # Extract F values
    F_values = []
    valid_stations = []

    for station in survey_data['stations']:
        elements = station.get('elements', {})
        if 'F' in elements and elements.get('error') is None:
            F_values.append(elements['F'])
            valid_stations.append(station)

    if not F_values:
        return {'error': 'No valid F measurements found'}

    F_min = min(F_values)
    F_max = max(F_values)

    # Generate contour levels if not provided
    if contour_levels is None:
        n_levels = min(10, len(F_values))
        contour_levels = list(np.linspace(F_min, F_max, n_levels))

    # Group stations by contour
    stations_by_contour = {level: [] for level in contour_levels}

    for station, F in zip(valid_stations, F_values):
        # Find nearest contour level
        nearest = min(contour_levels, key=lambda x: abs(x - F))
        stations_by_contour[nearest].append({
            'name': station['name'],
            'latitude': station['latitude'],
            'longitude': station['longitude'],
            'F': F,
        })

    return {
        'contour_levels': contour_levels,
        'stations_by_contour': stations_by_contour,
        'intensity_range': {'min': F_min, 'max': F_max},
        'num_valid_stations': len(valid_stations),
    }


@maxwell_cite(
    471,
    part=3, chapter="Terrestrial Magnetism",
    theory_class="maxwell_original",
    description="Lines of equal inclination (isoclinal lines)",
)
def isoclinal_lines(
    survey_data: Dict[str, any],
    contour_levels: List[float] = None,
) -> Dict[str, any]:
    """
    Generate isoclinal lines (lines of equal inclination/dip I).

    Art. 471: Isoclinal lines (also called isoclinic lines) connect
    points where the magnetic inclination (dip angle) is the same.

    Key features:
    - Magnetic equator: I = 0 (field is horizontal)
    - Magnetic poles: I = +/-90 degrees (field is vertical)
    - Inclination increases from equator toward poles

    Args:
        survey_data: Output from magnetic_survey_method().
        contour_levels: I values for contour lines (radians).
                       If None, auto-generated from data.

    Returns:
        Dictionary with:
        - contour_levels: I values for each contour (radians and degrees)
        - stations_by_contour: Stations grouped by contour
        - inclination_range: Min and max I values

    Reference:
        Part III, Art. 471: Isoclinic lines.
    """
    if 'stations' not in survey_data:
        raise ValueError("Invalid survey data: missing 'stations'")

    # Extract I values
    I_values = []
    valid_stations = []

    for station in survey_data['stations']:
        elements = station.get('elements', {})
        if 'I' in elements and elements.get('error') is None:
            I_values.append(elements['I'])
            valid_stations.append(station)

    if not I_values:
        return {'error': 'No valid I measurements found'}

    I_min = min(I_values)
    I_max = max(I_values)

    # Generate contour levels if not provided
    if contour_levels is None:
        n_levels = min(10, len(I_values))
        contour_levels = list(np.linspace(I_min, I_max, n_levels))

    # Group stations by contour
    stations_by_contour = {level: [] for level in contour_levels}

    for station, I in zip(valid_stations, I_values):
        nearest = min(contour_levels, key=lambda x: abs(x - I))
        stations_by_contour[nearest].append({
            'name': station['name'],
            'latitude': station['latitude'],
            'longitude': station['longitude'],
            'I': I,
            'I_degrees': float(np.degrees(I)),
        })

    return {
        'contour_levels': contour_levels,
        'contour_levels_degrees': [float(np.degrees(c)) for c in contour_levels],
        'stations_by_contour': stations_by_contour,
        'inclination_range': {
            'min': I_min,
            'max': I_max,
            'min_degrees': float(np.degrees(I_min)),
            'max_degrees': float(np.degrees(I_max)),
        },
        'num_valid_stations': len(valid_stations),
    }


@maxwell_cite(
    471,
    part=3, chapter="Terrestrial Magnetism",
    theory_class="maxwell_original",
    description="Lines of equal declination (isogonal lines)",
)
def isogonal_lines(
    survey_data: Dict[str, any],
    contour_levels: List[float] = None,
) -> Dict[str, any]:
    """
    Generate isogonal lines (lines of equal declination/variation D).

    Art. 471: Isogonal lines (also called isogonic lines) connect points
    where the magnetic declination (angle between magnetic and true north)
    is the same.

    Key features:
    - Agonic line: D = 0 (magnetic north = true north)
    - Positive D: East variation (magnetic north east of true north)
    - Negative D: West variation (magnetic north west of true north)

    Args:
        survey_data: Output from magnetic_survey_method().
        contour_levels: D values for contour lines (radians).
                       If None, auto-generated from data.

    Returns:
        Dictionary with:
        - contour_levels: D values for each contour (radians and degrees)
        - stations_by_contour: Stations grouped by contour
        - declination_range: Min and max D values

    Reference:
        Part III, Art. 471: Isogonic lines.
    """
    if 'stations' not in survey_data:
        raise ValueError("Invalid survey data: missing 'stations'")

    # Extract D values
    D_values = []
    valid_stations = []

    for station in survey_data['stations']:
        elements = station.get('elements', {})
        if 'D' in elements and elements.get('error') is None:
            D_values.append(elements['D'])
            valid_stations.append(station)

    if not D_values:
        return {'error': 'No valid D measurements found'}

    D_min = min(D_values)
    D_max = max(D_values)

    # Generate contour levels if not provided
    if contour_levels is None:
        n_levels = min(10, len(D_values))
        contour_levels = list(np.linspace(D_min, D_max, n_levels))

    # Group stations by contour
    stations_by_contour = {level: [] for level in contour_levels}

    for station, D in zip(valid_stations, D_values):
        nearest = min(contour_levels, key=lambda x: abs(x - D))
        stations_by_contour[nearest].append({
            'name': station['name'],
            'latitude': station['latitude'],
            'longitude': station['longitude'],
            'D': D,
            'D_degrees': float(np.degrees(D)),
        })

    return {
        'contour_levels': contour_levels,
        'contour_levels_degrees': [float(np.degrees(c)) for c in contour_levels],
        'stations_by_contour': stations_by_contour,
        'declination_range': {
            'min': D_min,
            'max': D_max,
            'min_degrees': float(np.degrees(D_min)),
            'max_degrees': float(np.degrees(D_max)),
        },
        'num_valid_stations': len(valid_stations),
    }


@maxwell_cite(
    469, 470,
    part=3, chapter="Terrestrial Magnetism",
    theory_class="maxwell_original",
    description="Gauss spherical harmonic analysis of Earth's field",
)
def gauss_spherical_analysis(
    survey_data: Dict[str, any],
    max_degree: int = 8,
) -> Dict[str, any]:
    """
    Perform Gauss's spherical harmonic analysis of Earth's magnetic field.

    Art. 469-470: Gauss showed that Earth's magnetic potential can be
    expanded in spherical harmonics:

        V(r, theta, phi) = R * sum_{n=1}^{inf} sum_{m=0}^{n} (R/r)^{n+1} *
                          [g_n^m * cos(m*phi) + h_n^m * sin(m*phi)] * P_n^m(cos(theta))

    where:
    - R = Earth radius
    - g_n^m, h_n^m = Gauss coefficients
    - P_n^m = Associated Legendre functions
    - theta = colatitude, phi = longitude

    The field components are derived from the potential:
        X = -dV/dtheta (northward)
        Y = -(1/sin(theta)) * dV/dphi (eastward)
        Z = -dV/dr (downward)

    Args:
        survey_data: Survey data with station locations and measurements.
        max_degree: Maximum degree n for spherical harmonic expansion.

    Returns:
        Dictionary with:
        - method: Description of Gauss's method
        - max_degree: Maximum spherical harmonic degree
        - num_coefficients: Number of (n,m) pairs
        - coefficient_names: List of coefficient names (g_n_m, h_n_m)

    Reference:
        Part III, Arts. 469-470: Spherical harmonic analysis.

    Note:
        This function sets up the framework for spherical harmonic analysis.
        Full coefficient determination requires solving a least-squares
        problem with global data.
    """
    # Generate coefficient names up to max_degree
    coefficients = []
    for n in range(1, max_degree + 1):
        for m in range(n + 1):
            coefficients.append(f'g_{n}^{m}')
            if m > 0:  # h_n^0 is conventionally zero
                coefficients.append(f'h_{n}^{m}')

    # Associated Legendre function degrees
    legendre_degrees = list(range(1, max_degree + 1))

    return {
        'method': 'Gauss spherical harmonic expansion',
        'potential_form': 'V = R * sum((R/r)^(n+1) * [g_n^m * cos(m*phi) + h_n^m * sin(m*phi)] * P_n^m(cos(theta)))',
        'max_degree': max_degree,
        'num_coefficients': len(coefficients),
        'coefficient_names': coefficients,
        'legendre_degrees': legendre_degrees,
        'field_components_from_potential': {
            'X': '-dV/dtheta (northward)',
            'Y': '-(1/sin(theta)) * dV/dphi (eastward)',
            'Z': '-dV/dr (downward)',
        },
    }


# =============================================================================
# DIURNAL VARIATION (Arts. 472-473)
# =============================================================================

@maxwell_cite(
    472,
    part=3, chapter="Terrestrial Magnetism",
    theory_class="maxwell_original",
    description="Diurnal (daily) variation of Earth's magnetic field",
)
def diurnal_variation(
    hour: float,
    latitude: float,
    season: str = 'equinox',
    elements: List[str] = None,
) -> Dict[str, float]:
    """
    Calculate the regular diurnal (daily) variation of Earth's magnetic field.

    Art. 472: The Earth's magnetic field exhibits regular daily variations
    caused by solar influence. These variations:

    - Have periods of 24 hours (daily) and 12 hours (semi-diurnal)
    - Are larger during daytime than nighttime
    - Are larger in summer than winter
    - Are larger at high latitudes than at the equator
    - Affect declination D and horizontal intensity H most strongly

    The variation is caused by electric currents in the upper atmosphere
    (ionosphere) driven by solar heating and tidal effects.

    Args:
        hour: Local time in hours (0-24).
        latitude: Geographic latitude (degrees).
        season: 'equinox', 'summer', or 'winter'.
        elements: List of elements to compute ['D', 'H', 'I', 'Z'].
                 If None, computes D and H.

    Returns:
        Dictionary with variation amplitudes (in gauss for intensities,
        radians for angles):
        - delta_D: Declination variation
        - delta_H: Horizontal intensity variation
        - delta_I: Inclination variation
        - delta_Z: Vertical variation

    Reference:
        Part III, Art. 472: Diurnal variation.

    Note:
        Amplitudes are approximate and vary with solar cycle and location.
        Typical values: delta_D ~ 0.1-0.5 degrees, delta_H ~ 10-50 nT.
    """
    if elements is None:
        elements = ['D', 'H']

    # Convert to radians
    lat_rad = np.radians(latitude)
    hour_angle = 2 * np.pi * (hour / 24)  # Radians

    # Season factor
    season_factors = {
        'equinox': 1.0,
        'summer': 1.3,
        'winter': 0.7,
    }
    season_factor = season_factors.get(season, 1.0)

    # Latitude factor (larger at high latitudes)
    lat_factor = abs(np.sin(lat_rad)) + 0.1

    # Diurnal variation model (simplified harmonic)
    # Primary 24-hour period
    daily = np.sin(hour_angle - np.pi/4)  # Peak around 1 PM
    # Secondary 12-hour period
    semi_daily = 0.3 * np.sin(2 * hour_angle)

    combined = daily + semi_daily

    result = {}

    # Declination variation (typical amplitude ~0.1-0.5 degrees)
    if 'D' in elements:
        delta_D = 0.003 * season_factor * lat_factor * combined  # radians
        result['delta_D'] = float(delta_D)
        result['delta_D_degrees'] = float(np.degrees(delta_D))

    # Horizontal intensity variation (typical amplitude ~10-50 nT = 1-5e-7 gauss)
    if 'H' in elements:
        delta_H = 2e-6 * season_factor * lat_factor * combined  # gauss
        result['delta_H'] = float(delta_H)
        result['delta_H_nT'] = float(delta_H * 1e5)  # nanoTesla

    # Inclination variation (smaller than D)
    if 'I' in elements:
        delta_I = 0.001 * season_factor * lat_factor * combined  # radians
        result['delta_I'] = float(delta_I)
        result['delta_I_degrees'] = float(np.degrees(delta_I))

    # Vertical component variation
    if 'Z' in elements:
        delta_Z = 1e-6 * season_factor * lat_factor * combined  # gauss
        result['delta_Z'] = float(delta_Z)
        result['delta_Z_nT'] = float(delta_Z * 1e5)

    result['hour'] = hour
    result['latitude'] = latitude
    result['season'] = season

    return result


@maxwell_cite(
    473,
    part=3, chapter="Terrestrial Magnetism",
    theory_class="maxwell_original",
    description="Magnetic storm effects on Earth's field",
)
def magnetic_storm(
    storm_intensity: str = 'moderate',
    latitude: float = 50.0,
    storm_phase: str = 'main',
) -> Dict[str, float]:
    """
    Calculate magnetic storm perturbations of Earth's field.

    Art. 473: Magnetic storms are irregular, worldwide disturbances of
    Earth's magnetic field caused by solar activity (coronal mass ejections,
    solar flares). Storm characteristics:

    - Sudden commencement (SC): Sharp increase in H
    - Main phase: Large decrease in H (ring current effect)
    - Recovery phase: Gradual return to normal

    Storm effects:
    - H decreases by 50-500 nT during main phase
    - D can change by several degrees
    - Auroral electrojets cause rapid fluctuations
    - Effects are largest at high latitudes

    Args:
        storm_intensity: 'weak', 'moderate', 'strong', or 'severe'.
        latitude: Geographic latitude (degrees).
        storm_phase: 'commencement', 'main', or 'recovery'.

    Returns:
        Dictionary with storm perturbations:
        - delta_H: Horizontal intensity change (gauss)
        - delta_D: Declination change (radians)
        - delta_Z: Vertical component change (gauss)
        - Dst_index: Storm-time disturbance index (nT)

    Reference:
        Part III, Art. 473: Magnetic storms.

    Note:
        Storm magnitudes are highly variable. This provides typical values.
    """
    # Storm intensity factors
    intensity_factors = {
        'weak': 1.0,
        'moderate': 3.0,
        'strong': 10.0,
        'severe': 30.0,
    }
    factor = intensity_factors.get(storm_intensity, 1.0)

    # Phase factors
    phase_effects = {
        'commencement': {'H': 1, 'sign': 1},   # H increases
        'main': {'H': 3, 'sign': -1},          # H decreases strongly
        'recovery': {'H': 1, 'sign': 0.5},     # Partial recovery
    }
    phase = phase_effects.get(storm_phase, phase_effects['main'])

    # Latitude enhancement (storms stronger at high latitudes)
    lat_rad = np.radians(latitude)
    lat_factor = 1 + 2 * abs(np.sin(lat_rad))

    # Storm-time disturbance index Dst (negative during main phase)
    base_Dst = -50 * factor * phase['sign']  # nT
    Dst = base_Dst * lat_factor

    # Horizontal intensity change (related to Dst)
    delta_H = Dst * 1e-5 * phase['H']  # Convert nT to gauss

    # Declination disturbance (larger at high latitudes)
    delta_D = 0.01 * factor * lat_factor * phase['sign']  # radians

    # Vertical component disturbance
    delta_Z = 0.5 * delta_H * np.sign(lat_rad)  # Smaller than H change

    return {
        'delta_H': float(delta_H),
        'delta_H_nT': float(delta_H * 1e5),
        'delta_D': float(delta_D),
        'delta_D_degrees': float(np.degrees(delta_D)),
        'delta_Z': float(delta_Z),
        'delta_Z_nT': float(delta_Z * 1e5),
        'Dst_index_nT': float(Dst),
        'storm_intensity': storm_intensity,
        'storm_phase': storm_phase,
        'latitude': latitude,
    }


# =============================================================================
# MAGNETIC POTENTIAL (Art. 474)
# =============================================================================

@maxwell_cite(
    474,
    part=3, chapter="Terrestrial Magnetism",
    theory_class="maxwell_original",
    description="Earth's magnetic scalar potential",
)
def earth_magnetic_potential(
    latitude: float,
    longitude: float,
    radius: float = None,
    gauss_coeffs: Dict[str, float] = None,
    max_degree: int = 5,
) -> Dict[str, float]:
    """
    Calculate Earth's magnetic scalar potential using Gauss expansion.

    Art. 474: The Earth's magnetic field derives from a scalar potential V
    that satisfies Laplace's equation (no magnetic monopoles):

        nabla^2 V = 0

    Gauss showed that V can be expanded in spherical harmonics:

        V(r, theta, phi) = R * sum_{n=1}^{N} sum_{m=0}^{n} (R/r)^{n+1} *
                          [g_n^m * cos(m*phi) + h_n^m * sin(m*phi)] * P_n^m(cos(theta))

    where:
    - R = Earth's mean radius (6.371e8 cm)
    - r = radial distance from Earth's center
    - theta = colatitude (90 - latitude)
    - phi = longitude
    - g_n^m, h_n^m = Gauss coefficients
    - P_n^m = Associated Legendre functions of degree n, order m

    The magnetic field is H = -grad(V).

    Args:
        latitude: Geographic latitude (degrees).
        longitude: Geographic longitude (degrees).
        radius: Distance from Earth's center (cm). Default = Earth radius.
        gauss_coeffs: Dictionary of Gauss coefficients {g_1_0: ..., g_1_1: ..., ...}.
                     If None, uses dipole approximation.
        max_degree: Maximum degree for expansion.

    Returns:
        Dictionary with:
        - V: Scalar potential (gauss·cm)
        - H_north: North component = -dV/dtheta
        - H_east: East component = -(1/sin(theta)) * dV/dphi
        - H_down: Vertical component = -dV/dr

    Reference:
        Part III, Art. 474: Magnetic potential of the Earth.
    """
    # Earth radius in cm
    R = 6.371e8

    # Use Earth radius if not specified
    r = radius if radius is not None else R

    # Convert to spherical coordinates
    theta = np.radians(90 - latitude)  # Colatitude
    phi = np.radians(longitude)  # Longitude

    # Default dipole coefficients (approximate IGRF values, scaled for CGS)
    # g_1_0 ~ -0.3 Gauss, g_1_1 ~ 0.02, h_1_1 ~ -0.06
    if gauss_coeffs is None:
        gauss_coeffs = {
            'g_1_0': -0.30,
            'g_1_1': 0.02,
            'h_1_1': -0.06,
        }

    # Compute potential using spherical harmonics
    V = 0.0

    # Helper: Associated Legendre functions (unnormalized)
    def P(n, m, x):
        """Compute associated Legendre function P_n^m(x)."""
        from math import factorial, sqrt

        # Simple implementation for low degrees
        if n == 1:
            if m == 0:
                return x
            elif m == 1:
                return -sqrt(1 - x**2)
        elif n == 2:
            if m == 0:
                return 0.5 * (3*x**2 - 1)
            elif m == 1:
                return -3*x*sqrt(1 - x**2)
            elif m == 2:
                return 3*(1 - x**2)
        elif n == 3:
            if m == 0:
                return 0.5 * (5*x**3 - 3*x)
            elif m == 1:
                return -1.5 * (5*x**2 - 1)*sqrt(1 - x**2)
            elif m == 2:
                return 15*x*(1 - x**2)
            elif m == 3:
                return -15*(1 - x**2)**1.5

        # General recurrence for higher degrees
        x_val = x
        if abs(x_val) > 1:
            x_val = np.sign(x_val) * 1.0

        P_mm = 1.0
        for i in range(1, m + 1):
            P_mm *= -sqrt(1 - x_val**2) * (2*i - 1)

        if n == m:
            return P_mm

        P_m1m = x_val * (2*m + 1) * P_mm

        if n == m + 1:
            return P_m1m

        P = P_m1m
        for k in range(m + 2, n + 1):
            P_new = ((2*k - 1) * x_val * P - (k + m - 1) * P_m1m) / (k - m)
            P_m1m = P
            P = P_new

        return P

    cos_theta = np.cos(theta)
    x = cos_theta

    # Sum over degrees and orders
    for n in range(1, min(max_degree + 1, 6)):  # Limit to n=5 for this implementation
        r_factor = (R / r) ** (n + 1)

        for m in range(n + 1):
            # Get coefficient
            g_nm = gauss_coeffs.get(f'g_{n}_{m}', 0)
            h_nm = gauss_coeffs.get(f'h_{n}_{m}', 0)

            if g_nm == 0 and h_nm == 0:
                continue

            # Associated Legendre function
            P_nm = P(n, m, x)

            # Longitude terms
            cos_mphi = np.cos(m * phi)
            sin_mphi = np.sin(m * phi)

            # Add contribution
            V += R * r_factor * (g_nm * cos_mphi + h_nm * sin_mphi) * P_nm

    # Compute field components numerically
    dtheta = 1e-6
    dphi = 1e-6
    dr = 1e6  # 10 km

    # H_north = -dV/dtheta
    theta_plus = theta + dtheta
    theta_minus = theta - dtheta

    def compute_V(th, ph, rad):
        """Helper to compute V at given coordinates."""
        V_local = 0.0
        ct = np.cos(th)
        for n in range(1, min(max_degree + 1, 6)):
            r_fact = (R / rad) ** (n + 1)
            for m in range(n + 1):
                g_nm = gauss_coeffs.get(f'g_{n}_{m}', 0)
                h_nm = gauss_coeffs.get(f'h_{n}_{m}', 0)
                if g_nm == 0 and h_nm == 0:
                    continue
                P_nm = P(n, m, ct)
                V_local += R * r_fact * (g_nm * np.cos(m * ph) + h_nm * np.sin(m * ph)) * P_nm
        return V_local

    V_plus = compute_V(theta_plus, phi, r)
    V_minus = compute_V(theta_minus, phi, r)
    H_north = -(V_plus - V_minus) / (2 * dtheta)

    # H_east = -(1/sin(theta)) * dV/dphi
    phi_plus = phi + dphi
    phi_minus = phi - dphi
    V_phi_plus = compute_V(theta, phi_plus, r)
    V_phi_minus = compute_V(theta, phi_minus, r)
    sin_theta = np.sin(theta)
    if abs(sin_theta) > 1e-10:
        H_east = -(V_phi_plus - V_phi_minus) / (2 * dphi * sin_theta)
    else:
        H_east = 0.0

    # H_down = -dV/dr
    V_r_plus = compute_V(theta, phi, r + dr)
    V_r_minus = compute_V(theta, phi, r - dr)
    H_down = -(V_r_plus - V_r_minus) / (2 * dr)

    return {
        'V': float(V),
        'H_north': float(H_north),
        'H_east': float(H_east),
        'H_down': float(H_down),
        'latitude': latitude,
        'longitude': longitude,
        'radius_cm': r,
    }


@maxwell_cite(
    474,
    part=3, chapter="Terrestrial Magnetism",
    theory_class="maxwell_original",
    description="Gauss coefficients for geomagnetic field",
)
def gauss_coefficients(
    epoch: float = 1873.0,
    model: str = 'dipole',
) -> Dict[str, float]:
    """
    Provide Gauss coefficients for Earth's magnetic field.

    Art. 474: The Gauss coefficients g_n^m and h_n^m completely specify
    Earth's magnetic potential at a given epoch. These coefficients
    slowly change with time (secular variation).

    Maxwell's epoch (1873) coefficients were among the first determined
    by Gauss's method. Modern determinations use satellite data.

    Args:
        epoch: Year (decimal) for coefficients. Default 1873 (Maxwell's time).
        model: 'dipole' (n=1 only), 'quadrupole' (n=1,2), or 'octupole' (n=1,2,3).

    Returns:
        Dictionary with Gauss coefficients in gauss:
        - g_1_0, g_1_1, h_1_1: Dipole terms (dominant)
        - g_2_0, g_2_1, g_2_2, h_2_1, h_2_2: Quadrupole terms
        - g_3_0, g_3_1, g_3_2, g_3_3, h_3_1, h_3_2, h_3_3: Octupole terms

    Reference:
        Part III, Art. 474: Gauss coefficients.

    Note:
        Values are approximate and for educational purposes.
        For research, use IGRF or other modern models.
    """
    # Approximate coefficients for ~1873 epoch (CGS units: gauss)
    # Based on historical determinations by Gauss, Weber, and others
    # These are simplified/approximate values

    dipole_coeffs = {
        # Axial dipole (tilted ~11.5 degrees from rotation axis)
        'g_1_0': -0.290,  # Main axial dipole
        'g_1_1': 0.015,   # Equatorial dipole component
        'h_1_1': -0.055,  # Equatorial dipole component
    }

    quadrupole_coeffs = {
        'g_2_0': -0.025,
        'g_2_1': 0.012,
        'g_2_2': 0.018,
        'h_2_1': -0.008,
        'h_2_2': 0.005,
    }

    octupole_coeffs = {
        'g_3_0': 0.010,
        'g_3_1': -0.005,
        'g_3_2': 0.003,
        'g_3_3': 0.002,
        'h_3_1': 0.004,
        'h_3_2': -0.002,
        'h_3_3': 0.001,
    }

    coeffs = {}

    if model in ['dipole', 'quadrupole', 'octupole']:
        coeffs.update(dipole_coeffs)

    if model in ['quadrupole', 'octupole']:
        coeffs.update(quadrupole_coeffs)

    if model == 'octupole':
        coeffs.update(octupole_coeffs)

    # Secular variation (simplified linear drift)
    years_from_1873 = epoch - 1873.0
    if years_from_1873 != 0:
        # Typical secular variation rates (gauss/year)
        sv_rates = {
            'g_1_0': -0.00005,
            'g_1_1': 0.00002,
            'h_1_1': -0.00008,
        }
        for key in coeffs:
            if key in sv_rates:
                coeffs[key] += sv_rates[key] * years_from_1873

    return {
        'epoch': epoch,
        'model': model,
        'coefficients': coeffs,
        'units': 'gauss',
        'note': 'Approximate values for educational use. Use IGRF for research.',
    }


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

@maxwell_cite(
    465, 466, 467, 468, 469, 470, 471, 472, 473, 474,
    part=3, chapter="Terrestrial Magnetism",
    theory_class="maxwell_original",
    description="Complete terrestrial magnetism analysis pipeline",
)
def terrestrial_analysis(
    latitude: float,
    longitude: float,
    include_diurnal: bool = True,
    include_potential: bool = True,
) -> Dict[str, any]:
    """
    Perform complete terrestrial magnetism analysis for a location.

    This function combines all aspects of Maxwell's terrestrial magnetism
    theory (Arts. 465-474) into a comprehensive analysis:

    1. Earth's field components (Arts. 465-466)
    2. Seven magnetic elements (Art. 467)
    3. Observatory protocol (Art. 468)
    4. Spherical harmonic analysis setup (Arts. 469-470)
    5. Diurnal variation (Arts. 472-473)
    6. Magnetic potential (Art. 474)

    Args:
        latitude: Geographic latitude (degrees).
        longitude: Geographic longitude (degrees).
        include_diurnal: Whether to compute diurnal variation.
        include_potential: Whether to compute magnetic potential.

    Returns:
        Comprehensive dictionary with all analysis results.

    Reference:
        Part III, Arts. 465-474: Complete terrestrial magnetism theory.
    """
    from datetime import datetime

    # 1. Earth's field components (dipole approximation)
    field = earth_field_components(latitude, longitude)

    # 2. Seven magnetic elements
    elements = magnetic_elements(
        X=field['X'], Y=field['Y'], Z=field['Z']
    )

    # 3. Observatory data
    observatory = magnetic_observatory_protocol(
        station_name=f"Station_{latitude}_{longitude}",
        latitude=latitude,
        longitude=longitude,
        measurements={'H': elements['H'], 'D': elements['D'], 'I': elements['I']},
    )

    # 4. Gauss spherical analysis setup
    gauss_analysis = gauss_spherical_analysis(
        survey_data={'stations': [{'latitude': latitude, 'longitude': longitude,
                                   'elements': elements}]},
        max_degree=5,
    )

    result = {
        'location': {
            'latitude': latitude,
            'longitude': longitude,
        },
        'field_components': field,
        'magnetic_elements': elements,
        'observatory': observatory,
        'gauss_analysis': gauss_analysis,
    }

    # 5. Diurnal variation
    if include_diurnal:
        hour = datetime.utcnow().hour + datetime.utcnow().minute / 60
        diurnal = diurnal_variation(
            hour=hour,
            latitude=latitude,
            season='equinox',
        )
        result['diurnal_variation'] = diurnal

    # 6. Magnetic potential
    if include_potential:
        coeffs = gauss_coefficients(epoch=1873.0, model='dipole')
        potential = earth_magnetic_potential(
            latitude=latitude,
            longitude=longitude,
            gauss_coeffs=coeffs['coefficients'],
        )
        result['magnetic_potential'] = potential
        result['gauss_coefficients'] = coeffs

    return result

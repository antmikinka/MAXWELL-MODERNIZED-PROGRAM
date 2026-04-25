# Field Computation Helper Utilities

## Purpose

Helper functions for electromagnetic field computations. These utilities provide common operations used across physics implementations.

## Module: field_computation_helper.py

```python
"""
Field Computation Helper Utilities

Common operations for electromagnetic field calculations.
Used across electrostatics, magnetostatics, and electrodynamics.

Maxwell Articles: Various (see individual functions)
"""

import numpy as np
from typing import Tuple, Union, Optional
from maxwell.core.vector import VectorField, ScalarField
from maxwell.core.units import cgs_units


def r_vector(source_pos: np.ndarray, obs_pos: np.ndarray) -> Tuple[np.ndarray, float]:
    """
    Compute displacement vector from source to observation point.
    
    Parameters
    ----------
    source_pos : np.ndarray
        Source position [x, y, z] in cm
    obs_pos : np.ndarray
        Observation point [x, y, z] in cm
    
    Returns
    -------
    r_vec : np.ndarray
        Displacement vector r = obs - source (cm)
    r_mag : float
        Distance |r| (cm)
    
    Raises
    ------
    ValueError
        If observation point coincides with source
    
    Examples
    --------
    >>> r_vec, r_mag = r_vector([0, 0, 0], [1, 0, 0])
    >>> r_vec
    array([1., 0., 0.])
    >>> r_mag
    1.0
    """
    source = np.asarray(source_pos, dtype=np.float64)
    obs = np.asarray(obs_pos, dtype=np.float64)
    
    r_vec = obs - source
    r_mag = np.linalg.norm(r_vec)
    
    if r_mag == 0:
        raise ValueError("Observation point coincides with source")
    
    return r_vec, r_mag


def unit_vector(v: np.ndarray) -> np.ndarray:
    """
    Compute unit vector in direction of v.
    
    Parameters
    ----------
    v : np.ndarray
        Input vector
    
    Returns
    -------
    v_hat : np.ndarray
        Unit vector v/|v|
    """
    mag = np.linalg.norm(v)
    if mag == 0:
        raise ValueError("Cannot normalize zero vector")
    return v / mag


def dipole_field(p: np.ndarray, r_vec: np.ndarray, r_mag: float) -> np.ndarray:
    """
    Compute field from point dipole.
    
    Formula: E = [3(p·r̂)r̂ - p] / r³
    
    Applies to both electric and magnetic dipoles.
    
    Parameters
    ----------
    p : np.ndarray
        Dipole moment vector (statcoulomb·cm or erg/gauss)
    r_vec : np.ndarray
        Displacement vector from dipole to observation (cm)
    r_mag : float
        Distance from dipole (cm)
    
    Returns
    -------
    field : np.ndarray
        Field vector (statvolt/cm or gauss)
    
    Maxwell Articles
    ----------------
    - Electric dipole: Arts. 69-71, 113-116
    - Magnetic dipole: Arts. 385-392
    """
    p = np.asarray(p, dtype=np.float64)
    r_hat = r_vec / r_mag
    
    # E = [3(p·r̂)r̂ - p] / r³
    p_dot_r = np.dot(p, r_hat)
    field = (3 * p_dot_r * r_hat - p) / r_mag**3
    
    return field


def monopole_field(q: float, r_vec: np.ndarray, r_mag: float) -> np.ndarray:
    """
    Compute field from point monopole (charge or magnetic pole).
    
    Formula: E = q·r̂/r² = q·r/r³
    
    Parameters
    ----------
    q : float
        Source strength (statcoulomb or magnetic pole)
    r_vec : np.ndarray
        Displacement vector (cm)
    r_mag : float
        Distance (cm)
    
    Returns
    -------
    field : np.ndarray
        Field vector
    
    Maxwell Articles
    ----------------
    - Electric charge: Arts. 44-49
    - Magnetic pole: Arts. 371-376
    """
    return q * r_vec / r_mag**3


def superpose_fields(fields: list, positions: list) -> np.ndarray:
    """
    Superpose multiple field contributions.
    
    Parameters
    ----------
    fields : list of np.ndarray
        Field vectors at observation point
    positions : list
        Source positions (for validation)
    
    Returns
    -------
    total_field : np.ndarray
        Vector sum of all fields
    
    Maxwell Articles
    ----------------
    - Superposition principle: Art. 84
    """
    total = np.zeros(3, dtype=np.float64)
    for field in fields:
        total += np.asarray(field, dtype=np.float64)
    return total


def compute_divergence(field_func, point: np.ndarray, 
                       h: float = 1e-6) -> float:
    """
    Compute numerical divergence of a vector field.
    
    ∇·F = ∂F_x/∂x + ∂F_y/∂y + ∂F_z/∂z
    
    Parameters
    ----------
    field_func : callable
        Function that returns field vector at given point
    point : np.ndarray
        Point at which to compute divergence
    h : float
        Step size for finite difference (cm)
    
    Returns
    -------
    div : float
        Divergence at point
    
    Uses central difference for 2nd order accuracy.
    """
    point = np.asarray(point, dtype=np.float64)
    div = 0.0
    
    for i in range(3):
        plus = point.copy()
        minus = point.copy()
        plus[i] += h
        minus[i] -= h
        
        f_plus = np.asarray(field_func(plus), dtype=np.float64)
        f_minus = np.asarray(field_func(minus), dtype=np.float64)
        
        div += (f_plus[i] - f_minus[i]) / (2 * h)
    
    return div


def compute_curl(field_func, point: np.ndarray,
                 h: float = 1e-6) -> np.ndarray:
    """
    Compute numerical curl of a vector field.
    
    (∇×F)_x = ∂F_z/∂y - ∂F_y/∂z
    (∇×F)_y = ∂F_x/∂z - ∂F_z/∂x
    (∇×F)_z = ∂F_y/∂x - ∂F_x/∂y
    
    Parameters
    ----------
    field_func : callable
        Function that returns field vector at given point
    point : np.ndarray
        Point at which to compute curl
    h : float
        Step size for finite difference (cm)
    
    Returns
    -------
    curl : np.ndarray
        Curl vector at point
    """
    point = np.asarray(point, dtype=np.float64)
    
    def partial(F_component, var_idx, pt, h):
        plus = pt.copy()
        minus = pt.copy()
        plus[var_idx] += h
        minus[var_idx] -= h
        return (F_component(plus) - F_component(minus)) / (2 * h)
    
    # curl_x = ∂F_z/∂y - ∂F_y/∂z
    curl_x = partial(lambda p: field_func(p)[2], 1, point, h) - \
             partial(lambda p: field_func(p)[1], 2, point, h)
    
    # curl_y = ∂F_x/∂z - ∂F_z/∂x
    curl_y = partial(lambda p: field_func(p)[0], 2, point, h) - \
             partial(lambda p: field_func(p)[2], 0, point, h)
    
    # curl_z = ∂F_y/∂x - ∂F_x/∂y
    curl_z = partial(lambda p: field_func(p)[1], 0, point, h) - \
             partial(lambda p: field_func(p)[0], 1, point, h)
    
    return np.array([curl_x, curl_y, curl_z])


def compute_gradient(scalar_func, point: np.ndarray,
                     h: float = 1e-6) -> np.ndarray:
    """
    Compute numerical gradient of a scalar field.
    
    (∇φ)_i = ∂φ/∂x_i
    
    Parameters
    ----------
    scalar_func : callable
        Function that returns scalar value at given point
    point : np.ndarray
        Point at which to compute gradient
    h : float
        Step size for finite difference (cm)
    
    Returns
    -------
    grad : np.ndarray
        Gradient vector at point
    """
    point = np.asarray(point, dtype=np.float64)
    grad = np.zeros(3, dtype=np.float64)
    
    for i in range(3):
        plus = point.copy()
        minus = point.copy()
        plus[i] += h
        minus[i] -= h
        
        grad[i] = (scalar_func(plus) - scalar_func(minus)) / (2 * h)
    
    return grad


def verify_solenoidal(field_func, test_points: list,
                      tolerance: float = 1e-8) -> bool:
    """
    Verify that a field is solenoidal (∇·F = 0).
    
    Parameters
    ----------
    field_func : callable
        Field function
    test_points : list
        Points at which to test
    tolerance : float
        Maximum allowed divergence
    
    Returns
    -------
    is_solenoidal : bool
        True if divergence is zero within tolerance
    
    Maxwell Articles
    ----------------
    - Art. 403-404: Solenoidal condition for B
    """
    for point in test_points:
        div = compute_divergence(field_func, point)
        if abs(div) > tolerance:
            return False
    return True


def verify_conservative(field_func, test_points: list,
                        tolerance: float = 1e-8) -> bool:
    """
    Verify that a field is conservative (∇×F = 0).
    
    Parameters
    ----------
    field_func : callable
        Field function
    test_points : list
        Points at which to test
    tolerance : float
        Maximum allowed curl
    
    Returns
    -------
    is_conservative : bool
        True if curl is zero within tolerance
    
    Maxwell Articles
    ----------------
    - Art. 24: Electrostatic field is conservative
    """
    for point in test_points:
        curl = compute_curl(field_func, point)
        if np.linalg.norm(curl) > tolerance:
            return False
    return True


def spherical_to_cartesian(r: float, theta: float, phi: float) -> np.ndarray:
    """
    Convert spherical coordinates to Cartesian.
    
    Parameters
    ----------
    r : float
        Radial distance (cm)
    theta : float
        Polar angle from z-axis (radians)
    phi : float
        Azimuthal angle from x-axis (radians)
    
    Returns
    -------
    xyz : np.ndarray
        Cartesian coordinates [x, y, z] (cm)
    """
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return np.array([x, y, z])


def cartesian_to_spherical(x: float, y: float, z: float) -> Tuple[float, float, float]:
    """
    Convert Cartesian coordinates to spherical.
    
    Parameters
    ----------
    x, y, z : float
        Cartesian coordinates (cm)
    
    Returns
    -------
    r : float
        Radial distance (cm)
    theta : float
        Polar angle from z-axis (radians)
    phi : float
        Azimuthal angle from x-axis (radians)
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z / r) if r > 0 else 0
    phi = np.arctan2(y, x)
    return r, theta, phi


def vector_in_spherical_basis(F_cart: np.ndarray, 
                               theta: float, phi: float) -> np.ndarray:
    """
    Transform vector from Cartesian to spherical basis.
    
    Parameters
    ----------
    F_cart : np.ndarray
        Vector in Cartesian basis [F_x, F_y, F_z]
    theta : float
        Polar angle (radians)
    phi : float
        Azimuthal angle (radians)
    
    Returns
    -------
    F_sph : np.ndarray
        Vector in spherical basis [F_r, F_θ, F_φ]
    """
    sin_t, cos_t = np.sin(theta), np.cos(theta)
    sin_p, cos_p = np.sin(phi), np.cos(phi)
    
    # Transformation matrix
    F_r = sin_t * cos_p * F_cart[0] + sin_t * sin_p * F_cart[1] + cos_t * F_cart[2]
    F_theta = cos_t * cos_p * F_cart[0] + cos_t * sin_p * F_cart[1] - sin_t * F_cart[2]
    F_phi = -sin_p * F_cart[0] + cos_p * F_cart[1]
    
    return np.array([F_r, F_theta, F_phi])
```

## Usage Examples

```python
from maxwell.utils.field_computation_helper import (
    r_vector, dipole_field, monopole_field,
    compute_divergence, compute_curl, verify_conservative
)
import numpy as np

# Example 1: Point charge field
q = 1.0  # statcoulomb
source = np.array([0, 0, 0])
obs = np.array([1, 0, 0])

r_vec, r_mag = r_vector(source, obs)
E = monopole_field(q, r_vec, r_mag)
print(f"E at (1,0,0): {E} statvolt/cm")

# Example 2: Dipole field
p = np.array([0, 0, 10])  # dipole moment in z-direction
E_dipole = dipole_field(p, r_vec, r_mag)
print(f"Dipole field at (1,0,0): {E_dipole} statvolt/cm")

# Example 3: Verify electrostatic field is conservative
def E_field(point):
    return monopole_field(1.0, point - source, np.linalg.norm(point - source))

is_conservative = verify_conservative(E_field, [
    np.array([1, 0, 0]),
    np.array([0, 1, 0]),
    np.array([0, 0, 1])
])
print(f"Field is conservative: {is_conservative}")
```

## Related Utilities

- `unit_converter.py` - Unit conversions
- `validation_helper.py` - Physics validation

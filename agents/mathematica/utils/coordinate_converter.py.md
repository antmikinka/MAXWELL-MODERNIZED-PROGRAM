# Utility: Coordinate System Converter

## Description

Utility for converting between coordinate systems and transforming fields accordingly.

## Purpose

Provide reliable coordinate conversion with proper handling of:
- Position transformation
- Vector component transformation
- Differential operator transformation
- Scale factor computation

## Implementation

```python
"""
Coordinate System Converter Utility

Maxwell Articles: 15-27 (vector foundations)
"""

import numpy as np
from typing import Tuple, Callable
from maxwell.core.citation import cite_article


@cite_article([15, 16, 17, 23, 24, 25])
class CoordinateConverter:
    """
    Convert between Cartesian, cylindrical, and spherical coordinates.
    
    Attributes
    ----------
    source_system : str
        Source coordinate system
    target_system : str
        Target coordinate system
    """
    
    def __init__(self, source: str = 'cartesian', target: str = 'cartesian'):
        self.source = source
        self.target = target
    
    # === Coordinate Transformations ===
    
    def cartesian_to_cylindrical(
        self,
        x: float,
        y: float,
        z: float
    ) -> Tuple[float, float, float]:
        """
        Convert Cartesian (x, y, z) to cylindrical (ρ, φ, z).
        
        Returns
        -------
        rho : float
            Radial distance (always ≥ 0)
        phi : float
            Azimuthal angle in radians (-π to π)
        z : float
            Height (unchanged)
        """
        rho = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x)
        return rho, phi, z
    
    def cylindrical_to_cartesian(
        self,
        rho: float,
        phi: float,
        z: float
    ) -> Tuple[float, float, float]:
        """
        Convert cylindrical (ρ, φ, z) to Cartesian (x, y, z).
        """
        x = rho * np.cos(phi)
        y = rho * np.sin(phi)
        return x, y, z
    
    def cartesian_to_spherical(
        self,
        x: float,
        y: float,
        z: float
    ) -> Tuple[float, float, float]:
        """
        Convert Cartesian (x, y, z) to spherical (r, θ, φ).
        
        Returns
        -------
        r : float
            Radial distance (always ≥ 0)
        theta : float
            Polar angle in radians (0 to π)
        phi : float
            Azimuthal angle in radians (-π to π)
        """
        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arccos(z / r) if r > 0 else 0
        phi = np.arctan2(y, x)
        return r, theta, phi
    
    def spherical_to_cartesian(
        self,
        r: float,
        theta: float,
        phi: float
    ) -> Tuple[float, float, float]:
        """
        Convert spherical (r, θ, φ) to Cartesian (x, y, z).
        """
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        return x, y, z
    
    # === Scale Factors ===
    
    def scale_factors_cylindrical(
        self,
        rho: float,
        phi: float,
        z: float
    ) -> Tuple[float, float, float]:
        """
        Return scale factors (h_ρ, h_φ, h_z) for cylindrical coordinates.
        
        h_ρ = 1
        h_φ = ρ
        h_z = 1
        """
        return 1.0, rho, 1.0
    
    def scale_factors_spherical(
        self,
        r: float,
        theta: float,
        phi: float
    ) -> Tuple[float, float, float]:
        """
        Return scale factors (h_r, h_θ, h_φ) for spherical coordinates.
        
        h_r = 1
        h_θ = r
        h_φ = r sin θ
        """
        return 1.0, r, r * np.sin(theta)
    
    # === Vector Component Transformation ===
    
    def vector_cartesian_to_cylindrical(
        self,
        Fx: float,
        Fy: float,
        Fz: float,
        phi: float
    ) -> Tuple[float, float, float]:
        """
        Transform vector components from Cartesian to cylindrical.
        
        F_ρ = F_x cos φ + F_y sin φ
        F_φ = -F_x sin φ + F_y cos φ
        F_z = F_z
        """
        cos_phi = np.cos(phi)
        sin_phi = np.sin(phi)
        
        F_rho = Fx * cos_phi + Fy * sin_phi
        F_phi = -Fx * sin_phi + Fy * cos_phi
        F_z = Fz
        
        return F_rho, F_phi, F_z
    
    def vector_cartesian_to_spherical(
        self,
        Fx: float,
        Fy: float,
        Fz: float,
        theta: float,
        phi: float
    ) -> Tuple[float, float, float]:
        """
        Transform vector components from Cartesian to spherical.
        
        F_r = F_x sin θ cos φ + F_y sin θ sin φ + F_z cos θ
        F_θ = F_x cos θ cos φ + F_y cos θ sin φ - F_z sin θ
        F_φ = -F_x sin φ + F_y cos φ
        """
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        sin_phi = np.sin(phi)
        cos_phi = np.cos(phi)
        
        F_r = Fx * sin_theta * cos_phi + Fy * sin_theta * sin_phi + Fz * cos_theta
        F_theta = Fx * cos_theta * cos_phi + Fy * cos_theta * sin_phi - Fz * sin_theta
        F_phi = -Fx * sin_phi + Fy * cos_phi
        
        return F_r, F_theta, F_phi
    
    # === Full Field Conversion ===
    
    def convert_position(
        self,
        position: np.ndarray,
        source: str = None,
        target: str = None
    ) -> np.ndarray:
        """
        Convert position from one coordinate system to another.
        """
        source = source or self.source
        target = target or self.target
        
        if source == target:
            return position
        
        if source == 'cartesian' and target == 'cylindrical':
            return np.array(self.cartesian_to_cylindrical(*position))
        elif source == 'cylindrical' and target == 'cartesian':
            return np.array(self.cylindrical_to_cartesian(*position))
        elif source == 'cartesian' and target == 'spherical':
            return np.array(self.cartesian_to_spherical(*position))
        elif source == 'spherical' and target == 'cartesian':
            return np.array(self.spherical_to_cartesian(*position))
        else:
            # Convert via Cartesian
            if source == 'cylindrical':
                cart = self.cylindrical_to_cartesian(*position)
            else:  # spherical
                cart = self.spherical_to_cartesian(*position)
            
            if target == 'cylindrical':
                return np.array(self.cartesian_to_cylindrical(*cart))
            else:  # spherical
                return np.array(self.cartesian_to_spherical(*cart))
    
    def convert_vector_components(
        self,
        components: np.ndarray,
        position: np.ndarray,
        source: str = None,
        target: str = None
    ) -> np.ndarray:
        """
        Convert vector components between coordinate systems.
        
        Note: Position is needed to determine the local basis vectors.
        """
        source = source or self.source
        target = target or self.target
        
        if source == target:
            return components
        
        # Convert to Cartesian first, then to target
        if source == 'cartesian':
            Fx, Fy, Fz = components
        elif source == 'cylindrical':
            rho, phi, z = position
            F_rho, F_phi, F_z = components
            # Cylindrical to Cartesian
            Fx = F_rho * np.cos(phi) - F_phi * np.sin(phi)
            Fy = F_rho * np.sin(phi) + F_phi * np.cos(phi)
            Fz = F_z
        else:  # spherical
            r, theta, phi = position
            F_r, F_theta, F_phi = components
            # Spherical to Cartesian
            Fx = F_r * np.sin(theta) * np.cos(phi) + F_theta * np.cos(theta) * np.cos(phi) - F_phi * np.sin(phi)
            Fy = F_r * np.sin(theta) * np.sin(phi) + F_theta * np.cos(theta) * np.sin(phi) + F_phi * np.cos(phi)
            Fz = F_r * np.cos(theta) - F_theta * np.sin(theta)
        
        # Now convert from Cartesian to target
        if target == 'cartesian':
            return np.array([Fx, Fy, Fz])
        elif target == 'cylindrical':
            rho, phi, z = self.cartesian_to_cylindrical(Fx, Fy, Fz)
            # Use position's phi, not converted
            _, phi, _ = position if source != 'cylindrical' else (None, position[1], None)
            return self.vector_cartesian_to_cylindrical(Fx, Fy, Fz, phi)
        else:  # spherical
            r, theta, phi = self.cartesian_to_spherical(Fx, Fy, Fz)
            _, theta, phi = position if source != 'spherical' else (None, position[1], position[2])
            return self.vector_cartesian_to_spherical(Fx, Fy, Fz, theta, phi)


# Convenience functions
@cite_article([23, 24, 25])
def convert_coordinates(
    position: np.ndarray,
    source: str,
    target: str
) -> np.ndarray:
    """
    Convert position between coordinate systems.
    
    Parameters
    ----------
    position : np.ndarray
        Position in source coordinates
    source : str
        Source coordinate system
    target : str
        Target coordinate system
    
    Returns
    -------
    np.ndarray
        Position in target coordinates
    """
    converter = CoordinateConverter(source, target)
    return converter.convert_position(position, source, target)
```

## Usage Examples

```python
from maxwell.mathematics.utils import CoordinateConverter

converter = CoordinateConverter()

# Position conversion
cart_pos = np.array([1.0, 1.0, 1.0])
spherical_pos = converter.convert_position(cart_pos, 'cartesian', 'spherical')
print(f"Spherical: r={spherical_pos[0]:.3f}, θ={spherical_pos[1]:.3f}, φ={spherical_pos[2]:.3f}")

# Vector component transformation
cart_vec = np.array([1.0, 0.0, 0.0])
spherical_vec = converter.convert_vector_components(
    cart_vec, 
    cart_pos,
    'cartesian',
    'spherical'
)
```

## Maxwell Article References

| Article | Content |
|---------|---------|
| 15-18 | Vector quantities |
| 23-27 | Vector operations in different coordinates |

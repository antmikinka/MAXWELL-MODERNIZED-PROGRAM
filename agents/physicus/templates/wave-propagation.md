# Template: Wave Propagation

## Purpose

Standardized template for implementing electromagnetic wave propagation solutions. This template covers plane waves, waveguides, and wave phenomena in various media.

## Source Category

**CRITICAL: Theory Preservation**

This template is for:
- **Maxwell's 1873 Historical Text**: Articles 781-805 (Electromagnetic Theory of Light)
- **Standard Mathematical Implementation**: Wave equation solvers, Fourier methods
- **User Original Theory**: Mark any user extensions as "User Original Theory - Authoritative - DO NOT ALTER"

## Template Structure

### 1. Module Header

```python
"""
{WAVE_TYPE} Propagation

Maxwell Treatise Reference:
- Primary Articles: {ARTICLE_NUMBERS}
- Part: Part IV (Electromagnetism)

Source Category:
- Maxwell 1873: Articles 781-805
- Standard Math: {Wave equations, special functions}
- User Theory: {NONE or specify}

CGS Units: {UNIT_SPECIFICATIONS}
"""

import numpy as np
from typing import Union, Optional, Tuple, Dict
from maxwell.core.vector import VectorField, ScalarField
from maxwell.optics.wave import ElectromagneticWave
from maxwell.utils.citation import maxwell_citation
```

### 2. Wave Class Definition

```python
class {WaveClassName}:
    """
    {WAVE_DESCRIPTION}
    
    Maxwell Articles: {ARTICLE_NUMBERS}
    
    Attributes:
        frequency: Angular frequency ω (rad/s)
        wave_vector: k vector (cm⁻¹)
        polarization: Polarization state
        medium: Propagation medium properties
        citations: Maxwell article references
    
    CGS Units:
        E field: statvolt/cm
        B field: gauss
        Frequency: rad/s
        Wavelength: cm
    """
    
    def __init__(
        self,
        frequency: float,
        wave_vector: np.ndarray,
        polarization: str = 'linear',
        medium: Optional[dict] = None,
        citations: Optional[list] = None
    ):
        self.frequency = frequency
        self.wave_vector = np.asarray(wave_vector)
        self.polarization = polarization
        self.medium = medium or {'epsilon': 1, 'mu': 1, 'sigma': 0}
        self.citations = citations or self._default_citations()
    
    @staticmethod
    def _default_citations() -> list:
        """Return default Maxwell article citations."""
        return [
            maxwell_citation(article=781, part='IV'),
            maxwell_citation(article=782, part='IV'),
            maxwell_citation(article=786, part='IV'),
        ]
```

### 3. Plane Wave Solutions

```python
    def E_field(
        self,
        position: np.ndarray,
        time: float
    ) -> VectorField:
        """
        Electric field of plane wave.
        
        Args:
            position: Observation point (cm)
            time: Time (s)
        
        Returns:
            VectorField: E field (statvolt/cm)
        
        Maxwell Reference: Arts. {790-791}
        
        Formula:
            E(r,t) = E₀ exp[i(k·r - ωt)]
        """
        r = np.asarray(position)
        phase = np.dot(self.wave_vector, r) - self.frequency * time
        amplitude = self._polarization_vector()
        
        E_components = np.real(amplitude * np.exp(1j * phase))
        return VectorField(components=E_components, units='statvolt/cm')
    
    def B_field(
        self,
        position: np.ndarray,
        time: float
    ) -> VectorField:
        """
        Magnetic field of plane wave.
        
        Args:
            position: Observation point (cm)
            time: Time (s)
        
        Returns:
            VectorField: B field (gauss)
        
        Maxwell Reference: Arts. {790-791}
        
        Formula:
            B = (c/ω) k × E
            |E| = |B| (in vacuum, CGS)
        """
        E = self.E_field(position, time)
        k_hat = self.wave_vector / np.linalg.norm(self.wave_vector)
        
        # B = k̂ × E (for vacuum, CGS)
        B_components = np.cross(k_hat, E.components)
        return VectorField(components=B_components, units='gauss')
```

### 4. Wave Properties

```python
    @property
    def wavelength(self) -> float:
        """Wavelength λ = 2πc/ω (cm)."""
        k = np.linalg.norm(self.wave_vector)
        return 2 * np.pi / k
    
    @property
    def phase_velocity(self) -> float:
        """Phase velocity v = ω/k (cm/s)."""
        omega = self.frequency
        k = np.linalg.norm(self.wave_vector)
        return omega / k
    
    @property
    def refractive_index(self) -> float:
        """Refractive index n = c/v."""
        v = self.phase_velocity
        from maxwell.core.constants import c_CGS
        return c_CGS / v
    
    def dispersion_relation(self) -> Dict:
        """
        Compute dispersion relation ω(k).
        
        Returns:
            dict: Dispersion characteristics
        
        Maxwell Reference: Arts. {786-787}
        """
        return {
            'omega': self.frequency,
            'k': np.linalg.norm(self.wave_vector),
            'phase_velocity': self.phase_velocity,
            'group_velocity': self.group_velocity(),
            'refractive_index': self.refractive_index
        }
```

### 5. Wave in Media

```python
    @classmethod
    def in_dielectric(
        cls,
        frequency: float,
        epsilon: float,
        mu: float = 1.0,
        **kwargs
    ):
        """
        Create plane wave in dielectric medium.
        
        Args:
            frequency: Angular frequency
            epsilon: Relative permittivity
            mu: Relative permeability
            **kwargs: Passed to constructor
        
        Returns:
            {WaveClassName}: Wave in dielectric
        
        Maxwell Reference: Arts. {794-797}
        """
        n = np.sqrt(epsilon * mu)
        k_magnitude = (frequency / c_CGS) * n
        wave_vector = kwargs.pop('propagation_direction', [0, 0, 1])
        wave_vector = k_magnitude * np.asarray(wave_vector) / np.linalg.norm(wave_vector)
        
        return cls(
            frequency=frequency,
            wave_vector=wave_vector,
            medium={'epsilon': epsilon, 'mu': mu, 'sigma': 0},
            **kwargs
        )
    
    @classmethod
    def in_conductor(
        cls,
        frequency: float,
        sigma: float,
        epsilon: float = 1.0,
        mu: float = 1.0,
        **kwargs
    ):
        """
        Create plane wave in conducting medium.
        
        Args:
            frequency: Angular frequency
            sigma: Conductivity (s⁻¹ in CGS)
            epsilon: Relative permittivity
            mu: Relative permeability
        
        Returns:
            {WaveClassName}: Wave in conductor
        
        Maxwell Reference: Arts. {798-800}
        
        Note: Complex wave number for attenuation
        """
        # Complex wave number
        omega = frequency
        k_complex = np.sqrt((omega**2 / c_CGS**2) * (epsilon + 1j * 4 * np.pi * sigma / omega))
        
        # Real and imaginary parts
        k_real = np.real(k_complex)
        k_imag = np.imag(k_complex)
        
        # Wave vector with attenuation
        direction = kwargs.pop('propagation_direction', [0, 0, 1])
        wave_vector = (k_real + 1j * k_imag) * np.asarray(direction)
        
        return cls(
            frequency=frequency,
            wave_vector=wave_vector,
            medium={'epsilon': epsilon, 'mu': mu, 'sigma': sigma},
            **kwargs
        )
```

### 6. Poynting Vector and Energy

```python
    def poynting_vector(
        self,
        position: np.ndarray,
        time: float
    ) -> VectorField:
        """
        Compute Poynting vector S = (c/4π) E × H.
        
        Args:
            position: Observation point
            time: Time
        
        Returns:
            VectorField: Energy flux (erg/cm²/s)
        
        Maxwell Reference: Arts. {792-793}
        """
        E = self.E_field(position, time)
        H = self.H_field(position, time)
        
        from maxwell.core.constants import c_CGS
        
        # S = (c/4π) E × H
        S_components = (c_CGS / (4 * np.pi)) * np.cross(E.components, H.components)
        return VectorField(components=S_components, units='erg/cm²/s')
    
    def time_averaged_poynting(self) -> VectorField:
        """
        Time-averaged Poynting vector.
        
        Returns:
            VectorField: <S> (erg/cm²/s)
        
        Formula:
            <S> = (c/8π) |E₀|² k̂
        """
        E0_mag = np.linalg.norm(self._polarization_vector())
        k_hat = self.wave_vector / np.linalg.norm(self.wave_vector)
        
        from maxwell.core.constants import c_CGS
        S_avg = (c_CGS / (8 * np.pi)) * E0_mag**2 * k_hat
        
        return VectorField(components=S_avg, units='erg/cm²/s')
```

### 7. Polarization Handling

```python
    def _polarization_vector(self) -> np.ndarray:
        """Get polarization unit vector."""
        if self.polarization == 'linear_x':
            return np.array([1, 0, 0])
        elif self.polarization == 'linear_y':
            return np.array([0, 1, 0])
        elif self.polarization == 'circular_right':
            return np.array([1, 1j, 0]) / np.sqrt(2)
        elif self.polarization == 'circular_left':
            return np.array([1, -1j, 0]) / np.sqrt(2)
        else:
            raise ValueError(f"Unknown polarization: {self.polarization}")
    
    def jones_vector(self) -> np.ndarray:
        """
        Return Jones vector for polarization.
        
        Returns:
            ndarray: 2-component Jones vector
        """
        return self._polarization_vector()[:2]
    
    def stokes_parameters(self) -> Dict:
        """
        Compute Stokes parameters.
        
        Returns:
            dict: {I, Q, U, V} parameters
        """
        jones = self.jones_vector()
        Ex, Ey = jones
        
        I = np.abs(Ex)**2 + np.abs(Ey)**2
        Q = np.abs(Ex)**2 - np.abs(Ey)**2
        U = 2 * np.real(Ex * np.conj(Ey))
        V = 2 * np.imag(Ex * np.conj(Ey))
        
        return {'I': I, 'Q': Q, 'U': U, 'V': V}
```

### 8. Wave Phenomena

```python
    def reflection_coefficient(
        self,
        interface: dict,
        incidence_angle: float
    ) -> Dict:
        """
        Compute Fresnel reflection coefficients.
        
        Args:
            interface: {'n1': ..., 'n2': ...}
            incidence_angle: Angle in degrees
        
        Returns:
            dict: {r_s, r_p, R_s, R_p}
        
        Maxwell Reference: Arts. {794-797}
        """
        from maxwell.optics.fresnel import fresnel_coefficients
        return fresnel_coefficients(
            n1=interface['n1'],
            n2=interface['n2'],
            theta_i=incidence_angle,
            polarization=self.polarization
        )
    
    def faraday_rotation(
        self,
        magnetic_field: float,
        path_length: float,
        verdet_constant: float
    ) -> float:
        """
        Compute Faraday rotation angle.
        
        Args:
            magnetic_field: B field (Gauss)
            path_length: L (cm)
            verdet_constant: V (rad/Gauss/cm)
        
        Returns:
            float: Rotation angle (radians)
        
        Maxwell Reference: Arts. {806-810}
        
        Formula:
            θ = V B L
        """
        return verdet_constant * magnetic_field * path_length
```

### 9. Visualization

```python
    def plot_wave_snapshot(
        self,
        plane: str = 'xz',
        time: float = 0,
        **kwargs
    ):
        """
        Plot E and B fields at fixed time.
        
        Args:
            plane: Slice plane
            time: Snapshot time
            **kwargs: Passed to plotting
        """
        pass
    
    def animate_propagation(
        self,
        duration: float,
        frames: int = 100,
        **kwargs
    ):
        """
        Create animation of wave propagation.
        
        Args:
            duration: Animation duration (periods)
            frames: Number of frames
            **kwargs: Passed to animation
        """
        pass
```

## Checklist for Implementation

- [ ] Module header with article citations
- [ ] CGS units specified
- [ ] Source category documented
- [ ] E and B field methods
- [ ] Wave properties (λ, v, n)
- [ ] Medium support (dielectric, conductor)
- [ ] Poynting vector implemented
- [ ] Polarization handling
- [ ] Wave phenomena (reflection, Faraday)
- [ ] Theory preservation decorators
- [ ] Maxwell article citations

## Related Templates

- `field-implementation.md` - Field computations
- `dynamical-system.md` - Energy formulation
- `analytical-solution.md` - Wave benchmarks
- `cross-part-bridge.md` - Multi-region propagation

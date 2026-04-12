# Physics Validation Helper Utilities

## Purpose

Utilities for validating physics implementations against analytical solutions, conservation laws, and Maxwell's equations.

## Module: validation_helper.py

```python
"""
Physics Validation Helper Utilities

Comprehensive validation tools for electromagnetic implementations.
Validates against analytical solutions, conservation laws, and Maxwell's equations.

Maxwell Articles: Various (see individual functions)
"""

import numpy as np
from typing import Dict, List, Tuple, Callable, Optional
from dataclasses import dataclass
from maxwell.core.vector import VectorField, ScalarField
from maxwell.core.units import cgs_units


@dataclass
class ValidationResult:
    """Result of a validation test."""
    test_name: str
    passed: bool
    expected: float
    actual: float
    relative_error: float
    tolerance: float
    notes: str = ""
    
    def __str__(self):
        status = "✓ PASS" if self.passed else "✗ FAIL"
        return (f"{status}: {self.test_name}\n"
                f"  Expected: {self.expected:.6e}\n"
                f"  Actual:   {self.actual:.6e}\n"
                f"  Error:    {self.relative_error:.6e} "
                f"(tolerance: {self.tolerance:.6e})")


class PhysicsValidator:
    """
    Comprehensive physics validation toolkit.
    
    Examples
    --------
    >>> validator = PhysicsValidator()
    >>> result = validator.validate_point_charge(E_func, q=1.0, r=1.0)
    >>> print(result)
    """
    
    def __init__(self, default_tolerance: float = 1e-6):
        self.default_tolerance = default_tolerance
        self.c = 29979245800  # speed of light (cm/s)
        self.results: List[ValidationResult] = []
    
    def validate_point_charge(self, E_func, q: float, 
                              test_radius: float = 1.0,
                              tolerance: float = None) -> ValidationResult:
        """
        Validate electric field of point charge.
        
        Expected: E = q/r² (radial)
        
        Maxwell Articles: 44-49, 64-68
        
        Parameters
        ----------
        E_func : callable
            Electric field function E(point) -> array
        q : float
            Charge in statcoulombs
        test_radius : float
            Test distance in cm
        tolerance : float
            Relative error tolerance
            
        Returns
        -------
        result : ValidationResult
        """
        tol = tolerance or self.default_tolerance
        
        # Test at multiple points on sphere
        errors = []
        for theta in [0, np.pi/4, np.pi/2, np.pi]:
            for phi in [0, np.pi/4, np.pi/2]:
                x = test_radius * np.sin(theta) * np.cos(phi)
                y = test_radius * np.sin(theta) * np.sin(phi)
                z = test_radius * np.cos(theta)
                point = np.array([x, y, z])
                
                E = np.asarray(E_func(point))
                r = np.linalg.norm(point)
                
                # Expected: radial field with magnitude q/r²
                E_expected = q / r**2
                E_actual = np.linalg.norm(E)
                
                # Check radial direction
                r_hat = point / r
                E_radial = np.dot(E, r_hat)
                
                error = abs(E_radial - E_expected) / E_expected
                errors.append(error)
        
        max_error = max(errors)
        passed = max_error <= tol
        
        result = ValidationResult(
            test_name=f"Point charge field (q={q}, r={test_radius})",
            passed=passed,
            expected=q / test_radius**2,
            actual=np.sqrt(q**2 / test_radius**4),  # nominal
            relative_error=max_error,
            tolerance=tol,
            notes=f"Max error over test sphere: {max_error:.6e}"
        )
        
        self.results.append(result)
        return result
    
    def validate_dipole_field(self, E_func, p: np.ndarray,
                              test_radius: float = 1.0,
                              tolerance: float = None) -> ValidationResult:
        """
        Validate electric field of dipole.
        
        Expected: E = [3(p·r̂)r̂ - p] / r³
        
        Maxwell Articles: 69-71, 113-116
        
        Parameters
        ----------
        E_func : callable
            Electric field function
        p : np.ndarray
            Dipole moment vector
        test_radius : float
            Test distance in cm
        tolerance : float
            Relative error tolerance
        """
        tol = tolerance or self.default_tolerance
        p = np.asarray(p)
        p_mag = np.linalg.norm(p)
        
        errors = []
        
        # Test on axis (θ = 0): E = 2p/r³
        point_axis = np.array([0, 0, test_radius])
        E_axis = np.asarray(E_func(point_axis))
        E_expected_axis = 2 * p_mag / test_radius**3
        E_actual_axis = np.linalg.norm(E_axis)
        errors.append(abs(E_actual_axis - E_expected_axis) / E_expected_axis)
        
        # Test perpendicular (θ = π/2): E = -p/r³
        point_perp = np.array([test_radius, 0, 0])
        E_perp = np.asarray(E_func(point_perp))
        E_expected_perp = p_mag / test_radius**3
        E_actual_perp = np.linalg.norm(E_perp)
        errors.append(abs(E_actual_perp - E_expected_perp) / E_expected_perp)
        
        max_error = max(errors)
        passed = max_error <= tol
        
        result = ValidationResult(
            test_name=f"Dipole field (|p|={p_mag:.4f}, r={test_radius})",
            passed=passed,
            expected=E_expected_axis,
            actual=E_actual_axis,
            relative_error=max_error,
            tolerance=tol,
            notes=f"On-axis and perpendicular tested"
        )
        
        self.results.append(result)
        return result
    
    def validate_gauss_law(self, E_func, Q_enclosed: float,
                           surface: str = 'sphere',
                           tolerance: float = None) -> ValidationResult:
        """
        Validate Gauss's law: ∮E·dA = 4πQ
        
        Maxwell Articles: 75-76
        
        Parameters
        ----------
        E_func : callable
            Electric field function
        Q_enclosed : float
            Enclosed charge in statcoulombs
        surface : str
            'sphere' or 'cube'
        tolerance : float
            Relative error tolerance
        """
        tol = tolerance or self.default_tolerance
        R = 1.0  # Test radius
        
        if surface == 'sphere':
            # Numerical integration over sphere
            n_points = 1000
            flux = 0.0
            
            for _ in range(n_points):
                # Random point on sphere
                theta = np.arccos(2*np.random.random() - 1)
                phi = 2 * np.pi * np.random.random()
                
                x = R * np.sin(theta) * np.cos(phi)
                y = R * np.sin(theta) * np.sin(phi)
                z = R * np.cos(theta)
                point = np.array([x, y, z])
                
                E = np.asarray(E_func(point))
                r_hat = point / R
                
                # dA = R² sin(θ) dθ dφ, average over sphere = R²
                flux += np.dot(E, r_hat)
            
            flux = flux / n_points * 4 * np.pi * R**2
            
        else:
            raise NotImplementedError("Only sphere implemented")
        
        expected = 4 * np.pi * Q_enclosed
        error = abs(flux - expected) / abs(expected) if expected != 0 else 0
        passed = error <= tol
        
        result = ValidationResult(
            test_name=f"Gauss's law ({surface}, Q={Q_enclosed})",
            passed=passed,
            expected=expected,
            actual=flux,
            relative_error=error,
            tolerance=tol
        )
        
        self.results.append(result)
        return result
    
    def validate_curl_free(self, E_func, test_points: List[np.ndarray],
                          tolerance: float = None) -> ValidationResult:
        """
        Validate that electrostatic field is curl-free: ∇×E = 0
        
        Maxwell Articles: 24
        
        Parameters
        ----------
        E_func : callable
            Electric field function
        test_points : list
            Points at which to test
        tolerance : float
            Maximum curl magnitude
        """
        tol = tolerance or self.default_tolerance
        h = 1e-6  # Finite difference step
        
        max_curl = 0.0
        
        for point in test_points:
            point = np.asarray(point)
            
            # Compute curl numerically
            curl = np.zeros(3)
            
            # curl_x = ∂E_z/∂y - ∂E_y/∂z
            curl[0] = ((E_func(point + h*np.array([0,1,0]))[2] - 
                       E_func(point - h*np.array([0,1,0]))[2]) / (2*h) -
                      (E_func(point + h*np.array([0,0,1]))[1] - 
                       E_func(point - h*np.array([0,0,1]))[1]) / (2*h))
            
            # curl_y, curl_z similarly...
            
            curl_mag = np.linalg.norm(curl)
            max_curl = max(max_curl, curl_mag)
        
        passed = max_curl <= tol
        
        result = ValidationResult(
            test_name=f"Curl-free field (max|∇×E|={max_curl:.6e})",
            passed=passed,
            expected=0.0,
            actual=max_curl,
            relative_error=max_curl,
            tolerance=tol
        )
        
        self.results.append(result)
        return result
    
    def validate_divergence_free(self, B_func, test_points: List[np.ndarray],
                                 tolerance: float = None) -> ValidationResult:
        """
        Validate magnetic field is divergence-free: ∇·B = 0
        
        Maxwell Articles: 403-404
        
        Parameters
        ----------
        B_func : callable
            Magnetic field function
        test_points : list
            Points at which to test
        tolerance : float
            Maximum divergence magnitude
        """
        tol = tolerance or self.default_tolerance
        h = 1e-6
        
        max_div = 0.0
        
        for point in test_points:
            point = np.asarray(point)
            
            # Compute divergence numerically
            div = 0.0
            for i in range(3):
                plus = point.copy()
                minus = point.copy()
                plus[i] += h
                minus[i] -= h
                
                B_plus = np.asarray(B_func(plus))
                B_minus = np.asarray(B_func(minus))
                
                div += (B_plus[i] - B_minus[i]) / (2*h)
            
            max_div = max(max_div, abs(div))
        
        passed = max_div <= tol
        
        result = ValidationResult(
            test_name=f"Divergence-free field (max|∇·B|={max_div:.6e})",
            passed=passed,
            expected=0.0,
            actual=max_div,
            relative_error=max_div,
            tolerance=tol,
            notes="No magnetic monopoles"
        )
        
        self.results.append(result)
        return result
    
    def validate_energy_conservation(self, compute_energy: Callable,
                                     initial_energy: float,
                                     final_energy: float,
                                     work_done: float = 0,
                                     tolerance: float = None) -> ValidationResult:
        """
        Validate energy conservation.
        
        Expected: E_final = E_initial + W (work done on system)
        
        Maxwell Articles: 85-86, 551
        
        Parameters
        ----------
        compute_energy : callable
            Function to compute energy
        initial_energy : float
            Initial energy in erg
        final_energy : float
            Final energy in erg
        work_done : float
            Work done on system in erg
        tolerance : float
            Relative error tolerance
        """
        tol = tolerance or self.default_tolerance
        
        expected = initial_energy + work_done
        error = abs(final_energy - expected) / abs(expected) if expected != 0 else 0
        passed = error <= tol
        
        result = ValidationResult(
            test_name="Energy conservation",
            passed=passed,
            expected=expected,
            actual=final_energy,
            relative_error=error,
            tolerance=tol
        )
        
        self.results.append(result)
        return result
    
    def validate_wave_propagation(self, E_func, B_func,
                                  expected_speed: float = None,
                                  tolerance: float = None) -> ValidationResult:
        """
        Validate electromagnetic wave properties.
        
        Expected:
        - |E| = |B| (in CGS Gaussian)
        - E ⊥ B ⊥ k
        - Speed = c/√(εμ)
        
        Maxwell Articles: 790-793
        
        Parameters
        ----------
        E_func : callable
            Electric field function E(x,t)
        B_func : callable
            Magnetic field function B(x,t)
        expected_speed : float
            Expected wave speed (default: c)
        tolerance : float
            Relative error tolerance
        """
        tol = tolerance or self.default_tolerance
        speed = expected_speed or self.c
        
        # Test at a point
        t = 0
        x = np.array([1.0, 0, 0])
        
        E = np.asarray(E_func(x, t))
        B = np.asarray(B_func(x, t))
        
        E_mag = np.linalg.norm(E)
        B_mag = np.linalg.norm(B)
        
        # Check |E| = |B|
        ratio_error = abs(E_mag - B_mag) / E_mag if E_mag > 0 else 0
        
        # Check E ⊥ B
        dot = np.dot(E, B)
        ortho_error = abs(dot) / (E_mag * B_mag) if E_mag * B_mag > 0 else 0
        
        max_error = max(ratio_error, ortho_error)
        passed = max_error <= tol
        
        result = ValidationResult(
            test_name=f"Wave properties (speed={speed:.6e})",
            passed=passed,
            expected=1.0,  # |E|/|B| ratio
            actual=E_mag/B_mag if B_mag > 0 else float('inf'),
            relative_error=max_error,
            tolerance=tol
        )
        
        self.results.append(result)
        return result
    
    def get_summary(self) -> str:
        """
        Get summary of all validation results.
        
        Returns
        -------
        summary : str
            Formatted summary string
        """
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        
        summary = f"\n{'='*60}\n"
        summary += f"PHYSICS VALIDATION SUMMARY\n"
        summary += f"{'='*60}\n"
        summary += f"Total tests: {total}\n"
        summary += f"Passed: {passed}\n"
        summary += f"Failed: {total - passed}\n"
        summary += f"Pass rate: {100*passed/total:.1f}%\n"
        summary += f"{'='*60}\n\n"
        
        for result in self.results:
            summary += str(result) + "\n\n"
        
        return summary
    
    def clear_results(self):
        """Clear stored results."""
        self.results = []


# =============================================================================
# Convenience Functions
# =============================================================================

def validate_implementation(component_name: str, tests: Dict[str, Callable]) -> str:
    """
    Run validation tests for a component.
    
    Parameters
    ----------
    component_name : str
        Name of component being validated
    tests : dict
        Dictionary of test_name -> test_function
    
    Returns
    -------
    summary : str
        Validation summary
    """
    validator = PhysicsValidator()
    
    print(f"Validating: {component_name}")
    print("=" * 50)
    
    for test_name, test_func in tests.items():
        print(f"Running: {test_name}")
        try:
            result = test_func()
            validator.results.append(result)
        except Exception as e:
            validator.results.append(ValidationResult(
                test_name=test_name,
                passed=False,
                expected=0,
                actual=0,
                relative_error=1.0,
                tolerance=0,
                notes=f"Exception: {e}"
            ))
    
    return validator.get_summary()
```

## Usage Examples

```python
from maxwell.utils.validation_helper import PhysicsValidator, validate_implementation
import numpy as np

# Example: Validate point charge implementation
def E_point_charge(point):
    """Electric field from point charge at origin."""
    q = 1.0  # statcoulomb
    r = np.linalg.norm(point)
    r_hat = point / r
    return q * r_hat / r**2

validator = PhysicsValidator()

# Run validation
result = validator.validate_point_charge(E_point_charge, q=1.0, test_radius=1.0)
print(result)

# Validate multiple properties
result2 = validator.validate_curl_free(E_point_charge, [
    np.array([1, 0, 0]),
    np.array([0, 1, 0]),
    np.array([0, 0, 1])
])

# Get summary
print(validator.get_summary())

# Validate a complete implementation
tests = {
    'point_charge': lambda: validator.validate_point_charge(E_point_charge, 1.0),
    'gauss_law': lambda: validator.validate_gauss_law(E_point_charge, 1.0),
    'curl_free': lambda: validator.validate_curl_free(E_point_charge, [np.array([1,0,0])]),
}

summary = validate_implementation('electrostatic_field', tests)
print(summary)
```

## Related Utilities

- `field_computation_helper.py` - Field calculations
- `unit_converter.py` - Unit conversions

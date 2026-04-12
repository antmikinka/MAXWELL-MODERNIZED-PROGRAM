# Utility: Validation Helper

## Description

Utility for mathematical validation including analytical comparison, identity verification, and convergence testing.

## Purpose

Provide reusable validation functions for testing mathematical implementations against known results.

## Implementation

```python
"""
Validation Helper for Mathematical Implementations

Provides utilities for verifying mathematical correctness
through analytical comparison, identity verification, and
convergence testing.

Maxwell Articles: 15-27 (vector identities), 77-78 (Laplace)
"""

import numpy as np
from typing import Callable, Dict, Any, Tuple
from dataclasses import dataclass
from maxwell.core.citation import cite_article


@dataclass
class ValidationResult:
    """Container for validation test results."""
    test_name: str
    passed: bool
    error: float
    tolerance: float
    details: Dict[str, Any]


@cite_article([20, 21, 22, 23, 24, 25, 26, 27])
class VectorCalculusValidator:
    """
    Validator for vector calculus operations.
    """
    
    def __init__(self, tolerance: float = 1e-10):
        self.tolerance = tolerance
    
    def verify_curl_gradient(
        self,
        scalar_field: Callable,
        gradient_func: Callable,
        curl_func: Callable,
        test_points: np.ndarray
    ) -> ValidationResult:
        """
        Verify that curl(grad φ) = 0 for any scalar field.
        
        Parameters
        ----------
        scalar_field : callable
            Scalar field φ(x, y, z)
        gradient_func : callable
            Function that computes ∇φ
        curl_func : callable
            Function that computes ∇×F
        test_points : np.ndarray
            Array of (x, y, z) test points
        
        Returns
        -------
        ValidationResult
            Result of the verification
        """
        max_norm = 0.0
        
        for point in test_points:
            # Compute gradient
            grad_phi = gradient_func(scalar_field, point)
            
            # Compute curl of gradient
            curl_grad = curl_func(grad_phi, point)
            
            # Compute norm
            norm = np.linalg.norm(curl_grad)
            max_norm = max(max_norm, norm)
        
        passed = max_norm < self.tolerance
        
        return ValidationResult(
            test_name="curl(grad φ) = 0",
            passed=passed,
            error=max_norm,
            tolerance=self.tolerance,
            details={"test_points": len(test_points), "max_norm": max_norm}
        )
    
    def verify_divergence_curl(
        self,
        vector_field: Callable,
        divergence_func: Callable,
        curl_func: Callable,
        test_points: np.ndarray
    ) -> ValidationResult:
        """
        Verify that div(curl F) = 0 for any vector field.
        """
        max_value = 0.0
        
        for point in test_points:
            # Compute curl
            curl_F = curl_func(vector_field, point)
            
            # Compute divergence of curl
            div_curl = divergence_func(curl_F, point)
            
            max_value = max(max_value, abs(div_curl))
        
        passed = max_value < self.tolerance
        
        return ValidationResult(
            test_name="div(curl F) = 0",
            passed=passed,
            error=max_value,
            tolerance=self.tolerance,
            details={"test_points": len(test_points), "max_value": max_value}
        )
    
    def verify_stokes_theorem(
        self,
        vector_field: Callable,
        curl_func: Callable,
        surface: Any,
        boundary: Any,
        line_integral_func: Callable,
        surface_integral_func: Callable
    ) -> ValidationResult:
        """
        Verify Stokes' theorem: ∮_C F·dl = ∫_S (∇×F)·n dS
        
        Parameters
        ----------
        vector_field : callable
            Vector field F
        curl_func : callable
            Curl operator
        surface : Any
            Surface definition
        boundary : Any
            Boundary curve definition
        line_integral_func : callable
            Computes ∮_C F·dl
        surface_integral_func : callable
            Computes ∫_S (∇×F)·n dS
        
        Returns
        -------
        ValidationResult
        """
        # Compute line integral
        circulation = line_integral_func(vector_field, boundary)
        
        # Compute surface integral of curl
        curl = lambda p: curl_func(vector_field, p)
        flux_of_curl = surface_integral_func(curl, surface)
        
        # Compare
        error = abs(circulation - flux_of_curl)
        relative_error = error / (abs(circulation) + 1e-15)
        
        passed = relative_error < self.tolerance
        
        return ValidationResult(
            test_name="Stokes' theorem",
            passed=passed,
            error=relative_error,
            tolerance=self.tolerance,
            details={
                "circulation": circulation,
                "flux_of_curl": flux_of_curl,
                "absolute_error": error
            }
        )
    
    def verify_divergence_theorem(
        self,
        vector_field: Callable,
        divergence_func: Callable,
        volume: Any,
        volume_integral_func: Callable,
        surface_integral_func: Callable
    ) -> ValidationResult:
        """
        Verify Divergence theorem: ∫_V (∇·F) dV = ∮_S F·n dS
        """
        # Compute volume integral of divergence
        div_F = lambda p: divergence_func(vector_field, p)
        volume_integral = volume_integral_func(div_F, volume)
        
        # Compute surface flux
        flux = surface_integral_func(vector_field, volume.boundary)
        
        # Compare
        error = abs(volume_integral - flux)
        relative_error = error / (abs(volume_integral) + 1e-15)
        
        passed = relative_error < self.tolerance
        
        return ValidationResult(
            test_name="Divergence theorem",
            passed=passed,
            error=relative_error,
            tolerance=self.tolerance,
            details={
                "volume_integral": volume_integral,
                "surface_flux": flux,
                "absolute_error": error
            }
        )


@cite_article([125, 126, 127, 128, 129, 130, 131, 132, 133])
class SphericalHarmonicsValidator:
    """
    Validator for spherical harmonic computations.
    """
    
    def __init__(self, tolerance: float = 1e-10):
        self.tolerance = tolerance
    
    def verify_orthogonality(
        self,
        spherical_harmonic_func: Callable,
        l_max: int,
        quadrature_order: int = 64
    ) -> ValidationResult:
        """
        Verify orthogonality of spherical harmonics.
        
        ∫ Y_l^m Y_l'^m'* dΩ = δ_ll' δ_mm'
        """
        from scipy.integrate import dblquad
        
        max_error = 0.0
        worst_case = None
        
        for l in range(l_max + 1):
            for m in range(-l, l + 1):
                for l_prime in range(l_max + 1):
                    for m_prime in range(-l_prime, l_prime + 1):
                        # Compute overlap integral
                        def integrand(phi, theta):
                            Y_lm = spherical_harmonic_func(l, m, theta, phi)
                            Y_lmp = spherical_harmonic_func(l_prime, m_prime, theta, phi)
                            return Y_lm * np.conj(Y_lmp) * np.sin(theta)
                        
                        # Numerical integration
                        result, _ = dblquad(
                            integrand,
                            0, np.pi,      # theta limits
                            lambda _: 0, lambda _: 2*np.pi  # phi limits
                        )
                        
                        # Expected value
                        expected = 1.0 if (l == l_prime and m == m_prime) else 0.0
                        
                        error = abs(result - expected)
                        if error > max_error:
                            max_error = error
                            worst_case = (l, m, l_prime, m_prime)
        
        passed = max_error < self.tolerance
        
        return ValidationResult(
            test_name="Spherical harmonic orthogonality",
            passed=passed,
            error=max_error,
            tolerance=self.tolerance,
            details={"worst_case": worst_case, "l_max": l_max}
        )
    
    def verify_addition_theorem(
        self,
        spherical_harmonic_func: Callable,
        legendre_func: Callable,
        l: int,
        n_samples: int = 100
    ) -> ValidationResult:
        """
        Verify Legendre addition theorem.
        
        P_l(cos γ) = (4π/(2l+1)) Σ_m Y_l^m(θ,φ) Y_l^m*(θ',φ')
        """
        max_error = 0.0
        
        for _ in range(n_samples):
            # Random directions
            theta = np.random.uniform(0, np.pi)
            phi = np.random.uniform(0, 2*np.pi)
            theta_prime = np.random.uniform(0, np.pi)
            phi_prime = np.random.uniform(0, 2*np.pi)
            
            # Compute cos γ from spherical law of cosines
            cos_gamma = (np.cos(theta) * np.cos(theta_prime) + 
                        np.sin(theta) * np.sin(theta_prime) * np.cos(phi - phi_prime))
            
            # Left side: P_l(cos γ)
            left = legendre_func.P(l, cos_gamma)
            
            # Right side: sum over m
            right = 0.0
            for m in range(-l, l + 1):
                Y_lm = spherical_harmonic_func(l, m, theta, phi)
                Y_lm_c = spherical_harmonic_func(l, m, theta_prime, phi_prime)
                right += Y_lm * np.conj(Y_lm_c)
            right *= (4 * np.pi / (2 * l + 1))
            
            error = abs(left - right)
            max_error = max(max_error, error)
        
        passed = max_error < self.tolerance
        
        return ValidationResult(
            test_name="Legendre addition theorem",
            passed=passed,
            error=max_error,
            tolerance=self.tolerance,
            details={"l": l, "samples": n_samples}
        )


@cite_article([77, 78, 100, 101, 102, 103])
class ConvergenceValidator:
    """
    Validator for numerical convergence analysis.
    """
    
    def __init__(self, tolerance: float = 0.1):  # 10% tolerance on order
        self.tolerance = tolerance
    
    def grid_convergence_analysis(
        self,
        solver_func: Callable,
        exact_solution: Callable,
        grid_sizes: list,
        norm: str = 'L2'
    ) -> ValidationResult:
        """
        Analyze grid convergence order.
        
        Parameters
        ----------
        solver_func : callable
            Numerical solver that takes grid size
        exact_solution : callable
            Analytical solution for comparison
        grid_sizes : list
            List of grid sizes to test
        norm : str
            Norm type ('L1', 'L2', 'Linf')
        
        Returns
        -------
        ValidationResult
            Includes computed convergence order
        """
        errors = []
        
        for size in grid_sizes:
            # Compute numerical solution
            numerical = solver_func(size)
            
            # Compute exact solution on same grid
            exact = exact_solution(numerical.grid)
            
            # Compute error
            diff = numerical.values - exact.values
            if norm == 'L2':
                error = np.sqrt(np.mean(diff**2))
            elif norm == 'L1':
                error = np.mean(np.abs(diff))
            else:  # Linf
                error = np.max(np.abs(diff))
            
            errors.append(error)
        
        # Compute convergence order using Richardson extrapolation
        orders = []
        for i in range(1, len(errors) - 1):
            r = grid_sizes[i] / grid_sizes[i-1]
            if errors[i] > 0 and errors[i-1] > 0:
                order = np.log(errors[i-1] / errors[i]) / np.log(r)
                orders.append(order)
        
        avg_order = np.mean(orders) if orders else 0
        
        # For second-order methods, expect order ≈ 2
        expected_order = 2.0  # Default assumption
        error = abs(avg_order - expected_order)
        passed = error < self.tolerance
        
        return ValidationResult(
            test_name="Grid convergence analysis",
            passed=passed,
            error=error,
            tolerance=self.tolerance,
            details={
                "grid_sizes": grid_sizes,
                "errors": errors,
                "orders": orders,
                "avg_order": avg_order,
                "expected_order": expected_order
            }
        )


def run_validation_suite(validators: list) -> Dict[str, ValidationResult]:
    """
    Run a suite of validation tests and return results.
    
    Parameters
    ----------
    validators : list
        List of validator callables
    
    Returns
    -------
    dict
        Dictionary of test name -> ValidationResult
    """
    results = {}
    
    for validator in validators:
        result = validator()
        results[result.test_name] = result
    
    return results


def print_validation_summary(results: Dict[str, ValidationResult]) -> None:
    """
    Print a summary of validation results.
    """
    print("=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for r in results.values() if r.passed)
    total = len(results)
    
    for name, result in results.items():
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {name}")
        print(f"       Error: {result.error:.6e}, Tolerance: {result.tolerance:.6e}")
    
    print("=" * 60)
    print(f"OVERALL: {passed}/{total} tests passed ({100*passed/total:.1f}%)")
    print("=" * 60)
```

## Usage Examples

```python
from maxwell.mathematics.validation import VectorCalculusValidator

validator = VectorCalculusValidator(tolerance=1e-10)

# Test points
points = np.random.rand(100, 3) * 10 - 5

# Define test scalar field
def phi(x, y, z):
    return x**2 + y**2 + z**2

# Run validation
result = validator.verify_curl_gradient(
    scalar_field=phi,
    gradient_func=compute_gradient,
    curl_func=compute_curl,
    test_points=points
)

print(f"Test: {result.test_name}")
print(f"Passed: {result.passed}")
print(f"Max error: {result.error}")
```

## Maxwell Article References

| Article | Content |
|---------|---------|
| 20-22 | Divergence theorem |
| 23-27 | Curl and vector identities |
| 77-78 | Laplace operator |
| 100-103 | Potential theory |
| 125-133 | Spherical harmonics |

# Template: Potential Solver

## Purpose

Standardized template for implementing scalar and vector potential solvers. This template covers both electrostatic potential V and magnetic scalar potential Ω, as well as vector potential A.

## Source Category

**CRITICAL: Theory Preservation**

This template is for:
- **Maxwell's 1873 Historical Text**: Articles 69-73 (Electric Potential), 385-386 (Magnetic Potential), 405-406 (Vector Potential)
- **Standard Mathematical Implementation**: PDE solvers, harmonic expansions
- **User Original Theory**: Mark any user extensions as "User Original Theory - Authoritative - DO NOT ALTER"

## Template Structure

### 1. Module Header

```python
"""
{POTENTIAL_NAME} Solver

Maxwell Treatise Reference:
- Primary Articles: {ARTICLE_NUMBERS}
- Part: {PART_NUMBER}

Source Category:
- Maxwell 1873: Articles {X-Y}
- Standard Math: {PDE solvers, special functions}
- User Theory: {NONE or specify}

CGS Units: {UNIT_SPECIFICATIONS}
"""

import numpy as np
from typing import Union, Optional, Tuple, Callable
from maxwell.core.vector import ScalarField, VectorField
from maxwell.solvers.laplace import LaplaceSolver
from maxwell.solvers.poisson import PoissonSolver
from maxwell.utils.citation import maxwell_citation
```

### 2. Potential Class Definition

```python
class {PotentialName}:
    """
    {POTENTIAL_DESCRIPTION}
    
    Maxwell Articles: {ARTICLE_NUMBERS}
    
    Attributes:
        source: Source of potential (charge, current, etc.)
        equation_type: 'laplace', 'poisson', 'vector'
        coordinate_system: 'cartesian', 'cylindrical', 'spherical'
        boundary_conditions: Dirichlet/Neumann conditions
        citations: List of Maxwell article references
    
    CGS Units:
        Scalar Potential V: statvolt
        Vector Potential A: gauss·cm
    """
    
    def __init__(
        self,
        source: {SOURCE_TYPE},
        equation_type: str = 'poisson',
        coordinate_system: str = 'cartesian',
        boundary_conditions: Optional[dict] = None,
        citations: Optional[list] = None
    ):
        self.source = source
        self.equation_type = equation_type
        self.coordinate_system = coordinate_system
        self.boundary_conditions = boundary_conditions
        self.citations = citations or self._default_citations()
    
    @staticmethod
    def _default_citations() -> list:
        """Return default Maxwell article citations."""
        return [
            maxwell_citation(article={N}, part={I}),
            # Add more as needed
        ]
```

### 3. Direct Integration Methods

```python
    def compute_direct(
        self,
        observation_points: np.ndarray
    ) -> Union[ScalarField, VectorField]:
        """
        Compute potential via direct integration.
        
        Args:
            observation_points: Positions for evaluation (cm)
        
        Returns:
            ScalarField or VectorField: Potential
        
        Maxwell Reference: Arts. {69-73}
        
        Formula:
            V(r) = ∫ ρ(r')/|r - r'| d³r'  (electrostatic)
            A(r) = (1/c) ∫ J(r')/|r - r'| d³r'  (vector potential)
        """
        r = np.asarray(observation_points)
        # Implementation here
        pass
    
    def compute_from_distribution(
        self,
        distribution: Callable,
        method: str = 'direct_integration'
    ):
        """
        Compute potential from continuous distribution.
        
        Args:
            distribution: Source density function
            method: 'direct', 'multipole', 'fft', 'greens'
        
        Returns:
            {PotentialName}: Self for chaining
        
        Maxwell Reference: Arts. {96-98}
        """
        pass
```

### 4. PDE Solution Methods

```python
    def solve_laplace(
        self,
        domain: dict,
        boundary_conditions: dict,
        method: str = 'separation_of_variables'
    ) -> ScalarField:
        """
        Solve Laplace equation ∇²V = 0.
        
        Args:
            domain: Domain specification
            boundary_conditions: Dirichlet/Neumann BCs
            method: 'separation', 'images', 'harmonics', 'numerical'
        
        Returns:
            ScalarField: Potential solution
        
        Maxwell Reference: Art. {77}
        
        Equation:
            ∇²V = 0
        """
        solver = LaplaceSolver(
            coordinate_system=self.coordinate_system,
            method=method
        )
        return solver.solve(domain, boundary_conditions)
    
    def solve_poisson(
        self,
        charge_density: Callable,
        boundary_conditions: dict,
        method: str = 'greens_function'
    ) -> ScalarField:
        """
        Solve Poisson equation ∇²V = -4πρ.
        
        Args:
            charge_density: ρ(x,y,z)
            boundary_conditions: BCs
            method: 'greens', 'finite_difference', 'finite_element'
        
        Returns:
            ScalarField: Potential solution
        
        Maxwell Reference: Art. {77}
        
        Equation:
            ∇²V = -4πρ
        """
        solver = PoissonSolver(
            coordinate_system=self.coordinate_system,
            method=method
        )
        return solver.solve(charge_density, boundary_conditions)
```

### 5. Spherical Harmonic Expansion

```python
    def expand_in_spherical_harmonics(
        self,
        boundary_potential: Callable,
        max_degree: int = 10
    ) -> dict:
        """
        Expand potential in spherical harmonics.
        
        Args:
            boundary_potential: V(θ,φ) on sphere
            max_degree: Maximum harmonic degree l_max
        
        Returns:
            dict: Expansion coefficients {l, m: A_lm, B_lm}
        
        Maxwell Reference: Arts. {128-146}
        
        Formula:
            V(r,θ,φ) = Σ_lm [A_lm r^l + B_lm r^(-l-1)] Y_lm(θ,φ)
        """
        from maxwell.math.spherical import SphericalHarmonics
        
        coeffs = SphericalHarmonics.compute_coefficients(
            boundary_potential, max_degree
        )
        return coeffs
    
    def evaluate_harmonic_expansion(
        self,
        coefficients: dict,
        r: float,
        theta: float,
        phi: float
    ) -> float:
        """
        Evaluate potential from harmonic expansion.
        
        Args:
            coefficients: From expand_in_spherical_harmonics
            r, theta, phi: Spherical coordinates
        
        Returns:
            float: Potential value
        """
        pass
```

### 6. Method of Images

```python
    @classmethod
    def method_of_images(
        cls,
        source: {SOURCE_TYPE},
        boundary: dict
    ):
        """
        Solve using method of images.
        
        Args:
            source: Original source
            boundary: {'type': 'plane'/'sphere', 'position': ...}
        
        Returns:
            {PotentialName}: With image sources included
        
        Maxwell Reference: Arts. {155-175}
        
        Examples:
            - Point charge near conducting plane
            - Point charge near conducting sphere
        """
        image_sources = cls._compute_image_sources(source, boundary)
        return cls(source=source + image_sources)
```

### 7. Vector Potential Methods

```python
    def curl(self) -> VectorField:
        """
        Compute B = ∇ × A (for vector potential).
        
        Returns:
            VectorField: Magnetic induction
        
        Maxwell Reference: Arts. {405-406}
        """
        pass
    
    def verify_gauge(self, gauge: str = 'coulomb') -> bool:
        """
        Verify gauge condition.
        
        Args:
            gauge: 'coulomb' (∇·A=0) or 'lorenz' (∇·A + (1/c)∂V/∂t=0)
        
        Returns:
            bool: True if condition satisfied
        """
        pass
```

### 8. Validation Methods

```python
    def verify_boundary_conditions(
        self,
        tolerance: float = 1e-6
    ) -> bool:
        """
        Verify boundary conditions are satisfied.
        
        Args:
            tolerance: Maximum allowable error
        
        Returns:
            bool: True if BCs satisfied
        """
        pass
    
    def verify_pde_residual(
        self,
        test_points: np.ndarray,
        tolerance: float = 1e-6
    ) -> dict:
        """
        Verify PDE is satisfied.
        
        Args:
            test_points: Points for testing
            tolerance: Maximum residual
        
        Returns:
            dict: Residual statistics
        """
        pass
```

## Template Usage Example

```python
"""
Electric Potential Solver

Maxwell Treatise Reference:
- Primary Articles: 69-73, 77
- Part: Part I (Electrostatics)

CGS Units: statvolt
"""

class ElectricPotential({PotentialName}):
    """Electrostatic potential V where E = -∇V."""
    
    @preserve_theory('maxwell')
    def point_charge_potential(self, q, r):
        """
        V = q/r
        
        Maxwell Reference: Arts. 69-73
        """
        return q / np.linalg.norm(r)
```

## Checklist for Implementation

- [ ] Module header with article citations
- [ ] CGS units specified
- [ ] Source category documented
- [ ] Direct integration implemented
- [ ] PDE solvers included
- [ ] Spherical harmonic expansion (if applicable)
- [ ] Method of images (if applicable)
- [ ] Gauge verification (for vector potential)
- [ ] Boundary condition verification
- [ ] Theory preservation decorators applied
- [ ] Maxwell article citations in docstrings

## Related Templates

- `field-implementation.md` - Field from potential
- `analytical-solution.md` - Benchmark solutions
- `cross-part-bridge.md` - Multi-part problems
- `wave-propagation.md` - Time-dependent potentials

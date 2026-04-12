# Template: numerical-method

## Description

Template for implementing numerical methods for solving electromagnetic problems that lack analytical solutions. This template ensures numerical stability, accuracy, and proper validation.

## Structure

```python
"""
Numerical Method: {method_name}

Maxwell Articles: {article_citations}
Part: {part_number} ({part_name})
Layer: {layer_number}

Numerical Scheme: {scheme_type}
Order of Accuracy: {order}
Stability: {stability_property}

Theory Classification:
- [ ] Maxwell's original formulation
- [ ] User original theory (authoritative - DO NOT CHANGE)
- [ ] Standard mathematical implementation
"""

import numpy as np
from maxwell.core.citation import cite_article
from maxwell.core.grid import Grid
from typing import {type_hints}

@cite_article([{article_numbers}], part={part})
class {NumericalSolver}:
    """
    {brief_description}
    
    Numerical Method
    ----------------
    {method_description}
    
    Discretization
    --------------
    {discretization_scheme}
    
    Stability Condition
    -------------------
    {cfl_or_stability}
    
    Physical Background
    -------------------
    {physical_explanation}
    
    Maxwell's Treatment
    -------------------
    {maxwell_original_approach}
    
    Parameters
    ----------
    {parameter_docs}
    
    Attributes
    ----------
    {attribute_docs}
    
    Methods
    -------
    {method_docs}
    
    Examples
    --------
    >>> {example_usage}
    
    Notes
    -----
    {additional_notes}
    
    CGS Units
    ---------
    {unit_specifications}
    
    References
    ----------
    - Maxwell, Article {article_numbers}: {description}
    - Numerical reference: {numerical_reference}
    
    See Also
    --------
    {related_functions}
    """
    
    def __init__(self, {init_parameters}):
        {initialization}
    
    def setup(self):
        """Initialize solver."""
        {setup_code}
    
    def step(self):
        """Advance solution by one time step."""
        {step_code}
    
    def run(self, {run_parameters}):
        """Run full simulation."""
        {run_code}
    
    def validate(self):
        """Run validation tests."""
        {validation_code}
```

## LLM Instructions

When using this template:

1. **Method Specification**: Clearly state numerical scheme and order
2. **Stability Analysis**: Include CFL or other stability conditions
3. **Convergence**: Document expected convergence rate
4. **Boundary Conditions**: Specify treatment of boundaries
5. **Validation**: Include comparison with analytical solutions
6. **CGS Units**: Maintain unit consistency throughout

## Variables

- `{method_name}`: FDTD, FEM, BEM, etc.
- `{scheme_type}`: Explicit, implicit, etc.
- `{order}`: First, second order, etc.
- `{stability_property}`: Unconditionally stable, CFL-limited
- `{method_description}`: How the method works
- `{discretization_scheme}`: Grid and difference formulas
- `{cfl_or_stability}`: Stability condition formula

## Numerical Methods

### Time Domain
| Method | Order | Stability | Use Case |
|--------|-------|-----------|----------|
| FDTD (Yee) | 2nd | CFL-limited | Wideband EM |
| Runge-Kutta 4 | 4th | CFL-limited | ODE systems |
| Crank-Nicolson | 2nd | Unconditional | Diffusion |

### Frequency Domain
| Method | Order | Stability | Use Case |
|--------|-------|-----------|----------|
| FEM | Variable | Unconditional | Complex geometry |
| BEM | Variable | Unconditional | Open boundaries |
| Spectral | Exponential | Unconditional | Smooth problems |

## Example Usage

```python
"""
Numerical Method: FDTD (Finite-Difference Time-Domain)

Maxwell Articles: 604-611, 781-785
Part: IV (Electromagnetism)
Layer: 74

Numerical Scheme: Yee lattice, leapfrog time integration
Order of Accuracy: 2nd order in space and time
Stability: CFL condition dt ≤ dx/(c√D)

Theory Classification:
- [ ] Maxwell's original formulation
- [ ] User original theory
- [x] Standard mathematical implementation
"""

import numpy as np
from maxwell.core.citation import cite_article
from maxwell.core.grid import Grid, YeeCell
from typing import Tuple, Optional

@cite_article([604, 605, 606, 607, 781, 782, 783, 784, 785], part='IV')
class FDTDSolver:
    """
    Finite-Difference Time-Domain solver for Maxwell's equations.
    
    Numerical Method
    ----------------
    Yee lattice with staggered E and H fields.
    Leapfrog time integration (E at integer steps, H at half-steps).
    
    Discretization
    --------------
    Spatial: 2nd order central differences on Yee cell
    Temporal: 2nd order leapfrog
    
    Update equations (CGS Gaussian):
    E^(n+1) = E^n + (c dt/dx) × (∇×H)^(n+1/2) - (4π dt) J^(n+1/2)
    H^(n+3/2) = H^(n+1/2) - (c dt/dx) × (∇×E)^(n+1)
    
    Stability Condition
    -------------------
    CFL: dt ≤ min(dx,dy,dz) / (c √3)
    
    For 3D: dt ≤ dx / (c √3) where dx is smallest cell dimension
    
    Physical Background
    -------------------
    FDTD directly discretizes Maxwell's time-dependent equations,
    providing the full temporal evolution of electromagnetic fields.
    It is particularly useful for wideband problems and complex geometries.
    
    Maxwell's Treatment
    -------------------
    While Maxwell did not use numerical methods, his time-dependent
    equations (Articles 604-611) are the foundation of this solver.
    The wave propagation follows Articles 781-785.
    
    Parameters
    ----------
    grid : Grid
        Computational domain with Yee cell structure
    dt : float
        Time step in seconds
    cfl : float
        CFL number (0 < cfl ≤ 1, typically 0.99)
    pml_layers : int
        Number of PML absorbing boundary layers
    pml_reflection : float
        Target PML reflection coefficient
    
    Attributes
    ----------
    Ex, Ey, Ez : ndarray
        Electric field components
    Hx, Hy, Hz : ndarray
        Magnetic field components
    epsilon : ndarray
        Permittivity distribution
    mu : ndarray
        Permeability distribution
    sigma : ndarray
        Conductivity distribution
    time : float
        Current simulation time
    
    Examples
    --------
    >>> grid = Grid(size=[100, 100, 100], spacing=[0.1, 0.1, 0.1])
    >>> solver = FDTDSolver(grid, cfl=0.99, pml_layers=8)
    >>> solver.add_source('gaussian', location=[50, 50, 10], 
    ...                   amplitude=1.0, width=1e-12)
    >>> solver.add_monitor('E', location=[50, 50, 90])
    >>> solver.run(num_steps=10000)
    >>> fields = solver.get_monitor_data()
    
    Notes
    -----
    - Uses CGS Gaussian units throughout
    - PML (Perfectly Matched Layer) for absorption
    - Subpixel smoothing available for curved boundaries
    - MPI parallelization for large problems
    
    CGS Units
    ---------
    - E: statvolt/cm
    - H: oersted
    - dt: seconds
    - dx, dy, dz: cm
    - c: 2.99792458×10¹⁰ cm/s
    
    References
    ----------
    - Yee, K.S. (1966). "Numerical solution of initial boundary value
      problems involving Maxwell's equations." IEEE Trans. Antennas Propag.
    - Taflove, A. & Hagness, S.C. Computational Electrodynamics: FDTD Method
    - Maxwell, Articles 604-611: General field equations
    
    See Also
    --------
    FEMSolver, SpectralSolver, wave-equation-solution task
    """
    
    def __init__(
        self,
        grid: Grid,
        dt: Optional[float] = None,
        cfl: float = 0.99,
        pml_layers: int = 8,
        pml_reflection: float = 1e-6
    ):
        self.grid = grid
        self.cfl = cfl
        self.pml_layers = pml_layers
        
        # Auto-calculate dt from CFL if not specified
        if dt is None:
            dx_min = min(grid.spacing)
            self.dt = cfl * dx_min / (3e10 * np.sqrt(3))  # c in cm/s
        else:
            self.dt = dt
            
        # Initialize fields on Yee lattice
        self.yee_cell = YeeCell(grid, pml_layers)
        self.Ex = np.zeros_like(self.yee_cell.x_ex)
        self.Ey = np.zeros_like(self.yee_cell.y_ey)
        self.Ez = np.zeros_like(self.yee_cell.z_ez)
        self.Hx = np.zeros_like(self.yee_cell.x_hx)
        self.Hy = np.zeros_like(self.yee_cell.y_hy)
        self.Hz = np.zeros_like(self.yee_cell.z_hz)
        
        # Material properties (default to vacuum)
        self.epsilon = np.ones_like(self.yee_cell.epsilon)
        self.mu = np.ones_like(self.yee_cell.mu)
        self.sigma = np.zeros_like(self.yee_cell.sigma)
        
        self.sources = []
        self.monitors = []
        self.time = 0.0
    
    def setup(self):
        """Initialize solver with PML and materials."""
        self.yee_cell.setup_pml(self.pml_layers, self.pml_reflection)
        self._validate_cfl()
    
    def _validate_cfl(self):
        """Check CFL stability condition."""
        dx_min = min(self.grid.spacing)
        dt_max = dx_min / (3e10 * np.sqrt(3))
        if self.dt > dt_max:
            raise CFLViolationError(
                f"dt={self.dt} exceeds CFL limit {dt_max}"
            )
    
    def step(self):
        """Advance fields by one time step using Yee algorithm."""
        # Update H (half step behind E)
        curl_E = self._compute_curl_E()
        self.Hx -= (self.dt / self.mu) * curl_E[0]
        self.Hy -= (self.dt / self.mu) * curl_E[1]
        self.Hz -= (self.dt / self.mu) * curl_E[2]
        
        # Update E
        curl_H = self._compute_curl_H()
        J = self._compute_current()  # Include sources
        
        self.Ex += (self.dt / self.epsilon) * (
            3e10 * curl_H[0] - 4 * np.pi * J[0]
        )
        self.Ey += (self.dt / self.epsilon) * (
            3e10 * curl_H[1] - 4 * np.pi * J[1]
        )
        self.Ez += (self.dt / self.epsilon) * (
            3e10 * curl_H[2] - 4 * np.pi * J[2]
        )
        
        # Apply PML absorption
        self._apply_pml()
        
        self.time += self.dt
    
    def run(self, num_steps: int, progress_interval: int = 1000):
        """Run simulation for specified number of steps."""
        for step in range(num_steps):
            self.step()
            
            # Update monitors
            for monitor in self.monitors:
                monitor.record(self.time, self.get_fields_at(monitor.location))
            
            if step % progress_interval == 0:
                self._report_progress(step, num_steps)
    
    def validate(self):
        """Run validation against analytical solutions."""
        # Plane wave propagation test
        self._validate_plane_wave()
        
        # Energy conservation test
        self._validate_energy_conservation()
        
        # Cavity resonance test
        self._validate_cavity_modes()
```

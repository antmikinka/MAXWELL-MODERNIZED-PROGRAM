# Task: maxwell-solver-setup

## Description

Configures and executes full Maxwell equation solvers for general time-dependent electromagnetic problems from Maxwell's Part IV (Arts. 604-619). This task workflow guides the user through setting up complex 3D EM simulations.

## Workflow Steps

### 1. Problem Specification
- Define simulation domain and extent
- Specify all materials and their properties
- Identify sources and excitations
- Set boundary conditions

### 2. Mesh Generation
- Create computational grid
- Refine near features of interest
- Add PML layers for absorption
- Check CFL condition

### 3. Solver Configuration
- Select numerical method (FDTD, FEM, etc.)
- Set time step and simulation duration
- Configure monitors and outputs
- Initialize fields

### 4. Execution and Monitoring
- Run simulation
- Monitor energy conservation
- Check for instabilities
- Save intermediate results

### 5. Post-Processing
- Extract field data
- Compute derived quantities
- Generate visualizations
- Validate results

## Requirements

**Input:**
- `domain`: dict - Simulation volume and boundaries
- `materials`: dict - Material distribution
- `sources`: list - Excitations
- `monitors`: list - Field and flux monitors
- `solver_config`: dict - Numerical parameters

**Output:**
- `fields`: dict - E(t), H(t) at monitors
- `derived`: dict - S-parameters, radiation patterns
- `diagnostics`: dict - Energy, CFL, convergence
- `metadata`: dict - Citations, version info

## Implementation

```python
from maxwell.tasks.full_wave import MaxwellSolverSetup
from maxwell.materials import Material
from maxwell.core import Grid, Source

# Example: Microstrip patch antenna simulation

# 1. Define domain
domain = {
    'dimensions': [10, 8, 5],  # cm (x, y, z)
    'background': 'air',
    'boundaries': {
        'x_min': 'PML', 'x_max': 'PML',
        'y_min': 'PML', 'y_max': 'PML',
        'z_min': 'PEC', 'z_max': 'open'
    }
}

# 2. Define materials
materials = {
    'substrate': {
        'material': Material(epsilon=4.4, mu=1, loss_tangent=0.02),
        'geometry': {'type': 'box', 'bounds': [[0,10], [0,8], [0,0.159]]}
    },
    'ground_plane': {
        'material': 'PEC',
        'geometry': {'type': 'plane', 'z': 0}
    },
    'patch': {
        'material': 'PEC',
        'geometry': {'type': 'box', 'bounds': [[2,8], [1,7], [0.159,0.16]]}
    },
    'feed': {
        'type': 'voltage_source',
        'location': [5, 4, 0.159],
        'impedance': 50  # ohms
    }
}

# 3. Define sources
sources = [
    Source(
        type='gaussian',
        location=[5, 4, 0.159],
        direction='z',
        parameters={'amplitude': 1.0, 'width': 1e-11}
    )
]

# 4. Define monitors
monitors = [
    {'type': 'E_field', 'location': [5, 4, 3], 'name': 'far_field_point'},
    {'type': 'H_field', 'location': [5, 4, 3], 'name': 'far_field_point_h'},
    {'type': 'flux', 'surface': 'z=4', 'name': 'radiated_power'},
    {'type': 'voltage', 'location': 'feed', 'name': 'feed_voltage'},
    {'type': 'current', 'location': 'feed', 'name': 'feed_current'}
]

# 5. Configure solver
solver_config = {
    'method': 'fdtd',
    'grid_spacing': [0.1, 0.1, 0.05],  # cm
    'time_step': 1e-13,  # seconds (auto-calculated from CFL)
    'num_steps': 50000,
    'pml_layers': 8,
    'subpixel_smoothing': True
}

# 6. Setup and run
solver = MaxwellSolverSetup(
    domain=domain,
    materials=materials,
    sources=sources,
    monitors=monitors,
    config=solver_config
)

# Validate setup
validation = solver.validate_setup()
# Checks: CFL condition, PML thickness, mesh quality

# Run simulation
results = solver.run(
    progress_interval=1000,
    checkpoint_interval=10000,
    resume_from=None  # or checkpoint file
)

# 7. Post-process
s11 = results.compute_s_parameter('feed')
gain_pattern = results.compute_radiation_pattern(
    frequency=2.4e9,
    phi_cuts=[0, 45, 90]
)

bandwidth = results.compute_bandwidth(s11_threshold=-10)  # -10 dB
efficiency = results.compute_radiation_efficiency()

# 8. Export results
results.export_fields('patch_antenna_fields.h5')
results.export_s_parameters('patch_antenna_sparams.csv')
results.generate_report('patch_antenna_report.pdf')
```

## Solver Methods

### FDTD (Finite-Difference Time-Domain)
- Yee lattice for E and H fields
- Explicit time stepping
- Wideband response from single run
- CFL stability limit

### FEM (Finite Element Method)
- Unstructured tetrahedral mesh
- Frequency domain solution
- Accurate for curved boundaries
- Requires separate run per frequency

### Spectral Methods
- Fourier basis functions
- Exponential convergence for smooth problems
- Periodic boundaries natural
- Global communication

## Validation Criteria

- [ ] CFL condition satisfied: dt ≤ dx/(c√D)
- [ ] PML reflection < -60 dB
- [ ] Energy conservation < 1% drift
- [ ] Field singularities handled properly
- [ ] Convergence with mesh refinement
- [ ] Comparison with analytical solutions where available

## Maxwell Article References

| Article | Content |
|---------|---------|
| 604-611 | General field equations |
| 606-607 | Ampère-Maxwell law |
| 610-611 | Displacement current |
| 781-785 | Wave propagation |

## Related Tasks

- `wave-equation-solution` - Frequency domain approach
- `antenna-design` - Specific application
- `emc-analysis` - Interference studies

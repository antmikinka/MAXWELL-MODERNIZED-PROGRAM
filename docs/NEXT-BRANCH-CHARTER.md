# Next Branch Charter

> Strategic roadmap for post-v0.1.0 development branches
> Created: 2026-05-06 | Status: Draft

## Branch 1: `feat/simulation-engine`

### Scope
Build the dynamic simulation engine on top of the static field calculations.

### Layers
- **Layer 90: EtherGrid** -- Spatial discretization framework for electromagnetic field simulation
  - Grid-based field solver with adaptive refinement
  - Boundary condition framework (Dirichlet, Neumann, periodic)
  - Material property mapping onto grid cells
  - Coupling to existing `maxwell.core` primitives (PointCharge, Magnet, etc.)

- **Layer 92: Time Integrator** -- Temporal evolution engine
  - Multiple integration schemes: Euler, RK4, Verlet, symplectic
  - Adaptive timestep control based on CFL condition
  - Energy conservation monitoring and correction
  - Event detection (particle collisions, boundary crossings)

### Dependencies
- Requires `maxwell.core` (charge, field, magnet primitives)
- Requires `maxwell.electromagnetism` (Lorentz force, Maxwell equations)
- Benefits from `maxwell.jax` (GPU-accelerated field evaluation)

### Deliverables
- `maxwell/simulation/grid.py` -- EtherGrid spatial discretization
- `maxwell/simulation/integrator.py` -- Time integration schemes
- `maxwell/simulation/boundary.py` -- Boundary condition handlers
- `maxwell/simulation/materials.py` -- Material property grid mapping
- 100+ tests covering all integration schemes and boundary conditions
- Example simulations: particle in uniform B-field, cyclotron motion, capacitor discharge

### Estimated Effort
- 3-4 weeks of focused development
- ~15 new modules, ~100 tests

---

## Branch 2: `feat/vis-round-3`

### Scope
Complete the remaining 7 visualizations from the visualization audit.

### Pending Visualizations
1. **Plasma Discharge** (Art. 500+) -- Glow discharge visualization with ionization zones
2. **Electromagnetic Radiation** (Art. 790+) -- Far-field radiation patterns from accelerating charges
3. **Waveguide Modes** (Art. 795+) -- TE/TM mode patterns in rectangular and circular waveguides
4. **Optical Interference** (Art. 798+) -- Double-slit and thin-film interference patterns
5. **Faraday Rotation** (Art. 805+) -- Polarization rotation in magneto-optic materials
6. **Galvanometer Response** (Art. 730+) -- Time-domain step response of moving-coil galvanometer
7. **Helmholtz Coil Field** (Art. 650+) -- Uniform field region visualization with field line density

### Standards
- Follow existing `maxwell.vis` patterns (`require_matplotlib`, `@maxwell_cite`, `_base` utilities)
- Each module: 1-2 `calc_*` functions + 2-3 `plot_*` functions
- ~10 tests per module following existing test patterns
- 2D and 3D visualizations as appropriate

### Dependencies
- Requires existing `maxwell.vis` infrastructure
- Some modules require physics from `maxwell.electromagnetism` and `maxwell.optics`

### Deliverables
- 7 new visualization modules in `maxwell/vis/`
- ~70 new tests
- Updated `maxwell/vis/__init__.py` exports
- Total visualization modules: 13 -> 20

### Estimated Effort
- 2-3 weeks of focused development
- ~7 modules, ~70 tests

---

## Branch 3: `feat/scaffold-fill`

### Scope
Fill the 26 empty subpackage scaffolds with actual implementations.

### Empty Subpackages
Based on the architecture analysis, the following subpackages exist but contain only `__init__.py` with no substantive code:

| Subpackage | Expected Content | Priority |
|------------|-----------------|----------|
| `maxwell/electrostatics/capacitors/` | Capacitance calculations for various geometries | High |
| `maxwell/electrostatics/dielectrics/` | Dielectric constant models, polarization | High |
| `maxwell/electrostatics/green/` | Green's function implementations | Medium |
| `maxwell/electrokinematics/network/` | Circuit network analysis | High |
| `maxwell/electrokinematics/instruments/` | Galvanometer, Wheatstone bridge models | Medium |
| `maxwell/magnetism/terrestrial/` | Earth magnetic field models | Medium |
| `maxwell/magnetism/compass/` | Compass deviation calculations | Low |
| `maxwell/electromagnetism/radiation/` | EM radiation theory | High |
| `maxwell/electromagnetism/waveguides/` | Waveguide mode analysis | Medium |
| `maxwell/electromagnetism/optics/` | Light as EM wave | High |
| `maxwell/fields/boundary/` | Boundary value problem solvers | Medium |
| `maxwell/fields/greens/` | Green's function methods | Medium |
| `maxwell/materials/dielectric/` | Dielectric material models | High |
| `maxwell/materials/magnetic/` | Magnetic material models | High |
| `maxwell/materials/conductors/` | Conductor properties | Medium |
| `maxwell/math/elliptic/` | Elliptic integral computations | Low |
| `maxwell/math/tensor/` | Tensor calculus operations | Medium |
| `maxwell/math/fourier/` | Fourier analysis tools | Medium |
| `maxwell/instruments/galvanometer/` | Galvanometer models | Low |
| `maxwell/instruments/electrometer/` | Electrometer models | Low |
| `maxwell/signal/transform/` | Signal transform methods | Low |
| `maxwell/signal/filter/` | Filtering operations | Low |
| `maxwell/optics/polarization/` | Polarization calculations | Medium |
| `maxwell/optics/reflection/` | Reflection/refraction | Medium |
| `maxwell/optics/dispersion/` | Dispersion relations | Low |
| `maxwell/molecular/crystal/` | Crystal magnetization models | Low |

### Approach
- Prioritize by user value and dependency order
- Each subpackage: implement core calculations from Maxwell's articles
- Follow established patterns: `@maxwell_cite`, type hints, docstrings, tests
- Minimum 5 tests per new module

### Deliverables
- 26 filled subpackages with implementations
- ~130+ new tests
- Updated coverage to include all subpackages

### Estimated Effort
- 6-8 weeks of focused development
- ~50+ new modules, ~130+ tests

---

## Branch Dependencies

```
feat/scaffold-fill ──────────────────┐
                                      ├──> feat/simulation-engine (needs physics modules)
feat/vis-round-3 ──────────────────┤
                                      └──> Independent (can run in parallel)
```

## Timeline

| Phase | Branch | Duration | Target |
|-------|--------|----------|--------|
| v0.1.0 Release | `feat/pypi-package` | Current | May 2026 |
| Scaffold Fill (Phase 1) | `feat/scaffold-fill` | 3 weeks | June 2026 |
| Vis Round 3 | `feat/vis-round-3` | 2-3 weeks | June 2026 |
| Simulation Engine | `feat/simulation-engine` | 4 weeks | July 2026 |
| Scaffold Fill (Phase 2) | `feat/scaffold-fill` | 3 weeks | July 2026 |
| v0.2.0 Release | `main` | -- | August 2026 |

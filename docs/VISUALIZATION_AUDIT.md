# Maxwell Modernized -- Visualization Audit & Cross-Repo Analysis Plan

> **Comprehensive audit of all 17 planned visualizations vs. 15 implemented (100% classical scope complete), plus plan for cross-analyzing the codebase against the 16 architecture map documents in a separate GitHub repository.**

**Generated:** 2026-05-06
**Source Document:** `Maxwell's Treatise_ The Visualization Strategy.md`
**Architecture Maps:** 16 documents in `archive/docs/`

---

## Part 1: Visualization Audit -- 17 Planned vs. 15 Implemented (100% Classical)

### Implementation Status Overview

| # | Visualization | Part | Article | Planned Implementation | Actual Status | Notes |
|---|--------------|------|---------|----------------------|---------------|-------|
| 1 | **Equipotential Surfaces** | I | Art. 46 | `maxwell.vis.scalar.render_isosurfaces()` | **[DONE]** `plot_equipotentials_2d()` | 2D contours only, 3D isosurfaces pending |
| 2 | **Lines of Force** | I | Art. 47 | `maxwell.vis.vector.trace_streamlines()` | **[DONE]** `plot_field_lines_2d()` | 2D streamlines, 3D tracing pending |
| 3 | **Method of Images** | I | Art. 155 | `maxwell.vis.method_of_images.plot_method_of_images()` | **[DONE]** `calc_method_of_images()`, `plot_method_of_images()` | Full 2D implementation with equipotential + field lines |
| 4 | **Edge Singularities** | I | Art. 191 | `maxwell.vis.edge_singularities.plot_edge_singularity()` | **[DONE]** `calc_wedge_field()`, `calc_edge_singularity()`, `plot_edge_singularity()`, `plot_singularity_comparison()` | Full 2D heatmap + comparison plot |
| 5 | **Unit Tubes of Flow** | II | Art. 290 | `maxwell.vis.flow_tubes.render_flow_tubes()` | **[DONE]** `plot_flow_tubes_2d()` | 2D flow tube visualization with current density field |
| 6 | **Thermal Gradients** | II | Art. 242/249 | `maxwell.vis.scalar.render_joule_heating()` | **[DONE]** `calc_joule_heat_distribution()`, `calc_thermal_gradients()`, `calc_peltier_junction()`, `plot_thermal_gradients()`, `plot_joule_heat_distribution()`, `plot_thermoelectric_effects()` | Current+temperature overlay, thermoelectric effects |
| 7 | **Dielectric Soakage** | II | Art. 329 | `maxwell.vis.plots.plot_transient_recovery()` | **[DONE]** `calc_dielectric_absorption()`, `plot_dielectric_soakage()` | Time-domain multi-exponential decay current plot |
| 8 | **Magnetic Shell** | III | Art. 409 | `maxwell.vis.geometry.render_solid_angle_cap()` | **[DONE]** `calc_solid_angle()`, `calc_shell_potential()`, `plot_magnetic_shell()`, `plot_shell_potential()` | 3D/2D magnetic shell with current loop equivalence and solid angle calculation |
| 9 | **Spherical Harmonic Globes** | III | Art. 467 | `maxwell.vis.geophysics.render_gauss_harmonics()` | **[DONE]** `calc_gauss_harmonics()`, `calc_field_intensity()`, `plot_harmonic_globe()`, `plot_harmonic_modes()`, `plot_harmonic_contour()` | 3D globe and 2D map visualization of Gauss coefficient decomposition |
| 10 | **Hysteresis Loops** | III | Art. 442 | `maxwell.vis.plots.animate_hysteresis_cycle()` | **[DONE]** `calc_hysteresis_loop()`, `plot_hysteresis_loops()`, `plot_material_comparison()` | B-H loop with coercivity/retentivity labels, area shading, material comparison |
| 11 | **Electrotonic State (Vector Potential A)** | IV | Art. 540/617 | `maxwell.vis.vector.render_vector_potential_A()` | **[DONE]** `calc_electrotonic_straight_wire()`, `calc_electrotonic_transient()`, `calc_B_from_electrotonic()`, `plot_electrotonic_state_2d()`, `plot_A_and_B_fields()`, `plot_A_transient()`, `plot_electrotonic_3d_surface()` | A-field lines, magnitude contours, curl relationship, transient evolution |
| 12 | **Maxwell Stress Tensor** | IV | Art. 641 | `maxwell.vis.tensor.render_stress_ellipsoids()` | **[DONE]** `plot_stress_tensor_2d()` | 2D stress plot, 3D ellipsoids pending |
| 13 | **Helicoidal Potentials** | IV | Art. 487 | `maxwell.vis.topology.render_cyclic_surface()` | **[DONE]** `calc_solid_angle_loop()`, `plot_helicoidal_potentials()`, `plot_loop_potential_3d()`, `plot_loop_field_lines()` | Helicoidal magnetic equipotential surfaces for current loops |
| 14 | **Molecular Vortices** | IV | Art. 822 | `maxwell.vis.mechanical.animate_vortex_lattice()` | **[DONE]** `calc_vortex_lattice()`, `calc_magnetic_field_from_vortices()`, `plot_molecular_vortices()`, `plot_vortex_3d_surface()` | Vortex lattice with streamlines/quiver and 3D surface |
| 15 | **EM Wave Propagation** | IV | Art. 791 | `maxwell.vis.optics.render_plane_wave()` | **[DONE]** `calc_em_wave()`, `plot_em_wave_propagation()`, `plot_wave_snapshot_3d()` | Orthogonal E/B fields vs position, 3D vector field, linear/circular/elliptical polarization |
| 16 | **Aharonov-Bohm Phase** | VI | Extension | `maxwell.vis.scalar.render_potential_fog()` | **NOT DONE** | Part VI not implemented |
| 17 | **Longitudinal Waves** | VI | Extension | `maxwell.vis.scalar.animate_longitudinal_pulse()` | **NOT DONE** | Part VI not implemented |

### Summary

| Status | Count | Percentage |
|--------|-------|------------|
| Implemented (Classical) | 15 | 100% of classical scope |
| Partially implemented | 0 | 0% |
| Deferred (Part VI Extension) | 2 | Outside classical scope |

### Current vis/ Package (17 files: 15 modules + 2 support)

| Module | Content |
|--------|---------|
| `__init__.py` | Package exports with graceful degradation (56 exports) |
| `_base.py` | Mesh grid and evaluation utilities |
| `_compat.py` | Matplotlib import with graceful fallback |
| `field_lines.py` | 2D electric/magnetic field line plotting |
| `equipotential.py` | 2D equipotential contour plotting |
| `stress.py` | 2D Maxwell stress tensor visualization |
| `method_of_images.py` | Method of Images visualization (Art. 155) |
| `edge_singularities.py` | Edge singularity heatmap + comparison (Art. 191) |
| `dielectric_soakage.py` | Dielectric absorption time-domain decay (Art. 329) |
| `hysteresis_loops.py` | Magnetic B-H hysteresis loops + material comparison (Arts. 442-446) |
| `em_wave_propagation.py` | EM wave propagation & polarization (Art. 791) |
| `magnetic_shell.py` | Magnetic shell / solid angle visualization (Art. 409) |
| `spherical_harmonics.py` | Spherical harmonic globe visualization (Art. 467) |
| `flow_tubes.py` | Unit Tubes of Flow visualization (Art. 290) |
| `thermal_gradients.py` | Joule heating & thermoelectric effects (Arts. 242, 249) |
| `molecular_vortices.py` | Molecular vortex lattice (Arts. 822-824) |
| `helicoidal_potentials.py` | Helicoidal potential surfaces (Arts. 486-487) |
| `electrotonic_state.py` | Electrotonic state / vector potential (Arts. 540, 617) |

### What Each Implemented Visualization Does

**1. `plot_field_lines_2d()`** (field_lines.py)
- Plots 2D electric or magnetic field lines as streamlines
- Supports multiple charge configurations
- Uses matplotlib quiver + streamplot
- Handles arbitrary charge arrays

**2. `plot_equipotentials_2d()`** (equipotential.py)
- Plots 2D equipotential contour lines
- Supports single and multi-charge systems
- Uses matplotlib contour with configurable levels
- Overlays field lines on equipotentials

**3. `plot_stress_tensor_2d()`** (stress.py)
- Plots 2D Maxwell stress tensor as quiver field
- Shows tension along field lines, pressure perpendicular
- Supports uniform and computed stress fields
- Single tensor or full stress computation

**4. `plot_method_of_images()`** (method_of_images.py)
- Visualizes Method of Images for a charge above conducting plane (Art. 155)
- Shows equipotential contours, field lines, and charge positions
- Real charge (+q) and image charge (-q) marked on plot
- Conducting plane shown as dashed line at x=0
- Includes `calc_method_of_images()` for underlying computation

**5. `plot_edge_singularity()`** (edge_singularities.py)
- Visualizes field enhancement near conducting wedge edges (Art. 191)
- Power-law singularity: E ~ r^(pi/alpha - 1)
- Supports logarithmic color scale for wide dynamic range
- Includes `calc_wedge_field()`, `calc_edge_singularity()`, `plot_singularity_comparison()`
- Comparison plot shows singularity strength for different wedge angles

**6. `plot_dielectric_soakage()`** (dielectric_soakage.py)
- Visualizes dielectric absorption current decay over time (Art. 329)
- Multi-exponential decay model with configurable time constants
- Time-domain current plot showing soakage and recovery phases
- Includes `calc_dielectric_absorption()` for underlying computation

**7. `plot_hysteresis_loops()`** (hysteresis_loops.py)
- Plots magnetic B-H hysteresis loops (Arts. 442-446)
- Shows coercivity, retentivity, and loop area shading
- Includes `calc_hysteresis_loop()`, `plot_material_comparison()`
- Material comparison: soft iron vs steel vs permanent magnet

**8. `plot_em_wave_propagation()`** (em_wave_propagation.py)
- Visualizes EM wave propagation with orthogonal E/B fields (Art. 791)
- Supports linear, circular, and elliptical polarization
- Includes `calc_em_wave()`, `plot_wave_snapshot_3d()`
- 3D vector field visualization

**9. `plot_magnetic_shell()`** (magnetic_shell.py)
- Visualizes Maxwell's magnetic shell theory with current loop equivalence (Art. 409)
- Computes solid angle subtended by a current loop: Omega = 2*pi*(1 - cos(theta))
- Calculates shell potential: V = (I / 4*pi) * Omega
- 3D surface plot of solid angle, 2D contour plot of shell potential
- Includes `calc_solid_angle()`, `calc_shell_potential()`, `plot_shell_potential()`

**10. `plot_harmonic_globe()`** (spherical_harmonics.py)
- Visualizes Gauss coefficient spherical harmonic decomposition of terrestrial magnetism (Art. 467)
- 3D globe with color-mapped scalar field from spherical harmonic expansion
- 2D contour map and mode decomposition plots
- Includes `calc_gauss_harmonics()`, `calc_field_intensity()`, `plot_harmonic_modes()`, `plot_harmonic_contour()`

**11. `plot_unit_tubes_of_flow()`** (flow_tubes.py)
- Visualizes Maxwell's unit tubes of flow for current density fields (Art. 290)
- Renders 2D flow tubes showing current direction and magnitude
- Supports arbitrary current source configurations
- Uses matplotlib streamplot with tube-width proportional to current density
- Includes `calc_unit_tubes()`, `plot_unit_tubes_3d()`

**12. `plot_thermal_gradients()`** (thermal_gradients.py)
- Visualizes Joule heating and thermal gradients (Arts. 242, 249)
- 2D temperature field with heat flux arrows
- Supports rectangular and circular geometries
- Includes `calc_joule_heat_distribution()`, `calc_thermal_gradients()`, `calc_peltier_junction()`
- Thermoelectric effects: Seebeck coefficient comparison, Peltier junction EMF
- Additional plots: `plot_joule_heat_distribution()`, `plot_thermoelectric_effects()`

**13. `plot_molecular_vortices()`** (molecular_vortices.py)
- Visualizes Maxwell's mechanical vortex lattice model (Arts. 822-824)
- Alternating checkerboard vortex pattern with velocity field
- Shows streamlines or quiver arrows for vortex flow
- Includes `calc_vortex_lattice()`, `calc_magnetic_field_from_vortices()`
- Collective magnetic field computation from vortex lattice
- 3D vorticity surface: `plot_vortex_3d_surface()`

**14. `plot_helicoidal_potentials()`** (helicoidal_potentials.py)
- Visualizes helicoidal magnetic equipotential surfaces (Arts. 486-487)
- Solid angle formulation for circular current loop
- Multi-valued potential surface with screw-like topology
- Includes `calc_solid_angle_loop()`, `plot_loop_potential_3d()`, `plot_loop_field_lines()`
- 3D potential surface and field line visualization

**15. `plot_electrotonic_state_2d()`** (electrotonic_state.py)
- Visualizes Maxwell's Electrotonic State -- the vector potential A-field (Arts. 540, 617)
- A-field magnitude contours around current-carrying conductors
- Side-by-side A and B field comparison showing curl relationship
- Time evolution during current transients ("extra current" effect)
- Includes `calc_electrotonic_straight_wire()`, `calc_electrotonic_transient()`, `calc_B_from_electrotonic()`
- Additional plots: `plot_A_and_B_fields()`, `plot_A_transient()`, `plot_electrotonic_3d_surface()`

### Tech Stack per Visualization Strategy

| Technology | Purpose | Status |
|-----------|---------|--------|
| **Matplotlib** | 2D plots, contours, quiver fields | Installed (optional via `[viz]`) |
| **PyVista** | 3D meshes, isosurfaces, vector fields | NOT integrated |
| **Manim** | Educational animations | NOT integrated |

---

## Part 2: Visualization Implementation Priority -- COMPLETE

All classical visualization priorities have been fulfilled.

### Phase 1: Complete Part I Visualizations -- DONE

| # | Visualization | Complexity | Dependencies | Article | Status |
|---|--------------|------------|-------------|---------|--------|
| 3 | Method of Images | Medium | Image charge solver (exists) | Art. 155 | **DONE** |
| 4 | Edge Singularities | Low-Medium | 2D heatmap, existing grid tools | Art. 191 | **DONE** |

### Phase 2: Part II & III Visualizations -- DONE

| # | Visualization | Complexity | Dependencies | Article | Status |
|---|--------------|------------|-------------|---------|--------|
| 5 | Unit Tubes of Flow | Medium | 2D flow tubes, current density field | Art. 290 | **DONE** |
| 6 | Thermal Gradients | Medium | Joule heating solver (exists) | Art. 242/249 | **DONE** |
| 7 | Dielectric Soakage | Low | Time-series plotting | Art. 329 | **DONE** |
| 8 | Magnetic Shell | Medium | Solid angle computation | Art. 409 | **DONE** |
| 9 | Spherical Harmonic Globes | High | PyVista or matplotlib 3D sphere | Art. 467 | **DONE** |
| 10 | Hysteresis Loops | Low | B-H data from hysteresis.py | Art. 442 | **DONE** |

### Phase 3: Part IV Visualizations (Crown Jewels) -- DONE

| # | Visualization | Complexity | Dependencies | Article | Status |
|---|--------------|------------|-------------|---------|--------|
| 11 | Electrotonic State | High | Vector potential (JAX: VectorPotentialJAX) | Art. 540/617 | **DONE** |
| 12 | Stress Tensor 3D | Medium | Complete 3D ellipsoid rendering | Art. 641 | **DONE** (2D) |
| 13 | Helicoidal Potentials | High | Multi-valued potential topology | Art. 487 | **DONE** |
| 14 | Molecular Vortices | Very High | Manim animation engine | Art. 822 | **DONE** |
| 15 | EM Wave Propagation | High | Manim or matplotlib animation | Art. 791 | **DONE** |

### Phase 4: Part VI Visualizations (Research Frontier) -- DEFERRED

| # | Visualization | Complexity | Dependencies | Article | Status |
|---|--------------|------------|-------------|---------|--------|
| 16 | Aharonov-Bohm Phase | Very High | Scalar physics not implemented | Extension | **DEFERRED** |
| 17 | Longitudinal Waves | Very High | Superpotential theory | Extension | **DEFERRED** |

---

## Part 3: Cross-Repo Analysis Plan

### The Problem

The **16 architecture map documents** in `archive/docs/` contain the authoritative planned architecture:
- `Maxwell's Treatise_ Modernized Architecture Map - PART I.md` through `PART VI.md`
- `Maxwell_Treatise_Part_I_Architecture_COMPLETE.md` through `Part_VI_Architecture_COMPLETE.md`
- `Maxwell's Treatise_ The Visualization Strategy.md`
- `Maxwell's Treatise_ The Master Synthesis - A Modern Computational Architecture for Classical Physics.md`

The **codebase** (`maxwell/`) contains what was actually implemented.

There is a growing gap between **what was planned** (16 architecture documents, detailed layer-by-layer specifications) and **what was built** (252 Python modules, 1787 tests, 30+ JAX classes).

### The Cross-Repo Strategy

Create a **separate GitHub repository** (e.g., `maxwell-treatise/architecture`) that contains:

1. **The 16 architecture map documents** as the authoritative planned specification
2. **A `validation/` directory** with scripts that cross-analyze planned vs. implemented:
   - Layer-by-layer coverage checker
   - Module-to-layer mapping validator
   - Visualization gap tracker
   - Article-to-code traceability matrix

### Repository Structure

```
maxwell-treatise/architecture/
├── README.md                    # Architecture overview
├── maps/
│   ├── PART_I.md                # Architecture Map - Part I
│   ├── PART_II.md               # Architecture Map - Part II
│   ├── PART_III.md              # Architecture Map - Part III
│   ├── PART_IV.md               # Architecture Map - Part IV
│   ├── PART_V.md                # Architecture Map - Part V
│   ├── PART_VI.md               # Architecture Map - Part VI
│   ├── PART_I_COMPLETE.md       # Part I Architecture Complete
│   ├── PART_II_COMPLETE.md      # Part II Architecture Complete
│   ├── PART_III_COMPLETE.md     # Part III Architecture Complete
│   ├── PART_IV_COMPLETE.md      # Part IV Architecture Complete
│   ├── PART_V_COMPLETE.md       # Part V Architecture Complete
│   ├── PART_VI_COMPLETE.md      # Part VI Architecture Complete
│   └── visualization_strategy.md # Visualization Strategy
├── validation/
│   ├── cross_check.py           # Planned vs. implemented analyzer
│   ├── layer_coverage.py        # Layer-by-layer coverage tracker
│   ├── visualization_audit.py   # 17 planned vs. 15 implemented checker
│   ├── article_traceability.py  # Article-to-code mapping validator
│   └── report.py                # Cross-repo report generator
├── reports/
│   ├── coverage_report.json     # Machine-readable coverage
│   ├── visualization_report.md  # Visualization gap report
│   └── master_audit.md          # Full cross-analysis report
└── sync/
    └── sync_from_codebase.sh    # Script to pull latest from codebase repo
```

### Cross-Analysis Script Logic

The `validation/cross_check.py` script would:

1. **Parse architecture maps**: Extract planned layers, modules, classes, functions, and article mappings from the 16 markdown documents
2. **Scan codebase**: Use git submodule or API to list actual files in the `maxwell/` codebase
3. **Cross-reference**: For each planned layer in the architecture maps, check if the corresponding Python files exist in the codebase
4. **Generate report**: Output a JSON/markdown report showing:
   - Layers fully implemented
   - Layers partially implemented (which modules exist, which are missing)
   - Layers not implemented at all
   - Files in codebase that don't map to any planned layer
   - Visualization gap analysis (17 planned vs. 15 implemented)

### CI Integration

Add a GitHub Actions workflow to the architecture repo that:
- Runs weekly or on PR
- Fetches the latest codebase state
- Runs cross-analysis
- Commits updated coverage reports
- Optionally opens issues for missing implementations

---

## Part 4: Immediate Action Items

### This Session

- [x] Complete visualization audit (this document)
- [x] Magnetic Shell visualization (`maxwell/vis/magnetic_shell.py`) -- Art. 409
- [x] Spherical Harmonic Globes visualization (`maxwell/vis/spherical_harmonics.py`) -- Art. 467
- [x] Unit Tubes of Flow visualization (`maxwell/vis/flow_tubes.py`) -- Art. 290
- [x] Thermal Gradients visualization (`maxwell/vis/thermal_gradients.py`) -- Arts. 242, 249
- [x] Molecular Vortices visualization (`maxwell/vis/molecular_vortices.py`) -- Arts. 822-824
- [x] Helicoidal Potentials visualization (`maxwell/vis/helicoidal_potentials.py`) -- Arts. 486-487
- [x] Electrotonic State visualization (`maxwell/vis/electrotonic_state.py`) -- Arts. 540, 617
- [x] Jupyter notebooks: quick start, EM deep dive, visualization showcase
- [x] Cycle 11: All classical visualization gaps CLOSED
- [x] Cycle 12: Citation decorators, new exports, type annotations, examples, rendering tests
- [ ] Commit this document to codebase repo

### Next Session

- [ ] Add PyVista as optional dependency (`[viz3d]`)
- [ ] Create 3D stress tensor ellipsoid visualization
- [ ] Create 3D isosurface rendering for equipotentials
- [ ] Create 3D field line tracing

### Future Sessions

- [ ] Set up `maxwell-treatise/architecture` GitHub repo
- [ ] Copy all 16 architecture documents to architecture repo
- [ ] Build cross-analysis script (`validation/cross_check.py`)
- [ ] Implement CI workflow for automated cross-analysis
- [ ] Integrate Manim for educational animations (Molecular Vortices, EM Waves)
- [ ] Implement JAX-accelerated visualizations (GPU-rendered field lines)

---

## Part 5: Visualization Metrics

### Code Metrics

| Metric | Value |
|--------|-------|
| Visualization modules | 15 (13 code + 2 support) |
| Visualization exports | 56 functions |
| Visualization test files | 11 |
| Visualization test functions | 232 (224 module tests + 8 rendering validation) |
| Example scripts | 5 (in `examples/` directory) |
| Matplotlib dependency | Optional (`[viz]`) |
| PyVista integration | None |
| Manim integration | None |

### Coverage by Part

| Part | Visualizations Planned | Implemented | Gap |
|------|----------------------|-------------|-----|
| I: Electrostatics | 4 | 4 (equipotential, field lines, method of images, edge singularities) | 0 |
| II: Electrokinematics | 3 | 3 (dielectric soakage, flow tubes, thermal gradients) | 0 |
| III: Magnetism | 3 | 3 (hysteresis loops, magnetic shell, spherical harmonics) | 0 |
| IV: Electromagnetism | 5 | 5 (stress tensor 2D, EM wave propagation, helicoidal potentials, molecular vortices, electrotonic state) | 0 |
| VI: Scalar Physics | 2 | 0 (DEFERRED -- outside classical scope) | 2 (deferred) |
| **Total (Classical)** | **15** | **15** | **0 -- COMPLETE** |

### Test Coverage

| Visualization Test | Status |
|-------------------|--------|
| `test_vis_import_from_package` | PASS |
| `test_vis_all_exports` | PASS |
| `test_field_lines_basic` | PASS |
| `test_equipotentials_basic` | PASS |
| `test_stress_tensor_basic` | PASS |
| `test_method_of_images_*` | PASS (6 tests) |
| `test_edge_singularity_*` | PASS (8 tests) |
| `test_vis_dielectric_soakage_*` | PASS (15 tests) |
| `test_vis_hysteresis_loops_*` | PASS (14 tests) |
| `test_vis_em_wave_propagation_*` | PASS (15 tests) |
| `test_vis_magnetic_shell_*` | PASS (22 tests) |
| `test_vis_spherical_harmonics_*` | PASS (22 tests) |
| `test_vis_flow_tubes_*` | PASS (21 tests) |
| `test_vis_thermal_gradients_*` | PASS (28 tests) |
| `test_vis_molecular_vortices_*` | PASS (22 tests) |
| `test_vis_helicoidal_potentials_*` | PASS (21 tests) |
| `test_vis_electrotonic_state_*` | PASS (28 tests) |

### Jupyter Notebooks

Three Jupyter notebooks provide guided tours of the package capabilities:

| Notebook | Cells | Content |
|----------|-------|---------|
| `notebooks/01-quick-start-tour.ipynb` | 15 | Quick start: PointCharge, Lorentz force, speed of light |
| `notebooks/02-em-deep-dive.ipynb` | 18 | EM deep dive: Poynting vector, stress tensor, Faraday induction |
| `notebooks/03-visualization-showcase.ipynb` | 18 | Visualization gallery: all 15 visualization types |

---

### Cycle 12 Quality Improvements

**Citation Decorators:**
- `field_lines.py` -- Arts. 52-61 (2 functions)
- `equipotential.py` -- Arts. 16-19 (2 functions)
- `stress.py` -- Arts. 616-620 (2 functions)

**New Exports (previously internal):**
- `plot_dipole_field_lines` (field_lines.py)
- `plot_dipole_equipotentials` (equipotential.py)
- `verify_stress_tensor_plot` (stress.py)

**Type Annotation Modernization:**
- `Optional[X]` -> `X | None` across all vis modules
- `Tuple[X, ...]` -> `tuple[X, ...]` across all vis modules
- Files updated: `field_lines.py`, `equipotential.py`, `stress.py`, `_base.py`, `_compat.py`

**Examples Directory (`examples/`):**
- 5 example scripts demonstrating visualization workflows
- `examples/output/` added to `.gitignore` for generated figures
- Scripts serve as executable documentation for users

**Rendering Validation:**
- 8 rendering validation tests added to `test_vis.py`
- Tests verify figure generation, output quality, and plot structure
- Pillow dependency moved from `dev` to `viz` extra in `pyproject.toml`

---

*This document serves as the authoritative audit of visualization work completed vs. planned, and the strategic plan for cross-repo analysis between the codebase and architecture map documents. As of Cycle 12, all 15 classical visualizations are complete, with 56 exports, 232 vis tests, and 5 example scripts.

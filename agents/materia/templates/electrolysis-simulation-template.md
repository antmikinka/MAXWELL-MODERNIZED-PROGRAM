# Template: electrolysis-simulation-template

## Purpose

Standardized template for electrolysis simulation setup and documentation following Maxwell's electrokinematics framework.

## LLM Instructions

You are an electrochemistry simulation specialist. Generate comprehensive electrolysis simulation documentation that connects Maxwell's electrokinematic theory (Part II) with modern computational methods.

1. **Establish Theoretical Foundation**: Link to Maxwell's Articles 236-238 (electrolysis), 269-286 (electrochemical effects)
2. **Define Cell Geometry**: Specify electrode configuration, electrolyte volume
3. **Specify Governing Equations**: Nernst-Planck, charge conservation, boundary conditions
4. **Document Parameters**: Concentrations, potentials, transport properties
5. **Define Output Quantities**: Current density, concentration profiles, overpotentials

## Template Structure

```yaml
simulation:
  name: "{{simulation_name}}"
  maxwell_articles: ["Art. 236-238", "Art. 269-286"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
electrolytic_cell:
  geometry:
    type: "{{planar | cylindrical | spherical | custom}}"
    electrode_separation: {{d}} cm
    electrode_area: {{A}} cm²
    electrolyte_volume: {{V}} cm³
    
  electrodes:
    anode:
      material: "{{anode_material}}"
      half_reaction: "{{anode_reaction}}"
      standard_potential: {{E0_anode}} statvolt
      
    cathode:
      material: "{{cathode_material}}"
      half_reaction: "{{cathode_reaction}}"
      standard_potential: {{E0_cathode}} statvolt
      
  electrolyte:
    solvent: "{{solvent}}"
    dielectric_constant: {{K}}
    viscosity: {{eta}} poise
    temperature: {{T}} K
    
    ions:
      - name: "{{ion_name}}"
        charge: {{z}} (elementary charges)
        mobility: {{u}} cm²/statvolt·s
        diffusion_coeffient: {{D}} cm²/s
        bulk_concentration: {{c0}} mol/cm³
        
governing_equations:
  ion_transport:
    equation: "Nernst-Planck"
    form: "J_i = -D_i·grad(c_i) - z_i·u_i·c_i·grad(phi) + c_i·v"
    maxwell_reference: "Art. 236-238"
    
  charge_conservation:
    equation: "Continuity"
    form: "div(J) = -d(rho)/dt"
    maxwell_reference: "Art. 230-235"
    
  electric_field:
    equation: "Poisson"
    form: "div(E) = 4*pi·rho (CGS)"
    maxwell_reference: "Art. 77-78"
    
boundary_conditions:
  anode_surface:
    type: "{{potentiostatic | galvanostatic | mixed}}"
    value: {{applied_value}}
    overpotential: {{eta_anode}}
    
  cathode_surface:
    type: "{{potentiostatic | galvanostatic | mixed}}"
    value: {{applied_value}}
    overpotential: {{eta_cathode}}
    
  walls:
    type: "no-flux"
    condition: "J_i · n = 0"
    
initial_conditions:
  concentration: {{c_initial}} mol/cm³
  potential: {{phi_initial}} statvolt
  current: {{I_initial}} statampere
  
numerical_setup:
  discretization:
    method: "{{FEM | FDM | FVM | BEM}}"
    mesh_elements: {{num_elements}}
    timestep: {{dt}} s
    
  solver:
    type: "{{coupled | segregated}}"
    linear_solver: "{{solver_name}}"
    tolerance: {{tol}}
    max_iterations: {{max_iter}}
    
output_quantities:
  - quantity: "current_density"
    units: "statampere/cm²"
    location: "{{electrode_surface | bulk | specific_point}}"
    
  - quantity: "concentration_profile"
    units: "mol/cm³"
    location: "interior"
    
  - quantity: "potential_distribution"
    units: "statvolt"
    location: "interior"
    
  - quantity: "overpotential"
    units: "statvolt"
    location: "{{anode | cathode}}"
    
  - quantity: "faradaic_efficiency"
    units: "dimensionless (0-1)"
    calculation: "{{method}}"
```

## Variables

| Variable | Description | Type | Required |
|----------|-------------|------|----------|
| simulation_name | Simulation identifier | string | Yes |
| theory_classification | Classification per Maxwell framework | enum | Yes |
| d | Electrode separation | number | Yes |
| A | Electrode area | number | Yes |
| z | Ion charge number | integer | Yes |
| u | Ion mobility | number | Yes |
| D | Diffusion coefficient | number | Yes |

## CGS Unit Reference

| Quantity | CGS Unit | Conversion |
|----------|----------|------------|
| Potential | statvolt | 1 statvolt = 299.79 V |
| Current | statampere | 1 statampere = 3.336×10⁻¹⁰ A |
| Current density | statampere/cm² | - |
| Concentration | mol/cm³ | 1 mol/cm³ = 10⁶ mol/m³ |
| Electric field | statvolt/cm | 1 statvolt/cm = 29979 V/m |

## Usage Example

```yaml
simulation:
  name: "Copper Sulfate Electrolysis"
  maxwell_articles: ["Art. 236", "Art. 237", "Art. 280-286"]
  theory_classification: "standard_math"
  
electrolytic_cell:
  geometry:
    type: "planar"
    electrode_separation: 5.0 cm
    electrode_area: 100.0 cm²
    
  electrodes:
    anode:
      material: "Copper"
      half_reaction: "Cu → Cu²⁺ + 2e⁻"
      standard_potential: -0.337 V
      
  electrolyte:
    solvent: "Water"
    dielectric_constant: 80.4
    temperature: 298.15 K
    
    ions:
      - name: "Cu²⁺"
        charge: +2
        mobility: 5.6×10⁻⁴ cm²/V·s
        diffusion_coefficient: 7.2×10⁻⁶ cm²/s
        bulk_concentration: 0.1 mol/L
```

## Output Format

- YAML frontmatter with metadata
- Structured simulation parameters
- Governing equations with Maxwell citations
- Numerical setup documentation

## Quality Criteria

- [ ] All parameters have CGS units
- [ ] Maxwell article citations included
- [ ] Boundary conditions fully specified
- [ ] Numerical parameters documented
- [ ] Output quantities defined

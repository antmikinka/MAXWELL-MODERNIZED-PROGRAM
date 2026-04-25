# Template: galvanometer-design-template

## Purpose

Standardized template for galvanometer design and analysis following Maxwell's treatment of current measurement instruments.

## LLM Instructions

You are a galvanometer design specialist. Generate comprehensive galvanometer documentation connecting Maxwell's electromagnetic theory (Part IV) with instrument design principles.

1. **Establish Theoretical Foundation**: Link to Maxwell's Articles 475-500, 730-750
2. **Define Galvanometer Type**: Moving coil, moving magnet, mirror, etc.
3. **Design Magnetic Circuit**: Field strength, air gap, pole pieces
4. **Design Coil System**: Turns, dimensions, resistance
5. **Analyze Performance**: Sensitivity, response time, damping

## Template Structure

```yaml
galvanometer_design:
  name: "{{galvanometer_name}}"
  type: "{{moving_coil | moving_magnet | mirror | tangent | astatic}}"
  maxwell_articles: ["Art. 475-500", "Art. 730-750"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
magnetic_circuit:
  
  {% if type == 'moving_coil' %}
  permanent_magnet:
    material: "{{magnet_material}}"
    remanence: {{B_r}} gauss
    coercivity: {{H_c}} oersted
    dimensions:
      length: {{L_m}} cm
      width: {{W_m}} cm
      thickness: {{T_m}} cm
      
  air_gap:
    length: {{g}} cm
    flux_density: {{B_g}} gauss
    field_uniformity: "{{uniformity}}%"
    
  pole_pieces:
    material: "{{soft_iron}}"
    permeability: {{mu}}
    shape: "{{cylindrical | rectangular}}"
    
  {% elsif type == 'moving_magnet' %}
  suspended_magnet:
    material: "{{magnet_material}}"
    magnetic_moment: {{m}} emu
    dimensions:
      length: {{L}} cm
      cross_section: {{A}} cm²
      
  external_coil:
    num_turns: {{N}}
    radius: {{R}} cm
    length: {{L}} cm
  {% endif %}
  
coil_system:
  
  {% if type == 'moving_coil' %}
  moving_coil:
    num_turns: {{N}}
    wire_gauge: "{{AWG}}"
    wire_diameter: {{d}} cm
    
    dimensions:
      height: {{h}} cm
      width: {{w}} cm
      depth: {{d}} cm
    
    resistance: {{R_c}} statohm
    mass: {{m_c}} g
    moment_of_inertia: {{J}} g·cm²
    
  {% elsif type == 'tangent' %}
  tangent_coil:
    num_turns: {{N}}
    radius: {{R}} cm
    orientation: "Aligned with magnetic meridian"
  {% endif %}
  
sensitivity_analysis:

  {% if type == 'moving_coil' %}
  current_sensitivity:
    formula: "S = N·A·B / κ"
    where:
      N: "Number of turns"
      A: "Coil area (cm²)"
      B: "Air gap flux density (gauss)"
      κ: "Spring constant (dyne·cm/rad)"
    
    calculated: {{S}} cm/statampere
    in_divisions: {{S_div}} divisions/statampere
    
  voltage_sensitivity:
    formula: "S_V = S / R_total"
    where:
      R_total: "Coil resistance + external resistance"
    
    calculated: {{S_V}} divisions/statvolt
    
  {% elsif type == 'moving_magnet' %}
  current_sensitivity:
    formula: "S = (2π·N·m) / (κ·R)"
    where:
      m: "Magnetic moment (emu)"
      R: "Coil radius (cm)"
    
    calculated: {{S}} rad/statampere
    
  {% elsif type == 'tangent' %}
  tangent_law:
    formula: "I = (2·R·H / N) · tan(θ)"
    where:
      R: "Coil radius (cm)"
      H: "Earth's horizontal field (oersted)"
      θ: "Deflection angle"
    
    reduction_factor: {{K}} = (2·R·H / N) statampere
  {% endif %}
  
restoring_system:

  {% if type == 'moving_coil' %}
  suspension:
    type: "{{ribbon | pivot | taut_band}}"
    material: "{{phosphor_bronze | quartz}}"
    
    properties:
      spring_constant: {{κ}} dyne·cm/rad
      maximum_torque: {{τ_max}} dyne·cm
      elastic_limit: "{{within_limits | exceeded}}"
      
  {% elsif type == 'moving_magnet' %}
  suspension:
    type: "{{fiber | pivot}}"
    material: "{{silk | quartz}}"
    
    torsion_constant: {{κ}} dyne·cm/rad
  {% endif %}
  
damping_analysis:

  electromagnetic_damping:
    mechanism: "Eddy currents in coil/circuit"
    damping_constant: {{D_em}} = (N·A·B)² / R_total
    
  air_damping:
    contribution: {{D_air}} dyne·cm·s
    vane_design: "{{if_applicable}}"
    
  total_damping:
    D_total = {{D_total}} dyne·cm·s
    
  damping_ratio:
    ζ = D_total / (2·√(J·κ)) = {{zeta}}
    
  response_characteristic: "{{underdamped | critically_damped | overdamped}}"
  
dynamic_response:

  natural_frequency:
    ω_n = √(κ/J) = {{omega_n}} rad/s
    f_n = {{f_n}} Hz
    
  settling_time:
    2% criterion: {{t_s}} s
    
  bandwidth:
    {{BW}} Hz
    
  step_response:
    rise_time: {{t_r}} s
    overshoot: {{overshoot}}%
    
  frequency_response:
    flat_to: {{f_flat}} Hz
    -3dB_point: {{f_3dB}} Hz
    
error_analysis:

  systematic_errors:
    - source: "Non-uniform field"
      magnitude: {{error_field}}%
      mitigation: "{{pole_piece_design}}"
      
    - source: "Temperature drift"
      magnitude: {{tempco}}%/K
      mitigation: "{{compensation}}"
      
    - source: "Zero drift"
      magnitude: {{drift}} divisions/hour
      mitigation: "Regular zero adjustment"
      
    - source: "Non-linearity"
      magnitude: {{nonlinearity}}% FS
      mitigation: "{{correction_curve}}"
      
  random_errors:
    - source: "Mechanical vibration"
      standard_deviation: {{sigma_vib}} divisions
      
    - source: "Thermal noise"
      standard_deviation: {{sigma_thermal}} divisions
      
  total_uncertainty:
    expanded: {{U}} divisions (k=2)
    
maxwell_design_principles:
  electromagnetic_force: "Art. 475-500"
  galvanometer_theory: "Art. 730-750"
  measurement_accuracy: "Art. 287-300"
  calibration: "Art. 343-348"
  
cgs_units:
  current: "statampere"
  voltage: "statvolt"
  magnetic_field: "gauss (B), oersted (H)"
  magnetic_moment: "emu"
  torque: "dyne·cm"
  spring_constant: "dyne·cm/rad"
  inertia: "g·cm²"
```

## Galvanometer Types Comparison

| Type | Sensitivity | Range | Best For |
|------|-------------|-------|----------|
| Moving Coil | Medium | 1 μA - 1 mA | General purpose |
| Moving Magnet | Low | 1 mA - 1 A | Rugged applications |
| Mirror | High | 1 nA - 10 μA | Sensitive measurements |
| Tangent | Low | 0.1 A - 10 A | Educational |
| Astatic | Very High | 0.1 nA - 1 μA | Ultra-sensitive |

## Quality Criteria

- [ ] Magnetic circuit designed
- [ ] Coil system specified
- [ ] Sensitivity calculated
- [ ] Dynamic response analyzed
- [ ] Error sources identified
- [ ] Maxwell article citations included

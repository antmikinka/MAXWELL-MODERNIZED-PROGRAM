# Template: magnetometer-calibration-template

## Purpose

Standardized template for magnetometer calibration and measurement documentation.

## LLM Instructions

You are a magnetometry specialist. Generate comprehensive magnetometer calibration documentation following Maxwell's magnetic theory (Part III) and modern calibration practices.

1. **Establish Theoretical Foundation**: Link to Maxwell's Articles 424-440
2. **Define Magnetometer Type**: Deflection, vibration, fluxgate, etc.
3. **Document Calibration Procedure**: Step-by-step protocol
4. **Analyze Uncertainty**: Complete uncertainty budget
5. **Establish Traceability**: Calibration chain

## Template Structure

```yaml
magnetometer_calibration:
  name: "{{magnetometer_name}}"
  type: "{{deflection | vibration | fluxgate | hall | search_coil | squid}}"
  maxwell_articles: ["Art. 424-440", "Art. 449-474"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
instrument_description:
  manufacturer: "{{manufacturer}}"
  model: "{{model}}"
  serial: "{{serial_number}}"
  
  sensing_element:
    type: "{{element_type}}"
    dimensions: {{dimensions}}
    material: "{{material}}"
    
  readout:
    type: "{{visual | electronic | digital}}"
    resolution: {{resolution}}
    range: {{range}} oersted
    
theoretical_basis:

  {% if type == 'deflection' %}
  deflection_magnetometer:
    principle: "Torque on magnetic needle in external field"
    equation: "τ = m·H·sin(θ) = κ·θ (at equilibrium)"
    
    measurement_equation: "H = (κ/m) · θ"
    
    where:
      m: "Magnetic moment of needle (emu)"
      H: "External field (oersted)"
      θ: "Deflection angle (radians)"
      κ: "Torsion constant (dyne·cm/rad)"
      
    maxwell_reference: "Art. 424-440"
    
  {% elsif type == 'vibration' %}
  vibration_magnetometer:
    principle: "Oscillation period of magnetic needle"
    equation: "T = 2π·√(J/(m·H))"
    
    measurement_equation: "H = (4π²·J) / (m·T²)"
    
    where:
      J: "Moment of inertia (g·cm²)"
      m: "Magnetic moment (emu)"
      T: "Period (s)"
      
    maxwell_reference: "Art. 424-440"
    
  {% elsif type == 'fluxgate' %}
  fluxgate_magnetometer:
    principle: "Core saturation modulation"
    equation: "V_out ∝ H_ext"
    
    sensitivity: {{S}} statvolt/oersted
    
  {% elsif type == 'hall' %}
  hall_effect_magnetometer:
    principle: "Hall voltage in semiconductor"
    equation: "V_H = (R_H · I · B) / t"
    
    where:
      R_H: "Hall coefficient"
      I: "Control current"
      B: "Magnetic flux density"
      t: "Sensor thickness"
  {% endif %}
  
calibration_setup:

  reference_standard:
    type: "{{standard_magnet | helmholtz_coils | NMR_magnetometer}}"
    certificate: "{{cert_number}}"
    uncertainty: {{u_ref}} oersted
    traceability: "{{NIST | PTB | etc.}}"
    
  helmholtz_coils:
    {% if used %}
    radius: {{R}} cm
    num_turns: {{N}}
    separation: {{s}} cm (ideally s = R)
    
    field_constant: {{K_H}} oersted/statampere
    formula: "H = (32π·N / (5√5·R)) · I" (CGS)
    
    uniformity: "{{uniformity}}%"
    volume: "{{uniform_volume}} cm³"
    {% endif %}
    
  environmental_conditions:
    temperature: {{T}} ± {{ΔT}} K
    humidity: {{RH}} ± {{ΔRH}} %
    ambient_field: {{H_amb}} oersted
    
calibration_procedure:

  steps:
    - step: "Warm-up"
      duration: {{duration}} minutes
      criteria: "{{stability_criterion}}"
      
    - step: "Zero adjustment"
      procedure: "{{zero_procedure}}"
      tolerance: {{zero_tol}} oersted
      
    - step: "Span calibration"
      points: {{num_points}}
      values: [{{calibration_points}}] oersted
      procedure: "{{span_procedure}}"
      
    - step: "Linearity check"
      direction: "Increasing and decreasing"
      hysteresis_check: "{{yes | no}}"
      
    - step: "Repeatability test"
      repetitions: {{n}}
      at_field: {{test_field}} oersted
      
  data_recording:
    format: "{{data_format}}"
    sampling_rate: {{rate}} Hz
    averaging: {{avg_count}} readings
    
calibration_data:

  raw_data:
    {{calibration_readings}}
    
  calibration_curve:
    fitted_model: "{{linear | polynomial | lookup_table}}"
    equation: "{{fitted_equation}}"
    coefficients:
      {{coefficients}}
    r_squared: {{R²}}
    residual_std: {{σ_res}} oersted
    
  linearity:
    maximum_deviation: {{max_dev}} oersted
    percentage_fs: {{linearity}}% FS
    
  hysteresis:
    maximum_hysteresis: {{hyst}} oersted
    percentage_fs: {{hyst_pct}}% FS
    
  repeatability:
    standard_deviation: {{s}} oersted
    relative: {{s_rel}}%
    
uncertainty_budget:

  type_a (statistical):
    - source: "Repeatability"
      value: {{u_rep}} oersted
      distribution: "normal"
      dof: {{dof}}
      
    - source: "Resolution"
      value: {{u_res}} oersted
      distribution: "rectangular"
      
  type_b (systematic):
    - source: "Reference standard"
      value: {{u_ref}} oersted
      distribution: "normal"
      coverage: {{k_ref}}
      
    - source: "Temperature effect"
      value: {{u_temp}} oersted
      distribution: "rectangular"
      
    - source: "Non-linearity"
      value: {{u_lin}} oersted
      distribution: "rectangular"
      
    - source: "Hysteresis"
      value: {{u_hyst}} oersted
      distribution: "rectangular"
      
  combined_uncertainty:
    u_c = √(Σu_i²) = {{u_c}} oersted
    
  expanded_uncertainty:
    U = k·u_c = {{U}} oersted
    coverage_factor: k = 2
    confidence_level: 95%
    
traceability:

  calibration_chain:
    - level: "Primary standard"
      institution: "{{NIST | PTB | etc.}}"
      
    - level: "Secondary standard"
      uncertainty: {{u_secondary}} oersted
      
    - level: "Working standard"
      uncertainty: {{u_working}} oersted
      
  traceability_statement:
    "Measurements traceable to national standards through {{chain}}"
    
maxwell_contributions:
  magnetic_force: "Art. 424-440"
  magnetic_measurements: "Art. 449-474"
  magnetometry_methods: "Detailed in Treatise"
  
cgs_units:
  magnetic_field_h: "oersted"
  magnetic_induction_b: "gauss"
  magnetic_moment: "emu"
  torque: "dyne·cm"
  moment_of_inertia: "g·cm²"
```

## Calibration Points Example

| Point | Applied H (oersted) | Reading (oersted) | Deviation |
|-------|---------------------|-------------------|-----------|
| 1 | 0.00 | 0.002 | +0.002 |
| 2 | 0.25 | 0.251 | +0.001 |
| 3 | 0.50 | 0.498 | -0.002 |
| 4 | 0.75 | 0.752 | +0.002 |
| 5 | 1.00 | 0.999 | -0.001 |

## Quality Criteria

- [ ] Theoretical basis documented
- [ ] Calibration setup described
- [ ] Procedure followed step-by-step
- [ ] Data recorded completely
- [ ] Uncertainty budget complete
- [ ] Traceability established
- [ ] Maxwell article citations included

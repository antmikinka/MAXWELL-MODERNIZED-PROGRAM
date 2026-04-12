# Template: instrument-modeling-template

## Purpose

Standardized template for instrument modeling documentation covering galvanometers, magnetometers, electrometers, and other measurement devices.

## LLM Instructions

You are an instrument modeling specialist. Generate comprehensive instrument documentation that connects Maxwell's measurement theory with modern instrument analysis.

1. **Establish Theoretical Foundation**: Link to Maxwell's Articles on measurement
2. **Define Instrument Physics**: Operating principle, governing equations
3. **Model Dynamic Response**: Time response, frequency response
4. **Characterize Errors**: Systematic errors, random errors
5. **Document Calibration**: Calibration procedures, traceability

## Template Structure

```yaml
instrument_model:
  name: "{{instrument_name}}"
  type: "{{galvanometer | magnetometer | electrometer | ammeter | voltmeter | wattmeter}}"
  maxwell_articles: ["{{relevant_articles}}"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
operating_principle:
  physical_effect: "{{effect_description}}"
  maxwell_reference: "{{article}}"
  
  {% if type == 'galvanometer' %}
  principle: "Torque on current-carrying coil in magnetic field"
  torque: "τ = N·I·A·B·sin(θ)"
  maxwell_reference: "Art. 475-500, Art. 730-750"
  
  {% elsif type == 'magnetometer' %}
  principle: "Deflection of magnetic needle in external field"
  torque: "τ = m·H·sin(θ)"
  maxwell_reference: "Art. 424-440"
  
  {% elsif type == 'electrometer' %}
  principle: "Force on charged body in electric field"
  force: "F = q·E"
  maxwell_reference: "Art. 44-49, Art. 230-235"
  {% endif %}
  
governing_equations:
  
  mechanical:
    equation: "J·d²θ/dt² + D·dθ/dt + κ·θ = τ_drive"
    
    where:
      J: "Moment of inertia (g·cm²)"
      D: "Damping coefficient (dyne·cm·s)"
      κ: "Restoring spring constant (dyne·cm/rad)"
      θ: "Deflection angle (radians)"
      τ_drive: "Driving torque (dyne·cm)"
    
  electrical:
    {% if type == 'galvanometer' %}
    back_emf: "e = N·A·B·dθ/dt"
    circuit: "V = I·R + e"
    {% elsif type == 'electrometer' %}
    charge_relation: "Q = C·V"
    force: "F = (1/2)·V²·dC/dx"
    {% endif %}
  
  coupling:
    {% if type == 'galvanometer' %}
    torque_constant: "K_t = N·A·B (dyne·cm/statampere)"
    back_emf_constant: "K_e = N·A·B (statvolt·s/rad)"
    note: "K_t = K_e in consistent units"
    {% endif %}
  
static_characteristics:

  sensitivity:
    current_sensitivity: {{S_I}} statampere/division
    voltage_sensitivity: {{S_V}} statvolt/division
    deflection_factor: {{K_d}} divisions/statunit
    
  range:
    full_scale: {{FS}} {{unit}}
    minimum_readable: {{min}} {{unit}}
    resolution: {{resolution}} {{unit}}
    
  accuracy:
    linearity: {{linearity_error}} % FS
    hysteresis: {{hysteresis_error}} % FS
    repeatability: {{repeatability_error}} % FS
    
dynamic_response:

  transfer_function:
    G(s) = θ(s)/I(s) = K / (J·s² + D·s + κ)
    
  natural_frequency:
    ω_n = √(κ/J) rad/s
    f_n = ω_n/(2π) Hz
    
  damping_ratio:
    ζ = D / (2·√(J·κ))
    
  response_types:
    underdamped: "ζ < 1 (oscillatory)"
    critically_damped: "ζ = 1 (fastest non-oscillatory)"
    overdamped: "ζ > 1 (sluggish)"
    
  settling_time:
    2% criterion: "t_s ≈ 4/(ζ·ω_n)"
    
  frequency_response:
    bandwidth: "{{BW}} Hz"
    resonance_peak: "{{M_p}} dB"
    phase_margin: "{{PM}} degrees"
    
error_sources:

  systematic:
    - source: "{{error_type}}"
      magnitude: {{magnitude}}
      correction: "{{correction_method}}"
      
    - source: "Zero drift"
      magnitude: {{drift}} {{unit}}/hour
      correction: "Regular zero adjustment"
      
    - source: "Temperature coefficient"
      magnitude: {{tempco}} %/K
      correction: "Temperature compensation"
      
    - source: "Non-linearity"
      magnitude: {{nonlinearity}} % FS
      correction: "Calibration curve"
      
  random:
    - source: "{{noise_type}}"
      standard_deviation: {{sigma}}
      distribution: "{{normal | uniform | etc}}"
      
  environmental:
    temperature_range: {{T_min}} - {{T_max}} K
    humidity_range: {{RH_min}} - {{RH_max}} %
    magnetic_interference: "{{sensitivity}} statampere/(oersted·cm³)"
    
calibration:

  procedure:
    steps:
      - "Warm-up: {{duration}}"
      - "Zero adjustment: {{procedure}}"
      - "Span adjustment: {{procedure}}"
      - "Linearity check: {{points}} points"
      - "Hysteresis check: {{procedure}}"
      
  standards:
    - standard: "{{standard_name}}"
      value: {{value}} {{unit}}
      uncertainty: {{u}} {{unit}}
      traceability: "{{chain}}"
      
  calibration_curve:
    fitted_equation: "{{equation}}"
    r_squared: {{R²}}
    residual_max: {{max_residual}}
    
  calibration_interval: "{{interval}}"
  
maxwell_contributions:
  measurement_theory: "{{article}}"
  instrument_analysis: "{{article}}"
  error_discussion: "{{article}}"
  calibration_methods: "{{article}}"
  
cgs_units:
  current: "statampere"
  voltage: "statvolt"
  charge: "statcoulomb"
  field: "statvolt/cm (E), oersted (H)"
  torque: "dyne·cm"
  inertia: "g·cm²"
```

## Instrument Types Reference

| Instrument | Measures | Maxwell Articles | Principle |
|------------|----------|------------------|-----------|
| Galvanometer | Current | Art. 475-500, 730-750 | Magnetic torque |
| Magnetometer | H field | Art. 424-440 | Needle deflection |
| Electrometer | Voltage | Art. 44-49, 230-235 | Electric force |
| Tangent Galvanometer | Current | Art. 730-750 | Tangent law |
| Mirror Galvanometer | Small current | Art. 730-750 | Optical lever |
| Quadrant Electrometer | Voltage | Art. 230-235 | Attracted disc |

## Quality Criteria

- [ ] Operating principle documented
- [ ] Governing equations complete
- [ ] Dynamic response characterized
- [ ] Error sources identified
- [ ] Calibration procedures documented
- [ ] Maxwell article citations included

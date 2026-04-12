# Template: sensitivity-analysis-template

## Purpose

Standardized template for instrument sensitivity analysis covering current, voltage, and magnetic field measurements.

## LLM Instructions

You are a sensitivity analysis specialist. Generate comprehensive sensitivity documentation following Maxwell's instrument analysis and modern metrology practices.

1. **Establish Theoretical Foundation**: Link to Maxwell's measurement articles
2. **Define Sensitivity Metrics**: Input/output relations
3. **Analyze Limiting Factors**: Noise, drift, resolution
4. **Optimize Design**: Parameter selection for maximum sensitivity
5. **Document Results**: Sensitivity tables, graphs

## Template Structure

```yaml
sensitivity_analysis:
  name: "{{analysis_name}}"
  instrument_type: "{{instrument_type}}"
  measurand: "{{measurand}}"
  maxwell_articles: ["{{relevant_articles}}"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
sensitivity_definitions:

  absolute_sensitivity:
    definition: "S = output_change / input_change"
    formula: "{{sensitivity_formula}}"
    units: "{{output_unit}}/{{input_unit}}"
    
  relative_sensitivity:
    definition: "S_rel = (Δoutput/output) / (Δinput/input)"
    formula: "{{relative_sensitivity_formula}}"
    units: "dimensionless"
    
  resolution:
    definition: "Smallest detectable input change"
    limited_by: "{{limiting_factor}}"
    value: {{resolution}} {{input_unit}}
    
  threshold:
    definition: "Minimum input to produce measurable output"
    value: {{threshold}} {{input_unit}}
    
theoretical_sensitivity:

  {% if instrument_type == 'galvanometer' %}
  current_sensitivity:
    formula: "S_I = N·A·B / κ"
    
    parameters:
      N: {{N}} "turns"
      A: {{A}} "cm² (coil area)"
      B: {{B}} "gauss (field strength)"
      κ: {{κ}} "dyne·cm/rad (spring constant)"
    
    calculated: {{S_I}} cm/statampere
    in_divisions: {{S_I_div}} divisions/statampere
    
  voltage_sensitivity:
    formula: "S_V = S_I / R_total"
    
    parameters:
      R_total: {{R_total}} "statohm"
    
    calculated: {{S_V}} divisions/statvolt
    
  {% elsif instrument_type == 'electrometer' %}
  voltage_sensitivity:
    formula: "S_V = dθ/dV = (1/2)·V_n·(dC/dθ) / κ"
    
    parameters:
      V_n: {{V_n}} "statvolt (needle potential)"
      dC/dθ: {{dC_dθ}} "statfarad/rad"
      κ: {{κ}} "dyne·cm/rad"
    
    calculated: {{S_V}} rad/statvolt
    
  charge_sensitivity:
    formula: "S_Q = dV_out/dQ = 1/C_f"
    
    parameters:
      C_f: {{C_f}} "statfarad (feedback capacitance)"
    
    calculated: {{S_Q}} statvolt/statcoulomb
    
  {% elsif instrument_type == 'magnetometer' %}
  field_sensitivity:
    formula: "{{field_sensitivity_formula}}"
    
    parameters:
      {{parameters}}
    
    calculated: {{S_H}} {{output_unit}}/oersted
  {% endif %}
  
noise_limited_sensitivity:

  thermal_noise:
    johnson_noise:
      formula: "e_n² = 4·k_B·T·R·Δf"
      
      parameters:
        k_B: "1.381×10⁻¹⁶ erg/K (Boltzmann constant)"
        T: {{T}} "K"
        R: {{R}} "statohm"
        Δf: {{BW}} "Hz"
      
      calculated: {{e_n}} statvolt
      
    current_noise:
      formula: "i_n² = 4·k_B·T·Δf / R"
      calculated: {{i_n}} statampere
      
  shot_noise:
    formula: "i_n² = 2·q·I·Δf"
    
    parameters:
      q: "4.803×10⁻¹⁰ statcoulomb (elementary charge)"
      I: {{I}} "statampere"
      Δf: {{BW}} "Hz"
    
    calculated: {{i_n}} statampere
    
  flicker_noise:
    formula: "e_n² = K_f / f"
    
    parameters:
      K_f: {{K_f}} "noise coefficient"
    
    corner_frequency: {{f_c}} Hz
    
  vibration_noise:
    microphonic_sensitivity: {{S_v}} {{output_unit}}/(cm/s²)
    ambient_vibration: {{a_vib}} cm/s²
    contribution: {{e_vib}} {{output_unit}}
    
  total_noise:
    rss_sum: {{e_total}} = √(Σe_i²) = {{e_total_val}} {{output_unit}}
    bandwidth: {{BW}} Hz
    
minimum_detectable_signal:

  definition: "Input signal that produces output equal to noise level"
  
  snr_criterion:
    minimum_snr: {{SNR_min}} (typically 1-3)
    
  mds_calculation:
    MDS = (SNR_min × e_total) / S
    
    where:
      S: "Sensitivity ({{sensitivity_units}})"
      e_total: "Total noise ({{noise_units}})"
    
    calculated: {{MDS}} {{input_unit}}
    
  integration_improvement:
    formula: "MDS(t) = MDS(1s) / √t"
    
    with_1s: {{MDS_1s}} {{input_unit}}
    with_10s: {{MDS_10s}} {{input_unit}}
    with_100s: {{MDS_100s}} {{input_unit}}
    
drift_limited_sensitivity:

  thermal_drift:
    temperature_coefficient: {{TC}} {{output_unit}}/K
    temperature_stability: {{ΔT}} K/hour
    drift_rate: {{drift_T}} = {{TC}}×{{ΔT}} = {{drift_T_val}} {{output_unit}}/hour
    
  zero_drift:
    specified_drift: {{zero_drift}} {{output_unit}}/hour
    dominant_mechanism: "{{mechanism}}"
    
  sensitivity_drift:
    gain_stability: {{gain_drift}} %/hour
    effect_on_reading: {{gain_effect}} {{output_unit}}/hour
    
  drift_limited_resolution:
    definition: "Minimum input detectable before drift dominates"
    for_{{integration_time}}s: {{DLR}} {{input_unit}}
    
dynamic_sensitivity:

  frequency_dependent_sensitivity:
    formula: "S(f) = S_0 / √(1 + (f/f_c)²)"
    
    parameters:
      S_0: {{S_0}} "low-frequency sensitivity"
      f_c: {{f_c}} "Hz (corner frequency)"
    
    at_{{f1}}_Hz: {{S_f1}} {{units}}
    at_{{f2}}_Hz: {{S_f2}} {{units}}
    
  bandwidth:
    definition: "Frequency where sensitivity drops to S_0/√2"
    value: {{BW}} Hz
    
  phase_shift:
    at_bandwidth: "{{phase}} degrees"
    
optimization:

  parameters_to_optimize:
    - parameter: "{{param_name}}"
      current_value: {{current}}
      optimal_value: {{optimal}}
      improvement: {{improvement}}%
      
  trade_studies:
    - trade: "Sensitivity vs. Bandwidth"
      relationship: "S × BW ≈ constant (for some instruments)"
      optimum: "{{optimum_point}}"
      
    - trade: "Sensitivity vs. Input Range"
      relationship: "Higher sensitivity = narrower range"
      optimum: "{{optimum_point}}"
      
  design_recommendations:
    - "{{recommendation_1}}"
    - "{{recommendation_2}}"
    - "{{recommendation_3}}"
    
sensitivity_summary:

  | Metric | Value | Units | Conditions |
  |--------|-------|-------|------------|
  | Theoretical Sensitivity | {{S_theory}} | {{S_units}} | {{conditions}} |
  | Noise-Limited MDS | {{MDS}} | {{input_units}} | {{BW}} Hz |
  | Drift-Limited Resolution | {{DLR}} | {{input_units}} | {{time}} |
  | Dynamic Range | {{DR}} | dB | {{conditions}} |
  
maxwell_contributions:
  instrument_sensitivity: "{{article}}"
  measurement_limits: "{{article}}"
  error_analysis: "{{article}}"
  
cgs_units:
  input: "{{input_unit}}"
  output: "{{output_unit}}"
  sensitivity: "{{output_unit}}/{{input_unit}}"
```

## Sensitivity Comparison Table

| Instrument | Typical Sensitivity | Best Achievable | Limiting Factor |
|------------|--------------------|-----------------|-----------------|
| Moving coil galvanometer | 1 μA/div | 0.1 μA/div | Thermal noise |
| Mirror galvanometer | 1 nA/div | 0.01 nA/div | Vibration |
| Quadrant electrometer | 0.1 V/div | 0.001 V/div | Mechanical drift |
| Vibrating reed electrometer | 1 mV/div | 10 μV/div | Electronic noise |
| Fluxgate magnetometer | 0.001 Oe | 0.00001 Oe | Core noise |

## Quality Criteria

- [ ] Sensitivity definitions complete
- [ ] Theoretical sensitivity calculated
- [ ] Noise analysis included
- [ ] Drift analysis included
- [ ] Optimization recommendations provided
- [ ] Maxwell article citations included

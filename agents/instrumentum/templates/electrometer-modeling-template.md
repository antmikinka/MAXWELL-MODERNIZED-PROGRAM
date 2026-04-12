# Template: electrometer-modeling-template

## Purpose

Standardized template for electrometer modeling and analysis following Maxwell's electrostatic theory.

## LLM Instructions

You are an electrometer specialist. Generate comprehensive electrometer documentation that connects Maxwell's electrostatic theory (Part I) with modern high-impedance measurement techniques.

1. **Establish Theoretical Foundation**: Link to Maxwell's Articles 44-49, 230-235
2. **Define Electrometer Type**: Quadrant, vibrating reed, Faraday cup, etc.
3. **Model Electrostatic Forces**: Force/voltage relations
4. **Characterize Input Impedance**: Ultra-high resistance, low capacitance
5. **Analyze Noise and Sensitivity**: Fundamental limits

## Template Structure

```yaml
electrometer_model:
  name: "{{electrometer_name}}"
  type: "{{quadrant | vibrating_reed | faraday_cup | linear | digital}}"
  maxwell_articles: ["Art. 44-49", "Art. 230-235"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
operating_principle:

  {% if type == 'quadrant' %}
  quadrant_electrometer:
    principle: "Torque on charged needle between quadrants"
    
    configuration:
      - "Four insulated quadrants (A, B, C, D)"
      - "Suspended needle at potential V_n"
      - "Opposite quadrants connected together"
      
    torque_equation:
      τ = (1/2) · (V_A - V_B) · V_n · (dC/dθ)
      
    where:
      V_A, V_B: "Quadrant potentials (statvolt)"
      V_n: "Needle potential (statvolt)"
      dC/dθ: "Rate of capacitance change (statfarad/rad)"
      
    maxwell_reference: "Art. 230-235"
    
  {% elsif type == 'vibrating_reed' %}
  vibrating_reed_electrometer:
    principle: "Capacitance modulation converts DC to AC"
    
    configuration:
      - "Fixed electrode at measured potential"
      - "Vibrating reed (grounded)"
      - "AC amplifier and demodulator"
      
    output_voltage:
      V_out = V_in · (ΔC/C) · G
      
    where:
      ΔC: "Capacitance variation"
      G: "Amplifier gain"
      
  {% elsif type == 'faraday_cup' %}
  faraday_cup_electrometer:
    principle: "Charge collection on isolated conductor"
    
    configuration:
      - "Isolated collecting electrode"
      - "Electrometer amplifier"
      - "Feedback resistor for current measurement"
      
    current_measurement:
      I = V_out / R_f
      
    charge_measurement:
      Q = C_f · V_out
  {% endif %}
  
electrostatic_analysis:

  {% if type == 'quadrant' %}
  capacitance_model:
    needle_to_quadrant: {{C_nq}} statfarad
    quadrant_to_quadrant: {{C_qq}} statfarad
    variation_with_angle: "dC/dθ = {{dC_dθ}} statfarad/rad"
    
  torque_sensitivity:
    dτ/dV = {{dτ_dV}} dyne·cm/statvolt²
    angular_deflection: "θ = τ/κ = {{theta}} rad/statvolt²"
    
  {% elsif type == 'any' %}
  input_impedance:
    resistance: {{R_in}} statohm
    capacitance: {{C_in}} statfarad
    
  input_bias_current:
    value: {{I_bias}} statampere
    temperature_coefficient: {{tempco}} statampere/K
  {% endif %}
  
sensitivity_analysis:

  voltage_sensitivity:
    formula: "{{sensitivity_formula}}"
    calculated: {{S_V}} divisions/statvolt
    
  charge_sensitivity:
    minimum_detectable: {{Q_min}} statcoulomb
    limited_by: "{{noise | leakage | mechanical}}"
    
  current_sensitivity:
    minimum_detectable: {{I_min}} statampere
    integration_time: {{t_int}} s
    
  energy_resolution:
    minimum_energy: {{E_min}} erg
    thermal_limit: "k_B·T = {{kT}} erg at {{T}} K"
  
noise_analysis:

  thermal_noise:
    voltage_noise: {{e_n}} statvolt/√Hz
    formula: "e_n² = 4·k_B·T·R"
    
  shot_noise:
    current_noise: {{i_n}} statampere/√Hz
    formula: "i_n² = 2·q·I"
    
  flicker_noise:
    corner_frequency: {{f_c}} Hz
    magnitude: {{e_1hz}} statvolt/√Hz at 1 Hz
    
  vibration_noise:
    microphonic_sensitivity: {{S_v}} statvolt/(cm/s²)
    
  total_noise:
    integrated_rms: {{e_rms}} statvolt
    bandwidth: {{BW}} Hz
    
dynamic_response:

  bandwidth:
    small_signal: {{BW_ss}} Hz
    large_signal: {{BW_ls}} Hz
    
  rise_time:
    10-90%: {{t_r}} s
    
  settling_time:
    to_0.1%: {{t_s}} s
    
  frequency_response:
    flat_to: {{f_flat}} Hz
    rolloff: "{{rolloff_rate}} dB/octave"
    
error_sources:

  systematic:
    - source: "Input bias current"
      effect: "{{effect_description}}"
      correction: "{{correction_method}}"
      
    - source: "Input offset voltage"
      magnitude: {{V_os}} statvolt
      drift: {{drift}} statvolt/K
      
    - source: "Gain error"
      magnitude: {{gain_error}} %
      stability: {{stability}} %/year
      
    - source: "Non-linearity"
      magnitude: {{nonlinearity}} % FS
      
    - source: "Dielectric absorption"
      effect: "Memory effect in capacitors"
      mitigation: "{{material_selection}}"
      
    - source: "Leakage currents"
      magnitude: {{I_leak}} statampere
      paths: "{{leakage_paths}}"
      
  environmental:
    temperature_range: {{T_min}} - {{T_max}} K
    temperature_coefficient: {{tempco}} %/K
    humidity_sensitivity: "{{sensitivity_description}}"
    
  electromagnetic_interference:
    rf_susceptibility: "{{susceptibility_level}}"
    shielding: "{{shielding_description}}"
    guarding: "{{guarding_description}}"
    
applications:

  charge_measurement:
    range: {{Q_range}} statcoulomb
    accuracy: {{accuracy}} %
    
  current_measurement:
    range: {{I_range}} statampere
    accuracy: {{accuracy}} %
    
  voltage_measurement:
    range: {{V_range}} statvolt
    input_impedance: {{Z_in}} statohm
    
  specialized:
    - "{{application_1}}"
    - "{{application_2}}"
    
maxwell_contributions:
  electrostatic_potential: "Art. 44-49"
  capacitance_theory: "Art. 75-76"
  electrometer_design: "Art. 230-235"
  measurement_methods: "Throughout Treatise"
  
cgs_units:
  voltage: "statvolt"
  charge: "statcoulomb"
  current: "statampere"
  capacitance: "statfarad"
  resistance: "statohm"
  force: "dyne"
  torque: "dyne·cm"
```

## Electrometer Types Comparison

| Type | Voltage Range | Input R | Input C | Best For |
|------|---------------|---------|---------|----------|
| Quadrant | ±500 statV | >10²⁰ | <1 pF | High voltage |
| Vibrating Reed | ±50 statV | >10¹⁸ | <10 pF | General purpose |
| Faraday Cup | N/A | >10²⁰ | <1 pF | Charge/current |
| Linear | ±10 statV | >10¹⁶ | <100 pF | Low voltage |

## Quality Criteria

- [ ] Operating principle documented
- [ ] Electrostatic analysis complete
- [ ] Sensitivity characterized
- [ ] Noise analysis included
- [ ] Error sources identified
- [ ] Maxwell article citations included

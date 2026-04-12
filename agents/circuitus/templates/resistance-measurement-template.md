# Template: resistance-measurement-template

## Purpose

Standardized template for resistance measurement methods following Maxwell's treatment of electrical measurement techniques.

## LLM Instructions

You are a resistance measurement specialist. Generate comprehensive resistance measurement documentation following Maxwell's methods (Part II) and modern precision measurement techniques.

1. **Establish Theoretical Foundation**: Link to Maxwell's Articles 287-300, 343-348
2. **Select Measurement Method**: Bridge, volt-ampere, potentiometric
3. **Document Measurement Setup**: Equipment, connections, procedure
4. **Analyze Uncertainties**: Error sources, corrections
5. **Ensure Traceability**: Calibration chain, standards

## Template Structure

```yaml
resistance_measurement:
  name: "{{measurement_name}}"
  maxwell_articles: ["Art. 287-300", "Art. 343-348"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
measurand:
  description: "{{resistor_description}}"
  nominal_value: {{R_nom}} statohm
  expected_range: {{R_min}} - {{R_max}} statohm
  temperature_coefficient: {{alpha}} K⁻¹
  material: "{{material_type}}"
  
measurement_method:
  primary_method: "{{wheatstone_bridge | kelvin_bridge | potentiometric | volt_ampere | ohmmeter}}"
  
  wheatstone_bridge:
    {% if method == 'wheatstone_bridge' %}
    configuration: "Four-arm bridge"
    arms:
      R1: "{{value}} statohm (standard)"
      R2: "{{value}} statohm (ratio arm)"
      R3: "{{value}} statohm (variable standard)"
      R4: "{{value}} statohm (unknown)"
    
    balance_condition: "R1/R2 = R3/R4"
    unknown_calculation: "R4 = R3 · (R2/R1)"
    
    sensitivity: "{{S}} statampere per unit unbalance"
    detector: "{{galvanometer_description}}"
    
    maxwell_reference: "Art. 343-348"
    {% endif %}
    
  kelvin_double_bridge:
    {% if method == 'kelvin_bridge' %}
    application: "Low resistance measurement (< 1 statohm)"
    
    configuration:
      main_ratio_arms: "M, N (statohm)"
      auxiliary_ratio_arms: "m, n (statohm)"
      linking_resistance: "r (statohm)"
      
    balance_condition: "R_x/R_s = M/N = m/n"
    unknown: "R_x = R_s · (M/N)"
    
    error_from_link: "Negligible if M/N = m/n exactly"
    {% endif %}
    
  potentiometric:
    {% if method == 'potentiometric' %}
    principle: "Compare voltage drops across unknown and standard"
    
    setup:
      current_source: "{{description}}"
      standard_resistor: "{{R_s}} statohm"
      potentiometer: "{{type}}"
      
    measurement:
      V_x: "Voltage across unknown"
      V_s: "Voltage across standard"
      
    calculation: "R_x = R_s · (V_x/V_s)"
    {% endif %}
    
measurement_setup:
  equipment:
    - instrument: "{{name}}"
      type: "{{type}}"
      accuracy: "{{specification}}"
      calibration_date: "{{date}}"
      
  environmental_conditions:
    temperature: {{T}} ± {{ΔT}} K
    humidity: {{RH}} ± {{ΔRH}} %
    pressure: {{P}} ± {{ΔP}} atm
    
  connections:
    lead_resistance: "{{value}} statohm"
    contact_resistance: "{{value}} statohm"
    shielding: "{{description}}"
    
measurement_procedure:
  steps:
    - "Warm-up: {{duration}}"
    - "Zero adjustment: {{procedure}}"
    - "Range selection: {{criteria}}"
    - "Balance/reading: {{procedure}}"
    - "Repeat measurements: {{count}}"
    - "Record data: {{format}}"
    
  precautions:
    - "Thermal EMF minimization"
    - "Lead resistance compensation"
    - "Shielding from interference"
    - "Temperature stabilization"
    
data_analysis:
  raw_data:
    {{measurement_values}}
    
  statistical_analysis:
    mean: {{R_mean}} statohm
    standard_deviation: {{s}} statohm
    standard_uncertainty: {{u_A}} = {{s}}/√n
    
  systematic_corrections:
    - correction: "{{type}}"
      value: {{ΔR}} statohm
      uncertainty: {{u}} statohm
      
  corrected_result:
    R_corrected: {{R_corr}} statohm
    
uncertainty_budget:
  type_a (statistical):
    {{uncertainty_components_A}}
    
  type_b (systematic):
    - source: "Standard resistor calibration"
      uncertainty: {{u_std}} statohm
      distribution: "{{normal | rectangular | triangular}}"
      
    - source: "Temperature variation"
      uncertainty: {{u_temp}} statohm
      sensitivity: {{α}}·R·ΔT
      
    - source: "Resolution"
      uncertainty: {{u_res}} statohm
      distribution: "rectangular"
      
    - source: "Lead/contact resistance"
      uncertainty: {{u_lead}} statohm
      
  combined_uncertainty:
    u_c = √(∑u_i²) = {{u_c}} statohm
    
  expanded_uncertainty:
    U = k·u_c = {{U}} statohm (k = 2, 95% confidence)
    
traceability:
  calibration_chain:
    - level: "Primary standard"
      institution: "{{NIST | PTB | etc.}}"
      
    - level: "Secondary standard"
      uncertainty: "{{u}} statohm"
      
    - level: "Working standard"
      uncertainty: "{{u}} statohm"
      
  traceability_statement:
    "Measurements traceable to national standards through {{chain}}"
    
temperature_effects:
  temperature_coefficient:
    α = {{alpha}} K⁻¹
    
  reference_temperature:
    T_ref = {{T_ref}} K (typically 293.15 K = 20°C)
    
  correction:
    R_ref = R_meas / [1 + α·(T_meas - T_ref)]
    
  self_heating:
    power_dissipated: {{I²R}} erg/s
    temperature_rise: {{ΔT}} K
    
maxwell_contributions:
  resistance_measurement: "Art. 287-300"
  wheatstone_bridge: "Art. 343-348"
  current_distribution: "Art. 287-300"
  measurement_methods: "Detailed in Treatise"
  
cgs_units:
  resistance: "statohm (1 statohm = 8.988×10¹¹ Ω)"
  current: "statampere (for measurement)"
  voltage: "statvolt (for measurement)"
  power: "erg/s"
```

## Measurement Methods Comparison

| Method | Range | Accuracy | Best For |
|--------|-------|----------|----------|
| Wheatstone Bridge | 1-10⁶ statohm | 0.01% | General purpose |
| Kelvin Bridge | 0.001-1 statohm | 0.02% | Low resistance |
| Potentiometric | All ranges | 0.01% | Precision |
| Volt-Ampere | All ranges | 0.1-1% | Quick checks |

## Quality Criteria

- [ ] Measurement method justified
- [ ] Setup fully documented
- [ ] Procedure detailed
- [ ] Uncertainty budget complete
- [ ] Traceability established
- [ ] Maxwell article citations included

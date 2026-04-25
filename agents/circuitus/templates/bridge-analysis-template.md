# Template: bridge-analysis-template

## Purpose

Standardized template for bridge circuit analysis including Wheatstone, Kelvin, AC bridges, and Maxwell's bridge methods.

## LLM Instructions

You are a bridge circuit specialist. Generate comprehensive bridge analysis documentation following Maxwell's resistance measurement methods and modern bridge analysis techniques.

1. **Establish Theoretical Foundation**: Link to Maxwell's Articles 343-348 (Wheatstone bridge), 287-300 (resistance)
2. **Define Bridge Topology**: Four-arm configuration, source, detector
3. **Derive Balance Conditions**: Null condition equations
4. **Analyze Sensitivity**: Response to imbalance
5. **Document Measurement Procedure**: Step-by-step protocol

## Template Structure

```yaml
bridge_analysis:
  name: "{{bridge_name}}"
  type: "{{wheatstone | kelvin | maxwell | hay | schering | anderson | wien}}"
  maxwell_articles: ["Art. 343-348", "Art. 287-300"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
bridge_topology:
  configuration: "Four-arm bridge"
  
  arms:
    arm_1:
      impedance: {{Z1}}
      composition: "{{R | L | C | combination}}"
      value: {{value1}}
      unit: "{{statohm | cm | statfarad}}"
      
    arm_2:
      impedance: {{Z2}}
      composition: "{{R | L | C | combination}}"
      value: {{value2}}
      unit: "{{unit}}"
      
    arm_3:
      impedance: {{Z3}}
      composition: "{{R | L | C | combination}}"
      value: {{value3}}
      unit: "{{unit}}"
      
    arm_4:
      impedance: {{Z4}}
      composition: "{{R | L | C | combination}}"
      value: {{value4}}
      unit: "{{unit}}"
      note: "{{unknown | standard | variable}}"
      
  source:
    type: "{{DC | AC}}"
    value: {{V_s}} statvolt (or I_s statampere)
    frequency: {{f}} Hz (if AC)
    internal_resistance: {{R_s}} statohm
    
  detector:
    type: "{{galvanometer | null_meter | lock-in}}"
    resistance: {{R_d}} statohm
    sensitivity: {{S}} statampere/division
    internal_resistance: {{R_g}} statohm
    
balance_condition:
  general_form: "Z1/Z2 = Z3/Z4"
  or: "Z1 · Z4 = Z2 · Z3"
  
  derived_condition:
    magnitude: "|Z1| · |Z4| = |Z2| · |Z3|"
    phase: "∠Z1 + ∠Z4 = ∠Z2 + ∠Z3"
    
  for_{{bridge_type}}:
    {% if type == 'wheatstone' %}
    balance_equation: "R1/R2 = R3/R4"
    unknown: "R4 = R3 · (R2/R1)"
    maxwell_reference: "Art. 343-348"
    
    {% elsif type == 'maxwell_bridge' %}
    balance_equation: "R1 · R4 = R2 · R3"
    inductance_balance: "L = R2 · R3 · C"
    unknown: "L_x = R2 · R3 · C1"
    maxwell_reference: "Art. 541-570"
    
    {% elsif type == 'hay_bridge' %}
    balance_equation: "Complex equation for high-Q coils"
    inductance: "L_x = R2 · R3 · C1 / (1 + ω²·R1²·C1²)"
    resistance: "R_x = ω²·R1·R2·R3·C1² / (1 + ω²·R1²·C1²)"
    
    {% elsif type == 'schering_bridge' %}
    balance_equation: "For capacitance measurement"
    capacitance: "C_x = C2 · (R4/R3)"
    loss_angle: "tan δ = ω · C4 · R4"
    
    {% elsif type == 'anderson_bridge' %}
    balance_equation: "For precise inductance measurement"
    inductance: "L_x = C · R2 · R3 · (1 + R4/R2)"
    {% endif %}
    
sensitivity_analysis:
  definition: "S = dθ/d(ΔZ/Z) (deflection per unit fractional change)"
  
  voltage_sensitivity:
    formula: "S_V = dV_out/d(ΔR/R)"
    at_balance: "{{value}} statvolt per unit change"
    
  current_sensitivity:
    formula: "S_I = dI_g/d(ΔR/R)"
    at_balance: "{{value}} statampere per unit change"
    
  bridge_current:
    formula: "I_g = V_s · (ΔR/R) / (total_resistance)"
    
  optimum_conditions:
    maximum_sensitivity: "When R1 = R2 = R3 = R4"
    practical_considerations: "{{notes}}"
    
measurement_procedure:
  steps:
    - "Initial setup: {{setup_instructions}}"
    - "Coarse balance: {{coarse_adjustment}}"
    - "Fine balance: {{fine_adjustment}}"
    - "Reading: {{reading_procedure}}"
    - "Verification: {{verification_steps}}"
    
  precautions:
    - "{{precaution_1}}"
    - "{{precaution_2}}"
    - "{{precaution_3}}"
    
error_analysis:
  systematic_errors:
    - source: "{{error_source}}"
      magnitude: {{magnitude}}
      correction: "{{correction_method}}"
      
  random_errors:
    - source: "{{error_source}}"
      standard_deviation: {{sigma}}
      
  total_uncertainty:
    combined: {{u_c}}
    expanded: {{U}} (k=2, 95% confidence)
    
applications:
  - "{{application_1}}"
  - "{{application_2}}"
  - "{{application_3}}"
  
maxwell_contributions:
  wheatstone_bridge_analysis: "Art. 343-348"
  resistance_measurement: "Art. 287-300"
  bridge_sensitivity: "Detailed analysis in Treatise"
```

## Bridge Types Reference

| Bridge Type | Measures | Balance Equation | Frequency Dependent |
|-------------|----------|------------------|---------------------|
| Wheatstone | Resistance | R1·R4 = R2·R3 | No |
| Kelvin (Double) | Low resistance | Ratio arms | No |
| Maxwell | Inductance | L = R2·R3·C | No |
| Hay | High-Q inductance | Complex | Yes |
| Schering | Capacitance | C_x = C2·(R4/R3) | No |
| Anderson | Inductance (precise) | Complex | No |
| Wien | Frequency | Complex | Yes |

## CGS Unit Reference

| Quantity | CGS Unit | Conversion |
|----------|----------|------------|
| Resistance | statohm | 1 statohm = 8.988×10¹¹ Ω |
| Capacitance | statfarad | 1 statfarad = 1.113×10⁻¹² F |
| Inductance | cm | 1 cm = 1.113×10⁻¹² H |
| Voltage | statvolt | 1 statvolt = 299.79 V |
| Current | statampere | 1 statampere = 3.336×10⁻¹⁰ A |

## Quality Criteria

- [ ] Bridge topology fully defined
- [ ] Balance condition derived
- [ ] Sensitivity analysis included
- [ ] Maxwell article citations present
- [ ] Measurement procedure documented

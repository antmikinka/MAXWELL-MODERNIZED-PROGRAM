# Template: transmission-line-template

## Purpose

Standardized template for transmission line analysis following Maxwell's electromagnetic theory and telegraph equation formulation.

## LLM Instructions

You are a transmission line specialist. Generate comprehensive transmission line documentation that connects Maxwell's electromagnetic theory (Part IV) with modern transmission line analysis.

1. **Establish Theoretical Foundation**: Link to Maxwell's equations, telegraph equation
2. **Define Line Parameters**: R, L, G, C per unit length
3. **Derive Transmission Line Equations**: Telegrapher's equations
4. **Analyze Wave Propagation**: Characteristic impedance, propagation constant
5. **Document Termination Effects**: Reflection, standing waves

## Template Structure

```yaml
transmission_line:
  name: "{{line_name}}"
  type: "{{coaxial | two_wire | stripline | microstrip | waveguide}}"
  maxwell_articles: ["Art. 604-619", "Art. 781-797", "Art. 287-300"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
line_geometry:
  {% if type == 'coaxial' %}
  coaxial:
    inner_radius: {{a}} cm
    outer_radius: {{b}} cm
    length: {{l}} cm
    dielectric: "{{dielectric_name}}"
    
  {% elsif type == 'two_wire' %}
  two_wire:
    wire_radius: {{a}} cm
    wire_separation: {{d}} cm
    length: {{l}} cm
    height_above_ground: {{h}} cm
    
  {% elsif type == 'stripline' %}
  stripline:
    trace_width: {{w}} cm
    substrate_height: {{h}} cm
    trace_thickness: {{t}} cm
    dielectric_constant: {{K}}
  {% endif %}
  
distributed_parameters:
  resistance: {{R}} statohm/cm
  inductance: {{L}} cm/cm (CGS) or stathenry/cm
  conductance: {{G}} s⁻¹/cm (CGS)
  capacitance: {{C}} statfarad/cm
  
  calculations:
    {% if type == 'coaxial' %}
    R: "R = 1/(2πσδ) · (1/a + 1/b) (skin effect)"
    L: "L = (μ/2π) · ln(b/a) (CGS: μ dimensionless)"
    C: "C = K/(2·ln(b/a)) (CGS)"
    G: "G = 4πσ/K (CGS, if lossy dielectric)"
    
    {% elsif type == 'two_wire' %}
    R: "R = 1/(πσδa) (skin effect)"
    L: "L = (μ/π) · arccosh(d/2a) (CGS)"
    C: "C = K/(2·arccosh(d/2a)) (CGS)"
    G: "G = 4πσ/K (CGS)"
    {% endif %}
    
telegrapher_equations:
  time_domain:
    - "∂V/∂z = -L · ∂I/∂t - R · I"
    - "∂I/∂z = -C · ∂V/∂t - G · V"
    
  frequency_domain (sinusoidal steady state):
    - "dV/dz = -(R + jωL) · I = -Z' · I"
    - "dI/dz = -(G + jωC) · V = -Y' · V"
    
  wave_equations:
    - "d²V/dz² = γ² · V"
    - "d²I/dz² = γ² · I"
    
  where:
    Z_prime: "Z' = R + jωL (series impedance per unit length)"
    Y_prime: "Y' = G + jωC (shunt admittance per unit length)"
    
propagation_constant:
  gamma: "γ = α + jβ = sqrt((R + jωL)(G + jωC))"
  
  attenuation_constant:
    alpha: "{{alpha}} Np/cm"
    formula: "α = Re{γ}"
    low_loss_approx: "α ≈ R/(2·Z0) + G·Z0/2"
    
  phase_constant:
    beta: "{{beta}} rad/cm"
    formula: "β = Im{γ}"
    lossless: "β = ω·sqrt(L·C)"
    
  wavelength:
    lambda: "λ = 2π/β cm"
    
  phase_velocity:
    v_p: "v_p = ω/β cm/s"
    lossless: "v_p = 1/sqrt(L·C)"
    
characteristic_impedance:
  Z0: "Z0 = sqrt((R + jωL)/(G + jωC))"
  
  lossless_case:
    Z0_ideal: "Z0 = sqrt(L/C)"
    value: "{{Z0}} statohm"
    
  low_loss_case:
    approximation: "Z0 ≈ sqrt(L/C) · [1 + j(R/ωL - G/ωC)/2]"
    
  for_{{type}}:
    {% if type == 'coaxial' %}
    Z0: "Z0 = (1/2π) · sqrt(μ/K) · ln(b/a) (CGS)"
    value: "{{Z0}} statohm"
    
    {% if type == 'two_wire' %}
    Z0: "Z0 = (1/π) · sqrt(μ/K) · arccosh(d/2a) (CGS)"
    {% endif %}
    {% endif %}
    
termination_analysis:
  load_impedance: {{Z_L}} statohm
  
  reflection_coefficient:
    Gamma: "Γ = (Z_L - Z0)/(Z_L + Z0)"
    magnitude: "|Γ| = {{gamma_mag}}"
    phase: "∠Γ = {{gamma_phase}}°"
    
  special_cases:
    matched: "Z_L = Z0 → Γ = 0 (no reflection)"
    open_circuit: "Z_L = ∞ → Γ = +1"
    short_circuit: "Z_L = 0 → Γ = -1"
    
  vswr:
    formula: "VSWR = (1 + |Γ|)/(1 - |Γ|)"
    value: {{vswr}}
    
input_impedance:
  general: "Z_in = Z0 · (Z_L + Z0·tanh(γl))/(Z0 + Z_L·tanh(γl))"
  
  lossless: "Z_in = Z0 · (Z_L + j·Z0·tan(βl))/(Z0 + j·Z_L·tan(βl))"
  
  special_lengths:
    quarter_wave: "l = λ/4 → Z_in = Z0²/Z_L (impedance inverter)"
    half_wave: "l = λ/2 → Z_in = Z_L (repeat)"
    
power_analysis:
  incident_power: {{P_inc}} erg/s
  reflected_power: {{P_ref}} erg/s
  delivered_power: {{P_del}} = {{P_inc}} - {{P_ref}}
  
  reflection_loss: "RL = -20·log|Γ| dB"
  transmission_efficiency: "η = P_del/P_inc × 100%"
  
maxwell_connection:
  electromagnetic_waves: "Art. 781-797"
  field_equations: "Art. 604-619"
  energy_transport: "Poynting vector analysis"
  speed_of_light: "c = 1/sqrt(με) (CGS)"
```

## CGS Unit Reference

| Quantity | CGS Unit | Conversion |
|----------|----------|------------|
| Resistance | statohm/cm | per unit length |
| Inductance | cm/cm | dimensionless (CGS) |
| Capacitance | statfarad/cm | per unit length |
| Voltage | statvolt | - |
| Current | statampere | - |
| Impedance | statohm | - |

## Quality Criteria

- [ ] Line geometry fully specified
- [ ] Distributed parameters calculated
- [ ] Telegrapher's equations documented
- [ ] Maxwell article citations included
- [ ] Termination effects analyzed

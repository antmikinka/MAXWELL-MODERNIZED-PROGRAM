# Template: telegraph-equation-template

## Purpose

Standardized template for telegraph equation analysis covering wave propagation on transmission lines following Maxwell's electromagnetic theory.

## LLM Instructions

You are a transmission line theory specialist. Generate comprehensive telegraph equation documentation that connects Maxwell's field equations with distributed circuit theory.

1. **Establish Theoretical Foundation**: Link to Maxwell's equations derivation
2. **Derive Telegraph Equation**: From distributed parameters
3. **Analyze Solutions**: Traveling waves, standing waves
4. **Document Boundary Conditions**: Source and load effects
5. **Include Applications**: Signal transmission, reflections

## Template Structure

```yaml
telegraph_equation:
  name: "{{analysis_name}}"
  maxwell_articles: ["Art. 604-619", "Art. 781-797"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
derivation_from_maxwell:
  starting_point: "Maxwell's equations in CGS"
  
  maxwell_equations:
    - "div(E) = 4πρ"
    - "div(B) = 0"
    - "curl(E) = -(1/c)·∂B/∂t"
    - "curl(B) = (4π/c)·J + (1/c)·∂E/∂t"
    
  transmission_line_approximation:
    - "TEM mode assumed (E ⊥ B ⊥ propagation direction)"
    - "Transverse field variations neglected"
    - "Longitudinal variation dominates"
    
  distributed_parameter_model:
    series_elements: "R·dz (resistance), L·dz (inductance)"
    shunt_elements: "G·dz (conductance), C·dz (capacitance)"
    
  from_field_to_circuit:
    V(z,t): "Line integral of E between conductors"
    I(z,t): "Line integral of H around conductor"
    R: "Conductor loss (skin effect)"
    L: "Magnetic flux linkage"
    G: "Dielectric loss"
    C: "Electric energy storage"
    
telegrapher_equations:
  time_domain_form:
    - "∂V/∂z = -L·∂I/∂t - R·I"
    - "∂I/∂z = -C·∂V/∂t - G·V"
    
  physical_interpretation:
    voltage_equation: "Voltage drop due to inductance and resistance"
    current_equation: "Current分流 due to capacitance and conductance"
    
  matrix_form:
    ∂/∂z [V] = -[0  L; C  0] · ∂/∂t [V] - [0  R; G  0] · [V]
    ∂/∂t [I]        [I]                    [I]
    
wave_equation:
  derivation:
    - "Differentiate voltage equation w.r.t. z"
    - "Differentiate current equation w.r.t. t"
    - "Eliminate mixed derivatives"
    
  second_order_form:
    - "∂²V/∂z² = LC·∂²V/∂t² + (RC + LG)·∂V/∂t + RG·V"
    - "∂²I/∂z² = LC·∂²I/∂t² + (RC + LG)·∂I/∂t + RG·I"
    
  lossless_case (R = 0, G = 0):
    - "∂²V/∂z² = LC·∂²V/∂t²"
    - "∂²I/∂z² = LC·∂²I/∂t²"
    wave_speed: "v = 1/√(LC)"
    
  lossy_case:
    damping_term: "(RC + LG)·∂V/∂t"
    attenuation: "RG·V term"
    
sinusoidal_steady_state:
  phasor_representation:
    V(z,t) = Re{V(z)·exp(jωt)}
    I(z,t) = Re{I(z)·exp(jωt)}
    
  frequency_domain_equations:
    - "dV/dz = -(R + jωL)·I = -Z'·I"
    - "dI/dz = -(G + jωC)·V = -Y'·V"
    
  propagation_constant:
    γ = α + jβ = √(Z'·Y') = √((R + jωL)(G + jωC))
    
  characteristic_impedance:
    Z0 = √(Z'/Y') = √((R + jωL)/(G + jωC))
    
general_solution:
  voltage:
    V(z) = V⁺·exp(-γz) + V⁻·exp(+γz)
    
  current:
    I(z) = (V⁺/Z0)·exp(-γz) - (V⁻/Z0)·exp(+γz)
    
  physical_interpretation:
    V⁺: "Forward-traveling wave amplitude"
    V⁻: "Backward-traveling (reflected) wave amplitude"
    exp(-γz): "Forward propagation with attenuation"
    exp(+γz): "Backward propagation with attenuation"
    
  time_domain_solution:
    V(z,t) = V⁺·exp(-αz)·cos(ωt - βz + φ⁺) 
           + V⁻·exp(+αz)·cos(ωt + βz + φ⁻)
    
boundary_conditions:
  source_end (z = 0):
    V(0) = V_s - I(0)·Z_s
    where:
      V_s: "Source voltage"
      Z_s: "Source impedance"
      
  load_end (z = l):
    V(l) = I(l)·Z_L
    where:
      Z_L: "Load impedance"
      
  reflection_coefficient:
    Γ_L = (Z_L - Z0)/(Z_L + Z0)
    Γ(z) = Γ_L·exp(-2γ(l-z))
    
special_cases:
  distortionless_line:
    condition: "R/L = G/C (Heaviside condition)"
    properties:
      - "α = √(RG) (frequency independent)"
      - "β = ω√(LC) (linear with frequency)"
      - "Z0 = √(L/C) (real, frequency independent)"
    maxwell_reference: "Art. 781-797"
    
  lossless_line:
    conditions: "R = 0, G = 0"
    properties:
      - "α = 0 (no attenuation)"
      - "β = ω√(LC)"
      - "Z0 = √(L/C) (real)"
      - "v = 1/√(LC)"
      
  low_loss_approximation:
    conditions: "R << ωL, G << ωC"
    alpha: "α ≈ R/(2Z0) + G·Z0/2"
    beta: "β ≈ ω√(LC)"
    Z0: "Z0 ≈ √(L/C)"
    
energy_and_power:
  poynting_vector:
    S = (c/4π) · (E × H) (CGS)
    
  power_flow:
    P(z) = (1/2)·Re{V(z)·I(z)*}
    
  for_lossless_line:
    P_forward: "P⁺ = |V⁺|²/(2Z0)"
    P_reflected: "P⁻ = |V⁻|²/(2Z0)"
    P_net: "P = P⁺ - P⁻"
    
  energy_storage:
    electric: "W_E = (1/4)·C·|V|² per unit length"
    magnetic: "W_M = (1/4)·L·|I|² per unit length"
    
dispersion_analysis:
  phase_velocity:
    v_p = ω/β
    
  group_velocity:
    v_g = dω/dβ
    
  dispersion_relation:
    β(ω) = Im{√((R + jωL)(G + jωC))}
    
  distortion_mechanisms:
    - "Frequency-dependent attenuation (amplitude distortion)"
    - "Nonlinear β(ω) (phase/frequency distortion)"
    
maxwell_connection:
  electromagnetic_wave_theory: "Art. 781-797"
  field_equations: "Art. 604-619"
  speed_of_light: "c = 1/√(με) (CGS)"
  energy_transport: "Poynting theorem"
```

## CGS Unit Reference

| Quantity | CGS Unit | Notes |
|----------|----------|-------|
| R (resistance/length) | statohm/cm | - |
| L (inductance/length) | cm/cm | dimensionless |
| G (conductance/length) | s⁻¹/cm | - |
| C (capacitance/length) | statfarad/cm | - |
| γ (propagation) | cm⁻¹ | - |
| Z0 (impedance) | statohm | - |

## Quality Criteria

- [ ] Derivation from Maxwell's equations complete
- [ ] Telegraph equations properly formulated
- [ ] Solutions documented for all cases
- [ ] Maxwell article citations included
- [ ] Energy/power analysis included

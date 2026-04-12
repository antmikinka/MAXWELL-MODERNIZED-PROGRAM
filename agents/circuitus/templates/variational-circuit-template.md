# Template: variational-circuit-template

## Purpose

Standardized template for variational methods in circuit analysis including energy methods, least action principles, and Lagrangian/Hamiltonian formulations.

## LLM Instructions

You are a variational methods specialist. Generate comprehensive documentation for variational circuit analysis following Maxwell's energy methods and modern variational principles.

1. **Establish Theoretical Foundation**: Link to Maxwell's energy analysis, variational principles
2. **Define Energy Functions**: Magnetic coenergy, electric energy
3. **Formulate Lagrangian**: T - V for circuits
4. **Derive Equations**: Euler-Lagrange equations
5. **Apply to Problems**: Coupled circuits, electromechanical systems

## Template Structure

```yaml
variational_analysis:
  name: "{{analysis_name}}"
  maxwell_articles: ["Art. 541-570", "Art. 424-440", "Art. 287-300"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
energy_formulations:
  electric_energy:
    formula: "W_E = (1/2)·∫ E·D dV = (1/2)·∑ C_ij·V_i·V_j"
    cgs_form: "W_E = (1/8π)·∫ K·E² dV (CGS)"
    circuit_form: "W_E = (1/2)·C·V² = (1/2)·Q²/C"
    maxwell_reference: "Art. 56-57, 75-76"
    
  magnetic_energy:
    formula: "W_M = (1/2)·∫ H·B dV = (1/2)·∑ L_ij·I_i·I_j"
    cgs_form: "W_M = (1/8π)·∫ μ·H² dV (CGS)"
    circuit_form: "W_M = (1/2)·L·I² = (1/2)·Φ·I"
    maxwell_reference: "Art. 424-430, 541-570"
    
  coenergy:
    definition: "W'_M = ∑ Φ_i·I_i - W_M"
    for_linear: "W'_M = W_M (linear systems)"
    application: "Force/torque calculation"
    
lagrangian_formulation:
  lagrangian:
    L = T - V
    
  where:
    T: "Kinetic coenergy (magnetic): T = (1/2)·∑ L_ij·q̇_i·q̇_j"
    V: "Potential energy (electric): V = (1/2)·∑ (1/C_ij)·q_i·q_j"
    q: "Charge (generalized coordinate)"
    q̇: "Current (generalized velocity)"
    
  euler_lagrange_equations:
    d/dt(∂L/∂q̇_i) - ∂L/∂q_i = Q_i (non-conservative forces)
    
  for_RLC_circuit:
    L = (1/2)·L·q̇² - (1/2C)·q²
    d/dt(L·q̇) + q/C = -R·q̇ (with dissipation)
    L·q̈ + R·q̇ + q/C = 0
    
  with_sources:
    voltage_source: "Add V_s·q to Lagrangian"
    current_source: "Use constrained formulation"
    
hamiltonian_formulation:
  legendre_transform:
    H = ∑ p_i·q̇_i - L
    
  canonical_momentum:
    p = ∂L/∂q̇ = L·q̇ = Φ (flux linkage)
    
  hamiltonian:
    H = p²/(2L) + q²/(2C) (for LC circuit)
    
  hamilton_equations:
    q̇ = ∂H/∂p = p/L
    ṗ = -∂H/∂q = -q/C
    
  physical_interpretation:
    H: "Total energy = H = W_M + W_E"
    
coupled_circuits:
  mutual_inductance:
    M = k·√(L₁·L₂)
    where: "0 ≤ k ≤ 1 (coupling coefficient)"
    
  lagrangian:
    L = (1/2)·L₁·q̇₁² + (1/2)·L₂·q̇₂² + M·q̇₁·q̇₂ 
      - (1/2C₁)·q₁² - (1/2C₂)·q₂²
      
  equations_of_motion:
    L₁·q̈₁ + M·q̈₂ + R₁·q̇₁ + q₁/C₁ = V₁
    M·q̈₁ + L₂·q̈₂ + R₂·q̇₂ + q₂/C₂ = V₂
    
  energy_exchange:
    beat_frequency: "ω_beat = |ω₁ - ω₂|"
    energy_transfer: "Complete transfer when k is optimal"
    
electromechanical_systems:
  mechanical_coordinates:
    Add mechanical degrees of freedom: x, θ, etc.
    
  mechanical_energy:
    T_mech: "(1/2)·m·ẋ² or (1/2)·J·θ̇²"
    V_mech: "(1/2)·k·x² or m·g·h"
    
  coupling:
    magnetic_force: "F = ∂W'_M/∂x (at constant current)"
    torque: "τ = ∂W'_M/∂θ (at constant current)"
    
  example_electromagnet:
    L(x): "Inductance as function of gap"
    F = (1/2)·I²·dL/dx
    maxwell_reference: "Art. 424-440"
    
dissipation:
  rayleigh_dissipation_function:
    F = (1/2)·∑ R_i·q̇_i²
    
  modified_euler_lagrange:
    d/dt(∂L/∂q̇_i) - ∂L/∂q_i + ∂F/∂q̇_i = Q_i
    
  power_dissipation:
    P_diss = 2·F = ∑ R_i·I_i²
    
variational_principles:
  least_action:
    δ∫ L dt = 0 (for conservative systems)
    
  minimum_heat:
    "Currents distribute to minimize I²R loss"
    maxwell_reference: "Art. 287-300"
    
  minimum_energy:
    "System settles to minimum energy state"
    
numerical_implementation:
  finite_element:
    - "Discretize energy functional"
    - "Minimize w.r.t. nodal variables"
    - "Obtain matrix equations"
    
  time_integration:
    - "Symplectic integrators (energy preserving)"
    - "Newmark-beta, Runge-Kutta"
    
applications:
  - "{{application_1}}"
  - "{{application_2}}"
  - "{{application_3}}"
  
maxwell_contributions:
  energy_methods: "Art. 424-430, 541-570"
  mutual_inductance: "Art. 541-570"
  electromagnetic_forces: "Art. 424-440"
  variational_thinking: "Precursor to modern methods"
```

## CGS Unit Reference

| Quantity | CGS Unit | Conversion |
|----------|----------|------------|
| Energy | erg | 1 erg = 10⁻⁷ J |
| Inductance | cm | 1 cm = 1.113×10⁻¹² H |
| Capacitance | statfarad | 1 statfarad = 1.113×10⁻¹² F |
| Charge | statcoulomb | 1 statcoulomb = 3.336×10⁻¹⁰ C |
| Current | statampere | 1 statampere = 3.336×10⁻¹⁰ A |
| Flux | maxwell | 1 maxwell = 10⁻⁸ Wb |

## Quality Criteria

- [ ] Energy functions properly defined
- [ ] Lagrangian formulation complete
- [ ] Euler-Lagrange equations derived
- [ ] Maxwell article citations included
- [ ] Applications documented

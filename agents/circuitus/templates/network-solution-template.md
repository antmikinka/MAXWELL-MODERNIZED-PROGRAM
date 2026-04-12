# Template: network-solution-template

## Purpose

Standardized template for network solution documentation including nodal, mesh, and state-space methods.

## LLM Instructions

You are a network analysis specialist. Generate comprehensive network solution documentation following Maxwell's conduction theory and modern network analysis methods.

1. **Establish Theoretical Foundation**: Link to Maxwell's Articles 287-320 (networks, conduction)
2. **Define Network Structure**: Graph representation, incidence matrices
3. **Select Solution Method**: Nodal, mesh, or state-space
4. **Document Matrix Formulation**: Systematic equation setup
5. **Verify Solution**: Conservation laws, boundary conditions

## Template Structure

```yaml
network_solution:
  name: "{{network_name}}"
  maxwell_articles: ["Art. 287-300", "Art. 301-320"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
network_graph:
  representation: "{{directed | undirected}}"
  num_nodes: {{n}}
  num_branches: {{b}}
  
  incidence_matrix:
    description: "A: branch-node incidence matrix"
    size: {{b × n}}
    rank: {{n-1}} (for connected graph)
    
  loop_matrix:
    description: "B: fundamental loop matrix"
    size: {{l × b}}
    where_l: {{l = b - n + 1}}
    
  cutset_matrix:
    description: "Q: fundamental cutset matrix"
    size: {{(n-1) × b}}
    
branch_constitutive_relations:
  general_form: "V_b = Z_b · I_b + V_s  (impedance form)"
  or: "I_b = Y_b · V_b + I_s  (admittance form)"
  
  branch_types:
    - type: "Resistor"
      impedance: "Z = R"
      admittance: "Y = 1/R = G"
      maxwell_reference: "Art. 287-300"
      
    - type: "Inductor"
      impedance: "Z = L·s (Laplace)"
      admittance: "Y = 1/(L·s)"
      maxwell_reference: "Art. 541-570"
      
    - type: "Capacitor"
      impedance: "Z = 1/(C·s)"
      admittance: "Y = C·s"
      maxwell_reference: "Art. 75-76"
      
    - type: "Voltage source"
      relation: "V = V_s (known)"
      maxwell_reference: "Art. 230-235"
      
    - type: "Current source"
      relation: "I = I_s (known)"
      maxwell_reference: "Art. 230-235"
      
nodal_analysis:
  formulation: "Y_n · V_n = I_n"
  
  where:
    Y_n: "A · Y_b · A^T  (nodal admittance matrix)"
    V_n: "Node voltage vector (n-1 unknowns)"
    I_n: "Nodal current source vector"
    
  solution_steps:
    - "Form branch admittance matrix Y_b"
    - "Construct incidence matrix A"
    - "Compute Y_n = A · Y_b · A^T"
    - "Solve Y_n · V_n = I_n"
    - "Compute branch voltages: V_b = A^T · V_n"
    - "Compute branch currents: I_b = Y_b · V_b"
    
  matrix_properties:
    symmetric: "{{yes | no}}"
    positive_definite: "{{yes | no}}"
    sparse: "{{yes | no}}"
    size: {{(n-1) × (n-1)}}
    
mesh_analysis:
  formulation: "Z_m · I_m = V_m"
  
  where:
    Z_m: "B · Z_b · B^T  (mesh impedance matrix)"
    I_m: "Mesh current vector (l unknowns)"
    V_m: "Mesh voltage source vector"
    
  solution_steps:
    - "Form branch impedance matrix Z_b"
    - "Construct loop matrix B"
    - "Compute Z_m = B · Z_b · B^T"
    - "Solve Z_m · I_m = V_m"
    - "Compute branch currents: I_b = B^T · I_m"
    - "Compute branch voltages: V_b = Z_b · I_b"
    
modified_nodal_analysis:
  formulation: "Extended system for voltage sources"
  
  augmented_matrix:
    | Y_n    B_v |   | V_n  |   | I_n  |
    |            | · |      | = |      |
    | C_v    D_v |   | I_v  |   | E_v  |
    
  where:
    I_v: "Current through voltage sources"
    B_v, C_v, D_v: "Constraint matrices"
    E_v: "Voltage source values"
    
state_space_formulation:
  state_variables: [{{state_variable_list}}]
  
  state_equations:
    dx/dt = A·x + B·u  (state equation)
    y = C·x + D·u      (output equation)
    
  where:
    x: "State vector (inductor currents, capacitor voltages)"
    u: "Input vector (sources)"
    y: "Output vector (quantities of interest)"
    
  system_matrices:
    A: {{n_states × n_states}} "System matrix"
    B: {{n_states × n_inputs}} "Input matrix"
    C: {{n_outputs × n_states}} "Output matrix"
    D: {{n_outputs × n_inputs}} "Feedthrough matrix"
    
numerical_solution:
  solver: "{{direct | iterative}}"
  
  direct_methods:
    - "{{Gaussian elimination}}"
    - "{{LU decomposition}}"
    - "{{Cholesky (if symmetric positive definite)}}"
    
  iterative_methods:
    - "{{Jacobi}}"
    - "{{Gauss-Seidel}}"
    - "{{Conjugate Gradient}}"
    - "{{GMRES}}"
    
  convergence_criteria:
    tolerance: {{tol}}
    max_iterations: {{max_iter}}
    
results:
  node_voltages:
    {{node_voltage_results}}
    
  branch_currents:
    {{branch_current_results}}
    
  power_dissipation:
    {{power_results}}
    
verification:
  tellegens_theorem: "{{verified | not_verified}}"
  reciprocity: "{{verified | not_verified}}"
  energy_conservation: "{{verified | not_verified}}"
```

## CGS Unit Reference

| Quantity | CGS Unit | Notes |
|----------|----------|-------|
| Voltage | statvolt | Electric potential |
| Current | statampere | Charge flow rate |
| Resistance | statohm | V/I ratio |
| Admittance | s⁻¹ | 1/statohm |
| Impedance | statohm | Complex resistance |

## Quality Criteria

- [ ] Graph representation complete
- [ ] Matrix formulations documented
- [ ] Maxwell article citations included
- [ ] Solution verification performed
- [ ] CGS units used throughout

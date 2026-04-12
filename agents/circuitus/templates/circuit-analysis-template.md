# Template: circuit-analysis-template

## Purpose

Standardized template for circuit analysis documentation following Maxwell's electrokinematics framework.

## LLM Instructions

You are a circuit analysis specialist. Generate comprehensive circuit documentation that connects Maxwell's electrokinematic theory (Part II) with modern circuit analysis methods.

1. **Establish Theoretical Foundation**: Link to Maxwell's Articles 230-300 (currents, conduction)
2. **Define Circuit Topology**: Nodes, branches, loops, reference directions
3. **Specify Governing Equations**: KCL, KVL, component relations
4. **Document Solution Method**: Nodal, mesh, or modified analysis
5. **Include Maxwell References**: Cite relevant treatise articles

## Template Structure

```yaml
circuit_analysis:
  name: "{{circuit_name}}"
  maxwell_articles: ["Art. 230-235", "Art. 287-300", "Art. 301-320"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
circuit_topology:
  num_nodes: {{n}}
  num_branches: {{b}}
  num_independent_loops: {{l}}  # l = b - n + 1
  
  nodes:
    - name: "{{node_name}}"
      type: "{{essential | reference | interior}}"
      voltage: {{V}} (if known)
      
  branches:
    - branch_id: "{{branch_id}}"
      from_node: {{node_a}}
      to_node: {{node_b}}
      element_type: "{{R | L | C | V_source | I_source}}"
      value: {{value}}
      unit: "{{ohm | henry | farad | statvolt | statampere}}"
      
  loops:
    - loop_id: "{{loop_id}}"
      branches: [{{branch_ids}}]
      direction: "{{cw | ccw}}"
      
governing_equations:
  kcl:
    formulation: "{{node_voltage | modified}}"
    equations:
      - node: "{{node_name}}"
        equation: "{{sum_of_currents = 0}}"
        
  kvl:
    formulation: "{{mesh_current | loop}}"
    equations:
      - loop: "{{loop_id}}"
        equation: "{{sum_of_voltages = 0}}"
        
  component_relations:
    - element: "Resistor"
      relation: "V = I·R (CGS: statvolt = statampere × statohm)"
      maxwell_reference: "Art. 287-300"
      
    - element: "Inductor"
      relation: "V = L·dI/dt"
      maxwell_reference: "Art. 541-570"
      
    - element: "Capacitor"
      relation: "I = C·dV/dt"
      maxwell_reference: "Art. 75-76"
      
solution_method:
  method: "{{nodal_analysis | mesh_analysis | modified_nodal | state_space}}"
  
  nodal_analysis:
    {% if method == 'nodal_analysis' %}
    unknowns: "Node voltages (except reference)"
    matrix_form: "Y·V = I"
    admittance_matrix:
      size: {{(n-1) × (n-1)}}
      sparse: "{{yes | no}}"
    solution: "{{direct | iterative}}"
    {% endif %}
    
  mesh_analysis:
    {% if method == 'mesh_analysis' %}
    unknowns: "Mesh currents"
    matrix_form: "Z·I = V"
    impedance_matrix:
      size: {{l × l}}
    solution: "{{direct | iterative}}"
    {% endif %}
    
results:
  node_voltages:
    {% for node in nodes %}
    - {{node.name}}: {{V_node}} statvolt
    {% endfor %}
    
  branch_currents:
    {% for branch in branches %}
    - {{branch.branch_id}}: {{I_branch}} statampere
    {% endfor %}
    
  power:
    total_supplied: {{P_supplied}} erg/s
    total_dissipated: {{P_dissipated}} erg/s
    balance_check: "{{balanced | unbalanced}}"
    
verification:
  kcl_verified: "{{yes | no}}"
  kvl_verified: "{{yes | no}}"
  power_balance: "{{yes | no}}"
  maxwell_consistency: "{{yes | no}}"
```

## Variables

| Variable | Description | Type | Required |
|----------|-------------|------|----------|
| circuit_name | Circuit identifier | string | Yes |
| n | Number of nodes | integer | Yes |
| b | Number of branches | integer | Yes |
| method | Analysis method | enum | Yes |

## CGS Unit Reference

| Quantity | CGS Unit | Conversion |
|----------|----------|------------|
| Voltage | statvolt | 1 statvolt = 299.79 V |
| Current | statampere | 1 statampere = 3.336×10⁻¹⁰ A |
| Resistance | statohm | 1 statohm = 8.988×10¹¹ Ω |
| Capacitance | statfarad | 1 statfarad = 1.113×10⁻¹² F |
| Inductance | cm (CGS) | 1 cm = 1.113×10⁻¹² H |
| Power | erg/s | 1 erg/s = 10⁻⁷ W |

## Usage Example

```yaml
circuit_analysis:
  name: "Wheatstone Bridge"
  maxwell_articles: ["Art. 287-300", "Art. 343-348"]
  theory_classification: "standard_math"
  
circuit_topology:
  num_nodes: 4
  num_branches: 6
  num_independent_loops: 3
  
  branches:
    - branch_id: "R1"
      from_node: "A"
      to_node: "B"
      element_type: "R"
      value: 1000
      unit: "statohm"
```

## Output Format

- YAML frontmatter with metadata
- Structured circuit topology
- Governing equations with Maxwell citations
- Solution results

## Quality Criteria

- [ ] All values have CGS units
- [ ] Maxwell article citations included
- [ ] KCL/KVL verification documented
- [ ] Power balance checked
- [ ] Solution method documented

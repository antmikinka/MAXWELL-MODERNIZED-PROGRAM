# Template: effective-medium-template

## Purpose

Standardized template for computing effective properties of composite materials using Maxwell's mixing formulas and effective medium theories.

## LLM Instructions

You are a composite materials specialist. Generate comprehensive effective medium documentation that connects Maxwell's mixing theory with modern homogenization methods.

1. **Establish Theoretical Foundation**: Link to Maxwell's treatment of heterogeneous media
2. **Define Composite Structure**: Phases, volume fractions, inclusion geometry
3. **Select Effective Medium Model**: Maxwell-Garnett, Bruggeman, or other
4. **Compute Effective Properties**: Permittivity, permeability, conductivity
5. **Validate Model**: Compare predictions with measurements or bounds

## Template Structure

```yaml
effective_medium:
  name: "{{composite_name}}_effective_properties"
  composite_type: "{{particulate | layered | fibrous | foam | random}}"
  maxwell_articles: ["{{relevant_articles}}"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
constituent_phases:
  matrix:
    name: "{{matrix_material}}"
    volume_fraction: {{f_m}} (must sum to 1 with inclusions)
    
    properties:
      permittivity: {{K_m}} (dimensionless, CGS)
      permeability: {{mu_m}} (dimensionless, CGS)
      conductivity: {{sigma_m}} s⁻¹ (CGS)
      
  inclusions:
    {% for inclusion in inclusions %}
    - phase_{{loop.index}}:
        name: "{{inclusion_name}}"
        volume_fraction: {{f_i}}
        geometry: "{{sphere | ellipsoid | fiber | platelet}}"
        
        properties:
          permittivity: {{K_i}}
          permeability: {{mu_i}}
          conductivity: {{sigma_i}}
          
        aspect_ratio: {{a/b}} (for non-spherical)
        orientation: "{{random | aligned | {{direction_vector}}}}"
    {% endfor %}
    
effective_medium_model:
  model: "{{Maxwell-Garnett | Bruggeman | Wiener | Hashin-Shtrikman | Differential}}"
  
  maxwell_garnett:
    {% if model == 'Maxwell-Garnett' %}
    applicability: "Dilute inclusions (f < 0.2)"
    formula: "K_eff = K_m · [(K_i + 2K_m + 2f(K_i - K_m)) / (K_i + 2K_m - f(K_i - K_m))]"
    maxwell_reference: "Maxwell's Treatise, Vol. I, Art. 314"
    
    effective_permittivity: {{K_eff}}
    effective_permeability: {{mu_eff}}
    effective_conductivity: {{sigma_eff}}
    
    validity_check:
      dilute_limit: {{f}} < 0.2 ? "{{valid | marginal | invalid}}"
      percolation: "{{not_applicable | approaching | exceeded}}"
    {% endif %}
    
  bruggeman:
    {% if model == 'Bruggeman' %}
    applicability: "Higher volume fractions, symmetric treatment"
    formula: "f₁·(K₁-K_eff)/(K₁+2K_eff) + f₂·(K₂-K_eff)/(K₂+2K_eff) = 0"
    self_consistent: true
    
    effective_permittivity: {{K_eff}}
    effective_permeability: {{mu_eff}}
    effective_conductivity: {{sigma_eff}}
    
    percolation_threshold: {{f_c}} (theoretical)
    {% endif %}
    
  bounds:
    wiener_bounds:
      upper: {{K_upper}} (parallel/Voigt)
      lower: {{K_lower}} (series/Reuss)
      
    hashin_shtrikman_bounds:
      {% if K_i > K_m %}
      upper: {{K_HS_plus}}
      lower: {{K_HS_minus}}
      {% else %}
      upper: {{K_HS_minus}}
      lower: {{K_HS_plus}}
      {% endif %}
      
    computed_value_within_bounds: "{{yes | no}}"
    
microstructure_effects:
  interfacial_layer:
    present: "{{yes | no}}"
    {% if present %}
    thickness: {{t}} cm
    properties: {{interfacial_properties}}
    maxwell_wagner: "{{applicable | not_applicable}}"
    {% endif %}
    
  size_effects:
    characteristic_size: {{d}} cm
    mean_free_path: {{lambda}} cm
    knudsen_number: {{Kn}} = {{lambda}} / {{d}}
    size_dependent: "{{yes | no}}"
    
  clustering:
    present: "{{yes | no}}"
    correlation_length: {{xi}} cm
    structure_factor: {{S_0}}
    
frequency_dependence:
  {% if frequency_dependent %}
  frequency_range: {{f_min}} - {{f_max}} Hz
  
  dispersion_model: "{{Debye | Lorentz | Drude | Jonscher}}"
  
  effective_complex_permittivity:
    K_eff_prime: {{K_eff_prime(f)}}
    K_eff_double_prime: {{K_eff_double_prime(f)}}
    
  effective_complex_permeability:
    mu_eff_prime: {{mu_eff_prime(f)}}
    mu_eff_double_prime: {{mu_eff_double_prime(f)}}
  {% endif %}
  
anisotropy:
  {% if is_anisotropic %}
  symmetry: "{{uniaxial | biaxial | orthorhombic}}"
  
  effective_tensor:
    K_xx: {{K_xx}}
    K_yy: {{K_yy}}
    K_zz: {{K_zz}}
    
  principal_axes: "{{directions}}"
  {% else %}
  isotropic: true
  {% endif %}
  
validation:
  experimental_data: "{{data_source}}"
  numerical_simulation: "{{simulation_reference}}"
  
  comparison:
    model_prediction: {{K_eff_model}}
    experimental_value: {{K_eff_exp}}
    relative_error: {{error}} %
    
  bounds_check:
    within_wiener_bounds: "{{yes | no}}"
    within_HS_bounds: "{{yes | no}}"
    
application_notes:
  - "{{note_1}}"
  - "{{note_2}}"
  - "{{note_3}}"
```

## Variables

| Variable | Description | Type | Required |
|----------|-------------|------|----------|
| composite_name | Composite identifier | string | Yes |
| composite_type | Morphology class | enum | Yes |
| f_m | Matrix volume fraction | number | Yes |
| f_i | Inclusion volume fraction | number | Yes |
| model | Effective medium model | enum | Yes |
| K_m, K_i | Phase permittivities | numbers | Yes |

## CGS Unit Reference

| Quantity | CGS Unit | Notes |
|----------|----------|-------|
| Permittivity | dimensionless | K (relative) |
| Permeability | dimensionless | mu (relative) |
| Conductivity | s⁻¹ | CGS electrostatic |
| Length | cm | All dimensions |

## Usage Example

```yaml
effective_medium:
  name: "Silver_Epoxy_Composite"
  composite_type: "particulate"
  maxwell_articles: ["Art. 314"]
  theory_classification: "standard_math"
  
constituent_phases:
  matrix:
    name: "Epoxy"
    volume_fraction: 0.7
    
    properties:
      permittivity: 3.5
      permeability: 1.0
      conductivity: 10⁻¹⁵ s⁻¹
      
  inclusions:
    - phase_1:
        name: "Silver particles"
        volume_fraction: 0.3
        geometry: "sphere"
        
        properties:
          permittivity: 1000 (effective, frequency-dependent)
          permeability: 1.0
          conductivity: 6.3×10¹⁷ s⁻¹
          
effective_medium_model:
  model: "Maxwell-Garnett"
  
  maxwell_garnett:
    applicability: "Dilute inclusions (f < 0.2)"
    effective_permittivity: 5.2
    effective_conductivity: 1.9×10¹⁷ s⁻¹
```

## Output Format

- YAML frontmatter with metadata
- Structured phase properties
- Effective medium calculation results
- Validation against bounds/data

## Quality Criteria

- [ ] Volume fractions sum to 1
- [ ] All properties have CGS units
- [ ] Model applicability checked
- [ ] Bounds computed and verified
- [ ] Maxwell article citations included

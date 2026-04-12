# Template: hysteresis-model-template

## Purpose

Standardized template for magnetic hysteresis modeling and documentation following Maxwell's magnetism theory and Weber's molecular hypothesis.

## LLM Instructions

You are a magnetic materials modeling specialist. Generate comprehensive hysteresis documentation that connects Maxwell's magnetic theory (Part III) with modern computational hysteresis models.

1. **Establish Theoretical Foundation**: Link to Maxwell's Articles 424-448 (magnetization), Weber's theory (Art. 444-447)
2. **Define Hysteresis Parameters**: Coercivity, remanence, saturation, loop shape
3. **Select Hysteresis Model**: Preisach, Jiles-Atherton, or phenomenological
4. **Document Energy Loss**: Hysteresis loss per cycle, Steinmetz equation
5. **Validate Against Data**: Compare model predictions with measurements

## Template Structure

```yaml
hysteresis_model:
  name: "{{model_name}}"
  material: "{{material_name}}"
  maxwell_articles: ["Art. 424-448", "Art. 444-447 (Weber)"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
magnetic_properties:
  saturation_magnetization: {{I_s}} emu/cm³
  remanence: {{B_r}} gauss
  coercivity: {{H_c}} oersted
  initial_permeability: {{mu_i}}
  maximum_permeability: {{mu_max}}
  squareness_ratio: {{M_r}}/{{M_s}}
  
hysteresis_model_type:
  model: "{{Preisach | Jiles-Atherton | Stoner-Wohlfarth | Phenomenological}}"
  
  preisach_parameters:
    {% if model == 'Preisach' %}
    distribution_type: "{{gaussian | lorentzian | measured}}"
    mean_coercivity: {{H_c_mean}} oersted
    std_coercivity: {{sigma_Hc}} oersted
    mean_interaction: {{H_int_mean}} oersted
    std_interaction: {{sigma_Hint}} oersted
    irreversible_fraction: {{f_irrev}}
    {% endif %}
    
  jiles_atherton_parameters:
    {% if model == 'Jiles-Atherton' %}
    saturation_magnetization: {{M_s}} emu/cm³
    domain_coupling: {{alpha}} (dimensionless)
    domain_wall_energy: {{a}} oersted
    pinning_parameter: {{k}} oersted
    reversible_fraction: {{c}} (0-1)
    {% endif %}
    
maxwell_weber_connection:
  molecular_hypothesis:
    maxwell_article: "Art. 444-447"
    weber_theory: "Molecular magnets with friction"
    modern_interpretation: "Domain wall pinning"
    
  hysteresis_loss:
    steinmetz_equation: "W = eta · B_max^n · f"
    steinmetz_exponent: {{n}} (typically 1.6-2.0)
    loss_coefficient: {{eta}} erg/cm³·cycle
    maxwell_reference: "Art. 424-430"
    
loop_characteristics:
  major_loop:
    saturation_field: {{H_sat}} oersted
    remanent_field: {{B_r}} gauss
    coercive_field: {{H_c}} oersted
    loop_area: {{area}} erg/cm³
    
  minor_loops:
    num_loops: {{num_minor}}
    field_amplitudes: [{{H_amp_values}}]
    recoil_curves: "{{documented | calculated}}"
    
anhysteretic_curve:
  model: "{{Langevin | Hyperbolic | Modified}}"
  parameters:
    {{anhysteretic_parameters}}
  maxwell_reference: "Art. 429-432"
    
energy_considerations:
  hysteresis_loss_per_cycle: {{W_h}} erg/cm³
  eddy_current_loss: {{W_e}} erg/cm³ (if applicable)
  anomalous_loss: {{W_a}} erg/cm³ (if applicable)
  total_loss: {{W_total}} = {{W_h}} + {{W_e}} + {{W_a}}
  
  maxwell_energy_relation:
    energy_density: "W = (1/4pi) integral H·dB"
    maxwell_article: "Art. 424-426"
    
numerical_implementation:
  integration_method: "{{Runge-Kutta | Euler | Adaptive}}"
  field_step: {{dH}} oersted
  convergence_tolerance: {{tol}}
  rate_dependence: "{{included | excluded}}"
  
validation:
  experimental_data: "{{data_source}}"
  fit_quality:
    r_squared: {{R²}}
    rmse: {{RMSE}}
    max_error: {{max_err}} gauss
  residual_plot: "{{plot_reference}}"
```

## Variables

| Variable | Description | Type | Required |
|----------|-------------|------|----------|
| model_name | Model identifier | string | Yes |
| material_name | Magnetic material | string | Yes |
| B_r | Remanence | number | Yes |
| H_c | Coercivity | number | Yes |
| M_s | Saturation magnetization | number | Yes |
| model | Hysteresis model type | enum | Yes |

## CGS Unit Reference

| Quantity | CGS Unit | Conversion |
|----------|----------|------------|
| Magnetic field H | oersted | 1 oersted = 79.577 A/m |
| Magnetic induction B | gauss | 1 gauss = 10⁻⁴ T |
| Magnetization I | emu/cm³ | 1 emu/cm³ = 1000 A/m |
| Energy density | erg/cm³ | 1 erg/cm³ = 0.1 J/m³ |
| Permeability | dimensionless | mu = B/H (CGS) |

## Usage Example

```yaml
hysteresis_model:
  name: "Soft Iron Hysteresis"
  material: "Armco Iron"
  maxwell_articles: ["Art. 424-448", "Art. 444-447"]
  theory_classification: "standard_math"
  
magnetic_properties:
  saturation_magnetization: 1714 emu/cm³
  remanence: 8500 gauss
  coercivity: 0.5 oersted
  initial_permeability: 1500
  maximum_permeability: 5000
  
hysteresis_model_type:
  model: "Jiles-Atherton"
  
  jiles_atherton_parameters:
    saturation_magnetization: 1714 emu/cm³
    domain_coupling: 0.0001
    domain_wall_energy: 300 oersted
    pinning_parameter: 45 oersted
    reversible_fraction: 0.3
    
maxwell_weber_connection:
  molecular_hypothesis:
    maxwell_article: "Art. 444-447"
    weber_theory: "Molecular magnets with friction"
    modern_interpretation: "Domain wall pinning"
```

## Output Format

- YAML frontmatter with metadata
- Structured hysteresis parameters
- Maxwell article cross-references
- Model validation results

## Quality Criteria

- [ ] All parameters have CGS units
- [ ] Maxwell article citations included
- [ ] Weber's molecular hypothesis referenced
- [ ] Hysteresis loss documented
- [ ] Validation against data included

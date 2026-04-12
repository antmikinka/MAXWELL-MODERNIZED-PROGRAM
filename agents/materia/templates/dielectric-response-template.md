# Template: dielectric-response-template

## Purpose

Standardized template for dielectric response modeling and documentation following Maxwell's electrostatic theory and dielectric absorption analysis.

## LLM Instructions

You are a dielectric materials specialist. Generate comprehensive dielectric response documentation that connects Maxwell's electrostatic theory (Part I) with modern dielectric spectroscopy methods.

1. **Establish Theoretical Foundation**: Link to Maxwell's Articles 50-62 (dielectrics), 103-111 (dielectric absorption)
2. **Define Dielectric Properties**: Permittivity, loss tangent, breakdown strength
3. **Characterize Frequency Response**: Complex permittivity, relaxation times
4. **Document Absorption Effects**: Maxwell-Wagner polarization, interfacial effects
5. **Specify Breakdown Criteria**: Dielectric strength, safety margins

## Template Structure

```yaml
dielectric_response:
  name: "{{material_name}}_dielectric_characterization"
  material: "{{material_name}}"
  maxwell_articles: ["Art. 50-62", "Art. 79-83", "Art. 103-111"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
constitutive_relation:
  form: "D = K·E = E + 4*pi*P (CGS)"
  maxwell_reference: "Art. 60-62"
  dielectric_constant: {{K}} (dimensionless)
  electric_susceptibility: {{chi}} = (K - 1) / 4*pi
  
static_properties:
  dielectric_constant: {{K_s}} (static, dimensionless)
  refractive_index: {{n}} (optical, dimensionless)
  maxwell_relation: "K = n² (Art. 79-83)"
  breakdown_strength: {{E_bd}} statvolt/cm
  volume_resistivity: {{rho_v}} statohm·cm
  surface_resistivity: {{rho_s}} statohm
  
frequency_response:
  measurement_range: {{f_min}} - {{f_max}} Hz
  temperature: {{T}} K
  
  complex_permittivity:
    model: "{{Debye | Cole-Cole | Havriliak-Negami | Jonscher}}"
    
    debye_parameters:
      {% if model == 'Debye' %}
      static_permittivity: {{epsilon_s}}
      high_frequency_permittivity: {{epsilon_inf}}
      relaxation_time: {{tau}} s
      {% endif %}
      
    cole_cole_parameters:
      {% if model == 'Cole-Cole' %}
      static_permittivity: {{epsilon_s}}
      high_frequency_permittivity: {{epsilon_inf}}
      relaxation_time: {{tau}} s
      distribution_parameter: {{alpha}} (0-1)
      {% endif %}
      
  loss_tangent:
    tan_delta: {{tan_d}}
    loss_factor: {{epsilon_double_prime}} = {{epsilon_prime}} · tan_delta
    maxwell_reference: "Art. 103-111 (absorption)"
    
dielectric_absorption:
  phenomenon: "Charge accumulation at interfaces"
  maxwell_wagner_polarization:
    description: "Interfacial polarization in heterogeneous media"
    maxwell_reference: "Art. 103-111"
    relaxation_time: {{tau_MW}} s
    interfacial_capacitance: {{C_int}} statfarad
    
  absorption_current:
    model: "{{Curie-von-Schweidler | stretched_exponential | power_law}}"
    I(t) = {{absorption_current_expression}}
    decay_exponent: {{n}} (typically 0.5-1.0)
    
temperature_dependence:
  model: "{{Arrhenius | VFT | Linear}}"
  
  arrhenius_parameters:
    {% if model == 'Arrhenius' %}
    activation_energy: {{E_a}} erg/mol
    preexponential: {{tau_0}} s
    relation: "tau = tau_0 · exp(E_a / k_B·T)"
    {% endif %}
    
  temperature_range: {{T_min}} - {{T_max}} K
  reference_temperature: {{T_ref}} K
  
anisotropy:
  {% if is_anisotropic %}
  crystal_system: "{{uniaxial | biaxial | orthorhombic | etc}}"
  principal_axes:
    K_x: {{K_x}}
    K_y: {{K_y}}
    K_z: {{K_z}}
  optic_axis: "{{direction}}"
  {% else %}
  isotropic: true
  {% endif %}
  
breakdown_characteristics:
  intrinsic_breakdown: {{E_int}} statvolt/cm
  thermal_breakdown: {{E_therm}} statvolt/cm
  electromechanical_breakdown: {{E_em}} statvolt/cm
  practical_breakdown: {{E_practical}} statvolt/cm
  
  breakdown_mechanism:
    dominant: "{{electronic | thermal | electromechanical | discharge}}"
    maxwell_reference: "Art. 56-57"
    
  safety_factor: {{SF}} = {{E_practical}} / {{E_operating}}
  
energy_storage:
  energy_density: {{u}} = (K / 8*pi) · E² (erg/cm³)
  maxwell_reference: "Art. 56-57"
  maximum_energy_density: {{u_max}} erg/cm³
  
quality_metrics:
  dielectric_quality: {{Q}} = 1 / tan_delta
  figure_of_merit: {{FOM}} = K / tan_delta
  dissipation_factor: {{DF}} = tan_delta · 100 %
```

## Variables

| Variable | Description | Type | Required |
|----------|-------------|------|----------|
| material_name | Dielectric material name | string | Yes |
| K | Dielectric constant | number | Yes |
| E_bd | Breakdown strength | number | Yes |
| model | Frequency response model | enum | Yes |
| tan_delta | Loss tangent | number | Yes |

## CGS Unit Reference

| Quantity | CGS Unit | Conversion |
|----------|----------|------------|
| Electric field E | statvolt/cm | 1 statvolt/cm = 29979 V/m |
| Electric displacement D | statvolt/cm | (same as E in CGS) |
| Polarization P | statvolt/cm | (same units in CGS) |
| Capacitance | statfarad | 1 statfarad = 1.113×10⁻¹² F |
| Energy density | erg/cm³ | 1 erg/cm³ = 0.1 J/m³ |

## Usage Example

```yaml
dielectric_response:
  name: "Mica_Dielectric_Characterization"
  material: "Muscovite Mica"
  maxwell_articles: ["Art. 50-62", "Art. 103-111"]
  theory_classification: "standard_math"
  
constitutive_relation:
  form: "D = K·E = E + 4*pi*P (CGS)"
  maxwell_reference: "Art. 60-62"
  dielectric_constant: 7.0 (dimensionless)
  
static_properties:
  dielectric_constant: 7.0
  refractive_index: 1.59
  breakdown_strength: 2000 statvolt/cm
  volume_resistivity: 10^15 statohm·cm
  
frequency_response:
  measurement_range: 100 Hz - 1 MHz
  temperature: 293 K
  
  complex_permittivity:
    model: "Debye"
    
    debye_parameters:
      static_permittivity: 7.0
      high_frequency_permittivity: 2.52
      relaxation_time: 1.5e-6 s
      
  loss_tangent:
    tan_delta: 0.0002
```

## Output Format

- YAML frontmatter with metadata
- Structured dielectric properties
- Maxwell article cross-references
- Frequency response data

## Quality Criteria

- [ ] All properties have CGS units
- [ ] Maxwell article citations included
- [ ] Constitutive relation documented
- [ ] Frequency response characterized
- [ ] Breakdown criteria specified

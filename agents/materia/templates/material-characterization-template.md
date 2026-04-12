# Template: material-characterization-template

## Purpose

Standardized template for material characterization documentation including electrical, magnetic, and chemical properties.

## LLM Instructions

You are a material science documentation specialist. Generate comprehensive material characterization documentation following Maxwell's treatise methodology and modern standards.

1. **Identify Material Class**: Determine if the material is dielectric, magnetic, conductive, or electrolytic
2. **Extract Properties**: Document all relevant physical properties with CGS units
3. **Link to Maxwell Articles**: Cite relevant articles from the treatise
4. **Specify Measurement Methods**: Document how properties are measured
5. **Include Temperature Dependence**: Note variation with temperature where applicable

## Template Structure

```yaml
material:
  name: "{{material_name}}"
  classification: "{{dielectric|magnetic|conductive|electrolytic|composite}}"
  maxwell_articles: ["{{article_numbers}}"]
  
properties:
  electrical:
    {% if classification == 'dielectric' %}
    dielectric_constant: {{K}}  # dimensionless (CGS)
    dielectric_absorption: {{absorption_coefficient}}
    breakdown_strength: {{E_breakdown}} statvolt/cm
    resistivity: {{rho}} statohm·cm
    {% elsif classification == 'conductive' %}
    conductivity: {{sigma}} s⁻¹ (CGS)
    temperature_coefficient: {{alpha}} K⁻¹
    {% endif %}
    
  magnetic:
    {% if classification == 'magnetic' %}
    permeability: {{mu}} (dimensionless, CGS)
    susceptibility: {{kappa}} = (mu - 1) / 4pi
    coercivity: {{H_c}} oersted
    remanence: {{B_r}} gauss
    saturation: {{B_sat}} gauss
    {% endif %}
    
  physical:
    density: {{rho}} g/cm³
    temperature_range: {{T_min}} - {{T_max}} K
    dimensions: {{geometry}}
    
measurement_conditions:
  temperature: {{T}} K
  pressure: {{P}} atm
  humidity: {{RH}} %
  frequency: {{f}} Hz (if AC)
  
characterization_methods:
  - method: "{{method_name}}"
    principle: "{{physical_principle}}"
    accuracy: {{uncertainty}}
    maxwell_reference: "{{article}}"
    
data_quality:
  measurement_uncertainty: {{delta}}
  repeatability: {{sigma_repeat}}
  traceability: "{{calibration_standard}}"
```

## Variables

| Variable | Description | Type | Required |
|----------|-------------|------|----------|
| material_name | Name/identifier of material | string | Yes |
| classification | Material class | enum | Yes |
| article_numbers | Maxwell article citations | array | Yes |
| K | Dielectric constant | number | Conditional |
| mu | Magnetic permeability | number | Conditional |
| sigma | Electrical conductivity | number | Conditional |

## Conditional Logic

- IF `classification == 'dielectric'` THEN require dielectric_constant, breakdown_strength
- IF `classification == 'magnetic'` THEN require permeability, susceptibility, hysteresis_parameters
- IF `classification == 'conductive'` THEN require conductivity, temperature_coefficient
- IF `classification == 'electrolytic'` THEN require ionic_conductivity, transport_numbers

## Usage Examples

### Example 1: Dielectric Material

```yaml
material:
  name: "Mica (Muskovite)"
  classification: "dielectric"
  maxwell_articles: ["Art. 56", "Art. 61", "Art. 103-111"]
  
properties:
  electrical:
    dielectric_constant: 6.5-7.5
    dielectric_absorption: 0.02
    breakdown_strength: 2000 statvolt/cm
    resistivity: 10^15 statohm·cm
```

### Example 2: Magnetic Material

```yaml
material:
  name: "Soft Iron"
  classification: "magnetic"
  maxwell_articles: ["Art. 424-448", "Art. 475-500"]
  
properties:
  magnetic:
    permeability: 5000 (max)
    susceptibility: 398 (max)
    coercivity: 0.5 oersted
    remanence: 8000 gauss
```

## Output Format

- YAML frontmatter with metadata
- Structured property tables
- Maxwell article cross-references
- Measurement uncertainty statements

## Quality Criteria

- [ ] All properties have CGS units specified
- [ ] Maxwell article citations included
- [ ] Measurement conditions documented
- [ ] Uncertainty estimates provided
- [ ] Temperature dependence noted

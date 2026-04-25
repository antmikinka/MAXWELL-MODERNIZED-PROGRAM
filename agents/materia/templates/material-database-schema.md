# Template: material-database-schema

## Purpose

Standardized template for material database schema and query interface following Maxwell's systematic classification of material properties.

## LLM Instructions

You are a materials database architect. Generate comprehensive database schema documentation that organizes material properties consistent with Maxwell's treatise structure and modern materials informatics standards.

1. **Establish Classification System**: Organize by property type (electrical, magnetic, chemical)
2. **Define Data Model**: Entities, relationships, constraints
3. **Specify Query Interface**: Search, filter, comparison operations
4. **Link to Maxwell Articles**: Cross-reference all properties to treatise
5. **Document Data Quality**: Uncertainty, provenance, version control

## Template Structure

```yaml
material_database:
  name: "{{database_name}}"
  version: "{{version}}"
  maxwell_based: true
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
schema_version: "{{schema_version}}"
created: "{{date}}"
last_updated: "{{last_updated}}"

entity_definitions:

  material:
    description: "Core material entity"
    fields:
      - name: material_id
        type: string (UUID)
        primary_key: true
        
      - name: name
        type: string
        unique: true
        indexed: true
        
      - name: classification
        type: enum
        values: [dielectric, magnetic, conductive, electrolytic, composite, semiconductor]
        indexed: true
        
      - name: maxwell_articles
        type: array[string]
        description: "Related Maxwell article citations"
        
      - name: source
        type: string
        description: "Data source reference"
        
      - name: uncertainty_level
        type: enum
        values: [high, medium, low, certified]
        
  electrical_properties:
    description: "Electrical property measurements"
    fields:
      - name: material_id
        type: string (FK → material.material_id)
        indexed: true
        
      - name: property_type
        type: enum
        values: [permittivity, conductivity, resistivity, breakdown_strength, loss_tangent]
        indexed: true
        
      - name: value
        type: float
        cgs_unit: "{{unit_expression}}"
        
      - name: uncertainty
        type: float
        relative: true
        
      - name: temperature
        type: float
        unit: K
        
      - name: frequency
        type: float
        unit: Hz
        nullable: true
        
      - name: measurement_method
        type: string
        maxwell_reference: "{{article}}"
        
  magnetic_properties:
    description: "Magnetic property measurements"
    fields:
      - name: material_id
        type: string (FK → material.material_id)
        
      - name: property_type
        type: enum
        values: [permeability, susceptibility, coercivity, remanence, saturation, hysteresis_loss]
        indexed: true
        
      - name: value
        type: float
        cgs_unit: "{{unit_expression}}"
        
      - name: field_condition
        type: float
        unit: oersted
        nullable: true
        
      - name: temperature
        type: float
        unit: K
        
      - name: maxwell_reference
        type: string
        description: "Article citation"
        
  dielectric_properties:
    description: "Dielectric-specific properties"
    fields:
      - name: material_id
        type: string (FK → material.material_id)
        
      - name: static_permittivity
        type: float
        dimensionless: true
        
      - name: optical_permittivity
        type: float
        description: "n² where n is refractive index"
        
      - name: loss_tangent
        type: float
        dimensionless: true
        
      - name: breakdown_strength
        type: float
        cgs_unit: statvolt/cm
        
      - name: absorption_coefficient
        type: float
        dimensionless: true
        
      - name: maxwell_reference
        type: string
        description: "Art. 50-62, 103-111"
        
  electrolytic_properties:
    description: "Electrolysis and ionic conduction properties"
    fields:
      - name: material_id
        type: string (FK → material.material_id)
        
      - name: ion_name
        type: string
        indexed: true
        
      - name: charge_number
        type: integer
        description: "z (elementary charges)"
        
      - name: mobility
        type: float
        cgs_unit: cm²/statvolt·s
        
      - name: diffusion_coefficient
        type: float
        cgs_unit: cm²/s
        
      - name: transport_number
        type: float
        dimensionless: true
        constraint: "0 <= value <= 1"
        
      - name: maxwell_reference
        type: string
        description: "Art. 236-238, 269-286"
        
  hysteresis_data:
    description: "Complete hysteresis loop data"
    fields:
      - name: material_id
        type: string (FK → material.material_id)
        
      - name: loop_type
        type: enum
        values: [major, minor, anhysteretic, initial]
        
      - name: field_amplitude
        type: float
        cgs_unit: oersted
        
      - name: loop_data
        type: JSON
        description: "Array of {H, B} points"
        format: "[{\"H\": value, \"B\": value}, ...]"
        
      - name: loop_area
        type: float
        cgs_unit: erg/cm³
        
      - name: maxwell_reference
        type: string
        description: "Art. 424-448"
        
relationships:
  - name: material_electrical
    type: one-to-many
    from: material.material_id
    to: electrical_properties.material_id
    
  - name: material_magnetic
    type: one-to-many
    from: material.material_id
    to: magnetic_properties.material_id
    
  - name: material_dielectric
    type: one-to-many
    from: material.material_id
    to: dielectric_properties.material_id
    
  - name: material_electrolytic
    type: one-to-many
    from: material.material_id
    to: electrolytic_properties.material_id
    
  - name: material_hysteresis
    type: one-to-many
    from: material.material_id
    to: hysteresis_data.material_id
    
query_interface:

  search_operations:
    - operation: find_by_name
      parameters: [name_pattern]
      returns: "material[]"
      
    - operation: find_by_property
      parameters: [property_type, min_value, max_value, unit]
      returns: "material[]"
      
    - operation: find_by_maxwell_article
      parameters: [article_number]
      returns: "material[]"
      
    - operation: find_by_classification
      parameters: [classification]
      returns: "material[]"
      
  filter_operations:
    - operation: filter_temperature_range
      parameters: [T_min, T_max]
      
    - operation: filter_frequency_range
      parameters: [f_min, f_max]
      
    - operation: filter_uncertainty
      parameters: [max_uncertainty]
      
  comparison_operations:
    - operation: compare_materials
      parameters: [material_ids, property_type]
      returns: "comparison_table"
      
    - operation: rank_by_property
      parameters: [property_type, order]
      returns: "ranked_list"
      
data_quality:

  uncertainty_levels:
    certified: "NIST-traceable, u < 1%"
    low: "Multiple sources agree, u < 5%"
    medium: "Single reliable source, u < 10%"
    high: "Estimated or old data, u >= 10%"
    
  provenance_tracking:
    source_citation: required
    measurement_date: required
    laboratory: optional
    standard_reference: optional
    
  version_control:
    schema_versioning: true
    data_versioning: true
    change_log: required
    
cgs_unit_system:
  enforced: true
  conversion_table: "See data/cgs-unit-reference.md"
  validation: "Automatic on data entry"
  
maxwell_article_index:
  Part_I_Electrostatics: "Art. 1-229"
  Part_II_Electrokinematics: "Art. 230-370"
  Part_III_Magnetism: "Art. 371-474"
  Part_IV_Electromagnetism: "Art. 475-866"
```

## Output Format

- YAML frontmatter with metadata
- Structured entity definitions
- Relationship mappings
- Query interface specification

## Quality Criteria

- [ ] All entities have primary keys
- [ ] Foreign key relationships defined
- [ ] CGS units specified for all properties
- [ ] Maxwell article references included
- [ ] Data quality constraints defined

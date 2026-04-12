# Template: composite-material-specification

## Purpose

Standardized template for composite material specification combining multiple constituent properties with structural geometry.

## LLM Instructions

You are a composite materials engineer. Generate comprehensive composite material specifications that integrate constituent properties, geometric structure, and effective behavior.

1. **Define Composite Architecture**: Layup, fiber orientation, volume fractions
2. **Specify Constituent Properties**: Matrix, reinforcement, interfaces
3. **Compute Effective Properties**: Homogenized behavior in all directions
4. **Document Manufacturing Parameters**: Processing conditions, quality control
5. **Link to Maxwell's Theory**: Dielectric mixing, magnetic composites

## Template Structure

```yaml
composite_specification:
  name: "{{composite_name}}"
  designation: "{{industry_designation}}"
  maxwell_articles: ["{{relevant_articles}}"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
architecture:
  type: "{{laminate | particulate | fiber_reinforced | sandwich | functionally_graded}}"
  
  laminate:
    {% if type == 'laminate' %}
    total_plies: {{n_plies}}
    stacking_sequence: [{{ply_angles}}]  # e.g., [0, 90, 45, -45, s]
    ply_thickness: {{t_ply}} cm
    total_thickness: {{t_total}} cm
    
    ply_materials:
      - ply_range: "1-4"
        material: "{{prepreg_designation}}"
        fiber_orientation: {{theta}} degrees
        
      - ply_range: "5-8"
        material: "{{prepreg_designation}}"
        fiber_orientation: {{theta}} degrees
    {% endif %}
    
  fiber_reinforced:
    {% if type == 'fiber_reinforced' %}
    fiber_type: "{{carbon | glass | aramid | boron | ceramic}}"
    fiber_volume_fraction: {{V_f}}
    matrix_volume_fraction: {{V_m}}
    void_fraction: {{V_v}}
    
    fiber_architecture: "{{unidirectional | woven | braided | random_mat}}"
    weave_pattern: "{{plain | twill | satin}}" (if woven)
    
    fiber_properties:
      diameter: {{d_fiber}} cm
      tensile_modulus: {{E_f}} dyne/cm²
      tensile_strength: {{sigma_f}} dyne/cm²
      density: {{rho_f}} g/cm³
      
    matrix_properties:
      material: "{{epoxy | polyester | PEEK | ceramic}}"
      tensile_modulus: {{E_m}} dyne/cm²
      tensile_strength: {{sigma_m}} dyne/cm²
      density: {{rho_m}} g/cm³
    {% endif %}
    
constituent_materials:

  matrix:
    name: "{{matrix_name}}"
    phase: "continuous"
    
    electrical:
      permittivity: {{K_m}}
      conductivity: {{sigma_m}} s⁻¹
      breakdown_strength: {{E_bd_m}} statvolt/cm
      
    magnetic:
      permeability: {{mu_m}}
      susceptibility: {{kappa_m}}
      
    mechanical:
     Young's_modulus: {{E_m}} dyne/cm²
      Poisson_ratio: {{nu_m}}
      shear_modulus: {{G_m}} dyne/cm²
      
  reinforcement:
    name: "{{reinforcement_name}}"
    phase: "dispersed"
    geometry: "{{fiber | particle | platelet | whisker}}"
    
    electrical:
      permittivity: {{K_r}}
      conductivity: {{sigma_r}} s⁻¹
      
    magnetic:
      permeability: {{mu_r}}
      saturation: {{B_sat_r}} gauss
      
    mechanical:
      Young's_modulus: {{E_r}} dyne/cm²
      aspect_ratio: {{L/D}}
      
  interface:
    present: "{{yes | no}}"
    {% if present %}
    type: "{{coupling_agent | coating | graded | none}}"
    thickness: {{t_int}} cm
    properties:
      shear_strength: {{tau_int}} dyne/cm²
      fracture_toughness: {{G_c}} erg/cm²
    {% endif %}
    
effective_properties:

  electrical:
    permittivity_tensor:
      K_xx: {{K_xx}}
      K_yy: {{K_yy}}
      K_zz: {{K_zz}}
      K_xy: {{K_xy}} (if anisotropic)
      K_yz: {{K_yz}}
      K_xz: {{K_xz}}
      
    conductivity_tensor:
      sigma_xx: {{sigma_xx}} s⁻¹
      sigma_yy: {{sigma_yy}} s⁻¹
      sigma_zz: {{sigma_zz}} s⁻¹
      
    model_used: "{{Maxwell-Garnett | Bruggeman | Mori-Tanaka | self_consistent}}"
    maxwell_reference: "Art. 314"
    
  magnetic:
    permeability_tensor:
      mu_xx: {{mu_xx}}
      mu_yy: {{mu_yy}}
      mu_zz: {{mu_zz}}
      
    saturation_induction: {{B_sat}} gauss
    coercivity: {{H_c}} oersted
    
  mechanical:
    stiffness_matrix: "[C_ij] (6x6 Voigt notation)"
    engineering_constants:
      E_1: {{E1}} dyne/cm²
      E_2: {{E2}} dyne/cm²
      E_3: {{E3}} dyne/cm²
      G_12: {{G12}} dyne/cm²
      G_23: {{G23}} dyne/cm²
      G_13: {{G13}} dyne/cm²
      nu_12: {{nu12}}
      nu_23: {{nu23}}
      nu_13: {{nu13}}
      
    model_used: "{{rule_of_mixtures | Halpin-Tsai | Mori-Tanaka | CLT}}"
    
  thermal:
    conductivity_tensor:
      k_xx: {{k_xx}} erg/cm·s·K
      k_yy: {{k_yy}}
      k_zz: {{k_zz}}
      
    expansion_coefficient:
      alpha_1: {{alpha1}} K⁻¹
      alpha_2: {{alpha2}} K⁻¹
      
specific_properties:

  density: {{rho}} g/cm³
  specific_stiffness: {{E}}/{{rho}} cm²/s²
  specific_strength: {{sigma}}/{{rho}} cm²/s²
  
quality_control:

  void_content: {{V_v}} % (target: < 2%)
  fiber_waviness: {{waviness_angle}} degrees (target: < 1°)
  resin_rich_areas: "{{none | minimal | acceptable | excessive}}"
  
  ndt_methods:
    - method: "ultrasonic"
      parameters: "{{scan_parameters}}"
      acceptance_criteria: "{{criteria}}"
      
    - method: "thermography"
      parameters: "{{scan_parameters}}"
      acceptance_criteria: "{{criteria}}"
      
manufacturing:

  process: "{{autoclave | RTM | filament_winding | pultrusion | compression_molding}}"
  
  cure_cycle:
    ramp_1: "{{rate}} K/min to {{T1}} K"
    hold_1: "{{time}} at {{T1}} K"
    ramp_2: "{{rate}} K/min to {{T2}} K"
    hold_2: "{{time}} at {{T2}} K"
    cool: "{{rate}} K/min to room temperature"
    
  post_processing: "{{none | annealing | machining | coating}}"
  
applications:

  primary: "{{application_area}}"
  operating_conditions:
    temperature_range: {{T_min}} - {{T_max}} K
    humidity_range: {{RH_min}} - {{RH_max}} %
    chemical_exposure: "{{none | mild | severe}}"
    
  electromagnetic_applications:
    - "{{RF_absorbing | EMI_shielding | radar_transparent | antenna_substrate}}"
    
  maxwell_relevance: "{{dielectric_structural | magnetic_composite | multifunctional}}"
```

## Variables

| Variable | Description | Type | Required |
|----------|-------------|------|----------|
| composite_name | Composite identifier | string | Yes |
| type | Architecture type | enum | Yes |
| V_f | Fiber volume fraction | number | Conditional |
| V_m | Matrix volume fraction | number | Yes |
| stacking_sequence | Ply orientation array | array | Conditional |

## Output Format

- YAML frontmatter with metadata
- Structured specification data
- Effective property tensors
- Manufacturing parameters

## Quality Criteria

- [ ] Volume fractions sum correctly
- [ ] All properties have CGS units
- [ ] Anisotropy properly characterized
- [ ] Manufacturing parameters specified
- [ ] Quality control criteria defined

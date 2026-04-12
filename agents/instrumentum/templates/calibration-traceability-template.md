# Template: calibration-traceability-template

## Purpose

Standardized template for calibration traceability documentation establishing the chain from working instruments to primary standards.

## LLM Instructions

You are a calibration specialist. Generate comprehensive traceability documentation following Maxwell's measurement principles and modern calibration hierarchy practices.

1. **Establish Theoretical Foundation**: Link to Maxwell's calibration articles
2. **Define Calibration Chain**: Primary → Secondary → Working
3. **Document Each Level**: Standards, uncertainties, procedures
4. **Establish Traceability**: Unbroken chain to national standards
5. **Maintain Records**: Certificates, calibration history

## Template Structure

```yaml
calibration_traceability:
  name: "{{traceability_name}}"
  measurand: "{{measurand}}"
  maxwell_articles: ["{{relevant_articles}}"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
calibration_hierarchy:

  level_1_primary:
    level: "Primary Standard"
    institution: "{{NIST | PTB | NPL | etc.}}"
    
    standard:
      name: "{{standard_name}}"
      type: "{{standard_type}}"
      certificate: "{{cert_number}}"
      
    realization:
      method: "{{realization_method}}"
      principle: "{{physical_principle}}"
      maxwell_reference: "{{article}}"
      
    uncertainty:
      value: {{u_primary}} {{unit}}
      confidence: {{confidence}}%
      coverage_factor: {{k}}
      
    stability:
      drift_rate: {{drift}} {{unit}}/year
      recalibration_interval: "{{interval}}"
      
  level_2_secondary:
    level: "Secondary Standard"
    institution: "{{calibration_lab}}"
    
    standard:
      name: "{{standard_name}}"
      type: "{{standard_type}}"
      model: "{{model}}"
      serial: "{{serial}}"
      
    calibration:
      calibrated_against: "{{primary_standard}}"
      certificate: "{{cert_number}}"
      date: "{{cal_date}}"
      next_due: "{{next_due}}"
      
    uncertainty:
      value: {{u_secondary}} {{unit}}
      confidence: {{confidence}}%
      coverage_factor: {{k}}
      
      uncertainty_from_primary: {{u_from_primary}} {{unit}}
      uncertainty_from_process: {{u_process}} {{unit}}
      combined: {{u_combined}} = √(Σu_i²) = {{u_sec_val}} {{unit}}
      
    stability:
      drift_rate: {{drift}} {{unit}}/year
      historical_data: "{{reference}}"
      
  level_3_working:
    level: "Working Standard"
    location: "{{laboratory_location}}"
    
    standard:
      name: "{{standard_name}}"
      type: "{{standard_type}}"
      model: "{{model}}"
      serial: "{{serial}}"
      
    calibration:
      calibrated_against: "{{secondary_standard}}"
      certificate: "{{cert_number}}"
      date: "{{cal_date}}"
      next_due: "{{next_due}}"
      
    uncertainty:
      value: {{u_working}} {{unit}}
      confidence: {{confidence}}%
      coverage_factor: {{k}}
      
      uncertainty_from_secondary: {{u_from_secondary}} {{unit}}
      uncertainty_from_process: {{u_process}} {{unit}}
      combined: {{u_combined}} = {{u_work_val}} {{unit}}
      
    usage:
      frequency: "{{usage_frequency}}"
      handling: "{{handling_procedures}}"
      storage: "{{storage_conditions}}"
      
  level_4_instrument:
    level: "Field/Process Instrument"
    location: "{{installation_location}}"
    
    instrument:
      name: "{{instrument_name}}"
      type: "{{instrument_type}}"
      model: "{{model}}"
      serial: "{{serial}}"
      
    calibration:
      calibrated_against: "{{working_standard}}"
      procedure: "{{procedure_number}}"
      date: "{{cal_date}}"
      next_due: "{{next_due}}"
      
    performance:
      as_found: "{{before_calibration}}"
      as_left: "{{after_calibration}}"
      tolerance: {{tolerance}} {{unit}}
      pass_fail: "{{status}}"
    
traceability_chain_summary:

  chain:
    "{{primary_institution}}" (Primary)
         ↓ (uncertainty: {{u1}} {{unit}})
    "{{secondary_lab}}" (Secondary)
         ↓ (uncertainty: {{u2}} {{unit}})
    "{{working_lab}}" (Working)
         ↓ (uncertainty: {{u3}} {{unit}})
    "{{field_location}}" (Instrument)
    
  total_uncertainty_ratio:
    TUR = tolerance / u_combined
    TUR = {{TUR}}
    
    acceptance: "{{acceptable | marginal | unacceptable}}"
    
  traceability_gap_analysis:
    gaps_identified: "{{none | gaps}}"
    {% if gaps %}
    gap_description: "{{description}}"
    corrective_action: "{{action}}"
    {% endif %}
    
calibration_procedures:

  procedure_{{num}}:
    title: "{{procedure_title}}"
    revision: "{{revision}}"
    
    scope: "{{scope_description}}"
    
    equipment_required:
      - "{{equipment_1}}"
      - "{{equipment_2}}"
      
    environmental_conditions:
      temperature: {{T}} ± {{ΔT}} K
      humidity: {{RH}} ± {{ΔRH}} %
      
    procedure_steps:
      - step: "1"
        action: "{{action_description}}"
        acceptance: "{{criteria}}"
        
      - step: "2"
        action: "{{action_description}}"
        acceptance: "{{criteria}}"
        
    data_recording:
      format: "{{data_format}}"
      required_fields: [{{fields}}]
      
    uncertainty_evaluation:
      method: "{{GUM | ISO | other}}"
      documentation: "{{document_reference}}"
    
calibration_records:

  instrument_history:
    - date: "{{date_1}}"
      as_found: "{{reading_1}}"
      adjustment: "{{adjustment_1}}"
      as_left: "{{reading_1_final}}"
      technician: "{{tech_1}}"
      
    - date: "{{date_2}}"
      as_found: "{{reading_2}}"
      adjustment: "{{adjustment_2}}"
      as_left: "{{reading_2_final}}"
      technician: "{{tech_2}}"
      
  trend_analysis:
    drift_observed: "{{yes | no}}"
    drift_rate: {{drift_rate}} {{unit}}/year
    prediction: "{{next_calibration_recommendation}}"
    
certificates:

  primary_certificate:
    issuer: "{{NIST | etc.}}"
    certificate_number: "{{number}}"
    issue_date: "{{date}}"
    valid_until: "{{date}}"
    
  secondary_certificate:
    issuer: "{{lab_name}}"
    accreditation: "{{ISO 17025 | other}}"
    certificate_number: "{{number}}"
    issue_date: "{{date}}"
    
  working_certificate:
    issuer: "{{lab_name}}"
    certificate_number: "{{number}}"
    issue_date: "{{date}}"
    next_due: "{{date}}"
    
maxwell_measurement_principles:
  accuracy: "{{article}}"
  calibration: "{{article}}"
  standards: "{{article}}"
  measurement_chain: "{{article}}"
  
cgs_units:
  primary_unit: "{{unit}}"
  all_levels: "Consistent CGS units throughout chain"
```

## Traceability Chain Example

```
NIST Primary Standard (Quantum Hall Resistance)
  ↓ (u = 0.001 ppm)
NIST Secondary Standard (Resistance Bridge)
  ↓ (u = 0.01 ppm)
Accredited Calibration Lab (Working Standard)
  ↓ (u = 0.1 ppm)
Field Instrument (Digital Multimeter)
```

## Uncertainty Propagation

| Level | Uncertainty | Cumulative |
|-------|-------------|------------|
| Primary | 0.001 ppm | 0.001 ppm |
| Secondary | 0.01 ppm | 0.010 ppm |
| Working | 0.1 ppm | 0.100 ppm |
| Instrument | 1.0 ppm | 1.005 ppm |

## Quality Criteria

- [ ] Unbroken traceability chain
- [ ] All levels documented
- [ ] Uncertainties propagated correctly
- [ ] Certificates current and valid
- [ ] Calibration procedures documented
- [ ] Maxwell article citations included

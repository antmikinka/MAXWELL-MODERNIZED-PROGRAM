# Template: measurement-uncertainty-template

## Purpose

Standardized template for measurement uncertainty analysis in electrical and magnetic measurements.

## LLM Instructions

You are a metrology specialist. Generate comprehensive uncertainty analysis documentation following Maxwell's measurement principles and modern uncertainty evaluation (GUM).

1. **Establish Theoretical Foundation**: Link to Maxwell's measurement articles
2. **Define Measurand**: What is being measured
3. **Identify Uncertainty Sources**: All significant contributors
4. **Quantify Uncertainties**: Type A and Type B
5. **Combine and Report**: Combined and expanded uncertainty

## Template Structure

```yaml
uncertainty_analysis:
  name: "{{analysis_name}}"
  measurand: "{{measurand_description}}"
  maxwell_articles: ["{{relevant_articles}}"]
  theory_classification: "{{maxwell_original | user_original | standard_math}}"
  
measurement_description:
  instrument: "{{instrument_name}}"
  method: "{{measurement_method}}"
  range: {{range}} {{unit}}
  resolution: {{resolution}} {{unit}}
  
  environmental_conditions:
    temperature: {{T}} ± {{ΔT}} K
    humidity: {{RH}} ± {{ΔRH}} %
    pressure: {{P}} ± {{ΔP}} atm
    
  measurement_model:
    equation: "{{measurement_equation}}"
    
    where:
      {{variable_definitions}}
    
uncertainty_sources:

  type_a (statistical):
    - source: "{{source_name}}"
      description: "{{description}}"
      
      evaluation:
        num_observations: {{n}}
        mean: {{mean}} {{unit}}
        standard_deviation: {{s}} {{unit}}
        standard_uncertainty: {{u_A}} = {{s}}/√n = {{u_A_val}} {{unit}}
        
      degrees_of_freedom: {{ν}} = {{n-1}}
      
  type_b (systematic):
    - source: "{{source_name}}"
      description: "{{description}}"
      
      evaluation:
        estimated_value: {{value}} {{unit}}
        distribution: "{{normal | rectangular | triangular | U-shaped}}"
        
        {% if distribution == 'rectangular' %}
        divisor: √3
        standard_uncertainty: {{u}} = {{half_width}}/√3 = {{u_val}} {{unit}}
        
        {% elsif distribution == 'triangular' %}
        divisor: √6
        standard_uncertainty: {{u}} = {{half_width}}/√6 = {{u_val}} {{unit}}
        
        {% elsif distribution == 'normal' %}
        divisor: {{k}} (coverage factor)
        standard_uncertainty: {{u}} = {{expanded}}/{{k}} = {{u_val}} {{unit}}
        {% endif %}
        
      degrees_of_freedom: {{ν}} (∞ for well-known, or estimated)
      
    - source: "Instrument calibration"
      certificate: "{{cert_number}}"
      stated_uncertainty: {{U_cal}} {{unit}}
      coverage_factor: {{k_cal}}
      standard_uncertainty: {{u_cal}} = {{U_cal}}/{{k_cal}} = {{u_cal_val}} {{unit}}
      
    - source: "Resolution"
      resolution: {{res}} {{unit}}
      distribution: "rectangular"
      standard_uncertainty: {{u_res}} = {{res}}/(2√3) = {{u_res_val}} {{unit}}
      
    - source: "Temperature effect"
      temperature_coefficient: {{α}} {{unit}}/K
      temperature_variation: {{ΔT}} K
      distribution: "rectangular"
      standard_uncertainty: {{u_temp}} = {{α}}·{{ΔT}}/√3 = {{u_temp_val}} {{unit}}
      
    - source: "Non-linearity"
      specified_nonlinearity: {{NL}} % FS
      full_scale: {{FS}} {{unit}}
      distribution: "rectangular"
      standard_uncertainty: {{u_nl}} = {{NL}}·{{FS}}/100/√3 = {{u_nl_val}} {{unit}}
      
    - source: "Zero drift"
      drift_rate: {{drift}} {{unit}}/hour
      time_since_calibration: {{t}} hours
      distribution: "rectangular"
      standard_uncertainty: {{u_drift}} = {{drift}}·{{t}}/√3 = {{u_drift_val}} {{unit}}
      
uncertainty_combination:

  sensitivity_coefficients:
    {% for variable in input_variables %}
    - variable: "{{variable}}"
      coefficient: {{c_i}} = ∂f/∂{{variable}} = {{c_val}}
      contribution: {{c_i}}·{{u_i}} = {{contrib}} {{unit}}
    {% endfor %}
    
  combined_uncertainty:
    formula: "u_c = √(Σ(c_i·u_i)²)"
    
    calculation:
      u_c = √({{sum_of_squares}})
      u_c = {{u_c_val}} {{unit}}
      
    relative_uncertainty:
      u_r = u_c / |Y| = {{u_r_val}} ({{u_r_pct}}%)
      
  effective_degrees_of_freedom:
    Welch-Satterthwaite:
    ν_eff = u_c⁴ / Σ((c_i·u_i)⁴ / ν_i)
    ν_eff = {{ν_eff}} (rounded down to {{ν_eff_int}})
    
expanded_uncertainty:

  coverage_factor:
    k = {{k}} (for 95% confidence)
    from_t_distribution: t_{{ν_eff}}(0.95) = {{t_val}}
    
  expanded_uncertainty:
    U = k · u_c = {{U_val}} {{unit}}
    
  confidence_level: {{confidence}}%
  
  reporting:
    result: "{{measurand}} = {{Y}} ± {{U}} {{unit}}"
    statement: "The reported uncertainty is the expanded uncertainty with coverage factor k={{k}}, providing approximately {{confidence}}% level of confidence."
    
uncertainty_budget_table:

  | Source | Type | Distribution | u_i ({{unit}}) | c_i | c_i·u_i |
  |--------|------|--------------|----------------|-----|---------|
  {% for source in sources %}
  | {{source.name}} | {{source.type}} | {{source.distribution}} | {{source.u}} | {{source.c}} | {{source.contrib}} |
  {% endfor %}
  | **Combined** | | | | | **{{u_c_val}}** |
  | **Expanded (k={{k}})** | | | | | **{{U_val}}** |
  
maxwell_measurement_principles:
  accuracy_discussion: "{{article}}"
  error_analysis: "{{article}}"
  calibration_methods: "{{article}}"
  measurement_limits: "{{article}}"
  
cgs_units:
  measured_quantity: "{{unit}}"
  uncertainty: "{{unit}}"
  reference: "All uncertainties expressed in CGS units"
```

## Uncertainty Distribution Guide

| Distribution | Use Case | Divisor |
|--------------|----------|---------|
| Normal (Gaussian) | Statistical data, calibration certs | k (usually 2) |
| Rectangular (Uniform) | Resolution, tolerances, drift | √3 |
| Triangular | Sum of two rectangular, conservative estimate | √6 |
| U-shaped | Sinusoidal variation, temperature cycling | √2 |

## Coverage Factors

| Confidence Level | k (large ν) | k (ν=10) | k (ν=5) |
|-----------------|-------------|----------|---------|
| 90% | 1.645 | 1.812 | 2.015 |
| 95% | 2.000 | 2.228 | 2.571 |
| 99% | 2.576 | 3.169 | 4.032 |

## Quality Criteria

- [ ] All uncertainty sources identified
- [ ] Type A/B classification correct
- [ ] Distributions appropriately assigned
- [ ] Sensitivity coefficients evaluated
- [ ] Combined uncertainty calculated
- [ ] Expanded uncertainty reported
- [ ] Maxwell article citations included

# Template: quality-gate-template

## Description

Template for defining CI/CD quality gates.

## Structure

```yaml
quality_gate:
  name: {gate_name}
  required: {true|false}
  
  checks:
    - name: {check_name}
      type: {test|coverage|audit}
      threshold: {value}
      
  failure_action: {block|warn|skip}
  
  notifications:
    on_failure: {true|false}
    channels: [{channels}]
```

## LLM Instructions

1. Define clear pass/fail criteria
2. Set appropriate thresholds
3. Configure failure handling
4. Set up notifications

# Checklist: CI/CD Quality Gates

## Purpose

Ensure CI/CD pipeline quality gates are effective and appropriate.

## Gate Configuration

### Required Gates
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Physics validation pass
- [ ] Citation audit pass
- [ ] Coverage requirements met

### Optional Gates
- [ ] Performance benchmarks
- [ ] Documentation build
- [ ] Security scan
- [ ] Code style check

## Threshold Settings

| Gate | Threshold | Justification |
|------|-----------|---------------|
| Test pass rate | 100% | Required for correctness |
| Coverage | 90% | Adequate test coverage |
| Physics tolerance | 1e-6 | Numerical precision |

## Notification Settings

- [ ] Failure notifications configured
- [ ] Right channels subscribed
- [ ] Escalation policy defined

## Monitoring

- [ ] Dashboard configured
- [ ] Trends tracked
- [ ] Alerts actionable

## Sign-off

| Role | Name | Date |
|------|------|------|
| DevOps | | |
| QA Lead | | |

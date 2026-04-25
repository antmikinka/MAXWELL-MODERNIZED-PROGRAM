# Template: Pipeline Status

## Description

Template for reporting pipeline execution status across all phases of the Maxwell Treatise modernization. This template ensures consistent tracking of phase progress, task completion, and agent workload.

## Structure

```markdown
# Pipeline Status Report

## Report Metadata

**Generated:** {DATE}  
**Report Period:** {PERIOD}  
**Architecture Version:** {ARCH_VERSION}  
**Pipeline Version:** {PIPELINE_VERSION}

---

## Executive Summary

**Current Phase:** {CURRENT_PHASE} ({PHASE_NAME})  
**Phase Progress:** {PHASE_PROGRESS}%  
**Overall Progress:** {OVERALL_PROGRESS}%  
**Status:** {STATUS} (On Track / At Risk / Delayed)

### Summary Dashboard

```
Phase 0: COMPLETE   ████████████████████ 100%
Phase 1: COMPLETE   ████████████████████ 100%
Phase 2: IN PROGRESS ████████████░░░░░░░░  67%
Phase 3: PENDING    ░░░░░░░░░░░░░░░░░░░░   0%
Phase 4: PENDING    ░░░░░░░░░░░░░░░░░░░░   0%
```

---

## Phase Details

### Phase 0: Tool Scoping

**Status:** COMPLETE  
**Duration:** {DURATION} days (planned: {PLANNED_DURATION} days)  
**Tasks:** {COMPLETE}/{TOTAL} complete

| Metric | Value |
|--------|-------|
| Articles Scoped | {COUNT} |
| Tools Selected | {COUNT} |
| Test Strategies | {COUNT} |
| Priority Matrix | {STATUS} |

**Exit Criteria:**
- [x] All articles scoped
- [x] Tools selected for each module
- [x] Test strategies defined
- [x] Priority matrix approved

---

### Phase 1: Foundation Implementation

**Status:** COMPLETE  
**Duration:** {DURATION} days (planned: {PLANNED_DURATION} days)  
**Tasks:** {COMPLETE}/{TOTAL} complete

| Metric | Value |
|--------|-------|
| Layers Implemented | 0-2 |
| Foundation Tests | {PASS_COUNT}/{TOTAL} passing |
| CGS/SI Duality | {STATUS} |
| Citation Tracking | {STATUS} |

**Exit Criteria:**
- [x] Layer 0-2 implemented
- [x] Foundation tests passing
- [x] CGS/SI duality working
- [x] Citation tracking functional

---

### Phase 2: Core Physics

**Status:** IN PROGRESS  
**Duration:** {DURATION} days (planned: {PLANNED_DURATION} days)  
**Tasks:** {COMPLETE}/{TOTAL} complete

| Metric | Value |
|--------|-------|
| Layers Implemented | 3-6 ({PERCENT}%) |
| Physics Tests | {PASS_COUNT}/{TOTAL} passing |
| Analytical Validations | {COMPLETE}/{TOTAL} |
| Visualization | {STATUS} |

**Current Tasks:**
| Task ID | Description | Assignee | Status | Due Date |
|---------|-------------|----------|--------|----------|
| {TASK_ID} | {DESC} | {ASSIGNEE} | {STATUS} | {DATE} |

**Exit Criteria:**
- [x] Core physics implemented ({PERCENT}%)
- [ ] Analytical solutions validated
- [ ] Visualization functional
- [ ] Cross-part integration tested

---

### Phase 3: Advanced Solvers

**Status:** PENDING  
**Planned Duration:** {PLANNED_DURATION} days  
**Tasks:** 0/{TOTAL} complete

**Planned Work:**
- Layers 7-10 implementation
- Spherical harmonics kernel
- Ellipsoidal coordinates
- Image method solvers
- 2D complex analysis

---

### Phase 4: Applications & Validation

**Status:** PENDING  
**Planned Duration:** {PLANNED_DURATION} days  
**Tasks:** 0/{TOTAL} complete

**Planned Work:**
- Component library completion
- Instrumentation models
- Verification test suite
- Documentation generation

---

## Agent Workload

### Current Task Assignment

| Agent | Active Tasks | Completed | Pending | Blockers |
|-------|--------------|-----------|---------|----------|
| PHYSICUS | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| MATHEMATICA | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| QUALITAS | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| SCRIBA | {COUNT} | {COUNT} | {COUNT} | {COUNT} |
| ARCHITECTUS | {COUNT} | {COUNT} | {COUNT} | {COUNT} |

### Workload Distribution

```
PHYSICUS:    ████████████████░░░░  75% utilized
MATHEMATICA: ████████████░░░░░░░░  60% utilized
QUALITAS:    ██████████████████░░  90% utilized
SCRIBA:      ████████░░░░░░░░░░░░  40% utilized
```

---

## Blockers and Risks

### Current Blockers

| ID | Description | Impact | Owner | Resolution Plan |
|----|-------------|--------|-------|-----------------|
| {ID} | {DESC} | {IMPACT} | {OWNER} | {PLAN} |

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| {RISK} | {PROB} | {IMPACT} | {MITIGATION} |

---

## Milestones

### Completed Milestones

| Milestone | Date | Status |
|-----------|------|--------|
| {MILESTONE} | {DATE} | ✅ |

### Upcoming Milestones

| Milestone | Target Date | Confidence |
|-----------|-------------|------------|
| {MILESTONE} | {DATE} | {PERCENT}% |

---

## Metrics and Trends

### Velocity

| Week | Tasks Complete | Story Points |
|------|----------------|--------------|
| {WEEK1} | {COUNT} | {POINTS} |
| {WEEK2} | {COUNT} | {POINTS} |
| {WEEK3} | {COUNT} | {POINTS} |

### Burnup Chart

```
Week 1: ████████░░░░░░░░░░░░ 40%
Week 2: ████████████░░░░░░░░ 60%
Week 3: ████████████████░░░░ 80%
Week 4: ████████████████████ 100% (projected)
```

---

## Recommendations

### Immediate Actions

1. {ACTION_1}
2. {ACTION_2}
3. {ACTION_3}

### Next Sprint Priorities

1. {PRIORITY_1}
2. {PRIORITY_2}
3. {PRIORITY_3}

---

## Appendix

### Task Legend

| Status | Meaning |
|--------|---------|
| TODO | Not started |
| IN PROGRESS | Currently working |
| REVIEW | Pending review |
| COMPLETE | Finished and validated |
| BLOCKED | Blocked by dependency |

### Report Generation

Generated by: `architectus pipeline-orchestrate --status`  
Command: `{COMMAND_USED}`

---

**END OF REPORT**
```

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{DATE}` | Report generation date | 2026-04-11 |
| `{PERIOD}` | Reporting period | 2026-Q1 |
| `{ARCH_VERSION}` | Architecture version | 2.0.0 |
| `{CURRENT_PHASE}` | Current phase number | 2 |
| `{PHASE_NAME}` | Phase name | Core Physics |
| `{PHASE_PROGRESS}` | Phase completion % | 67 |
| `{OVERALL_PROGRESS}` | Overall completion % | 42 |
| `{STATUS}` | Project status | On Track |

## Usage Instructions

1. Copy this template to new status report
2. Run pipeline orchestrate command for data
3. Fill in all phase details
4. Update agent workload
5. Document blockers and risks
6. Track milestones
7. Add recommendations

## Related Templates

- `agent-coordination.md` - Agent coordination template
- `consolidation-report.md` - Status consolidation

## Example Status Entry

```markdown
### Phase 2: Core Physics

**Status:** IN PROGRESS  
**Duration:** 38 days (planned: 56 days)  
**Tasks:** 18/27 complete

| Metric | Value |
|--------|-------|
| Layers Implemented | 3-6 (67%) |
| Physics Tests | 145/180 passing |
| Analytical Validations | 12/15 |
| Visualization | In Progress |

**Current Tasks:**
| Task ID | Description | Assignee | Status | Due Date |
|---------|-------------|----------|--------|----------|
| P2-089 | Maxwell stress tensor | PHYSICUS | IN PROGRESS | 2026-04-15 |
| P2-090 | Earnshaw theorem | PHYSICUS | REVIEW | 2026-04-12 |
| P2-091 | Equilibrium analysis | PHYSICUS | COMPLETE | 2026-04-10 |
```

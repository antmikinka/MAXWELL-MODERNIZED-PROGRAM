# Template: Agent Coordination

## Description

Template for coordinating tasks and communication between specialist agents in the Maxwell Treatise modernization pipeline. This template ensures clear task routing, dependency management, and inter-agent collaboration.

## Structure

```markdown
# Agent Coordination Record

## Coordination Metadata

**Coordination ID:** {COORD_ID}  
**Created:** {DATE}  
**Requesting Agent:** {REQUESTING_AGENT}  
**Priority:** {PRIORITY} (P0-Critical / P1-High / P2-Medium / P3-Low)  
**Status:** {STATUS} (Pending / In Progress / Complete / Blocked)

---

## Coordination Request

### Objective

{Clear statement of what needs to be accomplished}

### Scope

{Description of the scope and boundaries of the coordination}

### Dependencies

| Dependency | Providing Agent | Status |
|------------|-----------------|--------|
| {DEPENDENCY} | {AGENT} | {STATUS} |

---

## Agent Task Assignments

### PHYSICUS

**Role:** {ROLE}  
**Tasks:**
| Task ID | Description | Due Date | Status |
|---------|-------------|----------|--------|
| {TASK_ID} | {DESC} | {DATE} | {STATUS} |

**Deliverables:**
- {DELIVERABLE_1}
- {DELIVERABLE_2}

**Dependencies:**
- {DEPENDENCY_1}

---

### MATHEMATICA

**Role:** {ROLE}  
**Tasks:**
| Task ID | Description | Due Date | Status |
|---------|-------------|----------|--------|
| {TASK_ID} | {DESC} | {DATE} | {STATUS} |

**Deliverables:**
- {DELIVERABLE_1}
- {DELIVERABLE_2}

**Dependencies:**
- {DEPENDENCY_1}

---

### QUALITAS

**Role:** {ROLE}  
**Tasks:**
| Task ID | Description | Due Date | Status |
|---------|-------------|----------|--------|
| {TASK_ID} | {DESC} | {DATE} | {STATUS} |

**Deliverables:**
- {DELIVERABLE_1}
- {DELIVERABLE_2}

**Dependencies:**
- {DEPENDENCY_1}

---

### SCRIBA

**Role:** {ROLE}  
**Tasks:**
| Task ID | Description | Due Date | Status |
|---------|-------------|----------|--------|
| {TASK_ID} | {DESC} | {DATE} | {STATUS} |

**Deliverables:**
- {DELIVERABLE_1}
- {DELIVERABLE_2}

**Dependencies:**
- {DEPENDENCY_1}

---

### ARCHITECTUS

**Role:** Orchestration & Architecture Management  
**Tasks:**
| Task ID | Description | Due Date | Status |
|---------|-------------|----------|--------|
| {TASK_ID} | {DESC} | {DATE} | {STATUS} |

**Deliverables:**
- Architecture validation
- Agent synchronization
- Pipeline orchestration

---

## Communication Log

### Updates

| Date | Agent | Update |
|------|-------|--------|
| {DATE} | {AGENT} | {UPDATE} |

### Decisions

| Date | Decision | Participants |
|------|----------|--------------|
| {DATE} | {DECISION} | {PARTICIPANTS} |

### Blockers

| Date | Agent | Blocker | Resolution |
|------|-------|---------|------------|
| {DATE} | {AGENT} | {BLOCKER} | {RESOLUTION} |

---

## Integration Points

### Handoffs

| From Agent | To Agent | Deliverable | Date | Status |
|------------|----------|-------------|------|--------|
| {AGENT} | {AGENT} | {DELIVERABLE} | {DATE} | {STATUS} |

### Shared Resources

| Resource | Used By | Access Pattern |
|----------|---------|----------------|
| {RESOURCE} | {AGENTS} | {PATTERN} |

### Interface Agreements

| Interface | Provider | Consumer | Contract |
|-----------|----------|----------|----------|
| {INTERFACE} | {AGENT} | {AGENT} | {CONTRACT} |

---

## Quality Gates

### Gate 1: {GATE_NAME}

**Criteria:**
- [ ] {CRITERION_1}
- [ ] {CRITERION_2}

**Verifier:** {AGENT}  
**Status:** {PASS/FAIL/PENDING}

### Gate 2: {GATE_NAME}

**Criteria:**
- [ ] {CRITERION_1}
- [ ] {CRITERION_2}

**Verifier:** {AGENT}  
**Status:** {PASS/FAIL/PENDING}

---

## Completion Criteria

- [ ] All agent tasks complete
- [ ] All deliverables produced
- [ ] All quality gates passed
- [ ] All dependencies resolved
- [ ] Architecture synchronized
- [ ] Documentation updated

---

## Sign-Off

| Agent | Role | Sign-Off | Date |
|-------|------|----------|------|
| PHYSICUS | Physics Implementation | {SIGN_OFF} | {DATE} |
| MATHEMATICA | Mathematics Foundation | {SIGN_OFF} | {DATE} |
| QUALITAS | Quality Assurance | {SIGN_OFF} | {DATE} |
| SCRIBA | Documentation | {SIGN_OFF} | {DATE} |
| ARCHITECTUS | Orchestration | {SIGN_OFF} | {DATE} |

---

## Appendix

### Related Documents

- {DOCUMENT_1}
- {DOCUMENT_2}

### Related Commands

- `{COMMAND_1}`
- `{COMMAND_2}`

### Escalation Path

If coordination issues arise:
1. Agent-to-agent resolution attempt
2. ARCHITECTUS mediation
3. Human architect review

---

**END OF COORDINATION RECORD**
```

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{COORD_ID}` | Coordination identifier | COORD-2026-001 |
| `{DATE}` | Date | 2026-04-11 |
| `{REQUESTING_AGENT}` | Requesting agent | PHYSICUS |
| `{PRIORITY}` | Priority level | P1-High |
| `{STATUS}` | Coordination status | In Progress |
| `{ROLE}` | Agent role in coordination | Lead Implementer |
| `{TASK_ID}` | Task identifier | P2-089 |
| `{DESC}` | Task description | Maxwell stress tensor implementation |

## Usage Instructions

1. Copy this template to new coordination record
2. Fill in coordination metadata
3. Define objective and scope
4. Assign tasks to each agent
5. Document dependencies
6. Track communication log
7. Monitor quality gates
8. Collect sign-offs on completion

## Related Templates

- `pipeline-status.md` - Pipeline status tracking
- `version-change-log.md` - Version change tracking

## Example Coordination Entry

```markdown
# Agent Coordination Record

## Coordination Metadata

**Coordination ID:** COORD-2026-004  
**Created:** 2026-04-11  
**Requesting Agent:** ARCHITECTUS  
**Priority:** P1-High  
**Status:** In Progress

---

## Coordination Request

### Objective

Implement and validate Maxwell's stress tensor (Arts. 103-110) across
Part I Layer 5 with proper cross-part integration.

### Scope

- PHYSICUS: Implement stress tensor calculations
- MATHEMATICA: Provide tensor operation support
- QUALITAS: Create validation tests
- SCRIBA: Document implementation
- ARCHITECTUS: Coordinate and validate architecture

### Dependencies

| Dependency | Providing Agent | Status |
|------------|-----------------|--------|
| Tensor operations | MATHEMATICA | Complete |
| Field definitions | PHYSICUS | Complete |
```

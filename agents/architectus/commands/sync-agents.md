# Command: sync-agents

## Description

Synchronizes all specialist agents with the latest architecture changes. This command ensures that PHYSICUS, MATHEMATICA, QUALITAS, and all other agents have current knowledge of architecture maps, layer assignments, and module boundaries.

## Usage

```bash
architectus sync-agents [OPTIONS]

Options:
  --agent <AGENT>         Sync specific agent only
  --force                 Force sync even if no changes detected
  --dry-run               Show what would be synced without making changes
  --verify                Verify sync completion after update
  --output <FORMAT>       Output format: text, json, markdown (default: text)
  --report <PATH>         Write sync report to file
```

## Input

- **Architecture COMPLETE Documents**: Updated architecture maps
- **Agent Configuration Files**: Each agent's architecture knowledge
- **Change Log**: Architecture changes since last sync

## Agent Architecture Knowledge

Each agent maintains architecture knowledge in their domain:

| Agent | Architecture Knowledge |
|-------|----------------------|
| PHYSICUS | Physics implementation boundaries, layer assignments |
| MATHEMATICA | Mathematical foundation layers, function locations |
| QUALITAS | Quality gate locations, test boundaries |
| SCRIBA | Documentation structure, article mappings |
| CIRCUITUS | Circuit layer boundaries, component locations |
| MATERIA | Material property locations, layer assignments |
| INSTRUMENTUM | Instrument layer mappings, calibration references |

## Sync Process

### 1. Change Detection

- [ ] Compare current architecture with agent knowledge
- [ ] Identify changed layers
- [ ] Identify changed module mappings
- [ ] Identify new/removed articles

### 2. Agent Notification

- [ ] Notify affected agents of changes
- [ ] Provide change details to each agent
- [ ] Queue agent knowledge updates

### 3. Knowledge Update

- [ ] Update agent architecture files
- [ ] Update agent command definitions
- [ ] Update agent task definitions
- [ ] Update agent templates

### 4. Verification

- [ ] Verify each agent received updates
- [ ] Verify agent knowledge consistency
- [ ] Test agent architecture queries

## Output

### Summary Output

```
Agent Synchronization Report
============================

Architecture Version: 2.0.0
Changes Detected: 15

Changed Layers:
  - Layer 8: 3 new spherical harmonic modules
  - Layer 35: Magnetic potential updated
  - Layer 67: Wave propagation refactored

Agent Updates:
  [✓] PHYSICUS - Updated (15 changes received)
  [✓] MATHEMATICA - Updated (5 changes received)
  [✓] QUALITAS - Updated (8 changes received)
  [✓] SCRIBA - Updated (12 changes received)
  [✓] CIRCUITUS - Updated (3 changes received)
  [✓] MATERIA - Updated (2 changes received)
  [✓] INSTRUMENTUM - Updated (4 changes received)

Sync Status: COMPLETE
Verification: PASSED
All agents synchronized with architecture v2.0.0
```

### Detailed Agent Output

```
PHYSICUS Agent Sync Details
===========================

Previous Architecture Version: 1.9.0
New Architecture Version: 2.0.0

Knowledge Updates:
  + Layer 8: Spherical harmonics modules added
    - maxwell/math/spherical/biaxal.py
    - maxwell/math/spherical/tesseral.py
    - maxwell/math/spherical/visualization.py
  
  ~ Layer 35: Magnetic potential updated
    - calc_solenoid_potential() signature changed
    - New function: calc_toroid_potential()
  
  ~ Module Boundaries:
    - maxwell/physics/fields.py moved to maxwell/core/fields.py
    - maxwell/em/induction.py now imports from maxwell/magnetics/

Action Required:
  - Update import statements in 3 physics modules
  - Regenerate physics implementation templates
```

### Dry Run Output

```
Sync Dry Run - No Changes Made
==============================

Agents to Update: 7
Changes to Distribute: 15

PHYSICUS:
  Would receive: 15 changes
  Files to update: 8

MATHEMATICA:
  Would receive: 5 changes
  Files to update: 3

[... remaining agents ...]

To perform actual sync, run without --dry-run
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All agents synchronized successfully |
| 1 | Sync completed with errors (some agents failed) |
| 2 | Sync completed with warnings (verification issues) |
| 3 | Configuration error (missing agent files) |

## Examples

```bash
# Full agent sync
architectus sync-agents

# Sync specific agent
architectus sync-agents --agent PHYSICUS

# Dry run first
architectus sync-agents --dry-run
architectus sync-agents  # If dry run looks good

# Force sync
architectus sync-agents --force

# Verify after sync
architectus sync-agents --verify
```

## Related Commands

- `validate-architecture` - Validate architecture before sync
- `pipeline-orchestrate` - Orchestrate pipeline after sync
- `check-dependencies` - Verify dependencies after sync

## Integration

### CI/CD Pipeline

```yaml
- name: Sync Agents After Architecture Change
  run: architectus sync-agents --verify --output json --report sync_report.json
  
- name: Verify Agent Knowledge
  run: |
    agents_synced=$(jq '.agents | map(select(.status == "updated")) | length' sync_report.json)
    if [ "$agents_synced" != "7" ]; then
      echo "Not all agents synchronized!"
      exit 1
    fi
```

### Pre-Commit Hook

```bash
#!/bin/bash
# Check if architecture files changed
if git diff --cached --name-only | grep -q "Architecture_COMPLETE"; then
  echo "Architecture changed, syncing agents..."
  architectus sync-agents --verify
fi
```

## Implementation Notes

This command:
1. Detects architecture document changes
2. Identifies affected agents
3. Generates change notifications
4. Updates agent knowledge files
5. Verifies sync completion
6. Generates detailed sync reports

## Agent Knowledge Files

Each agent maintains architecture knowledge:

```
agents/
  physicus/
    data/
      architecture-knowledge.md  # Physics domain boundaries
  mathematica/
    data/
      architecture-knowledge.md  # Math layer mappings
  [... each agent ...]
```

## Sync Triggers

Automatic sync is triggered by:
- Architecture COMPLETE document updates
- Layer numbering changes
- Module boundary changes
- New agent registration

## Version Tracking

Architecture versions follow semver:
- MAJOR: Breaking changes (layer renumbering)
- MINOR: New layers or modules
- PATCH: Article mapping corrections

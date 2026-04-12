# Task: Architecture Version Bump

## Description

Version management for architecture changes across all 6 Parts of Maxwell's Treatise. This task handles version numbering, changelog generation, and agent synchronization when architecture changes are made.

## Workflow

### Step 1: Change Assessment

Categorize architecture changes:
1. **MAJOR**: Breaking changes (layer renumbering, part restructuring)
2. **MINOR**: New layers, new modules, new articles added
3. **PATCH**: Article mapping corrections, documentation fixes

### Step 2: Version Number Calculation

Apply semantic versioning:
- Current version: `MAJOR.MINOR.PATCH`
- MAJOR change: `(MAJOR+1).0.0`
- MINOR change: `MAJOR.(MINOR+1).0`
- PATCH change: `MAJOR.MINOR.(PATCH+1)`

### Step 3: Version File Updates

Update version in all files:
1. Architecture COMPLETE documents (front-matter)
2. Agent configuration files
3. Package version files
4. Documentation version references

### Step 4: Changelog Generation

Generate changelog entry:
1. Date and version number
2. Change category (MAJOR/MINOR/PATCH)
3. Detailed change list by Part
4. Affected modules list
5. Migration notes (if MAJOR)

### Step 5: Agent Synchronization

Notify all agents:
1. Send version update notification
2. Provide changelog to each agent
3. Queue agent knowledge updates
4. Verify sync completion

### Step 6: Git Tagging

Create git tag:
1. Create annotated tag: `architecture-v{MAJOR}.{MINOR}.{PATCH}`
2. Sign tag with architect key
3. Push tag to remote
4. Create release notes

## Input

- Architecture change specification
- Current architecture version
- List of changed files
- Change description

## Output

### Primary Deliverable

`CHANGELOG.md` entry with:
```markdown
## [2.1.0] - 2026-04-11

### MINOR Changes
- Added Layer 67b: Advanced wave propagation modules
- Added 12 new articles to Part VI coverage
- Refactored Part IV module boundaries

### Affected Parts
- Part IV: Layers 65-67 refactored
- Part VI: Articles 801-812 mapped

### Migration Notes
No breaking changes. Backward compatible.

### Agent Updates
- PHYSICUS: Wave propagation module paths updated
- MATHEMATICA: No changes required
- QUALITAS: New test templates added
```

### Secondary Deliverables

- `version_info.json` - Version metadata
- `affected_modules.txt` - List of changed modules
- `migration_guide.md` - Migration instructions (if MAJOR)
- `git_tag.txt` - Tag creation confirmation

## Success Criteria

- [ ] Version number correctly incremented
- [ ] All files updated with new version
- [ ] Changelog entry complete
- [ ] All agents synchronized
- [ ] Git tag created
- [ ] Release notes published

## Estimated Duration

- PATCH bump: 30 minutes
- MINOR bump: 1-2 hours
- MAJOR bump: 4-8 hours (includes migration guide)

## Related Commands

- `sync-agents` - Agent synchronization
- `validate-architecture` - Post-bump validation

## Related Templates

- `version-change-log.md` - Version history template
- `agent-coordination.md` - Agent coordination template

## Version History Format

```markdown
## Version History

| Version | Date | Type | Changes |
|---------|------------|--------|------------------------------------------|
| 2.1.0 | 2026-04-11 | MINOR | Layer 67b added, Part VI expanded |
| 2.0.0 | 2026-01-15 | MAJOR | Complete architecture revision |
| 1.5.3 | 2025-12-01 | PATCH | Article mapping corrections |
| 1.5.0 | 2025-11-15 | MINOR | Part V system core added |
| 1.0.0 | 2025-01-01 | MAJOR | Initial architecture release |
```

## Example Output

```
Architecture Version Bump Complete
===================================

Previous Version: 2.0.0
New Version: 2.1.0
Change Type: MINOR

FILES UPDATED
-------------
[✓] Maxwell_Treatise_Part_IV_Architecture_COMPLETE.md
[✓] Maxwell_Treatise_Part_VI_Architecture_COMPLETE.md
[✓] agents/architectus/agent.md
[✓] agents/physicus/agent.md
[✓] CHANGELOG.md

CHANGELOG ENTRY
---------------
## [2.1.0] - 2026-04-11

### MINOR Changes
- Added Layer 67b: Advanced wave propagation modules
- Added 12 new articles to Part VI coverage

AGENT SYNC STATUS
-----------------
[✓] PHYSICUS - Synchronized
[✓] MATHEMATICA - Synchronized
[✓] QUALITAS - Synchronized
[✓] SCRIBA - Synchronized
[✓] All other agents - Synchronized

GIT TAG
-------
Tag: architecture-v2.1.0
Created: 2026-04-11T14:30:00Z
Pushed: origin/architecture-v2.1.0

NEXT STEPS
----------
1. Monitor agent implementations
2. Verify no breaking changes
3. Update documentation references
```

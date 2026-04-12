# Data: documentation-standards-guide

## Purpose

Comprehensive guide for documentation standards across the Maxwell Treatise Modernization Project.

---

## Documentation Hierarchy

### Level 1: Agent Documentation

| Component | Purpose | Location |
|-----------|---------|----------|
| agent.md | Agent definition and persona | agents/{name}/agent.md |
| commands/ | Agent capabilities | agents/{name}/commands/*.md |
| tasks/ | Workflows and processes | agents/{name}/tasks/*.md |

### Level 2: Support Infrastructure

| Component | Purpose | Location |
|-----------|---------|----------|
| templates/ | Reusable document structures | agents/{name}/templates/*.md |
| checklists/ | Validation criteria | agents/{name}/checklists/*.md |
| data/ | Reference information | agents/{name}/data/*.md |

### Level 3: Utilities

| Component | Purpose | Location |
|-----------|---------|----------|
| utils/ | Code utilities and helpers | agents/{name}/utils/*.md |

---

## Document Structure Standards

### YAML Frontmatter

All Markdown documents MUST include YAML frontmatter:

```yaml
---
type: [document_type]
version: "X.Y.Z"
created: YYYY-MM-DD
modified: YYYY-MM-DD
author: [Author Name]
reviewer: [Reviewer Name]
status: [draft | review | approved]
maxwell_articles: [Art. XXX-XXX]
cgs_units: [true | false]
theory_classification: [maxwell_original | user_original | standard_math]
---
```

### Required Sections

| Document Type | Required Sections |
|---------------|-------------------|
| Command | Purpose, Usage, Parameters, Examples |
| Task | Purpose, Workflow, Inputs, Outputs, Validation |
| Template | Purpose, Variables, Instructions, Examples |
| Checklist | Purpose, Levels, Criteria, Scoring |
| Data | Purpose, Reference Data, Sources |
| Utility | Purpose, Functions, Examples |

### Section Heading Hierarchy

```markdown
# H1: Document Title

## H2: Major Section

### H3: Subsection

#### H4: Detail

##### H5: Fine Detail (rarely used)
```

---

## Writing Standards

### Tone and Style

| Aspect | Standard |
|--------|----------|
| Voice | Active voice preferred |
| Person | Third person for technical content |
| Tense | Present tense for descriptions |
| Clarity | Concise, unambiguous language |

### Technical Precision

| Requirement | Standard |
|-------------|----------|
| CGS Units | ALWAYS primary (SI reference only) |
| Maxwell Citations | Accurate article numbers |
| Theory Classification | Clearly marked |
| Code Examples | Executable and tested |

### Terminology

| Term | Usage |
|------|-------|
| Maxwell's Treatise | The 1873 work by J.C. Maxwell |
| CGS units | Centimeter-gram-second system |
| maxwell_original | Directly from Maxwell's 1873 text |
| user_original | User's theoretical extensions (authoritative) |
| standard_math | Standard mathematical implementations |

---

## CGS Unit Standards

### Primary Rule

**ALL electrical quantities MUST use CGS units as primary:**

| Quantity | CGS Unit | SI Equivalent (reference only) |
|----------|----------|-------------------------------|
| Potential | statvolt (statV) | 299.79 V |
| Current | statampere (statA) | 3.336×10^-10 A |
| Resistance | statohm (statΩ) | 8.988×10^11 Ω |
| Charge | statcoulomb (statC) | 3.336×10^-10 C |
| Capacitance | statfarad (statF) | 1.113×10^-12 F |
| Magnetic field B | gauss (G) | 10^-4 T |
| Magnetic field H | oersted (Oe) | 79.577 A/m |

### Physical Constants

**Use these CGS values:**

```python
# Physical constants in CGS
c = 2.99792458e10      # cm/s (speed of light)
k_B = 1.381e-16        # erg/K (Boltzmann constant)
e = 4.803e-10          # statC (elementary charge)
h = 6.626e-27          # erg·s (Planck constant)
```

### Unit Notation

| Rule | Example |
|------|---------|
| No period after unit symbol | statV (not statV.) |
| Space between value and unit | 100 statV (not 100statV) |
| Lowercase unit names | statvolt, statampere |
| Capitalized symbols | statV, statA, statΩ |

---

## Maxwell Citation Standards

### Citation Format

**Full citation (first use):**
```
Maxwell, J.C. (1873). A Treatise on Electricity and Magnetism 
(3rd ed.). Clarendon Press, Oxford. Part IV, Art. 730-750.
```

**In-text citation:**
```
(Maxwell, 1873, Art. 730-750)
Maxwell (1873, Art. 730-750)
```

**Short form (subsequent):**
```
(Maxwell, Art. 730-750)
Maxwell, Art. 730-750
```

### Article Reference Format

| Format | Usage |
|--------|-------|
| Art. 730 | Single article |
| Art. 730-750 | Article range |
| Art. 730, 735, 742 | Multiple articles |
| Part IV, Art. 730-750 | Part + articles |

### Article Range Reference

| Part | Articles | Topic |
|------|----------|-------|
| Part I | Art. 1-229 | Electrostatics |
| Part II | Art. 230-370 | Electrokinematics |
| Part III | Art. 371-474 | Magnetism |
| Part IV | Art. 475-866 | Electromagnetism |

---

## Theory Classification Standards

### Classification Categories

| Classification | Description | Protection Level |
|----------------|-------------|------------------|
| maxwell_original | Maxwell's 1873 Treatise text | Historical accuracy |
| user_original | User's theoretical extensions | **NEVER ALTER** |
| standard_math | Standard mathematical implementations | Technical accuracy |

### Marking Requirements

**Every theoretical component MUST be classified:**

```markdown
**Theory Classification:** user_original

This extension builds upon Maxwell's Art. 730-750 by...

[Note: This is the user's authoritative theoretical contribution]
```

### User Original Protection

**CRITICAL REQUIREMENTS:**

1. **NEVER** alter user_original content
2. **NEVER** falsify user_original content
3. **NEVER** misrepresent user_original content
4. **NEVER** confuse user_original with Maxwell's text
5. **ALWAYS** maintain user_original authoritative status

---

## Code Documentation Standards

### Function Documentation

```python
def function_name(param1, param2):
    """
    Brief description of function purpose.
    
    Args:
        param1: Description with units (CGS)
        param2: Description with units (CGS)
    
    Returns:
        Description of return value with units (CGS)
    
    Maxwell Reference: Art. XXX-XXX
    
    Example:
        >>> result = function_name(100, 4.0)
        >>> print(result)
        25.0 statV/cm
    """
```

### Code Examples

```python
# CGS units example
# Calculate galvanometer sensitivity
N = 100              # Number of turns
A = 4.0              # cm² (coil area)
B = 2000             # gauss (magnetic field)
kappa = 0.1          # dyne·cm/rad (spring constant)

S_I = (N * A * B) / kappa  # cm/statA
print(f"Current sensitivity: {S_I:.2e} cm/statA")
```

### Output Examples

```
Current sensitivity: 8.00e+06 cm/statA

The reported uncertainty is the expanded uncertainty with 
coverage factor k = 2.00, providing approximately 95% 
level of confidence.
```

---

## Template Standards

### Template Structure

```markdown
# Template: {template-name}

## Purpose

{Brief description of template purpose}

## Applicability

{When to use this template}

---

## YAML Frontmatter

```yaml
{Required frontmatter fields}
```

---

## LLM Instructions

{Instructions for using the template}

---

## Template Structure

{Template sections and variables}

---

## Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| {{VAR}} | Description | Yes/No | Value |

---

## Conditional Logic

{Conditional inclusion rules}

---

## Quality Criteria

- [ ] Criterion 1
- [ ] Criterion 2
```

### Variable Notation

| Notation | Usage |
|----------|-------|
| {{VARIABLE}} | Required variable |
| {{VARIABLE}} | Optional variable |
| {{VARIABLE}} | Auto-generated |

---

## Checklist Standards

### Checklist Structure

```markdown
# Checklist: {checklist-name}

## Purpose

{Purpose of the checklist}

---

## Level 1: Category Name (Required)

### Criterion Group

- [ ] Criterion 1
- [ ] Criterion 2

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / X

**Level 1 Total:** ___ / X points

---

## Summary

| Level | Category | Score | Max | Percentage |
|-------|----------|-------|-----|------------|
| 1 | Category 1 | ___ | X | ___% |
| **TOTAL** | | **___** | **X** | **___%** |

### Approval Status

**Status:** [ ] Approved [ ] Conditional [ ] Rejected
```

### Scoring System

| Level | Type | Weight |
|-------|------|--------|
| Level 1 | Required | 1.0x |
| Level 2 | Required | 1.0x |
| Level 3 | Expert | 0.5x |
| Level 4 | Expert | 0.5x |
| Level 5 | Expert | 0.5x |

### Approval Thresholds

| Status | Threshold |
|--------|-----------|
| Approved | >= 90% |
| Conditional | 75-89% |
| Rejected | < 75% |

---

## Version Control Standards

### Version Numbering

```
MAJOR.MINOR.PATCH

MAJOR: Incompatible API changes
MINOR: Backward-compatible features
PATCH: Backward-compatible bug fixes
```

### Change Categories

| Category | Description |
|----------|-------------|
| Added | New features |
| Changed | Modified existing |
| Fixed | Bug fixes |
| Deprecated | Marked for removal |
| Removed | Deleted features |
| Security | Security fixes |
| CGS | CGS unit changes |
| Maxwell | Citation changes |

### Release Notes Format

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Summary

{Brief summary}

### Added

- {Added item}

### Changed

- {Changed item}

### Fixed

- {Fixed item}

### CGS Units

- {CGS unit changes}

### Maxwell Articles

- Coverage added: Art. XXX-XXX
```

---

## Quality Criteria

- [ ] All documents follow structure standards
- [ ] CGS units used consistently
- [ ] Maxwell citations accurate
- [ ] Theory classification correct
- [ ] User_original protected (NEVER ALTERED)

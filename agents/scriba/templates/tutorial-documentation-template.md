# Template: tutorial-documentation-template

## Purpose

Standardized template for creating educational tutorials and how-to guides.

## Applicability

User tutorials, getting started guides, workflow tutorials, educational materials

---

## YAML Frontmatter

```yaml
documentation_type: tutorial
version: "{{VERSION}}"
difficulty_level: "{{DIFFICULTY}}"
estimated_time: "{{ESTIMATED_TIME}}"
maxwell_articles: "{{MAXWELL_ARTICLES}}"
prerequisites:
  {{PREREQUISITES}}
learning_objectives:
  {{LEARNING_OBJECTIVES}}
cgs_units_required: true
```

---

## LLM Instructions

You are creating a tutorial for the Maxwell Treatise Modernization Project. Follow these guidelines:

1. **Educational Approach**: Build understanding progressively from fundamentals
2. **CGS Units**: All calculations MUST use CGS units, explaining Maxwell's choice
3. **Historical Context**: Connect modern implementations to Maxwell's 1873 text
4. **Hands-On Examples**: Provide executable examples with expected outputs
5. **Theory Classification**: Distinguish Maxwell's original, user extensions, and standard implementations
6. **Clear Prerequisites**: State what knowledge is required before starting

---

## Template Structure

### Tutorial Title and Introduction

```markdown
# Tutorial: {{TUTORIAL_TITLE}}

## Overview

{{TUTORIAL_OVERVIEW}}

**Difficulty:** {{DIFFICULTY_LEVEL}}  
**Estimated Time:** {{ESTIMATED_TIME}}  
**Prerequisites:** {{PREREQUISITES}}

## Learning Objectives

After completing this tutorial, you will be able to:

1. {{OBJECTIVE_1}}
2. {{OBJECTIVE_2}}
3. {{OBJECTIVE_3}}

## Maxwell's Historical Context

{{HISTORICAL_CONTEXT}}

Maxwell's original treatment can be found in **{{MAXWELL_ARTICLES}}**.
```

### Background Theory

```markdown
## Background Theory

### Maxwell's Formulation

{{MAXWELL_THEORY}}

**In CGS units:**
```python
# Maxwell's equation in CGS
{{MAXWELL_CGS_EQUATION}}
```

### Modern Implementation

{{MODERN_IMPLEMENTATION}}

**Note:** This implementation is classified as:
- [ ] `maxwell_original` - Directly from Maxwell's 1873 text
- [ ] `user_original` - User's theoretical extension (authoritative)
- [ ] `standard_math` - Standard mathematical implementation
```

### Step-by-Step Instructions

```markdown
## Step 1: {{STEP_1_TITLE}}

{{STEP_1_DESCRIPTION}}

**Code:**
```python
{{STEP_1_CODE}}
```

**Expected Output:**
```
{{STEP_1_OUTPUT}}
```

**Explanation:**
{{STEP_1_EXPLANATION}}

## Step 2: {{STEP_2_TITLE}}

{{STEP_2_DESCRIPTION}}

...
```

### Complete Example

```markdown
## Complete Example

Here's a complete working example:

```python
{{COMPLETE_CODE}}
```

**Output:**
```
{{COMPLETE_OUTPUT}}
```

**CGS Units Used:**
| Quantity | CGS Unit | SI Equivalent |
|----------|----------|---------------|
| {{quantity}} | {{cgs_unit}} | {{si_unit}} |
```

### Exercises

```markdown
## Exercises

### Exercise 1: {{EXERCISE_1_TITLE}}

{{EXERCISE_1_DESCRIPTION}}

**Hint:** {{EXERCISE_1_HINT}}

**Solution:**
```python
{{EXERCISE_1_SOLUTION}}
```
```

### Summary

```markdown
## Summary

In this tutorial, you learned to:

- {{SUMMARY_POINT_1}}
- {{SUMMARY_POINT_2}}
- {{SUMMARY_POINT_3}}

## Next Steps

- [{{RELATED_TUTORIAL_1}}]({{LINK_1}})
- [{{RELATED_TUTORIAL_2}}]({{LINK_2}})

## References

- Maxwell, J.C. (1873). Art. {{ARTICLE_RANGE}}: {{TOPIC}}
- {{ADDITIONAL_REFERENCE}}
```

---

## Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `{{VERSION}}` | Tutorial version | Yes | - |
| `{{DIFFICULTY}}` | Beginner/Intermediate/Advanced | Yes | - |
| `{{ESTIMATED_TIME}}` | Time to complete | Yes | - |
| `{{MAXWELL_ARTICLES}}` | Article citations | Yes | - |
| `{{PREREQUISITES}}` | Required knowledge | Yes | - |
| `{{LEARNING_OBJECTIVES}}` | What will be learned | Yes | - |
| `{{TUTORIAL_TITLE}}` | Tutorial title | Yes | - |
| `{{TUTORIAL_OVERVIEW}}` | Brief overview | Yes | - |
| `{{HISTORICAL_CONTEXT}}` | Maxwell's historical background | Yes | - |
| `{{MAXWELL_THEORY}}` | Theoretical background | Yes | - |
| `{{MAXWELL_CGS_EQUATION}}` | Equation in CGS | Yes | - |
| `{{STEP_N_TITLE}}` | Step title | Yes | - |
| `{{STEP_N_DESCRIPTION}}` | Step description | Yes | - |
| `{{STEP_N_CODE}}` | Code for step | Yes | - |
| `{{STEP_N_OUTPUT}}` | Expected output | Yes | - |
| `{{COMPLETE_CODE}}` | Full working example | Yes | - |
| `{{COMPLETE_OUTPUT}}` | Full output | Yes | - |
| `{{EXERCISE_N_TITLE}}` | Exercise title | Conditional | - |
| `{{EXERCISE_N_DESCRIPTION}}` | Exercise description | Conditional | - |
| `{{EXERCISE_N_HINT}}` | Exercise hint | Conditional | - |
| `{{EXERCISE_N_SOLUTION}}` | Exercise solution | Conditional | - |

---

## Conditional Logic

### Include Historical Context If:

```
IF tutorial_has_maxwell_connection:
  INCLUDE historical_context_section
  INCLUDE maxwell_article_citations
ELSE:
  BRIEF reference to applicable articles
```

### Include Exercises If:

```
IF difficulty_level IN ["Intermediate", "Advanced"]:
  INCLUDE exercises_section
  INCLUDE hints_and_solutions
ELSE IF difficulty_level == "Beginner":
  INCLUDE guided_practice_only
```

### Include CGS Unit Table If:

```
IF tutorial_involves_calculations:
  INCLUDE cgs_units_table
  INCLUDE si_equivalents (reference only)
```

### Include Theory Classification If:

```
IF uses_user_extensions OR uses_standard_implementations:
  INCLUDE theory_classification_box
  EXPLAIN classification clearly
```

---

## Difficulty Levels

### Beginner

- No prerequisites beyond basic physics
- Step-by-step guidance
- All code provided
- Focus on concepts and usage

### Intermediate

- Requires basic CGS unit familiarity
- Some derivation expected
- Partial code provided
- Focus on application

### Advanced

- Requires Maxwell treatise familiarity
- Full derivations expected
- Code frameworks only
- Focus on extension and research

---

## Quality Criteria

### Content Quality

- [ ] Learning objectives clearly stated
- [ ] Prerequisites accurately specified
- [ ] Steps are logically ordered
- [ ] Explanations are clear and complete

### Technical Quality

- [ ] All code examples are executable
- [ ] All outputs are verified
- [ ] CGS units used consistently
- [ ] Maxwell articles correctly cited

### Educational Quality

- [ ] Concepts build progressively
- [ ] Examples reinforce learning
- [ ] Exercises test understanding
- [ ] Summary reinforces key points

### Theory Classification

- [ ] Maxwell's original text identified
- [ ] User extensions marked (NOT ALTERED)
- [ ] Standard implementations marked
- [ ] No misrepresentation of theories

---

## Output Format

Tutorial should be:
- Markdown format
- Clear hierarchical headings
- Numbered steps
- Code blocks with syntax highlighting
- Tables for reference data
- Links to related tutorials

---

## Maxwell Article Quick Reference

| Tutorial Topic | Articles | Description |
|----------------|----------|-------------|
| Electrostatics | Art. 1-229 | Electric fields, potential |
| Magnetism | Art. 371-474 | Magnetic fields, induction |
| Electromagnetism | Art. 475-866 | EM force, galvanometers |
| Circuits | Art. 287-300 | Networks, Ohm's law |
| Bridges | Art. 343-348 | Wheatstone bridge |
| Instruments | Art. 730-750 | Galvanometer design |

---

## Related Templates

- `{{api-documentation-template.md}}` - API reference
- `{{cross-reference-template.md}}` - Citation linking
- `{{release-notes-template.md}}` - Version changes

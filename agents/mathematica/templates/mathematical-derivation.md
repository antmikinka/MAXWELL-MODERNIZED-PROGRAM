# Template: mathematical-derivation

## Description

Template for documenting mathematical derivations with full citation tracking to Maxwell's original articles. This template ensures derivations are reproducible and traceable.

## Structure

```markdown
# Mathematical Derivation: {title}

## Maxwell Article References
{citation_list}

## Problem Statement
{clear_statement_of_what_is_being_derived}

## Starting Equations
{list_of_fundamental_equations_with_citations}

## Derivation Steps

### Step 1: {step_name}
{mathematical_operation}
{justification}
{result}

### Step 2: {step_name}
...

## Final Result
{final_equation}

## Verification
- [ ] Dimensional analysis check
- [ ] Limiting case verification
- [ ] Comparison with known results
- [ ] Numerical validation

## Implementation Notes
{python_implementation_details}

## Related Derivations
{links_to_related_derivations}
```

## LLM Instructions

When using this template:

1. **Citation First**: Always identify relevant Maxwell articles before beginning
2. **Step by Step**: Each derivation step must be clearly justified
3. **Verification Required**: Include at least two verification methods
4. **Implementation Link**: Connect to actual Python implementation

## Variables

- `{title}`: Derivation title
- `{citation_list}`: List of Maxwell article citations
- `{clear_statement_of_what_is_being_derived}`: Problem description
- `{list_of_fundamental_equations_with_citations}`: Starting point equations
- `{step_name}`: Descriptive name for each derivation step
- `{mathematical_operation}`: The mathematical operation performed
- `{justification}`: Why this operation is valid
- `{result}`: Result after this step
- `{final_equation}`: The derived equation
- `{python_implementation_details}`: Implementation notes
- `{links_to_related_derivations}`: Cross-references

## Conditional Logic

IF derivation involves vector calculus:
  INCLUDE vector identity verification
  ADD coordinate system specification

IF derivation involves special functions:
  INCLUDE function definitions
  ADD recurrence relation verification

IF derivation is used in multiple parts:
  INCLUDE cross-part dependency list
  ADD usage examples from each part

## Example Usage

```markdown
# Mathematical Derivation: Electric Field of a Dipole

## Maxwell Article References
- Article 69-71: Electric potential
- Article 113-116: Dipole fields

## Problem Statement
Derive the electric field E from a point dipole with moment p.

## Starting Equations
- Potential of point dipole: φ = (p·r)/r³ (Art. 70)
- Electric field: E = -∇φ (Art. 24)

## Derivation Steps
...
```

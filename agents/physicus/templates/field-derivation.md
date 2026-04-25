# Template: field-derivation

## Description

Template for documenting electromagnetic field derivations with full citation tracking to Maxwell's original articles. This template ensures derivations are physically sound and traceable.

## Structure

```markdown
# Field Derivation: {title}

## Maxwell Article References
{citation_list}

## Part and Layer
- **Part:** {part_name}
- **Layer:** {layer_number}

## Problem Statement
{clear_statement_of_what_is_being_derived}

## Starting Equations
{list_of_fundamental_equations_with_citations}

## Physical Assumptions
- {assumption_1}
- {assumption_2}
- {assumption_3}

## Derivation Steps

### Step 1: {step_name}
**Physical Justification:** {why_this_step}

{mathematical_operation}

**Result:**
{intermediate_result}

### Step 2: {step_name}
...

## Final Result
{final_equation}

## Physical Interpretation
{what_the_result_means_physically}

## Limiting Cases
- {limit_1}: {behavior}
- {limit_2}: {behavior}

## Verification
- [ ] Dimensional analysis check (CGS)
- [ ] Limiting case verification
- [ ] Comparison with known results
- [ ] Numerical validation
- [ ] Energy conservation (if applicable)

## Relation to Maxwell's Text
{how_this_derivation_relates_to_maxwell_original}

## Modern Context
{comparison_with_modern_formulations}

## Implementation Notes
{python_implementation_details}

## Related Derivations
{links_to_related_derivations}
```

## LLM Instructions

When using this template:

1. **Start from Maxwell's Equations**: Always trace back to fundamental equations
2. **Document Each Step**: Physical justification for each mathematical operation
3. **CGS Units**: Ensure dimensional consistency in CGS throughout
4. **Theory Preservation**: Never alter user's original theoretical extensions
5. **Cross-Reference**: Link to related derivations and implementations

## Variables

- `{title}`: Derivation title
- `{citation_list}`: Maxwell article citations
- `{part_name}`: Electrostatics, Electrokinematics, Magnetism, Electromagnetism
- `{layer_number}`: Architecture layer
- `{clear_statement}`: What is being derived
- `{fundamental_equations}`: Starting equations with citations
- `{assumptions}`: Physical and mathematical assumptions
- `{step_name}`: Descriptive name for each step
- `{physical_justification}`: Why this operation is valid
- `{mathematical_operation}`: The mathematics performed
- `{intermediate_result}`: Result after step
- `{final_equation}`: The derived equation
- `{physical_interpretation}`: What the result means
- `{limiting_cases}`: Behavior in limits
- `{maxwell_original}`: How Maxwell derived this
- `{modern_context}`: Comparison with SI/modern notation

## Conditional Logic

IF derivation involves time-dependence:
  INCLUDE discussion of causality
  ADD frequency domain equivalent

IF derivation involves boundaries:
  INCLUDE boundary condition discussion
  ADD surface term handling

IF derivation involves approximations:
  DOCUMENT validity range
  INCLUDE error order estimate

IF derivation leads to implementation:
  INCLUDE code reference
  ADD numerical considerations

## Example Usage

```markdown
# Field Derivation: Electric Field of a Dipole

## Maxwell Article References
- Articles 69-71: Electric potential
- Articles 113-116: Dipole fields

## Part and Layer
- **Part:** I (Electrostatics)
- **Layer:** 4

## Problem Statement
Derive the electric field E from a point dipole with moment p located at the origin.

## Starting Equations
- Potential of point dipole: φ = (p·r)/r³ (Art. 70)
- Electric field: E = -∇φ (Art. 24)

## Physical Assumptions
- Point dipole limit (dipole size → 0)
- Static fields (no time dependence)
- Vacuum (no dielectric)

## Derivation Steps

### Step 1: Express potential in coordinates
**Physical Justification:** Need explicit form for gradient operation

φ(r) = (p·r)/r³ = (p_x x + p_y y + p_z z) / (x² + y² + z²)^(3/2)

**Result:** Potential in Cartesian form

### Step 2: Compute gradient
**Physical Justification:** E = -∇φ by definition

∇φ = ∂φ/∂x x̂ + ∂φ/∂y ŷ + ∂φ/∂z ẑ

For ∂φ/∂x:
∂φ/∂x = p_x/r³ - 3(p·r)x/r⁵

**Result:** ∇φ = p/r³ - 3(p·r)r/r⁵

### Step 3: Apply negative sign
E = -∇φ = 3(p·r̂)r̂/r³ - p/r³

**Result:** E = (3(p·r̂)r̂ - p)/r³

## Final Result
E(r) = [3(p·r̂)r̂ - p] / r³

In dyadic notation: E = (3r̂r̂ - I)·p / r³

## Physical Interpretation
- Field falls off as 1/r³ (faster than point charge 1/r²)
- Field has angular dependence through r̂
- On axis (r̂ || p): E = 2p/r³
- Perpendicular (r̂ ⊥ p): E = -p/r³

## Limiting Cases
- r → 0: Singular (point dipole approximation breaks)
- r → ∞: Dominant term for any localized charge distribution

## Verification
- [x] Dimensional analysis: [p] = statcoulomb·cm, [E] = statvolt/cm ✓
- [x] On-axis matches known result
- [x] ∇ × E = 0 (electrostatic)
- [x] Flux through sphere = 0 (no net charge)

## Relation to Maxwell's Text
Maxwell derives this in Articles 113-116 using spherical harmonics.
This derivation uses direct vector calculus for clarity.

## Modern Context
Same result in SI units: E = (1/4πε₀)(3(p·r̂)r̂ - p)/r³

## Implementation Notes
See: `maxwell/physics/electrostatics/dipole.py::electric_field_dipole`

## Related Derivations
- Potential of arbitrary charge distribution
- Magnetic dipole field
- Quadrupole field expansion
```

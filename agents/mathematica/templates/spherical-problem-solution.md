# Template: spherical-problem-solution

## Description

Template for solving boundary value problems using spherical harmonics. This template provides a systematic approach to problems with spherical symmetry.

## Structure

```markdown
# Spherical Harmonic Solution: {problem_name}

## Problem Definition

### Geometry
{description_of_spherical_geometry}

### Boundary Conditions
{specified_boundary_conditions}

### Symmetry Properties
{axial|full|no symmetry}

## Solution Method

### Harmonic Selection
{which_harmonics_are_needed}

### General Solution Form
φ(r,θ,φ) = Σ(l,m) [A_lm r^l + B_lm r^{-(l+1)}] Y_l^m(θ,φ)

### Coefficient Determination
{method_for_finding_coefficients}

## Solution

### Interior Solution (r < R)
φ_in(r,θ,φ) = {solution}

### Exterior Solution (r > R)
φ_out(r,θ,φ) = {solution}

### Matching Conditions
{continuity_conditions_at_boundaries}

## Verification

### Boundary Condition Check
- [ ] φ matches at r = R
- [ ] ∂φ/∂r discontinuity matches surface charge
- [ ] Regularity at origin (if applicable)
- [ ] Decay at infinity (if applicable)

### Physical Interpretation
{multipole_expansion_interpretation}

## Implementation

```python
{python_implementation}
```

## Maxwell Article References
{relevant_articles}
```

## LLM Instructions

When using this template:

1. **Identify Symmetry**: Determine which harmonics are needed
2. **General Solution**: Write general form with unknown coefficients
3. **Apply BCs**: Systematically apply boundary conditions
4. **Verify**: Check all physical requirements
5. **Interpret**: Provide multipole interpretation

## Variables

- `{problem_name}`: Name of the problem
- `{description_of_spherical_geometry}`: Geometry description
- `{specified_boundary_conditions}`: BC specification
- `{axial|full|no symmetry}`: Symmetry type
- `{which_harmonics_are_needed}`: Harmonic selection
- `{method_for_finding_coefficients}`: Coefficient method
- `{solution}`: Final solution expression
- `{continuity_conditions_at_boundaries}`: Matching conditions
- `{python_implementation}`: Code implementation
- `{relevant_articles}`: Maxwell citations

## Conditional Logic

IF problem has axial symmetry:
  USE only m=0 harmonics (Legendre polynomials)
  SIMPLIFY to P_l(cos θ) expansion

IF problem involves surface charge:
  INCLUDE discontinuity in normal derivative
  RELATE to surface charge density

IF problem has multiple spherical boundaries:
  USE separate expansions for each region
  MATCH at each interface

## Example Usage

```markdown
# Spherical Harmonic Solution: Conducting Sphere in Uniform Field

## Problem Definition
- Conducting sphere of radius R
- Uniform external field E₀ in z-direction
- Sphere held at zero potential

## Solution
φ(r,θ) = -E₀ r cos θ + E₀ R³ cos θ / r²  (r > R)
φ(r,θ) = 0  (r < R)

## Maxwell Article References
- Article 140-145: Spherical harmonic applications
```

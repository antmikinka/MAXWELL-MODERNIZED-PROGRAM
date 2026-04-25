# Template: analytical-solution

## Description

Template for documenting analytical solutions to electromagnetic problems. These closed-form solutions serve as validation benchmarks and provide physical insight.

## Structure

```markdown
# Analytical Solution: {problem_name}

## Maxwell Article References
{citation_list}

## Classification
- **Part:** {part_name}
- **Layer:** {layer_number}
- **Geometry:** {geometry_type}
- **Method:** {solution_method}

## Problem Statement
{precise_mathematical_statement}

## Geometry
{diagram_description}
{coordinate_system}

## Governing Equation
{differential_equation}
{boundary_conditions}

## Solution Method
{technique_used}

### Step 1: {method_step}
{description}

### Step 2: {method_step}
{description}

## Final Solution
{closed_form_solution}

## Field Components
{explicit_field_expressions}

## Derived Quantities
- Energy: {energy_expression}
- Force: {force_expression}
- Capacitance/Inductance: {circuit_parameter}

## Validation
- [ ] Satisfies governing equation
- [ ] Satisfies boundary conditions
- [ ] Correct limiting behavior
- [ ] Dimensional consistency (CGS)
- [ ] Energy conservation

## Limiting Cases
- {limit_1}: {behavior}
- {limit_2}: {behavior}

## Numerical Implementation
```python
{python_implementation}
```

## Example Calculation
{worked_example}

## Related Solutions
{cross_references}
```

## LLM Instructions

When using this template:

1. **Complete Statement**: Specify geometry, equations, and BCs precisely
2. **Solution Method**: Document the mathematical technique used
3. **Explicit Forms**: Give complete closed-form expressions
4. **CGS Units**: Ensure all expressions use CGS consistently
5. **Validation**: Verify solution satisfies all conditions

## Variables

- `{problem_name}`: Descriptive name
- `{geometry_type}`: Sphere, cylinder, plane, etc.
- `{solution_method}`: Separation of variables, images, etc.
- `{differential_equation}`: Laplace, Poisson, wave, etc.
- `{boundary_conditions}`: All BCs specified
- `{closed_form_solution}`: Final analytical result
- `{explicit_field_expressions}`: E, B, V, A components

## Solution Categories

### Electrostatics
- Point charge, dipole, multipole
- Conducting sphere, cylinder, plane
- Dielectric sphere in uniform field
- Method of images configurations

### Magnetostatics
- Magnetic dipole
- Current loop (on and off axis)
- Solenoid (infinite and finite)
- Magnetic sphere in uniform field

### Time-Varying
- Plane wave solutions
- Waveguide modes
- Cavity resonances
- Radiation from antennas

## Example Usage

```markdown
# Analytical Solution: Conducting Sphere in Uniform Electric Field

## Maxwell Article References
- Articles 144-146: Spherical conductors
- Articles 155-160: Method of images

## Classification
- **Part:** I (Electrostatics)
- **Layer:** 10
- **Geometry:** Sphere
- **Method:** Separation of variables / Images

## Problem Statement
Find the electric potential and field for a grounded conducting sphere
of radius a placed in a uniform electric field E₀ in the z-direction.

## Geometry
- Sphere of radius a centered at origin
- Uniform field E₀ = E₀ ẑ at infinity
- Sphere at potential V = 0

Spherical coordinates (r, θ, φ) with θ measured from z-axis.

## Governing Equation
∇²V = 0 (Laplace equation, charge-free region)

Boundary Conditions:
1. V(r=a, θ) = 0 (grounded sphere)
2. V(r→∞) → -E₀ r cos(θ) (uniform field)
3. V finite everywhere except r→∞

## Solution Method
Separation of variables in spherical coordinates with azimuthal symmetry.
General solution: V = Σ(Aₗr^l + Bₗr^{-(l+1)}) Pₗ(cos θ)

### Step 1: Apply far-field condition
As r→∞: V → -E₀ r cos θ = -E₀ r P₁(cos θ)
Therefore only l=1 term survives at large r.

### Step 2: General l=1 solution
V(r,θ) = (A₁r + B₁/r²) cos θ

### Step 3: Apply boundary conditions
At r→∞: A₁ = -E₀
At r=a: V = 0 → -E₀ a + B₁/a² = 0 → B₁ = E₀ a³

## Final Solution
V(r,θ) = -E₀ (r - a³/r²) cos θ

## Field Components
E = -∇V

E_r = -∂V/∂r = E₀ (1 + 2a³/r³) cos θ
E_θ = -(1/r)∂V/∂θ = -E₀ (1 - a³/r³) sin θ
E_φ = 0

## Derived Quantities

### Induced Surface Charge
σ(θ) = (1/4π) E_r(r=a) = (3E₀/4π) cos θ

### Total Induced Dipole Moment
p = E₀ a³ (in z-direction)

### Far-Field Behavior (r >> a)
V ≈ -E₀ r cos θ + (E₀ a³/r²) cos θ
    = V_uniform + V_dipole

## Validation
- [x] ∇²V = 0 verified by direct substitution
- [x] V(a,θ) = 0 satisfied
- [x] V→∞ → -E₀ r cos θ satisfied
- [x] Dimensions: [V] = statvolt ✓
- [x] Energy: U = (1/8π)∫E² dV = (1/2)E₀² a³

## Limiting Cases
- r → a: E_r = 3E₀ cos θ, E_θ = 0 (perpendicular to surface)
- r → ∞: E → E₀ ẑ (uniform field)
- a → 0: V → -E₀ r cos θ (just uniform field)

## Numerical Implementation
```python
def conducting_sphere_uniform_field(E0, a, r, theta):
    """Potential of grounded sphere in uniform field."""
    if r < a:
        return 0  # Inside conductor, V = constant = 0
    return -E0 * (r - a**3 / r**2) * np.cos(theta)

def electric_field_sphere(E0, a, r, theta):
    """Electric field components."""
    if r < a:
        return np.array([0, 0])
    factor = a**3 / r**3
    E_r = E0 * (1 + 2*factor) * np.cos(theta)
    E_theta = -E0 * (1 - factor) * np.sin(theta)
    return np.array([E_r, E_theta])
```

## Example Calculation
For a = 1 cm, E₀ = 100 statvolt/cm:
- Maximum field: E_max = 3E₀ = 300 statvolt/cm at θ=0,π
- Induced dipole: p = 100 × 1³ = 100 statcoulomb·cm
- Surface charge at pole: σ = 3×100/(4π) ≈ 24 statcoulomb/cm²

## Related Solutions
- Point charge near conducting sphere (images)
- Dielectric sphere in uniform field
- Conducting cylinder in uniform field (2D analog)
```

# Command: derive-equations

## Description

Derives governing electromagnetic equations from Maxwell's original articles using systematic mathematical reasoning. This command traces the logical development of electromagnetic theory from fundamental principles to the complete field equations.

## Source Category

**CRITICAL: Theory Preservation**

This command implements:
- **Maxwell's 1873 Historical Text**: Derivations from Articles across all Parts (I-IV)
- **Standard Mathematical Implementation**: Vector calculus, tensor analysis, variational methods
- **User Original Theory**: NONE - if user provides extensions, label as "User Original Theory - Authoritative - DO NOT ALTER"

## Functionality

### Electrostatic Equation Derivations (Part I)

1. **Coulomb's Law from First Principles** (Arts. 66-68)
   ```
   F = q₁q₂/r² r̂  (CGS ESU)
   E = F/q₀ = q/r² r̂
   ```

2. **Gauss's Law Derivation** (Arts. 75-76)
   ```
   ∮ E · dA = 4πQ_enclosed
   ∇ · E = 4πρ  (differential form)
   ```

3. **Potential Equation Derivation** (Arts. 69-73, 77)
   ```
   E = -∇V
   ∇²V = -4πρ  (Poisson)
   ∇²V = 0  (Laplace, charge-free)
   ```

4. **Maxwell Stress Tensor Derivation** (Arts. 103-110)
   ```
   T_ij = (1/4π)[E_i E_j - (1/2)δ_ij E²]
   F_i = ∮ T_ij n_j dS
   ```

### Electrokinematic Equation Derivations (Part II)

5. **Continuity Equation** (Arts. 285-296)
   ```
   ∇ · J + ∂ρ/∂t = 0
   ```
   - From charge conservation
   - From tube of flow analysis

6. **3D Ohm's Law** (Arts. 297-298)
   ```
   J = σE
   J_i = σ_ij E_j  (anisotropic)
   ```

7. **Thermoelectric Equations** (Arts. 249-254)
   ```
   E = S∇T  (Seebeck effect)
   q = ΠJ  (Peltier effect)
   dE/dT = σ  (Thomson effect)
   ```

### Magnetostatic Equation Derivations (Part III)

8. **Magnetic Field Equations** (Arts. 395-400)
   ```
   H = -∇Ω  (scalar potential)
   B = H + 4πI  (constitutive)
   ∇ · B = 0  (solenoidal)
   ```

9. **Vector Potential Derivation** (Arts. 405-406)
   ```
   B = ∇ × A
   A = (1/c) ∫ (J/r) dτ
   ```

10. **Magnetic Shell Equations** (Arts. 409-411)
    ```
    Ω = Φ ω  (potential = strength × solid angle)
    ΔΩ = 4πΦ  (discontinuity across shell)
    ```

### Electromagnetic Field Equations (Part IV)

11. **Faraday's Law Derivation** (Arts. 528-531, 590)
    ```
    EMF = -(1/c) dΦ/dt
    ∇ × E = -(1/c) ∂B/∂t
    ```

12. **Ampère's Law with Maxwell's Addition** (Arts. 606-607)
    ```
    ∇ × H = (4π/c) J + (1/c) ∂D/∂t
    ```
    - Conduction current term: (4π/c)J
    - Displacement current term: (1/c)∂D/∂t

13. **Complete Maxwell Equations** (Arts. 598-601)
    ```
    (G)  D = εE
    (H)  B = μH
    (A)  ∇ × E = -(1/c) ∂B/∂t
    (B)  ∇ × H = (4π/c)J + (1/c) ∂D/∂t
    (C)  ∇ · D = 4πρ
    (D)  ∇ · B = 0
    ```

14. **Wave Equation Derivation** (Arts. 781-785)
    ```
    ∇²E - (1/c²) ∂²E/∂t² = 0
    ∇²B - (1/c²) ∂²B/∂t² = 0
    Wave speed: v = c/√(εμ)
    ```

### Dynamical Theory Derivations (Part IV)

15. **Lagrangian Formulation** (Arts. 553-558)
    ```
    L = T - V  (kinetic - potential)
    d/dt(∂L/∂q̇) - ∂L/∂q = Q  (generalized force)
    ```

16. **Electrokinetic Energy** (Arts. 551-552)
    ```
    T = (1/2) Σ L_ij q̇_i q̇_j  (inductance energy)
    ```

17. **Ponderomotive Force** (Arts. 602-603)
    ```
    F = q(E + v/c × B)  (Lorentz force)
    ```

## Usage

```python
from maxwell.physics.derivation import EquationDerivation
from maxwell.math.vector_calculus import VectorOperators
from maxwell.physics.constants import CGS_CONSTANTS

# ===== ELECTROSTATICS DERIVATIONS =====

# Derive Coulomb's law from experimental basis
coulomb = EquationDerivation.derive_coulomb_law(
    starting_principles=['charge_conservation', 'inverse_square'],
    target_form='vector'
)
# Returns: F = q1*q2/r^2 * r_hat

# Derive Gauss's law
gauss = EquationDerivation.derive_gauss_law(
    starting_from='coulomb_law',
    method='surface_integral'
)
# Returns: div(E) = 4*pi*rho

# Derive Maxwell stress tensor
stress = EquationDerivation.derive_stress_tensor(
    from_energy='electrostatic_energy',
    method='virtual_work'
)
# Returns: T_ij = (1/4pi)[E_i*E_j - (1/2)*delta_ij*E^2]

# ===== MAGNETOSTATICS DERIVATIONS =====

# Derive magnetic field equations
mag_field = EquationDerivation.derive_magnetic_field_equations(
    starting_from=['magnetic_poles', 'solenoidal_condition']
)
# Returns: div(B) = 0, B = curl(A)

# Derive vector potential
vector_pot = EquationDerivation.derive_vector_potential(
    from_biot_savart=True,
    gauge='coulomb'
)
# Returns: A = (1/c) * integral(J/r) dtau

# ===== ELECTROMAGNETIC FIELD DERIVATIONS =====

# Derive Faraday's law
faraday = EquationDerivation.derive_faradays_law(
    from_experiments=['faraday_induction', 'lenz_law'],
    include_motion_emf=True
)
# Returns: curl(E) = -(1/c) * dB/dt

# Derive Ampère-Maxwell law
ampere_maxwell = EquationDerivation.derive_ampere_maxwell(
    from_ampere_law=True,
    include_displacement_current=True,
    trace_to_article=607
)
# Returns: curl(H) = (4pi/c)*J + (1/c)*dD/dt

# Derive wave equation
wave = EquationDerivation.derive_wave_equation(
    from_maxwell_equations=True,
    medium='vacuum',
    show_light_speed_identity=True
)
# Returns: d^2E/dt^2 = c^2 * laplacian(E)
# And: c = 1/sqrt(epsilon*mu)

# ===== DYNAMICAL DERIVATIONS =====

# Derive Lagrangian for EM field
lagrangian = EquationDerivation.derive_em_lagrangian(
    field_variables=['A', 'V'],
    include_sources=True
)
# Returns: L = (1/8pi)(E^2 - B^2) - rho*V + (1/c)*J·A

# Derive ponderomotive force
ponderomotive = EquationDerivation.derive_ponderomotive_force(
    from_energy_variation=True,
    general_form=True
)
# Returns: F = q(E + v/c × B)

# ===== COMPLETE SYSTEM =====

# Generate complete Maxwell equation system
maxwell_system = EquationDerivation.derive_complete_system(
    include_constitutive=True,
    include_boundary_conditions=True,
    format='vector_calculus'
)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `equation_type` | str | Type of equation to derive |
| `starting_principles` | list | Fundamental principles to start from |
| `method` | str | Derivation method ('variational', 'direct', 'integral') |
| `coordinate_system` | str | Coordinate system for derivation |
| `include_sources` | bool | Include charge/current sources |
| `include_boundary_conditions` | bool | Include BCs in derivation |
| `trace_to_articles` | list | Maxwell articles to reference |
| `format` | str | Output format ('vector', 'tensor', 'component') |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `derivation` | DerivationTree | Step-by-step derivation tree |
| `final_equation` | Equation | Final derived equation |
| `intermediate_steps` | list | Key intermediate results |
| `article_references` | list | Maxwell article citations |
| `assumptions` | list | Assumptions made during derivation |

## Implementation Notes

### Derivation Methodology

Each derivation follows Maxwell's original reasoning:
1. State starting principles/experiments
2. Apply mathematical operations step-by-step
3. Cite Maxwell article for each physical principle
4. Distinguish physical postulates from mathematical identities
5. Arrive at final equation with clear logical chain

### Vector Calculus Notation

Modern vector notation is used but mapped to Maxwell's component notation:
- Maxwell: (dR/dy - dQ/dz, dP/dz - dR/dx, dQ/dx - dP/dy)
- Modern: ∇ × F = (∂F_z/∂y - ∂F_y/∂z, ...)

### CGS Units Throughout

All derivations use CGS units as Maxwell did:
- Force: dyne
- Charge: statcoulomb (ESU) or abcoulomb (EMU)
- Field factors: 4π appears explicitly
- Speed of light c appears in EM equations

## Validation

### Historical Accuracy
- Cross-reference with Maxwell's original derivations
- Verify article citations are accurate
- Check that reasoning follows Maxwell's logic

### Mathematical Rigor
- Each step mathematically verified
- Vector identities confirmed
- Boundary terms properly handled

### Physical Consistency
- Limiting cases match known physics
- Conservation laws satisfied
- Dimensional consistency verified

## Maxwell Article References

| Article | Content |
|---------|---------|
| 66-68 | Coulomb's law derivation |
| 75-76 | Gauss's law derivation |
| 77 | Poisson equation |
| 103-110 | Stress tensor derivation |
| 285-296 | Continuity equation |
| 395-400 | Magnetic field equations |
| 405-406 | Vector potential |
| 528-531 | Faraday's law |
| 590 | Faraday's law (differential) |
| 606-607 | Ampère-Maxwell law |
| 608-609 | Constitutive equations |
| 781-785 | Wave equation derivation |
| 786-787 | Light speed identification |

## Related Commands

- `implement-field` - Implement derived field equations
- `solve-analytical` - Solve derived equations
- `implement-wave` - Wave equation implementation
- `implement-dynamics` - Dynamical formulations

## Error Handling

- Raises `DerivationError` if logical steps are invalid
- Warns about assumptions made
- Flags steps needing user theory input
- Validates final equation dimensions

## Theory Preservation Protocol

During any derivation:
1. Cite Maxwell articles for physical principles
2. Mark mathematical identities as standard
3. For User theories: INCLUDE EXACTLY AS SPECIFIED - DO NOT ALTER
4. Document all assumptions explicitly
5. Preserve Maxwell's original reasoning where possible

# Command: implement-constitutive

## Description

Implements material constitutive relations connecting electromagnetic fields to material response. This command covers dielectric, magnetic, and conductive material behavior from Maxwell's Parts I-IV, including anisotropic and nonlinear responses.

## Source Category

**CRITICAL: Theory Preservation**

This command implements:
- **Maxwell's 1873 Historical Text**: Articles 52-53, 60-62, 101a-h, 400, 424-426, 605-609
- **Standard Mathematical Implementation**: Tensor operations, anisotropy handling
- **User Original Theory**: NONE - if user provides extensions, label as "User Original Theory - Authoritative - DO NOT ALTER"

## Functionality

### Dielectric Constitutive Relations (Part I)

1. **Electric Displacement** (Arts. 60-62, 111)
   ```
   D = εE = E + 4πP  (CGS)
   P = χ_e E  (polarization)
   ε = 1 + 4πχ_e  (permittivity)
   ```

2. **Specific Inductive Capacity** (Arts. 52-53)
   - K = ε/ε_0 (dielectric constant)
   - Isotropic: scalar K
   - Anisotropic: tensor K_ij

3. **Anisotropic Dielectrics** (Arts. 101a-h)
   ```
   D_i = ε_ij E_j  (tensor relation)
   ```
   - Principal axes determination
   - Energy density: w = (1/8π) E_i D_i

### Magnetic Constitutive Relations (Part III)

4. **Magnetic Induction Relation** (Art. 400)
   ```
   B = H + 4πI = μH  (CGS)
   I = κH  (magnetization intensity)
   μ = 1 + 4πκ  (permeability)
   ```

5. **Magnetic Susceptibility** (Arts. 424-426)
   - κ > 0: Paramagnetic
   - κ < 0: Diamagnetic
   - κ >> 1: Ferromagnetic

6. **Induced Magnetization** (Arts. 427-430)
   - Linear: I = κH
   - Nonlinear: I = f(H) (saturation, hysteresis)
   - Anisotropic: I_i = κ_ij H_j

### Conductive Relations (Part II)

7. **Ohm's Law in 3D** (Arts. 241, 297-298)
   ```
   J = σE  (current density)
   ```
   - Isotropic: scalar σ
   - Anisotropic: J_i = σ_ij E_j

8. **Anisotropic Conduction** (Arts. 297-303)
   - Conductivity tensor σ_ij
   - Principal conductivity axes
   - Stratified materials

### Unified Constitutive Framework (Part IV)

9. **Maxwell's Constitutive Equations** (Arts. 605-609)
   - Equation (D): B = μH (magnetization)
   - Equation (F): D = εE (displacement)
   - Equation (G): J = σE (conduction)

10. **Energy Density** (Arts. 630-638)
    - Electrostatic: w_e = (1/8π) E·D
    - Magnetostatic: w_m = (1/8π) B·H
    - Electrokinetic: w_k = (1/2) L_i q_i q_j (inductance energy)

## Usage

```python
from maxwell.materials.constitutive import (
    DielectricResponse,
    MagneticResponse,
    ConductiveResponse,
    ConstitutiveTensor
)
from maxwell.physics.fields import ElectricField, MagneticField

# ===== DIELECTRIC RESPONSE =====

# Isotropic dielectric
dielectric = DielectricResponse(
    material='glass',
    dielectric_constant=K=4.5,  # dimensionless
    loss_tangent=0.01  # optional
)
D = dielectric.compute_displacement(E_field)
P = dielectric.compute_polarization(E_field)
energy_density = dielectric.energy_density(E_field)

# Anisotropic dielectric (Arts. 101a-h)
tensor_dielectric = DielectricResponse(
    material='crystal',
    permittivity_tensor=[
        [ε_xx, ε_xy, ε_xz],
        [ε_yx, ε_yy, ε_yz],
        [ε_zx, ε_zy, ε_zz]
    ],
    principal_axes=principal_axes  # optional
)
D_aniso = tensor_dielectric.compute_displacement(E_field)

# ===== MAGNETIC RESPONSE =====

# Linear magnetic material
magnetic = MagneticResponse(
    material='soft_iron',
    susceptibility=κ=200,  # dimensionless
    saturation_magnetization=I_s=None  # linear regime
)
B = magnetic.compute_induction(H_field)
I = magnetic.compute_magnetization(H_field)

# Nonlinear magnetic (saturation)
nonlinear_magnetic = MagneticResponse(
    material='steel',
    hysteresis_model='preisach',
    saturation_magnetization=I_s=1700,  # gauss
    coercivity=H_c=50  # Oersted
)
B_nonlinear = nonlinear_magnetic.compute_induction(H_field, history=H_history)

# Anisotropic magnetic
anisotropic_magnetic = MagneticResponse(
    material='grain_oriented_steel',
    susceptibility_tensor=κ_tensor,
    easy_axis=[1, 0, 0]
)

# ===== CONDUCTIVE RESPONSE =====

# Ohmic conductor
conductor = ConductiveResponse(
    material='copper',
    conductivity=σ=5.96e17  # s⁻¹ in CGS
)
J = conductor.compute_current_density(E_field)

# Anisotropic conductor (Arts. 297-298)
anisotropic_conductor = ConductiveResponse(
    material='graphite',
    conductivity_tensor=[
        [σ_parallel, 0, 0],
        [0, σ_perp, 0],
        [0, 0, σ_perp]
    ]
)
J_aniso = anisotropic_conductor.compute_current_density(E_field)

# ===== CONSTITUTIVE TENSOR OPERATIONS =====

# Build general constitutive tensor
constitutive = ConstitutiveTensor(
    type='dielectric',
    components=ε_ij,
    coordinate_system='crystal'
)

# Transform to principal axes
principal_tensor = constitutive.to_principal_axes()
principal_values = principal_tensor.eigenvalues()

# Verify positive definiteness (stability condition, Art. 300)
is_stable = constitutive.verify_stability()
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `material` | str | Material name or identifier |
| `response_type` | str | 'dielectric', 'magnetic', 'conductive' |
| `parameters` | dict | Material-specific parameters (K, κ, σ, etc.) |
| `tensor` | ndarray | Anisotropic tensor components |
| `nonlinear_model` | str | 'saturation', 'hysteresis', 'custom' |
| `temperature` | float | Optional temperature (K) |
| `frequency` | float | Optional frequency for AC response |
| `citations` | list | Maxwell article references |

## Returns

| Return | Type | Description |
|--------|------|-------------|
| `D`, `B`, or `J` | VectorField | Response field |
| `P` or `I` | VectorField | Material polarization/magnetization |
| `tensor` | ConstitutiveTensor | Material tensor object |
| `energy_density` | ScalarField | Energy per unit volume |
| `metadata` | dict | Material properties, validity range, citations |

## Implementation Notes

### CGS Units for Constitutive Parameters

| Quantity | CGS Unit | Relation |
|----------|----------|----------|
| Permittivity ε | dimensionless | D = εE |
| Susceptibility κ | dimensionless | I = κH |
| Permeability μ | dimensionless | B = μH |
| Conductivity σ | s⁻¹ | J = σE |

### Anisotropy Handling (Arts. 101a-h, 297-303)

For anisotropic materials:
1. Build tensor in laboratory coordinates
2. Diagonalize to find principal axes
3. Apply constitutive relation in principal coordinates
4. Transform back to laboratory coordinates

### Nonlinear Magnetic Response

For ferromagnetic materials:
- Initial susceptibility κ_initial (low field)
- Saturation magnetization I_s (high field limit)
- Hysteresis loop (history-dependent)
- Weber's molecular theory (Art. 430)

### Energy Considerations (Arts. 630-638)

Constitutive relations must satisfy:
- Positive energy density
- Thermodynamic stability
- Reciprocity relations

## Validation

### Material Property Checks
- Permittivity ε > 1 for dielectrics
- Susceptibility κ > 0 for paramagnets, κ < 0 for diamagnets
- Conductivity σ > 0 for passive materials
- Tensor eigenvalues positive (stability)

### Constitutive Relation Verification
- D = εE verified for known E
- B = μH verified for known H
- J = σE verified for known E

### Energy Conservation
- Work done = change in field energy
- Hysteresis loss computed correctly
- Dissipation in conductors: J·E = σE²

## Maxwell Article References

| Article | Content |
|---------|---------|
| 52-53 | Specific inductive capacity |
| 60-62 | Electric polarization and displacement |
| 101a-h | Anisotropic dielectrics, extended Green's theorem |
| 111 | Theory of electric polarization |
| 300 | Stability conditions for anisotropic conduction |
| 400 | B = H + 4πI constitutive relation |
| 424-426 | Magnetic susceptibility and induction |
| 427-430 | Induced magnetization theory |
| 605-609 | Maxwell's constitutive equations (D, F, G) |
| 630-638 | Electrokinetic energy and stress |

## Related Commands

- `implement-field` - Field computations in materials
- `derive-equations` - Derive constitutive equations
- `solve-analytical` - Material boundary value problems
- `implement-dynamics` - Energy in material systems

## Error Handling

- Raises `ConstitutiveError` for unphysical parameters
- Warns about nonlinear regime boundaries
- Validates tensor symmetry and positive definiteness
- Flags temperature/frequency limits

## Theory Preservation Protocol

Before any constitutive computation:
1. Identify source category (Maxwell/User/Standard)
2. Apply appropriate citation label
3. For User theories: IMPLEMENT EXACTLY AS SPECIFIED - DO NOT ALTER
4. For Maxwell: Implement as described in Treatise
5. Document material assumptions and validity ranges

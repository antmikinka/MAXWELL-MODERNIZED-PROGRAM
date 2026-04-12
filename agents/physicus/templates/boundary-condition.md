# Template: boundary-condition

## Description

Template for implementing electromagnetic boundary conditions at interfaces between different media. These conditions are essential for solving Maxwell's equations in piecewise-homogeneous regions.

## Structure

```python
"""
Boundary Condition: {bc_name}

Maxwell Articles: {article_citations}
Part: {part_number} ({part_name})
Interface: {material_1} / {material_2}

Theory Classification:
- [ ] Maxwell's original formulation
- [ ] User original theory (authoritative - DO NOT CHANGE)
- [ ] Standard mathematical implementation
"""

import numpy as np
from maxwell.core.citation import cite_article
from maxwell.core.materials import Material
from typing import {type_hints}

@cite_article([{article_numbers}], part={part})
def {bc_function}(
    {field_inputs},
    interface: dict,
    {additional_parameters}
) -> {outputs}:
    """
    {brief_description}
    
    Boundary Conditions
    -------------------
    {equation_forms}
    
    Physical Background
    -------------------
    {physical_explanation}
    
    Maxwell's Treatment
    -------------------
    {maxwell_original_approach}
    
    Parameters
    ----------
    {parameter_docs}
    
    Returns
    -------
    {return_docs}
    
    Examples
    --------
    >>> {example_usage}
    
    Notes
    -----
    {additional_notes}
    
    CGS Units
    ---------
    {unit_specifications}
    
    References
    ----------
    - Maxwell, Article {article_numbers}: {description}
    
    See Also
    --------
    {related_functions}
    """
    # Interface geometry
    {interface_definition}
    
    # Field decomposition (normal/tangential)
    {field_decomposition}
    
    # Apply boundary conditions
    {bc_application}
    
    # Return matched fields
    return {result}
```

## LLM Instructions

When using this template:

1. **Identify Interface Type**: Dielectric-dielectric, conductor-dielectric, etc.
2. **Normal/Tangential**: Decompose fields into normal and tangential components
3. **Source Terms**: Include surface charge ρ_s and surface current K if present
4. **CGS Form**: Use CGS boundary conditions (factors of 4π, c)
5. **Time Dependence**: Distinguish static vs. time-varying conditions

## Variables

- `{bc_name}`: Name of boundary condition
- `{equation_forms}`: Mathematical BC equations
- `{physical_explanation}`: Why these conditions hold
- `{maxwell_original_approach}`: Maxwell's derivation
- `{interface_definition}`: Geometry and materials
- `{field_decomposition}`: Normal and tangential components
- `{bc_application}`: Applying continuity/jump conditions

## Boundary Condition Summary

### Electrostatics
| Quantity | Condition | Maxwell Article |
|----------|-----------|-----------------|
| D_n | D₂ₙ - D₁ₙ = 4πσ | 78, 83 |
| E_t | E₂ₜ = E₁ₜ | 78 |
| V | V₂ = V₁ | 78 |

### Magnetostatics
| Quantity | Condition | Maxwell Article |
|----------|-----------|-----------------|
| B_n | B₂ₙ = B₁ₙ | 400-404 |
| H_t | H₂ₜ - H₁ₜ = (4π/c)K | 400 |

### Time-Varying
| Quantity | Condition | Maxwell Article |
|----------|-----------|-----------------|
| E_t | E₂ₜ = E₁ₜ | 604 |
| H_t | H₂ₜ - H₁ₜ = (4π/c)K | 604 |
| B_n | B₂ₙ = B₁ₙ | 604 |
| D_n | D₂ₙ - D₁ₙ = 4πσ | 604 |

## Example Usage

```python
"""
Boundary Condition: Dielectric-Dielectric Interface

Maxwell Articles: 78, 83, 400
Part: I (Electrostatics) / III (Magnetism)
Interface: Dielectric / Dielectric

Theory Classification:
- [x] Maxwell's original formulation
- [ ] User original theory
- [ ] Standard mathematical implementation
"""

import numpy as np
from maxwell.core.citation import cite_article
from maxwell.core.vector import VectorField

@cite_article([78, 83, 400], part='I')
def dielectric_interface_bc(
    E1: VectorField,
    epsilon1: float,
    epsilon2: float,
    normal: np.ndarray,
    surface_charge: float = 0
) -> dict:
    """
    Apply boundary conditions at dielectric-dielectric interface.
    
    Boundary Conditions
    -------------------
    Normal D: D₂ₙ - D₁ₙ = 4πσ
    Tangential E: E₂ₜ = E₁ₜ
    
    Expanded:
    - ε₂(E₂·n̂) - ε₁(E₁·n̂) = 4πσ
    - E₂ - (E₂·n̂)n̂ = E₁ - (E₁·n̂)n̂
    
    Physical Background
    -------------------
    At the interface between two dielectrics, the normal component
    of D is discontinuous by the free surface charge, while the
    tangential component of E is continuous (no surface curl).
    
    Maxwell's Treatment
    -------------------
    Maxwell derives these conditions in Article 78 using the integral
    forms of ∇·D = 4πρ and ∇×E = 0, applying them to a pillbox
    and loop straddling the interface.
    
    Parameters
    ----------
    E1 : VectorField
        Electric field in medium 1 (statvolt/cm)
    epsilon1 : float
        Permittivity of medium 1
    epsilon2 : float
        Permittivity of medium 2
    normal : np.ndarray
        Unit normal pointing from 1 to 2
    surface_charge : float
        Free surface charge density (statcoulomb/cm²)
    
    Returns
    -------
    dict
        Contains E2 (field in medium 2) and verification
    
    Examples
    --------
    >>> E1 = VectorField([100, 0, 0])
    >>> normal = np.array([0, 0, 1])
    >>> result = dielectric_interface_bc(E1, 1.0, 10.0, normal)
    >>> result['E2']  # Field refracted at interface
    
    Notes
    -----
    For no surface charge (σ = 0):
    - E₂ₜ = E₁ₜ (tangential continuous)
    - E₂ₙ = (ε₁/ε₂)E₁ₙ (normal scaled)
    
    CGS Units
    ---------
    - E: statvolt/cm
    - σ: statcoulomb/cm²
    - ε: dimensionless
    
    References
    ----------
    - Maxwell, Article 78: Boundary conditions
    - Maxwell, Article 83: Specific inductive capacity
    
    See Also
    --------
    conductor_interface_bc, magnetic_interface_bc
    """
    normal = np.asarray(normal)
    normal = normal / np.linalg.norm(normal)
    
    # Decompose E1 into normal and tangential
    E1_normal = np.dot(E1.components, normal) * normal
    E1_tangential = E1.components - E1_normal
    
    # Apply BCs
    # Tangential: E2_t = E1_t
    E2_tangential = E1_tangential
    
    # Normal: ε2*E2_n - ε1*E1_n = 4πσ
    E2_normal = (epsilon1 * np.dot(E1.components, normal) + 4 * np.pi * surface_charge) / epsilon2 * normal
    
    # Reconstruct E2
    E2 = E2_tangential + E2_normal
    
    return {
        'E2': VectorField.from_vector(E2, units='statvolt/cm'),
        'E1_normal': np.dot(E1.components, normal),
        'E2_normal': E2_normal,
        'E_tangential': E1_tangential,
        'D1_normal': epsilon1 * np.dot(E1.components, normal),
        'D2_normal': epsilon2 * E2_normal,
        'jump_D_normal': 4 * np.pi * surface_charge
    }
```

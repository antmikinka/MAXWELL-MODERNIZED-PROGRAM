# Template: constitutive-relation

## Description

Template for implementing material constitutive relations that connect field quantities. These relations (D = εE, B = μH, J = σE) are fundamental to solving Maxwell's equations in matter.

## Structure

```python
"""
Constitutive Relation: {relation_name}

Maxwell Articles: {article_citations}
Part: {part_number} ({part_name})
Layer: {layer_number}

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
def {relation_name}(
    {field_input},
    material: Material,
    {additional_parameters}
) -> {field_output}:
    """
    {brief_description}
    
    Constitutive Relation
    ---------------------
    {equation_form}
    
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
    
    Validity Range
    --------------
    {applicable_conditions}
    
    CGS Units
    ---------
    {unit_specifications}
    
    References
    ----------
    - Maxwell, Article {article_numbers}: {description}
    - Modern reference: {reference}
    
    See Also
    --------
    {related_functions}
    """
    # Input validation
    {input_validation}
    
    # Material property extraction
    {material_properties}
    
    # Constitutive relation
    {relation_computation}
    
    # Output validation
    {output_validation}
    
    return {result}


# === Material Classes ===
class {MaterialClass}(Material):
    """
    Material class for {material_type}.
    
    Parameters
    ----------
    {material_parameters}
    
    Attributes
    ----------
    {material_attributes}
    """
    
    def __init__(self, {init_parameters}):
        super().__init__(name={name})
        {initialization}
    
    def constitutive_response(self, field):
        """Compute response to applied field."""
        {response_calculation}
```

## LLM Instructions

When using this template:

1. **Identify Theory Source**: Clearly mark if Maxwell original, user theory, or standard
2. **CGS Convention**: Use CGS forms (D = E + 4πP, not D = ε₀E + P)
3. **Linearity**: Specify if relation is linear or nonlinear
4. **Anisotropy**: Handle tensor relations for anisotropic materials
5. **Dispersion**: Include frequency dependence if applicable
6. **Temperature**: Note temperature dependence if relevant

## Variables

- `{relation_name}`: Name of constitutive relation
- `{equation_form}`: Mathematical form (e.g., D = εE)
- `{physical_explanation}`: Microscopic origin
- `{maxwell_original_approach}`: How Maxwell formulated this
- `{material_properties}`: ε, μ, σ, etc.
- `{relation_computation}`: Implementation of relation
- `{applicable_conditions}`: When relation is valid
- `{material_type}`: Dielectric, magnetic, conductor, etc.

## Conditional Logic

IF linear isotropic:
  USE scalar constitutive parameter

IF anisotropic:
  USE tensor relation: D_i = ε_ij E_j
  INCLUDE principal axis transformation

IF nonlinear:
  INCLUDE functional form: D = ε(E)E
  ADD saturation/limiting behavior

IF dispersive:
  INCLUDE frequency dependence: ε(ω)
  ADD time-domain convolution form

IF temperature dependent:
  INCLUDE ε(T) relation
  ADD thermal coefficients

## Example Usage

```python
"""
Constitutive Relation: Electric Displacement in Dielectrics

Maxwell Articles: 60-62, 79-83
Part: I (Electrostatics)
Layer: 5

Theory Classification:
- [x] Maxwell's original formulation
- [ ] User original theory
- [ ] Standard mathematical implementation
"""

import numpy as np
from maxwell.core.citation import cite_article
from maxwell.core.materials import DielectricMaterial
from maxwell.core.vector import VectorField
from typing import Union

@cite_article([60, 61, 62, 79, 80, 81, 82, 83], part='I')
def electric_displacement(
    E_field: VectorField,
    material: DielectricMaterial,
    frequency: float = None
) -> VectorField:
    """
    Compute electric displacement D from electric field E.
    
    Constitutive Relation
    ---------------------
    D = εE = E + 4πP (CGS Gaussian)
    
    For linear isotropic media: D = εE where ε = 1 + 4πχ_e
    
    Physical Background
    -------------------
    The electric displacement D accounts for both the applied field E
    and the material's polarization response P. In CGS Gaussian units,
    D and E have the same dimensions, differing by 4πP.
    
    Maxwell's Treatment
    -------------------
    Maxwell introduces D as the "electric displacement" in Articles 60-62,
    relating it to polarization through the specific inductive capacity K
    (dielectric constant). He notes that D = KE in isotropic media.
    
    Parameters
    ----------
    E_field : VectorField
        Electric field intensity (statvolt/cm)
    material : DielectricMaterial
        Material with permittivity property
    frequency : float, optional
        Frequency in Hz for dispersive materials
    
    Returns
    -------
    VectorField
        Electric displacement D (same units as E in CGS)
    
    Examples
    --------
    >>> E = VectorField([100, 0, 0])  # statvolt/cm
    >>> glass = DielectricMaterial(epsilon=10.0)
    >>> D = electric_displacement(E, glass)
    >>> D.components
    array([1000., 0., 0.])  # D = εE = 10 × 100
    
    Notes
    -----
    CGS Gaussian form: D = E + 4πP
    
    In SI: D = ε₀E + P
    
    For linear media: P = χ_e E, so D = (1 + 4πχ_e)E = εE
    
    Validity Range
    --------------
    - Linear response (E below breakdown)
    - Isotropic material
    - Frequency below optical resonance (if static ε used)
    
    CGS Units
    ---------
    - E: statvolt/cm
    - D: statvolt/cm (same as E in CGS)
    - P: statvolt/cm (dipole moment per volume)
    - ε: dimensionless (relative permittivity)
    
    References
    ----------
    - Maxwell, Articles 60-62: Electric displacement
    - Maxwell, Articles 79-83: Specific inductive capacity
    
    See Also
    --------
    polarization, magnetic_induction, current_density
    """
    # Input validation
    if not isinstance(E_field, VectorField):
        raise TypeError("E_field must be VectorField")
    
    # Material property extraction
    if frequency is not None and hasattr(material, 'permittivity_dispersion'):
        epsilon = material.get_permittivity(frequency)
    else:
        epsilon = material.permittivity
    
    # Constitutive relation: D = εE
    D_components = epsilon * E_field.components
    
    # Output validation
    assert np.isfinite(D_components).all()
    
    return VectorField.from_vector(
        D_components,
        units='statvolt/cm',
        derived_from='electric_displacement'
    )
```

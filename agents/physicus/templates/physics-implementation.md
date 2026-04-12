# Template: physics-implementation

## Description

Template for implementing physics functions with proper documentation, Maxwell article citations, and CGS unit consistency. This template ensures consistent, high-quality code across all physics implementations.

## Structure

```python
"""
{module_docstring}

Maxwell Articles: {article_citations}
Part: {part_number} ({part_name})
Layer: {layer_number}
"""

import numpy as np
from maxwell.core.citation import cite_article
from maxwell.core.units import cgs_units
from typing import {type_hints}

@cite_article([{article_numbers}], part={part})
@cgs_units({unit_annotations})
def {function_name}(
    {parameters}
) -> {return_type}:
    """
    {brief_description}
    
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
    {mathematical_background}
    
    CGS Units
    ---------
    {unit_specifications}
    
    References
    ----------
    - Maxwell, Article {article_numbers}: {article_descriptions}
    - Modern reference: {modern_reference}
    
    See Also
    --------
    {related_functions}
    """
    # Input validation
    {input_validation}
    
    # Physics computation
    {computation}
    
    # Unit consistency check
    {unit_verification}
    
    # Output validation
    {output_validation}
    
    return {result}


# === Validation Tests ===
def _validate_{function_name}():
    """
    Internal validation tests.
    """
    {test_cases}
    pass
```

## LLM Instructions

When using this template:

1. **Citation First**: Always identify relevant Maxwell articles before implementation
2. **Theory Preservation**: Distinguish between:
   - Maxwell's 1873 text (historical source)
   - User's original theories (authoritative - DO NOT CHANGE)
   - Standard mathematical implementations (established)
3. **CGS Units**: Document all units in CGS system (ESU, EMU, or Gaussian)
4. **Physical Validation**: Include validation against analytical solutions
5. **Modern Context**: Add notes comparing with modern formulations (SI units, etc.)

## Variables

- `{module_docstring}`: Module-level physics documentation
- `{article_citations}`: Maxwell article numbers
- `{part_number}`: Part I-IV
- `{part_name}`: Electrostatics, Electrokinematics, Magnetism, Electromagnetism
- `{layer_number}`: Architecture layer
- `{function_name}`: Physics function name (snake_case)
- `{physical_explanation}`: Physical intuition and background
- `{maxwell_original_approach}`: How Maxwell derived this
- `{parameter_docs}`: Parameter documentation with units
- `{return_docs}`: Return value documentation with units
- `{example_usage}`: Working code example with CGS units
- `{mathematical_background}`: Mathematical formulation
- `{unit_specifications}`: CGS unit specifications
- `{modern_reference}`: Modern textbook reference
- `{related_functions}`: Links to related physics functions

## Conditional Logic

IF function involves fields:
  INCLUDE coordinate system specification
  ADD vector/tensor nature documentation

IF function involves materials:
  INCLUDE constitutive relation
  ADD linearity assumptions

IF function is time-dependent:
  INCLUDE causality discussion
  ADD frequency domain equivalent

IF function involves approximations:
  DOCUMENT validity range
  INCLUDE error estimates

## Example Usage

```python
"""
Electric field computation from point charges.

Maxwell Articles: 44-49, 64-68
Part: I (Electrostatics)
Layer: 2
"""

import numpy as np
from maxwell.core.citation import cite_article
from maxwell.core.units import cgs_units
from maxwell.core.vector import VectorField
from typing import Union, Tuple

@cite_article([44, 45, 46, 47, 48, 49], part='I')
@cgs_units({'charge': 'statcoulomb', 'distance': 'cm', 'field': 'statvolt/cm'})
def electric_field_point_charge(
    charge: float,
    position: np.ndarray,
    observation_point: np.ndarray
) -> VectorField:
    """
    Compute electric field from a point charge.
    
    Physical Background
    -------------------
    A point charge creates a radial electric field that falls off as 1/r².
    This is the fundamental solution to electrostatics from which all
    other solutions can be built via superposition.
    
    Maxwell's Treatment
    -------------------
    Maxwell defines the electric field intensity E as the force per unit
    charge (Art. 44-49). For a point charge e at distance r, the field
    is E = e/r² in the radial direction (CGS ESU).
    
    Parameters
    ----------
    charge : float
        Point charge in statcoulombs
    position : np.ndarray
        Charge position [x, y, z] in cm
    observation_point : np.ndarray
        Field evaluation point [x, y, z] in cm
    
    Returns
    -------
    VectorField
        Electric field vector at observation point (statvolt/cm)
    
    Examples
    --------
    >>> q = 1.0  # statcoulomb
    >>> pos = np.array([0, 0, 0])
    >>> obs = np.array([1, 0, 0])
    >>> E = electric_field_point_charge(q, pos, obs)
    >>> E.magnitude()
    1.0  # statvolt/cm
    
    Notes
    -----
    Formula: E = q * r_hat / r²
    
    In Cartesian components:
    E_x = q * (x - x₀) / |r - r₀|³
    E_y = q * (y - y₀) / |r - r₀|³
    E_z = q * (z - z₀) / |r - r₀|³
    
    CGS Units
    ---------
    - Charge: statcoulomb (esu)
    - Distance: cm
    - Field: statvolt/cm = dyne/statcoulomb
    
    References
    ----------
    - Maxwell, Articles 44-49: Electric field definition
    - Maxwell, Articles 64-68: Point charge field
    - Jackson, Classical Electrodynamics, 3rd ed., Eq. 1.4
    
    See Also
    --------
    electric_field_dipole, electric_field_distribution, potential_point_charge
    """
    # Input validation
    position = np.asarray(position, dtype=np.float64)
    observation_point = np.asarray(observation_point, dtype=np.float64)
    
    if position.shape != (3,):
        raise ValueError("Position must be 3D vector")
    
    # Displacement vector
    r_vec = observation_point - position
    r_mag = np.linalg.norm(r_vec)
    
    if r_mag == 0:
        raise SingularFieldError("Cannot evaluate field at charge location")
    
    # Physics computation: E = q * r_hat / r^2
    E_vector = charge * r_vec / r_mag**3
    
    # Output validation
    assert np.isfinite(E_vector).all(), "Field must be finite"
    
    return VectorField.from_vector(E_vector, units='statvolt/cm')
```

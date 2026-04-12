# Template: code-implementation

## Description

Template for implementing mathematical functions with proper documentation, citations, and validation. This template ensures consistent, high-quality code across the Maxwell package.

## Structure

```python
"""
{module_docstring}

Maxwell Articles: {article_citations}
"""

import numpy as np
from maxwell.core.citation import cite_article
from typing import {type_hints}

@cite_article([{article_numbers}])
def {function_name}(
    {parameters}
) -> {return_type}:
    """
    {brief_description}
    
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
    
    References
    ----------
    - Maxwell, Article {article_numbers}: {article_descriptions}
    
    See Also
    --------
    {related_functions}
    """
    # Input validation
    {input_validation}
    
    # Main computation
    {computation}
    
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

1. **Citation Decorator**: Always include @cite_article with relevant article numbers
2. **Type Hints**: Use complete type hints for all parameters and return values
3. **Docstring**: Follow NumPy docstring convention
4. **Examples**: Include working examples in docstring
5. **Validation**: Include internal validation function
6. **Units**: Specify CGS units in parameter documentation

## Variables

- `{module_docstring}`: Module-level documentation
- `{article_citations}`: Comma-separated article numbers
- `{function_name}`: Function name (snake_case)
- `{parameters}`: Function parameters with type hints
- `{return_type}`: Return type annotation
- `{brief_description}`: One-line function description
- `{parameter_docs}`: Parameter documentation
- `{return_docs}`: Return value documentation
- `{example_usage}`: Working code example
- `{mathematical_background}`: Mathematical context
- `{article_descriptions}`: Description of cited articles
- `{related_functions}`: Links to related functions
- `{input_validation}`: Input validation code
- `{computation}`: Main computation code
- `{output_validation}`: Output validation code
- `{result}`: Return value
- `{test_cases}`: Validation test cases

## Conditional Logic

IF function is vector/tensor valued:
  INCLUDE shape documentation for arrays
  ADD coordinate system specification

IF function uses numerical methods:
  INCLUDE convergence criteria
  ADD tolerance parameters
  DOCUMENT numerical stability considerations

IF function is performance-critical:
  ADD @njit decorator (numba)
  INCLUDE benchmark results
  DOCUMENT complexity

## Example Usage

```python
"""
Vector calculus operations for Maxwell's electromagnetic theory.

Maxwell Articles: 15-27, 77-78
"""

import numpy as np
from maxwell.core.citation import cite_article
from maxwell.core.scalar import ScalarField
from maxwell.core.vector import VectorField

@cite_article([23, 24, 25])
def gradient(
    scalar_field: ScalarField,
    coords: str = 'cartesian'
) -> VectorField:
    """
    Compute the gradient of a scalar field.
    
    E = -∇φ (electric field from potential)
    
    Parameters
    ----------
    scalar_field : ScalarField
        The scalar potential field
    coords : str
        Coordinate system: 'cartesian', 'cylindrical', 'spherical'
    
    Returns
    -------
    VectorField
        The gradient vector field
    
    Examples
    --------
    >>> phi = ScalarField(lambda x, y, z: x**2 + y**2 + z**2)
    >>> grad_phi = gradient(phi)
    >>> grad_phi.at_point([1, 0, 0])
    array([2., 0., 0.])
    
    Notes
    -----
    In Cartesian coordinates:
    ∇φ = (∂φ/∂x, ∂φ/∂y, ∂φ/∂z)
    
    References
    ----------
    - Maxwell, Article 23-27: Vector quantities and gradient
    
    See Also
    --------
    divergence, curl, laplacian
    """
    # Implementation...
```

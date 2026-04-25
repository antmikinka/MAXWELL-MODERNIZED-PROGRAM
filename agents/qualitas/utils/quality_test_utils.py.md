# Quality Test Utilities

## Purpose

Utility functions for quality assurance testing.

## Module: quality_test_utils.py

```python
"""
Quality Test Utilities

Common functions for validation testing.
"""

import numpy as np
from typing import Callable, Dict, Tuple


def compute_l2_error(numerical: np.ndarray, 
                     analytical: np.ndarray) -> float:
    """
    Compute L2 (RMS) error between numerical and analytical.
    
    Parameters
    ----------
    numerical : np.ndarray
        Numerical solution
    analytical : np.ndarray
        Analytical reference
        
    Returns
    -------
    error : float
        L2 norm of difference
    """
    return np.sqrt(np.mean((numerical - analytical)**2))


def compute_linf_error(numerical: np.ndarray,
                       analytical: np.ndarray) -> float:
    """
    Compute L-infinity (max) error.
    """
    return np.max(np.abs(numerical - analytical))


def compute_relative_error(numerical: float,
                           analytical: float) -> float:
    """
    Compute relative error.
    """
    if analytical == 0:
        return np.abs(numerical)
    return np.abs(numerical - analytical) / np.abs(analytical)


def verify_dimensional_consistency(
    equation_terms: list
) -> bool:
    """
    Verify all terms in equation have same dimensions.
    
    Parameters
    ----------
    equation_terms : list
        List of (value, dimensions) tuples
        
    Returns
    -------
    consistent : bool
        True if dimensions match
    """
    if len(equation_terms) < 2:
        return True
    
    first_dim = equation_terms[0][1]
    for value, dim in equation_terms[1:]:
        if dim != first_dim:
            return False
    return True


def check_cfl_condition(
    dt: float,
    dx: float,
    c: float,
    dimensions: int
) -> bool:
    """
    Check CFL stability condition for FDTD.
    
    dt <= dx / (c * sqrt(dimensions))
    """
    cfl_max = dx / (c * np.sqrt(dimensions))
    return dt <= cfl_max


def generate_convergence_table(
    errors: list,
    resolutions: list
) -> str:
    """
    Generate formatted convergence table.
    """
    table = "Resolution    Error      Rate\n"
    table += "-" * 35 + "\n"
    
    for i, (res, err) in enumerate(zip(resolutions, errors)):
        if i == 0:
            rate = "-"
        else:
            rate = f"{np.log(errors[i-1]/err)/np.log(2):.2f}"
        
        table += f"{res:10d}    {err:.6e}    {rate}\n"
    
    return table
```

## Usage Examples

```python
from maxwell.quality.utils.quality_test_utils import (
    compute_l2_error, compute_linf_error, check_cfl_condition
)

# Compute errors
l2 = compute_l2_error(numerical, analytical)
linf = compute_linf_error(numerical, analytical)

# Check stability
stable = check_cfl_condition(dt=1e-15, dx=0.01, c=3e10, dimensions=3)
```

## Related Utilities

- `field_computation_helper.py` (PHYSICUS)
- `unit_converter.py` (PHYSICUS)
- `validation_helper.py` (PHYSICUS)

"""maxwell.vis._base — Shared grid and axis utilities for visualization.

Provides common functionality for creating evaluation grids and converting
between coordinate systems used across all visualization modules.
"""

from __future__ import annotations

from typing import Callable, Tuple

import numpy as np

from maxwell.vis._compat import require_matplotlib


def create_meshgrid(
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    nx: int = 100,
    ny: int = 100,
) -> Tuple[np.ndarray, np.ndarray]:
    """Create a 2D evaluation meshgrid.

    Args:
        x_min: Minimum x coordinate.
        x_max: Maximum x coordinate.
        y_min: Minimum y coordinate.
        y_max: Maximum y coordinate.
        nx: Number of x grid points.
        ny: Number of y grid points.

    Returns:
        Tuple of (X, Y) meshgrid arrays, each of shape (ny, nx).
    """
    x = np.linspace(x_min, x_max, nx)
    y = np.linspace(y_min, y_max, ny)
    return np.meshgrid(x, y)


def evaluate_on_grid(
    field_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    X: np.ndarray,
    Y: np.ndarray,
    component: int = 0,
) -> np.ndarray:
    """Evaluate a 2D vector field function on a grid.

    Args:
        field_func: Function that takes (x, y) arrays and returns
                    an array of shape (ny, nx, 2) for 2D vector fields
                    or (ny, nx) for scalar fields.
        X: X coordinate meshgrid.
        Y: Y coordinate meshgrid.
        component: Which component to extract from vector field
                   (0 for x-component, 1 for y-component).
                   Ignored for scalar fields.

    Returns:
        Array of shape (ny, nx) with the evaluated field values.
    """
    result = field_func(X, Y)
    if result.ndim == 3:
        return result[:, :, component]
    return result


def format_axis_labels(
    ax,
    xlabel: str = "x (cm)",
    ylabel: str = "y (cm)",
    title: str = "",
) -> None:
    """Apply standard axis formatting to a matplotlib axes.

    Args:
        ax: Matplotlib axes to format.
        xlabel: X-axis label.
        ylabel: Y-axis label.
        title: Plot title.
    """
    require_matplotlib()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)

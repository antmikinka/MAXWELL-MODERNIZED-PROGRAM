"""maxwell.vis._compat — Safe matplotlib import with graceful degradation.

Provides a unified import interface for matplotlib that gracefully handles
the case where matplotlib is not installed. All visualization modules in
maxwell.vis should import through this module rather than importing
matplotlib directly.

Usage:
    from maxwell.vis._compat import plt, mpl, require_matplotlib

    require_matplotlib()  # Raises ImportError with install instructions
    # or
    if plt is not None:
        # use plt...
"""

from __future__ import annotations

from typing import Optional, Tuple

# Attempt to import matplotlib
try:
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend for headless/server use
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import matplotlib.cm as cm
    import matplotlib.patches as mpatches
    from matplotlib.figure import Figure
    from matplotlib.axes import Axes
    from matplotlib.colorbar import Colorbar

    HAS_MATPLOTLIB = True
    _IMPORT_ERROR = None
except ImportError:
    plt = None
    mcolors = None
    cm = None
    mpatches = None
    Figure = None
    Axes = None
    Colorbar = None

    HAS_MATPLOTLIB = False
    _IMPORT_ERROR = (
        "matplotlib is required for visualization. "
        "Install it with: pip install maxwell[viz]"
    )


def require_matplotlib() -> None:
    """Raise ImportError with install instructions if matplotlib is missing."""
    if not HAS_MATPLOTLIB and _IMPORT_ERROR is not None:
        raise ImportError(_IMPORT_ERROR)


def get_default_colormap(name: str = "viridis") -> object:
    """Get a matplotlib colormap, returning a safe default if unavailable."""
    if cm is None:
        return None
    import matplotlib
    return matplotlib.colormaps[name]


def create_figure(
    figsize: Tuple[float, float] = (10.0, 8.0),
    dpi: int = 100,
) -> Tuple[Figure, Axes]:
    """Create a new figure and axes with standard settings.

    Args:
        figsize: Figure size in inches (width, height).
        dpi: Dots per inch for rendering.

    Returns:
        Tuple of (Figure, Axes).

    Raises:
        ImportError: If matplotlib is not installed.
    """
    require_matplotlib()
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    return fig, ax


def save_figure(fig: Figure, filename: str, **kwargs) -> str:
    """Save a figure to file.

    Args:
        fig: Matplotlib figure to save.
        filename: Output file path (supports .png, .pdf, .svg).
        **kwargs: Additional arguments passed to fig.savefig().

    Returns:
        The filename the figure was saved to.
    """
    if "bbox_inches" not in kwargs:
        kwargs["bbox_inches"] = "tight"
    fig.savefig(filename, **kwargs)
    return filename

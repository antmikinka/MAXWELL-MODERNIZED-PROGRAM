"""Maxwell stress tensor visualization -- Maxwell Part IV, Arts. 616-620.

Generates a plot of the stress tensor for a uniform electric field, verifies
tensor properties, and saves the visualization as a PNG.

Usage:
    python examples/03_stress_tensor_visualization.py
"""
import os

import numpy as np

from maxwell.vis import plot_stress_tensor_2d, verify_stress_tensor_plot


def main():
    # Define a uniform field for clean visualization
    def uniform_field(x, y):
        return np.ones_like(x) * 1.0, np.ones_like(y) * 0.5

    fig = plot_stress_tensor_2d(
        uniform_field,
        x_min=-5.0,
        x_max=5.0,
        y_min=-5.0,
        y_max=5.0,
        nx=30,
        ny=30,
        skip=2,
        quiver_scale=1.0,
        cmap="seismic",
    )
    fig.savefig("examples/output/stress_tensor.png", dpi=150, bbox_inches="tight")
    print("Saved: examples/output/stress_tensor.png")

    # Verify tensor properties
    result = verify_stress_tensor_plot(
        E_field=(1.0, 2.0, 0.0),
        B_field=(0.0, 1.0, 3.0),
    )
    print(f"\nStress Tensor Verification:")
    print(f"  Symmetric: {result['symmetric']}")
    print(f"  Trace: {result['trace']:.6f}")
    print(f"  Expected trace: {result['expected_trace']:.6f}")
    print(f"  Trace error: {result['trace_error']:.2e}")
    print(f"  Energy density: {result['energy_density']:.6f}")


if __name__ == "__main__":
    os.makedirs("examples/output", exist_ok=True)
    main()

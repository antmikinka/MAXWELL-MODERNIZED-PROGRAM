"""Edge singularity study -- Maxwell Part II, Art. 191.

Visualizes field enhancement near sharp conducting edges and compares
singularity strength for different wedge angles. Saves plots as PNGs.

Usage:
    python examples/05_edge_singularity_study.py
"""
import os

import numpy as np

from maxwell.vis import plot_edge_singularity, plot_singularity_comparison


def main():
    # Single wedge visualization (90-degree edge)
    fig1, ax1 = plot_edge_singularity(
        alpha=np.pi / 2,
        resolution=100,
        log_scale=True,
    )
    fig1.savefig("examples/output/edge_singularity.png", dpi=150, bbox_inches="tight")
    print("Saved: examples/output/edge_singularity.png")

    # Comparison of different wedge angles
    fig2, ax2 = plot_singularity_comparison(
        x_range=(0.01, 3.0),
        resolution=100,
    )
    fig2.savefig("examples/output/singularity_comparison.png", dpi=150, bbox_inches="tight")
    print("Saved: examples/output/singularity_comparison.png")


if __name__ == "__main__":
    os.makedirs("examples/output", exist_ok=True)
    main()

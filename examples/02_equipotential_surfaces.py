"""Dipole equipotential surfaces -- Maxwell Part I, Arts. 16-19.

Generates a publication-quality plot of equipotential lines for a dipole
and saves it as a PNG.

Usage:
    python examples/02_equipotential_surfaces.py
"""
import os

from maxwell.vis import plot_dipole_equipotentials


def main():
    fig = plot_dipole_equipotentials(
        charge_magnitude=1.0,
        separation=2.0,
        x_min=-5.0,
        x_max=5.0,
        y_min=-5.0,
        y_max=5.0,
        nx=200,
        ny=200,
        n_levels=30,
        filled=True,
        cmap="RdBu_r",
    )
    fig.savefig("examples/output/dipole_equipotentials.png", dpi=150, bbox_inches="tight")
    print("Saved: examples/output/dipole_equipotentials.png")


if __name__ == "__main__":
    os.makedirs("examples/output", exist_ok=True)
    main()

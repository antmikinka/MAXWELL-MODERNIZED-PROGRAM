"""Electric dipole field lines -- Maxwell Part I, Arts. 52-61.

Generates a publication-quality plot of electric field lines for a dipole
configuration and saves it as a PNG.

Usage:
    python examples/01_dipole_field_lines.py
"""
import os

from maxwell.vis import plot_dipole_field_lines


def main():
    fig = plot_dipole_field_lines(
        charge_magnitude=1.0,
        separation=2.0,
        x_min=-5.0,
        x_max=5.0,
        y_min=-5.0,
        y_max=5.0,
        nx=50,
        ny=50,
        density=1.5,
        cmap="autumn",
    )
    fig.savefig("examples/output/dipole_field_lines.png", dpi=150, bbox_inches="tight")
    print("Saved: examples/output/dipole_field_lines.png")


if __name__ == "__main__":
    os.makedirs("examples/output", exist_ok=True)
    main()

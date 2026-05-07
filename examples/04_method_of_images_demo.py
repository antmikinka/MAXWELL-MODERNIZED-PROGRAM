"""Method of Images -- Maxwell Part II, Art. 155.

Visualizes a point charge above an infinite conducting plane using the
image charge technique. Saves the plot as a PNG.

Usage:
    python examples/04_method_of_images_demo.py
"""
import os

from maxwell.vis import plot_method_of_images


def main():
    fig, ax = plot_method_of_images(
        q=1.0,
        d=1.0,
        x_range=(-3.0, 3.0),
        y_range=(-3.0, 3.0),
        resolution=100,
    )
    fig.savefig("examples/output/method_of_images.png", dpi=150, bbox_inches="tight")
    print("Saved: examples/output/method_of_images.png")


if __name__ == "__main__":
    os.makedirs("examples/output", exist_ok=True)
    main()

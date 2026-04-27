#!/usr/bin/env python3
"""Generate all 4 figures for the JOSS paper.

Run: python scripts/generate_joss_figures.py

Produces:
  - paper/figures/architecture.png  (layered package architecture)
  - paper/figures/coverage.png      (function count per Treatise part)
  - paper/figures/convergence.png   (spherical harmonic convergence)
  - paper/figures/verification.png  (cross-validation relative errors)
"""

from __future__ import annotations

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Ensure the project root is on sys.path so `maxwell` is importable even
# when this script is invoked from a working directory other than the repo
# root.
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import matplotlib

matplotlib.use("Agg")  # non-interactive backend for headless rendering
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as patches  # noqa: E402
import numpy as np  # noqa: E402

# Attempt a clean style; fall back gracefully if seaborn is absent.
try:
    matplotlib.style.use("seaborn-v0_8-whitegrid")
except OSError:
    pass

DPI = 300
FIGURES_DIR = _PROJECT_ROOT / "paper" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Figure 1: Architecture Diagram
# ---------------------------------------------------------------------------


def generate_architecture() -> None:
    """Create a layered package architecture diagram."""
    layers: list[dict] = [
        {
            "label": "Applications",
            "modules": ["maxwell.vis", "maxwell.instruments", "maxwell.meta"],
            "color": "#3F51B5",
        },
        {
            "label": "Domain Packages",
            "modules": [
                "maxwell.electromagnetism",
                "maxwell.electrostatics",
                "maxwell.optics",
                "maxwell.magnetism",
            ],
            "color": "#00897B",
        },
        {
            "label": "Math Infrastructure",
            "modules": ["maxwell.math", "maxwell.verification"],
            "color": "#F4511E",
        },
        {
            "label": "Core Objects",
            "modules": ["maxwell.core\n(charge, units, constants)"],
            "color": "#039BE5",
        },
        {
            "label": "Configuration",
            "modules": ["maxwell.config\n(constants, constants_cgs)"],
            "color": "#5C6BC0",
        },
    ]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_aspect("equal")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")
    fig.suptitle("Maxwell Modernized -- Package Architecture", fontsize=14, fontweight="bold", y=1.02)

    layer_height = 0.95
    gap = 0.12
    start_y = 6.2
    box_left = 1.2
    box_width = 7.6

    for i, layer in enumerate(layers):
        y = start_y - i * (layer_height + gap)
        # Draw layer label on the left
        ax.text(
            0.15,
            y + layer_height / 2,
            layer["label"],
            ha="right",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=layer["color"],
        )
        # Draw module boxes in a horizontal row
        n = len(layer["modules"])
        module_width = box_width / n
        for j, mod in enumerate(layer["modules"]):
            x = box_left + j * module_width
            rect = patches.FancyBboxPatch(
                (x, y),
                module_width - 0.08,
                layer_height,
                linewidth=1,
                edgecolor="gray",
                facecolor=layer["color"],
                alpha=0.75,
                boxstyle="round,pad=0.08",
            )
            ax.add_patch(rect)
            ax.text(
                x + module_width / 2 - 0.04,
                y + layer_height / 2,
                mod,
                ha="center",
                va="center",
                fontsize=7.5,
                color="white",
                fontweight="medium",
                wrap=True,
            )

    # Subtle downward arrows between layers
    arrow_x = 5.0
    for i in range(len(layers) - 1):
        arrow_y_top = start_y - i * (layer_height + gap) - gap - layer_height
        ax.annotate(
            "",
            xy=(arrow_x, arrow_y_top),
            xytext=(arrow_x, arrow_y_top + layer_height + gap),
            arrowprops=dict(arrowstyle="->", color="#9E9E9E", lw=1.2),
        )

    plt.savefig(FIGURES_DIR / "architecture.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("[OK] architecture.png")


# ---------------------------------------------------------------------------
# Figure 2: Coverage Heatmap (bar chart)
# ---------------------------------------------------------------------------


def generate_coverage() -> None:
    """Bar chart showing function count per Treatise part."""
    parts = [
        ("Part I\n(Arts. 1-229)", 288),
        ("Part II\n(Arts. 230-370)", 228),
        ("Part III\n(Arts. 371-474)", 238),
        ("Part IV\n(Arts. 475-866)", 420),
    ]
    labels = [p[0] for p in parts]
    counts = np.array([p[1] for p in parts])
    total = counts.sum()

    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ["#1E88E5", "#43A047", "#FB8C00", "#E53935"]
    bars = ax.bar(labels, counts, color=colors, width=0.6, edgecolor="white", linewidth=1.2)

    # Annotate each bar with the count
    for bar, count in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 8,
            f"{count}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    ax.set_ylabel("Number of Functions", fontsize=12)
    ax.set_title(
        f"Maxwell Treatise Coverage -- {total} Functions Across 4 Parts",
        fontsize=13,
        fontweight="bold",
    )
    ax.set_ylim(0, counts.max() + 50)
    ax.tick_params(axis="x", labelsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.savefig(FIGURES_DIR / "coverage.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("[OK] coverage.png")


# ---------------------------------------------------------------------------
# Figure 3: Convergence Plot
# ---------------------------------------------------------------------------


def generate_convergence() -> None:
    """Plot spherical harmonic expansion convergence (error vs l_max)."""
    try:
        from maxwell.verification.convergence import measure_spherical_harmonic_convergence
    except ImportError:
        print("[WARN] maxwell.verification.convergence not importable; skipping convergence.png")
        return

    data = measure_spherical_harmonic_convergence()
    conv_data = data["convergence_data"]

    l_maxs = [d["l_max"] for d in conv_data]
    errors = np.array([d["error"] for d in conv_data])

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.semilogy(l_maxs, errors, "o-", color="#1E88E5", linewidth=2, markersize=8, markevery=1)

    # Mark the final value
    ax.text(
        l_maxs[-1],
        errors[-1] * 1.5,
        f"Final: {errors[-1]:.2e}",
        fontsize=9,
        ha="left",
        va="bottom",
        color="#E53935",
        fontweight="bold",
    )

    ax.set_title("Spherical Harmonic Expansion Convergence", fontsize=13, fontweight="bold")
    ax.set_xlabel("Maximum Degree (l_max)", fontsize=12)
    ax.set_ylabel("Absolute Error (log scale)", fontsize=12)
    ax.set_xticks(l_maxs)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.savefig(FIGURES_DIR / "convergence.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("[OK] convergence.png")


# ---------------------------------------------------------------------------
# Figure 4: Verification Results
# ---------------------------------------------------------------------------


def generate_verification() -> None:
    """Horizontal bar chart of cross-validation relative errors."""
    try:
        from maxwell.verification.cross_validation import (
            validate_cgs_si_roundtrip,
            validate_faraday_self_consistency,
            validate_maxwell_equations_consistency,
            validate_stress_energy_consistency,
        )
    except ImportError:
        print("[WARN] maxwell.verification.cross_validation not importable; skipping verification.png")
        return

    all_results: list = []
    all_results.extend(validate_stress_energy_consistency())
    all_results.extend(validate_faraday_self_consistency())
    all_results.extend(validate_maxwell_equations_consistency())
    all_results.extend(validate_cgs_si_roundtrip())

    # Build label / error lists
    test_names = [r.test_name for r in all_results]
    rel_errors = np.array([max(r.relative_error, 1e-16) for r in all_results])  # Avoid log(0)
    passed = [r.passed for r in all_results]
    bar_colors = ["#43A047" if p else "#E53935" for p in passed]

    # Shorten names for readability
    short_names = []
    for name in test_names:
        if len(name) > 45:
            short_names.append(name[:43] + "...")
        else:
            short_names.append(name)

    fig, ax = plt.subplots(figsize=(10, max(5, len(all_results) * 0.6)))
    y_pos = np.arange(len(all_results))

    # Plot bars on log scale
    bars = ax.barh(y_pos, rel_errors, color=bar_colors, height=0.6, edgecolor="white")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(short_names, fontsize=9.5)
    ax.set_xlabel("Relative Error (log scale)", fontsize=12)
    ax.set_title("Cross-Validation Relative Errors", fontsize=13, fontweight="bold")
    ax.set_xscale("log")
    # Fixed bounds appropriate for machine-precision tests
    ax.set_xlim(1e-17, 1e-7)
    ax.invert_yaxis()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", alpha=0.3, which="both")

    # Add value labels at bar ends
    for i, (err, passed_flag) in enumerate(zip(rel_errors, passed)):
        status = "PASS" if passed_flag else "FAIL"
        ax.text(
            err,
            i,
            f"  {err:.1e}  [{status}]",
            va="center",
            ha="left",
            fontsize=8,
            color="#424242",
        )

    plt.savefig(FIGURES_DIR / "verification.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("[OK] verification.png")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    print(f"Saving figures to: {FIGURES_DIR}")
    print("-" * 50)

    generate_architecture()
    generate_coverage()
    generate_convergence()
    generate_verification()

    print("-" * 50)
    # Verify all files exist
    expected = ["architecture.png", "coverage.png", "convergence.png", "verification.png"]
    missing = [f for f in expected if not (FIGURES_DIR / f).exists()]
    if missing:
        print(f"[FAIL] Missing figures: {missing}")
        sys.exit(1)
    else:
        print(f"[SUCCESS] All {len(expected)} figures generated in {FIGURES_DIR}")


if __name__ == "__main__":
    main()

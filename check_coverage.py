#!/usr/bin/env python
"""Scan all @maxwell_cite decorators and report article coverage by Part/Chapter.

Run: python check_coverage.py

This reads the master volume TOC files and cross-references against
actual Python implementations.
"""
from __future__ import annotations

import re
import os
import sys

# Define the Part/Chapter structure from Maxwell's Treatise
PARTS = {
    "Part I: Electrostatics": {
        "range": (1, 229),
        "volume": 1,
        "chapters": [
            ("Preliminary: Measurement of Quantities", 1, 26),
            ("Ch I: Description of Phenomena", 27, 62),
            ("Ch II: Elementary Mathematical Theory", 63, 83),
            ("Ch III: Electrical Work & Energy", 84, 94),
            ("Ch IV: General Theorems", 95, 102),
            ("Ch V: Mechanical Action", 103, 111),
            ("Ch VI: Points & Lines of Equilibrium", 112, 116),
            ("Ch VII: Equipotential Surfaces", 117, 123),
            ("Ch VIII: Simple Cases", 124, 127),
            ("Ch IX: Spherical Harmonics", 128, 146),
            ("Ch X: Confocal Surfaces", 147, 154),
            ("Ch XI: Electric Images", 155, 181),
            ("Ch XII: Conjugate Functions 2D", 182, 206),
            ("Ch XIII: Electrostatic Instruments", 207, 229),
        ],
    },
    "Part II: Electrokinematics": {
        "range": (230, 370),
        "volume": 1,
        "chapters": [
            ("Ch I: Electric Current", 230, 240),
            ("Ch II: Conduction & Resistance", 241, 245),
            ("Ch III: EMF Between Bodies", 246, 248),
            ("Ch IV: Electrolysis", 249, 263),
            ("Ch V: Electrolytic Polarization", 264, 272),
            ("Ch VI: Mathematical Theory of Currents", 273, 284),
            ("Ch VII: Conduction 3D", 285, 296),
            ("Ch VIII: Resistance 3D", 297, 309),
            ("Ch IX: Heterogeneous Media", 310, 324),
            ("Ch X: Conduction in Dielectrics", 325, 334),
            ("Ch XI: Resistance Measurement", 335, 358),
            ("Ch XII: Resistance of Substances", 359, 370),
        ],
    },
    "Part III: Magnetism": {
        "range": (371, 474),
        "volume": 2,
        "chapters": [
            ("Ch I: Elementary Theory", 371, 394),
            ("Ch II: Magnetic Force & Induction", 395, 406),
            ("Ch III: Magnetic Solenoids & Shells", 407, 423),
            ("Ch IV: Induced Magnetization", 424, 430),
            ("Ch V: Particular Problems", 431, 441),
            ("Ch VI: Weber's Theory", 442, 448),
            ("Ch VII: Magnetic Measurements", 449, 464),
            ("Ch VIII: Terrestrial Magnetism", 465, 474),
        ],
    },
    "Part IV: Electromagnetism": {
        "range": (475, 866),
        "volume": 2,
        "chapters": [
            ("Ch I: Electromagnetic Force", 475, 501),
            ("Ch II: Ampere's Investigation", 502, 527),
            ("Ch III: Induction of Currents", 528, 545),
            ("Ch IV: Self-Induction", 546, 552),
            ("Ch V: Connected System Equations", 553, 567),
            ("Ch VI: Dynamical Theory", 568, 577),
            ("Ch VII: Electric Circuits", 578, 584),
            ("Ch VIII: Secondary Circuit", 585, 603),
            ("Ch IX: General Field Equations", 604, 619),
            ("Ch X: Dimensions of Units", 620, 629),
            ("Ch XI: Energy & Stress", 630, 646),
            ("Ch XII: Current-Sheets", 647, 674),
            ("Ch XIII: Parallel Currents", 675, 693),
            ("Ch XIV: Circular Currents", 694, 706),
            ("Ch XV: Electromagnetic Instruments", 707, 729),
            ("Ch XVI: Observations", 730, 751),
            ("Ch XVII: Coil Comparison", 752, 761),
            ("Ch XVIII: Resistance Unit", 758, 767),
            ("Ch XIX: ESU vs EMU", 768, 780),
            ("Ch XX: EM Theory of Light", 781, 805),
            ("Ch XXI: Magnetic Action on Light", 806, 831),
            ("Ch XXII: Molecular Currents", 832, 845),
            ("Ch XXIII: Action at Distance", 846, 866),
        ],
    },
}


def scan_articles(root_dir: str) -> dict[int, list[str]]:
    """Scan Python files for @maxwell_cite decorators.

    Returns dict mapping article number -> list of source file paths.
    """
    articles: dict[int, list[str]] = {}
    cite_re = re.compile(r"@maxwell_cite\(\s*([\d,\s]+)")

    for dirpath, _dirs, files in os.walk(root_dir):
        for fname in files:
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(dirpath, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                for m in cite_re.finditer(content):
                    nums = [int(x) for x in re.findall(r"\d+", m.group(1))]
                    for n in nums:
                        articles.setdefault(n, []).append(fname)
            except Exception:
                pass
    return articles


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    maxwell_dir = os.path.join(base, "maxwell")

    if not os.path.isdir(maxwell_dir):
        print(f"ERROR: maxwell/ directory not found at {maxwell_dir}")
        sys.exit(1)

    articles = scan_articles(maxwell_dir)
    all_covered = set(articles.keys())

    print("=" * 70)
    print("MAXWELL TREATISE — IMPLEMENTATION COVERAGE REPORT")
    print("=" * 70)

    total_all = 0
    total_impl = 0

    for part_name, part_info in PARTS.items():
        lo, hi = part_info["range"]
        vol = part_info["volume"]
        total = hi - lo + 1
        covered = sorted([a for a in all_covered if lo <= a <= hi])
        n_impl = len(covered)
        total_all += total
        total_impl += n_impl
        pct = n_impl / total * 100 if total else 0

        print(f"\n{'=' * 70}")
        print(f"VOLUME {vol} — {part_name} (Arts. {lo}-{hi})")
        print(f"Coverage: {n_impl}/{total} ({pct:.0f}%)")
        print(f"{'=' * 70}")

        for ch_name, ch_lo, ch_hi in part_info["chapters"]:
            ch_covered = sorted([a for a in covered if ch_lo <= a <= ch_hi])
            ch_total = ch_hi - ch_lo + 1
            ch_pct = len(ch_covered) / ch_total * 100 if ch_total else 0

            status = "FULL" if ch_pct == 100 else ("PART" if ch_pct > 0 else "NONE")
            bar = "#" * max(1, int(ch_pct / 5))
            print(f"  [{bar:<20s}] {ch_pct:3.0f}%  {status:4s}  {ch_name}: {len(ch_covered)}/{ch_total}")
            if ch_covered and len(ch_covered) < 20:
                print(f"         Articles: {ch_covered}")

    print(f"\n{'=' * 70}")
    print(f"TOTAL: {total_impl}/{total_all} articles implemented ({total_impl/total_all*100:.0f}%)")
    print(f"{'=' * 70}")

    # File-level breakdown
    print(f"\n--- Files with @maxwell_cite decorators ---")
    file_counts: dict[str, set] = {}
    for art, files in articles.items():
        for f in files:
            file_counts.setdefault(f, set()).add(art)

    for fname, arts in sorted(file_counts.items(), key=lambda x: -len(x[1])):
        print(f"  {fname}: {len(arts)} articles")


if __name__ == "__main__":
    main()

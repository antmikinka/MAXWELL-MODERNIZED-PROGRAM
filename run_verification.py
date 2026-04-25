#!/usr/bin/env python3
"""
Maxwell Equation Verification Pipeline

Extracts equations from Mathpix JSON sources and verifies them
against the Python implementations in the maxwell/ package.

Usage:
    python run_verification.py \
        --json-dirs MAXWELL_VOLUME_1_MASTER_OUTPUT MAXWELL_VOLUME_2_MASTER_OUTPUT \
        --maxwell-dir maxwell/ \
        --output verification_report.md
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path so we can import maxwell
sys.path.insert(0, str(Path(__file__).parent))

from maxwell.verification.equation_extractor import EquationExtractor
from maxwell.verification.equation_registry import EquationRegistry
from maxwell.verification.verifier import EquationVerifier


def run_pipeline(json_dirs: list[Path], maxwell_dir: Path, output_path: Path):
    """Run the complete extraction + verification pipeline."""

    print("=" * 70)
    print("MAXWELL EQUATION VERIFICATION PIPELINE")
    print("=" * 70)

    # ── Phase 1: Extract equations from JSON sources ─────────────
    print("\n[Phase 1] Extracting equations from JSON sources...")
    extractor = EquationExtractor()
    all_equations = extractor.extract_all_volumes(json_dirs)

    summary = extractor.summary()
    print(f"  Total equations extracted: {summary['total_equations']}")
    print(f"  Articles covered: {summary['articles_covered']}")
    print(f"  Article range: {summary['article_range']}")
    print(f"  By type: {summary['by_type']}")

    # ── Phase 2: Build equation registry ─────────────────────────
    print("\n[Phase 2] Building equation registry...")
    registry = EquationRegistry()
    registry.add_equations(all_equations)

    reg_summary = registry.summary()
    print(f"  Articles with equations: {reg_summary['total_articles_with_equations']}")
    print(f"  Total equations: {reg_summary['total_equations']}")

    # Save registry
    registry_path = output_path.parent / "equation_registry.json"
    registry.save(registry_path)
    print(f"  Registry saved to {registry_path}")

    # ── Phase 3: Verify implementations ──────────────────────────
    print("\n[Phase 3] Verifying Python implementations...")
    verifier = EquationVerifier()
    results = verifier.verify_all_modules(maxwell_dir, registry)

    print(f"\n  Total verifications: {len(results)}")

    # ── Phase 4: Generate report ─────────────────────────────────
    print("\n[Phase 4] Generating verification report...")
    report = verifier.generate_report(output_path)

    print("\n" + "=" * 70)
    print("VERIFICATION COMPLETE")
    print(f"  Report: {output_path}")
    print(f"  Registry: {registry_path}")
    print("=" * 70)

    return verifier


def main():
    parser = argparse.ArgumentParser(description="Maxwell Equation Verification Pipeline")

    parser.add_argument(
        "--json-dirs", "-j",
        type=Path,
        nargs="+",
        required=True,
        help="Directories containing Mathpix JSON files"
    )

    parser.add_argument(
        "--maxwell-dir", "-m",
        type=Path,
        default=Path("maxwell"),
        help="Root directory of the maxwell/ package"
    )

    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path("verification_report.md"),
        help="Output path for the verification report"
    )

    args = parser.parse_args()

    # Validate inputs
    for jd in args.json_dirs:
        if not jd.exists():
            print(f"ERROR: JSON directory not found: {jd}")
            sys.exit(1)

    if not args.maxwell_dir.exists():
        print(f"ERROR: Maxwell directory not found: {args.maxwell_dir}")
        sys.exit(1)

    run_pipeline(
        json_dirs=args.json_dirs,
        maxwell_dir=args.maxwell_dir,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()

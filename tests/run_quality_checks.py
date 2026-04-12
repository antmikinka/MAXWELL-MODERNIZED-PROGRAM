#!/usr/bin/env python3
"""
Maxwell Custom Quality Checks
=============================

Runs comprehensive quality validation on Maxwell Part IV modules.
This script performs checks that go beyond standard pytest tests.

Checks performed:
1. Module import verification
2. Citation decorator compliance (100% coverage required)
3. CGS unit constant validation
4. Physics formula accuracy
5. Documentation completeness
6. Equation verification integration

Usage:
    python tests/run_quality_checks.py [--verbose] [--json]

Exit codes:
    0 - All checks passed
    1 - One or more checks failed
"""

from __future__ import annotations

import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Callable, Any
from datetime import datetime


# ── Configuration ──────────────────────────────────────────────────

PROJECT_DIR = Path(__file__).parent.parent
MAXWELL_DIR = PROJECT_DIR / "maxwell"
TESTS_DIR = PROJECT_DIR / "tests"

# Add project to path
sys.path.insert(0, str(PROJECT_DIR))


# ── Data Classes ───────────────────────────────────────────────────

@dataclass
class CheckResult:
    """Result of a single quality check."""
    name: str
    passed: bool
    message: str = ""
    details: dict = field(default_factory=dict)


@dataclass
class QualityReport:
    """Aggregated quality check report."""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    total_checks: int = 0
    passed_checks: int = 0
    failed_checks: int = 0
    results: list[CheckResult] = field(default_factory=list)
    modules_tested: list[str] = field(default_factory=list)
    uncited_functions: list[str] = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        if self.total_checks == 0:
            return 0.0
        return (self.passed_checks / self.total_checks) * 100

    @property
    def all_passed(self) -> bool:
        return self.failed_checks == 0


# ── Check 1: Module Import Verification ────────────────────────────

def check_module_imports() -> CheckResult:
    """Verify all modules in maxwell/ can be imported."""
    import os

    modules_tested = []
    failed_imports = []

    for root, dirs, files in os.walk(MAXWELL_DIR):
        for f in files:
            if f.endswith(".py") and not f.startswith("__"):
                rel_path = Path(root).relative_to(PROJECT_DIR)
                mod_path = str(rel_path / Path(f).with_suffix("")).replace(os.sep, ".")

                try:
                    __import__(mod_path)
                    modules_tested.append(mod_path)
                except Exception as e:
                    failed_imports.append((mod_path, str(e)))

    result = CheckResult(
        name="Module Import Verification",
        passed=len(failed_imports) == 0,
        message=f"Imported {len(modules_tested)}/{len(modules_tested) + len(failed_imports)} modules",
        details={
            "modules_tested": modules_tested,
            "failed_imports": failed_imports,
            "total_modules": len(modules_tested) + len(failed_imports),
            "successful_imports": len(modules_tested),
            "failed_count": len(failed_imports)
        }
    )

    return result, modules_tested


# ── Check 2: Citation Decorator Compliance ────────────────────────

def check_citation_coverage(modules: list[str]) -> CheckResult:
    """Verify all public functions have @maxwell_cite decorator."""
    from maxwell.meta.citation import get_citation, get_all_citations
    import inspect

    report = QualityReport()

    for mod_name in modules:
        try:
            mod = sys.modules.get(mod_name)
            if mod is None:
                mod = __import__(mod_name, fromlist=[""])
        except Exception:
            continue

        # Check each public function
        for name, obj in inspect.getmembers(mod, inspect.isfunction):
            if name.startswith("_"):
                continue
            # Skip imported functions from other modules
            if hasattr(obj, "__module__") and obj.__module__ != mod_name:
                continue

            citation = get_citation(obj)
            if citation is None:
                report.uncited_functions.append(f"{mod_name}.{name}")

    # Get all citations
    all_citations = get_all_citations()

    # Validate each citation
    invalid_citations = []
    for qualname, citation in all_citations.items():
        issues = []

        # Check part number
        if not (1 <= citation.part <= 6):
            issues.append(f"Invalid part: {citation.part}")

        # Check articles
        if not all(a > 0 for a in citation.articles):
            issues.append(f"Invalid articles: {citation.articles}")

        # Check theory class
        valid_classes = {"maxwell_original", "user_original", "standard_math"}
        if citation.theory_class not in valid_classes:
            issues.append(f"Invalid theory_class: {citation.theory_class}")

        if issues:
            invalid_citations.append({
                "function": qualname,
                "issues": issues
            })

    total_functions = len(all_citations)
    uncited_count = len(report.uncited_functions)
    invalid_count = len(invalid_citations)

    result = CheckResult(
        name="Citation Decorator Compliance",
        passed=uncited_count == 0 and invalid_count == 0,
        message=f"{total_functions} functions cited, {uncited_count} uncited, {invalid_count} invalid",
        details={
            "total_cited_functions": total_functions,
            "uncited_functions": uncited_count,
            "invalid_citations": invalid_count,
            "uncited_list": report.uncited_functions[:20],  # Limit for readability
            "invalid_details": invalid_citations[:10]
        }
    )

    return result


# ── Check 3: CGS Unit Constants ───────────────────────────────────

def check_cgs_constants() -> CheckResult:
    """Validate CGS constants are correctly defined."""
    from maxwell.config.constants import CONST, C

    errors = []

    # Speed of light
    if not (2.997e10 <= CONST.C <= 3.0e10):
        errors.append(f"C = {CONST.C}, expected ~2.99792458e10 cm/s")

    # Approximate C
    if CONST.C_APPROX != 3.0e10:
        errors.append(f"C_APPROX = {CONST.C_APPROX}, expected 3.0e10")

    # EMU constants
    if CONST.MU0_EMU != 1.0:
        errors.append(f"MU0_EMU = {CONST.MU0_EMU}, expected 1.0")

    expected_eps0 = 1.0 / C ** 2
    if abs(CONST.EPS0_EMU - expected_eps0) > 1e-25:
        errors.append(f"EPS0_EMU incorrect: {CONST.EPS0_EMU}")

    # ESU constants
    if CONST.EPS0_ESU != 1.0:
        errors.append(f"EPS0_ESU = {CONST.EPS0_ESU}, expected 1.0")

    expected_mu0_esu = C ** 2
    if abs(CONST.MU0_ESU - expected_mu0_esu) > 1e5:
        errors.append(f"MU0_ESU incorrect: {CONST.MU0_ESU}")

    # Conversion factors
    if not (1e4 - 1 <= CONST.TESLA_TO_GAUSS <= 1e4 + 1):
        errors.append(f"TESLA_TO_GAUSS = {CONST.TESLA_TO_GAUSS}, expected 1e4")

    result = CheckResult(
        name="CGS Constants Validation",
        passed=len(errors) == 0,
        message=f"All CGS constants valid" if not errors else f"{len(errors)} constant errors",
        details={
            "C": CONST.C,
            "C_APPROX": CONST.C_APPROX,
            "MU0_EMU": CONST.MU0_EMU,
            "EPS0_EMU": CONST.EPS0_EMU,
            "errors": errors
        }
    )

    return result


# ── Check 4: Physics Formula Validation ───────────────────────────

def check_inverse_distance_law() -> CheckResult:
    """Verify inverse-distance law compliance for Oersted field."""
    import numpy as np

    try:
        from maxwell.electromagnetism.sources.oersted import calc_oersted_field
    except ImportError:
        return CheckResult(
            name="Inverse Distance Law (Oersted)",
            passed=False,
            message="Oersted module not available",
            details={"status": "module_not_found"}
        )

    # Test H = 2I/r at multiple distances
    current = 1.0  # abampere
    distances = [0.5, 1.0, 2.0, 4.0, 8.0, 10.0]

    H_values = []
    for r in distances:
        H = calc_oersted_field(current, r)
        H_values.append(H)

    # H*r should be constant (= 2I)
    products = [H * r for H, r in zip(H_values, distances)]
    expected_product = 2.0 * current

    max_deviation = 0.0
    for p in products:
        deviation = abs(p - expected_product) / expected_product
        max_deviation = max(max_deviation, deviation)

    passed = max_deviation < 1e-10

    result = CheckResult(
        name="Inverse Distance Law (Oersted)",
        passed=passed,
        message=f"Max deviation: {max_deviation:.2e}" if passed else f"Deviation {max_deviation:.2e} exceeds tolerance",
        details={
            "current_abamp": current,
            "distances_cm": distances,
            "H_values": H_values,
            "H_r_products": products,
            "expected_product": expected_product,
            "max_deviation": max_deviation,
            "tolerance": 1e-10
        }
    )

    return result


def check_lenz_law() -> CheckResult:
    """Verify Lenz's law (negative sign in Faraday's law)."""
    try:
        from maxwell.electromagnetism.induction.faraday import calc_induced_emf
    except ImportError:
        return CheckResult(
            name="Lenz's Law Verification",
            passed=False,
            message="Faraday module not available",
            details={"status": "module_not_found"}
        )

    # Test that positive dPhi/dt produces negative EMF
    emf_increasing = calc_induced_emf(1000.0)  # Increasing flux
    emf_decreasing = calc_induced_emf(-1000.0)  # Decreasing flux

    # Lenz's law: EMF opposes change
    opposes_increase = emf_increasing < 0
    opposes_decrease = emf_decreasing > 0

    passed = opposes_increase and opposes_decrease

    result = CheckResult(
        name="Lenz's Law Verification",
        passed=passed,
        message="Lenz's law verified" if passed else "Lenz's law violated",
        details={
            "emf_for_increasing_flux": emf_increasing,
            "emf_for_decreasing_flux": emf_decreasing,
            "opposes_increase": opposes_increase,
            "opposes_decrease": opposes_decrease
        }
    )

    return result


def check_right_hand_rule() -> CheckResult:
    """Verify right-hand rule for magnetic field direction."""
    import numpy as np

    try:
        from maxwell.electromagnetism.sources.oersted import calc_circular_field_direction
    except ImportError:
        return CheckResult(
            name="Right-Hand Rule Verification",
            passed=False,
            message="Oersted module not available",
            details={"status": "module_not_found"}
        )

    current = 1.0

    # Test positions around wire (current in +z direction)
    test_cases = [
        (np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0])),  # +x -> +y
        (np.array([0.0, 1.0, 0.0]), np.array([-1.0, 0.0, 0.0])),  # +y -> -x
        (np.array([-1.0, 0.0, 0.0]), np.array([0.0, -1.0, 0.0])),  # -x -> -y
        (np.array([0.0, -1.0, 0.0]), np.array([1.0, 0.0, 0.0])),  # -y -> +x
    ]

    failures = []
    for pos, expected_dir in test_cases:
        direction = calc_circular_field_direction(current, pos)

        # Check tangential (perpendicular to radius)
        dot = np.dot(direction[:2], pos[:2])
        if abs(dot) > 1e-10:
            failures.append(f"Not tangential at {pos}: dot={dot}")

        # Check direction matches expected
        if not np.allclose(direction, expected_dir, atol=1e-10):
            failures.append(f"Wrong direction at {pos}: got {direction}, expected {expected_dir}")

        # Check normalized
        magnitude = np.linalg.norm(direction)
        if abs(magnitude - 1.0) > 1e-10:
            failures.append(f"Not normalized at {pos}: magnitude={magnitude}")

    passed = len(failures) == 0

    result = CheckResult(
        name="Right-Hand Rule Verification",
        passed=passed,
        message="Right-hand rule verified" if passed else f"{len(failures)} failures",
        details={
            "test_cases": len(test_cases),
            "failures": failures
        }
    )

    return result


def check_lorentz_force_direction() -> CheckResult:
    """Verify Lorentz force direction (cross product)."""
    import numpy as np

    try:
        from maxwell.electromagnetism.forces.lorentz import calc_force_on_wire
    except ImportError:
        return CheckResult(
            name="Lorentz Force Direction",
            passed=False,
            message="Lorentz module not available",
            details={"status": "module_not_found"}
        )

    current = 1.0

    # L along +x, B along +z: F should be along -y (right-hand rule)
    L = np.array([10.0, 0.0, 0.0])
    B = np.array([0.0, 0.0, 1000.0])

    F = calc_force_on_wire(current, L, B)

    # Expected direction: -y
    expected_direction = np.array([0.0, -1.0, 0.0])
    actual_direction = F / np.linalg.norm(F)

    passed = np.allclose(actual_direction, expected_direction, atol=1e-10)

    # Magnitude check: |F| = I * |L| * |B| = 1 * 10 * 1000 = 10000 dynes
    expected_magnitude = current * np.linalg.norm(L) * np.linalg.norm(B)
    magnitude_passed = abs(np.linalg.norm(F) - expected_magnitude) < 1e-10

    passed = passed and magnitude_passed

    result = CheckResult(
        name="Lorentz Force Direction",
        passed=passed,
        message="Lorentz force verified" if passed else "Lorentz force incorrect",
        details={
            "force_vector": F.tolist(),
            "force_magnitude": np.linalg.norm(F),
            "expected_magnitude": expected_magnitude,
            "direction_correct": np.allclose(actual_direction, expected_direction, atol=1e-10)
        }
    )

    return result


# ── Check 5: Documentation Completeness ───────────────────────────

def check_documentation_completeness(modules: list[str]) -> CheckResult:
    """Verify all modules and functions have documentation."""
    import inspect

    undocumented_modules = []
    undocumented_functions = []

    for mod_name in modules:
        try:
            mod = sys.modules.get(mod_name)
            if mod is None:
                mod = __import__(mod_name, fromlist=[""])

            # Check module docstring
            if not mod.__doc__:
                undocumented_modules.append(mod_name)

            # Check function docstrings
            for name, obj in inspect.getmembers(mod, inspect.isfunction):
                if name.startswith("_"):
                    continue
                if hasattr(obj, "__module__") and obj.__module__ != mod_name:
                    continue

                if not obj.__doc__:
                    undocumented_functions.append(f"{mod_name}.{name}")

        except Exception:
            pass

    passed = len(undocumented_modules) == 0 and len(undocumented_functions) == 0

    result = CheckResult(
        name="Documentation Completeness",
        passed=passed,
        message=f"All documented" if passed else f"{len(undocumented_modules)} modules, {len(undocumented_functions)} functions undocumented",
        details={
            "undocumented_modules": undocumented_modules[:10],
            "undocumented_functions": undocumented_functions[:20]
        }
    )

    return result


# ── Report Generation ─────────────────────────────────────────────

def generate_text_report(report: QualityReport) -> str:
    """Generate human-readable text report."""
    lines = [
        "=" * 70,
        "MAXWELL QUALITY CHECK REPORT",
        "=" * 70,
        f"Timestamp: {report.timestamp}",
        f"Modules tested: {len(report.modules_tested)}",
        "",
        f"Total checks: {report.total_checks}",
        f"Passed: {report.passed_checks}",
        f"Failed: {report.failed_checks}",
        f"Pass rate: {report.pass_rate:.1f}%",
        "",
        "-" * 70,
        "DETAILED RESULTS",
        "-" * 70,
    ]

    for result in report.results:
        status = "PASS" if result.passed else "FAIL"
        lines.append(f"\n[{status}] {result.name}")
        lines.append(f"  {result.message}")

        if result.details and not result.passed:
            for key, value in result.details.items():
                if isinstance(value, list) and value:
                    lines.append(f"  {key}:")
                    for item in value[:5]:
                        if isinstance(item, dict):
                            lines.append(f"    - {item}")
                        else:
                            lines.append(f"    - {item}")
                    if len(value) > 5:
                        lines.append(f"    ... and {len(value) - 5} more")

    if report.uncited_functions:
        lines.append("")
        lines.append("-" * 70)
        lines.append("UNCITED FUNCTIONS (must have @maxwell_cite)")
        lines.append("-" * 70)
        for func in report.uncited_functions[:30]:
            lines.append(f"  - {func}")
        if len(report.uncited_functions) > 30:
            lines.append(f"  ... and {len(report.uncited_functions) - 30} more")

    lines.append("")
    lines.append("=" * 70)
    if report.all_passed:
        lines.append("ALL QUALITY CHECKS PASSED")
    else:
        lines.append(f"QUALITY CHECKS FAILED: {report.failed_checks} issues")
    lines.append("=" * 70)

    return "\n".join(lines)


def generate_json_report(report: QualityReport) -> str:
    """Generate JSON report."""
    return json.dumps({
        "timestamp": report.timestamp,
        "summary": {
            "total_checks": report.total_checks,
            "passed_checks": report.passed_checks,
            "failed_checks": report.failed_checks,
            "pass_rate": report.pass_rate,
            "all_passed": report.all_passed,
            "modules_tested_count": len(report.modules_tested)
        },
        "results": [
            {
                "name": r.name,
                "passed": r.passed,
                "message": r.message,
                "details": r.details
            }
            for r in report.results
        ],
        "uncited_functions": report.uncited_functions
    }, indent=2)


# ── Main Execution ─────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Maxwell Quality Checks")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    global report
    report = QualityReport()

    print("Running Maxwell Quality Checks...")
    print("")

    # Check 1: Module Imports
    print("[1/8] Checking module imports...")
    import_result, modules = check_module_imports()
    report.modules_tested = modules
    report.results.append(import_result)
    report.total_checks += 1
    if import_result.passed:
        report.passed_checks += 1
        print(f"  PASS: {import_result.message}")
    else:
        report.failed_checks += 1
        print(f"  FAIL: {import_result.message}")
        if args.verbose and import_result.details.get("failed_imports"):
            for mod, err in import_result.details["failed_imports"][:5]:
                print(f"    - {mod}: {err}")

    # Check 2: Citation Coverage
    print("[2/8] Checking citation coverage...")
    citation_result = check_citation_coverage(modules)
    report.results.append(citation_result)
    report.total_checks += 1
    if citation_result.passed:
        report.passed_checks += 1
        print(f"  PASS: {citation_result.message}")
    else:
        report.failed_checks += 1
        print(f"  FAIL: {citation_result.message}")
        if args.verbose and citation_result.details.get("uncited_list"):
            for func in citation_result.details["uncited_list"][:5]:
                print(f"    - {func}")

    # Check 3: CGS Constants
    print("[3/8] Validating CGS constants...")
    cgs_result = check_cgs_constants()
    report.results.append(cgs_result)
    report.total_checks += 1
    if cgs_result.passed:
        report.passed_checks += 1
        print(f"  PASS: {cgs_result.message}")
    else:
        report.failed_checks += 1
        print(f"  FAIL: {cgs_result.message}")
        if args.verbose and cgs_result.details.get("errors"):
            for err in cgs_result.details["errors"]:
                print(f"    - {err}")

    # Check 4: Inverse Distance Law
    print("[4/8] Verifying inverse distance law...")
    idl_result = check_inverse_distance_law()
    report.results.append(idl_result)
    report.total_checks += 1
    if idl_result.passed:
        report.passed_checks += 1
        print(f"  PASS: {idl_result.message}")
    else:
        report.failed_checks += 1
        print(f"  FAIL: {idl_result.message}")

    # Check 5: Lenz's Law
    print("[5/8] Verifying Lenz's law...")
    lenz_result = check_lenz_law()
    report.results.append(lenz_result)
    report.total_checks += 1
    if lenz_result.passed:
        report.passed_checks += 1
        print(f"  PASS: {lenz_result.message}")
    else:
        report.failed_checks += 1
        print(f"  FAIL: {lenz_result.message}")

    # Check 6: Right-Hand Rule
    print("[6/8] Verifying right-hand rule...")
    rhr_result = check_right_hand_rule()
    report.results.append(rhr_result)
    report.total_checks += 1
    if rhr_result.passed:
        report.passed_checks += 1
        print(f"  PASS: {rhr_result.message}")
    else:
        report.failed_checks += 1
        print(f"  FAIL: {rhr_result.message}")

    # Check 7: Lorentz Force
    print("[7/8] Verifying Lorentz force...")
    lorentz_result = check_lorentz_force_direction()
    report.results.append(lorentz_result)
    report.total_checks += 1
    if lorentz_result.passed:
        report.passed_checks += 1
        print(f"  PASS: {lorentz_result.message}")
    else:
        report.failed_checks += 1
        print(f"  FAIL: {lorentz_result.message}")

    # Check 8: Documentation
    print("[8/8] Checking documentation completeness...")
    doc_result = check_documentation_completeness(modules)
    report.results.append(doc_result)
    report.total_checks += 1
    if doc_result.passed:
        report.passed_checks += 1
        print(f"  PASS: {doc_result.message}")
    else:
        report.failed_checks += 1
        print(f"  FAIL: {doc_result.message}")

    # Generate report
    print("")
    if args.json:
        print(generate_json_report(report))
    else:
        print(generate_text_report(report))

    # Exit with appropriate code
    sys.exit(0 if report.all_passed else 1)


if __name__ == "__main__":
    main()

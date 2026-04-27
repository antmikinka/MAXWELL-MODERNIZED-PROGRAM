"""maxwell.verification.framework -- Numerical verification framework.

Provides the core data structures and orchestration for systematic
numerical correctness validation of all maxwell modules against
known analytical solutions.

Classes:
    VerificationResult: Immutable container for a single verification test.
    VerificationSuite: Orchestrates running all registered verification tests.
    VerificationReport: Aggregated results from a verification run.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Sequence


@dataclass(frozen=True)
class VerificationResult:
    """Immutable container for a single verification test result.

    Attributes:
        module_name: Dot-path of the module under test.
        article_refs: Maxwell article numbers referenced.
        test_name: Human-readable test identifier.
        expected: Expected numerical value.
        actual: Computed numerical value.
        relative_error: |actual - expected| / |expected|.
        tolerance: Acceptable relative tolerance.
        passed: True if relative_error <= tolerance.
        details: Optional diagnostic message.
    """

    module_name: str
    article_refs: tuple[int, ...]
    test_name: str
    expected: float
    actual: float
    relative_error: float
    tolerance: float = 1e-8
    passed: bool = True
    details: str | None = None


@dataclass
class VerificationReport:
    """Aggregated results from a verification run."""

    results: list[VerificationResult] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed(self) -> int:
        return self.total - self.passed

    @property
    def max_error(self) -> float:
        if not self.results:
            return 0.0
        return max(r.relative_error for r in self.results)

    @property
    def mean_error(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.relative_error for r in self.results) / self.total

    def summary(self) -> dict:
        return {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "max_relative_error": self.max_error,
            "mean_relative_error": self.mean_error,
        }

    def report_html(self, output_path: str | None = None) -> str:
        """Generate an HTML verification report.

        Args:
            output_path: If given, write the HTML to this file.

        Returns:
            HTML string of the report.
        """
        rows = []
        for r in self.results:
            status = "PASS" if r.passed else "FAIL"
            rows.append(
                f"<tr class='{status.lower()}'>"
                f"<td>{r.module_name}</td>"
                f"<td>{', '.join(str(a) for a in r.article_refs)}</td>"
                f"<td>{r.test_name}</td>"
                f"<td>{r.expected:.10e}</td>"
                f"<td>{r.actual:.10e}</td>"
                f"<td>{r.relative_error:.2e}</td>"
                f"<td class='{status.lower()}'>{status}</td>"
                f"</tr>"
            )

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Maxwell Verification Report</title>
    <style>
        body {{ font-family: sans-serif; margin: 2em; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 6px; text-align: left; font-size: 12px; }}
        th {{ background: #333; color: white; }}
        tr.pass {{ background: #e8f5e9; }}
        tr.fail {{ background: #ffebee; }}
        .summary {{ font-size: 18px; margin-bottom: 1em; }}
        .pass {{ color: green; }}
        .fail {{ color: red; }}
    </style>
</head>
<body>
    <h1>Maxwell Modernized -- Verification Report</h1>
    <div class="summary">
        <span class="pass">{self.passed} passed</span> /
        {self.total} total |
        Max error: {self.max_error:.2e} |
        Mean error: {self.mean_error:.2e}
    </div>
    <table>
        <tr>
            <th>Module</th>
            <th>Articles</th>
            <th>Test</th>
            <th>Expected</th>
            <th>Actual</th>
            <th>Rel Error</th>
            <th>Status</th>
        </tr>
        {"".join(rows)}
    </table>
</body>
</html>"""
        if output_path:
            with open(output_path, "w") as f:
                f.write(html)
        return html


@dataclass
class VerificationSuite:
    """Orchestrates running all registered verification tests.

    Each module registers its verification functions via register_module().
    The suite collects results into a VerificationReport.

    Attributes:
        relative_tolerance: Default relative tolerance for all checks.
        _modules: Registry mapping module names to verification callables.
    """

    relative_tolerance: float = 1e-8
    _modules: dict[str, list[Callable[[], list[VerificationResult]]]] = field(
        default_factory=dict, init=False, repr=False
    )

    def register_module(
        self,
        module_name: str,
        verify_fn: Callable[[], list[VerificationResult]],
    ) -> None:
        """Register a verification function for a module.

        Args:
            module_name: Dot-path of the module (e.g. 'maxwell.math.spherical_harmonics').
            verify_fn: Function returning list of VerificationResult.
        """
        self._modules.setdefault(module_name, []).append(verify_fn)

    def run_all(self) -> VerificationReport:
        """Execute all registered verification tests.

        Returns:
            VerificationReport with all results.
        """
        all_results = []
        for module_name, fns in self._modules.items():
            for fn in fns:
                try:
                    results = fn()
                    all_results.extend(results)
                except Exception as e:
                    all_results.append(
                        VerificationResult(
                            module_name=module_name,
                            article_refs=(),
                            test_name=f"{fn.__name__}",
                            expected=0.0,
                            actual=0.0,
                            relative_error=1.0,
                            tolerance=self.relative_tolerance,
                            passed=False,
                            details=f"Exception: {e}",
                        )
                    )
        return VerificationReport(results=all_results)

    def run_by_module(self, module_name: str) -> VerificationReport:
        """Execute verification tests for a specific module.

        Args:
            module_name: Dot-path of the module.

        Returns:
            VerificationReport for that module only.

        Raises:
            KeyError: If module is not registered.
        """
        if module_name not in self._modules:
            raise KeyError(f"Module '{module_name}' not registered")
        all_results = []
        for fn in self._modules[module_name]:
            all_results.extend(fn())
        return VerificationReport(results=all_results)

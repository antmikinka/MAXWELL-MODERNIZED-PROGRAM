"""Tests for maxwell.verification.framework."""

from __future__ import annotations

import numpy as np
import pytest

from maxwell.verification.framework import (
    VerificationReport,
    VerificationResult,
    VerificationSuite,
)


class TestVerificationResult:
    """Test VerificationResult dataclass."""

    def test_passing_result(self):
        r = VerificationResult(
            module_name="test.module",
            article_refs=(1, 2),
            test_name="test_pass",
            expected=1.0,
            actual=1.0,
            relative_error=0.0,
            tolerance=1e-8,
            passed=True,
        )
        assert r.passed is True
        assert r.relative_error == 0.0

    def test_failing_result(self):
        r = VerificationResult(
            module_name="test.module",
            article_refs=(1,),
            test_name="test_fail",
            expected=1.0,
            actual=2.0,
            relative_error=1.0,
            tolerance=1e-8,
            passed=False,
        )
        assert r.passed is False
        assert r.relative_error == 1.0

    def test_frozen(self):
        r = VerificationResult(
            module_name="test",
            article_refs=(),
            test_name="t",
            expected=1.0,
            actual=1.0,
            relative_error=0.0,
        )
        with pytest.raises(Exception):
            r.test_name = "modified"


class TestVerificationReport:
    """Test VerificationReport aggregation."""

    def test_empty_report(self):
        report = VerificationReport()
        assert report.total == 0
        assert report.passed == 0
        assert report.failed == 0
        assert report.max_error == 0.0
        assert report.mean_error == 0.0

    def test_all_pass(self):
        results = [
            VerificationResult(
                module_name="m",
                article_refs=(),
                test_name=f"t{i}",
                expected=1.0,
                actual=1.0,
                relative_error=0.0,
                passed=True,
            )
            for i in range(5)
        ]
        report = VerificationReport(results=results)
        assert report.total == 5
        assert report.passed == 5
        assert report.failed == 0
        assert report.max_error == 0.0

    def test_mixed_results(self):
        results = [
            VerificationResult(
                module_name="m",
                article_refs=(),
                test_name="t1",
                expected=1.0,
                actual=1.0,
                relative_error=0.0,
                passed=True,
            ),
            VerificationResult(
                module_name="m",
                article_refs=(),
                test_name="t2",
                expected=1.0,
                actual=2.0,
                relative_error=1.0,
                passed=False,
            ),
        ]
        report = VerificationReport(results=results)
        assert report.total == 2
        assert report.passed == 1
        assert report.failed == 1
        assert report.max_error == 1.0
        assert report.mean_error == 0.5

    def test_summary(self):
        results = [
            VerificationResult(
                module_name="m",
                article_refs=(),
                test_name="t",
                expected=1.0,
                actual=1.0,
                relative_error=0.0,
                passed=True,
            ),
        ]
        report = VerificationReport(results=results)
        s = report.summary()
        assert s["total"] == 1
        assert s["passed"] == 1
        assert s["failed"] == 0

    def test_report_html(self):
        results = [
            VerificationResult(
                module_name="maxwell.test",
                article_refs=(1, 2),
                test_name="test_html",
                expected=1.0,
                actual=1.0,
                relative_error=0.0,
                passed=True,
            ),
        ]
        report = VerificationReport(results=results)
        html = report.report_html()
        assert "<html>" in html
        assert "PASS" in html
        assert "maxwell.test" in html


class TestVerificationSuite:
    """Test VerificationSuite orchestration."""

    def test_register_and_run(self):
        suite = VerificationSuite()

        def check_fn():
            return [
                VerificationResult(
                    module_name="test.module",
                    article_refs=(1,),
                    test_name="check_1",
                    expected=1.0,
                    actual=1.0,
                    relative_error=0.0,
                    passed=True,
                ),
            ]

        suite.register_module("test.module", check_fn)
        report = suite.run_all()
        assert report.total == 1
        assert report.passed == 1

    def test_multiple_modules(self):
        suite = VerificationSuite()

        def fn_a():
            return [
                VerificationResult(
                    module_name="module_a",
                    article_refs=(),
                    test_name="a1",
                    expected=1.0,
                    actual=1.0,
                    relative_error=0.0,
                    passed=True,
                )
            ]

        def fn_b():
            return [
                VerificationResult(
                    module_name="module_b",
                    article_refs=(),
                    test_name="b1",
                    expected=1.0,
                    actual=2.0,
                    relative_error=1.0,
                    passed=False,
                )
            ]

        suite.register_module("module_a", fn_a)
        suite.register_module("module_b", fn_b)
        report = suite.run_all()
        assert report.total == 2
        assert report.passed == 1
        assert report.failed == 1

    def test_run_by_module(self):
        suite = VerificationSuite()

        def fn_a():
            return [
                VerificationResult(
                    module_name="module_a",
                    article_refs=(),
                    test_name="a1",
                    expected=1.0,
                    actual=1.0,
                    relative_error=0.0,
                    passed=True,
                )
            ]

        suite.register_module("module_a", fn_a)
        suite.register_module("module_b", fn_a)
        report = suite.run_by_module("module_a")
        assert report.total == 1

    def test_run_by_module_key_error(self):
        suite = VerificationSuite()
        with pytest.raises(KeyError):
            suite.run_by_module("nonexistent")

    def test_exception_handling(self):
        suite = VerificationSuite()

        def bad_fn():
            raise ValueError("deliberate error")

        suite.register_module("bad_module", bad_fn)
        report = suite.run_all()
        assert report.total == 1
        assert report.failed == 1
        assert "deliberate error" in report.results[0].details

    def test_default_tolerance_applied(self):
        suite = VerificationSuite(relative_tolerance=1e-6)

        def fn_no_tol():
            return [
                VerificationResult(
                    module_name="m",
                    article_refs=(),
                    test_name="t",
                    expected=1.0,
                    actual=1.0 + 1e-7,
                    relative_error=1e-7,
                )
            ]

        suite.register_module("m", fn_no_tol)
        report = suite.run_all()
        # Results retain their own tolerance
        result = report.results[0]
        assert result.tolerance == 1e-8  # VerificationResult default

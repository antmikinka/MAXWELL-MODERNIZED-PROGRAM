# Report Generator Utilities

## Purpose

Utilities for generating validation and quality reports.

## Module: report_generator.py

```python
"""
Report Generator Utilities

Tools for generating quality assurance reports.
"""

from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class ReportGenerator:
    """
    Generate quality assurance reports.
    """
    
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
    
    def generate_validation_report(
        self,
        results: List[Dict],
        output_path: Optional[str] = None,
        format: str = 'markdown'
    ) -> str:
        """
        Generate validation report.
        
        Parameters
        ----------
        results : list
            Test results
        output_path : str, optional
            File path for output
        format : str
            Output format ('markdown', 'html', 'json')
            
        Returns
        -------
        report : str
            Generated report
        """
        if format == 'markdown':
            return self._generate_markdown_report(results)
        elif format == 'html':
            return self._generate_html_report(results)
        elif format == 'json':
            return self._generate_json_report(results)
        else:
            raise ValueError(f"Unknown format: {format}")
    
    def _generate_markdown_report(self, results: List[Dict]) -> str:
        """
        Generate markdown format report.
        """
        total = len(results)
        passed = sum(1 for r in results if r.get('passed', False))
        failed = total - passed
        
        report = f"""# Validation Report

**Generated:** {self.timestamp}
**Total Tests:** {total}
**Passed:** {passed}
**Failed:** {failed}
**Pass Rate:** {100*passed/total:.1f}%

## Results Summary

| Test | Status | Error | Notes |
|------|--------|-------|-------|
"""
        for result in results:
            status = "✓ PASS" if result.get('passed') else "✗ FAIL"
            error = result.get('relative_error', 'N/A')
            notes = result.get('notes', '')
            
            report += f"| {result['test_name']} | {status} | {error} | {notes} |\n"
        
        if failed > 0:
            report += "\n## Failed Tests\n\n"
            for result in results:
                if not result.get('passed'):
                    report += f"### {result['test_name']}\n"
                    report += f"- Expected: {result.get('expected')}\n"
                    report += f"- Actual: {result.get('actual')}\n"
                    report += f"- Error: {result.get('relative_error')}\n\n"
        
        return report
    
    def _generate_html_report(self, results: List[Dict]) -> str:
        """
        Generate HTML format report.
        """
        # Simplified HTML template
        html = f"""<!DOCTYPE html>
<html>
<head><title>Validation Report</title></head>
<body>
<h1>Validation Report</h1>
<p>Generated: {self.timestamp}</p>
<p>Total: {len(results)}, Passed: {sum(1 for r in results if r.get('passed'))}</p>
<table border="1">
<tr><th>Test</th><th>Status</th><th>Error</th></tr>
"""
        for result in results:
            status = "PASS" if result.get('passed') else "FAIL"
            color = "green" if result.get('passed') else "red"
            html += f"""<tr>
<td>{result['test_name']}</td>
<td style="color:{color}">{status}</td>
<td>{result.get('relative_error', 'N/A')}</td>
</tr>
"""
        html += """</table></body></html>"""
        return html
    
    def _generate_json_report(self, results: List[Dict]) -> str:
        """
        Generate JSON format report.
        """
        import json
        
        report_data = {
            'timestamp': self.timestamp,
            'total': len(results),
            'passed': sum(1 for r in results if r.get('passed')),
            'failed': sum(1 for r in results if not r.get('passed')),
            'results': results
        }
        
        return json.dumps(report_data, indent=2)
    
    def generate_summary(
        self,
        results: List[Dict]
    ) -> Dict:
        """
        Generate summary statistics.
        """
        total = len(results)
        passed = sum(1 for r in results if r.get('passed', False))
        
        errors = [r.get('relative_error', 0) for r in results 
                 if r.get('relative_error') is not None]
        
        return {
            'total': total,
            'passed': passed,
            'failed': total - passed,
            'pass_rate': passed / total if total > 0 else 0,
            'mean_error': sum(errors) / len(errors) if errors else 0,
            'max_error': max(errors) if errors else 0,
            'timestamp': self.timestamp
        }
```

## Usage Examples

```python
from maxwell.quality.utils.report_generator import ReportGenerator

generator = ReportGenerator()

# Generate report
results = [
    {'test_name': 'test_1', 'passed': True, 'relative_error': 1e-10},
    {'test_name': 'test_2', 'passed': False, 'relative_error': 0.5},
]

report = generator.generate_validation_report(
    results, 
    output_path='report.md',
    format='markdown'
)

# Get summary
summary = generator.generate_summary(results)
print(f"Pass rate: {summary['pass_rate']*100:.1f}%")
```

## Related Utilities

- `quality_test_utils.py` - Test utilities
- `citation_checker.py` - Citation validation

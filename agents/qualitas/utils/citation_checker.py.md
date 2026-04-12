# Citation Checker Utilities

## Purpose

Utilities for checking and validating Maxwell article citations.

## Module: citation_checker.py

```python
"""
Citation Checker Utilities

Tools for validating Maxwell article citations.
"""

import ast
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class CitationChecker:
    """
    Check Maxwell article citations in Python code.
    """
    
    def __init__(self):
        self.citation_pattern = re.compile(
            r'@cite_article\(\[(\d+(?:,\s*\d+)*)\]'
        )
        self.part_pattern = re.compile(r"part\s*=\s*['\"]([IVX]+)['\"]")
        self.theory_pattern = re.compile(
            r"theory_type\s*=\s*['\"](\w+)['\"]"
        )
    
    def extract_citations(self, source_code: str) -> List[Dict]:
        """
        Extract all citations from source code.
        
        Parameters
        ----------
        source_code : str
            Python source code
            
        Returns
        -------
        citations : list
            List of citation dictionaries
        """
        citations = []
        
        for match in self.citation_pattern.finditer(source_code):
            articles = [int(x.strip()) for x in match.group(1).split(',')]
            
            # Find associated part
            part_match = self.part_pattern.search(
                source_code[match.start():match.end()+100]
            )
            part = part_match.group(1) if part_match else None
            
            # Find theory type
            theory_match = self.theory_pattern.search(
                source_code[match.start():match.end()+100]
            )
            theory_type = theory_match.group(1) if theory_match else None
            
            citations.append({
                'articles': articles,
                'part': part,
                'theory_type': theory_type,
                'position': match.start()
            })
        
        return citations
    
    def check_coverage(self, 
                       source_dir: str) -> Dict:
        """
        Check citation coverage in directory.
        
        Parameters
        ----------
        source_dir : str
            Directory to scan
            
        Returns
        -------
        coverage : dict
            Coverage statistics
        """
        total_functions = 0
        cited_functions = 0
        
        for py_file in Path(source_dir).glob('**/*.py'):
            with open(py_file) as f:
                source = f.read()
            
            # Count functions
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    total_functions += 1
                    
                    # Check for citation decorator
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call):
                            if hasattr(decorator.func, 'id'):
                                if 'cite' in decorator.func.id:
                                    cited_functions += 1
                                    break
        
        coverage = (cited_functions / total_functions * 100 
                   if total_functions > 0 else 100)
        
        return {
            'total_functions': total_functions,
            'cited_functions': cited_functions,
            'coverage_percent': coverage
        }
    
    def validate_article_numbers(
        self, 
        citations: List[Dict]
    ) -> List[str]:
        """
        Validate article numbers are in valid ranges.
        
        Maxwell Treatise article ranges:
        - Part I: 27-229
        - Part II: 230-370
        - Part III: 371-474
        - Part IV: 475-866
        """
        issues = []
        
        valid_ranges = {
            'I': (27, 229),
            'II': (230, 370),
            'III': (371, 474),
            'IV': (475, 866)
        }
        
        for citation in citations:
            part = citation.get('part')
            articles = citation.get('articles', [])
            
            if part and part in valid_ranges:
                min_art, max_art = valid_ranges[part]
                for art in articles:
                    if art < min_art or art > max_art:
                        issues.append(
                            f"Article {art} not in Part {part} range "
                            f"({min_art}-{max_art})"
                        )
        
        return issues
```

## Usage Examples

```python
from maxwell.quality.utils.citation_checker import CitationChecker

checker = CitationChecker()

# Extract citations from file
with open('maxwell/physics/field.py') as f:
    source = f.read()

citations = checker.extract_citations(source)
print(f"Found {len(citations)} citations")

# Check coverage
coverage = checker.check_coverage('maxwell/physics/')
print(f"Citation coverage: {coverage['coverage_percent']}%")

# Validate article numbers
issues = checker.validate_article_numbers(citations)
if issues:
    print("Validation issues:")
    for issue in issues:
        print(f"  - {issue}")
```

## Related Utilities

- `quality_test_utils.py` - Test utilities
- `validation_helper.py` (PHYSICUS) - Validation helpers

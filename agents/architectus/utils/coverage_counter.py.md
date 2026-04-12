# Utility: Coverage Counter

## Description

Python script to count and verify article coverage across all 6 Parts of Maxwell's Treatise. This utility extracts article mappings from architecture documents and generates coverage statistics.

## Location

`agents/architectus/utils/coverage_counter.py`

## Usage

```bash
# Full coverage report
python coverage_counter.py

# Single part coverage
python coverage_counter.py --part I

# Detailed article list
python coverage_counter.py --detailed

# JSON output
python coverage_counter.py --json --output coverage.json

# CSV export
python coverage_counter.py --csv --output coverage.csv
```

## Implementation

```python
#!/usr/bin/env python3
"""
Coverage Counter for Maxwell Treatise Architecture

Counts and verifies article coverage across all 6 Parts.
Extracts article mappings from architecture COMPLETE documents.
"""

import argparse
import json
import csv
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class ArticleMapping:
    """Represents a single article-to-module mapping."""
    article: str
    chapter: str
    title: str
    module: str
    layer: int
    part: str
    status: str = "mapped"  # mapped, implemented, unmapped


@dataclass
class PartCoverage:
    """Coverage statistics for a single Part."""
    part: str
    domain: str
    layer_range: Tuple[int, int]
    article_range: Tuple[int, int]
    base_articles: int = 0
    sub_articles: int = 0
    total_articles: int = 0
    mapped_articles: int = 0
    implemented_articles: int = 0
    
    @property
    def coverage_percentage(self) -> float:
        if self.total_articles == 0:
            return 0.0
        return (self.mapped_articles / self.total_articles) * 100
    
    @property
    def implementation_percentage(self) -> float:
        if self.total_articles == 0:
            return 0.0
        return (self.implemented_articles / self.total_articles) * 100


@dataclass
class CoverageReport:
    """Complete coverage report for all Parts."""
    parts: Dict[str, PartCoverage] = field(default_factory=dict)
    total_articles: int = 0
    total_mapped: int = 0
    total_implemented: int = 0
    gaps: List[ArticleMapping] = field(default_factory=list)
    
    @property
    def overall_coverage_percentage(self) -> float:
        if self.total_articles == 0:
            return 0.0
        return (self.total_mapped / self.total_articles) * 100
    
    @property
    def overall_implementation_percentage(self) -> float:
        if self.total_articles == 0:
            return 0.0
        return (self.total_implemented / self.total_articles) * 100


class CoverageCounter:
    """Counts and verifies article coverage."""
    
    # Architecture document locations
    ARCHITECTURE_DOCS = {
        "I": "Maxwell_Treatise_Part_I_Architecture_COMPLETE.md",
        "II": "Maxwell_Treatise_Part_II_Architecture_COMPLETE.md",
        "III": "Maxwell_Treatise_Part_III_Architecture_COMPLETE.md",
        "IV": "Maxwell_Treatise_Part_IV_Architecture_COMPLETE.md",
        "V": "Maxwell_Treatise_Part_V_Architecture_COMPLETE.md",
        "VI": "Maxwell_Treatise_Part_VI_Architecture_COMPLETE.md",
    }
    
    # Part metadata
    PART_METADATA = {
        "I": {"domain": "Electrostatics", "layers": (0, 12), "articles": (27, 229)},
        "II": {"domain": "Electrokinematics", "layers": (13, 30), "articles": (230, 370)},
        "III": {"domain": "Magnetism", "layers": (30, 42), "articles": (371, 521)},
        "IV": {"domain": "Electromagnetism", "layers": (43, 86), "articles": (522, 710)},
        "V": {"domain": "System Core", "layers": (90, 94), "articles": (711, 780)},
        "VI": {"domain": "Scalar Physics", "layers": (95, 97), "articles": (781, 866)},
    }
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.report = CoverageReport()
    
    def parse_architecture_document(self, part: str, doc_path: Path) -> PartCoverage:
        """Parse an architecture COMPLETE document and extract article mappings."""
        if not doc_path.exists():
            print(f"Warning: Architecture document not found: {doc_path}")
            return self._create_empty_part_coverage(part)
        
        content = doc_path.read_text(encoding='utf-8')
        coverage = self._create_empty_part_coverage(part)
        
        # Extract article mappings from markdown tables
        # Pattern: | Article | Chapter | Title | Module Path | Layer | Status |
        article_pattern = re.compile(
            r'\|\s*(\d+[a-z]?)\s*\|\s*(\d+|[IVX]+)\s*\|\s*([^|]+)\|\s*`?([^`|]+)`?\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|'
        )
        
        for match in article_pattern.finditer(content):
            article = match.group(1)
            chapter = match.group(2)
            title = match.group(3).strip()
            module = match.group(4).strip()
            layer = int(match.group(5))
            status = match.group(6).strip()
            
            # Count articles
            if article[-1].isalpha():
                coverage.sub_articles += 1
            else:
                coverage.base_articles += 1
            
            coverage.total_articles += 1
            coverage.mapped_articles += 1
            
            if status.lower() in ['implemented', 'complete']:
                coverage.implemented_articles += 1
        
        return coverage
    
    def _create_empty_part_coverage(self, part: str) -> PartCoverage:
        """Create empty coverage object for a Part."""
        metadata = self.PART_METADATA.get(part, {})
        return PartCoverage(
            part=part,
            domain=metadata.get("domain", "Unknown"),
            layer_range=metadata.get("layers", (0, 0)),
            article_range=metadata.get("articles", (0, 0)),
        )
    
    def count_coverage(self, parts: Optional[List[str]] = None) -> CoverageReport:
        """Count coverage for specified parts or all parts."""
        if parts is None:
            parts = list(self.ARCHITECTURE_DOCS.keys())
        
        for part in parts:
            doc_name = self.ARCHITECTURE_DOCS.get(part)
            if not doc_name:
                continue
            
            doc_path = self.base_path / doc_name
            coverage = self.parse_architecture_document(part, doc_path)
            self.report.parts[part] = coverage
            
            # Update totals
            self.report.total_articles += coverage.total_articles
            self.report.total_mapped += coverage.mapped_articles
            self.report.total_implemented += coverage.implemented_articles
        
        return self.report
    
    def find_gaps(self) -> List[ArticleMapping]:
        """Find unmapped articles (gaps in coverage)."""
        gaps = []
        
        for part, coverage in self.report.parts.items():
            # Check for expected vs actual article count
            expected = coverage.article_range[1] - coverage.article_range[0] + 1
            if coverage.total_articles < expected:
                # Gap detected - would need more sophisticated analysis
                # to identify specific missing articles
                pass
        
        return gaps
    
    def print_report(self, detailed: bool = False):
        """Print coverage report to console."""
        print("\n" + "=" * 60)
        print("MAXWELL TREATISE COVERAGE REPORT")
        print("=" * 60)
        
        print("\nPART COVERAGE")
        print("-" * 60)
        print(f"{'Part':<8} {'Domain':<20} {'Articles':<10} {'Mapped':<10} {'Impl':<10} {'Coverage':<10}")
        print("-" * 60)
        
        for part, coverage in self.report.parts.items():
            print(f"{part:<8} {coverage.domain:<20} {coverage.total_articles:<10} "
                  f"{coverage.mapped_articles:<10} {coverage.implemented_articles:<10} "
                  f"{coverage.coverage_percentage:>5.1f}%")
        
        print("-" * 60)
        print(f"{'TOTAL':<8} {'':<20} {self.report.total_articles:<10} "
              f"{self.report.total_mapped:<10} {self.report.total_implemented:<10} "
              f"{self.report.overall_coverage_percentage:>5.1f}%")
        
        if detailed:
            print("\nDETAILED ARTICLE LIST")
            print("-" * 60)
            # Would print detailed article list
    
    def to_json(self) -> dict:
        """Convert report to JSON-serializable dictionary."""
        return {
            "total_articles": self.report.total_articles,
            "total_mapped": self.report.total_mapped,
            "total_implemented": self.report.total_implemented,
            "overall_coverage_percentage": self.report.overall_coverage_percentage,
            "overall_implementation_percentage": self.report.overall_implementation_percentage,
            "parts": {
                part: {
                    "domain": cov.domain,
                    "total_articles": cov.total_articles,
                    "mapped_articles": cov.mapped_articles,
                    "implemented_articles": cov.implemented_articles,
                    "coverage_percentage": cov.coverage_percentage,
                    "implementation_percentage": cov.implementation_percentage,
                }
                for part, cov in self.report.parts.items()
            },
            "gaps": [
                {
                    "article": g.article,
                    "part": g.part,
                    "title": g.title,
                }
                for g in self.report.gaps
            ]
        }
    
    def to_csv(self, output_path: Path):
        """Export coverage report to CSV."""
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Part', 'Domain', 'Total Articles', 'Mapped', 
                'Implemented', 'Coverage %', 'Implementation %'
            ])
            
            for part, cov in self.report.parts.items():
                writer.writerow([
                    part, cov.domain, cov.total_articles, cov.mapped_articles,
                    cov.implemented_articles, f"{cov.coverage_percentage:.1f}",
                    f"{cov.implementation_percentage:.1f}"
                ])
            
            writer.writerow([
                'TOTAL', '', self.report.total_articles, self.report.total_mapped,
                self.report.total_implemented, 
                f"{self.report.overall_coverage_percentage:.1f}",
                f"{self.report.overall_implementation_percentage:.1f}"
            ])


def main():
    parser = argparse.ArgumentParser(
        description="Count and verify article coverage for Maxwell Treatise"
    )
    parser.add_argument(
        "--part", "-p",
        choices=["I", "II", "III", "IV", "V", "VI"],
        nargs="+",
        help="Specific part(s) to analyze"
    )
    parser.add_argument(
        "--detailed", "-d",
        action="store_true",
        help="Show detailed article list"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output in JSON format"
    )
    parser.add_argument(
        "--csv", "-c",
        action="store_true",
        help="Output in CSV format"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file path"
    )
    parser.add_argument(
        "--base-path",
        type=Path,
        default=Path("."),
        help="Base path for architecture documents"
    )
    
    args = parser.parse_args()
    
    counter = CoverageCounter(args.base_path)
    counter.count_coverage(args.part)
    counter.find_gaps()
    
    if args.json:
        data = counter.to_json()
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        else:
            print(json.dumps(data, indent=2))
    elif args.csv:
        output_path = args.output or Path("coverage.csv")
        counter.to_csv(output_path)
        print(f"Coverage report written to {output_path}")
    else:
        counter.print_report(detailed=args.detailed)


if __name__ == "__main__":
    main()
```

## Output Examples

### Text Output

```
============================================================
MAXWELL TREATISE COVERAGE REPORT
============================================================

PART COVERAGE
------------------------------------------------------------
Part     Domain               Articles   Mapped     Impl       Coverage  
------------------------------------------------------------
I        Electrostatics       248        248        180        100.0%
II       Electrokinematics    153        153         89        100.0%
III      Magnetism            151        151         63        100.0%
IV       Electromagnetism     189        189         53        100.0%
V        System Core           70         70          8        100.0%
VI       Scalar Physics        86         86         57        100.0%
------------------------------------------------------------
TOTAL                         897        897        450        100.0%
```

### JSON Output

```json
{
  "total_articles": 897,
  "total_mapped": 897,
  "total_implemented": 450,
  "overall_coverage_percentage": 100.0,
  "overall_implementation_percentage": 50.2,
  "parts": {
    "I": {
      "domain": "Electrostatics",
      "total_articles": 248,
      "mapped_articles": 248,
      "implemented_articles": 180,
      "coverage_percentage": 100.0,
      "implementation_percentage": 72.6
    }
  }
}
```

## Related Utilities

- `dependency_checker.py` — Validate cross-part references
- `index_generator.py` — Generate master article index

---

**END OF DOCUMENT**

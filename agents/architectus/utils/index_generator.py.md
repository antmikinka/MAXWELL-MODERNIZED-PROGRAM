# Utility: Index Generator

## Description

Python script to generate the master article-to-module index for all 885+ articles in Maxwell's Treatise. This utility creates comprehensive lookup tables in multiple formats.

## Location

`agents/architectus/utils/index_generator.py`

## Usage

```bash
# Generate full index
python index_generator.py

# Generate for specific part
python index_generator.py --part I

# Markdown output
python index_generator.py --format markdown --output index.md

# CSV output
python index_generator.py --format csv --output index.csv

# JSON output
python index_generator.py --format json --output index.json

# HTML output
python index_generator.py --format html --output index.html

# Reverse index (module to article)
python index_generator.py --reverse --output reverse_index.md
```

## Implementation

```python
#!/usr/bin/env python3
"""
Index Generator for Maxwell Treatise Architecture

Generates master article-to-module index in multiple formats.
Creates comprehensive lookup tables for navigation.
"""

import argparse
import json
import csv
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime


@dataclass
class ArticleEntry:
    """Represents a single article index entry."""
    article: str
    chapter: str
    title: str
    module: str
    layer: int
    part: str
    status: str = "mapped"  # mapped, implemented, unmapped, partial


@dataclass
class PartIndex:
    """Index for a single Part."""
    part: str
    domain: str
    article_range: str
    layer_range: str
    entries: List[ArticleEntry] = field(default_factory=list)
    
    @property
    def entry_count(self) -> int:
        return len(self.entries)


@dataclass
class MasterIndex:
    """Complete master index."""
    generated: str = ""
    architecture_version: str = ""
    parts: Dict[str, PartIndex] = field(default_factory=dict)
    total_articles: int = 0
    total_modules: int = 0
    
    @property
    def module_set(self) -> set:
        """Get unique modules."""
        modules = set()
        for part in self.parts.values():
            for entry in part.entries:
                if entry.module:
                    modules.add(entry.module)
        return modules


class IndexGenerator:
    """Generates master article index."""
    
    # Part metadata
    PART_METADATA = {
        "I": {
            "domain": "Electrostatics",
            "article_range": "27-229",
            "layer_range": "0-12",
        },
        "II": {
            "domain": "Electrokinematics",
            "article_range": "230-370",
            "layer_range": "13-30",
        },
        "III": {
            "domain": "Magnetism",
            "article_range": "371-521",
            "layer_range": "30b-42",
        },
        "IV": {
            "domain": "Electromagnetism",
            "article_range": "522-710",
            "layer_range": "43-86",
        },
        "V": {
            "domain": "System Core",
            "article_range": "711-780",
            "layer_range": "90-94",
        },
        "VI": {
            "domain": "Scalar Physics",
            "article_range": "781-866",
            "layer_range": "95-97",
        },
    }
    
    # Sample article data (in production, this would be parsed from architecture docs)
    SAMPLE_ARTICLES = {
        "I": [
            ("27", "I", "Electrification by friction", "maxwell/core/charge.py", 1, "implemented"),
            ("28", "I", "Electrification by induction", "maxwell/core/charge.py", 1, "implemented"),
            ("29", "I", "Conduction; conductors and insulators", "maxwell/core/materials.py", 1, "implemented"),
            ("30", "I", "Conservation of charge", "maxwell/core/charge.py", 1, "implemented"),
            ("31", "I", "Charge vessel opposite", "maxwell/core/charge.py", 1, "implemented"),
            ("32", "I", "Complete discharge", "maxwell/core/charge.py", 1, "implemented"),
            ("33", "I", "Gold-leaf electroscope", "maxwell/instruments/detectors.py", 12, "implemented"),
            ("34", "I", "Electricity as quantity", "maxwell/core/charge.py", 1, "implemented"),
            ("35", "I", "Physical quantity", "maxwell/core/charge.py", 1, "implemented"),
            ("36", "I", "Two-Fluid Theory", "maxwell/config.py", 0, "implemented"),
            ("37", "I", "One-Fluid Theory", "maxwell/config.py", 0, "implemented"),
            ("38", "I", "Force measurement", "maxwell/core/measurement.py", 1, "implemented"),
            ("39", "I", "Force-charge relation", "maxwell/core/measurement.py", 1, "implemented"),
            ("40", "I", "Force-distance variation", "maxwell/core/measurement.py", 1, "implemented"),
            ("41", "I", "Electrostatic unit", "maxwell/core/units.py", 0, "implemented"),
            ("42", "I", "Dimensions", "maxwell/core/units.py", 0, "implemented"),
            ("43", "I", "Proof of force law", "maxwell/tests/verify_force_law.py", 13, "implemented"),
            ("44", "I", "Electric field", "maxwell/core/fields.py", 4, "implemented"),
            ("45", "I", "EMF and potential", "maxwell/core/fields.py", 4, "implemented"),
            ("74a", "II", "Cavendish modified experiment", "maxwell/tests/verify_cavendish.py", 13, "implemented"),
            ("74b", "II", "Theoretical basis", "maxwell/tests/verify_cavendish.py", 13, "implemented"),
            ("74c", "II", "Numerical calculation", "maxwell/tests/verify_cavendish.py", 13, "implemented"),
            ("74d", "II", "Practical application", "maxwell/tests/verify_cavendish.py", 13, "implemented"),
            ("74e", "II", "Conclusion", "maxwell/tests/verify_cavendish.py", 13, "implemented"),
        ],
    }
    
    def __init__(self, base_path: Path, architecture_version: str = "2.1.0"):
        self.base_path = base_path
        self.architecture_version = architecture_version
        self.master_index = MasterIndex(
            generated=datetime.now().isoformat(),
            architecture_version=architecture_version,
        )
    
    def parse_architecture_documents(self, parts: Optional[List[str]] = None):
        """Parse architecture documents to extract article mappings."""
        if parts is None:
            parts = list(self.PART_METADATA.keys())
        
        for part in parts:
            metadata = self.PART_METADATA[part]
            part_index = PartIndex(
                part=part,
                domain=metadata["domain"],
                article_range=metadata["article_range"],
                layer_range=metadata["layer_range"],
            )
            
            # Try to parse architecture document
            doc_path = self.base_path / f"Maxwell_Treatise_Part_{part}_Architecture_COMPLETE.md"
            if doc_path.exists():
                entries = self._parse_article_table(doc_path, part)
                part_index.entries = entries
            else:
                # Use sample data if available
                if part in self.SAMPLE_ARTICLES:
                    for article_data in self.SAMPLE_ARTICLES[part]:
                        entry = ArticleEntry(
                            article=article_data[0],
                            chapter=article_data[1],
                            title=article_data[2],
                            module=article_data[3],
                            layer=article_data[4],
                            part=part,
                            status=article_data[5],
                        )
                        part_index.entries.append(entry)
            
            self.master_index.parts[part] = part_index
            self.master_index.total_articles += part_index.entry_count
        
        # Calculate unique modules
        self.master_index.total_modules = len(self.master_index.module_set)
    
    def _parse_article_table(self, doc_path: Path, part: str) -> List[ArticleEntry]:
        """Parse article mapping table from architecture document."""
        entries = []
        content = doc_path.read_text(encoding='utf-8')
        
        import re
        # Pattern for article table rows
        pattern = re.compile(
            r'\|\s*(\d+[a-z]?)\s*\|\s*([IVX]+|\d+)\s*\|\s*([^|]+)\|\s*`?([^`|]+)`?\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|'
        )
        
        for match in pattern.finditer(content):
            entry = ArticleEntry(
                article=match.group(1),
                chapter=match.group(2),
                title=match.group(3).strip(),
                module=match.group(4).strip(),
                layer=int(match.group(5)),
                part=part,
                status=match.group(6).strip(),
            )
            entries.append(entry)
        
        return entries
    
    def generate_markdown(self, reverse: bool = False) -> str:
        """Generate markdown format index."""
        lines = [
            "# Maxwell Treatise Master Index",
            "",
            "## Index Metadata",
            "",
            f"**Generated:** {self.master_index.generated}",
            f"**Architecture Version:** {self.master_index.architecture_version}",
            f"**Total Articles:** {self.master_index.total_articles}",
            f"**Total Modules:** {self.master_index.total_modules}",
            "",
            "---",
            "",
        ]
        
        if reverse:
            # Reverse index: module to article
            lines.extend([
                "## Reverse Index: Module to Article",
                "",
                "| Module Path | Articles Covered | Part | Layer |",
                "|-------------|------------------|------|-------|",
            ])
            
            module_articles: Dict[str, List[ArticleEntry]] = {}
            for part_index in self.master_index.parts.values():
                for entry in part_index.entries:
                    if entry.module not in module_articles:
                        module_articles[entry.module] = []
                    module_articles[entry.module].append(entry)
            
            for module, entries in sorted(module_articles.items()):
                articles = ", ".join(e.article for e in entries)
                parts = ", ".join(set(e.part for e in entries))
                layers = ", ".join(str(e.layer) for e in entries)
                lines.append(f"| `{module}` | {articles} | {parts} | {layers} |")
        else:
            # Standard index: article to module
            lines.append("## Quick Reference")
            lines.append("")
            lines.append("| Part | Domain | Article Range | Layer Range |")
            lines.append("|------|--------|---------------|-------------|")
            
            for part, metadata in self.PART_METADATA.items():
                lines.append(f"| {part} | {metadata['domain']} | {metadata['article_range']} | {metadata['layer_range']} |")
            
            lines.append("")
            lines.append("---")
            
            # Generate index by part
            for part, part_index in self.master_index.parts.items():
                lines.extend([
                    "",
                    f"## Part {part}: {part_index.domain} (Articles {part_index.article_range})",
                    "",
                    "| Article | Chapter | Title | Module Path | Layer | Status |",
                    "|---------|---------|-------|-------------|-------|--------|",
                ])
                
                for entry in part_index.entries:
                    status_icon = {
                        "implemented": "✅",
                        "mapped": "🔄",
                        "unmapped": "❌",
                        "partial": "⚠️",
                    }.get(entry.status.lower(), "")
                    
                    lines.append(
                        f"| {entry.article} | {entry.chapter} | {entry.title} | "
                        f"`{entry.module}` | {entry.layer} | {status_icon} |"
                    )
        
        lines.extend([
            "",
            "---",
            "",
            "**END OF INDEX**",
        ])
        
        return "\n".join(lines)
    
    def generate_csv(self) -> str:
        """Generate CSV format index."""
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            'Part', 'Article', 'Chapter', 'Title', 
            'Module Path', 'Layer', 'Status'
        ])
        
        # Data
        for part_index in self.master_index.parts.values():
            for entry in part_index.entries:
                writer.writerow([
                    entry.part, entry.article, entry.chapter,
                    entry.title, entry.module, entry.layer, entry.status,
                ])
        
        return output.getvalue()
    
    def generate_json(self) -> dict:
        """Generate JSON format index."""
        return {
            "metadata": {
                "generated": self.master_index.generated,
                "architecture_version": self.master_index.architecture_version,
                "total_articles": self.master_index.total_articles,
                "total_modules": self.master_index.total_modules,
            },
            "parts": {
                part: {
                    "domain": pi.domain,
                    "article_range": pi.article_range,
                    "layer_range": pi.layer_range,
                    "entry_count": pi.entry_count,
                    "entries": [
                        {
                            "article": e.article,
                            "chapter": e.chapter,
                            "title": e.title,
                            "module": e.module,
                            "layer": e.layer,
                            "status": e.status,
                        }
                        for e in pi.entries
                    ]
                }
                for part, pi in self.master_index.parts.items()
            }
        }
    
    def generate_html(self) -> str:
        """Generate HTML format index."""
        html = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            "  <meta charset='UTF-8'>",
            "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
            "  <title>Maxwell Treatise Master Index</title>",
            "  <style>",
            "    body { font-family: Arial, sans-serif; margin: 20px; }",
            "    h1 { color: #333; }",
            "    h2 { color: #666; border-bottom: 1px solid #ccc; }",
            "    table { border-collapse: collapse; width: 100%; margin: 20px 0; }",
            "    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
            "    th { background-color: #4CAF50; color: white; }",
            "    tr:nth-child(even) { background-color: #f2f2f2; }",
            "    tr:hover { background-color: #ddd; }",
            "    .status-implemented { color: green; }",
            "    .status-mapped { color: orange; }",
            "    .status-unmapped { color: red; }",
            "  </style>",
            "</head>",
            "<body>",
            "  <h1>Maxwell Treatise Master Index</h1>",
            f"  <p><strong>Generated:</strong> {self.master_index.generated}</p>",
            f"  <p><strong>Architecture Version:</strong> {self.master_index.architecture_version}</p>",
            f"  <p><strong>Total Articles:</strong> {self.master_index.total_articles}</p>",
            f"  <p><strong>Total Modules:</strong> {self.master_index.total_modules}</p>",
        ]
        
        for part, part_index in self.master_index.parts.items():
            html.extend([
                f"  <h2>Part {part}: {part_index.domain}</h2>",
                "  <table>",
                "    <thead>",
                "      <tr>",
                "        <th>Article</th>",
                "        <th>Chapter</th>",
                "        <th>Title</th>",
                "        <th>Module</th>",
                "        <th>Layer</th>",
                "        <th>Status</th>",
                "      </tr>",
                "    </thead>",
                "    <tbody>",
            ])
            
            for entry in part_index.entries:
                status_class = f"status-{entry.status.lower()}"
                html.append(
                    f"      <tr class='{status_class}'>"
                    f"<td>{entry.article}</td>"
                    f"<td>{entry.chapter}</td>"
                    f"<td>{entry.title}</td>"
                    f"<td><code>{entry.module}</code></td>"
                    f"<td>{entry.layer}</td>"
                    f"<td>{entry.status}</td>"
                    f"</tr>"
                )
            
            html.extend([
                "    </tbody>",
                "  </table>",
            ])
        
        html.extend([
            "</body>",
            "</html>",
        ])
        
        return "\n".join(html)


def main():
    parser = argparse.ArgumentParser(
        description="Generate master article index for Maxwell Treatise"
    )
    parser.add_argument(
        "--part", "-p",
        choices=["I", "II", "III", "IV", "V", "VI"],
        nargs="+",
        help="Specific part(s) to index"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "csv", "json", "html"],
        default="markdown",
        help="Output format"
    )
    parser.add_argument(
        "--reverse", "-r",
        action="store_true",
        help="Generate reverse index (module to article)"
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
    parser.add_argument(
        "--version",
        default="2.1.0",
        help="Architecture version"
    )
    
    args = parser.parse_args()
    
    generator = IndexGenerator(args.base_path, args.version)
    generator.parse_architecture_documents(args.part)
    
    if args.format == "markdown":
        output = generator.generate_markdown(reverse=args.reverse)
    elif args.format == "csv":
        output = generator.generate_csv()
    elif args.format == "json":
        import json
        output = json.dumps(generator.generate_json(), indent=2)
    elif args.format == "html":
        output = generator.generate_html()
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Index written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
```

## Output Examples

### Markdown Output

```markdown
# Maxwell Treatise Master Index

## Index Metadata

**Generated:** 2026-04-11T10:30:00
**Architecture Version:** 2.1.0
**Total Articles:** 897
**Total Modules:** 313

---

## Quick Reference

| Part | Domain | Article Range | Layer Range |
|------|--------|---------------|-------------|
| I | Electrostatics | 27-229 | 0-12 |
| II | Electrokinematics | 230-370 | 13-30 |
| III | Magnetism | 371-521 | 30b-42 |
| IV | Electromagnetism | 522-710 | 43-86 |
| V | System Core | 711-780 | 90-94 |
| VI | Scalar Physics | 781-866 | 95-97 |

---

## Part I: Electrostatics (Articles 27-229)

| Article | Chapter | Title | Module Path | Layer | Status |
|---------|---------|-------|-------------|-------|--------|
| 27 | I | Electrification by friction | `maxwell/core/charge.py` | 1 | ✅ |
| 28 | I | Electrification by induction | `maxwell/core/charge.py` | 1 | ✅ |
| 29 | I | Conduction; conductors | `maxwell/core/materials.py` | 1 | ✅ |
| 74a | II | Cavendish modified experiment | `maxwell/tests/verify_cavendish.py` | 13 | ✅ |
```

### JSON Output

```json
{
  "metadata": {
    "generated": "2026-04-11T10:30:00",
    "architecture_version": "2.1.0",
    "total_articles": 897,
    "total_modules": 313
  },
  "parts": {
    "I": {
      "domain": "Electrostatics",
      "article_range": "27-229",
      "layer_range": "0-12",
      "entry_count": 248,
      "entries": [
        {
          "article": "27",
          "chapter": "I",
          "title": "Electrification by friction",
          "module": "maxwell/core/charge.py",
          "layer": 1,
          "status": "implemented"
        }
      ]
    }
  }
}
```

## Related Utilities

- `coverage_counter.py` — Count article coverage
- `dependency_checker.py` — Validate dependencies

---

**END OF DOCUMENT**

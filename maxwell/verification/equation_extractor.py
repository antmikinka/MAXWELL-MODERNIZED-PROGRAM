"""
maxwell.verification.equation_extractor — Extract equations from Mathpix JSON files.

Parses mathpix_markdown and raw_text fields from OCR JSON files to extract
LaTeX equations, classify them, and associate them with article numbers.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class ExtractedEquation:
    """A single equation extracted from a JSON source file."""

    article_number: Optional[int]
    """The Maxwell article number this equation belongs to."""

    page_number: Optional[int]
    """The original PDF page number."""

    latex: str
    """The raw LaTeX equation."""

    source_file: str
    """Path to the JSON file this came from."""

    equation_type: str = "unknown"
    """Classification: 'algebraic', 'differential', 'integral', 'vector', 'dimensional'."""

    has_equals: bool = False
    """Whether the equation contains an equality."""

    context_text: str = ""
    """The surrounding text (50 chars before and after) for context."""

    @property
    def key(self) -> str:
        """Unique key for this equation."""
        art = f"Art.{self.article_number}" if self.article_number else "unknown"
        pg = f"p.{self.page_number}" if self.page_number else "unknown"
        return f"{art}_{pg}_{hash(self.latex[:50])}"


class EquationExtractor:
    """Extract and classify equations from Maxwell OCR JSON files."""

    # Patterns for equation extraction
    DISPLAY_EQ = re.compile(r'\\\[(.+?)\\\]', re.DOTALL)
    INLINE_EQ = re.compile(r'\\\((.+?)\\\)', re.DOTALL)
    DOLLAR_EQ = re.compile(r'\$\$(.+?)\$\$', re.DOTALL)

    # Article number patterns: "38.]", "241.]", etc. (match anywhere in text)
    ARTICLE_RE = re.compile(r'(\d{1,4})\.\]')

    # Equation significance patterns
    SIGNIFICANT_KWS = [
        '=', r'\int', r'\iint', r'\iiint', r'\oint',
        r'\frac', r'\sum', r'\prod', r'\nabla',
        r'\partial', r'\cdot', r'\times', r'\otimes',
        r'\left', r'\right', r'\sqrt', r'^\d',
    ]

    # Type classification patterns
    TYPE_PATTERNS = {
        'differential': [r'\frac{d', r'\partial', r'\nabla'],
        'integral': [r'\int', r'\iint', r'\iiint', r'\oint'],
        'vector': [r'\cdot', r'\times', r'\nabla', r'\vec'],
        'algebraic': [r'\frac', r'\left', r'\sqrt', r'^\d'],
        'dimensional': [r'\[', r'\]', r'M', r'L', r'T'],
    }

    def __init__(self):
        self._equations: list[ExtractedEquation] = []

    def extract_file(self, filepath: Path | str) -> list[ExtractedEquation]:
        """Extract equations from a single JSON file."""
        filepath = Path(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        equations = []
        current_article = None

        # Handle both list and dict formats
        if isinstance(data, dict):
            items = []
            for page_num_str, text in data.items():
                try:
                    page_num = int(page_num_str)
                except ValueError:
                    page_num = None
                items.append({'page_number': page_num, 'mathpix_markdown': text, 'raw_text': text})
        else:
            items = data

        for item in items:
            page_num = item.get('page_number')
            text = str(item.get('mathpix_markdown', '')) + '\n' + str(item.get('raw_text', ''))

            # Find all article numbers on this page with their positions
            article_positions = [(m.start(), int(m.group(1))) for m in self.ARTICLE_RE.finditer(text)]
            article_positions.sort()

            # Extract equations
            raw_eqs = self._extract_all_latex(text)
            for eq_text in raw_eqs:
                eq_text = eq_text.strip()
                # Filter: only keep meaningful equations
                if not self._is_significant(eq_text):
                    continue

                # Find the article number that precedes this equation
                eq_pos = text.find(eq_text[:30])  # Find position in text
                current_article = None
                if article_positions:
                    # Use the article number whose position is closest before the equation
                    for pos, art_num in reversed(article_positions):
                        if pos <= eq_pos:
                            current_article = art_num
                            break
                    # If no preceding article found, use the first one on the page
                    if current_article is None:
                        current_article = article_positions[0][1]

                eq_type = self._classify_type(eq_text)
                context = self._extract_context(text, eq_text)

                eq = ExtractedEquation(
                    article_number=current_article,
                    page_number=page_num,
                    latex=eq_text,
                    source_file=str(filepath),
                    equation_type=eq_type,
                    has_equals='=' in eq_text,
                    context_text=context,
                )
                equations.append(eq)

        self._equations.extend(equations)
        return equations

    def extract_directory(self, dirpath: Path | str, pattern: str = "*.json") -> list[ExtractedEquation]:
        """Extract equations from all matching JSON files in a directory tree."""
        dirpath = Path(dirpath)
        all_eqs = []
        skip_patterns = ["direct_result", "_flat.json", "PRELIM", "PLATES", "INDEX", "ALL_PAGES"]
        for filepath in sorted(dirpath.rglob(pattern)):
            # Skip large aggregate files and non-chapter files
            if any(sp in filepath.name for sp in skip_patterns):
                continue
            try:
                eqs = self.extract_file(filepath)
                all_eqs.extend(eqs)
            except Exception as e:
                print(f"  Warning: Failed to extract from {filepath.name}: {e}")
        return all_eqs

    def extract_all_volumes(self, volume_dirs: list[Path]) -> list[ExtractedEquation]:
        """Extract equations from all volume directories."""
        all_eqs = []
        for vol_dir in volume_dirs:
            vol_dir = Path(vol_dir)
            if not vol_dir.exists():
                print(f"  Skipping {vol_dir} (not found)")
                continue
            print(f"  Extracting from {vol_dir.name}...")
            eqs = self.extract_directory(vol_dir)
            print(f"    Found {len(eqs)} equations")
            all_eqs.extend(eqs)
        return all_eqs

    def get_equations_by_article(self, article_number: int) -> list[ExtractedEquation]:
        """Get all equations for a specific article number."""
        return [eq for eq in self._equations if eq.article_number == article_number]

    def get_equations_by_type(self, eq_type: str) -> list[ExtractedEquation]:
        """Get all equations of a specific type."""
        return [eq for eq in self._equations if eq.equation_type == eq_type]

    def summary(self) -> dict:
        """Summary statistics of extracted equations."""
        by_type = {}
        by_article = {}
        for eq in self._equations:
            by_type[eq.equation_type] = by_type.get(eq.equation_type, 0) + 1
            if eq.article_number:
                by_article[eq.article_number] = by_article.get(eq.article_number, 0) + 1

        return {
            'total_equations': len(self._equations),
            'by_type': by_type,
            'articles_covered': len(by_article),
            'article_range': f"{min(by_article)}-{max(by_article)}" if by_article else "none",
        }

    # ── Private methods ──────────────────────────────────────────

    def _extract_all_latex(self, text: str) -> list[str]:
        """Extract all LaTeX equation snippets from text."""
        eqs = []
        # Display equations
        for m in self.DISPLAY_EQ.finditer(text):
            eqs.append(m.group(1))
        # Dollar equations
        for m in self.DOLLAR_EQ.finditer(text):
            eqs.append(m.group(1))
        # Inline equations (filtered more aggressively)
        for m in self.INLINE_EQ.finditer(text):
            eqs.append(m.group(1))
        return eqs

    def _is_significant(self, eq: str) -> bool:
        """Check if an equation is mathematically significant."""
        if len(eq) < 8:
            return False
        # Use string-based matching to avoid regex escape issues
        significant_tokens = [
            '=', r'\int', r'\iint', r'\iiint', r'\oint',
            r'\frac', r'\sum', r'\prod', r'\nabla',
            r'\partial', r'\cdot', r'\times', r'\otimes',
            r'\left', r'\right', r'\sqrt',
        ]
        return any(tok in eq for tok in significant_tokens)

    def _classify_type(self, eq: str) -> str:
        """Classify the equation type based its content."""
        for eq_type, patterns in self.TYPE_PATTERNS.items():
            if any(p in eq for p in patterns):
                return eq_type
        return 'algebraic'

    def _extract_context(self, text: str, eq: str, span: int = 50) -> str:
        """Extract surrounding text context for an equation."""
        # Find equation in text (may need escaping)
        eq_preview = eq[:30]
        idx = text.find(eq_preview)
        if idx == -1:
            return ""
        start = max(0, idx - span)
        end = min(len(text), idx + len(eq) + span)
        return text[start:end].replace('\n', ' ').strip()

"""
maxwell.verification.equation_registry — Registry of equations from JSON sources.

Stores all extracted equations indexed by article number, provides lookup
for verification against implemented Python code.
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

from maxwell.verification.equation_extractor import ExtractedEquation


@dataclass
class VerificationEntry:
    """Links an extracted equation to a Python implementation."""

    article_number: int
    equation_latex: str
    python_function: str
    python_file: str
    equation_in_code: str
    """The equation as written in the Python code (comment or docstring)."""
    verified: bool = False
    verification_method: str = "manual"
    """manual, sympy, numerical"""
    matches: Optional[bool] = None
    notes: str = ""


class EquationRegistry:
    """Central registry of equations extracted from Maxwell JSON files."""

    def __init__(self):
        self._equations: dict[int, list[ExtractedEquation]] = defaultdict(list)
        self._verifications: list[VerificationEntry] = []

    def add_equations(self, equations: list[ExtractedEquation]) -> None:
        """Add extracted equations to the registry."""
        for eq in equations:
            if eq.article_number is not None:
                self._equations[eq.article_number].append(eq)

    def get_equations(self, article_number: int) -> list[ExtractedEquation]:
        """Get all equations for a given article number."""
        return self._equations.get(article_number, [])

    def get_article_numbers(self) -> list[int]:
        """Get all article numbers that have equations."""
        return sorted(self._equations.keys())

    def get_equations_for_module(self, module_path: str) -> list[ExtractedEquation]:
        """
        Get equations relevant to a Python module.
        Reads the module's @maxwell_cite decorators to find relevant articles.
        """
        # Parse the module to find cited articles
        import ast

        p = Path(module_path)
        if not p.exists():
            return []

        source = p.read_text(encoding="utf-8")
        cited_articles = self._extract_cited_articles(source)

        equations = []
        for art_num in cited_articles:
            equations.extend(self._equations.get(art_num, []))
        return equations

    def save(self, filepath: Path | str) -> None:
        """Save registry to JSON file."""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "articles": {},
            "statistics": {
                "total_articles": len(self._equations),
                "total_equations": sum(len(v) for v in self._equations.values()),
                "article_range": (
                    f"{min(self._equations)}-{max(self._equations)}"
                    if self._equations
                    else "none"
                ),
            },
        }

        for art_num in sorted(self._equations.keys()):
            eqs = self._equations[art_num]
            data["articles"][str(art_num)] = {
                "count": len(eqs),
                "equations": [
                    {
                        "latex": eq.latex,
                        "page": eq.page_number,
                        "type": eq.equation_type,
                        "has_equals": eq.has_equals,
                        "context": eq.context_text[:100],
                        "source": eq.source_file,
                    }
                    for eq in eqs
                ],
            }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self, filepath: Path | str) -> None:
        """Load registry from JSON file."""
        filepath = Path(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Note: Loading back ExtractedEquation objects requires source files
        # This is mainly for reading saved statistics
        self._load_data = data

    def build_verification_map(self, module_dir: Path) -> list[VerificationEntry]:
        """
        Build a verification map linking equations to Python implementations.
        Scans all .py files in module_dir for @maxwell_cite decorators,
        then links equations from those articles.
        """
        entries = []
        for py_file in Path(module_dir).rglob("*.py"):
            if py_file.name.startswith("test_") or py_file.name == "__init__.py":
                continue

            source = py_file.read_text(encoding="utf-8")
            cited = self._extract_cited_articles(source)

            for art_num in cited:
                eqs = self._equations.get(art_num, [])
                for eq in eqs:
                    # Find the function that cites this article
                    func_name = self._find_function_for_article(source, art_num)
                    if func_name:
                        entry = VerificationEntry(
                            article_number=art_num,
                            equation_latex=eq.latex,
                            python_function=func_name,
                            python_file=str(py_file),
                            equation_in_code="",  # Filled by manual review or LLM
                            verification_method="pending",
                        )
                        entries.append(entry)

        self._verifications = entries
        return entries

    def summary(self) -> dict:
        """Generate summary statistics."""
        total = sum(len(v) for v in self._equations.values())
        by_type = defaultdict(int)
        for eqs in self._equations.values():
            for eq in eqs:
                by_type[eq.equation_type] += 1

        return {
            "total_articles_with_equations": len(self._equations),
            "total_equations": total,
            "by_type": dict(by_type),
            "article_range": (
                f"{min(self._equations)}-{max(self._equations)}"
                if self._equations
                else "none"
            ),
            "verification_entries": len(self._verifications),
        }

    # ── Private methods ──────────────────────────────────────────

    def _extract_cited_articles(self, source: str) -> list[int]:
        """Extract article numbers from @maxwell_cite decorators in source code."""
        import ast

        articles = set()
        try:
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call):
                            # Get positional args (article numbers)
                            for arg in decorator.args:
                                if isinstance(arg, ast.Constant) and isinstance(
                                    arg.value, int
                                ):
                                    articles.add(arg.value)
                            # Also check for articles= keyword (list form)
                            for kw in decorator.keywords:
                                if kw.arg == "articles":
                                    if isinstance(kw.value, ast.List):
                                        for elt in kw.value.elts:
                                            if isinstance(
                                                elt, ast.Constant
                                            ) and isinstance(elt.value, int):
                                                articles.add(elt.value)
        except SyntaxError:
            pass
        return sorted(articles)

    def _find_function_for_article(
        self, source: str, article_number: int
    ) -> Optional[str]:
        """Find the function name that cites a specific article."""
        import ast

        try:
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call):
                            # Check positional args (article numbers)
                            for arg in decorator.args:
                                if (
                                    isinstance(arg, ast.Constant)
                                    and isinstance(arg.value, int)
                                    and arg.value == article_number
                                ):
                                    return node.name
                            # Also check articles= keyword
                            for kw in decorator.keywords:
                                if kw.arg == "articles":
                                    if isinstance(kw.value, ast.List):
                                        for elt in kw.value.elts:
                                            if (
                                                isinstance(elt, ast.Constant)
                                                and isinstance(elt.value, int)
                                                and elt.value == article_number
                                            ):
                                                return node.name
        except SyntaxError:
            pass
        return None

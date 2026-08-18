"""
Maxwell article citation decorator.

Tags every Python function with the Maxwell article(s) it implements,
enabling full traceability from code back to the original 1873 text.

This is the core of the theory preservation system: every computation
can be linked to its source in Maxwell's Treatise.

Category: B (user_original) — Citation system designed for this project.
"""

from __future__ import annotations

import functools
import inspect
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class MaxwellCitation:
    """Citation metadata linking code to Maxwell's Treatise."""

    #: Article number(s) from the Treatise (e.g., 230, or 282 for 282a+b)
    articles: tuple[int, ...]

    #: Part of the Treatise (I–VI)
    part: int

    #: Chapter title (e.g., "The Electric Current")
    chapter: str = ""

    #: Theory classification
    #: "maxwell_original" = from Maxwell's 1873 text
    #: "user_original" = user's theoretical extension (AUTHORITATIVE)
    #: "standard_math" = established mathematics (vector calculus, etc.)
    theory_class: str = "maxwell_original"

    #: Brief description of what the function implements
    description: str = ""

    def __repr__(self) -> str:
        art_str = ", ".join(f"Art. {a}" for a in self.articles)
        return f"MaxwellCitation(Part {self.part}, {art_str})"


# ── Registry of all cited functions ──────────────────────────────
_citation_registry: dict[str, MaxwellCitation] = {}


def maxwell_cite(
    *articles: int,
    part: int = 1,
    chapter: str = "",
    theory_class: str = "maxwell_original",
    description: str = "",
) -> Callable:
    """Decorator that tags a function with its Maxwell article source.

    Args:
        *articles: Article number(s) from the Treatise.
        part: Part number (1–6).
        chapter: Chapter title.
        theory_class: One of "maxwell_original", "user_original", "standard_math".
        description: Brief description of what the function implements.

    Returns:
        Decorated function with citation metadata attached.

    Example:
        >>> @maxwell_cite(241, part=2, chapter="Conduction and Resistance")
        >>> def solve_ohm_law(V, R):
        ...     return V / R
    """
    valid_classes = {"maxwell_original", "user_original", "standard_math"}
    if theory_class not in valid_classes:
        raise ValueError(f"theory_class must be one of {valid_classes}")

    def decorator(func: Callable) -> Callable:
        citation = MaxwellCitation(
            articles=articles,
            part=part,
            chapter=chapter,
            theory_class=theory_class,
            description=description or func.__doc__ or "",
        )

        # Attach citation to function
        func._maxwell_citation = citation  # type: ignore[attr-defined]

        # Register globally
        qualname = f"{func.__module__}.{func.__qualname__}"
        _citation_registry[qualname] = citation

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper._maxwell_citation = citation  # type: ignore[attr-defined]
        return wrapper

    return decorator


def get_citation(func: Callable) -> MaxwellCitation | None:
    """Get the Maxwell citation for a function.

    Args:
        func: The function to look up.

    Returns:
        Citation metadata, or None if not decorated.
    """
    return getattr(func, "_maxwell_citation", None)


def get_all_citations() -> dict[str, MaxwellCitation]:
    """Get all registered citations.

    Returns:
        Mapping of qualified function names to their citations.
    """
    return dict(_citation_registry)


def verify_traceability(modules: list[Any]) -> dict[str, Any]:
    """Verify that all public functions in modules have citations.

    Args:
        modules: List of module objects to check.

    Returns:
        Dict with 'total', 'cited', 'uncited', and 'uncited_functions' keys.
    """
    total = 0
    cited = 0
    uncited = []

    for mod in modules:
        for name, obj in inspect.getmembers(mod, inspect.isfunction):
            if name.startswith("_"):
                continue
            total += 1
            if get_citation(obj) is not None:
                cited += 1
            else:
                uncited.append(f"{mod.__name__}.{name}")

    return {
        "total": total,
        "cited": cited,
        "uncited": len(uncited),
        "uncited_functions": uncited,
        "coverage_pct": (cited / total * 100) if total else 0.0,
    }

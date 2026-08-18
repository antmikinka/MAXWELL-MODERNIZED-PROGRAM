"""maxwell.meta — Citation traceability system.

Links every function in the codebase to its source article in Maxwell's 1873
Treatise on Electricity and Magnetism via the @maxwell_cite decorator.

Exports:
    maxwell_cite: Decorator for tagging functions with article citations.
    get_citation: Retrieve citation metadata for a decorated function.
    get_all_citations: Retrieve all citations in the codebase.
"""

from maxwell.meta.citation import get_all_citations, get_citation, maxwell_cite

__all__ = [
    "maxwell_cite",
    "get_citation",
    "get_all_citations",
]

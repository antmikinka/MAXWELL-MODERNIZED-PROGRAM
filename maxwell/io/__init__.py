"""
maxwell.io — Input/Output utilities for Maxwell's Treatise data.

This subpackage provides utilities for loading and parsing OCR output
from Mathpix JSON files containing Maxwell's Treatise text:

- JSON loaders for article-level and chapter-level files
- Article parsing for extracting equations, figures, and cross-references
- Batch loading utilities for processing multiple articles

Category: B (user_original) — Data loading utilities designed for this project.

References:
    Maxwell's Treatise on Electricity and Magnetism, Volumes I & II.
    Mathpix OCR output formats: volume_direct_result.json, ARTICLE_*.json.
"""

from __future__ import annotations

from maxwell.io.json_loader import (
    load_article_json,
    load_chapter_json,
    load_volume_result,
    list_available_articles,
    batch_load_articles,
)

from maxwell.io.article_parser import (
    extract_article_number,
    extract_all_articles_from_chapter,
    extract_equations,
    extract_figure_references,
    extract_cross_references,
)

__all__ = [
    # JSON Loaders
    "load_article_json",
    "load_chapter_json",
    "load_volume_result",
    "list_available_articles",
    "batch_load_articles",
    # Article Parser
    "extract_article_number",
    "extract_all_articles_from_chapter",
    "extract_equations",
    "extract_figure_references",
    "extract_cross_references",
]

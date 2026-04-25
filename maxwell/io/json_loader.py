"""
JSON loaders for Mathpix OCR output files.

This module provides functions to load the various JSON file formats
produced by the Mathpix OCR pipeline for Maxwell's Treatise:

- Article-level JSON: Array format with page_number, raw_text, mathpix_markdown
- Chapter-level JSON: Object format with "page_num": "text" mappings
- Volume result JSON: Large files with complete OCR output (lazy loading)

All loaders handle the specific structure of Mathpix output and return
normalized data structures for downstream processing.

Category: B (user_original) — Data loading utilities for Maxwell OCR data.

References:
    Mathpix OCR output formats from Maxwell Volumes I & II digitization.
    Volume directory structure: ARTICLE_*.json, CHAPTER_*.json, volume_direct_result.json.
"""

from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Any, Generator, Iterator
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(
    1,
    part=5, chapter="Data Loading Utilities",
    theory_class="user_original",
    description="Load article-level JSON array from Mathpix OCR output",
)
def load_article_json(filepath: str | os.PathLike) -> list[dict[str, Any]]:
    """Load an article-level JSON file from Mathpix OCR output.

    Expected format (array):
        [
            {"page_number": 1, "raw_text": "...", "mathpix_markdown": "..."},
            {"page_number": 2, "raw_text": "...", "mathpix_markdown": "..."},
            ...
        ]

    Args:
        filepath: Path to the ARTICLE_*.json file.

    Returns:
        List of page dictionaries with keys: page_number, raw_text, mathpix_markdown.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
        ValueError: If the JSON structure is unexpected.

    Example:
        >>> pages = load_article_json("volume_1/ARTICLE_27.json")
        >>> for page in pages:
        ...     print(f"Page {page['page_number']}: {page['raw_text'][:50]}...")
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Article JSON not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(
            f"Expected array format for article JSON, got {type(data).__name__}. "
            f"File: {filepath}"
        )

    # Validate structure
    for i, page in enumerate(data):
        if not isinstance(page, dict):
            raise ValueError(f"Page {i} is not a dictionary in {filepath}")
        required_keys = {"page_number", "raw_text", "mathpix_markdown"}
        missing = required_keys - set(page.keys())
        if missing:
            raise ValueError(
                f"Page {i} missing required keys {missing} in {filepath}"
            )

    return data


@maxwell_cite(
    1,
    part=5, chapter="Data Loading Utilities",
    theory_class="user_original",
    description="Load chapter-level JSON object from Mathpix OCR output",
)
def load_chapter_json(filepath: str | os.PathLike) -> dict[str, str]:
    """Load a chapter-level JSON file from Mathpix OCR output.

    Expected format (object):
        {
            "1": "Full text of page 1...",
            "2": "Full text of page 2...",
            ...
        }

    Args:
        filepath: Path to the CHAPTER_*.json file.

    Returns:
        Dictionary mapping page numbers (as strings) to text content.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
        ValueError: If the JSON structure is unexpected.

    Example:
        >>> chapter = load_chapter_json("volume_1/CHAPTER_5.json")
        >>> for page_num, text in chapter.items():
        ...     print(f"Page {page_num}: {text[:50]}...")
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Chapter JSON not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(
            f"Expected object format for chapter JSON, got {type(data).__name__}. "
            f"File: {filepath}"
        )

    # Validate structure - keys should be page numbers
    for key, value in data.items():
        if not isinstance(value, str):
            raise ValueError(
                f"Page '{key}' value is not a string in {filepath}"
            )

    return data


@maxwell_cite(
    1,
    part=5, chapter="Data Loading Utilities",
    theory_class="user_original",
    description="Lazy load volume result JSON for large OCR files",
)
def load_volume_result(
    filepath: str | os.PathLike,
    lazy: bool = True,
) -> dict[str, Any] | Generator[dict[str, Any], None, None]:
    """Load a volume_direct_result.json file with optional lazy loading.

    This loader handles large OCR output files (can be 100MB+) by
    providing lazy loading via a generator.

    Expected format:
        {
            "volume": "Volume I",
            "articles": {
                "27": [{"page": 1, "text": "...", "markdown": "..."}],
                "28": [{"page": 2, "text": "...", "markdown": "..."}],
                ...
            }
        }

    Args:
        filepath: Path to volume_direct_result.json.
        lazy: If True, return a generator for streaming access.
              If False, load entire file into memory.

    Returns:
        If lazy=False: Full dictionary with all OCR data.
        If lazy=True: Generator yielding article dictionaries one at a time.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.

    Example:
        >>> # Lazy loading (memory efficient)
        >>> for article in load_volume_result("volume_1/volume_direct_result.json"):
        ...     process_article(article)

        >>> # Full load (faster for repeated access)
        >>> data = load_volume_result("volume_1/volume_direct_result.json", lazy=False)
        >>> print(f"Volume: {data['volume']}")
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Volume result JSON not found: {filepath}")

    if lazy:
        # Stream the file using incremental JSON parsing
        def stream_articles() -> Generator[dict[str, Any], None, None]:
            with open(filepath, "r", encoding="utf-8") as f:
                # Read opening brace
                char = ""
                while char != "{":
                    char = f.read(1)
                    if not char:
                        return

                # Find "articles" key
                content = f.read()
                if '"articles"' in content:
                    articles_start = content.find('"articles"') + len('"articles"')
                    articles_content = content[articles_start:].lstrip(" :")

                    # Parse articles one at a time
                    import re
                    article_pattern = r'"(\d+)":\s*\['

                    for match in re.finditer(article_pattern, articles_content):
                        article_num = match.group(1)
                        # Extract this article's data
                        start_idx = match.end()
                        # Find matching bracket
                        bracket_count = 1
                        end_idx = start_idx
                        while bracket_count > 0 and end_idx < len(articles_content):
                            if articles_content[end_idx] == "[":
                                bracket_count += 1
                            elif articles_content[end_idx] == "]":
                                bracket_count -= 1
                            end_idx += 1

                        article_json = "[" + articles_content[start_idx:end_idx-1] + "]"
                        try:
                            article_data = json.loads(article_json)
                            yield {
                                "article_number": int(article_num),
                                "pages": article_data,
                            }
                        except json.JSONDecodeError:
                            continue

        return stream_articles()
    else:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError(
                f"Expected object format for volume result, got {type(data).__name__}"
            )

        return data


@maxwell_cite(
    1,
    part=5, chapter="Data Loading Utilities",
    theory_class="user_original",
    description="Scan directory for available article JSON files",
)
def list_available_articles(
    volume_dir: str | os.PathLike,
    pattern: str = "ARTICLE_*.json",
) -> list[Path]:
    """Scan a volume directory for available article JSON files.

    Args:
        volume_dir: Path to the volume directory (e.g., "volume_1/").
        pattern: Glob pattern for article files (default: "ARTICLE_*.json").

    Returns:
        Sorted list of Path objects pointing to article JSON files.

    Example:
        >>> articles = list_available_articles("volume_1")
        >>> print(f"Found {len(articles)} articles")
        >>> for path in articles:
        ...     print(f"  - {path.name}")
    """
    volume_dir = Path(volume_dir)
    if not volume_dir.exists():
        raise FileNotFoundError(f"Volume directory not found: {volume_dir}")
    if not volume_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {volume_dir}")

    articles = sorted(volume_dir.glob(pattern))
    return articles


@maxwell_cite(
    1,
    part=5, chapter="Data Loading Utilities",
    theory_class="user_original",
    description="Batch load multiple article JSON files from a directory",
)
def batch_load_articles(
    directory: str | os.PathLike,
    pattern: str = "ARTICLE_*.json",
) -> dict[int, list[dict[str, Any]]]:
    """Load multiple article JSON files from a directory.

    This function scans a directory for article files matching the pattern,
    loads each one, and returns a dictionary mapping article numbers to
    their page data.

    Args:
        directory: Path to the directory containing article JSON files.
        pattern: Glob pattern for article files (default: "ARTICLE_*.json").
                 The article number is extracted from the filename
                 (e.g., "ARTICLE_27.json" -> article 27).

    Returns:
        Dictionary mapping article numbers (int) to list of page dictionaries.

    Raises:
        FileNotFoundError: If the directory does not exist.
        json.JSONDecodeError: If any file is not valid JSON.

    Example:
        >>> articles = batch_load_articles("volume_1")
        >>> print(f"Loaded {len(articles)} articles")
        >>> article_27 = articles.get(27)
        >>> if article_27:
        ...     print(f"Article 27 has {len(article_27)} pages")
    """
    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    result = {}
    article_paths = list_available_articles(directory, pattern)

    for path in article_paths:
        # Extract article number from filename (ARTICLE_27.json -> 27)
        article_num_str = path.stem.replace("ARTICLE_", "").replace("ARTÍCULO_", "")
        try:
            article_num = int(article_num_str)
        except ValueError:
            # Skip files that don't match expected naming
            continue

        try:
            pages = load_article_json(path)
            result[article_num] = pages
        except (json.JSONDecodeError, ValueError) as e:
            # Log but continue with other articles
            print(f"Warning: Failed to load {path.name}: {e}")
            continue

    return result


@maxwell_cite(
    1,
    part=5, chapter="Data Loading Utilities",
    theory_class="user_original",
    description="Extract article number from filename",
)
def extract_article_number_from_filename(filename: str | Path) -> int | None:
    """Extract article number from a filename like ARTICLE_27.json.

    Args:
        filename: The filename to parse.

    Returns:
        Article number as integer, or None if not matching pattern.

    Example:
        >>> extract_article_number_from_filename("ARTICLE_27.json")
        27
        >>> extract_article_number_from_filename("ARTICLE_118.json")
        118
    """
    filename = Path(filename).stem
    import re
    match = re.search(r"ARTICLE[_\s]*(\d+)", filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

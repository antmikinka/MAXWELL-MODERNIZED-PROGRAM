"""
Article parser utilities for Mathpix markdown content.

This module provides functions to parse and extract structured information
from the mathpix_markdown field of OCR output:

- Extract article numbers from text boundaries (e.g., "27.]")
- Find all article boundaries within chapter text
- Extract LaTeX equations from markdown
- Find figure and diagram references
- Extract cross-references to other articles

Category: B (user_original) — Parsing utilities for Maxwell OCR data.

References:
    Maxwell's Treatise article numbering convention (e.g., "27.", "118a.").
    Mathpix markdown format for LaTeX equations and figure references.
"""

from __future__ import annotations
import re
from typing import Any
from maxwell.meta.citation import maxwell_cite


@maxwell_cite(
    1,
    part=5, chapter="Data Loading Utilities",
    theory_class="user_original",
    description="Parse article number from Maxwell's notation (e.g., '27.]')",
)
def extract_article_number(text: str) -> int | None:
    """Extract article number from Maxwell's Treatise text.

    Maxwell's articles are marked with numbers followed by a period
    and sometimes a closing bracket, e.g.:
        "27.]" — Standard article marker
        "118a.]" — Article with letter suffix
        "Art. 27" — Explicit article reference

    Args:
        text: Text content containing an article marker.

    Returns:
        Article number as integer (ignores letter suffixes),
        or None if no article marker found.

    Examples:
        >>> extract_article_number("27.] The theory of electrification...")
        27
        >>> extract_article_number("118a.] Electrokinematics...")
        118
        >>> extract_article_number("See Art. 45 for more details")
        45
    """
    if not text:
        return None

    # Pattern 1: Standard article marker at start (e.g., "27.]" or "27.")
    # Matches: 27, 118a, 230b, etc.
    standard_pattern = r"^\s*(\d+)([a-z])?\.\]?"
    match = re.match(standard_pattern, text.strip(), re.IGNORECASE)
    if match:
        return int(match.group(1))

    # Pattern 2: "Art." or "Article" reference anywhere in text
    art_pattern = r"[Aa]rt\.\s*(\d+)([a-z])?"
    match = re.search(art_pattern, text)
    if match:
        return int(match.group(1))

    # Pattern 3: Standalone number followed by period (e.g., "27." at line start)
    standalone_pattern = r"^\s*(\d+)\.\s+[A-Z]"
    match = re.match(standalone_pattern, text)
    if match:
        # Verify it's not a page number or other numbering
        num = int(match.group(1))
        # Maxwell's articles range from ~27 to ~866
        if 20 <= num <= 900:
            return num

    return None


@maxwell_cite(
    1,
    part=5, chapter="Data Loading Utilities",
    theory_class="user_original",
    description="Find all article boundaries in chapter text",
)
def extract_all_articles_from_chapter(chapter_text: str) -> list[dict[str, Any]]:
    """Extract all article boundaries from a chapter's text.

    This function identifies where each article begins and ends within
    a chapter's combined text, returning structured data for each article.

    Article boundaries are marked by patterns like:
        "27.]" — Article number with bracket
        "27." at start of line followed by capital letter
        "Art. 27" — Explicit article reference

    Args:
        chapter_text: Full text content of a chapter.

    Returns:
        List of dictionaries, each containing:
            - article_number: int (e.g., 27, 118)
            - article_suffix: str or None (e.g., "a", "b" for 118a, 118b)
            - start_index: int (character position in chapter_text)
            - end_index: int or None (end position, None for last article)
            - content: str (the article text content)

    Example:
        >>> articles = extract_all_articles_from_chapter(chapter_text)
        >>> for art in articles:
        ...     print(f"Article {art['article_number']}: {art['content'][:50]}...")
    """
    if not chapter_text:
        return []

    # Pattern to match article markers with optional letter suffix
    # Matches: "27.]", "118a.]", "230b.]", etc.
    article_pattern = r"(\d+)([a-z])?\.\]"

    matches = list(re.finditer(article_pattern, chapter_text, re.IGNORECASE))

    if not matches:
        # Try alternative pattern for "Art. XX" format
        alt_pattern = r"[Aa]rt\.\s*(\d+)([a-z])?"
        matches = list(re.finditer(alt_pattern, chapter_text))

    articles = []
    for i, match in enumerate(matches):
        article_num = int(match.group(1))
        suffix = match.group(2).lower() if match.group(2) else None
        start_idx = match.start()

        # End index is start of next article or end of text
        if i + 1 < len(matches):
            end_idx = matches[i + 1].start()
        else:
            end_idx = None

        # Extract content (from after the marker to next article or end)
        content_start = match.end()
        content = chapter_text[content_start:end_idx].strip() if end_idx else chapter_text[content_start:].strip()

        articles.append({
            "article_number": article_num,
            "article_suffix": suffix,
            "start_index": start_idx,
            "end_index": end_idx,
            "content": content,
        })

    return articles


@maxwell_cite(
    1,
    part=5, chapter="Data Loading Utilities",
    theory_class="user_original",
    description="Extract LaTeX equations from Mathpix markdown",
)
def extract_equations(mathpix_markdown: str) -> list[dict[str, str]]:
    """Extract LaTeX equations from Mathpix markdown content.

    Mathpix outputs LaTeX in several formats:
        - Inline: $E = mc^2$ or \\(E = mc^2\\)
        - Display: $$E = mc^2$$ or \\[E = mc^2\\]
        - Aligned: \\begin{aligned} ... \\end{aligned}

    Args:
        mathpix_markdown: Markdown content from Mathpix OCR.

    Returns:
        List of dictionaries, each containing:
            - type: "inline" | "display" | "aligned" | "gathered" | "matrix"
            - latex: str (the raw LaTeX content)
            - position: int (character position in source)

    Example:
        >>> equations = extract_equations(markdown_text)
        >>> for eq in equations:
        ...     print(f"{eq['type']}: {eq['latex'][:50]}...")
    """
    if not mathpix_markdown:
        return []

    equations = []

    # Pattern 1: Display equations $$...$$
    display_pattern = r"\$\$(.+?)\$\$"
    for match in re.finditer(display_pattern, mathpix_markdown, re.DOTALL):
        equations.append({
            "type": "display",
            "latex": match.group(1).strip(),
            "position": match.start(),
        })

    # Pattern 2: Inline equations $...$ (but not $$)
    # Negative lookbehind for $ and negative lookahead for $
    inline_pattern = r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)"
    for match in re.finditer(inline_pattern, mathpix_markdown):
        latex = match.group(1).strip()
        # Skip if it contains newlines (likely a misidentified display eq)
        if "\n" not in latex:
            equations.append({
                "type": "inline",
                "latex": latex,
                "position": match.start(),
            })

    # Pattern 3: \\[...\\] display equations
    bracket_display_pattern = r"\\\\\[(.+?)\\\\\]"
    for match in re.finditer(bracket_display_pattern, mathpix_markdown, re.DOTALL):
        equations.append({
            "type": "display_bracket",
            "latex": match.group(1).strip(),
            "position": match.start(),
        })

    # Pattern 4: \\(...\\) inline equations
    bracket_inline_pattern = r"\\\\\((.+?)\\\\\)"
    for match in re.finditer(bracket_inline_pattern, mathpix_markdown):
        equations.append({
            "type": "inline_bracket",
            "latex": match.group(1).strip(),
            "position": match.start(),
        })

    # Pattern 5: aligned, gathered, matrix environments
    env_pattern = r"\\begin\{(aligned|gathered|matrix|pmatrix|bmatrix|cases)\}(.+?)\\end\{\1\}"
    for match in re.finditer(env_pattern, mathpix_markdown, re.DOTALL):
        equations.append({
            "type": match.group(1),
            "latex": f"\\begin{{{match.group(1)}}}{match.group(2)}\\end{{{match.group(1)}}}",
            "position": match.start(),
        })

    # Sort by position
    equations.sort(key=lambda x: x["position"])

    return equations


@maxwell_cite(
    1,
    part=5, chapter="Data Loading Utilities",
    theory_class="user_original",
    description="Extract figure and diagram references from markdown",
)
def extract_figure_references(mathpix_markdown: str) -> list[dict[str, Any]]:
    """Extract figure and diagram references from Mathpix markdown.

    Maxwell's Treatise contains numerous diagrams and figures referenced as:
        - "Fig. 1", "Figure 1"
        - "see Diagram X"
        - "[Figure 2.1]"
        - Markdown image syntax: ![alt text](image_url)

    Args:
        mathpix_markdown: Markdown content from Mathpix OCR.

    Returns:
        List of dictionaries, each containing:
            - type: "figure" | "diagram" | "plate" | "image"
            - reference: str (the figure number or description)
            - position: int (character position in source)
            - context: str (surrounding text, ~50 chars)

    Example:
        >>> figures = extract_figure_references(chapter_text)
        >>> for fig in figures:
        ...     print(f"{fig['type']} {fig['reference']}: {fig['context']}")
    """
    if not mathpix_markdown:
        return []

    references = []

    # Pattern 1: "Fig. X" or "Figure X" (with optional letter suffix)
    fig_pattern = r"[Ff]ig(?:ure)?\.\s*(\d+)([a-z])?"
    for match in re.finditer(fig_pattern, mathpix_markdown, re.IGNORECASE):
        fig_num = match.group(1)
        suffix = match.group(2).lower() if match.group(2) else None
        reference = f"{fig_num}{suffix}" if suffix else fig_num

        # Get context
        start = max(0, match.start() - 25)
        end = min(len(mathpix_markdown), match.end() + 25)
        context = mathpix_markdown[start:end].strip()

        references.append({
            "type": "figure",
            "reference": reference,
            "position": match.start(),
            "context": context,
        })

    # Pattern 2: "Diagram X"
    diagram_pattern = r"[Dd]iagram\s*(\d+)([a-z])?"
    for match in re.finditer(diagram_pattern, mathpix_markdown):
        diagram_num = match.group(1)
        suffix = match.group(2).lower() if match.group(2) else None
        reference = f"{diagram_num}{suffix}" if suffix else diagram_num

        start = max(0, match.start() - 25)
        end = min(len(mathpix_markdown), match.end() + 25)
        context = mathpix_markdown[start:end].strip()

        references.append({
            "type": "diagram",
            "reference": reference,
            "position": match.start(),
            "context": context,
        })

    # Pattern 3: "Plate X" (for full-page illustrations)
    plate_pattern = r"[Pp]late\s*(\d+)([a-z])?"
    for match in re.finditer(plate_pattern, mathpix_markdown):
        plate_num = match.group(1)
        suffix = match.group(2).lower() if match.group(2) else None
        reference = f"{plate_num}{suffix}" if suffix else plate_num

        start = max(0, match.start() - 25)
        end = min(len(mathpix_markdown), match.end() + 25)
        context = mathpix_markdown[start:end].strip()

        references.append({
            "type": "plate",
            "reference": reference,
            "position": match.start(),
            "context": context,
        })

    # Pattern 4: Markdown image syntax ![alt](url)
    image_pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    for match in re.finditer(image_pattern, mathpix_markdown):
        alt_text = match.group(1)
        image_url = match.group(2)

        start = max(0, match.start() - 25)
        end = min(len(mathpix_markdown), match.end() + 25)
        context = mathpix_markdown[start:end].strip()

        references.append({
            "type": "image",
            "reference": image_url,
            "alt_text": alt_text,
            "position": match.start(),
            "context": context,
        })

    # Sort by position
    references.sort(key=lambda x: x["position"])

    return references


@maxwell_cite(
    1,
    part=5, chapter="Data Loading Utilities",
    theory_class="user_original",
    description="Extract cross-references to other articles",
)
def extract_cross_references(text: str) -> list[dict[str, Any]]:
    """Extract cross-references to other articles in Maxwell's Treatise.

    Maxwell frequently references other articles using patterns like:
        - "see Art. 27"
        - "as shown in Art. 118a"
        - "(Art. 45-67)"
        - "described in Arts. 230-245"
        - "compare Art. 76"

    Args:
        text: Text content to search for cross-references.

    Returns:
        List of dictionaries, each containing:
            - type: "single" | "range" | "multiple"
            - articles: list[int] (referenced article numbers)
            - raw_reference: str (the original text)
            - position: int (character position in source)
            - context: str (surrounding text for context)

    Example:
        >>> refs = extract_cross_references("As shown in Art. 27 and Arts. 45-50...")
        >>> for ref in refs:
        ...     print(f"{ref['type']}: {ref['articles']} - {ref['raw_reference']}")
    """
    if not text:
        return []

    references = []

    # Pattern 1: "Art. X" or "Arts. X" (with optional letter suffix)
    single_art_pattern = r"[Aa]rt\.\s*(\d+)([a-z])?"
    for match in re.finditer(single_art_pattern, text):
        article_num = int(match.group(1))
        suffix = match.group(2).lower() if match.group(2) else None

        start = max(0, match.start() - 20)
        end = min(len(text), match.end() + 20)
        context = text[start:end].strip()

        references.append({
            "type": "single",
            "articles": [article_num],
            "raw_reference": match.group(0),
            "position": match.start(),
            "context": context,
        })

    # Pattern 2: "Arts. X-Y" or "Arts. X to Y" (range)
    range_art_pattern = r"[Aa]rts\.\s*(\d+)([a-z])?\s*(?:[-–]|to)\s*(\d+)([a-z])?"
    for match in re.finditer(range_art_pattern, text):
        start_num = int(match.group(1))
        end_num = int(match.group(3))

        # Generate range of article numbers
        article_range = list(range(start_num, end_num + 1))

        start = max(0, match.start() - 20)
        end = min(len(text), match.end() + 20)
        context = text[start:end].strip()

        references.append({
            "type": "range",
            "articles": article_range,
            "raw_reference": match.group(0),
            "position": match.start(),
            "context": context,
        })

    # Pattern 3: "(Art. X)" or "(Arts. X-Y)" in parentheses
    paren_pattern = r"\([Aa]rt\.?\s*(\d+)([a-z])?(?:\s*[-–]\s*(\d+)([a-z])?)?\)"
    for match in re.finditer(paren_pattern, text):
        article_num = int(match.group(1))

        if match.group(3):  # It's a range
            end_num = int(match.group(3))
            article_range = list(range(article_num, end_num + 1))
            ref_type = "range"
        else:
            article_range = [article_num]
            ref_type = "single"

        start = max(0, match.start() - 20)
        end = min(len(text), match.end() + 20)
        context = text[start:end].strip()

        references.append({
            "type": ref_type,
            "articles": article_range,
            "raw_reference": match.group(0),
            "position": match.start(),
            "context": context,
        })

    # Pattern 4: "compare Art. X" or "see Art. X"
    directive_pattern = r"(?:compare|see|refer\sto|cf\.?)\s+[Aa]rt\.\s*(\d+)([a-z])?"
    for match in re.finditer(directive_pattern, text, re.IGNORECASE):
        article_num = int(match.group(1))

        start = max(0, match.start() - 15)
        end = min(len(text), match.end() + 15)
        context = text[start:end].strip()

        references.append({
            "type": "directive",
            "articles": [article_num],
            "raw_reference": match.group(0),
            "position": match.start(),
            "context": context,
            "directive": match.group(0).split()[0].lower().rstrip(".,"),
        })

    # Remove duplicates based on position
    seen_positions = set()
    unique_references = []
    for ref in references:
        if ref["position"] not in seen_positions:
            seen_positions.add(ref["position"])
            unique_references.append(ref)

    # Sort by position
    unique_references.sort(key=lambda x: x["position"])

    return unique_references

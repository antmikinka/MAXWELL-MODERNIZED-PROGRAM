"""
Deterministic Article Extraction from Maxwell's Treatise OCR JSON

This module extracts article markers from chapter text using regex,
without requiring AI. This provides "hints" to the AI about article
boundaries, making responses more reliable.
"""

import re
from typing import List, Dict, Optional, Tuple


# Pattern to match article markers like "27.]", "85 a.]", "74c.]"
# Captures: (article_number)(optional_sub_letter)
ARTICLE_PATTERN = re.compile(
    r'(?:^|\n|\s)(\d+)\s*([a-z])?\s*\.\]',
    re.IGNORECASE | re.MULTILINE
)

# Pattern to detect references to other articles
# Matches: "Art. 70", "Arts. 84-86", "Art. 100 c"
REFERENCE_PATTERN = re.compile(
    r'Art(?:s)?\.?\s*(\d+)\s*([a-z])?\s*(?:[-–]\s*(\d+))?',
    re.IGNORECASE
)

# Pattern to extract section headers
SECTION_PATTERN = re.compile(
    r'\\section\*?\{([^}]+)\}',
    re.IGNORECASE
)


def extract_article_markers(chapter_pages: List[Dict]) -> List[Dict]:
    """
    Extract article boundary markers from chapter JSON.
    
    Args:
        chapter_pages: List of page dictionaries with 'page_number', 
                       'raw_text', and 'mathpix_markdown' fields
    
    Returns:
        List of article markers with:
        - article: Article number (string)
        - sub: Sub-article letter or None
        - page: Page number where found
        - offset: Character offset in page text
        - context: Surrounding text for verification
        - title: Extracted or inferred title
    """
    markers = []
    
    for page in chapter_pages:
        # Prefer mathpix_markdown for better LaTeX preservation
        text = page.get('mathpix_markdown', page.get('raw_text', ''))
        page_num = page.get('page_number', 0)
        
        for match in ARTICLE_PATTERN.finditer(text):
            article_num = match.group(1)
            sub_article = match.group(2)  # 'a', 'b', etc. or None
            
            if sub_article:
                sub_article = sub_article.lower()
            
            # Extract surrounding context (200 chars after match)
            start = match.end()
            end = min(len(text), start + 300)
            context_after = text[start:end].strip()
            
            # Try to extract title (text before first period or newline)
            title = extract_title_from_context(context_after)
            
            markers.append({
                'article': article_num,
                'sub': sub_article,
                'page': page_num,
                'offset': match.start(),
                'context': context_after[:150].replace('\n', ' '),
                'title': title
            })
    
    # Sort by article number, then sub-article
    markers.sort(key=lambda x: (int(x['article']), x['sub'] or ''))
    
    # Remove duplicates (same article might appear in headers)
    seen = set()
    unique_markers = []
    for m in markers:
        key = (m['article'], m['sub'])
        if key not in seen:
            seen.add(key)
            unique_markers.append(m)
    
    return unique_markers


def extract_title_from_context(context: str) -> str:
    """
    Try to extract the article title from the text following the article marker.
    
    Maxwell's articles often have titles in the form:
    - "On the Work which must be done..."
    - "Electrification by Friction"
    """
    # Clean up the context
    context = context.strip()
    
    # Remove LaTeX section markers
    context = re.sub(r'\\section\*?\{[^}]*\}', '', context)
    context = context.strip()
    
    # Look for title-like text (up to first sentence end or certain keywords)
    # Title usually ends with period, colon, or starts a new sentence
    
    # Pattern 1: "On X..." or "The X..." style
    title_match = re.match(
        r'^((?:On|The|A|An|If|Let|We|In|When|This|That|For|To|From)\s+[^.]{10,100}?)[\.\n]',
        context,
        re.IGNORECASE
    )
    if title_match:
        return title_match.group(1).strip()
    
    # Pattern 2: Short phrase before first period
    first_sentence = re.match(r'^([^.]{5,80})\.', context)
    if first_sentence:
        return first_sentence.group(1).strip()
    
    # Pattern 3: Just first line
    first_line = context.split('\n')[0].strip()
    if len(first_line) > 5 and len(first_line) < 100:
        return first_line
    
    return ""


def extract_references(text: str) -> List[Tuple[str, Optional[str]]]:
    """
    Extract references to other articles from text.
    
    Returns list of (article_number, sub_letter) tuples.
    """
    refs = []
    
    for match in REFERENCE_PATTERN.finditer(text):
        art_num = match.group(1)
        sub = match.group(2)
        range_end = match.group(3)
        
        if sub:
            sub = sub.lower()
        
        refs.append((art_num, sub))
        
        # Handle ranges like "Arts. 84-86"
        if range_end:
            try:
                start = int(art_num)
                end = int(range_end)
                for i in range(start + 1, end + 1):
                    refs.append((str(i), None))
            except ValueError:
                pass
    
    return refs


def extract_equations(text: str) -> List[str]:
    """
    Extract LaTeX equations from mathpix_markdown text.
    
    Returns list of equation strings.
    """
    equations = []
    
    # Display equations: $$...$$ or \begin{equation}...\end{equation}
    display_pattern = re.compile(
        r'\$\$(.+?)\$\$|\\\[(.+?)\\\]|\\begin\{equation\*?\}(.+?)\\end\{equation\*?\}',
        re.DOTALL
    )
    
    for match in display_pattern.finditer(text):
        eq = match.group(1) or match.group(2) or match.group(3)
        if eq:
            # Clean up whitespace
            eq = ' '.join(eq.split())
            equations.append(eq)
    
    return equations


def concatenate_chapter_text(
    chapter_pages: List[Dict],
    use_markdown: bool = True,
    include_page_markers: bool = True
) -> str:
    """
    Concatenate all pages of a chapter into a single text string.
    
    Args:
        chapter_pages: List of page dictionaries
        use_markdown: Whether to use mathpix_markdown (True) or raw_text (False)
        include_page_markers: Whether to include [PAGE XX] markers
    
    Returns:
        Single string with all chapter text
    """
    text_field = 'mathpix_markdown' if use_markdown else 'raw_text'
    
    parts = []
    for page in chapter_pages:
        text = page.get(text_field, page.get('raw_text', ''))
        page_num = page.get('page_number', 0)
        
        if include_page_markers:
            parts.append(f"\n[PAGE {page_num}]\n")
        
        parts.append(text)
    
    return '\n'.join(parts)


def split_chapter_by_articles(
    chapter_pages: List[Dict],
    article_markers: List[Dict]
) -> Dict[str, str]:
    """
    Split chapter text into sections by article.
    
    Returns dict mapping article keys (e.g., "27", "85a") to their text content.
    """
    # First, concatenate with page markers
    full_text = concatenate_chapter_text(chapter_pages)
    
    # Build article positions
    positions = []
    for marker in article_markers:
        # Find article in full text
        pattern = rf'(?:^|\n|\s){marker["article"]}\s*{marker["sub"] or ""}\s*\.\]'
        match = re.search(pattern, full_text, re.IGNORECASE)
        if match:
            key = marker['article'] + (marker['sub'] or '')
            positions.append((match.start(), key))
    
    # Sort by position
    positions.sort(key=lambda x: x[0])
    
    # Extract sections
    sections = {}
    for i, (pos, key) in enumerate(positions):
        if i + 1 < len(positions):
            end_pos = positions[i + 1][0]
        else:
            end_pos = len(full_text)
        
        sections[key] = full_text[pos:end_pos].strip()
    
    return sections


def analyze_chapter_structure(chapter_pages: List[Dict]) -> Dict:
    """
    Analyze the structure of a chapter.
    
    Returns summary of:
    - Total pages
    - Article count
    - Equation count
    - Reference count
    - Section headers
    """
    full_text = concatenate_chapter_text(chapter_pages, include_page_markers=False)
    markers = extract_article_markers(chapter_pages)
    
    # Extract sections
    sections = []
    for match in SECTION_PATTERN.finditer(full_text):
        sections.append(match.group(1).strip())
    
    # Count equations
    equations = extract_equations(full_text)
    
    # Count references
    refs = extract_references(full_text)
    
    return {
        'page_count': len(chapter_pages),
        'page_range': (
            chapter_pages[0].get('page_number', 0) if chapter_pages else 0,
            chapter_pages[-1].get('page_number', 0) if chapter_pages else 0
        ),
        'article_count': len(markers),
        'article_range': (
            markers[0]['article'] if markers else None,
            markers[-1]['article'] if markers else None
        ),
        'equation_count': len(equations),
        'reference_count': len(refs),
        'section_headers': sections,
        'character_count': len(full_text),
        'estimated_tokens': len(full_text) // 4  # Rough estimate
    }


# CLI for testing
if __name__ == "__main__":
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python article_extractor.py <chapter.json>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        pages = json.load(f)
    
    print("=== Chapter Structure Analysis ===")
    structure = analyze_chapter_structure(pages)
    for key, value in structure.items():
        print(f"  {key}: {value}")
    
    print("\n=== Article Markers ===")
    markers = extract_article_markers(pages)
    for m in markers:
        art_key = m['article'] + (m['sub'] or '')
        print(f"  Art. {art_key}: {m['title'] or '(no title)'}")
        print(f"    Page {m['page']}: {m['context'][:60]}...")
        print()

# Utility: citation_linking_utils

## Purpose

Python utility module for citation management and linking.

## Location

`agents/scriba/utils/citation_linking_utils.py`

---

## Module Contents

```python
"""
SCRIBA Citation Linking Utilities

Citation management, linking, and validation for the Maxwell 
Treatise Modernization Project.

Citation Types:
- Maxwell article citations (Art. 1-866)
- Cross-references between documents
- Bibliographic references
- Digital object identifiers

Theory Classification:
- maxwell_original: Maxwell's 1873 formulations
- user_original: User's theoretical extensions (DO NOT CHANGE)
- standard_math: Standard mathematical implementations

Maxwell References: Complete Treatise (Art. 1-866)
"""

from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import re
from collections import defaultdict


class CitationType(Enum):
    """Citation types."""
    MAXWELL_ARTICLE = "maxwell_article"
    CROSS_REFERENCE = "cross_reference"
    BIBLIOGRAPHIC = "bibliographic"
    DIGITAL = "digital"


class CitationStatus(Enum):
    """Citation status."""
    VALID = "valid"
    BROKEN = "broken"
    UNVERIFIED = "unverified"
    DEPRECATED = "deprecated"


@dataclass
class Citation:
    """Base citation."""
    id: str
    citation_type: CitationType
    status: CitationStatus
    created: datetime
    modified: datetime
    tags: List[str] = field(default_factory=list)
    
    def format(self) -> str:
        """Format citation string."""
        raise NotImplementedError


@dataclass
class MaxwellArticleCitation(Citation):
    """Maxwell article citation."""
    part: int
    start_article: int
    end_article: int
    topic: str
    context: str = ""
    
    def __post_init__(self):
        if self.end_article < self.start_article:
            raise ValueError("end_article must be >= start_article")
    
    def format(self) -> str:
        """Format citation."""
        if self.start_article == self.end_article:
            articles = f"Art. {self.start_article}"
        else:
            articles = f"Art. {self.start_article}-{self.end_article}"
        
        part_roman = {1: "I", 2: "II", 3: "III", 4: "IV"}.get(self.part, str(self.part))
        
        return f"Maxwell (1873, Part {part_roman}, {articles}): {self.topic}"
    
    def full_reference(self) -> str:
        """Full reference string."""
        return (
            f"Maxwell, J.C. (1873). A Treatise on Electricity and Magnetism. "
            f"Part {self.part}, {self.format().split('):')[0].split('(')[1]}: {self.topic}"
        )


@dataclass
class CrossReference:
    """Cross-reference between documents."""
    source_doc: str
    target_doc: str
    source_section: str
    target_section: str
    context: str
    link_type: str  # "see_also", "related", "prerequisite", "follows_from"
    status: CitationStatus = CitationStatus.UNVERIFIED


@dataclass
class CitationIndex:
    """Index of all citations."""
    citations: Dict[str, Citation] = field(default_factory=dict)
    cross_references: List[CrossReference] = field(default_factory=list)
    article_coverage: Dict[int, Set[str]] = field(default_factory=lambda: defaultdict(set))
    
    def add_citation(self, citation: Citation):
        """Add citation to index."""
        self.citations[citation.id] = citation
        
        if isinstance(citation, MaxwellArticleCitation):
            for article in range(citation.start_article, citation.end_article + 1):
                self.article_coverage[article].add(citation.id)
    
    def get_articles_covered(self) -> Set[int]:
        """Get set of all covered article numbers."""
        return set(self.article_coverage.keys())
    
    def get_coverage_stats(self) -> Dict[str, float]:
        """Get coverage statistics."""
        total_articles = 866
        covered = len(self.get_articles_covered())
        
        part_coverage = {}
        part_ranges = [(1, 229), (230, 370), (371, 474), (475, 866)]
        part_names = ["I: Electrostatics", "II: Electrokinematics", 
                      "III: Magnetism", "IV: Electromagnetism"]
        
        for (start, end), name in zip(part_ranges, part_names):
            part_articles = set(range(start, end + 1))
            part_covered = part_articles & self.get_articles_covered()
            part_coverage[name] = len(part_covered) / (end - start + 1) * 100
        
        return {
            "total_coverage": covered / total_articles * 100,
            "articles_covered": covered,
            "total_articles": total_articles,
            **part_coverage
        }


# ============================================================================
# CITATION EXTRACTION
# ============================================================================

def extract_maxwell_citations(text: str) -> List[Tuple[int, int]]:
    """
    Extract Maxwell article citations from text.
    
    Args:
        text: Text to extract from
    
    Returns:
        List of (start_article, end_article) tuples
    """
    patterns = [
        r'Art\.?\s*(\d+)-(\d+)',  # Art. 730-750
        r'Art\.?\s*(\d+)',         # Art. 730
        r'Article\s*(\d+)-(\d+)',  # Article 730-750
        r'Article\s*(\d+)',        # Article 730
    ]
    
    citations = []
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if len(match) == 2:
                citations.append((int(match[0]), int(match[1])))
            else:
                citations.append((int(match[0]), int(match[0])))
    
    return citations


def extract_document_references(text: str) -> List[str]:
    """
    Extract document references from text.
    
    Args:
        text: Text to extract from
    
    Returns:
        List of document reference strings
    """
    patterns = [
        r'\[([^\]]+)\]\(([^)]+)\)',  # Markdown links
        r'`([^`]+)`',                 # Code references
        r'@(\w+)',                    # Agent mentions
    ]
    
    references = []
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                references.append(match[0])
            else:
                references.append(match)
    
    return references


def parse_citation_context(
    text: str,
    citation: str,
    context_window: int = 100
) -> str:
    """
    Get context around a citation.
    
    Args:
        text: Full text
        citation: Citation to find
        context_window: Characters before and after
    
    Returns:
        Context string
    """
    pos = text.find(citation)
    if pos == -1:
        return ""
    
    start = max(0, pos - context_window)
    end = min(len(text), pos + len(citation) + context_window)
    
    context = text[start:end]
    
    # Clean up
    if start > 0:
        context = "..." + context
    if end < len(text):
        context = context + "..."
    
    return context


# ============================================================================
# CITATION VALIDATION
# ============================================================================

def validate_article_number(article: int) -> bool:
    """
    Validate Maxwell article number.
    
    Args:
        article: Article number
    
    Returns:
        True if valid
    """
    return 1 <= article <= 866


def validate_citation_format(citation: str) -> bool:
    """
    Validate citation format.
    
    Args:
        citation: Citation string
    
    Returns:
        True if valid format
    """
    patterns = [
        r'^Maxwell\s*\(\s*1873\s*,?\s*Art\.?\s*\d+',
        r'^Art\.?\s*\d+(?:-\d+)?',
        r'^Part\s+[IVX]+',
    ]
    
    return any(re.match(p, citation, re.IGNORECASE) for p in patterns)


def validate_cross_reference(
    source: str,
    target: str,
    document_index: Dict[str, List[str]]
) -> bool:
    """
    Validate cross-reference exists.
    
    Args:
        source: Source document
        target: Target document
        document_index: Index of documents and sections
    
    Returns:
        True if valid
    """
    if source not in document_index:
        return False
    
    # Check if target exists
    for doc, sections in document_index.items():
        if target in doc or any(target in s for s in sections):
            return True
    
    return False


# ============================================================================
# CITATION NETWORK ANALYSIS
# ============================================================================

def build_citation_network(
    citations: List[MaxwellArticleCitation]
) -> Dict[int, List[str]]:
    """
    Build citation network by article.
    
    Args:
        citations: List of citations
    
    Returns:
        Dictionary mapping article to citing documents
    """
    network = defaultdict(list)
    
    for citation in citations:
        for article in range(citation.start_article, citation.end_article + 1):
            network[article].append(citation.id)
    
    return dict(network)


def find_most_cited_articles(
    citations: List[MaxwellArticleCitation],
    top_n: int = 10
) -> List[Tuple[int, int]]:
    """
    Find most frequently cited articles.
    
    Args:
        citations: List of citations
        top_n: Number to return
    
    Returns:
        List of (article, count) tuples
    """
    citation_counts = defaultdict(int)
    
    for citation in citations:
        for article in range(citation.start_article, citation.end_article + 1):
            citation_counts[article] += 1
    
    sorted_articles = sorted(
        citation_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    return sorted_articles[:top_n]


def find_uncited_articles(
    citations: List[MaxwellArticleCitation]
) -> List[int]:
    """
    Find articles not cited in any document.
    
    Args:
        citations: List of citations
    
    Returns:
        List of uncited article numbers
    """
    cited = set()
    
    for citation in citations:
        for article in range(citation.start_article, citation.end_article + 1):
            cited.add(article)
    
    all_articles = set(range(1, 867))
    uncited = all_articles - cited
    
    return sorted(list(uncited))


# ============================================================================
# BIBLIOGRAPHIC UTILITIES
# ============================================================================

def create_bibliography_entry(
    author: str,
    year: int,
    title: str,
    publisher: str = "",
    location: str = "",
    edition: str = ""
) -> str:
    """
    Create bibliography entry.
    
    Args:
        author: Author name
        year: Publication year
        title: Title
        publisher: Publisher name
        location: Publication location
        edition: Edition
    
    Returns:
        Formatted bibliography entry
    """
    entry = f"{author} ({year}). {title}"
    
    if edition:
        entry += f" ({edition} ed.)"
    
    if publisher:
        entry += f". {publisher}"
    
    if location:
        entry += f", {location}"
    
    entry += "."
    
    return entry


def create_maxwell_bibliography(
    edition: str = "3rd"
) -> str:
    """
    Create Maxwell Treatise bibliography entry.
    
    Args:
        edition: Edition number
    
    Returns:
        Bibliography entry
    """
    return create_bibliography_entry(
        author="Maxwell, J.C",
        year=1873,
        title="A Treatise on Electricity and Magnetism",
        publisher="Clarendon Press",
        location="Oxford",
        edition=edition
    )


def format_bibliography(
    entries: List[str],
    style: str = "apa"
) -> str:
    """
    Format bibliography.
    
    Args:
        entries: List of bibliography entries
        style: Citation style
    
    Returns:
        Formatted bibliography
    """
    if style == "apa":
        entries.sort()
        return "\n\n".join(entries)
    elif style == "ieee":
        return "\n".join(
            f"[{i+1}] {entry}" 
            for i, entry in enumerate(entries)
        )
    else:
        return "\n".join(entries)


# ============================================================================
# CGS CITATION CONTEXT
# ============================================================================

def get_cgs_context_for_article(article: int) -> List[str]:
    """
    Get CGS units relevant to specific article.
    
    Args:
        article: Article number
    
    Returns:
        List of relevant CGS units
    """
    article_unit_map = {
        (1, 229): ["statC", "statV", "statΩ", "statF"],    # Electrostatics
        (230, 370): ["statA", "statV", "statΩ"],           # Electrokinematics
        (371, 474): ["G", "Oe", "emu", "Mx"],              # Magnetism
        (475, 866): ["statA", "statV", "G", "Oe"],         # Electromagnetism
        (730, 750): ["statA", "statV", "dyn·cm", "cm"],    # Galvanometers
        (343, 348): ["statΩ", "statV", "statA"],           # Wheatstone Bridge
    }
    
    for (start, end), units in article_unit_map.items():
        if start <= article <= end:
            return units
    
    return ["statV", "statA", "statΩ"]  # Default


def add_cgs_note_to_citation(
    citation: str,
    article: int
) -> str:
    """
    Add CGS unit note to citation.
    
    Args:
        citation: Citation string
        article: Article number
    
    Returns:
        Citation with CGS note
    """
    units = get_cgs_context_for_article(article)
    unit_str = ", ".join(units)
    
    return (
        f"{citation}\n\n*Note: All units in CGS system "
        f"({unit_str}) per Maxwell's convention.*"
    )


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Example: Extract citations
    text = "See Maxwell (1873, Art. 730-750) and Art. 343-348 for bridges."
    citations = extract_maxwell_citations(text)
    print(f"Found citations: {citations}")
    
    # Example: Validate article
    print(f"Article 730 valid: {validate_article_number(730)}")
    print(f"Article 900 valid: {validate_article_number(900)}")
    
    # Example: Create citation
    citation = MaxwellArticleCitation(
        id="CIT-001",
        citation_type=CitationType.MAXWELL_ARTICLE,
        status=CitationStatus.VALID,
        part=4,
        start_article=730,
        end_article=750,
        topic="Galvanometers",
        context="Galvanometer sensitivity analysis",
        created=datetime.now(),
        modified=datetime.now()
    )
    
    print(f"\nFormatted: {citation.format()}")
    print(f"Reference: {citation.full_reference()}")
    
    # Example: Find most cited
    sample = [
        MaxwellArticleCitation(
            id=f"CIT-{i}",
            citation_type=CitationType.MAXWELL_ARTICLE,
            status=CitationStatus.VALID,
            part=4,
            start_article=730,
            end_article=750,
            topic="Galvanometers",
            created=datetime.now(),
            modified=datetime.now()
        )
        for i in range(5)
    ]
    
    most_cited = find_most_cited_articles(sample, top_n=5)
    print(f"\nMost cited: {most_cited}")
```

---

## Usage Examples

```python
from citation_linking_utils import *

# Example 1: Extract citations from text
text = "According to Maxwell (Art. 730-750)..."
citations = extract_maxwell_citations(text)
print(citations)  # [(730, 750)]

# Example 2: Validate article number
valid = validate_article_number(730)
print(f"Valid: {valid}")

# Example 3: Build citation index
index = CitationIndex()
citation = MaxwellArticleCitation(...)
index.add_citation(citation)
stats = index.get_coverage_stats()
print(f"Coverage: {stats}")

# Example 4: Find most cited
top = find_most_cited_articles(citations, top_n=10)
```

---

## Quality Criteria

- [ ] Citation extraction accurate
- [ ] Validation functions correct
- [ ] Network analysis functional
- [ ] Bibliography formatting correct
- [ ] CGS context integration working

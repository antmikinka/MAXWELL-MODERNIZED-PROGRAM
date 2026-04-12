# Utility: documentation_generator_utils

## Purpose

Python utility module for automated documentation generation.

## Location

`agents/scriba/utils/documentation_generator_utils.py`

---

## Module Contents

```python
"""
SCRIBA Documentation Generator Utilities

Automated documentation generation for the Maxwell Treatise 
Modernization Project.

Documentation Types:
- API reference documentation
- Tutorial documentation
- Cross-reference indices
- Citation management
- Release notes

Theory Classification:
- maxwell_original: Maxwell's 1873 formulations
- user_original: User's theoretical extensions (DO NOT CHANGE)
- standard_math: Standard mathematical implementations

Maxwell References: Art. 1-866 (complete Treatise)
"""

from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import re


class DocumentationType(Enum):
    """Documentation types."""
    API_REFERENCE = "api_reference"
    TUTORIAL = "tutorial"
    CROSS_REFERENCE = "cross_reference"
    CITATION_INDEX = "citation_index"
    RELEASE_NOTES = "release_notes"
    VERSION_HISTORY = "version_history"
    VALIDATION_REPORT = "validation_report"


class TheoryClassification(Enum):
    """Theory classification."""
    MAXWELL_ORIGINAL = "maxwell_original"
    USER_ORIGINAL = "user_original"
    STANDARD_MATH = "standard_math"


@dataclass
class MaxwellCitation:
    """Maxwell article citation."""
    part: int
    articles: Tuple[int, int]  # Start, end
    topic: str
    context: str
    
    def format_citation(self) -> str:
        """Format citation string."""
        if self.articles[0] == self.articles[1]:
            return f"Art. {self.articles[0]}"
        else:
            return f"Art. {self.articles[0]}-{self.articles[1]}"
    
    def full_reference(self) -> str:
        """Full reference string."""
        part roman = {
            1: "I", 2: "II", 3: "III", 4: "IV"
        }.get(self.part, str(self.part))
        
        return (
            f"Maxwell, J.C. (1873). A Treatise on Electricity and Magnetism. "
            f"Part {part_roman}, {self.format_citation()}: {self.topic}"
        )


@dataclass
class DocumentationComponent:
    """Documentation component."""
    name: str
    doc_type: DocumentationType
    cgs_units: List[str]
    maxwell_citations: List[MaxwellCitation]
    theory_classification: TheoryClassification
    content: str
    variables: Dict[str, str]


# ============================================================================
# CGS UNIT DOCUMENTATION
# ============================================================================

def get_cgs_units_for_topic(topic: str) -> List[str]:
    """
    Get CGS units relevant to topic.
    
    Args:
        topic: Topic name
    
    Returns:
        List of relevant CGS units
    """
    unit_map = {
        "electrostatics": ["statC", "statV", "statΩ", "statF"],
        "electrokinematics": ["statA", "statV", "statΩ"],
        "magnetism": ["G", "Oe", "emu", "Mx"],
        "electromagnetism": ["statA", "statV", "G", "Oe"],
        "galvanometer": ["statA", "statV", "dyn·cm", "cm"],
        "magnetometer": ["Oe", "G", "emu", "rad"],
        "electrometer": ["statV", "statC", "statF", "rad"],
        "bridge": ["statΩ", "statV", "statA"],
    }
    
    for key, units in unit_map.items():
        if key in topic.lower():
            return units
    
    return ["statV", "statA", "statΩ"]  # Default electrical units


def format_cgs_unit_table(units: List[str]) -> str:
    """
    Format CGS unit reference table.
    
    Args:
        units: List of CGS unit symbols
    
    Returns:
        Markdown table string
    """
    unit_details = {
        "statV": ("statvolt", "Potential", "299.79 V"),
        "statA": ("statampere", "Current", "3.336×10^-10 A"),
        "statΩ": ("statohm", "Resistance", "8.988×10^11 Ω"),
        "statC": ("statcoulomb", "Charge", "3.336×10^-10 C"),
        "statF": ("statfarad", "Capacitance", "1.113×10^-12 F"),
        "G": ("gauss", "Magnetic induction B", "10^-4 T"),
        "Oe": ("oersted", "Magnetic field H", "79.577 A/m"),
        "emu": ("emu", "Magnetic moment", "10^-3 A·m²"),
        "Mx": ("maxwell", "Magnetic flux", "10^-8 Wb"),
        "dyn·cm": ("dyne-centimeter", "Torque", "10^-7 N·m"),
        "cm": ("centimeter", "Deflection", "0.01 m"),
        "rad": ("radian", "Angle", "1 rad"),
    }
    
    lines = []
    lines.append("| Quantity | CGS Unit | Symbol | SI Equivalent |")
    lines.append("|----------|----------|--------|---------------|")
    
    for unit in units:
        if unit in unit_details:
            name, quantity, si = unit_details[unit]
            lines.append(f"| {quantity} | {name} | {unit} | {si} |")
    
    return "\n".join(lines)


def get_physical_constants() -> Dict[str, str]:
    """
    Get physical constants in CGS units.
    
    Returns:
        Dictionary of constants
    """
    return {
        "c": "2.99792458×10^10 cm/s (speed of light)",
        "k_B": "1.381×10^-16 erg/K (Boltzmann constant)",
        "e": "4.803×10^-10 statC (elementary charge)",
        "h": "6.626×10^-27 erg·s (Planck constant)",
        "ℏ": "1.055×10^-27 erg·s (reduced Planck constant)",
        "m_e": "9.109×10^-28 g (electron mass)",
        "m_p": "1.673×10^-24 g (proton mass)",
    }


# ============================================================================
# MAXWELL CITATION MANAGEMENT
# ============================================================================

def parse_article_range(article_str: str) -> Tuple[int, int]:
    """
    Parse Maxwell article range string.
    
    Args:
        article_str: Article string (e.g., "Art. 730-750")
    
    Returns:
        (start_article, end_article)
    """
    match = re.search(r'Art\.?\s*(\d+)(?:-(\d+))?', article_str)
    if not match:
        raise ValueError(f"Invalid article format: {article_str}")
    
    start = int(match.group(1))
    end = int(match.group(2)) if match.group(2) else start
    
    return start, end


def get_maxwell_part(article: int) -> int:
    """
    Get Maxwell Treatise part for article number.
    
    Args:
        article: Article number
    
    Returns:
        Part number (1-4)
    """
    if article <= 229:
        return 1  # Electrostatics
    elif article <= 370:
        return 2  # Electrokinematics
    elif article <= 474:
        return 3  # Magnetism
    else:
        return 4  # Electromagnetism


def get_maxwell_topic(article_range: Tuple[int, int]) -> str:
    """
    Get topic description for article range.
    
    Args:
        article_range: (start, end) article numbers
    
    Returns:
        Topic description
    """
    topics = {
        (1, 229): "Electrostatics",
        (230, 370): "Electrokinematics",
        (371, 474): "Magnetism",
        (475, 866): "Electromagnetism",
        (730, 750): "Galvanometers",
        (343, 348): "Wheatstone Bridge",
        (449, 474): "Magnetic Measurements",
        (44, 49): "Electric Potential",
        (230, 235): "Electrification",
    }
    
    start, end = article_range
    
    for (s, e), topic in topics.items():
        if s <= start <= end <= e:
            return topic
    
    return "Electromagnetism"  # Default


def format_maxwell_citation(
    articles: Tuple[int, int],
    include_part: bool = True,
    include_topic: bool = True
) -> str:
    """
    Format Maxwell article citation.
    
    Args:
        articles: (start, end) article numbers
        include_part: Include part number
        include_topic: Include topic description
    
    Returns:
        Formatted citation
    """
    start, end = articles
    
    if start == end:
        article_str = f"Art. {start}"
    else:
        article_str = f"Art. {start}-{end}"
    
    result = article_str
    
    if include_part:
        part = get_maxwell_part(start)
        part_roman = {1: "I", 2: "II", 3: "III", 4: "IV"}.get(part, str(part))
        result = f"Part {part_roman}, {result}"
    
    if include_topic:
        topic = get_maxwell_topic(articles)
        result = f"{result}: {topic}"
    
    return result


def create_full_maxwell_reference(
    articles: Tuple[int, int],
    edition: str = "3rd"
) -> str:
    """
    Create full Maxwell reference.
    
    Args:
        articles: (start, end) article numbers
        edition: Edition number
    
    Returns:
        Full reference string
    """
    article_citation = format_maxwell_citation(articles)
    
    return (
        f"Maxwell, J.C. (1873). A Treatise on Electricity and Magnetism "
        f"({edition} ed.). Clarendon Press, Oxford. {article_citation}"
    )


# ============================================================================
# THEORY CLASSIFICATION
# ============================================================================

def classify_theory(content: str) -> TheoryClassification:
    """
    Classify theory content.
    
    Args:
        content: Content to classify
    
    Returns:
        TheoryClassification
    
    Note: This is a helper - actual classification should be 
    determined by content analysis and user input.
    """
    content_lower = content.lower()
    
    if "user_original" in content_lower or "user's extension" in content_lower:
        return TheoryClassification.USER_ORIGINAL
    elif "standard_math" in content_lower or "standard implementation" in content_lower:
        return TheoryClassification.STANDARD_MATH
    else:
        return TheoryClassification.MAXWELL_ORIGINAL


def format_theory_classification(classification: TheoryClassification) -> str:
    """
    Format theory classification for documentation.
    
    Args:
        classification: TheoryClassification
    
    Returns:
        Formatted description
    """
    descriptions = {
        TheoryClassification.MAXWELL_ORIGINAL: (
            "**maxwell_original**: From Maxwell's 1873 Treatise"
        ),
        TheoryClassification.USER_ORIGINAL: (
            "**user_original**: User's theoretical extension (authoritative - DO NOT ALTER)"
        ),
        TheoryClassification.STANDARD_MATH: (
            "**standard_math**: Standard mathematical implementation"
        ),
    }
    
    return descriptions.get(classification, "")


# ============================================================================
# DOCUMENTATION TEMPLATE UTILITIES
# ============================================================================

def extract_template_variables(template: str) -> List[str]:
    """
    Extract variables from template.
    
    Args:
        template: Template string with {{VARIABLE}} markers
    
    Returns:
        List of variable names
    """
    return re.findall(r'\{\{(\w+)\}\}', template)


def populate_template(template: str, variables: Dict[str, str]) -> str:
    """
    Populate template with variables.
    
    Args:
        template: Template string
        variables: Variable dictionary
    
    Returns:
        Populated template
    """
    result = template
    for name, value in variables.items():
        result = result.replace(f"{{{{{name}}}}}", value)
    return result


def validate_template_completion(
    template: str,
    variables: Dict[str, str]
) -> List[str]:
    """
    Validate all required variables are populated.
    
    Args:
        template: Template string
        variables: Variable dictionary
    
    Returns:
        List of missing variables
    """
    required = extract_template_variables(template)
    missing = []
    
    for var in required:
        if var not in variables or not variables[var]:
            missing.append(var)
    
    return missing


# ============================================================================
# DOCUMENTATION QUALITY VALIDATION
# ============================================================================

def validate_cgs_units(content: str) -> Tuple[bool, List[str]]:
    """
    Validate CGS units in content.
    
    Args:
        content: Content to validate
    
    Returns:
        (is_valid, list of issues)
    """
    issues = []
    
    # Check for SI units as primary (should be CGS)
    si_patterns = [
        r'\d+\.?\d*\s*V(?!stat)',  # Volts (not statvolt)
        r'\d+\.?\d*\s*A(?!stat)',  # Amperes (not statampere)
        r'\d+\.?\d*\s*Ω(?!stat)',  # Ohms (not statohm)
    ]
    
    for pattern in si_patterns:
        if re.search(pattern, content):
            issues.append("SI units detected - use CGS as primary")
    
    # Check for CGS units (should be present)
    cgs_patterns = [r'statV', r'statA', r'statΩ', r'statC', r'gauss', r'oersted']
    has_cgs = any(re.search(p, content) for p in cgs_patterns)
    
    if not has_cgs and any(p in content for p in ['potential', 'current', 'resistance']):
        issues.append("CGS units expected but not found")
    
    return len(issues) == 0, issues


def validate_maxwell_citations(content: str) -> Tuple[bool, List[str]]:
    """
    Validate Maxwell citations in content.
    
    Args:
        content: Content to validate
    
    Returns:
        (is_valid, list of issues)
    """
    issues = []
    
    # Check for article citations
    citations = re.findall(r'Art\.?\s*\d+(?:-\d+)?', content)
    
    if not citations and any(kw in content.lower() for kw in ['maxwell', 'treatise']):
        issues.append("Maxwell mention without article citation")
    
    # Validate article numbers
    for citation in citations:
        start, end = parse_article_range(citation)
        if start < 1 or end > 866:
            issues.append(f"Invalid article number in {citation}")
    
    return len(issues) == 0, issues


# ============================================================================
# VERSION AND RELEASE UTILITIES
# ============================================================================

def parse_semver(version: str) -> Tuple[int, int, int]:
    """
    Parse semantic version string.
    
    Args:
        version: Version string (e.g., "1.2.3")
    
    Returns:
        (major, minor, patch)
    """
    match = re.match(r'(\d+)\.(\d+)\.(\d+)', version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def increment_version(
    version: str,
    increment_type: str = "patch"
) -> str:
    """
    Increment version number.
    
    Args:
        version: Current version
        increment_type: "major", "minor", or "patch"
    
    Returns:
        New version string
    """
    major, minor, patch = parse_semver(version)
    
    if increment_type == "major":
        return f"{major + 1}.0.0"
    elif increment_type == "minor":
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Example: Format Maxwell citation
    citation = format_maxwell_citation((730, 750))
    print(f"Citation: {citation}")
    
    # Example: Get CGS units
    units = get_cgs_units_for_topic("galvanometer")
    print(f"CGS units: {units}")
    
    # Example: Full reference
    ref = create_full_maxwell_reference((730, 750))
    print(f"Reference: {ref}")
    
    # Example: CGS unit table
    table = format_cgs_unit_table(["statV", "statA", "statΩ"])
    print(table)
```

---

## Usage Examples

```python
from documentation_generator_utils import *

# Example 1: Format Maxwell citation
citation = format_maxwell_citation((730, 750))
print(citation)  # Part IV, Art. 730-750: Galvanometers

# Example 2: Get CGS units
units = get_cgs_units_for_topic("magnetometer")
print(units)  # ['Oe', 'G', 'emu', 'rad']

# Example 3: Full reference
ref = create_full_maxwell_reference((343, 348))
print(ref)  # Maxwell, J.C. (1873). A Treatise...

# Example 4: Populate template
template = "Module: {{MODULE_NAME}}\n\nPurpose: {{PURPOSE}}"
variables = {"MODULE_NAME": "galvanometer", "PURPOSE": "Modeling"}
result = populate_template(template, variables)
```

---

## Quality Criteria

- [ ] CGS unit utilities functional
- [ ] Maxwell citation formatting correct
- [ ] Theory classification preserved
- [ ] Template utilities working
- [ ] Validation functions accurate

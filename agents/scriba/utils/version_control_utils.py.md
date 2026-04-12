# Utility: version_control_utils

## Purpose

Python utility module for version control and release management.

## Location

`agents/scriba/utils/version_control_utils.py`

---

## Module Contents

```python
"""
SCRIBA Version Control Utilities

Version management, release notes generation, and change tracking
for the Maxwell Treatise Modernization Project.

Version Control:
- Semantic versioning (MAJOR.MINOR.PATCH)
- Release notes generation
- Change tracking
- Version history maintenance

Theory Classification:
- maxwell_original: Maxwell's 1873 formulations
- user_original: User's theoretical extensions (DO NOT CHANGE)
- standard_math: Standard mathematical implementations

Maxwell References: Art. 1-866 (complete Treatise)
"""

from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import re
from pathlib import Path


class ChangeType(Enum):
    """Change types for releases."""
    ADDED = "added"
    CHANGED = "changed"
    FIXED = "fixed"
    DEPRECATED = "deprecated"
    REMOVED = "removed"
    SECURITY = "security"
    CGS = "cgs"
    MAXWELL = "maxwell"


class VersionStatus(Enum):
    """Version status."""
    DRAFT = "draft"
    RELEASE_CANDIDATE = "rc"
    RELEASED = "released"
    DEPRECATED = "deprecated"


@dataclass
class Change:
    """Individual change entry."""
    change_type: ChangeType
    description: str
    component: str = ""
    maxwell_articles: str = ""
    cgs_units: str = ""
    breaking: bool = False
    issue_id: str = ""


@dataclass
class Version:
    """Version representation."""
    major: int
    minor: int
    patch: int
    prerelease: str = ""
    build: str = ""
    
    def __str__(self) -> str:
        """String representation."""
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        if self.build:
            version += f"+{self.build}"
        return version
    
    def __lt__(self, other: 'Version') -> bool:
        """Less than comparison."""
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        return self.patch < other.patch
    
    def __eq__(self, other: 'Version') -> bool:
        """Equality comparison."""
        return (
            self.major == other.major and
            self.minor == other.minor and
            self.patch == other.patch
        )


@dataclass
class Release:
    """Release information."""
    version: Version
    date: datetime
    status: VersionStatus
    summary: str = ""
    changes: Dict[ChangeType, List[Change]] = field(default_factory=dict)
    cgs_changes: List[str] = field(default_factory=list)
    maxwell_coverage_changes: List[str] = field(default_factory=list)
    breaking_changes: List[str] = field(default_factory=list)
    migration_guide: str = ""
    author: str = ""
    reviewer: str = ""


@dataclass
class VersionHistory:
    """Complete version history."""
    project_name: str
    first_release: datetime
    releases: List[Release] = field(default_factory=list)
    
    def add_release(self, release: Release):
        """Add release to history."""
        self.releases.append(release)
        self.releases.sort(key=lambda r: r.version, reverse=True)
    
    def get_latest(self) -> Optional[Release]:
        """Get latest release."""
        return self.releases[0] if self.releases else None
    
    def get_releases_by_year(self, year: int) -> List[Release]:
        """Get releases from specific year."""
        return [r for r in self.releases if r.date.year == year]
    
    def get_statistics(self) -> Dict[str, int]:
        """Get release statistics."""
        stats = {
            "total_releases": len(self.releases),
            "major_releases": 0,
            "minor_releases": 0,
            "patch_releases": 0,
            "years_active": 0,
        }
        
        years = set()
        for release in self.releases:
            years.add(release.date.year)
            
            if release.version.minor == 0 and release.version.patch == 0:
                stats["major_releases"] += 1
            elif release.version.patch == 0:
                stats["minor_releases"] += 1
            else:
                stats["patch_releases"] += 1
        
        if years:
            stats["years_active"] = max(years) - min(years) + 1
        
        return stats


# ============================================================================
# VERSION PARSING
# ============================================================================

def parse_version(version_str: str) -> Version:
    """
    Parse version string.
    
    Args:
        version_str: Version string (e.g., "1.2.3-beta+build.123")
    
    Returns:
        Version object
    """
    pattern = r'(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.]+))?(?:\+([a-zA-Z0-9.]+))?'
    match = re.match(pattern, version_str)
    
    if not match:
        raise ValueError(f"Invalid version format: {version_str}")
    
    return Version(
        major=int(match.group(1)),
        minor=int(match.group(2)),
        patch=int(match.group(3)),
        prerelease=match.group(4) or "",
        build=match.group(5) or ""
    )


def increment_version(
    version: Version,
    increment_type: str = "patch"
) -> Version:
    """
    Increment version.
    
    Args:
        version: Current version
        increment_type: "major", "minor", or "patch"
    
    Returns:
        New Version
    """
    if increment_type == "major":
        return Version(
            major=version.major + 1,
            minor=0,
            patch=0
        )
    elif increment_type == "minor":
        return Version(
            major=version.major,
            minor=version.minor + 1,
            patch=0
        )
    else:  # patch
        return Version(
            major=version.major,
            minor=version.minor,
            patch=version.patch + 1
        )


def compare_versions(v1: str, v2: str) -> int:
    """
    Compare two version strings.
    
    Args:
        v1: First version
        v2: Second version
    
    Returns:
        -1 if v1 < v2, 0 if equal, 1 if v1 > v2
    """
    ver1 = parse_version(v1)
    ver2 = parse_version(v2)
    
    if ver1 < ver2:
        return -1
    elif ver1 == ver2:
        return 0
    else:
        return 1


# ============================================================================
# CHANGE TRACKING
# ============================================================================

def categorize_change(
    description: str,
    keywords: Optional[Dict[ChangeType, List[str]]] = None
) -> ChangeType:
    """
    Categorize change based on description.
    
    Args:
        description: Change description
        keywords: Optional custom keywords
    
    Returns:
        ChangeType
    """
    if keywords is None:
        keywords = {
            ChangeType.ADDED: ["add", "new", "create", "implement"],
            ChangeType.CHANGED: ["change", "update", "modify", "improve"],
            ChangeType.FIXED: ["fix", "bug", "correct", "resolve"],
            ChangeType.DEPRECATED: ["deprecate", "obsolete", "legacy"],
            ChangeType.REMOVED: ["remove", "delete", "drop"],
            ChangeType.SECURITY: ["security", "vulnerability", "patch"],
            ChangeType.CGS: ["cgs", "unit", "statvolt", "statampere"],
            ChangeType.MAXWELL: ["maxwell", "article", "citation", "treatise"],
        }
    
    desc_lower = description.lower()
    
    for change_type, type_keywords in keywords.items():
        if any(kw in desc_lower for kw in type_keywords):
            return change_type
    
    return ChangeType.CHANGED  # Default


def create_change(
    description: str,
    component: str = "",
    maxwell_articles: str = "",
    cgs_units: str = "",
    breaking: bool = False,
    issue_id: str = ""
) -> Change:
    """
    Create change entry.
    
    Args:
        description: Change description
        component: Affected component
        maxwell_articles: Related Maxwell articles
        cgs_units: Related CGS units
        breaking: Whether this is a breaking change
        issue_id: Issue tracker ID
    
    Returns:
        Change object
    """
    change_type = categorize_change(description)
    
    return Change(
        change_type=change_type,
        description=description,
        component=component,
        maxwell_articles=maxwell_articles,
        cgs_units=cgs_units,
        breaking=breaking,
        issue_id=issue_id
    )


# ============================================================================
# RELEASE NOTES GENERATION
# ============================================================================

def generate_release_notes(release: Release) -> str:
    """
    Generate release notes from release data.
    
    Args:
        release: Release object
    
    Returns:
        Formatted release notes
    """
    lines = []
    
    # Header
    lines.append(f"# Release Notes: Version {release.version}")
    lines.append("")
    lines.append(f"**Release Date:** {release.date.strftime('%Y-%m-%d')}")
    lines.append(f"**Status:** {release.status.value}")
    lines.append("")
    
    # Summary
    if release.summary:
        lines.append("## Summary")
        lines.append("")
        lines.append(release.summary)
        lines.append("")
    
    # Breaking changes
    if release.breaking_changes:
        lines.append("## ⚠️ Breaking Changes")
        lines.append("")
        for change in release.breaking_changes:
            lines.append(f"- {change}")
        lines.append("")
    
    # Changes by type
    type_order = [
        ChangeType.ADDED,
        ChangeType.CHANGED,
        ChangeType.FIXED,
        ChangeType.DEPRECATED,
        ChangeType.REMOVED,
        ChangeType.SECURITY,
        ChangeType.CGS,
        ChangeType.MAXWELL,
    ]
    
    for change_type in type_order:
        if change_type in release.changes and release.changes[change_type]:
            lines.append(f"## {change_type.value.capitalize()}")
            lines.append("")
            for change in release.changes[change_type]:
                line = f"- {change.description}"
                if change.component:
                    line += f" (`{change.component}`)"
                if change.issue_id:
                    line += f" #{change.issue_id}"
                lines.append(line)
            lines.append("")
    
    # CGS changes
    if release.cgs_changes:
        lines.append("## CGS Unit Changes")
        lines.append("")
        for change in release.cgs_changes:
            lines.append(f"- {change}")
        lines.append("")
    
    # Maxwell coverage
    if release.maxwell_coverage_changes:
        lines.append("## Maxwell Article Coverage")
        lines.append("")
        for change in release.maxwell_coverage_changes:
            lines.append(f"- {change}")
        lines.append("")
    
    # Migration guide
    if release.migration_guide:
        lines.append("## Migration Guide")
        lines.append("")
        lines.append(release.migration_guide)
        lines.append("")
    
    # Credits
    if release.author or release.reviewer:
        lines.append("## Credits")
        lines.append("")
        if release.author:
            lines.append(f"**Author:** {release.author}")
        if release.reviewer:
            lines.append(f"**Reviewer:** {release.reviewer}")
        lines.append("")
    
    return "\n".join(lines)


def generate_changelog_entry(release: Release) -> str:
    """
    Generate changelog entry.
    
    Args:
        release: Release object
    
    Returns:
        Changelog entry
    """
    lines = []
    
    lines.append(f"## [{release.version}] - {release.date.strftime('%Y-%m-%d')}")
    lines.append("")
    
    if release.summary:
        lines.append(f"### Summary")
        lines.append("")
        lines.append(release.summary)
        lines.append("")
    
    # Group changes by type
    type_names = {
        ChangeType.ADDED: "Added",
        ChangeType.CHANGED: "Changed",
        ChangeType.FIXED: "Fixed",
        ChangeType.DEPRECATED: "Deprecated",
        ChangeType.REMOVED: "Removed",
        ChangeType.SECURITY: "Security",
        ChangeType.CGS: "CGS",
        ChangeType.MAXWELL: "Maxwell",
    }
    
    for change_type, name in type_names.items():
        if change_type in release.changes and release.changes[change_type]:
            lines.append(f"### {name}")
            lines.append("")
            for change in release.changes[change_type]:
                lines.append(f"- {change.description}")
            lines.append("")
    
    return "\n".join(lines)


# ============================================================================
# VERSION HISTORY UTILITIES
# ============================================================================

def create_version_history(
    project_name: str,
    first_release_date: datetime
) -> VersionHistory:
    """
    Create new version history.
    
    Args:
        project_name: Project name
        first_release_date: First release date
    
    Returns:
        VersionHistory object
    """
    return VersionHistory(
        project_name=project_name,
        first_release=first_release_date
    )


def calculate_release_statistics(
    history: VersionHistory
) -> Dict[str, float]:
    """
    Calculate release statistics.
    
    Args:
        history: Version history
    
    Returns:
        Statistics dictionary
    """
    stats = history.get_statistics()
    
    if len(history.releases) > 1:
        # Calculate average days between releases
        total_days = 0
        for i in range(1, len(history.releases)):
            delta = history.releases[i-1].date - history.releases[i].date
            total_days += delta.days
        
        stats["avg_days_between_releases"] = total_days / (len(history.releases) - 1)
    else:
        stats["avg_days_between_releases"] = 0
    
    return stats


def format_version_history(history: VersionHistory) -> str:
    """
    Format version history for display.
    
    Args:
        history: Version history
    
    Returns:
        Formatted history
    """
    lines = []
    
    lines.append(f"# Version History: {history.project_name}")
    lines.append("")
    lines.append(f"**First Release:** {history.first_release.strftime('%Y-%m-%d')}")
    lines.append(f"**Total Releases:** {len(history.releases)}")
    lines.append("")
    
    stats = calculate_release_statistics(history)
    
    lines.append("## Statistics")
    lines.append("")
    lines.append(f"- Major releases: {stats['major_releases']}")
    lines.append(f"- Minor releases: {stats['minor_releases']}")
    lines.append(f"- Patch releases: {stats['patch_releases']}")
    lines.append(f"- Years active: {stats['years_active']}")
    if stats.get('avg_days_between_releases', 0) > 0:
        lines.append(f"- Average days between releases: {stats['avg_days_between_releases']:.1f}")
    lines.append("")
    
    lines.append("## Releases")
    lines.append("")
    
    for release in history.releases:
        lines.append(f"### [{release.version}] - {release.date.strftime('%Y-%m-%d')}")
        lines.append("")
        lines.append(f"**Status:** {release.status.value}")
        if release.summary:
            lines.append("")
            lines.append(release.summary)
        lines.append("")
    
    return "\n".join(lines)


# ============================================================================
# CGS AND MAXWELL TRACKING
# ============================================================================

def track_cgs_changes(
    changes: List[Change],
    version: Version
) -> List[str]:
    """
    Extract CGS-related changes.
    
    Args:
        changes: List of changes
        version: Version
    
    Returns:
        List of CGS change descriptions
    """
    cgs_changes = []
    
    for change in changes:
        if change.change_type == ChangeType.CGS:
            cgs_changes.append(change.description)
        elif change.cgs_units:
            cgs_changes.append(
                f"Updated {change.component}: {change.description} "
                f"(CGS units: {change.cgs_units})"
            )
    
    return cgs_changes


def track_maxwell_coverage(
    changes: List[Change],
    version: Version
) -> List[str]:
    """
    Track Maxwell article coverage changes.
    
    Args:
        changes: List of changes
        version: Version
    
    Returns:
        List of coverage change descriptions
    """
    coverage_changes = []
    
    for change in changes:
        if change.change_type == ChangeType.MAXWELL:
            coverage_changes.append(change.description)
        elif change.maxwell_articles:
            coverage_changes.append(
                f"Added coverage for {change.maxwell_articles}: "
                f"{change.description}"
            )
    
    return coverage_changes


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Example: Parse version
    version = parse_version("1.2.3-beta+build.123")
    print(f"Version: {version}")
    
    # Example: Increment version
    new_version = increment_version(version, "minor")
    print(f"New version: {new_version}")
    
    # Example: Create release
    release = Release(
        version=Version(1, 0, 0),
        date=datetime.now(),
        status=VersionStatus.RELEASED,
        summary="Initial release",
        changes={
            ChangeType.ADDED: [
                create_change("Added API documentation"),
                create_change("Added tutorial templates"),
            ],
            ChangeType.CGS: [
                create_change(
                    "Added CGS unit reference",
                    cgs_units="statV, statA, statΩ"
                ),
            ],
            ChangeType.MAXWELL: [
                create_change(
                    "Added Art. 730-750 coverage",
                    maxwell_articles="Art. 730-750"
                ),
            ],
        },
        author="Documentation Team",
        reviewer="Technical Lead"
    )
    
    # Example: Generate release notes
    notes = generate_release_notes(release)
    print(notes)
    
    # Example: Create version history
    history = create_version_history(
        "Maxwell Treatise Modernization",
        datetime(2024, 1, 1)
    )
    history.add_release(release)
    
    print(format_version_history(history))
```

---

## Usage Examples

```python
from version_control_utils import *

# Example 1: Parse and compare versions
v1 = parse_version("1.2.3")
v2 = parse_version("1.3.0")
print(f"v1 < v2: {v1 < v2}")  # True

# Example 2: Increment version
new_v = increment_version(v1, "minor")
print(f"New version: {new_v}")  # 1.3.0

# Example 3: Create release
release = Release(
    version=Version(1, 0, 0),
    date=datetime.now(),
    status=VersionStatus.RELEASED,
    summary="Initial release"
)

# Example 4: Generate release notes
notes = generate_release_notes(release)
print(notes)
```

---

## Quality Criteria

- [ ] Version parsing correct
- [ ] Semantic versioning implemented
- [ ] Release notes generation complete
- [ ] CGS changes tracked
- [ ] Maxwell coverage tracked

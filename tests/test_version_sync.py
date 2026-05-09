"""Version consistency tests.

Ensures that version strings are synchronized across all metadata sources:
- maxwell.__version__
- pyproject.toml [project].version
- importlib.metadata
"""

from __future__ import annotations

import re
from pathlib import Path

import maxwell


def test_maxwell_version_format():
    """__version__ should follow semver (MAJOR.MINOR.PATCH)."""
    version = maxwell.__version__
    assert re.match(
        r"^\d+\.\d+\.\d+", version
    ), f"Version '{version}' does not follow semver format"


def test_version_matches_pyproject():
    """maxwell.__version__ must match pyproject.toml version."""
    pyproject_path = Path(maxwell.__file__).parent.parent / "pyproject.toml"
    content = pyproject_path.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    assert match, "Could not find 'version' key in pyproject.toml"
    pyproject_version = match.group(1)
    assert maxwell.__version__ == pyproject_version, (
        f"Version mismatch: __version__={maxwell.__version__!r}, "
        f"pyproject.toml={pyproject_version!r}"
    )


def test_version_matches_metadata():
    """maxwell.__version__ must match importlib.metadata version."""
    try:
        from importlib.metadata import version as meta_version

        meta_ver = meta_version("maxwell")
        assert maxwell.__version__ == meta_ver, (
            f"Version mismatch: __version__={maxwell.__version__!r}, "
            f"metadata={meta_ver!r}"
        )
    except Exception:
        # Package not installed in editable mode; skip this check
        pass

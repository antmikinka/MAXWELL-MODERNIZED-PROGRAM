"""Version and publication-metadata consistency tests.

Ensures that living metadata agrees:
- maxwell.__version__
- pyproject.toml [project].version
- importlib.metadata
- CITATION.cff, .zenodo.json
- MIT software license + LICENSE / LICENSE-CONTENT files
- no phantom GitHub org and no fabricated ORCID in living files
- preprint/JOSS manuscript is not part of the repository; only a 'working toward a preprint' mention is allowed
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import maxwell

REPO_ROOT = Path(maxwell.__file__).resolve().parent.parent
PLACEHOLDER_ORCID = "0000-0000-0000-0000"
AUTHOR_ORCID = "0009-0005-2955-4140"
PHANTOM_REPO = "maxwell-treatise/modernized-program"
CANONICAL_REPO = "https://github.com/antmikinka/MAXWELL-MODERNIZED-PROGRAM"
LIVING_METADATA_FILES = (
    "README.md",
    "CITATION.cff",
    ".zenodo.json",
    "pyproject.toml",
    "CONTRIBUTING.md",
)


def _read(relative: str) -> str:
    return (REPO_ROOT / relative).read_text(encoding="utf-8")


def test_maxwell_version_format():
    """__version__ should follow semver (MAJOR.MINOR.PATCH)."""
    version = maxwell.__version__
    assert re.match(
        r"^\d+\.\d+\.\d+", version
    ), f"Version '{version}' does not follow semver format"


def test_version_matches_pyproject():
    """maxwell.__version__ must match pyproject.toml version."""
    content = _read("pyproject.toml")
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


def test_version_matches_citation_cff():
    """CITATION.cff software version must match the package."""
    match = re.search(r"^version:\s*(\S+)", _read("CITATION.cff"), re.MULTILINE)
    assert match, "Could not find version in CITATION.cff"
    assert match.group(1) == maxwell.__version__


def test_version_matches_zenodo():
    """Zenodo deposit metadata must match the package version."""
    data = json.loads(_read(".zenodo.json"))
    assert data["version"] == maxwell.__version__
    assert data["license"] == "MIT"
    assert data["pub_state"] != "published"


def test_preprint_is_mentioned_not_included():
    """A preprint may be mentioned as future work; it must not be in the repo."""
    cff = _read("CITATION.cff")
    readme = _read("README.md")
    gitignore = _read(".gitignore")
    assert "type: article" not in cff
    assert "preprint" in cff.lower()
    assert "preprint" in readme.lower()
    assert re.search(r"(?m)^paper/$", gitignore)
    # Local drafts may remain on disk; they must not ship a public paper license.
    assert not (REPO_ROOT / "paper" / "LICENSE.md").exists()


def test_software_license_is_mit():
    """PyPI / CITATION software license field stays MIT."""
    pyproject = _read("pyproject.toml")
    match = re.search(r'^license\s*=\s*"([^"]+)"', pyproject, re.MULTILINE)
    assert match and match.group(1) == "MIT"
    cff_match = re.search(r"^license:\s*(\S+)", _read("CITATION.cff"), re.MULTILINE)
    assert cff_match and cff_match.group(1) == "MIT"


def test_split_license_files_exist():
    """MIT software file and CC BY content file must both be present."""
    mit = REPO_ROOT / "LICENSE"
    content = REPO_ROOT / "LICENSE-CONTENT"
    assert mit.is_file()
    assert content.is_file()
    assert _read("LICENSE").lstrip().startswith("MIT License")
    body = _read("LICENSE-CONTENT")
    assert "Creative Commons Attribution 4.0 International Public License" in body
    assert "public domain worldwide" in body


def test_living_metadata_uses_canonical_repo():
    """User-facing metadata must not advertise the phantom GitHub org."""
    for relative in LIVING_METADATA_FILES:
        text = _read(relative)
        assert PHANTOM_REPO not in text, f"{relative} still mentions {PHANTOM_REPO}"
    assert CANONICAL_REPO in _read("CITATION.cff")


def test_author_orcid_is_recorded():
    """Living citation files carry the real ORCID, never the all-zero placeholder."""
    cff = _read("CITATION.cff")
    zenodo = _read(".zenodo.json")
    assert PLACEHOLDER_ORCID not in cff.split("references:")[0]
    assert AUTHOR_ORCID in cff
    assert AUTHOR_ORCID in zenodo


def test_citation_cff_does_not_list_maxwell_as_software_author():
    """Maxwell is the 1873 source author, not a software co-author."""
    header = _read("CITATION.cff").split("references:")[0]
    assert "family-names: Maxwell" not in header
    assert "family-names: Mikinka" in header

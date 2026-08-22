"""Page catalog: index OCR pages + resolve photos without loading everything twice.

Loads volume JSON once per volume (cached), strips heavy fields, maps page
photos by ``page_NNN.png`` naming convention.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator

from page_verifier import config

# Article markers like "27.]" or "241.]" in Maxwell text
_ARTICLE_RE = re.compile(r"(?<!\d)(\d{1,4})[a-z]?\.\s*\]")


@dataclass
class PageRecord:
    """Lightweight page index entry + lazy content fields."""

    page_id: str
    volume: int
    page_number: int
    confidence: float | None = None
    image_path: str | None = None
    article_numbers: list[int] = field(default_factory=list)
    has_markdown: bool = False
    has_raw: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PageContent:
    """Full content for one page (loaded on demand from cached volume)."""

    page_id: str
    volume: int
    page_number: int
    mathpix_markdown: str
    raw_text: str
    confidence: float | None
    image_path: str | None
    article_numbers: list[int]
    equations: list[Any] = field(default_factory=list)


def page_id_for(volume: int, page_number: int) -> str:
    return f"v{volume}-p{int(page_number):03d}"


def parse_page_id(page_id: str) -> tuple[int, int]:
    m = re.fullmatch(r"v(\d+)-p(\d+)", page_id.strip(), re.I)
    if not m:
        raise ValueError(f"Invalid page_id: {page_id}")
    return int(m.group(1)), int(m.group(2))


def extract_article_numbers(text: str) -> list[int]:
    if not text:
        return []
    found = {int(n) for n in _ARTICLE_RE.findall(text)}
    return sorted(found)


@lru_cache(maxsize=4)
def _load_volume_pages(volume: int) -> dict[int, dict[str, Any]]:
    """Load and slim volume OCR pages into memory (keyed by page_number)."""
    path = config.VOLUME_JSON.get(volume)
    if path is None or not Path(path).exists():
        return {}

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    pages_raw = data.get("pages", data)
    out: dict[int, dict[str, Any]] = {}

    if isinstance(pages_raw, dict):
        items = pages_raw.items()
    elif isinstance(pages_raw, list):
        items = ((str(p.get("page_number", i + 1)), p) for i, p in enumerate(pages_raw))
    else:
        return {}

    for key, page in items:
        if not isinstance(page, dict):
            # chapter-style: key -> text only
            try:
                pn = int(key)
            except (TypeError, ValueError):
                continue
            text = page if isinstance(page, str) else str(page)
            out[pn] = {
                "page_number": pn,
                "raw_text": text,
                "mathpix_markdown": text,
                "confidence_score": None,
                "equations": [],
            }
            continue

        pn = int(page.get("page_number") or key)
        md = page.get("mathpix_markdown") or ""
        raw = page.get("raw_text") or ""
        conf = page.get("confidence_score")
        if conf is None:
            conf = page.get("average_confidence_rate")
        # Drop heavy line_data — not needed for human review UI
        out[pn] = {
            "page_number": pn,
            "raw_text": raw,
            "mathpix_markdown": md,
            "confidence_score": conf,
            "equations": page.get("equations") or [],
        }
    return out


@lru_cache(maxsize=1)
def _image_index() -> dict[tuple[int, int], Path]:
    """Map (volume_hint, page_number) -> image path.

    Volume is inferred from folder names when possible; pages may appear
    under generic folders with only page_NNN.png names.
    """
    index: dict[tuple[int, int], Path] = {}
    # Also keep volume-agnostic fallback: page_number -> path
    by_page: dict[int, Path] = {}

    roots = [r for r in config.IMAGE_SEARCH_ROOTS if r.exists()]
    patterns = ("**/page_*.png", "**/page_*.jpg", "**/page_*.jpeg", "**/page_*.webp")

    for root in roots:
        for pattern in patterns:
            for img in root.glob(pattern):
                m = re.search(r"page[_\-]?(\d+)", img.stem, re.I)
                if not m:
                    continue
                pn = int(m.group(1))
                name_upper = str(img).upper()
                vol_hint: int | None = None
                if "VOLUME_2" in name_upper or "VOL-II" in name_upper or "VOL_II" in name_upper:
                    vol_hint = 2
                elif "VOLUME_1" in name_upper or "VOL-I" in name_upper or "VOL_I" in name_upper:
                    vol_hint = 1
                elif "PART_3" in name_upper or "PART_4" in name_upper or "MAGNETISM" in name_upper:
                    vol_hint = 2
                elif "ELECTROSTATIC" in name_upper or "ELECTROKINEMATIC" in name_upper:
                    vol_hint = 1

                if vol_hint is not None:
                    index.setdefault((vol_hint, pn), img)
                by_page.setdefault(pn, img)

    # Fill missing volume-specific slots from generic map
    for (vol, pn), path in list(index.items()):
        by_page.setdefault(pn, path)

    # Store generic fallbacks under volume 0
    for pn, path in by_page.items():
        index.setdefault((0, pn), path)

    return index


def resolve_image(volume: int, page_number: int) -> Path | None:
    idx = _image_index()
    path = idx.get((volume, page_number)) or idx.get((0, page_number))
    return path if path and path.exists() else None


def build_catalog(volumes: tuple[int, ...] = (1, 2)) -> list[PageRecord]:
    """Build a sorted list of page records for available volumes."""
    records: list[PageRecord] = []
    # Prime image index once
    _ = _image_index()

    for vol in volumes:
        pages = _load_volume_pages(vol)
        for pn in sorted(pages.keys()):
            page = pages[pn]
            md = page.get("mathpix_markdown") or ""
            raw = page.get("raw_text") or ""
            articles = extract_article_numbers(md or raw)
            img = resolve_image(vol, pn)
            conf = page.get("confidence_score")
            try:
                conf_f = float(conf) if conf is not None else None
            except (TypeError, ValueError):
                conf_f = None
            records.append(
                PageRecord(
                    page_id=page_id_for(vol, pn),
                    volume=vol,
                    page_number=pn,
                    confidence=conf_f,
                    image_path=str(img) if img else None,
                    article_numbers=articles,
                    has_markdown=bool(md.strip()),
                    has_raw=bool(raw.strip()),
                )
            )
    return records


def get_page_content(page_id: str) -> PageContent:
    vol, pn = parse_page_id(page_id)
    pages = _load_volume_pages(vol)
    if pn not in pages:
        raise KeyError(f"Page not found in OCR data: {page_id}")
    page = pages[pn]
    md = page.get("mathpix_markdown") or ""
    raw = page.get("raw_text") or ""
    articles = extract_article_numbers(md or raw)
    img = resolve_image(vol, pn)
    conf = page.get("confidence_score")
    try:
        conf_f = float(conf) if conf is not None else None
    except (TypeError, ValueError):
        conf_f = None
    return PageContent(
        page_id=page_id,
        volume=vol,
        page_number=pn,
        mathpix_markdown=md,
        raw_text=raw,
        confidence=conf_f,
        image_path=str(img) if img else None,
        article_numbers=articles,
        equations=page.get("equations") or [],
    )


def iter_catalog(volumes: tuple[int, ...] = (1, 2)) -> Iterator[PageRecord]:
    yield from build_catalog(volumes)


def catalog_stats(records: list[PageRecord]) -> dict[str, Any]:
    with_img = sum(1 for r in records if r.image_path)
    with_md = sum(1 for r in records if r.has_markdown)
    return {
        "total_pages": len(records),
        "with_image": with_img,
        "with_markdown": with_md,
        "volumes": sorted({r.volume for r in records}),
        "missing_images": len(records) - with_img,
    }


@lru_cache(maxsize=1)
def build_article_page_index() -> dict[int, list[str]]:
    """Map treatise article number → page_ids that mention it (from OCR markers)."""
    index: dict[int, list[str]] = {}
    for r in build_catalog((1, 2)):
        for art in r.article_numbers:
            index.setdefault(art, []).append(r.page_id)
    for art in index:
        index[art] = sorted(set(index[art]))
    return index


def pages_for_articles(article_numbers: list[int]) -> list[str]:
    """All page_ids whose OCR text marks any of the given article numbers."""
    idx = build_article_page_index()
    pages: set[str] = set()
    for art in article_numbers:
        pages.update(idx.get(int(art), []))
    return sorted(pages)

"""Yes/No verdict persistence and bulk export."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from page_verifier import config

VerdictValue = Literal["yes", "no", "unset"]


@dataclass
class Verdict:
    page_id: str
    volume: int
    page_number: int
    verdict: VerdictValue = "unset"
    note: str = ""
    article_numbers: list[int] = field(default_factory=list)
    image_path: str | None = None
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Verdict":
        return cls(
            page_id=str(data["page_id"]),
            volume=int(data.get("volume") or 0),
            page_number=int(data.get("page_number") or 0),
            verdict=data.get("verdict") or "unset",  # type: ignore[arg-type]
            note=data.get("note") or "",
            article_numbers=list(data.get("article_numbers") or []),
            image_path=data.get("image_path"),
            updated_at=data.get("updated_at") or "",
        )


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_data_dir() -> Path:
    config.VERDICTS_DIR.mkdir(parents=True, exist_ok=True)
    config.EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    return config.VERDICTS_DIR


def load_verdicts(path: Path | None = None) -> dict[str, Verdict]:
    path = path or config.VERDICTS_PATH
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    items = raw.get("verdicts", raw) if isinstance(raw, dict) else raw
    out: dict[str, Verdict] = {}
    if isinstance(items, dict):
        for pid, v in items.items():
            if isinstance(v, dict):
                v = {**v, "page_id": v.get("page_id", pid)}
                out[pid] = Verdict.from_dict(v)
    elif isinstance(items, list):
        for v in items:
            if isinstance(v, dict) and "page_id" in v:
                out[v["page_id"]] = Verdict.from_dict(v)
    return out


def save_verdicts(verdicts: dict[str, Verdict], path: Path | None = None) -> Path:
    path = path or config.VERDICTS_PATH
    ensure_data_dir()
    payload = {
        "schema_version": 1,
        "product": "MAXWELL-MODERNIZED-PROGRAM",
        "updated_at": _utc_now(),
        "count": len(verdicts),
        "verdicts": {pid: v.to_dict() for pid, v in sorted(verdicts.items())},
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return path


def set_verdict(
    verdicts: dict[str, Verdict],
    *,
    page_id: str,
    volume: int,
    page_number: int,
    verdict: VerdictValue,
    note: str = "",
    article_numbers: list[int] | None = None,
    image_path: str | None = None,
) -> Verdict:
    existing = verdicts.get(page_id)
    v = Verdict(
        page_id=page_id,
        volume=volume,
        page_number=page_number,
        verdict=verdict,
        note=note if note is not None else (existing.note if existing else ""),
        article_numbers=list(article_numbers or (existing.article_numbers if existing else [])),
        image_path=image_path if image_path is not None else (existing.image_path if existing else None),
        updated_at=_utc_now(),
    )
    verdicts[page_id] = v
    save_verdicts(verdicts)
    return v


def verdict_stats(verdicts: dict[str, Verdict], total_pages: int | None = None) -> dict[str, Any]:
    yes = sum(1 for v in verdicts.values() if v.verdict == "yes")
    no = sum(1 for v in verdicts.values() if v.verdict == "no")
    unset_stored = sum(1 for v in verdicts.values() if v.verdict == "unset")
    reviewed = yes + no
    return {
        "stored": len(verdicts),
        "yes": yes,
        "no": no,
        "unset_stored": unset_stored,
        "reviewed": reviewed,
        "total_pages": total_pages,
        "remaining": (total_pages - reviewed) if total_pages is not None else None,
    }


def _product_export_for_articles(article_numbers: list[int]) -> dict[str, Any]:
    """Resolve @maxwell_cite product identity for export (map wrongs → maxwell/)."""
    # Lazy import: avoids circular imports at module load; uses citation index cache.
    from page_verifier.product_view import product_matches_for_articles

    matches = product_matches_for_articles(list(article_numbers or []), limit=80)
    compact = [
        {
            "package": m.package,
            "library": m.library,
            "library_role": m.library_role,
            "module": m.module,
            "function": m.function,
            "qualified_name": m.qualified_name,
            "signature": m.signature,
            "rel_path": m.rel_path,
            "articles": list(m.articles),
            "part": m.part,
            "theory_class": m.theory_class,
        }
        for m in matches
    ]
    libraries = sorted({m["library"] for m in compact})
    return {
        "product_package": "maxwell",
        "match_count": len(compact),
        "libraries": libraries,
        "import_prefixes": [f"maxwell.{lib}" for lib in libraries],
        "qualified_names": [m["qualified_name"] for m in compact],
        "rel_paths": [m["rel_path"] for m in compact],
        "signatures": [m["signature"] for m in compact],
        "product_matches": compact,
    }


def _enriched_verdict_row(v: Verdict) -> dict[str, Any]:
    """Verdict dict plus product function paths for product-consumption export."""
    row = v.to_dict()
    product = _product_export_for_articles(v.article_numbers)
    row["product_package"] = product["product_package"]
    row["match_count"] = product["match_count"]
    row["libraries"] = product["libraries"]
    row["import_prefixes"] = product["import_prefixes"]
    row["qualified_names"] = product["qualified_names"]
    row["rel_paths"] = product["rel_paths"]
    row["signatures"] = product["signatures"]
    row["product_matches"] = product["product_matches"]
    row["right_wrong"] = {"yes": "right", "no": "wrong"}.get(v.verdict, "unset")
    return row


def export_json(
    verdicts: dict[str, Verdict],
    path: Path | None = None,
    *,
    only_reviewed: bool = False,
) -> Path:
    ensure_data_dir()
    path = path or (config.EXPORT_DIR / f"verdicts_export_{_utc_now().replace(':', '')}.json")
    items = list(verdicts.values())
    if only_reviewed:
        items = [v for v in items if v.verdict in ("yes", "no")]
    rows = [
        _enriched_verdict_row(v)
        for v in sorted(items, key=lambda x: (x.volume, x.page_number))
    ]
    payload = {
        "schema_version": 2,
        "export_type": "page_verification_verdicts",
        "exported_at": _utc_now(),
        "description": (
            "Human Yes/No page verification: yes=product math matches page; "
            "no=incorrect/mismatch. page_id format: v{volume}-p{page:03d}. "
            "Each row includes product_matches (package maxwell, library, module, "
            "qualified_name, signature, rel_path) so wrongs map back into maxwell/."
        ),
        "product": {
            "package": "maxwell",
            "definition": (
                "Only @maxwell_cite-tagged functions under maxwell/ for articles "
                "on the page — not OCR, photos, or untagged helpers."
            ),
        },
        "counts": {
            "total_exported": len(rows),
            "yes": sum(1 for v in items if v.verdict == "yes"),
            "no": sum(1 for v in items if v.verdict == "no"),
            "with_product_matches": sum(1 for r in rows if r.get("match_count", 0) > 0),
        },
        "verdicts": rows,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return path


def export_csv(
    verdicts: dict[str, Verdict],
    path: Path | None = None,
    *,
    only_reviewed: bool = False,
) -> Path:
    ensure_data_dir()
    path = path or (config.EXPORT_DIR / f"verdicts_export_{_utc_now().replace(':', '')}.csv")
    items = list(verdicts.values())
    if only_reviewed:
        items = [v for v in items if v.verdict in ("yes", "no")]
    items = sorted(items, key=lambda x: (x.volume, x.page_number))
    fieldnames = [
        "page_id",
        "volume",
        "page_number",
        "verdict",
        "right_wrong",
        "note",
        "article_numbers",
        "product_package",
        "match_count",
        "libraries",
        "import_prefixes",
        "qualified_names",
        "rel_paths",
        "signatures",
        "image_path",
        "updated_at",
    ]
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for v in items:
            row = _enriched_verdict_row(v)
            w.writerow(
                {
                    "page_id": row["page_id"],
                    "volume": row["volume"],
                    "page_number": row["page_number"],
                    "verdict": row["verdict"],
                    "right_wrong": row["right_wrong"],
                    "note": row["note"],
                    "article_numbers": ";".join(str(a) for a in row["article_numbers"]),
                    "product_package": row["product_package"],
                    "match_count": row["match_count"],
                    "libraries": ";".join(row["libraries"]),
                    "import_prefixes": ";".join(row["import_prefixes"]),
                    "qualified_names": ";".join(row["qualified_names"]),
                    "rel_paths": ";".join(row["rel_paths"]),
                    "signatures": " | ".join(row["signatures"]),
                    "image_path": row.get("image_path") or "",
                    "updated_at": row["updated_at"],
                }
            )
    return path

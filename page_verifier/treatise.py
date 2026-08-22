"""Maxwell *Treatise* hierarchy — volumes, parts, chapters, articles.

Ground truth for this project (Third Edition scans + product package):

**One work**
    James Clerk Maxwell, *A Treatise on Electricity and Magnetism*.

**Two printed volumes (books)** — the physical / PDF split used by OCR:

    Volume I  — PDF ``15773-A Treatise On Electricity And Magnetism Vol-i``
                OCR: MAXWELL_VOLUME_1_MASTER_OUTPUT (572 pages)
                Content: Part I + Part II (+ prelim / plates)

    Volume II — PDF ``15774-A Treatise On Electricity And Magnetism Vol-ii``
                OCR: MAXWELL_VOLUME_2_MASTER_OUTPUT (544 pages)
                Content: Part III + Part IV (+ prelim / plates)

**Four main Parts** (Maxwell's own division of the *scientific* content):

    Part I   Electrostatics       Arts. 27–229   → mostly Vol I
    Part II  Electrokinematics    Arts. 230–370  → mostly Vol I
    Part III Magnetism            Arts. 371–474  → mostly Vol II
    Part IV  Electromagnetism     Arts. 475–866  → mostly Vol II

**Chapters** are subdivisions *inside* each Part (many per part). The verifier
does not require chapter IDs; article numbers are the stable join key.

**Not** Maxwell's original four parts:
    Modern project docs labeled PART V / PART VI under maxwell-latex-books are
    *architecture maps* for this modernization, not extra treatise volumes.

Article numbering: the body of the Treatise is numbered continuously across
both volumes. Prelim/TOC/plates pages often have **no** article markers.
"""

from __future__ import annotations

from typing import Any

# Canonical structure used by PRODUCT (maxwell/__init__.py) and OCR join
TREATISE = {
    "work": "A Treatise on Electricity and Magnetism",
    "edition_used": "Third Edition (project scans / Mathpix)",
    "volumes": {
        1: {
            "label": "Volume I",
            "also_called": ["Book 1", "Vol-i", "15773"],
            "pdf": "15773-A Treatise On Electricity And Magnetism Vol-i.pdf",
            "parts": [1, 2],
            "ocr_key": "volume_1_direct_result.json",
        },
        2: {
            "label": "Volume II",
            "also_called": ["Book 2", "Vol-ii", "15774"],
            "pdf": "15774-A Treatise On Electricity And Magnetism Vol-ii.pdf",
            "parts": [3, 4],
            "ocr_key": "volume_2_direct_result.json",
        },
    },
    "parts": {
        1: {
            "roman": "I",
            "title": "Electrostatics",
            "articles": (27, 229),
            "primary_volume": 1,
            "product_libraries": ["electrostatics", "core", "math", "components"],
        },
        2: {
            "roman": "II",
            "title": "Electrokinematics",
            "articles": (230, 370),
            "primary_volume": 1,
            "product_libraries": ["electrokinematics", "circuits", "physics"],
        },
        3: {
            "roman": "III",
            "title": "Magnetism",
            "articles": (371, 474),
            "primary_volume": 2,
            "product_libraries": ["magnetism", "magnetics", "materials", "core"],
        },
        4: {
            "roman": "IV",
            "title": "Electromagnetism",
            "articles": (475, 866),
            "primary_volume": 2,
            "product_libraries": ["electromagnetism", "optics", "molecular", "jax"],
        },
    },
    "notes": [
        "Two volumes + four parts (not four volumes).",
        "Chapters nest under parts; articles are the global sequence.",
        "Product @maxwell_cite part=5/6 is rare modern/supplementary tagging, not treatise books.",
        "Prelim, TOC, and plate pages often lack article markers but are still in the OCR catalog.",
    ],
}


def part_for_article(article: int) -> int | None:
    for p, meta in TREATISE["parts"].items():
        lo, hi = meta["articles"]
        if lo <= article <= hi:
            return int(p)
    return None


def articles_in_part(part: int) -> range:
    meta = TREATISE["parts"][int(part)]
    lo, hi = meta["articles"]
    return range(lo, hi + 1)


def classify_page_parts(article_numbers: list[int]) -> list[int]:
    """Which scientific parts appear on a page (via detected article markers)."""
    parts: set[int] = set()
    for a in article_numbers:
        p = part_for_article(int(a))
        if p is not None:
            parts.add(p)
    return sorted(parts)


def coverage_report(
    records: list[Any],
    articles_with_code: set[int],
    *,
    article_page_index: dict[int, list[str]] | None = None,
) -> dict[str, Any]:
    """Full-content coverage: OCR pages + product cites, by volume and part.

    For Parts III–IV especially, also classify *product* gaps:

    - **class_A_missing_code_has_ocr**: treatise article has OCR page markers but
      no ``@maxwell_cite`` product function — *this* is where III/IV need
      assistance (implement and/or tag code for those articles).
    - **class_B_missing_code_no_ocr**: no product cite *and* no OCR article
      marker — need OCR fix or manual page link.
    - **class_C_has_code_no_ocr**: product has cite but OCR did not detect the
      article on any page — reverse join (function→pages) is weak.
    """
    by_vol: dict[int, list] = {1: [], 2: []}
    for r in records:
        by_vol.setdefault(int(r.volume), []).append(r)

    # article → page_ids (prefer caller-supplied index to avoid recompute)
    if article_page_index is None:
        article_page_index = {}
        for r in records:
            for a in r.article_numbers:
                article_page_index.setdefault(int(a), []).append(r.page_id)
        for a, pids in list(article_page_index.items()):
            article_page_index[a] = sorted(set(pids))

    volumes_out = {}
    for vol, rows in sorted(by_vol.items()):
        arts: set[int] = set()
        for r in rows:
            arts.update(int(a) for a in r.article_numbers)
        # keep only plausible treatise body arts
        body = {a for a in arts if 1 <= a <= 866}
        volumes_out[str(vol)] = {
            "label": TREATISE["volumes"].get(vol, {}).get("label", f"Volume {vol}"),
            "pages": len(rows),
            "with_image": sum(1 for r in rows if r.image_path),
            "with_markdown": sum(1 for r in rows if getattr(r, "has_markdown", False)),
            "pages_with_article_markers": sum(1 for r in rows if r.article_numbers),
            "pages_without_article_markers": sum(1 for r in rows if not r.article_numbers),
            "distinct_article_markers_1_866": len(body),
            "parts": TREATISE["volumes"].get(vol, {}).get("parts", []),
        }

    parts_out = {}
    assistance_focus: dict[str, Any] = {}
    for p, meta in TREATISE["parts"].items():
        lo, hi = meta["articles"]
        span = list(range(lo, hi + 1))
        with_code = [a for a in span if a in articles_with_code]
        missing_code = [a for a in span if a not in articles_with_code]
        class_a = [a for a in missing_code if article_page_index.get(a)]
        class_b = [a for a in missing_code if not article_page_index.get(a)]
        class_c = [a for a in with_code if not article_page_index.get(a)]
        pages = [
            r
            for r in records
            if any(lo <= int(a) <= hi for a in r.article_numbers)
        ]
        needs_help = len(class_a) + len(class_b) + len(class_c) > 0
        topic_hint = {
            1: "Core electrostatics — nearly complete product cites",
            2: "Conduction / networks — product cites complete on span",
            3: (
                "Magnetism — thin gaps in molecular moments, magnetic potential, "
                "induction geometry, and measurement instruments"
            ),
            4: (
                "Electromagnetism — gaps cluster in galvanometer/coil instruments, "
                "telegraphy detail, and late magneto-optics / vortex articles"
            ),
        }.get(int(p), "")
        parts_out[str(p)] = {
            "roman": meta["roman"],
            "title": meta["title"],
            "articles": f"{lo}–{hi}",
            "article_lo": lo,
            "article_hi": hi,
            "primary_volume": meta["primary_volume"],
            "span_count": len(span),
            "product_articles_with_code": len(with_code),
            "product_articles_missing_code": len(missing_code),
            "product_missing_sample": missing_code[:25],
            "product_missing_all": missing_code,
            "gap_class_A_missing_code_has_ocr": class_a,
            "gap_class_B_missing_code_no_ocr": class_b,
            "gap_class_C_has_code_no_ocr_marker": class_c,
            "needs_extra_assistance": needs_help and int(p) in (3, 4),
            "assistance_summary": topic_hint if (int(p) in (3, 4) and needs_help) else "",
            "ocr_pages_with_part_markers": len(pages),
            "ocr_volumes_seen": sorted({int(r.volume) for r in pages}),
            "product_libraries_hint": meta["product_libraries"],
            "class_A_page_map": {str(a): article_page_index.get(a, []) for a in class_a},
        }
        if int(p) in (3, 4):
            assistance_focus[str(p)] = {
                "part": meta["roman"],
                "title": meta["title"],
                "what_is_fine": (
                    f"Volume {meta['primary_volume']} OCR is loaded; "
                    f"{len(with_code)}/{len(span)} articles already have @maxwell_cite code."
                ),
                "what_needs_help": topic_hint,
                "class_A_implement_or_tag": class_a,
                "class_B_ocr_or_manual_link": class_b,
                "class_C_fix_ocr_markers": class_c,
                "meaning": (
                    "III/IV do NOT need extra *volumes*. They need product coverage "
                    "(implement/tag @maxwell_cite) on class A articles, and OCR/marker "
                    "fixes for class B/C so page↔function join works in the verifier."
                ),
            }

    total_pages = len(records)
    return {
        "treatise": TREATISE,
        "summary": {
            "volumes_loaded": sorted(by_vol.keys()),
            "total_ocr_pages": total_pages,
            "both_volumes_present": 1 in by_vol and 2 in by_vol,
            "four_parts_defined": list(TREATISE["parts"].keys()),
            "product_articles_with_any_code": len(articles_with_code),
            "explanation": (
                "Full content = Volume I + Volume II OCR pages (all parts). "
                "Scientific body = Parts I–IV via continuous article numbers. "
                "Prelim/TOC/plate pages have fewer article markers but remain in the catalog."
            ),
            "part_iii_iv_note": (
                "Parts III and IV need *product/OCR-join* assistance on specific "
                "articles (see assistance_focus), not additional treatise volumes."
            ),
        },
        "volumes": volumes_out,
        "parts": parts_out,
        "assistance_focus": assistance_focus,
    }

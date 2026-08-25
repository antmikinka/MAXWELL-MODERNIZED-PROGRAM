#!/usr/bin/env python
"""Build the article ledger: every Maxwell Treatise article -> its citations.

Scans ``maxwell/**/*.py`` for ``@maxwell_cite`` decorators, captures the
full decorator metadata (article numbers, part, chapter, description) plus
the name of the decorated function/class, joins that against the Treatise
chapter structure (imported from ``check_coverage.PARTS``), and writes:

* ``docs/reports/article_ledger.json``  — machine-readable ledger keyed by
  article number (string).
* ``docs/reports/article_ledger_summary.md`` — human summary with totals,
  a per-chapter article-count table, a singleton watchlist (articles with
  exactly one citation, grouped by chapter), and an anomalies section.

Python stdlib only.  Run:  ``python scripts/build_article_ledger.py``
"""
from __future__ import annotations

import ast
import json
import os
import re
import sys
from datetime import date, datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from check_coverage import PARTS  # noqa: E402  (repo-root import)

EXPECTED_TOTAL_ARTICLES = 866
WATCHLIST_RANGE = (667, 866)

DECORATOR_RE = re.compile(r"^[ \t]*@maxwell_cite[ \t]*\(", re.MULTILINE)
DEF_RE = re.compile(r"(?:async\s+)?(?:def|class)\s+([A-Za-z_]\w*)")
ROMAN_CH_RE = re.compile(r"Ch\s+([IVXLC]+)\s*:")


# ── chapter structure ─────────────────────────────────────────────


def build_chapter_index() -> tuple[dict[int, dict], list[tuple[str, str, str, int, int]]]:
    """Map article -> chapter record, and list chapters in Treatise order.

    Returns (article_map, chapters) where each chapter entry is
    (part_name, chapter_id, chapter_title, lo, hi).
    """
    article_map: dict[int, dict] = {}
    chapters: list[tuple[str, str, str, int, int]] = []
    for part_name, info in PARTS.items():
        part_roman = part_name.split(":")[0].split()[1]
        for ch_name, lo, hi in info["chapters"]:
            m = ROMAN_CH_RE.match(ch_name)
            ch_roman = m.group(1) if m else "Prelim"
            chapter_id = f"{part_roman}.{ch_roman}"
            chapters.append((part_name, chapter_id, ch_name, lo, hi))
            for art in range(lo, hi + 1):
                article_map[art] = {
                    "part": part_name,
                    "chapter_id": chapter_id,
                    "chapter_title": ch_name,
                    "range": (lo, hi),
                }
    return article_map, chapters


# ── decorator parsing ─────────────────────────────────────────────


def _extract_call(text: str, open_idx: int) -> tuple[str, int] | None:
    """Return (args_string, close_idx) for the call opening at open_idx.

    Tracks string literals (incl. triple-quoted) and comments so that
    parentheses inside descriptions do not break the balance scan.
    """
    depth = 0
    i = open_idx
    n = len(text)
    in_str: str | None = None
    while i < n:
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == in_str:
                in_str = None
        else:
            if ch in "\"'":
                if text[i : i + 3] == ch * 3:
                    j = text.find(ch * 3, i + 3)
                    if j == -1:
                        return None
                    i = j + 3
                    continue
                in_str = ch
            elif ch == "#":
                j = text.find("\n", i)
                if j == -1:
                    return None
                i = j
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return text[open_idx + 1 : i], i
        i += 1
    return None


def _split_args(args: str) -> list[str]:
    """Split a decorator argument list on top-level commas."""
    parts: list[str] = []
    cur: list[str] = []
    depth = 0
    in_str: str | None = None
    i = 0
    n = len(args)
    while i < n:
        ch = args[i]
        if in_str:
            if ch == "\\":
                cur.append(args[i : i + 2])
                i += 2
                continue
            if ch == in_str:
                in_str = None
            cur.append(ch)
        elif ch in "\"'":
            if args[i : i + 3] == ch * 3:
                j = args.find(ch * 3, i + 3)
                end = j + 3 if j != -1 else n
                cur.append(args[i:end])
                i = end
                continue
            in_str = ch
            cur.append(ch)
        elif ch == "#":
            j = args.find("\n", i)
            i = n if j == -1 else j
            continue
        elif ch in "([{":
            depth += 1
            cur.append(ch)
        elif ch in ")]}":
            depth -= 1
            cur.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
        i += 1
    tail = "".join(cur)
    if tail.strip():
        parts.append(tail)
    return parts


def _literal(value: str) -> object:
    """Best-effort literal evaluation of a keyword-argument value."""
    v = value.strip()
    try:
        return ast.literal_eval(v)
    except (ValueError, SyntaxError):
        m = re.search(r"['\"]((?:[^'\"\\]|\\.)*)['\"]", v)
        return m.group(1) if m else v


def parse_decorator(text: str, open_idx: int) -> dict | None:
    """Parse one @maxwell_cite call; return articles/part/chapter/description."""
    call = _extract_call(text, open_idx)
    if call is None:
        return None
    args_str, close_idx = call

    articles: list[int] = []
    part: int | None = None
    chapter = ""
    description = ""
    keywords_seen = False
    for raw in _split_args(args_str):
        arg = raw.strip()
        if not arg:
            continue
        if not keywords_seen and re.fullmatch(r"\d+", arg):
            articles.append(int(arg))
            continue
        m = re.match(r"([A-Za-z_]\w*)\s*=\s*(.*)$", arg, re.DOTALL)
        if not m:
            continue
        keywords_seen = True
        key, value = m.group(1), m.group(2)
        if key == "part":
            lit = _literal(value)
            part = int(lit) if isinstance(lit, int) else None
        elif key == "chapter":
            chapter = str(_literal(value))
        elif key == "description":
            description = str(_literal(value))
    if not articles:
        return None
    return {
        "articles": articles,
        "part": part,
        "chapter": chapter,
        "description": description,
        "close_idx": close_idx,
    }


def find_decorated_name(text: str, after_idx: int) -> str | None:
    """Name of the def/class decorated, scanning forward from after_idx.

    Skips blank lines, comments and further decorator lines (stacked
    decorators such as @staticmethod / @dataclass).
    """
    for line in text[after_idx:].splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("@"):
            continue
        m = DEF_RE.match(stripped)
        return m.group(1) if m else None
    return None


# ── scan ──────────────────────────────────────────────────────────


def scan_repo(maxwell_dir: str) -> tuple[list[dict], list[dict]]:
    """Collect citation records and scan warnings."""
    records: list[dict] = []
    warnings: list[dict] = []
    for dirpath, _dirs, files in os.walk(maxwell_dir):
        for fname in sorted(files):
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(dirpath, fname)
            relpath = os.path.relpath(fpath, REPO_ROOT).replace(os.sep, "/")
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
            except OSError:
                warnings.append({"file": relpath, "issue": "unreadable"})
                continue
            for m in DECORATOR_RE.finditer(content):
                open_idx = m.end() - 1
                parsed = parse_decorator(content, open_idx)
                if parsed is None:
                    warnings.append({"file": relpath, "issue": "unparseable decorator"})
                    continue
                func_name = find_decorated_name(content, parsed["close_idx"] + 1)
                if func_name is None:
                    warnings.append(
                        {"file": relpath, "issue": "no def/class found after decorator"}
                    )
                for art in parsed["articles"]:
                    records.append(
                        {
                            "article": art,
                            "file": relpath,
                            "function": func_name,
                            "part": parsed["part"],
                            "chapter": parsed["chapter"],
                            "description": parsed["description"],
                        }
                    )
    return records, warnings


# ── ledger assembly ───────────────────────────────────────────────


def build_ledger(
    records: list[dict], article_map: dict[int, dict]
) -> tuple[dict[str, dict], list[dict], list[int]]:
    """Assemble the ledger dict, anomaly list, and unmapped article list."""
    ledger: dict[int, dict] = {}
    anomalies: list[dict] = []
    part_index = {name: i + 1 for i, name in enumerate(PARTS)}

    for rec in records:
        art = rec["article"]
        info = article_map.get(art)
        if info is None:
            anomalies.append(
                {
                    "article": art,
                    "kind": "unmapped",
                    "file": rec["file"],
                    "detail": "article not covered by any PARTS chapter",
                }
            )
        entry = ledger.setdefault(
            art,
            {
                "part": info["part"] if info else "UNMAPPED",
                "chapter_id": info["chapter_id"] if info else "UNMAPPED",
                "chapter_title": info["chapter_title"] if info else "",
                "citations": [],
            },
        )
        entry["citations"].append(
            {
                "file": rec["file"],
                "function": rec["function"] or "<unknown>",
                "description": rec["description"],
            }
        )
        # decorator part= vs PARTS chapter assignment
        if rec["part"] is not None:
            expected_part = part_index.get(info["part"]) if info else None
            if expected_part is not None and rec["part"] != expected_part:
                anomalies.append(
                    {
                        "article": art,
                        "kind": "part-conflict",
                        "file": rec["file"],
                        "detail": (
                            f"decorator part={rec['part']} but PARTS assigns "
                            f"article to Part {'I II III IV V VI'.split()[expected_part - 1]}"
                        ),
                    }
                )

    ledger_out: dict[str, dict] = {}
    for art in sorted(ledger):
        entry = ledger[art]
        cites = sorted(
            entry["citations"], key=lambda c: (c["file"], c["function"], c["description"])
        )
        deduped = [dict(t) for t in {tuple(sorted(c.items())) for c in cites}]
        deduped.sort(key=lambda c: (c["file"], c["function"], c["description"]))
        ledger_out[str(art)] = {
            "part": entry["part"],
            "chapter_id": entry["chapter_id"],
            "chapter_title": entry["chapter_title"],
            "citations": deduped,
            "cite_count": len(deduped),
        }
    unmapped = sorted(a for a in ledger if a not in article_map)
    deduped_anomalies = sorted(
        {tuple(sorted(a.items())) for a in anomalies}, key=lambda t: dict(t)["article"]
    )
    return ledger_out, [dict(t) for t in deduped_anomalies], unmapped


# ── report writing ────────────────────────────────────────────────


def write_summary(
    path: str,
    ledger: dict[str, dict],
    chapters: list[tuple[str, str, str, int, int]],
    anomalies: list[dict],
    warnings: list[dict],
) -> None:
    cited_articles = set(ledger)
    total_citations = sum(e["cite_count"] for e in ledger.values())
    files = {c["file"] for e in ledger.values() for c in e["citations"]}
    singletons = sorted(int(a) for a in ledger if ledger[a]["cite_count"] == 1)
    watch_singletons = [a for a in singletons if WATCHLIST_RANGE[0] <= a <= WATCHLIST_RANGE[1]]

    lines: list[str] = []
    lines.append("# Article Ledger Summary")
    lines.append("")
    lines.append(f"Generated: {date.today().isoformat()} "
                 f"({datetime.now().strftime('%H:%M:%S')})")
    lines.append("Source: `scripts/build_article_ledger.py` scanning "
                 "`maxwell/**/*.py` for `@maxwell_cite` decorators.")
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    lines.append(f"- Articles expected (Treatise, Arts 1-866): **{EXPECTED_TOTAL_ARTICLES}**")
    lines.append(f"- Articles with at least one citation: **{len(ledger)}**")
    lines.append(f"- Coverage: {len(ledger)}/{EXPECTED_TOTAL_ARTICLES} "
                 f"({len(ledger) / EXPECTED_TOTAL_ARTICLES * 100:.1f}%)")
    lines.append(f"- Total citation records: **{total_citations}**")
    lines.append(f"- Distinct files carrying citations: **{len(files)}**")
    lines.append(f"- Singleton articles (cite_count == 1): **{len(singletons)}** "
                 f"(of which {len(watch_singletons)} lie in Arts "
                 f"{WATCHLIST_RANGE[0]}-{WATCHLIST_RANGE[1]})")
    lines.append("")
    lines.append("## Per-Chapter Article Counts")
    lines.append("")
    lines.append("| Part | Chapter | ID | Range | Expected | Cited | Citations |")
    lines.append("|------|---------|----|-------|----------|-------|-----------|")
    for part_name, ch_id, ch_title, lo, hi in chapters:
        expected = hi - lo + 1
        arts_in_ch = [a for a in range(lo, hi + 1) if str(a) in ledger]
        cites_in_ch = sum(ledger[str(a)]["cite_count"] for a in arts_in_ch)
        lines.append(
            f"| {part_name} | {ch_title} | {ch_id} | {lo}-{hi} "
            f"| {expected} | {len(arts_in_ch)} | {cites_in_ch} |"
        )
    lines.append("")
    lines.append("## Singleton Watchlist (cite_count == 1)")
    lines.append("")
    lines.append(f"{len(singletons)} articles have exactly one citation; "
                 f"{len(watch_singletons)} of them fall in the "
                 f"Arts {WATCHLIST_RANGE[0]}-{WATCHLIST_RANGE[1]} watch range.")
    lines.append("")
    by_chapter: dict[str, list[int]] = {}
    for art in singletons:
        by_chapter.setdefault(ledger[str(art)]["chapter_id"], []).append(art)
    # Emit groups in Treatise order (PARTS chapter order), not string order.
    for part_name, ch_id, ch_title, _lo, _hi in chapters:
        if ch_id not in by_chapter:
            continue
        lines.append(f"### {part_name} / {ch_id}: {ch_title}")
        lines.append("")
        for art in by_chapter.pop(ch_id):
            cite = ledger[str(art)]["citations"][0]
            lines.append(f"- Art. {art} — `{cite['file']}` :: `{cite['function']}`")
        lines.append("")
    for ch_id, arts in by_chapter.items():  # any UNMAPPED leftovers
        lines.append(f"### {ch_id}")
        lines.append("")
        for art in arts:
            cite = ledger[str(art)]["citations"][0]
            lines.append(f"- Art. {art} — `{cite['file']}` :: `{cite['function']}`")
        lines.append("")
    lines.append("## Anomalies")
    lines.append("")
    if anomalies:
        for a in sorted(anomalies, key=lambda x: (x["article"], x["kind"])):
            lines.append(f"- Art. {a['article']} [{a['kind']}] `{a['file']}`: {a['detail']}")
    else:
        lines.append("- None detected.")
    lines.append("")
    if warnings:
        lines.append("## Scanner Warnings")
        lines.append("")
        for w in warnings:
            lines.append(f"- `{w['file']}`: {w['issue']}")
        lines.append("")

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def main() -> int:
    maxwell_dir = os.path.join(REPO_ROOT, "maxwell")
    reports_dir = os.path.join(REPO_ROOT, "docs", "reports")
    if not os.path.isdir(maxwell_dir):
        print(f"ERROR: maxwell/ directory not found at {maxwell_dir}")
        return 1
    os.makedirs(reports_dir, exist_ok=True)

    article_map, chapters = build_chapter_index()
    records, warnings = scan_repo(maxwell_dir)
    ledger, anomalies, unmapped = build_ledger(records, article_map)

    json_path = os.path.join(reports_dir, "article_ledger.json")
    with open(json_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)
        f.write("\n")

    md_path = os.path.join(reports_dir, "article_ledger_summary.md")
    write_summary(md_path, ledger, chapters, anomalies, warnings)

    singletons = [a for a in ledger if ledger[a]["cite_count"] == 1]
    watch = [a for a in singletons
             if WATCHLIST_RANGE[0] <= int(a) <= WATCHLIST_RANGE[1]]
    print(f"Article ledger written:")
    print(f"  {os.path.relpath(json_path, REPO_ROOT)}  ({len(ledger)} articles)")
    print(f"  {os.path.relpath(md_path, REPO_ROOT)}")
    print(f"  citations: {sum(e['cite_count'] for e in ledger.values())}, "
          f"singletons: {len(singletons)} ({len(watch)} in "
          f"{WATCHLIST_RANGE[0]}-{WATCHLIST_RANGE[1]}), "
          f"anomalies: {len(anomalies)}, warnings: {len(warnings)}")
    if unmapped:
        print(f"  unmapped articles: {unmapped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Locate **exact** product implementations linked to Maxwell articles on a page.

PRODUCT (what this pane shows)
==============================
The shippable Python package at::

    MAXWELL-MODERNIZED-PROGRAM/maxwell/

This is **not**:
  - the LaTeX books tree (maxwell-latex-books)
  - Mathpix OCR JSON
  - maxwell-em-processor
  - every function in every subpackage blindly

It **is** only functions (and methods) under ``maxwell/`` that are tagged with
``@maxwell_cite(...)`` from ``maxwell.meta.citation``, filtered to the article
numbers detected on the current OCR page (markers like ``27.]``).

There are many libraries *inside* that package (math, calculus, jax,
electrostatics, electromagnetism, verification, …). Each match is labeled with:

  - package root: always ``maxwell``
  - library (top-level subpackage): e.g. ``electrostatics``, ``math``, ``jax``
  - module path: e.g. ``maxwell.electrostatics.force_theory``
  - function name + signature
  - file path relative to product root
  - part / chapter / theory_class / description from the decorator
  - code snippet

So when you verify a page you know *exactly which library and function* claims
to implement the math on that page.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from page_verifier import config

_CITE_RE = re.compile(
    r"@maxwell_cite\s*\((.*?)\)\s*\n(?:async\s+)?def\s+(\w+)",
    re.DOTALL,
)
_ART_NUM_RE = re.compile(r"(?<![\w.])(\d{1,4})(?![\w.])")
_STR_KW = re.compile(
    r'(part|chapter|theory_class|description)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|(\d+))'
)

# Human-readable roles for top-level subpackages under maxwell/
LIBRARY_ROLES: dict[str, str] = {
    "math": "Pure mathematics helpers (vectors, special functions, tensors)",
    "calculus": "Vector calculus / cyclic integrals / potential operators",
    "jax": "JAX-accelerated ports of treatise computations",
    "core": "Core primitives (charge, field, potential, units)",
    "config": "Constants, conventions, equation catalogs",
    "electrostatics": "Part I — Electrostatics implementations",
    "electrokinematics": "Part II — Electrokinematics / circuits / conduction",
    "magnetism": "Part III — Magnetism implementations",
    "magnetics": "Magnetic materials / related helpers",
    "electromagnetism": "Part IV — Electromagnetism (fields, forces, induction, waves)",
    "fields": "Field geometry / field-line utilities",
    "components": "Geometric bodies (spheres, ellipsoids, etc.)",
    "materials": "Material models (dielectrics, permeability, hysteresis)",
    "molecular": "Molecular / microscopic models from the treatise",
    "optics": "Optical / light-related Maxwell results",
    "magneto_optics": "Magneto-optical effects",
    "instruments": "Instrument models (galvanometers, magnetometers, …)",
    "calibration": "Absolute calibration / metrology chains",
    "circuits": "Circuit dynamics",
    "dynamics": "Lagrangian / dynamical formulations",
    "physics": "Cross-cutting physics modules",
    "solvers": "Numerical solvers",
    "verification": "Symbolic / numeric verification (e.g. SymPy checks)",
    "vis": "Visualization helpers (not the math itself)",
    "experiments": "Historical experiment recreations",
    "engineering": "Engineering applications",
    "signal_processing": "Signal / telegraph-related processing",
    "theories": "Theory frameworks",
    "mechanics": "Mechanics bridge modules",
    "geometry": "Geometry helpers",
    "io": "I/O utilities",
    "meta": "Citation / metadata system",
    "vortex_engine": "Molecular vortex engine models",
    "sim": "Simulation harnesses",
    "telecom": "Telegraphy / telecom related",
    "thermodynamics": "Thermal / thermoelectric links",
    "chemistry": "Electrochemistry hooks",
    "kinematics": "Kinematics placeholders",
    "philosophy": "Philosophical notes (not computational math)",
}


@dataclass
class ProductMatch:
    """One concrete product function linked to treatise article(s)."""

    # Identity — what the user needs to see
    package: str  # always "maxwell"
    library: str  # top-level subpackage: electrostatics, math, jax, ...
    library_role: str  # plain-English role of that library
    module: str  # dotted module: maxwell.electrostatics.force_theory
    function: str  # def name
    qualified_name: str  # module.function
    signature: str  # def name(...): line
    rel_path: str  # path under product root
    file: str  # absolute path

    # Citation metadata from @maxwell_cite
    articles: list[int]
    part: int | None
    chapter: str
    theory_class: str
    description: str

    # Display
    docstring_preview: str
    snippet: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _parse_cite_args(arg_src: str) -> tuple[list[int], int | None, str, str, str]:
    """Parse decorator args: articles, part, chapter, theory_class, description."""
    articles: list[int] = []
    part: int | None = None
    chapter = ""
    theory_class = "maxwell_original"
    description = ""

    for tok in arg_src.split(","):
        t = tok.strip()
        if "=" in t:
            break
        if re.fullmatch(r"\d+", t):
            articles.append(int(t))

    for m in _STR_KW.finditer(arg_src):
        key = m.group(1)
        val = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else m.group(4)
        )
        if key == "part" and val is not None:
            try:
                part = int(val)
            except ValueError:
                pass
        elif key == "chapter" and val is not None:
            chapter = val
        elif key == "theory_class" and val is not None:
            theory_class = val
        elif key == "description" and val is not None:
            description = val

    if not articles:
        head = arg_src.split("part=")[0] if "part=" in arg_src else arg_src
        for m in _ART_NUM_RE.finditer(head):
            articles.append(int(m.group(1)))
        articles = sorted(set(articles))
    return articles, part, chapter, theory_class, description


def _module_from_path(py: Path) -> tuple[str, str, str]:
    """Return (package, library, dotted_module) for a file under maxwell/."""
    root = Path(config.PRODUCT_SRC)
    try:
        rel = py.relative_to(root)
    except ValueError:
        return "maxwell", "unknown", py.stem

    parts = list(rel.parts)
    if parts and parts[-1].endswith(".py"):
        parts[-1] = parts[-1][:-3]
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]

    library = parts[0] if parts else "root"
    module = "maxwell." + ".".join(parts) if parts else "maxwell"
    return "maxwell", library, module


def _function_block(source: str, func_name: str, max_lines: int = 50) -> tuple[str, str, str]:
    """Return (signature_line, docstring_preview, full_snippet)."""
    lines = source.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(rf"^(async\s+)?def\s+{re.escape(func_name)}\s*\(", line):
            start = i
            j = i - 1
            while j >= 0 and (lines[j].strip().startswith("@") or not lines[j].strip()):
                start = j
                j -= 1
            break
    if start is None:
        return f"def {func_name}(...)", "", ""

    end = len(lines)
    for k in range(start + 1, len(lines)):
        if re.match(r"^(async\s+)?def\s+|^class\s+", lines[k]):
            end = k
            break
    block = lines[start:end]

    sig = f"def {func_name}(...)"
    for line in block:
        if re.match(rf"^(async\s+)?def\s+{re.escape(func_name)}\s*\(", line):
            # may be multi-line signature
            sig = line.rstrip()
            if not sig.endswith(":") and not sig.endswith(")"):
                # collect continuation lines until ): or ):
                buf = [sig]
                idx = block.index(line) + 1
                while idx < len(block):
                    buf.append(block[idx].rstrip())
                    if ":" in block[idx] and ")" in "".join(buf):
                        break
                    idx += 1
                sig = " ".join(s.strip() for s in buf)
            break

    doc = ""
    # crude docstring first non-empty lines after def
    in_doc = False
    doc_lines: list[str] = []
    for line in block:
        s = line.strip()
        if not in_doc:
            if s.startswith('"""') or s.startswith("'''"):
                in_doc = True
                quote = s[:3]
                rest = s[3:]
                if rest.endswith(quote) and len(rest) >= 3:
                    doc_lines.append(rest[:-3].strip())
                    break
                if rest:
                    doc_lines.append(rest)
                continue
        else:
            if s.endswith('"""') or s.endswith("'''"):
                doc_lines.append(s[:-3].strip())
                break
            doc_lines.append(s)
    doc = " ".join(x for x in doc_lines if x)[:400]

    if len(block) > max_lines:
        block = block[:max_lines] + ["    # ... truncated ..."]
    return sig, doc, "\n".join(block)


@lru_cache(maxsize=1)
def build_citation_index() -> dict[int, list[ProductMatch]]:
    """Map article number -> product matches (scanned from maxwell/ source tree)."""
    root = Path(config.PRODUCT_SRC)
    index: dict[int, list[ProductMatch]] = {}
    if not root.exists():
        return index

    for py in root.rglob("*.py"):
        if "__pycache__" in py.parts:
            continue
        try:
            source = py.read_text(encoding="utf-8")
        except OSError:
            continue
        if "@maxwell_cite" not in source:
            continue

        package, library, module = _module_from_path(py)
        rel = (
            str(py.relative_to(config.PRODUCT_ROOT))
            if py.is_relative_to(config.PRODUCT_ROOT)
            else str(py)
        )
        role = LIBRARY_ROLES.get(
            library,
            f"Subpackage maxwell.{library} (see maxwell package tree)",
        )

        for m in _CITE_RE.finditer(source):
            arg_src, func_name = m.group(1), m.group(2)
            articles, part, chapter, theory_class, description = _parse_cite_args(arg_src)
            if not articles:
                continue
            sig, doc, snippet = _function_block(source, func_name)
            match = ProductMatch(
                package=package,
                library=library,
                library_role=role,
                module=module,
                function=func_name,
                qualified_name=f"{module}.{func_name}",
                signature=sig,
                rel_path=rel.replace("\\", "/"),
                file=str(py),
                articles=articles,
                part=part,
                chapter=chapter,
                theory_class=theory_class,
                description=description,
                docstring_preview=doc,
                snippet=snippet,
            )
            for art in articles:
                index.setdefault(art, []).append(match)
    return index


def product_matches_for_articles(
    article_numbers: list[int],
    limit: int = 40,
    *,
    library_filter: str | None = None,
) -> list[ProductMatch]:
    idx = build_citation_index()
    out: list[ProductMatch] = []
    seen: set[tuple[str, str]] = set()
    for art in article_numbers:
        for match in idx.get(art, []):
            if library_filter and match.library != library_filter:
                continue
            key = (match.rel_path, match.function)
            if key in seen:
                continue
            seen.add(key)
            out.append(match)
            if len(out) >= limit:
                return out
    return out


def product_payload_for_articles(article_numbers: list[int]) -> dict[str, Any]:
    """Structured product pane data for the HTML API (detailed, explicit)."""
    matches = product_matches_for_articles(article_numbers)
    by_library: Counter[str] = Counter(m.library for m in matches)
    return {
        "product_root": str(config.PRODUCT_ROOT),
        "product_package": "maxwell",
        "product_src": str(config.PRODUCT_SRC),
        "product_definition": (
            "The modernized Treatise implementation: Python package "
            "`maxwell/` inside MAXWELL-MODERNIZED-PROGRAM. "
            "Only @maxwell_cite-tagged functions for articles on this page."
        ),
        "not_included": [
            "maxwell-latex-books (source scans / LaTeX)",
            "Mathpix OCR JSON (page text — middle pane)",
            "maxwell_em_processor / maxwell-em-processor (OCR pipeline)",
            "Untagged helpers without @maxwell_cite",
        ],
        "articles_on_page": list(article_numbers),
        "match_count": len(matches),
        "libraries_on_page": [
            {
                "library": lib,
                "count": n,
                "role": LIBRARY_ROLES.get(lib, ""),
                "import_prefix": f"maxwell.{lib}",
            }
            for lib, n in by_library.most_common()
        ],
        "matches": [m.to_dict() for m in matches],
    }


def format_product_view(article_numbers: list[int]) -> str:
    """Human-readable markdown for legacy Streamlit pane (kept for compatibility)."""
    payload = product_payload_for_articles(article_numbers)
    if not article_numbers:
        return (
            "_No article numbers detected on this page "
            "(markers like `27.]`). Browse neighboring pages or search the product source._"
        )
    lines = [
        f"**PRODUCT:** Python package `{payload['product_package']}/` "
        f"at `{payload['product_src']}`",
        "",
        payload["product_definition"],
        "",
        f"**Articles on page:** {', '.join(f'Art. {a}' for a in article_numbers)}",
        "",
    ]
    if not payload["matches"]:
        lines.append(
            "_No `@maxwell_cite` product implementations found for these articles yet._"
        )
        lines.append(f"Searched under `{config.PRODUCT_SRC}`.")
        return "\n".join(lines)

    lines.append("**Libraries hit on this page:**")
    for lib in payload["libraries_on_page"]:
        lines.append(
            f"- `maxwell.{lib['library']}` ({lib['count']} fn) — {lib['role']}"
        )
    lines.append("")
    lines.append(f"**{payload['match_count']} exact function(s):**")
    lines.append("")
    for m in payload["matches"]:
        arts = ", ".join(str(a) for a in m["articles"])
        part = f"Part {m['part']}" if m["part"] is not None else "Part ?"
        lines.append(f"### `{m['qualified_name']}`")
        lines.append(
            f"- **Library:** `maxwell.{m['library']}` — {m['library_role']}"
        )
        lines.append(f"- **Module:** `{m['module']}`")
        lines.append(f"- **File:** `{m['rel_path']}`")
        lines.append(f"- **Function:** `{m['function']}`")
        lines.append(f"- **Signature:** `{m['signature']}`")
        lines.append(f"- **Cite:** {part}, Arts. {arts}, `{m['theory_class']}`")
        if m.get("chapter"):
            lines.append(f"- **Chapter:** {m['chapter']}")
        if m.get("description"):
            lines.append(f"- **Description:** _{m['description']}_")
        lines.append("")
        lines.append("```python")
        lines.append(m["snippet"] or f"# def {m['function']} ...")
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


@lru_cache(maxsize=1)
def build_function_index() -> dict[str, ProductMatch]:
    """Unique product functions keyed by qualified_name (function → articles).

    Inverse of the page-first view: start from a function, get its treatise
    article numbers, then join to OCR pages that contain those articles.
    """
    idx = build_citation_index()
    by_qname: dict[str, ProductMatch] = {}
    for matches in idx.values():
        for m in matches:
            existing = by_qname.get(m.qualified_name)
            if existing is None:
                by_qname[m.qualified_name] = m
            else:
                # merge article lists if the same function was indexed under multiple arts
                arts = sorted(set(existing.articles) | set(m.articles))
                if arts != existing.articles:
                    by_qname[m.qualified_name] = ProductMatch(
                        package=existing.package,
                        library=existing.library,
                        library_role=existing.library_role,
                        module=existing.module,
                        function=existing.function,
                        qualified_name=existing.qualified_name,
                        signature=existing.signature,
                        rel_path=existing.rel_path,
                        file=existing.file,
                        articles=arts,
                        part=existing.part,
                        chapter=existing.chapter,
                        theory_class=existing.theory_class,
                        description=existing.description,
                        docstring_preview=existing.docstring_preview,
                        snippet=existing.snippet,
                    )
    return by_qname


def search_functions(query: str, limit: int = 30) -> list[dict[str, Any]]:
    """Search product functions by name, qualified_name, module, library, or description."""
    q = (query or "").strip().lower()
    if not q:
        return []
    hits: list[tuple[int, ProductMatch]] = []
    for m in build_function_index().values():
        score = 0
        fn = m.function.lower()
        qn = m.qualified_name.lower()
        if q == fn or q == qn:
            score = 100
        elif fn.startswith(q) or qn.endswith("." + q):
            score = 80
        elif q in fn or q in qn:
            score = 60
        elif q in m.module.lower() or q in m.library.lower():
            score = 40
        elif q in (m.description or "").lower() or q in (m.rel_path or "").lower():
            score = 20
        elif q.isdigit() and int(q) in m.articles:
            score = 50
        if score:
            hits.append((score, m))
    hits.sort(key=lambda t: (-t[0], t[1].qualified_name))
    out = []
    for score, m in hits[:limit]:
        d = m.to_dict()
        d["search_score"] = score
        # drop huge snippet in search results for speed
        d.pop("snippet", None)
        out.append(d)
    return out


def resolve_function(query: str) -> ProductMatch | None:
    """Resolve exact qualified_name, or unique bare function name.

    Does **not** pick an arbitrary best search hit when several functions share
    a short name (e.g. three different ``electric_tension``). Use
    ``search_functions`` for disambiguation, or pass a full qualified_name.
    """
    q = (query or "").strip()
    if not q:
        return None
    idx = build_function_index()
    if q in idx:
        return idx[q]
    # case-insensitive full qualified name
    ql = q.lower()
    for qn, m in idx.items():
        if qn.lower() == ql:
            return m
    # bare function name only if unique across the product
    name_hits = [m for m in idx.values() if m.function == q or m.function.lower() == ql]
    if len(name_hits) == 1:
        return name_hits[0]
    return None


def resolve_function_or_candidates(query: str) -> dict[str, Any]:
    """Resolve one function, or return candidates when the name is ambiguous."""
    q = (query or "").strip()
    match = resolve_function(q)
    if match is not None:
        return {"match": match, "ambiguous": False, "candidates": []}
    idx = build_function_index()
    ql = q.lower()
    name_hits = [m for m in idx.values() if m.function == q or m.function.lower() == ql]
    if len(name_hits) > 1:
        return {
            "match": None,
            "ambiguous": True,
            "candidates": [
                {
                    "qualified_name": m.qualified_name,
                    "function": m.function,
                    "library": m.library,
                    "articles": m.articles,
                    "rel_path": m.rel_path,
                }
                for m in sorted(name_hits, key=lambda x: x.qualified_name)
            ],
        }
    hits = search_functions(q, limit=15)
    if len(hits) == 1:
        m = idx.get(hits[0]["qualified_name"])
        return {"match": m, "ambiguous": False, "candidates": []}
    return {
        "match": None,
        "ambiguous": len(hits) > 1,
        "candidates": [
            {
                "qualified_name": h["qualified_name"],
                "function": h["function"],
                "library": h["library"],
                "articles": h["articles"],
                "rel_path": h["rel_path"],
            }
            for h in hits
        ],
    }


def citation_index_stats() -> dict[str, Any]:
    idx = build_citation_index()
    lib_counts: Counter[str] = Counter()
    n_funcs = 0
    seen: set[tuple[str, str]] = set()
    for matches in idx.values():
        for m in matches:
            key = (m.rel_path, m.function)
            if key in seen:
                continue
            seen.add(key)
            n_funcs += 1
            lib_counts[m.library] += 1
    return {
        "articles_with_code": len(idx),
        "total_cite_links": sum(len(v) for v in idx.values()),
        "unique_functions": n_funcs,
        "product_package": "maxwell",
        "product_src": str(config.PRODUCT_SRC),
        "product_root": str(config.PRODUCT_ROOT),
        "libraries": [
            {
                "library": lib,
                "unique_functions": n,
                "role": LIBRARY_ROLES.get(lib, ""),
                "import_prefix": f"maxwell.{lib}",
            }
            for lib, n in lib_counts.most_common()
        ],
    }

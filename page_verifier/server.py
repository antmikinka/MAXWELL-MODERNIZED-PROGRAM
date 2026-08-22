"""Fast HTML/CSS page verifier — stdlib HTTP server (no Streamlit).

Launch:
    python -m page_verifier.server
    python run_page_verifier.py

UI: page_verifier/static/  |  API: /api/*
"""

from __future__ import annotations

import json
import mimetypes
import sys
import traceback
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from page_verifier import config
from page_verifier.catalog import (
    build_article_page_index,
    build_catalog,
    catalog_stats,
    get_page_content,
    pages_for_articles,
)  # build_article_page_index used in coverage
from page_verifier.product_view import (
    build_citation_index,
    citation_index_stats,
    product_payload_for_articles,
    resolve_function_or_candidates,
    search_functions,
)
from page_verifier.treatise import (
    TREATISE,
    classify_page_parts,
    coverage_report,
    part_for_article,
)
from page_verifier.latex_render import (
    latex_status,
    render_page_latex,
)
from page_verifier.verdicts import (
    export_csv,
    export_json,
    load_verdicts,
    set_verdict,
    verdict_stats,
)

STATIC_DIR = Path(__file__).resolve().parent / "static"
HOST = "127.0.0.1"
PORT = 8765

# In-process caches (built once per process)
_CATALOG = None
_CITE_STATS = None
_VERDICTS = None


def _catalog():
    global _CATALOG
    if _CATALOG is None:
        print("[verifier] Building page catalog…", flush=True)
        _CATALOG = build_catalog((1, 2))
        print(f"[verifier] Catalog: {len(_CATALOG)} pages", flush=True)
    return _CATALOG


def _cite_stats():
    global _CITE_STATS
    if _CITE_STATS is None:
        print("[verifier] Indexing @maxwell_cite product functions…", flush=True)
        _CITE_STATS = citation_index_stats()
        print(
            f"[verifier] Product: {_CITE_STATS['unique_functions']} functions, "
            f"{_CITE_STATS['articles_with_code']} articles",
            flush=True,
        )
    return _CITE_STATS


def _verdicts():
    global _VERDICTS
    if _VERDICTS is None:
        _VERDICTS = load_verdicts()
    return _VERDICTS


def _json_response(handler: BaseHTTPRequestHandler, data: Any, status: int = 200) -> None:
    body = json.dumps(data, ensure_ascii=False, default=str).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


def _text_response(
    handler: BaseHTTPRequestHandler,
    body: bytes,
    content_type: str,
    status: int = 200,
    cache: str = "no-store",
) -> None:
    handler.send_response(status)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", cache)
    handler.end_headers()
    handler.wfile.write(body)


def _read_json(handler: BaseHTTPRequestHandler) -> dict:
    length = int(handler.headers.get("Content-Length") or 0)
    raw = handler.rfile.read(length) if length else b"{}"
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def _filter_pages(
    volume: str,
    status: str,
    only_image: bool,
    q: str,
    *,
    articles: list[int] | None = None,
    page_ids: set[str] | None = None,
    part: str | None = None,
    include_no_articles: bool = True,
) -> list[dict[str, Any]]:
    records = _catalog()
    verdicts = _verdicts()
    art_set = set(articles or [])
    part_n: int | None = int(part) if part and part not in ("all", "", "0") else None
    out = []
    for r in records:
        if page_ids is not None and r.page_id not in page_ids:
            continue
        if volume and volume != "all" and str(r.volume) != volume:
            continue
        if only_image and not r.image_path:
            continue
        page_parts = classify_page_parts(r.article_numbers)
        if part_n is not None and part_n not in page_parts:
            # Part filter: only pages with article markers in that scientific part
            continue
        v = verdicts.get(r.page_id)
        verd = v.verdict if v else "unset"
        if status == "unreviewed" and verd in ("yes", "no"):
            continue
        if status == "yes" and verd != "yes":
            continue
        if status == "no" and verd != "no":
            continue
        if art_set and not art_set.intersection(r.article_numbers):
            continue
        if q:
            ql = q.strip().lower()
            ok = (
                ql in r.page_id.lower()
                or (ql.isdigit() and int(ql) == r.page_number)
                or any(ql == str(a) for a in r.article_numbers)
                or (ql in ("prelim", "toc", "plates") and not r.article_numbers)
            )
            if not ok:
                continue
        out.append(
            {
                "page_id": r.page_id,
                "volume": r.volume,
                "page_number": r.page_number,
                "article_numbers": r.article_numbers,
                "parts": page_parts,
                "has_image": bool(r.image_path),
                "has_markdown": r.has_markdown,
                "verdict": verd,
            }
        )
    return out


def _parse_int_list(raw: str) -> list[int]:
    if not raw or not raw.strip():
        return []
    out: list[int] = []
    for part in raw.replace(";", ",").split(","):
        part = part.strip()
        if part.isdigit():
            out.append(int(part))
    return out


class Handler(BaseHTTPRequestHandler):
    server_version = "MaxwellPageVerifier/2.0"

    def log_message(self, fmt: str, *args) -> None:
        # quieter access log
        if args and str(args[0]).startswith('"GET /api/'):
            return
        super().log_message(fmt, *args)

    def do_GET(self) -> None:  # noqa: N802
        try:
            self._dispatch_get()
        except Exception as e:
            traceback.print_exc()
            _json_response(self, {"error": str(e)}, 500)

    def do_POST(self) -> None:  # noqa: N802
        try:
            self._dispatch_post()
        except Exception as e:
            traceback.print_exc()
            _json_response(self, {"error": str(e)}, 500)

    def _dispatch_get(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)

        if path in ("/", "/index.html"):
            return self._serve_static("index.html")
        if path.startswith("/static/"):
            return self._serve_static(path[len("/static/") :])

        if path == "/api/meta":
            records = _catalog()
            stats = catalog_stats(records)
            cites = _cite_stats()
            vstats = verdict_stats(_verdicts(), total_pages=stats["total_pages"])
            art_code = set(build_citation_index().keys())
            cov = coverage_report(
                records,
                art_code,
                article_page_index=build_article_page_index(),
            )
            return _json_response(
                self,
                {
                    "product": {
                        "name": "MAXWELL-MODERNIZED-PROGRAM",
                        "package": "maxwell",
                        "src": str(config.PRODUCT_SRC),
                        "root": str(config.PRODUCT_ROOT),
                        "definition": (
                            "Python package maxwell/ — modernized Treatise math. "
                            "Verifier shows only @maxwell_cite functions for articles on the page."
                        ),
                        "libraries": cites.get("libraries", []),
                        "unique_functions": cites.get("unique_functions"),
                        "articles_with_code": cites.get("articles_with_code"),
                    },
                    "treatise": TREATISE,
                    "coverage": cov,
                    "catalog": stats,
                    "verdicts": vstats,
                    "latex": latex_status(),
                    "paths": {
                        "ocr_root": str(config.OCR_ROOT),
                        "books_root": str(config.BOOKS_ROOT),
                        "verdicts": str(config.VERDICTS_PATH),
                        "exports": str(config.EXPORT_DIR),
                        "volume_json": {str(k): str(v) for k, v in config.VOLUME_JSON.items()},
                    },
                },
            )

        if path == "/api/coverage":
            records = _catalog()
            art_code = set(build_citation_index().keys())
            return _json_response(
                self,
                coverage_report(
                    records,
                    art_code,
                    article_page_index=build_article_page_index(),
                ),
            )

        if path == "/api/pages":
            arts = _parse_int_list(qs.get("articles", [""])[0])
            page_id_raw = qs.get("page_ids", [""])[0].strip()
            page_ids = (
                {p.strip() for p in page_id_raw.replace(";", ",").split(",") if p.strip()}
                if page_id_raw
                else None
            )
            pages = _filter_pages(
                volume=qs.get("volume", ["all"])[0],
                status=qs.get("status", ["all"])[0],
                only_image=qs.get("only_image", ["0"])[0] in ("1", "true", "yes"),
                q=qs.get("q", [""])[0],
                articles=arts or None,
                page_ids=page_ids,
                part=qs.get("part", ["all"])[0],
            )
            return _json_response(
                self,
                {
                    "count": len(pages),
                    "pages": pages,
                    "filter_articles": arts,
                    "filter_part": qs.get("part", ["all"])[0],
                },
            )

        # Search product functions (function-first navigation)
        if path == "/api/functions":
            q = qs.get("q", [""])[0]
            limit = int(qs.get("limit", ["30"])[0] or 30)
            hits = search_functions(q, limit=min(limit, 100))
            return _json_response(self, {"query": q, "count": len(hits), "functions": hits})

        # Function → articles → book pages (the inverse of page → product)
        if path == "/api/function-pages":
            q = qs.get("q", [""])[0] or qs.get("qualified", [""])[0]
            resolved = resolve_function_or_candidates(q)
            match = resolved.get("match")
            if match is None:
                return _json_response(
                    self,
                    {
                        "error": (
                            f"Ambiguous or unknown function: {q!r}"
                            if resolved.get("ambiguous")
                            else f"No @maxwell_cite function matched: {q!r}"
                        ),
                        "ambiguous": bool(resolved.get("ambiguous")),
                        "candidates": resolved.get("candidates") or [],
                        "hint": (
                            "Pick a full qualified_name from candidates "
                            "(several product libraries may share a short name)."
                        ),
                    },
                    404,
                )
            arts = list(match.articles)
            page_ids = pages_for_articles(arts)
            art_index = build_article_page_index()
            pages_detail = _filter_pages(
                volume=qs.get("volume", ["all"])[0],
                status=qs.get("status", ["all"])[0],
                only_image=qs.get("only_image", ["0"])[0] in ("1", "true", "yes"),
                q="",
                page_ids=set(page_ids) if page_ids else set(),
            )
            return _json_response(
                self,
                {
                    "function": match.to_dict()
                    | {"snippet": (match.snippet[:500] if match.snippet else "")},
                    "articles": arts,
                    "pages_per_article": {str(a): art_index.get(a, []) for a in arts},
                    "page_ids": page_ids,
                    "page_count": len(page_ids),
                    "pages": pages_detail,
                    "explanation": (
                        f"Function {match.qualified_name} is tagged @maxwell_cite for "
                        f"Arts. {', '.join(map(str, arts))}. "
                        f"Book pages listed are OCR pages that contain those article markers."
                    ),
                },
            )

        if path.startswith("/api/page/"):
            page_id = urllib.parse.unquote(path[len("/api/page/") :])
            content = get_page_content(page_id)
            v = _verdicts().get(page_id)
            product = product_payload_for_articles(content.article_numbers)
            return _json_response(
                self,
                {
                    "page_id": content.page_id,
                    "volume": content.volume,
                    "page_number": content.page_number,
                    "article_numbers": content.article_numbers,
                    "confidence": content.confidence,
                    "image_path": content.image_path,
                    "has_image": bool(
                        content.image_path and Path(content.image_path).exists()
                    ),
                    "mathpix_markdown": content.mathpix_markdown,
                    "raw_text": content.raw_text,
                    "equations": content.equations[:80],
                    "verdict": v.to_dict() if v else None,
                    "product": product,
                    "latex": {
                        "source_is_latex": True,
                        "render_url": f"/api/latex/{content.page_id}",
                    },
                },
            )

        if path.startswith("/api/latex/"):
            page_id = urllib.parse.unquote(path[len("/api/latex/") :])
            content = get_page_content(page_id)
            source = content.mathpix_markdown or content.raw_text or ""
            result = render_page_latex(content.page_id, source)
            payload = result.to_dict()
            payload["page_id"] = content.page_id
            payload["image_urls"] = [
                f"/api/latex-image/{content.page_id}?i={i}&v={result.cache_key}"
                for i in range(result.page_count)
            ]
            return _json_response(self, payload, 200 if result.ok else 503)

        if path.startswith("/api/latex-image/"):
            page_id = urllib.parse.unquote(path[len("/api/latex-image/") :])
            idx_raw = qs.get("i", ["0"])[0]
            try:
                idx = int(idx_raw)
            except ValueError:
                idx = 0
            content = get_page_content(page_id)
            source = content.mathpix_markdown or content.raw_text or ""
            result = render_page_latex(content.page_id, source)
            if not result.ok or idx < 0 or idx >= len(result.image_paths):
                return _json_response(
                    self,
                    {"error": result.error or "latex image not found", "log_tail": result.log_tail},
                    404,
                )
            img = Path(result.image_paths[idx])
            if not img.exists():
                return _json_response(self, {"error": "latex png missing"}, 404)
            return _text_response(self, img.read_bytes(), "image/png", cache="no-store")

        if path.startswith("/api/image/"):
            page_id = urllib.parse.unquote(path[len("/api/image/") :])
            content = get_page_content(page_id)
            if not content.image_path or not Path(content.image_path).exists():
                return _json_response(self, {"error": "image not found"}, 404)
            img = Path(content.image_path)
            data = img.read_bytes()
            mime = mimetypes.guess_type(str(img))[0] or "image/png"
            return _text_response(self, data, mime, cache="public, max-age=3600")

        _json_response(self, {"error": f"not found: {path}"}, 404)

    def _dispatch_post(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = _read_json(self)

        if path == "/api/verdict":
            page_id = body["page_id"]
            content = get_page_content(page_id)
            v = set_verdict(
                _verdicts(),
                page_id=page_id,
                volume=content.volume,
                page_number=content.page_number,
                verdict=body.get("verdict", "unset"),
                note=body.get("note", ""),
                article_numbers=content.article_numbers,
                image_path=content.image_path,
            )
            return _json_response(self, {"ok": True, "verdict": v.to_dict()})

        if path == "/api/export":
            fmt = (body.get("format") or "json").lower()
            only_reviewed = bool(body.get("only_reviewed", True))
            if fmt == "csv":
                path_out = export_csv(_verdicts(), only_reviewed=only_reviewed)
            else:
                path_out = export_json(_verdicts(), only_reviewed=only_reviewed)
            return _json_response(self, {"ok": True, "path": str(path_out)})

        _json_response(self, {"error": f"not found: {path}"}, 404)

    def _serve_static(self, rel: str) -> None:
        # prevent path traversal
        rel = rel.replace("\\", "/").lstrip("/")
        if ".." in rel.split("/"):
            return _json_response(self, {"error": "bad path"}, 400)
        target = (STATIC_DIR / rel).resolve()
        if not str(target).startswith(str(STATIC_DIR.resolve())):
            return _json_response(self, {"error": "bad path"}, 400)
        if not target.exists() or not target.is_file():
            return _json_response(self, {"error": "static not found"}, 404)
        data = target.read_bytes()
        mime = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        if target.suffix == ".js":
            mime = "application/javascript; charset=utf-8"
        elif target.suffix == ".css":
            mime = "text/css; charset=utf-8"
        elif target.suffix == ".html":
            mime = "text/html; charset=utf-8"
        return _text_response(self, data, mime, cache="no-cache")


def main() -> None:
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    # warm caches in main thread so first browser request is fast
    _catalog()
    _cite_stats()
    _verdicts()
    tex = latex_status()
    if tex["installed"]:
        print(
            f"[verifier] Native LaTeX: {tex['engine']} · {tex['version']} · {tex['path']}",
            flush=True,
        )
    else:
        print(
            "[verifier] Native LaTeX MISSING — pane 2 cannot typeset Mathpix. "
            "Install TinyTeX/MiKTeX so xelatex is on PATH.",
            flush=True,
        )

    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{HOST}:{PORT}/"
    print(f"\nMaxwell Page Verifier (HTML/CSS) → {url}")
    print(f"PRODUCT package: {config.PRODUCT_SRC}")
    print("Ctrl+C to stop.\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        httpd.server_close()


if __name__ == "__main__":
    main()

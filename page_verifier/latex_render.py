"""Native TinyTeX / XeLaTeX rendering for Mathpix OCR (already LaTeX).

The verifier treats ``mathpix_markdown`` as a LaTeX *body*, wraps it in a
document, compiles with the local TeX engine, and rasterizes the PDF.
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from page_verifier import config

# Cache compiled pages next to verdicts so they persist across restarts.
CACHE_DIR = Path(
    os.environ.get(
        "MAXWELL_LATEX_CACHE",
        Path(__file__).resolve().parent / "data" / "latex_cache",
    )
)

PREAMBLE_VERSION = "v7-visible-tags"

_COMMON_TEX_BIN_DIRS = (
    Path(os.environ.get("TINYTEX_ROOT", "")) / "bin" / "windows" if os.environ.get("TINYTEX_ROOT") else None,
    Path.home() / "AppData" / "Roaming" / "TinyTeX" / "bin" / "windows",
    Path.home() / "AppData" / "Local" / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64",
    Path(r"C:\texlive\2026\bin\windows"),
    Path(r"C:\texlive\2025\bin\windows"),
    Path(r"C:\Program Files\MiKTeX\miktex\bin\x64"),
)

_IMG_MD_RE = re.compile(r"!\[([^\]]*)\]\((https?://[^)\s]+)\)")
_INCLUDE_URL_RE = re.compile(
    r"(\\includegraphics(?:\[[^\]]*\])?)\{(https?://[^}]+)\}"
)
_MATH_ENV_RE = re.compile(
    r"\\begin\{([A-Za-z*]+)\}.*?\\end\{\1\}",
    re.DOTALL,
)
_DISPLAY_RE = re.compile(r"\$\$.*?\$\$|\\\[.*?\\\]", re.DOTALL)
_INLINE_RE = re.compile(r"(?<!\$)\$(?!\$)(?:\\.|[^$\\])+\$")
_FOOTNOTE_RE = re.compile(r"\\footnotetext\{", re.DOTALL)
# Mathpix wraps amsmath displays in $$ $$; that kills \tag.
_WRAPPED_AMS_RE = re.compile(
    r"\$\$\s*(\\begin\{((?:equation|align|gather|multline|flalign|alignat)\*?)\}"
    r".*?\\end\{\2\})\s*\$\$",
    re.DOTALL,
)
_DISPLAY_MATH_RE = re.compile(r"\$\$(.*?)\$\$|\\\[(.*?)\\\]", re.DOTALL)

_lock_guard = threading.Lock()
_page_locks: dict[str, threading.Lock] = {}


def _page_lock(key: str) -> threading.Lock:
    with _lock_guard:
        lock = _page_locks.get(key)
        if lock is None:
            lock = threading.Lock()
            _page_locks[key] = lock
        return lock


def _ensure_tex_on_path() -> None:
    """Prepend known TinyTeX / MiKTeX bins if pdflatex is not already on PATH."""
    if shutil.which("xelatex") or shutil.which("pdflatex"):
        return
    parts = os.environ.get("PATH", "").split(os.pathsep)
    for d in _COMMON_TEX_BIN_DIRS:
        if d is None:
            continue
        if (d / "xelatex.exe").exists() or (d / "pdflatex.exe").exists():
            if str(d) not in parts:
                os.environ["PATH"] = str(d) + os.pathsep + os.environ.get("PATH", "")
            return


def find_tex_engine() -> dict[str, str | None]:
    """Locate a real TeX engine. Prefers XeLaTeX (Unicode Mathpix bodies)."""
    _ensure_tex_on_path()
    info: dict[str, str | None] = {
        "engine": None,
        "path": None,
        "family": None,
        "version": None,
    }
    for name, family in (("xelatex", "xetex"), ("lualatex", "luatex"), ("pdflatex", "pdftex")):
        path = shutil.which(name)
        if not path:
            continue
        info["engine"] = name
        info["path"] = path
        info["family"] = family
        try:
            proc = subprocess.run(
                [path, "--version"],
                capture_output=True,
                text=True,
                timeout=8,
                check=False,
            )
            first = (proc.stdout or proc.stderr or "").splitlines()
            info["version"] = first[0].strip() if first else name
        except (OSError, subprocess.TimeoutExpired):
            info["version"] = name
        return info
    return info


def _tex_path(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/")


def _image_cache_dir() -> Path:
    d = CACHE_DIR / "_images"
    d.mkdir(parents=True, exist_ok=True)
    return d


def fetch_remote_image(url: str) -> Path | None:
    """Download a Mathpix CDN image once and keep it next to the TeX cache."""
    url = (url or "").strip()
    if not url.startswith(("http://", "https://")):
        return None
    ext = ".png" if ".png" in url.lower() else ".jpg"
    dest = _image_cache_dir() / (hashlib.sha256(url.encode("utf-8")).hexdigest()[:20] + ext)
    if dest.exists() and dest.stat().st_size > 32:
        return dest
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "MaxwellPageVerifier/1.0", "Accept": "image/*"},
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = resp.read()
    except (urllib.error.URLError, TimeoutError, OSError):
        return None
    if not data:
        return None
    dest.write_bytes(data)
    return dest


def _local_include(url: str) -> str:
    local = fetch_remote_image(url)
    if local is None:
        return r"\par\fbox{\small missing figure}\par"
    return r"\includegraphics[width=\linewidth]{" + _tex_path(local) + "}"


def rewrite_remote_graphics(text: str) -> str:
    """Point \\includegraphics and markdown images at downloaded local files."""

    def inc(match: re.Match[str]) -> str:
        prefix, url = match.group(1), match.group(2)
        local = fetch_remote_image(url)
        if local is None:
            return r"\fbox{\small missing figure}"
        return prefix + "{" + _tex_path(local) + "}"

    text = _INCLUDE_URL_RE.sub(inc, text)

    def md_img(match: re.Match[str]) -> str:
        return r"\par\noindent " + _local_include(match.group(2)) + r"\par"

    return _IMG_MD_RE.sub(md_img, text)


def latex_status() -> dict[str, Any]:
    eng = find_tex_engine()
    return {
        "installed": bool(eng["path"]),
        "engine": eng["engine"],
        "path": eng["path"],
        "family": eng["family"],
        "version": eng["version"],
        "cache_dir": str(CACHE_DIR),
        "preamble": PREAMBLE_VERSION,
        "renderer": "native-tex",
    }


def _stash_math(body: str) -> tuple[str, list[str]]:
    chunks: list[str] = []

    def stash(match: re.Match[str]) -> str:
        chunks.append(match.group(0))
        return f"@@MATH{len(chunks) - 1}@@"

    # Outer display first so inner \begin{aligned} stays inside the $$ chunk.
    text = _DISPLAY_RE.sub(stash, body)
    text = _MATH_ENV_RE.sub(stash, text)
    text = _INLINE_RE.sub(stash, text)
    return text, chunks


def _restore_math(text: str, chunks: list[str]) -> str:
    # Reverse order so an outer $$ chunk that still contains @@MATHN@@
    # is expanded before its inner environments.
    for i in range(len(chunks) - 1, -1, -1):
        text = text.replace(f"@@MATH{i}@@", chunks[i])
    return text


def _balanced_brace_block(text: str, start: int) -> int | None:
    """Return index after matching ``}`` for a ``{`` at *start*, or None."""
    if start >= len(text) or text[start] != "{":
        return None
    depth = 0
    i = start
    while i < len(text):
        ch = text[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return None


def _stash_footnotetext(body: str) -> tuple[str, list[str]]:
    chunks: list[str] = []
    out: list[str] = []
    pos = 0
    for match in _FOOTNOTE_RE.finditer(body):
        brace = match.end() - 1
        end = _balanced_brace_block(body, brace)
        if end is None:
            continue
        out.append(body[pos : match.start()])
        chunks.append(body[match.start() : end])
        out.append(f"@@FN{len(chunks) - 1}@@")
        pos = end
    out.append(body[pos:])
    return "".join(out), chunks


def enable_mathpix_tags(text: str) -> str:
    """Make Mathpix ``\\tag{n}`` actually print.

    Mathpix writes ``$$\\begin{equation*} ... \\tag{1} \\end{equation*}$$``.
    Nested ``$$`` + amsmath display is illegal, so the tag is dropped.
    Raw ``$$ ... \\tag{1} $$`` is also illegal (``\\tag`` is amsmath-only).
    """
    text = _WRAPPED_AMS_RE.sub(r"\1", text)

    def tagged_display(match: re.Match[str]) -> str:
        inner = match.group(1)
        if inner is None:
            inner = match.group(2) or ""
        if "\\tag" not in inner:
            return match.group(0)
        if re.search(r"\\begin\{(?:equation|align|gather|multline)", inner):
            return inner
        return "\\begin{equation*}\n" + inner.strip() + "\n\\end{equation*}"

    return _DISPLAY_MATH_RE.sub(tagged_display, text)


def mathpix_to_tex_body(source: str) -> str:
    """Turn a Mathpix LaTeX/markdown page into a compilable document body."""
    text = (source or "").replace("\r\n", "\n").replace("\r", "\n")
    text = rewrite_remote_graphics(text)
    text = enable_mathpix_tags(text)
    if "\\begin{document}" in text:
        inner = re.search(
            r"\\begin\{document\}(.*)\\end\{document\}",
            text,
            re.DOTALL,
        )
        if inner:
            text = inner.group(1)

    text, fns = _stash_footnotetext(text)
    text, maths = _stash_math(text)

    def heading(match: re.Match[str]) -> str:
        level = len(match.group(1))
        cmd = {1: "section", 2: "subsection", 3: "subsubsection"}.get(level, "paragraph")
        title = match.group(2).strip()
        return f"\\{cmd}*{{{title}}}"

    text = re.sub(r"^(#{1,6})\s+(.+)$", heading, text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)

    # Percent in prose would comment out the rest of the TeX line.
    text = text.replace("%", r"\%")
    text = _restore_math(text, maths)
    for i, chunk in enumerate(fns):
        text = text.replace(f"@@FN{i}@@", chunk)
    return text.strip()


def wrap_tex_document(body: str, *, title: str = "") -> str:
    # Mathpix uses \title/\author as *visible* headings, not \maketitle metadata.
    # \captionsetup comes from caption.sty (often missing in TinyTeX).
    del title  # page identity lives in the UI chrome, not the typeset page
    return r"""\documentclass[11pt]{article}
\usepackage{fontspec}
\usepackage[margin=0.62in,paperwidth=6.35in,paperheight=9.15in]{geometry}
\usepackage{amsmath,amssymb,amsfonts,bm}
\usepackage{graphicx}
\usepackage{xcolor}
\IfFontExistsTF{Times New Roman}{\setmainfont{Times New Roman}}{}
\pagestyle{empty}
\setlength{\parskip}{0.42em}
\setlength{\parindent}{1.15em}
\sloppy
\providecommand{\captionsetup}[2][]{}
\providecommand{\mathscr}{\mathcal}
% Show caption text only (Mathpix already writes "Fig. N.")
\makeatletter
\long\def\@makecaption#1#2{%
  \vskip\abovecaptionskip
  \sbox\@tempboxa{#2}%
  \ifdim\wd\@tempboxa >\hsize #2\par \else \hb@xt@\hsize{\hfil #2\hfil}\fi
  \vskip\belowcaptionskip}
\makeatother
\renewcommand{\title}[1]{%
  \par\begingroup\centering\bfseries\Large #1\par\endgroup\vspace{0.55em}}
\renewcommand{\author}[1]{%
  \par\begingroup\centering\normalsize #1\par\endgroup\vspace{0.35em}}
\renewcommand{\date}[1]{%
  \par\begingroup\centering\small #1\par\endgroup\vspace{0.25em}}
\makeatletter
\renewcommand{\maketag@@@}[1]{\hbox{\m@th\large\normalfont\bfseries#1}}
\makeatother
\begin{document}
""" + body + r"""
\end{document}
"""


def _hash_source(source: str, engine: str) -> str:
    h = hashlib.sha256()
    h.update(PREAMBLE_VERSION.encode("utf-8"))
    h.update(b"\0")
    h.update(engine.encode("utf-8"))
    h.update(b"\0")
    h.update(source.encode("utf-8", errors="replace"))
    return h.hexdigest()[:16]


def _run_tex(engine_path: str, tex_path: Path, out_dir: Path, timeout: int = 45) -> subprocess.CompletedProcess[str]:
    cmd = [
        engine_path,
        "-interaction=nonstopmode",
        "-output-directory",
        str(out_dir),
        tex_path.name,
    ]
    return subprocess.run(
        cmd,
        cwd=str(out_dir),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        encoding="utf-8",
        errors="replace",
    )


def _rasterize_pdf(pdf_path: Path, dest_dir: Path, stem: str, zoom: float = 1.85) -> list[Path]:
    import fitz  # PyMuPDF

    doc = fitz.open(pdf_path)
    written: list[Path] = []
    try:
        matrix = fitz.Matrix(zoom, zoom)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            out = dest_dir / f"{stem}-{i:02d}.png"
            pix.save(str(out))
            written.append(out)
    finally:
        doc.close()
    return written


@dataclass
class LatexRenderResult:
    ok: bool
    engine: str | None
    engine_path: str | None
    cached: bool
    page_count: int
    image_paths: list[str] = field(default_factory=list)
    pdf_path: str | None = None
    log_tail: str = ""
    error: str | None = None
    elapsed_s: float = 0.0
    cache_key: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "engine": self.engine,
            "engine_path": self.engine_path,
            "cached": self.cached,
            "page_count": self.page_count,
            "image_paths": self.image_paths,
            "pdf_path": self.pdf_path,
            "log_tail": self.log_tail,
            "error": self.error,
            "elapsed_s": round(self.elapsed_s, 3),
            "cache_key": self.cache_key,
            "renderer": "native-tex",
        }


def render_latex_source(
    source: str,
    *,
    cache_key: str | None = None,
    title: str = "",
) -> LatexRenderResult:
    """Compile Mathpix/LaTeX *source* and return rasterized page images."""
    t0 = time.perf_counter()
    status = latex_status()
    if not status["installed"] or not status["path"]:
        return LatexRenderResult(
            ok=False,
            engine=None,
            engine_path=None,
            cached=False,
            page_count=0,
            error=(
                "No TeX engine found. Install TinyTeX or MiKTeX and ensure "
                "xelatex/pdflatex is on PATH."
            ),
            elapsed_s=time.perf_counter() - t0,
        )

    engine = str(status["engine"])
    engine_path = str(status["path"])
    body_src = source if (source or "").strip() else r"\textit{(empty page)}"
    digest = _hash_source(body_src + "\n" + title, engine)
    key = cache_key or digest
    work = CACHE_DIR / f"{key}_{digest}"
    lock = _page_lock(str(work))
    with lock:
        existing = sorted(work.glob(f"{key}-*.png")) if work.exists() else []
        pdf_existing = work / "page.pdf"
        if existing and pdf_existing.exists():
            return LatexRenderResult(
                ok=True,
                engine=engine,
                engine_path=engine_path,
                cached=True,
                page_count=len(existing),
                image_paths=[str(p) for p in existing],
                pdf_path=str(pdf_existing),
                cache_key=digest,
                elapsed_s=time.perf_counter() - t0,
            )

        work.mkdir(parents=True, exist_ok=True)
        body = mathpix_to_tex_body(body_src)
        tex = wrap_tex_document(body, title=title)
        tex_path = work / "page.tex"
        tex_path.write_text(tex, encoding="utf-8")

        log_parts: list[str] = []
        try:
            # Two passes so \footnotetext / refs settle when present.
            for _ in range(2):
                proc = _run_tex(engine_path, tex_path, work)
                log_parts.append(proc.stdout or "")
                log_parts.append(proc.stderr or "")
        except subprocess.TimeoutExpired:
            return LatexRenderResult(
                ok=False,
                engine=engine,
                engine_path=engine_path,
                cached=False,
                page_count=0,
                error="TeX compile timed out",
                log_tail="\n".join(log_parts)[-4000:],
                cache_key=digest,
                elapsed_s=time.perf_counter() - t0,
            )
        except OSError as exc:
            return LatexRenderResult(
                ok=False,
                engine=engine,
                engine_path=engine_path,
                cached=False,
                page_count=0,
                error=str(exc),
                cache_key=digest,
                elapsed_s=time.perf_counter() - t0,
            )

        pdf_path = work / "page.pdf"
        log_tail = "\n".join(log_parts)[-5000:]
        if not pdf_path.exists():
            return LatexRenderResult(
                ok=False,
                engine=engine,
                engine_path=engine_path,
                cached=False,
                page_count=0,
                error="TeX produced no PDF",
                log_tail=log_tail,
                cache_key=digest,
                elapsed_s=time.perf_counter() - t0,
            )

        try:
            pngs = _rasterize_pdf(pdf_path, work, key)
        except Exception as exc:  # noqa: BLE001 — rasterizer is optional path
            return LatexRenderResult(
                ok=False,
                engine=engine,
                engine_path=engine_path,
                cached=False,
                page_count=0,
                pdf_path=str(pdf_path),
                error=f"PDF rasterize failed: {exc}",
                log_tail=log_tail,
                cache_key=digest,
                elapsed_s=time.perf_counter() - t0,
            )

        return LatexRenderResult(
            ok=bool(pngs),
            engine=engine,
            engine_path=engine_path,
            cached=False,
            page_count=len(pngs),
            image_paths=[str(p) for p in pngs],
            pdf_path=str(pdf_path),
            log_tail=log_tail if not pngs else log_tail[-1200:],
            error=None if pngs else "No PNG pages written",
            cache_key=digest,
            elapsed_s=time.perf_counter() - t0,
        )


def render_page_latex(page_id: str, source: str) -> LatexRenderResult:
    return render_latex_source(source, cache_key=page_id, title=page_id)

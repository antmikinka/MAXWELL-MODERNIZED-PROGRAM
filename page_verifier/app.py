"""Maxwell page Yes/No verifier — legacy Streamlit UI.

Prefer the fast HTML/CSS app instead:

    python run_page_verifier.py
    # → http://127.0.0.1:8765/

This Streamlit entry remains for compatibility only.
Product pane = exact maxwell.* library/module/function via @maxwell_cite
(see product_view.py and page_verifier/README.md).

Launch Streamlit (slow):
    streamlit run page_verifier/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow `streamlit run page_verifier/app.py` from product root
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

try:
    import streamlit as st
except ImportError:
    print("streamlit is required. Install with: pip install streamlit")
    sys.exit(1)

from page_verifier import config
from page_verifier.catalog import (
    build_catalog,
    catalog_stats,
    get_page_content,
)
from page_verifier.latex_render import latex_status, render_page_latex
from page_verifier.product_view import citation_index_stats, format_product_view
from page_verifier.verdicts import (
    export_csv,
    export_json,
    load_verdicts,
    set_verdict,
    verdict_stats,
)


st.set_page_config(
    page_title="Maxwell Page Verifier",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource(show_spinner="Indexing OCR pages + photos…")
def _cached_catalog():
    return build_catalog((1, 2))


@st.cache_resource(show_spinner="Indexing product @maxwell_cite…")
def _cached_cite_stats():
    return citation_index_stats()


def _load_verdicts_session() -> dict:
    if "verdicts" not in st.session_state:
        st.session_state.verdicts = load_verdicts()
    return st.session_state.verdicts


def _filter_records(records, volume_filter, status_filter, only_with_image, query):
    out = records
    if volume_filter != "all":
        vol = int(volume_filter)
        out = [r for r in out if r.volume == vol]
    if only_with_image:
        out = [r for r in out if r.image_path]
    verdicts = _load_verdicts_session()
    if status_filter == "unreviewed":
        out = [r for r in out if verdicts.get(r.page_id) is None or verdicts[r.page_id].verdict not in ("yes", "no")]
    elif status_filter == "yes":
        out = [r for r in out if verdicts.get(r.page_id) and verdicts[r.page_id].verdict == "yes"]
    elif status_filter == "no":
        out = [r for r in out if verdicts.get(r.page_id) and verdicts[r.page_id].verdict == "no"]
    if query:
        q = query.strip().lower()
        def match(r):
            if q in r.page_id.lower():
                return True
            if q.isdigit() and int(q) == r.page_number:
                return True
            if any(q == str(a) for a in r.article_numbers):
                return True
            return False
        out = [r for r in out if match(r)]
    return out


def main() -> None:
    st.title("Maxwell Page Verifier")
    st.caption(
        "Human Yes/No check: product math ↔ OCR markdown ↔ page photo. "
        "Verdicts survive restart and export to JSON/CSV."
    )

    records = _cached_catalog()
    stats = catalog_stats(records)
    cite_stats = _cached_cite_stats()
    verdicts = _load_verdicts_session()
    vstats = verdict_stats(verdicts, total_pages=stats["total_pages"])

    with st.sidebar:
        st.header("Navigation")
        volume_filter = st.selectbox("Volume", ["all", "1", "2"], index=0)
        status_filter = st.selectbox(
            "Status",
            ["all", "unreviewed", "yes", "no"],
            index=1,
        )
        only_with_image = st.checkbox("Only pages with photo", value=False)
        query = st.text_input("Jump (page # / article / page_id)", "")

        filtered = _filter_records(
            records, volume_filter, status_filter, only_with_image, query
        )

        st.metric("Catalog pages", stats["total_pages"])
        st.metric("With photos", stats["with_image"])
        st.metric("Reviewed (Y/N)", vstats["reviewed"])
        st.metric("Yes / No", f"{vstats['yes']} / {vstats['no']}")
        st.caption(
            f"Product cites: {cite_stats['articles_with_code']} articles, "
            f"{cite_stats['total_cite_links']} links"
        )

        if not filtered:
            st.warning("No pages match filters.")
            page_options = []
        else:
            page_options = [r.page_id for r in filtered]

        # Preserve index across reruns when possible
        if "page_idx" not in st.session_state:
            st.session_state.page_idx = 0
        if page_options:
            if st.session_state.page_idx >= len(page_options):
                st.session_state.page_idx = 0
            # If query uniquely matches, jump
            if query.strip() and len(page_options) == 1:
                st.session_state.page_idx = 0

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("◀ Prev", use_container_width=True) and page_options:
                st.session_state.page_idx = (st.session_state.page_idx - 1) % len(page_options)
        with col_b:
            if st.button("Next ▶", use_container_width=True) and page_options:
                st.session_state.page_idx = (st.session_state.page_idx + 1) % len(page_options)

        if page_options:
            selected = st.selectbox(
                "Page",
                page_options,
                index=min(st.session_state.page_idx, len(page_options) - 1),
                key="page_select",
            )
            # Sync idx with selectbox
            st.session_state.page_idx = page_options.index(selected)
        else:
            selected = None

        st.divider()
        st.subheader("Export")
        only_reviewed = st.checkbox("Export only reviewed", value=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Export JSON", use_container_width=True):
                path = export_json(verdicts, only_reviewed=only_reviewed)
                st.success(f"Wrote {path}")
                st.session_state["last_export"] = str(path)
        with c2:
            if st.button("Export CSV", use_container_width=True):
                path = export_csv(verdicts, only_reviewed=only_reviewed)
                st.success(f"Wrote {path}")
                st.session_state["last_export"] = str(path)
        if st.session_state.get("last_export"):
            st.caption(st.session_state["last_export"])

        st.divider()
        st.caption(f"Verdicts file: `{config.VERDICTS_PATH}`")
        st.caption(f"OCR root: `{config.OCR_ROOT}`")
        st.caption(f"Books root: `{config.BOOKS_ROOT}`")

    if not selected:
        st.info("Adjust filters to select a page.")
        return

    # ── Load current page (single page content) ───────────────────
    try:
        content = get_page_content(selected)
    except KeyError as e:
        st.error(str(e))
        return

    rec = next(r for r in records if r.page_id == selected)
    existing = verdicts.get(selected)

    st.subheader(
        f"Volume {content.volume} · Page {content.page_number} · `{content.page_id}`"
    )
    meta_cols = st.columns(4)
    meta_cols[0].write(
        f"**Articles:** {', '.join(map(str, content.article_numbers)) or '—'}"
    )
    conf = content.confidence
    meta_cols[1].write(f"**OCR confidence:** {conf:.3f}" if conf is not None else "**OCR confidence:** —")
    meta_cols[2].write(
        f"**Photo:** {'yes' if content.image_path else 'missing'}"
    )
    cur_v = existing.verdict if existing else "unset"
    meta_cols[3].write(f"**Verdict:** {cur_v}")

    # ── Three panes ───────────────────────────────────────────────
    left, mid, right = st.columns(3, gap="medium")

    with left:
        st.markdown("#### 1 · Product / math")
        st.markdown(format_product_view(content.article_numbers))

    with mid:
        st.markdown("#### 2 · OCR LaTeX")
        md = content.mathpix_markdown or content.raw_text or ""
        tex = latex_status()
        if tex["installed"]:
            st.caption(f"Native {tex['engine']}: `{tex['path']}`")
        else:
            st.error("No TeX engine on PATH — cannot typeset Mathpix LaTeX.")
        view_mode = st.radio("LaTeX view", ["Typeset", "Source"], horizontal=True, key="md_mode")
        if view_mode == "Typeset":
            result = render_page_latex(content.page_id, md)
            if result.ok:
                for png in result.image_paths:
                    st.image(png, use_container_width=True)
            else:
                st.error(result.error or "TeX compile failed")
                if result.log_tail:
                    st.code(result.log_tail[-2000:], language="text")
        else:
            st.code(md or "(empty)", language="latex")
        if content.equations:
            with st.expander(f"Structured equations ({len(content.equations)})"):
                for eq in content.equations[:50]:
                    st.write(eq)

    with right:
        st.markdown("#### 3 · Page photo")
        if content.image_path and Path(content.image_path).exists():
            st.image(content.image_path, width=420)
            st.caption(content.image_path)
        else:
            st.warning("No local page photo found for this page.")
            st.caption(
                "Expected `page_NNN.png` under maxwell-latex-books Third Edition image folders."
            )

    st.divider()
    st.markdown("### Verdict")
    note_default = existing.note if existing else ""
    note = st.text_area("Notes (optional)", value=note_default, height=80, key=f"note_{selected}")

    b1, b2, b3, b4 = st.columns([1, 1, 1, 3])
    with b1:
        if st.button("✅ Yes (correct)", type="primary", use_container_width=True):
            set_verdict(
                verdicts,
                page_id=selected,
                volume=content.volume,
                page_number=content.page_number,
                verdict="yes",
                note=note,
                article_numbers=content.article_numbers,
                image_path=content.image_path,
            )
            st.session_state.verdicts = verdicts
            # auto-advance
            if page_options:
                st.session_state.page_idx = (st.session_state.page_idx + 1) % len(page_options)
            st.rerun()
    with b2:
        if st.button("❌ No (incorrect)", use_container_width=True):
            set_verdict(
                verdicts,
                page_id=selected,
                volume=content.volume,
                page_number=content.page_number,
                verdict="no",
                note=note,
                article_numbers=content.article_numbers,
                image_path=content.image_path,
            )
            st.session_state.verdicts = verdicts
            if page_options:
                st.session_state.page_idx = (st.session_state.page_idx + 1) % len(page_options)
            st.rerun()
    with b3:
        if st.button("Clear verdict", use_container_width=True):
            set_verdict(
                verdicts,
                page_id=selected,
                volume=content.volume,
                page_number=content.page_number,
                verdict="unset",
                note=note,
                article_numbers=content.article_numbers,
                image_path=content.image_path,
            )
            st.session_state.verdicts = verdicts
            st.rerun()
    with b4:
        if existing and existing.updated_at:
            st.caption(f"Last saved: {existing.updated_at} · file `{config.VERDICTS_PATH.name}`")

    # quiet use of rec for linter-friendly reference
    _ = rec


if __name__ == "__main__":
    main()

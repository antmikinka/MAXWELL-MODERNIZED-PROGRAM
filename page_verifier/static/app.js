/* Maxwell Page Verifier — client (HTML/CSS/JS, no Streamlit) */
(() => {
  "use strict";

  const SNIPPET_COLLAPSE_LINES = 12;

  const state = {
    pages: [],
    index: 0,
    current: null,
    mdMode: "render",
    latexToken: 0,
    meta: null,
    libFilter: null, // null = all libraries; else top-level lib name e.g. "electrostatics"
    // Function → book pages navigation
    functionFilter: null, // { qualified_name, articles, page_ids, explanation }
  };

  const $ = (id) => document.getElementById(id);

  async function api(path, opts) {
    const res = await fetch(path, opts);
    const data = await res.json();
    if (!res.ok) {
      const err = new Error(data.error || res.statusText);
      err.payload = data;
      throw err;
    }
    return data;
  }

  function esc(s) {
    return String(s ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function updateProductPathBar(product) {
    const el = $("product-path-detail");
    if (!el) return;
    if (!product) {
      el.textContent = "Select a page…";
      return;
    }
    const pkg = product.product_package || "maxwell";
    const libs = (product.libraries_on_page || []).map((L) => L.import_prefix || `maxwell.${L.library}`);
    const matches = product.matches || [];
    const arts = (product.articles_on_page || []).join(", ") || "—";
    if (!matches.length) {
      el.innerHTML =
        `<code>${esc(pkg)}</code> · arts [${esc(arts)}] · ` +
        `<span class="pp-warn">no @maxwell_cite for these articles</span>`;
      return;
    }
    const qnames = matches.slice(0, 3).map((m) => m.qualified_name);
    const more = matches.length > 3 ? ` +${matches.length - 3} more` : "";
    const libStr = libs.length ? libs.map((x) => `<code>${esc(x)}</code>`).join(" ") : "—";
    el.innerHTML =
      `<code>${esc(pkg)}</code> · libs ${libStr} · ` +
      `${matches.length} fn · arts [${esc(arts)}] · ` +
      qnames.map((q) => `<code class="pp-qn">${esc(q)}</code>`).join(" ") +
      (more ? `<span class="muted">${esc(more)}</span>` : "");
  }

  async function loadMeta() {
    const meta = await api("/api/meta");
    state.meta = meta;
    const p = meta.product;
    $("product-def").innerHTML =
      `<strong>${esc(p.name)}</strong> · package <code>${esc(p.package)}</code><br>` +
      `${esc(p.definition)}<br>` +
      `<code>${esc(p.src)}</code>`;

    const libs = (p.libraries || []).slice(0, 20);
    $("product-libs").innerHTML = libs
      .map(
        (L) =>
          `<div class="lib-row"><code>maxwell.${esc(L.library)}</code>` +
          `<span>${L.unique_functions} fn</span></div>`
      )
      .join("");

    // Treatise: 2 volumes × 4 parts — full content map
    const cov = meta.coverage || {};
    const sum = cov.summary || {};
    const tmap = $("treatise-map");
    if (tmap) {
      tmap.innerHTML =
        `<b>2 volumes</b> (printed books) + <b>4 parts</b> (scientific) · ` +
        `not four volumes.<br>` +
        `OCR loaded: Vol ${esc((sum.volumes_loaded || []).join(" + "))} · ` +
        `<b>${sum.total_ocr_pages || "?"} pages</b> · ` +
        `both volumes: <b>${sum.both_volumes_present ? "yes" : "NO — GAP"}</b>`;
    }
    const box = $("coverage-box");
    if (box && cov.parts) {
      let html = "";
      for (const [pk, part] of Object.entries(cov.parts)) {
        const miss = part.product_articles_missing_code || 0;
        const ok = part.product_articles_with_code || 0;
        const span = part.span_count || 0;
        const help = part.needs_extra_assistance
          ? ` · <span class="pp-warn">needs assistance</span>`
          : "";
        html +=
          `<div class="cov-row">` +
          `<button type="button" class="chip-btn" data-part-jump="${esc(pk)}">` +
          `Part ${esc(part.roman)} · ${esc(part.title)}</button>` +
          `<span class="muted">Arts ${esc(part.articles)} · Vol ${part.primary_volume} · ` +
          `OCR pgs ${part.ocr_pages_with_part_markers} · product ${ok}/${span}` +
          (miss ? ` · <span class="pp-warn">${miss} arts no code</span>` : "") +
          help +
          `</span></div>`;
      }
      // Parts III/IV assistance focus — what the gaps actually mean
      const focus = cov.assistance_focus || {};
      if (Object.keys(focus).length) {
        html += `<div class="assist-box">`;
        html += `<div class="assist-title">Parts III–IV — what “extra help” means</div>`;
        html += `<p class="hint">Not missing volumes. Product/OCR-join gaps on specific articles:</p>`;
        for (const [pk, af] of Object.entries(focus)) {
          const a = (af.class_A_implement_or_tag || []).join(", ") || "—";
          const b = (af.class_B_ocr_or_manual_link || []).join(", ") || "—";
          const c = (af.class_C_fix_ocr_markers || []).join(", ") || "—";
          html +=
            `<div class="assist-part">` +
            `<b>Part ${esc(af.part)} · ${esc(af.title)}</b><br>` +
            `<span class="muted">${esc(af.what_is_fine || "")}</span><br>` +
            `<span>${esc(af.what_needs_help || "")}</span><br>` +
            `<span class="pp-warn">A — no @maxwell_cite but OCR pages exist (implement/tag):</span> ` +
            `<code class="assist-arts" data-arts-jump="${esc(a)}">${esc(a)}</code><br>` +
            `<span class="pp-warn">B — no code and no OCR marker:</span> <code>${esc(b)}</code><br>` +
            `<span class="muted">C — has code but no OCR marker (join weak):</span> <code>${esc(c)}</code>` +
            `</div>`;
        }
        html += `</div>`;
      }
      if (cov.volumes) {
        html += `<div class="cov-vol muted">`;
        for (const [vk, vol] of Object.entries(cov.volumes)) {
          html += `Vol ${esc(vk)}: ${vol.pages} pgs (${vol.pages_without_article_markers} prelim/no-art) · `;
        }
        html += `</div>`;
      }
      box.innerHTML = html;
      box.querySelectorAll("[data-part-jump]").forEach((btn) => {
        btn.onclick = () => {
          $("f-part").value = btn.getAttribute("data-part-jump");
          $("f-status").value = "all";
          loadPages();
        };
      });
      box.querySelectorAll("[data-arts-jump]").forEach((el) => {
        el.style.cursor = "pointer";
        el.title = "Jump to first article’s pages";
        el.onclick = async () => {
          const raw = el.getAttribute("data-arts-jump") || "";
          const first = raw.split(",")[0].trim();
          if (!first || first === "—") return;
          $("f-status").value = "all";
          $("f-part").value = "all";
          $("f-q").value = first;
          state.functionFilter = null;
          await loadPages();
        };
      });
    }

    const lx = meta.latex || {};
    const lxBit = lx.installed
      ? ` · TeX ${lx.engine}`
      : " · TeX MISSING";
    $("top-stats").textContent =
      `${meta.catalog.total_pages} pages (Vol1+2) · ` +
      `${meta.catalog.with_image} photos · ` +
      `Y/N ${meta.verdicts.yes}/${meta.verdicts.no} · ` +
      `product ${p.unique_functions} fn · 4 parts` +
      lxBit;
  }

  function updateFnStatus() {
    const el = $("fn-status");
    const clearBtn = $("btn-fn-clear");
    if (!el) return;
    if (!state.functionFilter) {
      el.textContent = "";
      if (clearBtn) clearBtn.hidden = true;
      return;
    }
    const f = state.functionFilter;
    el.innerHTML =
      `Filtering to <code>${esc(f.qualified_name)}</code> · Arts. ` +
      `${esc((f.articles || []).join(", "))} · ${f.page_ids.length} page(s)`;
    if (clearBtn) clearBtn.hidden = false;
  }

  async function loadPages(opts) {
    opts = opts || {};
    const qs = new URLSearchParams({
      volume: $("f-volume").value,
      status: $("f-status").value,
      only_image: $("f-image").checked ? "1" : "0",
      q: $("f-q").value.trim(),
      part: ($("f-part") && $("f-part").value) || "all",
    });
    if (state.functionFilter && state.functionFilter.page_ids.length) {
      qs.set("page_ids", state.functionFilter.page_ids.join(","));
    } else if (state.functionFilter && state.functionFilter.articles.length) {
      qs.set("articles", state.functionFilter.articles.join(","));
    }
    const data = await api("/api/pages?" + qs.toString());
    state.pages = data.pages || [];
    $("page-count").textContent = `(${state.pages.length})`;
    updateFnStatus();
    const sel = $("page-select");
    sel.innerHTML = "";
    for (const p of state.pages) {
      const opt = document.createElement("option");
      opt.value = p.page_id;
      const mark =
        p.verdict === "yes" ? "✓" : p.verdict === "no" ? "✗" : "·";
      const parts =
        p.parts && p.parts.length ? ` P${p.parts.join("/")}` : "";
      opt.textContent = `${mark} ${p.page_id}${parts} arts[${(p.article_numbers || []).join(",")}]`;
      sel.appendChild(opt);
    }
    if (state.pages.length) {
      if (opts.preferPageId) {
        const idx = state.pages.findIndex((p) => p.page_id === opts.preferPageId);
        state.index = idx >= 0 ? idx : 0;
      } else if (state.index >= state.pages.length) {
        state.index = 0;
      }
      sel.selectedIndex = state.index;
      await loadPage(state.pages[state.index].page_id);
    } else {
      $("page-bar").textContent = state.functionFilter
        ? "No book pages found for this function’s articles (OCR may lack markers)."
        : "No pages match filters.";
      $("product-pane").textContent = "—";
      $("ocr-pane").textContent = "—";
      $("photo-pane").textContent = "—";
      updateProductPathBar(null);
    }
  }

  async function goToFunctionPages(query) {
    const q = (query || "").trim();
    if (!q) return;
    $("fn-status").textContent = "Looking up function → articles → pages…";
    try {
      const data = await api(
        "/api/function-pages?" +
          new URLSearchParams({
            q,
            volume: $("f-volume").value,
            status: "all", // show all statuses when hunting math
            only_image: $("f-image").checked ? "1" : "0",
          }).toString()
      );
      // Prefer "all" status so we don't hide reviewed pages for this hunt
      $("f-status").value = "all";
      state.functionFilter = {
        qualified_name: data.function.qualified_name,
        articles: data.articles || [],
        page_ids: data.page_ids || [],
        explanation: data.explanation || "",
        function: data.function,
      };
      $("fn-results").innerHTML = "";
      $("f-fn").value = data.function.qualified_name;
      state.index = 0;
      await loadPages();
      if (!data.page_count) {
        $("fn-status").textContent =
          data.explanation +
          " — no OCR pages currently mark those articles.";
      }
    } catch (err) {
      // Ambiguous short names (e.g. electric_tension in core + electrostatics + jax)
      $("fn-status").textContent = err.message + " — pick a full name below.";
      const cands = err.payload && err.payload.candidates;
      if (cands && cands.length) {
        $("fn-results").innerHTML = cands
          .map((f) => {
            const arts = (f.articles || []).join(", ");
            return (
              `<button type="button" class="fn-hit" data-fn-go="${esc(f.qualified_name)}">` +
              `<code>${esc(f.qualified_name)}</code>` +
              `<span class="muted">Arts. ${esc(arts)} · maxwell.${esc(f.library)}</span>` +
              `</button>`
            );
          })
          .join("");
      } else {
        await searchFunctionsList(q);
      }
    }
  }

  async function searchFunctionsList(query) {
    const q = (query || "").trim();
    const box = $("fn-results");
    if (!q) {
      box.innerHTML = "";
      return;
    }
    try {
      const data = await api(
        "/api/functions?" + new URLSearchParams({ q, limit: "20" }).toString()
      );
      if (!data.functions.length) {
        box.innerHTML = `<p class="hint">No functions match <code>${esc(q)}</code></p>`;
        return;
      }
      box.innerHTML = data.functions
        .map((f) => {
          const arts = (f.articles || []).join(", ");
          return (
            `<button type="button" class="fn-hit" data-fn-go="${esc(f.qualified_name)}">` +
            `<code>${esc(f.qualified_name)}</code>` +
            `<span class="muted">Arts. ${esc(arts)} · maxwell.${esc(f.library)}</span>` +
            `</button>`
          );
        })
        .join("");
    } catch (err) {
      box.innerHTML = `<p class="hint">${esc(err.message)}</p>`;
    }
  }

  function clearFunctionFilter() {
    state.functionFilter = null;
    $("f-fn").value = "";
    $("fn-results").innerHTML = "";
    updateFnStatus();
    loadPages();
  }

  function snippetBlock(snippet) {
    const text = snippet || "";
    const lines = text.split("\n");
    const long = lines.length > SNIPPET_COLLAPSE_LINES;
    const cls = long ? "snippet collapsed" : "snippet";
    let html = `<pre class="${cls}">${esc(text)}</pre>`;
    if (long) {
      html +=
        `<button type="button" class="btn tiny snippet-toggle" data-snippet-toggle="1">` +
        `Show full snippet (${lines.length} lines)</button>`;
    }
    return html;
  }

  function renderProduct(product) {
    if (!product) {
      $("product-pane").innerHTML = "<p class='muted'>No product payload.</p>";
      updateProductPathBar(null);
      return;
    }
    updateProductPathBar(product);

    const arts = (product.articles_on_page || []).map((a) => `Art. ${a}`).join(", ") || "—";
    const allMatches = product.matches || [];
    const filtered = state.libFilter
      ? allMatches.filter((m) => m.library === state.libFilter)
      : allMatches;

    let html = `<div class="product-summary">
      <div><b>PRODUCT package:</b> <code>${esc(product.product_package)}</code>
        @ <code>${esc(product.product_src)}</code></div>
      <div>${esc(product.product_definition)}</div>
      <div><b>Articles on this page:</b> ${esc(arts)}</div>
      <div><b>Matches:</b> ${product.match_count} function(s) across
        ${(product.libraries_on_page || []).length} library(ies)
        ${state.libFilter ? ` · showing <code>maxwell.${esc(state.libFilter)}</code> (${filtered.length})` : ""}</div>`;
    if (product.libraries_on_page && product.libraries_on_page.length) {
      html += "<ul>";
      for (const L of product.libraries_on_page) {
        html += `<li><code>${esc(L.import_prefix)}</code> — ${L.count} · ${esc(L.role)}</li>`;
      }
      html += "</ul>";
    }
    if (product.not_included) {
      html += `<div class="muted" style="margin-top:0.35rem"><b>Not this pane:</b> ${esc(
        product.not_included.join(" · ")
      )}</div>`;
    }
    html += "</div>";

    // Library filter chips — critical when multiple math libs hit one page
    if (product.libraries_on_page && product.libraries_on_page.length) {
      html += `<div class="lib-filter" role="group" aria-label="Filter by product library">`;
      html += `<span class="lib-filter-label">Libraries on page:</span>`;
      const allActive = !state.libFilter ? " active" : "";
      html += `<button type="button" class="chip-btn${allActive}" data-lib-filter="">All (${allMatches.length})</button>`;
      for (const L of product.libraries_on_page) {
        const active = state.libFilter === L.library ? " active" : "";
        html +=
          `<button type="button" class="chip-btn${active}" data-lib-filter="${esc(L.library)}">` +
          `<code>maxwell.${esc(L.library)}</code> (${L.count})</button>`;
      }
      html += `</div>`;
    }

    if (!allMatches.length) {
      const artList = (product.articles_on_page || []).map((a) => String(a)).join(", ") || "none";
      html +=
        `<div class="empty-product">` +
        `<p><b>No <code>@maxwell_cite</code> product code</b> for articles on this page ` +
        `(${esc(artList)}).</p>` +
        `<p class="muted">Searched package <code>maxwell/</code> only. ` +
        `OCR and photos are not product. Untagged helpers are not listed.</p>` +
        `</div>`;
      $("product-pane").innerHTML = html;
      return;
    }

    if (!filtered.length) {
      html +=
        `<p class="muted">No matches in library <code>maxwell.${esc(state.libFilter)}</code>. ` +
        `Choose <b>All</b> or another library chip.</p>`;
      $("product-pane").innerHTML = html;
      return;
    }

    for (const m of filtered) {
      const artsJoined = (m.articles || []).join(",");
      html += `<article class="match" data-library="${esc(m.library)}">
        <h3>${esc(m.qualified_name)}</h3>
        <div class="chips">
          <span class="chip lib">lib: maxwell.${esc(m.library)}</span>
          <span class="chip part">Part ${m.part ?? "?"}</span>
          <span class="chip art">Arts. ${esc((m.articles || []).join(", "))}</span>
          <span class="chip theory">${esc(m.theory_class || "")}</span>
        </div>
        <div class="match-actions">
          <button type="button" class="btn tiny yes" data-fn-go="${esc(m.qualified_name)}"
            title="Filter page list to book pages for Arts. ${esc((m.articles || []).join(", "))}">
            → Book pages for this function
          </button>
          <button type="button" class="btn tiny secondary" data-arts-filter="${esc(artsJoined)}"
            title="Filter by article numbers only">
            → Pages for Arts. ${esc((m.articles || []).join(", ") || "—")}
          </button>
        </div>
        <div class="meta">
          <div><b>Package:</b> <code>${esc(m.package || "maxwell")}</code></div>
          <div><b>Library:</b> <code>maxwell.${esc(m.library)}</code> — ${esc(m.library_role)}</div>
          <div><b>Module:</b> <code>${esc(m.module)}</code></div>
          <div><b>File:</b> <code>${esc(m.rel_path)}</code></div>
          <div><b>Function:</b> <code>${esc(m.function)}</code></div>
          <div><b>Signature:</b> <code>${esc(m.signature)}</code></div>
          ${m.chapter ? `<div><b>Chapter:</b> ${esc(m.chapter)}</div>` : ""}
          ${m.description ? `<div><b>Description:</b> ${esc(m.description)}</div>` : ""}
          ${m.docstring_preview ? `<div><b>Doc:</b> ${esc(m.docstring_preview)}</div>` : ""}
        </div>
        ${snippetBlock(m.snippet)}
      </article>`;
    }
    $("product-pane").innerHTML = html;
  }

  function setLatexStatus(text) {
    const el = $("latex-status");
    if (el) el.textContent = text;
  }

  async function renderOcr(page) {
    const md = page.mathpix_markdown || page.raw_text || "";
    if (state.mdMode === "raw") {
      setLatexStatus("Mathpix LaTeX source");
      $("ocr-pane").innerHTML = `<pre class="ocr-raw">${esc(md || "(empty)")}</pre>`;
      return;
    }
    const token = ++state.latexToken;
    setLatexStatus("Typesetting with local TeX engine…");
    $("ocr-pane").innerHTML = `<p class="muted">Compiling Mathpix LaTeX with native XeLaTeX/pdfLaTeX…</p>`;
    try {
      const res = await fetch("/api/latex/" + encodeURIComponent(page.page_id));
      const data = await res.json();
      if (token !== state.latexToken || state.mdMode === "raw") return;
      if (!data.ok || !(data.image_urls || []).length) {
        setLatexStatus("TeX failed · " + (data.engine || "no engine"));
        $("ocr-pane").innerHTML =
          `<div class="latex-error"><p><b>Native LaTeX did not produce pages.</b> ` +
          `${esc(data.error || res.statusText)}</p>` +
          (data.log_tail ? `<pre>${esc(data.log_tail.slice(-1800))}</pre>` : "") +
          `</div>`;
        return;
      }
      const cached = data.cached ? "cached" : `${data.elapsed_s}s`;
      setLatexStatus(
        `Native ${esc(data.engine || "TeX")} · ${data.page_count} page(s) · ${cached}`
      );
      $("ocr-pane").innerHTML =
        `<div class="latex-pages">` +
        data.image_urls
          .map(
            (u, i) =>
              `<img src="${esc(u)}" alt="typeset LaTeX page ${i + 1}" />`
          )
          .join("") +
        `</div>`;
    } catch (err) {
      if (token !== state.latexToken) return;
      setLatexStatus("TeX request failed");
      $("ocr-pane").innerHTML = `<div class="latex-error">${esc(err.message)}</div>`;
    }
  }

  function renderPhoto(page) {
    $("photo-caption").textContent = page.image_path || "no image";
    if (page.has_image) {
      $("photo-pane").innerHTML =
        `<img class="page-photo" src="/api/image/${encodeURIComponent(page.page_id)}" alt="page photo" />`;
    } else {
      $("photo-pane").innerHTML =
        `<p class="muted" style="color:#ccc;padding:1rem">No local page photo for this page.</p>`;
    }
  }

  async function loadPage(pageId) {
    const page = await api("/api/page/" + encodeURIComponent(pageId));
    state.current = page;
    state.libFilter = null; // reset library chip on page flip
    const arts = (page.article_numbers || []).join(", ") || "—";
    const verd = page.verdict ? page.verdict.verdict : "unset";
    const libs = (page.product && page.product.libraries_on_page) || [];
    const libHint = libs.length
      ? libs.map((L) => `maxwell.${L.library}`).join(", ")
      : "no @maxwell_cite";
    $("page-bar").innerHTML =
      `<b>Vol ${page.volume}</b> · Page <b>${page.page_number}</b> · ` +
      `<code>${esc(page.page_id)}</code> · Articles: <b>${esc(arts)}</b> · ` +
      `Verdict: <b>${esc(verd)}</b> · ` +
      `<span class="page-bar-libs">PRODUCT: <code>maxwell</code> → ${esc(libHint)}</span>` +
      (page.confidence != null
        ? ` · OCR conf ${Number(page.confidence).toFixed(3)}`
        : "");

    $("note").value = page.verdict ? page.verdict.note || "" : "";
    $("verdict-status").textContent = page.verdict?.updated_at
      ? `Last saved ${page.verdict.updated_at}`
      : "";

    renderProduct(page.product);
    renderOcr(page);
    renderPhoto(page);

    // sync select
    const sel = $("page-select");
    const idx = state.pages.findIndex((p) => p.page_id === pageId);
    if (idx >= 0) {
      state.index = idx;
      sel.selectedIndex = idx;
    }
  }

  async function saveVerdict(verdict) {
    if (!state.current) return;
    const data = await api("/api/verdict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        page_id: state.current.page_id,
        verdict,
        note: $("note").value,
      }),
    });
    $("verdict-status").textContent = `Saved ${data.verdict.verdict} · ${data.verdict.updated_at}`;
    // update list marker
    if (state.pages[state.index]) {
      state.pages[state.index].verdict = data.verdict.verdict;
      const opt = $("page-select").options[state.index];
      if (opt) {
        const p = state.pages[state.index];
        const mark =
          p.verdict === "yes" ? "✓" : p.verdict === "no" ? "✗" : "·";
        const parts =
          p.parts && p.parts.length ? ` P${p.parts.join("/")}` : "";
        opt.textContent = `${mark} ${p.page_id}${parts} arts[${(p.article_numbers || []).join(",")}]`;
      }
    }
    if (verdict === "yes" || verdict === "no") {
      // auto-advance
      if (state.index < state.pages.length - 1) {
        state.index += 1;
        await loadPage(state.pages[state.index].page_id);
      }
    }
  }

  async function doExport(fmt) {
    const data = await api("/api/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        format: fmt,
        only_reviewed: $("export-reviewed").checked,
      }),
    });
    $("export-msg").textContent = "Wrote " + data.path;
  }

  function wire() {
    $("btn-apply").onclick = () => loadPages();
    $("f-q").addEventListener("keydown", (e) => {
      if (e.key === "Enter") loadPages();
    });
    $("btn-fn-go").onclick = () => goToFunctionPages($("f-fn").value);
    $("btn-fn-clear").onclick = () => clearFunctionFilter();
    $("f-fn").addEventListener("keydown", (e) => {
      if (e.key === "Enter") goToFunctionPages($("f-fn").value);
    });
    let fnTimer = null;
    $("f-fn").addEventListener("input", () => {
      clearTimeout(fnTimer);
      fnTimer = setTimeout(() => searchFunctionsList($("f-fn").value), 250);
    });
    $("fn-results").addEventListener("click", (e) => {
      const hit = e.target.closest("[data-fn-go]");
      if (hit) goToFunctionPages(hit.getAttribute("data-fn-go"));
    });
    $("btn-prev").onclick = async () => {
      if (!state.pages.length) return;
      state.index = (state.index - 1 + state.pages.length) % state.pages.length;
      await loadPage(state.pages[state.index].page_id);
    };
    $("btn-next").onclick = async () => {
      if (!state.pages.length) return;
      state.index = (state.index + 1) % state.pages.length;
      await loadPage(state.pages[state.index].page_id);
    };
    $("page-select").onchange = async (e) => {
      const id = e.target.value;
      state.index = state.pages.findIndex((p) => p.page_id === id);
      await loadPage(id);
    };
    $("btn-yes").onclick = () => saveVerdict("yes");
    $("btn-no").onclick = () => saveVerdict("no");
    $("btn-clear").onclick = () => saveVerdict("unset");
    $("btn-export-json").onclick = () => doExport("json");
    $("btn-export-csv").onclick = () => doExport("csv");

    // Library filter chips + snippet expand + function→pages (event delegation)
    $("product-pane").addEventListener("click", (e) => {
      const fnGo = e.target.closest("[data-fn-go]");
      if (fnGo) {
        goToFunctionPages(fnGo.getAttribute("data-fn-go"));
        return;
      }
      const artsBtn = e.target.closest("[data-arts-filter]");
      if (artsBtn) {
        const raw = artsBtn.getAttribute("data-arts-filter") || "";
        const articles = raw.split(",").map((x) => parseInt(x, 10)).filter((n) => !isNaN(n));
        state.functionFilter = {
          qualified_name: "(articles only)",
          articles,
          page_ids: [],
          explanation: "Filtered by article numbers on product match",
        };
        $("f-status").value = "all";
        state.index = 0;
        loadPages();
        return;
      }
      const chip = e.target.closest("[data-lib-filter]");
      if (chip) {
        const lib = chip.getAttribute("data-lib-filter") || "";
        state.libFilter = lib || null;
        if (state.current) renderProduct(state.current.product);
        return;
      }
      const toggle = e.target.closest("[data-snippet-toggle]");
      if (toggle) {
        const pre = toggle.previousElementSibling;
        if (pre && pre.classList.contains("snippet")) {
          pre.classList.toggle("collapsed");
          const isCollapsed = pre.classList.contains("collapsed");
          const n = (pre.textContent || "").split("\n").length;
          toggle.textContent = isCollapsed
            ? `Show full snippet (${n} lines)`
            : "Collapse snippet";
        }
      }
    });

    document.querySelectorAll("[data-md]").forEach((btn) => {
      btn.onclick = () => {
        document.querySelectorAll("[data-md]").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        state.mdMode = btn.getAttribute("data-md");
        if (state.current) renderOcr(state.current);
      };
    });

    document.addEventListener("keydown", (e) => {
      if (e.target.matches("textarea, input, select")) return;
      if (e.key === "y" || e.key === "Y") saveVerdict("yes");
      if (e.key === "n" || e.key === "N") saveVerdict("no");
      if (e.key === "ArrowRight" || e.key === "j" || e.key === "J") $("btn-next").click();
      if (e.key === "ArrowLeft" || e.key === "k" || e.key === "K") $("btn-prev").click();
      if (e.key === "Escape") {
        if (state.libFilter) {
          state.libFilter = null;
          if (state.current) renderProduct(state.current.product);
        } else if (state.functionFilter) {
          clearFunctionFilter();
        }
      }
    });
  }

  async function boot() {
    wire();
    try {
      await loadMeta();
      await loadPages();
    } catch (err) {
      $("top-stats").textContent = "Error: " + err.message;
      console.error(err);
    }
  }

  boot();
})();

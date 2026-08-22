# Maxwell Page Verifier (Yes/No) — HTML/CSS

Fast local app for human verification of the **product** math against OCR and page photos.

## Treatise structure (what “all content” means)

Maxwell’s work is **one treatise**, not four separate books of equal rank:

| Layer | Count | Labels in this project |
|-------|-------|------------------------|
| **Work** | 1 | *A Treatise on Electricity and Magnetism* (Third Edition scans) |
| **Volumes (printed books)** | **2** | **Vol I** (PDF 15773) · **Vol II** (PDF 15774) |
| **Parts (scientific)** | **4** | **I** Electrostatics · **II** Electrokinematics · **III** Magnetism · **IV** Electromagnetism |
| **Chapters** | many | Nested under each Part |
| **Articles** | continuous ~27–866 | Global numbering across both volumes |

| Part | Title | Articles | Primary volume |
|------|-------|----------|----------------|
| I | Electrostatics | 27–229 | Vol I |
| II | Electrokinematics | 230–370 | Vol I |
| III | Magnetism | 371–474 | Vol II |
| IV | Electromagnetism | 475–866 | Vol II |

OCR sources (both must load for full coverage):

- `maxwell_em_processor/MAXWELL_VOLUME_1_MASTER_OUTPUT/volume_1_direct_result.json` (~572 pages)
- `maxwell_em_processor/MAXWELL_VOLUME_2_MASTER_OUTPUT/volume_2_direct_result.json` (~544 pages)

**Total catalog ≈ 1116 pages.** Prelim / TOC / plates often have **no** article markers but remain in the list.

Modern docs named “PART V / PART VI” under `maxwell-latex-books` are **project architecture maps**, not extra Maxwell volumes.

Filter in the UI: **Volume (book)** and **Part (scientific)**. Coverage panel shows OCR pages + product `@maxwell_cite` density per part.

## What “PRODUCT” means (exact)

**PRODUCT** = the Python package:

```
MAXWELL-MODERNIZED-PROGRAM/maxwell/
```

That package has **many libraries** (subpackages), for example:

| Library import | Role |
|----------------|------|
| `maxwell.electrostatics` | Part I electrostatics |
| `maxwell.electrokinematics` | Part II conduction / networks |
| `maxwell.magnetism` | Part III magnetism |
| `maxwell.electromagnetism` | Part IV EM (largest) |
| `maxwell.math` | Pure math helpers |
| `maxwell.calculus` | Vector calculus |
| `maxwell.jax` | JAX-accelerated ports |
| `maxwell.verification` | SymPy / symbolic checks |
| `maxwell.core` | Charge, field, potential primitives |
| `maxwell.config` | Constants / equation catalogs |
| … | (full tree under `maxwell/`) |

The product pane does **not** dump all libraries. For each page it shows **only**
functions tagged with `@maxwell_cite(...)` (from `maxwell.meta.citation`) whose
article numbers match markers on that OCR page (e.g. `27.]`).

Each match card shows:

- **Library** — e.g. `maxwell.electrostatics` + plain-English role  
- **Module** — e.g. `maxwell.electrostatics.force_theory`  
- **File** — e.g. `maxwell/electrostatics/force_theory.py`  
- **Function + signature** — exact `def` name  
- **Qualified name** — `module.function`  
- **Part / Arts / theory_class / chapter / description** from the decorator  
- **Code snippet**

### Not product (other panes / other trees)

| Asset | Role in verifier |
|-------|------------------|
| Mathpix OCR JSON (`maxwell_em_processor`) | Middle pane — already LaTeX, compiled natively |
| Page photos (`maxwell-latex-books` Third Edition) | Right pane — scan image |
| LaTeX books source | Not loaded as code |
| Untagged helpers without `@maxwell_cite` | Not listed |

## Launch (no Streamlit)

From product root:

```bash
python run_page_verifier.py
# or
python -m page_verifier.server
```

Open **http://127.0.0.1:8765/**

stdlib HTTP server. Pane 2 typesets Mathpix OCR as real LaTeX via the local
TinyTeX/MiKTeX engine (`xelatex` preferred) and rasterizes the PDF.

## Workflow

### Page-first (default)
1. Filter volume / unreviewed / photo in the left sidebar.  
2. Compare three panes: **exact product functions**, OCR markdown, photo.  
3. **Yes** / **No** (or keys `Y` / `N`); optional note; auto-advances on Yes/No.  
4. Export JSON or CSV from the sidebar.

### Function-first (go to book pages for a product function)
The math lives in product functions tagged with treatise **article** numbers.
OCR pages mark those articles (e.g. `27.]`). The join is:

```text
product function  →  @maxwell_cite articles  →  OCR/book pages with those markers
```

1. Sidebar **Go to function → book pages**: type e.g. `electric_tension` or
   `maxwell.electrostatics.force_theory.electric_tension`.
2. Click **Find book pages** (or pick a search hit). Page list filters to those pages.
3. On any product match card: **→ Book pages for this function**.
4. **Clear function filter** (or Esc) returns to the full catalog.

API:

- `GET /api/functions?q=electric_tension` — search product functions  
- `GET /api/function-pages?q=electric_tension` — function + articles + page_ids  
- `GET /api/pages?articles=27,28` or `?page_ids=v1-p067,...`

## Data paths

| Asset | Default |
|-------|---------|
| Product code | `./maxwell/` |
| OCR volumes | `C:\Users\antmi\Downloads\maxwell_em_processor\MAXWELL_VOLUME_*_MASTER_OUTPUT\volume_*_direct_result.json` |
| Photos | `C:\Users\antmi\maxwell-latex-books\Third Edition\**\page_NNN.png` |
| Verdicts | `page_verifier/data/verdicts.json` |
| Exports | `page_verifier/data/exports/` |

Env overrides: `MAXWELL_PRODUCT_ROOT`, `MAXWELL_OCR_ROOT`, `MAXWELL_BOOKS_ROOT`, `MAXWELL_VERDICTS_DIR`.

## Module layout

| File | Role |
|------|------|
| `server.py` | Fast stdlib HTTP API + static host |
| `static/` | HTML/CSS/JS UI |
| `catalog.py` | OCR index + photos + lazy page content |
| `product_view.py` | Detailed `@maxwell_cite` → library/module/function |
| `verdicts.py` | Persist + export |
| `config.py` | Paths |
| `app.py` | Legacy Streamlit UI (optional; prefer `server.py`) |

## API (for debugging)

- `GET /api/meta` — product libraries + catalog stats  
- `GET /api/pages?volume=&status=&q=` — page list  
- `GET /api/page/{page_id}` — full page + **detailed product matches**  
- `GET /api/image/{page_id}` — page photo  
- `POST /api/verdict` — `{page_id, verdict, note}`  
- `POST /api/export` — `{format: json|csv, only_reviewed}`  

## Export schema (v2) — map wrongs into `maxwell/`

JSON (`schema_version: 2`) and CSV include product identity per page so a **No**
verdict points at the exact code to fix:

| Field | Meaning |
|-------|---------|
| `product_package` | Always `maxwell` |
| `match_count` | Number of `@maxwell_cite` hits for page articles |
| `libraries` / `import_prefixes` | e.g. `electrostatics` / `maxwell.electrostatics` |
| `qualified_names` | e.g. `maxwell.electrostatics.force_theory.foo` |
| `rel_paths` | File under product root, e.g. `maxwell/electrostatics/force_theory.py` |
| `signatures` | `def name(...):` lines |
| `product_matches` (JSON only) | Full objects: package, library, module, function, qualified_name, signature, rel_path, articles, part |

CSV flattens list fields with `;` (signatures with ` | `).

## License

- Application code in this directory (`*.py`, `static/` HTML/CSS/JS) is licensed under the [MIT License](../LICENSE).
- `data/` holds generated cache and local verdicts, not a curated scholarly dataset. See [data/README.md](data/README.md).
- Treatise page photos and OCR text used by this tool, where they reproduce Maxwell 1873, remain public domain.

## Smoke check

```bash
python -c "from page_verifier.product_view import product_payload_for_articles, citation_index_stats; print(citation_index_stats()['libraries'][:5]); p=product_payload_for_articles([27]); print(p['match_count'], p['matches'][0]['qualified_name'] if p['matches'] else None)"

python -c "from page_verifier.verdicts import load_verdicts, export_json, export_csv; from page_verifier import config; v=load_verdicts(); r=export_json(v, only_reviewed=False); c=export_csv(v, only_reviewed=False); print(r); print(c)"
```

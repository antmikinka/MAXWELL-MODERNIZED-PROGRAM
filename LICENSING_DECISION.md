# Licensing Decision Document — Maxwell Modernized

> **Status:** Adopted (corrected Option C)
> **Date:** 2026-08-18
> **Scope:** All materials in the MAXWELL-MODERNIZED-PROGRAM repository
> **Prepared by:** Security & licensing audit pipeline
> **Implemented:** 2026-08-18 — MIT software + CC BY 4.0 scholarly content + public-domain Treatise text. The original draft inventory below was corrected before implementation (see §5.1 and §11).

---

## 1. Project Context

**Maxwell Modernized** is a computational implementation of James Clerk Maxwell's
1873 *A Treatise on Electricity and Magnetism* — all 866 articles, modernized in
Python with CGS-EMU units, citation-traceable to the original text.

The repository contains **three fundamentally different types of material**:

| Type | Examples | Volume |
|------|----------|--------|
| **Executable software** | Python library (`maxwell/`), JAX adapters, SymPy verifiers, test suite, CI/CD, page-verifier code | ~200+ modules, 1683 tests |
| **Scholarly content** | JOSS paper, architecture maps (Parts I–VI), documentation, strategic roadmaps, API references | ~30+ documents |
| **Public domain source material** | Maxwell's original 1873 Treatise text (excerpts, OCR extractions, page mappings) | Scattered across docs and data |

**This is the core of the licensing dilemma:** these three types of material are
governed by different legal frameworks, community expectations, and tooling
requirements. A single license cannot optimally serve all three.

---

## 2. The Dilemma

### 2.1 Why CC BY 4.0 Feels Right

The project is a **scholarly modernization** of a 19th-century scientific classic.
CC BY 4.0 strongly emphasizes **attribution**, which fits a project that:

- Takes a public domain masterwork and makes it computationally usable
- Produces interpretive documents (architecture maps, article-to-function mappings)
- Builds a JOSS-style academic paper
- Wants credit to flow back when others cite the modernization analysis

It *feels culturally appropriate* for "taking a 19th-century classic and making
it usable today."

### 2.2 Why CC BY 4.0 Alone Is Wrong for the Code

CC BY 4.0 is a **content license, not a software license**. Using it as the primary
license on a Python library creates several practical problems:

| Problem | Impact |
|---------|--------|
| **Not OSI-approved** | JOSS requires an OSI-approved license for the software component. CC BY 4.0 would cause rejection. |
| **Wrong community instrument** | PyPI and scientific-Python tooling expect a conventional software SPDX id (`MIT`, `Apache-2.0`, `BSD-3-Clause`). `CC-BY-4.0` *is* a valid SPDX identifier, but it is a content license, not the license this library should declare. |
| **Patent silence** | CC licenses do not grant patents. MIT is also silent on patents; Apache-2.0 is the license with an explicit grant. Patent language is not the reason to reject CC BY on this code — JOSS/OSI and software-license norms are. |
| **Source/binary distinction** | CC licenses don't distinguish between source code and compiled/binary forms — a distinction that software licenses are built around. |
| **Tooling friction** | Dependency scanners (Snyk, Dependabot, FOSSA), SBOM generators, and institutional compliance teams parse MIT/Apache/BSD. CC BY on code triggers warnings or false positives. |
| **Community expectations** | Scientific Python developers expect MIT, Apache 2.0, or BSD. CC BY on a library invites confusion and unnecessary friction. |

### 2.3 Why MIT Alone Is Insufficient

MIT is the correct license for the **code**, but applying it to everything
undersells the scholarly content:

| Problem | Impact |
|---------|--------|
| **No attribution requirement on content** | MIT requires preserving the copyright notice, but it doesn't carry the same attribution culture as CC BY for scholarly documents. |
| **JOSS paper licensing** | JOSS papers are typically CC BY 4.0. A paper under MIT is unusual and may confuse reviewers. |
| **Documentation reuse** | Researchers who want to cite or adapt the architecture maps and analysis documents benefit from CC BY's clear attribution terms. |
| **Data licensing** | Page mappings, article-to-function tables, and the equation registry are *data*, not code. MIT doesn't address database rights (relevant under EU sui generis database law). |

### 2.4 The Public Domain Complication

Maxwell died in 1879. The Treatise text is **public domain worldwide**. This means:

- **No one can claim copyright** over Maxwell's original words
- **OCR extractions** of the raw text are arguably mechanical reproductions (thin or no copyright)
- **However**, the user's *annotations, corrections, modernized commentary, article-to-function mappings, and registry structure* **are new creative works** with their own copyright
- The license must clearly distinguish between "Maxwell's PD text" and "our new creative layer"

---

## 3. Why This Matters Now

| Trigger | Relevance |
|---------|-----------|
| **JOSS submission planned** | JOSS requires OSI-approved software license + clear paper license. Split licensing is effectively mandatory. |
| **PyPI publication** | `pip install maxwell` reads the license from `pyproject.toml`. Must be a valid software SPDX identifier. |
| **Repo going public** | Once public, the license is the first thing contributors and users see. Getting it right before publication avoids confusing history. |
| **Security audit complete** | The repo has been hardened (no secrets, no PII). Licensing is the last governance item before publication. |

---

## 4. The Three Options

### Option A: MIT Everything (Status Quo)

> One MIT license covers all code, content, and data.

| Pros | Cons |
|------|------|
| Simple — one license file | Wrong tool for scholarly content |
| PyPI-compatible | JOSS paper under MIT is unusual |
| No changes needed | Doesn't distinguish PD source material |
| Well-understood by developers | Undersells attribution for documentation |

**Verdict:** Works for a pure code repo. Suboptimal for a project with significant
scholarly content and a JOSS paper.

---

### Option B: CC BY 4.0 Everything

> One CC BY 4.0 license covers all code, content, and data.

| Pros | Cons |
|------|------|
| Culturally fits a modernization project | **Not OSI-approved** — JOSS will reject |
| Strong attribution culture | **Not a software license** — patent ambiguity |
| Single license file | PyPI tooling friction |
| | Dependency scanner false positives |
| | Community confusion |

**Verdict:** Understandable from a scholarly perspective, but **breaks JOSS and PyPI**.
Not viable as the sole license.

---

### Option C: Split Licensing (MIT + CC BY 4.0) — RECOMMENDED

> MIT for all executable software. CC BY 4.0 for all content, documentation, and data.

| Pros | Cons |
|------|------|
| Correct license for each material type | Two license files to maintain |
| JOSS-compatible (OSI-approved code license) | Slightly more complex to explain |
| PyPI-compatible (MIT in pyproject.toml) | Need per-directory license notes |
| CC BY for scholarly content | |
| Clear PD attribution for Maxwell's text | |
| Follows precedent (Astropy, scikit-learn, etc.) | |

**Verdict:** The professional, correct approach for a project that is both software
and scholarship. This is the recommended option.

---

### Decision Matrix

| Criterion | Option A (MIT only) | Option B (CC BY only) | Option C (Split) |
|-----------|:-------------------:|:---------------------:|:----------------:|
| JOSS compatible | ⚠️ Partial | ❌ No | ✅ Yes |
| PyPI compatible | ✅ Yes | ❌ No | ✅ Yes |
| Correct for code | ✅ Yes | ❌ No | ✅ Yes |
| Correct for content | ⚠️ Weak | ✅ Yes | ✅ Yes |
| Correct for data | ⚠️ Weak | ✅ Yes | ✅ Yes |
| PD source handling | ❌ None | ⚠️ Unclear | ✅ Explicit |
| Community expectations | ✅ Met | ❌ Confusing | ✅ Met |
| Tooling compatibility | ✅ Full | ❌ Issues | ✅ Full |
| Simplicity | ✅ Simple | ✅ Simple | ⚠️ Moderate |
| **Overall** | **6/10** | **3/10** | **9/10** |

---

## 5. Recommended Approach: Split Licensing (Option C)

### 5.1 Complete File-by-File Mapping (corrected at adoption)

Do **not** execute the first draft of this table. The adopted inventory is below.

#### MIT License — Software and project operations

| Path | Description |
|------|-------------|
| `maxwell/**` | Entire Python library — core physics, JAX adapters, SymPy verifiers, including `maxwell/jax/*.md` |
| `tests/**` | Full test suite, including `tests/test_quality_review_plan.md` |
| `page_verifier/*.py` | Application code (`app.py`, `catalog.py`, `config.py`, `latex_render.py`, `product_view.py`, `server.py`, `treatise.py`, `verdicts.py`) |
| `page_verifier/static/**` | HTML/CSS/JS — this is software, not scholarly content |
| `page_verifier/README.md` | Tool documentation shipped with the application |
| `scripts/**` | Helper and utility scripts |
| `examples/**` | Example calculation scripts |
| `notebooks/**` | Jupyter notebooks (executable code) |
| `agents/**` | Agent definitions, prompts, and templates — operational software artifacts |
| `*.py` (root) | `api_client.py`, `article_extractor.py`, `check_coverage.py`, `code_generator.py`, `main.py`, `prompts.py`, `run_page_verifier.py`, `run_verification.py`, `state.py`, `validate_math.py` |
| `*.sh`, `*.bat` (root) | `run_quality_checks.sh`, `run_quality_checks.bat` |
| `.github/workflows/**` | CI/CD pipeline definitions |
| `pyproject.toml` | Package configuration (`license = "MIT"`) |
| `MANIFEST.in` | Package manifest |
| `requirements.txt` | Dependency specification |
| `CONTRIBUTING.md` | Contribution terms (code contributions are MIT) |
| `CODE_OF_CONDUCT.md` | Community governance |
| `SECURITY.md` | Security policy |
| `CHANGELOG.md` | Software changelog (ships in the sdist) |
| `LICENSE` | MIT legal text (kept pure for JOSS OSI review) |

#### CC BY 4.0 License — Scholarly content

| Path | Description |
|------|-------------|
| `paper/**` | **Unpublished draft only.** A JOSS paper is in preparation. Not a released article and not part of the current software citation. See `paper/README.md`. |
| `docs/**` | Documentation, architecture analysis, curated page-map PDFs; `docs/LICENSE.md` |
| `archive/**` | Architecture Maps Parts I–VI and preserved scholarly reports; `archive/LICENSE.md` |
| `IMPLEMENTATION_PLAN_*.md` | Implementation planning documents |
| `SECURITY_AUDIT_PHASE*.md` | Audit reports (prose) |
| `LICENSING_DECISION.md` | This decision record |

#### Not licensed as scholarly content

| Path | Why |
|------|-----|
| `equation_registry.json` | **Not in HEAD.** Removed during the security audit. Do not recreate it to license it. |
| `page_verifier/data/**` | Generated cache (`latex_cache/`, PNG/AUX/LOG, verdict dumps). See `page_verifier/data/README.md`. |
| `chroma_data/`, `build/`, `dist/` | Runtime / build artifacts |

#### Public Domain — Maxwell's Original Text

| Material | Status |
|----------|--------|
| Raw Treatise text excerpts (1873) | Public Domain — no copyright can be claimed |
| OCR extractions of raw text | Public Domain (mechanical reproduction) |
| **User's annotations, corrections, modernized commentary** | **CC BY 4.0** (new creative work layered on PD) |
| **Article-to-function mapping structure** | **CC BY 4.0** (creative arrangement) |

### 5.2 How Major Projects Handle This

This split approach is **standard practice** in scientific Python:

| Project | Code License | Content License |
|---------|-------------|-----------------|
| **Astropy** | BSD-3-Clause | CC BY 4.0 (docs) |
| **scikit-learn** | BSD-3-Clause | CC BY 4.0 (docs) |
| **NumPy** | BSD-3-Clause | CC BY 4.0 (docs) |
| **SciPy** | BSD-3-Clause | CC BY 4.0 (docs) |
| **JOSS papers** | OSI-approved (software) | CC BY 4.0 (paper) |

---

## 6. Current State vs Target State

### Adopted / implemented state (2026-08-18)

```
LICENSE              → MIT (software; pure OSI text)
LICENSE-CONTENT      → CC BY 4.0 legal text + scope header
pyproject.toml       → license = "MIT" (comment notes CC BY content)
CITATION.cff         → license: MIT; message notes CC BY content and PD source
                       URLs: antmikinka/MAXWELL-MODERNIZED-PROGRAM
                       Maxwell cited as book reference, not software author
.zenodo.json         → license MIT; same URL; Maxwell not a software creator
README.md            → Dual badge + License section + correct clone URL
paper/               → unpublished draft (`paper/README.md`); not a citable JOSS article
docs/                → LICENSE.md (CC BY 4.0)
archive/             → LICENSE.md (CC BY 4.0)
CONTRIBUTING.md      → dual contribution grant
MANIFEST.in          → includes LICENSE-CONTENT; excludes docs/paper/archive
```

---

## 7. Implementation Checklist

### Phase 1: License Files

- [x] Keep existing `LICENSE` (MIT) — applies to all software (pure OSI text)
- [x] Create `LICENSE-CONTENT` with official CC BY 4.0 legal text
- [x] Scope header on `LICENSE-CONTENT` names software vs scholarship vs PD
      and states that governance files and CHANGELOG stay MIT

### Phase 2: Directory License Notes

- [x] `paper/README.md` — draft is in preparation, not a released JOSS article
- [x] `docs/LICENSE.md`
- [x] `archive/LICENSE.md`
- [x] `page_verifier/data/README.md` — generated cache, **not** CC BY scholarship
- [x] `page_verifier/README.md` license section

### Phase 3: Metadata Updates

- [x] Update `CITATION.cff`:
  - URLs set to `https://github.com/antmikinka/MAXWELL-MODERNIZED-PROGRAM`
  - `license: MIT` for the software entry
  - Paper reference with `license: CC-BY-4.0`
  - Maxwell removed as software author; cited as 1873 book
- [x] Update `pyproject.toml`:
  - Keep `license = "MIT"` (correct for PyPI)
  - Comment documents CC BY content
- [x] Update `.zenodo.json` (MIT software license, corrected URL, Maxwell not a creator)
- [x] Update `CONTRIBUTING.md` dual grant
- [x] Update `MANIFEST.in` to include `LICENSE-CONTENT` and exclude `docs/`, `paper/`, `archive/`

### Phase 4: README Update

- [x] License section explains the split
- [x] Dual badge (MIT + CC BY 4.0)
- [x] Clone URL and citation URL corrected
- [x] "Open access" principle no longer claims the implementation is public domain

### Phase 5: Verification

- [x] `pyproject.toml` still declares MIT
- [x] Root `LICENSE` remains a plain-text OSI-approved MIT file (JOSS)
- [x] Scholarly docs are not shipped in the Python sdist (`MANIFEST.in` excludes `docs/`, `paper/`, `archive/`)

---

## 8. FAQ

### "Can't I just use CC BY 4.0 for everything since it's a scholarly project?"

You *can*, but it will:
1. **Break JOSS submission** — they require an OSI-approved software license
2. **Cause PyPI / community issues** — `CC-BY-4.0` is a valid SPDX id, but it is the wrong instrument to declare on a scientific Python library
3. **Confuse contributors** — developers expect MIT/Apache/BSD on Python code
4. **Create patent ambiguity** — CC licenses don't address patent rights

### "Does CC BY 4.0 on the content affect the code?"

No. The licenses are cleanly separated by directory. Code in `maxwell/`, `tests/`,
etc. is MIT. Content in `docs/`, `paper/`, `archive/` is CC BY 4.0. There is no
overlap. The equation registry is a special case: the *equations* are mathematical
facts (not copyrightable), but the *registry structure and annotations* are CC BY 4.0.

### "What about Maxwell's original text?"

It's public domain. You cannot license it. But your *annotations, corrections,
modernized commentary, and mapping structure* are new creative works that ARE
protected by CC BY 4.0. The license should note this distinction.

### "What if someone copies just the docs?"

They must comply with CC BY 4.0 — attribute the work. That's the point. Under
MIT-only, the attribution requirement is weaker (just preserve the copyright notice).

### "Is this over-engineering for a solo project?"

No. This is the **standard pattern** used by Astropy, scikit-learn, NumPy, SciPy,
and every JOSS-published project. It takes ~30 minutes to implement and prevents
confusion later. It also signals professionalism to reviewers, contributors, and
institutional users.

---

## 9. References

- [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
- [MIT License](https://opensource.org/licenses/MIT)
- [JOSS License Requirements](https://joss.readthedocs.io/en/latest/submitting.html#license)
- [PyPI License Classifiers](https://pypi.org/classifiers/)
- [SPDX License List](https://spdx.org/licenses/)
- [Astropy Licensing Policy](https://www.astropy.org/license.html)
- [Choosing a License (choosealicense.com)](https://choosealicense.com/)
- [EU Database Directive (sui generis rights)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex%3A31996L0009)

---

## 10. Decision

| | |
|---|---|
| **Adopted option** | **Option C — Split Licensing (corrected inventory)** |
| **Code license** | MIT |
| **Content license** | CC BY 4.0 |
| **Public domain material** | Explicitly noted as PD |
| **Not adopted** | Option B (CC BY on code). Apache-2.0 switch. Draft map that CC-BY'd CHANGELOG/CONTRIBUTING and a missing `equation_registry.json`. |
| **Canonical repository** | `https://github.com/antmikinka/MAXWELL-MODERNIZED-PROGRAM` |

> **Bottom line:** Using only CC BY 4.0 on everything is understandable from a
> historical/modernization perspective, but it is the wrong instrument for the
> library and breaks JOSS. Using only MIT undersells the scholarly content and
> leaves Maxwell's text unmarked. The split is the honest, standard way to
> handle a project that is both software and scholarship.

## 11. Corrections made at adoption

These draft claims were **not** implemented:

1. **MIT does not grant patents.** The draft said software licenses "explicitly address" patents. Apache-2.0 does. MIT does not. This project stays on MIT because there is no patent surface in a 1873-physics reconstruction.
2. **`CC-BY-4.0` is an SPDX identifier.** The reason not to put it on the library is JOSS/OSI and software-license norms, not SPDX absence.
3. **`equation_registry.json` is not in the tree.** Do not recreate it.
4. **`page_verifier/data/` is generated cache**, not article-to-function tables.
5. **`page_verifier/static/`, `server.py`, `treatise.py`, `verdicts.py`, and `agents/`** are software (MIT).
6. **`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and `CHANGELOG.md` stay MIT.**
7. **James Clerk Maxwell is not a software author.** Cite the 1873 book.
8. **`MANIFEST.in` must not ship `docs/` inside an MIT-only sdist** without `LICENSE-CONTENT`. Adopted approach: ship `LICENSE` + `LICENSE-CONTENT` + README; keep bulk scholarly docs in git, not in the wheel.
9. **The JOSS paper is not included yet.** A manuscript may exist under `paper/` as a working draft. It is not a published article and must not appear in `CITATION.cff` as a citable paper. Mention only that a JOSS paper is in preparation.

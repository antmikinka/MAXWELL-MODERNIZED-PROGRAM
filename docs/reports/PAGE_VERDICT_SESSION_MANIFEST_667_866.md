# PAGE VERDICT SESSION MANIFEST — Arts. 667–866 (Vol II, Part IV, Ch. XII–XXIII)

- **Generated:** 2026-08-22T06:17:48Z (UTC)
- **Generator:** ARCHITECTUS (wave 8d), read-only derivation — **no verdict was invented, inferred, or auto-filled**
- **Deliverable class:** G1 input pack for G4 (the human-blocked input). Files: this manifest + machine-readable sibling `PAGE_VERDICT_SESSION_MANIFEST_667_866.json`.
- **Session scope:** Volume II pages `v2-p326` … `v2-p519` (body) + boundary page `v2-p520` = **195 pages**, carrying exactly the articles {667 … 866}.

---

## 1. Purpose and G4 dependency

G4 (Stage-5 doc §4 item 9 and §8) requires: *≥60 SymPy spine verifiers ·* ***100% page verdicts*** *· zero open S1/S2 · SCRIBA certification records → Arts. 667–866 declared ENSURED at ≥T3, spine at T4.*

G1 (Stage-5 doc §4 item 6) defines the page-verdict work package as: *"page_verifier semantic verdicts for all Vol II pages covering 667–866 + 200 signed formula sheets (PHYSICUS leads;* ***human adjudicates verdict sessions****)"*.

**Current truth:** `page_verifier/data/verdicts.json` holds 7 verdicts, all Volume I smoke tests; **zero Vol II verdicts exist**. The article/test dimension was certified at G3 (PASS — see §6), but the page-verdict dimension is **the sole human-blocked G4 input**. Spine T4 promotion awaits these verdicts. This manifest makes the session turnkey: every page is identified, its expected articles and image are listed, and a verdict slot is provided in the exact store schema.

*(Citation note: the wave brief referenced "§4.6" of the Stage-5 doc for the human-adjudication rule; in the on-disk document the binding statements are §4 item 6 (G1), §4 item 9 and §8 (G4 criteria), and the §5 ground rules. They are cited precisely here.)*

## 2. Session procedure (how verdicts are recorded)

1. Launch the verifier UI from the product root: `python run_page_verifier.py` → http://127.0.0.1:8765/ (legacy alternative: `streamlit run page_verifier/app.py`).
2. Filter **Volume II**; walk the pages in §7 order. The UI shows the page photo, the OCR/LaTeX text, and the product pane.
3. For each page, make the semantic judgment: open the page photo (`image_path`), read the Treatise article text actually present on the page, and compare against the product math shown for those articles (product pane = only `@maxwell_cite`-tagged `maxwell.*` functions).
   - **yes** = product math matches the rendered page content;
   - **no** = incorrect / mismatch (explain in `note`; the export feeds corrections back into `maxwell/`);
   - put anything ambiguous in `note` rather than guessing.
4. Recording: the UI persists via `page_verifier/verdicts.py::set_verdict` into `page_verifier/data/verdicts.json`. **Human-only writes.** If the UI is unavailable, a human may edit the JSON directly following §3 — same file, same schema.
5. **Session complete** when every row in §7 (195 rows) has a `yes`/`no` verdict recorded. The six `R` rows and the `B` row specifically need the visual confirmation described in their evidence cells.

## 3. Verdict schema (as observed in `verdicts.json` / `verdicts.py`)

Store wrapper (schema_version 1):

```json
{ "schema_version": 1,
  "product": "MAXWELL-MODERNIZED-PROGRAM",
  "updated_at": "<UTC ISO-8601 Z>",
  "count": 7,
  "verdicts": { "<page_id>": { } } }
```

Verdict object fields (verbatim from the live store / the `Verdict` dataclass):

| Field | Type | Meaning / session guidance |
|---|---|---|
| `page_id` | str | `v{volume}-p{page:03d}` — e.g. `v2-p326` |
| `volume` | int | `2` for every entry in this session |
| `page_number` | int | PDF page number within Vol II (326…520) |
| `verdict` | str | `"yes"` \| `"no"` \| `"unset"` — yes = product math matches page; no = incorrect/mismatch |
| `note` | str | free text; required for every `no`; recommended for the six `R` pages |
| `article_numbers` | list[int] | articles whose **start** appears on the page — copy the "starts here" column of §7 |
| `image_path` | str | page photo path (pre-filled per row in §7) |
| `updated_at` | str | UTC ISO-8601 with `Z`, set at write time |

Example entry as it should appear in the store after adjudicating the first session page:

```json
"v2-p326": {
  "page_id": "v2-p326", "volume": 2, "page_number": 326,
  "verdict": "yes", "note": "Art 667 normal-B continuity; tail of Art 666 also present",
  "article_numbers": [667],
  "image_path": "C:\\Users\\antmi\\maxwell-latex-books\\Third Edition\\15774-A Treatise On Electricity And Magnetism Vol-ii_images\\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\\page_326.png",
  "updated_at": "<set at write time>"
}
```

## 4. Evidence sources for the page↔article mapping (provenance)

Every row in §7 was derived from the sources below — never guessed. Where a mapping could not be established from available data it is flagged and deferred to visual confirmation in the session, per the honesty rule.

| ID | Source (read-only) | What it supplied |
|---|---|---|
| **E1** | `page_verifier/treatise.py` (`TREATISE` table) | Part IV = Arts 475–866, primary volume 2; Vol II OCR = 544 pages; article numbers are the stable join key |
| **E2** | `maxwell_em_processor\MAXWELL_VOLUME_2_MASTER_OUTPUT\volume_2_direct_result.json` via `page_verifier.catalog.build_catalog((2,))` | **144** Vol II pages carrying in-range article markers (regex `(\d{1,4})[a-z]?\.\s*\]`); all images resolved |
| **E3** | Vol II printed TOC (`maxwell-latex-books\Third Edition\VOLUME_2_PRELIM_TOC.JSON`) | printed start page for **168/200** articles; a constant printed→PDF offset of **+27** verified at 14+ control points (667→p326, 682→p342, 693→p355, 763→p435, 765→p437, 828→p491, 830→p493, 846→p507, 866→p519, …); placed the 6 marker-missing articles; **zero TOC-vs-marker disagreements** anywhere checked |
| **E4** | `MAXWELL_VOLUME_2_MASTER_OUTPUT\VOLUME_2_PART_4_CHAPTERS\*.JSON` | chapter extents (Ch XII … Ch XXIII); corrupted marker `83:.]` on p498 = Art 832 (first article of Ch XXII); Ch XXIII file spans pp 507–520 proving p520 belongs to Art 866 |
| **E5** | `maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\` | image convention `page_NNN.png`; **all 195 session pages resolve to existing files** |

Derivation method: article start page = OCR marker page where detected (E2), else TOC printed page + 27 (E3); page `p` carries article `a` iff `start(a) ≤ p < start(a+1)` (and through p520 for Art 866 per E4). The 32 articles whose TOC line failed extraction (671, 672, 675, 683, 688, 690, 710, 723, 728, 735, 752, 772–774, 778, 780, 781, 788, 791, 804, 810, 812, 814–816, 820, 833, 834, 842, 850, 852, 853) all have OCR marker pages, so **every one of the 200 articles is placed**.

**Consistency proof (exit criterion):** the union of article ranges across the manifest pages is **exactly {667…866}** — 200/200 articles, no gaps, no out-of-range entries; the page union is the contiguous block v2-p326…v2-p519 plus boundary v2-p520. Asserted programmatically at generation time from the sources above.

## 5. Chapter ↔ article ↔ page correspondence (Part IV, Ch. XII–XXIII)

Chapter numbering is **Part-IV-local**, exactly as printed in the Vol II TOC (E3: *"PART IV. ELECTROMAGNETISM. CHAPTER I. ELECTROMAGNETIC FORCE. 475."*); hence Arts 667–866 = Ch. XII (partial) through Ch. XXIII — the brief's "Ch XII–XXIII" is confirmed against the primary source.

| Ch. | Title (OCR chapter file) | Articles (chapter) | In scope | Pages (PDF) |
|---|---|---|---|---|
| XII | Current Sheets | 647–681 | **667–681** | 326–341 (chapter pp 313–341) |
| XIII | Parallel Currents | 682–693 | all | 342–357 |
| XIV | Circular Currents | 694–706 | all | 358–377 |
| XV | Electromagnetic Instruments | 707–729 | all | 378–400 |
| XVI | Electromagnetic Observations | 730–751 | all | 401–418 |
| XVII | Comparison of Coils | 752–757 | all | 419–428 |
| XVIII | Electromagnetic Unit of Resistance | 758–767 | all | 429–439 |
| XIX | Comparison of the Electrostatic with the Electromagnetic Units | 768–780 | all | 440–457 |
| XX | Electromagnetic Theory of Light | 781–805 | all | 458–477 |
| XXI | Magnetic Action on Light | 806–831 | all | 478–497 |
| XXII | Ferromagnetism and Diamagnetism Explained by Molecular Currents | **832**–845 | all | 498–506 |
| XXIII | Theories of Action at a Distance | 846–866 | all | 507–520 |

*(E4 note: the bracket-marker scan alone would give Ch XXII as 833–845, because Art 832's marker is corrupted in OCR to `83:.]` on p498, immediately after the CHAPTER XXII heading — Art 832 is the first article of Ch XXII.)*

## 6. G1 status honesty block (verbatim truth of the verdict store)

`page_verifier/data/verdicts.json` — `schema_version 1`, `updated_at 2026-08-18T04:18:20Z`, `count 7`:

| page_id | verdict | note | article_numbers | updated_at |
|---|---|---|---|---|
| `v1-p001` | no | NOT THAT IMP, BUT IS WRONG | [] | 2026-08-18T04:18:10Z |
| `v1-p002` | no | I MEAN NOT THAT IMP BTUT IS WRONG | [] | 2026-08-18T04:18:01Z |
| `v1-p003` | yes | Y` | [] | 2026-08-18T04:18:17Z |
| `v1-p004` | no | A TREATISE OF ELECTICITY AND MAGNETISM IS MISSING | [] | 2026-08-18T04:18:19Z |
| `v1-p005` | yes | (none) | [] | 2026-08-18T04:18:20Z |
| `v1-p036` | yes | smoke test | [1, 2] | 2026-08-10T03:56:13Z |
| `v1-p409` | yes | (none) | [254] | 2026-08-10T18:37:17Z |

- **Volume II verdicts: 0. In-scope (667–866) verdicts: 0.** The seven entries above are Vol I smoke tests (five prelim pages, one prelim/TOC page carrying arts [1,2], one Part II body page carrying art [254]).
- This is **the sole human-blocked G4 input**. The article-level dimension is already certified: `docs/reports/G3_GATE_REVIEW_2026-08-21.md` — G3 **PASS** (2312/0/0/0 suite reproduced twice; 200/200 articles with 333 marked qualifying tests; 0 in-scope HIGH lint findings; five S2 closures independently verified; honesty reconciliation clean). The G3 audit covers the article/test/defect dimensions; the page-verdict dimension is reserved for human adjudication per Stage-5 §4 item 6, and nothing in G3 substitutes for it.
- **Anti-theater rule (binding):** every verdict in this session must be a *human semantic judgment* on the rendered page versus the Treatise and the product math. No auto-fill, no agent-written verdicts, no carried-over defaults. Stage-5 §5 ground rules prohibit hardcoded verdicts; an empty checkbox in §7 stays empty until a human decides it.

## 7. Session manifest — 195 pages

Legend (status column):

| Code | Meaning | Count |
|---|---|---|
| **M** | Marker-confirmed: OCR of the volume shows an in-range article marker on this page (the catalog join key) | 144 |
| **R** | Recovered article start: an in-scope article *starts* here but its marker is absent/garbled in OCR; page fixed by TOC (E3) and/or text trace (see per-page evidence) | 6 |
| **C** | Continuation: no article starts here; article text continues from the previous page (span derived from TOC article-start pages) | 44 |
| **B** | Boundary: concluding page of Art. 866 / end of Part IV (no article starts; optional but recommended) | 1 |

Column notes: *articles carried* = articles whose text appears anywhere on the page (span-derived); *starts here* = articles whose numbered start appears on the page (copy these into `article_numbers` when recording). Tick exactly one of yes/no per row and record per §2/§3. Per-page evidence (source E2/E3/E4 derivations) for the flagged rows is given in §4–§5 and §8; the JSON sibling carries an `evidence` field for **every** row.

| # | page_id | articles carried | starts here | status | verdict | note (human) | image_path |
|---|---|---|---|---|---|---|---|
| 1 | `v2-p326` | 667 | 667 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_326.png` |
| 2 | `v2-p327` | 668 | 668 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_327.png` |
| 3 | `v2-p328` | 668 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_328.png` |
| 4 | `v2-p329` | 668 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_329.png` |
| 5 | `v2-p330` | 669 | 669 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_330.png` |
| 6 | `v2-p331` | 670 | 670 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_331.png` |
| 7 | `v2-p332` | 671 | 671 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_332.png` |
| 8 | `v2-p333` | 672-673 | 672-673 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_333.png` |
| 9 | `v2-p334` | 674 | 674 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_334.png` |
| 10 | `v2-p335` | 675 | 675 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_335.png` |
| 11 | `v2-p336` | 676 | 676 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_336.png` |
| 12 | `v2-p337` | 677 | 677 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_337.png` |
| 13 | `v2-p338` | 678-679 | 678-679 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_338.png` |
| 14 | `v2-p339` | 680 | 680 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_339.png` |
| 15 | `v2-p340` | 681 | 681 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_340.png` |
| 16 | `v2-p341` | 681 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_341.png` |
| 17 | `v2-p342` | 682 | 682 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_342.png` |
| 18 | `v2-p343` | 683 | 683 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_343.png` |
| 19 | `v2-p344` | 684-685 | 684-685 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_344.png` |
| 20 | `v2-p345` | 686-687 | 686-687 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_345.png` |
| 21 | `v2-p346` | 687 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_346.png` |
| 22 | `v2-p347` | 688-689 | 688-689 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_347.png` |
| 23 | `v2-p348` | 689 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_348.png` |
| 24 | `v2-p349` | 690 | 690 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_349.png` |
| 25 | `v2-p350` | 690 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_350.png` |
| 26 | `v2-p351` | 691 | 691 | **R** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_351.png` |
| 27 | `v2-p352` | 691 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_352.png` |
| 28 | `v2-p353` | 692 | 692 | **R** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_353.png` |
| 29 | `v2-p354` | 692 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_354.png` |
| 30 | `v2-p355` | 693 | 693 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_355.png` |
| 31 | `v2-p356` | 693 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_356.png` |
| 32 | `v2-p357` | 693 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_357.png` |
| 33 | `v2-p358` | 694 | 694 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_358.png` |
| 34 | `v2-p359` | 694 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_359.png` |
| 35 | `v2-p360` | 695 | 695 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_360.png` |
| 36 | `v2-p361` | 696 | 696 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_361.png` |
| 37 | `v2-p362` | 697 | 697 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_362.png` |
| 38 | `v2-p363` | 698-699 | 698-699 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_363.png` |
| 39 | `v2-p364` | 700 | 700 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_364.png` |
| 40 | `v2-p365` | 701 | 701 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_365.png` |
| 41 | `v2-p366` | 701 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_366.png` |
| 42 | `v2-p367` | 702 | 702 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_367.png` |
| 43 | `v2-p368` | 703 | 703 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_368.png` |
| 44 | `v2-p369` | 704 | 704 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_369.png` |
| 45 | `v2-p370` | 705 | 705 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_370.png` |
| 46 | `v2-p371` | 705 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_371.png` |
| 47 | `v2-p372` | 706 | 706 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_372.png` |
| 48 | `v2-p373` | 706 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_373.png` |
| 49 | `v2-p374` | 706 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_374.png` |
| 50 | `v2-p375` | 706 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_375.png` |
| 51 | `v2-p376` | 706 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_376.png` |
| 52 | `v2-p377` | 706 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_377.png` |
| 53 | `v2-p378` | 707 | 707 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_378.png` |
| 54 | `v2-p379` | 708 | 708 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_379.png` |
| 55 | `v2-p380` | 709 | 709 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_380.png` |
| 56 | `v2-p381` | 710-711 | 710-711 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_381.png` |
| 57 | `v2-p382` | 711 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_382.png` |
| 58 | `v2-p383` | 712-713 | 712-713 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_383.png` |
| 59 | `v2-p384` | 714 | 714 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_384.png` |
| 60 | `v2-p385` | 715 | 715 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_385.png` |
| 61 | `v2-p386` | 716 | 716 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_386.png` |
| 62 | `v2-p387` | 717-718 | 717-718 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_387.png` |
| 63 | `v2-p388` | 719 | 719 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_388.png` |
| 64 | `v2-p389` | 719 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_389.png` |
| 65 | `v2-p390` | 719 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_390.png` |
| 66 | `v2-p391` | 720-721 | 720-721 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_391.png` |
| 67 | `v2-p392` | 722 | 722 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_392.png` |
| 68 | `v2-p393` | 723-724 | 723-724 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_393.png` |
| 69 | `v2-p394` | 725 | 725 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_394.png` |
| 70 | `v2-p395` | 725 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_395.png` |
| 71 | `v2-p396` | 725 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_396.png` |
| 72 | `v2-p397` | 725 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_397.png` |
| 73 | `v2-p398` | 726 | 726 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_398.png` |
| 74 | `v2-p399` | 727-728 | 727-728 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_399.png` |
| 75 | `v2-p400` | 729 | 729 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_400.png` |
| 76 | `v2-p401` | 730 | 730 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_401.png` |
| 77 | `v2-p402` | 731 | 731 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_402.png` |
| 78 | `v2-p403` | 732 | 732 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_403.png` |
| 79 | `v2-p404` | 733-735 | 733-735 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_404.png` |
| 80 | `v2-p405` | 736-737 | 736-737 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_405.png` |
| 81 | `v2-p406` | 738-739 | 738-739 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_406.png` |
| 82 | `v2-p407` | 740 | 740 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_407.png` |
| 83 | `v2-p408` | 741 | 741 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_408.png` |
| 84 | `v2-p409` | 742-743 | 742-743 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_409.png` |
| 85 | `v2-p410` | 744 | 744 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_410.png` |
| 86 | `v2-p411` | 745-746 | 745-746 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_411.png` |
| 87 | `v2-p412` | 747 | 747 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_412.png` |
| 88 | `v2-p413` | 748 | 748 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_413.png` |
| 89 | `v2-p414` | 749 | 749 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_414.png` |
| 90 | `v2-p415` | 750 | 750 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_415.png` |
| 91 | `v2-p416` | 750 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_416.png` |
| 92 | `v2-p417` | 751 | 751 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_417.png` |
| 93 | `v2-p418` | 751 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_418.png` |
| 94 | `v2-p419` | 752 | 752 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_419.png` |
| 95 | `v2-p420` | 753 | 753 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_420.png` |
| 96 | `v2-p421` | 754 | 754 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_421.png` |
| 97 | `v2-p422` | 755 | 755 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_422.png` |
| 98 | `v2-p423` | 755 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_423.png` |
| 99 | `v2-p424` | 756 | 756 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_424.png` |
| 100 | `v2-p425` | 757 | 757 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_425.png` |
| 101 | `v2-p426` | 757 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_426.png` |
| 102 | `v2-p427` | 757 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_427.png` |
| 103 | `v2-p428` | 757 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_428.png` |
| 104 | `v2-p429` | 758-759 | 758-759 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_429.png` |
| 105 | `v2-p430` | 759 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_430.png` |
| 106 | `v2-p431` | 760 | 760 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_431.png` |
| 107 | `v2-p432` | 761-762 | 761-762 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_432.png` |
| 108 | `v2-p433` | 762 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_433.png` |
| 109 | `v2-p434` | 762 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_434.png` |
| 110 | `v2-p435` | 763 | 763 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_435.png` |
| 111 | `v2-p436` | 764 | 764 | **R** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_436.png` |
| 112 | `v2-p437` | 765 | 765 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_437.png` |
| 113 | `v2-p438` | 766-767 | 766-767 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_438.png` |
| 114 | `v2-p439` | 767 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_439.png` |
| 115 | `v2-p440` | 768 | 768 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_440.png` |
| 116 | `v2-p441` | 769 | 769 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_441.png` |
| 117 | `v2-p442` | 770 | 770 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_442.png` |
| 118 | `v2-p443` | 771 | 771 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_443.png` |
| 119 | `v2-p444` | 772 | 772 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_444.png` |
| 120 | `v2-p445` | 773 | 773 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_445.png` |
| 121 | `v2-p446` | 774 | 774 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_446.png` |
| 122 | `v2-p447` | 775 | 775 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_447.png` |
| 123 | `v2-p448` | 776 | 776 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_448.png` |
| 124 | `v2-p449` | 776 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_449.png` |
| 125 | `v2-p450` | 777 | 777 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_450.png` |
| 126 | `v2-p451` | 777 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_451.png` |
| 127 | `v2-p452` | 778 | 778 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_452.png` |
| 128 | `v2-p453` | 778 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_453.png` |
| 129 | `v2-p454` | 779 | 779 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_454.png` |
| 130 | `v2-p455` | 779 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_455.png` |
| 131 | `v2-p456` | 779 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_456.png` |
| 132 | `v2-p457` | 780 | 780 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_457.png` |
| 133 | `v2-p458` | 781 | 781 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_458.png` |
| 134 | `v2-p459` | 782 | 782 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_459.png` |
| 135 | `v2-p460` | 783 | 783 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_460.png` |
| 136 | `v2-p461` | 784 | 784 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_461.png` |
| 137 | `v2-p462` | 785-786 | 785-786 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_462.png` |
| 138 | `v2-p463` | 787 | 787 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_463.png` |
| 139 | `v2-p464` | 788-789 | 788-789 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_464.png` |
| 140 | `v2-p465` | 790 | 790 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_465.png` |
| 141 | `v2-p466` | 791 | 791 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_466.png` |
| 142 | `v2-p467` | 792 | 792 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_467.png` |
| 143 | `v2-p468` | 793 | 793 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_468.png` |
| 144 | `v2-p469` | 794 | 794 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_469.png` |
| 145 | `v2-p470` | 794 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_470.png` |
| 146 | `v2-p471` | 795-796 | 795-796 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_471.png` |
| 147 | `v2-p472` | 797-798 | 797-798 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_472.png` |
| 148 | `v2-p473` | 799-800 | 799-800 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_473.png` |
| 149 | `v2-p474` | 801-802 | 801-802 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_474.png` |
| 150 | `v2-p475` | 803-804 | 803-804 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_475.png` |
| 151 | `v2-p476` | 805 | 805 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_476.png` |
| 152 | `v2-p477` | 805 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_477.png` |
| 153 | `v2-p478` | 806 | 806 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_478.png` |
| 154 | `v2-p479` | 807-808 | 807-808 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_479.png` |
| 155 | `v2-p480` | 809-810 | 809-810 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_480.png` |
| 156 | `v2-p481` | 811 | 811 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_481.png` |
| 157 | `v2-p482` | 812-813 | 812-813 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_482.png` |
| 158 | `v2-p483` | 814-815 | 814-815 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_483.png` |
| 159 | `v2-p484` | 816-817 | 816-817 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_484.png` |
| 160 | `v2-p485` | 818 | 818 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_485.png` |
| 161 | `v2-p486` | 819-820 | 819-820 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_486.png` |
| 162 | `v2-p487` | 821 | 821 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_487.png` |
| 163 | `v2-p488` | 822 | 822 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_488.png` |
| 164 | `v2-p489` | 823-824 | 823-824 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_489.png` |
| 165 | `v2-p490` | 825-826 | 825-826 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_490.png` |
| 166 | `v2-p491` | 827-828 | 827-828 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_491.png` |
| 167 | `v2-p492` | 829 | 829 | **R** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_492.png` |
| 168 | `v2-p493` | 830 | 830 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_493.png` |
| 169 | `v2-p494` | 830 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_494.png` |
| 170 | `v2-p495` | 831 | 831 | **R** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_495.png` |
| 171 | `v2-p496` | 831 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_496.png` |
| 172 | `v2-p497` | 831 | - | **C** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_497.png` |
| 173 | `v2-p498` | 832 | 832 | **R** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_498.png` |
| 174 | `v2-p499` | 833-834 | 833-834 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_499.png` |
| 175 | `v2-p500` | 835 | 835 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_500.png` |
| 176 | `v2-p501` | 836-837 | 836-837 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_501.png` |
| 177 | `v2-p502` | 838-839 | 838-839 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_502.png` |
| 178 | `v2-p503` | 840-841 | 840-841 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_503.png` |
| 179 | `v2-p504` | 842-843 | 842-843 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_504.png` |
| 180 | `v2-p505` | 844 | 844 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_505.png` |
| 181 | `v2-p506` | 845 | 845 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_506.png` |
| 182 | `v2-p507` | 846-847 | 846-847 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_507.png` |
| 183 | `v2-p508` | 848 | 848 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_508.png` |
| 184 | `v2-p509` | 849-850 | 849-850 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_509.png` |
| 185 | `v2-p510` | 851-852 | 851-852 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_510.png` |
| 186 | `v2-p511` | 853-854 | 853-854 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_511.png` |
| 187 | `v2-p512` | 855 | 855 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_512.png` |
| 188 | `v2-p513` | 856 | 856 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_513.png` |
| 189 | `v2-p514` | 857 | 857 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_514.png` |
| 190 | `v2-p515` | 858 | 858 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_515.png` |
| 191 | `v2-p516` | 859-861 | 859-861 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_516.png` |
| 192 | `v2-p517` | 862-863 | 862-863 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_517.png` |
| 193 | `v2-p518` | 864 | 864 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_518.png` |
| 194 | `v2-p519` | 865-866 | 865-866 | **M** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_519.png` |
| 195 | `v2-p520` | 866 | - | **B** | [ ] yes&nbsp;&nbsp;[ ] no | | `C:\Users\antmi\maxwell-latex-books\Third Edition\15774-A Treatise On Electricity And Magnetism Vol-ii_images\VOLUME_2_PART_4_ELECTROMAGNETISM_IMAGES\page_520.png` |

## 8. Adjudicator notes and known OCR artifacts

1. **The six marker-missing articles** (the only pages needing extra care — status **R**):

   | Art | TOC title | Printed p | Session page | Evidence |
   |---|---|---|---|---|
   | 691 | Geometrical mean distance of two figures in a plane | 324 | **v2-p351** | TOC+27; OCR text shows `691.$]$` (bracket mangled into math mode) |
   | 692 | Particular cases | 326 | **v2-p353** | TOC+27 only; no legible marker — confirm visually |
   | 764 | Mathematical theory of the revolving coil | 409 | **v2-p436** | TOC+27; OCR text shows `764. Let $H$…` (bracket dropped) |
   | 829 | The magnetic rotation | 465 | **v2-p492** | TOC+27; OCR text shows `829. If λ…` (bracket dropped) |
   | 831 | Note on a mechanical theory of molecular vortices | 468 | **v2-p495** | TOC+27 only; no legible marker — confirm visually |
   | 832 | Magnetism is a phenomenon of molecules | 471 | **v2-p498** | TOC+27; OCR shows corrupted marker `83:.]` after the CHAPTER XXII heading |

2. **Spurious OCR markers:** `v2-p372` is indexed with an extra marker `75` alongside the real `706` — an OCR artifact (ignore `75` when adjudicating). The only other in-scope page with out-of-range material is `v2-p326`, which legitimately also carries the tail of Art. 666 (out of scope; belongs to Ch. XII but numbered below 667).
3. **Continuation pages (status C):** the verifier's own ledger joins pages↔articles by start markers, but articles regularly span 2+ pages; this manifest lists continuation pages so the human judges the *whole* text of Arts 667–866. The store accepts a verdict for any `v2-pNNN`, so recording them is fully supported.
4. **Boundary page (status B):** `v2-p520` carries the concluding paragraph of Art. 866 (…"this has been my constant aim in this treatise.") — end of Part IV and of the Treatise body. Adjudicate it as part of Art. 866.
5. **If a row's mapping looks wrong in session:** do not force a verdict; record `no` with a note describing the discrepancy (or leave unset and report it). This manifest's mapping is only as strong as its E2/E3/E4 evidence; the human eye is the final arbiter.

---
*Prepared by ARCHITECTUS, wave 8d. Read-only inputs: page_verifier sources/data, maxwell_em_processor OCR outputs, maxwell-latex-books Third Edition tree, G3 gate review, Stage-5 orchestration doc. Wrote only this manifest and its JSON sibling. `page_verifier/data/verdicts.json` untouched (human-only writes).*

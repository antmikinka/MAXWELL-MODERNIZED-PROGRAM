---
type: report
collab_reviewed: true
---

# Part/Chapter Conflict Adjudication — `@maxwell_cite` Metadata Audit

- **Agent:** ARCHITECTUS (architecture-management)
- **Date:** 2026-08-21
- **Ground truth:** `PARTS` table in `check_coverage.py` (repaired: Ch XVII = 752-757,
  Ch XVIII = 758-767; validated contiguous, zero overlaps).
  Part I = Arts 1-229, Part II = 230-370, Part III = 371-474, Part IV = 475-866.
- **Method:** Programmatic scan of `maxwell/**/*.py` (1,976 `@maxwell_cite` decorators,
  3,833 cited-article records) reusing the parser in `scripts/build_article_ledger.py`.
  Every cited article was joined to its canonical (part, chapter) from the PARTS table.
  Enumerator script run from a temp location (not committed; scope guard: metadata edits
  + this report only).
- **Scope guard:** decorator metadata only (`part=`, `chapter=`). Article numbers,
  function code, and docstring prose untouched.

## 1. Summary of Findings

| Category | Count | Action |
|---|---|---|
| `part=` wrong for ALL cited articles (pure conflicts), decorator instances | 27 | **FIX** — 27 edits (§2) |
| Ledger anomalies represented by the 27 pure conflicts (article×file dedup) | 10 | resolved by fixes |
| Part-spanning decorators (cited articles live in >1 Part) | 17 | adjudicate individually (§3) |
| — of which in excluded file `maxwell/math/spherical_harmonics.py` | 15 | SKIP (delegated) |
| `chapter=` semantic mismatches vs canonical chapter of cited article | 155 raw | **0 fixed** — all adjudicated KEEP (§4) |
| Decorators missing `part=` entirely (informational, not a conflict) | 8 | none (out of scope, §6) |
| Articles cited outside 1-866 (unmapped) | 0 | — |

Note: 28 edits = 27 pure-conflict decorators + 1 span decorator
(`math/calculus_calculator.py`, §3). Ledger anomaly arithmetic: 32 baseline →
12 resolved − 0 + 1 new documented span side-effect (Art 77) = **21 expected after fix**,
all 21 documented (19 excluded/delegated + 2 adjudicated spans).

## 2. Pure `part=` conflicts — FIX

Declared `part=` matches NO cited article's PARTS assignment. Verdict column gives the
adjudication; correct part/chapter come from the PARTS table. `chapter=` values in these
decorators are module-topic tags (see §4 policy) and are retained unless noted.

| # | File | Line | Articles | Declared part/chapter | Correct part/chapter (PARTS) | Verdict |
|---|------|------|----------|----------------------|------------------------------|---------|
| 1 | `maxwell/io/article_parser.py` | 28 | 1 | 5 / "Data Loading Utilities" | 1 / I.Prelim "Preliminary: Measurement of Quantities" | **FIX part=5→1** (keep chapter: module topic tag) |
| 2 | `maxwell/io/article_parser.py` | 88 | 1 | 5 / "Data Loading Utilities" | 1 / I.Prelim | **FIX part=5→1** |
| 3 | `maxwell/io/article_parser.py` | 169 | 1 | 5 / "Data Loading Utilities" | 1 / I.Prelim | **FIX part=5→1** |
| 4 | `maxwell/io/article_parser.py` | 270 | 1 | 5 / "Data Loading Utilities" | 1 / I.Prelim | **FIX part=5→1** |
| 5 | `maxwell/io/article_parser.py` | 393 | 1 | 5 / "Data Loading Utilities" | 1 / I.Prelim | **FIX part=5→1** |
| 6 | `maxwell/io/json_loader.py` | 31 | 1 | 5 / "Data Loading Utilities" | 1 / I.Prelim | **FIX part=5→1** |
| 7 | `maxwell/io/json_loader.py` | 89 | 1 | 5 / "Data Loading Utilities" | 1 / I.Prelim | **FIX part=5→1** |
| 8 | `maxwell/io/json_loader.py` | 143 | 1 | 5 / "Data Loading Utilities" | 1 / I.Prelim | **FIX part=5→1** |
| 9 | `maxwell/io/json_loader.py` | 256 | 1 | 5 / "Data Loading Utilities" | 1 / I.Prelim | **FIX part=5→1** |
| 10 | `maxwell/io/json_loader.py` | 292 | 1 | 5 / "Data Loading Utilities" | 1 / I.Prelim | **FIX part=5→1** |
| 11 | `maxwell/io/json_loader.py` | 358 | 1 | 5 / "Data Loading Utilities" | 1 / I.Prelim | **FIX part=5→1** |
| 12 | `maxwell/physics/current.py` | 102 | 150 | 2 / "The Electric Current" | 1 / I.X "Confocal Surfaces" | **FIX part=2→1** (keep chapter: topic tag; Art 150 assignment is PARTS ground truth) |
| 13 | `maxwell/physics/current.py` | 154 | 177 | 2 / "Mathematical Theory of Distribution" | 1 / I.XI "Electric Images" | **FIX part=2→1** |
| 14 | `maxwell/physics/current.py` | 250 | 150 | 2 / "The Electric Current" | 1 / I.X | **FIX part=2→1** |
| 15 | `maxwell/physics/current.py` | 329 | 64 | 2 / "Electric Currents" | 1 / I.II "Elementary Mathematical Theory" | **FIX part=2→1** |
| 16 | `maxwell/physics/current.py` | 364 | 150 | 2 / "The Electric Current" | 1 / I.X | **FIX part=2→1** |
| 17 | `maxwell/physics/current.py` | 399 | 177 | 2 / "Mathematical Theory of Distribution" | 1 / I.XI | **FIX part=2→1** |
| 18 | `maxwell/physics/current.py` | 489 | 152 | 2 / "The Electric Current" | 1 / I.X | **FIX part=2→1** |
| 19 | `maxwell/physics/current.py` | 529 | 150 | 2 / "The Electric Current" | 1 / I.X | **FIX part=2→1** |
| 20 | `maxwell/verification/sympy_verify.py` | 219 | 787 | 6 / "Electromagnetic Theory of Light" | 4 / IV.XX "EM Theory of Light" | **FIX part=6→4** (chapter CORRECT for Art 787, keep) |
| 21 | `maxwell/verification/sympy_verify.py` | 282 | 134 | 2 / "General Equations of Electrostatics" | 1 / I.IX "Spherical Harmonics" | **FIX part=2→1** (keep chapter: non-canonical topic tag) |
| 22 | `maxwell/vis/edge_singularities.py` | 21 | 191 | 2 / "Singular Points and Lines of Force" | 1 / I.XII "Conjugate Functions 2D" | **FIX part=2→1** (keep chapter: paraphrase of I.VI topic, same Part) |
| 23 | `maxwell/vis/edge_singularities.py` | 61 | 191 | 2 / same | 1 / I.XII | **FIX part=2→1** |
| 24 | `maxwell/vis/edge_singularities.py` | 96 | 191 | 2 / same | 1 / I.XII | **FIX part=2→1** |
| 25 | `maxwell/vis/edge_singularities.py` | 176 | 191 | 2 / same | 1 / I.XII | **FIX part=2→1** |
| 26 | `maxwell/vis/method_of_images.py` | 21 | 155 | 2 / "Theory of Electric Images" | 1 / I.XI "Electric Images" | **FIX part=2→1** (chapter accurate for I.XI, keep) |
| 27 | `maxwell/vis/method_of_images.py` | 82 | 155 | 2 / "Theory of Electric Images" | 1 / I.XI | **FIX part=2→1** |

**Root cause:** `part=5` / `part=6` values originate from the agents' layer model
("Part V = System Core", "Part VI = Scalar Physics" in `agents/architectus/agent.md`),
and `part=2` guesses were made for current-themed functions whose cited articles are
actually Part I. The PARTS table (Arts 1-866, Parts I-IV) is the declared ground truth
for article→Part mapping; io/theory/calculus/verification/vis modules citing real
articles must carry the article's Part. `maxwell/meta/citation.py` stores `part` as
inert metadata (no validation or branching), so these edits are behaviorally safe.

## 3. Part-spanning decorators (cited articles in >1 Part) — ADJUDICATE

Rule applied (per task directive): normalize to the **dominant part** — the Part
containing the majority of the cited articles; on ties, the part of the primary
(first-listed) article. Every case is recorded below.

| File | Line | Articles | Declared part | Parts hit (count) | Verdict |
|------|------|----------|---------------|-------------------|---------|
| `maxwell/electromagnetism/theory/remaining_gaps.py` | 1091 | 391, 516, 523-525, 532-535, 545, 552, 615 | 4 | III (1), IV (11) | **KEEP part=4.** Dominant part = IV (11/12 articles: IV.II, IV.III, IV.IV, IV.IX). Art 391 (III.I) is a deliberate cross-part anchor citation ("Magnetic induction relation", docstring item 1); PARTS ground truth for Art 391 itself is Part III, which is already correctly declared by a second decorator in the same file (line 47, Art 391, part=3). Ledger `part-conflict` on Art 391 remains **by design** as the documented span marker. Splitting the decorator would change citation counts and is outside metadata-only scope. |
| `maxwell/math/calculus_calculator.py` | 1027 | 77, 401, 402 | 1 | I (1), III (2) | **FIX part=1→3.** Dominant part = III (2/3 articles; Arts 401-402 are the Stokes'-theorem content articles in III.II "Magnetic Force & Induction"; Art 77 (I.II) is the supporting calculus reference). Side-effect: ledger will now flag Art 77 (documented span marker, symmetric to the Art 391 case above). |
| `maxwell/math/spherical_harmonics.py` | 1478, 1505, 1548, 1576, 1636, 1669, 1704, 1735, 1782, 1811, 1845, 1875, 1909, 1973, 2057 | Arts 128-146 each paired with Arts 675-695 | 4 | I (15 art-mentions), IV (15 art-mentions) | **SKIP — EXCLUDED** (delegated to another agent). For the record: these 15 decorators produce the 19 ledger anomalies on Arts 128-146. Same normalization rule would apply when the delegated agent addresses them. |

## 4. `chapter=` audit — 155 raw mismatches, all KEEP

**Policy:** `chapter=` in this codebase is a **topic tag**, not a claim of canonical
chapter membership: 198 distinct strings exist, many non-canonical module/function
themes ("Data Loading Utilities", "Signal Transmission", "Failure Modes", ...).
A `chapter=` is only "clearly wrong" if it names a canonical chapter **in a different
Part** with no topical justification. No case meets that bar; every raw mismatch falls
into one of the adjudicated categories below. **0 chapter edits.**

| Category (files × count) | Articles | Declared chapter → canonical map | Article's true chapter | Verdict & rationale |
|---|---|---|---|---|
| `electromagnetism/components/circular_coils.py` ×9 | 670-678 | "Circular Coils" → IV.XIV | IV.XII / IV.XIII | **SKIP — EXCLUDED** file. (Tag is the module theme anyway.) |
| `molecular/webers_theory.py` ×13, `molecular/competing_theories.py` ×1 | 841-850 | "Weber's Theory" → III.VI | IV.XXII / IV.XXIII | KEEP. Weber's theory is developed in III.VI (Arts 442-448) and applied in IV.XXII Molecular Currents; module is named `webers_theory.py`. Topical, cross-referential by nature. |
| `electromagnetism/physics/stress.py` ×11 | 501 | "Electromagnetic Stress" → IV.XI | IV.I | KEEP. Same Part; stress theme (IV.XI) applied to Art 501 summary of electromagnetic force. |
| `electromagnetism/potentials/surfaces.py` ×11, `vis/helicoidal_potentials.py` ×4 | 486, 487 | "Equipotential Surfaces" → I.VII | IV.I | KEEP. Cross-part but topically justified: functions compute equipotential surfaces of electromagnetic potentials (Part IV treatment); tag describes the computation, not the article's chapter. |
| `electrostatics/dielectrics.py` ×11 | 157-164 | "Theory of Dielectrics" → II.X | I.XI | KEEP. Cross-part module-theme tag (dielectrics file); cited articles are the electric-image theory used by the functions. |
| `electrostatics/force_theory.py` ×11 | 50-65 | "Elementary Theory" → III.I (alias) | I.I / I.II | KEEP — **ambiguous, not confidently adjudicable.** "Elementary Theory" may abbreviate I.II "Elementary Mathematical Theory" (same Part) or reference III.I; articles are Part I. No safe single correction; flagged for future review. |
| `electrostatics/phenomena.py` ×14 | 12-19 | "Description of Phenomena" → I.I | I.Prelim | KEEP. Same Part; file-level theme tag (phenomena module), articles are adjacent Preliminary arts 12-19. |
| `engineering/naval.py` ×8 | 441 | "Naval Magnetism" → non-canonical | III.V | KEEP. "Naval Magnetism" is not a PARTS chapter title; applied-topic tag for ship-magnetism functions citing Art 441 (III.V Particular Problems). |
| `jax/electromagnetism/electrokinetic.py` ×8 | 634-638 | "Electrokinetic Energy" → non-canonical | IV.XI | KEEP. Non-canonical theme tag; articles 634-638 are in IV.XI Energy & Stress (consistent theme). |
| `optics/diffusion.py` ×12 | 806-808 | "Electromagnetic Theory of Light" → IV.XX | IV.XXI | KEEP. Same Part, adjacent chapter (IV.XXI Magnetic Action on Light); optics-module theme tag. |
| `config/equations.py` ×1 | 591-622 | "General Equations of the Electromagnetic Field" → IV.IX | IV.VIII+IX+X span | KEEP. Legitimate 3-chapter span; tag names the dominant chapter (16/31 articles in IV.IX, whose canonical title is "General Field Equations" — Maxwell's own title for Ch IX). |
| `electromagnetism/theory/general_equations.py` ×1, `jax/electromagnetism/equations.py` ×1, `math/derivatives.py` ×4, `electromagnetism/theory/em_light_theory.py` ×2, `verification/sympy_verify.py:472` ×1 | 591-603, 593 | same tag → IV.IX | IV.VIII | KEEP. Same Part, adjacent chapter; functions concern the general field equations built on Arts 585-603 groundwork. Noted as minor topical drift. |
| `electromagnetism/theory/remaining_gaps.py` ×5 | 391, 516, 523, 525, 615 | "Magnetic Induction" / "Induction of Currents" / "Electromagnetic Theory of Light" | III.I; IV.II; IV.IX | KEEP. Same-Part topical tags (Art 391 B=μH; Arts 516/523/525 treated as induced-current laws per module docstring; Art 615 refractive-index relation feeding light theory). |
| `core/charge.py` ×1 | 45 | "Electrical Work and Energy" → I.III | I.I | KEEP. Same Part topical tag. |
| `core/magnet.py` ×1, `jax/core/magnet.py` ×1 | 392 | "Terrestrial Magnetism" → III.VIII | III.I | KEEP — noted; same Part, function-theme tag. |
| `core/units/dimensions.py` ×3 | 620, 771 | "Ratio of Units" → IV.XIX; "Electromagnetic Theory of Light" → IV.XX | IV.X; IV.XIX | KEEP. Same Part; unit-ratio articles topically tied to light-speed ratio (ESU/EMU). |
| `physics/conduction.py` ×2 | 230 | "Conduction and Resistance" → II.II | II.I | KEEP. Same Part, adjacent chapter (Art 230 opens Part II). |
| `vis/thermal_gradients.py` ×6 | 242, 249 | "Conduction in Linear Conductors" → II.VI | II.II / II.IV | KEEP. Same Part topical tag. |
| `vis/equipotential.py` ×2 | 16 | "On Equipotential Surfaces and Lines of Force" → I.VII | I.Prelim | KEEP. Same Part; visualization-theme tag. |
| `vis/edge_singularities.py` ×4 | 191 | "Singular Points and Lines of Force" → I.VI (paraphrase) | I.XII | KEEP. Same Part; paraphrase of I.VI "Points & Lines of Equilibrium" topic; part= fixed in §2. |
| `physics/current.py` ×6 | 64, 150, 152 | "The Electric Current"/"Electric Currents" → II.I | Part I chapters | KEEP. Module-theme tags on a current module; part= fixed in §2. |

## 5. Exclusions honored (other agents own these now)

- `maxwell/math/spherical_harmonics.py` — 15 span decorators / 19 ledger anomalies — **skipped, delegated**.
- `maxwell/magneto_optics/**`, `maxwell/vortex_engine/**`, `maxwell/instruments/**`,
  `maxwell/experiments/ratio_v/**`, `maxwell/electromagnetism/components/circular_coils.py`,
  `maxwell/math/elliptic_integrals.py`, `maxwell/math/geometry/gmd.py` — scanned, no
  in-scope part= conflicts found (circular_coils.py had 9 chapter-only flags, §4).

## 6. Observations (informational, no action)

- 8 decorators in `maxwell/electrokinematics/resistance_measurement.py` (lines 239, 344,
  482, 628, 790, 924, 1050, 1181; Arts 335-358, all Part II) omit `part=` entirely.
  Not a conflict (nothing wrong to fix); adding metadata is outside this audit's scope.
- 0 articles cited outside the 1-866 range (no unmapped citations).
- No non-literal `part=`/`chapter=` values in real decorators (the two regex hits were a
  docstring example in `io/json_loader.py` and the pass-through in `meta/citation.py`).

## 7. Expected post-fix state

- Ledger anomalies: 32 → **21** = 19 (excluded spherical_harmonics, delegated) +
  Art 391 (remaining_gaps span marker, §3) + Art 77 (calculus span marker, §3).
- Coverage invariants: 866 ledger entries, 866/866 in `check_coverage.py`,
  singleton counts unchanged (metadata edits neither add nor remove citations).

*Verification results appended after fixes in §8.*

## 8. Post-fix verification (2026-08-21)

**Edits applied:** 28 decorator instances across 7 files; `git diff` confirms exactly
28 single-line `part=N` changes and nothing else. Re-scan after edits: **0 pure part=
conflicts** (was 27); the 17 part-spanning decorators remain as adjudicated in §3
(15 of them in the excluded/delegated `spherical_harmonics.py`).

**`scripts/build_article_ledger.py`:**
- Articles: **866** ✓ (unchanged)
- Anomalies: 32 → **21** ✓ — = 19 Arts 128-146 (`spherical_harmonics.py`, excluded/
  delegated) + Art 391 (`remaining_gaps.py` span marker, §3) + Art 77
  (`calculus_calculator.py` span marker, §3). All 21 documented; 0 unadjudicated.
- Citations 3829 → 3832 and singletons 152 → 151 (42 → 41 in 667-866): **not caused
  by this audit.** Concurrent agents modified excluded-domain files during the audit
  window (`git status`: `instruments/galvanometers.py` +492 lines,
  `magneto_optics/rotation.py`, `magneto_optics/circular_polarization.py`,
  `experiments/ratio_v/combined.py`, `optics/diffusion.py`,
  `electromagnetism/measurements/galvanometers_extended.py`, `tests/conftest.py`).
  Three independent proofs: (a) ledger `cite_count` is derived solely from
  (file, function, description) tuples — `part=` enters only the anomaly check in
  `build_ledger`; (b) `git diff` of this audit's 7 files shows only `part=N` lines;
  (c) the only watch-range article cited by any of the 7 audited files is Art 787
  (`cite_count` 18, not a singleton). All 41 current watch-range singletons reside in
  other-agent domains (instruments, ratio_v, magneto_optics, vortex_engine,
  signal_processing).

**`check_coverage.py`:** `TOTAL: 866/866 articles implemented (100%)` ✓ (unchanged).

**Tests (task 5):** modules touched have test coverage via `tests/test_sympy_verify.py`,
`tests/test_calculus_calculator.py`, `tests/test_vis.py`, `tests/test_citation_decorator.py`:
**117 + 45 + 14 = 176 passed, 0 failed** (run with `-p no:randomly`). All 7 touched
modules import cleanly. Note: with `pytest-randomly` enabled, `test_vis.py` hits a
pre-existing matplotlib `streamplot`/`transforms.get_affine` recursion abort that
depends on test order; deterministic order is 45/45 green. A `part=` integer cannot
influence rendering; the instability predates this audit. No tests import
`maxwell/io/article_parser.py`, `maxwell/io/json_loader.py`, or
`maxwell/physics/current.py` directly.

**Ambiguities not resolvable with confidence (deferred):**
1. `electrostatics/force_theory.py` ×11 `chapter="Elementary Theory"` on Arts 50-65
   (may abbreviate I.II "Elementary Mathematical Theory" or reference III.I) — kept.
2. The 21 remaining ledger anomalies: 19 delegated (spherical_harmonics.py), 2 are
   irreducible single-field markers of legitimate cross-part spans (Arts 391, 77);
   a future task could split those two decorators if per-article part fidelity is
   required (would change citation counts — outside metadata-only scope here).

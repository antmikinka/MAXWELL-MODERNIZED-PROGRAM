---
type: remediation-plan
program: below-667 backlog (pre-LAST200 scope) — scheduled per examiner recommendation R7
date: 2026-08-22
author: ARCHITECTUS (architecture & evidence persona), Wave 9b
status: PLAN ONLY — no fixes executed; execution gated by planning-analysis-v2 scope review (Stage-5 §5 scope lock)
lint_run: python scripts/anti_theater_lint.py (default scan dirs maxwell/ + tests/), 2026-08-22, 364 files scanned
---

# Remediation Plan — Anti-Theater Lint Backlog Below Art. 667

**Deliverable class:** planning artifact (Wave 9b, examiner recommendation R7: "schedule the
13-item <667 HIGH backlog"). This document **plans only**. It executes nothing. The in-scope
program (Arts. 667–866) is G3-PASS and G4-READY-PENDING-HUMAN; every item below targets code
that cites articles **< 667**, which the Stage-5 scope lock places outside this program's
authority to change.

**Gate precondition (binding, restated in §6):** execution of any item in this plan requires a
**planning-analysis-v2 scope review** per `docs/LAST200_STAGE5_AGENT_ORCHESTRATION.md` §5
("Scope lock: 667–866 only. Anything outside requires planning-analysis-v2 scope review"), and
would run as a **separate program** — not under the 667–866 G0–G4 gate structure.

---

## 1. The lint run (ARCHITECTUS's own, 2026-08-22)

Command: `python scripts/anti_theater_lint.py` with default scan directories (`maxwell/`,
`tests/`), full ten rules R1–R10, emitted via `--json` and re-verified in text mode.

| Metric | Value |
|---|---|
| Files scanned | **364** |
| Total findings | **1548** |
| HIGH findings | **13** |
| MEDIUM findings | **1535** (R7-in-tests = 5, R8 chapter drift = 1530) |
| By rule | R1=1, R2=1, R3=0, R4=0, R5=0, **R6=11**, R7=5, R8=1530, R9=0, R10=0 |
| Exit code semantics | 1 (≥1 HIGH) — entirely driven by the <667 backlog |

### 1.1 All 13 HIGH findings, verbatim from this run

```text
maxwell/config/conventions.py:300: [R6|HIGH] @maxwell_cite function 'magnetic_convention_summary' body is the constant return `{'polarity': 'Austral (N) = positive (+), Boreal (S) = ne...` -- implement the article's computation instead of returning a verdict/prose
maxwell/core/charge.py:104: [R6|HIGH] @maxwell_cite function 'faraday_isolation_proof' body is the constant return `"Faraday's Doctrine (Art. 45): Electrification always occ...` -- implement the article's computation instead of returning a verdict/prose
maxwell/electromagnetism/theory/remaining_gaps.py:945: [R2|HIGH] verdict variable 'verified' assigned literal True and never recomputed -- compute the check instead of asserting it
maxwell/electrostatics/force_theory.py:354: [R6|HIGH] @maxwell_cite function 'two_fluid_theory' body is the constant return `{'name': 'Two-Fluid Theory', 'proponent': 'Robert Symmer ...` -- implement the article's computation instead of returning a verdict/prose
maxwell/electrostatics/force_theory.py:412: [R6|HIGH] @maxwell_cite function 'one_fluid_theory' body is the constant return `{'name': 'One-Fluid Theory', 'proponent': 'Benjamin Frank...` -- implement the article's computation instead of returning a verdict/prose
maxwell/electrostatics/force_theory.py:811: [R6|HIGH] @maxwell_cite function 'field_concept' body is the constant return `{'action_at_distance': {'description': 'Charges act direc...` -- implement the article's computation instead of returning a verdict/prose
maxwell/electrostatics/force_theory.py:903: [R6|HIGH] @maxwell_cite function 'field_reality_statement' body is the constant return `'The electric field is a real physical state of the mediu...` -- implement the article's computation instead of returning a verdict/prose
maxwell/electrostatics/phenomena.py:1122: [R6|HIGH] @maxwell_cite function 'complete_phenomenology' body is the constant return `{'friction': {'articles': [12, 13, 14], 'description': 'E...` -- implement the article's computation instead of returning a verdict/prose
maxwell/fields/solenoidal.py:78: [R1|HIGH] verifier 'verify_flux_conservation' returns only literal bools (2 return site(s)) -- verdicts must be computed from compared quantities
maxwell/fields/solenoidal.py:471: [R6|HIGH] @maxwell_cite function 'prove_no_magnetic_monopoles' body is the constant return `"Proof (Art. 404): Magnetic monopoles cannot exist becaus...` -- implement the article's computation instead of returning a verdict/prose
maxwell/materials/hysteresis.py:421: [R6|HIGH] @maxwell_cite function 'explain_hysteresis_phenomena' body is the constant return `{'retentivity': "After a ferromagnetic material is magnet...` -- implement the article's computation instead of returning a verdict/prose
maxwell/physics/gauss.py:702: [R6|HIGH] @maxwell_cite function 'derive_inverse_square_from_gauss' body is the constant return `"\nDerivation of Inverse-Square Law from Gauss's Law\n===...` -- implement the article's computation instead of returning a verdict/prose
maxwell/physics/magnetostriction.py:557: [R6|HIGH] @maxwell_cite function 'explain_magnetostriction_phenomena' body is the constant return `{'joule_effect': 'Discovered by James Joule in 1842, this...` -- implement the article's computation instead of returning a verdict/prose
```

### 1.2 Article census and reconciliation with the prior verification

All 13 HIGH findings cite articles **< 667 — confirmed, no exceptions**. The cited-article set
from this run:

> **Arts 12–19 (×8 in one citation), 45, 50–55 (×6 across two citations), 65 ×2, 76,
> 393/394, 404 ×2, 444, 447, 552** — 25 article citations across 13 findings.

This **matches exactly** the prior program record (`LAST200_STAGE5_AGENT_ORCHESTRATION.md` §6,
G3 close table: "13 HIGH mapped to Arts 12–19, 45, 50–55, 65×2, 76, 393/394, 404×2, 444, 447,
552 — all <667"). **No discrepancy.** Part distribution: Part I (12–19, 45, 50–55, 65×2, 76),
Part III (393/394, 404×2, 444, 447), Part IV pre-scope (552).

Severity rationale (why HIGH, per `scripts/anti_theater_lint.py` docstring and Stage-3 §5.3):

- **R6 (11 findings):** a `@maxwell_cite`-decorated function whose entire body is a constant
  return is prose-as-implementation under a Treatise citation (Stage-3 rules 2–3 class). R6 is
  HIGH everywhere regardless of tree; none of these sit in `tests/`.
- **R1 (1 finding):** verifier-named function (`verify_*`) whose every return is a literal
  bool — the verdict is asserted, not computed (Stage-3 rule 2). HIGH in `maxwell/`.
- **R2 (1 finding):** verdict variable assigned a literal and never recomputed (Stage-3 rule 1).
  HIGH in `maxwell/`.

Note on Wave 5a: the Stage-5 record states CIRCUITUS "remediated … solenoidal R1" in Wave 5a.
The sibling verifiers in the same module (`verify_solenoidal`, line 158; `verify_zero_net_flux`,
line 234) and `components/solenoids.py:verify_solenoid_field` are computed and unflagged — that
wave evidently cleared a different solenoidal R1 site. The Art-404 method flagged here
(`MagneticInductionTube.verify_flux_conservation`, line 78) **persists** and is scheduled below.

---

## 2. Finding-by-finding remediation classification

Strategy key for R6 findings (per mission directive):
- **(a)** implement-real-computation — the article has computable content; replace the constant
  return with a genuine calculation (oracles required, as everywhere in this program).
- **(b)** re-decorate as exposition — the content is genuinely historical/conceptual
  exposition; classify it as such (`theory_class="historical_exposition"` or equivalent) with
  the lint policy adjusted accordingly. **Precondition:** `maxwell/meta/citation.py` currently
  validates `theory_class` against `{"maxwell_original", "user_original", "standard_math"}`
  only — a new exposition class and an R6 exemption/downgrade in `anti_theater_lint.py` are
  governance decisions (the lint is a Stage-5 §5 merge gate; its semantics are not changed
  casually). If policy is declined, the fallback for each (b) item is (c).
- **(c)** strip the citation — remove `@maxwell_cite` (keep the article reference in prose/docstring);
  honest when the body is modern commentary rather than an implementation or faithful
  exposition of the article. Ledger impact: the article leaves the citation ledger counts —
  acceptable for <667 articles, must be recorded.

| # | Finding | file:line | Rule | Art(s) | Recommended strategy (one-line rationale) | Effort |
|---|---|---|---|---|---|---|
| 1 | `magnetic_convention_summary` | `maxwell/config/conventions.py:300` | R6 | 393, 394 (Pt III) | **(b) exposition** — convention reference metadata, not physics; the computable convention logic already lives in sibling functions (`convert_pole_naming`, signed field helpers). | S |
| 2 | `faraday_isolation_proof` | `maxwell/core/charge.py:104` | R6 | 45 (Pt I) | **(a) implement** — the doctrine has a quantitative core (Σq = 0 in any charging process); the module already computes exactly this in `verify_charge_conservation` (Art 245), giving a ready pattern and independent residual. | S–M |
| 3 | `two_fluid_theory` | `maxwell/electrostatics/force_theory.py:354` | R6 | 50, 51, 52 (Pt I) | **(b) exposition** — Maxwell's review of Symmer's discarded theory is history-of-science narrative with no computable content. | S |
| 4 | `one_fluid_theory` | `maxwell/electrostatics/force_theory.py:412` | R6 | 53, 54, 55 (Pt I) | **(b) exposition** — same class: Franklin's one-fluid theory as reviewed narrative. | S |
| 5 | `field_concept` | `maxwell/electrostatics/force_theory.py:811` | R6 | 65 (Pt I) | **(b) exposition** — conceptual contrast (action-at-a-distance vs medium); no formula in the article to compute. | S |
| 6 | `field_reality_statement` | `maxwell/electrostatics/force_theory.py:903` | R6 | 65 (Pt I) | **(c) strip citation** — modern commentary paraphrase, duplicative of #5; fold into #5's docstring rather than cite Art 65 twice for prose. | S |
| 7 | `complete_phenomenology` | `maxwell/electrostatics/phenomena.py:1122` | R6 | 12–19 (Pt I) | **(b) exposition** — a phenomenology reference table; its few numeric hooks (e.g. breakdown field) are annotations, not the article's computation. | S |
| 8 | `verify_flux_conservation` | `maxwell/fields/solenoidal.py:78` | R1 | 404 (Pt III) | **Computed-verdict refactor** — accept independent per-point B samples; verdict = `max|B_i·A_i − Φ| ≤ tol·Φ`; keep the degenerate-input guard (`len(areas) < 2`); return "not evaluated" when no independent B data is supplied (a B derived as Φ/A would be self-confirming and must not be used). | M |
| 9 | `prove_no_magnetic_monopoles` | `maxwell/fields/solenoidal.py:471` | R6 | 404 (Pt III) | **(a) implement** — Art. 404's proof is exactly "∮B·dA = 0 on closed surfaces", and the module already carries surface-flux quadrature machinery; convert to a computed net-flux check over a closed surface with the prose moved to the docstring. | M |
| 10 | `explain_hysteresis_phenomena` | `maxwell/materials/hysteresis.py:421` | R6 | 444 (Pt III) | **(b) exposition** — retentivity/coercivity prose; the module's computable loop/energy-loss content lives in the neighboring (unflagged) functions. | S |
| 11 | `derive_inverse_square_from_gauss` | `maxwell/physics/gauss.py:702` | R6 | 76 (Pt I) | **(a) implement** — the derivation is demonstrable: E(R) from independent surface-integral quadrature vs q/R² residuals; the module already computes verified Gauss-law numerics (computed `verified` pattern at lines 684–692). | M |
| 12 | `explain_magnetostriction_phenomena` | `maxwell/physics/magnetostriction.py:557` | R6 | 447 (Pt III) | **(b) exposition** — Joule/Villari-effect prose; the module's computable magnetoelastic energy sits directly above it (line 547) and is unflagged. | S |
| 13 | `generalized_ampere_law` — `verified = True` | `maxwell/electromagnetism/theory/remaining_gaps.py:945` | R2 | 552 (Pt IV, pre-scope) | **Computed-verdict refactor** — accept an optional measured/`curl_H_actual` input; set `verified = allclose(curl_H_actual, total_rhs, tol)`; when absent, emit `verified: None` + `status: "not_evaluated"` instead of a structural-True. The forward computation (conduction + displacement terms) is already real; only the verdict is theater. | M |

### 2.1 Strategy counts

- **R6 findings: 11** → (a) implement-real-computation: **3** (#2, #9, #11); (b) re-decorate
  as exposition: **7** (#1, #3, #4, #5, #7, #10, #12); (c) strip citation: **1** (#6).
- **R1/R2 findings: 2** → computed-verdict refactors: **2** (#8, #13).

### 2.2 Cross-cutting implementation constraints for the (a) and computed-verdict items

- Every new computation needs an **independent oracle** (program-wide discipline; cf. G3 review
  §5 spot checks). Beware self-confirmation traps: in #8, B must not be derived from Φ/A before
  being checked against Φ; in #11, the Gauss-side and Coulomb-side must not share one code path.
- Any API change (new optional parameters on #8, #13) must be reviewed for existing callers
  before execution; the backlog program owns its own regression run.
- Items #8/#9 share one file; #2, #11, #13, #10, #12, #1 sit in distinct modules and
  parallelize cleanly.

---

## 3. Doc-only work entries — abampere unit labels (Arts 647–662)

QUALITAS (Wave 8c) fixed the in-scope "abamperes" docstrings (5 files, examiner R2) and
recorded: **"Out-of-scope abampere notes (Arts 647–662) recorded for the <667 backlog."**
Both affected modules were inspected for this plan; the defect class matches the G3-review
S3-2 ruling (docstrings say abamperes while formulas carry explicit-`c` factors, i.e. the code
consumes Gaussian statampere-family quantities):

| # | File | Arts | Concrete evidence | Work | Effort |
|---|---|---|---|---|---|
| D-1 | `maxwell/electromagnetism/current_sheets/sheet_theory.py` | 647–655 | Header line 23 and docstrings at lines 53, 65, 103, 131–132 label surface current "abamperes/cm" while the boundary condition uses `4π/c` (line 330) and shell/moment conversions divide by `CONST.C` (lines 224, 271, 504) — Gaussian signature; line 256 additionally mislabels a *per-unit-length* argument as plain "(abamperes)". | Audit every unit label against the formula's `c`-factor signature; relabel to the Gaussian-CGS explicit-c convention with the ESU↔EMU bridge note, exactly as Wave 8 did in `components/circular_coils.py` lines 34–50. Doc-only. | S |
| D-2 | `maxwell/electromagnetism/current_sheets/surface_currents.py` | 656–662 | Header lines 13/18 and docstrings at lines 51, 59–60, 84, 116, 158, 204, 210–211, 447 label currents "abamperes" while Biot–Savart (line 303) and the boundary condition (line 368) carry `1/c` and `4π/c`. `calc_surface_current` (line 225) is unit-agnostic (`I/w`) and needs a convention note rather than a forced relabel. | Same audit-and-relabel pattern as D-1; mark unit-agnostic helpers explicitly. Doc-only. | S |

These are documentation fixes only — behavior in both modules is unaltered, and no numeric
golden moves. They remain subject to the §6 gate precondition because Arts 647–662 < 667.

---

## 4. Parallel MEDIUM backlog (honest census, from the same run)

### 4.1 R7 hardcoded-constant MEDIUMs in `tests/` (5 findings)

```text
tests/run_quality_checks.py:204: [MEDIUM] hardcoded physical constant 30000000000.0 (speed-of-light family; use CONST.C)   | if not (2.997e10 <= CONST.C <= 3.0e10):
tests/run_quality_checks.py:208: [MEDIUM] hardcoded physical constant 30000000000.0 (speed-of-light family; use CONST.C)   | if CONST.C_APPROX != 3.0e10:
tests/test_cgs_units.py:40:      [MEDIUM] hardcoded physical constant 29979245800.0 (speed-of-light family; use CONST.C)   | expected = 2.99792458e10
tests/test_cgs_units.py:55:      [MEDIUM] hardcoded physical constant 30000000000.0 (speed-of-light family; use CONST.C)   | assert CONST.C_APPROX >= 3.0e10
tests/test_jax_adapter.py:1449:  [MEDIUM] hardcoded physical constant 30000000000.0 (speed-of-light family; use CONST.C)   | [0.0, 0.0, 3e10],
```

Recommendation: all five clear via the rule's own escape hatch — R7 in `tests/` is suppressed
when a provenance comment (matching the provenance regex) appears within 2 lines. Per-item:

- `run_quality_checks.py:204/208` — sanity bounds on `CONST.C`/`CONST.C_APPROX` themselves;
  add provenance ("bounds derived from the SI definition 299 792 458 m/s") or re-express bounds
  via `CONST.C_APPROX` arithmetic. **S.**
- `test_cgs_units.py:40` — this golden is *deliberately independent* of `constants.py` (it
  mirrors the SI definition, the same independence Wave 6 built into `module_checks`); the fix
  is a provenance comment stating that intent, not a `CONST.C` substitution. **S.**
- `test_cgs_units.py:55`, `test_jax_adapter.py:1449` — provenance comment or `CONST.C`
  reference. **S.**

**Coordination note:** another agent is concurrently editing `tests/articles/reference_values.json`;
this plan owns nothing under `tests/`, and these five items should execute only after that
reference-store migration settles, so provenance comments can point at the pinned store.

### 4.2 R8 chapter drift (1530 MEDIUM findings) — bulk normalization vs acceptance

Census from this run (AST re-parse, agreeing with the lint's 1530):

- **167 distinct drifted chapter strings**; top drifts: 'Electromagnetic Theory of Light' (191),
  'Energy in the Electromagnetic Field' (64), 'Constitutive Relations' (47), 'Mathematical
  Definitions' (37), 'General Equations' (35).
- **Article-concentration test (computed for this plan):** for each drifted title, the set of
  articles cited under it was checked against the PARTS chapter ranges in `check_coverage.py`.
  **139 of 167 titles concentrate in exactly one canonical chapter** — pure alias drift
  (e.g. the PARTS table's abbreviated "EM Theory of Light" vs the fuller 'Electromagnetic
  Theory of Light'; "Coil Comparison" vs 'Ch XVII: Comparison of Coils'; "ESU vs EMU" vs
  'Comparison of Electrostatic and Electromagnetic Units'). Of the 28 mixed titles, ~14 still
  show a dominant chapter at ≥0.85 fraction; only ~7 are genuinely ambiguous (dominant fraction
  < 0.7: 'general equations of the electromagnetic field' 0.57, 'induction and electromagnetic
  theory' 0.42, "ampere's force investigations" 0.56, 'electromagnetism' 0.62,
  'ohm's law analysis' 0.50, 'circular coils' 0.62, 'on the relation of electrification to
  liquid action' 0.67).
- **Scope split of the 1530 sites:** citing only articles <667: **1197**; citing only articles
  ≥667: **318**; mixed scope: **3**; no integer articles on the decorator: **12**.

**Recommendation: a bulk-title-normalization work package, not bare acceptance.** Grounds:

1. The large majority of findings is mechanically resolvable with article-validated aliasing
   (139/167 titles unambiguous; the article numbers, which the ledger has certified, arbitrate
   the intended chapter).
2. The rule's own docstring anticipates remediation: severity is MEDIUM only because "~1.5k
   drifting call sites predate this rule and are unowned; **promote to HIGH after a dedicated
   remediation wave**." Acceptance is therefore not a stable end state — any future wave turns
   the residue HIGH, and permanent MEDIUM noise masks genuine new drift.
3. Acceptance-with-annotation would itself require building a waiver ledger and amending the
   rule's promotion clause — comparable effort to fixing, with weaker gate semantics.

**Package shape (proposed):**
- **WP-R8a (alias-validated codemod, effort L for the <667 bulk; M for the 318 in-scope
  sites):** introduce a chapter **alias registry** keyed to the canonical PARTS titles —
  `check_coverage.py` remains the single source of truth; the registry absorbs near-miss
  synonyms — then rewrite decorator `chapter=` strings by validated mapping (each rewrite
  checked against the decorator's own article numbers). Dry-run the codemod and report the
  residue before committing anything.
- **WP-R8b (adjudication, effort M):** per-site review of the ~28 mixed-concentration titles,
  especially the ~7 ambiguous ones, using the Treatise table-of-contents as arbiter; correct
  article↔chapter pairs where the article number itself is wrong.

**Evidence that decides bulk-vs-acceptance (what to demand before executing WP-R8a):**
- The single-chapter concentration table above, re-run at execution time (cheap, AST-only).
  If ≥85% of findings remain unambiguously mappable, bulk normalization wins on cost.
- A ~30-site manual sample audit across the low-fraction titles confirming that **article
  numbers, not chapter strings, are ground truth** against the Treatise TOC. If the audit finds
  double drift (article numbers also wrong), normalization would bless bad metadata — in that
  case downgrade to acceptance-with-waiver-ledger for the affected subset.
- Codemod dry-run residue count (mechanical replacements vs manual remainder).

**Scope-lock note for R8:** the 1197 + 3 + part-of-12 out-of-scope sites fall under the §6
precondition like everything else in this plan. The **318 in-scope sites** (functions citing
only 667–866) are metadata hygiene *inside* the locked scope and could, in principle, run as a
post-G4 in-program pass — but this plan recommends deferring them until after G4 adjudication so
the frozen G3 baseline is not disturbed mid-review.

---

## 5. Effort summary and wave ordering (proposed backlog program)

| Wave | Contents | Findings cleared | Dependency |
|---|---|---|---|
| **B0 — Governance** | planning-analysis-v2 scope review (§6); policy decision on `theory_class="historical_exposition"` + R6 exemption/downgrade in the lint (prereq for the seven (b) items); confirm implementer ≠ certifier pairing for the backlog program | — (gate precondition) | user/orchestrator authorization |
| **B1 — Structural theater first** | #8 (R1 solenoidal computed-verdict refactor), #13 (R2 remaining_gaps computed-verdict refactor) | 2 HIGH | B0 scope approval only (no policy dependency) |
| **B2 — Implement real computations** | #2 (Art 45), #9 (Art 404 proof), #11 (Art 76) — disjoint modules, parallelizable; each with independent oracle + pinning tests | 3 HIGH | B0; MATHEMATICA/PHYSICUS-style implementation + QUALITAS-authored tests |
| **B3 — Exposition reclassification** | #1, #3, #4, #5, #7, #10, #12 via (b); #6 via (c) strip-and-fold | 6 HIGH + 1 HIGH | B0 policy decision landed |
| **B4 — Doc & test-golden hygiene** | D-1, D-2 abampere relabels (Arts 647–662); the five R7 test MEDIUMs (provenance/CONST) | 0 HIGH; 5 MEDIUM; doc defects | after `tests/articles/reference_values.json` migration settles |
| **B5 — Chapter drift** | WP-R8a codemod + WP-R8b adjudication (§4.2), sequenced after B1–B4 so the lint baseline movement is attributable | up to 1530 MEDIUM | B0 (out-of-scope sites); post-G4 adjudication for the 318 in-scope sites |

Effort key: S ≤ half agent-day; M ≈ 1–2 agent-days including tests; L ≥ a week with review.
Totals: HIGH side — 2×M (B1) + 3×M (B2) + 8×S (B3) = **13 HIGH findings addressed**; plus 2×S
doc entries (D-1/D-2), 5×S test-golden provenance items, and the L-scale R8 package.

Exit criterion for the backlog program (proposed): `python scripts/anti_theater_lint.py`
reports **0 HIGH** with every rule at full strength; R8 either cleared or explicitly
waiver-ledgered per §4.2 evidence; ledger regenerated and reconciled (articles whose citations
were stripped under strategy (c) honestly leave the coverage counts).

---

## 6. Gate precondition (binding)

Per `docs/LAST200_STAGE5_AGENT_ORCHESTRATION.md` §5 Ground rules: **"Scope lock: 667–866 only.
Anything outside requires planning-analysis-v2 scope review."** Therefore:

1. **Nothing in this plan may be executed under the 667–866 program's gates (G0–G4).** The
   in-scope program is G3-PASS / G4-READY-PENDING-HUMAN, and its gate structure, evidence
   ledger, and frozen baselines (`article_evidence_report_G3_BASELINE.json`, certification
   records) must not absorb out-of-scope change.
2. Execution requires a **planning-analysis-v2 scope review** admitting Arts <667 work as a
   **separate program** with its own gate structure, its own implementer ≠ certifier pairings,
   and its own evidence ledger (the whole-treatise `article_ledger.json` will move when
   citations change; that movement is the backlog program's responsibility, not the 667–866
   program's).
3. Until that review happens, this document is the scheduled record demanded by examiner
   recommendation R7 — the backlog is **known, enumerated, costed, and ordered**, and no
   finding in it is disputed.

---

## Appendix A — Provenance of this plan's evidence

- Lint run: `python scripts/anti_theater_lint.py` (also via `--json`), repo root, 2026-08-22;
  364 files; 1548 findings (13 HIGH / 1535 MEDIUM); rule histogram R1=1, R2=1, R6=11, R7=5,
  R8=1530, all others 0.
- Source inspection for article attribution: `maxwell/config/conventions.py` (292–324),
  `maxwell/core/charge.py` (97–146), `maxwell/electromagnetism/theory/remaining_gaps.py`
  (827–958), `maxwell/electrostatics/force_theory.py` (345–464, 804–924),
  `maxwell/electrostatics/phenomena.py` (1108–1185), `maxwell/fields/solenoidal.py` (71–107,
  464–501), `maxwell/materials/hysteresis.py` (414–475), `maxwell/physics/gauss.py`
  (695–748), `maxwell/physics/magnetostriction.py` (550–603).
- Abampere entries: `maxwell/electromagnetism/current_sheets/sheet_theory.py` and
  `surface_currents.py` (full read); precedent fix pattern from
  `maxwell/electromagnetism/components/circular_coils.py` (lines 34–50); QUALITAS Wave-8c
  record in `LAST200_STAGE5_AGENT_ORCHESTRATION.md` §6 Wave 8.
- R8 analysis: AST re-parse of all `maxwell/` `@maxwell_cite` decorators cross-referenced
  against `check_coverage.py` PARTS ranges (alias-concentration and scope-split statistics in
  §4.2); canonical title normalization per `anti_theater_lint._normalize_chapter_title`.
- Citation policy check: `maxwell/meta/citation.py` — `theory_class` valid set is
  `{"maxwell_original", "user_original", "standard_math"}`; "historical_exposition" does not
  yet exist.
- No file other than this plan was created or modified by ARCHITECTUS in Wave 9b; `tests/` was
  not touched (concurrent `tests/articles/reference_values.json` edit in progress elsewhere).

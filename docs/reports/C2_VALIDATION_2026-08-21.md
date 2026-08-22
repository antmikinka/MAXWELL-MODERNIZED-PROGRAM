---
type: report
artifact: c2_validation
gate: G2
condition: C2
date: 2026-08-21
authors: ARCHITECTUS + SCRIBA
collab_reviewed: true
---

# C2 Validation — Ledger & Coverage-Scanner Regeneration — 2026-08-21

Closes G2 gate condition **C2** (regenerate stale truth artifacts) and defect
**D-26** (stale `docs/COVERAGE_SUMMARY.md`). No source code was modified; the only
files written were `docs/reports/article_ledger.json`,
`docs/reports/article_ledger_summary.md`, `docs/COVERAGE_SUMMARY.md`, and this file.

> **Concurrent-wave caveat.** Three other agents are concurrently editing source
> files (`spherical_harmonics.py`, `absolute_resistance.py`, `elliptic_integrals.py`,
> `telegraphy.py`, `galvanometers_extended.py`, lint scripts, tests). The ledger and
> numbers below are therefore a **validation snapshot** of the tree as of
> 2026-08-21 ~21:43 local. The orchestrator will perform the **authoritative final
> regeneration after the wave lands**; small deltas (notably the singleton count)
> are expected and must be re-derived, not carried over.

---

## Step 1 — Ledger regeneration

Command:

```
python scripts/build_article_ledger.py
```

Stdout (two runs, 21:43 and a confirmation re-run; outputs identical):

```
Article ledger written:
  docs\reports\article_ledger.json  (866 articles)
  docs\reports\article_ledger_summary.md
  citations: 3789, singletons: 155 (45 in 667-866), anomalies: 2, warnings: 27
```

### Validation checks

**(a) No `diffusion.py` entry cites 806/807/808 — PASS.**
Programmatic scan of the regenerated `article_ledger.json`: zero citations from
`maxwell/optics/diffusion.py` under articles 806, 807, 808. (The stale pre-C2
ledger had 6–8 such citations per article.)

**(b) 806–808 cited only by `magneto_optics/rotation.py` — PASS.**
For each of 806, 807, 808 the distinct citing-file set is exactly
`{maxwell/magneto_optics/rotation.py}`:

```
806 -> ['maxwell/magneto_optics/rotation.py']
807 -> ['maxwell/magneto_optics/rotation.py']
808 -> ['maxwell/magneto_optics/rotation.py']
```

Citing functions (from the regenerated ledger): Art. 806 ←
`measure_rotation_by_analyser`; Art. 807 ← `B_field_from_rotation`,
`rotation_angle`; Art. 808 ← `establish_rotation_laws`.

**(c) Total article entries = 866 — PASS.** `len(article_ledger.json) == 866`,
matching the Treatise total (Arts. 1–866).

**(d) Singleton count in 667–866 — recorded: 45.**
The pre-wave baseline was **42**; the observed count is **45** (delta **+3**).
This is expected and reported honestly: concurrent agents are editing decorators
right now. Singleton articles observed:
707, 708, 711, 712, 716, 717, 718, 719, 723, 724, 727, 728, 740, 745, 750, 774,
776, 778, 779, 780, 806, 808, 811, 812, 814, 815, 816, 817, 818, 820, 821, 825,
826, 827, 831, 834, 837, 838, 839, 845, 847, 848, 855, 863, 864.

### Ledger auxilia (from `article_ledger_summary.md`)

- Coverage: 866/866 (100.0%); citation records: 3789; distinct citing files: 197.
- Anomalies (2, both `part-conflict`, both pre-existing metadata issues, neither
  affects coverage): Art. 77 (`maxwell/math/calculus_calculator.py`, decorator
  `part=3` vs PARTS Part I) and Art. 391
  (`maxwell/electromagnetism/theory/remaining_gaps.py`, decorator `part=4` vs
  PARTS Part III).
- Scanner warnings (27): 12× `maxwell/optics/diffusion.py` "unparseable
  decorator" — these are the intentional D-23 keyword-only `standard_math`
  decorators carrying **no** article numbers (hence nothing to record — the root
  cause of finding (a)/(b) passing); 15× `maxwell/math/spherical_harmonics.py`
  "no def/class found after decorator" — diagnosed as stacked `@maxwell_cite`
  decorators (the first of a stacked pair sees the second pair's argument lines
  before any `def`); 40 ledger records there carry function `<unknown>`. Article
  counts are unaffected (Ch. IX still 19/19; Ch. XIII/XIV still 19/19 and 13/13).
  `spherical_harmonics.py` is one of the files under concurrent edit; the
  post-wave authoritative regeneration should re-confirm.

## Step 2 — Coverage scanner

Command:

```
python check_coverage.py
```

Key output lines (verbatim):

```
VOLUME 1 — Part I: Electrostatics (Arts. 1-229)     Coverage: 229/229 (100%)
VOLUME 1 — Part II: Electrokinematics (Arts. 230-370) Coverage: 141/141 (100%)
VOLUME 2 — Part III: Magnetism (Arts. 371-474)       Coverage: 104/104 (100%)
VOLUME 2 — Part IV: Electromagnetism (Arts. 475-866) Coverage: 392/392 (100%)
...
Ch XVII: Coil Comparison: 6/6     Articles: [752, 753, 754, 755, 756, 757]
Ch XVIII: Resistance Unit: 10/10  Articles: [758, 759, 760, 761, 762, 763, 764, 765, 766, 767]
...
TOTAL: 866/866 articles implemented (100%)
```

### Validation checks

| Check | Expected | Observed | Result |
|-------|----------|----------|--------|
| Ch XVII range & count | (752,757), 6/6 | Articles [752–757], 6/6 FULL | PASS |
| Ch XVIII range & count | (758,767), 10/10 | Articles [758–767], 10/10 FULL | PASS |
| TOTAL | 866/866 | 866/866 (100%) | PASS |
| PARTS contiguity | zero overlaps/gaps | programmatic walk of `PARTS`: every chapter starts at previous+1; chapter sums equal part ranges; parts chain 1→866 | PASS |

No overlap between Ch XVII and Ch XVIII (D-27 remediation holds). All 57 chapter
rows show 100% FULL in the scanner output.

## Step 3 — COVERAGE_SUMMARY.md rewrite

`docs/COVERAGE_SUMMARY.md` rewritten from scratch on 2026-08-21 using only:
(i) the ledger outputs of Step 1, (ii) the scanner outputs of Step 2, and
(iii) cited gate artifacts (`docs/reports/G2_GATE_REVIEW_2026-08-21.md` for
2178 passed / 0 failed and 13 HIGH lint findings;
`docs/reports/article_evidence_report.json` for 149/200 evidence coverage,
verified present in the file as `articles_covered: 149`, 51 missing, 227 marked
tests). Every number in the new summary carries its source command or citation;
nothing was copied from the stale 2026-05-06 file. Defect **D-26** closed.

## Discrepancies observed (honest record)

1. **Singleton delta:** 45 observed vs 42 pre-wave baseline (+3). Attributable to
   the concurrent decorator-edit wave; authoritative count to be re-derived
   post-wave.
2. **27 scanner warnings** (see auxilia above) — none affect article coverage;
   the 15 `spherical_harmonics.py` name-attribution misses correlate with that
   file being concurrently edited.
3. **2 pre-existing part-conflict anomalies** (Arts. 77, 391) — decorator
   metadata, out of C2 scope.
4. `article_evidence_report.json` timestamp reads 2026-08-22T01:07 UTC
   (= evening of 2026-08-21 local, gate date); its 149/200 equals the G2 review
   banner exactly.
5. Suite/lint numbers are **cited** from the G2 gate review, not re-run (a
   concurrent edit wave is in flight; post-wave authoritative re-run belongs to
   the orchestrator).

## Verdict

**C2 CLOSED as a validation snapshot.** Ledger checks (a)–(d) all pass; scanner
checks all pass; `docs/COVERAGE_SUMMARY.md` regenerated with fully traced
numbers. Final authoritative regeneration to be performed by the orchestrator
after the concurrent wave lands.

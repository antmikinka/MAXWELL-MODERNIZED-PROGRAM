---
gate: G2
program: ensure Arts 667-866 (last 200)
date: 2026-08-21
reviewer: independent gate reviewer (fresh context, read-only audit)
verdict: CONDITIONAL PASS
suite: 2178 passed / 0 failed / 0 errors
evidence_coverage: 149/200
---

# G2 Gate Review — Arts. 667-866 — 2026-08-21

**Verdict: G2 CONDITIONAL PASS** — all theater/stub/green-suite/lint criteria are
independently verified met; two precisely scoped shortfalls remain (4 residual
meta-only/T0-class articles; stale ledger artifact). Conditions C1-C3 are mandatory
before G3 counting begins; C4-C6 are strongly recommended.

Audit method: fresh context; no prior report trusted; every claim below re-derived
from the tree, the test suite, the lint, and independent AST/grep census. Only write
performed: this report. Suite run command:
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest` (full suite).

---

## Check 1 — Full suite: MET

```
2178 passed, 0 failed, 0 errors, 3 warnings in 158.01s (0:02:38)
```

* The 3 warnings are pre-existing `scipy.integrate.IntegrationWarning`s in
  `maxwell/math/calculus_calculator.py:686` (line-integral tests), unchanged from
  Wave-2; no new warnings.
* Terminal evidence-map banner: `covered 149/200  missing 51  marked tests 227`.

## Check 2 — Zero T0: MET for stubs/prose; 4 meta-only articles remain

### Named theater remediations — all landed (verified in source)

| Item | File | Evidence of remediation |
|---|---|---|
| Art 820 `return True` | `magneto_optics/energy_analysis.py` | `prove_real_rotation_required` computes `faraday_round_trip=2θ`, `natural=0`, `discriminant=2θ`, `requires_real_rotation: bool(discriminant != 0.0)` |
| Art 821 prose dict | same | `summarize_magneto_optic_results` all-numeric, derived from sibling computations |
| Arts 841-858 invented scores | `molecular/competing_theories.py` | `experimental_agreement` has **0 occurrences repo-wide**; replaced by `_ampere/_weber/_neumann/_maxwell_computed_residuals` batteries (dipole-axis 2m/r³, RK4 energy conservation, reciprocity vs elliptic closed form, historical wave speed); verdicts thresholded from residuals; `diamagnetic_response` computes M=χH (D-18) |
| Rigged verdict + water datum | `philosophy/medium_check.py` | `"verified": bool(all_agree)` computed; rigged row (K=80, n=9.0) removed; honest dataset (air, paraffin, sulfur, water_optical K=1.776/n=1.3330) with provenance; water_static excluded with dispersion reason; `media_data` injectable; `_wave_impedance` = √(μ/K), the baseless 4π/c removed (D-38) |
| Art 831 prose notes | `vortex_engine/vortex_lattice.py` | computes `wave_speed=√(elastic_constant/mean_density)`, wave_speed_over_light, energies; `verify_vortex_gear_condition` raises `ValueError` for <2 vortices (was vacuous True), computed alternation loop |

### Independent stub scan

AST scan of **every** decorated function citing 667-866 across `maxwell/`: 6 pattern
hits, all triaged as computed branches / degenerate-case guards, none stubs:

* `instruments/dynamometers.py:125` — `return False` guards `tau_1==0`; verdict
  `bool(abs(exponent-2.0)<1e-9)` computed.
* `electromagnetism/components/circular_coils.py:453` — `verified: False` early-exit
  only for zero center field; main verdict `bool(variation_z < tolerance)`.
* `electromagnetism/vis/circular_fields.py:321` — `verified: False` only on failed
  trace; main verdict computed (tolerance `psi_variation < 1.0` is generous — G3
  quality note).
* `optics/metals.py:869` — `return False` guards ω/ε ≤ 0; verdict computed.

No remaining `"verified": True` literals in any file citing 667-866 (remaining
literals are in files citing Arts 177/578/581/582/590 — out of scope — or in
docstrings).

### Residual T0-class articles (the one strict shortfall)

Ledger (`docs/reports/article_ledger.json`) still flags **Arts 694, 695, 765, 766**
as `meta_only=True` (cited only by `verify_*`/`analyze_*` functions). Under the
Stage-2 tier definition these are T0-class. Note: the 765-767 `verify` battery
(`calibration/absolute_resistance.py`) now computes genuine independent checks
(perturbation-verified in `tests/test_lint_remediation_last200.py`, qualifying test
marked article 767), so this is a classification/citation gap, not stub code.
Arts 759, 762, 767 are covered by the new lint-remediation qualifying tests.

## Check 3 — Anti-theater lint: MET in scope

`python scripts/anti_theater_lint.py` → 346 files scanned, **13 findings, 13 HIGH,
exit 1** (expected with findings present; the gate criterion is in-scope findings).
Rule counts: R1=1, R2=1, R6=11.

Every finding's citation set was AST-extracted independently:
Arts {12-19}, 45, 50-55, 65×2, 76, 393-394, 404×2, 444, 447, 552 — **all < 667**.
Zero HIGH findings in 667-866. The documented out-of-scope set (13 findings) is
exactly reproduced; no new findings, none suppressed.

Caveat (recorded, non-blocking for G2): the lint implements R1-R6 only, of the ten
rules specified in Stage-3 §5.3. In particular no hardcoded-constant rule (the D-33
class) exists yet.

## Check 4 — Evidence map: reconciled exactly, zero discrepancy

* Plugin report `docs/reports/article_evidence_report.json` regenerated by the Check-1
  suite run (conftest plugin emits on every run — sanctioned side effect; prior
  artifact sha256 `2da36a6e…`). Regenerated coverage: **149/200 covered, 51 missing,
  227 marked tests** — identical to the pre-run artifact.
* Independent census: regex census of `@pytest.mark.article(...)` across `tests/`
  (deduped), 8 files:

  | File | Articles |
  |---|---|
  | test_articles_math_spine_691_706.py | 23 (670-679, 691-705) |
  | test_articles_instruments_707_729.py | 23 (707-729) |
  | test_articles_ratio_v_768_780.py | 13 (768-780) |
  | test_articles_optics_781_805.py | 25 (781-805) |
  | test_articles_magneto_optics_vortex.py | 26 (806-831) |
  | test_articles_molecular_832_866.py | 35 (832-866) |
  | test_defects_s1.py | 6 (702, 751, 777, 801, 802, 812) |
  | test_lint_remediation_last200.py | 6 (623-625 out-of-range + 759, 762, 767) |

* **Bidirectional match is exact**: 149 = 149; the 51-missing sets are identical:
  667-669, 680-690, 694-695, 706, 730-750, 752-758, 760-761, 763-766. No marks outside
  1..866; five articles (702, 777, 801, 802, 812) are legitimately double-marked
  (per-article file + defect-regression file) and dedupe correctly.
* True evidence coverage: **149/200 (74.5%)**. Discrepancy vs plugin report: **none**.

## Check 5 — S1 defect regression: MET, 5/5 green, xfails gone

`tests/test_defects_s1.py` — five named tests, all green within the 2178:

1. `test_regression_D03_art777_correction_halves_v` [article(777)]
2. `test_regression_D04_art812_delta_n_identity` [article(812)]
3. `test_regression_D01_art801_diffusion_time_copper_and_roundtrip` [article(801, 802)]
4. `test_regression_D02_art702_near_axis_psi_and_curl` [article(702)]
5. `test_regression_D05_art751_force_equals_I2_dMdx` [article(751)]

`xfail` appears only in the module docstring ("The xfail markers have now been
removed"); repo-wide grep confirms no live xfail markers on these tests. The
Stage-4 §7 xfail→pass diff requirement is satisfied.

## Check 6 — Stage-3 S2 residuals (triage; not G2 criteria)

**Verified remediated during this audit** (source inspected): D-06, D-07, D-08, D-09,
D-10, D-11, D-18, D-19 (`prove_ratio_is_velocity` now derives dimensions symbolically;
measurement separated into `historical_v_anchor`), D-20 (ring geometry I=qω/2π),
D-21, D-23 (Beer-Lambert decorators stripped to `standard_math`, arts=[]), D-27
(`check_coverage.py` chapter table now Ch XVII=752-757 / Ch XVIII=758-767, no
overlap), D-33 **in scope** (0 hardcoded-c literals in ratio_v/combined.py,
ratio_v/theory.py, circular_polarization.py, energy_analysis.py,
magnetic_rotation.py; the remaining literals in `math/potential_theorems.py` cite
only Arts 79-244 — out of 667-866 scope), D-38.

**Partially closed**: D-25 (765/766 still meta-only), D-28 (51 articles still lack
marked tests), D-24 (conftest quarantine mechanism exists and is wired into the G3
count, but **no quarantine-marked tests exist**; 740/745/750 simply uncovered).

**Open / not verified remediated — schedule in G3**: D-12 (Weber ½ convention),
D-14 (673-675 elliptic truncation), D-15 (709 torsion units), D-16 (707-709 c-factor
clash), D-17 (755-757 Joule-balance citation), D-22 (824-826 dimensional heuristics),
D-26 (COVERAGE_SUMMARY.md still says "2026-05-06, 1795 tests" — regenerate), D-39
(`elliptic_integrals.py:307` `parameter()` helper still hijacks Art 702 — trivially
closable), D-40/41/42 (S4).

## Check 7 — Honesty checks (3 files): 3/3 PASS

* **test_articles_optics_781_805.py** — independent oracles hand-derived: Stokes
  5-3-0-4 identity, Malus cos²(π/3)=0.25, Poynting c/4π golden, Hagen-Rubens checked
  against an independent Fresnel oracle `R=[(1-n)²+n²κ²…]/…` with n=√(2πσ/ω),
  radiation-pressure unit goldens, Fresnel wave-normal equation. Provenance in
  docstrings; sign/negation-sensitive asserts. Observation: Arts 791-794 are
  double-marked (polarization + radiation pressure) while Stage-4 §3.5 maps radiation
  pressure to 804-805 — mapping hygiene for G3.
* **test_articles_molecular_832_866.py** — oracles written from scratch: `_biot_savart_loop`
  quadrature, dipole-tensor field, CODATA k_B=1.380649e-16, Weber factors with
  c_W=√2·c, Neumann quadrature vs scipy elliptic closed form, L=4πR(ln(8R/a)−2),
  sphere B=(8π/3)M. Anti-theater mutation test present: injecting
  ("water", 80.4, 1.3330) flips `verified` to False with error≈0.8513.
* **test_articles_magneto_optics_vortex.py** — hand goldens (T=0.28125π, |L|=0.1875π);
  Art-820 test asserts discriminant=2θ **and** θ=0 → `requires_real_rotation is False`
  (kills any `return True` regression); Art-821 asserts every entry float and
  cross-consistent with the Art-815 machinery.

Deviation recorded: reference goldens are inlined in test files; the central
`reference_values.json` (Stage-4 Decision D-05 / anomaly A11) **does not exist yet**.

## Additional findings

1. **Ledger staleness (discrepancy resolved)**: `article_ledger.json` (mtime 17:42)
   still records `diffusion.py` functions under Arts 806/807/808, but the current
   tree (mtime 19:56) carries `arts=[]` `standard_math` decorators there; 806-808 are
   now cited only by `magneto_optics/rotation.py` (legitimate). Wave-2 anomaly A2 is
   remediated in code; the ledger was not regenerated afterwards. "200/200
   ledger-verified" therefore cannot be certified from the current artifact.
2. **Durability**: 74 working-tree paths (50 modified + 24 untracked) are uncommitted
   on top of `fce0348`. All remediation evidence exists only on disk.
3. `docs/COVERAGE_SUMMARY.md` stale (D-26 open).

---

## Verdict: G2 CONDITIONAL PASS

| Stage-2 §4.3 exit criterion | Status |
|---|---|
| Zero T0 articles in range | **PARTIAL** — no stub/prose survivors; 4 meta-only (694, 695, 765, 766) |
| 200/200 article-specific computation, ledger-verified | **NOT CERTIFIABLE** — ledger stale; code largely compliant |
| Existing tests green | **MET** — 2178 passed, 0 failed, 0 errors |
| Anti-theater lint green | **MET in scope** — 13 HIGH, all Arts <667; 0 in-scope |
| All three theater items remediated | **MET** — verified in source + qualifying tests |
| Stage-4 CI contract (S1 xfail→pass) | **MET** — 5/5 green, xfails gone |

FAIL would be inaccurate: no verification theater survives in scope, the suite is
green, and every named remediation was re-verified from source. Unconditional PASS
would overstate: Stage-2 §4.3 literally requires zero T0 and ledger verification.

### Conditions (mandatory before G3 counting)

* **C1** — Close the 4 meta-only articles 694, 695, 765, 766: attach article-specific
  computation (physics-content `calc_*`) or record a formal re-tier adjudication; add
  qualifying tests (none of the four currently has one).
* **C2** — Regenerate `docs/reports/article_ledger.json` and
  `docs/COVERAGE_SUMMARY.md` from the current tree; re-run the ledger-vs-tree diff
  (clears A2-ledger staleness and D-26).
* **C3** — Land central `reference_values.json` (Stage-4 Decision D-05 / anomaly A11)
  and begin migrating inlined goldens before G3 test counting.

### Conditions (strongly recommended)

* **C4** — Expand anti-theater lint R1-R6 → the full ten rules of Stage-3 §5.3
  (prioritize a hardcoded-constant rule covering the D-33 class).
* **C5** — Commit the 74-path working tree.
* **C6** — Adjudicate or quarantine D-24 (telegraphy anachronisms, Arts 740/745/750);
  the conftest quarantine mechanism is built but unused.

## G3 readiness

* Qualifying tests required for **51 articles**: 667-669, 680-690 (boundary/cylinder
  clusters), 694-695, 706, **730-750** (21-article Ch XVI observations cluster — the
  largest single gap, gated by the D-24 adjudication of C6), 752-758, 760-761,
  763-766 (Ch XVII-XVIII coil-comparison/resistance cluster).
* Critical path per Stage-2 §4.4: WP-1.1/1.2 (scanner/ledger truth — C2) →
  WP-2.2/2.4 (reference values, plugin hardening — C3) → WP-3.1 (article-specific
  computation for the 4 meta-only — C1) → WP-4.3/4.7 (qualifying-test wave 3 for the
  51) → WP-5.1 → G4.
* G3 should also schedule the open S2 physics-correctness defects: D-12, D-14, D-15,
  D-16, D-17, D-22; and the trivial closures D-26 (regenerate) and D-39 (remove the
  Art-702 hijack decorator on `parameter()`).

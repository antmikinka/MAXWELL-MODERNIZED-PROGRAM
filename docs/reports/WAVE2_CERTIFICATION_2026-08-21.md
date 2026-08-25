# Wave 2 Certification Record — 2026-08-21

**Certifier:** QUALITAS (sole certifier; implementer ≠ certifier, Stage 2 §5.4)
**Scope:** Wave-2 bundles — PHYSICUS (Arts. 806-831), INSTRUMENTUM (707-729), CIRCUITUS (768-780), MATHEMATICA (spine 670-679/691-693/696-705 subset), ARCHITECTUS (28 `part=` metadata fixes + adjudication table)
**Method:** Full re-run, conftest integrity audit, anti-theater rubric (Stage 3 §5.3 + Stage 4 §2.3/§2.5), independent AST parse of the evidence map, S1 regression re-run. Trust nothing; recompute oracles by hand where feasible.

## 0. Suite results (re-run twice by QUALITAS)

| Run | Command | Result |
|---|---|---|
| Full suite #1 | `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/ -q` | **2059 passed, 0 failed, 0 errors** in 129.84 s (3 warnings: scipy quad, pre-existing) |
| S1 guards | `... pytest tests/test_defects_s1.py -v` | **5/5 passed** (D-01..D-05 regression guards green) |
| Full suite #2 (evidence regeneration) | as #1 | **2059 passed, 0 failed** in 131.94 s |

Arithmetic reconciliation: pre-wave baseline 1952 + 107 new tests (29 magneto-optics/vortex + 29 instruments + 27 ratio-V incl. 9 parametrized anchor cases + 22 math spine) = **2059**. No silent skips, no xfails, no quarantines.

## 1. Conftest integrity check (Task 2)

`git diff HEAD -- tests/conftest.py` shows an **addition-only** diff: +112 lines, zero deletions, zero modifications of pre-existing lines. The P0 article-evidence plugin is present in full and was verified clause-by-clause against Stage 4 §2.2:

- marker registration (article/regression/quarantine) — intact;
- collection-time validation (int check, 1..866, **rejects bools** — stricter than spec) — intact;
- scope fence 667-866 + quarantine exclusion — intact;
- UsageError hard-fail on invalid markers (errors aggregated, not first-offender) — intact;
- evidence JSON emission with no-clobber guard on USAGE/INTERNAL error — intact (hardening, not weakening);
- report path anchored to the tree — intact.

**Verdict: INTACT — no weakening detected; no repair required.** The mid-session touch reported by one agent left no degrading trace. sha256 of certified conftest: `af77db057118bd86561c2a39a16164525da81e876c15d401fb25dfd8047ab519` (354 lines).

## 2. Anti-theater rubric (Task 3)

Criteria (Stage 3 §5.3 rules 1-10; Stage 4 §2.3 AST rubric; §2.5 tolerance classes): (a) no function-vs-self or implementation-echo comparisons; (b) no hardcoded verdicts / literal-True-only asserts; (c) no tolerance laundering (EMPIRICAL hiding TIGHT/STANDARD-class checks); (d) golden values require provenance; (e) no tautologies. ≥5 tests per file audited in depth; starred (★) oracles recomputed by hand.

### 2.1 tests/test_articles_magneto_optics_vortex.py — **PASS**
- 29 tests; every test carries `@pytest.mark.article(N)`, N ∈ 806..831 (all 26 articles covered).
- Deep audits: art807★ (θ = 0.020·(π/10800)·1000·10 = π/54 ✓), art808★ (resolved field 1000·4/5 = 800 G ✓), art818★ (CGS energy E²V/8π = 1 for V = 8π ✓), art819★ (2n²−4n−6: disc 64, roots {3,−1} ✓), art822★ (T = (π/4)·2·9·(1/16) = 0.28125π; |L| = 0.1875π; T = ½|L|ω ✓), art825★ (v·J = 32 ✓), art826★ (24.75 hand case ✓), art830 (Verdet table provenance: Maxwell 1873 Vol. II p. 468; observed 592/768/1000/1234/1704, formula-I 589/760/1000/1234/1713), art830-inv-square★ (θλ²: 592·6.563² = 25499.2 ✓; independent in-test LSQ oracle), art831★ (wave speed √(ρc²/ρ) = c ✓).
- (a) art815 cross-compares two modules but both are independently pinned to the analytic c·VBλ/(πn²) — not self-echo. (b) bool asserts (`requires_real_rotation`, `agrees`) always cohabit with numeric approx asserts — rubric satisfied. (c) EMPIRICAL confined to Verdet historical data with explicit provenance. (d)/(e) clean.
- Notes: none material.

### 2.2 tests/test_articles_instruments_707_729.py — **PASS**
- 29 tests (30 marks); N ∈ 707..729 (all 23 articles covered).
- Independent oracles verified genuine: `_biot_savart_axis` is a true line-integral quadrature (on-axis z-component is φ-constant ⇒ quadrature is analytically exact; the 1e-6 tolerance is conservative, not laundered); `_solve` is an independent Newton iteration for torque balances (D-15 guard).
- Deep audits: art707★ (G = 2π·100/10 = 20π ✓), art709 (residual + independent Newton root ✓), art713★ (B = 32πnI/(5√5 a) ✓; Richardson-extrapolated B″(a) = 0; quartic flatness coefficient 144/125 = 1.152 hand-derived ✓), art713-far★ (dipole B·z³ → 4πnIa² ✓), art718★ (d/dR[√R/(R+R_ext)] = 0 at R = R_ext ✓), art727★ (F = 4π·50·20·10·0.25 = 10000π = 31415.926535897932 ✓; work identity F·ℓ₂ = M_total·I² ✓), art716-c-pin (EMU abampere = c × Gaussian/statampere field — D-16 reconciliation pinned ✓).
- (b) one `verify_force_proportional_to_I_squared() is True` backed by numeric square-law asserts. (c) no EMPIRICAL declared or used. (d) goldens provenanced (incl. g = 980.665 cm/s²).
- Notes: lines 188-189 assert the same comparison twice (rel 1e-4 then 1e-6) — redundant, harmless.

### 2.3 tests/test_articles_ratio_v_768_780.py — **PASS**
- 27 test items (18 functions + 9 parametrized anchor cases, each with its own `pytest.mark.article`); N ∈ 768..780 (all 13 articles covered).
- Deep audits: art769★ (all six ratio exponent vectors recomputed from the hand `_DIM` table: charge (0,1,−1), potential (0,−1,1), resistance (0,−2,2), capacitance (0,2,−2), inductance (0,−2,2) ✓), art769-sympy (symbolic oracle built from Coulomb + Ampère force laws, independent of code ✓), art770★ (I_ESU = qω/2π; H = qω/(va) ✓), art771★ (parallel 9 / series 2; v² commutation ✓), art773★ (RC invariant τ = R_EMU·C_ESU/c² = 0.55633 s ✓; wrong-branch guard √(R_ESU/R_EMU) = 1/c ✓), art776★ (wippe dim oracle (0,4,−4)→velocity ✓), art777 (fraction 1−exp(−t½/RC); engineered 0.5 case; never-amplifies ✓), art780 (direction guard ✓).
- (a) secondary route `convert_esu_to_emu` is a separately coded module (D-20) — legitimate independent cross-check. (b) bool verdicts (`verify_equals_c() is True`, `is_velocity_power`) always backed by numeric asserts. (c) EMPIRICAL 5e-2 used **only** on the v = 3.107e10 cm/s historical anchor (provenance: Weber-Kohlrausch 1856 / Treatise Arts. 775-778), exactly per §2.5; every method is additionally pinned at CONST.C with STANDARD — no laundering. (e) the shared-anchor parametrization builds readings at V_HIST — spec-mandated (§3.4 Maxwell-parameter golden); anti-circularity held by 9-way cross-method spread (1e-9) plus per-method STANDARD anchors at c.
- Notes: golden store inlined (documented deviation; no `tests/articles/reference_values.json` yet — see §5 item 10).

### 2.4 tests/test_articles_math_spine_691_706.py — **PASS** (two notes)
- 22 tests (36 marks); N ∈ 670..705; 694/695/706 deliberately unmarked (no touched code claims them — documented in file header).
- Deep audits: K(1/2)★ = 1.8540746773013719 reproduced from Γ(1/4)²/(4√π) (hand: 13.14515766/7.08981540 ✓) — oracle independent of both AGM and scipy; K(−1)★ = K(1/2)/√2 = 1.31102878 ✓; E(−1)★ = √2·E(1/2) = 1.91009889 ✓; Landen iteration to the π/2 fixed point ✓; Legendre relation ✓; self-GMD★ a·e^{−1/4} = 0.7788007830714049 ✓; thin-strip★ w·e^{−3/2} ✓; disjoint-GMD = d theorem (harmonic mean-value proof checked ✓); coaxial-ring far-field★ d(1+(a₁²+a₂²)/2d²) ✓; inductance correction★ 4πR·(1/4) = πR ✓; tensor-GL oracle gated by its own two-resolution convergence check before use ✓.
- Notes (rubric-adjacent, non-blocking): (i) `test_verify_and_analyze_elliptic_relations` asserts `res["verified"] is True` — backed by `legendre_error < 1e-10` + monotonicity sweep, rubric satisfied but the bool mirrors an implementation verdict; (ii) `test_spherical_harmonics_citation_split_keeps_part4_winning` is a metadata guard with **no numeric assert** — would fail a strict §2.3 AST enforcer; Article 675 remains numerically qualified via `test_off_axis_matches_biot_savart_oracle`. When the meta-rubric enforcer lands, this test needs a carve-out or a numeric spine.
- (c) tolerances honestly disclosed (1e-3 for the trapezoidal third-kind check is stated, not laundered). (d) SQUARE_GMD_GOLDEN provenance is a converged numerical derivation (n=500 tensor GL), documented — acceptable, flagged for the future reference-store migration.

**No file quarantined; no catastrophic rubric failure.**

## 3. Evidence map (Task 4)

`docs/reports/article_evidence_report.json` (regenerated by suite run #2, 2026-08-21T22:54:42Z):

- **Before (S1 certification): 6 articles / 200** (702, 751, 777, 801, 802, 812).
- **After: 88 articles / 200; 131 marked tests; gate_G3 = FAIL (112 missing)** — expected at this stage.
- Cluster completeness in the JSON: **707-729 = 23/23, 768-780 = 13/13, 806-831 = 26/26, spine subset = {670-679, 691-693, 696-705} = 23**, prior-6 all retained. 29 articles carry ≥2 marked tests.
- **Independent cross-check (QUALITAS AST parse, separate code path):** union of the four new files = 85 articles; ∪ S1 markers = 88; mark count 116 (new files, incl. multi-marks) + 6 (S1) + 9 (param cases) = 131. **Matches the plugin JSON exactly; no marker outside 1..866; no orphaned articles.**

## 4. Tier promotions granted (Stage 3 §6 REQ-T)

All promotions **T2 → T3** (passing marked numeric test with independent oracle, rubric-audited by QUALITAS). T4 withheld everywhere (requires symbolically independent SymPy verifier + page_verifier verdict + triple signature; the single art-769 sympy test is partial evidence only).

| Cluster | Articles | Count |
|---|---|---|
| F — magneto-optics/vortex (PHYSICUS) | 806-831 | 26 |
| Instruments (INSTRUMENTUM) | 707-729 | 23 |
| Ratio-V (CIRCUITUS) | 768-780 | 13 |
| Math spine subset (MATHEMATICA) | 670-679, 691-693, 696-705 | 23 |
| **Wave-2 total (union)** | | **85** |

S1-certified T3 articles 702, 751, 777, 801, 802, 812 remain valid (702/777/812 now carry additional wave-2 evidence). Reminder from S1: 752-754 and 803 were promoted on fix scope with markers only at 751/801/802 — they still lack their own marked tests.

## 5. Anomaly ledger (Task 6) — recorded, not fixed (scope guard)

| # | Anomaly | Recommended owner | Severity |
|---|---|---|---|
| A1 | `CONST.G_STANDARD` absent from `maxwell/config/constants.py`; Stage 4 §2.4 `cgs_constants` fixture cannot be built as specified | ARCHITECTUS (constants hygiene, D-33 line) | Med |
| A2 | `optics/diffusion.py` still mis-cites **Arts. 806-808** (Beer-Lambert/mean-free-path content on magnetic-rotation articles; D-23). WP-3.1 explicitly required removing these citations — not done | PHYSICUS | High (citation integrity) |
| A3 | `core/units/dimensions.py` `convert_esu_to_emu` docstring power table mixes ESU/EMU conventions (potential lumped at n = +1 though the worked example uses ×c, i.e. p = −1; cites 620/771-772 for Ch. XIX content spanning 768-781) | CIRCUITUS | Med |
| A4 | D-16 convention pin: `circular_coils.py` (Gaussian, statampere, explicit CONST.C) vs instruments (EMU, no c). Pinned numerically by `test_art_716_emu_statampere_c_convention`, but the repo-wide convention adjudication is still open | ARCHITECTUS + INSTRUMENTUM | High |
| A5 | Breaking signature changes without compat shims/versioning: `calc_solenoid_suction`, `optimize_galvanometer_sensitivity`, `determine_magnetic_force` (+current), `design_sensitive_galvanometer` (+mean_radius), `prove_ratio_is_velocity` (float→dict), `motivate_ratio_investigation` (dict value type) | ARCHITECTUS (API policy); INSTRUMENTUM/CIRCUITUS (changelog) | Med |
| A6 | `verify_spherical_harmonics` returns `verified=False`: normalization_error = 2.04e-2 (orthogonality is 1.0e-14 — a normalization-convention mismatch inside the verifier, re-verified by QUALITAS this session) | MATHEMATICA | Med |
| A7 | `force_theory.py` chapter-tag deferral (noted by ARCHITECTUS) | ARCHITECTUS | Low |
| A8 | ARCHITECTUS residual 21 ledger anomalies: 19 delegated/excluded (Part I/IV spherical-harmonics split, Arts. 128-146) + 2 adjudicated spans (Arts. 391, 77 by design) | ARCHITECTUS (+ MATHEMATICA for the split verdict) | Low |
| A9 | **QUALITAS finding:** G2 theater items NOT fully remediated — `philosophy/medium_check.py:255` still literal `"verified": True`; `molecular/competing_theories.py` still carries invented `experimental_agreement` scores; `calibration/absolute_resistance.py` improved (verdict now computed) but retains `velocity_check = True` "by construction" stub | PHYSICUS/MATERIA per WP-3.4/3.5 (escalate: G2 blocker) | High |
| A10 | **QUALITAS finding:** anti-theater static gate (WP-1.4) not wired into `run_quality_checks.sh` — no theater/lint rules present | ARCHITECTUS/QUALITAS | High (gate infra) |
| A11 | **QUALITAS finding:** central `tests/articles/reference_values.json` store (D-05/§2.5) still absent; all four wave-2 files inline goldens with provenance (documented deviation) — must consolidate before G3 | QUALITAS + cluster leads | Med |

## 6. Gate status vs Stage 2 G2 (honest assessment)

| G2 criterion | Status |
|---|---|
| Zero T0 articles in range | **NOT DEMONSTRATED** — 112 of 200 articles still lack any marked test; ledger tier burn-down not re-verified here |
| 200/200 article-specific computation (ledger-verified) | **NOT MET** — 88/200 evidence coverage |
| Existing tests green | **MET** — 2059/2059, baseline preserved exactly |
| Anti-theater lint green | **CANNOT BE MET** — the lint does not exist in `run_quality_checks.sh` (A10) |
| All three theater items remediated | **NOT MET** — 2 of 3 untouched + 1 residual (A9) |

**G2 verdict: NOT MET.** Wave 2 is a clean, theater-free increment (all four bundles PASS the rubric; conftest intact; S1 green), but the tree-wide theater remediation and the static gate are still outstanding and are now the critical path.

## 7. Repairs / quarantines

None required. conftest intact; no test file failed the rubric catastrophically; nothing quarantined; QUALITAS edited **no files** outside this certification record (tests/ and docs/reports/ domain respected; maxwell/ untouched).

*Certified by QUALITAS, 2026-08-21. Artifacts: this record; `article_evidence_report.json` (generated 2026-08-21T22:54:42Z); suite transcripts (2059 passed × 2 runs; 5/5 S1).*

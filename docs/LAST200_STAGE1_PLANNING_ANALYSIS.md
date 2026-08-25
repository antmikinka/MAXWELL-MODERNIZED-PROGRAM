# LAST 200 ARTICLES (667-866) — Stage 1 Planning & Requirement Analysis

**Pipeline stage:** 1 of 4 (Planning & Requirement Analysis)
**Date:** 2026-08-21
**Scope:** Part IV, Ch XII tail (Arts. 667-674) through Ch XXIII (Arts. 846-866) — 200 articles.
**Method:** Read-only codebase exploration (decorator parse of all 1,976 `@maxwell_cite` occurrences, test-import mapping, module sampling with line-level reads, pytest collection, verdict/SymPy registry inspection). No source was modified.

---

## 1. Executive Summary

### What "ensured implementation" means
Citation coverage is necessary but far from sufficient. `check_coverage.py` reports 866/866 because its scanner (`check_coverage.py:101-123`, regex at `:107`) counts an article as "implemented" if **any** `@maxwell_cite` decorator anywhere under `maxwell/` mentions its number — including decorators on visualization functions, on `verify_*`/`analyze_*` meta functions, and on functions that return hardcoded prose dictionaries. An article is **ensured** only when four evidences coincide:

1. **Semantic correctness** — the cited code computes what that Treatise article actually states (validated against the 1873 text / page images).
2. **Mathematical fidelity** — the formula is the article's formula, with correct CGS constants, not a heuristic substitute or a dimensionally inconsistent shorthand.
3. **Numerical verification** — at least one test named for the article asserts a known value, limit case, or identity.
4. **Cross-validation** — independent confirmation (SymPy symbolic check, second implementation, or page_verifier human verdict).

### Current confidence level: **LOW-MEDIUM** (evidence below)

| Evidence | Finding | Verdict |
|---|---|---|
| Citation coverage, 667-866 | 200/200 articles have ≥1 decorator; 42 articles have exactly 1 | ✅ necessary condition met |
| Chapter structure scanner | `check_coverage.py:89-90` defines Ch XVII as (752,761) overlapping Ch XVIII (758,767) — true Treatise range is 752-757; scanner also keys files by basename only (`:120`) | ❌ instrumentation bug |
| Depth sampling | Art. 820 is `return True` (`magneto_optics/energy_analysis.py:93-116`); Art. 821 and Art. 831 return string dicts; Arts. 841-850/851-858 largely "covered" by two qualitative dictionaries with fabricated agreement scores (`molecular/competing_theories.py:694-796`) | ❌ T0 stubs present |
| Test coverage | 1,942 tests collect, but **zero** tests import instruments/, galvanometers_extended.py, ratio_v/, waves/, components/, magneto_optics/, vortex_engine/, gmd.py, coil_forces.py, medium_check.py; **no test identifier references any article number 667-866** | ❌ per-article tests absent for ~120 articles |
| SymPy layer | Of 15 registered symbolic verifiers, exactly **one** article in range (Art. 787, `verification/sympy_verify.py`) | ❌ T4 unreachable as-is |
| Page verification | `page_verifier/` infra exists but holds **7 verdicts, all Vol I prelim pages** (0 for Vol II / 667-866), `page_verifier/data/verdicts.json` updated 2026-08-18 | ❌ ground-truth loop not yet run |
| Documentation | `docs/COVERAGE_SUMMARY.md` is stale/wrong (claims Part I "1-206", Part IV "475-795", "Supplementary 796-866, 320 articles", 1795 tests) | ❌ coverage claims unreliable |

**Bottom line:** the last 200 articles are ~100% *cited*, ~90% *transcribed* at formula level, but only ≈25% are numerically verified and ≈0.5% cross-validated. The April-2026 "48%→100%" result measured citation presence; it did not measure depth. The mission of Stages 2-4 is to convert citation coverage into evidenced implementation depth.

### Estimated tier distribution (200 articles)

| Tier | Definition (§2) | Est. count | Est. % | Representative articles |
|---|---|---|---|---|
| T0 | Cited-only / stub / prose / meta-only | ~20 | 10% | 820, 821, 831, 768, 848-850, 856-858, 694, 695, 703-705, 765-767, 838-840 |
| T1 | Formula transcribed, unverified, untested | ~69 | 34.5% | 707-729 (instruments), 736-757 untested core, 769-770, 774-780, 810-819, 823-830, 740/745/750 semantic suspects |
| T2 | Functionally implemented, self-consistency only | ~60 | 30% | 667-687, 691-693, 697-699, 781-795, 841-847, 851-855, 865-866 |
| T3 | Numerically verified by tests | ~50 | 25% | 696-701, 730-735, 740, 745, 750, 758-764, 771-773, 786-805 (optics subset), 832-837 |
| T4 | Cross-validated (SymPy+numeric+tests) | 1 | 0.5% | 787 |

±1 tier uncertainty per article; figures are sums of the §2.3 cluster tallies (±2 total from borderline classifications). Only ~25% of the 200 articles have any numeric test evidence; ~10% are outright stubs or meta-only citations.

---

## 2. Depth Tier Rubric and Article-by-Article Taxonomy

### 2.1 Tier definitions

- **T0 — Cited-only / stub.** Decorator present, but the function (a) returns hardcoded strings/booleans/dicts, (b) is prose-as-data, or (c) the article is cited only by `verify_*`/`analyze_*` meta-functions or visualization code with no article-specific computation.
- **T1 — Formula transcribed.** A plausible formula is coded (often one-liner), dimensionally passable, but: no tests, no numeric anchoring, possibly heuristic/empirical substitutions, possible docstring-vs-code mismatch.
- **T2 — Functionally implemented.** Real computation with classes, parameter handling, edge cases; any verification is self-consistency (potentially circular); no per-article external reference values.
- **T3 — Numerically verified.** ≥1 test asserts known values, limit cases, or physical identities for that article's computation.
- **T4 — Cross-validated.** SymPy symbolic identity registered in `verification/sympy_verify.py`/`equation_registry.py` **plus** numeric tests **plus** (where applicable) page_verifier verdict.

### 2.2 File-to-article map for 667-866 (verified by decorator parse)

| File | Articles | Decorator hits |
|---|---|---|
| `electromagnetism/current_sheets/boundary_conditions.py` | 667-674 | 49 (incl. 670-672 shared w/ coils) |
| `electromagnetism/components/circular_coils.py` | 670-679 | — |
| `electromagnetism/components/solenoids.py` | 675-683 | — |
| `electromagnetism/components/cylinders.py` | 680-687 | — |
| `math/spherical_harmonics.py` | 675-678, 685-695 | — |
| `math/geometry/gmd.py` | 691-693 | — |
| `math/elliptic_integrals.py` | 696-705 | 634-line module, Landen transforms present |
| `electromagnetism/forces/coil_forces.py` | 697-699 | — |
| `electromagnetism/vis/circular_fields.py` | 702 (**vis-only**) | — |
| `electromagnetism/optimization/coil_design.py` | 706 | — |
| `instruments/galvanometers.py` | 707-712, 714, 715, 717, 720 | — |
| `instruments/helmholtz.py` | 713 | — |
| `instruments/optimization/sensitivity.py` | 716, 718, 719 | — |
| `instruments/suspended_coil.py` | 721-724, 728 | — |
| `instruments/dynamometers.py` | 725-727, 729 | — |
| `signal_processing/telegraphy.py` | 730-735, 740, 745, 750 | — |
| `electromagnetism/measurements/galvanometers_extended.py` | 736-739, 741-744, 746-757 (19 arts) | 1076 lines |
| `calibration/absolute_resistance.py` | 758-767 | — |
| `experiments/ratio_v/{theory,condensers,combined}.py` | 768-780 (771-773 shared w/ `core/units/dimensions.py`) | — |
| `electromagnetism/waves/{wave_equation,plane_wave,polarization}.py` | 781-795 | — |
| `optics/{wave_equation,velocity,constants,plane_waves,radiation_pressure,crystals,metals,diffusion}.py` | 781-808 (overlapping) | — |
| `magneto_optics/{rotation,circular_polarization,energy_analysis}.py` | 807-821 | — |
| `vis/molecular_vortices.py`, `vortex_engine/*.py` | 822-831 | — |
| `molecular/{amperes_theory,webers_theory,neumanns_theory,competing_theories}.py` | 832-866 | `competing_theories.py` alone cites 26 arts |
| `theories/failure_modes.py` | 857-859 | — |
| `philosophy/medium_check.py` | 865-866 | — |

### 2.3 Cluster-by-cluster classification (sampled evidence)

#### Cluster A — Arts 667-706 (Ch XII tail, XIII Parallel, XIV Circular) — 40 arts
- **Sampled:** `circular_coils.py:43-154` — real on-axis field `B_z = 2πnIa²/(c(a²+z²)^{3/2})` (line 84), off-axis via elliptic integrals (line 120+). **T2**, with fidelity flag: private `_elliptic_K/_elliptic_E` (lines 87-108) are 4-term series, poor convergence near k²→1, duplicating the proper Landen implementation in `math/elliptic_integrals.py`.
- `boundary_conditions.py:288-354` — genuine vector boundary-condition computations. **T2**. Semantic flag: cites 666-667 for what is generic field boundary math; Treatise 666-674 is current-sheet-specific content — needs page verification.
- `gmd.py` (691-693), `coil_forces.py` (697-699), `solenoids.py`, `cylinders.py` — real formulas, **T2**, **no tests**.
- `elliptic_integrals.py` (696-701) + `spherical_harmonics.py` (685-695) — exercised with numeric asserts in `tests/test_new_part_iv_math.py` (57 tests) → **T3** for tested functions.
- **Weak:** 694, 695 (only `verify_spherical_harmonics`/`analyze_spherical_harmonics` cite them), 703-705 (only `verify_elliptic_integrals`/`analyze_elliptic_integrals`), 702 (**vis-only**, `electromagnetism/vis/circular_fields.py`), 706 (optimization heuristic only). → **T0/T1**.
- **Cluster tally (40 arts):** ~8 T3, ~22 T2, ~6 T1, ~4 T0.

#### Cluster B — Arts 707-751 (Ch XV Instruments, XVI Observations) — 45 arts
- **Sampled:** `instruments/galvanometers.py:50-160` — `G = 2πn/R` (line 53), tangent law `tan θ = GI/H` (line 116). Real formulas but: dimensionally suspect `restoring = horizontal_field + torsion_constant` (line 115 — torsion constant added to field without normalization); `design_standard_coil` (line 57) uses heuristic `0.9*max_radius` rather than Maxwell's Art. 708 construction rules. **T1**.
- `instruments/optimization/sensitivity.py:16+` (Arts. 716/718/719) — real optimization math, untested. **T1-T2**.
- `galvanometers_extended.py` (19 arts, 736-757 span) — full classes (tangent/sine/Helmholtz galvanometers, wattmeter, electrodynamometer, current weigher, Joule balance); **zero tests import this file**. **T1-T2**.
- `telegraphy.py` Arts. 730-735, 740, 745, 750 — exercised in `tests/test_new_part_iv_signal_calibration.py` (54 tests, `TelegraphLine` class + `rise_time`/`bandwidth_limit`/`max_signaling_rate`) → **T3**. Semantic flag: 740/745/750 as telegraph bandwidth/signaling functions sit oddly in Ch XVI "Observations" — verify against Treatise text (telegraph content may legitimately be there, but must be confirmed page-by-page).
- **Cluster tally (45 arts):** ~8 T3, ~16 T2, ~21 T1. This is the largest tested-gap mass in the range: all 23 articles of Ch XV and 16 of Ch XVI have no tests.

#### Cluster C — Arts 752-767 (Ch XVII Coil Comparison, XVIII Resistance Unit) — 16 arts
- **Chapter bug (confirmed):** `check_coverage.py:89` `("Ch XVII: Coil Comparison", 752, 761)` vs `:90` `("Ch XVIII: Resistance Unit", 758, 767)`. Arts 758-761 are double-counted; Ch XVII denominator inflated 6→10. True Treatise: Ch XVII = 752-757. Continuity audit of the full PARTS table (`:16-98`) found **no other overlap or gap** in Parts I-IV (all other chapter boundaries contiguous).
- **Sampled:** `galvanometers_extended.py:877-982` `current_weigher` (cites 751-754) — docstring admits "Simplified geometric factor" / "empirical correction" (lines 949-959) instead of the elliptic-integral force it mentions; `joule_balance` (755-757) similar. **T1**, plus **semantic flag**: Ch XVII is "Comparison of Coils" — current-weigher/Joule-balance physics may belong to different articles; Stage 2 must reconcile against the text.
- `calibration/absolute_resistance.py:68-295` (recoil, Lenz, rotating-coil, energy-dissipation, temperature methods, 758-764) — real methods, tested via `AbsoluteResistance`/`StandardResistanceCoil` in `tests/test_new_part_iv_signal_calibration.py` → **T2→T3**. **Verification-theater flag:** `verify_absolute_resistance` (`:510-586`) computes `heat` *from* `R_lenz` then "cross-checks" `R_energy` recovered from that same heat (lines 564-574) — consistency error is identically ~0; `velocity_check = True` hardcoded (line 571).
- Arts. 765-767 cited only by `verify_absolute_resistance`/`analyze_absolute_resistance` → **T0 (meta-only)**.
- **Cluster tally (16 arts):** ~7 T3, ~2 T2, ~4 T1, ~3 T0 (765-767).

#### Cluster D — Arts 768-780 (Ch XIX ESU vs EMU, the ratio-V experiments) — 13 arts
- **Sampled:** `experiments/ratio_v/combined.py:67-206` — one-line formulas per method: intermittent current `v = CVf/I` (line 96), condenser wippe `v = 1/√(RCf)` (line 124), LC resonance (line 180), coil+condenser period (line 206). Plausible, **T1**, **zero tests**.
- `theory.py:22` `motive_ratio_investigation` (Art. 768) returns motivational prose → **T0**; `theory.py:66` `calc_convection_current` (770) T1; `theory.py:94` `compare_resistance_systems` (780) T1.
- Arts. 771-773 live in `core/units/dimensions.py` and are tested in `tests/test_part_iv_advanced.py` (`calc_unit_ratio`, `convert_esu_to_emu`, `verify_speed_of_light_relationship`) → **T3**.
- **Critical missing anchor:** no function/test pins the measured ratio to Maxwell's historical result v ≈ 3.1×10¹⁰ cm/s (Weber-Kohlrausch ~3.107×10¹⁰). The chapter's entire point — v equals the speed of light — is asserted only via `verify_equals_c` in theory.py (untested).
- **Cluster tally (13 arts):** ~3 T3 (771-773), ~9 T1, ~1 T0 (768).

#### Cluster E — Arts 781-805 (Ch XX EM Theory of Light) — 25 arts
- Richest cluster by decorator mass (274 hits). Two parallel implementations: `electromagnetism/waves/{wave_equation,plane_wave,polarization}.py` (781-795) and `optics/*.py` (781-808).
- `electromagnetism/waves/*` — substantial code (wave equation derivation, plane waves, Stokes/polarization machinery), **T2**, but **zero tests import these modules**.
- `optics/{velocity,constants,plane_waves,radiation_pressure,crystals,metals,diffusion}.py` — exercised by `tests/test_new_part_iv_optics.py` (51 tests, numeric asserts) → Arts. 786-805 covered there are **T3**.
- Fidelity flag: `optics/diffusion.py:631-699` (Arts. 801-803) — `calc_diffusion_time` returns `σL²` with "conductivity (s⁻¹)" docstring: magnetic diffusion in CGS carries 4π/c² factors; dimensional confusion → **T1** until fixed.
- **Cluster tally (25 arts):** ~12 T3 (optics-tested subset of 786-805), ~11 T2 (all of 781-795 waves module, untested), ~2 T1 (801-803 diffusion defects counted once here).

#### Cluster F — Arts 806-831 (Ch XXI Magnetic Action on Light) — 26 arts
- The weakest substantive cluster. `magneto_optics/`, `vortex_engine/` and vis/molecular_vortices have **zero tests**.
- **Sampled stubs (T0):** `energy_analysis.py:93-116` Art. 820 `prove_real_rotation_required()` — *returns the literal constant `True`*; `energy_analysis.py:119-143` Art. 821 — returns a dict of six prose strings; `vortex_engine/vortex_lattice.py:153` Art. 831 `append_mechanical_theory_notes()` — returns a dict of five prose strings.
- **T1 formulas:** Arts. 811-817 (`circular_polarization.py:19-250`, kinematic velocity-split analyses), 818-819 (`energy_analysis.py:31-90` — generic 1/8π energy densities, not the article-specific medium Lagrangian), 810 (`rotation.py:116` natural-rotation model).
- **Internal inconsistency found:** `vortex_engine/magnetic_rotation.py:16-51` (Art. 829) — docstring states `θ = (ω/c)(λ/2π)L` but the code computes `ω r² L/(cλ²)` (lines 47-49). Art. 830 `compare_verdet_data` is a generic error comparator with no Verdet dataset.
- Semantic flag: Arts. 806-808 are *also* cited by `optics/diffusion.py:83-242` (Beer-Lambert transmission/absorbance/mean-free-path) — absorption code is not the Faraday-effect content of these articles (rotation.py correctly covers 807-809). Remove/repair the diffusion citations.
- **Cluster tally (26 arts):** ~2 T2 (807-809 rotation core), ~21 T1, ~3 T0 (820, 821, 831).

#### Cluster G — Arts 832-866 (Ch XXII Molecular Currents, XXIII Action at Distance) — 35 arts
- `molecular/amperes_theory.py` (832-840): real moment/field/magnetization/susceptibility/bound-current math; tested in `tests/test_new_part_iv_molecular.py` (33 tests, numeric: dipole axis B=2, equator B=−1) → 832-837 **T3**; 838-840 cited only by `verify_amperes_theory`/`analyze_amperes_theory` → **T0**.
- `webers_theory.py` (841-850): real Weber force/potential/induction code; `weber_force`/`weber_potential` tested → 841-845 **T2-T3**. **Fidelity flag:** velocity correction uses `v²/(2c²)` (`webers_theory.py:103`) — Maxwell's presentation of Weber's law (Arts. 841-845) carries coefficient 1, not ½, on the ṙ² term; verify against text and fix one or the other. 846-847 (`force_between_current_elements`, `induced_emf`) untested **T2**. 848-850 cited only by `verify_webers_theory`/`analyze_webers_theory` → **T0**.
- `neumanns_theory.py` (851-858): real vector-potential/flux/mutual-inductance code; `neumann_mutual_inductance` tested → 851-855 **T2-T3**; 856-858 verify/analyze-only → **T0**.
- `competing_theories.py` (841-866, 26 articles): **`analyze_webers_theory` (:694-744) is a single decorator citing TEN articles returning a qualitative dict with invented "experimental_agreement" scores (0.95/0.85/0.0…); `analyze_neumanns_theory` (:747-796) likewise for EIGHT articles.** These two functions are load-bearing for the coverage scanner's 100%. Arts. 859-866 additionally covered by `characteristics`/`experimental_agreement`/`compare_all`/`verify_theory_consistency`/`synthesize_theory_comparison`/`maxwell_advantages` — mostly qualitative dicts (**T1**) with `compare_theories` tested.
- `philosophy/medium_check.py` (865-866): real Fresnel/refractive-index math — **T2**, but **integrity defect:** `verify_maxwell_relation` returns `"verified": True` hardcoded (line 255) even when `all_agree` is False (water row fails at 10% tolerance).
- **Cluster tally (35 arts):** ~12 T3 (832-837 + tested weber/neumann cores), ~8 T2, ~6 T1 (859-864 qualitative dicts), ~9 T0 (838-840, 848-850, 856-858 meta-only).

---

## 3. Precise Gap List

### 3.1 Instrumentation & metadata gaps

| # | Gap | Evidence | Fix owner |
|---|---|---|---|
| G1 | Ch XVII range bug: `(752,761)` should be `(752,757)`; arts 758-761 double-counted | `check_coverage.py:89-90` | ARCHITECTUS |
| G2 | Scanner counts decorator presence only; no depth signal; file aggregation keyed by basename (collides e.g. `solenoids.py` in `geometry/` vs `components/`) | `check_coverage.py:107,120,176-182` | ARCHITECTUS/QUALITAS |
| G3 | `docs/COVERAGE_SUMMARY.md` factually wrong (Part I "1-206"; Part IV "475-795"; "Supplementary 796-866, 320 articles"; 1795 tests vs actual 1942 collected) | `docs/COVERAGE_SUMMARY.md` header | SCRIBA |
| G4 | PARTS table must be audited article-by-article against the Treatise TOC (continuity verified clean except G1; semantic titles for Ch XVI "Observations" and Ch XXII to confirm against 3rd-edition TOC) | `check_coverage.py:16-98` | ARCHITECTUS |
| G5 | Decorator chapter strings sometimes disagree with PARTS chapters (e.g. `circular_coils.py:43-51` labels 670-675 "Circular Coils"; `boundary_conditions.py:288` labels 666-667) | grep evidence §2.3 | ARCHITECTUS |
| G6 | page_verifier has 0 verdicts for Vol II; verdict store has only v1-p001..p005 (some verdict notes themselves garbled) | `page_verifier/data/verdicts.json` | ARCHITECTUS/SCRIBA |

### 3.2 Articles needing tier promotion (promotion targets in parentheses)

- **T0 stubs → ≥T2:** 820 (real non-reciprocity proof computation), 821 (derive summary from computed results), 831 (at minimum a quantitative vortex-lattice wave-speed check), 768 (derive dimensional relation, not prose).
- **Meta-only coverage → ≥T2 article-specific implementation:** 694, 695, 703, 704, 705 (elliptic/spherical-harmonic results specific to circular-current potential theory), 765, 766, 767 (Ch XVIII closing results: dimensional summary of resistance unit, temperature effects, comparison with Weber-Kohlrausch), 838, 839, 840 (Ampère-theory consequences), 848, 849, 850 (Weber-theory critiques with computed counterexamples), 856, 857, 858 (Neumann-theory consequences).
- **T1 → ≥T3 (no tests at all):** all of `instruments/` (707-729), `galvanometers_extended.py` (736-739, 741-744, 746-757), `ratio_v/` (768-770, 774-780), `electromagnetism/waves/` (781-795), `electromagnetism/components/` (670-687), `boundary_conditions.py` (667-674), `coil_forces.py` (697-699), `gmd.py` (691-693), `magneto_optics/` (810-821), `vortex_engine/` (823-831), `coil_design.py` (706), `sensitivity.py` (716-719), `medium_check.py` (865-866), `failure_modes.py` (857-859).
- **42 single-cite articles** (brieﬁng-confirmed list: 707, 708, 711, 712, 716, 717, 718, 719, 723, 724, 727, 728, 740, 745, 750, 768, 770, 774, 775, 776, 777, 778, 779, 780, 810, 811, 812, 814, 815, 816, 817, 818, 819, 820, 821, 824, 825, 826, 828, 829, 830, 831) — each requires a second independent piece of evidence (test or SymPy entry) regardless of tier.

### 3.3 Visualization-only or constant-only coverage

- **Art. 702** — only `electromagnetism/vis/circular_fields.py` (stream function/field-line tracing). Needs numeric core (current-sheet / circular-current field computation).
- **Art. 822** — `vis/molecular_vortices.py` plus `vortex_engine/vortex_lattice.py`; visualization is fine but the lattice numerics are untested.
- **Arts. 820/821/831** — effectively constant-only (see §3.2).

### 3.4 Suspected wrong decorator article-numbers (verify in Stage 2 via page_verifier)

| Articles | Current host | Why suspect |
|---|---|---|
| 667-674 | `boundary_conditions.py` + `circular_coils.py` | Ch XII tail is current-sheet theory; generic boundary/coil math may not match specific articles |
| 685-690 | `math/spherical_harmonics.py` | Plausible (circular-current potential expansion) but must match text |
| 740, 745, 750 | `signal_processing/telegraphy.py` rise_time/bandwidth/signaling | Telephony-style metrics vs Ch XVI "Observations" |
| 751-754 | `galvanometers_extended.py` `current_weigher` | Weigher physics vs Ch XVII "Comparison of Coils" |
| 755-757 | `galvanometers_extended.py` `joule_balance` | Same |
| 806-808 | `optics/diffusion.py` absorbance/mean-free-path | Absorption code ≠ Faraday-effect opening articles |
| 829 | `vortex_engine/magnetic_rotation.py` | Docstring formula ≠ coded formula |
| 841-850 / 851-858 | single dicts in `competing_theories.py` | 10/8 articles per qualitative dict |

### 3.5 Verification-theater (must be re-engineered, not extended)

- `calibration/absolute_resistance.py:510-586` — circular consistency check; hardcoded `velocity_check = True`.
- `philosophy/medium_check.py:255` — `"verified": True` returned regardless of data outcome.
- `competing_theories.py` agreement scores (0.95/0.85/…) — invented constants presented as results.
- **Recommended static gate:** grep-level lint forbidding `verified": True`/`agrees": True` literals in `verify_*` functions and requiring every `verify_*` to consume at least one externally-sourced reference value.

---

## 4. Requirements for "Ensured" Status (per article)

**REQ-F (Functional).** ≥1 public function or class method whose computation is specific to the article (not a generic helper), exported and importable; stub returns (bare bool/dict-of-strings) prohibited for `maxwell_original` citations.

**REQ-M (Mathematical fidelity).** Formula matches the Treatise expression in CGS with explicit c, 4π factors; any deviation (modern reformulation, numerical shortcut) documented in the docstring with `theory_class` set accordingly; docstring formula and code must agree; approximations (series truncation, far-field) carry stated error bounds or are replaced by the rigorous module (e.g., `math/elliptic_integrals.py` Landen instead of 4-term series).

**REQ-V (Verification).** Each article has ≥1 named reference value: Maxwell's own numerical result where the text gives one (e.g., v ≈ 3.1×10¹⁰ cm/s; Helmholtz coil uniformity condition; GMD tabulated cases), otherwise an analytic limit case or identity. `verify_*` functions must compute verdicts from inputs — no literal verdicts.

**REQ-T (Testing).** ≥1 pytest test named `test_art_<NNN>_<topic>` (or parametrize marker `@pytest.mark.article(NNN)`) asserting the REQ-V value within stated tolerance; tests live in `tests/articles/test_part_iv_<chapter>.py` bundles; the suite must be runnable without external assets.

**REQ-D (Documentation).** Decorator `chapter` string consistent with the corrected PARTS table; `description` states the article's specific result; `docs/COVERAGE_SUMMARY.md` regenerated from the fixed scanner (never hand-edited).

**REQ-X (Cross-validation, for T4).** SymPy identity registered (`verification/sympy_verify.py` pattern, `article_refs` tuple) **and** passing, plus page_verifier verdict "yes" for the article's pages.

**Definition of Done (article):** REQ-F + REQ-M + REQ-V + REQ-T satisfied ⇒ T3 ("ensured"). T4 additionally REQ-X. Stage-4 acceptance target: **200/200 ≥ T3; the mathematical spine (670-706, 752-780, 781-795) at T4.**

---

## 5. Technical Roadmap

### Phase 0 — Instrumentation Repair & Evidence Ledger (entry: now; ~1 wk)
**Work:** fix G1 (Ch XVII → (752,757)); extend `check_coverage.py` to a depth-aware report (per-article: decorator count, test-presence via test-file AST scan, SymPy presence, vis-only flag); create `docs/article_evidence_667_866.json` ledger seeded from Stage-1 findings; regenerate `COVERAGE_SUMMARY.md`; commit `page_verifier/` (currently untracked).
**Agents:** ARCHITECTUS (PARTS table, ledger), QUALITAS (depth scanner), SCRIBA (docs).
**Entry:** this document accepted. **Exit:** `python check_coverage.py` emits per-article tier estimates matching §1 table within ±5 articles; ledger loads; no chapter overlaps; summary doc regenerated.

### Phase 1 — Ground Truth: Semantic Audit via page_verifier (~1-2 wks)
**Work:** run the page_verifier workflow over all Vol II pages carrying arts 667-866 (product function ↔ OCR ↔ page-photo comparison); record verdicts; for every "No", file a mapping defect; resolve all §3.4 suspects; produce per-article *expected-formula sheet* with Treatise numerics (this is Stage-2's input contract).
**Agents:** ARCHITECTUS (mapping), PHYSICUS (physics reading), SCRIBA (records). Human-in-loop via page_verifier UI.
**Entry:** Phase 0 exit. **Exit:** 100% of Vol II pages for 667-866 carry a verdict; §3.4 table fully adjudicated; expected-formula sheet reviewed.

### Phase 2 — T0/T1 → T2 Uplift (implementation wave, ~2-3 wks)
**Work packages:**
- **WP-F1 magneto-optics & vortex (806-831)** — replace stubs 820/821/831 with computations; fix 829 docstring/code mismatch; implement real velocity-split kinematics for 811-817 and medium-energy analysis for 818-819; anchor 829-830 to Verdat/Verdet data tables. Agents: MATERIA, PHYSICUS, MATHEMATICA.
- **WP-B1 instruments (707-729)** — repair dimensional defects (galvanometer torsion term), replace heuristic design rules with Maxwell's construction (708), add Gaugain suspension math (712), dynamometer/solenoid-suction rigor (727). Agent: INSTRUMENTUM.
- **WP-D1 ratio-V experiments (768-780)** — implement the four historical methods with error analysis; anchor to v = 3.107×10¹⁰ cm/s. Agent: CIRCUITUS.
- **WP-C1 coil comparison & resistance (752-767)** — re-map current-weigher/Joule-balance per Phase-1 verdicts; implement genuine coil-comparison methods (differential galvanometer, transient methods) for 752-757; replace circular `verify_absolute_resistance` with independent cross-method checks. Agents: INSTRUMENTUM, CIRCUITUS.
- **WP-G1 theory chapters (838-840, 848-850, 856-858, 859-866)** — convert qualitative dicts into computed comparisons; fix Weber ½-vs-1 coefficient; fix `medium_check` forced verdict. Agents: PHYSICUS, MATHEMATICA.
- **WP-A1 math spine fidelity (670-706)** — switch coil field code to `math/elliptic_integrals.py`; add numeric core for Art. 702; GMD validation cases for 691-693. Agent: MATHEMATICA.
**Entry:** Phase 1 exit (formula sheets in hand). **Exit:** zero T0 in range; every article has article-specific computation (ledger-verified); existing 1,942 tests still green.

### Phase 3 — T2 → T3: Per-Article Numeric Tests (~2-3 wks)
**Work:** create `tests/articles/` bundles per chapter (12 bundles), each article ≥1 test asserting its REQ-V reference value; priority order by current weakness: Ch XV, XVI, XIX, XXI first, then XII-XIV, XX, XXII-XXIII. Introduce `pytest.mark.article(N)` marker + a `tests/test_article_coverage.py` meta-test that fails if any of 667-866 lacks a marked test.
**Agents:** QUALITAS (framework + gates), INSTRUMENTUM (B/C), CIRCUITUS (C/D), MATHEMATICA (A/E), MATERIA (F), PHYSICUS (G).
**Entry:** Phase 2 exit. **Exit:** 200/200 articles carry ≥1 passing marked test; suite total ≈ 2,300+ tests green; ledger tiers recomputed.

### Phase 4 — T3 → T4 Cross-Validation & Certification (~1-2 wks)
**Work:** register SymPy identities for the spine (670-706, 752-780, 781-795: ≥60 verifiers) following `sympy_verify.py` patterns; wire SymPy + depth report into CI (`run_quality_checks.sh`); optional JAX cross-checks for hot numerics; final audit: page_verifier verdicts green, ledger complete, regenerated coverage docs, Stage-4 certification report.
**Agents:** MATHEMATICA (SymPy), QUALITAS (CI gates), SCRIBA (final report), ARCHITECTUS (sign-off).
**Entry:** Phase 3 exit. **Exit:** Success metrics §6 all green; `check_coverage.py` prints tiered report showing 0 articles below T3.

---

## 6. Risk Register & Success Metrics

### Risks

| # | Risk | L | I | Mitigation |
|---|---|---|---|---|
| R1 | Wrong article-numbers in decorators persist (coverage illusion) | High | High | Phase-1 page_verifier audit is a hard gate; §3.4 suspects list; forbid closing until adjudicated |
| R2 | Verification theater recurs (hardcoded verdicts, circular checks) | Med | High | Static lint gate (§3.5), code review checklist item, QUALITAS sign-off |
| R3 | Effort underestimate: ~150 articles need new tests/math | High | Med | Phase ordering by weakness mass; per-chapter exit gates; allow T3 (not T4) as acceptance floor |
| R4 | Silent numeric fidelity errors (truncated elliptic series, missing 4π/c² factors, Weber ½) | Med | High | Reference-value tests with tight tolerances; cross-check against `math/elliptic_integrals.py` and dimensional analysis tests (`core/units/dimensions.py`) |
| R5 | Test-count inflation via trivial smoke tests | Med | Med | Rubric: a qualifying test must assert a numeric value/limit with tolerance; meta-test enforces marker presence and ≥1 numeric assert |
| R6 | Downstream stages consume stale PARTS/coverage data | Med | Med | Single source of truth (`check_coverage.py` PARTS + ledger JSON), versioned; COVERAGE_SUMMARY.md machine-generated only |
| R7 | page_verifier external dependencies (OCR JSON at `C:\Users\antmi\Downloads\maxwell_em_processor\...`, page photos) missing/corrupt | Med | Med | Phase-1 pre-flight check of both volume JSONs + Vol II photo set; env overrides documented in `page_verifier/README.md:125-135` |
| R8 | Regression in the existing 1,942-test suite during rework | Med | Med | Full-suite gate at every phase exit; behavior-preserving refactors for T2→T3; new code behind new functions |
| R9 | CGS unit drift (mixed conventions for c factors between modules) | Med | Med | `cgs_unit_of`/`CONST.C` used exclusively; add dimensional-consistency tests per WP |
| R10 | `user_original`/`standard_math` extensions (vortex_engine, telegraphy metrics) entangled with `maxwell_original` claims | Med | Low | Keep extensions but require a separate `maxwell_original` core per article before promotion |

### Success metrics (measurable)

1. **200/200 articles ≥ T3**, i.e., each has ≥1 passing `pytest.mark.article(N)` test asserting a reference value/limit.
2. **0 articles** covered only by `verify_*`/`analyze_*`/vis functions.
3. **0 single-cite articles** without an independent test or SymPy entry (currently 42).
4. **≥60 SymPy verifiers** registered for the spine (670-706, 752-780, 781-795); T4 count ≥ 60.
5. `check_coverage.py` PARTS table passes automated continuity + TOC-match check; **no overlapping ranges**.
6. **100% of Vol II pages for arts 667-866 have page_verifier verdicts**; all "no" verdicts resolved or annotated.
7. Full suite green: existing 1,942 + ~200-400 new article tests; SymPy checks green in CI.
8. `docs/COVERAGE_SUMMARY.md` regenerated and byte-consistent with scanner output.

---

## 7. Open Questions for Downstream Stages

1. **Vis-only articles (702, 822):** is a tested numeric core mandatory for T3, or is a validated visualization plus analytic spot-check acceptable?
2. **Edition authority:** page_verifier uses Third Edition scans; article numbering is stable across editions but figure/table references differ — confirm 3rd edition as ground truth for Stage 2 formula sheets.
3. **JAX scope:** are JAX adapter ports required for any of the last-200 modules (instruments, waves, vortex lattice), or is NumPy core sufficient for "ensured"?
4. **Fabricated metadata:** delete or compute the `experimental_agreement` score dicts in `competing_theories.py`? (Recommendation: compute from defined metrics or delete.)
5. **Reference-value store:** inline-in-test vs central `tests/articles/reference_values.json` — decide before Phase 3 to keep tolerances auditable.
6. **Ch XVI content boundary:** does the Treatise's Ch XVI (730-751) genuinely contain the telegraph/signaling analyses mapped to 740/745/750, or should those decorators move? (Phase 1 adjudication.)
7. **Article 282-style sub-articles:** range 667-866 appears to contain no a/b sub-articles; confirm none exist (e.g., near 866) before Stage 2 locks the ledger schema.

---

## Appendix A — Verified single-cite article locations (42)

707 `instruments/galvanometers.py:50`; 708 `:56`; 711 `:241`; 712 `:259`; 716 `instruments/optimization/sensitivity.py:16`; 717 `galvanometers.py:371`; 718 `sensitivity.py:62`; 719 `sensitivity.py:106`; 723 `instruments/suspended_coil.py:179`; 724 `:151`; 727 `instruments/dynamometers.py:159`; 728 `suspended_coil.py:200`; 740 `signal_processing/telegraphy.py:285`; 745 `:313`; 750 `:342`; 768 `experiments/ratio_v/theory.py:22`; 770 `:66`; 774 `ratio_v/condensers.py:95`; 775 `ratio_v/combined.py:67`; 776 `:99`; 777 `:127`; 778 `:156`; 779 `:183`; 780 `ratio_v/theory.py:94`; 810 `magneto_optics/rotation.py:116`; 811 `circular_polarization.py:19`; 812 `:56`; 814 `:155`; 815 `:188`; 816 `:225`; 817 `:250`; 818 `energy_analysis.py:31`; 819 `:65`; 820 `:93`; 821 `:119`; 824 `vortex_engine/kinetic_energy.py:15`; 825 `:43`; 826 `:75`; 828 `vortex_engine/equations_of_motion.py:63`; 829 `magnetic_rotation.py:15`; 830 `:54`; 831 `vortex_lattice.py:153`.

## Appendix B — Test assets touching 667-866

`tests/test_new_part_iv_math.py` (57 tests; elliptic_integrals, spherical_harmonics) · `tests/test_new_part_iv_signal_calibration.py` (54; telegraphy, absolute_resistance classes) · `tests/test_new_part_iv_optics.py` (51; optics/* only) · `tests/test_new_part_iv_molecular.py` (33; molecular/*) · `tests/test_part_iv_advanced.py` (core/units/dimensions, general_equations) · vis tests for 822/791 · `tests/test_sympy_verify.py` (exercises the 15 registered SymPy verifiers in `sympy_verify.py`; only Art. 787 lies in 667-866). **Zero test files exist for:** instruments/, galvanometers_extended, ratio_v/, waves/, components/, boundary_conditions, coil_forces, gmd, magneto_optics/, vortex_engine/, coil_design, sensitivity, medium_check, failure_modes.

*Stage 1 deliverable complete. Hand-off to Stage 2: §4 requirements, §5 Phase-1 formula-sheet contract, §3 gap list.*

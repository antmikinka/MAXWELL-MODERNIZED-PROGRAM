---
type: quality_review
pipeline_stage: 3 of 4 (Quality Review / Independent Audit)
input_artifacts:
  - docs/LAST200_STAGE1_PLANNING_ANALYSIS.md
  - docs/LAST200_STAGE2_PROGRAM_MANAGEMENT.md
status: complete
collab_reviewed: false
---

# LAST 200 ARTICLES (667-866) — Stage 3 Independent Quality Review

**Pipeline stage:** 3 of 4 (Quality Review / Independent Audit)
**Date:** 2026-08-21
**Method:** Read-only code audit. Every upstream claim below was re-verified by opening the cited file; file:line evidence is quoted. No source file was modified. The only executed commands were `check_coverage.py`, `pytest --collect-only`, and a JSON read of `page_verifier/data/verdicts.json`.

**Scope reminder:** This audit was run against the **pre-program baseline** (Phase 0 has not started). Stage 2 §8 artifacts that do not yet exist — `docs/article_evidence_667_866.json`, `tests/articles/`, `docs/last200_formula_sheets/` — are recorded as *expected-at-G0/G1*, not as missing evidence.

---

## 1. Audit methodology

1. Read Stage 1 and Stage 2 documents in full; extracted every falsifiable claim (file, line, article number).
2. Opened each cited file and quoted the exact lines. Where a claim involved arithmetic (tolerances, dimensional analysis, formula factors), the arithmetic was re-done by hand.
3. Live-ran `check_coverage.py` and `pytest --collect-only -q` (1947 tests collected in 5.63 s) to confirm instrument behavior rather than trusting descriptions.
4. Extended audit: 25+ files read across all 7 chapter clusters (list in §2.0), hunting stubs, magic numbers without provenance, unit-system errors, dead code, duplicated physics, wrong signs/factors, docstring-code divergence, decorator/article mismatches, and unphysical defaults.
5. Every defect was classified S1-S4 (definitions in §3) and given a concrete fix.

Severity rubric:
- **S1 — Critical math error.** The computation is numerically wrong, dimensionally inconsistent, or has an inverted sign/factor; any downstream use produces false physics.
- **S2 — Major gap.** Stub/prose-as-implementation, fabricated data, verification theater, wrong unit system, or semantic mis-mapping that blocks "ensured" status.
- **S3 — Minor.** Correctable divergence (docstring vs code, unit labels, magic constants with plausible provenance), single-function scope.
- **S4 — Cosmetic.** Naming, duplication, style.

---

## 2. Verdicts on upstream claims

Legend: ✅ CONFIRMED · ⚠️ PARTIALLY CONFIRMED · ❌ REFUTED

### 2.1 T0 stub cluster

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| U1 | Art. 820 is `return True` | ✅ | `magneto_optics/energy_analysis.py:93` decorator `@maxwell_cite(820, ..., theory_class="standard_math")`; function `prove_real_rotation_required()` lines 94-116 ends `return True` (line 116). Body is prose comments only. |
| U2 | Art. 821 returns a string dict | ✅ | `energy_analysis.py:119-143` `summarize_magneto_optic_results()` returns six hard-coded prose strings (`result_1`…`result_6`), no computation. |
| U3 | Art. 831 returns a string dict | ✅ | `vortex_engine/vortex_lattice.py:153-177` `append_mechanical_theory_notes()` decorated `@maxwell_cite(831, ..., theory_class="maxwell_original")`, returns five prose strings. Note: this one is `maxwell_original`, so it directly violates Stage 1 REQ-F. |
| U4 | `competing_theories.py` ~694-796 holds two qualitative dicts citing 10 and 8 articles | ✅ | `molecular/competing_theories.py:694-705` — one decorator lists articles 841-850 (ten ints); `analyze_webers_theory()` returns a dict of strings with invented `experimental_agreement` scores 1.0/0.9/0.8/0.0 (lines 738-743). `:747-756` — one decorator lists 851-858 (eight ints); `analyze_neumanns_theory()` dict with scores 0.9/0.8/1.0/0.0 (lines 790-795). Both are load-bearing for scanner coverage of 18 articles. |

**Corrections found:** Stage 1 §3.5 attributes scores "0.95/0.85" to these dicts; those exact values actually live in `analyze_amperes_theory` (lines 686-690, citing 859-860). Substance unchanged: invented constants in three dicts (also `maxwell_advantages`, lines 855-861, all 1.0, citing 859-866).

### 2.2 Verification theater

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| U5 | Circular `verify_absolute_resistance` | ✅ | `calibration/absolute_resistance.py:526-586`. Line 562 computes `R_lenz`; line 566 `heat = R_lenz * induced_current**2 * time`; line 567 `R_energy = ar.energy_dissipation_method(induced_current, time, heat)`. Since `energy_dissipation_method` is `heat/(I²t)` (line 228), `R_energy ≡ R_lenz` identically; `consistency_error` (line 574) is zero by construction. The "cross-check" compares a value to itself. |
| U6 | Hardcoded `velocity_check = True` | ✅ | Same function, line 571: `velocity_check = True  # By construction in CGS`. No dimensional analysis is performed. |
| U7 | Hardcoded `"verified": True` in `philosophy/medium_check.py:255` | ✅ (with correction) | Line 255: `"verified": True,  # Theory explains all data including dispersion` — literal verdict, returned regardless of `all_agree`. **Correction to Stage 1:** the parenthetical "water row fails at 10% tolerance" is **refuted by arithmetic**: water K=80 → √80=8.944 vs n_exp=9.0 → error 0.6% < 10%; all five media pass at default tolerance. The deeper defect: the water row is *rigged* — `n_measured=9.0` is √K_static, not water's optical refractive index (1.33; optical K≈1.77, which the same file uses at line 303). The dataset self-confirms, then the verdict is hardcoded anyway. |
| U8 | Invented "agreement score" constants | ✅ | Four dicts carry fabricated scores (see U4 + lines 686-690, 855-861). `tests/test_new_part_iv_molecular.py:376-410` currently tests these dicts only by key-presence asserts — the theater is not yet enshrined numerically, but the smoke tests legitimize it (see D-36). |

### 2.3 Math-fidelity bugs

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| U9 | 4-term elliptic series in `circular_coils.py` duplicating a Landen implementation | ✅ | `electromagnetism/components/circular_coils.py:87-108`: `_elliptic_K`/`_elliptic_E` truncate at m³. Near the coil wire k²→1, true K diverges logarithmically while this polynomial stays ≈2.34 — order-of-magnitude wrong exactly where off-axis fields matter. The alternative: `math/elliptic_integrals.py` uses `scipy.special.ellipk/ellipe` (lines 94, 138) and has a `landen_transformation` method (lines 234-264); `jax/_elliptic.py:190-232` implements genuine iterative descending Landen. **Correction:** calling `math/elliptic_integrals.py` "a proper Landen implementation" is generous — its Landen method performs one transform step then delegates to scipy (line 262). Either source would still beat the 4-term series. Additional defects found here: §3 D-29, D-30. |
| U10 | Weber force ½ coefficient | ✅ (needs adjudication) | `molecular/webers_theory.py:103` `velocity_correction = v_squared / (2.0 * c**2)` and line 104 `acceleration_correction = (r * a) / (c**2)`. Docstring (line 82) matches the code, so the module is internally consistent; the question is fidelity to the Treatise. Maxwell's presentation of Weber's law (Art. 845) carries coefficient **1** on ṙ² and **2** on rr̈; the code uses ½ and 1 (the modern convention). Same ½-convention duplicated in `theories/failure_modes.py:73-88`. Phase-1 formula sheet must adjudicate; exactly one convention must then be fixed everywhere and pinned by a test. |
| U11 | Missing 4π/c² in diffusion time (Arts 801-802) | ✅ | `optics/diffusion.py:631-660` `calc_diffusion_time` returns `sigma * L**2` with "sigma: Conductivity (s^-1 in CGS)" (line 643). Dimensions: [σL²] = L²T⁻¹ — a diffusivity, not a time. CGS magnetic diffusion is ∂B/∂t = (c²/4πσ)∇²B → τ = 4πσL²/c². Worse, `verify_diffusion_equation` in the *same file* contradicts both: line 715 docstring PDE omits c² ("dB/dt = (1/4π·sigma)∇²B") and line 719 states `tau = 4πσL²`. Three inconsistent formulas in one module. `calc_diffusion_length` (line 699) returns `sqrt(t/σ)`, which has dimension T (seconds), while the docstring claims cm. |
| U12 | Art. 829 docstring-vs-code mismatch | ✅ (worse than reported) | `vortex_engine/magnetic_rotation.py:15-51`. Docstring line 28: `theta = (omega/c)(lambda/2pi)L` — **dimensionally a length, not an angle**. Inline comment line 42 gives a *third* formula `(omega/2c)(r²/lambda)L`. Code lines 47-49 compute `omega·r²·L/(c·lambda²)` (dimensionless — the only dimensionally sane one). Also dead code: line 44 computes `H_equiv = vortex.magnetic_field_equivalent()` and never uses it. Art. 829 therefore presents three contradictory formulas; the docstring formula is unphysical. |

### 2.4 Suspect article→code mappings

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| U13 | Arts 740/745/750 in `signal_processing/telegraphy.py` | ✅ mis-mapping substantiated | `telegraphy.py:285-311` Art 740 → `rise_time` = `2.2·R·C·ℓ²`; `:313-340` Art 745 → `bandwidth_limit` = `0.35/t_r`; `:342-371` Art 750 → `max_signaling_rate` = `1/(2t_r)`. These are 20th-century oscilloscope/Nyquist rules of thumb, not 1873 content; Ch XVI "Observations" concerns methods of observation with galvanometers. Decorator chapter string is "Signal Transmission" (not a PARTS chapter). Bonus divergence: docstring line 298 says `t_r ≈ 2.2·R·C·L_line` while code squares `line_length` (line 311). These functions are tested (`tests/test_new_part_iv_signal_calibration.py`) — the tests currently enshrine the anachronisms. |
| U14 | Arts 806-808 absorption in `optics/diffusion.py` | ✅ | `diffusion.py:83-89` (Beer-Lambert, cites 806), `:117-122` (absorbance, 807), `:146-151` + `:175-180` (mean free path/penetration depth, 808 twice), `:201-206`, `:242-247` (again 806). Treatise 806-808 open Ch XXI (magnetic action on light / Faraday effect) — covered properly by `magneto_optics/rotation.py` (807-809). The chapter string on all these decorators, "Electromagnetic Theory of Light", is Ch XX (ends at 805) — wrong for 806+. |
| U15 | Art. 702 vis-only in `electromagnetism/vis/circular_fields.py` | ⚠️ partially confirmed | `circular_fields.py:97-103` cites 702 (vis stream function). **Correction:** 702 is *also* cited by `math/elliptic_integrals.py:293-298` (trivial helper "parameter m = k²") — so not strictly vis-only, but that citation is a thin generic helper (arguably citation-hijacking; D-39). The only substantive Art. 702 computation is the vis module's `_vector_potential_azimuthal` — which this audit found to be **wrong** (D-02). |

### 2.5 Tooling

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| U16 | Ch XVII/XVIII overlap in `check_coverage.py` | ✅ | `check_coverage.py:89` `("Ch XVII: Coil Comparison", 752, 761)` and `:90` `("Ch XVIII: Resistance Unit", 758, 767)`. Live run confirms articles 758-761 printed under **both** chapters; Ch XVII denominator inflated 6→10. Regex line 107 counts decorator presence only; file aggregation keyed by basename at line 120 (live output shows ambiguous basenames `total.py`, `volume.py`, `surface.py`, `helmholtz.py`, `circular_fields.py`). |
| U17 | Stale `COVERAGE_SUMMARY.md` | ✅ | Header: "Generated 2026-05-06", "1795/1795 tests". Table (lines 18-24): Part I "1-206, 126 articles" (229 articles exist; 206 numbers ≠ 126 count), Part III "371-474, 26 articles" (actually 104), Part IV "475-795, 269 articles" (actually 392), invented "Supplementary 796-866, 320 articles" (actually 71; no such Part). Current suite: **1947** collected. |

### 2.6 Supporting claims also checked

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| U18 | Arts 765-767 meta-only | ✅ | Decorator hits only in `verify_absolute_resistance` (`absolute_resistance.py:518-520`) and `analyze_absolute_resistance` (`:597-599`); elsewhere only prose mentions (line 236 docstring). |
| U19 | Arts 856-858 meta-only | ✅ | `neumanns_theory.py:521-523` (verify) and `:620-622` (analyze) are the only decorator citations. |
| U20 | Zero tests import instruments/, ratio_v/, waves/, magneto_optics/, vortex_engine/, components/, measurements/, philosophy/, theories/ | ✅ | Exhaustive grep over `tests/` (module-level and function-level imports): the only last-200 modules exercised are `signal_processing.telegraphy` + `calibration.absolute_resistance` (test_new_part_iv_signal_calibration.py), `optics/*` (test_new_part_iv_optics.py), `molecular/*` (test_new_part_iv_molecular.py), `math/elliptic_integrals` + `math/spherical_harmonics` (test_new_part_iv_math.py), `core/units/dimensions` (test_part_iv_advanced.py). |
| U21 | page_verifier: 7 verdicts, all Vol I prelim, 0 for 667-866 | ⚠️ | `verdicts.json` holds exactly 7 entries, all volume 1, zero intersecting 667-866; notes garbled as claimed ("NOT THAT IMP, BUT IS WRONG", "Y`"). **Correction:** not all are prelim pages — v1-p036 (articles 1-2) and v1-p409 (article 254) are included. |
| U22 | 1 SymPy verifier in range (Art. 787) | ✅ | `verification/sympy_verify.py:220` and `:234` (`arts = (787,)`); ~15 verifiers registered total. |
| U23 | Test count 1,942 | ⚠️ | `pytest --collect-only -q` now reports **1947 tests** collected. Stage 1's figure was accurate at writing; COVERAGE_SUMMARY's 1795 is stale either way. |

---

## 3. Defect register

42 defects. U-IDs reference §2 upstream confirmations; D-IDs are new findings of this audit. Articles affected use Treatise numbering.

| ID | Sev. | File:line | Article(s) | Description | Fix recommendation |
|---|---|---|---|---|---|
| D-01 | **S1** | `optics/diffusion.py:631-699, 709-719` | 801-803 | Magnetic diffusion time `τ=σL²` omits 4π/c² and is dimensionally a diffusivity; `calc_diffusion_length` returns seconds labeled as cm; `verify_diffusion_equation` docstring contradicts both (τ=4πσL², PDE missing c²). | Implement τ = 4πσL²/c² (CGS), derive length as √(t·c²/4πσ); make the three statements mutually derivable; add copper-slab reference test with provenance. |
| D-02 | **S1** | `electromagnetism/vis/circular_fields.py:47-76` | 702 | `_vector_potential_azimuthal` prefactor `(I/(cπ))·√(a/ρ)/√α²` disagrees with the standard form A_φ = (I/2c)(√α²/ρ)[(2−k²)K−2E] by a non-constant factor; near-axis asymptotic is ∝ρ^{3.5} instead of the required ∝ρ. Stream function / field-line geometry for Art. 702 is wrong. Also uses its own 3-term elliptic series (lines 65-66). | Replace with the standard formula (Jackson 5.37 analog) using `math/elliptic_integrals.py`; add near-axis asymptotic test ψ ∝ ρ² and cross-check B=∇×A against `calc_coil_off_axis`. |
| D-03 | **S1** | `experiments/ratio_v/combined.py:127-153` | 777 | `apply_rapid_action_correction` returns `measured_v / charge_fraction`. An under-charged condenser makes measured v too *large* (v_meas = v_true/charge_fraction), so the correction must **multiply** by charge_fraction. Current code amplifies the error. | Return `measured_v * charge_fraction`; regression test with charge_fraction=0.5 must halve v. |
| D-04 | **S1** | `magneto_optics/circular_polarization.py:56-82` | 812 | Δn = 2V·λ·B/π carries a spurious factor 2. From θ = (k_L−k_R)L/2 = VBL: Δn = V·B·λ/π. | Remove factor 2; add identity test coupling `perform_kinematic_analysis` rotation/length to V·B. |
| D-05 | **S1** | `electromagnetism/measurements/galvanometers_extended.py:877-982` | 751-754 | `current_weigher`: force = 2πN₁N₂I²·geom/**c²** with I declared in abamperes mixes SI docstring (μ₀/4π, line 902), Gaussian c², and EMU current — in EMU the coil force is I²·dM/dx with no c². Near-field "empirical correction" `r²/(d²+r²)` (line 959) is invented, no provenance. | Compute dM/dx from the elliptic-integral mutual inductance (coaxial-loop formula); drop the c² for abampere input or convert units explicitly via `cgs_unit_of`; validate against a tabulated Kelvin-balance case. |
| D-06 | **S2** | `magneto_optics/energy_analysis.py:93-116` | 820 | `prove_real_rotation_required()` returns literal `True`. | Implement the non-reciprocity argument computationally: forward+reflected round-trip rotation = 2θ for Faraday effect vs 0 for reciprocal rotation; return computed discriminant. (Stage 1 WP-F1.) |
| D-07 | **S2** | `magneto_optics/energy_analysis.py:119-143` | 821 | Prose-dict summary as implementation. | Derive each "result" numerically from the sibling computations (v=1/√(εμ), velocity split, round-trip rotation) or drop the citation. |
| D-08 | **S2** | `vortex_engine/vortex_lattice.py:153-177` | 831 | Prose-dict "notes" decorated `maxwell_original`. | At minimum compute the lattice wave speed and compare to c (the note_4 claim) — that computation is the article's substance. |
| D-09 | **S2** | `molecular/competing_theories.py:651-862` | 841-858, 859-866 | Three one-decorator multi-article dicts (10 + 8 + 8 articles) with invented `experimental_agreement` scores (0.95/0.85/0.0; 1.0/0.9/0.8/0.0; 0.9/0.8/1.0/0.0; all-1.0). Load-bearing for the scanner's 100%. | Per Decision D-04: compute defined metrics (e.g., Weber-force residuals vs Ampère law on test configurations; Neumann vs elliptic M) or delete scores; split into per-article functions (WP-3.5). |
| D-10 | **S2** | `calibration/absolute_resistance.py:510-586` | 758-767 | Circular cross-check (heat derived from R_lenz, then R_energy recovered from that heat → error identically 0) + hardcoded `velocity_check = True` (line 571). | Cross-method check must use independent inputs (e.g., recoil vs Lenz with independently-sourced M, T, EMF, I); velocity dimension check must be a real dimensional assertion (`cgs_unit_of`). |
| D-11 | **S2** | `philosophy/medium_check.py:221-256` | 865-866 | Hardcoded `"verified": True` (line 255) ignoring `all_agree`; water datum rigged (n_measured=9.0 = √K_static; optical n=1.33, K_opt≈1.77 — the file itself uses 1.77 at line 303). | Use optical-frequency K/n data (air, water 1.77/1.33, glass, quartz, sulfur); verdict = computed `all_agree`. |
| D-12 | **S2** | `molecular/webers_theory.py:82-108`; `theories/failure_modes.py:73-88` | 841-845 | Weber coefficient convention ½/1 vs Treatise 1/2 (ṙ², rr̈). Docstring matches code, so internally consistent; fidelity to Art. 845 doubtful. | Phase-1 formula sheet adjudicates against the 3rd-edition text; fix both files to the adjudicated convention; pin with a reference test. |
| D-13 | **S2** | `vortex_engine/magnetic_rotation.py:15-51` | 829 | Three contradictory formulas (docstring θ=(ω/c)(λ/2π)L — dimensionally a length; comment θ=(ω/2c)(r²/λ)L; code ωr²L/(cλ²)); dead variable `H_equiv` (line 44). | Choose the one formula the vortex model actually yields, state it once, delete dead code, Verdet-anchor per WP-3.1. |
| D-14 | **S2** | `electromagnetism/components/circular_coils.py:87-108` | 673-675 | Truncated 4-term elliptic series used for off-axis fields; K error → ∞ as k²→1 (near wire); duplicates `math/elliptic_integrals.py`. | Import/evaluate via `math/elliptic_integrals.py` (scipy or Landen); if a series is retained for speed, state error bound in docstring and test against scipy at k²=0.99. |
| D-15 | **S2** | `instruments/galvanometers.py:89-116` | 709 | `restoring = horizontal_field + torsion_constant` adds a torsion constant to a field without dividing by magnetic moment; torsion torque is θ-dependent, so the equilibrium is implicit, not `arctan`. `magnetic_moment` parameter (line 94) is never used. | Implement the correct torque balance mGI cosθ = mH sinθ + τθ; solve implicitly; use magnetic_moment. |
| D-16 | **S2** | `instruments/galvanometers.py:53,137` vs `electromagnetism/components/circular_coils.py:84` | 707-709 | Cross-module c-factor clash: same physical center-field computed as 2πnI/R (no c) here and 2πnIa²/(c·r³) (with c) there — factor 3×10¹⁰ discrepancy between modules (risk R9 realized). | Pick one CGS convention repo-wide (`cgs_unit_of`/`CONST.C`); add a consistency test that both modules agree for the same coil. |
| D-17 | **S2** | `electromagnetism/measurements/galvanometers_extended.py:985-1015` | 755-757 | `joule_balance` cites 755-757, but Ch XVII is "Comparison of Coils"; the Joule balance post-dates the 1873 Treatise (anachronism). Q=I²Rt is generic Joule law, not article-specific. | Re-map per Phase-1 verdicts (WP-3.4); if kept as extension, change theory_class and article numbers; implement genuine coil-comparison methods for 752-757. |
| D-18 | **S2** | `molecular/competing_theories.py:873-898` | 859-860 | `diamagnetic_response(applied_field, material_constant)` returns `material_constant` verbatim — applied_field ignored; default −1e-5 returned as "computed susceptibility". | Compute M = χH (and χ from a molecular-current model per Ampère theory) or remove the fake argument. |
| D-19 | **S2** | `experiments/ratio_v/theory.py:46-63` | 769 | `prove_ratio_is_velocity()` returns the hardcoded constant C_CGS — a "proof" that returns the answer. | Derive dimensions symbolically (SymPy: [q_ESU]/[q_EMU] = L·T⁻¹) and return the dimensional result; keep c only as the measured value in a separate anchored function. |
| D-20 | **S2** | `experiments/ratio_v/theory.py:66-91` | 770 | `calc_convection_current` returns q·v/c: q·v is not a current (needs a geometry/period), and the ESU→EMU conversion is misapplied (comment "1 ESU of charge = c EMU" conflates unit size with conversion direction). | Define the geometry (e.g., charge on rotating disc per Art. 770 analog), convert units via `core/units/dimensions.py`, test against `convert_esu_to_emu`. |
| D-21 | **S2** | `magneto_optics/energy_analysis.py:40-63, 84` | 818-819 | Docstring labels T=(εE²/8π)V "electric/potential" and V=(μB²/8π)V "magnetic/kinetic", but the return dict assigns `"kinetic_energy": T`, `"potential_energy": V_energy` — labels swapped. Separately, `delta_mu = 2·V·c/π` (line 84) is a fabricated Verdet↔permeability relation with no provenance and suspect dimensions. | Fix labels (or conventions, documented); derive delta_mu from the velocity-split relation of Arts. 811-817 or delete. |
| D-22 | **S2** | `vortex_engine/kinetic_energy.py:38, 69, 95-104` | 824-826 | Dimensional heuristics decorated `maxwell_original`: perturbation energy ½|δ|² with no density/stiffness; "coupling_energy" = (J·axis)·H has units of current-density×field, not energy; plane-wave term mixes 0.25 and /2 against its own comment. | Derive energies from the lattice parameters (ρ, ω, r) with stated formulas; or reclassify as `user_original` per D-08 boundary. |
| D-23 | **S2** | `optics/diffusion.py:83-247` | 806-808 | Beer-Lambert/absorbance/mean-free-path code cites the Faraday-effect opening articles of Ch XXI; chapter string also wrong ("Electromagnetic Theory of Light" ends at 805). | Remove/re-point the decorators (WP-3.1); if absorption physics is wanted, map to justified modern extension with `standard_math` and no article numbers. |
| D-24 | **S2** | `signal_processing/telegraphy.py:285-371` | 740, 745, 750 | Modern signal-integrity heuristics (2.2RC, 0.35/t_r, 1/(2t_r)) attributed to Treatise articles; fabricated chapter string "Signal Transmission"; docstring omits the ℓ² the code applies (298 vs 311). | Phase-1 adjudication (Decision D-06): re-decorate to correct articles or reclassify as `user_original`; fix docstring. Existing tests must be re-pointed, not extended. |
| D-25 | **S2** | `calibration/absolute_resistance.py:518-520,597-599`; `molecular/neumanns_theory.py:521-523,620-622` | 765-767; 856-858 | Six articles covered solely by `verify_*`/`analyze_*` meta-decorators (T0). | Article-specific implementations per Stage 1 §3.2 (WP-3.4, WP-3.5). |
| D-26 | **S2** | `docs/COVERAGE_SUMMARY.md:3-24` | all | Stale/wrong summary (1795 tests; Part I "1-206=126"; Part III "=26"; "Supplementary 796-866=320"). | Regenerate from fixed scanner only (WP-1.3); CI byte-consistency check. |
| D-27 | **S2** | `check_coverage.py:89-90, 107, 120` | 752-767 | Ch XVII (752,761) overlaps Ch XVIII (758,767) — live run prints 758-761 twice; scanner counts decorator presence only; aggregation keyed by basename. | Ch XVII → (752,757); automated continuity/overlap check; key by relative path; depth-aware report (WP-1.1). |
| D-28 | **S2** | `tests/` (absence) | ~120 articles | No test file imports instruments/, galvanometers_extended, ratio_v/, waves/, components/, boundary_conditions, coil_forces, gmd, magneto_optics/, vortex_engine/, coil_design, sensitivity, medium_check, failure_modes, philosophy/. | Stage 1 §3.2/Phase 3 bundles B/D/F first (WP-4.3/4.5/4.7). |
| D-29 | **S3** | `electromagnetism/components/circular_coils.py:89-90, 101-102` | 673-675 | `_elliptic_K`/`_elliptic_E` return π/2 for all m<0 (K(−1)≈2.06, not 1.57); silently wrong for any geometry producing negative parameter. | Delete the private approximants entirely (see D-14) or implement m<0 branch correctly. |
| D-30 | **S3** | `electromagnetism/components/circular_coils.py:13-14 vs 166-180` | 673-675 | Module-header formulas for B_ρ/B_z use an α/β parameterization that does not match the implemented standard form (prefactor 2I/(cβ²), α²=(a−ρ)²+z² denominator). | Rewrite header to the actually-implemented formulas with definitions of α², β², k². |
| D-31 | **S3** | `instruments/galvanometers.py:73-75` | 708 | `design_standard_coil` uses magic `0.9*max_radius` and `depth = 2r_wire√n` heuristics, not Maxwell's Art. 708 construction rules. | Implement the Treatise construction (WP-3.2) or document the heuristic as `standard_math` extension. |
| D-32 | **S3** | `magneto_optics/rotation.py:30-34, 151-163` | 807-809 | Verdet-constant unit drift: docstring "rad/T/m" (SI), comment "rad/(gauss*cm)", `VerdetTable` in minutes/(gauss·cm); downstream `apply_verdet_negative_rotation` claims to return radians. Mixing these silently errs by π/10800. | Single canonical unit (min/(G·cm) or rad/(G·cm)) declared once; convert explicitly in the table accessor; annotate `material_type` sign convention with a citation. |
| D-33 | **S3** | `ratio_v/combined.py:20`; `ratio_v/theory.py:19`; `magneto_optics/circular_polarization.py:78`; `magneto_optics/energy_analysis.py:79`; `vortex_engine/magnetic_rotation.py:38` | many | `c = 2.99792458e10` hardcoded locally in ≥5 modules while `CONST.C` exists (`config/constants.py:81`). | Use `CONST.C` exclusively (risk R9 mitigation); add a lint for the literal. |
| D-34 | **S3** | `electromagnetism/current_sheets/boundary_conditions.py:288-295` | (666), 667 | Decorator cites Art. 666 (below the 667-866 scope) for generic ∇·B boundary math, not current-sheet-specific content. | Adjudicate in Phase 1; restrict decorator to in-range articles with article-specific computations. |
| D-35 | **S3** | `theories/failure_modes.py:115-120` | 857-859 | Cites 857-858, which are Neumann-theory articles; the failure-analysis content maps better to Ch XXIII closing articles (859-866). Also `_maxwell_field_retarded` (101-112) is a toy radiation model presented as `maxwell_original`. | Re-decorate after Phase-1; mark toy model `standard_math`. |
| D-36 | **S3** | `tests/test_new_part_iv_molecular.py:376-410` | 841-866 | "Tests" for the qualitative dicts assert only dictionary key presence (`assert "velocity_dependent" in analysis`) — smoke tests that legitimize T0 coverage (risk R5 realized). | Replace with numeric asserts per REQ-T rubric once computed comparisons exist; until then they must not count toward T3. |
| D-37 | **S3** | `signal_processing/telegraphy.py:298 vs 311` | 740 | Docstring `t_r ≈ 2.2·R·C·L_line` (linear) vs code `line_length**2`. | Align docstring to the distributed-RC ℓ² law (and cite provenance). |
| D-38 | **S3** | `philosophy/medium_check.py:99-101` | 865-866 | `_wave_impedance` = √(μ/K)·(4π/c): the CGS plane-wave impedance is √(μ/K) (dimensionless ratio E/H); the extra 4π/c factor is not the standard Gaussian impedance. | Verify against formula sheet; likely drop 4π/c or document the convention. |
| D-39 | **S3** | `math/elliptic_integrals.py:293-298` | 702 | Trivial helper "parameter m = k²" decorated with Art. 702 — hijacks the article number, inflates 702's apparent coverage (also distorts Stage 1's "vis-only" characterization). | Re-point to a genuinely related article or remove the decorator. |
| D-40 | **S4** | `optics/diffusion.py:175-198` | 808 | `penetration_depth` returns `self.mean_free_path()` verbatim — duplicate API citing the same article twice. | Merge into one method or differentiate (1/e vs transport MFP). |
| D-41 | **S4** | `molecular/competing_theories.py:813, 902` | 859-866 | Naming drift: `maxwell_advantages` aliased as `maxwells_theory_advantages` solely for the test import. | Pick one name; update test. |
| D-42 | **S4** | repo-wide decorators | many | ≥15 free-form chapter strings not in the PARTS table ("Signal Transmission", "Current Weigher", "Joule Balance", "Failure Modes", "Theory Completeness", "Circular Field Lines", "Geometric Mean Distance", "Absolute Resistance", "Competing Theories", "Weber's Theory", …). | Lint decorator chapter strings against PARTS titles (WP-1.3). |

**Totals: 42 defects — S1: 5, S2: 23, S3: 11, S4: 3.** (U-claim confirmations are folded into D-01…D-14, D-23, D-24, D-25, D-27.)

---

## 4. Code-quality & coherence review

### 4.1 Architecture consistency across the last-200 modules

**Two conflicting CGS conventions coexist.** The dominant "c-explicit" family (Gaussian-flavored: `CONST.C` in every coil/field formula) includes `circular_coils.py`, `circular_fields.py`, `amperes_theory.py`, `medium_check.py`, `waves/wave_equation.py`, `galvanometers_extended.py`. A "c-free" family (EMU-flavored) includes `instruments/galvanometers.py` (G = 2πn/R; H_center = 2πnI/R — no c). For the *same physical quantity* (field at the center of a circular coil) the two families differ by a factor c ≈ 3×10¹⁰ (D-16). The repo already provides the standardization tools (`CONST.C`, `cgs_unit_of` at `config/constants.py:81,91`) — they are simply not used uniformly. This is the single most dangerous coherence defect because tests written per-module will pass while the modules disagree with each other.

**Constant hygiene.** `c` is re-hardcoded in at least 5 last-200 modules (D-33); `g = 980.665` hardcoded in the weigher; historical values (3.1e10, 3.15e10) inline in `medium_check.py` (acceptable with provenance comments, but should move to a reference-values store per D-05 decision).

**Module grain.** `galvanometers_extended.py` packs 19 articles / 1076 lines into one file; `competing_theories.py` packs 26 citations. Both are context-hostile for per-article work tickets (risk R11) and test-hostile (see §7). Splitting along article boundaries is recommended before WP-3.4/3.5.

**`verify_*` quality is bimodal.** Good pattern: `verify_coil_field` (circular_coils.py:352-413) and `verify_wave_speed` (medium_check.py:267-323) compute verdicts from independent expected values. Bad pattern: `verify_absolute_resistance` (circular), `verify_maxwell_relation` (hardcoded verdict), `verify_vortex_gear_condition` (vacuous True for <2 vortices). The anti-theater lint (§5.3) must be defined against the bad patterns and the good ones held as exemplars.

**Decorator discipline.** Multi-article decorators (up to 10 articles on one function) are the mechanical root of the coverage illusion; chapter strings drift from PARTS (D-42); one out-of-range citation (666, D-34); one article hijacked by a trivial helper (702, D-39).

### 4.2 Naming/API conventions vs the rest of the repo

- `calc_*` / `verify_*` / `analyze_*` prefixes are used consistently — good.
- Return-dict key naming is inconsistent: `"verified"` (bool) appears in some dicts, `"uniform"` in another (circular_coils.py:468), `"agrees"` per-row in medium_check; `verify_helmholtz_uniformity` returns two different key sets on its two return paths (lines 455 vs 462-469). Standardize one verdict schema (recommend: `{"value", "expected", "rel_error", "passed"}` with `passed` always computed).
- Dataclass-first design (WeberForce, MolecularCurrent, TelegraphLine, FaradayRotator) is consistent and test-friendly; keep it.
- Alias-for-test (`maxwells_theory_advantages`) is a smell (D-41).

### 4.3 Tier-promotion readiness per module (baseline)

| Module | Articles | Current tier (verified) | Ready for T3 uplift? | Blocker |
|---|---|---|---|---|
| components/circular_coils.py | 670-679 | T2 (untested) | Yes after D-14/D-29/D-30 | elliptic series |
| vis/circular_fields.py | 702 | T1 | No — D-02 wrong formula | rewrite A_φ |
| math/elliptic_integrals.py | 696-705 | T3 subset (57 tests) | Mostly ready | D-39 citation hijack |
| math/geometry/gmd.py | 691-693 | T2 (correct formulas, untested) | Yes | tests only |
| instruments/galvanometers.py | 707-720 | T1 | No — D-15/D-16/D-31 | dimensional repair |
| instruments/{suspended_coil,dynamometers,helmholtz,sensitivity} | 713-729 | T1-T2 | After review | tests + audit |
| measurements/galvanometers_extended.py | 736-757 | T1 | No — D-05/D-17 | split + re-map |
| signal_processing/telegraphy.py | 730-750 | T3-by-test but D-24 semantics | Hold 740/745/750 pending D-06 | adjudication |
| calibration/absolute_resistance.py | 758-767 | T2-T3 (758-764), T0 (765-767) | Partially — D-10 | de-circularize |
| experiments/ratio_v/* | 768-780 | T0-T1 | No — D-03/D-19/D-20 | math repairs + v-anchor |
| electromagnetism/waves/* | 781-795 | T2 (solid, untested) | Yes | tests only |
| optics/* | 781-808 | T3 subset (51 tests) | Yes except diffusion (D-01, D-23) | 4π/c² fix |
| magneto_optics/* | 807-821 | T0-T1 | No — D-04/D-06/D-07/D-21/D-32 | full uplift (WP-3.1) |
| vortex_engine/* | 822-831 | T0-T1 | No — D-08/D-13/D-22 | full uplift |
| molecular/amperes_theory.py | 832-840 | T3 (832-837), T0 (838-840) | Partially | article-specific 838-840 |
| molecular/webers_theory.py | 841-850 | T2-T3 core, T0 (848-850) | After D-12 adjudication | coefficient fix |
| molecular/neumanns_theory.py | 851-858 | T2-T3 core, T0 (856-858) | Partially | article-specific 856-858 |
| molecular/competing_theories.py | 841-866 | T0-T1 dicts | No — D-09/D-18 | compute-or-delete |
| theories/failure_modes.py | 857-859 | T1 | No — D-35 | re-map |
| philosophy/medium_check.py | 865-866 | T2 | After D-11/D-38 | data + verdict fix |

---

## 5. Quality gates

### 5.1 P2-exit gate (end of T0/T1 → T2 uplift; Stage 2 Gate G2)

Implementation teams MUST present all of the following; QUALITAS verifies, never the implementing agent:

- [ ] **Zero T0** in 667-866: no article's only citations are `verify_*`/`analyze_*`/vis functions; no `return True`/dict-of-strings implementations remain (D-06..D-08, D-19, D-25 closed).
- [ ] Every article has ≥1 **article-specific computation** (ledger field, machine-derived).
- [ ] **Theater remediated:** D-09 (scores computed-or-deleted), D-10 (independent cross-methods; velocity_check computed), D-11 (verdict computed; optical data) — verified by diff review, not by author assertion.
- [ ] **All S1 defects closed** (D-01..D-05), each with a failing-before/passing-after regression test.
- [ ] **Anti-theater lint green** (§5.3) in `run_quality_checks.sh`.
- [ ] Existing suite green (≥1947 tests; any intentional behavior change listed in the gate report).
- [ ] Decorator lint green: chapter strings ∈ PARTS titles; no out-of-range article numbers; no decorator with ≥5 articles lacking per-article justification comment.
- [ ] Unit-convention decision recorded in the decision log and applied (D-16, D-33); `CONST.C`/`cgs_unit_of` used exclusively.

### 5.2 P3-exit gate (end of T2 → T3 tests; Stage 2 Gate G3)

- [ ] 200/200 articles carry ≥1 passing `pytest.mark.article(N)` test.
- [ ] Each marked test satisfies the **qualifying rubric**: asserts a numeric value/limit/identity with stated tolerance sourced from `tests/articles/reference_values.json` (provenance field mandatory). Key-presence/bool-only asserts do not qualify (D-36 class disallowed).
- [ ] Meta-test `test_article_coverage.py` green; demonstrated red when any marked test is removed (mutation check at gate).
- [ ] v ≈ 3.1×10¹⁰ cm/s anchor test present for Ch XIX (Weber-Kohlrausch value with historical tolerance).
- [ ] Cross-module c-consistency test green (circular_coils vs galvanometers vs amperes_theory conventions reconciled).
- [ ] Suite ≈2,300+ green; runtime budget ≤10 min; zero flaky (rerun-stable).
- [ ] Ledger recomputed; all articles ≥ T3; ledger diff reviewed by INDEPENDENT GATE REVIEWER.

### 5.3 Anti-theater lint rules (must never pass review)

Static patterns for the WP-1.4 gate (grep/AST level):

1. **Literal verdicts:** `"verified": True`, `"agrees": True`, `"passed": True`, `"ok": True` (or False literals) inside any `verify_*`/`prove_*`/`check_*` function body. Verdicts must be expressions derived from compared quantities.
2. **Bare-bool stubs:** `return True`/`return False` as the entire body of any decorated function whose name starts with `verify_`, `prove_`, `check_`, `is_`.
3. **Prose-as-implementation:** any `maxwell_original`-decorated function whose only returns are dicts/lists of `str` (AST check).
4. **Circular cross-checks:** within one function, a variable produced by method A feeding the input of method B whose output is then compared to method A's output (heuristic AST pattern: `x = A(...); y = B(..., f(x), ...); assert/error(x, y)` where B inverts f). Require ≥1 externally-sourced reference input per `verify_*`.
5. **Invented scores:** dict keys matching `*agreement*|*score*|*confidence*` whose values are bare numeric literals without an adjacent provenance comment naming source/derivation.
6. **God-decorators:** `@maxwell_cite` with ≥5 article numbers unless the decorator carries `range_justification="..."`.
7. **Hardcoded physical constants:** literal `2.99792458e10` (or 3e10-family) outside `maxwell/config/constants.py`; literal `980.665` outside a constants/data module.
8. **Chapter drift:** decorator `chapter=` value not in the PARTS title set.
9. **Out-of-range citations:** in last-200 work, any decorator article < 667 without parking-lot annotation (scope fence R13).
10. **Test theater:** marked article tests containing no numeric assert (only `in`, `isinstance`, key-presence, or bare bool asserts).

---

## 6. Certification criteria for tier promotion

### T3 ("ensured") — evidence requirements, per article
1. **REQ-F:** ≥1 exported function/class-method whose computation is specific to the article; no stub/prose returns under *any* theory_class (closing the loophole exploited by 820/821's `standard_math`).
2. **REQ-M:** formula matches the Phase-1 formula sheet (CGS, explicit c/4π); docstring formula and code textually derivable from the same expression; any approximation carries a stated, tested error bound.
3. **REQ-V:** ≥1 reference value in `tests/articles/reference_values.json` with provenance (Treatise article/page, or derivation ID): Maxwell's own numbers where the text gives them (v ≈ 3.1×10¹⁰ cm/s; GMD self-factor e^{−1/4}≈0.7788; Helmholtz uniformity; dipole axis/equator 2/−1 ratios), else analytic limits/identities.
4. **REQ-T:** ≥1 passing `pytest.mark.article(N)` test asserting the REQ-V value within stated tolerance, certified by QUALITAS (not the implementer).
5. Zero open defects with severity ≤ S2 touching the article.

### T4 (cross-validated) — additionally
1. SymPy identity registered in `verification/sympy_verify.py` following the Art. 787 exemplar (`article_refs` tuple), passing in CI, and **symbolically independent** of the implementation under test (no restatement of the same code path).
2. Page-verifier verdict "yes" for the article's Vol II pages (or formally annotated "n/a — derivative result").
3. Triple signature recorded in the ledger: MATHEMATICA (symbolic) + QUALITAS (numeric) + ARCHITECTUS (traceability); HUMAN acceptance at G4.
4. For spine articles (670-706, 752-780, 781-795): T4 is mandatory at program exit (Stage 2 E9); ≥60 verifiers total.

Promotion attempts by the implementing agent on its own work revert automatically (Stage 2 §5.4).

---

## 7. Handoff to Stage 4 (testing specialist)

### 7.1 Defects needing regression tests FIRST (in this order)

1. **D-03** (ratio_v correction inverted) — trivial to test, currently silently wrong: `charge_fraction=0.5` must halve v_meas.
2. **D-04** (Δn factor 2) — test the closed loop: rotation_per_length from `perform_kinematic_analysis` must equal V·B.
3. **D-01** (diffusion τ units) — dimensional/regime test with a documented conductor; also catches the intra-file contradiction.
4. **D-02** (A_φ asymptotic) — near-axis ψ ∝ ρ² test + B=∇×A cross-check vs `calc_coil_off_axis`.
5. **D-16/D-33** (c-convention) — one cross-module consistency test before ANY instrument tests are written, otherwise the wrong convention gets enshrined.
6. **D-14/D-29** — off-axis field vs scipy reference at k² = {0.5, 0.9, 0.99, 0.9999}.
7. **D-12** — after adjudication: Weber force coefficient pin test (ṙ² term only, a=0).
8. **D-11** — water optical data test (n=1.33, K=1.77) which must fail against the current rigged row.
9. **D-05** — weigher against one independently computed dM/dx (elliptic formula) at a documented geometry.
10. **D-21** — energy-label semantics test (E-field energy must be the electric term).

### 7.2 Test-hostile modules requiring refactoring before bundling

- **`galvanometers_extended.py`** (1076 lines, 19 articles): split per instrument class first (WP-3.4); current single-file import surface invites giant fixtures.
- **`competing_theories.py`**: dict-only APIs give tests nothing numeric to assert until D-09 remediation; write tests against the *new* computed metrics only.
- **`vortex_engine/*`**: tightly coupled dataclasses with no physical anchor values; needs at least one calibrated lattice case (wave speed = c claim, note_4 of D-08) before bundle F.
- **`optics/diffusion.py`**: mixed-chapter content (Ch XX + misplaced 806-808) — re-map (D-23) before tests, else tests encode wrong article bindings.
- **`signal_processing/telegraphy.py`**: existing 54 tests cover Telecom-class heuristics well, but tests for 740/745/750 must be quarantined pending D-06 adjudication or they enshrine anachronisms.
- **Inline-import style** (all four existing Part-IV test files import inside test bodies): acceptable, but Stage 4 should standardize module-level imports for collect-time failure detection.

### 7.3 What Stage 4 can rely on (verified strengths)

- `math/elliptic_integrals.py` + `math/spherical_harmonics.py`: real math, 57 tests, Landen/scipy available — good exemplar for T4 verifiers.
- `molecular/amperes_theory.py` core: correct dipole math with numeric tests (axis/equator 2/−1) — model for bundle G.
- `electromagnetism/waves/wave_equation.py`: internally sound (v=c/√εμ, B₀=E₀/v, transversality) — tests-only gap, high ROI.
- `math/geometry/gmd.py`: correct GMD definitions incl. self-GMD e^{−1/4} — ready for validation cases (Arts. 691-693).
- `calibration/absolute_resistance.py` method cores (recoil/Lenz/rotating/energy): individually correct formulas; only the meta-verifier is circular.

---

*Stage 3 deliverable complete. Handoff to Stage 4: §3 defect register (42 defects), §5 gates, §7 priorities. All upstream claims verified read-only against the tree at commit state 2026-08-21; 1,947 tests collect; no source modified.*

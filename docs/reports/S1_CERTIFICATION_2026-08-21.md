# S1 Defect Certification Record — 2026-08-21

**Certifier:** QUALITAS (sole certifier; implementer ≠ certifier rule, Stage 2 §5.4)
**Scope:** Stage-3 S1 defects D-01..D-05 (register: `docs/LAST200_STAGE3_QUALITY_REVIEW.md` §3; regression specs: `docs/LAST200_STAGE4_TESTING_STRATEGY.md` §4.1)
**Verdict:** ALL FIVE FIXES CERTIFIED. Tier promotions granted (see §4).

## 0. Suite results (independently re-run by QUALITAS)

| Run | Command | Result |
|---|---|---|
| Baseline (pre-edit) | `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/ -q` | **6 failed, 1946 passed** — failure set EXACTLY the expected 5 XPASS(strict) in `tests/test_defects_s1.py` + `TestFieldDiffusion::test_diffusion_length`; no unexpected reds |
| Verification | `python -m pytest tests/test_defects_s1.py --runxfail -v` | **5 passed** (R1-R5 pass under their own assertions) |
| Final (post-edit) | `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/ -q` | **1952 passed, 0 failed, 0 errors, 0 xfailed** |

## 1. Per-defect certification

### D-01 — Arts. 801-803 (PHYSICUS)
- **Defect:** `τ = σL²` omitted 4π/c² (dimensionally a diffusivity, not a time); `calc_diffusion_length` inverted inconsistently.
- **Fix location:** `maxwell/optics/diffusion.py:663` (`calc_diffusion_time` → `4.0*np.pi*sigma*L**2/CONST.C**2`), `:701` (`calc_diffusion_length` → `sqrt(t*CONST.C**2/(4*np.pi*sigma))`), consistent pair also in `verify_diffusion_equation` `:744-747`.
- **Independent verification (QUALITAS hand calc):** τ = 4πσL²/c² with σ_Cu = 5.35e17 s⁻¹, L = 1 cm, c = 2.99792458e10 cm/s → **7.4804e-3 s** (matches test golden value 7.4804e-3, rel 1e-3). Unit sanity: σ_CGS = σ_SI/(4πε₀) = 5.96e7/1.11265e-10 = **5.357e17 s⁻¹**, confirming the s⁻¹ CGS convention. Round-trip L(time(L)) = L passes at rel 1e-9.

### D-02 — Art. 702 (PHYSICUS)
- **Defect:** `_vector_potential_azimuthal` prefactor wrong (near-axis ψ ∝ ρ^4.5 instead of ρ²; B = ∇×A off by ~1e3).
- **Fix location:** `maxwell/electromagnetism/vis/circular_fields.py:51-95` (standard elliptic form A_φ = (I/c)(α/ρ)[(2−m)K(m)−2E(m)], m = 4aρ/α², at `:89-93`).
- **Independent verification:** (i) my own direct quadrature A_φ = (Ia/c)∮cosφ′ dφ′/|r−r′| agrees with the implementation at rel ≤ 9e-11 over (ρ,z) = {(0.01,0), (0.1,0), (5,2.5), (8,−3)}, and matches the analytic near-axis limit πIρ/(ca); (ii) log-log slope of ψ = ρA_φ = 2.00 ± 0.05; (iii) B = ∇×A matches the independent Biot-Savart oracle at rel 1e-3 (finite-difference curl tolerance).

### D-03 — Art. 777 (CIRCUITUS)
- **Defect:** `apply_rapid_action_correction` DIVIDED by charge_fraction, amplifying the under-charge error.
- **Fix location:** `maxwell/experiments/ratio_v/combined.py:159` (`return measured_v * charge_fraction`).
- **Independent verification:** engineered case 1−exp(−t½/RC) = 0.5 exactly (t½/RC = ln 2) → corrected v = **0.5** (halved, rel 1e-12); property guard: correction < measured for all charge_fraction < 1 (three cases).

### D-04 — Art. 812 (PHYSICUS)
- **Defect:** Δn = 2VλB/π carried a spurious factor 2.
- **Fix location:** `maxwell/magneto_optics/circular_polarization.py:81` (`delta_n = verdet_constant*wavelength*magnetic_field/PI`).
- **Independent verification:** my own derivation θ = VBL = (k_L−k_R)L/2 → Δk = 2VB → Δn = cΔk/ω = VBλ/π = **1.875800e-3** (V=0.1, B=1000 G, λ=5.893e-5 cm); implementation gives Δv = cΔn/n² = **2.499337e7 cm/s** at rel 1e-12. Kinematic closed loop rotation_per_length = (k_right−k_left)/2 holds at rel 1e-12.

### D-05 — Arts. 751-754 (INSTRUMENTUM)
- **Defect:** `current_weigher` mixed SI/Gaussian/EMU (spurious c² divisor, invented near-field factor r²/(d²+r²)); force ~1e-23 dyn instead of ~1.24 dyn.
- **Fix location:** `maxwell/electromagnetism/measurements/galvanometers_extended.py:970-1068` (pure EMU `force = current**2 * dM_dx` at `:1053`; dM/dx from analytic elliptic derivative via `_coaxial_mutual_gradient_emu` `:1046`).
- **Independent verification:** my own DOUBLE LINE INTEGRAL (Neumann) oracle — no elliptic integrals — gives dM/dx = **−123.994** for a = 10 cm, d = 1 cm, hence F = I²|dM/dx| = **1.2399 dyn** (I = 0.1 abA), matching the test's elliptic-gradient oracle (rel 2e-3) and the implementation. equivalent_mass = F/980.665 self-consistent at rel 1e-12.

**Oracle audit:** all reference values in R1-R5 were re-derived independently above (two spot-checks mandated: D-01 copper τ = 7.4804 ms ✓; D-03 fraction 0.5 halves ✓; plus D-02 quadrature, D-04 derivation, D-05 line-integral cross-checks). No oracle found wanting; none certified over a wrong oracle.

## 2. Test-file changes (QUALITAS)

1. `tests/test_defects_s1.py` — removed the five `@pytest.mark.xfail(strict=True)` decorators from R1-R5; KEPT all `@pytest.mark.article(...)` and `@pytest.mark.regression(defect="D-0X")` markers and the docstrings; module header updated (defects fixed 2026-08-21; tests are permanent green regression guards); five stale "CURRENTLY ..." inline comments restated in past tense (comment-only, zero assertion changes).
2. `tests/test_new_part_iv_optics.py::TestFieldDiffusion::test_diffusion_length` — enshrined defective assertion `L_diff < 1.0` (= √(t/σ) behavior) REPLACED by correct physics L_diff = √(t·c²/(4πσ)), citing Arts. 801-803 and defect D-01 (fixed 2026-08-21); asserts the symbolic value (rel 1e-12) and the hand-computed golden **26.74334770792584 cm** (rel 1e-9), plus the qualitative guard L_diff ≪ c·t. Assertion STRENGTHENED, not weakened. Sibling tests untouched (note: `test_diffusion_time_scale` asserts only τ > 0 and passes; its docstring formula predates the fix — cosmetic, no functional impact).

## 3. Evidence report

`docs/reports/article_evidence_report.json` regenerated during the final green run (generated 2026-08-21T20:35:51Z): `articles_covered: 6`, `total_marked_tests: 6`, mapping articles **702, 751, 777, 801, 802, 812** to the five R1-R5 regression tests, all PASSING in the final suite. (gate_G3 reads FAIL solely on 6/200 article coverage of the 667-866 range — unrelated to S1.)

## 4. Tier outcome

Per Stage 3 §6 REQ-T (passing `pytest.mark.article(N)` numeric test with independent oracle, certified by QUALITAS), the following articles are promoted **T2 → T3 (numerically tested with independent oracle)**:

- **Art. 702** (D-02 fixed, R4 green)
- **Arts. 751-754** (D-05 fixed, R5 green; article-marked evidence at 751, fix scope covers 751-754)
- **Art. 777** (D-03 fixed, R1 green)
- **Arts. 801-803** (D-01 fixed, R3 green; article-marked evidence at 801/802, fix scope covers 801-803)
- **Art. 812** (D-04 fixed, R2 green)

Zero open S1 defects remain. T4 promotion additionally requires SymPy identity verifiers + page-verifier verdicts (Stage 3 §6 T4) — out of scope here.

**Files changed by QUALITAS:** `tests/test_defects_s1.py`, `tests/test_new_part_iv_optics.py`, `docs/reports/S1_CERTIFICATION_2026-08-21.md` (this file). No `maxwell/` source touched.

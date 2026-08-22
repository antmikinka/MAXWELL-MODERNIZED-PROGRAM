---
type: test_strategy
pipeline_stage: 4 of 4 (Testing & Quality Strategy)
input_artifacts:
  - docs/LAST200_STAGE1_PLANNING_ANALYSIS.md
  - docs/LAST200_STAGE2_PROGRAM_MANAGEMENT.md
  - docs/LAST200_STAGE3_QUALITY_REVIEW.md
status: complete
collab_reviewed: false
---

# LAST 200 ARTICLES (667-866) — Stage 4 Testing & Quality Strategy

**Pipeline stage:** 4 of 4 (Testing & Quality Strategy)
**Date:** 2026-08-21
**Method:** Read-only exploration plus read-only test execution. All upstream claims re-measured: AST parse of every `@maxwell_cite` decorator under `maxwell/`; AST parse of every import/method-call in `tests/` mapped to the article→file index; `pytest --collect-only` (1,947 tests); full-suite execution under a clean plugin environment; live verification of golden constants with scipy. No source file was modified.

---

## 0. Executive summary — measured baseline

| Quantity | Measured value | Method |
|---|---|---|
| Tests collected | **1,947** in 8.75 s | `pytest tests/ --collect-only -q` |
| Tests passing (clean env) | **1,947 passed in 103.5 s** | full run with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` |
| Articles decorated (667-866) | **200 / 200** | my own AST decorator parse (variadic positional form) |
| Single-cite articles | **42** — list identical to Stage 1 Appendix A | AST parse (independent confirmation) |
| `pytest.mark.article(N)` in tree | **0 occurrences** | grep of `tests/` |
| `tests/articles/` directory | **does not exist** | `ls` |
| Articles with zero function-level test contact | **100 / 200 (50.0%)** | AST cross-map (§1.4) |
| Articles with no *qualifying* numeric test | **137 / 200 (68.5%)** | §1.5 (adds meta-only 28, vis-only 1, smoke-only 8) |
| Clean T3-grade candidates today | **≈58 (29%)** | §1.5, consistent with Stage 1 "≈50 at T3" |
| SymPy verifiers in range | **1** (Art. 787, `verification/sympy_verify.py`) | Stage 3 U22, re-confirmed |
| page_verifier verdicts for 667-866 | **0** (7 verdicts, all Vol I) | `verdicts.json` read |

**Environment finding (new, CI-critical):** on the dev machine the suite *hard-crashes* (numpy LAPACK `Aborted` inside `leggauss→eigvalsh`; ~37 setup ERRORs in `test_new_part_iv_math.py` alone). Root cause isolated: globally installed pytest plugins (**pytest-randomly** reseeding through **thinc**'s `fix_random_seed` hook, seed-boundary `ValueError`) — *not* project code. With `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` the same files pass 242/242 in <1 s. **CI must pin a clean venv and set `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`.** (§7)

**Headline test targets:** 200 article-marked qualifying tests (one-plus per article, G3 gate) + 15 defect-regression tests (5 S1 + 10 S2) + ~15 meta-tests + ~10 cross-module consistency tests ⇒ **≈350-420 new tests**, final suite **≈2,300-2,370 green**, full-suite budget **< 5 min** (measured headroom: current suite runs in 1:43).

---

## 1. Current-state test audit

### 1.1 Method

1. `pytest --collect-only -q` → 1,947 tests.
2. AST parse of all `maxwell/**.py` (excluding `__pycache__`) collecting every `@maxwell_cite` call with **all positional int arguments and int-list first arguments** → `article → [(file, function)]` index (200 articles; 0 missing).
3. AST parse of every `tests/test_*.py`: module-level and function-body `ImportFrom maxwell.*` plus attribute accesses (to catch method calls on imported classes). A citing function counts as *touched* if it is imported directly or its name is used as an attribute in a test file that imports its module.
4. Classification per article: **SUBSTANTIVE** (a non-`verify_*`/`analyze_*`, non-vis citing function is touched), **VIS-ONLY**, **META-ONLY** (only `verify_*`/`analyze_*` touched), **NONE**.
5. Manual demotions for known theater (D-36 smoke tests) and defect-enshrinement (§1.5).

### 1.2 Test files that cover any of Arts 667-866 today

| Test file | Collected | Last-200 modules exercised | Articles touched |
|---|---|---|---|
| `test_new_part_iv_math.py` | 57 | `math/elliptic_integrals.py`, `math/spherical_harmonics.py` | 675-678, 685-695, 696-705 (partial) |
| `test_new_part_iv_optics.py` | 51 | `optics/{constants,crystals,diffusion,metals,plane_waves,radiation_pressure,velocity}.py` | 786-805 (partial; 801-802 via defective D-01 functions) |
| `test_new_part_iv_signal_calibration.py` | 54 | `signal_processing/telegraphy.py`, `calibration/absolute_resistance.py` | 730-735, 740/745/750 (via `SignalTransmission` methods), 758-764 |
| `test_new_part_iv_molecular.py` | 33 | `molecular/{amperes,webers,neumanns,competing}_theory(ies).py` | 832-837, 841-842, 852-854 substantive; 859-866 smoke-only |
| `test_part_iv_advanced.py` | 47 | `core/units/dimensions.py` (+ out-of-range `general_equations`) | 771-773 (+ 781 via `verify_speed_of_light_relationship`, meta) |
| `test_sympy_verify.py` | 66 | `verification/sympy_verify.py` (15 verifiers) | 787 only in range |
| `test_vis_molecular_vortices.py` | 22 | `vis/molecular_vortices.py` | 822 (vis-only) |
| `test_vis_em_wave_propagation.py` | 15 | `vis/em_wave_propagation.py` | 791 neighborhood (vis-only) |
| `test_vis_spherical_harmonics.py` | — | `vis/spherical_harmonics.py` | 685-695 (vis-only) |
| `test_magnetic_measurements.py` | 53 | `magnetism` (Part III) | none in range |
| `test_cross_validation.py` / `test_verification_framework.py` | 15 / 14 | verification infra | framework only |

**Zero test imports (confirmed by exhaustive import map):** `instruments/` (all 5 files), `electromagnetism/measurements/galvanometers_extended.py`, `experiments/ratio_v/` (all 3 files), `electromagnetism/waves/` (all 3 files), `electromagnetism/components/` (circular_coils, solenoids, cylinders), `electromagnetism/current_sheets/boundary_conditions.py`, `electromagnetism/forces/coil_forces.py`, `math/geometry/gmd.py`, `electromagnetism/optimization/coil_design.py`, `instruments/optimization/sensitivity.py`, `magneto_optics/` (all 3 files), `vortex_engine/` (all files), `philosophy/medium_check.py`, `theories/failure_modes.py`, `optics/wave_equation.py`, `electromagnetism/vis/circular_fields.py`.

### 1.3 Per-chapter-cluster test-density table

SUB = substantive (upper bound, §1.5 demotions below); META = only `verify_*`/`analyze_*` exercised; NONE = no function-level contact. Host-file tests are the collected counts above.

| Cluster | Arts | n | SUB | META | VIS | NONE | Host tests | Tests/article (nominal) | Qualifying today |
|---|---|---|---|---|---|---|---|---|---|
| A — Ch XII-XIV tail + math spine | 667-706 | 40 | 19 | 6 | 0 | 15 | 57 (+vis) | 1.4 | ~17 (2 demoted: 694/695 borderline) |
| B — Ch XV-XVI instruments & observations | 707-751 | 45 | 9 | 0 | 0 | 36 | 54 (shared w/ C) | ~0.6 | ~6 (740/745/750 held pending D-06) |
| C — Ch XVII-XVIII coil comparison & resistance | 752-767 | 16 | 7 | 3 | 0 | 6 | (54 shared) | ~1.8 | ~7 |
| D — Ch XIX ratio-V | 768-780 | 13 | 3 | 0 | 0 | 10 | ≤10 of 47 | ~0.6 | 3 (771-773) |
| E — Ch XX EM theory of light | 781-805 | 25 | 15 | 2 | 0 | 8 | 51 | 2.0 | ~13 (801/802 defect-enshrined) |
| F — Ch XXI magneto-optics & vortex | 806-831 | 26 | 0 | 0 | 1 | 25 | 22 (vis, for 822 only) | 0.0 substantive | **0** |
| G — Ch XXII-XXIII molecular & action-at-distance | 832-866 | 35 | 18 | 17 | 0 | 0 | 33 | 0.9 | ~10 (859-866 smoke demoted) |
| **Total** | 667-866 | **200** | **71** | **28** | **1** | **100** | | | **≈58 clean** |

### 1.4 True zero-coverage article list

**(a) Zero function-level test contact — 100 articles** (no citing function, not even meta, is exercised by any test):

```
A (15): 667 668 669 670 671 672 673 674 679 680 681 682 683 684 693
B (36): 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722 723 724
        725 726 727 728 729 736 737 738 739 741 742 743 744 746 747 748 749 751
C (6):  752 753 754 755 756 757
D (10): 768 769 770 774 775 776 777 778 779 780
E (8):  782 783 784 785 793 795 796 800
F (25): 806 807 808 809 810 811 812 813 814 815 816 817 818 819 820 821 823 824
        825 826 827 828 829 830 831
G (0):  —
```

**(b) No qualifying numeric test — 137 articles** = (a) 100 + META-ONLY 28 (`694 695 703 704 705 765 766 767 781 803 834 838 839 840 843 844 845 846 847 848 849 850 851 855 856 857 858` + 1 borderline) + VIS-ONLY 1 (822) + smoke-only 8 (859-866, key-presence asserts per D-36).

**137 / 200 = 68.5% of the range has no test that could support a T3 promotion today.** Cluster F (Ch XXI) is the only chapter with literally zero substantive contact (0/26); Cluster B is the largest mass (36/45 zero-contact).

### 1.5 Corrections & refinements vs upstream stages (verified, file:line-level)

1. **740/745/750 ARE tested** — via `SignalTransmission` class methods: `tests/test_new_part_iv_signal_calibration.py:190-222` (`TestSignalTransmission.test_rise_time` asserts `t_r = 2.2·R·C·ℓ²` with tolerance). Stage 1's claim stands; however these tests **enshrine the D-24 anachronisms** — they must be quarantined, not extended, pending D-06 adjudication.
2. **`optics/wave_equation.py` is imported by NO test** despite being a listed host for Ch XX articles — 781-785 coverage relies solely on `electromagnetism/waves/*`, which is also untested ⇒ 781 is META-only (via `dimensions.verify_speed_of_light_relationship`), 782-785 NONE.
3. **790/793/795/796/800** sit in imported optics modules but their citing functions (`calc_fresnel_reflection_metal`, `normal_reflectance`, `stokes_parameters`, `calc_wave_interference`, Jones machinery) are never called ⇒ NONE despite module import. Module-level coverage metrics overcount here.
4. **834-837**: citing functions (`vector_potential_at`, `magnetization`, `susceptibility`, `bound_current_density`) appear as attribute accesses in the molecular test file — counted SUBSTANTIVE (upper bound) but the numeric-assert requirement is unverified; WP-4.1 must confirm per REQ-T.
5. **735**: `voltage_at_distance` touched only via attribute heuristic ⇒ SUBSTANTIVE upper bound; likely qualifies only after confirmation.
6. **801-802 are defect-enshrined**: `test_new_part_iv_optics.py` imports `calc_diffusion_time`/`calc_diffusion_length` (the S1-defective D-01 functions). Their current tests pass against the wrong formula (self-consistent). They flip at D-01 fix by design.
7. **K(−1) golden value correction**: Stage 3 D-29 states K(−1)≈2.06; scipy gives **K(m=−1) = 1.3110287771** (verified live). Use the measured value in the D-29 regression.
8. **Suite-green is environment-relative**: see §0 environment finding; all upstream "tests green" statements hold only under clean plugin autoload.

### 1.6 Audit tooling (to be committed at WP-4.1)

The AST cross-mapper used for §1.3-1.4 (decorator parse → article index → test import/method matching → classification) becomes `scripts/article_coverage_audit.py`, re-run at every gate; its JSON output feeds the ledger (WP-1.2) and the G3 evidence report (§7.5). This makes the audit reproducible and removes all hand-counting from tier claims.

---

## 2. Test architecture

### 2.1 The `pytest.mark.article(N)` marker scheme

Registration in `pyproject.toml` `[tool.pytest.ini_options]` (existing markers `jax/sympy/slow/visualization` kept):

```toml
markers = [
    "jax: tests requiring JAX (accel extra)",
    "sympy: tests requiring SymPy (symbolic extra)",
    "slow: tests that take a long time to run",
    "visualization: tests for matplotlib visualization",
    "article(N): test provides evidence for Treatise article N (int, 1-866)",
    "regression(defect): failing-before/passing-after test for defect register ID",
    "quarantine: test enshrines unadjudicated content (D-06 etc.); excluded from G3 count",
]
```

Conventions:
- Every qualifying test carries exactly one `@pytest.mark.article(N)` (parametrized tests may cover several articles via `pytest.param(..., marks=[pytest.mark.article(N)])`).
- Naming: `test_art_<NNN>_<topic>` inside `tests/articles/test_part_iv_<chapter-cluster>.py`; regression tests: `tests/articles/regressions/test_defects_s{1,2}.py` with names `test_regression_D<id>_art<NNN>_<behavior>`.
- Module-level imports only in new bundles (collect-time failure detection; Stage 3 §7.2(f)) — breaking the current inline-import style.

### 2.2 conftest additions + article-coverage report plugin (concrete code)

`tests/articles/conftest.py` — marker validation, evidence-map builder, and terminal report:

```python
"""Article-evidence plugin: validates article marks, builds the
article -> test evidence map, emits the G3 evidence report."""
from __future__ import annotations
import json, pathlib
import pytest

RANGE = range(667, 867)          # LAST200 scope fence (R13)
REPORT_JSON = pathlib.Path("docs/reports/article_evidence_report.json")

def pytest_configure(config):
    config.addinivalue_line("markers", "article(N): evidence for Treatise article N")
    config._article_map = {}      # article -> list of nodeids

def pytest_collection_modifyitems(config, items):
    amap = config._article_map
    for item in items:
        for mark in item.iter_markers(name="article"):
            if not mark.args:
                raise pytest.UsageError(f"{item.nodeid}: article marker needs N")
            n = mark.args[0]
            if not isinstance(n, int) or n not in range(1, 867):
                raise pytest.UsageError(f"{item.nodeid}: bad article number {n!r}")
            if n in RANGE and "quarantine" not in [m.name for m in item.iter_markers()]:
                amap.setdefault(n, []).append(item.nodeid)

def pytest_terminal_summary(terminalreporter, config):
    """Emit the article->test evidence map (G3 evidence artifact)."""
    amap = getattr(config, "_article_map", {})
    missing = [n for n in RANGE if n not in amap]
    report = {
        "range": [667, 866],
        "articles_covered": len(amap),
        "articles_missing": missing,
        "gate_G3": "PASS" if not missing else "FAIL",
        "evidence": {str(n): amap[n] for n in sorted(amap)},
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=1))
    tr = terminalreporter
    tr.write_sep("=", "ARTICLE EVIDENCE MAP (667-866)")
    tr.write_line(f"covered {len(amap)}/200  missing {len(missing)}")
    if missing:
        tr.write_line("missing: " + " ".join(map(str, missing[:50]))
                      + (" ..." if len(missing) > 50 else ""))
```

The G3 **meta-test** (`tests/articles/test_article_coverage.py`) imports the generated map (or recomputes via `pytest --collect-only` subprocess) and fails while any of 667-866 lacks a marked test. A **mutation check** is mandatory at the gate: temporarily delete one marked test ⇒ the report must flip that article to missing (demonstrates the meter works; Stage 2 §8.3 requirement).

### 2.3 Qualifying-test rubric enforcer (anti-R5)

`tests/articles/meta/test_meta_rubric.py` AST-parses every `pytest.mark.article`-marked test body and requires ≥1 of: `pytest.approx(...)`, `math.isclose`, `assert_cgs_close`, `assert_vectors_close`, or a comparison against a `reference_values.json` entry with explicit tolerance. Key-presence (`in`), `isinstance`, and bare-bool-only tests fail the rubric (this mechanically disallows the D-36 class).

### 2.4 Fixtures: physical constants and CGS/SI guardrails

Extend the existing `tests/conftest.py` (keep `cgs_tolerance=1e-10`, `cgs_coarse_tolerance=1e-6`, `assert_cgs_close`, `assert_vectors_close`, `require_citation`, `validate_citation_articles` — they are sound):

```python
@pytest.fixture(scope="session")
def cgs_constants():
    """Single source of truth for CGS constants (D-33 guardrail)."""
    from maxwell.config.constants import CONST
    return {"c": CONST.C, "g": CONST.G_STANDARD}   # c = 2.99792458e10 cm/s

@pytest.fixture
def assert_dimensions():
    """Dimensional guardrail: assert a result's CGS dimensions match.

    Uses core.units.dimensions / cgs_unit_of so that a silent
    SI/CGS or factor-c drift (D-16 class) fails loudly."""
    from maxwell.config.constants import cgs_unit_of
    def _check(quantity, expected_unit_symbol):
        assert cgs_unit_of(quantity) == expected_unit_symbol
    return _check

@pytest.fixture
def ref_value():
    """Load a golden value + tolerance + provenance from the central store."""
    store = json.loads(pathlib.Path(
        "tests/articles/reference_values.json").read_text())
    def _get(key):  # returns (value, rel_tol, provenance)
        e = store[key]
        return e["value"], e["rel_tol"], e["provenance"]
    return _get
```

Guardrail policy:
- **Gaussian CGS is the repo convention**; every field/force formula test must state its expected c-power via `assert_dimensions` (kills the D-16 c-factor clash class: EMU-flavored `G=2πn/R` vs Gaussian `2πnIa²/(c r³)` differ by 3×10¹⁰).
- SI values may appear only with explicit conversion through `core/units/dimensions.py`, never as bare literals.
- No literal `2.99792458e10` / `980.665` outside `config/constants.py` + data files (meta-test §5.5).

### 2.5 Tolerance policy (per computation class)

| Class | rel tol | Use | Examples |
|---|---|---|---|
| `TIGHT` | 1e-10 | pure math identities, closed-form algebra | elliptic K/E identities, Legendre orthogonality, GMD self-factor e^{−1/4}=0.7788007831 |
| `STANDARD` | 1e-8 | analytic physics formulas at exact points | on-axis coil field, dipole 2/−1 ratios, v=c/√(εμ) |
| `NUMERIC` | 1e-6 | quadrature/series/FD derivatives | off-axis fields vs scipy, B=∇×A finite differences, Landen vs scipy |
| `EMPIRICAL` | 1e-2 – 5e-2 | historical anchors & lab data | v ≈ 3.107e10 cm/s (±5% historical), Verdet table entries, optical n/K data |

Tolerances are **never chosen by the test author to make a test pass**; each lives in `reference_values.json` next to its value and provenance (Decision D-05):

```json
{
  "art768_weber_kohlrausch_v": {"value": 3.107e10, "rel_tol": 0.05, "unit": "cm/s",
    "provenance": "Weber-Kohlrausch 1856 / Treatise Art. 769-770"},
  "art691_gmd_self_circle": {"value": 0.7788007830714049, "rel_tol": 1e-12,
    "provenance": "GMD of circle about itself = a*exp(-1/4), Art. 691"},
  "art696_K_m_half": {"value": 1.8540746773013719, "rel_tol": 1e-12,
    "provenance": "scipy.special.ellipk(0.5), cross-checked Art. 696-701 tables"},
  "art801_tau_copper_1cm": {"value": 7.4804e-3, "rel_tol": 1e-3, "unit": "s",
    "provenance": "tau=4*pi*sigma*L^2/c^2, sigma_Cu=5.35e17 s^-1 (CGS), Art. 801-802"}
}
```

### 2.6 Parametrization conventions

- Geometry sweeps: `@pytest.mark.parametrize("k_sq", [0.0, 0.5, 0.9, 0.99, 0.9999], ids=...)` with `pytest.param(..., marks=pytest.mark.article(696))` per item when articles differ.
- Limit cases always paired with the finite case (k→0 AND k→1; far-field AND near-axis) so a truncated series cannot pass both.
- Data-anchored tests (Verdet, optical media) parametrize over the data rows from `reference_values.json`, so adding a medium is data, not code.
- Fixed seeds for any randomized property test (`np.random.default_rng(1234)`); SymPy-marked tests carry `@pytest.mark.sympy` and a timeout fixture.

---

## 3. Per-article test matrix plan

Test categories per tier promotion:

- **T2 → T3 (mandatory per article):** ≥1 golden value OR analytic limit case; dimensional-analysis check (`assert_dimensions`) for every formula family; ≥1 conservation/identity check where the article's physics admits one; all values sourced from `reference_values.json` with provenance.
- **T3 → T4 (spine 670-706, 752-780, 781-795; ≥60 articles):** SymPy identity registered per the Art. 787 exemplar (`VerificationResult(..., article_refs=(N,))`), **symbolically independent** of the implementation (built from Maxwell's equations / textbook canonical form, never by re-deriving the code's own expression); independent reimplementation cross-check where a second route exists; page_verifier verdict `yes` (or annotated `n/a`) linked in the ledger; triple signature (MATHEMATICA+QUALITAS+ARCHITECTUS).

### 3.1 Cluster A — Arts 667-706 (math spine; T4-mandatory core)

| Articles | Physics | Primary validation technique | Golden/limit anchors |
|---|---|---|---|
| 667-674 | current sheets, boundary conditions | identity checks on constructed fields | tangential-H jump = 4πK/c; normal-B continuity = 0 |
| 670-679 | circular coils on/off axis | golden values + asymptotic limits | on-axis exact `2πnIa²/(c(a²+z²)^{3/2})`; far-field dipole ∝z⁻³; **off-axis vs scipy at k²∈{0.5,0.9,0.99,0.9999}** (D-14) |
| 675-683 | solenoids, cylinders | limit cases | long-solenoid interior 4πnI/c (c-explicit!); end-field = half at mouth |
| 685-695 | spherical harmonics for circular currents | orthogonality + explicit polynomials | ∫P_lP_m=2δ/(2l+1); P₂=(3x²−1)/2; zonal values |
| 691-693 | GMD | golden values (tabulated) | self-GMD of circle a·e^{−1/4}=0.77880a; two-circle tabulated cases |
| 696-705 | elliptic integrals, Landen | golden values + singular limits | K(0.5)=1.85407468, K(0.99)=3.69563736, K(0.9999)=5.99158934, **K(−1)=1.31102878** (D-29); K→log-divergence as m→1 kills 4-term series |
| 697-699 | coil forces | reciprocity + energy identity | F_ij=F_ji; F=I₁I₂ dM/dz vs direct force |
| 702 | circular-current field lines | near-axis asymptotic + curl cross-check | ψ ∝ ρ² (slope fit 2±0.05); B=∇×A vs `calc_coil_off_axis` ≤1e-5 (D-02) |
| 706 | coil design | stationarity golden | Helmholtz condition d²B/dz²=0 at separation=a |

### 3.2 Cluster B — Arts 707-751 (instruments; priority 1)

| Articles | Technique | Anchors |
|---|---|---|
| 707-715 galvanometers | dimensional analysis + cross-module consistency | G includes correct c-power; **c-consistency test vs `circular_coils` precedes all of Bundle B** (D-16); torsion torque balance solved implicitly (D-15) |
| 713 Helmholtz | golden uniformity condition | d²B/dz²=0 at center; ≤1e-4 variation over \|z\|<a/10 |
| 716-719 sensitivity optimization | stationarity under constraint | dG/dx=0 at optimum; second-order flatness |
| 721-729 suspended coil, dynamometers | torque identities, small-angle limits | restoring-torque equilibrium; linear limit θ→0 |
| 730-735, 736-750 observations & extended instruments | first-principles recomputation after WP-3.2/3.4 | null-method identities (bridge balance ⇒ ratio equality); error-budget closure |
| 740/745/750 | **quarantined** pending D-06 | no new tests until adjudication; existing tests marked, not counted |
| 751-754 current weigher | independent dM/dx oracle (elliptic M) | F = I²·dM/dx in EMU, no stray c² (D-05) |

### 3.3 Cluster C — Arts 752-767 (coil comparison, resistance unit)

| Articles | Technique | Anchors |
|---|---|---|
| 752-757 | null/identity methods | differential galvanometer null ⇒ M₁=M₂; charge-balance identities |
| 758-764 | **cross-method independence** (anti-circular, D-10) | recoil/Lenz/rotating-coil/energy each computed from *independently sourced* M, T, EMF, I; perturbation oracle §5.1; dimensional check [R]=L/T (velocity dimensions!) |
| 765-767 | dimensional summary | R↔v linkage identities; velocity_check computed via `cgs_unit_of`, never literal True |

### 3.4 Cluster D — Arts 768-780 (ratio-V; priority 2)

| Articles | Technique | Anchors |
|---|---|---|
| 768-770 | symbolic dimensional derivation (SymPy) | [q_ESU]/[q_EMU] = L·T⁻¹ derived, not returned (D-19) |
| 771-773 | existing dimensions tests + round-trips | `calc_unit_ratio` = c; `convert_esu_to_emu` round trip |
| 774-779 the four methods | per-method internal consistency + shared anchor | intermittent current, condenser wippe (v=1/√(RC)-family), LC resonance, coil+condenser period; each returns v within method tolerance |
| 777 rapid-action correction | regression D-03 | correction MULTIPLIES by charge_fraction (0.5 ⇒ halve) |
| all of Ch XIX | **the v-anchor** | v = 3.107e10 cm/s ± 5% historical (Weber-Kohlrausch), `art768_weber_kohlrausch_v` in reference store |

### 3.5 Cluster E — Arts 781-805 (EM theory of light)

| Articles | Technique | Anchors |
|---|---|---|
| 781-795 waves module (untested today) | wave-identity suite | dispersion ω=ck/√(εμ); v=c/√(εμ) (ε=μ=1 ⇒ c); B₀=E₀/v; transversality k·E=k·B=0; SymPy wave-equation family extends the 787 exemplar |
| 786-792 optics velocity/constants/plane waves | golden identities | Poynting S=(c/4π)E×B; Stokes completeness S₀²=S₁²+S₂²+S₃²; Jones unitarity |
| 793-795 polarization (functions untested) | golden matrices | linear/circular decomposition; wave-plate phase retardation |
| 796-800 metals (functions untested) | limits | Hagen-Rubens reflectance limit; skin-depth scaling δ∝1/√(ωσ) |
| 801-803 diffusion | regime test after D-01 fix | τ=4πσL²/c²; copper slab 1 cm ⇒ 7.48 ms; round-trip length(time) = L |
| 804-805 crystals/radiation pressure | golden values | optic-axis directions from index ellipsoid; p=I/c and 2I/c |

### 3.6 Cluster F — Arts 806-831 (magneto-optics & vortex; priority 3)

| Articles | Technique | Anchors |
|---|---|---|
| 806-809 | Faraday rotation with **Verdet data anchoring** | θ=VBL; single canonical Verdet unit (D-32); historical heavy-glass V entries with provenance in reference store |
| 810-817 velocity-split kinematics | closed-loop identities | rotation_per_length from `perform_kinematic_analysis` = V·B; Δn = VBλ/π **no factor 2** (D-04); v_L/R split consistent with n±Δn |
| 818-819 medium energy | label-semantics test (D-21) | pure-E configuration reports electric term in electric slot |
| 820 | computed non-reciprocity discriminant (D-06) | round trip: Faraday 2θ vs reciprocal 0; no literal True |
| 821, 831 | derived-not-prose (D-07/D-08) | each "result" numerically derived from sibling computations |
| 822-831 vortex engine | calibrated lattice case | lattice wave speed vs c claim (note_4); gear-ratio identities; dimensional sanity of every energy (D-22); Art. 829 single consistent formula pinned dimensionally (D-13) |

### 3.7 Cluster G — Arts 832-866 (molecular currents, action at distance)

| Articles | Technique | Anchors |
|---|---|---|
| 832-837 Ampère theory | golden dipole ratios (existing pattern is the model) | axis B=2m/r³, equator B=−m/r³; bound-current identity J_b=c∇×M |
| 838-840 | computed consequences | article-specific numeric results from the Ampère core |
| 841-845 Weber | coefficient pin + steady-current limit | after D-12 adjudication: ṙ²-term coefficient pinned (a=0 case, rel 1e-12); Weber→Ampère recovery for steady currents |
| 846-847 | force/EMF identities | current-element force symmetry; induced_emf = −dΦ/dt |
| 851-855 Neumann | **reciprocity + independent reimplementation** (prime T4 material) | M₁₂=M₂₁; Neumann double integral vs elliptic closed form for coaxial circles (two independent code paths); EMF=−dM/dt·I |
| 856-858 | computed consequences | article-specific results from Neumann core |
| 859-866 comparisons & medium check | computed residuals (D-09) + optical data (D-11) | Weber residual vs Ampère on defined test configurations (metric defined in reference store); n=√(εμ) with water n=1.33/K=1.77; verdict = computed `all_agree` |

---

## 4. Regression test specs — 5 S1 + top-10 S2 (Stage 3 §7.1 order)

Location: `tests/articles/regressions/`. All carry `@pytest.mark.article(N)` and `@pytest.mark.regression(defect="D-xx")`. Authored W5 as `xfail(strict=True)` so they flip green only when the WS3 fix lands (failing-before/passing-after evidence at G2).

### 4.1 S1 defects

**R1 — D-03 (Art. 777) — rapid-action correction inverted.** Target `experiments/ratio_v/combined.py::apply_rapid_action_correction`. File `test_defects_s1.py`:

```python
@pytest.mark.article(777)
@pytest.mark.regression(defect="D-03")
def test_regression_D03_art777_correction_halves_v():
    from maxwell.experiments.ratio_v.combined import apply_rapid_action_correction
    # engineer charge_fraction = 0.5 exactly: 1 - exp(-t_half/RC) = 0.5
    import numpy as np, math
    f, RC = 1.0, 1.0 / (2.0 * math.log(2.0))     # t_half/RC = ln 2
    corrected = apply_rapid_action_correction(1.0, f, RC)
    assert corrected == pytest.approx(0.5, rel=1e-12)   # CURRENTLY returns 2.0

@pytest.mark.article(777)
def test_regression_D03_art777_correction_never_amplifies():
    # property: under-charging always makes measured v too LARGE;
    # the correction must shrink it for any charge_fraction < 1
    for f, RC in [(1.0, 0.1), (10.0, 0.5), (0.5, 2.0)]:
        assert apply_rapid_action_correction(1.0, f, RC) < 1.0
```

**R2 — D-04 (Art. 812) — Δn factor-of-2.** Target `magneto_optics/circular_polarization.py::calc_circular_velocity_split`:

```python
@pytest.mark.article(812)
@pytest.mark.regression(defect="D-04")
def test_regression_D04_art812_delta_n_identity(ref_value, cgs_constants):
    from maxwell.magneto_optics.circular_polarization import (
        calc_circular_velocity_split, perform_kinematic_analysis)
    V, B, lam, n = 0.1, 1000.0, 5.893e-5, 1.5      # min/(G cm) → rad consistent
    # theta = (k_L - k_R) L / 2 = V B L  =>  dn = V B lam / pi  (NO factor 2)
    expected_dn = V * B * lam / math.pi
    dv = calc_circular_velocity_split(n, B, V, lam)
    expected_dv = cgs_constants["c"] * expected_dn / n**2
    assert dv == pytest.approx(expected_dv, rel=1e-12)   # CURRENTLY 2x off
    # closed loop: kinematic rotation per length must equal V*B
    ka = perform_kinematic_analysis(1.0, k_right=2.0e5*0.999, k_left=2.0e5*1.001)
    assert ka["rotation_per_length"] == pytest.approx((2.0e5*1.001-2.0e5*0.999)/2, rel=1e-12)
```

**R3 — D-01 (Arts 801-803) — diffusion τ missing 4π/c².** Target `optics/diffusion.py::calc_diffusion_time/calc_diffusion_length`:

```python
@pytest.mark.article(801)
@pytest.mark.regression(defect="D-01")
def test_regression_D01_art801_copper_slab_golden(ref_value):
    from maxwell.optics.diffusion import calc_diffusion_time
    tau_expected, tol, prov = ref_value("art801_tau_copper_1cm")   # 7.48e-3 s
    sigma_cu = 5.35e17                                               # s^-1 CGS
    assert calc_diffusion_time(1.0, sigma_cu) == pytest.approx(tau_expected, rel=1e-3)
    # CURRENTLY returns sigma*L^2 ~ 5.35e17  (a diffusivity, not a time)

@pytest.mark.article(802)
def test_regression_D01_art802_roundtrip_length():
    from maxwell.optics.diffusion import calc_diffusion_time, calc_diffusion_length
    L, sigma = 2.5, 1.0e16
    assert calc_diffusion_length(calc_diffusion_time(L, sigma), sigma) == pytest.approx(L, rel=1e-9)

@pytest.mark.article(801)
def test_regression_D01_art801_c_squared_scaling(cgs_constants):
    # tau = 4 pi sigma L^2 / c^2: check the c^-2 dependence by ratio at fixed sigma,L
    # (guards against re-introducing the diffusivity form)
    ...
```

**R4 — D-02 (Art. 702) — A_φ prefactor / near-axis asymptotic.** Target `electromagnetism/vis/circular_fields.py::_vector_potential_azimuthal`:

```python
@pytest.mark.article(702)
@pytest.mark.regression(defect="D-02")
def test_regression_D02_art702_near_axis_psi_rho_squared():
    from maxwell.electromagnetism.vis.circular_fields import _vector_potential_azimuthal
    a = 10.0
    rhos = np.array([1e-4, 3e-4, 1e-3, 3e-3, 1e-2]) * a
    psi = np.array([r * _vector_potential_azimuthal(1.0, a, r, 0.0) for r in rhos])
    slope = np.polyfit(np.log(rhos), np.log(psi), 1)[0]
    assert slope == pytest.approx(2.0, abs=0.05)     # CURRENTLY ~3.5

@pytest.mark.article(702)
def test_regression_D02_art702_curl_A_matches_B_field():
    # B = curl A by central differences vs calc_coil_off_axis at (rho,z)=(0.5a, 0.25a)
    # rel err <= 1e-5 in both components                     # CURRENTLY fails
```

**R5 — D-05 (Arts 751-754) — current weigher fabricated geometry.** Target `electromagnetism/measurements/galvanometers_extended.py::current_weigher`:

```python
@pytest.mark.article(751)
@pytest.mark.regression(defect="D-05")
def test_regression_D05_art751_force_equals_I2_dMdx():
    from maxwell.electromagnetism.measurements.galvanometers_extended import current_weigher
    # independent oracle: dM/dx from elliptic-integral mutual inductance of
    # two coaxial loops (maxwell.math.elliptic_integrals) by central difference
    a, d, I = 10.0, 1.0, 0.1          # cm, cm, abamperes
    dMdx = elliptic_mutual_gradient_oracle(a, a, d)          # NEW fixture, EMU
    res = current_weigher(I, a, 1, 1, d)
    assert res["force"] == pytest.approx(I * I * dMdx, rel=2e-3)  # EMU: no c^2
    assert res["equivalent_mass"] == pytest.approx(res["force"] / CONST.G_STANDARD, rel=1e-12)
    # CURRENTLY: invented r^2/(d^2+r^2) near-field factor + mixed SI/c^2/EMU
```

### 4.2 Top-10 S2 (Stage 3 §7.1 priority 5-10 + theater closures)

| # | Defect | Test (name, target) | Assertion logic |
|---|---|---|---|
| S2-1 | **D-16** c-convention clash | `test_c_convention_coil_center_field_consistency` (`components/circular_coils.py` vs `instruments/galvanometers.py`) | compute the *same physical* center field both ways; assert equality rel 1e-9 **before any Bundle B test is written** |
| S2-2 | **D-33** hardcoded constants | meta-test `test_meta_no_hardcoded_c` | AST scan of `maxwell/`: forbid `2.99792458e10`/`3.0e10`-family and `980.665` literals outside `config/constants.py` (+data) |
| S2-3 | **D-14/D-29** truncated elliptic series | `test_off_axis_field_vs_scipy_k2_sweep` | off-axis B vs scipy-based reference at k²∈{0.5,0.9,0.99,0.9999} rel ≤1e-8; `K(m=-1)==1.3110287771` (corrected golden) kills the m<0 clamp |
| S2-4 | **D-12** Weber coefficient | `test_weber_force_coefficient_pin` | `weber_force` with a=0, ṙ≠0: F/F_coulomb == 1 − ṙ²/c² (coefficient pinned per adjudicated convention) rel 1e-12 |
| S2-5 | **D-11** rigged water row | `test_maxwell_relation_optical_water` | `verify_maxwell_relation` with water n=1.33, K=1.77 must return `passed == (max_rel_error < tol)` computed from data; rigged 9.0 row must fail the dataset sanity check |
| S2-6 | **D-21** swapped energy labels | `test_energy_labels_semantics` | pure-E input configuration ⇒ energy reported in the electric/potential slot (and vice versa) |
| S2-7 | **D-06** Art. 820 `return True` | `test_art820_rotation_discriminant_computed` | result equals 2θ for Faraday round trip, 0 for reciprocal; output varies with input θ; AST guard: function body is not a bare `return True` |
| S2-8 | **D-10** circular resistance check | `test_verify_absolute_resistance_independence` | perturbation oracle §5.1: perturb R_lenz's independent inputs by +1% ⇒ R_energy must not move by ~1% (a circular check propagates 1:1) |
| S2-9 | **D-09** invented agreement scores | `test_agreement_metrics_sensitive_to_inputs` | computed metric values change when underlying force residuals change; AST: no bare numeric Constant under `*agreement*/*score*/*confidence*` keys |
| S2-10 | **D-13** Art. 829 three formulas | `test_art829_single_formula_dimensional_pin` | result is dimensionless angle; docstring formula string == coded expression (REQ-M textual check); golden calibrated-lattice value |

---

## 5. Anti-theater test patterns (meta-tests that audit the verifiers)

Location: `tests/articles/meta/`. These are the runtime twins of the Stage 3 §5.3 static lint (WP-1.4); both layers run in CI.

### 5.1 Circularity detection — the perturbation oracle

```python
def assert_cross_check_independent(verify_fn, method_a_inputs, method_b_inputs, perturb=0.01):
    """A genuine cross-check uses INDEPENDENT inputs. If perturbing A's inputs
    moves B's output by the same fraction, B is computed FROM A (D-10 class)."""
    base = verify_fn(**method_a_inputs, **method_b_inputs)
    bumped = {**method_a_inputs}
    k = next(iter(method_a_inputs))
    bumped[k] = method_a_inputs[k] * (1.0 + perturb)
    after = verify_fn(**bumped, **method_b_inputs)
    propagation = abs(after["cross_value"] - base["cross_value"]) / (perturb * abs(base["cross_value"]) + 1e-300)
    assert propagation < 0.1, "cross-check propagates method-A perturbations 1:1 => circular"
```

Applied to every `verify_*` that claims a cross-method check (registry built from `get_all_citations` + naming convention). Static twin (AST): within one function body, a name computed by call A may not flow into call B whose result is compared to A's (Stage 3 rule 4 heuristic), and every `verify_*` must consume ≥1 reference input sourced from `reference_values.json` or an explicit independent parameter.

### 5.2 Hardcoded-verdict detection

AST scan of all decorated `verify_*/prove_*/check_*` functions: the returned `passed`/`verified`/`agrees`/`ok` values must be **expressions**, never `Constant(True/False)` or dict literals containing them (Stage 3 rules 1-2). Runtime twin: each such function must be callable with a seeded *known-bad* dataset (from `tests/articles/meta/bad_datasets.json`) that flips the verdict; a verifier that passes the bad dataset is theater.

### 5.3 Agreement-score provenance

Any dict key matching `*agreement*|*score*|*confidence*` must have a value that is (a) an expression involving function inputs/calls, or (b) loaded from `reference_values.json` with a provenance field (D-09). Bare numeric literals in those positions fail the meta-test.

### 5.4 Test-theater detection (rubric enforcer)

§2.3's AST check over every `pytest.mark.article` test: ≥1 numeric assert with tolerance (approx/isclose/assert_cgs_close/assert_vectors_close/ref_value comparison). Membership/`isinstance`/key-presence/bare-bool-only bodies fail. This is the mechanical implementation of the REQ-T rubric and the countermeasure to R5/D-36.

### 5.5 Constant hygiene & god-decorator guards

- No c/g literals outside `config/constants.py` (§4.2 S2-2).
- `@maxwell_cite` with ≥5 articles requires `range_justification=` (lint rule 6, runtime mirror), and each article in such a decorator must still show ≥1 article-specific computation in the ledger cross-check.
- Chapter-string lint: every decorator `chapter=` must be in the corrected PARTS title set (rule 8); out-of-range citations (<667) in last-200 work require parking-lot annotation (rule 9).

### 5.6 Mutation demonstration at G3

At the gate, QUALITAS demonstrates: (i) delete one marked test ⇒ `article_evidence_report.json` flips the article to missing and `test_article_coverage.py` goes red; (ii) replace a numeric assert with a key-presence assert ⇒ rubric enforcer goes red. Evidence attached to the G3 pack.

---

## 6. Test-hostile refactoring brief (seams before tests can bite)

From Stage 3 §7.2; **implementation is WS3's job** — this section defines the minimal test-side acceptance criteria.

| Module | Problem | Minimal refactor | Test-side acceptance |
|---|---|---|---|
| `measurements/galvanometers_extended.py` (1076 lines, 19 arts) | monolith; giant fixtures; 19 articles inseparable | split per instrument class (`tangent/sine/helmholtz/wattmeter/electrodynamometer/current_weigher/joule_balance`) before WP-3.4; re-export shims in `__init__` keep existing tests green | existing 54 tests stay green; each sub-module importable alone; D-05 fix isolated to `current_weigher` |
| `molecular/competing_theories.py` (26 citations) | dict-only APIs give tests nothing numeric | compute-or-delete per D-04/D-09 (WP-3.5); tests bind **only to the new computed-metric API** | S2-9 sensitivity test green; no smoke test counts toward T3 |
| `vortex_engine/*` | no physical anchor values | one calibrated lattice case (wave-speed=c claim, D-08 note_4) as a fixture constant set | Bundle F's first test is the calibrated-case golden before any parametric test |
| `optics/diffusion.py` | mixed-chapter content (Ch XX + misplaced 806-808 citations) | re-decorate 806-808 out (D-23) **before** tests are written | decorator AST audit shows 0 absorption-code citations of 806-808 |
| `signal_processing/telegraphy.py` 740/745/750 | anachronistic heuristics enshrined by tests | quarantine marks; adjudicate at G1 (D-06) | no new test may cite 740/745/750 until adjudication recorded in decision log |
| inline imports (existing 4 Part-IV files) | import errors surface at run time, not collection | leave existing files; **new bundles use module-level imports** | collect-only gate catches broken imports pre-run |
| verdict schema drift (`verified` vs `uniform` vs `agrees`, two return shapes) | tests can't assert a stable contract | standardize `{"value","expected","rel_error","passed"}` (Stage 3 §4.2) | new tests assert only against the standard schema; `passed` always computed |

---

## 7. CI integration

### 7.1 Job layout (single command reproduces gate evidence; feeds WP-5.2)

```
ci-quality (PR + nightly):
  env: pinned venv (requirements lock), PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
  step 0  canary:      python -c "import numpy; numpy.linalg.eigvalsh(...)"  # BLAS sanity
  step 1  static:      anti-theater lint (WP-1.4) + decorator chapter lint + constant-hygiene AST
  step 2  collect:     pytest tests/ --collect-only -q     # import-time failures fail fast
  step 3  core:        pytest tests/ -m "not slow and not sympy and not visualization and not jax" -q
  step 4  shards:      -m sympy | -m visualization | -m jax   (parallel jobs; nightly for jax)
  step 5  evidence:    pytest tests/articles/ --article-report   # emits article_evidence_report.json
  step 6  consistency: check_coverage.py --depth + COVERAGE_SUMMARY.md byte-consistency
  artifacts: article_evidence_report.json, ledger diff, lint logs, runtime summary
```

`run_quality_checks.sh` gains steps 1/5/6 (WS5 WP-5.2 wiring).

### 7.2 Runtime budget (< 5 min, measured)

Measured baseline: **1,947 tests in 103.5 s** single-process on the dev box. Budget model: +~420 new tests at ≤150 ms average (article tests are closed-form) + 60 SymPy verifiers capped at 2 s each (`@pytest.mark.sympy`, timeout fixture, result caching) ⇒ **≤4 min worst case**, typically <3 min. `-n auto` (pytest-xdist) is optional insurance, not a requirement; vis tests (`matplotlib` import cost) run in their own shard. Anything exceeding 1 s per test gets `@pytest.mark.slow` and moves to nightly.

### 7.3 Gates in CI terms

| Gate | CI condition |
|---|---|
| per-PR | steps 0-3 green; no new lint violation; no `article` marker removed without decision-log entry |
| G2 exit | all S1 regression tests flipped green (xfail→pass diff visible); theater remediation diffs green under steps 1+5 |
| G3 exit | `article_evidence_report.json` shows 200/200, rubric enforcer green, mutation demonstration recorded, suite ≈2,300+ green, runtime ≤5 min, zero flaky (§7.4) |
| G4 exit | steps 1-6 all green; SymPy spine ≥60 verifiers green; ledger frozen; certification evidence pack complete |

### 7.4 Flake policy

- **Environment-caused instability is infra, not flake**: the pytest-randomly/thinc incident (§0) mandates the pinned venv + autoload disable; a rerun-green test that failed due to external plugins is an infra ticket, never a test edit.
- Deterministic seeds everywhere (`np.random.default_rng(fixed)`); time-dependent tests forbidden.
- A test red→green across two identical reruns in the pinned env ⇒ quarantine mark + defect ticket + EXAMINATOR triage within 1 cycle; quarantined tests excluded from gate counts, burned down before G3 (Stage 2 R12).
- SymPy timeouts are budget failures: raise the per-verifier cap only with QUALITAS sign-off.

### 7.5 G3 evidence report format (emitted by the §2.2 plugin)

```json
{
  "range": [667, 866],
  "generated": "2026-10-16T..",
  "articles_covered": 200, "articles_missing": [],
  "gate_G3": "PASS",
  "suite": {"total": 2312, "passed": 2312, "runtime_s": 187,
            "article_marked": 214, "regression": {"s1_closed": 5, "s2_closed": 10}},
  "rubric": {"violations": 0},
  "evidence": {"667": ["tests/articles/test_part_iv_current_sheets.py::test_art_667_..."], "...": "..."},
  "defect_links": {"D-01": ["...test_regression_D01_art801_copper_slab_golden (passed)"], "...": "..."},
  "quarantine": {"740": "D-06 open", "745": "D-06 open", "750": "D-06 open"}
}
```

The INDEPENDENT GATE REVIEWER audits this artifact against the ledger (Stage 2 §8): every article's listed nodeids must exist, pass, and satisfy the rubric; any mismatch is a gate failure.

---

## 8. Effort estimate & sequencing (WS4-TEST, aligned to Stage 2)

### 8.1 Estimate (agent-hours)

Stage 2 WS4 baseline: WP-4.1 framework 12 + bundles 26/32/12/10/18/20/24 = **154 ah**. Stage 4 deltas:

| Delta | Scope | ah |
|---|---|---|
| D1 | S1+S2 regression suite (15 specs, failing-first authoring, perturbation fixtures, elliptic-oracle fixture) | +10 |
| D2 | Meta-test suite (coverage meta-test, rubric enforcer, circularity oracle, verdict checks, constant/god-decorator guards, bad-dataset seeds) | +8 |
| D3 | Article-coverage plugin + G3 evidence generator + CI wiring support (→ WP-5.2) | +8 |
| D4 | `scripts/article_coverage_audit.py` committed baseline + per-gate re-audit | +4 |
| D5 | Test-side acceptance of §6 refactors (split review, re-decoration audit, quarantine marks) | +4 |
| **Total WS4-TEST** | | **≈188 ah** |

+34 ah over Stage 2's 154, drawn from the 95 ah contingency reserve; program ceiling 720 ah intact. Productivity anchors: measured 242 tests execute in ~1 s; bundle throughput target 3-5 qualifying article-tests/ah including reference-value provenance; stub-heavy clusters (F, B) run slower, math spine faster.

### 8.2 Sequencing against WS3-IMPLEMENT

| Week | WS4 activity | Hard dependencies |
|---|---|---|
| W5 (P2 mid) | WP-4.1 framework + audit script; **S2-1 (D-16 c-consistency) written and run against current tree (expected RED — gates Bundle B entry)**; S1 regressions R1-R5 + S2-2..S2-10 authored `xfail(strict=True)` | none (starts alongside P2) |
| W6 (post-G2) | Bundle B (45 arts, prio 1); regression flips D-03/D-04/D-05 verified as WP-3.2/3.3/3.4 fixes land | WP-3.2 complete; D-16 test green |
| W7 | Bundle D (13, prio 2) + Bundle F (26, prio 3) + Bundles A/C/E/G in parallel; early spine SymPy verifiers (WP-5.1a) for stable 696-705/786-805 | WP-3.1/3.3/3.5/3.6 outputs per bundle |
| W8 | Closeout: meta-tests green, mutation demonstration, runtime verification, flake triage (EXAMINATOR), G3 evidence pack | all bundles complete; quarantine list adjudicated (D-06) |

Dependency edges: WP-3.4→Bundle C; WP-3.5→Bundle G; WP-3.6→Bundle A + R4/S2-3 regressions; G1 D-06 adjudication → unquarantine 740/745/750; **no instrument test may merge before S2-1 is green** (wrong convention must not be enshrined — Stage 3 §7.1 item 5).

---

## 9. Handoff to Stage 5 (agent orchestration)

### 9.1 Local agent ownership of test bundles

| Agent | Owns | Rationale |
|---|---|---|
| **qualitas** | WP-4.1 framework (marker/plugin/meta-tests/rubric), the perturbation oracle, G3 evidence pack, tier-promotion certification (never the implementer) | QA charter + theory-preservation constraint; separation of duties |
| **mathematica** | Bundle A (667-706) + Bundle E waves/optics identities; SymPy spine verifiers (WP-5.1); elliptic-oracle fixture for R5 | core math charter; owns `math/elliptic_integrals.py` exemplar |
| **instrumentum** | Bundle B (707-751) + Bundle C (752-767); D-16 c-consistency test; instrument error-budget fixtures | metrology charter; error budgets |
| **circuitus** | Bundle D (768-780) incl. the v=3.107e10 anchor; Bridge/null-method identities in Bundle C support | network/bridge charter; measurement uncertainty |
| **materia** | Bundle F (806-831); Verdet/material data entries in `reference_values.json` with provenance | materials-data charter; only agent that may add lab-data anchors |
| **physicus** | Bundle G (832-866); formula-sheet oracle linkage (every REQ-V value traces to the WP-2.4 sheet); Category B veto on vortex-engine tests | primary-physics charter; theory preservation |
| **architectus** | ledger/traceability co-signature for T4; PARTS/decorator-lint ownership; §1.6 audit script maintenance | mapping authority |
| **scriba** | G3/G4 report artifacts, COVERAGE_SUMMARY regeneration byte-consistency | records charter |

### 9.2 External testing support that remains

1. **EXAMINATOR** (test-automation specialist, Stage 2 §3.2): W6-W8 throughput under QUALITAS — parametrize hygiene, flake triage, runtime budgeting, xdist shard tuning.
2. **INDEPENDENT GATE REVIEWER**: audits `article_evidence_report.json` vs ledger at G3/G4; must never be an agent instance that authored a bundle under review.
3. **HUMAN VERIFIER**: page_verifier verdict linkage for T4 promotions (Vol II campaign is WS2, but T4 evidence consumption happens here); final acceptance at G4.

### 9.3 What Stage 5 receives

- This strategy (binding for all test work): marker scheme §2, matrix §3, regression specs §4, anti-theater rules §5, refactor acceptance §6, CI contract §7.
- Measured baseline artifacts: §0/§1 numbers; `artcov`-class audit becomes `scripts/article_coverage_audit.py` at WP-4.1.
- Open items for orchestration: quarantine lifecycle for 740/745/750; EXAMINATOR engagement window; contingency drawdown reporting (+34 ah consumed at W5 start).

---

## Appendix A — Self-critique & measurement uncertainty

1. **Upper-bound caveat:** the SUBSTANTIVE count (71) uses attribute-name matching for method calls; a same-named attribute on an unrelated object could false-positive (relevant to 834-837, 735, 764). Clean candidates are therefore stated as ≈58, consistent with Stage 1's ~50 T3 within the rubric's ±uncertainty. WP-4.1's committed audit tool re-derives everything at each gate, so no gate decision rests on a heuristic count.
2. **Two zero-coverage figures are both true and serve different purposes:** 100 articles have zero function-level contact; 137 lack a *qualifying* numeric test (adds 28 meta-only, 1 vis-only, 8 smoke-only). G3 targets the 137.
3. **Regression specs pin behavior against current signatures** (verified today); WS3 may rename functions — specs express input/output identities and must be reconciled at implementation, not weakened.
4. **Golden values were verified live** with scipy (K-set, copper τ, e^{−1/4}); one upstream value corrected (K(−1)=1.31103, not 2.06).
5. **"Suite green" is environment-relative** (§0): all claims here hold under `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` in the pinned venv; CI enforces this, and the BLAS canary catches regressions of the crash mode.
6. **Runtime extrapolation** (103.5 s → <5 min at 2,300+ tests) assumes new tests stay closed-form; SymPy growth and vis imports are the monitored risks (§7.2).

*Stage 4 deliverable complete. Handoff to Stage 5: §3 matrix, §4 regression specs, §7 CI contract, §9 ownership map.*

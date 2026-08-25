# D-24 Adjudication — False Treatise Attribution of Signal-Integrity Heuristics

- Date: 2026-08-21
- Adjudicator: INSTRUMENTUM (Wave 6, measurement-instruments scope)
- Stage/Severity: Stage-3, S2
- Governing decision: Program Decision D-06 (re-decorate or reclassify; no deletion of working math)
- Companion defect resolved in the same pass: D-17 (joule_balance anachronism), S2

## 1. Defect statement

`maxwell/signal_processing/telegraphy.py` (former lines 285-371) attributed three
modern signal-integrity heuristics via `@maxwell_cite` to Treatise Arts. 740, 745
and 750 under a fabricated chapter string `"Signal Transmission"`:

| method | heuristic | false citation |
|---|---|---|
| `SignalTransmission.rise_time` | t_r = 2.2 R C ell^2 | Art. 740, chapter "Signal Transmission", maxwell_original |
| `SignalTransmission.bandwidth_limit` | BW = 0.35 / t_r | Art. 745, chapter "Signal Transmission", maxwell_original |
| `SignalTransmission.max_signaling_rate` | f_max = 1/(2 t_r) | Art. 750, chapter "Signal Transmission", maxwell_original |

The `rise_time` docstring also omitted the ell^2 dependence the code applies.

## 2. Evidence considered

1. **Chapter map** (`check_coverage.py` PARTS table): Part IV Ch XVI is
   "Observations", Arts. 730-751; Ch XVII is "Coil Comparison", Arts. 752-757.
   No chapter named "Signal Transmission" exists anywhere in the Treatise map.
2. **Provenance of the cited articles**
   (`page_verifier/data/last200_arts_provenance.json`): Arts. 740, 745, 750 are
   genuine, equation-dense articles of Ch XVI (3rd-edition Vol. II pp. 407, 411,
   415-416) within the observations/measurement cluster. None states the
   20th-century rules t_r = 2.2 RC, BW = 0.35/t_r or f_max = 1/(2 t_r).
3. **Anachronism**: 2.2 = ln 9 is the 10-90 % step factor of a first-order RC
   section; 0.35 = ln 9/(2 pi) is the single-pole rise-time/bandwidth product;
   1/(2 t_r) is a Nyquist-style ISI thumb rule. All are mid-20th-century
   signal-integrity results, post-dating the 1873 Treatise.
4. Maxwell's genuine cable-diffusion work (the ell^2 dependence) belongs to the
   electrokinematics of Part II, not to Arts. 740-750.

## 3. Decision

Reclassify all three methods `theory_class="standard_math"` with **no article
numbers** (per D-06 option 2). The fabricated chapter string is removed
(`chapter=""`). No arithmetic was changed; the heuristics remain as honestly
labelled modern content. Arts. 740, 745 and 750 are now **residual Wave-7 gaps**
(their genuine Treatise content is unimplemented; fabricating it is forbidden).

## 4. Exact changes (D-24)

`maxwell/signal_processing/telegraphy.py`:
- `rise_time`, `bandwidth_limit`, `max_signaling_rate`: decorator changed to
  `@maxwell_cite(part=4, chapter="", theory_class="standard_math",
  description="Modern ... (post-Treatise)")`; D-24 comment block added above each.
- `rise_time` docstring now states `t_r = 2.2 * R * C * ell**2` and explains the
  distributed-RC origin of the ell^2 dependence.
- Module docstring and `TelegraphLine` scope corrected to Arts. 730-735;
  legitimate 730-735 citations re-chaptered `"Ch XVI: Observations"`;
  `SignalTransmission` and `analyze_telegraph_line` docstrings flag the
  standard_math keys.

`maxwell/signal_processing/__init__.py`:
- Package docstring and `__all__` comments corrected: Arts. 730-735 only;
  `SignalTransmission` labelled standard_math per D-24.

`tests/test_new_part_iv_signal_calibration.py` (re-pointed, not extended):
- `test_rise_time`, `test_bandwidth_limit`, `test_max_signaling_rate`: docstrings
  re-pointed to standard_math semantics; formulas unchanged.
- `test_signal_transmission_citation`: now asserts `part == 4`,
  `theory_class == "standard_math"`, `articles == ()`, no "Signal Transmission"
  chapter, and that 740/745/750 are absent from the citation.

## 5. Companion fix: D-17 (joule_balance)

`maxwell/electromagnetism/measurements/galvanometers_extended.py::joule_balance`
cited Arts. 755-757, but Ch XVII (752-757) is "Comparison of Coils" and the
Joule-balance instrument post-dates the 1873 Treatise; Q = I^2 R t is Joule's
1841 law. Re-mapped to `theory_class="standard_math"`, `chapter=""`, no article
numbers, with an anachronism note in the docstring and decorator comment.
`analyze_galvanometers` no longer lists 755/756/757 (now 736-754, with
range-justification comment). No Ch XVII coil-comparison code was faked.
`maxwell/electromagnetism/measurements/__init__.py` comments updated to match.

## 6. Incidental repair (self-found, in scope)

`HelmholtzGalvanometer.field_at_center` used the prefactor 8 pi/(5 sqrt(5)) —
short by a factor of 4 — and `helmholtz_factor`'s special case used
8/(5 sqrt(5)) = 0.7155, contradicting both the general-separation branch and
Biot-Savart quadrature. Repaired to 32 pi/(5 sqrt(5)) and 16/(5 sqrt(5))
(~1.4311) respectively; pinned by independent quadrature in
`tests/test_articles_ch16_observations_730_750.py` (Arts. 741-743) and
consistent with `maxwell.instruments.helmholtz.HelmholtzCoil`.

## 7. Verification

`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest
tests/test_articles_ch16_observations_730_750.py
tests/test_new_part_iv_signal_calibration.py tests/test_defects_s1.py -q`
-> 77 passed. Full suite `tests/` -> 2219 passed, 0 failed.
Anti-theater lint (R1-R6) on all touched files: 0 findings.
Article evidence map: 730-739, 741-744, 746-749 covered; 740, 745, 750 remain
documented gaps.

# Checklist: Instrument Noise Characterization

## Purpose

Validate noise performance characterization for precision instruments.

---

## Level 1: Noise Source Identification (Required)

### Thermal Noise Analysis
- [ ] Thermal noise voltage calculated: e_n = sqrt(4·k_B·T·R·Δf)
- [ ] Resistance value verified at operating temperature
- [ ] Bandwidth correctly specified (effective noise bandwidth)
- [ ] Temperature coefficient included for drift analysis

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Shot Noise Analysis
- [ ] Shot noise current calculated: i_n = sqrt(2·q·I·Δf)
- [ ] DC bias current documented
- [ ] Full formula used if bidirectional current (I_forward + I_reverse)
- [ ] Applicable devices identified (diodes, transistors, photodetectors)

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Flicker (1/f) Noise
- [ ] Corner frequency identified (f_c where flicker = white noise)
- [ ] Low-frequency behavior characterized
- [ ] 1/f coefficient (K_f) documented if applicable
- [ ] Integration time effects considered

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Vibration (Microphonic) Noise
- [ ] Microphonic sensitivity specified
- [ ] Vibration environment characterized
- [ ] Isolation requirements defined
- [ ] Cable/wiring microphonics considered

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

**Level 1 Total:** ___ / 16 points

---

## Level 2: Noise Calculation (Required)

### RMS Noise Calculation
- [ ] Total RMS noise computed in operating bandwidth
- [ ] Integration performed: e_n,total = sqrt(integral S(f) df)
- [ ] White noise approximation used correctly: e_n · sqrt(BW_n)
- [ ] Filter shape factor applied (pi/2 for single-pole lowpass)

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Noise Spectral Density
- [ ] PSD plot or table provided
- [ ] Frequency range covers operating bandwidth
- [ ] Noise types identified from slope
- [ ] Peak frequencies documented (if any)

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### CGS Unit Consistency
- [ ] Voltage noise in statvolt/sqrt(Hz)
- [ ] Current noise in statampere/sqrt(Hz)
- [ ] Boltzmann constant: k_B = 1.381×10^-16 erg/K
- [ ] Elementary charge: q = 4.803×10^-10 statC

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Room Temperature Reference
- [ ] T = 293 K (20°C) used for standard conditions
- [ ] k_B·T = 4.05×10^-14 erg documented
- [ ] Temperature variation effects included
- [ ] Thermal equilibrium assumed/verified

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

**Level 2 Total:** ___ / 16 points

---

## Level 3: Signal-to-Noise Analysis (Required)

### SNR Calculation
- [ ] Signal power/voltage documented
- [ ] Noise power/voltage calculated
- [ ] SNR computed: SNR = P_signal / P_noise
- [ ] SNR in dB: 20 · log10(V_signal / V_noise)

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Minimum Detectable Signal
- [ ] MDS = SNR_min × V_noise calculated
- [ ] SNR_min specified for application:
  - [ ] Detection: 1-3
  - [ ] Measurement: 10
  - [ ] Precision: 100
- [ ] MDS expressed in input units (current, voltage, field)
- [ ] Detection threshold clearly stated

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Integration Improvement
- [ ] Integration time specified
- [ ] Improvement factor calculated: sqrt(t)
- [ ] MDS(t) = MDS(1s) / sqrt(t) applied
- [ ] Practical integration limits discussed

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Noise Bandwidth Optimization
- [ ] Operating bandwidth justified
- [ ] Filter requirements specified
- [ ] Bandwidth vs. SNR tradeoff analyzed
- [ ] Optimal bandwidth identified

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

**Level 3 Total:** ___ / 16 points

---

## Level 4: Advanced Noise Analysis (Expert)

### Amplifier Noise Contribution
- [ ] Amplifier voltage noise (e_n,amp) included
- [ ] Amplifier current noise (i_n,amp) included
- [ ] Source resistance effect: (i_n,amp · R_s)^2
- [ ] Total input noise: e_n,total^2 = e_n,source^2 + e_n,amp^2 + (i_n,amp · R_s)^2

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Noise Figure Analysis
- [ ] Noise figure calculated: NF = SNR_in / SNR_out
- [ ] NF in dB: 10 · log10(NF)
- [ ] Noise factor: F = 1 + (T_e / T_0)
- [ ] Equivalent noise temperature documented

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Optimum Source Impedance
- [ ] R_opt = e_n,amp / i_n,amp calculated
- [ ] Source impedance matching discussed
- [ ] Noise matching vs. power matching distinguished
- [ ] Transformer coupling considered if applicable

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Correlation Analysis
- [ ] Correlated noise sources identified
- [ ] Cross-correlation coefficient specified
- [ ] Combined noise with correlation: u_total^2 = u_1^2 + u_2^2 + 2·r·u_1·u_2
- [ ] Uncorrelated assumption justified if used

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

**Level 4 Total:** ___ / 16 points

---

## Level 5: Maxwell Article Traceability (Expert)

### Historical Context
- [ ] Maxwell's statistical mechanics foundation referenced (Art. 301-320)
- [ ] Energy equipartition discussion included
- [ ] Fluctuation considerations noted
- [ ] Modern connection to thermal noise explained

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Instrument-Specific Articles
- [ ] Galvanometer: Art. 730-750, Art. 475-500
- [ ] Magnetometer: Art. 449-474, Art. 424-440
- [ ] Electrometer: Art. 230-235, Art. 44-49
- [ ] Relevant articles cited for noise sources

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### Theory Classification
- [ ] Maxwell's original text identified (maxwell_original)
- [ ] User extensions marked (user_original - NEVER ALTERED)
- [ ] Standard implementations marked (standard_math)
- [ ] Noise theory modern extensions documented

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

### CGS Consistency
- [ ] All noise formulas in CGS units
- [ ] Unit conversions documented if needed
- [ ] Maxwell's CGS choice respected throughout
- [ ] SI equivalents provided only as reference

**Status:** [ ] Pass [ ] Fail [ ] N/A  
**Score:** ___ / 4

**Level 5 Total:** ___ / 16 points

---

## Summary

| Level | Category | Score | Max | Percentage |
|-------|----------|-------|-----|------------|
| 1 | Noise Source Identification | ___ | 16 | ___% |
| 2 | Noise Calculation | ___ | 16 | ___% |
| 3 | Signal-to-Noise Analysis | ___ | 16 | ___% |
| 4 | Advanced Noise Analysis | ___ | 16 | ___% |
| 5 | Maxwell Article Traceability | ___ | 16 | ___% |
| **TOTAL** | | **___** | **80** | **___%** |

### Approval Status

**Status:** [ ] Approved [ ] Conditional [ ] Rejected

**Approver:** ______________________

**Date:** ______________________

**Next Review:** ______________________

---

## Reference Data

### Noise Formulas (CGS)

```
Thermal Voltage:    e_n = sqrt(4 · k_B · T · R · Δf)   [statvolt]
Thermal Current:    i_n = sqrt(4 · k_B · T · Δf / R)   [statampere]
Shot Noise:         i_n = sqrt(2 · q · I · Δf)         [statampere]
Flicker Noise:      S(f) = K_f / f^α                   [PSD]

Constants:
  k_B = 1.381×10^-16 erg/K
  q = 4.803×10^-10 statC
  T_room = 293 K
  k_B·T_room = 4.05×10^-14 erg
```

### Typical Noise Levels

| Device | e_n [statvolt/sqrt(Hz)] | i_n [statampere/sqrt(Hz)] |
|--------|------------------------|---------------------------|
| 1 statohm resistor | 1.28×10^-8 | - |
| 10 statohm resistor | 4.05×10^-8 | - |
| 1 statA current | - | 3.10×10^-5 |
| 10 statA current | - | 9.80×10^-5 |

### Maxwell Articles for Instruments

- **Galvanometers:** Art. 730-750 (primary), Art. 475-500 (EM force)
- **Magnetometers:** Art. 449-474 (measurements), Art. 424-440 (induction)
- **Electrometers:** Art. 230-235 (electrification), Art. 44-49 (potential)
- **Statistical Foundation:** Art. 301-320 (molecular statistics)

---

## Quality Criteria

- [ ] All noise sources identified and quantified
- [ ] RMS noise correctly integrated over bandwidth
- [ ] SNR and MDS calculated for application
- [ ] Integration improvement factor applied
- [ ] CGS units used consistently
- [ ] Maxwell articles cited where relevant

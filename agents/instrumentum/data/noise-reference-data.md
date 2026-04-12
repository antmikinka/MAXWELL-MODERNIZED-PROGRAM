# Data: noise-reference-data

## Purpose

Comprehensive reference data for noise analysis in electrical measurements.

---

## Noise Types and Formulas

### Thermal (Johnson-Nyquist) Noise

**Voltage Noise:**
```
e_n² = 4·k_B·T·R·Δf

e_n = √(4·k_B·T·R·Δf)  (RMS)

where:
  k_B = 1.381×10⁻¹⁶ erg/K (Boltzmann constant)
  T = temperature (K)
  R = resistance (statohm)
  Δf = bandwidth (Hz)
```

**Current Noise:**
```
i_n² = 4·k_B·T·Δf / R

i_n = √(4·k_B·T·Δf / R)  (RMS)
```

**Available Noise Power:**
```
P_n = k_B·T·Δf

At room temperature (T = 293 K):
P_n = 4.05×10⁻¹⁴ × Δf  erg/s
```

---

### Shot Noise

**Current Noise:**
```
i_n² = 2·q·I·Δf

i_n = √(2·q·I·Δf)  (RMS)

where:
  q = 4.803×10⁻¹⁰ statC (elementary charge)
  I = DC current (statA)
  Δf = bandwidth (Hz)
```

**Full Shot Noise Formula (including reverse current):**
```
i_n² = 2·q·(I_forward + I_reverse)·Δf
```

**Temperature Voltage Noise (diode):**
```
e_n = √(2·k_B·T·Δf / g_m)

where g_m = transconductance
```

---

### Flicker (1/f) Noise

**Noise Power Spectral Density:**
```
S(f) = K_f / f^α

where:
  K_f = noise coefficient (device dependent)
  α ≈ 1 (typically 0.8-1.2)
  f = frequency (Hz)
```

**RMS Noise in Band:**
```
i_n² = ∫(K_f / f^α) df  from f_L to f_H

For α = 1:
i_n² = K_f · ln(f_H / f_L)
```

**Corner Frequency:**
```
f_c = frequency where flicker noise = white noise

Below f_c: flicker noise dominates
Above f_c: white noise dominates
```

---

### Burst (Popcorn) Noise

**Characteristic:**
```
Discrete level transitions
Random telegraph signal
Amplitude: µV to mV range
Timescale: ms to seconds
```

**PSD Model:**
```
S(f) ∝ 1 / (1 + (f/f_c)²)

Lorentzian spectrum
```

---

### Vibration (Microphonic) Noise

**Output Noise:**
```
e_n = S_v · a

where:
  S_v = microphonic sensitivity (statvolt/(cm/s²))
  a = vibration acceleration (cm/s²)
```

**Vibration Spectra:**
```
Typical laboratory: 10⁻⁴ to 10⁻² cm/s²
With isolation: 10⁻⁶ to 10⁻⁴ cm/s²
```

---

## Noise Calculations at Room Temperature

### Reference Conditions

```
T = 293 K (20°C)
k_B·T = 4.05×10⁻¹⁴ erg
```

### Thermal Noise Examples

| Resistance | e_n (statvolt/√Hz) | e_n (statvolt) for 1 kHz BW |
|------------|-------------------|----------------------------|
| 1 statohm | 1.28×10⁻⁸ | 4.05×10⁻⁷ |
| 10 statohm | 4.05×10⁻⁸ | 1.28×10⁻⁶ |
| 100 statohm | 1.28×10⁻⁷ | 4.05×10⁻⁶ |
| 1000 statohm | 4.05×10⁻⁷ | 1.28×10⁻⁵ |

### Shot Noise Examples

| DC Current | i_n (statA/√Hz) | i_n (statA) for 1 kHz BW |
|------------|----------------|-------------------------|
| 1 statA | 3.10×10⁻⁵ | 9.80×10⁻⁴ |
| 10 statA | 9.80×10⁻⁵ | 3.10×10⁻³ |
| 100 statA | 3.10×10⁻⁴ | 9.80×10⁻³ |
| 1000 statA | 9.80×10⁻⁴ | 3.10×10⁻² |

---

## Noise in Amplifiers

### Equivalent Input Noise

**Voltage Noise:**
```
e_n,total² = e_n,source² + e_n,amp² + (i_n,amp · R_s)²

where:
  e_n,source = source thermal noise
  e_n,amp = amplifier voltage noise
  i_n,amp = amplifier current noise
  R_s = source resistance
```

**Optimum Source Resistance:**
```
R_opt = e_n,amp / i_n,amp

At R_opt, amplifier noise figure is minimum
```

### Noise Figure

**Definition:**
```
NF = SNR_in / SNR_out

NF (dB) = 10 · log₁₀(NF)
```

**Noise Factor:**
```
F = 1 + (T_e / T_0)

where:
  T_e = equivalent noise temperature
  T_0 = 293 K (reference)
```

---

## Noise Bandwidth

### Effective Noise Bandwidth

```
BW_n = (1 / |H(f_0)|²) · ∫|H(f)|² df

For single-pole lowpass:
BW_n = (π/2) · f_c = 1.57 · f_c

For brickwall filter:
BW_n = f_c
```

### Noise in Band

```
Total RMS noise in bandwidth [f_L, f_H]:

e_n,total = √(∫ S(f) df)

For white noise:
e_n,total = e_n · √(BW_n)
```

---

## Signal-to-Noise Ratio

### SNR Definition

```
SNR = P_signal / P_noise

SNR (dB) = 10 · log₁₀(SNR)

For voltage signals:
SNR (dB) = 20 · log₁₀(V_signal / V_noise)
```

### Minimum Detectable Signal

```
MDS = SNR_min × V_noise

Typical SNR_min values:
  Detection: 1-3
  Measurement: 10
  Precision: 100
```

### Integration Improvement

```
SNR improves with √(integration time)

SNR(t) = SNR(1s) × √t

MDS(t) = MDS(1s) / √t
```

---

## Noise Measurement Techniques

### Spectrum Analyzer Method

```
1. Connect device to spectrum analyzer
2. Set appropriate bandwidth
3. Measure noise PSD vs. frequency
4. Identify noise types from slope
```

### RMS Voltmeter Method

```
1. Measure total RMS noise
2. Bandwidth-limit if necessary
3. Subtract background noise
4. Calculate expected noise
```

### Correlation Method

```
1. Use two identical amplifiers
2. Cross-correlate outputs
3. Uncorrelated noise averages to zero
4. Very low noise measurable
```

---

## Maxwell's Noise Considerations

### Historical Context

Maxwell did not explicitly address thermal noise (discovered later by Johnson and Nyquist), but his statistical mechanics foundation enabled the theoretical understanding:

- Statistical treatment of molecular motion (Art. 301-320)
- Fluctuation considerations
- Energy equipartition

### Modern Connection

```
Thermal noise derivation uses:
- Equipartition theorem (from Maxwell-Boltzmann statistics)
- Random molecular motion
- Resistance as dissipation mechanism
```

---

## CGS Unit Reference

| Noise Quantity | CGS Unit | SI Equivalent |
|---------------|----------|---------------|
| Voltage noise | statvolt/√Hz | 299.79 V/√Hz |
| Current noise | statampere/√Hz | 3.336×10⁻¹⁰ A/√Hz |
| Power noise | erg/s | 10⁻⁷ W |
| Noise PSD | statvolt²/Hz | (299.79)² V²/Hz |

---

## Quality Criteria

- [ ] All formulas in CGS units
- [ ] Constants correctly specified
- [ ] Example calculations verified
- [ ] Measurement techniques documented

# Data: electrolysis-reference-data

## Purpose

Comprehensive reference data for electrolysis calculations and simulations in CGS units.

---

## Faraday's Laws of Electrolysis

### First Law
m = (Q / F) × (M / z) = (I·t / F) × (M / z)

where:
- m = mass deposited/dissolved (g)
- Q = total charge (statcoulomb)
- F = Faraday constant (see below)
- M = molar mass (g/mol)
- z = charge number (electrons per ion)
- I = current (statampere)
- t = time (s)

### Second Law
For the same quantity of electricity, masses deposited are proportional to equivalent weights (M/z).

**Maxwell Reference:** Art. 236-238

---

## Fundamental Constants (CGS)

| Constant | Symbol | Value | Units |
|----------|--------|-------|-------|
| Faraday constant | F | 96485 C/mol = 2.873×10¹⁴ statcoulomb/equiv | statcoulomb/equiv |
| Elementary charge | e | 1.602×10⁻¹⁹ C = 4.803×10⁻¹⁰ statcoulomb | statcoulomb |
| Avogadro's number | N_A | 6.022×10²³ mol⁻¹ | mol⁻¹ |
| Boltzmann constant | k_B | 1.381×10⁻¹⁶ erg/K | erg/K |
| Gas constant | R | 8.314×10⁷ erg/mol·K | erg/mol·K |
| Absolute zero | T_0 | -273.15°C = 0 K | K |

---

## Standard Electrode Potentials (25°C)

### Reduction Potentials (converted to CGS statvolt)

Note: 1 V = 1/299.79 statvolt

| Half-Reaction | E° (V vs SHE) | E° (statvolt) |
|---------------|---------------|---------------|
| Li⁺ + e⁻ → Li | -3.04 | -0.0101 |
| K⁺ + e⁻ → K | -2.93 | -0.00978 |
| Na⁺ + e⁻ → Na | -2.71 | -0.00904 |
| Mg²⁺ + 2e⁻ → Mg | -2.37 | -0.00791 |
| Al³⁺ + 3e⁻ → Al | -1.66 | -0.00554 |
| Zn²⁺ + 2e⁻ → Zn | -0.76 | -0.00254 |
| Fe²⁺ + 2e⁻ → Fe | -0.44 | -0.00147 |
| 2H⁺ + 2e⁻ → H₂ | 0.00 | 0.0000 |
| Cu²⁺ + 2e⁻ → Cu | +0.34 | +0.00113 |
| Ag⁺ + e⁻ → Ag | +0.80 | +0.00267 |
| Au³⁺ + 3e⁻ → Au | +1.50 | +0.00500 |
| Cl₂ + 2e⁻ → 2Cl⁻ | +1.36 | +0.00454 |
| O₂ + 4H⁺ + 4e⁻ → 2H₂O | +1.23 | +0.00410 |

**Maxwell Reference:** Art. 236-238, 280-286

---

## Electrochemical Equivalent Masses

### Mass per Unit Charge

| Element | M (g/mol) | z | E = M/z (g/equiv) | m/F (g/statcoulomb) |
|---------|-----------|----|-------------------|---------------------|
| Hydrogen | 1.008 | 1 | 1.008 | 3.51×10⁻¹⁵ |
| Oxygen | 16.00 | 2 | 16.00 | 5.57×10⁻¹⁴ |
| Copper | 63.55 | 2 | 31.77 | 1.11×10⁻¹³ |
| Silver | 107.87 | 1 | 107.87 | 3.75×10⁻¹³ |
| Gold | 196.97 | 3 | 65.66 | 2.28×10⁻¹³ |
| Zinc | 65.38 | 2 | 32.69 | 1.14×10⁻¹³ |
| Aluminum | 26.98 | 3 | 8.99 | 3.13×10⁻¹⁴ |
| Chlorine | 35.45 | 1 | 35.45 | 1.23×10⁻¹³ |

**Maxwell Reference:** Art. 236-237

---

## Ionic Conductivities (Infinite Dilution, 25°C)

### Molar Ionic Conductivities

| Ion | λ° (mho·cm²/equiv) | u (cm²/statvolt·s) | D (cm²/s) |
|-----|-------------------|-------------------|-----------|
| H⁺ | 349.8 | 3.63×10⁻³ | 9.31×10⁻⁵ |
| OH⁻ | 198.0 | 2.05×10⁻³ | 5.27×10⁻⁵ |
| Na⁺ | 50.1 | 5.19×10⁻⁴ | 1.33×10⁻⁵ |
| K⁺ | 73.5 | 7.62×10⁻⁴ | 1.96×10⁻⁵ |
| NH₄⁺ | 73.5 | 7.62×10⁻⁴ | 1.96×10⁻⁵ |
| Ca²⁺ | 59.5 | 6.17×10⁻⁴ | 7.92×10⁻⁶ |
| Mg²⁺ | 53.0 | 5.50×10⁻⁴ | 7.06×10⁻⁶ |
| Cl⁻ | 76.3 | 7.91×10⁻⁴ | 2.03×10⁻⁵ |
| Br⁻ | 78.1 | 8.10×10⁻⁴ | 2.08×10⁻⁵ |
| I⁻ | 76.8 | 7.97×10⁻⁴ | 2.05×10⁻⁵ |
| NO₃⁻ | 71.4 | 7.40×10⁻⁴ | 1.90×10⁻⁵ |
| SO₄²⁻ | 79.9 | 8.27×10⁻⁴ | 1.06×10⁻⁵ |
| CH₃COO⁻ | 40.9 | 4.24×10⁻⁴ | 1.09×10⁻⁵ |

**Maxwell Reference:** Art. 269-286

---

## Nernst Equation (CGS Form)

### General Form
E = E° - (RT/zF) × ln(Q)

At 25°C (298.15 K):
- RT/F = 0.02569 V = 8.57×10⁻⁵ statvolt
- (RT/F) × ln(10) = 0.05916 V = 1.97×10⁻⁴ statvolt

### CGS Form
E = E° - (k_B·T / z·e) × ln(Q)

where:
- k_B = 1.381×10⁻¹⁶ erg/K
- e = 4.803×10⁻¹⁰ statcoulomb
- T in Kelvin

**Maxwell Reference:** Art. 280-286

---

## Butler-Volmer Equation

### Current Density
j = j₀ × [exp(α·z·e·η / k_B·T) - exp(-(1-α)·z·e·η / k_B·T)]

where:
- j = net current density (statampere/cm²)
- j₀ = exchange current density (statampere/cm²)
- α = transfer coefficient (typically 0.5)
- η = overpotential (statvolt)
- z = charge number
- e = elementary charge
- k_B = Boltzmann constant
- T = temperature (K)

### Low Overpotential Limit (|η| << kT/e ≈ 0.0257 V)
j ≈ j₀ × (z·e·η / k_B·T)

### High Overpotential (Tafel Equation)
|η| >> kT/e: j ≈ j₀ × exp(α·z·e·|η| / k_B·T)

**Maxwell Reference:** Art. 280-286

---

## Exchange Current Densities

### Typical Values at 25°C

| Reaction | Electrode | j₀ (A/cm²) | j₀ (statampere/cm²) |
|----------|-----------|------------|--------------------|
| H⁺/H₂ | Pt | 10⁻³ | 3×10⁶ |
| H⁺/H₂ | Ni | 10⁻⁵ | 3×10⁴ |
| H⁺/H₂ | Hg | 10⁻¹² | 3×10⁻³ |
| O₂/H₂O | Pt | 10⁻¹⁰ | 3×10⁻¹ |
| Cu²⁺/Cu | Cu | 10⁻³ | 3×10⁶ |
| Zn²⁺/Zn | Zn | 10⁻⁵ | 3×10⁴ |
| Ag⁺/Ag | Ag | 10⁻³ | 3×10⁶ |

**Maxwell Reference:** Art. 280-286

---

## Diffusion Layer Parameters

### Nernst Diffusion Layer

| Condition | δ (cm) | Notes |
|-----------|--------|-------|
| Quiescent solution | 0.01-0.05 | Natural convection |
| Mild stirring | 0.001-0.01 | Forced convection |
| Rotating disk (1000 rpm) | 0.0001-0.001 | Levich equation |
| Flowing electrolyte | 0.0001-0.001 | Depends on flow rate |

### Limiting Current Density
j_L = z·F·D·c_b / δ

**Maxwell Reference:** Art. 230-235, 280-286

---

## Overpotential Components

### Total Overpotential
η_total = η_activation + η_concentration + η_ohmic

### Ohmic Drop (IR Drop)
η_ohmic = I × R = j × (δ/σ)

where:
- σ = electrolyte conductivity (s⁻¹, CGS)
- δ = distance (cm)

### Concentration Overpotential
η_conc = (RT/zF) × ln(1 - j/j_L)

**Maxwell Reference:** Art. 280-286

---

## Temperature Coefficients

### Conductivity Temperature Dependence
σ(T) = σ(T₀) × [1 + α(T - T₀)]

| Electrolyte | α (K⁻¹) | Reference T₀ |
|-------------|---------|--------------|
| H₂SO₄ (1M) | 0.015 | 298 K |
| NaOH (1M) | 0.018 | 298 K |
| NaCl (1M) | 0.023 | 298 K |
| KOH (1M) | 0.017 | 298 K |

### Viscosity Temperature Dependence (Water)
| T (°C) | η (poise) |
|--------|-----------|
| 0 | 0.0179 |
| 20 | 0.0100 |
| 40 | 0.0065 |
| 60 | 0.0047 |
| 80 | 0.0035 |
| 100 | 0.0028 |

---

## Notes on Data Quality

- All values converted to CGS electrostatic units
- Standard conditions: 25°C (298.15 K), 1 atm unless noted
- Theory classification: standard_math for electrochemical constants
- Maxwell article references provide historical context
- Verify critical values against primary sources

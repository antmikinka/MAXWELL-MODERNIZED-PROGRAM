# Data: magnetic-materials-reference

## Purpose

Comprehensive reference data for magnetic materials in CGS units including hysteresis parameters, permeability data, and loss characteristics.

---

## Magnetic Unit Reference (CGS)

| Quantity | Symbol | CGS Unit | SI Equivalent |
|----------|--------|----------|---------------|
| Magnetic field | H | oersted (Oe) | 1 Oe = 79.577 A/m |
| Magnetic induction | B | gauss (G) | 1 G = 10⁻⁴ T |
| Magnetization | I, M | emu/cm³ | 1 emu/cm³ = 1000 A/m |
| Permeability | μ | dimensionless | μ_CGS = μ_SI (relative) |
| Susceptibility | κ | dimensionless | κ_CGS = κ_SI / 4π |
| Magnetic moment | m | emu = erg/G | 1 emu = 10⁻³ A·m² |
| Energy density | W | erg/cm³ | 1 erg/cm³ = 0.1 J/m³ |

### Key Relations (CGS)
- B = H + 4πI = μH
- μ = 1 + 4πκ
- I = κH

**Maxwell Reference:** Art. 424-440

---

## Soft Magnetic Materials

### Iron and Steel (CGS Units)

| Material | μ_i | μ_max | H_c (Oe) | B_r (G) | B_sat (G) | Loss (erg/cm³·cycle) |
|----------|-----|-------|----------|---------|-----------|---------------------|
| Iron (pure, annealed) | 1500 | 5000 | 0.5 | 8000 | 21500 | 500 |
| Iron (pure, cold-worked) | 500 | 2000 | 2.0 | 9000 | 21500 | 1500 |
| Silicon steel (1%) | 1000 | 4000 | 0.4 | 7000 | 19000 | 300 |
| Silicon steel (3%) | 1500 | 7000 | 0.3 | 7500 | 20000 | 200 |
| Silicon steel (4%) | 1200 | 5000 | 0.2 | 6500 | 18000 | 150 |

### Nickel-Iron Alloys (Permalloys)

| Alloy | Composition | μ_i | μ_max | H_c (Oe) | B_r (G) | B_sat (G) |
|-------|-------------|-----|-------|----------|---------|-----------|
| Permalloy A | 78% Ni, 22% Fe | 5000 | 50000 | 0.05 | 5000 | 10000 |
| Permalloy B | 50% Ni, 50% Fe | 500 | 10000 | 0.3 | 7000 | 15000 |
| Permalloy C | 80% Ni, 20% Fe | 8000 | 100000 | 0.02 | 5000 | 10000 |
| Supermalloy | 79% Ni, 16% Fe, 5% Mo | 100000 | 800000 | 0.002 | 4000 | 8000 |

### Ferrites (Soft)

| Material | μ_i | μ_max | H_c (Oe) | B_sat (G) | Resistivity (Ω·cm) |
|----------|-----|-------|----------|-----------|-------------------|
| Mn-Zn ferrite | 1000-1500 | 3000 | 0.1 | 4500 | 10-100 |
| Ni-Zn ferrite | 100-500 | 1500 | 0.5 | 3000 | 10⁶-10⁸ |
| Mg-Zn ferrite | 50-200 | 500 | 1.0 | 2000 | 10⁶-10⁸ |

**Maxwell Reference:** Art. 424-448

---

## Hard Magnetic Materials

### Alnico Alloys (CGS Units)

| Alloy | H_c (Oe) | B_r (G) | (BH)_max (MGOe) | T_C (°C) |
|-------|----------|---------|-----------------|----------|
| Alnico 2 | 550 | 11500 | 4.0 | 850 |
| Alnico 5 | 600 | 12500 | 5.5 | 860 |
| Alnico 8 | 1700 | 8000 | 5.0 | 860 |
| Alnico 9 | 1300 | 10500 | 9.0 | 860 |

### Ferrite Magnets (Ceramic)

| Grade | H_c (Oe) | B_r (G) | (BH)_max (MGOe) |
|-------|----------|---------|-----------------|
| Ferrite 1 | 2200 | 3600 | 2.5 |
| Ferrite 5 | 3000 | 3800 | 3.5 |
| Ferrite 8 | 3500 | 4000 | 4.0 |

### Rare-Earth Magnets

| Material | H_c (Oe) | B_r (G) | (BH)_max (MGOe) | T_C (°C) |
|----------|----------|---------|-----------------|----------|
| NdFeB N35 | 12000 | 12000 | 35 | 310 |
| NdFeB N52 | 10500 | 14500 | 52 | 310 |
| SmCo₅ | 8000 | 10000 | 20 | 720 |
| Sm₂Co₁₇ | 9000 | 11000 | 25 | 800 |

**Maxwell Reference:** Art. 441-448

---

## Hysteresis Loop Parameters

### Typical Jiles-Atherton Parameters

| Material | M_s (emu/cm³) | α | a (Oe) | k (Oe) | c |
|----------|---------------|----|--------|--------|---|
| Pure iron | 1714 | 0.0001 | 300 | 45 | 0.3 |
| Silicon steel | 1600 | 0.0002 | 150 | 25 | 0.4 |
| Permalloy | 800 | 0.00005 | 50 | 5 | 0.5 |
| Ferrite | 350 | 0.001 | 100 | 30 | 0.2 |

### Typical Preisach Parameters

| Material | H_c_mean (Oe) | σ_Hc (Oe) | H_int_mean (Oe) | σ_Hint (Oe) |
|----------|---------------|-----------|-----------------|-------------|
| Pure iron | 0.5 | 0.2 | 0.01 | 0.05 |
| Silicon steel | 0.3 | 0.1 | 0.005 | 0.02 |
| Alnico 5 | 600 | 100 | 50 | 100 |
| Ferrite | 3000 | 500 | 100 | 200 |

**Maxwell Reference:** Art. 444-447 (Weber's molecular hypothesis)

---

## Hysteresis Loss Data

### Steinmetz Coefficients

| Material | η (erg/cm³·cycle) | n (exponent) |
|----------|-------------------|--------------|
| Pure iron | 500 | 1.6 |
| Silicon steel (3%) | 200 | 1.6 |
| Permalloy | 50 | 1.5 |
| Ferrite (Mn-Zn) | 100 | 1.8 |
| Ferrite (Ni-Zn) | 150 | 1.8 |

### Steinmetz Equation
W_h = η × B_max^n × f

where:
- W_h = hysteresis loss (erg/cm³·s)
- η = loss coefficient (erg/cm³·cycle)
- B_max = maximum flux density (G)
- n = Steinmetz exponent (typically 1.6-2.0)
- f = frequency (Hz)

**Maxwell Reference:** Art. 424-430

---

## Magnetic Anisotropy Constants

### Uniaxial Anisotropy (CGS: erg/cm³)

| Material | K₁ | Easy Axis |
|----------|-----|-----------|
| Cobalt (hcp) | 4.5×10⁶ | c-axis |
| Barium ferrite | 3.3×10⁵ | c-axis |
| Yttrium iron garnet | -6×10³ | <111> |

### Cubic Anisotropy (CGS: erg/cm³)

| Material | K₁ | K₂ | Easy Axes |
|----------|-----|-----|-----------|
| Iron | 4.8×10⁴ | 2.0×10⁴ | <100> |
| Nickel | -5.7×10³ | 0.5×10³ | <111> |
| Magnetite (Fe₃O₄) | -1.4×10⁴ | 0 | <111> |

**Maxwell Reference:** Art. 424-440

---

## Magnetostriction Coefficients

### Saturation Magnetostriction (dimensionless)

| Material | λ_s |
|----------|-----|
| Iron | 21×10⁻⁶ |
| Nickel | -33×10⁻⁶ |
| Cobalt | -60×10⁻⁶ |
| Permalloy (80% Ni) | ~0 |
| Terfenol-D | 1600×10⁻⁶ |

**Maxwell Reference:** Art. 424-440

---

## Temperature Dependence

### Curie Temperatures

| Material | T_C (K) | T_C (°C) |
|----------|---------|----------|
| Iron | 1043 | 770 |
| Cobalt | 1394 | 1121 |
| Nickel | 631 | 358 |
| Gadolinium | 292 | 19 |
| Magnetite (Fe₃O₄) | 858 | 585 |
| Permalloy (80% Ni) | 870 | 597 |
| Alnico 5 | 1133 | 860 |

### Temperature Coefficients of Permeability

| Material | α_μ (K⁻¹) | Temperature Range |
|----------|-----------|-------------------|
| Pure iron | +0.001 | 20-100°C |
| Silicon steel | +0.0005 | 20-100°C |
| Permalloy | variable | near T_C |
| Ferrite (Mn-Zn) | -0.002 | 20-100°C |

---

## Demagnetizing Factors

### Ellipsoid Demagnetizing Factors (N_x + N_y + N_z = 4π)

| Shape | N_x | N_y | N_z |
|-------|-----|-----|-----|
| Sphere | 4π/3 | 4π/3 | 4π/3 |
| Thin disk (⊥ plane) | 0 | 0 | 4π |
| Long cylinder (∥ axis) | 2π | 2π | 0 |
| Infinite plate | 0 | 0 | 4π |

**Maxwell Reference:** Art. 424-440

---

## Notes on Data Quality

- All values in CGS units (Maxwell's choice)
- Properties vary with processing, heat treatment, purity
- Theory classification: standard_math for measured properties
- Maxwell article references provide historical context
- Verify critical values against primary sources

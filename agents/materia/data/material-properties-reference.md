# Data: material-properties-reference

## Purpose

Comprehensive reference for material properties in CGS units covering dielectrics, magnetic materials, conductors, and electrolytes.

---

## Dielectric Materials

### Common Dielectrics (CGS Units)

| Material | K (dielectric constant) | tan δ | Breakdown (statvolt/cm) | Resistivity (statohm·cm) |
|----------|------------------------|-------|------------------------|-------------------------|
| Vacuum | 1.0 | 0 | ∞ | ∞ |
| Air (STP) | 1.0006 | ~0 | 75 | >10¹⁵ |
| Mica (Muskovite) | 6.5-7.5 | 0.0002 | 2000 | 10¹⁵ |
| Glass (Pyrex) | 4.5-5.0 | 0.001-0.01 | 300-500 | 10¹²-10¹⁴ |
| Quartz (fused) | 3.78 | 0.0001 | 500 | 10¹⁴ |
| Polystyrene | 2.4-2.7 | 0.0001-0.0003 | 500-700 | 10¹⁶ |
| Polyethylene | 2.25 | 0.0002 | 500 | 10¹⁶ |
| Teflon (PTFE) | 2.1 | 0.0002 | 500 | 10¹⁷ |
| Paper (dry) | 3.0-3.5 | 0.01-0.03 | 150 | 10¹⁰ |
| Water (pure, 20°C) | 80.4 | 0.0001 | ~65 | 10⁶ |
| Barium titanate | 1200-10000 | 0.01-0.02 | 100-300 | 10⁸ |

### Dielectric Absorption Coefficients

| Material | Absorption Coefficient | Relaxation Time (s) |
|----------|----------------------|---------------------|
| Mica | 0.02 | 10⁻⁶ - 10⁻³ |
| Glass | 0.05-0.15 | 10⁻⁵ - 1 |
| Paper | 0.1-0.3 | 10⁻⁴ - 10 |
| Polyethylene | 0.001-0.01 | 10⁻⁷ - 10⁻⁴ |

**Maxwell References:** Art. 50-62, 79-83, 103-111

---

## Magnetic Materials

### Soft Magnetic Materials (CGS Units)

| Material | μ (max permeability) | H_c (coercivity, Oe) | B_r (remanence, G) | B_sat (saturation, G) |
|----------|---------------------|---------------------|-------------------|----------------------|
| Iron (pure, annealed) | 5000 | 0.5 | 8000 | 21500 |
| Silicon steel (3%) | 7000 | 0.3 | 7500 | 20000 |
| Permalloy (80% Ni) | 100000 | 0.002 | 5000 | 10000 |
| Supermalloy | 800000 | 0.0002 | 4000 | 8000 |
| Ferrite (Mn-Zn) | 1500 | 0.1 | 1500 | 4500 |
| Ferrite (Ni-Zn) | 500 | 0.5 | 1000 | 3000 |

### Hard Magnetic Materials (CGS Units)

| Material | H_c (coercivity, Oe) | B_r (remanence, G) | (BH)_max (MGOe) |
|----------|---------------------|-------------------|-----------------|
| Alnico 5 | 600 | 12500 | 5.5 |
| Ferrite (ceramic) | 3000 | 3800 | 3.5 |
| Neodymium (NdFeB) | 12000 | 13000 | 40 |
| Samarium-cobalt | 8000 | 10000 | 25 |

### Magnetic Susceptibilities (CGS, dimensionless)

| Material | κ = (μ-1)/4π | Classification |
|----------|-------------|----------------|
| Vacuum | 0 | Non-magnetic |
| Copper | -1.0×10⁻⁶ | Diamagnetic |
| Water | -0.7×10⁻⁶ | Diamagnetic |
| Aluminum | 2.2×10⁻⁵ | Paramagnetic |
| Air | 0.04×10⁻⁶ | Weakly paramagnetic |
| Iron (saturated) | ~1700 | Ferromagnetic |

**Maxwell References:** Art. 424-448, 444-447 (Weber)

---

## Conductive Materials

### Electrical Conductivity (CGS: s⁻¹)

| Material | σ (s⁻¹) | ρ (statohm·cm) | Temperature Coefficient (K⁻¹) |
|----------|---------|----------------|-------------------------------|
| Silver | 6.3×10¹⁷ | 1.6×10⁻¹⁸ | 0.0038 |
| Copper (annealed) | 5.8×10¹⁷ | 1.7×10⁻¹⁸ | 0.0039 |
| Gold | 4.5×10¹⁷ | 2.2×10⁻¹⁸ | 0.0034 |
| Aluminum | 3.5×10¹⁷ | 2.8×10⁻¹⁸ | 0.0043 |
| Tungsten | 1.8×10¹⁷ | 5.5×10⁻¹⁸ | 0.0045 |
| Iron | 1.0×10¹⁷ | 9.7×10⁻¹⁸ | 0.0050 |
| Nichrome | 1.1×10¹⁶ | 9.1×10⁻¹⁷ | 0.0004 |
| Graphite | 2×10¹⁴ | 5×10⁻¹⁵ | -0.0005 |
| Sea water | ~5×10¹⁰ | ~2×10⁻¹¹ | variable |

### Superconductors (below T_c)

| Material | T_c (K) | Critical Field (G) |
|----------|---------|-------------------|
| Mercury | 4.15 | 410 |
| Lead | 7.2 | 800 |
| Niobium | 9.2 | 2000 |
| NbTi | 10 | 100000 |
| YBCO | 92 | >10⁶ |

**Maxwell References:** Art. 230-300, 269-286

---

## Electrolytic Materials

### Ionic Mobilities (CGS: cm²/statvolt·s, 25°C, infinite dilution)

| Ion | u (cm²/statvolt·s) | z | λ (mho·cm²/equiv) |
|-----|-------------------|----|------------------|
| H⁺ | 3.63×10⁻³ | +1 | 349.8 |
| Na⁺ | 5.19×10⁻⁴ | +1 | 50.1 |
| K⁺ | 7.62×10⁻⁴ | +1 | 73.5 |
| Ca²⁺ | 6.17×10⁻⁴ | +2 | 59.5 |
| Cl⁻ | 7.91×10⁻⁴ | -1 | 76.3 |
| OH⁻ | 2.05×10⁻³ | -1 | 198.0 |
| SO₄²⁻ | 8.27×10⁻⁴ | -2 | 79.9 |

### Diffusion Coefficients (CGS: cm²/s, 25°C)

| Ion | D (cm²/s) |
|-----|-----------|
| H⁺ | 9.31×10⁻⁵ |
| Na⁺ | 1.33×10⁻⁵ |
| K⁺ | 1.96×10⁻⁵ |
| Cl⁻ | 2.03×10⁻⁵ |
| OH⁻ | 5.27×10⁻⁵ |

### Transport Numbers (aqueous, 25°C)

| Electrolyte | t₊ | t₋ |
|-------------|----|----|
| HCl | 0.821 | 0.179 |
| NaCl | 0.396 | 0.604 |
| KCl | 0.490 | 0.510 |
| CuSO₄ | 0.37 | 0.63 |

**Maxwell References:** Art. 236-238, 269-286

---

## Composite Materials

### Effective Medium Parameters

| Composite Type | f_critical | Model | Validity Range |
|----------------|------------|-------|----------------|
| Spherical inclusions | 0.64 (random close pack) | Maxwell-Garnett | f < 0.2 |
| Spherical inclusions | 0.64 | Bruggeman | 0 < f < 0.6 |
| Fibers (aligned) | 0.91 (hexagonal) | Rule of mixtures | all f |
| Platelets | variable | Halpin-Tsai | all f |

**Maxwell References:** Art. 314

---

## Temperature Dependence Parameters

### Arrhenius Parameters for Dielectrics

| Material | E_a (erg/mol) | τ₀ (s) | Reference T (K) |
|----------|---------------|--------|-----------------|
| Polyethylene | 8.4×10¹¹ | 10⁻¹⁴ | 300 |
| PTFE | 1.2×10¹² | 10⁻¹³ | 300 |
| Epoxy | 1.0×10¹² | 10⁻¹² | 300 |

### Curie Temperatures (Magnetic Materials)

| Material | T_C (K) |
|----------|---------|
| Iron | 1043 |
| Cobalt | 1394 |
| Nickel | 631 |
| Gadolinium | 292 |

---

## Conversion Factors

### To CGS from SI

| Quantity | Multiply SI by | Result |
|----------|---------------|--------|
| Electric field (V/m) | 1/29979 | statvolt/cm |
| Potential (V) | 1/299.79 | statvolt |
| Current (A) | 3.336×10⁻¹⁰ | statampere |
| Charge (C) | 3.336×10⁻⁹ | statcoulomb |
| Capacitance (F) | 8.988×10¹¹ | statfarad |
| Resistance (Ω) | 1.113×10⁻¹² | statohm |
| Conductivity (S/m) | 8.988×10⁹ | s⁻¹ |
| Magnetic field (A/m) | 4π×10⁻³ | oersted |
| Magnetic induction (T) | 10⁴ | gauss |

---

## Notes on Data Quality

- Values are typical; actual properties depend on processing, purity, temperature
- Always verify critical values against primary sources
- CGS units are used throughout to maintain consistency with Maxwell's treatise
- Theory classification should be assigned to each dataset

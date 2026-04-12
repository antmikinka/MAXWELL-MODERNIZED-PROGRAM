# Data: network-theorems-reference

## Purpose

Comprehensive reference data for network theorems in CGS units.

---

## Fundamental Network Theorems

### Kirchhoff's Laws

**Kirchhoff's Current Law (KCL):**
```
Σ I_entering = Σ I_leaving

or: Σ I = 0  (at any node)

Maxwell Reference: Art. 230-235
```

**Kirchhoff's Voltage Law (KVL):**
```
Σ V_rises = Σ V_drops

or: Σ V = 0  (around any closed loop)

Maxwell Reference: Art. 287-300
```

---

### Thevenin's Theorem

**Statement:**
Any linear two-terminal network can be replaced by an equivalent circuit consisting of a voltage source V_th in series with a resistance R_th.

**Procedure:**
```
1. Remove the load
2. Calculate open-circuit voltage: V_th = V_oc
3. Zero all independent sources
4. Calculate equivalent resistance: R_th = R_eq
5. Reconnect load to Thevenin equivalent
```

**Load Current:**
```
I_L = V_th / (R_th + R_L)

Load Voltage:
V_L = V_th × R_L / (R_th + R_L)

Load Power:
P_L = V_L² / R_L
```

**CGS Units:**
- V_th: statvolt
- R_th, R_L: statohm
- I_L: statampere
- P_L: erg/s

---

### Norton's Theorem

**Statement:**
Any linear two-terminal network can be replaced by an equivalent circuit consisting of a current source I_N in parallel with a resistance R_N.

**Procedure:**
```
1. Remove the load
2. Calculate short-circuit current: I_N = I_sc
3. Zero all independent sources
4. Calculate equivalent resistance: R_N = R_eq
5. Reconnect load to Norton equivalent
```

**Load Current:**
```
I_L = I_N × R_N / (R_N + R_L)

Load Voltage:
V_L = I_N × (R_N || R_L)
```

**Thevenin-Norton Conversion:**
```
V_th = I_N × R_th
R_th = R_N
I_N = V_th / R_th
```

**CGS Units:**
- I_N: statampere
- R_N: statohm
- V_th: statvolt

---

### Superposition Theorem

**Statement:**
In a linear circuit with multiple independent sources, the response (voltage or current) at any element is the algebraic sum of the responses due to each source acting alone.

**Procedure:**
```
1. Consider one independent source at a time
2. Replace other voltage sources with short circuits
3. Replace other current sources with open circuits
4. Calculate response due to active source
5. Sum all individual responses algebraically
```

**Important Notes:**
- Applies only to linear circuits
- Does NOT apply to power calculations
- Dependent sources remain active

**Example:**
```
For circuit with V1, V2, I3:

I_x = I_x(V1 only) + I_x(V2 only) + I_x(I3 only)

P_x ≠ P_x(V1 only) + P_x(V2 only) + P_x(I3 only)
```

---

### Maximum Power Transfer Theorem

**Statement:**
Maximum power is transferred from a source to a load when the load resistance equals the Thevenin resistance of the source.

**For Resistive Load:**
```
Condition: R_L = R_th

Maximum Power:
P_max = V_th² / (4 × R_th)

Efficiency at Maximum Power:
η = P_L / P_source = 50%
```

**For Complex Load:**
```
Condition: Z_L = Z_th*  (conjugate match)

where:
  Z_th* = complex conjugate of Thevenin impedance
```

**CGS Units:**
- P_max: erg/s
- V_th: statvolt
- R_th: statohm

---

### Reciprocity Theorem

**Statement:**
In a linear bilateral network with a single source, if the positions of source and response are interchanged, the ratio of response to excitation remains the same.

**Form Statement:**
```
If a voltage source V in branch 1 produces current I in branch 2,
then the same voltage source V in branch 2 produces the same current I in branch 1.

V₁/I₂ = V₂/I₁  (transfer impedances are equal)
```

**Conditions:**
- Linear network
- Bilateral elements (R, L, C)
- Single independent source
- No dependent sources (or handled correctly)

**Application:**
- Antenna theory
- Filter design
- Network analysis verification

---

### Tellegen's Theorem

**Statement:**
For any lumped network, the sum of the products of branch voltages and branch currents (with consistent reference directions) is zero.

**Mathematical Form:**
```
Σ (v_k × i_k) = 0

where:
  v_k = voltage across branch k
  i_k = current through branch k
  Sum over all branches
```

**Implications:**
- Based only on topology (KCL, KVL)
- Independent of element types
- Applies to linear and nonlinear networks
- Power conservation special case

**Application:**
- Network verification
- Sensitivity analysis
- Network synthesis

---

### Millman's Theorem

**Statement:**
For parallel voltage sources, the equivalent voltage is the weighted average of individual source voltages.

**Formula:**
```
V_eq = Σ(V_i / R_i) / Σ(1 / R_i)

R_eq = 1 / Σ(1 / R_i)

or using conductance (G = 1/R):

V_eq = Σ(V_i × G_i) / Σ(G_i)
```

**CGS Units:**
- V_i: statvolt
- R_i: statohm
- G_i: s⁻¹ (CGS conductance)

**Application:**
- Parallel battery analysis
- Op-amp summing circuits
- Node voltage calculation

---

## Network Transformations

### Y-Δ (Star-Delta) Transformation

**Δ to Y Conversion:**
```
Given Δ resistances: R_ab, R_bc, R_ca

Y resistances:
R_a = (R_ab × R_ca) / (R_ab + R_bc + R_ca)
R_b = (R_ab × R_bc) / (R_ab + R_bc + R_ca)
R_c = (R_bc × R_ca) / (R_ab + R_bc + R_ca)
```

**Y to Δ Conversion:**
```
Given Y resistances: R_a, R_b, R_c

Δ resistances:
R_ab = (R_a×R_b + R_b×R_c + R_c×R_a) / R_c
R_bc = (R_a×R_b + R_b×R_c + R_c×R_a) / R_a
R_ca = (R_a×R_b + R_b×R_c + R_c×R_a) / R_b
```

**Memory Aid:**
- Y from Δ: Product of adjacent Δ / Sum of all Δ
- Δ from Y: Sum of products / Opposite Y

**CGS Units:**
- All resistances in statohm

---

### Source Transformation

**Voltage to Current Source:**
```
Given: Voltage source V_s in series with R_s

Equivalent: Current source I_s = V_s / R_s
            Parallel resistance R_p = R_s
```

**Current to Voltage Source:**
```
Given: Current source I_s in parallel with R_p

Equivalent: Voltage source V_s = I_s × R_p
            Series resistance R_s = R_p
```

**CGS Units:**
- V_s: statvolt
- I_s: statampere
- R_s, R_p: statohm

---

## Substitution Theorem

**Statement:**
If the voltage across and current through any branch of a network are known, that branch may be replaced by any combination of elements that maintains the same voltage and current.

**Applications:**
- Simplify analysis
- Model complex devices
- Verify calculations

---

## Compensation Theorem

**Statement:**
For a small change in impedance ΔZ in a branch, the resulting change in any response is equal to the response produced by a compensating voltage source -I×ΔZ in series with the changed impedance.

**Formula:**
```
For impedance change Z → Z + ΔZ:

Compensating source: V_comp = -I × ΔZ

where I is the original current through the branch
```

**Application:**
- Sensitivity analysis
- Tolerance analysis
- Bridge circuit analysis

---

## Middlebrook's Extra Element Theorem

**Statement:**
The transfer function of a network with an extra element can be expressed in terms of the transfer function without that element.

**Formula:**
```
H(s) = H_0(s) × (1 + Z_n/Z) / (1 + Z_d/Z)

where:
  H_0 = transfer function without extra element
  Z = impedance of extra element
  Z_n = null double injection impedance
  Z_d = driving point impedance
```

**Application:**
- Circuit design
- Feedback analysis
- Filter synthesis

---

## Norton-Thevenin Duality

| Thevenin | Norton |
|----------|--------|
| V_th (voltage source) | I_N (current source) |
| R_th (series) | R_N (parallel) |
| V_th = I_N × R_th | I_N = V_th / R_th |
| Open-circuit voltage | Short-circuit current |

---

## CGS Unit Reference for Network Theorems

| Quantity | CGS Unit | Conversion |
|----------|----------|------------|
| Voltage | statvolt | 1 statV = 299.79 V |
| Current | statampere | 1 statA = 3.336×10⁻¹⁰ A |
| Resistance | statohm | 1 statΩ = 8.988×10¹¹ Ω |
| Conductance | s⁻¹ | 1 s⁻¹ (CGS) = 8.988×10¹¹ S |
| Power | erg/s | 1 erg/s = 10⁻⁷ W |
| Energy | erg | 1 erg = 10⁻⁷ J |

---

## Maxwell Article References

| Topic | Maxwell Articles |
|-------|------------------|
| Current continuity | Art. 230-235 |
| Network conduction | Art. 287-300 |
| Conduction theory | Art. 301-320 |
| Wheatstone bridge | Art. 343-348 |
| Self-inductance | Art. 541-570 |
| Mutual inductance | Art. 541-570 |

---

## Quality Criteria

- [ ] Theorem conditions verified
- [ ] CGS units used consistently
- [ ] Maxwell article citations included
- [ ] Results verified by alternate method
- [ ] Physical reasonableness checked

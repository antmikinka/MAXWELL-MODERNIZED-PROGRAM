# Checklist: Maxwell Article Traceability

## Purpose

Ensure every physics implementation is traceable to specific articles in Maxwell's Treatise. This maintains historical accuracy and provides authoritative reference.

## Review Information

| Field | Value |
|-------|-------|
| Component | {component_name} |
| Maxwell Part | {part} |
| Coverage | {article_range} |
| Reviewer | {reviewer_name} |
| Date | {date} |

## Citation Completeness

### Primary Citations
- [ ] Every function has @cite_article decorator
- [ ] All relevant articles are cited (not just one)
- [ ] Article numbers match standard Treatise pagination
- [ ] Part number is specified in citation

### Secondary References
- [ ] Related articles mentioned in docstrings
- [ ] Cross-references to other implementations
- [ ] Links to architecture documents

## Article Coverage by Part

### Part I: Electrostatics (Arts. 27-229)

| Article Range | Topic | Implementation | Verified |
|---------------|-------|----------------|----------|
| 27-40 | Charge and measurement | {module} | [ ] |
| 41-49 | Electric field and potential | {module} | [ ] |
| 50-62 | Dielectrics and displacement | {module} | [ ] |
| 63-83 | Mathematical foundations | {module} | [ ] |
| 84-94 | Multi-conductor systems | {module} | [ ] |
| 95-103 | Green's theorem and energy | {module} | [ ] |
| 104-116 | Stress and equilibrium | {module} | [ ] |
| 117-123 | Visualization | {module} | [ ] |
| 124-127 | Standard components | {module} | [ ] |
| 128-146 | Spherical harmonics | {module} | [ ] |
| 147-154 | Ellipsoidal coordinates | {module} | [ ] |
| 155-181 | Image methods | {module} | [ ] |
| 182-206 | 2D field theory | {module} | [ ] |
| 207-229 | Instrumentation | {module} | [ ] |

### Part II: Electrokinematics (Arts. 230-370)

| Article Range | Topic | Implementation | Verified |
|---------------|-------|----------------|----------|
| 230-240 | Electric current | {module} | [ ] |
| 241-245 | Ohm's law and Joule heating | {module} | [ ] |
| 246-248 | Contact EMF | {module} | [ ] |
| 249-254 | Thermoelectric effects | {module} | [ ] |
| 255-268 | Electrolysis | {module} | [ ] |
| 269-286 | Current flow in 3D | {module} | [ ] |
| 287-296 | Material conductivity | {module} | [ ] |
| 297-300 | Telegraph equation | {module} | [ ] |
| 301-320 | Network theory | {module} | [ ] |
| 321-350 | Measurement methods | {module} | [ ] |
| 351-370 | Standards and calibration | {module} | [ ] |

### Part III: Magnetism (Arts. 371-474)

| Article Range | Topic | Implementation | Verified |
|---------------|-------|----------------|----------|
| 371-384 | Magnetic fundamentals | {module} | [ ] |
| 385-392 | Dipole interactions | {module} | [ ] |
| 393-400 | Field definitions | {module} | [ ] |
| 401-406 | Vector potential | {module} | [ ] |
| 407-411 | Solenoids and shells | {module} | [ ] |
| 412-423 | Field decomposition | {module} | [ ] |
| 424-428 | Induced magnetization | {module} | [ ] |
| 429-440 | Shape-dependent effects | {module} | [ ] |
| 441-448 | Material magnetism | {module} | [ ] |
| 449-464 | Measurement instruments | {module} | [ ] |
| 465-474 | Terrestrial magnetism | {module} | [ ] |

### Part IV: Electromagnetism (Arts. 475-866)

| Article Range | Topic | Implementation | Verified |
|---------------|-------|----------------|----------|
| 475-497 | Oersted-Ampère discoveries | {module} | [ ] |
| 498-520 | Ampère's force law | {module} | [ ] |
| 521-545 | Induction (Faraday) | {module} | [ ] |
| 546-570 | Self and mutual inductance | {module} | [ ] |
| 571-600 | Dynamical theory | {module} | [ ] |
| 601-619 | General field equations | {module} | [ ] |
| 620-650 | Energy and stress | {module} | [ ] |
| 651-700 | Detailed solutions | {module} | [ ] |
| 701-750 | Instrumentation | {module} | [ ] |
| 751-780 | Absolute measurements | {module} | [ ] |
| 781-805 | Electromagnetic waves | {module} | [ ] |
| 806-831 | Magneto-optics | {module} | [ ] |
| 832-866 | Molecular vortices | {module} | [ ] |

## Theory Classification

For each implementation, verify classification:

### Maxwell's Original Formulation
- [ ] Matches Maxwell's mathematical formulation
- [ ] Uses Maxwell's notation where preserved
- [ ] Follows Maxwell's reasoning

### User's Original Theoretical Extensions
- [ ] Clearly marked as "User Original Theory"
- [ ] Treated as authoritative (NOT TO BE CHANGED)
- [ ] Distinguished from Maxwell's text
- [ ] Documentation explains extension

### Standard Mathematical Implementation
- [ ] Uses established mathematical methods
- [ ] Vector calculus, tensor operations
- [ ] Numerical methods (FDTD, FEM)
- [ ] Clearly marked as standard

## Citation Format Verification

- [ ] Format: "Maxwell Article {number}" or "Art. {number}"
- [ ] Part specified: Part I, II, III, or IV
- [ ] Volume mapping correct (Vol. 1: Arts. 1-229, Vol. 2: 230-474, Vol. 3: 475-866)
- [ ] Cross-references use same format

## Documentation Quality

- [ ] Docstrings include article citations
- [ ] Examples reference relevant articles
- [ ] "Maxwell's Treatment" sections accurate
- [ ] Historical notes are correct

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Maxwell Scholar | | | |
| Implementation | | | |
| QA | | | |

## Missing Citations

| Function/Module | Missing Articles | Priority | Status |
|-----------------|------------------|----------|--------|
| {function} | {articles} | {HIGH|MEDIUM|LOW} | {OPEN|RESOLVED} |

## Overall Assessment

**Citation Coverage:** {COMPLETE | MOSTLY_COMPLETE | PARTIAL | INADEQUATE}

**Accuracy:** {EXCELLENT | GOOD | NEEDS_CORRECTION | POOR}

**Recommendation:** {APPROVE | APPROVE_WITH_CHANGES | REJECT}

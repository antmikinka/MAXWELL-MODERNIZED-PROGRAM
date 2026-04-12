# Data: maxwell-article-mapping-documentation

## Purpose

Comprehensive mapping of Maxwell's treatise articles to documentation topics and requirements.

---

## Documentation Topics by Article Range

### Part I: Electrostatics (Art. 1-229)

| Article Range | Topic | Documentation Type | Required Components |
|---------------|-------|-------------------|---------------------|
| Art. 1-20 | Fundamental concepts | Reference | CGS units, definitions |
| Art. 21-43 | Electric field theory | Reference, Tutorial | Field equations, examples |
| Art. 44-49 | Electric potential | API, Reference | Electrometer APIs |
| Art. 50-62 | Dielectrics | Reference | Material properties |
| Art. 63-74 | Induction | Reference, Tutorial | Induction examples |
| Art. 75-76 | Capacitance | API, Reference | Capacity APIs |
| Art. 77-150 | Field configurations | Reference | Field solutions |
| Art. 151-229 | Potential theory | Reference, Tutorial | Mathematical methods |

### Part II: Electrokinematics (Art. 230-370)

| Article Range | Topic | Documentation Type | Required Components |
|---------------|-------|-------------------|---------------------|
| Art. 230-250 | Current theory | Reference | Current definitions |
| Art. 251-286 | Conduction | Reference, API | Conduction models |
| Art. 287-300 | Networks | API, Tutorial | Circuit analysis |
| Art. 301-320 | Resistance theory | Reference | Resistance models |
| Art. 321-342 | Resistance measurement | API, Tutorial | Ohmmeter methods |
| Art. 343-348 | Wheatstone bridge | API, Tutorial | Bridge APIs |
| Art. 349-370 | Network theory | Reference | Advanced networks |

### Part III: Magnetism (Art. 371-474)

| Article Range | Topic | Documentation Type | Required Components |
|---------------|-------|-------------------|---------------------|
| Art. 371-380 | Magnetic poles | Reference | Magnetic theory |
| Art. 381-400 | Magnetic force | Reference, API | Force calculations |
| Art. 401-423 | Magnetic field | Reference | Field theory |
| Art. 424-440 | Magnetic induction | API, Reference | B = H + 4πI |
| Art. 441-448 | Magnetic properties | Reference | Material properties |
| Art. 449-474 | Magnetic measurements | API, Tutorial | Magnetometer methods |

### Part IV: Electromagnetism (Art. 475-866)

| Article Range | Topic | Documentation Type | Required Components |
|---------------|-------|-------------------|---------------------|
| Art. 475-500 | Electromagnetic force | API, Reference | Force calculations |
| Art. 501-520 | Ampère's law | Reference, Tutorial | Current-field relation |
| Art. 521-540 | Induction | API, Reference | Induction models |
| Art. 541-600 | Mutual inductance | Reference, API | Coupled circuits |
| Art. 601-700 | Electromagnetic waves | Reference | Wave theory |
| Art. 701-729 | Field theory | Reference | Advanced fields |
| Art. 730-750 | Galvanometers | API, Tutorial, Reference | Complete galvanometer docs |
| Art. 751-770 | EM measurements | API, Tutorial | Measurement methods |
| Art. 771-780 | Instrument calibration | API, Checklist | Calibration procedures |
| Art. 781-866 | Light and EM theory | Reference | Electromagnetic theory of light |

---

## Documentation Requirements by Topic

### Galvanometer Documentation (Art. 730-750)

| Component | Type | Description |
|-----------|------|-------------|
| galvanometer-model | Command | Galvanometer modeling |
| galvanometer-design | Task | Design workflow |
| galvanometer-design-template | Template | Design template |
| instrument-validation | Checklist | Validation criteria |
| instrument-reference | Data | Reference parameters |

### Magnetometer Documentation (Art. 449-474)

| Component | Type | Description |
|-----------|------|-------------|
| magnetometer-model | Command | Magnetometer modeling |
| magnetometer-calibration | Task | Calibration workflow |
| magnetometer-calibration-template | Template | Calibration template |
| calibration-procedure-validation | Checklist | Validation criteria |
| instrument-reference | Data | Reference parameters |

### Electrometer Documentation (Art. 44-49, Art. 230-235)

| Component | Type | Description |
|-----------|------|-------------|
| electrometer-model | Command | Electrometer modeling |
| electrometer-sensitivity-optimization | Task | Sensitivity workflow |
| electrometer-modeling-template | Template | Modeling template |
| instrument-validation | Checklist | Validation criteria |
| instrument-reference | Data | Reference parameters |

### Bridge Circuit Documentation (Art. 343-348)

| Component | Type | Description |
|-----------|------|-------------|
| bridge-instrument | Command | Bridge analysis |
| bridge-analysis | Task | Bridge workflow |
| bridge-analysis-template | Template | Analysis template |
| bridge-measurement-validation | Checklist | Validation criteria |
| bridge-circuits-reference | Data | Reference data |

### Circuit Analysis Documentation (Art. 287-300)

| Component | Type | Description |
|-----------|------|-------------|
| circuit-analysis | Command | Circuit analysis |
| circuit-analysis | Task | Analysis workflow |
| circuit-analysis-template | Template | Analysis template |
| circuit-analysis-validation | Checklist | Validation criteria |
| circuit-analysis-reference | Data | Reference data |

---

## Documentation Coverage Matrix

### Coverage by Part

| Part | Articles | Documented | Coverage % |
|------|----------|------------|------------|
| I: Electrostatics | 1-229 | {{COUNT}} | {{PCT}}% |
| II: Electrokinematics | 230-370 | {{COUNT}} | {{PCT}}% |
| III: Magnetism | 371-474 | {{COUNT}} | {{PCT}}% |
| IV: Electromagnetism | 475-866 | {{COUNT}} | {{PCT}}% |
| **TOTAL** | **1-866** | **{{COUNT}}** | **{{PCT}}%** |

### Coverage by Documentation Type

| Type | Count | Description |
|------|-------|-------------|
| API Documentation | {{COUNT}} | API reference docs |
| Tutorials | {{COUNT}} | How-to guides |
| Reference | {{COUNT}} | Reference material |
| Templates | {{COUNT}} | Document templates |
| Checklists | {{COUNT}} | Validation checklists |
| Data Files | {{COUNT}} | Reference data |

---

## Cross-Reference by Agent

### MATERIA Agent

| Maxwell Articles | Component | Documentation |
|------------------|-----------|---------------|
| Art. 50-62 | Dielectric response | dielectric-response-template |
| Art. 424-440 | Magnetic materials | magnetic-materials-reference |
| Art. 441-448 | Hysteresis | hysteresis-model-template |

### CIRCUITUS Agent

| Maxwell Articles | Component | Documentation |
|------------------|-----------|---------------|
| Art. 287-300 | Network analysis | circuit-analysis-template |
| Art. 343-348 | Bridge circuits | bridge-analysis-template |
| Art. 730-750 | Instrument circuits | transmission-line-template |

### INSTRUMENTUM Agent

| Maxwell Articles | Component | Documentation |
|------------------|-----------|---------------|
| Art. 44-49 | Electrometer theory | electrometer-modeling-template |
| Art. 449-474 | Magnetometer methods | magnetometer-calibration-template |
| Art. 730-750 | Galvanometer design | galvanometer-design-template |

### SCRIBA Agent

| Maxwell Articles | Component | Documentation |
|------------------|-----------|---------------|
| All articles | Citation guide | maxwell-article-citation-style-guide |
| All articles | Documentation standards | documentation-standards-guide |
| All articles | Article mapping | maxwell-article-mapping-documentation |

---

## Citation Requirements

### Minimum Citation Requirements

| Documentation Type | Citation Requirement |
|-------------------|---------------------|
| API Reference | Cite relevant articles |
| Tutorial | Cite foundational articles |
| Reference | Comprehensive article coverage |
| Template | Article range in frontmatter |
| Checklist | Article validation criteria |
| Data File | Article source attribution |

### Citation Format by Type

**In-text:**
```
Maxwell (1873, Art. 730-750)
```

**Frontmatter:**
```yaml
maxwell_articles: "Art. 730-750"
```

**Reference list:**
```
Maxwell, J.C. (1873). Art. 730-750: Galvanometry.
```

---

## CGS Unit Requirements by Article

### Articles Requiring CGS Units

| Article Range | Primary CGS Units |
|---------------|-------------------|
| Art. 1-229 | statC, statV, statΩ |
| Art. 230-370 | statA, statV, statΩ |
| Art. 371-474 | G, Oe, emu |
| Art. 475-866 | Mixed Gaussian |

### Physical Constants by Topic

| Topic | Constants Required |
|-------|-------------------|
| Electrostatics | e, ε_0 (CGS) |
| Magnetism | μ_0 (CGS) |
| Electromagnetism | c, e, k_B |
| Instruments | k_B, e, c |

---

## Quality Criteria

- [ ] All article ranges mapped to documentation
- [ ] Coverage tracked by part and topic
- [ ] Cross-reference by agent complete
- [ ] Citation requirements defined
- [ ] CGS unit requirements specified

# Command: review-layer-mapping

## Description

Reviews and validates the layer numbering scheme across all 6 Parts of Maxwell's Treatise. This command ensures layer numbers are sequential, non-overlapping, and properly documented, maintaining the architectural integrity of the layered system.

## Usage

```bash
architectus review-layer-mapping [OPTIONS]

Options:
  --part <PART>           Review layers for specific part only
  --layer <LAYER>         Review specific layer details
  --check-gaps            Check for layer numbering gaps
  --check-conflicts       Check for layer conflicts between parts
  --visualize             Generate layer visualization
  --output <FORMAT>       Output format: text, json, markdown, diagram (default: text)
  --report <PATH>         Write review report to file
```

## Input

- **Architecture COMPLETE Documents**: All 6 Part architecture maps
- **Layer Numbering Scheme Reference**: Official layer assignments
- **Module Registry**: Layer-to-module mappings

## Layer Numbering Scheme

### Official Layer Allocation

| Layer Range | Part | Domain | Module Count |
|-------------|------|--------|--------------|
| 0-12 | Part I | Electrostatics | ~50 |
| 13-30 | Part II | Electrokinematics | ~50 |
| 30b-42 | Part III | Magnetism | ~45 |
| 43-86 | Part IV | Electromagnetism | ~120 |
| 90-94 | Part V | System Core | ~25 |
| 95-97 | Part VI | Scalar Physics | ~30 |

### Layer Structure Within Parts

Each part follows a consistent layer pattern:

```
Layer 0:  Units, Configuration (Foundation)
Layer 1-N: Core primitives and definitions
Layer N+1: Basic physics engine
Layer N+2: System management
Layer N+3: Advanced solvers
Layer N+4: Field analysis
Layer N+5: Visualization
Layer N+6: Component library
Layer N+7: Mathematics kernel
Layer N+8: Instrumentation
Layer N+9: Verification tests
```

## Validation Checks

### 1. Layer Gap Detection

- [ ] No gaps in layer numbering within parts
- [ ] Intentional gaps between parts are documented
- [ ] Layer 30-30b transition is valid (Part II to III)
- [ ] Layer 86-90 gap is documented (Part IV to V)

### 2. Layer Conflict Detection

- [ ] No layer number assigned to multiple parts
- [ ] Layer boundaries are clearly defined
- [ ] Cross-part layer references use correct numbering

### 3. Layer Content Validation

- [ ] Each layer has documented purpose
- [ ] Layer modules are cohesive
- [ ] Layer dependencies are acyclic
- [ ] Layer naming is consistent

## Output

### Summary Output

```
Layer Mapping Review
====================

Part I: Electrostatics
  Layer Range: 0-12 (13 layers)
  Modules: 52
  Gaps: None
  Status: VALID

Part II: Electrokinematics
  Layer Range: 13-30 (18 layers)
  Modules: 48
  Gaps: None
  Status: VALID

Part III: Magnetism
  Layer Range: 30b-42 (13 layers)
  Modules: 45
  Gaps: None
  Status: VALID

Part IV: Electromagnetism
  Layer Range: 43-86 (44 layers)
  Modules: 118
  Gaps: None
  Status: VALID

Part V: System Core
  Layer Range: 90-94 (5 layers)
  Modules: 22
  Intentional Gap: 87-89 (reserved for future expansion)
  Status: VALID

Part VI: Scalar Physics
  Layer Range: 95-97 (3 layers)
  Modules: 28
  Status: VALID

OVERALL STATUS: VALIDATED
Total Layers: 98 (0-97)
Total Modules: 313
Layer Gaps: 0 (3 intentional)
Layer Conflicts: 0
```

### Layer Detail Output

```
Layer 8: Spherical Harmonics Math Kernel
========================================

Part: I (Electrostatics)
Purpose: Advanced mathematical basis functions for spherical boundary problems
Source: Chapter IX, Arts. 128-146
Modules:
  - maxwell/math/spherical/foundations.py
  - maxwell/math/spherical/harmonics.py
  - maxwell/math/spherical/shell.py
  - maxwell/math/spherical/expansion.py
  - maxwell/math/spherical/orthogonality.py
  - maxwell/math/spherical/trigonometric.py
  - maxwell/math/spherical/zonal.py
  - maxwell/math/spherical/conjugate.py
  - maxwell/math/spherical/standard.py
  - maxwell/math/spherical/biaxal.py
  - maxwell/math/spherical/tesseral.py

Dependencies:
  - Layer 0: Configuration
  - Layer 2: Potential theory

Dependents:
  - Layer 10: Image method solvers
  - Layer 4: Advanced solvers
```

### Visualization Output (Diagram)

```
Layer Architecture Diagram
==========================

  Part I        Part II       Part III      Part IV       Part V        Part VI
  ======        =======       ========      =======       ======        =======
  [0-12]        [13-30]       [30b-42]      [43-86]       [90-94]       [95-97]
  
  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
  │ Layer  │    │ Layer  │    │ Layer  │    │ Layer  │    │ Layer  │    │ Layer  │
  │ 12     │    │ 30     │    │ 42     │    │ 86     │    │ 94     │    │ 97     │
  │  ...   │    │  ...   │    │  ...   │    │  ...   │    │  ...   │    │  ...   │
  │ 0      │───▶│ 13     │───▶│ 30b    │───▶│ 43     │───▶│ 90     │───▶│ 95     │
  └────────┘    └────────┘    └────────┘    └────────┘    └────────┘    └────────┘
      │             │             │             │             │             │
      ▼             ▼             ▼             ▼             ▼             ▼
  Electro-      Electro-      Magnetism     Electro-      System        Scalar
  statics       kinematics                    magnetism     Core          Physics
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Layer mapping validated, no issues |
| 1 | Layer gaps detected |
| 2 | Layer conflicts detected |
| 3 | Configuration error (missing files) |

## Examples

```bash
# Full layer review
architectus review-layer-mapping

# Review specific part
architectus review-layer-mapping --part IV

# Review specific layer
architectus review-layer-mapping --layer 8

# Check for gaps only
architectus review-layer-mapping --check-gaps

# Generate visualization
architectus review-layer-mapping --visualize --output layer_diagram.md

# JSON report
architectus review-layer-mapping --output json --report layers.json
```

## Related Commands

- `validate-architecture` - Overall architecture validation
- `check-dependencies` - Dependency chain verification
- `generate-master-index` - Master index generation

## Implementation Notes

This command:
1. Parses all architecture COMPLETE documents
2. Extracts layer numbering from each part
3. Validates layer ranges and boundaries
4. Detects gaps and conflicts
5. Generates layer dependency graphs
6. Creates visual layer architecture diagrams

## Intentional Gaps

Some layer gaps are intentional and documented:

| Gap | Reason |
|-----|--------|
| 30-30b | Transition from Part II (integer) to Part III (lettered) |
| 87-89 | Reserved for Part IV expansion |
| 88-89 | Reserved for future electromagnetic layers |

## Layer Naming Conventions

Layers follow consistent naming:

```
Layer N: [Domain] [Purpose]

Examples:
  Layer 0: Units, Dimensions & Configuration
  Layer 8: Spherical Harmonics Math Kernel
  Layer 10: Image Method Solvers
  Layer 12: Instrumentation & Metrology
```

## Layer Documentation Requirements

Each layer must document:
1. Layer number and range
2. Purpose and goals
3. Source articles (Maxwell reference)
4. Module list
5. Dependencies on other layers
6. Dependents (layers that depend on this)

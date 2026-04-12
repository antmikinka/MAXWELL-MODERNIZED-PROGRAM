# Data: Agent Domain Boundaries

## Description

Defines which specialist agent owns which modules and domains across the Maxwell Treatise modernization. This document establishes clear agent responsibility boundaries.

---

## Agent Overview

| Agent | Domain | Layer Responsibility | Article Coverage |
|-------|--------|---------------------|------------------|
| MATHEMATICA | Mathematical Foundations | 0, 8, 9, 11 | Supporting all parts |
| PHYSICUS | Physics Implementation | 1-7, 13-42 | Parts I, II, III |
| QUALITAS | Quality Assurance | All layers | All parts |
| SCRIBA | Documentation | All layers | All parts |
| ARCHITECTUS | Architecture Management | All layers | All parts |
| CIRCUITUS | Circuit Analysis | 20-27 | Part II |
| MATERIA | Material Physics | 24-29, 35-38 | Parts II, III |
| INSTRUMENTUM | Instrumentation | 12, 27-28, 40 | Parts I, II, III |

---

## MATHEMATICA Agent

**Domain:** Mathematical Foundations

**Primary Layers:**
- Layer 0: Units, Configuration (math components)
- Layer 8: Spherical Harmonics Math Kernel
- Layer 9: Ellipsoidal Coordinates
- Layer 11: 2D Complex Analysis

**Module Ownership:**
```
maxwell/math/
├── spherical/
│   ├── foundations.py
│   ├── harmonics.py
│   ├── shell.py
│   ├── expansion.py
│   ├── orthogonality.py
│   ├── trigonometric.py
│   ├── zonal.py
│   ├── conjugate.py
│   ├── standard.py
│   ├── biaxal.py
│   └── tesseral.py
├── ellipsoidal/
│   ├── coordinates.py
│   ├── laplacian.py
│   ├── solutions.py
│   ├── transforms.py
│   └── paraboloids.py
├── complex/
│   ├── two_dim.py
│   ├── conjugate.py
│   ├── inversion_2d.py
│   └── neumann.py
└── transformations/
    └── inversion.py
```

**Commands:**
- `vector-calculus-ops` — Implement vector field operations
- `spherical-harmonics` — Compute and expand spherical harmonics
- `solid-angle-calc` — Calculate solid angles for surfaces
- `quaternion-algebra` — Quaternion operations
- `tensor-ops` — Tensor manipulations
- `potential-theory` — Solve potential equations
- `validate-math` — Mathematical verification

**Boundaries:**
- Provides mathematical foundations to all agents
- Does not implement physics (PHYSICUS domain)
- Does not implement solvers (shared with PHYSICUS)

---

## PHYSICUS Agent

**Domain:** Physics Implementation

**Primary Layers:**
- Layer 1: Core Primitives
- Layer 2: Basic Physics Engine
- Layer 3: System Manager
- Layer 4: Advanced Solvers
- Layer 5: Field Analysis
- Layer 6: Visualization

**Module Ownership:**
```
maxwell/core/
├── charge.py
├── fields.py
├── materials.py
├── measurement.py
├── polarization.py
└── units.py

maxwell/physics/
├── definitions.py
├── density.py
├── forces.py
├── potential.py
├── integrals.py
├── poisson.py
├── boundary.py
├── surface_forces.py
├── induction.py
└── dielectrics.py

maxwell/systems/
├── superposition.py
├── energy.py
├── reciprocity.py
├── coefficients.py
├── constraints.py
├── approximation.py
├── analysis.py
├── forces.py
└── comparison.py

maxwell/solvers/
├── methodology.py
├── greens.py
├── energy_integrals.py
├── uniqueness.py
├── thomson.py
├── anisotropic.py
├── bounds.py
├── edges.py
├── spherical_conductor.py
└── images/

maxwell/analysis/
├── stress.py
└── stability.py

maxwell/vis/
├── contours.py
├── field_lines.py
└── spherical_harmonics.py
```

**Commands:**
- `electrostatic-field` — Compute electrostatic fields
- `dielectric-response` — Model dielectric materials
- `current-flow` — Analyze current distribution
- `electrolysis-model` — Model electrolytic processes
- `magnetic-field` — Compute magnetic fields
- `magnetization-model` — Model magnetization
- `em-coupling` — Electromagnetic coupling
- `maxwell-equations` — Maxwell's equations solver
- `wave-propagation` — Wave propagation analysis

**Boundaries:**
- Owns all physics implementations
- Receives mathematical foundations from MATHEMATICA
- Provides validated physics to QUALITAS for testing
- Provides implementations to SCRIBA for documentation

---

## QUALITAS Agent

**Domain:** Quality Assurance and Validation

**Primary Layers:** All layers (validation focus)

**Module Ownership:**
```
maxwell/tests/
├── verification/
│   ├── verify_force_law.py
│   ├── verify_cavendish.py
│   ├── verify_poisson.py
│   ├── verify_images.py
│   └── verify_earnshaw.py
├── unit/
├── integration/
└── performance/
```

**Commands:**
- `validate-physics` — Physics correctness validation
- `check-units` — Unit consistency audit
- `verify-conservation` — Conservation law verification
- `test-analytical` — Analytical solution comparison
- `integration-test` — Integration test execution
- `convergence-study` — Numerical convergence analysis
- `audit-citations` — Citation compliance audit
- `benchmark-performance` — Performance benchmarking

**Boundaries:**
- Validates all agent implementations
- Does not implement production code
- Owns all test infrastructure
- Sets quality gates for pipeline

---

## SCRIBA Agent

**Domain:** Documentation and Technical Writing

**Primary Layers:** All layers (documentation focus)

**Module Ownership:**
```
maxwell/docs/
├── api/
├── tutorials/
├── theory/
│   ├── maxwell_plan.md
│   ├── maxwell_theory.md
│   └── stress_discussion.md
└── user/
```

**Commands:**
- `generate-docs` — Documentation generation
- `write-api-reference` — API documentation
- `create-tutorial` — Tutorial creation
- `track-citations` — Citation tracking
- `update-changelog` — Changelog management

**Boundaries:**
- Documents all agent implementations
- Does not implement production code
- Owns all user-facing documentation
- Manages citation tracking

---

## ARCHITECTUS Agent

**Domain:** Architecture Management and Orchestration

**Primary Layers:** All layers (architecture focus)

**Module Ownership:**
```
agents/architectus/
├── agent.md
├── commands/
│   ├── validate-architecture.md
│   ├── audit-coverage.md
│   ├── check-dependencies.md
│   ├── generate-master-index.md
│   ├── review-layer-mapping.md
│   ├── sync-agents.md
│   └── pipeline-orchestrate.md
├── tasks/
├── templates/
├── checklists/
├── data/
└── utils/
```

**Commands:**
- `validate-architecture` — Architecture validation
- `audit-coverage` — Coverage auditing
- `check-dependencies` — Dependency verification
- `generate-master-index` — Master index generation
- `review-layer-mapping` — Layer mapping review
- `sync-agents` — Agent synchronization
- `pipeline-orchestrate` — Pipeline orchestration

**Boundaries:**
- Manages architecture for all agents
- Does not implement physics or math
- Owns architecture documents
- Coordinates pipeline execution

---

## CIRCUITUS Agent

**Domain:** Circuit Analysis and Network Theory

**Primary Layers:**
- Layer 20: Network Theory
- Layer 21-27: Circuit analysis

**Module Ownership:**
```
maxwell/circuits/
├── topology.py
├── network.py
└── components/
```

**Boundaries:**
- Owns circuit simulation
- Receives component models from PHYSICUS
- Provides circuit analysis to system

---

## MATERIA Agent

**Domain:** Material Physics

**Primary Layers:**
- Layer 24-29: Material databases
- Layer 35-38: Magnetic materials

**Module Ownership:**
```
maxwell/materials/
├── database/
│   ├── metals.py
│   ├── liquids.py
│   ├── insulators.py
│   └── gases.py
├── contact.py
├── electrolytes.py
├── composites.py
├── stratified.py
└── leakage.py
```

**Boundaries:**
- Owns material property databases
- Provides material models to PHYSICUS

---

## INSTRUMENTUM Agent

**Domain:** Instrumentation and Metrology

**Primary Layers:**
- Layer 12: Part I Instrumentation
- Layer 27-28: Part II Measurement
- Layer 40: Part III Measurements

**Module Ownership:**
```
maxwell/instruments/
├── detectors.py
├── generators/
├── meters/
└── standards/
```

**Boundaries:**
- Owns instrument models
- Provides measurement capabilities

---

## Inter-Agent Collaboration

### MATHEMATICA → PHYSICUS

**Interface:** Mathematical foundations
**Data Flow:** Functions, operators, special functions
**Protocol:** Import from `maxwell/math/*`

### PHYSICUS → QUALITAS

**Interface:** Physics implementations
**Data Flow:** Modules for validation
**Protocol:** Test discovery and execution

### PHYSICUS → SCRIBA

**Interface:** Implementation details
**Data Flow:** Docstrings, examples
**Protocol:** Documentation extraction

### ARCHITECTUS → All Agents

**Interface:** Architecture updates
**Data Flow:** Architecture documents, sync notifications
**Protocol:** Agent synchronization command

---

## Conflict Resolution

### Overlapping Domains

| Agents | Overlap | Resolution |
|--------|---------|------------|
| MATHEMATICA/PHYSICUS | Layer 0 math | MATHEMATICA implements, PHYSICUS uses |
| PHYSICUS/CIRCUITUS | Circuit physics | PHYSICUS provides models, CIRCUITUS implements circuits |
| PHYSICUS/MATERIA | Material physics | MATERIA provides data, PHYSICUS implements physics |

### Escalation Path

1. Agent-to-agent negotiation
2. ARCHITECTUS mediation
3. Human architect review

---

**END OF DOCUMENT**

# Maxwell Modernized

[![Tests](https://github.com/antmikinka/MAXWELL-MODERNIZED-PROGRAM/actions/workflows/test.yml/badge.svg)](https://github.com/antmikinka/MAXWELL-MODERNIZED-PROGRAM/actions/workflows/test.yml)
[![Math Verification](https://github.com/antmikinka/MAXWELL-MODERNIZED-PROGRAM/actions/workflows/math-verification.yml/badge.svg)](https://github.com/antmikinka/MAXWELL-MODERNIZED-PROGRAM/actions/workflows/math-verification.yml)
[![Coverage](https://img.shields.io/badge/coverage-866%2F866%20articles-brightgreen)](docs/COVERAGE_SUMMARY.md)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE-CONTENT)

> A computational implementation of James Clerk Maxwell's 1873 _A Treatise on Electricity and Magnetism_ -- all 866 articles, modernized in Python.

## What This Is

In 1873, James Clerk Maxwell published _A Treatise on Electricity and Magnetism_, the definitive work that unified electricity, magnetism, and light into a single theoretical framework. This project is a complete computational re-implementation of that Treatise -- every one of its 866 articles translated into modern, executable Python.

**100% coverage** means the entire work is represented: from the elementary definitions of charge and force in Part I through the electromagnetic theory of light in Part IV, including the supplementary chapters on molecular theory, optics, and the philosophy of the electromagnetic field. Every function is traceable to its source article. Every result is computationally reproducible.

The project serves two audiences:

- **Scholars and historians** who want to explore Maxwell's theory as executable mathematics rather than prose alone
- **Developers and physicists** who need a verified, well-tested implementation of classical electromagnetic theory

## Quick Start

### Installation

From PyPI (recommended):

```bash
pip install maxwell           # Core library
pip install maxwell[viz]      # With visualization support
pip install maxwell[dev]      # With development tools
pip install maxwell[accel]    # With JAX GPU/TPU acceleration
pip install maxwell[all]      # Everything
```

From source:

```bash
git clone https://github.com/antmikinka/MAXWELL-MODERNIZED-PROGRAM.git
cd MAXWELL-MODERNIZED-PROGRAM
pip install -e ".[dev,viz]"
```

### Your First Calculation

```python
from maxwell.config.constants import C, CONST
from maxwell.core.units import MagneticDimensions, verify_speed_of_light_relationship
from maxwell.math.vector_operators import gradient, divergence, curl
from maxwell.core.field import gauss_law_closed_surface

# The speed of light emerges from Maxwell's electromagnetic theory (Art. 782)
print(f"c = {C:.4e} cm/s")  # 2.9979e+10

# Verify the EM/ESU unit ratio equals c (Arts. 771-781)
ratio = verify_speed_of_light_relationship()
print(f"Unit ratio / c = {ratio}")  # 1.0

# Compute the gradient of a potential -- Art. 72
potential_field = lambda x, y, z: 1.0 / (x**2 + y**2 + z**2)**0.5
E_field = gradient(potential_field)
```

### Run the Test Suite

```bash
pytest tests/ -v
# 1795 passed in <N> seconds
```

## What Can I Use This For?

A detailed practical guide is available at **[docs/USE_CASES.md](docs/USE_CASES.md)**. Briefly, this library supports:

- **Electromagnetic calculations** -- Coulomb fields, Lorentz forces, Faraday induction, Oersted fields, Maxwell stress tensors
- **Education** -- executable examples tied to primary-source articles for teaching classical EM theory
- **Scientific research** -- computational exploration of 19th-century electromagnetic theory and competing formulations (Maxwell, Weber, Neumann, Ampere)
- **Engineering reference** -- back-of-envelope calculations for magnetic fields, forces, inductance, hysteresis, and compass deviation
- **Unit system verification** -- dimensional analysis, ESU/EMU/CGS/SI conversions, speed-of-light relationship checks

See [USE_CASES.md](docs/USE_CASES.md) for 20+ concrete code examples, limitations, target audiences, and a quick-reference table mapping common problems to modules.

## Project Structure

The codebase mirrors the Treatise's four-part structure.

| Part | Scope | Articles | Package |
|------|-------|----------|---------|
| **I** | Electrostatics | 1-206 | `maxwell/electrostatics/` |
| **II** | Electrokinematics | 230-370 | `maxwell/electrokinematics/` |
| **III** | Magnetism | 371-474 | `maxwell/magnetism/` |
| **IV** | Electromagnetism | 475-866 | `maxwell/electromagnetism/` |

The **core** package (`maxwell/core/`) provides shared abstractions -- `Charge`, `Field`, `Potential`, `Magnet` -- used across all Parts. Supplementary domains (optics, molecular theory, instrumentation, signal processing) live in their own top-level packages.

For the full module-level breakdown, see [docs/API_REFERENCE.md](docs/API_REFERENCE.md).

## Key Features

### CGS-EMU Unit System

The codebase uses the centimeter-gram-second electromagnetic unit system throughout -- the system Maxwell himself employed. All constants, dimensions, and conversions are defined in `maxwell/config/constants.py` and `maxwell/core/units/`. ESU equivalents and SI reference values are available for cross-checking.

### Citation-Based Traceability

Every function carries a `@maxwell_cite` decorator that links it to Maxwell's original article numbers:

```python
from maxwell.meta.citation import maxwell_cite

@maxwell_cite(528, 529, 530, part=4, chapter="Electromagnetic Induction")
def faraday_induction(circuit, d_flux_dt):
    """Induced EMF from time-varying magnetic flux (Arts. 528-530)."""
    return -d_flux_dt
```

Query citations programmatically or search the codebase by article number:

```python
from maxwell.meta.citation import get_citation, get_all_citations

citation = get_citation(faraday_induction)
print(citation)  # MaxwellCitation(Part 4, Art. 528, Art. 529, Art. 530)
```

### Scope

| Metric | Count |
|--------|-------|
| Articles covered | 866 / 866 (100%) |
| Python modules | 290+ |
| Functions | 2,900+ |
| Classes | 290+ |
| Tests | 1795 / 1795 passing |
| Math validations | 50 / 50 passing |
| SymPy verifiers | 66 / 66 passing |
| JAX adapters | 20+ |
| Visualization modules | 15 (15 visualizations) |

### Validation

- 1795/1795 tests passing (629 core + 847 JAX + 66 SymPy + 232 visualization + 21 dynamics)
- 50/50 mathematical validation checks pass (dimensional analysis, vector calculus, spherical harmonics, elliptic integrals, differential equations, integral transforms)
- 100% citation compliance -- every public function is linked to its source article
- All 260+ modules import without errors

### Lagrangian Kernel (Layer 52)

The `maxwell.dynamics.lagrangian` package provides a JAX-powered Lagrangian mechanics framework:

- **`GeneralizedSystem`** -- dataclass representing a system in generalized coordinates (q, p state)
- **Force-from-energy derivation** -- forces computed via `jax.grad` of potential/kinetic energy
- **Proof of concept** -- `derive_electrostatic_force()` derives Coulomb force from U = q1*q2/r via auto-diff

```python
from maxwell.dynamics.lagrangian import GeneralizedSystem, derive_electrostatic_force

# Derive Coulomb force from potential energy via JAX auto-diff
force = derive_electrostatic_force(q1=1.0, q2=1.0, r=1.0)  # Uses jax.grad internally
```

### JAX GPU/TPU Acceleration

The `maxwell.jax` package provides JAX-compatible implementations of core Maxwell calculations, enabling:

- **GPU/TPU execution** -- vectorized batch evaluation of fields, forces, and energies across thousands of points
- **Automatic differentiation** -- exact gradients via `jax.grad` for field derivatives and sensitivity analysis
- **JIT compilation** -- compiled kernels for repeated evaluation via `jax.jit`
- **CGS-EMU precision** -- 64-bit floats (`jax_enable_x64`) preserve unit consistency

20+ JAX adapters cover all four Parts of the Treatise: `PointChargeJAX`, `MagneticPoleJAX`, `MagnetJAX`, `VectorPotentialJAX`, `ElectricFieldJAX`, `FaradayInductionJAX`, `MaxwellEquationsJAX`, `SphericalHarmonicExpansionJAX`, `LorentzForceJAX`, `MaxwellStressTensorJAX`, `DisplacementCurrentJAX`, `AmpereMaxwellLawJAX`, `ElectrostaticEnergyJAX`, `CapacitorEnergyJAX`, `MagneticEnergyJAX`, `InductorEnergyJAX`, `ElectrokineticEnergyJAX`, `CoupledCircuitEnergyJAX`, `OhmsLawJAX`, `NetworkSolverJAX`, `Conduction3DJAX`, `FaradayLawsJAX`, `ElectrolysisCellJAX`, `JouleHeatingJAX`, and more.

```python
import jax
from maxwell.jax.core.charge import PointChargeJAX

charge = PointChargeJAX(q=1.0, position=jax.numpy.array([0.0, 0.0, 0.0]))

# Auto-differentiation: dV/dq at r=1
V_at = lambda q: PointChargeJAX(q=q, position=jax.numpy.zeros(3)).potential_at(
    jax.numpy.array([1.0, 0.0, 0.0])
)
dVdq = jax.grad(V_at)(1.0)  # = 1.0

# Batched field evaluation over 1000 points
points = jax.numpy.linspace(-10, 10, 1000).reshape(-1, 3)
E_batch = charge.field_at_batched(points)  # shape (1000, 3)
```

Install with `pip install maxwell[accel]` for the JAX runtime. See `maxwell/jax/README.md` for the complete adapter registry.

## Documentation

| Document | Contents |
|----------|----------|
| [docs/USE_CASES.md](docs/USE_CASES.md) | Practical guide: what you can do with this library, code examples, and quick reference |
| [docs/API_REFERENCE.md](docs/API_REFERENCE.md) | Module-by-module API index with function counts and article mappings |
| [docs/COVERAGE_SUMMARY.md](docs/COVERAGE_SUMMARY.md) | Article coverage by Part, chapter, and module |
| [docs/validation_report.md](docs/validation_report.md) | Test results, math validation, import verification |
| [maxwell/jax/README.md](maxwell/jax/README.md) | JAX GPU/TPU adapter documentation, auto-diff, JIT compilation |

The `archive/docs/` directory contains 24 legacy development documents (architecture maps, OCR audits, integration reports) preserved for historical reference.

## Citing This Work

If you use Maxwell Modernized in your research, please cite it using the
[CITATION.cff](CITATION.cff) file provided with this repository. You can
import the citation directly from GitHub or use the following BibTeX entry.
Cite the software (MIT) for the library; cite the paper manuscript (CC BY 4.0)
when you reuse the written analysis. Always cite Maxwell 1873 as the source work.

```bibtex
@software{maxwell_modernized_2026,
  title = {Maxwell Modernized},
  author = {Mikinka, Anthony},
  year = {2026},
  url = {https://github.com/antmikinka/MAXWELL-MODERNIZED-PROGRAM},
  description = {A complete computational implementation of Maxwell's 1873 Treatise}
}
```

The original Treatise should also be cited:

```bibtex
@book{maxwell1873,
  author = {Maxwell, James Clerk},
  title = {A Treatise on Electricity and Magnetism},
  publisher = {Clarendon Press},
  address = {Oxford},
  year = {1873}
}
```

## For Scholars

### Tracing Code to Articles

Every function in the codebase is linked to a specific article or group of articles in Maxwell's Treatise. To find what implements a given article:

```bash
# Search by article number
grep -r "@maxwell_cite.*528" maxwell/
```

Or use the citation module directly:

```python
from maxwell.meta.citation import get_all_citations

all_citations = get_all_citations()
for func_name, citation in all_citations.items():
    if 528 in citation.articles:
        print(f"{func_name} -> {citation}")
```

### Citation Methodology

Citations use three theory classifications:

- **`maxwell_original`** -- implementations derived directly from Maxwell's 1873 text
- **`user_original`** -- theoretical extensions built by the modernization project (e.g., the spherical harmonics infrastructure)
- **`standard_math`** -- established mathematical machinery (vector calculus, elliptic integrals)

### CGS vs SI Units

This project uses CGS-EMU as its primary unit system. SI values are available for reference only. Conversion utilities in `maxwell/core/units/` handle ESU/EMU/CGS/SI conversions. The constants module (`maxwell/config/constants.py`) provides both CGS and SI reference values.

## For Developers

### Project Layout

```
maxwell/
    __init__.py          # Package entry point, version info
    core/                # Shared abstractions: Charge, Field, Potential, Magnet
    electrostatics/      # Part I: Static electric fields (Arts. 1-206)
    electrokinematics/   # Part II: Currents and conduction (Arts. 230-370)
    magnetism/           # Part III: Magnetic measurements (Arts. 371-474)
    electromagnetism/    # Part IV: Unified theory (Arts. 475-866)
    math/                # Spherical harmonics, elliptic integrals, vector calculus
    fields/              # General field theory and constitutive relations
    materials/           # Hysteresis, saturation, permeability
    optics/              # Electromagnetic theory of light
    molecular/           # Molecular theories of magnetism
    config/              # Physical constants and conventions
    meta/                # Citation system (@maxwell_cite)
    ... and more
tests/
    test_*.py            # 1795 tests (629 core + 847 JAX + 66 SymPy + 232 visualization + 21 dynamics)
archive/                 # Legacy development documents
docs/                    # API reference, coverage, validation
```

### Adding a New Function

1. Create the function in the appropriate module
2. Decorate it with `@maxwell_cite(article_numbers)`
3. Write a test with a descriptive name

```python
# maxwell/electrostatics/my_module.py
from maxwell.meta.citation import maxwell_cite

@maxwell_cite(86, 87, part=1, chapter="General Theorems")
def my_electrostatics_function(charge, distance):
    """Implement Maxwell's formulation from Arts. 86-87."""
    ...
```

### Running Tests

```bash
# Full suite
pytest tests/ -v

# Specific test file
pytest tests/test_part_iv_electromagnetism.py -v

# With coverage
pytest tests/ --cov=maxwell --cov-report=term-missing
```

### Type Checking and Formatting

```bash
mypy maxwell/
black maxwell/ tests/
isort maxwell/ tests/
```

## Principles

- **Scholarly fidelity.** Every implementation must trace back to a specific article in the Treatise. The original text is the authoritative specification.
- **Computational correctness.** Mathematical implementations are validated against analytical results. All 50 math checks pass.
- **Open access.** The Treatise is public domain. The software is MIT-licensed and the scholarly content is CC BY 4.0 -- free for scholars, students, and developers everywhere.
- **Reproducibility.** Every result can be recomputed from source. The test suite is the specification.

## License

- **Software** (Python library, tests, scripts, CI/CD, page-verifier application, agent definitions, notebooks): [MIT License](LICENSE)
- **Content** (paper, documentation, architecture maps, figures, curated interpretive material): [CC BY 4.0](LICENSE-CONTENT)
- **Maxwell's original Treatise text** (1873): public domain. This project does not claim copyright in Maxwell's words, mechanical OCR of those words, or mathematical facts.

See [LICENSING_DECISION.md](LICENSING_DECISION.md) for the adopted split and inventory.

## Acknowledgments

This project is a computational homage to [James Clerk Maxwell](https://en.wikipedia.org/wiki/James_Clerk_Maxwell) and his _A Treatise on Electricity and Magnetism_ (1873), one of the foundational works of classical physics. The Treatise text is in the public domain.

The implementation follows the article numbering and chapter structure of the original Dover Publications reprint.

---

_Maxwell Modernized. All 866 articles. Fully tested. Scholarly traceable._

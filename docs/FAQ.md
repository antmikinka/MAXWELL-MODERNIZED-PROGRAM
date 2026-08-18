# FAQ -- Maxwell Modernized

## Installation

### Q: Why is it `pip install maxwell-modernized` but `import maxwell`?
A: `maxwell` is already taken on PyPI by an unrelated linguistics library. The distribution name is `maxwell-modernized`. The Python import stays `maxwell`.

### Q: Which Python versions are supported?
A: Python 3.10, 3.11, 3.12, and 3.13.

### Q: How do I install with GPU support?
A: `pip install maxwell-modernized[accel]` installs JAX for GPU/TPU acceleration.

### Q: What are the optional dependency groups?
A:
- `[dev]` -- pytest, mypy, black, isort
- `[viz]` -- matplotlib
- `[symbolic]` -- SymPy
- `[accel]` -- JAX
- `[all]` -- all of the above

## Units

### Q: Why CGS-EMU instead of SI?
A: Maxwell's 1873 Treatise used CGS-EMU throughout. The library preserves this for historical fidelity. SI reference values and conversion utilities are provided.

### Q: How do I convert CGS results to SI?
A: Use `CGSUnitConverter` from `maxwell.core.units`:
```python
from maxwell.core.units import CGSUnitConverter
converter = CGSUnitConverter()
si_value = converter.cgs_to_si_electric_field(cgs_value)
```

## JAX

### Q: Do I need a GPU to use maxwell.jax?
A: No. JAX runs on CPU by default. GPU/TPU acceleration is automatic when available.

### Q: Why is float64 required?
A: CGS unit ratios require ~15 digits of precision. JAX defaults to float32, so `jax_enable_x64` must be set.

### Q: Can I use auto-differentiation with any Maxwell function?
A: Only the JAX adapters support `jax.grad`. The NumPy versions do not.

## Citation System

### Q: How do I find which functions implement a specific article?
A: `grep -r "@maxwell_cite.*<article_number>" maxwell/`

### Q: What do the theory classifications mean?
A:
- `maxwell_original` -- from Maxwell's 1873 text
- `user_original` -- modernization project extensions
- `standard_math` -- established mathematical tools

## Troubleshooting

### Q: Tests are failing after installation
A: Ensure you installed the correct extras: `pip install -e ".[dev,accel]"` for the full test suite.

### Q: JAX tests are skipped
A: Install the accel extra: `pip install maxwell-modernized[accel]`.

### Q: Import error on maxwell.jax
A: JAX is an optional dependency. Install with `pip install maxwell-modernized[accel]`.

## Licensing

### Q: What license is this project under?
A: Split licensing:

- **Software** (the Python library, tests, scripts, CI, notebooks): [MIT License](../LICENSE)
- **Scholarly content** (documentation, architecture maps, figures): [CC BY 4.0](../LICENSE-CONTENT)
- **Maxwell's 1873 Treatise text**: public domain. This project does not claim copyright in Maxwell's words.

We are working toward a preprint. It is not included in this repository and is not a citable article yet.

See [LICENSING_DECISION.md](../LICENSING_DECISION.md).

### Q: Why isn't everything CC BY 4.0? This is a scholarly modernization.
A: CC BY 4.0 is the right license for released documentation. It is not an OSI-approved software license, so it cannot be the license of the PyPI package.

### Q: Why isn't James Clerk Maxwell listed as a software author?
A: He wrote the 1873 Treatise, which is public domain. He did not write this Python library. Cite the book as the source work; cite this repository for the computational edition.

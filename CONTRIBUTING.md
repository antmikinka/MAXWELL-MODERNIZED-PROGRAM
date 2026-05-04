# Contributing to Maxwell Modernized

Thank you for your interest in contributing to Maxwell Modernized. This project aims to provide a complete computational implementation of Maxwell's 1873 _Treatise on Electricity and Magnetism_.

## Development Setup

```bash
# Clone the repository
git clone https://github.com/maxwell-treatise/modernized-program.git
cd modernized-program

# Install with development dependencies
pip install -e ".[dev]"

# Run the test suite
pytest -v
```

## Project Structure

The codebase is organized to mirror the Treatise's four-part structure:

```
maxwell/
├── core/                  # Shared domain objects (Charge, Field, Potential)
├── electrostatics/        # Part I: Electrostatics (Arts. 1-206)
├── electrokinematics/     # Part II: Electrokinematics (Arts. 230-370)
├── magnetism/             # Part III: Magnetism (Arts. 371-474)
├── electromagnetism/      # Part IV: Electromagnetism (Arts. 475-866)
├── math/                  # Mathematical infrastructure
├── optics/                # Optics and wave propagation
├── molecular/             # Molecular theory of action at a distance
├── verification/          # Numerical verification framework
├── meta/                  # Citation and metadata system
├── config/                # Physical constants and configuration
├── jax/                   # JAX adapter (GPU/TPU, auto-diff)
│   ├── _compat.py         # Pytree registration, safe arithmetic
│   ├── _elliptic.py       # AGM elliptic integrals
│   ├── _scipy_special.py  # Pure JAX special functions
│   ├── core/              # JAX domain classes (PointChargeJAX)
│   ├── electromagnetism/  # Faraday, Maxwell equations (JAX)
│   └── math/              # Spherical harmonics (JAX)
└── vis/                   # Visualization engine
```

## How to Contribute

### Implementing a Maxwell Article

1. **Identify the article** to implement and locate its corresponding Part/package.
2. **Create or extend the module** in the appropriate package.
3. **Decorate with `@maxwell_cite`** to link your implementation to the article number(s).
4. **Use CGS-EMU units** as the primary unit system (SI values are available in `maxwell/config/constants.py`).
5. **Write tests** that verify the implementation against known analytical results.

### Citation Decorator

Every public function must be decorated with `@maxwell_cite`:

```python
from maxwell.meta.citation import maxwell_cite

@maxwell_cite(230, 231, part=2, chapter="The Electric Current",
              theory_class="maxwell_original",
              description="Ohm's law in differential form")
def calc_current_density(E_field, conductivity):
    ...
```

### Unit System

- **Primary**: CGS-EMU (Electromagnetic Units) -- Maxwell's own system
- **Secondary**: CGS-ESU, Gaussian, SI (via conversion utilities in `maxwell/core/units/`)
- All constants are defined in `maxwell/config/constants.py`

### Code Style

- **Formatting**: Black (line length 88)
- **Imports**: isort with black profile
- **Type hints**: mypy strict mode (see `pyproject.toml`)

```bash
# Check formatting
black --check maxwell/

# Sort imports
isort maxwell/

# Type checking
mypy maxwell/
```

## Testing

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=maxwell --cov-report=html

# Run mathematical verification
pytest tests/test_math_verification.py -v

# Run a single test file
pytest tests/test_electrostatics.py -v

# Run test subsets using pytest markers
pytest -m jax           # JAX adapter tests (requires `pip install .[accel]`)
pytest -m sympy         # SymPy symbolic verification tests (requires `pip install .[symbolic]`)
pytest -m slow          # Long-running tests
pytest -m visualization # Visualization tests (requires `pip install .[viz]`)
pytest -m "jax and not slow"  # Combine markers
pytest -m "not jax"     # Exclude JAX tests for fast core-only runs
```

### Writing Tests

- Place tests in `tests/` with the naming convention `test_<module>.py`
- Test functions must be named `test_<description>`
- Each test should verify a specific physical or mathematical property
- Include numerical tolerance checks for floating-point comparisons

## Verification Framework

The verification system (`maxwell/verification/`) provides automated validation:

```python
from maxwell.verification import (
    VerificationSuite,
    VerificationReport,
    verify_spherical_harmonics,
    verify_electrostatics,
)

suite = VerificationSuite()
suite.register(verify_spherical_harmonics)
suite.register(verify_electrostatics)
report = suite.run()
print(report.summary())
```

## JAX Adapter

The `maxwell.jax` package provides GPU/TPU-accelerated, auto-differentiable versions of core computations.

### JAX Adapter Development

```bash
# Install JAX
pip install -e ".[accel]"

# Run JAX adapter tests
pytest tests/test_jax_adapter.py -v
```

### Creating a JAX-Compatible Class

1. **Use `@jax_tree` decorator** for pytree registration:
   ```python
   from maxwell.jax._compat import jax_tree, safe_div

   @jax_tree
   @dataclass
   class MyClassJAX:
       value: float
       field: jax.Array
   ```

2. **Replace all `np.*` calls with `jnp.*`** — no NumPy in computation paths.

3. **Use `jax.lax.fori_loop` / `jax.lax.while_loop`** for loops — Python `for`/`while` are not JIT-traceable.

4. **Use `jnp.where` instead of `if`** for array-valued conditionals.

5. **Enable float64** for CGS precision:
   ```python
   jax.config.update("jax_enable_x64", True)
   ```

### JAX Compatibility Checklist

- [ ] All dataclass fields are JAX-pytree leaves
- [ ] No Python control flow on traced values
- [ ] Safe division/sqrt/log via `_compat` module
- [ ] Tests verify JIT, vmap, and grad compatibility
- [ ] Numerical results match NumPy reference to 1e-10

## Pull Requests

1. Create a feature branch: `git checkout -b feat/article-NNN`
2. Implement the article(s) with citation decorators
3. Add tests verifying correctness
4. Ensure all existing tests pass: `pytest -v`
5. Submit a PR with:
   - Article numbers implemented
   - Brief description of the physics
   - Any deviations from Maxwell's original formulation

## Reporting Issues

- **Bug reports**: Include the article number, expected vs. actual output, and a minimal reproducer
- **Feature requests**: Specify the Treatise article(s) and desired functionality
- **Documentation issues**: Cite the specific function or module

## License

This project is licensed under the MIT License. By contributing, you agree that your contributions will be licensed under the same terms.

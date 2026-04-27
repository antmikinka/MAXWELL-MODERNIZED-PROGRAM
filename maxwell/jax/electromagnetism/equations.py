"""
JAX-compatible Maxwell's general equations of the electromagnetic field.

Provides JAX-pytree versions of the NumPy reference at
maxwell.electromagnetism.theory.general_equations, enabling JIT compilation,
automatic differentiation, and vectorized evaluation of all four Maxwell
equations in CGS Gaussian units.

Implemented equations (Part IV, Arts. 594-603):
    - Gauss's Law (Electric):   div D = 4*pi*rho
    - Gauss's Law (Magnetic):   div B = 0
    - Faraday's Law (Eq A):     curl E = -(1/c) * dB/dt
    - Ampere-Maxwell (Eq B):    curl H = (4*pi/c)*J + (1/c)*dD/dt

Numerical divergence and curl use central finite differences on uniform
spatial grids, implemented purely in jax.numpy for full JAX transform
compatibility (jit, grad, vmap).

Category: B (user_original) -- JAX adapter for Maxwell's theory.

References:
    Part IV, Arts. 594-603: General equations of the electromagnetic field.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
from jax import jit

from maxwell.jax._compat import jax_tree
from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import C

__all__ = [
    "ElectromagneticFieldJAX",
    "MaxwellEquationsJAX",
    "verify_maxwell_equations_jax",
]

# ── Numerical Differentiation Helpers ─────────────────────────────


def _central_diff(values: jax.Array, dx: float) -> jax.Array:
    """Central finite differences along axis 0.

    Interior points use (f[i+1] - f[i-1]) / (2*dx).
    Boundary points use one-sided differences.

    Args:
        values: 1-D array of function values at uniformly spaced points.
        dx: Grid spacing.

    Returns:
        Derivative at each point, same shape as values.
    """
    values = jnp.asarray(values, dtype=jnp.float64)
    n = values.shape[0]
    if n < 2:
        return jnp.zeros_like(values)

    # Interior: central difference
    interior = (values[2:] - values[:-2]) / (2.0 * dx)

    # Boundaries: one-sided
    left = values[1] - values[0]
    right = values[-1] - values[-2]

    return jnp.concatenate([
        jnp.array([left / dx], dtype=jnp.float64),
        interior,
        jnp.array([right / dx], dtype=jnp.float64),
    ])


def numerical_divergence_1d(
    field: jax.Array,
    dx: float = 0.01,
) -> jax.Array:
    """Divergence of a 3-vector field varying along one spatial axis.

    For F = (Fx, Fy, Fz) with shape (3, N):
        div F = dFx/dx + dFy/dy + dFz/dz

    Only the component aligned with the variation axis contributes
    when the field varies along that single axis.

    Args:
        field: Vector field, shape (3, N).
        dx: Grid spacing.

    Returns:
        Divergence, shape (N,).
    """
    field = jnp.asarray(field, dtype=jnp.float64)
    if field.ndim == 1 and field.shape[0] == 3:
        return jnp.float64(0.0)

    n_comp = field.shape[0]  # should be 3
    div = jnp.zeros(field.shape[1:], dtype=jnp.float64)
    for i in range(n_comp):
        div = div + _central_diff(field[i], dx)
    return div


def numerical_curl_1d(
    field: jax.Array,
    dx: float = 0.01,
) -> jax.Array:
    """Curl of a 3-vector field varying along one spatial axis.

    For F = (Fx, Fy, Fz) with shape (3, N) varying along x:
        curl F = (0, dFz/dx, -dFy/dx)

    Args:
        field: Vector field, shape (3, N).
        dx: Grid spacing.

    Returns:
        Curl, shape (3, N).
    """
    field = jnp.asarray(field, dtype=jnp.float64)
    if field.ndim == 1 and field.shape[0] == 3:
        return jnp.zeros(3, dtype=jnp.float64)

    n = field.shape[1]
    curl = jnp.zeros_like(field)
    # Only y and z components get non-zero curl when varying along x
    curl = curl.at[1].set(_central_diff(field[2], dx))   # (curl F)_y = dFz/dx
    curl = curl.at[2].set(-_central_diff(field[1], dx))   # (curl F)_z = -dFy/dx
    return curl


# ── ElectromagneticFieldJAX ──────────────────────────────────────


@jax_tree
@dataclass
class ElectromagneticFieldJAX:
    """Complete electromagnetic field state -- all field quantities at a point.

    Art. 594-603: Maxwell's general equations describe the relationships
    between these fundamental field quantities:

    - E: Electric field intensity (statvolts/cm)
    - B: Magnetic flux density (gauss)
    - H: Magnetic field intensity (oersted)
    - D: Electric displacement (statcoulombs/cm^2)
    - J: Current density (abamperes/cm^2)
    - rho: Charge density (statcoulombs/cm^3)

    This is the JAX-pytree equivalent of
    maxwell.electromagnetism.theory.general_equations.ElectromagneticField.

    Attributes:
        E: Electric field vector (statvolts/cm), shape (3,).
        B: Magnetic flux density vector (gauss), shape (3,).
        H: Magnetic field intensity vector (oersted), shape (3,).
        D: Electric displacement vector (statcoulombs/cm^2), shape (3,).
        J: Current density vector (abamperes/cm^2), shape (3,).
        rho: Charge density (statcoulombs/cm^3).
    """

    E: jax.Array = None  # type: ignore[assignment]
    B: jax.Array = None  # type: ignore[assignment]
    H: jax.Array = None  # type: ignore[assignment]
    D: jax.Array = None  # type: ignore[assignment]
    J: jax.Array = None  # type: ignore[assignment]
    rho: float = 0.0

    def __post_init__(self):
        zero3 = jnp.zeros(3, dtype=jnp.float64)
        object.__setattr__(self, 'E', jnp.asarray(self.E if self.E is not None else zero3, dtype=jnp.float64))
        object.__setattr__(self, 'B', jnp.asarray(self.B if self.B is not None else zero3, dtype=jnp.float64))
        object.__setattr__(self, 'H', jnp.asarray(self.H if self.H is not None else zero3, dtype=jnp.float64))
        object.__setattr__(self, 'D', jnp.asarray(self.D if self.D is not None else zero3, dtype=jnp.float64))
        object.__setattr__(self, 'J', jnp.asarray(self.J if self.J is not None else zero3, dtype=jnp.float64))


# ── MaxwellEquationsJAX ─────────────────────────────────────────


@jax_tree
@dataclass
class MaxwellEquationsJAX:
    """Maxwell's equations calculator (JAX-compatible).

    Provides JIT-compatible implementations of Gauss's laws, Faraday's
    law, and the Ampere-Maxwell law in CGS Gaussian units.

    Art. 594-603: The general equations of the electromagnetic field.

    Attributes:
        permittivity: Permittivity epsilon (default: 1.0 for vacuum).
        permeability: Permeability mu (default: 1.0 for vacuum).
        conductivity: Conductivity sigma (default: 0.0).

    Example:
        >>> import jax.numpy as jnp
        >>> meq = MaxwellEquationsJAX()
        >>> # Single-point Faraday: curl E from a changing B field
        >>> dB_dt = jnp.array([1e10, 0.0, 0.0])
        >>> curl_E = meq.equation_A_faraday(dB_dt)
        >>> # Verify Gauss's law on a spatial grid
        >>> x = jnp.linspace(-1.0, 1.0, 50)
        >>> D = jnp.stack([1.0 + 2.0*x, jnp.zeros(50), jnp.zeros(50)], axis=0)
        >>> report = meq.gauss_law_electric(D, dx=0.04)
        >>> print(report['residual'])  # close to 0
    """

    permittivity: float = 1.0
    permeability: float = 1.0
    conductivity: float = 0.0

    def __post_init__(self):
        # Wrap in try/except: when JIT traces this dataclass the material
        # parameters become traced values and raise TracerBoolConversionError
        # on the <= comparison.  Validation is only needed at construction
        # time (concrete Python floats), not during tracing.
        try:
            if self.permittivity <= 0:
                raise ValueError(
                    f"Permittivity must be positive, got {self.permittivity}"
                )
            if self.permeability <= 0:
                raise ValueError(
                    f"Permeability must be positive, got {self.permeability}"
                )
            if self.conductivity < 0:
                raise ValueError(
                    f"Conductivity must be non-negative, got {self.conductivity}"
                )
        except jax.errors.TracerBoolConversionError:
            pass  # tracing path -- skip runtime validation

    # ── Gauss's Law (Electric): div D = 4*pi*rho ──────────────

    def gauss_law_electric(
        self,
        D: jax.Array,
        dx: float = 0.01,
        rho: float | None = None,
    ) -> dict[str, Any]:
        """Gauss's law for the electric field.

        Art. 594: div D = 4*pi*rho.

        Computes the numerical divergence of D on a uniform grid using
        central finite differences. If rho is provided, the residual
        |div D - 4*pi*rho| is reported.

        Args:
            D: Electric displacement, shape (3,) for a single point
               (returns zero divergence) or (3, N) for N grid points.
            dx: Grid spacing for numerical differentiation.
            rho: Optional known charge density for residual computation.

        Returns:
            Dictionary with:
                divergence: Scalar (single point) or array (N,) of div D.
                expected: 4*pi*rho if rho was provided, else None.
                residual: |divergence - expected|, None if rho not given.
        """
        D = jnp.asarray(D, dtype=jnp.float64)
        if D.ndim == 1 and D.shape[0] == 3:
            div_val = jnp.float64(0.0)
        else:
            div_val = numerical_divergence_1d(D, dx)

        expected = 4.0 * jnp.pi * rho if rho is not None else None
        residual = (
            jnp.abs(div_val - expected)
            if expected is not None
            else None
        )

        return {
            "divergence": div_val,
            "expected": expected,
            "residual": residual,
        }

    # ── Gauss's Law (Magnetic): div B = 0 ─────────────────────

    def gauss_law_magnetic(
        self,
        B: jax.Array,
        dx: float = 0.01,
    ) -> dict[str, Any]:
        """Gauss's law for the magnetic field.

        Art. 594: div B = 0 (no magnetic monopoles).

        Computes the numerical divergence of B and reports how close
        it is to zero.

        Args:
            B: Magnetic flux density, shape (3,) or (3, N).
            dx: Grid spacing for numerical differentiation.

        Returns:
            Dictionary with:
                divergence: Scalar or array of div B.
                max_abs_div: Maximum absolute divergence (should be ~0).
        """
        B = jnp.asarray(B, dtype=jnp.float64)
        if B.ndim == 1 and B.shape[0] == 3:
            div_val = jnp.float64(0.0)
        else:
            div_val = numerical_divergence_1d(B, dx)

        max_abs_div = jnp.max(jnp.abs(div_val)) if div_val.ndim > 0 else jnp.abs(div_val)

        return {
            "divergence": div_val,
            "max_abs_div": max_abs_div,
        }

    # ── Faraday's Law (Eq A): curl E = -(1/c) * dB/dt ────────

    def equation_A_faraday(
        self,
        dB_dt: jax.Array,
    ) -> jax.Array:
        """Faraday's law of electromagnetic induction.

        Art. 598, Equation (A): curl E = -(1/c) * dB/dt.

        Given the time derivative of the magnetic field, returns the
        implied curl of the electric field.  This is a point-wise
        operation -- no numerical differentiation required.

        Args:
            dB_dt: Time derivative of B (gauss/s), shape (3,) or (3, N).

        Returns:
            Curl of E (statvolts/cm^2), same shape as dB_dt.
        """
        dB_dt = jnp.asarray(dB_dt, dtype=jnp.float64)
        return -(1.0 / C) * dB_dt

    # ── Ampere-Maxwell (Eq B): curl H = (4pi/c)*J + (1/c)*dD/dt ─

    def equation_B_ampere(
        self,
        J: jax.Array,
        dD_dt: jax.Array | None = None,
    ) -> dict[str, Any]:
        """Ampere-Maxwell law.

        Art. 600, Equation (E):
            curl H = (4*pi/c) * J + (1/c) * dD/dt.

        Given current density J (and optionally displacement-current
        rate dD/dt), returns the implied curl of H broken into
        conduction and displacement contributions.

        Args:
            J: Conduction current density (abamperes/cm^2), shape (3,).
            dD_dt: Time derivative of D (statcoulombs/cm^2/s), shape (3,).
                   Defaults to zero.

        Returns:
            Dictionary with:
                curl_H: Total curl of H, shape (3,).
                conduction_term: (4*pi/c)*J, shape (3,).
                displacement_term: (1/c)*dD/dt, shape (3,).
        """
        J = jnp.asarray(J, dtype=jnp.float64)
        if dD_dt is None:
            dD_dt = jnp.zeros(3, dtype=jnp.float64)
        else:
            dD_dt = jnp.asarray(dD_dt, dtype=jnp.float64)

        conduction = (4.0 * jnp.pi / C) * J
        displacement = (1.0 / C) * dD_dt

        return {
            "curl_H": conduction + displacement,
            "conduction_term": conduction,
            "displacement_term": displacement,
        }

    # ── verify_no_monopoles: check div B = 0 ─────────────────

    def verify_no_monopoles(
        self,
        B: jax.Array,
        dx: float = 0.01,
        atol: float = 1e-6,
    ) -> dict[str, Any]:
        """Verify the absence of magnetic monopoles.

        Checks that div B = 0 within the given absolute tolerance.

        Args:
            B: Magnetic flux density, shape (3,) or (3, N).
            dx: Grid spacing for numerical differentiation.
            atol: Absolute tolerance for the zero-check.

        Returns:
            Dictionary with:
                max_abs_div: Maximum absolute divergence found.
                passed: True if max_abs_div < atol.
                atol: The tolerance used.
        """
        result = self.gauss_law_magnetic(B, dx)
        max_div = result["max_abs_div"]
        passed = jnp.less(max_div, atol)
        return {
            "max_abs_div": max_div,
            "passed": passed,
            "atol": atol,
        }


# ── verify_maxwell_equations_jax ────────────────────────────────


@maxwell_cite(
    594, 598, 600, 603,
    part=4, chapter="General Equations of the Electromagnetic Field",
    theory_class="maxwell_original",
    description="Numerical verification of all Maxwell equations (JAX)",
)
def verify_maxwell_equations_jax(
    atol: float = 1e-6,
) -> dict[str, Any]:
    """Numerical verification of all Maxwell equations (JAX).

    Runs a suite of tests on the JAX-pytree MaxwellEquationsJAX class:
      1. Gauss electric -- uniform D field (div = 0)
      2. Gauss electric -- non-uniform D field with known charge density
      3. Gauss magnetic -- uniform B field (div = 0)
      4. Gauss magnetic -- verify_no_monopoles check
      5. Faraday's law -- JIT-compiled point evaluation
      6. Ampere-Maxwell -- conduction + displacement terms

    All computations use jax.numpy and are compatible with JIT.

    Args:
        atol: Absolute tolerance for numerical assertions.

    Returns:
        Dictionary with per-equation results and an overall summary.
    """
    meq = MaxwellEquationsJAX()
    results: dict[str, Any] = {}

    # Grid for spatially varying fields
    x = jnp.linspace(-1.0, 1.0, 50)
    dx = float(x[1] - x[0])

    # ── Test 1: Gauss electric, uniform D ─────────────────────
    D_uniform = jnp.stack([
        jnp.full(50, 1000.0),
        jnp.zeros(50),
        jnp.zeros(50),
    ], axis=0)
    r1 = meq.gauss_law_electric(D_uniform, dx=dx)
    div1 = r1["divergence"]
    max_div1 = float(jnp.max(jnp.abs(div1))) if div1.ndim > 0 else float(jnp.abs(div1))
    results["gauss_electric_uniform"] = {
        "passed": max_div1 < atol,
        "max_abs_divergence": max_div1,
    }

    # ── Test 2: Gauss electric, D = (D0 + alpha*x, 0, 0) ─────
    #    div D = alpha, so rho = alpha / (4*pi)
    alpha = 500.0
    D0 = 1000.0
    D_radial = jnp.stack([
        D0 + alpha * x,
        jnp.zeros(50),
        jnp.zeros(50),
    ], axis=0)
    rho_expected = alpha / (4.0 * jnp.pi)
    r2 = meq.gauss_law_electric(D_radial, dx=dx, rho=float(rho_expected))
    res2 = r2["residual"]
    max_res2 = float(jnp.max(jnp.abs(res2))) if res2 is not None and res2.ndim > 0 else float(res2 or 0.0)
    results["gauss_electric_nonuniform"] = {
        "passed": max_res2 < atol * 1e3,
        "max_residual": max_res2,
        "expected_rho": float(rho_expected),
    }

    # ── Test 3: Gauss magnetic, uniform B ─────────────────────
    B_uniform = jnp.stack([
        jnp.full(50, 500.0),
        jnp.zeros(50),
        jnp.zeros(50),
    ], axis=0)
    r3 = meq.gauss_law_magnetic(B_uniform, dx=dx)
    results["gauss_magnetic_uniform"] = {
        "passed": r3["max_abs_div"] < atol,
        "max_abs_divergence": r3["max_abs_div"],
    }

    # ── Test 4: verify_no_monopoles ───────────────────────────
    r4 = meq.verify_no_monopoles(B_uniform, dx=dx, atol=atol)
    results["verify_no_monopoles"] = {
        "passed": r4["passed"],
        "max_abs_div": r4["max_abs_div"],
    }

    # ── Test 5: Faraday's law (JIT-compiled) ──────────────────
    @jit
    def _faraday_jit(dB_dt):
        return meq.equation_A_faraday(dB_dt)

    dB_dt = jnp.array([1e10, 0.0, 0.0])
    curl_E = _faraday_jit(dB_dt)
    expected_faraday = -(1.0 / C) * dB_dt
    faraday_err = float(jnp.max(jnp.abs(curl_E - expected_faraday)))
    results["faraday_law"] = {
        "passed": faraday_err < atol,
        "max_error": faraday_err,
        "curl_E": curl_E,
        "expected": expected_faraday,
    }

    # ── Test 6: Ampere-Maxwell ────────────────────────────────
    J_test = jnp.array([1.0, 0.0, 0.0])
    dD_dt_test = jnp.array([0.0, 1e5, 0.0])
    r6 = meq.equation_B_ampere(J_test, dD_dt=dD_dt_test)
    expected_cond = (4.0 * jnp.pi / C) * J_test
    expected_disp = (1.0 / C) * dD_dt_test
    cond_err = float(jnp.max(jnp.abs(r6["conduction_term"] - expected_cond)))
    disp_err = float(jnp.max(jnp.abs(r6["displacement_term"] - expected_disp)))
    results["ampere_maxwell"] = {
        "passed": cond_err < atol and disp_err < atol,
        "conduction_error": cond_err,
        "displacement_error": disp_err,
    }

    # ── Summary ───────────────────────────────────────────────
    all_passed = all(v.get("passed", False) for v in results.values())
    results["all_verified"] = all_passed
    results["equations_tested"] = [
        "gauss_electric",
        "gauss_magnetic",
        "faraday_A",
        "ampere_B",
        "verify_no_monopoles",
    ]
    results["atol"] = atol

    return results

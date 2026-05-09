"""maxwell.calculator_ui -- Streamlit UI for the Maxwell Calculus Calculator.

A single-page application with sidebar navigation across four calculator modes:

1. Equation Calculator -- Interactive computation of Maxwell's equation sets
   (A through H, Coulomb, Solenoidal, Free Charge) using EquationRegistry
   metadata for formulas, variables, and presets.

2. Derivatives -- Partial derivatives, higher-order, mixed partials, Hessian,
   and gradient computation using maxwell.math.derivatives.

3. Integral Calculus -- Volume, surface, and line integrals using
   maxwell.math.calculus_calculator.

4. Theorem Verification -- Divergence theorem, Stokes' theorem, and Green's
   theorem verification using maxwell.math.calculus_calculator.

Usage:
    pip install -e ".[ui]"
    streamlit run maxwell/calculator_ui.py

All units are in CGS (centimeter-gram-second) system.

References:
    Maxwell, J. C. "A Treatise on Electricity and Magnetism", 3rd ed., 1873.
"""

from __future__ import annotations

import sys
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np

# ── Streamlit import (may not be installed during linting) ────────
try:
    import streamlit as st
except ImportError:
    print("streamlit is required. Install with: pip install streamlit")
    sys.exit(1)

# ── SymPy optional import ─────────────────────────────────────────
try:
    import sympy
    from sympy import diff as sym_diff
    from sympy import symbols as sym_symbols
    from sympy.parsing.sympy_parser import (
        implicit_multiplication_application,
        parse_expr,
        standard_transformations,
    )

    SYMPY_AVAILABLE = True
    _SYMPY_TRANSFORMS = standard_transformations + (
        implicit_multiplication_application,
    )
except ImportError:
    SYMPY_AVAILABLE = False

# ── Maxwell module imports ────────────────────────────────────────
try:
    from maxwell.config.equations import (
        REGISTRY,
        EquationRegistry,
        EquationSetEntry,
        PresetExample,
    )
    from maxwell.math.calculus_calculator import (
        line_integral_circle,
        surface_integral_sphere,
        verify_divergence_theorem,
        verify_greens_theorem,
        verify_stokes_theorem,
        volume_integral_scalar,
    )
    from maxwell.math.derivatives import (
        hessian,
        mixed_partial_derivative,
        partial_derivative,
        partial_gradient,
        second_partial_derivative,
    )
    from maxwell.math.vector_operators import curl, divergence, gradient
except ImportError:
    st.error("maxwell package not found. Install with: pip install -e .")
    sys.exit(1)

# ── Configuration ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Maxwell Calculus Calculator",
    page_icon="\\u26A1",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state defaults ────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Equation Calculator"
if "sympy_enabled" not in st.session_state:
    st.session_state.sympy_enabled = SYMPY_AVAILABLE

PAGES = [
    "Equation Calculator",
    "Derivatives",
    "Integral Calculus",
    "Theorem Verification",
]

# ═══════════════════════════════════════════════════════════════════
# HELPER: Parse SymPy expression to callable f(x, y, z)
# ═══════════════════════════════════════════════════════════════════


def parse_function(expr_str: str) -> Optional[Callable[[float, float, float], float]]:
    """Parse a SymPy expression string into a numerical function f(x, y, z).

    Args:
        expr_str: Expression like "x*y + z**2", "sin(x)*cos(y)".

    Returns:
        Callable that evaluates the expression at given (x, y, z),
        or None if parsing fails.
    """
    if not SYMPY_AVAILABLE:
        return None
    try:
        x, y, z = sym_symbols("x y z")
        local_dict = {"x": x, "y": y, "z": z}
        expr = parse_expr(
            expr_str, local_dict=local_dict, transformations=_SYMPY_TRANSFORMS
        )

        def func(xv: float, yv: float, zv: float) -> float:
            return float(expr.subs([(x, xv), (y, yv), (z, zv)]))

        return func
    except Exception:
        return None


def parse_function_with_t(
    expr_str: str,
) -> Optional[Callable[[float, float, float, float], float]]:
    """Parse a SymPy expression string into f(x, y, z, t).

    Args:
        expr_str: Expression string.

    Returns:
        Callable f(x, y, z, t) or None.
    """
    if not SYMPY_AVAILABLE:
        return None
    try:
        x, y, z, t = sym_symbols("x y z t")
        local_dict = {"x": x, "y": y, "z": z, "t": t}
        expr = parse_expr(
            expr_str, local_dict=local_dict, transformations=_SYMPY_TRANSFORMS
        )

        def func(xv: float, yv: float, zv: float, tv: float) -> float:
            return float(expr.subs([(x, xv), (y, yv), (z, zv), (t, tv)]))

        return func
    except Exception:
        return None


def sympy_gradient(expr_str: str, point: Tuple[float, float, float]) -> Dict[str, str]:
    """Compute symbolic gradient using SymPy.

    Args:
        expr_str: SymPy-parseable expression.
        point: (x, y, z) evaluation point.

    Returns:
        Dictionary with 'df/dx', 'df/dy', 'df/dz' as LaTeX strings.
    """
    if not SYMPY_AVAILABLE:
        return {}
    try:
        x, y, z = sym_symbols("x y z")
        local_dict = {"x": x, "y": y, "z": z}
        expr = parse_expr(
            expr_str, local_dict=local_dict, transformations=_SYMPY_TRANSFORMS
        )
        px, py, pz = point
        result: Dict[str, str] = {}
        for var, label, val in [
            (x, "df/dx", px),
            (y, "df/dy", py),
            (z, "df/dz", pz),
        ]:
            deriv = sym_diff(expr, var)
            val_str = sympy.latex(deriv)
            num_val = float(deriv.subs([(x, px), (y, py), (z, pz)]))
            result[label] = f"{val_str} = {num_val:.6f}"
        return result
    except Exception:
        return {}


def sympy_hessian(expr_str: str, point: Tuple[float, float, float]) -> Optional[str]:
    """Compute symbolic Hessian using SymPy.

    Args:
        expr_str: SymPy-parseable expression.
        point: (x, y, z) evaluation point.

    Returns:
        LaTeX string of Hessian matrix, or None.
    """
    if not SYMPY_AVAILABLE:
        return None
    try:
        x, y, z = sym_symbols("x y z")
        local_dict = {"x": x, "y": y, "z": z}
        expr = parse_expr(
            expr_str, local_dict=local_dict, transformations=_SYMPY_TRANSFORMS
        )
        px, py, pz = point
        vars_list = [x, y, z]
        hess_matrix = sympy.Matrix(
            [[sym_diff(expr, vi, vj) for vj in vars_list] for vi in vars_list]
        )
        hess_num = hess_matrix.subs([(x, px), (y, py), (z, pz)])
        return sympy.latex(hess_num)
    except Exception:
        return None


def sympy_second_derivatives(
    expr_str: str, point: Tuple[float, float, float]
) -> Dict[str, str]:
    """Compute symbolic second derivatives using SymPy.

    Args:
        expr_str: SymPy-parseable expression.
        point: (x, y, z) evaluation point.

    Returns:
        Dictionary mapping derivative name to LaTeX + numerical result.
    """
    if not SYMPY_AVAILABLE:
        return {}
    try:
        x, y, z = sym_symbols("x y z")
        local_dict = {"x": x, "y": y, "z": z}
        expr = parse_expr(
            expr_str, local_dict=local_dict, transformations=_SYMPY_TRANSFORMS
        )
        px, py, pz = point
        subs_list = [(x, px), (y, py), (z, pz)]
        result: Dict[str, str] = {}
        for vi, vj, label in [
            (x, x, "d2f/dx2"),
            (y, y, "d2f/dy2"),
            (z, z, "d2f/dz2"),
            (x, y, "d2f/dxdy"),
            (x, z, "d2f/dxdz"),
            (y, z, "d2f/dydz"),
        ]:
            deriv = sym_diff(sym_diff(expr, vi), vj)
            val_str = sympy.latex(deriv)
            num_val = float(deriv.subs(subs_list))
            result[label] = f"{val_str} = {num_val:.6f}"
        return result
    except Exception:
        return {}


# ═══════════════════════════════════════════════════════════════════
# PAGE 1: EQUATION CALCULATOR
# ═══════════════════════════════════════════════════════════════════


def _render_equation_calculator(registry: EquationRegistry) -> None:
    """Render the Equation Calculator page."""
    st.title("Equation Calculator")
    st.caption(
        "Interactive computation of Maxwell's equation sets from the 1873 Treatise"
    )

    # Build display map: set_id -> human-readable name
    all_sets = registry.get_all()
    set_options: Dict[str, str] = {}
    for sid, entry in all_sets.items():
        art_str = f"Arts. {entry.articles[0]}-{entry.articles[-1]}"
        set_options[sid] = f"Set {sid}: {entry.name} ({art_str})"

    selected_set = st.sidebar.selectbox(
        "Equation Set",
        options=list(set_options.keys()),
        format_func=lambda s: set_options[s],
        key="eq_set_select",
    )

    entry = registry.get(selected_set)

    # Display metadata
    st.info(
        f"**{entry.name}**\n\n"
        f"Volume {entry.volume}, Part {entry.part}, Chapter: {entry.chapter}\n\n"
        f"{entry.notes}"
    )

    # Vector form
    st.latex(entry.vector_form)

    # Formula tabs (one tab per formula in the set)
    if entry.formulas:
        formula_tabs = st.tabs([f.equation_id for f in entry.formulas])
        for tab, formula in zip(formula_tabs, entry.formulas):
            with tab:
                st.latex(formula.latex)
                st.caption(formula.description)

                # Variable inputs
                st.subheader("Inputs")
                inputs: Dict[str, Any] = {}
                cols = st.columns(2)
                col_idx = 0

                for var in formula.variables:
                    with cols[col_idx % 2]:
                        var_def = entry.variables.get(var.name, var)
                        label = f"{var.name} -- {var_def.description}"

                        if var_def.var_type.value in ("field", "vector"):
                            # For fields, allow function expression or scalar value
                            expr_val = st.text_input(
                                label=f"{var.name} (function or value)",
                                value="0",
                                key=f"eq_{selected_set}_{formula.equation_id}_{var.name}",
                            )
                            inputs[f"{var.name}_raw"] = expr_val
                        else:
                            num_val = st.number_input(
                                label=label,
                                value=0.0,
                                step=1.0,
                                format="%.4f",
                                key=f"eq_{selected_set}_{formula.equation_id}_{var.name}",
                            )
                            inputs[var.name] = num_val

                    col_idx += 1

                # Evaluation point (for formulas needing derivatives)
                if formula.variables and any(
                    v.var_type.value in ("field",) for v in formula.variables
                ):
                    st.subheader("Evaluation Point (cm)")
                    pt_cols = st.columns(3)
                    with pt_cols[0]:
                        px = st.number_input(
                            "x", value=1.0, key=f"eq_pt_x_{formula.equation_id}"
                        )
                    with pt_cols[1]:
                        py = st.number_input(
                            "y", value=0.0, key=f"eq_pt_y_{formula.equation_id}"
                        )
                    with pt_cols[2]:
                        pz = st.number_input(
                            "z", value=0.0, key=f"eq_pt_z_{formula.equation_id}"
                        )
                    inputs["point"] = (px, py, pz)

                # Compute button
                if st.button(
                    f"Compute {formula.equation_id}",
                    type="primary",
                    key=f"compute_{selected_set}_{formula.equation_id}",
                ):
                    result = _compute_equation_formula(
                        formula, selected_set, inputs, registry
                    )
                    if result is not None:
                        st.subheader("Result")
                        st.latex(formula.latex)
                        for key, val in result.items():
                            if isinstance(val, (int, float, np.floating)):
                                unit = _get_unit_for_key(key, entry, formula)
                                st.metric(key, f"{float(val):.6f}", unit)
                            elif isinstance(val, str):
                                st.text(f"{key}: {val}")

                        # Units display
                        st.caption("All results in CGS units.")

                # Preset examples
                if entry.examples:
                    st.subheader("Load Example")
                    for idx, ex in enumerate(entry.examples):
                        if st.button(
                            f"{ex.name}: {ex.description}",
                            key=f"example_{selected_set}_{idx}",
                        ):
                            _load_example_to_session(ex, selected_set, formula)

    # Summary of all formulas
    st.divider()
    st.subheader("All Formulas in This Set")
    for formula in entry.formulas:
        st.latex(formula.latex)
        st.caption(f"{formula.equation_id}: {formula.description}")


def _compute_equation_formula(
    formula: Any, set_id: str, inputs: Dict[str, Any], registry: EquationRegistry
) -> Optional[Dict[str, Any]]:
    """Compute a formula given user inputs.

    Args:
        formula: EquationFormula instance.
        set_id: Equation set identifier.
        inputs: User input values.
        registry: EquationRegistry instance.

    Returns:
        Computation result dictionary or None.
    """
    try:
        kwargs: Dict[str, Any] = {}
        point = inputs.get("point", (1.0, 0.0, 0.0))

        for var in formula.variables:
            raw = inputs.get(f"{var.name}_raw")
            if raw is not None:
                # Try to parse as function
                func = parse_function(raw)
                if func is not None:
                    kwargs[f"{var.name}_func"] = func
                    continue
                # Try as numeric
                try:
                    kwargs[var.name] = float(raw)
                    continue
                except ValueError:
                    pass

            val = inputs.get(var.name)
            if val is not None:
                kwargs[var.name] = val

        # Set-specific handling
        if set_id == "A":
            return _compute_set_a(formula, kwargs, point)
        elif set_id == "C":
            return _compute_set_c(formula, kwargs)
        elif set_id == "D":
            return _compute_set_d(formula, kwargs)
        elif set_id == "E":
            return _compute_set_e(formula, kwargs, point)
        elif set_id == "F":
            return _compute_set_f(formula, kwargs)
        elif set_id == "G":
            return _compute_set_g(formula, kwargs)
        elif set_id == "H":
            return _compute_set_h(formula, kwargs)
        elif set_id == "coulomb":
            return _compute_coulomb(kwargs)
        elif set_id == "net_charge":
            return _compute_net_charge(kwargs)
        elif set_id == "solenoidal":
            return _compute_solenoidal(formula, kwargs, point)
        elif set_id == "free_charge":
            return _compute_free_charge(formula, kwargs, point)
        else:
            st.warning(f"Computation for set {set_id} not yet implemented.")
            return None
    except Exception as e:
        st.error(f"Computation error: {e}")
        return None


def _compute_set_a(
    formula: Any, kwargs: Dict[str, Any], point: Tuple[float, float, float]
) -> Dict[str, Any]:
    """Compute Set A: B = curl(A) component."""
    h_val = 1e-6
    x, y, z = point

    def get_func(name: str) -> Callable[[float, float, float], float]:
        func = kwargs.get(f"{name}_func")
        if func is not None:
            return func
        val = kwargs.get(name, 0.0)
        try:
            return float(val)  # type: ignore[return-value]
        except TypeError:
            return lambda x, y, z: 0.0

    if formula.component == "x":
        H_f = get_func("H")
        G_f = get_func("G")
        dH_dy = (H_f(x, y + h_val, z) - H_f(x, y - h_val, z)) / (2 * h_val)
        dG_dz = (G_f(x, y, z + h_val) - G_f(x, y, z - h_val)) / (2 * h_val)
        return {"a": dH_dy - dG_dz}
    elif formula.component == "y":
        F_f = get_func("F")
        H_f = get_func("H")
        dF_dz = (F_f(x, y, z + h_val) - F_f(x, y, z - h_val)) / (2 * h_val)
        dH_dx = (H_f(x + h_val, y, z) - H_f(x - h_val, y, z)) / (2 * h_val)
        return {"b": dF_dz - dH_dx}
    elif formula.component == "z":
        G_f = get_func("G")
        F_f = get_func("F")
        dG_dx = (G_f(x + h_val, y, z) - G_f(x - h_val, y, z)) / (2 * h_val)
        dF_dy = (F_f(x, y + h_val, z) - F_f(x, y - h_val, z)) / (2 * h_val)
        return {"c": dG_dx - dF_dy}
    return {}


def _compute_set_c(formula: Any, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Compute Set C: Lorentz force component."""
    if formula.component == "x":
        return {
            "X": kwargs.get("b", 0.0) * kwargs.get("w", 0.0)
            - kwargs.get("c", 0.0) * kwargs.get("v", 0.0)
        }
    elif formula.component == "y":
        return {
            "Y": kwargs.get("c", 0.0) * kwargs.get("u", 0.0)
            - kwargs.get("a", 0.0) * kwargs.get("w", 0.0)
        }
    elif formula.component == "z":
        return {
            "Z": kwargs.get("a", 0.0) * kwargs.get("v", 0.0)
            - kwargs.get("b", 0.0) * kwargs.get("u", 0.0)
        }
    return {}


def _compute_set_d(formula: Any, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Compute Set D: B = H + 4*pi*M component."""
    four_pi = 4.0 * np.pi
    mu = kwargs.get("mu")
    if formula.component == "x":
        alpha = kwargs.get("alpha", 0.0)
        A = kwargs.get("A", 0.0)
        return {"a": mu * alpha if mu is not None else alpha + four_pi * A}
    elif formula.component == "y":
        beta = kwargs.get("beta", 0.0)
        B = kwargs.get("B", 0.0)
        return {"b": mu * beta if mu is not None else beta + four_pi * B}
    elif formula.component == "z":
        gamma = kwargs.get("gamma", 0.0)
        C = kwargs.get("C", 0.0)
        return {"c": mu * gamma if mu is not None else gamma + four_pi * C}
    return {}


def _compute_set_e(
    formula: Any, kwargs: Dict[str, Any], point: Tuple[float, float, float]
) -> Dict[str, Any]:
    """Compute Set E: curl(H) = 4*pi*J component."""
    four_pi = 4.0 * np.pi
    h_val = 1e-6
    x, y, z = point

    def get_func(name: str) -> Callable[[float, float, float], float]:
        func = kwargs.get(f"{name}_func")
        if func is not None:
            return func
        val = kwargs.get(name, 0.0)
        try:
            return float(val)  # type: ignore[return-value]
        except TypeError:
            return lambda x, y, z: 0.0

    if formula.component == "x":
        gamma_f = get_func("gamma")
        beta_f = get_func("beta")
        dgamma_dy = (gamma_f(x, y + h_val, z) - gamma_f(x, y - h_val, z)) / (2 * h_val)
        dbeta_dz = (beta_f(x, y, z + h_val) - beta_f(x, y, z - h_val)) / (2 * h_val)
        return {"4pi*u": dgamma_dy - dbeta_dz, "u": (dgamma_dy - dbeta_dz) / four_pi}
    elif formula.component == "y":
        alpha_f = get_func("alpha")
        gamma_f = get_func("gamma")
        dalpha_dz = (alpha_f(x, y, z + h_val) - alpha_f(x, y, z - h_val)) / (2 * h_val)
        dgamma_dx = (gamma_f(x + h_val, y, z) - gamma_f(x - h_val, y, z)) / (2 * h_val)
        return {"4pi*v": dalpha_dz - dgamma_dx, "v": (dalpha_dz - dgamma_dx) / four_pi}
    elif formula.component == "z":
        beta_f = get_func("beta")
        alpha_f = get_func("alpha")
        dbeta_dx = (beta_f(x + h_val, y, z) - beta_f(x - h_val, y, z)) / (2 * h_val)
        dalpha_dy = (alpha_f(x, y + h_val, z) - alpha_f(x, y - h_val, z)) / (2 * h_val)
        return {"4pi*w": dbeta_dx - dalpha_dy, "w": (dbeta_dx - dalpha_dy) / four_pi}
    return {}


def _compute_set_f(formula: Any, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Compute Set F: D = (K/4pi)*E component."""
    K = kwargs.get("K", 1.0)
    four_pi_inv = 1.0 / (4.0 * np.pi)
    if formula.component == "x":
        return {"f": four_pi_inv * K * kwargs.get("X", 0.0)}
    elif formula.component == "y":
        return {"g": four_pi_inv * K * kwargs.get("Y", 0.0)}
    elif formula.component == "z":
        return {"h": four_pi_inv * K * kwargs.get("Z", 0.0)}
    return {}


def _compute_set_g(formula: Any, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Compute Set G: J = sigma*E (Ohm's law) component."""
    C = kwargs.get("C", 0.0)
    if formula.component == "x":
        return {"p": C * kwargs.get("X", 0.0)}
    elif formula.component == "y":
        return {"q": C * kwargs.get("Y", 0.0)}
    elif formula.component == "z":
        return {"r": C * kwargs.get("Z", 0.0)}
    return {}


def _compute_set_h(formula: Any, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Compute Set H: J_total = J_cond + dD/dt component."""
    if formula.component == "x":
        return {"u": kwargs.get("p", 0.0) + kwargs.get("df_dt", 0.0)}
    elif formula.component == "y":
        return {"v": kwargs.get("q", 0.0) + kwargs.get("dg_dt", 0.0)}
    elif formula.component == "z":
        return {"w": kwargs.get("r", 0.0) + kwargs.get("dh_dt", 0.0)}
    return {}


def _compute_coulomb(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Compute Coulomb's law."""
    e = kwargs.get("e", 0.0)
    e_prime = kwargs.get("e_prime", 0.0)
    r = kwargs.get("r", 1.0)
    if r == 0:
        raise ValueError("Distance r cannot be zero")
    return {"F": e * e_prime / r**2}


def _compute_net_charge(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """Compute net charge."""
    m = kwargs.get("m", 0.0)
    n = kwargs.get("n", 0.0)
    return {"e": m - n}


def _compute_solenoidal(
    formula: Any, kwargs: Dict[str, Any], point: Tuple[float, float, float]
) -> Dict[str, Any]:
    """Compute solenoidal condition: divergence of current = 0."""
    h_val = 1e-6
    x, y, z = point

    def get_func(name: str) -> Callable[[float, float, float], float]:
        func = kwargs.get(f"{name}_func")
        if func is not None:
            return func
        val = kwargs.get(name, 0.0)
        try:
            return float(val)  # type: ignore[return-value]
        except TypeError:
            return lambda x, y, z: 0.0

    u_f = get_func("u")
    v_f = get_func("v")
    w_f = get_func("w")
    du_dx = (u_f(x + h_val, y, z) - u_f(x - h_val, y, z)) / (2 * h_val)
    dv_dy = (v_f(x, y + h_val, z) - v_f(x, y - h_val, z)) / (2 * h_val)
    dw_dz = (w_f(x, y, z + h_val) - w_f(x, y, z - h_val)) / (2 * h_val)
    return {"div_J": du_dx + dv_dy + dw_dz}


def _compute_free_charge(
    formula: Any, kwargs: Dict[str, Any], point: Tuple[float, float, float]
) -> Dict[str, Any]:
    """Compute free charge density: divergence of D field."""
    h_val = 1e-6
    x, y, z = point

    def get_func(name: str) -> Callable[[float, float, float], float]:
        func = kwargs.get(f"{name}_func")
        if func is not None:
            return func
        val = kwargs.get(name, 0.0)
        try:
            return float(val)  # type: ignore[return-value]
        except TypeError:
            return lambda x, y, z: 0.0

    f_f = get_func("f")
    g_f = get_func("g")
    h_f = get_func("h")
    df_dx = (f_f(x + h_val, y, z) - f_f(x - h_val, y, z)) / (2 * h_val)
    dg_dy = (g_f(x, y + h_val, z) - g_f(x, y - h_val, z)) / (2 * h_val)
    dh_dz = (h_f(x, y, z + h_val) - h_f(x, y, z - h_val)) / (2 * h_val)
    return {"rho": df_dx + dg_dy + dh_dz}


def _get_unit_for_key(key: str, entry: EquationSetEntry, formula: Any) -> str:
    """Get the CGS unit for a result key."""
    for var in entry.variables.values():
        if var.name == key:
            return var.units
    return "CGS"


def _load_example_to_session(example: PresetExample, set_id: str, formula: Any) -> None:
    """Load a preset example into session state inputs."""
    st.info(f"Example: {example.name} -- {example.description}")
    for key, val in example.inputs.items():
        if callable(val):
            st.code(f"{key} = <function>")
        else:
            st.code(f"{key} = {val}")


# ═══════════════════════════════════════════════════════════════════
# PAGE 2: DERIVATIVES
# ═══════════════════════════════════════════════════════════════════


def _render_derivatives() -> None:
    """Render the Derivatives page."""
    st.title("Partial Derivatives")
    st.caption("Numerical and symbolic differentiation of scalar fields")

    st.info(
        "Enter a SymPy-parseable expression for f(x, y, z). "
        "Supported operations: +, -, *, /, **, sin, cos, exp, log, sqrt, etc."
    )

    # Function input
    func_expr = st.text_area(
        "f(x, y, z) =",
        value="x**2 + y**2 + z**2",
        height=60,
        key="deriv_func",
    )

    # Evaluation point
    st.subheader("Evaluation Point (cm)")
    pt_cols = st.columns(3)
    with pt_cols[0]:
        px = st.number_input("x", value=1.0, key="deriv_x")
    with pt_cols[1]:
        py = st.number_input("y", value=2.0, key="deriv_y")
    with pt_cols[2]:
        pz = st.number_input("z", value=3.0, key="deriv_z")

    point = (px, py, pz)

    # Step size
    h_val = st.number_input("Step size (h)", value=1e-6, format="%.1e", key="deriv_h")

    # Parse function
    func = parse_function(func_expr)
    if func is None:
        st.error("Could not parse the expression. Check syntax and try again.")
        return

    # Compute button
    if st.button("Compute Derivatives", type="primary", key="deriv_compute"):
        st.divider()

        # First-order partial derivatives
        st.subheader("First-Order Partial Derivatives")
        st.latex(
            r"\nabla f = \left(\frac{\partial f}{\partial x}, "
            r"\frac{\partial f}{\partial y}, \frac{\partial f}{\partial z}\right)"
        )

        results: Dict[str, Any] = {}
        for var in ["x", "y", "z"]:
            result = partial_derivative(func, point, variable=var, h=h_val)
            results[f"df/d{var}"] = result.value

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("df/dx", f"{results['df/dx']:.6f}")
        with col2:
            st.metric("df/dy", f"{results['df/dy']:.6f}")
        with col3:
            st.metric("df/dz", f"{results['df/dz']:.6f}")

        # Gradient via vector_operators
        st.subheader("Gradient (vector_operators)")
        gx, gy, gz = gradient(func, px, py, pz, h=h_val)
        st.latex(
            r"\nabla f = "
            + f"{gx:.6f}\\,\\hat{{i}} + {gy:.6f}\\,\\hat{{j}} + {gz:.6f}\\,\\hat{{k}}"
        )

        # Second-order partial derivatives
        st.subheader("Second-Order Partial Derivatives")
        for var in ["x", "y", "z"]:
            result = second_partial_derivative(func, point, variable=var, h=h_val)
            results[f"d2f/d{var}2"] = result.value

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("d2f/dx2", f"{results['d2f/dx2']:.6f}")
        with col2:
            st.metric("d2f/dy2", f"{results['d2f/dy2']:.6f}")
        with col3:
            st.metric("d2f/dz2", f"{results['d2f/dz2']:.6f}")

        # Mixed partials
        st.subheader("Mixed Partial Derivatives")
        st.latex(
            r"\frac{\partial^2 f}{\partial x \partial y}, \quad "
            r"\frac{\partial^2 f}{\partial x \partial z}, \quad "
            r"\frac{\partial^2 f}{\partial y \partial z}"
        )
        for v1, v2 in [("x", "y"), ("x", "z"), ("y", "z")]:
            result = mixed_partial_derivative(func, point, var1=v1, var2=v2)
            results[f"d2f/d{v1}d{v2}"] = result.value
            st.metric(
                f"d2f/d{v1}d{v2}",
                f"{results[f'd2f/d{v1}d{v2}']:.6f}",
            )

        # Hessian
        st.subheader("Hessian Matrix")
        st.latex(
            r"H(f) = \begin{pmatrix}"
            r"\frac{\partial^2 f}{\partial x^2} & "
            r"\frac{\partial^2 f}{\partial x \partial y} & "
            r"\frac{\partial^2 f}{\partial x \partial z} \\"
            r"\frac{\partial^2 f}{\partial y \partial x} & "
            r"\frac{\partial^2 f}{\partial y^2} & "
            r"\frac{\partial^2 f}{\partial y \partial z} \\"
            r"\frac{\partial^2 f}{\partial z \partial x} & "
            r"\frac{\partial^2 f}{\partial z \partial y} & "
            r"\frac{\partial^2 f}{\partial z^2}"
            r"\end{pmatrix}"
        )

        hess = hessian(func, point, h=h_val)
        st.latex(
            r"H(f) = \begin{pmatrix} "
            f"{hess[0,0]:.6f} & {hess[0,1]:.6f} & {hess[0,2]:.6f} \\\\ "
            f"{hess[1,0]:.6f} & {hess[1,1]:.6f} & {hess[1,2]:.6f} \\\\ "
            f"{hess[2,0]:.6f} & {hess[2,1]:.6f} & {hess[2,2]:.6f} "
            r"\end{pmatrix}"
        )

        # SymPy comparison
        if st.session_state.sympy_enabled and SYMPY_AVAILABLE:
            st.divider()
            st.subheader("SymPy Symbolic Comparison")

            sym_grad = sympy_gradient(func_expr, point)
            if sym_grad:
                st.latex(r"\text{Symbolic Gradient:}")
                for label, val in sym_grad.items():
                    st.latex(f"{label} = {val}")

                # Check numerical vs symbolic agreement
                st.caption("Numerical vs Symbolic comparison:")
                for var in ["x", "y", "z"]:
                    num_val = results[f"df/d{var}"]
                    sym_key = f"df/d{var}"
                    if sym_key in sym_grad:
                        sym_val_str = sym_grad[sym_key].split(" = ")[-1]
                        try:
                            sym_val = float(sym_val_str)
                            err = abs(num_val - sym_val)
                            status = "PASS" if err < 1e-4 else "WARN"
                            st.text(
                                f"  df/d{var}: numerical={num_val:.6f}, "
                                f"symbolic={sym_val:.6f}, error={err:.2e} [{status}]"
                            )
                        except ValueError:
                            pass

            sym_hess = sympy_hessian(func_expr, point)
            if sym_hess:
                st.latex(r"\text{Symbolic Hessian:}")
                st.latex(sym_hess)


# ═══════════════════════════════════════════════════════════════════
# PAGE 3: INTEGRAL CALCULUS
# ═══════════════════════════════════════════════════════════════════


def _render_integral_calculus() -> None:
    """Render the Integral Calculus page."""
    st.title("Integral Calculus")
    st.caption("Volume, surface, and line integrals of scalar and vector fields")

    integral_type = st.sidebar.radio(
        "Integral Type",
        ["Volume Integral", "Surface Integral (Sphere)", "Line Integral (Circle)"],
        key="integral_type",
    )

    if integral_type == "Volume Integral":
        _render_volume_integral()
    elif integral_type == "Surface Integral (Sphere)":
        _render_surface_integral()
    else:
        _render_line_integral()


def _render_volume_integral() -> None:
    """Render volume integral calculator."""
    st.subheader("Volume Integral")
    st.latex(r"I = \iiint_V f(x, y, z) \, dx \, dy \, dz")

    st.info(
        "Computes the triple integral of a scalar field over a rectangular "
        "volume using scipy.integrate.nquad."
    )

    func_expr = st.text_area("f(x, y, z) =", value="1.0", height=60, key="vol_func")

    st.subheader("Integration Bounds (cm)")
    col1, col2 = st.columns(2)
    with col1:
        st.caption("x bounds")
        x_min = st.number_input("x_min", value=-5.0, key="vol_xmin")
        x_max = st.number_input("x_max", value=5.0, key="vol_xmax")
    with col2:
        st.caption("y bounds")
        y_min = st.number_input("y_min", value=-5.0, key="vol_ymin")
        y_max = st.number_input("y_max", value=5.0, key="vol_ymax")

    st.caption("z bounds")
    z_min = st.number_input("z_min", value=-5.0, key="vol_zmin")
    z_max = st.number_input("z_max", value=5.0, key="vol_zmax")

    if st.button("Compute Volume Integral", type="primary", key="vol_compute"):
        func = parse_function(func_expr)
        if func is None:
            st.error("Could not parse the expression.")
            return

        if x_max <= x_min or y_max <= y_min or z_max <= z_min:
            st.error("Upper bounds must be greater than lower bounds.")
            return

        try:
            result = volume_integral_scalar(
                func, (x_min, x_max), (y_min, y_max), (z_min, z_max)
            )
            st.divider()
            st.subheader("Result")
            st.metric("Volume Integral", f"{result:.6f}")
            st.latex(
                r"\iiint_{"
                + f"{x_min}^{{{x_max}}} "
                + f"{y_min}^{{{y_max}}} "
                + f"{z_min}^{{{z_max}}}"
                + r"} "
                + f"{func_expr}"
                + r" \, dx \, dy \, dz = "
                + f"{result:.6f}"
            )
            st.caption("Result in CGS units (depends on integrand units * cm3).")
        except Exception as e:
            st.error(f"Integration error: {e}")


def _render_surface_integral() -> None:
    """Render surface integral calculator (sphere)."""
    st.subheader("Surface Integral over a Sphere")
    st.latex(r"\Phi = \oiint_S \mathbf{F} \cdot \mathbf{n} \, dA")

    st.info(
        "Computes the flux of a vector field through a spherical surface "
        "of radius R centered at the origin."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        fx_expr = st.text_area("Fx(x,y,z) =", value="x", height=60, key="surf_fx")
    with col2:
        fy_expr = st.text_area("Fy(x,y,z) =", value="y", height=60, key="surf_fy")
    with col3:
        fz_expr = st.text_area("Fz(x,y,z) =", value="z", height=60, key="surf_fz")

    radius = st.number_input("Sphere Radius R (cm)", value=10.0, key="surf_radius")

    if st.button("Compute Surface Integral", type="primary", key="surf_compute"):
        fx = parse_function(fx_expr)
        fy = parse_function(fy_expr)
        fz = parse_function(fz_expr)
        if any(f is None for f in [fx, fy, fz]):
            st.error("Could not parse one or more expressions.")
            return

        if radius <= 0:
            st.error("Radius must be positive.")
            return

        try:
            result = surface_integral_sphere(fx, fy, fz, radius)
            st.divider()
            st.subheader("Result")
            st.metric("Surface Flux", f"{result:.6f}")
            st.latex(
                r"\Phi = \oiint_{r="
                + f"{radius}"
                + r"} "
                + r"\mathbf{F} \cdot \mathbf{n} \, dA = "
                + f"{result:.6f}"
            )
            st.caption("Result in CGS units.")
        except Exception as e:
            st.error(f"Integration error: {e}")


def _render_line_integral() -> None:
    """Render line integral calculator (circle)."""
    st.subheader("Line Integral around a Circle")
    st.latex(r"W = \oint_C \mathbf{F} \cdot d\mathbf{l}")

    st.info(
        "Computes the circulation of a vector field around a circular path "
        "in the xy-plane, centered at the origin."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        fx_expr = st.text_area("Fx(x,y,z) =", value="-y", height=60, key="line_fx")
    with col2:
        fy_expr = st.text_area("Fy(x,y,z) =", value="x", height=60, key="line_fy")
    with col3:
        fz_expr = st.text_area("Fz(x,y,z) =", value="0", height=60, key="line_fz")

    radius = st.number_input("Circle Radius R (cm)", value=5.0, key="line_radius")

    if st.button("Compute Line Integral", type="primary", key="line_compute"):
        fx = parse_function(fx_expr)
        fy = parse_function(fy_expr)
        fz = parse_function(fz_expr)
        if any(f is None for f in [fx, fy, fz]):
            st.error("Could not parse one or more expressions.")
            return

        if radius <= 0:
            st.error("Radius must be positive.")
            return

        try:
            result = line_integral_circle(fx, fy, fz, radius)
            st.divider()
            st.subheader("Result")
            st.metric("Line Integral (Circulation)", f"{result:.6f}")
            st.latex(
                r"W = \oint_{r="
                + f"{radius}"
                + r"} "
                + r"\mathbf{F} \cdot d\mathbf{l} = "
                + f"{result:.6f}"
            )
            st.caption("Result in CGS units.")
        except Exception as e:
            st.error(f"Integration error: {e}")


# ═══════════════════════════════════════════════════════════════════
# PAGE 4: THEOREM VERIFICATION
# ═══════════════════════════════════════════════════════════════════


def _render_theorem_verification() -> None:
    """Render the Theorem Verification page."""
    st.title("Theorem Verification")
    st.caption("Verify the fundamental theorems of vector calculus numerically")

    theorem_type = st.sidebar.radio(
        "Theorem",
        ["Divergence Theorem", "Stokes' Theorem", "Green's Theorem"],
        key="theorem_type",
    )

    if theorem_type == "Divergence Theorem":
        _render_divergence_theorem()
    elif theorem_type == "Stokes' Theorem":
        _render_stokes_theorem()
    else:
        _render_greens_theorem()


def _render_divergence_theorem() -> None:
    """Render Divergence Theorem verification."""
    st.subheader("Divergence Theorem (Gauss's Theorem)")
    st.latex(
        r"\iiint_V (\nabla \cdot \mathbf{F}) \, dV = "
        r"\oiint_S \mathbf{F} \cdot \mathbf{n} \, dA"
    )

    st.info(
        "The volume integral of the divergence of F equals the surface flux "
        "of F through the boundary. We verify this for a rectangular box."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        fx_expr = st.text_area("Fx(x,y,z) =", value="x", height=60, key="div_fx")
    with col2:
        fy_expr = st.text_area("Fy(x,y,z) =", value="y", height=60, key="div_fy")
    with col3:
        fz_expr = st.text_area("Fz(x,y,z) =", value="z", height=60, key="div_fz")

    st.subheader("Box Bounds (cm)")
    bcol1, bcol2 = st.columns(2)
    with bcol1:
        st.caption("x bounds")
        x_min = st.number_input("x_min", value=0.0, key="div_xmin")
        x_max = st.number_input("x_max", value=1.0, key="div_xmax")
    with bcol2:
        st.caption("y bounds")
        y_min = st.number_input("y_min", value=0.0, key="div_ymin")
        y_max = st.number_input("y_max", value=1.0, key="div_ymax")

    st.caption("z bounds")
    z_min = st.number_input("z_min", value=0.0, key="div_zmin")
    z_max = st.number_input("z_max", value=1.0, key="div_zmax")

    tolerance = st.number_input(
        "Verification Tolerance", value=1e-4, format="%.1e", key="div_tol"
    )

    if st.button("Verify Divergence Theorem", type="primary", key="div_verify"):
        fx = parse_function(fx_expr)
        fy = parse_function(fy_expr)
        fz = parse_function(fz_expr)
        if any(f is None for f in [fx, fy, fz]):
            st.error("Could not parse one or more expressions.")
            return

        if x_max <= x_min or y_max <= y_min or z_max <= z_min:
            st.error("Upper bounds must be greater than lower bounds.")
            return

        try:
            result = verify_divergence_theorem(
                fx,
                fy,
                fz,
                ((x_min, x_max), (y_min, y_max), (z_min, z_max)),
                tolerance=tolerance,
            )

            st.divider()
            st.subheader("Verification Results")

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric(
                    "Volume Integral (LHS)",
                    f"{result['volume_integral']:.6f}",
                    "∭ div(F) dV",
                )
            with col_b:
                st.metric(
                    "Surface Integral (RHS)",
                    f"{result['surface_integral']:.6f}",
                    "∯ F.n dA",
                )
            with col_c:
                st.metric(
                    "Difference",
                    f"{result['difference']:.2e}",
                    "|LHS - RHS|",
                )

            st.latex(r"\text{Relative Error} = " + f"{result['relative_error']:.2e}")

            if result["verified"]:
                st.success(
                    f"DIVERGENCE THEOREM VERIFIED "
                    f"(relative error {result['relative_error']:.2e} < {tolerance})"
                )
            else:
                st.error(
                    f"VERIFICATION FAILED "
                    f"(relative error {result['relative_error']:.2e} >= {tolerance})"
                )
        except Exception as e:
            st.error(f"Verification error: {e}")


def _render_stokes_theorem() -> None:
    """Render Stokes' Theorem verification."""
    st.subheader("Stokes' Theorem")
    st.latex(
        r"\oint_C \mathbf{F} \cdot d\mathbf{l} = "
        r"\iint_S (\nabla \times \mathbf{F}) \cdot \mathbf{n} \, dA"
    )

    st.info(
        "The line integral of F around a closed curve equals the surface "
        "integral of curl(F) over any surface bounded by that curve. "
        "We verify this for a disk of radius R in the xy-plane."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        fx_expr = st.text_area("Fx(x,y,z) =", value="-y", height=60, key="stokes_fx")
    with col2:
        fy_expr = st.text_area("Fy(x,y,z) =", value="x", height=60, key="stokes_fy")
    with col3:
        fz_expr = st.text_area("Fz(x,y,z) =", value="0", height=60, key="stokes_fz")

    radius = st.number_input("Disk Radius R (cm)", value=1.0, key="stokes_radius")

    if st.button("Verify Stokes' Theorem", type="primary", key="stokes_verify"):
        fx = parse_function(fx_expr)
        fy = parse_function(fy_expr)
        fz = parse_function(fz_expr)
        if any(f is None for f in [fx, fy, fz]):
            st.error("Could not parse one or more expressions.")
            return

        if radius <= 0:
            st.error("Radius must be positive.")
            return

        try:
            # Define parameterized disk surface: r(u,v) = (u*cos(v), u*sin(v), 0)
            import math

            def surface_param(u: float, v: float) -> Tuple[float, float, float]:
                return (u * math.cos(v), u * math.sin(v), 0.0)

            # Define boundary curve: circle at radius R
            def boundary_curve(t: float) -> Tuple[float, float, float]:
                return (
                    radius * math.cos(t),
                    radius * math.sin(t),
                    0.0,
                )

            result = verify_stokes_theorem(
                fx,
                fy,
                fz,
                surface_param,
                (0, radius),
                (0, 2 * math.pi),
                boundary_curve,
                (0, 2 * math.pi),
            )

            st.divider()
            st.subheader("Verification Results")

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric(
                    "Line Integral (LHS)",
                    f"{result['line_integral']:.6f}",
                    "∮ F.dl",
                )
            with col_b:
                st.metric(
                    "Surface Integral (RHS)",
                    f"{result['surface_integral']:.6f}",
                    "∬ (∇×F).n dA",
                )
            with col_c:
                st.metric(
                    "Difference",
                    f"{result['difference']:.2e}",
                    "|LHS - RHS|",
                )

            st.latex(r"\text{Relative Error} = " + f"{result['relative_error']:.2e}")

            if result["verified"]:
                st.success(
                    f"STOKES' THEOREM VERIFIED "
                    f"(relative error {result['relative_error']:.2e})"
                )
            else:
                st.error(
                    f"VERIFICATION FAILED "
                    f"(relative error {result['relative_error']:.2e})"
                )
        except Exception as e:
            st.error(f"Verification error: {e}")


def _render_greens_theorem() -> None:
    """Render Green's Theorem verification."""
    st.subheader("Green's Theorem")
    st.latex(
        r"\oint_C (P \, dx + Q \, dy) = "
        r"\iint_D \left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right) dA"
    )

    st.info(
        "Green's theorem relates a line integral around a simple closed curve "
        "to a double integral over the plane region it bounds. We verify this "
        "for a circular region of radius R."
    )

    col1, col2 = st.columns(2)
    with col1:
        p_expr = st.text_area("P(x,y) =", value="-y", height=60, key="green_p")
    with col2:
        q_expr = st.text_area("Q(x,y) =", value="x", height=60, key="green_q")

    radius = st.number_input("Circle Radius R (cm)", value=1.0, key="green_radius")

    if st.button("Verify Green's Theorem", type="primary", key="green_verify"):
        p_func = parse_function(p_expr)
        q_func = parse_function(q_expr)
        if any(f is None for f in [p_func, q_func]):
            st.error("Could not parse one or more expressions.")
            return

        if radius <= 0:
            st.error("Radius must be positive.")
            return

        try:
            result = verify_greens_theorem(p_func, q_func, radius)

            st.divider()
            st.subheader("Verification Results")

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric(
                    "Line Integral (LHS)",
                    f"{result['line_integral']:.6f}",
                    "∮ Pdx + Qdy",
                )
            with col_b:
                st.metric(
                    "Double Integral (RHS)",
                    f"{result['double_integral']:.6f}",
                    "∬∬(dQ/dx - dP/dy)dA",
                )
            with col_c:
                st.metric(
                    "Difference",
                    f"{result['difference']:.2e}",
                    "|LHS - RHS|",
                )

            st.latex(r"\text{Relative Error} = " + f"{result['relative_error']:.2e}")

            if result["verified"]:
                st.success(
                    f"GREEN'S THEOREM VERIFIED "
                    f"(relative error {result['relative_error']:.2e})"
                )
            else:
                st.error(
                    f"VERIFICATION FAILED "
                    f"(relative error {result['relative_error']:.2e})"
                )
        except Exception as e:
            st.error(f"Verification error: {e}")


# ═══════════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════════


def main() -> None:
    """Main application entry point."""
    # Sidebar header
    st.sidebar.title("Maxwell Calculus Calculator")
    st.sidebar.caption("Based on Maxwell's Treatise (1873)")

    # Page selector
    page = st.sidebar.radio(
        "Navigation",
        PAGES,
        index=PAGES.index(st.session_state.page),
        key="page_selector",
    )
    st.session_state.page = page

    # Settings
    st.sidebar.divider()
    st.sidebar.subheader("Settings")

    sympy_status = "Available" if SYMPY_AVAILABLE else "Not installed"
    st.sidebar.text(f"SymPy: {sympy_status}")

    st.session_state.sympy_enabled = st.sidebar.checkbox(
        "Enable SymPy symbolic mode",
        value=st.session_state.sympy_enabled and SYMPY_AVAILABLE,
        disabled=not SYMPY_AVAILABLE,
        key="sympy_toggle",
    )

    # Registry info
    st.sidebar.divider()
    st.sidebar.subheader("Equation Catalog")
    summary = REGISTRY.summary()
    with st.sidebar.expander("View Catalog Summary"):
        st.text(summary)

    # Render selected page
    if page == "Equation Calculator":
        _render_equation_calculator(REGISTRY)
    elif page == "Derivatives":
        _render_derivatives()
    elif page == "Integral Calculus":
        _render_integral_calculus()
    elif page == "Theorem Verification":
        _render_theorem_verification()

    # Footer
    st.divider()
    st.caption(
        "Maxwell Calculus Calculator | "
        "All computations in CGS units | "
        "Based on Maxwell's Treatise on Electricity and Magnetism, 1873"
    )


if __name__ == "__main__":
    main()

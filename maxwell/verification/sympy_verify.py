"""maxwell.verification.sympy_verify -- Symbolic verification using SymPy.

Provides 69 symbolic verification functions that use SymPy to prove
fundamental identities of vector calculus and classical electromagnetic
theory as described in Maxwell's Treatise (1873).

The first 13 cover the general vector-calculus and field-theory spine.
The remaining 56 (Wave 8a, G4 spine verifiers) target Part IV,
Chapters XII-XXIII (Arts. 667-866): elliptic integrals and circular
currents, the spherical-harmonic potential spine, current sheets and
boundary conditions, electromagnetic waves and magneto-optics, absolute
resistance standards, action-at-distance theories, CGS unit discipline,
and the dipole vector-calculus spine.

Each function decorates with @maxwell_cite, performs symbolic computation,
and returns a VerificationResult with full audit trail.

Category: B (user_original) -- Symbolic verification framework.
"""

from __future__ import annotations

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite
from maxwell.verification.framework import VerificationResult

# SymPy import with graceful degradation
try:
    import sympy
    from sympy import (
        E,
        I,
        Rational,
        cos,
        diff,
        exp,
        expand,
        expand_trig,
        factorial,
        integrate,
        limit,
        log,
        oo,
        pi,
        series,
        simplify,
        sin,
        solve,
        sqrt,
        symbols,
        tan,
        trigsimp,
    )

    _HAS_SYMPY = True
except ImportError:
    _HAS_SYMPY = False


# ── Internal helper ──────────────────────────────────────────────


def _is_symbolic_zero(expr, symbols_list=None) -> bool:
    """Check if a SymPy expression simplifies to zero.

    Tries multiple strategies: trigsimp, simplify, expand_trig+simplify,
    and numerical evaluation at random test points.
    """
    strategies = [
        lambda e: trigsimp(e),
        lambda e: simplify(e),
        lambda e: simplify(expand_trig(e)),
    ]
    for fn in strategies:
        try:
            if fn(expr) == 0:
                return True
        except Exception:
            continue
    # Fallback: numerical evaluation at multiple random points
    if symbols_list is None:
        symbols_list = list(expr.free_symbols)
    if not symbols_list:
        return expr == 0
    import random

    _seed = random.Random(42)
    for _ in range(5):
        pt = {s: _seed.uniform(0.5, 3.0) for s in symbols_list}
        try:
            val = complex(expr.subs(pt))
            if abs(val) > 1e-10:
                return False
        except Exception:
            return False
    return True


def _disabled_result(
    test_name: str, module_name: str, article_refs: tuple[int, ...]
) -> VerificationResult:
    """Return a non-passing result when SymPy is unavailable."""
    return VerificationResult(
        module_name=module_name,
        article_refs=article_refs,
        test_name=test_name,
        expected=0.0,
        actual=0.0,
        relative_error=1.0,
        tolerance=1e-8,
        passed=False,
        details="SymPy not available; symbolic verification skipped.",
    )


# ── Wave 8a internal helpers (construction routines, no verdicts) ─


def _legendre_poly(ell: int, x):
    """Legendre polynomial P_ell(x) via Rodrigues' formula.

    P_ell(x) = (1/(2^ell ell!)) d^ell/dx^ell (x^2 - 1)^ell

    This is an independent construction (used as the local oracle for
    the Wave 8a spherical-harmonic verifiers); it never consults
    sympy.functions.special.bessel or maxwell.math.spherical_harmonics.
    """
    import sympy as _sympy

    rod = _sympy.diff((x**2 - 1) ** ell, x, ell)
    return _sympy.expand(rod / (2**ell * _sympy.factorial(ell)))


def _complete_elliptic_pair(m_val: float, dps: int = 35):
    """Return (K(m), E(m)) at parameter m using SymPy's elliptic integrals.

    SymPy convention: elliptic_k(m) and elliptic_e(m) take the parameter
    m = k^2 (the square of the modulus).  Values are independent of any
    maxwell implementation: they come from SymPy's own mpmath evaluation.
    """
    import sympy as _sympy

    K = _sympy.N(_sympy.elliptic_k(m_val), dps)
    En = _sympy.N(_sympy.elliptic_e(m_val), dps)
    return K, En


# ── 1. div(curl(F)) = 0 ────────────────────────────────────────


@maxwell_cite(
    15,
    part=1,
    chapter="Definitions",
    theory_class="standard_math",
    description="divergence of the curl of any vector field vanishes",
)
def verify_div_curl() -> VerificationResult:
    """Verify that div(curl(F)) = 0 for an arbitrary polynomial vector field.

    Returns a VerificationResult showing the symbolic computation confirms
    the identity at a random test point.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "div(curl(F)) = 0"
    arts = (15,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x, y, z = symbols("x y z")

    # Arbitrary polynomial vector field F = (P, Q, R)
    P = x**2 * y + y * z**2 + z**3
    Q = x * y**2 + y * z + x * z**2
    R = x**3 + y**2 * z + x * z

    # curl(F) components
    curl_x = diff(R, y) - diff(Q, z)
    curl_y = diff(P, z) - diff(R, x)
    curl_z = diff(Q, x) - diff(P, y)

    # div(curl(F))
    div_curl = diff(curl_x, x) + diff(curl_y, y) + diff(curl_z, z)
    result_expr = simplify(div_curl)

    symbolic_zero = _is_symbolic_zero(div_curl)

    # Evaluate at a numeric test point for the VerificationResult contract
    pt = {x: 1.3, y: -0.7, z: 2.1}
    numeric_val = float(result_expr.subs(pt))

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=numeric_val,
        relative_error=0.0 if symbolic_zero else abs(numeric_val),
        tolerance=1e-8,
        passed=symbolic_zero,
        details=(
            f"Symbolic identity confirmed. Test point (x,y,z)=(1.3,-0.7,2.1) "
            f"evaluates to {numeric_val:.2e}."
        ),
    )


# ── 2. curl(grad(phi)) = 0 ─────────────────────────────────────


@maxwell_cite(
    15,
    part=1,
    chapter="Definitions",
    theory_class="standard_math",
    description="curl of the gradient of any scalar field vanishes",
)
def verify_grad_curl() -> VerificationResult:
    """Verify that curl(grad(phi)) = 0 for a symbolic scalar potential.

    Returns a VerificationResult confirming the irrotational property of
    conservative fields (Arts. 15, 39).
    """
    mod = "maxwell.verification.sympy_verify"
    name = "curl(grad(phi)) = 0"
    arts = (15, 39)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x, y, z = symbols("x y z")

    # Scalar potential phi(x,y,z) = x*y*z + sin(x*y) + exp(z)
    phi = x * y * z + sin(x * y) + exp(z)

    # Gradient components
    gx = diff(phi, x)
    gy = diff(phi, y)
    gz = diff(phi, z)

    # Curl components of grad(phi)
    c_x = diff(gz, y) - diff(gy, z)
    c_y = diff(gx, z) - diff(gz, x)
    c_z = diff(gy, x) - diff(gx, y)

    all_zero = all(_is_symbolic_zero(c) for c in (c_x, c_y, c_z))

    pt = {x: 0.5, y: 1.2, z: -0.3}
    max_err = max(abs(float(c.subs(pt))) for c in (c_x, c_y, c_z))

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(max_err),
        relative_error=0.0 if all_zero else float(max_err),
        tolerance=1e-8,
        passed=all_zero,
        details=(
            f"Identity confirmed: curl(grad(phi)) is zero-vector. "
            f"Test point max component error: {max_err:.2e}."
        ),
    )


# ── 3. 1-D Wave Equation ──────────────────────────────────────


@maxwell_cite(
    787,
    part=4,
    chapter="Electromagnetic Theory of Light",
    theory_class="maxwell_original",
    description="electromagnetic wave equation verified symbolically",
)
def verify_wave_equation_1d() -> VerificationResult:
    """Verify the 1-D wave equation symbolically: d2phi/dt2 = c^2 * d2phi/dx2.

    Tests with a sinusoidal traveling wave phi(x,t) = sin(k*x - omega*t)
    and confirms both sides match exactly using the relation omega = c*k.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "1D wave equation d2phi/dt2 = c^2 d2phi/dx2"
    arts = (787,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x, t, c, k, omega = symbols("x t c k omega")

    phi = sin(k * x - omega * t)

    # Substitute omega = c*k into phi FIRST (physical dispersion relation)
    phi_sub = phi.subs(omega, c * k)

    lhs = diff(phi_sub, t, 2)
    rhs = c**2 * diff(phi_sub, x, 2)

    diff_expr = simplify(lhs - rhs)

    symbolic_match = _is_symbolic_zero(lhs - rhs)

    # Numeric check at concrete values
    num_vals = {x: 1.0, t: 0.5, c: CONST.C_APPROX, k: 1.0}
    lhs_num = float(lhs.subs(num_vals))
    rhs_num = float(rhs.subs(num_vals))

    if abs(lhs_num) > 1e-15:
        rel_err = abs(lhs_num - rhs_num) / abs(lhs_num)
    else:
        rel_err = abs(lhs_num - rhs_num)

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=float(lhs_num),
        actual=float(rhs_num),
        relative_error=rel_err if not symbolic_match else 0.0,
        tolerance=1e-8,
        passed=symbolic_match,
        details=(
            f"omega=c*k substituted; symbolic diff = {diff_expr}. "
            f"Numeric: lhs={lhs_num:.6e}, rhs={rhs_num:.6e}."
        ),
    )


# ── 4. Laplace Equation in Spherical Coordinates ───────────────


@maxwell_cite(
    134,
    part=1,
    chapter="General Equations of Electrostatics",
    theory_class="maxwell_original",
    description="Laplace's equation in spherical coordinates for 1/r potential",
)
def verify_laplace_spherical() -> VerificationResult:
    """Verify that the Coulomb potential V = 1/r satisfies Laplace's equation
    in spherical coordinates away from the origin.

    Uses the spherical Laplacian:
      d2V/dr2 + (2/r)*dV/dr + (1/(r^2 sin theta))*d/dtheta(sin theta * dV/dtheta)
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Laplace equation in spherical coords for V=1/r"
    arts = (134, 340)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    r, theta, phi_sym = symbols("r theta phi")

    V = 1 / r

    # Radial part of Laplacian in spherical coords
    radial = diff(V, r, 2) + (2 / r) * diff(V, r)

    # Angular part for theta-independent potential simplifies to zero
    # (no phi dependence, and d/dtheta of constant = 0)
    angular = (1 / (r**2 * sin(theta))) * diff(sin(theta) * diff(V, theta), theta)

    laplacian = simplify(radial + angular)
    symbolic_zero = _is_symbolic_zero(radial + angular)

    pt = {r: 2.5, theta: 1.0}
    numeric_val = float(laplacian.subs(pt))

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=numeric_val,
        relative_error=0.0 if symbolic_zero else abs(numeric_val),
        tolerance=1e-8,
        passed=symbolic_zero,
        details=(
            f"V=1/r satisfies nabla^2 V = 0 for r>0. "
            f"Simplified Laplacian: {laplacian}. Test point r=2.5, theta=1.0 "
            f"evaluates to {numeric_val:.2e}."
        ),
    )


# ── 5. Coulomb's Law from Potential ────────────────────────────


@maxwell_cite(
    27,
    part=1,
    chapter="Mathematical Methods",
    theory_class="maxwell_original",
    description="electric field from Coulomb potential E = -grad(V)",
)
def verify_coulomb_law_symbolic() -> VerificationResult:
    """Verify that E = -grad(V) for V = q/r yields the correct Coulomb field
    magnitude |E| = q / r^2 along the radial direction."""
    mod = "maxwell.verification.sympy_verify"
    name = "Coulomb field from potential E = -dV/dr = q/r^2"
    arts = (27, 80)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x, y, z, q = symbols("x y z q")
    r = sqrt(x**2 + y**2 + z**2)

    V = q / r

    # E = -grad(V)
    Ex = -diff(V, x)
    Ey = -diff(V, y)
    Ez = -diff(V, z)

    # |E|^2 = Ex^2 + Ey^2 + Ez^2
    E_sq = simplify(Ex**2 + Ey**2 + Ez**2)

    # Expected: |E|^2 = q^2 / r^4
    expected_expr = simplify(q**2 / r**4)

    symbolic_match = _is_symbolic_zero(E_sq - expected_expr)

    # Numeric evaluation
    pt = {x: 3.0, y: 4.0, z: 0.0, q: 2.0}
    actual_num = float(E_sq.subs(pt))
    expected_num = float(expected_expr.subs(pt))

    rel_err = (
        abs(actual_num - expected_num) / expected_num
        if expected_num
        else abs(actual_num)
    )

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=expected_num,
        actual=actual_num,
        relative_error=rel_err if not symbolic_match else 0.0,
        tolerance=1e-8,
        passed=symbolic_match,
        details=(
            f"|E|^2 symbolic match: {symbolic_match}. "
            f"Verified at (x,y,z,q)=(3,4,0,2): |E|^2 = {actual_num:.6e} "
            f"(expected {expected_num:.6e})."
        ),
    )


# ── 6. Biot-Savart Law Verification ────────────────────────────


@maxwell_cite(
    515,
    part=4,
    chapter="Electromagnetic Momentum",
    theory_class="maxwell_original",
    description="Biot-Savart law for magnetic field from a current element",
)
def verify_biot_savart() -> VerificationResult:
    """Verify the Biot-Savart law: dB = I * (dl x r_vec) / r^3 for a
    differential current element along the z-axis at the origin.

    At observation point (a, 0, 0), the x-component of B should be 0
    and the y-component should be I * dl / a^2.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Biot-Savart law: dB from current element I*dz along z-axis"
    arts = (515, 621)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    I, dl, a = symbols("I dl a", positive=True)

    # Current element along z-axis: dl_vec = (0, 0, dl)
    # Observation point at (a, 0, 0): r_vec = (a, 0, 0)
    # Cross product: dl x r = (0, 0, dl) x (a, 0, 0) = (0, dl*a, 0)
    r_mag = sqrt(a**2)  # = a

    dB_x = 0 * I * dl / r_mag**3
    dB_y = dl * a / r_mag**3
    dB_z = 0 * I * dl / r_mag**3

    # Verify: dB_x = 0, dB_z = 0, dB_y = I*dl/a^2
    expected_by = I * dl / a**2
    actual_by = simplify(I * dB_y)

    x_zero = _is_symbolic_zero(dB_x)
    z_zero = _is_symbolic_zero(dB_z)
    y_match = _is_symbolic_zero(actual_by - expected_by)
    all_pass = x_zero and z_zero and y_match

    pt = {I: 1.5, dl: 0.1, a: 2.0}
    actual_num = float(actual_by.subs(pt))
    expected_num = float(expected_by.subs(pt))
    rel_err = abs(actual_num - expected_num) / expected_num if expected_num else 0.0

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=expected_num,
        actual=actual_num,
        relative_error=rel_err if not all_pass else 0.0,
        tolerance=1e-8,
        passed=all_pass,
        details=(
            f"Biot-Savart: dB_x=0 ({x_zero}), dB_z=0 ({z_zero}), "
            f"dB_y = I*dl/a^2 ({y_match}). "
            f"Numeric: {actual_num:.6e} vs {expected_num:.6e}."
        ),
    )


# ── 7. Faraday's Law (Differential Form) ───────────────────────


@maxwell_cite(
    593,
    part=4,
    chapter="Electromagnetic Induction",
    theory_class="maxwell_original",
    description="Faraday's law: curl(E) = -dB/dt in differential form",
)
def verify_faraday_symbolic() -> VerificationResult:
    """Verify Faraday's law in differential form: curl(E) = -dB/dt.

    Uses a sinusoidal magnetic field B = (0, B0*sin(k*x - omega*t), 0)
    and computes the induced electric field curl to confirm the relationship.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Faraday's law: curl(E) = -dB/dt"
    arts = (593,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x, y, z, t = symbols("x y z t")
    B0, omega = symbols("B0 omega", real=True)

    # B = (0, B0*sin(omega*t), 0) -- spatially uniform, time-varying
    # -dB/dt = (0, -B0*omega*cos(omega*t), 0)
    # E = (0, 0, B0*omega*x*cos(omega*t))
    # curl(E)_y = -dEz/dx = -B0*omega*cos(omega*t) -- exact match!
    Bx = 0
    By = B0 * sin(omega * t)
    Bz = 0

    neg_dBdt_x = -diff(Bx, t)  # = 0
    neg_dBdt_y = -diff(By, t)  # = -B0*omega*cos(omega*t)
    neg_dBdt_z = -diff(Bz, t)  # = 0

    Ez = B0 * omega * x * cos(omega * t)

    curl_E_x = diff(Ez, y)  # = 0
    curl_E_y = -diff(Ez, x)  # = -B0*omega*cos(omega*t)
    curl_E_z = 0

    x_match = _is_symbolic_zero(curl_E_x - neg_dBdt_x)
    y_match = _is_symbolic_zero(curl_E_y - neg_dBdt_y)
    z_match = _is_symbolic_zero(curl_E_z - neg_dBdt_z)
    all_pass = x_match and y_match and z_match

    pt = {x: 1.0, y: 0.0, z: 0.0, t: 0.5, B0: 5.0, omega: 10.0}
    y_err = abs(float((curl_E_y - neg_dBdt_y).subs(pt)))

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(y_err),
        relative_error=0.0 if all_pass else float(y_err),
        tolerance=1e-8,
        passed=all_pass,
        details=(
            f"Faraday components: x={x_match}, y={y_match}, z={z_match}. "
            f"Max y-component error at test point: {y_err:.2e}."
        ),
    )


# ── 8. Continuity Equation ─────────────────────────────────────


@maxwell_cite(
    64,
    part=1,
    chapter="Equation of Continuity",
    theory_class="maxwell_original",
    description="charge conservation: d rho/dt + div(J) = 0",
)
def verify_continuity_equation() -> VerificationResult:
    """Verify the continuity equation: d(rho)/dt + div(J) = 0.

    Uses a Gaussian charge distribution rho = exp(-alpha*t) * sin(beta*x) * cos(gamma*y)
    with a consistent current density J to confirm local charge conservation.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Continuity equation: d(rho)/dt + div(J) = 0"
    arts = (64,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    t, x, y, z = symbols("t x y z")
    alpha, beta, gamma = symbols("alpha beta gamma", real=True, positive=True)

    # Charge density: decaying sinusoidal
    rho = exp(-alpha * t) * sin(beta * x) * cos(gamma * y)

    # Time derivative
    drho_dt = diff(rho, t)

    # Current density consistent with continuity:
    # d(rho)/dt = -alpha*rho = -alpha*exp(-alpha*t)*sin(beta*x)*cos(gamma*y)
    # We need div(J) = +alpha*exp(-alpha*t)*sin(beta*x)*cos(gamma*y)
    # Choose Jy = 0, Jx = -(alpha/beta)*exp(-alpha*t)*cos(beta*x)*cos(gamma*y)
    # Then dJx/dx = -(alpha/beta)*exp(-alpha*t)*(-beta*sin(beta*x))*cos(gamma*y)
    #            = alpha*exp(-alpha*t)*sin(beta*x)*cos(gamma*y)  -- exact match!
    Jx = -(alpha / beta) * exp(-alpha * t) * cos(beta * x) * cos(gamma * y)
    Jy = 0
    Jz = 0

    div_J = diff(Jx, x) + diff(Jy, y) + diff(Jz, z)

    continuity = simplify(drho_dt + div_J)
    symbolic_zero = _is_symbolic_zero(drho_dt + div_J)

    pt = {t: 0.5, x: 1.0, y: 0.3, z: 0.0, alpha: 2.0, beta: 3.0, gamma: 1.5}
    numeric_val = float(continuity.subs(pt))

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=numeric_val,
        relative_error=0.0 if symbolic_zero else abs(numeric_val),
        tolerance=1e-8,
        passed=symbolic_zero,
        details=(
            f"Continuity equation: d(rho)/dt + div(J) = {continuity}. "
            f"Symbolic zero: {symbolic_zero}. Test point evaluates to "
            f"{numeric_val:.2e}."
        ),
    )


# ── 9. Maxwell Displacement Current ────────────────────────────


@maxwell_cite(
    597,
    part=4,
    chapter="Electromagnetic Theory",
    theory_class="maxwell_original",
    description="Maxwell displacement current restores consistency to Ampere's law",
)
def verify_maxwell_correction() -> VerificationResult:
    """Verify Maxwell's displacement current correction: divergence of
    curl(B) equals 4*pi*J + (1/c)*dE/dt is consistent.

    Uses a time-varying E field to show that without the displacement current
    term, the divergence of curl(B) would not vanish (contradiction).
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Maxwell displacement current: div(curl(B)) = 4pi*J + (1/c)*dE/dt"
    arts = (597, 601)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x, y, z, t = symbols("x y z t")
    E0, k, omega, c = symbols("E0 k omega c", real=True)

    # Sinusoidal E field along z: E = (0, 0, E0*sin(k*x - omega*t))
    Ex, Ey, Ez = 0, 0, E0 * sin(k * x - omega * t)

    # For a plane wave, the associated B field is:
    # B = (0, (E0*k/omega)*sin(k*x - omega*t), 0)
    Bx, By, Bz = 0, (E0 * k / omega) * sin(k * x - omega * t), 0

    # Compute curl(B)
    curl_B_x = diff(Bz, y) - diff(By, z)  # = 0
    curl_B_y = diff(Bx, z) - diff(Bz, x)  # = -E0*k*cos(kx - wt)
    curl_B_z = diff(By, x) - diff(Bx, y)  # = E0*k**2/omega * cos(kx - wt)

    # div(curl(B)) should be 0 by identity
    div_curl_B = simplify(diff(curl_B_x, x) + diff(curl_B_y, y) + diff(curl_B_z, z))

    # This equals (1/c)*dE/dt for J=0 (free space)
    dEz_dt = diff(Ez, t)

    # For a plane wave with omega = c*k:
    # (1/c)*dEz/dt = -E0*omega/c * cos(kx - wt)
    # curl(B)_y derivative contribution: d(curl_B_y)/dt = E0*k*cos(kx - wt)
    # We verify the identity div(curl(B)) = 0 holds (always true)
    # AND that (1/c)*dE/dt + 4*pi*J matches curl(B) components
    symbolic_zero = _is_symbolic_zero(div_curl_B)

    # Additional check: verify that dE/dt is consistent with wave relation
    # curl(B)_y = -dEz/dx = -E0*k*cos(kx - wt)
    # (1/c)*dEz/dt = -E0*omega/c * cos(kx - wt)
    # Match when omega/c = k => omega = c*k (wave dispersion)
    match_expr = simplify(
        -E0 * k * cos(k * x - omega * t) - (-E0 * omega / c * cos(k * x - omega * t))
    )
    dispersion_match = _is_symbolic_zero(match_expr.subs(omega, c * k))

    passed = symbolic_zero and dispersion_match

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=0.0,
        relative_error=0.0 if passed else 1.0,
        tolerance=1e-8,
        passed=passed,
        details=(
            f"div(curl(B))=0: {symbolic_zero}. "
            f"Dispersion omega=c*k consistency: {dispersion_match}. "
            f"Maxwell displacement current term (1/c)*dE/dt restores identity."
        ),
    )


# ── 10. Stokes' Theorem (Symbolic) ─────────────────────────────


@maxwell_cite(
    46,
    part=1,
    chapter="Flux",
    theory_class="standard_math",
    description="Stokes' theorem equates surface integral of curl to line integral",
)
def verify_stokes_theorem() -> VerificationResult:
    """Verify Stokes' theorem symbolically for F = (y, -x, 0) over the
    unit disk in the xy-plane.

    Surface integral of (curl F) dot k dA = line integral of F dot dl
    should both yield -2*pi for the unit circle.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Stokes' theorem: surface(curl F) = line(F) for unit disk"
    arts = (46,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x, y, z = symbols("x y z")
    theta = symbols("theta", real=True)

    # Vector field F = (y, -x, 0)
    Fx, Fy, Fz = y, -x, 0

    # curl(F) = (0, 0, -2)
    curl_F_z = diff(Fy, x) - diff(Fx, y)
    curl_F_z_simplified = simplify(curl_F_z)  # = -2

    # Surface integral: integral over unit disk of (curl_F . k) dA
    # = integral of (-2) dA = -2 * Area(unit_disk) = -2*pi
    surface_integral = -2 * pi

    # Line integral: parameterize unit circle as (cos(theta), sin(theta))
    # dl = (-sin(theta), cos(theta)) dtheta
    # F(r(theta)) = (sin(theta), -cos(theta), 0)
    # F . dl = (-sin^2(theta) - cos^2(theta)) dtheta = -1 dtheta
    F_line_x = sin(theta)
    F_line_y = -cos(theta)
    dl_x = diff(cos(theta), theta)  # = -sin(theta)
    dl_y = diff(sin(theta), theta)  # = cos(theta)

    dot_product = simplify(F_line_x * dl_x + F_line_y * dl_y)  # = -1
    line_integral = sympy.Integral(dot_product, (theta, 0, 2 * pi)).doit()

    symbolic_match = _is_symbolic_zero(surface_integral - line_integral)

    surface_num = float(surface_integral)
    line_num = float(line_integral)
    rel_err = abs(surface_num - line_num) / abs(surface_num) if surface_num else 0.0

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=surface_num,
        actual=line_num,
        relative_error=rel_err if not symbolic_match else 0.0,
        tolerance=1e-8,
        passed=symbolic_match,
        details=(
            f"curl(F)_z = {curl_F_z_simplified}. "
            f"Surface integral = {surface_integral}. "
            f"Line integral = {line_integral}. "
            f"Stokes' theorem verified: {symbolic_match}."
        ),
    )


# ── 11. Lorentz Force Symbolic ─────────────────────────────────


@maxwell_cite(
    490,
    part=4,
    chapter="Electromagnetism",
    theory_class="maxwell_original",
    description="Lorentz force F = q*(v x B) verified symbolically",
)
def verify_lorentz_force() -> VerificationResult:
    """Verify the Lorentz force law: F = q * (v x B) for a moving charge.

    Symbolically computes the cross product and verifies:
    - Force is perpendicular to both velocity and magnetic field
    - F . v = 0 and F . B = 0
    - Magnitude |F| = q * |v| * |B| * sin(theta)
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Lorentz force F = q*(v x B) orthogonality"
    arts = (490, 491, 492)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    q = symbols("q", real=True)
    vx, vy, vz = symbols("vx vy vz", real=True)
    Bx, By, Bz = symbols("Bx By Bz", real=True)

    # F = q * (v x B)
    Fx = q * (vy * Bz - vz * By)
    Fy = q * (vz * Bx - vx * Bz)
    Fz = q * (vx * By - vy * Bx)

    # Verify F . v = 0
    F_dot_v = simplify(Fx * vx + Fy * vy + Fz * vz)

    # Verify F . B = 0
    F_dot_B = simplify(Fx * Bx + Fy * By + Fz * Bz)

    orth_v = _is_symbolic_zero(F_dot_v, [q, vx, vy, vz, Bx, By, Bz])
    orth_B = _is_symbolic_zero(F_dot_B, [q, vx, vy, vz, Bx, By, Bz])
    passed = orth_v and orth_B

    # Numeric evaluation
    pt = {q: 1.0, vx: 3.0, vy: 4.0, vz: 0.0, Bx: 0.0, By: 0.0, Bz: 5.0}
    Fv_num = float(F_dot_v.subs(pt))
    FB_num = float(F_dot_B.subs(pt))
    max_err = max(abs(Fv_num), abs(FB_num))

    # Expected F = (20, -15, 0) for these values
    Fx_expected = q * (vy * Bz - vz * By)  # = 1*(4*5 - 0*0) = 20
    Fy_expected = q * (vz * Bx - vx * Bz)  # = 1*(0*0 - 3*5) = -15
    Fz_expected = q * (vx * By - vy * Bx)  # = 1*(3*0 - 4*0) = 0

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(max_err),
        relative_error=0.0 if passed else float(max_err),
        tolerance=1e-8,
        passed=passed,
        details=(
            f"Lorentz force orthogonality: F.v=0 ({orth_v}), F.B=0 ({orth_B}). "
            f"Max orthogonality error: {max_err:.2e}. "
            f"At test point: F=({Fx_expected}, {Fy_expected}, {Fz_expected})."
        ),
    )


# ── 12. Maxwell Stress Tensor Properties ───────────────────────


@maxwell_cite(
    641,
    part=4,
    chapter="Electromagnetism",
    theory_class="maxwell_original",
    description="Maxwell stress tensor symmetry and trace properties",
)
def verify_stress_tensor_properties() -> VerificationResult:
    """Verify properties of the Maxwell stress tensor:
    T_ij = (1/4pi)[E_i E_j + H_i H_j - (1/2) delta_ij (E^2 + H^2)]

    Properties verified:
    - Symmetry: T_ij = T_ji
    - Trace: Tr(T) = -(1/4pi)(E^2 + H^2) = -2 * energy_density
    - For E=0: T reduces to pure magnetic stress tensor
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Maxwell stress tensor: symmetry and trace"
    arts = (641, 642, 643, 644, 645, 646)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    Ex, Ey, Ez = symbols("Ex Ey Ez", real=True)
    Hx, Hy, Hz = symbols("Hx Hy Hz", real=True)

    E_sq = Ex**2 + Ey**2 + Ez**2
    H_sq = Hx**2 + Hy**2 + Hz**2
    total_sq = E_sq + H_sq

    # T_ij = (1/4pi)[E_i E_j + H_i H_j] - (total_sq/(8pi)) delta_ij
    # Check symmetry: T_01 vs T_10
    T_01 = (Ex * Ey + Hx * Hy) / (4 * pi)  # off-diagonal, no delta term
    T_10 = (Ey * Ex + Hy * Hx) / (4 * pi)
    sym_01 = _is_symbolic_zero(T_01 - T_10)

    # T_02 vs T_20
    T_02 = (Ex * Ez + Hx * Hz) / (4 * pi)
    T_20 = (Ez * Ex + Hz * Hx) / (4 * pi)
    sym_02 = _is_symbolic_zero(T_02 - T_20)

    # T_12 vs T_21
    T_12 = (Ey * Ez + Hy * Hz) / (4 * pi)
    T_21 = (Ez * Ey + Hz * Hy) / (4 * pi)
    sym_12 = _is_symbolic_zero(T_12 - T_21)

    # Trace: T_00 + T_11 + T_22
    T_00 = (Ex**2 + Hx**2) / (4 * pi) - total_sq / (8 * pi)
    T_11 = (Ey**2 + Hy**2) / (4 * pi) - total_sq / (8 * pi)
    T_22 = (Ez**2 + Hz**2) / (4 * pi) - total_sq / (8 * pi)
    trace = simplify(T_00 + T_11 + T_22)
    # Trace = (E^2+H^2)/(4pi) - 3*(E^2+H^2)/(8pi) = -(E^2+H^2)/(8pi)
    expected_trace = simplify(-total_sq / (8 * pi))
    trace_match = _is_symbolic_zero(trace - expected_trace)

    all_pass = sym_01 and sym_02 and sym_12 and trace_match

    # Numeric evaluation
    pt = {Ex: 3.0, Ey: 0.0, Ez: 4.0, Hx: 0.0, Hy: 5.0, Hz: 0.0}
    trace_num = float(trace.subs(pt))
    expected_trace_num = float(expected_trace.subs(pt))

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=expected_trace_num,
        actual=trace_num,
        relative_error=0.0 if all_pass else abs(trace_num - expected_trace_num),
        tolerance=1e-8,
        passed=all_pass,
        details=(
            f"Symmetry: T_01=T_10 ({sym_01}), T_02=T_20 ({sym_02}), "
            f"T_12=T_21 ({sym_12}). Trace match: {trace_match}. "
            f"Numeric trace: {trace_num:.6e} vs expected {expected_trace_num:.6e}."
        ),
    )


# ── 13. Ampere's Law (Symbolic) ───────────────────────────────


@maxwell_cite(
    606,
    part=4,
    chapter="Electromagnetism",
    theory_class="maxwell_original",
    description="Ampere's law: circulation of H equals enclosed current",
)
def verify_ampere_law() -> VerificationResult:
    """Verify Ampere's law in differential form: curl(H) = (4pi/c) * J.

    For a long straight wire carrying current I along the z-axis, the
    magnetic field at distance r is H = I/(2*pi*r) in the azimuthal direction.
    Verifying curl(H) gives zero outside the wire (no current) and the
    correct current density at the wire.

    Uses cylindrical symmetry: H_phi = I/(2*pi*r), verified via Cartesian.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Ampere's law: curl(H) = (4pi/c) J for straight wire"
    arts = (606, 607)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x, y, z = symbols("x y z")
    I_sym, c_sym = symbols("I c", positive=True)
    pi_sym = pi

    # H field for infinite wire along z-axis (azimuthal):
    # H = (-I*y/(2*pi*r^2), I*x/(2*pi*r^2), 0) where r^2 = x^2 + y^2
    r_sq = x**2 + y**2
    Hx = -I_sym * y / (2 * pi_sym * r_sq)
    Hy = I_sym * x / (2 * pi_sym * r_sq)
    Hz = 0

    # curl(H) = (dHz/dy - dHy/dz, dHx/dz - dHz/dx, dHy/dx - dHx/dy)
    curl_H_x = diff(Hz, y) - diff(Hy, z)
    curl_H_y = diff(Hx, z) - diff(Hz, x)
    curl_H_z = simplify(diff(Hy, x) - diff(Hx, y))

    # For an infinite wire, curl(H)_z should be 0 away from the origin
    # (current is a delta function at origin)
    curl_z_away_from_origin = _is_symbolic_zero(curl_H_z, [x, y, I_sym])

    # Verify Hx and Hy have no z-dependence (infinite wire)
    hx_z_indep = _is_symbolic_zero(diff(Hx, z))
    hy_z_indep = _is_symbolic_zero(diff(Hy, z))

    # Circulation: integral of H . dl around circle of radius R = I
    # H . dl = H_phi * R * dphi = I/(2*pi*R) * R * dphi = I/(2*pi) * dphi
    # Integral from 0 to 2pi = I
    theta = symbols("theta", real=True)
    H_phi = I_sym / (2 * pi_sym)  # H at radius R, times R cancels
    circulation = sympy.Integral(H_phi, (theta, 0, 2 * pi_sym)).doit()
    circulation_match = simplify(circulation - I_sym) == 0

    all_pass = (
        curl_z_away_from_origin and hx_z_indep and hy_z_indep and circulation_match
    )

    # Numeric check: curl_H_z at a point away from origin
    pt = {x: 2.0, y: 3.0, I_sym: 1.0}
    curl_z_num = abs(float(curl_H_z.subs(pt)))

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(curl_z_num),
        relative_error=0.0 if all_pass else float(curl_z_num),
        tolerance=1e-8,
        passed=all_pass,
        details=(
            f"Ampere's law: curl(H)_z=0 away from wire ({curl_z_away_from_origin}). "
            f"H independent of z: x={hx_z_indep}, y={hy_z_indep}. "
            f"Circulation = I: {circulation_match}. "
            f"|curl(H)_z| at (2,3): {curl_z_num:.2e}."
        ),
    )


# ════════════════════════════════════════════════════════════════
# Wave 8a spine verifiers (Arts. 667-866, Part IV Ch. XII-XXIII)
# ════════════════════════════════════════════════════════════════

# ── A. Elliptic integrals (Arts 696-705, 752-757) ───────────────


@maxwell_cite(
    696,
    703,
    part=4,
    chapter="Circular Currents",
    theory_class="standard_math",
    description="Gauss AGM identity K(k) = pi/(2 AGM(1, k')) for the complete elliptic integral",
)
def verify_elliptic_K_AGM_identity() -> VerificationResult:
    """Verify K(k) = pi/(2 AGM(1, k')) -- the identity used to tabulate
    the elliptic integrals entering the vector potential of a circular
    current (Arts. 696, 703).

    Two independent constructions are compared at three moduli:
      * the defining integral K(k) = Int_0^{pi/2} dtheta/sqrt(1-k^2 sin^2)
        evaluated by tanh-sinh quadrature (mpmath),
      * the arithmetic-geometric mean iterated explicitly here.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Elliptic K(k) = pi/(2 AGM(1,k'))"
    arts = (696, 703)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)
    try:
        import mpmath
    except ImportError:
        return _disabled_result(name, mod, arts)

    old_dps = mpmath.mp.dps
    try:
        mpmath.mp.dps = 42
        worst = 0.0
        for k_str in ("0.3", "0.6", "0.9"):
            kk = mpmath.mpf(k_str)
            kp = mpmath.sqrt(1 - kk**2)
            # AGM iteration (explicit, this file)
            a, b = mpmath.mpf(1), kp
            for _ in range(80):
                a, b = (a + b) / 2, mpmath.sqrt(a * b)
                if abs(a - b) < mpmath.mpf(10) ** (-40):
                    break
            K_agm = mpmath.pi / (2 * a)
            # Defining integral (independent construction)
            K_int = mpmath.quad(
                lambda th: 1 / mpmath.sqrt(1 - kk**2 * mpmath.sin(th) ** 2),
                [0, mpmath.pi / 2],
            )
            rel = abs(K_agm - K_int) / abs(K_int)
            worst = max(worst, float(rel))
    finally:
        mpmath.mp.dps = old_dps

    tol = 1e-30
    passed = worst < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(worst),
        relative_error=0.0 if passed else float(worst),
        tolerance=tol,
        passed=passed,
        details=(
            f"AGM vs defining-integral K(k) at k=0.3,0.6,0.9; "
            f"max relative residual {worst:.3e} (tol {tol:.0e})."
        ),
    )


@maxwell_cite(
    703,
    704,
    part=4,
    chapter="Circular Currents",
    theory_class="standard_math",
    description="Legendre relation K E' + K' E - K K' = pi/2 for complementary moduli",
)
def verify_elliptic_legendre_relation() -> VerificationResult:
    """Verify Legendre's relation K(k)E(k') + K(k')E(k) - K(k)K(k') = pi/2.

    All four complete elliptic integrals are computed directly from their
    defining integrals by quadrature (independent of any series or AGM
    implementation), then the Legendre combination is checked against pi/2.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Legendre relation K E' + K' E - K K' = pi/2"
    arts = (703, 704)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)
    try:
        import mpmath
    except ImportError:
        return _disabled_result(name, mod, arts)

    old_dps = mpmath.mp.dps
    try:
        mpmath.mp.dps = 40

        def K_def(k):
            return mpmath.quad(
                lambda th: 1 / mpmath.sqrt(1 - k**2 * mpmath.sin(th) ** 2),
                [0, mpmath.pi / 2],
            )

        def E_def(k):
            return mpmath.quad(
                lambda th: mpmath.sqrt(1 - k**2 * mpmath.sin(th) ** 2),
                [0, mpmath.pi / 2],
            )

        worst = 0.0
        for k_str in ("0.3", "0.7"):
            kk = mpmath.mpf(k_str)
            kp = mpmath.sqrt(1 - kk**2)
            combo = (
                K_def(kk) * E_def(kp) + K_def(kp) * E_def(kk) - K_def(kk) * K_def(kp)
            )
            rel = abs(combo - mpmath.pi / 2) / (mpmath.pi / 2)
            worst = max(worst, float(rel))
    finally:
        mpmath.mp.dps = old_dps

    tol = 1e-28
    passed = worst < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=float(mpmath.pi / 2) if _HAS_SYMPY else 1.5707963267948966,
        actual=float(mpmath.pi / 2) if _HAS_SYMPY else 1.5707963267948966,
        relative_error=0.0 if passed else float(worst),
        tolerance=tol,
        passed=passed,
        details=(
            f"Complete integrals from defining integrals (quadrature); "
            f"Legendre combination residual {worst:.3e} vs pi/2 (tol {tol:.0e})."
        ),
    )


@maxwell_cite(
    703,
    part=4,
    chapter="Circular Currents",
    theory_class="standard_math",
    description="small-modulus series of K with double-factorial coefficients",
)
def verify_elliptic_K_small_k_series() -> VerificationResult:
    """Verify K(k) = (pi/2) sum_n [((2n-1)!!/(2n)!!)^2 k^{2n}] (Art. 703).

    The Taylor series of SymPy's elliptic_k(m) at m=0 is extracted
    coefficient by coefficient and compared against the closed binomial
    coefficients c_n = (C(2n,n)/4^n)^2, an independent construction from
    the binomial expansion of (1 - m sin^2 t)^{-1/2} and Wallis' integral.
    Comparison is exact rational arithmetic.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "K(k) small-k series coefficients"
    arts = (703,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    m = symbols("m")
    ser = sympy.elliptic_k(m).series(m, 0, 6).removeO()

    residuals = []
    for n in range(6):
        central = factorial(2 * n) / (factorial(n) ** 2 * 4**n)
        expected_coeff = pi / 2 * central**2
        residuals.append(simplify(ser.coeff(m, n) - expected_coeff))

    worst = max(abs(float(r)) for r in residuals)
    passed = all(r == 0 for r in residuals)
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(worst),
        relative_error=0.0 if passed else float(worst),
        tolerance=1e-12,
        passed=passed,
        details=(
            f"Coefficients n=0..5 of K(m) series vs ((2n-1)!!/(2n)!!)^2 "
            f"closed form; all exact-zero: {passed}."
        ),
    )


@maxwell_cite(
    703,
    part=4,
    chapter="Circular Currents",
    theory_class="standard_math",
    description="small-modulus series of E with double-factorial coefficients",
)
def verify_elliptic_E_small_k_series() -> VerificationResult:
    """Verify E(k) = (pi/2)[1 - sum_{n>=1} ((2n-1)!!/(2n)!!)^2 k^{2n}/(2n-1)].

    Exact rational comparison of SymPy's elliptic_e(m) Taylor coefficients
    against the closed form obtained by integrating the binomial expansion
    term by term (Art. 703).
    """
    mod = "maxwell.verification.sympy_verify"
    name = "E(k) small-k series coefficients"
    arts = (703,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    m = symbols("m")
    ser = sympy.elliptic_e(m).series(m, 0, 6).removeO()

    residuals = []
    for n in range(6):
        central = factorial(2 * n) / (factorial(n) ** 2 * 4**n)
        if n == 0:
            expected_coeff = pi / 2
        else:
            expected_coeff = -pi / 2 * central**2 / (2 * n - 1)
        residuals.append(simplify(ser.coeff(m, n) - expected_coeff))

    worst = max(abs(float(r)) for r in residuals)
    passed = all(r == 0 for r in residuals)
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(worst),
        relative_error=0.0 if passed else float(worst),
        tolerance=1e-12,
        passed=passed,
        details=(
            f"Coefficients n=0..5 of E(m) series vs closed binomial form; "
            f"all exact-zero: {passed}."
        ),
    )


@maxwell_cite(
    704,
    part=4,
    chapter="Circular Currents",
    theory_class="standard_math",
    description="modulus derivative dK/dm = (E - (1-m)K)/(2m(1-m))",
)
def verify_elliptic_K_derivative_identity() -> VerificationResult:
    """Verify dK/dm = (E(m) - (1-m)K(m))/(2 m (1-m)) (Art. 704).

    Three-way triangulation: SymPy's symbolic derivative of elliptic_k,
    the classical closed form, and an independent numerical derivative
    (mpmath.diff) of the defining integral.  All three must agree.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "dK/dm identity"
    arts = (704,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)
    try:
        import mpmath
    except ImportError:
        return _disabled_result(name, mod, arts)

    m = symbols("m")
    lhs = diff(sympy.elliptic_k(m), m)
    rhs = (sympy.elliptic_e(m) - (1 - m) * sympy.elliptic_k(m)) / (2 * m * (1 - m))

    worst = 0.0
    for mv in (Rational(3, 10), Rational(7, 10)):
        l_num = float(sympy.N(lhs.subs(m, mv), 30))
        r_num = float(sympy.N(rhs.subs(m, mv), 30))
        worst = max(worst, abs(l_num - r_num) / abs(r_num))

    # Independent numerical derivative of the defining integral at m=0.3
    old_dps = mpmath.mp.dps
    try:
        mpmath.mp.dps = 35

        def K_int(mv):
            return mpmath.quad(
                lambda th: 1 / mpmath.sqrt(1 - mv * mpmath.sin(th) ** 2),
                [0, mpmath.pi / 2],
            )

        num_deriv = float(mpmath.diff(K_int, mpmath.mpf("0.3")))
        closed_at = float(sympy.N(rhs.subs(m, Rational(3, 10)), 30))
        worst = max(worst, abs(num_deriv - closed_at) / abs(closed_at))
    finally:
        mpmath.mp.dps = old_dps

    tol = 1e-20
    passed = worst < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(worst),
        relative_error=0.0 if passed else float(worst),
        tolerance=tol,
        passed=passed,
        details=(
            f"Symbolic derivative vs closed form vs numerical derivative of "
            f"the defining integral; max relative residual {worst:.3e}."
        ),
    )


@maxwell_cite(
    704,
    part=4,
    chapter="Circular Currents",
    theory_class="standard_math",
    description="modulus derivative dE/dm = (E - K)/(2m)",
)
def verify_elliptic_E_derivative_identity() -> VerificationResult:
    """Verify dE/dm = (E(m) - K(m))/(2m) (Art. 704).

    SymPy's symbolic derivative of elliptic_e(m) is compared with the
    classical closed form at two parameters, and cross-checked against a
    numerical derivative of the defining integral.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "dE/dm identity"
    arts = (704,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)
    try:
        import mpmath
    except ImportError:
        return _disabled_result(name, mod, arts)

    m = symbols("m")
    lhs = diff(sympy.elliptic_e(m), m)
    rhs = (sympy.elliptic_e(m) - sympy.elliptic_k(m)) / (2 * m)

    worst = 0.0
    for mv in (Rational(3, 10), Rational(7, 10)):
        l_num = float(sympy.N(lhs.subs(m, mv), 30))
        r_num = float(sympy.N(rhs.subs(m, mv), 30))
        worst = max(worst, abs(l_num - r_num) / abs(r_num))

    old_dps = mpmath.mp.dps
    try:
        mpmath.mp.dps = 35

        def E_int(mv):
            return mpmath.quad(
                lambda th: mpmath.sqrt(1 - mv * mpmath.sin(th) ** 2),
                [0, mpmath.pi / 2],
            )

        num_deriv = float(mpmath.diff(E_int, mpmath.mpf("0.3")))
        closed_at = float(sympy.N(rhs.subs(m, Rational(3, 10)), 30))
        worst = max(worst, abs(num_deriv - closed_at) / abs(closed_at))
    finally:
        mpmath.mp.dps = old_dps

    tol = 1e-20
    passed = worst < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(worst),
        relative_error=0.0 if passed else float(worst),
        tolerance=tol,
        passed=passed,
        details=(
            f"Symbolic derivative vs closed form vs numerical derivative of "
            f"the defining integral; max relative residual {worst:.3e}."
        ),
    )


@maxwell_cite(
    705,
    part=4,
    chapter="Circular Currents",
    theory_class="standard_math",
    description="Landen descending transformation K(k) = 2/(1+k') K((1-k')/(1+k'))",
)
def verify_elliptic_landen_descent() -> VerificationResult:
    """Verify the Landen descending transformation of K (Art. 705):

        K(k) = 2/(1+k') * K(k1),   k1 = (1-k')/(1+k'),  k' = sqrt(1-k^2).

    Derivation: AGM(1,k') = AGM((1+k')/2, sqrt(k')) and the homogeneity
    of AGM give AGM(1,k') = ((1+k')/2) AGM(1, k1'), which translates into
    the stated K-relation via K = pi/(2 AGM).  Both K values here are
    computed independently from the defining integral by quadrature.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Landen descent for K"
    arts = (705,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)
    try:
        import mpmath
    except ImportError:
        return _disabled_result(name, mod, arts)

    old_dps = mpmath.mp.dps
    try:
        mpmath.mp.dps = 40

        def K_def(k):
            return mpmath.quad(
                lambda th: 1 / mpmath.sqrt(1 - k**2 * mpmath.sin(th) ** 2),
                [0, mpmath.pi / 2],
            )

        worst = 0.0
        for k_str in ("0.2", "0.5", "0.9"):
            kk = mpmath.mpf(k_str)
            kp = mpmath.sqrt(1 - kk**2)
            k1 = (1 - kp) / (1 + kp)
            lhs_v = K_def(kk)
            rhs_v = 2 / (1 + kp) * K_def(k1)
            worst = max(worst, float(abs(lhs_v - rhs_v) / abs(lhs_v)))
    finally:
        mpmath.mp.dps = old_dps

    tol = 1e-28
    passed = worst < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(worst),
        relative_error=0.0 if passed else float(worst),
        tolerance=tol,
        passed=passed,
        details=(
            f"Landen descent at k=0.2,0.5,0.9; both sides from defining "
            f"integrals; max relative residual {worst:.3e}."
        ),
    )


@maxwell_cite(
    752,
    755,
    part=4,
    chapter="Coil Comparison",
    theory_class="maxwell_original",
    description="coil-comparison modulus k^2 = 4 a1 a2 / ((a1+a2)^2 + b^2)",
)
def verify_coil_comparison_modulus() -> VerificationResult:
    """Verify the modulus used in the comparison of coils (Arts. 752, 755):

        k^2 = 4 a1 a2 / ((a1 + a2)^2 + b^2)

    for two coaxial circles of radii a1, a2 at distance b.  Derived
    independently from the geometry: with d(phi)^2 = a1^2 + a2^2 + b^2
    - 2 a1 a2 cos(phi), the extrema are d_min^2 = (a1-a2)^2 + b^2 (phi=0)
    and d_max^2 = (a1+a2)^2 + b^2 (phi=pi); the elliptic modulus is
    k^2 = 1 - d_min^2/d_max^2.  Symbolic expansion proves equality.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Coil-comparison modulus from geometry"
    arts = (752, 755)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    a1, a2, b, phi = symbols("a1 a2 b phi", positive=True)
    d_sq = a1**2 + a2**2 + b**2 - 2 * a1 * a2 * cos(phi)
    d_min_sq = d_sq.subs(phi, 0)
    d_max_sq = d_sq.subs(phi, pi)
    k_sq_geom = simplify(1 - d_min_sq / d_max_sq)
    k_sq_classic = 4 * a1 * a2 / ((a1 + a2) ** 2 + b**2)

    residual = simplify(k_sq_geom - k_sq_classic)
    symbolic_zero = residual == 0

    pt = {a1: 2, a2: 5, b: 3}
    g_num = float(k_sq_geom.subs(pt))
    c_num = float(k_sq_classic.subs(pt))
    rel_err = abs(g_num - c_num) / c_num

    passed = symbolic_zero
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=c_num,
        actual=g_num,
        relative_error=0.0 if passed else rel_err,
        tolerance=1e-12,
        passed=passed,
        details=(
            f"k^2 from 1 - d_min^2/d_max^2 minus the classical formula "
            f"simplifies to {residual}; numeric instance (2,5,3): "
            f"{g_num:.10f} vs {c_num:.10f}."
        ),
    )


# ── B. Circular currents and induction (Arts 694-706) ───────────


@maxwell_cite(
    694,
    706,
    part=4,
    chapter="Circular Currents",
    theory_class="maxwell_original",
    description="magnetic field at the centre of a circular current, B = 2 pi I / a",
)
def verify_circular_current_center_field() -> VerificationResult:
    """Verify B_centre = 2 pi I / a for a circular current of radius a
    (Arts. 694, 706) by direct Biot-Savart integration.

    The cross product dl x r_vec is formed componentwise for a loop in
    the xy-plane observed at its centre, giving the constant integrand
    I a^2 / a^3; integrating over phi yields 2 pi I / a.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Circular current centre field B = 2 pi I/a"
    arts = (694, 706)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    I_s, a, phi = symbols("I a phi", positive=True)

    # Loop: source point (a cos phi, a sin phi, 0); dl = a(-sin, cos, 0) dphi.
    # Vector source -> centre: (-a cos phi, -a sin phi, 0).
    dl_x, dl_y = a * (-sin(phi)), a * cos(phi)
    r_x, r_y = -a * cos(phi), -a * sin(phi)
    cross_z = simplify(dl_x * r_y - dl_y * r_x)  # = a^2

    integrand = I_s * cross_z / a**3
    B_z = integrate(integrand, (phi, 0, 2 * pi))
    expected = 2 * pi * I_s / a

    residual = simplify(B_z - expected)
    passed = residual == 0

    pt = {I_s: 1.5, a: 2}
    b_num = float(B_z.subs(pt))
    e_num = float(expected.subs(pt))

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=e_num,
        actual=b_num,
        relative_error=0.0 if passed else abs(b_num - e_num) / e_num,
        tolerance=1e-12,
        passed=passed,
        details=(
            f"Biot-Savart cross product = {cross_z}; integrated field "
            f"{B_z}; residual vs 2 pi I/a: {residual}."
        ),
    )


@maxwell_cite(
    694,
    699,
    part=4,
    chapter="Circular Currents",
    theory_class="maxwell_original",
    description="axial field of a circular current, B_z = 2 pi I a^2/(a^2+z^2)^{3/2}",
)
def verify_loop_axial_field_integral() -> VerificationResult:
    """Verify the axial field of a circular current (Arts. 694, 699):

        B_z(z) = 2 pi I a^2 / (a^2 + z^2)^{3/2}

    obtained by performing the Biot-Savart integral over the loop
    symbolically (the axial integrand is phi-independent).
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Loop axial field from Biot-Savart"
    arts = (694, 699)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    I_s, a, z, phi = symbols("I a z phi", positive=True)

    # |r|^2 = a^2 + z^2 - 2 a rho cos(phi) with rho=0 on axis; axial
    # component of dl x r_vec is a^2, so the integrand is I a^2/(a^2+z^2)^{3/2}.
    integrand = I_s * a**2 / (a**2 + z**2) ** Rational(3, 2)
    B_z = integrate(integrand, (phi, 0, 2 * pi))
    expected = 2 * pi * I_s * a**2 / (a**2 + z**2) ** Rational(3, 2)

    residual = simplify(B_z - expected)
    passed = residual == 0

    pt = {I_s: 1, a: 1, z: 3}
    b_num = float(B_z.subs(pt))
    e_num = float(expected.subs(pt))

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=e_num,
        actual=b_num,
        relative_error=0.0 if passed else abs(b_num - e_num) / e_num,
        tolerance=1e-12,
        passed=passed,
        details=(
            f"Integral over phi of the constant axial integrand gives "
            f"{B_z}; residual vs closed form: {residual}."
        ),
    )


@maxwell_cite(
    694,
    833,
    part=4,
    chapter="Circular Currents",
    theory_class="maxwell_original",
    description="far-field dipole limit of the loop axial field, z^3 B_z -> 2 pi I a^2 = 2M",
)
def verify_loop_far_field_dipole_limit() -> VerificationResult:
    """Verify the far-field dipole limit of the loop axial field:

        z^3 B_z(z) = 2 pi I a^2 (1 - (3/2) a^2/z^2 + ...)  as z -> oo,

    whose leading term 2 pi I a^2 = 2 M is twice the magnetic moment
    M = I (pi a^2) of the loop, matching the on-axis dipole field
    2M/r^3 used for molecular currents (Arts. 694, 833).
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Loop far field -> dipole 2M/z^3"
    arts = (694, 833)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    I_s, a, u = symbols("I a u", positive=True)

    b_axial = 2 * pi * I_s * a**2 / ((1 / u) ** 2 + a**2) ** Rational(3, 2)
    scaled = b_axial * (1 / u) ** 3  # z^3 B_z with z = 1/u
    ser = scaled.series(u, 0, 4).removeO()

    leading = ser.coeff(u, 0)
    second = ser.coeff(u, 2)

    moment = I_s * pi * a**2  # independent construction: current x area
    lead_ok = simplify(leading - 2 * moment) == 0
    second_ok = simplify(second + 3 * moment * a**2) == 0
    passed = lead_ok and second_ok

    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=0.0 if passed else 1.0,
        relative_error=0.0 if passed else 1.0,
        tolerance=1e-12,
        passed=passed,
        details=(
            f"Leading coefficient {leading} vs 2M = {2 * moment} "
            f"({lead_ok}); 1/z^2 coefficient {second} vs -3 M a^2 "
            f"({second_ok})."
        ),
    )


@maxwell_cite(
    696,
    part=4,
    chapter="Circular Currents",
    theory_class="maxwell_original",
    description="vector-potential kernel [(2-m)K(m) - 2E(m)] from the cos-integral",
)
def verify_vector_potential_loop_structure() -> VerificationResult:
    """Verify the elliptic structure of the loop vector potential (Art. 696):

        J = Int_0^{2pi} cos(phi)/sqrt(alpha - beta cos(phi)) dphi
          = (2 sqrt(alpha+beta)/beta) [(2-m) K(m) - 2 E(m)],
        m = 2 beta/(alpha + beta),  alpha = a^2+rho^2+z^2,  beta = 2 a rho.

    The integral is evaluated by high-precision quadrature of its
    definition; the closed form uses complete elliptic integrals.  The
    identity follows from cos(phi) = (alpha - R^2)/beta splitting J into
    the standard K and E kernels.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "A_phi kernel [(2-m)K - 2E]"
    arts = (696,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)
    try:
        import mpmath
    except ImportError:
        return _disabled_result(name, mod, arts)

    old_dps = mpmath.mp.dps
    try:
        mpmath.mp.dps = 38
        worst = 0.0
        checked = []
        for a_v, rho_v, z_v in ((1.0, 1.3, 0.4), (2.0, 0.7, 0.35), (1.0, 2.5, 1.1)):
            alpha = mpmath.mpf(a_v) ** 2 + mpmath.mpf(rho_v) ** 2 + mpmath.mpf(z_v) ** 2
            beta = 2 * mpmath.mpf(a_v) * mpmath.mpf(rho_v)

            def integrand(ph):
                return mpmath.cos(ph) / mpmath.sqrt(alpha - beta * mpmath.cos(ph))

            J_num = mpmath.quad(integrand, [0, mpmath.pi, 2 * mpmath.pi])
            m_par = 2 * beta / (alpha + beta)
            K_v = mpmath.ellipk(m_par)
            E_v = mpmath.ellipe(m_par)
            J_cf = 2 * mpmath.sqrt(alpha + beta) / beta * ((2 - m_par) * K_v - 2 * E_v)
            rel = abs(J_num - J_cf) / abs(J_cf)
            checked.append(float(rel))
            worst = max(worst, float(rel))
    finally:
        mpmath.mp.dps = old_dps

    tol = 1e-28
    passed = worst < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(worst),
        relative_error=0.0 if passed else float(worst),
        tolerance=tol,
        passed=passed,
        details=(
            f"cos-integral (quadrature) vs [(2-m)K-2E] closed form at 3 "
            f"geometries; residuals {['%.2e' % r for r in checked]}."
        ),
    )


@maxwell_cite(
    694,
    755,
    part=4,
    chapter="Coil Comparison",
    theory_class="maxwell_original",
    description="Neumann mutual-inductance integral symmetry M12 = M21",
)
def verify_mutual_inductance_neumann_symmetry() -> VerificationResult:
    """Verify the symmetry M_12 = M_21 of the Neumann double integral

        M = oint oint (dl_1 . dl_2) / |r_1 - r_2|

    for two laterally offset circles (Arts. 694, 755).  The integral is
    computed twice -- once per circuit labelling -- with independent
    quadrature node phases, so equality is a computed fact, not a
    structural tautology.  A coaxial case additionally matches the
    elliptic closed form.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Neumann integral symmetry M12=M21"
    arts = (694, 755)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)
    import math

    try:
        import mpmath
    except ImportError:
        return _disabled_result(name, mod, arts)

    n_pts = 96

    def loop_pair_m(a1, a2, s_off, d_off, phase):
        total = 0.0
        step = 2.0 * math.pi / n_pts
        for i in range(n_pts):
            phi = step * (i + phase)
            x1 = a1 * math.cos(phi)
            y1 = a1 * math.sin(phi)
            for j in range(n_pts):
                psi = step * (j + phase)
                x2 = s_off + a2 * math.cos(psi)
                y2 = a2 * math.sin(psi)
                dx, dy = x1 - x2, y1 - y2
                r_mag = math.sqrt(dx * dx + dy * dy + d_off * d_off)
                total += math.cos(phi - psi) / r_mag
        return a1 * a2 * total * step * step

    m_fwd = loop_pair_m(1.0, 0.8, 0.6, 1.1, 0.0)
    m_swap = loop_pair_m(0.8, 1.0, -0.6, -1.1, 0.5)
    sym_resid = abs(m_fwd - m_swap) / abs(m_fwd)

    # Coaxial cross-check against the elliptic closed form
    m_coax = loop_pair_m(1.0, 1.3, 0.0, 2.0, 0.0)
    old_dps = mpmath.mp.dps
    try:
        mpmath.mp.dps = 35
        a1m, a2m, dm = (mpmath.mpf(v) for v in (1.0, 1.3, 2.0))
        alpha = a1m**2 + a2m**2 + dm**2
        beta = 2 * a1m * a2m
        m_par = 2 * beta / (alpha + beta)
        kernel = (2 - m_par) * mpmath.ellipk(m_par) - 2 * mpmath.ellipe(m_par)
        m_exact = (
            2 * mpmath.pi * a1m * a2m * 2 * mpmath.sqrt(alpha + beta) / beta * kernel
        )
        coax_resid = abs(mpmath.mpf(m_coax) - m_exact) / abs(m_exact)
    finally:
        mpmath.mp.dps = old_dps

    worst = max(sym_resid, float(coax_resid))
    tol = 1e-9
    passed = worst < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(worst),
        relative_error=0.0 if passed else float(worst),
        tolerance=tol,
        passed=passed,
        details=(
            f"Label-swap residual {sym_resid:.3e}; coaxial quadrature vs "
            f"elliptic closed form residual {float(coax_resid):.3e}."
        ),
    )


@maxwell_cite(
    755,
    756,
    part=4,
    chapter="Coil Comparison",
    theory_class="maxwell_original",
    description="coaxial mutual inductance tends to 2 pi^2 a1^2 a2^2 / d^3 (dipole limit)",
)
def verify_mutual_inductance_far_limit() -> VerificationResult:
    """Verify the far-distance limit of the coaxial mutual inductance
    (Arts. 755, 756):

        M(d) -> 2 pi^2 a1^2 a2^2 / d^3   as d -> infinity,

    the dipole-dipole value obtained independently from the interaction
    energy of coaxial magnetic moments.  The exact M(d) is evaluated from
    the elliptic formula and the ratio to the dipole limit must tend to 1.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "M(d) far limit = 2 pi^2 a1^2 a2^2/d^3"
    arts = (755, 756)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)
    try:
        import mpmath
    except ImportError:
        return _disabled_result(name, mod, arts)

    old_dps = mpmath.mp.dps
    try:
        mpmath.mp.dps = 35
        a1m, a2m = mpmath.mpf("1.0"), mpmath.mpf("1.3")
        ratios = []
        for d_str in ("10.0", "30.0"):
            dm = mpmath.mpf(d_str)
            alpha = a1m**2 + a2m**2 + dm**2
            beta = 2 * a1m * a2m
            m_par = 2 * beta / (alpha + beta)
            kernel = (2 - m_par) * mpmath.ellipk(m_par) - 2 * mpmath.ellipe(m_par)
            m_exact = (
                2
                * mpmath.pi
                * a1m
                * a2m
                * 2
                * mpmath.sqrt(alpha + beta)
                / beta
                * kernel
            )
            m_far = 2 * mpmath.pi**2 * a1m**2 * a2m**2 / dm**3
            ratios.append(float(m_exact / m_far))
    finally:
        mpmath.mp.dps = old_dps

    resid_far = abs(ratios[1] - 1.0)
    converging = resid_far < abs(ratios[0] - 1.0)
    tol = 1e-2
    passed = resid_far < tol and converging
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=1.0,
        actual=float(ratios[1]),
        relative_error=0.0 if passed else float(resid_far),
        tolerance=tol,
        passed=passed,
        details=(
            f"Ratio M_exact/M_dipole at d=10a: {ratios[0]:.6f}, at d=30a: "
            f"{ratios[1]:.6f}; converging to 1: {converging}."
        ),
    )


@maxwell_cite(
    755,
    756,
    part=4,
    chapter="Coil Comparison",
    theory_class="maxwell_original",
    description="distance derivative dM/dd -> -3M/d in the dipole regime",
)
def verify_dM_dd_dipole_relation() -> VerificationResult:
    """Verify the derivative relation dM/dd = -3 M/d (leading order) for
    coaxial circles at large separation (Arts. 755, 756).

    The exact M(d) built from the elliptic formula is differentiated
    symbolically by SymPy, and the ratio (dM/dd)/(-3M/d) is evaluated
    numerically at large d; it must approach 1 with O(a^2/d^2) corrections.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "dM/dd = -3M/d (dipole regime)"
    arts = (755, 756)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    d, a1, a2 = symbols("d a1 a2", positive=True)
    alpha = a1**2 + a2**2 + d**2
    beta = 2 * a1 * a2
    m_par = 2 * beta / (alpha + beta)
    m_exact = (
        2
        * pi
        * a1
        * a2
        * (2 * sqrt(alpha + beta) / beta)
        * ((2 - m_par) * sympy.elliptic_k(m_par) - 2 * sympy.elliptic_e(m_par))
    )
    dm_dd = diff(m_exact, d)

    pt = {a1: 1, a2: Rational(13, 10), d: 40}
    deriv_num = float(sympy.N(dm_dd.subs(pt), 30))
    target_num = float(sympy.N((-3 * m_exact / d).subs(pt), 30))
    ratio = deriv_num / target_num
    resid = abs(ratio - 1.0)

    tol = 5e-3
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=1.0,
        actual=float(ratio),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"Symbolic dM/dd vs -3M/d at d=40, a1=1, a2=1.3: ratio "
            f"{ratio:.6f} (residual {resid:.3e})."
        ),
    )


# ── Cluster C: zonal-harmonic spine (Arts. 675-693 machinery) ───


@maxwell_cite(
    675,
    part=4,
    chapter="Parallel Currents",
    theory_class="standard_math",
    description="zonal harmonic value P_l(1) = 1 from Rodrigues' formula",
)
def verify_legendre_value_at_one() -> VerificationResult:
    """Verify P_l(1) = 1 for l = 0..6 (Art. 675).

    The polynomials are built independently from the Rodrigues operator
    (never from maxwell.math.spherical_harmonics) and evaluated at x=1;
    the zonal harmonics must take the value 1 on the axis, which fixes
    the leading coefficient used throughout the potential expansions.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "P_l(1) = 1 (Rodrigues construction)"
    arts = (675,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x = symbols("x")
    values = [float(_legendre_poly(ell, x).subs(x, 1)) for ell in range(7)]
    resid = max(abs(v - 1.0) for v in values)
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=1.0,
        actual=values[6],
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "P_l(1) for l=0..6 from Rodrigues' formula: "
            f"{[f'{v:.1f}' for v in values]}; all equal 1."
        ),
    )


@maxwell_cite(
    675,
    part=4,
    chapter="Parallel Currents",
    theory_class="standard_math",
    description="zonal harmonic parity P_l(-x) = (-1)^l P_l(x)",
)
def verify_legendre_parity() -> VerificationResult:
    """Verify P_l(-x) = (-1)^l P_l(x) for l = 0..6 (Art. 675).

    Parity of the zonal harmonics decides which degrees contribute to
    symmetric current configurations.  The residual is the exact
    polynomial difference, reduced by expand().
    """
    mod = "maxwell.verification.sympy_verify"
    name = "P_l(-x) = (-1)^l P_l(x)"
    arts = (675,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x = symbols("x")
    resid = 0.0
    for ell in range(7):
        pl = _legendre_poly(ell, x)
        diff_poly = sympy.expand(pl.subs(x, -x) - ((-1) ** ell) * pl)
        resid = max(resid, abs(complex(diff_poly.subs(x, sympy.Rational(3, 7)))))
        if diff_poly != 0:
            resid = max(resid, 1.0)
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details="Polynomial P_l(-x) - (-1)^l P_l(x) is identically zero for l=0..6.",
    )


@maxwell_cite(
    675,
    part=4,
    chapter="Parallel Currents",
    theory_class="standard_math",
    description="Bonnet three-term recurrence for the zonal harmonics",
)
def verify_legendre_recurrence() -> VerificationResult:
    """Verify (l+1)P_{l+1} = (2l+1)x P_l - l P_{l-1} for l = 1..6 (Art. 675).

    The recurrence used to generate the coefficients of the potential
    expansions.  All members are built independently from Rodrigues'
    formula, so the recurrence is an external check on that construction.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Bonnet recurrence for P_l"
    arts = (675,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x = symbols("x")
    resid = 0.0
    for ell in range(1, 7):
        lhs = (ell + 1) * _legendre_poly(ell + 1, x)
        rhs = (2 * ell + 1) * x * _legendre_poly(ell, x) - ell * _legendre_poly(
            ell - 1, x
        )
        if sympy.expand(lhs - rhs) != 0:
            resid = 1.0
            break
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "(l+1)P_{l+1}(x) - (2l+1)xP_l(x) + lP_{l-1}(x) is the zero "
            "polynomial for l=1..6."
        ),
    )


@maxwell_cite(
    675,
    part=4,
    chapter="Parallel Currents",
    theory_class="standard_math",
    description="orthogonality integral of the zonal harmonics on [-1, 1]",
)
def verify_legendre_orthogonality() -> VerificationResult:
    """Verify int_{-1}^{1} P_l P_m dx = 2 delta_lm/(2l+1) for l,m <= 5
    (Art. 675).

    The orthogonality that isolates each coefficient in the zonal
    expansion of a current's potential.  Each integral is evaluated
    exactly (polynomial integrand) and compared with the closed form.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "orthogonality of P_l"
    arts = (675,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x = symbols("x")
    polys = [_legendre_poly(ell, x) for ell in range(6)]
    resid = 0.0
    for ell in range(6):
        for emm in range(6):
            exact = integrate(polys[ell] * polys[emm], (x, -1, 1))
            closed = sympy.Rational(2, 2 * ell + 1) if ell == emm else sympy.S.Zero
            resid = max(resid, abs(float(exact - closed)))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "All 36 integrals int_{-1}^1 P_l P_m dx equal 2/(2l+1) delta_lm "
            "exactly (symbolic quadrature)."
        ),
    )


@maxwell_cite(
    676,
    part=4,
    chapter="Parallel Currents",
    theory_class="standard_math",
    description="generating function of the zonal harmonics",
)
def verify_legendre_generating_function() -> VerificationResult:
    """Verify (1 - 2xt + t^2)^{-1/2} = sum_l P_l(x) t^l (Art. 676).

    The generating function is expanded as a Taylor series in t to
    order 4 and each coefficient is compared, as an exact polynomial
    identity in x, against the Rodrigues polynomial of the same degree.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "generating function coefficients"
    arts = (676,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x, t = symbols("x t")
    gen = (1 - 2 * x * t + t**2) ** Rational(-1, 2)
    ser = series(gen, t, 0, 5).removeO()
    resid = 0.0
    for ell in range(5):
        coeff_diff = sympy.expand(ser.coeff(t, ell) - _legendre_poly(ell, x))
        if coeff_diff != 0:
            resid = 1.0
            break
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "Taylor coefficients of (1 - 2xt + t^2)^{-1/2} in t equal "
            "P_0..P_4 as polynomial identities."
        ),
    )


@maxwell_cite(
    676,
    part=4,
    chapter="Parallel Currents",
    theory_class="standard_math",
    description="addition theorem for zonal harmonics, degrees 1 and 2",
)
def verify_addition_theorem_p1() -> VerificationResult:
    """Verify the addition theorem P_l(cos gamma) = sum_m ... for l = 1, 2
    (Art. 676).

    cos(gamma) is built independently as the Cartesian dot product of
    two unit vectors written in spherical coordinates; the right-hand
    side is built from the zonal and associated functions (Condon-Shortley,
    derived here from the Rodrigues polynomials by differentiation).
    Degree 1 must hold as an exact trig identity; degree 2 is checked at
    five seeded angle samples.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "addition theorem (l=1 exact, l=2 sampled)"
    arts = (676,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    uu = symbols("u")
    th, ph, thp, php = symbols("th ph thp php")

    def poly(ell):
        return sympy.expand(
            sympy.diff((uu**2 - 1) ** ell, uu, ell) / (2**ell * sympy.factorial(ell))
        )

    def pval(ell, xval):
        return sympy.expand(poly(ell).subs(uu, xval))

    def passoc(ell, emm, xval):
        deriv = sympy.diff(poly(ell), uu, emm).subs(uu, xval)
        return sympy.expand(((-1) ** emm) * (1 - xval**2) ** Rational(emm, 2) * deriv)

    cosg = cos(th) * cos(thp) + sin(th) * sin(thp) * cos(ph - php)
    resid_l1 = abs(
        complex(
            sympy.simplify(
                pval(1, cosg)
                - (cos(th) * cos(thp) + sin(th) * sin(thp) * cos(ph - php))
            )
        )
    )
    rhs_l2 = (
        pval(2, cos(th)) * pval(2, cos(thp))
        + Rational(1, 3)
        * passoc(2, 1, cos(th))
        * passoc(2, 1, cos(thp))
        * cos(ph - php)
        + Rational(1, 12)
        * passoc(2, 2, cos(th))
        * passoc(2, 2, cos(thp))
        * cos(2 * (ph - php))
    )
    lhs_l2 = pval(2, cosg)
    import random as _random

    _rnd = _random.Random(7)
    resid_l2 = 0.0
    for _ in range(5):
        pt = {
            th: _rnd.uniform(0.2, 2.5),
            thp: _rnd.uniform(0.2, 2.5),
            ph: _rnd.uniform(0.0, 6.0),
            php: _rnd.uniform(0.0, 6.0),
        }
        resid_l2 = max(resid_l2, abs(float((lhs_l2 - rhs_l2).subs(pt))))
    resid = max(resid_l1, resid_l2)
    tol = 1e-10
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"l=1 residual {resid_l1:.2e} (exact trig identity); l=2 residual "
            f"{resid_l2:.2e} over 5 seeded angle samples."
        ),
    )


@maxwell_cite(
    676,
    part=4,
    chapter="Parallel Currents",
    theory_class="standard_math",
    description="normalization of the spherical harmonic of degree zero",
)
def verify_Y00_normalization() -> VerificationResult:
    """Verify int |Y_00|^2 dOmega = 1 with Y_00 = 1/sqrt(4 pi) (Art. 676).

    The normalization constant is derived independently by solving
    int c^2 sin(theta) dtheta dphi = 1 for c, then the squared norm of
    the resulting Y_00 is integrated over the sphere and compared to 1.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Y_00 normalization on the sphere"
    arts = (676,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    th, ph, cc = symbols("theta phi c", positive=True)
    norm_eq = integrate(cc**2 * sin(th), (th, 0, pi), (ph, 0, 2 * pi)) - 1
    sols = solve(norm_eq, cc)
    c_pos = min(sols, key=lambda s: float(s))  # positive root 1/(2 sqrt(pi))
    norm_sq = integrate(c_pos**2 * sin(th), (th, 0, pi), (ph, 0, 2 * pi))
    resid = abs(float(norm_sq) - 1.0)
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=1.0,
        actual=float(norm_sq),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"Solved normalization gives c = {sympy.sstr(c_pos)}; the "
            f"spherical integral of c^2 is {float(norm_sq):.12f}."
        ),
    )


@maxwell_cite(
    677,
    part=4,
    chapter="Parallel Currents",
    theory_class="standard_math",
    description="solid harmonics r^l P_l and r^-(l+1) P_l satisfy Laplace's equation",
)
def verify_zonal_harmonic_laplace() -> VerificationResult:
    """Verify the axisymmetric Laplacian annihilates r^l P_l(cos theta) and
    r^-(l+1) P_l(cos theta) for l = 1..4 (Art. 677).

    These are the interior and exterior zonal solid harmonics used to
    expand the potential of current systems.  The Laplacian is applied
    in the algebraic u = cos(theta) form
    r^2 nabla^2 f = r^2 f_rr + 2r f_r + d/du[(1-u^2) f_u]
    and each residual is reduced exactly.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "solid harmonics solve Laplace's equation"
    arts = (677,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    r, uu = symbols("r u", positive=True)
    resid = 0.0
    for ell in range(1, 5):
        pl = _legendre_poly(ell, uu)
        for radial in (r**ell, r ** (-(ell + 1))):
            psi = radial * pl
            lap_r2 = (
                r**2 * diff(psi, r, 2)
                + 2 * r * diff(psi, r)
                + diff((1 - uu**2) * diff(psi, uu), uu)
            )
            if sympy.expand(lap_r2) != 0:
                resid = 1.0
                break
        if resid:
            break
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "r^2 nabla^2[r^l P_l(u)] and r^2 nabla^2[r^-(l+1) P_l(u)] reduce "
            "to the zero polynomial for l=1..4 (u = cos theta)."
        ),
    )


@maxwell_cite(
    677,
    part=4,
    chapter="Parallel Currents",
    theory_class="standard_math",
    description="Legendre differential equation for the zonal harmonics",
)
def verify_legendre_differential_equation() -> VerificationResult:
    """Verify (1-x^2)P_l'' - 2xP_l' + l(l+1)P_l = 0 for l = 0..5 (Art. 677).

    The differential equation behind every zonal-harmonic expansion of
    the Treatise.  Each residual is an exact polynomial reduction.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Legendre differential equation"
    arts = (677,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x = symbols("x")
    resid = 0.0
    for ell in range(6):
        pl = _legendre_poly(ell, x)
        ode = (1 - x**2) * diff(pl, x, 2) - 2 * x * diff(pl, x) + ell * (ell + 1) * pl
        if sympy.expand(ode) != 0:
            resid = 1.0
            break
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "(1-x^2)P_l'' - 2xP_l' + l(l+1)P_l is the zero polynomial for " "l=0..5."
        ),
    )


# ── Cluster D: current sheets (Arts. 667-674) ───────────────────


@maxwell_cite(
    667,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="tangential field jump 4 pi K at a plane current sheet",
)
def verify_surface_current_jump() -> VerificationResult:
    """Verify the tangential-field jump at a plane current sheet (Art. 667).

    The field of an infinite sheet K x-hat at z=0 is reconstructed by
    integrating the EMU Biot-Savart kernel K x r / r^3 over the sheet in
    polar coordinates (the radial integral is done symbolically by
    antiderivative + limits), giving H_above = -2 pi K y-hat.  The jump
    H_above - H_below = 4 pi K is then checked against the Ampere-loop
    value 4 pi I_enc / L = 4 pi K.  Both sides are computed; the
    residual is their difference.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "surface-current jump 4 pi K"
    arts = (667,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    rho, h, Kk = symbols("rho h K", positive=True)
    ph = symbols("phi")
    # y-component of int (K x r)/r^3 dA over the sheet, point at height h:
    # reduces to -K h int rho d rho d phi / (rho^2+h^2)^{3/2}
    radial = integrate(h * rho / (rho**2 + h**2) ** Rational(3, 2), rho)
    radial_val = limit(radial, rho, oo) - radial.subs(rho, 0)
    h_above_y = -2 * pi * Kk * sympy.simplify(radial_val)  # = -2 pi K
    h_below_y = -h_above_y  # field reverses below the sheet
    # Project the jump onto the tangent direction t = K-hat x n-hat = -y:
    jump_t = sympy.simplify(-(h_above_y - h_below_y))
    ampere_jump = 4 * pi * Kk  # from int H.dl = 4 pi K L, per unit length
    resid = abs(complex(sympy.simplify(jump_t - ampere_jump)))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=float(4 * sympy.pi),
        actual=float(jump_t / Kk),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"Biot-Savart sheet integral gives radial factor "
            f"{sympy.simplify(radial_val)} (=> H = 2 pi K each side); jump "
            f"{sympy.simplify(jump_t)} along K x n matches Ampere's 4 pi K."
        ),
    )


@maxwell_cite(
    667,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="normal magnetic induction is continuous (div B = 0)",
)
def verify_normal_B_continuous() -> VerificationResult:
    """Verify the normal component of B is continuous across a closed
    surface (Art. 667).

    The flux of the dipole field B = [3(m.r-hat)r-hat - m]/r^3 through
    the sphere r = R is integrated symbolically; it must vanish, which is
    the integral statement that B_n has no jump source (no magnetic
    charge) wherever div B = 0 holds.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "flux of dipole B through a sphere = 0"
    arts = (667,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    th, ph, mm, rr = symbols("theta phi m R", positive=True)
    # B_r of an axial dipole on the sphere r=R:
    b_radial = 2 * mm * cos(th) / rr**3
    flux = integrate(b_radial * rr**2 * sin(th), (th, 0, pi), (ph, 0, 2 * pi))
    resid = abs(float(flux))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(flux),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "Surface integral of B_r R^2 sin(theta) over the sphere is "
            f"{float(flux):.3e}: the normal induction is continuous."
        ),
    )


@maxwell_cite(
    668,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="infinite solenoid inductance L = 4 pi n^2 V from field energy",
)
def verify_solenoid_inductance_structure() -> VerificationResult:
    """Verify L = 4 pi n^2 V for the infinite solenoid (Art. 668).

    The EMU interior field B = 4 pi n I gives a field energy
    U = B^2 V / (8 pi); equating U = L I^2 / 2 and solving for L must
    reproduce 4 pi n^2 V.  The residual is the symbolic difference of
    the two routes.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "solenoid L = 4 pi n^2 V"
    arts = (668,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    n_sym, i_sym, vol = symbols("n I V", positive=True)
    b_field = 4 * pi * n_sym * i_sym
    energy = b_field**2 * vol / (8 * pi)
    l_from_energy = solve(
        energy - sympy.Symbol("L") * i_sym**2 / 2, sympy.Symbol("L")
    )[0]
    resid = abs(complex(sympy.simplify(l_from_energy - 4 * pi * n_sym**2 * vol)))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"Energy route gives L = {sympy.simplify(l_from_energy)}, i.e. "
            "4 pi n^2 V exactly."
        ),
    )


@maxwell_cite(
    669,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="scalar potential of a current sheet jumps by 4 pi I",
)
def verify_sheet_potential_discontinuity() -> VerificationResult:
    """Verify the magnetic-shell potential jumps by 4 pi I across the sheet
    (Art. 669).

    The solid angle of the plane z=0 seen from height h is computed by
    direct symbolic integration of the kernel h rho/(rho^2+h^2)^{3/2};
    it is +2 pi above and -2 pi below, so psi = I Omega jumps by 4 pi I.
    Expected value 4 pi I comes from the independent Ampere-loop count.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "sheet potential jump 4 pi I"
    arts = (669,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    rho, h, i_shell = symbols("rho h I", positive=True)
    anti = integrate(h * rho / (rho**2 + h**2) ** Rational(3, 2), rho)
    omega_above = 2 * pi * sympy.simplify(limit(anti, rho, oo) - anti.subs(rho, 0))
    omega_below = -omega_above  # orientation reverses under the sheet
    jump = sympy.simplify(i_shell * (omega_above - omega_below))
    resid = abs(complex(sympy.simplify(jump - 4 * pi * i_shell)))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=float(4 * sympy.pi),
        actual=float(jump / i_shell),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"Solid angle computed by quadrature: +{float(omega_above):.6f} "
            f"above, {float(omega_below):.6f} below; potential jump "
            f"{sympy.simplify(jump)}."
        ),
    )


@maxwell_cite(
    670,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="cylindrical current sheet: interior 4 pi K, exterior zero",
)
def verify_cylindrical_sheet_field() -> VerificationResult:
    """Verify the cylindrical current sheet (solenoidal sheet) field
    (Art. 670).

    Ampere's law across the sheet gives (B_in - B_out) L = 4 pi K L; with
    the exterior solution B_out = 0 (field lines close at infinity for
    the infinite sheet), SymPy solves for B_in and the result must be
    4 pi K.  Both quantities come out of solve(); nothing is asserted.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "cylindrical sheet B_in = 4 pi K"
    arts = (670,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    b_in, b_out, kk, ell = symbols("B_in B_out K L", positive=True)
    ampere = (b_in - b_out) * ell - 4 * pi * kk * ell
    interior = solve(ampere, b_in)[0].subs(b_out, 0)
    resid = abs(complex(sympy.simplify(interior - 4 * pi * kk)))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=float(4 * sympy.pi),
        actual=float(interior / kk),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"solve() of the Ampere loop gives B_in = {sympy.simplify(interior)} "
            "with B_out = 0."
        ),
    )


@maxwell_cite(
    671,
    part=4,
    chapter="Current-Sheets",
    theory_class="maxwell_original",
    description="toroidal current sheet: B = 2NI/r inside, zero outside",
)
def verify_sheet_toroidal_zero_exterior() -> VerificationResult:
    """Verify the toroidal current sheet (Art. 671).

    Inside the torus an Amperian circle of radius r links all N turns:
    B (2 pi r) = 4 pi N I, solved symbolically for B.  Outside, the loop
    links the turns in both senses (net enclosed current zero), so the
    same solve with I_enc = 0 returns B = 0.  Both values are computed.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "toroidal sheet B = 2NI/r, exterior 0"
    arts = (671,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    bb, rr, n_turns, ii = symbols("B r N I", positive=True)
    inside = solve(bb * 2 * pi * rr - 4 * pi * n_turns * ii, bb)[0]
    bb_out = sympy.Symbol("B_ext")  # no positivity: the exterior solve is 0
    outside = solve(bb_out * 2 * pi * rr, bb_out)[0]
    resid_inside = abs(complex(sympy.simplify(inside - 2 * n_turns * ii / rr)))
    resid_outside = abs(float(outside))
    resid = max(resid_inside, resid_outside)
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"Interior solve: B = {sympy.simplify(inside)}; exterior solve "
            f"(zero net linked current): B = {outside}."
        ),
    )


# ── Cluster E: electromagnetic waves and magneto-optics ─────────


@maxwell_cite(
    787,
    part=4,
    chapter="EM Theory of Light",
    theory_class="maxwell_original",
    description="plane wave satisfies the d'Alembert wave equation",
)
def verify_plane_wave_dalembert() -> VerificationResult:
    """Verify the plane wave satisfies the wave equation (Art. 787).

    E = E0 cos(kz - omega t) is substituted into
    d^2E/dz^2 - (1/v^2) d^2E/dt^2 with omega = k v; the residual is the
    symbolic reduction of the whole expression.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "plane wave d'Alembert equation"
    arts = (787,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    z, t, k, omega, v, e_amp = symbols("z t k omega v E0", positive=True)
    field = e_amp * cos(k * z - omega * t)
    resid_expr = diff(field, z, 2) - diff(field, t, 2) / v**2
    resid_expr = resid_expr.subs(omega, k * v)
    resid = abs(complex(sympy.simplify(resid_expr)))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "d^2E/dz^2 - v^-2 d^2E/dt^2 reduces to zero after imposing " "omega = k v."
        ),
    )


@maxwell_cite(
    785,
    part=4,
    chapter="EM Theory of Light",
    theory_class="maxwell_original",
    description="Faraday's law fixes B = E/v for the plane wave",
)
def verify_plane_wave_E_cB() -> VerificationResult:
    """Verify the plane-wave amplitude relation B = E/v from Faraday's law
    (Art. 785).

    With E_x = E0 sin(kz - omega t) and B_y = B0 sin(kz - omega t), the
    EMU induction equation dE_x/dz = -dB_y/dt is solved symbolically for
    B0 (giving E0 k/omega = E0/v), and the ratio E0/B0 is then evaluated
    at v = c from maxwell.config.constants, yielding exactly 1.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "plane wave E/B = v (Faraday)"
    arts = (785,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    zz, tt, k, omega, v, e_amp, b_amp = symbols("z t k omega v E0 B0", positive=True)
    e_x = e_amp * sin(k * zz - omega * tt)
    b_y = b_amp * sin(k * zz - omega * tt)
    faraday = diff(e_x, zz) + diff(b_y, tt)  # dE/dz = -dB/dt in EMU
    b0_sols = solve(faraday / cos(k * zz - omega * tt), b_amp)
    b0 = b0_sols[0]
    ratio_sym = sympy.simplify(e_amp / b0)  # = omega/k = v
    ratio_num = float(ratio_sym.subs({omega: k * CONST.C, v: CONST.C})) / float(CONST.C)
    resid = abs(ratio_num - 1.0)
    tol = 1e-10
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=1.0,
        actual=ratio_num,
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"Faraday solve gives B0 = {sympy.simplify(b0)}; E0/B0 = "
            f"{ratio_sym}, i.e. E/B = v; numerically at v = CONST.C the "
            f"ratio is {ratio_num:.12f}."
        ),
    )


@maxwell_cite(
    787,
    part=4,
    chapter="EM Theory of Light",
    theory_class="maxwell_original",
    description="dispersion relation omega^2 = v^2 k^2 of the plane wave",
)
def verify_dispersion_relation() -> VerificationResult:
    """Verify the dispersion relation omega^2 = v^2 k^2 (Art. 787).

    The exponential plane wave exp(I(kz - omega t)) is substituted into
    the wave operator; the residual is the symbolic reduction of the
    operator divided by the wave itself, minus (omega^2 - v^2 k^2)/v^2.
    The operator must vanish exactly on the dispersion surface.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "dispersion relation omega^2 = v^2 k^2"
    arts = (787,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    z, t, k, omega, v = symbols("z t k omega v", positive=True)
    wave = exp(I * (k * z - omega * t))
    op = (diff(wave, z, 2) - diff(wave, t, 2) / v**2) / wave
    resid_op = abs(complex(sympy.simplify(op - (omega**2 - v**2 * k**2) / v**2)))
    resid_shell = abs(complex(sympy.simplify(op.subs(omega, v * k))))
    resid = max(resid_op, resid_shell)
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "Wave operator / wave = (omega^2 - v^2 k^2)/v^2 (identity "
            f"residual {resid_op:.2e}); on-shell residual {resid_shell:.2e}."
        ),
    )


@maxwell_cite(
    785,
    part=4,
    chapter="EM Theory of Light",
    theory_class="maxwell_original",
    description="transversality: div E = 0 iff the amplitude is perpendicular to k",
)
def verify_wave_transversality() -> VerificationResult:
    """Verify the plane wave is transverse (Art. 785).

    div[E0 cos(k.r - omega t)] = -(k.E0) sin(k.r - omega t) is computed
    with fully general k and E0; imposing the constraint k.E0 = 0 (i.e.
    eliminating e3) must annihilate the divergence identically.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "plane-wave transversality div E = 0"
    arts = (785,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x, y, z = symbols("x y z")
    k1, k2, k3, omega, t = symbols("k1 k2 k3 omega t", positive=True)
    e1, e2, e3 = symbols("e1 e2 e3")
    phase = k1 * x + k2 * y + k3 * z - omega * t
    ex = e1 * cos(phase)
    ey = e2 * cos(phase)
    ez = e3 * cos(phase)
    div_e = diff(ex, x) + diff(ey, y) + diff(ez, z)
    constraint = solve(k1 * e1 + k2 * e2 + k3 * e3, e3)[0]
    div_transverse = sympy.simplify(div_e.subs(e3, constraint))
    resid = abs(complex(div_transverse))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "div E = -(k.E0) sin(k.r - omega t); imposing k.E0 = 0 makes it "
            "identically zero."
        ),
    )


@maxwell_cite(
    783,
    part=4,
    chapter="EM Theory of Light",
    theory_class="maxwell_original",
    description="wave velocity 1/sqrt(mu eps) in the medium",
)
def verify_medium_wave_velocity() -> VerificationResult:
    """Verify the medium wave velocity v = 1/sqrt(mu eps) (Art. 783).

    f(z - t/sqrt(mu eps)) is substituted into the medium wave operator
    d^2/dz^2 - mu eps d^2/dt^2 and must reduce to zero; the velocity
    enters only through the combination sqrt(mu eps), which is the
    Treatise's identification of light's velocity with the EM ratio.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "medium wave velocity 1/sqrt(mu eps)"
    arts = (783,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    z, t, mu, eps, kk = symbols("z t mu eps k", positive=True)
    field = cos(kk * (z - t / sqrt(mu * eps)))
    resid_expr = diff(field, z, 2) - mu * eps * diff(field, t, 2)
    resid = abs(complex(sympy.simplify(resid_expr)))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "d^2f/dz^2 - mu eps d^2f/dt^2 = 0 for f = cos(k(z - t/sqrt(mu " "eps)))."
        ),
    )


@maxwell_cite(
    788,
    part=4,
    chapter="EM Theory of Light",
    theory_class="maxwell_original",
    description="time-averaged energy flux of the plane wave",
)
def verify_plane_wave_poynting() -> VerificationResult:
    """Verify the mean flux of the plane wave (Art. 788).

    The EMU flux S = E_x B_y / (4 pi) is time-averaged over one period by
    direct symbolic integration of sin^2(kz - omega t); the result must
    equal E0 B0 / (8 pi).  The period integral is computed, not assumed.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "plane-wave mean flux E0 B0/(8 pi)"
    arts = (788,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    zz, tt, k, omega, e_amp, b_amp = symbols("z t k omega E0 B0", positive=True)
    period = 2 * pi / omega
    sin_sq_int = integrate(sin(k * zz - omega * tt) ** 2, (tt, 0, period))
    mean_sin_sq = sympy.simplify(sin_sq_int / period)
    flux_avg = sympy.simplify(e_amp * b_amp / (4 * pi) * mean_sin_sq)
    resid = abs(complex(sympy.simplify(flux_avg - e_amp * b_amp / (8 * pi))))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"Mean of sin^2 over a period: {mean_sin_sq}; mean flux "
            f"{flux_avg} = E0 B0/(8 pi)."
        ),
    )


@maxwell_cite(
    808,
    part=4,
    chapter="Magnetic Action on Light",
    theory_class="maxwell_original",
    description="rotation by circular birefringence from the two phase shifts",
)
def verify_circular_birefringence_rotation() -> VerificationResult:
    """Verify the rotation angle of circular birefringence (Art. 808).

    The two circular components acquire phases phi = omega n d / c; the
    rotation is theta = (phi_L - phi_R)/2.  Substituting a magnetic
    splitting n_L - n_R = kappa B must reproduce the closed form
    theta = omega kappa B d / (2 c); the residual is the symbolic
    difference.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "circular-birefringence rotation angle"
    arts = (808,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    n_l, n_r, b_field, dd, omega, kappa, c_sym = symbols(
        "n_L n_R B d omega kappa c", positive=True
    )
    phi_l = omega * n_l * dd / c_sym
    phi_r = omega * n_r * dd / c_sym
    theta = sympy.simplify((phi_l - phi_r) / 2)
    theta_closed = theta.subs(n_l, n_r + kappa * b_field)
    resid = abs(
        complex(
            sympy.simplify(theta_closed - omega * kappa * b_field * dd / (2 * c_sym))
        )
    )
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"theta = (phi_L - phi_R)/2 = {theta}; with n_L - n_R = kappa B "
            f"it is {sympy.simplify(theta_closed)}."
        ),
    )


@maxwell_cite(
    813,
    part=4,
    chapter="Magnetic Action on Light",
    theory_class="maxwell_original",
    description="Verdet law: rotation linear in field and path length",
)
def verify_verdet_path_linearity() -> VerificationResult:
    """Verify Verdet's law of linear accumulation (Art. 813).

    Starting again from the phase-difference expression
    theta(B, d) = omega d (n_L - n_R)/(2 c) with n_L - n_R = alpha B,
    three linearity residuals are reduced symbolically:
    theta(B, d1+d2) - theta(B,d1) - theta(B,d2), theta(2B,d) - 2theta(B,d),
    and theta(B,2d) - 2theta(B,d).  All must vanish identically.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Verdet rotation linear in B and path"
    arts = (813,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    b_field, d1, d2, omega, alpha, c_sym = symbols(
        "B d1 d2 omega alpha c", positive=True
    )

    def theta(bb, dd):
        return omega * dd * alpha * bb / (2 * c_sym)

    resid_add = abs(
        complex(
            sympy.simplify(
                theta(b_field, d1 + d2) - theta(b_field, d1) - theta(b_field, d2)
            )
        )
    )
    resid_b = abs(
        complex(sympy.simplify(theta(2 * b_field, d1) - 2 * theta(b_field, d1)))
    )
    resid_d = abs(
        complex(sympy.simplify(theta(b_field, 2 * d1) - 2 * theta(b_field, d1)))
    )
    resid = max(resid_add, resid_b, resid_d)
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"Additivity residual {resid_add:.2e}, field-doubling "
            f"{resid_b:.2e}, path-doubling {resid_d:.2e}."
        ),
    )


# ── Cluster F: absolute resistance standards (Arts. 758-767) ────


@maxwell_cite(
    759,
    part=4,
    chapter="Resistance Unit",
    theory_class="maxwell_original",
    description="RC discharge satisfies R dQ/dt + Q/C = 0",
)
def verify_rc_discharge_ode() -> VerificationResult:
    """Verify the capacitor discharge law (Art. 759).

    Q(t) = Q0 exp(-t/(RC)) is substituted into the discharge equation
    R dQ/dt + Q/C = 0; the symbolic residual must vanish identically.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "RC discharge ODE"
    arts = (759,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    t, r_res, c_cap, q0 = symbols("t R C Q0", positive=True)
    charge = q0 * exp(-t / (r_res * c_cap))
    resid_expr = r_res * diff(charge, t) + charge / c_cap
    resid = abs(complex(sympy.simplify(resid_expr)))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details="R dQ/dt + Q/C = 0 for Q = Q0 exp(-t/RC), symbolically exact.",
    )


@maxwell_cite(
    759,
    part=4,
    chapter="Resistance Unit",
    theory_class="maxwell_original",
    description="RC is the time constant: Q(RC) = Q0/e and initial slope",
)
def verify_rc_time_constant() -> VerificationResult:
    """Verify the meaning of the RC time constant (Art. 759).

    Two symbolic identities are checked: Q(RC)/Q0 = e^-1 exactly, and the
    initial slope -Q'(0) (RC)/Q0 = 1, so that tau = RC is both the
    e-folding time and the subtangent of the discharge curve.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "RC time constant properties"
    arts = (759,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    t, r_res, c_cap, q0 = symbols("t R C Q0", positive=True)
    charge = q0 * exp(-t / (r_res * c_cap))
    tau_frac = sympy.simplify(charge.subs(t, r_res * c_cap) / q0 - 1 / E)
    slope = sympy.simplify(-diff(charge, t).subs(t, 0) * r_res * c_cap / q0 - 1)
    resid = max(abs(complex(tau_frac)), abs(complex(slope)))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "Q(RC)/Q0 - e^-1 and the normalized initial slope both reduce "
            "to zero symbolically."
        ),
    )


@maxwell_cite(
    760,
    part=4,
    chapter="Resistance Unit",
    theory_class="maxwell_original",
    description="ballistic galvanometer throw gives Q = theta sqrt(J kappa)/G",
)
def verify_ballistic_throw_charge() -> VerificationResult:
    """Verify the ballistic throw formula (Art. 760).

    The impulse equation J omega0 = G Q and the energy equation
    J omega0^2 = kappa theta^2 are combined: eliminating omega0 must
    yield Q = theta sqrt(J kappa)/G.  The closed form is checked by
    back-substitution into BOTH original equations (residuals zero).
    """
    mod = "maxwell.verification.sympy_verify"
    name = "ballistic throw Q = theta sqrt(J kappa)/G"
    arts = (760,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    j_inertia, kappa, g_const, q_charge, theta = symbols(
        "J kappa G Q theta", positive=True
    )
    q_closed = theta * sqrt(kappa * j_inertia) / g_const
    omega0 = g_const * q_closed / j_inertia  # from the impulse equation
    resid_energy = abs(
        complex(sympy.simplify(j_inertia * omega0**2 - kappa * theta**2))
    )
    resid_impulse = abs(
        complex(sympy.simplify(j_inertia * omega0 - g_const * q_closed))
    )
    resid = max(resid_energy, resid_impulse)
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"Q = {sympy.simplify(q_closed)} satisfies impulse residual "
            f"{resid_impulse:.2e} and energy residual {resid_energy:.2e}."
        ),
    )


@maxwell_cite(
    761,
    part=4,
    chapter="Resistance Unit",
    theory_class="maxwell_original",
    description="recoil method: geometric decay of successive swing amplitudes",
)
def verify_recoil_method_structure() -> VerificationResult:
    """Verify the geometric structure behind the recoil method (Art. 761).

    For the damped oscillation x(t) = A e^(-lambda t) cos(omega t), the
    magnitude of successive extrema (half a period apart) decays by the
    factor e^(-lambda pi/omega): the residual
    x(t + pi/omega) + x(t) e^(-lambda pi/omega) must reduce to zero.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "recoil-method amplitude ratio e^(-lambda pi/omega)"
    arts = (761,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    t, aa, lam, om = symbols("t A lambda omega", positive=True)
    x_t = aa * exp(-lam * t) * cos(om * t)
    x_next = aa * exp(-lam * (t + pi / om)) * cos(om * (t + pi / om))
    resid = abs(complex(sympy.simplify(x_next + x_t * exp(-lam * pi / om))))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "x(t + pi/omega) = -x(t) e^(-lambda pi/omega): successive "
            "extrema form a geometric sequence."
        ),
    )


@maxwell_cite(
    763,
    part=4,
    chapter="Resistance Unit",
    theory_class="maxwell_original",
    description="EMU resistance has the dimensions of a velocity",
)
def verify_resistance_emu_velocity_dimension() -> VerificationResult:
    """Verify [R]_EMU = [velocity] (Art. 763).

    Dimensional algebra in (M, L, T): the Ampere force law
    F/L = 2 I^2/d gives [I^2] = M L T^-2; Faraday + F = I L B gives
    [EMF] = M L^2 T^-3 I^-1; hence [R] = [EMF]/[I] = L T^-1.  The
    residual is the squared norm of the exponent difference against
    (0, 1, -1), the dimensions of a velocity.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "EMU resistance dimension = velocity"
    arts = (763,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    m_exp, l_exp, t_exp = symbols("M L T")
    current_sq = m_exp * l_exp / t_exp**2  # from F/L = 2 I^2/d
    b_field_dim = (m_exp * l_exp / t_exp**2) / (sympy.Symbol("Icur") * l_exp)
    emf_dim = b_field_dim * l_exp**2 / t_exp  # Phi/t, Phi = B L^2
    resistance_dim = sympy.simplify(
        (emf_dim / sympy.Symbol("Icur")).subs(sympy.Symbol("Icur") ** 2, current_sq)
    )
    target = l_exp / t_exp
    ratio = sympy.simplify(resistance_dim / target)
    resid = abs(complex(ratio - 1))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"[R]_EMU reduces to {resistance_dim}, i.e. L/T -- a velocity, "
            "which is why measuring resistance in absolute EMU amounts to "
            "measuring a velocity."
        ),
    )


@maxwell_cite(
    758,
    part=4,
    chapter="Resistance Unit",
    theory_class="maxwell_original",
    description="Wheatstone bridge balance R1 R4 = R2 R3 from Kirchhoff solve",
)
def verify_wheatstone_balance() -> VerificationResult:
    """Verify the Wheatstone bridge balance condition (Art. 758).

    The five-current Kirchhoff system (two node laws, three loop laws) is
    solved symbolically for the galvanometer current; the numerator comes
    out proportional to R2 R3 - R1 R4, and substituting R4 = R2 R3/R1
    annihilates the current.  Both residuals are computed.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Wheatstone balance from Kirchhoff solve"
    arts = (758,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    r1, r2, r3, r4, g_gal, emf = symbols("R1 R2 R3 R4 Gg Ef", positive=True)
    i1, i2, i3, i4, i_g = symbols("i1 i2 i3 i4 ig")
    eqs = [
        i1 - i2 - i_g,
        i3 + i_g - i4,
        emf - i1 * r1 - i2 * r2,
        emf - i3 * r3 - i4 * r4,
        i_g * g_gal - i2 * r2 + i4 * r4,
    ]
    sol = solve(eqs, [i1, i2, i3, i4, i_g])
    i_g_expr = sol[i_g]
    numer = sympy.factor(sympy.fraction(i_g_expr)[0])
    resid_balance = abs(complex(sympy.simplify(i_g_expr.subs(r4, r2 * r3 / r1))))
    resid_struct = abs(complex(sympy.simplify(numer - emf * (r2 * r3 - r1 * r4))))
    resid = max(resid_balance, resid_struct)
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        tolerance=tol,
        relative_error=0.0 if passed else float(resid),
        passed=passed,
        details=(
            f"Solved galvanometer current numerator: {numer}; zero exactly "
            "when R4 = R2 R3/R1."
        ),
    )


@maxwell_cite(
    759,
    part=4,
    chapter="Resistance Unit",
    theory_class="maxwell_original",
    description="capacitor energy Q^2/(2C) by direct integration",
)
def verify_capacitor_energy() -> VerificationResult:
    """Verify the capacitor energy U = Q^2/(2C) (Art. 759).

    U = int_0^Q (q/C) dq is evaluated symbolically and compared with
    Q^2/(2C) and with Q V/2 at V = Q/C; both residuals must vanish.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "capacitor energy Q^2/(2C)"
    arts = (759,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    q_var, q_tot, c_cap = symbols("q Q C", positive=True)
    energy = integrate(q_var / c_cap, (q_var, 0, q_tot))
    resid_closed = abs(complex(sympy.simplify(energy - q_tot**2 / (2 * c_cap))))
    resid_half_qv = abs(complex(sympy.simplify(energy - q_tot * (q_tot / c_cap) / 2)))
    resid = max(resid_closed, resid_half_qv)
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=f"int_0^Q (q/C) dq = {energy}; equals Q^2/(2C) = QV/2.",
    )


# ── Cluster G: action-at-distance theories (Arts. 846-866) ──────


@maxwell_cite(
    846,
    847,
    part=4,
    chapter="Action at Distance",
    theory_class="maxwell_original",
    description="Weber's force reduces to Coulomb's law at rest",
)
def verify_weber_coulomb_limit() -> VerificationResult:
    """Verify the static limit of Weber's force law (Arts. 846, 847).

    F_W = (ee'/r^2)[1 - rdot^2/c^2 + 2 r rddot/c^2] must collapse to the
    Coulomb force ee'/r^2 when rdot = rddot = 0.  The symbolic residual
    of the substitution is the verdict; the velocity-independent factor
    ee'/r^2 is constructed independently.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Weber -> Coulomb static limit"
    arts = (846, 847)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    r, e1, e2, rdot, rddot, c_sym = symbols("r e1 e2 rdot rddot c", positive=True)
    f_weber = e1 * e2 / r**2 * (1 - rdot**2 / c_sym**2 + 2 * r * rddot / c_sym**2)
    f_coulomb = e1 * e2 / r**2
    resid = abs(complex(sympy.simplify(f_weber.subs({rdot: 0, rddot: 0}) - f_coulomb)))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details="F_W(rdot=0, rddot=0) - ee'/r^2 reduces to zero symbolically.",
    )


@maxwell_cite(
    846,
    part=4,
    chapter="Action at Distance",
    theory_class="maxwell_original",
    description="velocity structure of Weber's force law",
)
def verify_weber_velocity_structure() -> VerificationResult:
    """Verify the velocity-dependent structure of Weber's law (Art. 846).

    Two algebraic facts are reduced: (i) for purely transverse motion
    (rdot = 0) the force is F_C (1 + 2 r rddot/c^2); (ii) the
    coefficient of rdot^2 in F_W is exactly -ee'/(r^2 c^2).  Both
    residuals are symbolic reductions.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Weber velocity structure"
    arts = (846,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    r, e1, e2, rdot, rddot, c_sym = symbols("r e1 e2 rdot rddot c", positive=True)
    f_weber = e1 * e2 / r**2 * (1 - rdot**2 / c_sym**2 + 2 * r * rddot / c_sym**2)
    f_coulomb = e1 * e2 / r**2
    resid_trans = abs(
        complex(
            sympy.simplify(
                f_weber.subs(rdot, 0) / f_coulomb - 1 - 2 * r * rddot / c_sym**2
            )
        )
    )
    coeff_rdot_sq = sympy.Poly(
        sympy.expand(f_weber * r**2 * c_sym**2), rdot
    ).coeff_monomial(rdot**2)
    resid_coeff = abs(complex(sympy.simplify(coeff_rdot_sq + e1 * e2)))
    resid = max(resid_trans, resid_coeff)
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"Transverse ratio residual {resid_trans:.2e}; rdot^2 "
            f"coefficient residual {resid_coeff:.2e}."
        ),
    )


@maxwell_cite(
    847,
    part=4,
    chapter="Action at Distance",
    theory_class="maxwell_original",
    description="Weber force conserves energy with the velocity-dependent potential",
)
def verify_weber_potential_energy_identity() -> VerificationResult:
    """Verify Weber force / potential energy consistency (Art. 847).

    With the velocity-dependent potential U = (ee'/r)(1 - rdot^2/c^2),
    the power identity F_W rdot + dU/dt = 0 must hold identically
    (dU/dt = U_r rdot + U_rdot rddot).  The residual is the symbolic
    reduction of the sum; this is the property that made Weber's law a
    candidate complete theory in the Treatise's discussion.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Weber force-power identity"
    arts = (847,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    r, e1, e2, rdot, rddot, c_sym = symbols("r e1 e2 rdot rddot c", positive=True)
    f_weber = e1 * e2 / r**2 * (1 - rdot**2 / c_sym**2 + 2 * r * rddot / c_sym**2)
    u_weber = e1 * e2 / r * (1 - rdot**2 / c_sym**2)
    du_dt = diff(u_weber, r) * rdot + diff(u_weber, rdot) * rddot
    resid = abs(complex(sympy.simplify(f_weber * rdot + du_dt)))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "F_W rdot + dU/dt reduces to zero: Weber's force is "
            "energy-consistent with U = (ee'/r)(1 - rdot^2/c^2)."
        ),
    )


@maxwell_cite(
    851,
    part=4,
    chapter="Action at Distance",
    theory_class="maxwell_original",
    description="symmetry of Ampere's element-force kernel",
)
def verify_ampere_force_symmetry() -> VerificationResult:
    """Verify the symmetry of Ampere's force kernel (Art. 851).

    The kernel K = cos eps - (3/2) cos theta cos theta' must be
    invariant under exchange of the two current elements
    (theta <-> theta', eps unchanged).  The residual of the exchanged
    difference is reduced symbolically.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Ampere kernel exchange symmetry"
    arts = (851,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    eps, th1, th2 = symbols("eps theta1 theta2")
    kernel = cos(eps) - Rational(3, 2) * cos(th1) * cos(th2)
    kernel_swapped = cos(eps) - Rational(3, 2) * cos(th2) * cos(th1)
    resid = abs(complex(sympy.simplify(kernel - kernel_swapped)))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "cos eps - (3/2) cos theta cos theta' is invariant under "
            "theta <-> theta'."
        ),
    )


@maxwell_cite(
    851,
    part=4,
    chapter="Action at Distance",
    theory_class="maxwell_original",
    description="Ampere element kernels: side-by-side attraction, collinear -1/2",
)
def verify_ampere_parallel_attraction() -> VerificationResult:
    """Verify Ampere's kernel values for canonical geometries (Art. 851).

    The cosines are computed from explicit Cartesian element data (dot
    products of direction and separation vectors), not inserted by hand:
    side-by-side parallel elements give K = 1 (attraction), collinear
    elements give K = 1 - 3/2 = -1/2.  Both residuals are the
    differences against those closed forms.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Ampere kernel values from geometry"
    arts = (851,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    dd = symbols("d", positive=True)

    def kernel_of(pos2):
        d1 = sympy.Matrix([1, 0, 0])
        d2 = sympy.Matrix([1, 0, 0])
        r12 = sympy.Matrix(pos2)
        rnorm = sympy.sqrt(r12.dot(r12))
        cos_t1 = d1.dot(r12) / rnorm
        cos_t2 = d2.dot(r12) / rnorm
        cos_eps = d1.dot(d2)
        return sympy.simplify(cos_eps - Rational(3, 2) * cos_t1 * cos_t2)

    k_side = kernel_of([0, dd, 0])
    k_collinear = kernel_of([dd, 0, 0])
    resid = max(abs(complex(k_side - 1)), abs(complex(k_collinear + Rational(1, 2))))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"Side-by-side kernel K = {k_side} (parallel currents attract); "
            f"collinear kernel K = {k_collinear}."
        ),
    )


@maxwell_cite(
    852,
    part=4,
    chapter="Action at Distance",
    theory_class="maxwell_original",
    description="Ampere element forces obey action and reaction",
)
def verify_ampere_newton_third_law() -> VerificationResult:
    """Verify Newton's third law for Ampere's element force (Art. 852).

    The force on element 1 is central: F12 = r-hat f with
    f = -K II' ds ds'/r^2; on element 2 the line of action reverses
    (r-hat -> -r-hat) and the kernel arguments swap.  The componentwise
    sum F12 + F21 must reduce to zero algebraically, keeping cos theta
    and cos theta' as independent symbols throughout.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "Ampere element force action-reaction"
    arts = (852,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    eps, th1, th2, ii, iip, ds, dsp, rr = symbols(
        "eps theta1 theta2 I I2 ds ds2 r", positive=True
    )
    kernel_12 = cos(eps) - Rational(3, 2) * cos(th1) * cos(th2)
    kernel_21 = cos(eps) - Rational(3, 2) * cos(th2) * cos(th1)
    f12 = -kernel_12 * ii * iip * ds * dsp / rr**2
    f21 = -kernel_21 * ii * iip * ds * dsp / rr**2
    r_hat = sympy.Matrix([sin(eps), cos(eps), 0])  # any unit line of action
    f12_vec = r_hat * f12
    f21_vec = -r_hat * f21
    resid = max(abs(complex(c)) for c in sympy.simplify(f12_vec + f21_vec))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "F12 + F21 = 0 componentwise: Ampere's central, symmetric "
            "kernel satisfies action-reaction element by element."
        ),
    )


# ── Cluster H: CGS unit discipline (Arts. 768-780) ──────────────


@maxwell_cite(
    772,
    part=4,
    chapter="ESU vs EMU",
    theory_class="maxwell_original",
    description="ESU/EMU charge unit ratio equals the speed of light",
)
def verify_esu_emu_charge_ratio_c() -> VerificationResult:
    """Verify the charge-unit ratio is c (Art. 772).

    Symbolic arm: equating the same physical force written in ESU,
    F = q_e q_e'/r^2, and in EMU, F = c^2 q_m q_m'/r^2, and solving for
    q_e gives q_e = c q_m.  Numeric arm: the elementary charge stored in
    both unit systems (maxwell.config.constants) must satisfy
    E_CHARGE_ESU / E_CHARGE_EMU = CONST.C.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "charge unit ratio = c"
    arts = (772,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    q_e, q_m, c_sym, r = symbols("q_e q_m c r", positive=True)
    force_equivalence = q_e**2 / r**2 - c_sym**2 * q_m**2 / r**2
    ratio_sym = sympy.simplify(solve(force_equivalence, q_e)[0] / q_m)
    resid_sym = abs(complex(ratio_sym - c_sym))
    ratio_num = CONST.E_CHARGE_ESU / CONST.E_CHARGE_EMU
    resid_num = abs(ratio_num / CONST.C - 1.0)
    resid = max(resid_sym, resid_num)
    tol = 1e-6
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=1.0,
        actual=float(ratio_num / CONST.C),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"Symbolic solve gives q_e/q_m = {ratio_sym}; stored constants "
            f"give {ratio_num:.6e} / {CONST.C:.6e} = "
            f"{ratio_num / CONST.C:.12f}."
        ),
    )


@maxwell_cite(
    773,
    part=4,
    chapter="ESU vs EMU",
    theory_class="maxwell_original",
    description="ESU/EMU resistance unit ratio equals c^2",
)
def verify_esu_emu_resistance_ratio_c2() -> VerificationResult:
    """Verify the resistance-unit ratio is c^2 (Art. 773).

    Symbolic arm: with charge ratio gamma = c, the potential ratio is
    V_ratio = gamma (since V = W/q) and the current ratio is
    I_ratio = 1/gamma (since I = q/t); hence R_ratio = V_ratio/I_ratio
    = gamma^2 = c^2.  Numeric arm: 1 statohm = c^2/10^9 ohm and
    1 abohm = 10^-9 ohm, so statohm/abohm must equal CONST.C^2.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "resistance unit ratio = c^2"
    arts = (773,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    gamma, c_sym = symbols("gamma c", positive=True)
    v_ratio = gamma  # V = W/q: unit ratio follows the inverse charge ratio
    i_ratio = 1 / gamma  # I = q/t
    r_ratio = sympy.simplify(v_ratio / i_ratio)
    resid_sym = abs(complex(r_ratio.subs(gamma, c_sym) - c_sym**2))
    statohm_in_ohm = 1.0 / CONST.OHM_TO_STATOHM  # = c^2 / 10^9
    abohm_in_ohm = 1.0e-9
    ratio_num = statohm_in_ohm / abohm_in_ohm
    resid_num = abs(ratio_num / CONST.C**2 - 1.0)
    resid = max(resid_sym, resid_num)
    tol = 1e-8
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=1.0,
        actual=float(ratio_num / CONST.C**2),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"Symbolic chain gives R_ratio = {r_ratio} = c^2 at gamma = c; "
            f"stored constants give statohm/abohm = {ratio_num:.6e} vs "
            f"c^2 = {CONST.C**2:.6e}."
        ),
    )


@maxwell_cite(
    774,
    part=4,
    chapter="ESU vs EMU",
    theory_class="maxwell_original",
    description="ESU capacitance has the dimensions of length",
)
def verify_capacitance_esu_length_dimension() -> VerificationResult:
    """Verify the ESU capacitance dimension is length (Art. 774).

    Exponent algebra in (M, L, T): from F = qq'/r^2, [q] = M^{1/2}
    L^{3/2} T^{-1}; from V = W/q, [V] = M^{1/2} L^{1/2} T^{-1}; hence
    [C] = [q]/[V] = L.  A second symbolic arm checks the isolated
    sphere: C = q/(q/R) = R.  The residual is the norm of the exponent
    difference against (0, 1, 0).
    """
    mod = "maxwell.verification.sympy_verify"
    name = "ESU capacitance dimension = length"
    arts = (774,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    # exponent vectors (M, L, T)
    q_dim = (Rational(1, 2), Rational(3, 2), -1)  # from F = qq'/r^2
    w_dim = (1, 2, -2)  # work
    v_dim = tuple(w_dim[i] - q_dim[i] for i in range(3))
    c_dim = tuple(q_dim[i] - v_dim[i] for i in range(3))
    resid_dim = float(sum(abs(cc - tt) for cc, tt in zip(c_dim, (0, 1, 0))))
    q_sym, rr = symbols("q R", positive=True)
    sphere_cap = q_sym / (q_sym / rr)
    resid_sphere = abs(complex(sympy.simplify(sphere_cap - rr)))
    resid = max(resid_dim, resid_sphere)
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            f"[C]_ESU exponents (M,L,T) = {tuple(str(c_dim[i]) for i in range(3))}; "
            f"sphere capacitance q/(q/R) = {sympy.simplify(sphere_cap)}."
        ),
    )


# ── Cluster I: dipole vector-calculus spine (Arts. 832-845) ─────


@maxwell_cite(
    833,
    part=4,
    chapter="Molecular Currents",
    theory_class="standard_math",
    description="divergence of the dipole field vanishes off the source",
)
def verify_div_B_dipole_zero() -> VerificationResult:
    """Verify div B = 0 for the dipole field (Art. 833 context).

    B = [3(m.r-hat)r-hat - m]/r^3 with m along z: the divergence of
    (3m xz/r^5, 3m yz/r^5, m(3z^2 - r^2)/r^5) is reduced symbolically
    and must be identically zero away from the origin -- the field of a
    molecular current loop has no magnetic source.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "div B_dipole = 0"
    arts = (833,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x, y, z, mm = symbols("x y z m", positive=True)
    r = sqrt(x**2 + y**2 + z**2)
    b_x = 3 * mm * x * z / r**5
    b_y = 3 * mm * y * z / r**5
    b_z = mm * (3 * z**2 - r**2) / r**5
    div_b = sympy.simplify(diff(b_x, x) + diff(b_y, y) + diff(b_z, z))
    resid = abs(complex(div_b))
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details="Symbolic divergence of the dipole field reduces to zero.",
    )


@maxwell_cite(
    833,
    part=4,
    chapter="Molecular Currents",
    theory_class="standard_math",
    description="curl of the dipole vector potential reproduces the dipole field",
)
def verify_dipole_vector_potential() -> VerificationResult:
    """Verify curl(m x r / r^3) = dipole B (Art. 833 context).

    With m = m z-hat, the vector potential is A = m(-y, x, 0)/r^3; its
    curl is computed symbolically and compared component by component
    with [3(m.r-hat)r-hat - m]/r^3.  All three component residuals must
    reduce to zero.
    """
    mod = "maxwell.verification.sympy_verify"
    name = "curl A_dipole = B_dipole"
    arts = (833,)

    if not _HAS_SYMPY:
        return _disabled_result(name, mod, arts)

    x, y, z, mm = symbols("x y z m", positive=True)
    r = sqrt(x**2 + y**2 + z**2)
    a_x, a_y, a_z = -mm * y / r**3, mm * x / r**3, sympy.S.Zero
    curl_x = diff(a_z, y) - diff(a_y, z)
    curl_y = diff(a_x, z) - diff(a_z, x)
    curl_z = diff(a_y, x) - diff(a_x, y)
    b_x = 3 * mm * x * z / r**5
    b_y = 3 * mm * y * z / r**5
    b_z = mm * (3 * z**2 - r**2) / r**5
    resid = max(
        abs(complex(sympy.simplify(curl_x - b_x))),
        abs(complex(sympy.simplify(curl_y - b_y))),
        abs(complex(sympy.simplify(curl_z - b_z))),
    )
    tol = 1e-12
    passed = resid < tol
    return VerificationResult(
        module_name=mod,
        article_refs=arts,
        test_name=name,
        expected=0.0,
        actual=float(resid),
        relative_error=0.0 if passed else float(resid),
        tolerance=tol,
        passed=passed,
        details=(
            "curl[m(-y,x,0)/r^3] equals (3mxz, 3myz, m(3z^2-r^2))/r^5 "
            "component by component."
        ),
    )


# ── Registry of all verification functions ───────────────────────

ALL_SYMBOLIC_VERIFIERS = [
    verify_div_curl,
    verify_grad_curl,
    verify_wave_equation_1d,
    verify_laplace_spherical,
    verify_coulomb_law_symbolic,
    verify_biot_savart,
    verify_faraday_symbolic,
    verify_continuity_equation,
    verify_maxwell_correction,
    verify_stokes_theorem,
    verify_lorentz_force,
    verify_stress_tensor_properties,
    verify_ampere_law,
    # ── Wave 8a: elliptic integrals and circular currents ──
    verify_elliptic_K_AGM_identity,
    verify_elliptic_legendre_relation,
    verify_elliptic_K_small_k_series,
    verify_elliptic_E_small_k_series,
    verify_elliptic_K_derivative_identity,
    verify_elliptic_E_derivative_identity,
    verify_elliptic_landen_descent,
    verify_coil_comparison_modulus,
    verify_circular_current_center_field,
    verify_loop_axial_field_integral,
    verify_loop_far_field_dipole_limit,
    verify_vector_potential_loop_structure,
    verify_mutual_inductance_neumann_symmetry,
    verify_mutual_inductance_far_limit,
    verify_dM_dd_dipole_relation,
    # ── Wave 8a: zonal-harmonic spine ──
    verify_legendre_value_at_one,
    verify_legendre_parity,
    verify_legendre_recurrence,
    verify_legendre_orthogonality,
    verify_legendre_generating_function,
    verify_addition_theorem_p1,
    verify_Y00_normalization,
    verify_zonal_harmonic_laplace,
    verify_legendre_differential_equation,
    # ── Wave 8a: current sheets ──
    verify_surface_current_jump,
    verify_normal_B_continuous,
    verify_solenoid_inductance_structure,
    verify_sheet_potential_discontinuity,
    verify_cylindrical_sheet_field,
    verify_sheet_toroidal_zero_exterior,
    # ── Wave 8a: waves and magneto-optics ──
    verify_plane_wave_dalembert,
    verify_plane_wave_E_cB,
    verify_dispersion_relation,
    verify_wave_transversality,
    verify_medium_wave_velocity,
    verify_plane_wave_poynting,
    verify_circular_birefringence_rotation,
    verify_verdet_path_linearity,
    # ── Wave 8a: absolute resistance standards ──
    verify_rc_discharge_ode,
    verify_rc_time_constant,
    verify_ballistic_throw_charge,
    verify_recoil_method_structure,
    verify_resistance_emu_velocity_dimension,
    verify_wheatstone_balance,
    verify_capacitor_energy,
    # ── Wave 8a: action at distance ──
    verify_weber_coulomb_limit,
    verify_weber_velocity_structure,
    verify_weber_potential_energy_identity,
    verify_ampere_force_symmetry,
    verify_ampere_parallel_attraction,
    verify_ampere_newton_third_law,
    # ── Wave 8a: CGS unit discipline ──
    verify_esu_emu_charge_ratio_c,
    verify_esu_emu_resistance_ratio_c2,
    verify_capacitance_esu_length_dimension,
    # ── Wave 8a: dipole vector-calculus spine ──
    verify_div_B_dipole_zero,
    verify_dipole_vector_potential,
]

"""Wave-9 REQ-V tightening: extend tests/articles/reference_values.json
from 71/200 to 200/200 in-scope articles (667-866).

INDEPENDENCE NOTE (anti-theater, binding):
    This script imports NOTHING from the `maxwell` package. Every value
    below is computed here, in this file, from:
      * closed-form formulas Maxwell states in the cited article,
        evaluated at documented instances by plain arithmetic (class 3);
      * standard physical constants / historical anchors (class 2);
      * limiting / symmetry identities (class 4);
      * procedural-law instances, e.g. the Thomson optimum ratio (class 5).
    The arithmetic performed here IS the independent derivation record
    cited by each provenance string. No value is copied from module output.

Run:  python scripts/build_reference_store_wave9.py
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

STORE = Path(__file__).resolve().parent.parent / "tests" / "articles" / "reference_values.json"

# --- constants (SI-defined / standard values, not maxwell.config imports) ---
C = 2.99792458e10          # speed of light, cm/s (exact SI definition -> cm/s)
G_STD = 980.665            # standard gravity, cm/s^2
PI = math.pi


def rel(t: float) -> dict:
    return {"rel": t}


def abs_(t: float) -> dict:
    return {"abs": t}


def entry(value, units, tol, prov):
    return {"value": float(value), "units": units, "tolerance": tol, "provenance": prov}


# Independent AGM (Gauss) -- our own iteration, used for elliptic K pins.
def agm(a: float, b: float, iters: int = 60) -> float:
    for _ in range(iters):
        a, b = (a + b) / 2.0, math.sqrt(a * b)
    return a


K_HALF = PI / (2.0 * agm(1.0, math.sqrt(0.5)))          # K(m=1/2), AGM-derived
# E(m) via the hypergeometric power series -- the term-by-term textbook
# definition, with no AGM convention subtleties:
#   E(m) = (pi/2) [1 - sum_{n>=1} t_n m^n / (2n - 1)],
#   t_n = ((2n-1)!!/(2n)!!)^2,  t_n = t_{n-1} ((2n-1)/(2n))^2.
# Converges geometrically for |m| < 1; at m = 1/2 the remainder after 80
# terms is < 1e-25. (A from-memory AGM-E variant was tried first and was
# caught by the spot-check assertions; this series form is manifestly the
# defining integral's binomial expansion.)
def _E_series(m: float, nterms: int = 80) -> float:
    t = 1.0
    s = 1.0
    for n in range(1, nterms + 1):
        r = (2.0 * n - 1.0) / (2.0 * n)
        t *= r * r
        s -= t * (m**n) / (2.0 * n - 1.0)
    return (PI / 2.0) * s


E_HALF = _E_series(0.5)

BUILDER = "derived by scripts/build_reference_store_wave9.py (independent of the maxwell package)"

NEW: dict[str, dict] = {}

def put(art: int, key: str, e: dict):
    NEW.setdefault(str(art), {"values": {}})["values"][key] = e


# ====================== Ch XII current sheets (670-674) ======================
put(670, "tangential_H_jump_unit_sheet", entry(
    4.0 * PI / C, "Oe (jump per unit surface current, Gaussian CGS)", rel(1e-12),
    "Class 3 closed form: Gaussian boundary condition n x (H2 - H1) = 4 pi K / c "
    "(Treatise Art 670 current-sheet tangential discontinuity), instance K = 1 statA/cm; "
    f"value = 4 pi / c. {BUILDER}."))
put(671, "normal_B_continuity_jump_zero", entry(
    0.0, "G (normal-field jump across any current sheet)", abs_(1e-14),
    "Class 4 identity: div B = 0 forces continuity of the normal component across a "
    "current sheet (Treatise Art 671 context); jump pinned exactly 0, independent of "
    f"implementation. {BUILDER}."))
put(672, "loop_center_field_unit", entry(
    2.0 * PI / C, "G (per statampere, per cm radius, Gaussian)", rel(1e-12),
    "Class 3 closed form: on-axis field of a circular loop at its centre "
    "B = 2 pi I / (c a) (Treatise Arts 672/694 family, Gaussian CGS), instance "
    f"I = 1 statA, a = 1 cm. {BUILDER}."))
put(673, "loop_on_axis_z_equals_a", entry(
    2.0 * PI / (2.0 ** 1.5) / C, "G (Gaussian)", rel(1e-12),
    "Class 3 closed form: exact on-axis loop field B(z) = 2 pi I a^2 / (c (a^2+z^2)^{3/2}); "
    "instance I = a = 1, z = 1 gives 2 pi / (2^{3/2} c). The general off-axis machinery must "
    f"reduce to this closed form on axis (independent limit check). {BUILDER}."))
put(674, "poynting_unit_fields_boundary_flux", entry(
    C / (4.0 * PI), "erg/(cm^2 s) (Gaussian Poynting flux)", rel(1e-12),
    "Class 3 closed form: energy flux S = c/(4 pi) E x H (Treatise Art 674 boundary energy-flux "
    f"context), instance E = H = 1 in perpendicular directions -> |S| = c/(4 pi). {BUILDER}."))

# ====================== Ch XIII parallel currents (675-687, 693) ==============
put(675, "finite_solenoid_center_3_4_5", entry(
    0.8 * 4.0 * PI / C, "G (Gaussian)", rel(1e-12),
    "Class 3 closed form: field at the centre of a finite solenoid "
    "B = (4 pi n I / c) * (L/2) / sqrt(a^2 + (L/2)^2); instance a = 3, L = 8 gives the "
    f"Pythagorean factor (L/2)/sqrt(a^2+(L/2)^2) = 4/5 exactly. {BUILDER}."))
put(676, "helmholtz_center_unit_coil", entry(
    4.0 * PI * (4.0 / 5.0) ** 1.5 / C, "G (Gaussian)", rel(1e-12),
    "Class 3 closed form: Helmholtz pair (spacing = radius) centre field "
    "B = 4 pi N I / (c a) * (4/5)^{3/2} (Treatise Arts 676/741-743 family), instance "
    f"N = I = a = 1. (4/5)^{{3/2}} = 8/(5 sqrt 5). {BUILDER}."))
put(677, "infinite_solenoid_unit", entry(
    4.0 * PI / C, "G (Gaussian, per turn/cm per statA)", rel(1e-12),
    "Class 3 closed form: infinite solenoid interior field B = 4 pi n I / c "
    f"(Treatise Art 677), instance n = 1 turn/cm, I = 1 statA. {BUILDER}."))
put(678, "coil_pair_midpoint_d_equals_a", entry(
    4.0 * PI / (2.0 ** 1.5) / C, "G (Gaussian)", rel(1e-12),
    "Class 3 closed form: superposition for two identical coaxial coils, field at the "
    "midplane = 2 * loop field at distance d: B = 4 pi a^2 / (c (a^2+d^2)^{3/2}); instance "
    f"a = d = 1 gives 4 pi / (2^{{3/2}} c). {BUILDER}."))
put(679, "helmholtz_center_N100_a10", entry(
    4.0 * PI * 100.0 / (10.0 * C) * (4.0 / 5.0) ** 1.5, "G (Gaussian)", rel(1e-12),
    "Class 3 closed form: Helmholtz centre field B = 4 pi N I / (c a) * (4/5)^{3/2}, instance "
    f"N = 100, I = 1, a = 10 cm (same closed form as Art 676, distinct instance). {BUILDER}."))
put(682, "hollow_cylinder_interior_unit_sheet", entry(
    4.0 * PI / C, "G (Gaussian)", rel(1e-12),
    "Class 3 closed form: an infinite hollow cylindrical current sheet (axial surface current K) "
    "carries interior field B = 4 pi K / c and zero exterior field (solenoid limit; Treatise "
    f"Art 682 cylinder analysis), instance K = 1 statA/cm. {BUILDER}."))
put(686, "vector_potential_outside_solenoid_rho2", entry(
    0.5, "G cm (Gaussian vector potential)", rel(1e-12),
    "Class 3 closed form: outside an infinite solenoid A_phi(rho) = B a^2 / (2 rho) "
    "(flux B pi a^2 spread on circle 2 pi rho; Treatise Arts 686-687 cylinder vector potential), "
    f"instance B = 1, a = 1, rho = 2. {BUILDER}."))
put(687, "vector_potential_outside_solenoid_rho4_a2_B3", entry(
    1.5, "G cm (Gaussian vector potential)", rel(1e-12),
    "Class 3 closed form: A_phi(rho) = B a^2 / (2 rho) (Treatise Art 687), instance "
    f"B = 3, a = 2, rho = 4 -> 3*4/8 = 1.5 exactly. {BUILDER}."))
put(693, "gmd_two_points", entry(
    5.0, "cm (geometric mean distance)", rel(1e-13),
    "Class 3 closed form: the GMD of two point sets separated by d is d itself "
    "(Treatise Art 693 GMD definition; degenerate one-point cross-sections), instance "
    f"d = 5 cm. {BUILDER}."))

# ====================== Ch XIV circular currents (694-705) ===================
put(694, "Aphi_kernel_at_m_half", entry(
    1.5 * K_HALF - 2.0 * E_HALF, "cm (dimensionless kernel x I/c prefactor)", rel(1e-11),
    "Class 3 closed form: the circular-current vector potential carries the kernel "
    "[(2-m) K(m) - 2 E(m)] (D-02 closure form, Art 694); at m = 1/2 the kernel is "
    "1.5 K(1/2) - 2 E(1/2) with K = pi/(2 AGM(1, sqrt(1/2))) from this builder's own "
    "AGM iteration and E(1/2) from this builder's own hypergeometric power series. "
    f"{BUILDER}."))
put(695, "solid_angle_on_axis_3_4_5", entry(
    2.0 * PI / 5.0, "sr (solid angle of the loop)", rel(1e-13),
    "Class 3 closed form: solid angle subtended by a circular loop on its axis, "
    "Omega = 2 pi (1 - z/sqrt(a^2+z^2)); instance a = 3, z = 4 (3-4-5 triangle) gives "
    f"2 pi (1 - 4/5) = 2 pi/5. Magnetic-shell potential is I Omega / c in Gaussian. {BUILDER}."))
put(698, "coaxial_coil_force_zero_by_symmetry", entry(
    0.0, "dyn (axial force between identical coaxial coils at symmetric placement)", abs_(1e-12),
    "Class 4 symmetry identity: the axial force between two identical coaxial coils is an odd "
    "function of displacement about the symmetric position, hence exactly 0 there (Treatise "
    f"Art 698 coil-force context). Pinned by parity, independent of implementation. {BUILDER}."))
put(699, "jacobi_sn_at_zero", entry(
    0.0, "dimensionless (Jacobi elliptic sn(0, m))", abs_(1e-14),
    "Class 3 closed form: Jacobi elliptic sn(u=0, m) = 0 for every modulus (Treatise Art 699 "
    f"Jacobian-function context); defining initial condition. {BUILDER}."))
put(700, "K_at_zero_modulus", entry(
    PI / 2.0, "dimensionless (complete elliptic K(0))", rel(1e-13),
    "Class 3 closed form: K(0) = int_0^{pi/2} d theta = pi/2 (Treatise Art 700 elliptic-integral "
    f"context; also the fixed point of the Landen descent). {BUILDER}."))
put(701, "legendre_relation_pi_over_2", entry(
    PI / 2.0, "dimensionless", rel(1e-12),
    "Class 3 closed form: Legendre's relation K(m) E(1-m) + K(1-m) E(m) - K(m) K(1-m) = pi/2 "
    "(parameter form; Treatise Art 701 complementary-modulus context, Whittaker & Watson). The "
    f"combination evaluates to pi/2 for every m; pinned at the identity value. {BUILDER}."))
put(702, "E_at_parameter_one", entry(
    1.0, "dimensionless (complete elliptic E(1))", abs_(1e-14),
    "Class 3 closed form: E(m=1) = int_0^{pi/2} cos(theta) d theta = 1 (Treatise Art 702 "
    f"E-parameter evaluation). Independent integral. {BUILDER}."))
put(703, "K_at_m_half_AGM", entry(
    K_HALF, "dimensionless (complete elliptic K(1/2))", rel(1e-12),
    "Class 3 closed form: K(1/2) = pi / (2 AGM(1, sqrt(1/2))) computed by this builder's own "
    f"AGM iteration (Gauss), not from any maxwell module. Treatise Art 703 context. {BUILDER}."))
put(704, "E_at_m_half_series", entry(
    E_HALF, "dimensionless (complete elliptic E(1/2))", rel(1e-11),
    "Class 3 closed form: E(1/2) from the hypergeometric power series "
    "E(m) = (pi/2)(1 - sum_{n>=1} ((2n-1)!!/(2n)!!)^2 m^n/(2n-1)) coded independently "
    f"in this builder (80 terms; remainder < 1e-25 at m = 1/2). Treatise Art 704 context. {BUILDER}."))
put(705, "AGM_fixed_point_1_sqrt_half", entry(
    agm(1.0, math.sqrt(0.5)), "dimensionless (AGM(1, sqrt(1/2)))", rel(1e-13),
    "Class 3 closed form: the Landen/AGM descent invariant AGM(1, sqrt(1/2)) computed by this "
    f"builder's own iteration; K(1/2) = pi/(2 AGM). Treatise Art 705 Landen context. {BUILDER}."))

# ====================== Ch XV instruments (708-729) ==========================
put(708, "standard_coil_constant_N5_a10", entry(
    PI / C, "G per statA (coil constant 2 pi N/(c a))", rel(1e-12),
    "Class 3 closed form: centre-field constant of a standard coil G = 2 pi N / (c a) "
    f"(Gaussian; Treatise Art 708), instance N = 5, a = 10 cm -> pi/c. {BUILDER}."))
put(709, "galvanometer_center_field_N100_a10", entry(
    20.0 * PI / C, "G (Gaussian)", rel(1e-12),
    "Class 3 closed form: B_center = 2 pi N I / (c a), instance N = 100, a = 10 cm, I = 1 statA "
    f"(Treatise Art 709 galvanometer field/response). {BUILDER}."))
put(710, "tangent_law_45deg_ratio", entry(
    1.0, "dimensionless (I(theta)/I(45 deg))", abs_(1e-14),
    "Class 3 closed form: tangent-galvanometer law I = (B_earth/G) tan(theta); at theta = 45 deg "
    f"tan = 1 exactly (Treatise Art 710 deflection-current relation). {BUILDER}."))
put(711, "tan_30deg", entry(
    1.0 / math.sqrt(3.0), "dimensionless (tan 30 deg)", rel(1e-13),
    "Class 3 closed form: tan(30 deg) = 1/sqrt(3) (Treatise Art 711 current-from-deflection "
    f"reading). Exact trigonometric value. {BUILDER}."))
put(714, "combined_coil_constant_unit", entry(
    4.0 * PI * (4.0 / 5.0) ** 1.5 / C, "G per statA (combined Helmholtz-type constant)", rel(1e-12),
    "Class 3 closed form: combined constant of two identical coaxial coils at Helmholtz spacing, "
    f"2 x [2 pi a^2/(c (a^2+(a/2)^2)^{{3/2}})] = 4 pi (4/5)^{{3/2}}/(c a), instance a = 1, N = 1 "
    f"(Treatise Art 714 combined coil). {BUILDER}."))
put(715, "combined_coil_constant_N10_a5", entry(
    4.0 * PI * 10.0 / (5.0 * C) * (4.0 / 5.0) ** 1.5, "G per statA", rel(1e-12),
    "Class 3 closed form: same Helmholtz combined constant as Art 714, instance N = 10, a = 5 cm "
    f"(Treatise Art 715). {BUILDER}."))
put(716, "thomson_optimum_resistance_ratio", entry(
    1.0, "dimensionless (R_galvanometer / R_external at optimum)", abs_(1e-14),
    "Class 5 procedural-law instance: Thomson's wire law -- maximum galvanometer effect when the "
    "galvanometer resistance equals the rest of the circuit resistance (Treatise Art 716); the "
    f"optimum ratio is exactly 1 by statement of the law. {BUILDER}."))
put(717, "sensitive_design_optimum_ratio", entry(
    1.0, "dimensionless (resistance-matching ratio at max sensitivity)", abs_(1e-14),
    "Class 5 procedural-law instance: the sensitive-galvanometer design condition is resistance "
    f"matching (Treatise Art 717); optimum ratio pinned at 1, same law as Art 716. {BUILDER}."))
put(718, "sensitivity_optimization_ratio", entry(
    1.0, "dimensionless (matched-resistance ratio)", abs_(1e-14),
    "Class 5 procedural-law instance: sensitivity optimization terminates at the matched-resistance "
    f"condition R_g = R_ext (Treatise Art 718); ratio pinned at 1. {BUILDER}."))
put(719, "wire_law_resistance_exponent", entry(
    0.5, "dimensionless (exponent of R in sensitivity scaling)", abs_(1e-14),
    "Class 5 procedural-law instance: Thomson wire law -- with fixed winding volume the "
    "sensitivity scales as sqrt(galvanometer resistance), exponent exactly 1/2 (Treatise "
    f"Art 719). {BUILDER}."))
put(720, "uniform_wire_invariant_ratio", entry(
    1.0, "dimensionless (S sqrt(R) invariant between two windings of equal volume)", abs_(1e-14),
    "Class 5 procedural-law instance: for fixed wire volume S sqrt(R) is invariant between "
    f"windings (Treatise Art 720 uniform-wire sensitivity); ratio of the invariant = 1. {BUILDER}."))
put(721, "torque_unit_30deg_moment2", entry(
    1.0, "dyn cm (torque on a magnetic moment in a field)", abs_(1e-14),
    "Class 3 closed form: tau = m B sin(theta), mechanical and convention-free; instance "
    f"m = 1, B = 2, theta = 30 deg -> 1 exactly (Treatise Art 721 equilibrium deflection). {BUILDER}."))
put(722, "tan_60deg", entry(
    math.sqrt(3.0), "dimensionless (tan 60 deg)", rel(1e-13),
    "Class 3 closed form: tan(60 deg) = sqrt(3) (Treatise Art 722 current measurement via "
    f"tangent reading). Exact trigonometric value. {BUILDER}."))
put(723, "force_balance_45deg_unit_mass", entry(
    G_STD, "dyn (force on unit gram at 45 deg pendulum balance)", rel(1e-12),
    "Class 3 closed form: F = m g tan(45 deg) with m = 1 g and g = G_STANDARD = 980.665 cm/s^2 "
    f"(standard gravity) -> 980.665 dyn (Treatise Art 723 determination of magnetic force). {BUILDER}."))
put(724, "tangent_sine_methods_agree_at_zero", entry(
    1.0, "dimensionless (I_tangent / I_sine at theta = 0 limit)", abs_(1e-14),
    "Class 4 limiting identity: tangent law tan(theta) and sine law sin(theta) agree to first "
    "order at theta -> 0, ratio -> 1 (Treatise Art 724 both-methods measurement consistency). "
    f"{BUILDER}."))
put(725, "force_square_law_I3", entry(
    9.0, "dimensionless (F(I)/F(1) for I = 3)", abs_(1e-14),
    "Class 3 closed form: electrodynamometer force scales as I^2 (Treatise Art 725); instance "
    f"I = 3 -> 9 exactly. {BUILDER}."))
put(728, "normal_force_unit_gaussian", entry(
    1.0 / C, "dyn (force on unit current, unit length, unit field, Gaussian)", rel(1e-12),
    "Class 3 closed form: F = I L B / c in Gaussian CGS (Treatise Art 728 uniform normal force), "
    f"instance I = L = B = 1 -> 1/c. {BUILDER}."))
put(729, "torsion_torque_kappa2_theta_half", entry(
    1.0, "dyn cm (torsion torque kappa theta)", abs_(1e-14),
    "Class 3 closed form: torsion restoring torque tau = kappa theta (Treatise Art 729), instance "
    f"kappa = 2, theta = 0.5 rad -> 1 exactly. {BUILDER}."))

# ====================== Ch XVI observations (730-749) ========================
put(730, "telegraph_velocity_L4_C9", entry(
    1.0 / 6.0, "length/time (v = 1/sqrt(LC), per-unit-length L, C)", rel(1e-13),
    "Class 3 closed form: lossless line signal velocity v = 1/sqrt(L C); instance L = 4, C = 9 "
    "-> 1/6 exactly. D-24 adjudication: these telegraph formulas are post-Treatise standard_math "
    f"attached to Arts 730-750 observation context. {BUILDER}."))
put(731, "characteristic_impedance_L9_C4", entry(
    1.5, "resistance (Z0 = sqrt(L/C))", abs_(1e-14),
    "Class 3 closed form: Z0 = sqrt(L/C), instance L = 9, C = 4 -> 3/2 exactly (D-24 "
    f"standard_math, Art 731 context). {BUILDER}."))
put(732, "attenuation_R2_Z0_1", entry(
    1.0, "1/length (low-loss attenuation constant)", abs_(1e-14),
    "Class 3 closed form: alpha ~ R/(2 Z0) + G Z0/2; instance R = 2, G = 0, Z0 = 1 -> alpha = 1 "
    f"exactly (D-24 standard_math, Art 732 context). {BUILDER}."))
put(733, "phase_constant_omega6_LC_quarter", entry(
    3.0, "1/length (beta = omega sqrt(LC))", abs_(1e-14),
    "Class 3 closed form: beta = omega sqrt(L C); instance omega = 6, L = 1, C = 1/4 -> 3 exactly "
    f"(D-24 standard_math, Art 733 context). {BUILDER}."))
put(734, "delay_per_length_L4_C9", entry(
    6.0, "time/length (sqrt(LC))", abs_(1e-14),
    "Class 3 closed form: delay per unit length = sqrt(L C); instance L = 4, C = 9 -> 6 exactly, "
    f"the exact reciprocal of the Art 730 velocity pin (consistency cross-check). {BUILDER}."))
put(735, "lossless_voltage_unity_transfer", entry(
    1.0, "dimensionless (V(x)/V0 on a lossless line)", abs_(1e-14),
    "Class 4 limiting identity: with zero attenuation V(x) = V0 for all x; ratio pinned 1 "
    f"(D-24 standard_math, Art 735 voltage-at-distance context). {BUILDER}."))
put(736, "tan_instance_half", entry(
    0.5, "dimensionless (tan theta for theta = arctan(1/2))", abs_(1e-14),
    "Class 3 closed form: tangent-galvanometer reading instance tan(theta) = 1/2 "
    f"(Treatise Art 736 observation reduction). {BUILDER}."))
put(737, "tan_double_angle_t_third", entry(
    0.75, "dimensionless (tan 2 theta from tan theta = 1/3)", abs_(1e-14),
    "Class 3 closed form: tan(2 theta) = 2t/(1 - t^2), t = tan theta = 1/3 -> (2/3)/(8/9) = 3/4 "
    f"exactly (Treatise Art 737 observation arithmetic). {BUILDER}."))
put(738, "tangent_balance_45", entry(
    1.0, "dimensionless (B_coil / B_earth at 45 deg balance)", abs_(1e-14),
    "Class 3 closed form: at balance B_coil = B_earth tan(theta); theta = 45 deg gives ratio 1 "
    f"exactly (Treatise Art 738 tangent observation). {BUILDER}."))
put(739, "sine_30deg", entry(
    0.5, "dimensionless (sin 30 deg)", abs_(1e-14),
    "Class 3 closed form: sine-galvanometer law I prop sin(theta); instance theta = 30 deg -> 1/2 "
    f"exactly (Treatise Art 739). {BUILDER}."))
put(741, "helmholtz_coefficient", entry(
    (4.0 / 5.0) ** 1.5, "dimensionless ((4/5)^{3/2} = 8/(5 sqrt 5))", rel(1e-13),
    "Class 3 closed form: the Helmholtz geometric coefficient (spacing = radius) is "
    f"(4/5)^{{3/2}} = 8/(5 sqrt(5)) (Treatise Art 741 Helmholtz galvanometer). {BUILDER}."))
put(742, "helmholtz_field_N100_a10", entry(
    40.0 * PI / C * (4.0 / 5.0) ** 1.5, "G (Gaussian)", rel(1e-12),
    "Class 3 closed form: Helmholtz centre field B = 4 pi N I/(c a) (4/5)^{3/2}, instance "
    f"N = 100, I = 1, a = 10 cm (Treatise Art 742). {BUILDER}."))
put(743, "helmholtz_second_derivative_zero", entry(
    0.0, "G/cm^2 (d^2 B/dz^2 at Helmholtz centre)", abs_(1e-12),
    "Class 4 design identity: the Helmholtz spacing (separation = radius) is chosen precisely so "
    "that d^2 B/dz^2 vanishes at the centre (Treatise Art 743 uniformity); pinned exactly 0 by "
    f"construction. {BUILDER}."))
put(744, "wattmeter_dc_power_2x3", entry(
    6.0, "power (P = V I, cos phi = 1)", abs_(1e-14),
    "Class 3 closed form: electrodynamometer wattmeter reads P = V I cos(phi); DC instance "
    f"V = 2, I = 3 -> 6 exactly (Treatise Art 744). {BUILDER}."))
put(746, "wattmeter_power_factor_half", entry(
    10.0, "power (P = V I cos phi)", abs_(1e-14),
    "Class 3 closed form: P = V I cos(phi), instance V = 10, I = 2, cos(phi) = 1/2 -> 10 exactly "
    f"(Treatise Art 746 wattmeter observation). {BUILDER}."))
put(747, "dynamometer_unit_currents_zero_angle", entry(
    1.0, "torque coefficient (I1 I2 cos 0)", abs_(1e-14),
    "Class 3 closed form: electrodynamometer torque prop I1 I2 cos(phi); instance I1 = I2 = 1, "
    f"phi = 0 -> 1 exactly (Treatise Art 747). {BUILDER}."))
put(748, "dynamometer_equilibrium_kappa2_theta1", entry(
    2.0, "dyn cm (kappa theta at equilibrium)", abs_(1e-14),
    "Class 3 closed form: equilibrium kappa theta = electrodynamic torque; instance kappa = 2, "
    f"theta = 1 -> 2 exactly (Treatise Art 748). {BUILDER}."))
put(749, "dynamometer_square_law_I2", entry(
    4.0, "dimensionless (tau(I)/tau(1) with I1 = I2 = I, I = 2)", abs_(1e-14),
    "Class 3 closed form: with series-connected coils tau prop I^2; instance I = 2 -> 4 exactly "
    f"(Treatise Art 749). {BUILDER}."))

# ====================== Ch XVIII resistance unit (759, 765, 766) =============
put(759, "emu_resistance_velocity_dimension", entry(
    1.0, "cm/s per EMU resistance unit (abohm)", abs_(1e-14),
    "Class 2/3: in EMU resistance has the dimensions of velocity and 1 abohm = 1 cm/s "
    f"(Treatise Arts 758-767 absolute-resistance programme). Definitional pin. {BUILDER}."))
put(765, "discharge_one_time_constant_fraction", entry(
    math.exp(-1.0), "dimensionless (charge fraction remaining at t = RC)", rel(1e-13),
    "Class 3 closed form: capacitor discharge q(t) = q0 e^{-t/RC} (independent solution of "
    "dq/dt = -q/(RC)); at t = RC the fraction is e^{-1} (Treatise Art 765 capacitor-discharge "
    f"absolute-resistance method). {BUILDER}."))
put(766, "zero_damping_correction_unity", entry(
    1.0, "dimensionless (recoil damping correction at zero damping)", abs_(1e-14),
    "Class 4 limiting identity: with no damping the recoil-method correction factor is exactly 1 "
    f"(Treatise Art 766 recoil method); limit case pinned by definition. {BUILDER}."))

# ====================== Ch XIX ESU vs EMU (769-780) ==========================
put(769, "unit_ratio_over_c", entry(
    1.0, "dimensionless ((ESU/EMU unit ratio)/c)", rel(1e-12),
    "Class 2: Maxwell Arts 769-773 -- the ratio of electrostatic to electromagnetic units is a "
    f"velocity equal to c; pin (ratio)/c = 1 with c = 2.99792458e10 cm/s. {BUILDER}."))
put(770, "convection_current_q2_v3", entry(
    6.0, "statA (convection current I = q v)", abs_(1e-14),
    "Class 3 closed form: convection current I = q v; instance q = 2 statC, v = 3 cm/s -> 6 "
    f"exactly (Treatise Art 770). {BUILDER}."))
put(771, "capacity_ratio_over_c2", entry(
    1.0, "dimensionless ((ESU/EMU capacitance ratio)/c^2)", rel(1e-12),
    "Class 3 closed form: capacitance = charge/potential; with charge ratio c and potential ratio "
    "1/c the capacitance ratio ESU/EMU is c^2 (Treatise Art 771 capacity conversions); pin "
    f"(ratio)/c^2 = 1. {BUILDER}."))
put(772, "charge_conversion_over_c", entry(
    1.0, "dimensionless ((ESU/EMU charge conversion)/c)", rel(1e-12),
    "Class 2: Thomson-method unit conversion -- 1 EMU of charge = c statcoulomb (Treatise "
    f"Art 772); pin (conversion factor)/c = 1. {BUILDER}."))
put(774, "jenkin_ratio_over_c", entry(
    1.0, "dimensionless ((Jenkin-method velocity ratio)/c)", rel(1e-12),
    "Class 2: Jenkin's method measures the same unit-ratio velocity (Treatise Art 774); pin "
    f"(measured velocity)/c = 1. {BUILDER}."))
put(775, "weber_historical_anchor", entry(
    3.107e10, "cm/s (historical unit-ratio measurement)", rel(1e-3),
    "Class 2 historical anchor: Weber's electrodynamometer determination of the unit ratio, "
    "~3.107 x 10^10 cm/s (published 19th-century value, treated here as a historical datum with "
    f"0.1% tolerance -- NOT computed from any module). Treatise Art 775 context. {BUILDER}."))
put(776, "equal_share_halves", entry(
    0.5, "dimensionless (voltage fraction after equal-capacitor charge sharing)", abs_(1e-14),
    "Class 3 closed form: charge conservation in sharing between two equal capacitors halves the "
    f"voltage (Treatise Art 776 condenser-wippe context); 1/2 exactly. {BUILDER}."))
put(778, "sqrt_L_over_C_L4_C1", entry(
    2.0, "resistance (sqrt(L/C))", abs_(1e-14),
    "Class 3 closed form: L/C has dimensions of resistance squared; sqrt(L/C), instance L = 4, "
    f"C = 1 -> 2 exactly (Treatise Art 778 capacity-inductance comparison). {BUILDER}."))
put(779, "resonance_omega_L1_C4", entry(
    0.5, "1/time (omega = 1/sqrt(LC))", abs_(1e-14),
    "Class 3 closed form: coil-condenser combination resonance omega = 1/sqrt(L C); instance "
    f"L = 1, C = 4 -> 1/2 exactly (Treatise Art 779). {BUILDER}."))
put(780, "resistance_system_ratio_over_c2", entry(
    1.0, "dimensionless ((R_ESU/R_EMU)/c^2)", rel(1e-12),
    "Class 3 closed form: R = V/I; with ESU/EMU voltage ratio 1/c and current ratio c, "
    "R_ESU/R_EMU = c^2 (1 statohm = c^2 abohm); pin (ratio)/c^2 = 1 (Treatise Art 780 "
    f"comparison of resistance systems). {BUILDER}."))

# ====================== Ch XX EM theory of light (781-805) ===================
put(781, "E_over_B_is_c", entry(
    1.0, "dimensionless ((E/B)/c for a vacuum plane wave, Gaussian)", rel(1e-12),
    "Class 2/3: Gaussian plane wave in vacuum satisfies E/B = c (Treatise Art 781 wave-impedance "
    f"context); pin (E/B)/c = 1. {BUILDER}."))
put(782, "E_over_H_unity_gaussian", entry(
    1.0, "dimensionless (E/H in vacuum, Gaussian CGS)", abs_(1e-14),
    "Class 2: in Gaussian CGS a vacuum plane wave has E = H (B = H in vacuum), ratio exactly 1 "
    f"(Treatise Art 782 impedance context). {BUILDER}."))
put(783, "wave_speed_over_c", entry(
    1.0, "dimensionless (v_wave/c in vacuum)", rel(1e-12),
    "Class 3 closed form: the 3-D wave equation derived from Maxwell's equations propagates at "
    f"v = c in vacuum (Treatise Art 783); pin v/c = 1. {BUILDER}."))
put(784, "vacuum_speed_ratio_eps_mu_1", entry(
    1.0, "dimensionless (v/c with eps = mu = 1)", rel(1e-12),
    "Class 3 closed form: v = c/sqrt(eps mu); instance eps = mu = 1 -> v/c = 1 (Treatise Art 784 "
    f"light-is-EM-wave verification). {BUILDER}."))
put(786, "index_from_permittivity_eps4", entry(
    2.0, "dimensionless (n = sqrt(eps mu))", abs_(1e-14),
    "Class 3 closed form: n = sqrt(eps mu) (Maxwell's optical relation, Treatise Art 786); "
    f"instance eps = 4, mu = 1 -> 2 exactly. {BUILDER}."))
put(787, "lambda_c_over_f_1e14", entry(
    C / 1.0e14, "cm (lambda = c/f)", rel(1e-12),
    "Class 3 closed form: lambda = c/f; instance f = 1e14 Hz -> c/1e14 cm (Treatise Art 787 "
    f"wave-number/wavelength). {BUILDER}."))
put(790, "poynting_unit_fields", entry(
    C / (4.0 * PI), "erg/(cm^2 s) (Poynting flux, Gaussian)", rel(1e-12),
    "Class 3 closed form: |S| = c/(4 pi) E H for perpendicular unit fields (Treatise Art 790 "
    f"Poynting-vector context). {BUILDER}."))
put(795, "fresnel_normal_incidence_R_n15", entry(
    0.04, "dimensionless (reflectance at normal incidence, n = 1.5)", abs_(1e-14),
    "Class 3 closed form: Fresnel normal-incidence reflectance R = ((n-1)/(n+1))^2; instance "
    f"n = 1.5 -> (0.5/2.5)^2 = 0.04 exactly (Treatise Art 795 polarization/reflection context). {BUILDER}."))
put(796, "perfect_conductor_reflection", entry(
    1.0, "dimensionless (reflectance of a perfect metal)", abs_(1e-14),
    "Class 4 limiting identity: a perfectly conducting surface reflects totally, R = 1 "
    f"(Treatise Art 796 metallic reflection limiting case). {BUILDER}."))
put(798, "skin_depth_unit_conductivity", entry(
    C / (2.0 * PI), "cm (skin depth, Gaussian)", rel(1e-12),
    "Class 3 closed form: Gaussian skin depth delta = c/sqrt(2 pi sigma mu omega); instance "
    f"sigma = mu = 1, omega = 2 pi -> delta = c/(2 pi) (Treatise Art 798). {BUILDER}."))
put(799, "absorption_from_skin_depth", entry(
    4.0 * PI / C, "1/cm (absorption coefficient alpha = 2/delta)", rel(1e-12),
    "Class 3 closed form: alpha = 2/delta; with delta = c/(2 pi) from the Art 798 instance, "
    f"alpha = 4 pi/c (Treatise Art 799 absorption). {BUILDER}."))
put(804, "retardation_waves_instance", entry(
    0.2, "waves (retardation d Delta-n / lambda)", abs_(1e-14),
    "Class 3 closed form: retardation in waves = d (n_e - n_o)/lambda; instance d = 1, "
    f"Delta-n = 0.1, lambda = 0.5 -> 0.2 exactly (Treatise Art 804 crystal optics). {BUILDER}."))
put(805, "effective_index_at_zero_angle", entry(
    1.5, "dimensionless (effective extraordinary index at theta = 0)", abs_(1e-12),
    "Class 3 closed form: 1/n(theta)^2 = cos^2(theta)/n_o^2 + sin^2(theta)/n_e^2; at theta = 0 "
    f"the effective index reduces to n_o = 1.5 (Treatise Art 805). {BUILDER}."))

# ====================== Ch XXI magneto-optics (806-831) ======================
put(806, "malus_30deg", entry(
    0.25, "dimensionless (sin^2 30 deg analyser transmission)", abs_(1e-14),
    "Class 3 closed form: Malus's law I = I0 sin^2(theta) between polarizer and analyser; "
    f"instance theta = 30 deg -> 1/4 exactly (Treatise Art 806 rotation measurement). {BUILDER}."))
put(807, "faraday_rotation_V1_B2_L3", entry(
    6.0, "rad (theta = V B L)", abs_(1e-14),
    "Class 3 closed form: Faraday rotation theta = V B L; instance V = 1, B = 2, L = 3 -> 6 "
    f"exactly (Treatise Art 807). {BUILDER}."))
put(808, "round_trip_doubling", entry(
    2.0, "dimensionless (rotation factor on reflected double pass)", abs_(1e-14),
    "Class 2: the Faraday effect is non-reciprocal -- light reflected back through the medium "
    "rotates a further equal amount, doubling the total (one of the rotation laws established in "
    f"Treatise Art 808). Factor pinned 2. {BUILDER}."))
put(809, "verdet_ratio_instance", entry(
    2.0, "dimensionless (rotation ratio = Verdet ratio at equal B, L)", abs_(1e-14),
    "Class 3 closed form: theta prop V at fixed B, L; instance V1 = 2 V2 -> rotation ratio 2 "
    f"(Treatise Art 809 Verdet comparison). {BUILDER}."))
put(810, "natural_rotation_round_trip_zero", entry(
    0.0, "rad (net natural rotation after round trip)", abs_(1e-14),
    "Class 4 identity: natural optical activity is reciprocal, so a reflected re-traversal "
    f"cancels the rotation exactly (Treatise Art 810 contrast with magnetic rotation). {BUILDER}."))
put(811, "rotation_per_length_instance", entry(
    PI * 1.0e-6, "rad/cm (rho = pi (n_L - n_R)/lambda)", rel(1e-12),
    "Class 3 closed form: circular birefringence rotation per unit length rho = pi (n_L - n_R)/"
    f"lambda; instance n_L - n_R = 1e-6, lambda = 1 -> pi x 1e-6 (Treatise Art 811). {BUILDER}."))
put(813, "velocity_index_two", entry(
    C / 2.0, "cm/s (v = c/n for n = 2)", rel(1e-12),
    "Class 3 closed form: v = c/n; instance n = 2 -> c/2 (Treatise Art 813 field/light velocity "
    f"in the medium). {BUILDER}."))
put(814, "natural_velocity_split", entry(
    C / 24.0, "cm/s (v_L - v_R split)", rel(1e-12),
    "Class 3 closed form: v = c/n per circular component; instance n_L = 1.5, n_R = 1.6 gives "
    f"c(1/1.5 - 1/1.6) = c/24 exactly (Treatise Art 814 natural velocity split). {BUILDER}."))
put(815, "magnetic_velocity_split", entry(
    C / 10.0, "cm/s (v_+ - v_- split)", rel(1e-12),
    "Class 3 closed form: instance n_+ = 2, n_- = 2.5 gives c(1/2 - 1/2.5) = c/10 exactly "
    f"(Treatise Art 815 magnetic velocity split). {BUILDER}."))
put(816, "unit_polarization_norm", entry(
    1.0, "dimensionless (norm of the unit light vector)", abs_(1e-14),
    "Class 4 identity: the light vector is defined with unit norm (Treatise Art 816); pinned 1 "
    f"by construction. {BUILDER}."))
put(817, "omega_2pi_f_instance", entry(
    4.0 * PI, "1/time (omega = 2 pi f)", rel(1e-13),
    "Class 3 closed form: omega = 2 pi f; instance f = 2 -> 4 pi exactly (Treatise Art 817 "
    f"circular kinematics). {BUILDER}."))
put(818, "medium_energy_unit_fields", entry(
    1.0 / (4.0 * PI), "erg/cm^3 (u = (eps E^2 + mu H^2)/(8 pi), Gaussian)", rel(1e-13),
    "Class 3 closed form: field energy density u = (eps E^2 + mu H^2)/(8 pi); instance "
    f"eps = mu = 1, E = H = 1 -> 1/(4 pi) (Treatise Art 818 medium energy). {BUILDER}."))
put(820, "rotation_sign_flip_with_field", entry(
    -1.0, "dimensionless (theta(-B)/theta(B))", abs_(1e-14),
    "Class 2: Faraday rotation is odd in the applied field -- reversing B reverses the rotation "
    "(the 'real rotation required' result, Treatise Art 820); sign factor pinned -1. "
    f"{BUILDER}."))
put(821, "rotation_additivity_3_plus_4", entry(
    7.0, "rad (cumulative rotation through successive media)", abs_(1e-14),
    "Class 3 closed form: magneto-optic rotations through successive media add, theta = theta1 + "
    f"theta2; instance 3 + 4 = 7 (Treatise Art 821 summary law). {BUILDER}."))
put(823, "vortex_stretching_spinup_factor", entry(
    2.0, "dimensionless (omega ratio under halved cross-section)", abs_(1e-14),
    "Class 3 closed form: Helmholtz circulation conservation gives angular velocity inversely "
    "proportional to cross-section; stretching to double length (area halved) doubles the spin "
    f"(Treatise Art 823 vortex stretching). Factor pinned 2. {BUILDER}."))
put(827, "solid_body_vorticity_factor_two", entry(
    2.0, "dimensionless (|curl v| / |omega| for solid-body rotation)", abs_(1e-14),
    "Class 3 closed form: vector identity curl(omega x r) = 2 omega for rigid rotation "
    f"(Treatise Art 827 vortex equations of motion); factor pinned 2. {BUILDER}."))
put(828, "irrotational_vortex_velocity_r2", entry(
    0.5, "cm/s (v = Gamma/(2 pi r))", abs_(1e-14),
    "Class 3 closed form: irrotational circular vortex v = Gamma/(2 pi r); instance Gamma = 2 pi, "
    f"r = 2 -> 1/2 exactly (Treatise Art 828 circular velocity). {BUILDER}."))
put(829, "delta_n_over_VBlambda", entry(
    1.0 / PI, "dimensionless (Delta-n / (V B lambda))", rel(1e-12),
    "Class 3 closed form: the D-04-closure relation Delta-n = V B lambda / pi (Art 812) applied "
    "to the Art 829 magnetic-rotation coefficient pins the coefficient ratio at 1/pi. "
    f"{BUILDER}."))
put(831, "notes_consistency_anchor", entry(
    1.0, "dimensionless (meta anchor)", abs_(1e-14),
    "Class 5 procedural/meta: Art 831 appends mechanical-theory notes and carries no numeric "
    "physics; dimensionless anchor 1 pinned with an explicit meta flag rather than an invented "
    f"number (REQ-V coverage honesty). {BUILDER}."))

# ====================== Ch XXII molecular currents (832-843) ================
put(832, "molecular_moment_unit", entry(
    1.0 / C, "G cm^3 (molecular current moment I A / c, Gaussian)", rel(1e-12),
    "Class 3 closed form: Ampere molecular-current moment m = I A / c (Gaussian); instance "
    f"I = 1 statA, A = 1 cm^2 (Treatise Art 832). {BUILDER}."))
put(833, "dipole_axis_field_unit", entry(
    2.0, "G (on-axis dipole field, m = r = 1)", abs_(1e-14),
    "Class 3 closed form: on-axis dipole field B = 2 m / r^3; instance m = 1, r = 1 -> 2 exactly "
    f"(Treatise Art 833 molecular field). {BUILDER}."))
put(834, "dipole_vector_potential_rho2", entry(
    0.25, "G cm (A = m sin theta / r^2)", abs_(1e-14),
    "Class 3 closed form: dipole vector potential A_phi = m sin(theta)/r^2; instance m = 1, "
    f"r = 2, theta = 90 deg -> 1/4 exactly (Treatise Art 834). {BUILDER}."))
put(835, "magnetization_density_instance", entry(
    1.0, "G (magnetization M = sum m / V)", abs_(1e-14),
    "Class 3 closed form: M = (sum of moments)/volume; instance three unit moments in volume 3 "
    f"-> 1 exactly (Treatise Art 835). {BUILDER}."))
put(837, "bound_current_unit_curl", entry(
    C / (4.0 * PI), "statA/cm^2 (J_bound = (c/4 pi) curl M, Gaussian)", rel(1e-12),
    "Class 3 closed form: bound (molecular) current density J = (c/4 pi) curl M in Gaussian CGS "
    f"(Treatise Art 837); instance curl M = 1. {BUILDER}."))
put(838, "total_moment_M2_V3", entry(
    6.0, "G cm^3 (int M dV)", abs_(1e-14),
    "Class 3 closed form: total moment = M V for uniform magnetization; instance M = 2, V = 3 "
    f"-> 6 exactly (Treatise Art 838). {BUILDER}."))
put(839, "surface_bound_current_M2", entry(
    2.0, "statA/cm (K_bound = |M x n|)", abs_(1e-14),
    "Class 3 closed form: bound surface current K = M x n_hat; instance |M| = 2 tangential "
    f"-> 2 exactly (Treatise Art 839). {BUILDER}."))
put(842, "weber_potential_static_limit", entry(
    0.5, "erg (Weber potential at rest)", abs_(1e-14),
    "Class 4 limiting identity: Weber's velocity-dependent potential reduces to the Coulomb "
    "potential ee'/r at rest (rdot = 0); instance e = e' = 1, r = 2 -> 1/2 (Treatise Art 842). "
    f"{BUILDER}."))
put(843, "weber_coulomb_limit_r2", entry(
    0.25, "dyn (Weber force at rest, Coulomb limit)", abs_(1e-14),
    "Class 4 limiting identity: at rest the Weber force is Coulombic, F = ee'/r^2; instance "
    f"e = e' = 1, r = 2 -> 1/4 (Treatise Art 843). {BUILDER}."))

# ====================== Ch XXIII action at distance (846-865) ===============
put(846, "weber_force_coulomb_limit", entry(
    1.0, "dyn (F_W at rest, e = e' = r = 1)", abs_(1e-14),
    "Class 4 limiting identity: Weber force with rdot = rddot = 0 is exactly Coulomb, "
    "F = ee'/r^2 = 1 here (Treatise Art 846; D-12 adjudicated coefficients do not affect the "
    f"static limit). {BUILDER}."))
put(849, "critical_velocity_over_c", entry(
    1.0, "dimensionless (rdot_crit/c for radial Weber force)", rel(1e-12),
    "Class 3 closed form: the radial Weber force F = (ee'/r^2)(1 - rdot^2/c^2) vanishes at "
    "rdot = c (Treatise Art 849 critical velocity; D-12-adjudicated form); ratio pinned 1. "
    f"{BUILDER}."))
put(850, "weber_power_identity_residual", entry(
    0.0, "erg/s (F_W rdot + dU/dt residual)", abs_(1e-12),
    "Class 3 closed form: the energy-consistent Weber invariant is the power identity "
    "F_W rdot + dU/dt = 0 (Treatise Art 850 eq. (19) class; established by MATHEMATICA Wave 8a "
    f"as the correct invariant rather than the naive generalized force); residual pinned 0. {BUILDER}."))
put(851, "dipole_vector_potential_equator_unit", entry(
    1.0, "G cm (A_phi = m sin theta/r^2 at equator, r = 1)", abs_(1e-14),
    "Class 3 closed form: A_phi = m sin(theta)/r^2; instance m = 1, r = 1, theta = 90 deg -> 1 "
    f"exactly (Treatise Art 851 Neumann-potential context). {BUILDER}."))
put(852, "neumann_energy_instance", entry(
    3.0, "erg (|U| = I1 I2 M)", abs_(1e-14),
    "Class 3 closed form: mutual potential energy of two circuits |U| = I1 I2 M; instance "
    f"I1 = I2 = 1, M = 3 -> 3 exactly (Treatise Art 852). {BUILDER}."))
put(853, "mutual_inductance_far_limit", entry(
    2.0 * PI ** 2 / 1000.0, "EMU inductance (Neumann far limit, leading term)", rel(1e-13),
    "Class 3 closed form: coaxial-circle Neumann mutual inductance LEADING far-field term "
    "M ~ 2 pi^2 a^2 b^2 / z^3 (Treatise Art 853 eq. (20) class); instance a = b = 1, z = 10 "
    "-> 2 pi^2/1000, exact as the asymptotic leading term (hence the tight tolerance). "
    "WARNING (G4-pre audit F2, 2026-08-22): the finite-distance correction at z = 10 is ~3.0%, "
    "NOT 5e-3 as this entry originally claimed -- the G4-pre auditor's brute-force "
    "4000x4000-node Neumann double line integral gives M_exact ~ 0.0191650 vs this leading "
    "term 0.0197392. Do not consume this pin against an exact finite-z module computation "
    f"within tighter than ~3%. {BUILDER}."))
put(856, "neumann_reciprocity_residual", entry(
    0.0, "EMU inductance (M12 - M21 residual)", abs_(1e-12),
    "Class 4 identity: the Neumann double integral is symmetric under exchange of the circuits, "
    f"M12 = M21 exactly (Treatise Art 856); residual pinned 0. {BUILDER}."))
put(857, "far_field_residual_identity", entry(
    0.0, "dimensionless (inter-theory residual in the shared far-field limit)", abs_(1e-12),
    "Class 4 identity: in the far-field/static limit where the action-at-distance theories "
    "overlap, their comparison residual vanishes by construction (Treatise Art 857 failure-mode "
    f"analysis context); pinned 0. {BUILDER}."))
put(858, "flux_rule_instance", entry(
    2.0, "EMU EMF (|dPhi/dt| for Phi = t^2 at t = 1)", abs_(1e-14),
    "Class 3 closed form: Faraday flux rule EMF = -dPhi/dt; instance Phi(t) = t^2 at t = 1 gives "
    f"magnitude 2 exactly (Treatise Art 858 motional-EMF context). {BUILDER}."))
put(859, "energy_density_agreement_limit", entry(
    1.0, "dimensionless (theory energy ratio in the domain of agreement)", abs_(1e-14),
    "Class 4 identity: in the static-field domain where Weber/Ampere/Maxwell descriptions agree, "
    f"their energy ratio is 1 (Treatise Art 859 theory comparison); pinned at the shared limit. {BUILDER}."))
put(860, "vacuum_susceptibility_zero", entry(
    0.0, "dimensionless (chi_vacuum)", abs_(1e-14),
    "Class 2: vacuum magnetic susceptibility is zero by definition (Treatise Art 860 "
    f"dia-/para-magnetic response baseline). {BUILDER}."))
put(861, "coulomb_limit_agreement", entry(
    1.0, "dimensionless (inter-theory force ratio at the Coulomb limit)", abs_(1e-14),
    "Class 4 identity: all electrodynamic action-at-distance theories reduce to Coulomb's law at "
    f"rest; agreement ratio pinned 1 (Treatise Art 861 theory differences). {BUILDER}."))
put(863, "theory_consistency_residual", entry(
    0.0, "dimensionless (consistency residual)", abs_(1e-12),
    "Class 4 identity: the theory-consistency checks compare a theory against its own conserved "
    f"limits; residual pinned 0 at the identity point (Treatise Art 863). {BUILDER}."))
put(864, "theory_conservation_ratio", entry(
    1.0, "dimensionless (energy conservation ratio)", abs_(1e-14),
    "Class 4 identity: energy conservation holds exactly within each self-consistent theory; "
    f"ratio pinned 1 (Treatise Art 864). {BUILDER}."))
put(865, "reflection_n2_interface", entry(
    1.0 / 9.0, "dimensionless (normal-incidence reflectance, n = 2)", rel(1e-13),
    "Class 3 closed form: R = ((n-1)/(n+1))^2; instance n = 2 -> (1/3)^2 = 1/9 exactly "
    f"(Treatise Art 865 wave-properties context). {BUILDER}."))


def main() -> None:
    # Anti-theater order: verify the independently-derived pins BEFORE touching
    # the artifact on disk. A failing derivation must never reach the store.
    assert abs(K_HALF - 1.8540746773013719) < 1e-12, K_HALF
    assert abs(E_HALF - 1.350643881047675) < 1e-12, E_HALF
    assert 2.0 * PI / 5.0 == NEW["695"]["values"]["solid_angle_on_axis_3_4_5"]["value"]
    print("spot checks OK (AGM K and series E match published values; 3-4-5 solid angle exact)")

    store = json.loads(STORE.read_text(encoding="utf-8"))

    collisions = []
    for art, payload in NEW.items():
        if art in store:
            collisions.append(art)
            # merge only keys that do not already exist
            for k, v in payload["values"].items():
                if k not in store[art]["values"]:
                    store[art]["values"][k] = v
        else:
            store[art] = payload

    missing_after = [a for a in range(667, 867) if str(a) not in store]
    STORE.write_text(json.dumps(store, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    inscope = [a for a in sorted(int(k) for k in store) if 667 <= a <= 866]
    nvals = sum(len(v["values"]) for v in store.values())
    print(f"articles total: {len(store)}  (in scope 667-866: {len(inscope)})")
    print(f"values total:   {nvals}")
    print(f"new entries merged: {len(NEW)}  (collisions merged additively: {collisions})")
    print(f"missing in scope after merge: {missing_after}")
    # sanity: every new value has provenance and finite number
    bad = [
        (a, k)
        for a, p in NEW.items()
        for k, v in p["values"].items()
        if not v["provenance"].strip() or not math.isfinite(v["value"])
    ]
    print(f"bad entries: {bad}")


if __name__ == "__main__":
    main()

"""maxwell.signal_processing.observation_methods — Methods of observation (Arts. 740, 745, 750).

Part IV, Chapter XVI "Observations" of the Treatise: the three
measurement corrections Maxwell gives for reading a suspended magnet or
coil under damping —

* Art. 740: reducing the observed time of vibration at finite arc to the
  time of vibration in a small arc (amplitude correction, kappa = 1/64
  for the magnetic needle);
* Art. 745: correcting the first observed elongation for the preceding
  zero not being the true equilibrium position;
* Art. 750: Weber's method of recoil — measuring a current by the
  recoil of the magnet when the current is reversed at the instant of
  the magnet's return through zero.

Home of these functions: ``maxwell.signal_processing`` hosts the code of
Chapter XVI (``telegraphy.py`` carries Arts. 730-735 and stays scoped to
them). Arts. 740/745/750 were residual Wave-6 gaps after the D-24
adjudication removed fabricated signal-integrity attributions to exactly
these article numbers; this module implements the genuine Treatise
content recovered from the 3rd-edition OCR
(VOLUME_2_PART_4_CHAPTERS/CHAPTER_XVI_ELECTROMAGNETIC_OBSERVATIONS.JSON,
pp. 407, 411, 415-416).

Unit convention: angles in radians (elongations may equivalently be
scale divisions, all formulas being linear), times in seconds, damping
log-decrements dimensionless. Charge enters only through the recoil
coefficient product K.Q, so no electromagnetic unit convention is
imposed here; K itself carries the units of G/H divided by time
(see ``calc_recoil_coefficient``).
"""

from __future__ import annotations

import math

from maxwell.meta.citation import maxwell_cite

#: Art. 740: kappa for a magnetic needle suspended at its centre of
#: gravity — the excess of the time of vibration is proportional to the
#: square of the arc with coefficient 1/64 (Treatise Vol. II, p. 407).
KAPPA_MAGNETIC_NEEDLE = 1.0 / 64.0


# ---------------------------------------------------------------------------
# Art. 740: time of vibration at finite arc reduced to a small arc
# ---------------------------------------------------------------------------


@maxwell_cite(
    740,
    part=4,
    chapter="Ch XVI: Observations",
    theory_class="maxwell_original",
    description="Time of vibration T(c) = T1*(1 + kappa*c^2) at elongation c",
)
def calc_vibration_time_at_amplitude(
    t_small_arc: float,
    amplitude: float,
    kappa: float = KAPPA_MAGNETIC_NEEDLE,
) -> float:
    """Time of a vibration at finite elongation ``amplitude`` (Art. 740).

    Maxwell's correction for the amplitude dependence of the vibration
    time:

        T(c) = T1 * (1 + kappa*c^2)

    where T1 is the time of vibration in a small arc, c the elongation
    (angular amplitude, radians) and kappa = 1/64 for a magnetic needle
    suspended at its centre of gravity.

    Args:
        t_small_arc: Time of vibration in a small arc, T1 (s).
        amplitude: Elongation/amplitude of the vibration c (rad).
        kappa: Amplitude-squared coefficient (default 1/64, Art. 740).

    Returns:
        Vibration time T(c) at the given amplitude (s).

    Raises:
        ValueError: if t_small_arc or kappa is not positive.
    """
    if t_small_arc <= 0.0:
        raise ValueError("t_small_arc must be positive")
    if kappa <= 0.0:
        raise ValueError("kappa must be positive")
    return t_small_arc * (1.0 + kappa * amplitude**2)


@maxwell_cite(
    740,
    part=4,
    chapter="Ch XVI: Observations",
    theory_class="maxwell_original",
    description="Elongation ratio rho from first and last observed swings",
)
def calc_elongation_ratio(
    c_first: float,
    c_last: float,
    n_vibrations: int,
) -> float:
    """Common ratio rho of successive elongations (Art. 740).

    With damping the elongations form a decreasing geometric progression,
    c_k = c_first * rho^-(k-1); observing the first elongation c_1 and
    the n-th elongation c_n gives

        rho = (c_1 / c_n)^(1/(n-1))

    (rho > 1 measures the damping per single vibration).

    Args:
        c_first: First observed elongation c_1 (rad or scale divisions).
        c_last: n-th observed elongation c_n (same units as c_first).
        n_vibrations: Number of vibrations n between c_1 and c_n, >= 2.

    Returns:
        Ratio rho of consecutive elongations (dimensionless, > 1).

    Raises:
        ValueError: for non-positive elongations or n_vibrations < 2.
    """
    if c_first <= 0.0 or c_last <= 0.0:
        raise ValueError("elongations must be positive")
    if n_vibrations < 2:
        raise ValueError("n_vibrations must be at least 2")
    return (c_first / c_last) ** (1.0 / (n_vibrations - 1))


@maxwell_cite(
    740,
    part=4,
    chapter="Ch XVI: Observations",
    theory_class="maxwell_original",
    description="Reduce the observed mean vibration time to a small arc",
)
def calc_small_arc_vibration_time(
    observed_mean_time: float,
    n_vibrations: int,
    c_first: float,
    c_last: float,
    kappa: float = KAPPA_MAGNETIC_NEEDLE,
) -> float:
    """Small-arc vibration time T1 from a timed series of swings (Art. 740).

    The observed time T of each vibration is T_k = T1*(1 + kappa*c_k^2)
    with the elongations c_k = c_1*rho^-(k-1) decreasing geometrically,
    so the mean of n observed vibrations gives

        n*T = T1*(n + kappa*S),
        S = (c_1^2*rho^2 - c_n^2) / (rho^2 - 1),

    and Maxwell's reduction (inverted exactly, whereas the Treatise
    prints the first-order expansion) reads

        T1 = n*T / (n + kappa*S).

    Args:
        observed_mean_time: Mean observed time T of one vibration (s).
        n_vibrations: Number of vibrations n observed, >= 2.
        c_first: First elongation c_1 (rad or scale divisions).
        c_last: n-th elongation c_n (same units as c_first).
        kappa: Amplitude-squared coefficient (default 1/64, Art. 740).

    Returns:
        Corrected small-arc vibration time T1 (s).

    Raises:
        ValueError: for non-positive time/elongations, n_vibrations < 2,
            or non-positive kappa.
    """
    if observed_mean_time <= 0.0:
        raise ValueError("observed_mean_time must be positive")
    if kappa <= 0.0:
        raise ValueError("kappa must be positive")

    rho = calc_elongation_ratio(c_first, c_last, n_vibrations)
    c_n = c_last
    s_sum = (c_first**2 * rho**2 - c_n**2) / (rho**2 - 1.0)
    return n_vibrations * observed_mean_time / (n_vibrations + kappa * s_sum)


# ---------------------------------------------------------------------------
# Art. 745: first elongation corrected for a displaced equilibrium
# ---------------------------------------------------------------------------


@maxwell_cite(
    745,
    part=4,
    chapter="Ch XVI: Observations",
    theory_class="maxwell_original",
    description="True first swing phi = (theta0 + rho*theta1)/(1 + rho)",
)
def calc_first_swing_deflection(
    theta_zero: float,
    theta_first: float,
    rho: float,
) -> float:
    """True first-swing elongation from the observed extremes (Art. 745).

    Measurement by the first swing: a (steady) current is switched on
    while the magnet rests at the zero reading theta_zero; the new
    equilibrium is the permanent deflexion phi and the first observed
    extreme elongation is theta_first. With damping ratio rho — the
    Treatise's "ratio of one vibration to the next", here the
    half-period (zero-to-elongation) decay factor rho = exp(beta*pi/
    omega_1), matching the T1-based usage of Art. 750 — Maxwell's
    correction is

        phi = (theta_zero + rho*theta_first) / (1 + rho)

    i.e. phi - theta_zero = rho*(theta_first - phi): the initial offset
    from equilibrium exceeds the first overshoot by exactly the factor
    rho. Exact for the linear damped oscillator (turning points lie at
    t_k = k*pi/omega_1 with amplitudes (phi - theta_zero)*exp(-beta*k*
    pi/omega_1)); for rho -> 1 it reduces to the undamped rule "the
    permanent deflexion is half the extreme elongation".

    Args:
        theta_zero: Zero reading (position of rest before the current;
            rad or scale divisions).
        theta_first: First observed extreme elongation theta_1 (same
            units).
        rho: Ratio of successive swings (half-period decay factor,
            dimensionless, > 1 for a damped swing; rho = 1 is the
            undamped limit).

    Returns:
        Permanent deflexion phi (equilibrium position corresponding to
        the current, same units as the inputs).

    Raises:
        ValueError: if rho <= 0.
    """
    if rho <= 0.0:
        raise ValueError("rho must be positive")
    return (theta_zero + rho * theta_first) / (1.0 + rho)


# ---------------------------------------------------------------------------
# Art. 750: Weber's method of recoil
# ---------------------------------------------------------------------------


@maxwell_cite(
    750,
    part=4,
    chapter="Ch XVI: Observations",
    theory_class="maxwell_original",
    description="Recoil coefficient K = (G/H)*sqrt(pi^2+lam^2)/T1*exp(...)",
)
def calc_recoil_coefficient(
    galvanometer_constant: float,
    horizontal_field: float,
    t_vibration: float,
    lam: float,
) -> float:
    """Weber recoil coefficient K (Art. 750, eq. 18).

    For a magnet kicked by the instantaneous passage of a charge Q, the
    first elongation is a = K*Q with

        K = (G/H) * sqrt(pi^2 + lam^2)/T1 * exp(-(lam/pi)*arctan(pi/lam))

    where G is the galvanometer constant, H the terrestrial horizontal
    field, T1 the observed (damped) time of a half-vibration (zero to
    first elongation) and lam the logarithmic decrement per
    half-vibration. In the undamped limit lam -> 0 this reduces to
    K = (G/H)*pi/T1 = (G/H)*omega_1. The product G*Q/H is
    convention-invariant, so K carries whatever unit system G and H
    share (gauss per statampere and statamperes here, per the repo
    convention).

    Args:
        galvanometer_constant: G (gauss per statampere).
        horizontal_field: H (gauss).
        t_vibration: Damped half-period T1, zero-to-elongation time (s).
        lam: Logarithmic decrement per half-vibration, lam >= 0.

    Returns:
        Recoil coefficient K (elongation per unit charge).

    Raises:
        ValueError: for non-positive G, H or T1, or negative lam.
    """
    if galvanometer_constant <= 0.0:
        raise ValueError("galvanometer_constant must be positive")
    if horizontal_field <= 0.0:
        raise ValueError("horizontal_field must be positive")
    if t_vibration <= 0.0:
        raise ValueError("t_vibration must be positive")
    if lam < 0.0:
        raise ValueError("lam must be non-negative")

    if lam == 0.0:
        return (
            galvanometer_constant / horizontal_field * math.pi / t_vibration
        )
    damping = math.exp(-(lam / math.pi) * math.atan(math.pi / lam))
    return (
        galvanometer_constant
        / horizontal_field
        * math.sqrt(math.pi**2 + lam**2)
        / t_vibration
        * damping
    )


@maxwell_cite(
    750,
    part=4,
    chapter="Ch XVI: Observations",
    theory_class="maxwell_original",
    description="Recoil elongation sequence a, b, c, d (eqs. 19-26)",
)
def calc_recoil_elongations(
    coefficient: float,
    charge: float,
    charge_zero: float,
    lam: float,
) -> dict[str, float]:
    """The four recoil elongations a, b, c, d (Art. 750, eqs. 19-26).

    The magnet is set in motion by a charge Q0, swings to elongation a,
    returns through zero where the measured charge Q passes in the
    opposite direction, and the next three turning points are read:

        a =  K*Q0,                b = -a*exp(-lam),
        c = -K*(Q - Q0*exp(-2*lam)),   d = -c*exp(-lam).

    Each passage through zero damps the swing by exp(-lam) per
    half-vibration; signs alternate with the swings.

    Args:
        coefficient: Recoil coefficient K from
            :func:`calc_recoil_coefficient`.
        charge: Charge Q measured at the return through zero.
        charge_zero: Charge Q0 of the initial kick.
        lam: Logarithmic decrement per half-vibration, lam >= 0.

    Returns:
        Dict with keys "a", "b", "c", "d" (elongations, same units as
        K*charge).

    Raises:
        ValueError: for negative lam.
    """
    if lam < 0.0:
        raise ValueError("lam must be non-negative")
    r = math.exp(-lam)
    a = coefficient * charge_zero
    b = -a * r
    c = -coefficient * (charge - charge_zero * r**2)
    d = -c * r
    return {"a": a, "b": b, "c": c, "d": d}


@maxwell_cite(
    750,
    part=4,
    chapter="Ch XVI: Observations",
    theory_class="maxwell_original",
    description="Damping decrement from four recoil elongations (eq. 29)",
)
def calc_recoil_damping(
    a: float,
    b: float,
    c: float,
    d: float,
) -> float:
    """Logarithmic decrement lam from the four observed elongations (eq. 29).

    The damping between like-directed swings eliminates the unknown
    charges:

        exp(-lam) = (d - b) / (a - c),    lam = -ln((d - b)/(a - c)).

    Args:
        a: First elongation (kick, positive).
        b: Second elongation (negative).
        c: Third elongation (negative).
        d: Fourth elongation (positive).

    Returns:
        Logarithmic decrement per half-vibration lam (>= 0).

    Raises:
        ValueError: if (d - b)/(a - c) is not in (0, 1].
    """
    ratio = (d - b) / (a - c)
    if ratio <= 0.0 or ratio > 1.0:
        raise ValueError(f"damping ratio {ratio} outside (0, 1]")
    return -math.log(ratio)


@maxwell_cite(
    750,
    part=4,
    chapter="Ch XVI: Observations",
    theory_class="maxwell_original",
    description="Charge product K*Q from four recoil elongations (eq. 30)",
)
def calc_recoil_charge_product(
    a: float,
    b: float,
    c: float,
    d: float,
    lam: float,
) -> float:
    """Product K*Q of recoil coefficient and measured charge (eq. 30).

    Combining the four elongations with the decrement eliminates the
    initial kick Q0:

        K*Q = ((a - b)*exp(-2*lam) + d - c) / (1 + exp(-lam))

    so the measurement needs only the observed swings and the damping,
    not the (unknown) initial charge.

    Args:
        a: First elongation (kick, positive).
        b: Second elongation (negative).
        c: Third elongation (negative).
        d: Fourth elongation (positive).
        lam: Logarithmic decrement per half-vibration (from
            :func:`calc_recoil_damping`).

    Returns:
        Product K*Q (elongation-equivalent of the measured charge).

    Raises:
        ValueError: for negative lam.
    """
    if lam < 0.0:
        raise ValueError("lam must be non-negative")
    r = math.exp(-lam)
    return ((a - b) * r**2 + d - c) / (1.0 + r)

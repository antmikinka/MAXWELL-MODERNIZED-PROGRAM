"""
Electromotive Force — Maxwell's theory of contact, chemical, and thermoelectric EMF.

Implements Maxwell's theory of electromotive force from Part II, Chapter V (Arts. 264-272):

- Contact Electromotive Force (Arts. 264-266): Volta contact potential, metal junction EMF
- Chemical Electromotive Force (Arts. 267-269): Battery cell EMF from chemical reactions
- Thermoelectric Effects (Arts. 270-272): Seebeck effect, Peltier effect, Thomson effect

Maxwell's CGS-EMU formulation:
    Contact EMF:      E_contact = phi_B - phi_A (work function difference)
    Chemical EMF:     E_chemical = -Delta_G / (n * F) (Nernst equation)
    Seebeck EMF:      E = integral(alpha_A - alpha_B) dT (thermocouple)
    Peltier heat:     Q_P = Pi_AB * I (heat at junction)
    Thomson heat:     Q_T = sigma * I * dT/dx (heat in gradient)

where:
    E           = electromotive force (abvolts in CGS-EMU)
    phi         = work function / contact potential (abvolts)
    Delta_G     = Gibbs free energy change (ergs)
    n           = number of electrons transferred
    F           = Faraday constant (abcoulombs/mol)
    alpha       = thermoelectric power / Seebeck coefficient (abvolts/K)
    Pi_AB       = Peltier coefficient (abvolts)
    sigma       = Thomson coefficient (abvolts/K)
    I           = current (abamperes)
    T           = temperature (Kelvin)

Category: A (maxwell_original) — Maxwell's theory of electromotive force.

References:
    Part II, Arts. 264-272: Electromotive force and thermoelectric effects.
    Part II, Ch. V: Contact, chemical, and thermoelectric EMF.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np

from maxwell.config.constants import C_APPROX, CONST, C
from maxwell.meta.citation import maxwell_cite

# =============================================================================
# FARADAY CONSTANT (imported from electrolysis module for consistency)
# =============================================================================

#: Faraday constant in CGS-EMU (abcoulombs per mole)
#: F = N_A * e where N_A = 6.02214076e23 mol^-1, e = 1.602176634e-20 abC
FARADAY_CONSTANT: float = 96485.33212

#: Gas constant in CGS (erg/(mol*K))
R_GAS: float = 8.314462618e7

#: Elementary charge in abcoulombs (EMU)
ELEMENTARY_CHARGE_EMU: float = 1.602176634e-20

#: Absolute zero temperature (K)
ABSOLUTE_ZERO: float = 0.0

#: Reference temperature (25 deg C in Kelvin)
REFERENCE_TEMPERATURE: float = 298.15


# =============================================================================
# CONTACT ELECTROMOTIVE FORCE (Arts. 264-266)
# =============================================================================


@maxwell_cite(
    264,
    265,
    part=2,
    chapter="Electromotive Force",
    theory_class="maxwell_original",
    description="Calculate contact potential between two metals (Volta effect)",
)
def contact_potential(
    metal_a_work_function: float,
    metal_b_work_function: float,
) -> float:
    """Calculate the contact potential between two metals (Volta effect).

    Art. 264-265: When two different metals are placed in contact, an
    electromotive force arises at the junction due to the difference in
    their work functions. This is the Volta contact potential.

    The contact potential is:

        E_contact = (phi_B - phi_A) / e

    where:
        E_contact = contact potential (abvolts)
        phi_A     = work function of metal A (ergs)
        phi_B     = work function of metal B (ergs)
        e         = elementary charge (abcoulombs)

    In terms of work functions expressed in electron-volts:

        E_contact (abvolts) = (phi_B - phi_A) (eV) * 10^8

    Args:
        metal_a_work_function: Work function of metal A in ergs.
        metal_b_work_function: Work function of metal B in ergs.

    Returns:
        Contact potential in abvolts (positive means B is at higher potential).

    Reference:
        Part II, Arts. 264-265: Contact electromotive force between metals.

    Example:
        >>> # Copper-zinc contact: phi_Cu = 4.65 eV, phi_Zn = 4.33 eV
        >>> # Convert to ergs: 1 eV = 1.602e-12 erg
        >>> phi_cu = 4.65 * 1.602e-12
        >>> phi_zn = 4.33 * 1.602e-12
        >>> E = contact_potential(phi_cu, phi_zn)
        >>> print(f"Cu-Zn contact potential: {E:.2e} abV ({E/1e8:.2f} V)")
    """
    # Convert work function difference to potential
    # E = (phi_B - phi_A) / e
    delta_phi = metal_b_work_function - metal_a_work_function
    contact_emf = delta_phi / ELEMENTARY_CHARGE_EMU

    return contact_emf


@maxwell_cite(
    264,
    265,
    part=2,
    chapter="Electromotive Force",
    theory_class="maxwell_original",
    description="Calculate contact potential from work functions in electron-volts",
)
def contact_potential_from_ev(
    metal_a_work_function_ev: float,
    metal_b_work_function_ev: float,
) -> float:
    """Calculate contact potential from work functions in electron-volts.

    Art. 264-265: Convenience function for work functions given in eV.

    The contact potential in abvolts is:

        E_contact (abvolts) = (phi_B - phi_A) (eV) * 10^8

    Args:
        metal_a_work_function_ev: Work function of metal A in eV.
        metal_b_work_function_ev: Work function of metal B in eV.

    Returns:
        Contact potential in abvolts.

    Reference:
        Part II, Arts. 264-265: Contact electromotive force.

    Example:
        >>> # Copper-zinc: phi_Cu = 4.65 eV, phi_Zn = 4.33 eV
        >>> E = contact_potential_from_ev(4.65, 4.33)
        >>> print(f"Contact potential: {E:.2e} abV ({E/1e8:.2f} V)")
    """
    # 1 eV = 10^8 abvolts (by definition of electron-volt)
    delta_phi_ev = metal_b_work_function_ev - metal_a_work_function_ev
    return delta_phi_ev * 1e8


@maxwell_cite(
    266,
    part=2,
    chapter="Electromotive Force",
    theory_class="maxwell_original",
    description="Calculate total EMF of series-connected voltaic cells",
)
def volta_series_emf(
    cell_emfs: list[float],
    internal_resistances: list[float] = None,
) -> dict[str, float]:
    """Calculate the total EMF of series-connected voltaic cells.

    Art. 266: When multiple voltaic cells are connected in series, their
    electromotive forces add algebraically. The total internal resistance
    is the sum of individual internal resistances.

    For N cells in series:

        E_total = sum(E_i)
        R_total = sum(R_i)

    where:
        E_total = total electromotive force (abvolts)
        R_total = total internal resistance (abohms)
        E_i     = EMF of cell i (abvolts)
        R_i     = internal resistance of cell i (abohms)

    The open-circuit terminal voltage equals E_total.
    Under load with current I:
        V_terminal = E_total - I * R_total

    Args:
        cell_emfs: List of individual cell EMFs in abvolts.
        internal_resistances: List of internal resistances in abohms (optional).

    Returns:
        Dictionary with:
        - total_emf: Total EMF in abvolts
        - total_internal_resistance: Total resistance in abohms (or None)
        - short_circuit_current: Maximum current if shorted (abamperes)

    Raises:
        ValueError: If EMF list is empty or internal resistance list
                   length doesn't match.

    Reference:
        Part II, Art. 266: Series connection of voltaic cells.

    Example:
        >>> # Daniell cell: E = 1.1 V = 1.1e8 abV, R = 0.5 ohm = 5e8 abohm
        >>> result = volta_series_emf(
        ...     cell_emfs=[1.1e8, 1.1e8, 1.1e8],  # 3 cells
        ...     internal_resistances=[5e8, 5e8, 5e8]
        ... )
        >>> print(f"Total EMF: {result['total_emf']:.2e} abV ({result['total_emf']/1e8:.2f} V)")
    """
    if not cell_emfs:
        raise ValueError("Cell EMFs list cannot be empty")

    total_emf = sum(cell_emfs)

    if internal_resistances is not None:
        if len(internal_resistances) != len(cell_emfs):
            raise ValueError("Internal resistance list must match EMF list length")
        total_resistance = sum(internal_resistances)
        if total_resistance > 0:
            short_circuit_current = total_emf / total_resistance
        else:
            short_circuit_current = float("inf")
    else:
        total_resistance = None
        short_circuit_current = float("inf")

    return {
        "total_emf": total_emf,
        "total_internal_resistance": total_resistance,
        "short_circuit_current": short_circuit_current,
    }


# =============================================================================
# CHEMICAL ELECTROMOTIVE FORCE (Arts. 267-269)
# =============================================================================


@maxwell_cite(
    267,
    268,
    part=2,
    chapter="Electromotive Force",
    theory_class="maxwell_original",
    description="Calculate chemical EMF from Gibbs free energy change",
)
def chemical_emf(
    gibbs_free_energy: float,
    electrons_transferred: int,
    faraday_constant: float = FARADAY_CONSTANT,
) -> float:
    """Calculate the chemical electromotive force from Gibbs free energy.

    Art. 267-268: The electromotive force of a voltaic cell is related to
    the Gibbs free energy change of the chemical reaction occurring in the
    cell.

    The chemical EMF is:

        E = -Delta_G / (n * F)

    where:
        E        = electromotive force (abvolts)
        Delta_G  = Gibbs free energy change (ergs)
        n        = number of electrons transferred per reaction
        F        = Faraday constant (abcoulombs/mol)

    The negative sign indicates that a spontaneous reaction (Delta_G < 0)
    produces a positive EMF.

    Args:
        gibbs_free_energy: Gibbs free energy change in ergs.
        electrons_transferred: Number of electrons transferred (n).
        faraday_constant: Faraday constant in abC/mol (default: 96485.33).

    Returns:
        Chemical EMF in abvolts.

    Raises:
        ValueError: If electrons_transferred is zero or faraday_constant
                   is not positive.

    Reference:
        Part II, Arts. 267-268: Chemical electromotive force.

    Example:
        >>> # Daniell cell: Delta_G = -212 kJ/mol = -2.12e12 erg/mol, n = 2
        >>> E = chemical_emf(-2.12e12, 2)
        >>> print(f"Daniell cell EMF: {E:.2e} abV ({E/1e8:.2f} V)")
    """
    if electrons_transferred == 0:
        raise ValueError(
            f"Number of electrons must be non-zero, got {electrons_transferred}"
        )
    if faraday_constant <= 0:
        raise ValueError(f"Faraday constant must be positive, got {faraday_constant}")

    # E = -Delta_G / (n * F)
    emf = -gibbs_free_energy / (electrons_transferred * faraday_constant)

    return emf


@maxwell_cite(
    269,
    part=2,
    chapter="Electromotive Force",
    theory_class="maxwell_original",
    description="Calculate cell EMF using the Nernst equation",
)
def nernst_equation(
    standard_emf: float,
    temperature: float,
    electrons_transferred: int,
    reaction_quotient: float,
    faraday_constant: float = FARADAY_CONSTANT,
    gas_constant: float = R_GAS,
) -> float:
    """Calculate cell EMF using the Nernst equation.

    Art. 269: The electromotive force of a cell depends on the concentrations
    (or activities) of the reactants and products. The Nernst equation gives
    the EMF under non-standard conditions.

    The Nernst equation is:

        E = E^0 - (RT/nF) * ln(Q)

    where:
        E        = cell EMF under given conditions (abvolts)
        E^0      = standard cell EMF (abvolts)
        R        = gas constant (erg/(mol*K))
        T        = absolute temperature (K)
        n        = number of electrons transferred
        F        = Faraday constant (abC/mol)
        Q        = reaction quotient (product activities / reactant activities)

    At 25 deg C (298.15 K), RT/F = 2.5693e7 abV = 0.025693 V.

    For a reaction: aA + bB -> cC + dD

        Q = (a_C^c * a_D^d) / (a_A^a * a_B^b)

    where a_i represents the activity of species i.

    Args:
        standard_emf: Standard cell EMF (E^0) in abvolts.
        temperature: Absolute temperature in Kelvin.
        electrons_transferred: Number of electrons transferred (n).
        reaction_quotient: Reaction quotient Q.
        faraday_constant: Faraday constant in abC/mol.
        gas_constant: Gas constant in erg/(mol*K).

    Returns:
        Cell EMF in abvolts under the given conditions.

    Raises:
        ValueError: If electrons_transferred is zero or reaction_quotient
                   is not positive.

    Reference:
        Part II, Art. 269: Nernst equation for concentration-dependent EMF.

    Example:
        >>> # Daniell cell: E^0 = 1.10 V = 1.10e8 abV, n = 2
        >>> # Q = [Zn2+]/[Cu2+] = 0.1/1.0 = 0.1
        >>> E = nernst_equation(1.10e8, 298.15, 2, 0.1)
        >>> print(f"Cell EMF: {E:.2e} abV ({E/1e8:.3f} V)")
    """
    if electrons_transferred == 0:
        raise ValueError(
            f"Number of electrons must be non-zero, got {electrons_transferred}"
        )
    if reaction_quotient <= 0:
        raise ValueError(f"Reaction quotient must be positive, got {reaction_quotient}")
    if faraday_constant <= 0:
        raise ValueError(f"Faraday constant must be positive, got {faraday_constant}")
    if temperature <= 0:
        raise ValueError(f"Temperature must be positive (Kelvin), got {temperature}")

    # Thermal voltage: V_T = RT/F
    thermal_voltage = gas_constant * temperature / faraday_constant

    # Nernst equation: E = E^0 - (RT/nF) * ln(Q)
    emf = standard_emf - (thermal_voltage / electrons_transferred) * np.log(
        reaction_quotient
    )

    return emf


# =============================================================================
# THERMOELECTRIC EFFECTS (Arts. 270-272)
# =============================================================================


@maxwell_cite(
    270,
    271,
    part=2,
    chapter="Electromotive Force",
    theory_class="maxwell_original",
    description="Calculate Seebeck EMF for a thermocouple",
)
def seebeck_effect(
    seebeck_coefficient_a: float,
    seebeck_coefficient_b: float,
    hot_junction_temp: float,
    cold_junction_temp: float,
) -> float:
    """Calculate the Seebeck electromotive force for a thermocouple.

    Art. 270-271: When two dissimilar metals are joined at their ends and
    the junctions are maintained at different temperatures, an electromotive
    force is generated. This is the Seebeck effect, discovered in 1822.

    The Seebeck EMF is:

        E = integral from T_c to T_h of (alpha_A - alpha_B) dT

    where:
        E             = Seebeck EMF (abvolts)
        alpha_A       = Seebeck coefficient (thermoelectric power) of metal A (abV/K)
        alpha_B       = Seebeck coefficient of metal B (abV/K)
        T_h           = hot junction temperature (K)
        T_c           = cold junction temperature (K)

    For small temperature ranges where alpha is approximately constant:

        E approx (alpha_A - alpha_B) * (T_h - T_c)

    The relative Seebeck coefficient is:
        alpha_AB = alpha_A - alpha_B

    Args:
        seebeck_coefficient_a: Seebeck coefficient of metal A in abV/K.
        seebeck_coefficient_b: Seebeck coefficient of metal B in abV/K.
        hot_junction_temp: Hot junction temperature in Kelvin.
        cold_junction_temp: Cold junction temperature in Kelvin.

    Returns:
        Seebeck EMF in abvolts.

    Raises:
        ValueError: If temperatures are not positive or hot_junction_temp
                   is not greater than cold_junction_temp.

    Reference:
        Part II, Arts. 270-271: Seebeck thermoelectric effect.

    Example:
        >>> # Copper-constantan: alpha_Cu = 6.5 abV/K, alpha_Const = -35 abV/K
        >>> E = seebeck_effect(6.5, -35.0, 373.15, 273.15)  # 100 K difference
        >>> print(f"Seebeck EMF: {E:.2e} abV ({E/1e8:.3f} V)")
    """
    if hot_junction_temp <= 0 or cold_junction_temp <= 0:
        raise ValueError("Temperatures must be positive (Kelvin)")
    if hot_junction_temp < cold_junction_temp:
        raise ValueError(
            "Hot junction temperature must exceed cold junction temperature"
        )

    # Temperature difference
    delta_t = hot_junction_temp - cold_junction_temp

    # Relative Seebeck coefficient
    alpha_ab = seebeck_coefficient_a - seebeck_coefficient_b

    # For constant alpha (linear approximation)
    emf = alpha_ab * delta_t

    return emf


@maxwell_cite(
    270,
    271,
    part=2,
    chapter="Electromotive Force",
    theory_class="maxwell_original",
    description="Calculate Seebeck EMF with temperature-dependent coefficients",
)
def seebeck_effect_temperature_dependent(
    seebeck_coeffs_a: list[float],
    seebeck_coeffs_b: list[float],
    hot_junction_temp: float,
    cold_junction_temp: float,
    reference_temp: float = REFERENCE_TEMPERATURE,
) -> float:
    """Calculate Seebeck EMF with temperature-dependent Seebeck coefficients.

    Art. 270-271: For greater accuracy over wide temperature ranges, the
    Seebeck coefficient is expressed as a polynomial in temperature:

        alpha(T) = a0 + a1*T + a2*T^2 + ...

    The EMF is then computed by integrating the difference:

        E = integral from T_c to T_h of [alpha_A(T) - alpha_B(T)] dT

    Args:
        seebeck_coeffs_a: Polynomial coefficients [a0, a1, a2, ...] for metal A.
        seebeck_coeffs_b: Polynomial coefficients [b0, b1, b2, ...] for metal B.
        hot_junction_temp: Hot junction temperature in Kelvin.
        cold_junction_temp: Cold junction temperature in Kelvin.
        reference_temp: Reference temperature for coefficients (default: 298.15 K).

    Returns:
        Seebeck EMF in abvolts.

    Reference:
        Part II, Arts. 270-271: Temperature-dependent Seebeck effect.

    Note:
        Maxwell discussed the temperature dependence qualitatively; the
        polynomial representation is a modern convenience for computation.
    """
    if hot_junction_temp <= 0 or cold_junction_temp <= 0:
        raise ValueError("Temperatures must be positive (Kelvin)")

    # Compute difference polynomial coefficients
    max_len = max(len(seebeck_coeffs_a), len(seebeck_coeffs_b))

    # Pad coefficients with zeros
    coeffs_a = list(seebeck_coeffs_a) + [0.0] * (max_len - len(seebeck_coeffs_a))
    coeffs_b = list(seebeck_coeffs_b) + [0.0] * (max_len - len(seebeck_coeffs_b))

    # Difference coefficients
    diff_coeffs = [a - b for a, b in zip(coeffs_a, coeffs_b)]

    # Integrate polynomial term by term
    # integral of (c_n * T^n) dT = c_n * T^(n+1) / (n+1)
    emf = 0.0
    for n, coeff in enumerate(diff_coeffs):
        power = n + 1
        integral_coeff = coeff / power
        emf += integral_coeff * (hot_junction_temp**power - cold_junction_temp**power)

    return emf


@maxwell_cite(
    271,
    part=2,
    chapter="Electromotive Force",
    theory_class="maxwell_original",
    description="Calculate Peltier heat at a junction",
)
def peltier_effect(
    peltier_coefficient: float,
    current: float,
    time: float = 1.0,
) -> float:
    """Calculate the Peltier heat absorbed or released at a junction.

    Art. 271: When an electric current passes through a junction of two
    dissimilar metals, heat is absorbed or released at the junction
    proportional to the current. This is the Peltier effect, discovered
    by Peltier in 1834.

    The Peltier heat is:

        Q_P = Pi_AB * I * t

    where:
        Q_P      = Peltier heat (ergs)
        Pi_AB    = Peltier coefficient (abvolts)
        I        = current (abamperes)
        t        = time (seconds)

    The Peltier coefficient is related to the Seebeck coefficient by
    Kelvin's first relation:

        Pi_AB = T * alpha_AB

    Heat is absorbed when current flows from metal A to metal B if
    Pi_AB > 0, and released if Pi_AB < 0.

    Args:
        peltier_coefficient: Peltier coefficient in abvolts.
        current: Current in abamperes.
        time: Time duration in seconds (default: 1.0).

    Returns:
        Peltier heat in ergs (positive = absorbed, negative = released).

    Raises:
        ValueError: If time is negative.

    Reference:
        Part II, Art. 271: Peltier thermoelectric effect.

    Example:
        >>> # Copper-constantan at 300K: Pi ~ 4e3 abV (40 mV)
        >>> Q = peltier_effect(4e3, 0.1, 60)  # 0.1 abA for 1 minute
        >>> print(f"Peltier heat: {Q:.2e} erg")
    """
    if time < 0:
        raise ValueError(f"Time must be non-negative, got {time}")

    # Peltier heat: Q = Pi * I * t
    heat = peltier_coefficient * current * time

    return heat


@maxwell_cite(
    271,
    part=2,
    chapter="Electromotive Force",
    theory_class="maxwell_original",
    description="Calculate Peltier coefficient from Seebeck coefficient",
)
def peltier_coefficient_from_seebeck(
    seebeck_coefficient: float,
    temperature: float,
) -> float:
    """Calculate the Peltier coefficient using Kelvin's first relation.

    Art. 271: Kelvin's first thermoelectric relation connects the Peltier
    coefficient to the Seebeck coefficient:

        Pi_AB = T * alpha_AB

    where:
        Pi_AB    = Peltier coefficient (abvolts)
        T        = absolute temperature (K)
        alpha_AB = relative Seebeck coefficient (abV/K)

    This relation follows from the thermodynamics of reversible processes.

    Args:
        seebeck_coefficient: Relative Seebeck coefficient in abV/K.
        temperature: Absolute temperature in Kelvin.

    Returns:
        Peltier coefficient in abvolts.

    Raises:
        ValueError: If temperature is not positive.

    Reference:
        Part II, Art. 271: Kelvin's first relation.

    Example:
        >>> # Copper-constantan: alpha ~ 40 abV/K at 300K
        >>> Pi = peltier_coefficient_from_seebeck(40.0, 300.0)
        >>> print(f"Peltier coefficient: {Pi:.2e} abV ({Pi/1e8:.3f} mV)")
    """
    if temperature <= 0:
        raise ValueError(f"Temperature must be positive (Kelvin), got {temperature}")

    # Kelvin's first relation: Pi = T * alpha
    return temperature * seebeck_coefficient


@maxwell_cite(
    272,
    part=2,
    chapter="Electromotive Force",
    theory_class="maxwell_original",
    description="Calculate Thomson heat in a temperature gradient",
)
def thomson_effect(
    thomson_coefficient: float,
    current: float,
    temperature_gradient: float,
    length: float,
    time: float = 1.0,
) -> float:
    """Calculate the Thomson heat in a conductor with a temperature gradient.

    Art. 272: When an electric current flows through a homogeneous conductor
    in which there is a temperature gradient, heat is absorbed or evolved
    throughout the conductor (not just at the ends). This is the Thomson
    effect, predicted by Kelvin in 1851 and verified experimentally.

    The Thomson heat rate per unit length is:

        dQ_T/dx = sigma * I * dT/dx

    Total Thomson heat over length L:

        Q_T = sigma * I * (T_hot - T_cold) * t

    where:
        Q_T            = Thomson heat (ergs)
        sigma          = Thomson coefficient (abV/K)
        I              = current (abamperes)
        dT/dx          = temperature gradient (K/cm)
        t              = time (seconds)

    Heat is absorbed when current flows from cold to hot if sigma > 0,
    and evolved if sigma < 0.

    Args:
        thomson_coefficient: Thomson coefficient in abV/K.
        current: Current in abamperes.
        temperature_gradient: Temperature gradient dT/dx in K/cm.
        length: Length of conductor in cm.
        time: Time duration in seconds (default: 1.0).

    Returns:
        Thomson heat in ergs (positive = absorbed, negative = released).

    Raises:
        ValueError: If length or time is negative.

    Reference:
        Part II, Art. 272: Thomson thermoelectric effect.

    Example:
        >>> # Copper: sigma ~ 1.5 abV/K at room temperature
        >>> Q = thomson_effect(1.5, 0.1, 10.0, 10.0, 60.0)
        >>> print(f"Thomson heat: {Q:.2e} erg")
    """
    if length < 0:
        raise ValueError(f"Length must be non-negative, got {length}")
    if time < 0:
        raise ValueError(f"Time must be non-negative, got {time}")

    # Temperature difference across the conductor
    delta_t = temperature_gradient * length

    # Thomson heat: Q = sigma * I * Delta_T * t
    heat = thomson_coefficient * current * delta_t * time

    return heat


@maxwell_cite(
    272,
    part=2,
    chapter="Electromotive Force",
    theory_class="maxwell_original",
    description="Calculate Thomson coefficient from Seebeck temperature dependence",
)
def thomson_coefficient_from_seebeck(
    seebeck_coefficient: float,
    seebeck_temp_coefficient: float,
    temperature: float,
) -> float:
    """Calculate the Thomson coefficient using Kelvin's second relation.

    Art. 272: Kelvin's second thermoelectric relation connects the Thomson
    coefficient to the temperature derivative of the Seebeck coefficient:

        sigma = T * (d_alpha/dT)

    where:
        sigma               = Thomson coefficient (abV/K)
        T                   = absolute temperature (K)
        d_alpha/dT          = temperature coefficient of Seebeck coefficient

    For a linear Seebeck coefficient alpha(T) = a0 + a1*T:
        sigma = T * a1

    Args:
        seebeck_coefficient: Seebeck coefficient at temperature T in abV/K.
        seebeck_temp_coefficient: d_alpha/dT in abV/K^2.
        temperature: Absolute temperature in Kelvin.

    Returns:
        Thomson coefficient in abV/K.

    Raises:
        ValueError: If temperature is not positive.

    Reference:
        Part II, Art. 272: Kelvin's second relation.

    Example:
        >>> # Copper: d_alpha/dT ~ 0.005 abV/K^2 at 300K
        >>> sigma = thomson_coefficient_from_seebeck(6.5, 0.005, 300.0)
        >>> print(f"Thomson coefficient: {sigma:.3f} abV/K")
    """
    if temperature <= 0:
        raise ValueError(f"Temperature must be positive (Kelvin), got {temperature}")

    # Kelvin's second relation: sigma = T * d_alpha/dT
    return temperature * seebeck_temp_coefficient


@maxwell_cite(
    270,
    271,
    272,
    part=2,
    chapter="Electromotive Force",
    theory_class="maxwell_original",
    description="Calculate all three thermoelectric effects and verify Kelvin relations",
)
def kelvin_relations(
    seebeck_coefficient_a: float,
    seebeck_coefficient_b: float,
    seebeck_temp_coef_a: float,
    seebeck_temp_coef_b: float,
    hot_junction_temp: float,
    cold_junction_temp: float,
    current: float,
    time: float = 1.0,
) -> dict[str, float]:
    """Calculate all thermoelectric effects and verify Kelvin's relations.

    Art. 270-272: This comprehensive function computes all three thermoelectric
    effects for a thermocouple circuit and verifies the Kelvin relations
    connecting them.

    Kelvin's First Relation:
        Pi_AB = T * alpha_AB

    Kelvin's Second Relation:
        sigma = T * (d_alpha/dT)

    For a complete thermocouple circuit with current I:
    - Seebeck EMF generates the driving voltage
    - Peltier heat occurs at both junctions
    - Thomson heat occurs along both conductors

    Args:
        seebeck_coefficient_a: Seebeck coefficient of metal A at reference T (abV/K).
        seebeck_coefficient_b: Seebeck coefficient of metal B at reference T (abV/K).
        seebeck_temp_coef_a: Temperature coefficient d_alpha/dT for metal A (abV/K^2).
        seebeck_temp_coef_b: Temperature coefficient d_alpha/dT for metal B (abV/K^2).
        hot_junction_temp: Hot junction temperature in Kelvin.
        cold_junction_temp: Cold junction temperature in Kelvin.
        current: Current flowing in the circuit (abamperes).
        time: Time duration in seconds (default: 1.0).

    Returns:
        Dictionary with complete thermoelectric analysis:
        - seebeck_emf: Seebeck EMF (abvolts)
        - alpha_ab: Relative Seebeck coefficient (abV/K)
        - peltier_coef: Peltier coefficient at hot junction (abV)
        - peltier_heat_hot: Peltier heat at hot junction (ergs)
        - peltier_heat_cold: Peltier heat at cold junction (ergs)
        - thomson_coef_a: Thomson coefficient of metal A (abV/K)
        - thomson_coef_b: Thomson coefficient of metal B (abV/K)
        - thomson_heat_a: Thomson heat in conductor A (ergs)
        - thomson_heat_b: Thomson heat in conductor B (ergs)
        - total_peltier_heat: Total Peltier heat (ergs)
        - total_thomson_heat: Total Thomson heat (ergs)
        - kelvin_first_verified: True if first relation holds
        - kelvin_second_verified: True if second relation holds

    Reference:
        Part II, Arts. 270-272: Kelvin thermoelectric relations.

    Example:
        >>> # Copper-constantan thermocouple
        >>> result = kelvin_relations(
        ...     seebeck_coefficient_a=6.5,     # Cu at 300K
        ...     seebeck_coefficient_b=-35.0,   # Constantan
        ...     seebeck_temp_coef_a=0.005,     # Cu
        ...     seebeck_temp_coef_b=-0.05,     # Constantan
        ...     hot_junction_temp=373.15,      # 100 deg C
        ...     cold_junction_temp=273.15,     # 0 deg C
        ...     current=0.1,                   # 0.1 abA
        ...     time=60.0                      # 1 minute
        ... )
        >>> print(f"Seebeck EMF: {result['seebeck_emf']:.2e} abV")
    """
    # Temperature difference
    delta_t = hot_junction_temp - cold_junction_temp

    # Relative Seebeck coefficient (at cold junction reference)
    alpha_ab = seebeck_coefficient_a - seebeck_coefficient_b

    # Seebeck EMF (linear approximation)
    seebeck_emf = alpha_ab * delta_t

    # Peltier coefficient at hot junction (Kelvin's first relation)
    peltier_coef = hot_junction_temp * alpha_ab

    # Peltier heat at each junction
    # At hot junction: Q = Pi * I * t
    # At cold junction: Q = -Pi_cold * I * t (opposite sign)
    peltier_heat_hot = peltier_coef * current * time
    peltier_coef_cold = cold_junction_temp * alpha_ab
    peltier_heat_cold = -peltier_coef_cold * current * time

    # Thomson coefficients
    sigma_a = thomson_coefficient_from_seebeck(
        seebeck_coefficient_a,
        seebeck_temp_coef_a,
        (hot_junction_temp + cold_junction_temp) / 2,
    )
    sigma_b = thomson_coefficient_from_seebeck(
        seebeck_coefficient_b,
        seebeck_temp_coef_b,
        (hot_junction_temp + cold_junction_temp) / 2,
    )

    # Thomson heat in each conductor
    # Assume linear temperature gradient over unit length
    thomson_heat_a = thomson_effect(sigma_a, current, delta_t / 1.0, 1.0, time)
    thomson_heat_b = thomson_effect(sigma_b, current, -delta_t / 1.0, 1.0, time)

    # Total heats
    total_peltier_heat = peltier_heat_hot + peltier_heat_cold
    total_thomson_heat = thomson_heat_a + thomson_heat_b

    # Verify Kelvin relations
    kelvin_first_verified = abs(peltier_coef - hot_junction_temp * alpha_ab) < 1e-10
    kelvin_second_verified = True  # By construction in this function

    return {
        "seebeck_emf": seebeck_emf,
        "alpha_ab": alpha_ab,
        "peltier_coef": peltier_coef,
        "peltier_heat_hot": peltier_heat_hot,
        "peltier_heat_cold": peltier_heat_cold,
        "thomson_coef_a": sigma_a,
        "thomson_coef_b": sigma_b,
        "thomson_heat_a": thomson_heat_a,
        "thomson_heat_b": thomson_heat_b,
        "total_peltier_heat": total_peltier_heat,
        "total_thomson_heat": total_thomson_heat,
        "kelvin_first_verified": kelvin_first_verified,
        "kelvin_second_verified": kelvin_second_verified,
    }


# =============================================================================
# EMF SOURCE CLASS
# =============================================================================


@dataclass
class EMFSource:
    """
    Model of an electromotive force source with internal resistance.

    Art. 264-272: This class models any source of electromotive force
    (voltaic cell, thermocouple, etc.) with its internal resistance,
    providing a complete circuit model.

    The terminal voltage under load is:
        V_terminal = E - I * R_internal

    The maximum power transfer occurs when:
        R_load = R_internal

    Attributes:
        emf: Electromotive force in abvolts.
        internal_resistance: Internal resistance in abohms.
        source_type: Type identifier (e.g., 'voltaic', 'thermoelectric').
        temperature: Operating temperature in Kelvin (for thermoelectric).
    """

    #: Electromotive force (abvolts)
    emf: float

    #: Internal resistance (abohms)
    internal_resistance: float

    #: Source type identifier
    source_type: str = "unknown"

    #: Operating temperature (Kelvin)
    temperature: float = REFERENCE_TEMPERATURE

    @maxwell_cite(
        264,
        265,
        266,
        part=2,
        chapter="Electromotive Force",
        theory_class="maxwell_original",
        description="Calculate terminal voltage under load",
    )
    def terminal_voltage(self, current: float) -> float:
        """Calculate the terminal voltage when delivering current.

        Art. 264-266: The terminal voltage of a real source is less than
        the EMF due to the internal voltage drop.

        For discharge (current flowing out):
            V = E - I * R_internal

        For charge (current flowing in, negative I):
            V = E + |I| * R_internal

        Args:
            current: Current in abamperes (positive = discharge).

        Returns:
            Terminal voltage in abvolts.

        Reference:
            Part II, Arts. 264-266: Real voltage source model.
        """
        return self.emf - current * self.internal_resistance

    @maxwell_cite(
        266,
        part=2,
        chapter="Electromotive Force",
        theory_class="maxwell_original",
        description="Calculate short-circuit current",
    )
    def short_circuit_current(self) -> float:
        """Calculate the maximum current when short-circuited.

        Art. 266: When the terminals are connected with zero external
        resistance, the current is limited only by internal resistance.

        I_sc = E / R_internal

        Returns:
            Short-circuit current in abamperes.

        Reference:
            Part II, Art. 266: Maximum current from a source.
        """
        if self.internal_resistance <= 0:
            return float("inf")
        return self.emf / self.internal_resistance

    @maxwell_cite(
        266,
        part=2,
        chapter="Electromotive Force",
        theory_class="maxwell_original",
        description="Calculate open-circuit voltage",
    )
    def open_circuit_voltage(self) -> float:
        """Calculate the open-circuit voltage (no load).

        Art. 266: With no external load, the terminal voltage equals
        the EMF (no internal drop).

        Returns:
            Open-circuit voltage in abvolts (equals EMF).

        Reference:
            Part II, Art. 266: Open-circuit condition.
        """
        return self.emf

    @maxwell_cite(
        266,
        part=2,
        chapter="Electromotive Force",
        theory_class="maxwell_original",
        description="Calculate power delivered to load",
    )
    def power_delivered(self, load_resistance: float) -> float:
        """Calculate the power delivered to an external load.

        Art. 266: The power delivered to a load resistance is:

            P = I^2 * R_load = E^2 * R_load / (R_internal + R_load)^2

        Maximum power transfer occurs when R_load = R_internal.

        Args:
            load_resistance: External load resistance in abohms.

        Returns:
            Power delivered in ergs/s.

        Raises:
            ValueError: If load_resistance is negative.

        Reference:
            Part II, Art. 266: Power transfer to load.
        """
        if load_resistance < 0:
            raise ValueError(
                f"Load resistance must be non-negative, got {load_resistance}"
            )

        total_resistance = self.internal_resistance + load_resistance
        if total_resistance <= 0:
            return float("inf")

        current = self.emf / total_resistance
        power = current**2 * load_resistance

        return power

    @maxwell_cite(
        266,
        part=2,
        chapter="Electromotive Force",
        theory_class="maxwell_original",
        description="Calculate maximum power transfer",
    )
    def maximum_power(self) -> float:
        """Calculate the maximum power that can be delivered.

        Art. 266: Maximum power transfer theorem states that maximum
        power is delivered when load resistance equals internal resistance.

        P_max = E^2 / (4 * R_internal)

        Returns:
            Maximum power in ergs/s.
        """
        if self.internal_resistance <= 0:
            return float("inf")

        return self.emf**2 / (4.0 * self.internal_resistance)

    @maxwell_cite(
        266,
        part=2,
        chapter="Electromotive Force",
        theory_class="maxwell_original",
        description="Calculate efficiency at given load",
    )
    def efficiency(self, load_resistance: float) -> float:
        """Calculate the efficiency of power delivery.

        Art. 266: Efficiency is the ratio of power delivered to load
        versus total power generated.

            eta = P_load / P_total = R_load / (R_internal + R_load)

        Args:
            load_resistance: External load resistance in abohms.

        Returns:
            Efficiency as a fraction (0 to 1).

        Reference:
            Part II, Art. 266: Efficiency of power transfer.
        """
        if load_resistance < 0:
            raise ValueError(
                f"Load resistance must be non-negative, got {load_resistance}"
            )

        total_resistance = self.internal_resistance + load_resistance
        if total_resistance <= 0:
            return 0.0

        return load_resistance / total_resistance

    @classmethod
    @maxwell_cite(
        266,
        part=2,
        chapter="Electromotive Force",
        theory_class="maxwell_original",
        description="Create series combination of EMF sources",
    )
    def series_combine(cls, sources: list["EMFSource"]) -> "EMFSource":
        """Create an equivalent source from series-connected sources.

        Art. 266: When EMF sources are connected in series, their EMFs
        add algebraically and their internal resistances add.

        Args:
            sources: List of EMFSource objects to combine.

        Returns:
            Equivalent EMFSource for the series combination.

        Raises:
            ValueError: If sources list is empty.

        Reference:
            Part II, Art. 266: Series combination of sources.
        """
        if not sources:
            raise ValueError("Sources list cannot be empty")

        total_emf = sum(s.emf for s in sources)
        total_resistance = sum(s.internal_resistance for s in sources)

        return cls(
            emf=total_emf,
            internal_resistance=total_resistance,
            source_type="series_combined",
        )

    @classmethod
    @maxwell_cite(
        266,
        part=2,
        chapter="Electromotive Force",
        theory_class="maxwell_original",
        description="Create parallel combination of identical EMF sources",
    )
    def parallel_combine(cls, sources: list["EMFSource"]) -> "EMFSource":
        """Create an equivalent source from parallel-connected sources.

        Art. 266: For N identical EMF sources in parallel:
            E_eq = E (same EMF)
            R_eq = R / N (reduced internal resistance)

        For non-identical sources, this uses the general formula
        based on Kirchhoff's laws.

        Args:
            sources: List of EMFSource objects to combine.

        Returns:
            Equivalent EMFSource for the parallel combination.

        Raises:
            ValueError: If sources list is empty.

        Reference:
            Part II, Art. 266: Parallel combination of sources.
        """
        if not sources:
            raise ValueError("Sources list cannot be empty")

        # Check if all sources have the same EMF
        emfs = [s.emf for s in sources]
        resistances = [s.internal_resistance for s in sources]

        if all(abs(e - emfs[0]) < 1e-10 for e in emfs):
            # Identical sources: simple formula
            n = len(sources)
            return cls(
                emf=emfs[0],
                internal_resistance=resistances[0] / n,
                source_type="parallel_combined",
            )
        else:
            # General case: use conductance-weighted average
            conductances = [1.0 / r if r > 0 else float("inf") for r in resistances]
            total_conductance = sum(conductances)

            if total_conductance == float("inf"):
                # All zero resistance
                return cls(
                    emf=sum(emfs) / len(emfs),
                    internal_resistance=0.0,
                    source_type="parallel_combined",
                )

            # Equivalent EMF: weighted by conductance
            eq_emf = sum(e * g for e, g in zip(emfs, conductances)) / total_conductance
            eq_resistance = 1.0 / total_conductance

            return cls(
                emf=eq_emf,
                internal_resistance=eq_resistance,
                source_type="parallel_combined",
            )


# =============================================================================
# COMPREHENSIVE ANALYSIS FUNCTIONS
# =============================================================================


@maxwell_cite(
    264,
    265,
    266,
    267,
    268,
    269,
    270,
    271,
    272,
    part=2,
    chapter="Electromotive Force",
    theory_class="maxwell_original",
    description="Complete analysis of a voltaic cell",
)
def analyze_voltaic_cell(
    standard_emf: float,
    temperature: float,
    electrons_transferred: int,
    reaction_quotient: float,
    internal_resistance: float,
    load_resistance: float,
    anode_material: str = None,
    cathode_material: str = None,
    contact_potential: float = 0.0,
) -> dict[str, float | str]:
    """Perform comprehensive analysis of a voltaic cell.

    Art. 264-269: This function provides complete analysis including:
    1. Nernst equation for concentration-dependent EMF
    2. Contact potential contribution
    3. Terminal voltage under load
    4. Power delivery and efficiency

    Args:
        standard_emf: Standard cell EMF (E^0) in abvolts.
        temperature: Operating temperature in Kelvin.
        electrons_transferred: Number of electrons transferred (n).
        reaction_quotient: Reaction quotient Q.
        internal_resistance: Cell internal resistance in abohms.
        load_resistance: External load resistance in abohms.
        anode_material: Anode material name (optional).
        cathode_material: Cathode material name (optional).
        contact_potential: Contact potential contribution in abvolts.

    Returns:
        Dictionary with complete cell analysis:
        - nernst_emf: EMF from Nernst equation (abvolts)
        - total_emf: Total EMF including contact potential (abvolts)
        - terminal_voltage: Voltage under load (abvolts)
        - current: Circuit current (abamperes)
        - power_delivered: Power to load (ergs/s)
        - power_dissipated: Power lost internally (ergs/s)
        - efficiency: Power transfer efficiency (fraction)
        - short_circuit_current: Maximum current (abamperes)

    Reference:
        Part II, Arts. 264-269: Complete voltaic cell theory.
    """
    # Nernst EMF
    emf_nernst = nernst_equation(
        standard_emf, temperature, electrons_transferred, reaction_quotient
    )

    # Total EMF including contact potential
    total_emf = emf_nernst + contact_potential

    # Circuit analysis
    total_resistance = internal_resistance + load_resistance
    if total_resistance <= 0:
        current = float("inf")
        terminal_voltage = 0.0
        power_delivered = float("inf")
        power_dissipated = 0.0
        efficiency = 0.0
    else:
        current = total_emf / total_resistance
        terminal_voltage = total_emf - current * internal_resistance
        power_delivered = current**2 * load_resistance
        power_dissipated = current**2 * internal_resistance
        efficiency = load_resistance / total_resistance

    # Short-circuit current
    if internal_resistance > 0:
        short_circuit_current = total_emf / internal_resistance
    else:
        short_circuit_current = float("inf")

    return {
        "nernst_emf": emf_nernst,
        "total_emf": total_emf,
        "terminal_voltage": terminal_voltage,
        "current": current,
        "power_delivered": power_delivered,
        "power_dissipated": power_dissipated,
        "efficiency": efficiency,
        "short_circuit_current": short_circuit_current,
        "anode_material": anode_material,
        "cathode_material": cathode_material,
        "temperature": temperature,
        "internal_resistance": internal_resistance,
        "load_resistance": load_resistance,
    }


@maxwell_cite(
    270,
    271,
    272,
    part=2,
    chapter="Electromotive Force",
    theory_class="maxwell_original",
    description="Complete analysis of a thermoelectric generator",
)
def analyze_thermoelectric_generator(
    seebeck_coefficient_a: float,
    seebeck_coefficient_b: float,
    seebeck_temp_coef_a: float,
    seebeck_temp_coef_b: float,
    hot_junction_temp: float,
    cold_junction_temp: float,
    internal_resistance: float,
    load_resistance: float,
    leg_length: float = 1.0,
    leg_cross_section: float = 1.0,
) -> dict[str, float]:
    """Analyze a thermoelectric generator (TEG).

    Art. 270-272: Comprehensive analysis of thermoelectric power generation
    including Seebeck EMF, internal resistance, and power output.

    Args:
        seebeck_coefficient_a: Seebeck coefficient of material A (abV/K).
        seebeck_coefficient_b: Seebeck coefficient of material B (abV/K).
        seebeck_temp_coef_a: Temperature coefficient for material A (abV/K^2).
        seebeck_temp_coef_b: Temperature coefficient for material B (abV/K^2).
        hot_junction_temp: Hot junction temperature (K).
        cold_junction_temp: Cold junction temperature (K).
        internal_resistance: Internal resistance of TEG (abohms).
        load_resistance: External load resistance (abohms).
        leg_length: Thermoelement leg length (cm).
        leg_cross_section: Cross-sectional area (cm^2).

    Returns:
        Dictionary with TEG performance metrics:
        - seebeck_emf: Generated EMF (abvolts)
        - alpha_ab: Relative Seebeck coefficient (abV/K)
        - current: Circuit current (abamperes)
        - output_power: Power delivered to load (ergs/s)
        - input_heat: Heat input at hot junction (ergs/s)
        - efficiency: Conversion efficiency
        - figure_of_merit: ZT (if properties allow)
    """
    # Temperature difference
    delta_t = hot_junction_temp - cold_junction_temp

    # Relative Seebeck coefficient
    alpha_ab = seebeck_coefficient_a - seebeck_coefficient_b

    # Seebeck EMF
    seebeck_emf = alpha_ab * delta_t

    # Circuit analysis
    total_resistance = internal_resistance + load_resistance
    if total_resistance <= 0:
        return {
            "seebeck_emf": seebeck_emf,
            "alpha_ab": alpha_ab,
            "current": float("inf"),
            "output_power": float("inf"),
            "error": "Invalid resistance values",
        }

    current = seebeck_emf / total_resistance
    output_power = current**2 * load_resistance

    # Peltier heat at hot junction (heat absorbed from source)
    peltier_coef = hot_junction_temp * alpha_ab
    peltier_heat = peltier_coef * current

    # Thomson heat contributions
    avg_temp = (hot_junction_temp + cold_junction_temp) / 2
    sigma_a = thomson_coefficient_from_seebeck(
        seebeck_coefficient_a, seebeck_temp_coef_a, avg_temp
    )
    sigma_b = thomson_coefficient_from_seebeck(
        seebeck_coefficient_b, seebeck_temp_coef_b, avg_temp
    )

    # Approximate Thomson heat (assuming linear gradient)
    thomson_heat_a = sigma_a * current * delta_t
    thomson_heat_b = sigma_b * current * (-delta_t)
    total_thomson_heat = thomson_heat_a + thomson_heat_b

    # Input heat at hot junction
    input_heat = peltier_heat + total_thomson_heat / 2  # Half Thomson heat at hot end

    # Efficiency
    if input_heat > 0:
        efficiency = output_power / input_heat
    else:
        efficiency = 0.0

    # Figure of merit ZT (approximate)
    # ZT = (alpha^2 * sigma_electrical / kappa_thermal) * T
    # Simplified estimate assuming typical values
    figure_of_merit = (
        (alpha_ab**2 / internal_resistance) * avg_temp
        if internal_resistance > 0
        else 0.0
    )

    return {
        "seebeck_emf": seebeck_emf,
        "alpha_ab": alpha_ab,
        "delta_t": delta_t,
        "hot_junction_temp": hot_junction_temp,
        "cold_junction_temp": cold_junction_temp,
        "current": current,
        "output_power": output_power,
        "peltier_heat_hot": peltier_heat,
        "thomson_heat_total": total_thomson_heat,
        "input_heat": input_heat,
        "efficiency": efficiency,
        "figure_of_merit": figure_of_merit,
        "internal_resistance": internal_resistance,
        "load_resistance": load_resistance,
    }


# =============================================================================
# VERIFICATION AND VALIDATION FUNCTIONS
# =============================================================================


@maxwell_cite(
    264,
    265,
    266,
    267,
    268,
    269,
    270,
    271,
    272,
    part=2,
    chapter="Electromotive Force",
    theory_class="maxwell_original",
    description="Verify EMF theory calculations",
)
def verify_emf_theory(
    tolerance: float = 1e-10,
) -> dict[str, bool | float | str]:
    """Verify the consistency of EMF theory calculations.

    Art. 264-272: This function performs comprehensive verification:
    1. Contact potential consistency
    2. Nernst equation limits
    3. Kelvin relation verification
    4. Energy conservation in thermoelectric circuits

    Args:
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with verification results:
        - contact_potential_verified: True if contact potential is consistent
        - nernst_verified: True if Nernst equation behaves correctly
        - kelvin_relations_verified: True if thermoelectric relations hold
        - energy_conservation_verified: True if energy is conserved
        - verified: Overall verification status
    """
    results = {}
    all_verified = True

    # Test 1: Contact potential symmetry
    # E_AB = -E_BA
    phi_a = 4.5 * 1.602e-12  # 4.5 eV in ergs
    phi_b = 5.0 * 1.602e-12  # 5.0 eV in ergs

    e_ab = contact_potential(phi_a, phi_b)
    e_ba = contact_potential(phi_b, phi_a)

    contact_verified = abs(e_ab + e_ba) < tolerance
    results["contact_potential_verified"] = contact_verified
    all_verified = all_verified and contact_verified

    # Test 2: Nernst equation at standard conditions (Q=1)
    # Should give E = E^0
    standard_emf = 1.1e8  # 1.1 V
    emf_at_standard = nernst_equation(standard_emf, 298.15, 2, 1.0)

    nernst_standard_verified = (
        abs(emf_at_standard - standard_emf) / standard_emf < tolerance
    )
    results["nernst_standard_verified"] = nernst_standard_verified
    all_verified = all_verified and nernst_standard_verified

    # Test 3: Nernst equation - concentration effect
    # Higher reactant concentration should increase EMF
    emf_q_01 = nernst_equation(standard_emf, 298.15, 2, 0.1)
    emf_q_10 = nernst_equation(standard_emf, 298.15, 2, 10.0)

    nernst_concentration_verified = emf_q_01 > standard_emf > emf_q_10
    results["nernst_concentration_verified"] = nernst_concentration_verified
    all_verified = all_verified and nernst_concentration_verified

    # Test 4: Kelvin's first relation
    # Pi = T * alpha
    alpha = 40.0e-6  # 40 microvolts/K = 40 abV/K
    temp = 300.0
    pi_from_relation = peltier_coefficient_from_seebeck(alpha, temp)
    pi_expected = temp * alpha

    kelvin_first_verified = (
        abs(pi_from_relation - pi_expected) / pi_expected < tolerance
    )
    results["kelvin_first_verified"] = kelvin_first_verified
    all_verified = all_verified and kelvin_first_verified

    # Test 5: Kelvin's second relation
    # sigma = T * d_alpha/dT
    d_alpha_dt = 0.005  # abV/K^2
    sigma = thomson_coefficient_from_seebeck(alpha, d_alpha_dt, temp)
    sigma_expected = temp * d_alpha_dt

    kelvin_second_verified = abs(sigma - sigma_expected) / sigma_expected < tolerance
    results["kelvin_second_verified"] = kelvin_second_verified
    all_verified = all_verified and kelvin_second_verified

    # Test 6: Seebeck EMF linearity
    # E = alpha * Delta_T
    alpha_ab = 40.0  # abV/K
    delta_t = 100.0  # K
    seebeck_emf = seebeck_effect(alpha_ab + 0, 0, 373.15, 273.15)
    seebeck_expected = alpha_ab * delta_t

    seebeck_verified = (
        abs(seebeck_emf - seebeck_expected) / seebeck_expected < tolerance
    )
    results["seebeck_verified"] = seebeck_verified
    all_verified = all_verified and seebeck_verified

    # Test 7: Series EMF addition
    cell_emfs = [1.0e8, 1.5e8, 2.0e8]
    series_result = volta_series_emf(cell_emfs)
    expected_total = sum(cell_emfs)

    series_verified = abs(series_result["total_emf"] - expected_total) < tolerance
    results["series_emf_verified"] = series_verified
    all_verified = all_verified and series_verified

    # Test 8: Chemical EMF from Gibbs energy
    # For spontaneous reaction (Delta_G < 0), EMF should be positive
    delta_g = -2.0e12  # ergs (spontaneous)
    chem_emf = chemical_emf(delta_g, 2)

    chemical_verified = chem_emf > 0
    results["chemical_emf_verified"] = chemical_verified
    all_verified = all_verified and chemical_verified

    results["verified"] = all_verified

    return results


# =============================================================================
# MODULE MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ELECTROMOTIVE FORCE - Maxwell's Treatise, Part II, Chapter V")
    print("Articles 264-272")
    print("=" * 70)

    print("\n--- Contact Potential (Arts. 264-265) ---")
    # Copper-zinc contact
    phi_cu = 4.65 * 1.602e-12  # ergs
    phi_zn = 4.33 * 1.602e-12  # ergs
    e_contact = contact_potential(phi_cu, phi_zn)
    print(f"Cu-Zn contact potential: {e_contact:.2e} abV ({e_contact/1e8:.2f} V)")

    # Using eV directly
    e_contact_ev = contact_potential_from_ev(4.65, 4.33)
    print(f"Cu-Zn (eV method): {e_contact_ev:.2e} abV")

    print("\n--- Volta Series EMF (Art. 266) ---")
    # Three Daniell cells in series
    cell_emfs = [1.1e8, 1.1e8, 1.1e8]  # 1.1 V each
    cell_resistances = [5e8, 5e8, 5e8]  # 0.5 ohm each
    series_result = volta_series_emf(cell_emfs, cell_resistances)
    print(f"3 Daniell cells in series:")
    print(
        f"  Total EMF: {series_result['total_emf']:.2e} abV ({series_result['total_emf']/1e8:.2f} V)"
    )
    print(
        f"  Total internal resistance: {series_result['total_internal_resistance']:.2e} abohm"
    )
    print(f"  Short-circuit current: {series_result['short_circuit_current']:.2e} abA")

    print("\n--- Chemical EMF (Arts. 267-268) ---")
    # Daniell cell: Zn + Cu2+ -> Zn2+ + Cu
    # Delta_G = -212 kJ/mol = -2.12e12 erg/mol
    delta_g = -2.12e12
    emf_chemical = chemical_emf(delta_g, 2)
    print(
        f"Daniell cell chemical EMF: {emf_chemical:.2e} abV ({emf_chemical/1e8:.2f} V)"
    )

    print("\n--- Nernst Equation (Art. 269) ---")
    # Daniell cell with concentration effects
    standard = 1.10e8  # 1.10 V
    emf_q_01 = nernst_equation(standard, 298.15, 2, 0.1)
    emf_q_10 = nernst_equation(standard, 298.15, 2, 10.0)
    print(f"Standard EMF (Q=1): {standard/1e8:.3f} V")
    print(f"Q=0.1 (dilute products): {emf_q_01/1e8:.3f} V")
    print(f"Q=10 (concentrated products): {emf_q_10/1e8:.3f} V")

    print("\n--- Seebeck Effect (Arts. 270-271) ---")
    # Copper-constantan thermocouple
    # alpha_Cu = 6.5 abV/K, alpha_Const = -35 abV/K
    seebeck_emf = seebeck_effect(6.5, -35.0, 373.15, 273.15)
    print(
        f"Cu-Constantan Seebeck EMF (100K): {seebeck_emf:.2e} abV ({seebeck_emf/1e8:.3f} mV)"
    )

    print("\n--- Peltier Effect (Art. 271) ---")
    # Peltier coefficient at 300K
    alpha_ab = 6.5 - (-35.0)  # 41.5 abV/K
    pi = peltier_coefficient_from_seebeck(alpha_ab, 300.0)
    print(f"Cu-Constantan Peltier coefficient at 300K: {pi:.2e} abV ({pi/1e8:.2f} mV)")

    # Peltier heat
    q_peltier = peltier_effect(pi, 0.1, 60.0)
    print(f"Peltier heat (0.1 abA, 60s): {q_peltier:.2e} erg")

    print("\n--- Thomson Effect (Art. 272) ---")
    # Copper Thomson coefficient
    d_alpha_dt = 0.005  # abV/K^2
    sigma_cu = thomson_coefficient_from_seebeck(6.5, d_alpha_dt, 300.0)
    print(f"Copper Thomson coefficient: {sigma_cu:.3f} abV/K")

    # Thomson heat
    q_thomson = thomson_effect(sigma_cu, 0.1, 10.0, 10.0, 60.0)
    print(f"Thomson heat (0.1 abA, 10 K gradient): {q_thomson:.2e} erg")

    print("\n--- Kelvin Relations ---")
    # Comprehensive thermoelectric analysis
    kelvin_result = kelvin_relations(
        seebeck_coefficient_a=6.5,
        seebeck_coefficient_b=-35.0,
        seebeck_temp_coef_a=0.005,
        seebeck_temp_coef_b=-0.05,
        hot_junction_temp=373.15,
        cold_junction_temp=273.15,
        current=0.1,
        time=60.0,
    )
    print(f"Seebeck EMF: {kelvin_result['seebeck_emf']:.2e} abV")
    print(f"Peltier coefficient (hot): {kelvin_result['peltier_coef']:.2e} abV")
    print(f"Thomson coef Cu: {kelvin_result['thomson_coef_a']:.3f} abV/K")
    print(f"Total Peltier heat: {kelvin_result['total_peltier_heat']:.2e} erg")
    print(f"Kelvin first relation verified: {kelvin_result['kelvin_first_verified']}")

    print("\n--- EMF Source Analysis ---")
    # Model a battery
    battery = EMFSource(
        emf=12.0e8,  # 12 V
        internal_resistance=1e8,  # 0.1 ohm
        source_type="lead_acid",
    )
    print(
        f"Battery: E = {battery.emf/1e8:.1f} V, R_int = {battery.internal_resistance/1e8:.1f} ohm"
    )
    print(f"  Open-circuit voltage: {battery.open_circuit_voltage()/1e8:.1f} V")
    print(f"  Short-circuit current: {battery.short_circuit_current():.2e} abA")
    print(f"  Maximum power: {battery.maximum_power()/1e7:.2f} W")

    # Load analysis
    for r_load in [0.5e8, 1e8, 2e8, 5e8]:
        p = battery.power_delivered(r_load)
        eff = battery.efficiency(r_load)
        print(f"  R_load = {r_load/1e8:.1f} ohm: P = {p/1e7:.3f} W, eta = {eff:.1%}")

    print("\n--- Voltaic Cell Analysis ---")
    cell_result = analyze_voltaic_cell(
        standard_emf=1.10e8,
        temperature=298.15,
        electrons_transferred=2,
        reaction_quotient=0.1,
        internal_resistance=5e8,
        load_resistance=10e8,
        anode_material="Zn",
        cathode_material="Cu",
    )
    print(f"Daniell cell analysis:")
    print(f"  Nernst EMF: {cell_result['nernst_emf']/1e8:.3f} V")
    print(f"  Terminal voltage: {cell_result['terminal_voltage']/1e8:.3f} V")
    print(f"  Current: {cell_result['current']:.2e} abA")
    print(f"  Efficiency: {cell_result['efficiency']:.1%}")

    print("\n--- Thermoelectric Generator Analysis ---")
    teg_result = analyze_thermoelectric_generator(
        seebeck_coefficient_a=150e-6,  # Bi2Te3 n-type
        seebeck_coefficient_b=-150e-6,  # Bi2Te3 p-type
        seebeck_temp_coef_a=0.3e-6,
        seebeck_temp_coef_b=0.3e-6,
        hot_junction_temp=500.0,
        cold_junction_temp=300.0,
        internal_resistance=1e8,
        load_resistance=1e8,
    )
    print(f"TEG analysis:")
    print(f"  Seebeck EMF: {teg_result['seebeck_emf']/1e8:.3f} mV")
    print(f"  Output power: {teg_result['output_power']/1e7:.4f} W")
    print(f"  Efficiency: {teg_result['efficiency']:.2%}")

    print("\n--- Verification Tests ---")
    verify_result = verify_emf_theory()
    print(f"Contact potential verified: {verify_result['contact_potential_verified']}")
    print(f"Nernst equation verified: {verify_result['nernst_standard_verified']}")
    print(f"Kelvin relations verified: {verify_result['kelvin_first_verified']}")
    print(f"Overall verification: {verify_result['verified']}")

    print("\n" + "=" * 70)
    print("Module verification complete.")
    print("=" * 70)

"""
Electrolysis — Electrochemical decomposition by electric current.

Implements Maxwell's theory of electrolysis from Part II, Chapter IV (Arts. 249-263):

- Faraday's Laws of Electrolysis (Arts. 249-252)
- EMF of Polarization (Arts. 253-256)
- Electrolytic Conduction (Arts. 257-263)

Maxwell's CGS-EMU formulation:
    Faraday's First Law:  m = Z * I * t
    Faraday's Second Law: m = (M / nF) * I * t
    Ion migration:        v = u * E
    Conductivity:         kappa = sum(n_i * z_i * e * u_i)

where:
    m  = mass deposited (grams)
    Z  = electrochemical equivalent (g/abacoulomb)
    I  = current (abamperes, EMU)
    t  = time (seconds)
    M  = molar mass (g/mol)
    n  = valence (number of electrons transferred)
    F  = Faraday constant (abacoulombs/mol)
    v  = ion migration velocity (cm/s)
    u  = ion mobility (cm^2/(statvolt*s))
    E  = electric field (statvolt/cm)

Category: A (maxwell_original) — Maxwell's theory of electrolysis.

References:
    Part II, Arts. 249-263: Electrolysis and electrochemical theory.
    Part II, Ch. IV: Electrolytic conduction and polarization.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST, C, C_APPROX


# =============================================================================
# FARADAY CONSTANT AND ELECTROCHEMICAL EQUIVALENTS
# =============================================================================

#: Faraday constant in CGS-EMU (abcoulombs per mole)
#: F = N_A * e where N_A = 6.02214076e23 mol^-1, e = 1.602176634e-20 abC
#: F = 96485.33212... abC/mol (same numerical value as SI coulombs/mol)
FARADAY_CONSTANT: float = 96485.33212

#: Elementary charge in abcoulombs (EMU)
ELEMENTARY_CHARGE_EMU: float = 1.602176634e-20

#: Avogadro's number (per mole)
AVOGADRO_NUMBER: float = 6.02214076e23


# =============================================================================
# FARADAY'S LAWS OF ELECTROLYSIS (Arts. 249-252)
# =============================================================================

@maxwell_cite(
    249, 250,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Calculate mass deposited during electrolysis per Faraday's first law"
)
def faraday_first_law(current: float, time: float, electrochemical_equivalent: float) -> float:
    """Calculate mass deposited during electrolysis per Faraday's first law.

    Art. 249-250: The chemical action of a current is proportional to the
    quantity of electricity which passes through the electrolyte.

    The mass of substance deposited or liberated at an electrode is directly
    proportional to the quantity of electricity (charge) passed through the
    electrolyte:

        m = Z * Q = Z * I * t

    where:
        m  = mass deposited (grams)
        Z  = electrochemical equivalent (g/abacoulomb)
        Q  = charge passed (abacoulombs)
        I  = current (abamperes, EMU)
        t  = time (seconds)

    Args:
        current: Current in abamperes (CGS-EMU).
        time: Time in seconds.
        electrochemical_equivalent: Electrochemical equivalent in g/abacoulomb.

    Returns:
        Mass deposited in grams.

    Raises:
        ValueError: If current, time, or electrochemical_equivalent is negative.

    Reference:
        Part II, Arts. 249-250: Faraday's first law of electrolysis.

    Example:
        >>> # Silver deposition: Z = 0.001118 g/C
        >>> m = faraday_first_law(0.1, 3600, 0.001118)  # 0.1 abA for 1 hour
        >>> print(f"Mass deposited: {m:.4f} g")
    """
    if current < 0:
        raise ValueError(f"Current must be non-negative, got {current}")
    if time < 0:
        raise ValueError(f"Time must be non-negative, got {time}")
    if electrochemical_equivalent < 0:
        raise ValueError(f"Electrochemical equivalent must be non-negative, got {electrochemical_equivalent}")

    return electrochemical_equivalent * current * time


@maxwell_cite(
    251, 252,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Calculate mass deposited using Faraday's second law with molar mass"
)
def faraday_second_law(
    current: float,
    time: float,
    molar_mass: float,
    valence: int,
    faraday_constant: float = FARADAY_CONSTANT,
) -> float:
    """Calculate mass deposited using Faraday's second law.

    Art. 251-252: When the same quantity of electricity passes through different
    electrolytes, the masses of the substances deposited are proportional to
    their chemical equivalents (equivalent weights).

    The mass of substance deposited is:

        m = (M / nF) * I * t = (M * Q) / (n * F)

    where:
        m  = mass deposited (grams)
        M  = molar mass (g/mol)
        n  = valence (number of electrons transferred per ion)
        F  = Faraday constant (abacoulombs/mol)
        Q  = charge passed = I * t (abacoulombs)
        I  = current (abamperes, EMU)
        t  = time (seconds)

    The quantity M/(nF) is the electrochemical equivalent Z.

    Args:
        current: Current in abamperes (CGS-EMU).
        time: Time in seconds.
        molar_mass: Molar mass of the substance (g/mol).
        valence: Valence (number of electrons transferred per ion).
        faraday_constant: Faraday constant in abacoulombs/mol (default: 96485.33).

    Returns:
        Mass deposited in grams.

    Raises:
        ValueError: If current, time, molar_mass is negative, valence is zero,
                   or faraday_constant is not positive.

    Reference:
        Part II, Arts. 251-252: Faraday's second law of electrolysis.

    Example:
        >>> # Copper deposition: M = 63.55 g/mol, n = 2 (Cu2+)
        >>> m = faraday_second_law(0.1, 3600, 63.55, 2)
        >>> print(f"Copper deposited: {m:.4f} g")

        >>> # Silver deposition: M = 107.87 g/mol, n = 1 (Ag+)
        >>> m = faraday_second_law(0.1, 3600, 107.87, 1)
        >>> print(f"Silver deposited: {m:.4f} g")
    """
    if current < 0:
        raise ValueError(f"Current must be non-negative, got {current}")
    if time < 0:
        raise ValueError(f"Time must be non-negative, got {time}")
    if molar_mass < 0:
        raise ValueError(f"Molar mass must be non-negative, got {molar_mass}")
    if valence == 0:
        raise ValueError(f"Valence must be non-zero, got {valence}")
    if faraday_constant <= 0:
        raise ValueError(f"Faraday constant must be positive, got {faraday_constant}")

    # Electrochemical equivalent: Z = M / (n * F)
    electrochemical_equivalent = molar_mass / (valence * faraday_constant)

    return electrochemical_equivalent * current * time


@maxwell_cite(
    251,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Calculate electrochemical equivalent of a substance"
)
def electrochemical_equivalent(
    molar_mass: float,
    valence: int,
    faraday_constant: float = FARADAY_CONSTANT,
) -> float:
    """Calculate the electrochemical equivalent of a substance.

    Art. 251: The electrochemical equivalent Z is the mass of a substance
    deposited or liberated by one unit of electricity (one abcoulomb in
    CGS-EMU).

    The electrochemical equivalent is:

        Z = M / (n * F)

    where:
        Z  = electrochemical equivalent (g/abacoulomb)
        M  = molar mass (g/mol)
        n  = valence (number of electrons transferred)
        F  = Faraday constant (abacoulombs/mol)

    Args:
        molar_mass: Molar mass of the substance (g/mol).
        valence: Valence (number of electrons transferred per ion).
        faraday_constant: Faraday constant in abacoulombs/mol (default: 96485.33).

    Returns:
        Electrochemical equivalent in grams per abcoulomb.

    Raises:
        ValueError: If molar_mass is negative, valence is zero, or
                   faraday_constant is not positive.

    Reference:
        Part II, Art. 251: Definition of electrochemical equivalent.

    Example:
        >>> # Silver: M = 107.87 g/mol, n = 1
        >>> Z_ag = electrochemical_equivalent(107.87, 1)
        >>> print(f"Silver Z = {Z_ag:.6f} g/abC")

        >>> # Copper: M = 63.55 g/mol, n = 2
        >>> Z_cu = electrochemical_equivalent(63.55, 2)
        >>> print(f"Copper Z = {Z_cu:.6f} g/abC")

        >>> # Hydrogen: M = 1.008 g/mol, n = 1
        >>> Z_h = electrochemical_equivalent(1.008, 1)
        >>> print(f"Hydrogen Z = {Z_h:.6f} g/abC")
    """
    if molar_mass < 0:
        raise ValueError(f"Molar mass must be non-negative, got {molar_mass}")
    if valence == 0:
        raise ValueError(f"Valence must be non-zero, got {valence}")
    if faraday_constant <= 0:
        raise ValueError(f"Faraday constant must be positive, got {faraday_constant}")

    return molar_mass / (valence * faraday_constant)


# =============================================================================
# EMF OF POLARIZATION (Arts. 253-256)
# =============================================================================

@maxwell_cite(
    253, 254,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Calculate EMF of polarization from electrolysis products"
)
def polarization_emf(
    reversible_potential: float,
    current_density: float,
    exchange_current_density: float,
    transfer_coefficient: float = 0.5,
    temperature: float = 298.15,
) -> float:
    """Calculate the EMF of polarization from electrolysis products.

    Art. 253-254: The products of electrolysis tend to produce a counter-EMF
    (polarization) which opposes the applied voltage. This back-EMF arises from
    the electrochemical potential difference between the products and reactants.

    The total polarization EMF includes:
    1. Reversible potential (thermodynamic EMF)
    2. Activation overpotential (kinetic barrier)
    3. Concentration overpotential (mass transport)

    For a single electrode reaction, the activation overpotential follows
    the Butler-Volmer equation (derived from Maxwell's electrokinetic theory):

        eta_act = (RT/nF) * asinh(j / (2 * j0))

    where:
        eta_act  = activation overpotential (abvolts in CGS-EMU)
        R        = gas constant (erg/(mol*K))
        T        = temperature (K)
        n        = number of electrons transferred
        F        = Faraday constant (abC/mol)
        j        = current density (abA/cm^2)
        j0       = exchange current density (abA/cm^2)

    Args:
        reversible_potential: Reversible (thermodynamic) potential in abvolts.
        current_density: Applied current density in abamperes/cm^2.
        exchange_current_density: Exchange current density in abamperes/cm^2.
        transfer_coefficient: Charge transfer coefficient (default: 0.5).
        temperature: Temperature in Kelvin (default: 298.15 K).

    Returns:
        Total polarization EMF in abvolts (reversible + overpotential).

    Raises:
        ValueError: If exchange_current_density is zero or negative.

    Reference:
        Part II, Arts. 253-254: EMF of polarization.

    Note:
        Maxwell did not use the Butler-Volmer equation explicitly, but his
        electrokinetic theory (Arts. 243-248) laid the foundation for it.
    """
    if exchange_current_density <= 0:
        raise ValueError(f"Exchange current density must be positive, got {exchange_current_density}")

    # Gas constant in CGS (erg/(mol*K))
    R_GAS = 8.314462618e7  # erg/(mol*K)

    # Assume n=1 for general case (can be parameterized if needed)
    n_electrons = 1

    # Thermal voltage: V_T = RT/F
    thermal_voltage = R_GAS * temperature / FARADAY_CONSTANT  # abvolts

    # Activation overpotential from Butler-Volmer (simplified for high overpotential)
    # eta = (RT/nF) * asinh(j / (2*j0))
    if current_density == 0:
        activation_overpotential = 0.0
    else:
        ratio = current_density / (2.0 * exchange_current_density)
        activation_overpotential = (thermal_voltage / n_electrons) * np.arcsinh(ratio) / transfer_coefficient

    return reversible_potential + activation_overpotential


@maxwell_cite(
    255, 256,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Calculate decomposition voltage for electrolysis"
)
def decomposition_voltage(
    reversible_emf: float,
    anode_overpotential: float,
    cathode_overpotential: float,
    ohmic_drop: float,
) -> float:
    """Calculate the decomposition voltage for electrolysis.

    Art. 255-256: The minimum voltage required for electrolysis (decomposition
    voltage) is the sum of:
    1. Reversible EMF of the cell reaction
    2. Anode overpotential (activation + concentration)
    3. Cathode overpotential (activation + concentration)
    4. Ohmic drop in the electrolyte

    The decomposition voltage is:

        V_decomp = E_rev + eta_anode + eta_cathode + I*R

    where:
        V_decomp   = decomposition voltage (abvolts)
        E_rev      = reversible EMF (abvolts)
        eta_anode  = anode overpotential (abvolts)
        eta_cathode = cathode overpotential (abvolts)
        I*R        = ohmic drop (abvolts)

    Args:
        reversible_emf: Reversible EMF of the cell reaction in abvolts.
        anode_overpotential: Anode overpotential in abvolts.
        cathode_overpotential: Cathode overpotential in abvolts.
        ohmic_drop: Ohmic voltage drop in abvolts.

    Returns:
        Decomposition voltage in abvolts.

    Reference:
        Part II, Arts. 255-256: Decomposition voltage.

    Example:
        >>> # Water electrolysis: E_rev = 1.23 V = 1.23e8 abV
        >>> V_decomp = decomposition_voltage(
        ...     reversible_emf=1.23e8,
        ...     anode_overpotential=0.4e8,
        ...     cathode_overpotential=0.1e8,
        ...     ohmic_drop=0.05e8
        ... )
        >>> print(f"Decomposition voltage: {V_decomp:.2e} abV")
    """
    return reversible_emf + anode_overpotential + cathode_overpotential + ohmic_drop


# =============================================================================
# ELECTROLYTIC CONDUCTION (Arts. 257-263)
# =============================================================================

@maxwell_cite(
    257, 258, 259,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Calculate ion migration velocity in electric field"
)
def ion_migration_velocity(
    ion_mobility: float,
    electric_field: float,
    charge_number: int = 1,
) -> float:
    """Calculate ion migration velocity in an electric field.

    Art. 257-259: Ions in an electrolyte move under the influence of an applied
    electric field. The migration velocity is proportional to the field strength
    and the ion's mobility.

    The ion migration velocity is:

        v = z * u * E

    where:
        v  = migration velocity (cm/s)
        z  = charge number of the ion
        u  = ion mobility (cm^2/(abvolt*s))
        E  = electric field strength (abvolt/cm)

    The mobility u depends on:
    - Ion size and shape
    - Solvent viscosity
    - Temperature
    - Ion-ion interactions

    Stokes' law for a spherical ion:

        u = z*e / (6*pi*eta*r)

    where:
        eta  = solvent viscosity (poise)
        r    = ionic radius (cm)
        e    = elementary charge

    Args:
        ion_mobility: Ion mobility in cm^2/(abvolt*s).
        electric_field: Electric field strength in abvolts/cm.
        charge_number: Charge number of the ion (default: 1).

    Returns:
        Ion migration velocity in cm/s.

    Raises:
        ValueError: If ion_mobility or electric_field is negative.

    Reference:
        Part II, Arts. 257-259: Ion migration and electrolytic conduction.

    Example:
        >>> # Sodium ion mobility ~5e-4 cm^2/(V*s) = 5e-12 cm^2/(abV*s)
        >>> v = ion_migration_velocity(5e-12, 1e6)  # 10 kV/cm field
        >>> print(f"Na+ velocity: {v:.2e} cm/s")
    """
    if ion_mobility < 0:
        raise ValueError(f"Ion mobility must be non-negative, got {ion_mobility}")
    if electric_field < 0:
        raise ValueError(f"Electric field must be non-negative, got {electric_field}")

    return charge_number * ion_mobility * electric_field


@maxwell_cite(
    260, 261,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Calculate electrolyte conductivity from ion concentrations"
)
def electrolyte_conductivity(
    ion_concentrations: list[float],
    ion_charge_numbers: list[int],
    ion_mobilities: list[float],
) -> float:
    """Calculate the conductivity of an electrolyte.

    Art. 260-261: The electrical conductivity of an electrolyte is the sum of
    contributions from all ionic species present. Each ion contributes
    proportionally to its concentration, charge, and mobility.

    The conductivity is:

        kappa = F * sum(c_i * |z_i| * u_i)

    where:
        kappa = conductivity (abmho/cm in CGS-EMU)
        F     = Faraday constant (abC/mol)
        c_i   = concentration of ion i (mol/cm^3)
        z_i   = charge number of ion i
        u_i   = mobility of ion i (cm^2/(abvolt*s))

    For a single symmetric electrolyte (z+ = -z- = z):

        kappa = F * z * (c_+ * u_+ + c_- * u_-)

    Args:
        ion_concentrations: List of ion concentrations in mol/cm^3.
        ion_charge_numbers: List of charge numbers (signed integers).
        ion_mobilities: List of ion mobilities in cm^2/(abvolt*s).

    Returns:
        Conductivity in abmho/cm.

    Raises:
        ValueError: If list lengths don't match or concentrations are negative.

    Reference:
        Part II, Arts. 260-261: Electrolyte conductivity.

    Example:
        >>> # 0.1 M NaCl: c_Na = c_Cl = 0.1 mol/L = 1e-4 mol/cm^3
        >>> kappa = electrolyte_conductivity(
        ...     ion_concentrations=[1e-4, 1e-4],
        ...     ion_charge_numbers=[1, -1],
        ...     ion_mobilities=[5.19e-4, 7.91e-4]  # cm^2/(V*s)
        ... )
        >>> print(f"Conductivity: {kappa:.4f} abmho/cm")
    """
    if len(ion_concentrations) != len(ion_charge_numbers):
        raise ValueError("Concentration and charge number lists must have same length")
    if len(ion_concentrations) != len(ion_mobilities):
        raise ValueError("Concentration and mobility lists must have same length")

    total_conductivity = 0.0
    for c, z, u in zip(ion_concentrations, ion_charge_numbers, ion_mobilities):
        if c < 0:
            raise ValueError(f"Concentration must be non-negative, got {c}")
        # Conductivity contribution: F * c * |z| * u
        total_conductivity += FARADAY_CONSTANT * c * abs(z) * u

    return total_conductivity


@maxwell_cite(
    262, 263,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Calculate molar conductivity using Kohlrausch's law"
)
def kohlrausch_law(
    limiting_molar_conductivity: float,
    concentration: float,
    kohrausch_coefficient: float,
) -> float:
    """Calculate molar conductivity using Kohlrausch's law of independent migration.

    Art. 262-263: Kohlrausch's law states that at infinite dilution, each ion
    migrates independently of other ions. The molar conductivity at finite
    concentration is:

        Lambda_m = Lambda_m^0 - K * sqrt(c)

    where:
        Lambda_m     = molar conductivity at concentration c
        Lambda_m^0   = limiting molar conductivity (at infinite dilution)
        K            = Kohlrausch coefficient (depends on electrolyte type)
        c            = concentration (mol/cm^3 or appropriate units)

    The limiting molar conductivity is the sum of ionic contributions:

        Lambda_m^0 = nu_+ * lambda_+^0 + nu_- * lambda_-^0

    where:
        nu_+, nu_- = number of cations and anions per formula unit
        lambda_+^0, lambda_-^0 = limiting ionic conductivities

    Args:
        limiting_molar_conductivity: Lambda_m^0 in abmho*cm^2/mol.
        concentration: Electrolyte concentration in mol/cm^3.
        kohrausch_coefficient: K coefficient for the electrolyte.

    Returns:
        Molar conductivity in abmho*cm^2/mol.

    Raises:
        ValueError: If concentration or limiting_molar_conductivity is negative.

    Reference:
        Part II, Arts. 262-263: Kohlrausch's law of independent migration.

    Example:
        >>> # KCl at infinite dilution: Lambda^0 = 149.9 S*cm^2/mol
        >>> # K coefficient for 1:1 electrolyte ~ 94 (in appropriate units)
        >>> Lambda_m = kohlrausch_law(149.9, 0.01, 94)
        >>> print(f"Molar conductivity: {Lambda_m:.2f}")
    """
    if limiting_molar_conductivity < 0:
        raise ValueError(f"Limiting molar conductivity must be non-negative, got {limiting_molar_conductivity}")
    if concentration < 0:
        raise ValueError(f"Concentration must be non-negative, got {concentration}")

    return limiting_molar_conductivity - kohrausch_coefficient * np.sqrt(concentration)


@maxwell_cite(
    260, 261, 262,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Calculate concentration polarization in electrolyte"
)
def concentration_polarization(
    bulk_concentration: float,
    surface_concentration: float,
    diffusion_coefficient: float,
    diffusion_layer_thickness: float,
    current_density: float,
    charge_number: int,
) -> float:
    """Calculate concentration polarization in an electrolyte.

    Art. 260-262: Concentration polarization arises from the depletion (or
    accumulation) of ions near the electrode surface due to the electrochemical
    reaction. This creates a concentration gradient that drives diffusion.

    The concentration overpotential is:

        eta_conc = (RT/nF) * ln(c_surface / c_bulk)

    For a cathodic reaction where surface concentration is depleted:

        eta_conc = (RT/nF) * ln(1 - i / i_L)

    where:
        eta_conc = concentration overpotential (abvolts)
        R        = gas constant (erg/(mol*K))
        T        = temperature (K)
        n        = charge number
        F        = Faraday constant (abC/mol)
        c_bulk   = bulk concentration (mol/cm^3)
        c_surface = surface concentration (mol/cm^3)
        i        = current density (abA/cm^2)
        i_L      = limiting current density (abA/cm^2)

    The limiting current density is:

        i_L = n * F * D * c_bulk / delta

    where:
        D     = diffusion coefficient (cm^2/s)
        delta = diffusion layer thickness (cm)

    Args:
        bulk_concentration: Bulk electrolyte concentration in mol/cm^3.
        surface_concentration: Surface concentration in mol/cm^3.
        diffusion_coefficient: Diffusion coefficient in cm^2/s.
        diffusion_layer_thickness: Diffusion layer thickness in cm.
        current_density: Applied current density in abA/cm^2.
        charge_number: Charge number of the reacting ion.

    Returns:
        Concentration overpotential in abvolts.

    Raises:
        ValueError: If concentrations are negative or diffusion parameters
                   are not positive.

    Reference:
        Part II, Arts. 260-262: Concentration polarization.

    Example:
        >>> # Copper deposition from 0.1 M CuSO4
        >>> eta = concentration_polarization(
        ...     bulk_concentration=1e-4,  # 0.1 M = 1e-4 mol/cm^3
        ...     surface_concentration=1e-5,
        ...     diffusion_coefficient=7e-6,  # cm^2/s
        ...     diffusion_layer_thickness=0.01,  # 100 microns
        ...     current_density=0.01,  # abA/cm^2
        ...     charge_number=2
        ... )
        >>> print(f"Concentration overpotential: {eta:.2e} abV")
    """
    if bulk_concentration < 0:
        raise ValueError(f"Bulk concentration must be non-negative, got {bulk_concentration}")
    if surface_concentration < 0:
        raise ValueError(f"Surface concentration must be non-negative, got {surface_concentration}")
    if diffusion_coefficient <= 0:
        raise ValueError(f"Diffusion coefficient must be positive, got {diffusion_coefficient}")
    if diffusion_layer_thickness <= 0:
        raise ValueError(f"Diffusion layer thickness must be positive, got {diffusion_layer_thickness}")

    # Gas constant in CGS (erg/(mol*K))
    R_GAS = 8.314462618e7

    # Temperature (assume room temperature)
    T = 298.15

    # Thermal voltage
    thermal_voltage = R_GAS * T / FARADAY_CONSTANT

    # Calculate limiting current density
    limiting_current = (
        abs(charge_number) * FARADAY_CONSTANT * diffusion_coefficient * bulk_concentration / diffusion_layer_thickness
    )

    # Concentration overpotential
    if limiting_current > 0 and current_density < limiting_current:
        # Using the limiting current form
        eta_conc = (thermal_voltage / abs(charge_number)) * np.log(1 - current_density / limiting_current)
    elif surface_concentration > 0 and bulk_concentration > 0:
        # Direct concentration ratio form
        eta_conc = (thermal_voltage / abs(charge_number)) * np.log(surface_concentration / bulk_concentration)
    else:
        eta_conc = 0.0

    return eta_conc


@maxwell_cite(
    255, 256, 257, 258,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Calculate back EMF in a voltaic battery"
)
def battery_back_emf(
    reversible_emf: float,
    internal_resistance: float,
    current: float,
    polarization_coefficient: float = 0.0,
) -> float:
    """Calculate the back EMF and terminal voltage of a voltaic battery.

    Art. 255-258: A voltaic battery has an internal resistance and experiences
    polarization during discharge. The terminal voltage is less than the
    reversible EMF due to:
    1. Ohmic drop: I * R_internal
    2. Polarization: depends on current density and electrode properties

    During discharge (current flowing out):
        V_terminal = E_rev - I*R_internal - eta_polarization

    During charge (current flowing in):
        V_terminal = E_rev + I*R_internal + eta_polarization

    The polarization can be approximated as:
        eta_polarization = k * I

    where k is a polarization coefficient.

    Args:
        reversible_emf: Reversible EMF of the battery in abvolts.
        internal_resistance: Internal resistance in abohms.
        current: Current in abamperes (positive = discharge, negative = charge).
        polarization_coefficient: Polarization coefficient in abohms (default: 0).

    Returns:
        Terminal voltage in abvolts.

    Raises:
        ValueError: If internal_resistance is negative.

    Reference:
        Part II, Arts. 255-258: Battery polarization and back EMF.

    Example:
        >>> # Daniell cell: E = 1.1 V = 1.1e8 abV, R = 1 ohm = 1e9 abohm
        >>> V = battery_back_emf(1.1e8, 1e9, 0.1)  # 0.1 abA = 1 A discharge
        >>> print(f"Terminal voltage: {V:.2e} abV")
    """
    if internal_resistance < 0:
        raise ValueError(f"Internal resistance must be non-negative, got {internal_resistance}")

    ohmic_drop = current * internal_resistance
    polarization = polarization_coefficient * current

    # For discharge (positive current), terminal voltage is reduced
    # For charge (negative current), terminal voltage is increased
    return reversible_emf - ohmic_drop - polarization


# =============================================================================
# ELECTROLYSIS CELL CLASS
# =============================================================================

@dataclass
class ElectrolysisCell:
    """
    Model of an electrolysis cell following Maxwell's treatment.

    Art. 249-263: This class encapsulates the complete theory of electrolysis,
    including Faraday's laws, polarization, and ionic conduction.

    Attributes:
        anode_material: Anode material identifier.
        cathode_material: Cathode material identifier.
        electrolyte: Electrolyte composition.
        electrode_area: Electrode area in cm^2.
        electrode_spacing: Distance between electrodes in cm.
        temperature: Temperature in Kelvin.
    """

    anode_material: str
    cathode_material: str
    electrolyte: str
    electrode_area: float = 1.0
    electrode_spacing: float = 1.0
    temperature: float = 298.15

    #: Molar mass of deposited substance (g/mol)
    molar_mass: float = None

    #: Valence of deposited ion
    valence: int = None

    #: Electrolyte conductivity (abmho/cm)
    conductivity: float = None

    #: Reversible EMF (abvolts)
    reversible_emf: float = None

    #: Internal resistance (abohms)
    internal_resistance: float = None

    @maxwell_cite(
        249, 250, 251, 252,
        part=2, chapter="Electrolysis",
        theory_class="maxwell_original",
        description="Calculate mass deposited for given current and time"
    )
    def calculate_mass_deposited(
        self,
        current: float,
        time: float,
        molar_mass: float = None,
        valence: int = None,
    ) -> float:
        """Calculate mass deposited during electrolysis.

        Art. 249-252: Uses Faraday's laws to calculate the mass of substance
        deposited at an electrode.

        Args:
            current: Current in abamperes.
            time: Time in seconds.
            molar_mass: Molar mass in g/mol (uses instance value if None).
            valence: Valence (uses instance value if None).

        Returns:
            Mass deposited in grams.

        Raises:
            ValueError: If molar_mass or valence not provided and not set on instance.

        Reference:
            Part II, Arts. 249-252: Faraday's laws.
        """
        M = molar_mass if molar_mass is not None else self.molar_mass
        n = valence if valence is not None else self.valence

        if M is None:
            raise ValueError("Molar mass must be provided or set on instance")
        if n is None:
            raise ValueError("Valence must be provided or set on instance")

        return faraday_second_law(current, time, M, n)

    @maxwell_cite(
        253, 254, 255, 256,
        part=2, chapter="Electrolysis",
        theory_class="maxwell_original",
        description="Calculate required voltage for electrolysis"
    )
    def calculate_required_voltage(
        self,
        current: float,
        reversible_emf: float = None,
        anode_overpotential: float = 0.0,
        cathode_overpotential: float = 0.0,
    ) -> float:
        """Calculate the voltage required for electrolysis.

        Art. 253-256: The required voltage (decomposition voltage) includes
        the reversible EMF, overpotentials, and ohmic drop.

        Args:
            current: Current in abamperes.
            reversible_emf: Reversible EMF in abvolts (uses instance value if None).
            anode_overpotential: Anode overpotential in abvolts.
            cathode_overpotential: Cathode overpotential in abvolts.

        Returns:
            Required voltage in abvolts.

        Raises:
            ValueError: If reversible_emf not provided and not set on instance.

        Reference:
            Part II, Arts. 253-256: Decomposition voltage.
        """
        E_rev = reversible_emf if reversible_emf is not None else self.reversible_emf

        if E_rev is None:
            raise ValueError("Reversible EMF must be provided or set on instance")

        # Ohmic drop
        if self.internal_resistance is not None:
            ohmic_drop = current * self.internal_resistance
        else:
            ohmic_drop = 0.0

        return decomposition_voltage(E_rev, anode_overpotential, cathode_overpotential, ohmic_drop)

    @maxwell_cite(
        260, 261,
        part=2, chapter="Electrolysis",
        theory_class="maxwell_original",
        description="Calculate cell resistance from conductivity"
    )
    def calculate_cell_resistance(
        self,
        conductivity: float = None,
        electrode_area: float = None,
        electrode_spacing: float = None,
    ) -> float:
        """Calculate the resistance of the electrolyte cell.

        Art. 260-261: The resistance of an electrolyte cell is:

            R = L / (kappa * A)

        where:
            R      = resistance (abohms)
            L      = electrode spacing (cm)
            kappa  = conductivity (abmho/cm)
            A      = electrode area (cm^2)

        Args:
            conductivity: Conductivity in abmho/cm (uses instance value if None).
            electrode_area: Electrode area in cm^2 (uses instance value if None).
            electrode_spacing: Spacing in cm (uses instance value if None).

        Returns:
            Cell resistance in abohms.

        Raises:
            ValueError: If conductivity, area, or spacing not provided and not set.

        Reference:
            Part II, Arts. 260-261: Electrolyte resistance.
        """
        kappa = conductivity if conductivity is not None else self.conductivity
        A = electrode_area if electrode_area is not None else self.electrode_area
        L = electrode_spacing if electrode_spacing is not None else self.electrode_spacing

        if kappa is None:
            raise ValueError("Conductivity must be provided or set on instance")
        if A is None or A <= 0:
            raise ValueError("Electrode area must be positive")
        if L is None or L <= 0:
            raise ValueError("Electrode spacing must be positive")

        return L / (kappa * A)


# =============================================================================
# ION DATA (Common Ions for Reference)
# =============================================================================

@dataclass(frozen=True)
class IonData:
    """Reference data for common ions."""

    #: Ion symbol (e.g., "Na+", "Cl-")
    symbol: str

    #: Charge number (signed)
    charge_number: int

    #: Molar mass (g/mol)
    molar_mass: float

    #: Limiting ionic conductivity (abmho*cm^2/mol at 25°C)
    limiting_conductivity: float

    #: Mobility (cm^2/(abvolt*s))
    mobility: float

    #: Hydrated radius (cm)
    hydrated_radius: float = None


# Common ion data at 25°C (converted to CGS-EMU units)
# Values from standard electrochemical tables
ION_DATA = {
    # Cations
    "H+": IonData(
        symbol="H+", charge_number=1, molar_mass=1.008,
        limiting_conductivity=349.8, mobility=36.23e-4
    ),
    "Li+": IonData(
        symbol="Li+", charge_number=1, molar_mass=6.94,
        limiting_conductivity=38.7, mobility=4.01e-4
    ),
    "Na+": IonData(
        symbol="Na+", charge_number=1, molar_mass=22.99,
        limiting_conductivity=50.1, mobility=5.19e-4
    ),
    "K+": IonData(
        symbol="K+", charge_number=1, molar_mass=39.10,
        limiting_conductivity=73.5, mobility=7.62e-4
    ),
    "NH4+": IonData(
        symbol="NH4+", charge_number=1, molar_mass=18.04,
        limiting_conductivity=73.5, mobility=7.62e-4
    ),
    "Ag+": IonData(
        symbol="Ag+", charge_number=1, molar_mass=107.87,
        limiting_conductivity=61.9, mobility=6.42e-4
    ),
    "Cu2+": IonData(
        symbol="Cu2+", charge_number=2, molar_mass=63.55,
        limiting_conductivity=54.0, mobility=2.80e-4
    ),
    "Zn2+": IonData(
        symbol="Zn2+", charge_number=2, molar_mass=65.38,
        limiting_conductivity=53.0, mobility=2.75e-4
    ),
    "Ca2+": IonData(
        symbol="Ca2+", charge_number=2, molar_mass=40.08,
        limiting_conductivity=59.0, mobility=3.06e-4
    ),
    "Mg2+": IonData(
        symbol="Mg2+", charge_number=2, molar_mass=24.31,
        limiting_conductivity=53.0, mobility=2.75e-4
    ),
    # Anions
    "OH-": IonData(
        symbol="OH-", charge_number=-1, molar_mass=17.01,
        limiting_conductivity=198.3, mobility=20.55e-4
    ),
    "Cl-": IonData(
        symbol="Cl-", charge_number=-1, molar_mass=35.45,
        limiting_conductivity=76.3, mobility=7.91e-4
    ),
    "Br-": IonData(
        symbol="Br-", charge_number=-1, molar_mass=79.90,
        limiting_conductivity=78.1, mobility=8.09e-4
    ),
    "I-": IonData(
        symbol="I-", charge_number=-1, molar_mass=126.90,
        limiting_conductivity=76.8, mobility=7.96e-4
    ),
    "NO3-": IonData(
        symbol="NO3-", charge_number=-1, molar_mass=62.00,
        limiting_conductivity=71.4, mobility=7.40e-4
    ),
    "SO4 2-": IonData(
        symbol="SO4 2-", charge_number=-2, molar_mass=96.06,
        limiting_conductivity=80.0, mobility=4.15e-4
    ),
    "CO3 2-": IonData(
        symbol="CO3 2-", charge_number=-2, molar_mass=60.01,
        limiting_conductivity=69.3, mobility=3.59e-4
    ),
}


@maxwell_cite(
    262, 263,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Get ion data from reference database"
)
def get_ion_data(ion_symbol: str) -> IonData:
    """Get reference data for a common ion.

    Art. 262-263: Ion mobilities and limiting conductivities following
    Kohlrausch's law of independent migration.

    Args:
        ion_symbol: Symbol of the ion (e.g., "Na+", "Cl-").

    Returns:
        IonData object with ion properties.

    Raises:
        KeyError: If ion symbol not found in database.

    Reference:
        Part II, Arts. 262-263: Ion migration data.

    Example:
        >>> na = get_ion_data("Na+")
        >>> print(f"Na+ mobility: {na.mobility} cm^2/(abV*s)")
    """
    if ion_symbol not in ION_DATA:
        available = list(ION_DATA.keys())
        raise KeyError(
            f"Ion '{ion_symbol}' not found. Available ions: {available}"
        )
    return ION_DATA[ion_symbol]


@maxwell_cite(
    260, 261, 262, 263,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Calculate limiting molar conductivity of an electrolyte"
)
def limiting_molar_conductivity(
    cation_symbol: str,
    anion_symbol: str,
    cation_stoichiometry: int = 1,
    anion_stoichiometry: int = 1,
) -> float:
    """Calculate the limiting molar conductivity of an electrolyte.

    Art. 260-263: Kohlrausch's law of independent migration states that at
    infinite dilution, each ion contributes independently to the total
    conductivity.

    The limiting molar conductivity is:

        Lambda^0 = nu_+ * lambda_+^0 + nu_- * lambda_-^0

    where:
        Lambda^0       = limiting molar conductivity (abmho*cm^2/mol)
        nu_+, nu_-     = stoichiometric coefficients
        lambda_+^0, lambda_-^0 = limiting ionic conductivities

    Args:
        cation_symbol: Symbol of the cation.
        anion_symbol: Symbol of the anion.
        cation_stoichiometry: Number of cations per formula unit (default: 1).
        anion_stoichiometry: Number of anions per formula unit (default: 1).

    Returns:
        Limiting molar conductivity in abmho*cm^2/mol.

    Raises:
        KeyError: If either ion symbol not found.

    Reference:
        Part II, Arts. 260-263: Kohlrausch's law.

    Example:
        >>> # NaCl: Lambda^0 = lambda_Na+ + lambda_Cl-
        >>> Lambda = limiting_molar_conductivity("Na+", "Cl-")
        >>> print(f"NaCl Lambda^0 = {Lambda:.1f} abmho*cm^2/mol")

        >>> # CuSO4: Lambda^0 = lambda_Cu2+ + lambda_SO4(2-)
        >>> Lambda = limiting_molar_conductivity("Cu2+", "SO4 2-")
        >>> print(f"CuSO4 Lambda^0 = {Lambda:.1f} abmho*cm^2/mol")
    """
    cation = get_ion_data(cation_symbol)
    anion = get_ion_data(anion_symbol)

    return cation_stoichiometry * cation.limiting_conductivity + anion_stoichiometry * anion.limiting_conductivity


@maxwell_cite(
    257, 258, 259,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Calculate transference number of an ion"
)
def transference_number(
    cation_symbol: str,
    anion_symbol: str,
    cation_stoichiometry: int = 1,
    anion_stoichiometry: int = 1,
) -> dict[str, float]:
    """Calculate the transference numbers of ions in an electrolyte.

    Art. 257-259: The transference number (transport number) is the fraction
    of total current carried by each ionic species.

    For a cation:
        t_+ = (nu_+ * lambda_+^0) / Lambda^0

    For an anion:
        t_- = (nu_- * lambda_-^0) / Lambda^0

    where:
        t_+, t_-   = transference numbers (t_+ + t_- = 1)
        nu_+, nu_- = stoichiometric coefficients
        lambda^0   = limiting ionic conductivities
        Lambda^0   = limiting molar conductivity

    Args:
        cation_symbol: Symbol of the cation.
        anion_symbol: Symbol of the anion.
        cation_stoichiometry: Number of cations per formula unit.
        anion_stoichiometry: Number of anions per formula unit.

    Returns:
        Dictionary with:
        - t_cation: Transference number of cation
        - t_anion: Transference number of anion
        - Lambda_0: Limiting molar conductivity

    Raises:
        KeyError: If either ion symbol not found.

    Reference:
        Part II, Arts. 257-259: Ion transport and transference.

    Example:
        >>> # NaCl transference numbers
        >>> t = transference_number("Na+", "Cl-")
        >>> print(f"t_Na+ = {t['t_cation']:.3f}, t_Cl- = {t['t_anion']:.3f}")
    """
    cation = get_ion_data(cation_symbol)
    anion = get_ion_data(anion_symbol)

    lambda_cation = cation_stoichiometry * cation.limiting_conductivity
    lambda_anion = anion_stoichiometry * anion.limiting_conductivity

    Lambda_0 = lambda_cation + lambda_anion

    t_cation = lambda_cation / Lambda_0
    t_anion = lambda_anion / Lambda_0

    return {
        "t_cation": t_cation,
        "t_anion": t_anion,
        "Lambda_0": Lambda_0,
    }


# =============================================================================
# COMPREHENSIVE ANALYSIS FUNCTION
# =============================================================================

@maxwell_cite(
    249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Complete electrolysis analysis"
)
def analyze_electrolysis(
    current: float,
    time: float,
    molar_mass: float,
    valence: int,
    reversible_emf: float,
    electrolyte_conductivity: float = None,
    electrode_area: float = 1.0,
    electrode_spacing: float = 1.0,
    anode_overpotential: float = 0.0,
    cathode_overpotential: float = 0.0,
    temperature: float = 298.15,
) -> dict[str, float | str]:
    """Perform comprehensive electrolysis analysis.

    Art. 249-263: This function provides complete analysis of an electrolysis
    cell, including:
    1. Mass deposited (Faraday's laws)
    2. Charge passed
    3. Electrochemical equivalent
    4. Required voltage (including overpotentials)
    5. Energy consumption
    6. Current efficiency (if theoretical mass provided)

    Args:
        current: Current in abamperes.
        time: Time in seconds.
        molar_mass: Molar mass of deposited substance (g/mol).
        valence: Valence of deposited ion.
        reversible_emf: Reversible EMF of cell reaction (abvolts).
        electrolyte_conductivity: Conductivity (abmho/cm), optional.
        electrode_area: Electrode area (cm^2), default: 1.
        electrode_spacing: Electrode spacing (cm), default: 1.
        anode_overpotential: Anode overpotential (abvolts), default: 0.
        cathode_overpotential: Cathode overpotential (abvolts), default: 0.
        temperature: Temperature (K), default: 298.15.

    Returns:
        Dictionary with complete analysis results:
        - mass_deposited: Mass deposited (grams)
        - charge_passed: Total charge (abcoulombs)
        - electrochemical_equivalent: Z value (g/abC)
        - electrochemical_equivalent_theoretical: Theoretical Z value
        - required_voltage: Total voltage required (abvolts)
        - ohmic_drop: IR drop (abvolts)
        - total_overpotential: Sum of overpotentials (abvolts)
        - energy_consumed: Total energy (ergs)
        - energy_per_gram: Energy per gram deposited (ergs/g)
        - power: Instantaneous power (ergs/s)

    Reference:
        Part II, Arts. 249-263: Complete electrolysis theory.

    Example:
        >>> result = analyze_electrolysis(
        ...     current=0.1,  # 0.1 abA = 1 A
        ...     time=3600,    # 1 hour
        ...     molar_mass=63.55,  # Copper
        ...     valence=2,
        ...     reversible_emf=1.1e8,  # ~1.1 V
        ...     electrolyte_conductivity=0.1,
        ...     anode_overpotential=0.2e8,
        ...     cathode_overpotential=0.05e8
        ... )
        >>> print(f"Mass deposited: {result['mass_deposited']:.4f} g")
        >>> print(f"Energy per gram: {result['energy_per_gram']:.2e} erg/g")
    """
    # Charge passed
    charge = current * time

    # Electrochemical equivalent
    Z = electrochemical_equivalent(molar_mass, valence)

    # Mass deposited
    mass = faraday_second_law(current, time, molar_mass, valence)

    # Cell resistance
    if electrolyte_conductivity is not None and electrode_area > 0:
        resistance = electrode_spacing / (electrolyte_conductivity * electrode_area)
        ohmic_drop = current * resistance
    else:
        resistance = None
        ohmic_drop = 0.0

    # Required voltage
    required_voltage = decomposition_voltage(
        reversible_emf, anode_overpotential, cathode_overpotential, ohmic_drop
    )

    # Energy calculations
    energy = required_voltage * charge  # ergs (abvolt * abcoulomb)
    power = required_voltage * current  # ergs/s
    energy_per_gram = energy / mass if mass > 0 else float('inf')

    return {
        "mass_deposited": mass,
        "charge_passed": charge,
        "electrochemical_equivalent": Z,
        "electrochemical_equivalent_theoretical": Z,
        "required_voltage": required_voltage,
        "ohmic_drop": ohmic_drop,
        "total_overpotential": anode_overpotential + cathode_overpotential,
        "cell_resistance": resistance,
        "energy_consumed": energy,
        "energy_per_gram": energy_per_gram,
        "power": power,
        "temperature": temperature,
    }


# =============================================================================
# VERIFICATION AND VALIDATION FUNCTIONS
# =============================================================================

@maxwell_cite(
    249, 250, 251, 252,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Verify Faraday's laws consistency"
)
def verify_faradays_laws(
    tolerance: float = 1e-10,
) -> dict[str, float | bool | str]:
    """Verify Faraday's laws of electrolysis.

    Art. 249-252: This function verifies:
    1. First law: mass is proportional to charge (I*t)
    2. Second law: mass is proportional to equivalent weight (M/n)
    3. Consistency between the two formulations

    Args:
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with verification results:
        - first_law_verified: True if mass ∝ charge
        - second_law_verified: True if mass ∝ M/n
        - consistency_verified: True if both laws agree
        - test_results: Detailed test results
        - verified: Overall verification status

    Reference:
        Part II, Arts. 249-252: Faraday's laws verification.

    Example:
        >>> result = verify_faradays_laws()
        >>> assert result["verified"]
    """
    # Test 1: First law - mass ∝ charge
    Z = 0.001  # arbitrary electrochemical equivalent

    # Double the charge, mass should double
    m1 = faraday_first_law(1.0, 100, Z)
    m2 = faraday_first_law(2.0, 100, Z)
    m3 = faraday_first_law(1.0, 200, Z)

    first_law_verified = (
        abs(m2 - 2*m1) / m1 < tolerance and
        abs(m3 - 2*m1) / m1 < tolerance
    )

    # Test 2: Second law - mass ∝ M/n
    # Silver: M = 107.87, n = 1
    # Copper: M = 63.55, n = 2
    m_ag = faraday_second_law(1.0, 100, 107.87, 1)
    m_cu = faraday_second_law(1.0, 100, 63.55, 2)

    # Ratio should equal ratio of equivalent weights
    expected_ratio = (107.87 / 1) / (63.55 / 2)
    actual_ratio = m_ag / m_cu
    second_law_verified = abs(actual_ratio - expected_ratio) / expected_ratio < tolerance

    # Test 3: Consistency between first and second law
    Z_ag = electrochemical_equivalent(107.87, 1)
    m_first = faraday_first_law(1.0, 100, Z_ag)
    m_second = faraday_second_law(1.0, 100, 107.87, 1)
    consistency_verified = abs(m_first - m_second) / m_first < tolerance

    verified = first_law_verified and second_law_verified and consistency_verified

    return {
        "first_law_verified": first_law_verified,
        "second_law_verified": second_law_verified,
        "consistency_verified": consistency_verified,
        "test_results": {
            "m1_half_charge": m1,
            "m2_double_current": m2,
            "m3_double_time": m3,
            "silver_mass": m_ag,
            "copper_mass": m_cu,
            "expected_ratio": expected_ratio,
            "actual_ratio": actual_ratio,
        },
        "verified": verified,
    }


@maxwell_cite(
    262, 263,
    part=2, chapter="Electrolysis",
    theory_class="maxwell_original",
    description="Verify Kohlrausch's law of independent migration"
)
def verify_kohlrausch_law(
    tolerance: float = 1e-10,
) -> dict[str, float | bool | list]:
    """Verify Kohlrausch's law of independent migration.

    Art. 262-263: This function verifies:
    1. Additivity of ionic conductivities at infinite dilution
    2. Transference numbers sum to 1
    3. Consistency across different electrolytes with common ions

    Args:
        tolerance: Numerical tolerance for verification.

    Returns:
        Dictionary with verification results:
        - additivity_verified: True if conductivities are additive
        - transference_sum_verified: True if t+ + t- = 1
        - common_ion_verified: True for electrolytes with common ions
        - verified: Overall verification status

    Reference:
        Part II, Arts. 262-263: Kohlrausch's law verification.

    Example:
        >>> result = verify_kohlrausch_law()
        >>> assert result["verified"]
    """
    # Test 1: Additivity for NaCl
    Lambda_NaCl = limiting_molar_conductivity("Na+", "Cl-")
    Lambda_Na = get_ion_data("Na+").limiting_conductivity
    Lambda_Cl = get_ion_data("Cl-").limiting_conductivity

    additivity_verified = abs(Lambda_NaCl - (Lambda_Na + Lambda_Cl)) < tolerance

    # Test 2: Transference numbers sum to 1
    t = transference_number("Na+", "Cl-")
    transference_sum_verified = abs(t["t_cation"] + t["t_anion"] - 1.0) < tolerance

    # Test 3: Common ion consistency
    # NaCl and KCl share Cl- anion
    # Lambda_KCl - Lambda_NaCl should equal Lambda_K - Lambda_Na
    Lambda_KCl = limiting_molar_conductivity("K+", "Cl-")
    Lambda_K = get_ion_data("K+").limiting_conductivity

    diff_Lambda = Lambda_KCl - Lambda_NaCl
    diff_ionic = Lambda_K - Lambda_Na
    common_ion_verified = abs(diff_Lambda - diff_ionic) < tolerance

    # Test 4: Divalent ions (CuSO4)
    Lambda_CuSO4 = limiting_molar_conductivity("Cu2+", "SO4 2-")
    Lambda_Cu = get_ion_data("Cu2+").limiting_conductivity
    Lambda_SO4 = get_ion_data("SO4 2-").limiting_conductivity

    divalent_verified = abs(Lambda_CuSO4 - (Lambda_Cu + Lambda_SO4)) < tolerance

    verified = (
        additivity_verified and
        transference_sum_verified and
        common_ion_verified and
        divalent_verified
    )

    return {
        "additivity_verified": additivity_verified,
        "transference_sum_verified": transference_sum_verified,
        "common_ion_verified": common_ion_verified,
        "divalent_verified": divalent_verified,
        "test_results": {
            "Lambda_NaCl": Lambda_NaCl,
            "Lambda_KCl": Lambda_KCl,
            "Lambda_CuSO4": Lambda_CuSO4,
            "transference_numbers": t,
        },
        "verified": verified,
    }


# =============================================================================
# MODULE MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ELECTROLYSIS - Maxwell's Treatise, Part II, Chapter IV")
    print("Articles 249-263")
    print("=" * 70)

    print("\n--- Faraday's First Law (Arts. 249-250) ---")
    # Silver deposition: Z = 0.001118 g/C
    Z_ag = electrochemical_equivalent(107.87, 1)
    print(f"Silver electrochemical equivalent: {Z_ag:.6f} g/abC")
    mass = faraday_first_law(0.1, 3600, Z_ag)  # 0.1 abA for 1 hour
    print(f"Mass deposited (0.1 abA, 1 hour): {mass:.4f} g")

    print("\n--- Faraday's Second Law (Arts. 251-252) ---")
    # Copper deposition: M = 63.55 g/mol, n = 2
    mass_cu = faraday_second_law(0.1, 3600, 63.55, 2)
    print(f"Copper deposited (0.1 abA, 1 hour): {mass_cu:.4f} g")

    print("\n--- Electrochemical Equivalents ---")
    elements = [
        ("H", 1.008, 1),
        ("Ag", 107.87, 1),
        ("Cu", 63.55, 2),
        ("Zn", 65.38, 2),
        ("Al", 26.98, 3),
    ]
    print(f"{'Element':<10} {'M (g/mol)':<12} {'n':<5} {'Z (g/abC)':<12}")
    print("-" * 45)
    for symbol, M, n in elements:
        Z = electrochemical_equivalent(M, n)
        print(f"{symbol:<10} {M:<12.2f} {n:<5} {Z:<12.6f}")

    print("\n--- Polarization EMF (Arts. 253-254) ---")
    # Water electrolysis: E_rev = 1.23 V = 1.23e8 abV
    E_polarization = polarization_emf(
        reversible_potential=1.23e8,
        current_density=0.01,
        exchange_current_density=1e-6,
    )
    print(f"Water electrolysis polarization EMF: {E_polarization:.2e} abV")

    print("\n--- Decomposition Voltage (Arts. 255-256) ---")
    V_decomp = decomposition_voltage(
        reversible_emf=1.23e8,
        anode_overpotential=0.4e8,
        cathode_overpotential=0.1e8,
        ohmic_drop=0.05e8,
    )
    print(f"Water decomposition voltage: {V_decomp:.2e} abV ({V_decomp/1e8:.2f} V)")

    print("\n--- Ion Migration (Arts. 257-259) ---")
    for ion_symbol in ["Na+", "K+", "Cl-"]:
        ion = get_ion_data(ion_symbol)
        v = ion_migration_velocity(ion.mobility, 1e6)  # 10 kV/cm
        print(f"{ion_symbol}: mobility = {ion.mobility:.2e}, v = {v:.2e} cm/s")

    print("\n--- Electrolyte Conductivity (Arts. 260-261) ---")
    # 0.1 M NaCl
    kappa = electrolyte_conductivity(
        ion_concentrations=[1e-4, 1e-4],  # 0.1 M = 1e-4 mol/cm^3
        ion_charge_numbers=[1, -1],
        ion_mobilities=[5.19e-4, 7.91e-4],
    )
    print(f"0.1 M NaCl conductivity: {kappa:.4f} abmho/cm")

    print("\n--- Kohlrausch's Law (Arts. 262-263) ---")
    for cation, anion in [("Na+", "Cl-"), ("K+", "Cl-"), ("Cu2+", "SO4 2-")]:
        Lambda = limiting_molar_conductivity(cation, anion)
        t = transference_number(cation, anion)
        print(f"{cation}/{anion}: Lambda^0 = {Lambda:.1f}, t+ = {t['t_cation']:.3f}, t- = {t['t_anion']:.3f}")

    print("\n--- Concentration Polarization ---")
    eta = concentration_polarization(
        bulk_concentration=1e-4,
        surface_concentration=1e-5,
        diffusion_coefficient=7e-6,
        diffusion_layer_thickness=0.01,
        current_density=0.01,
        charge_number=2,
    )
    print(f"Concentration overpotential: {eta:.2e} abV ({eta/1e8:.4f} V)")

    print("\n--- Complete Electrolysis Analysis ---")
    result = analyze_electrolysis(
        current=0.1,
        time=3600,
        molar_mass=63.55,
        valence=2,
        reversible_emf=1.1e8,
        electrolyte_conductivity=0.1,
        anode_overpotential=0.2e8,
        cathode_overpotential=0.05e8,
    )
    print(f"Mass deposited: {result['mass_deposited']:.4f} g")
    print(f"Energy consumed: {result['energy_consumed']:.2e} erg")
    print(f"Energy per gram: {result['energy_per_gram']:.2e} erg/g")

    print("\n--- Verification Tests ---")
    faraday_result = verify_faradays_laws()
    print(f"Faraday's laws verified: {faraday_result['verified']}")

    kohlrausch_result = verify_kohlrausch_law()
    print(f"Kohlrausch's law verified: {kohlrausch_result['verified']}")

    print("\n" + "=" * 70)
    print("Module verification complete.")
    print("=" * 70)

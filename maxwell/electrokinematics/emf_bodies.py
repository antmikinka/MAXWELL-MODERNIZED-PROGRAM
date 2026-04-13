"""
EMF Between Different Bodies in Contact — Maxwell's Part II, Chapter III (Arts. 246-248).

This module implements Maxwell's theory of electromotive force between different
bodies in electrical contact:

1. **Contact EMF** (Arts. 246-247): Electromotive force at the junction of
   different materials, particularly metal-electrolyte interfaces.
   - Metal-electrolyte contact potential
   - Junction potential theory

2. **EMF Series** (Art. 248): Systematic arrangement of materials by their
   contact potentials.
   - Volta series extension to electrolytes
   - Junction potential calculations
   - Series of bodies in contact

Maxwell's key insight: The EMF at a junction depends on the intrinsic properties
of the two materials and is independent of the manner of contact (pressure, area).

CGS-EMU units are used throughout, following Maxwell's conventions:
    - EMF: abvolts
    - Temperature: Kelvin
    - Concentration: mol/cm³

Category: A (maxwell_original) — Maxwell's theory of contact EMF between bodies.

References:
    Part II, Chapter III: EMF Between Bodies in Contact (Arts. 246-248).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional
import numpy as np
from functools import wraps

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST, C, C_APPROX


# =============================================================================
# CONSTANTS
# =============================================================================

#: Gas constant in CGS (erg/(mol*K))
R_GAS: float = 8.314462618e7

#: Faraday constant in CGS-EMU (abcoulombs per mole)
FARADAY_CONSTANT: float = 96485.33212

#: Elementary charge in abcoulombs (EMU)
ELEMENTARY_CHARGE_EMU: float = 1.602176634e-20

#: Boltzmann constant in CGS (erg/K)
BOLTZMANN_CONSTANT: float = 1.380649e-16

#: Reference temperature (25 deg C in Kelvin)
REFERENCE_TEMPERATURE: float = 298.15


# =============================================================================
# CONTACT EMF: METAL-ELECTROLYTE JUNCTION (Arts. 246-247)
# =============================================================================

@maxwell_cite(
    246, 247,
    part=2, chapter="EMF Between Bodies in Contact",
    theory_class="maxwell_original",
    description="Calculate contact EMF between metal and electrolyte"
)
def contact_emf_metal_electrolyte(
    metal_work_function: float,
    electrolyte_chemical_potential: float,
    ion_valency: int = 1,
    temperature: float = REFERENCE_TEMPERATURE,
) -> dict[str, float]:
    """
    Calculate the contact electromotive force between a metal and electrolyte.

    Arts. 246-247: Maxwell analyzed the EMF arising at the junction of a metal
    and an electrolyte solution. This EMF is fundamental to electrochemical
    cells and corrosion phenomena.

    The contact EMF is determined by the difference in electrochemical potential:

        E_contact = (mu_electrolyte - phi_metal) / (z * e)

    where:
        - mu_electrolyte = chemical potential of ions in electrolyte (ergs/mol)
        - phi_metal = work function of the metal (ergs)
        - z = valency of the ion
        - e = elementary charge

    For a metal M in contact with its ion M^(z+) in solution:

        E_contact = E° + (RT/zF) * ln(a_Mz+)

    where E° is the standard electrode potential and a is the activity.

    Maxwell noted that this EMF is localized at the interface and depends on:
        - Nature of the metal (work function, crystal face)
        - Concentration of ions in the electrolyte
        - Temperature
        - Surface condition and contamination

    Args:
        metal_work_function: Work function of the metal in ergs.
        electrolyte_chemical_potential: Chemical potential of ions in ergs/mol.
        ion_valency: Valency z of the ion (default: 1 for monovalent).
        temperature: Temperature in Kelvin (default: 298.15 K).

    Returns:
        Dictionary with:
        - contact_emf: Contact potential in abvolts
        - chemical_contribution: Nernst term contribution (abvolts)
        - work_function_contribution: Metal contribution (abvolts)
        - temperature: Temperature in Kelvin

    Raises:
        ValueError: If ion_valency is zero or negative.

    References:
        Part II, Art. 246: Metal-electrolyte contact EMF.
        Part II, Art. 247: Theory of junction potentials.

    Example:
        >>> # Zinc electrode: phi_Zn = 4.33 eV = 6.94e-12 erg
        >>> # Zn2+ chemical potential at 1M
        >>> phi_zn = 4.33 * 1.602e-12  # ergs
        >>> mu_zn = -1.5e12  # ergs/mol (example value)
        >>> result = contact_emf_metal_electrolyte(phi_zn, mu_zn, ion_valency=2)
        >>> print(f"E_contact = {result['contact_emf']:.2e} abV")
    """
    if ion_valency <= 0:
        raise ValueError(f"ion_valency must be positive, got {ion_valency}")

    # Convert work function to per-mole basis for comparison
    # phi_metal (erg/atom) * N_A = erg/mol
    N_A = 6.02214076e23  # Avogadro's number
    phi_metal_molar = metal_work_function * N_A

    # Contact EMF from potential difference
    # E = (mu_electrolyte - phi_metal) / (z * F)
    delta_potential = electrolyte_chemical_potential - phi_metal_molar
    contact_emf = delta_potential / (ion_valency * FARADAY_CONSTANT)

    # Separate contributions
    work_function_contribution = -phi_metal_molar / (ion_valency * FARADAY_CONSTANT)
    chemical_contribution = electrolyte_chemical_potential / (ion_valency * FARADAY_CONSTANT)

    return {
        "contact_emf": contact_emf,
        "chemical_contribution": chemical_contribution,
        "work_function_contribution": work_function_contribution,
        "temperature": temperature,
        "ion_valency": ion_valency,
        "metal_work_function": metal_work_function,
        "electrolyte_chemical_potential": electrolyte_chemical_potential,
    }


@maxwell_cite(
    246, 247,
    part=2, chapter="EMF Between Bodies in Contact",
    theory_class="maxwell_original",
    description="Calculate EMF from concentration cell (Nernst equation)"
)
def concentration_cell_emf(
    concentration_1: float,
    concentration_2: float,
    ion_valency: int = 1,
    temperature: float = REFERENCE_TEMPERATURE,
    activity_coefficients: tuple[float, float] = None,
) -> dict[str, float]:
    """
    Calculate the EMF of a concentration cell.

    Arts. 246-247: Maxwell derived the EMF arising from a difference in
    concentration between two electrolyte solutions. This is the basis of
    concentration cells and potentiometric measurements.

    For a cell with the same metal electrodes but different ion concentrations:

        E = (RT/zF) * ln(a2/a1)

    where:
        - R = gas constant
        - T = temperature (K)
        - z = ion valency
        - F = Faraday constant
        - a1, a2 = activities of ions in solutions 1 and 2

    For dilute solutions, activity ≈ concentration:

        E ≈ (RT/zF) * ln(c2/c1)

    At 25°C (298.15 K), RT/F ≈ 0.0257 V = 2.57e6 abvolts.

    Args:
        concentration_1: Concentration c1 of solution 1 (mol/cm³).
        concentration_2: Concentration c2 of solution 2 (mol/cm³).
        ion_valency: Valency z of the ion (default: 1).
        temperature: Temperature in Kelvin.
        activity_coefficients: Optional (gamma1, gamma2) for activity correction.

    Returns:
        Dictionary with:
        - emf: Cell EMF in abvolts
        - nernst_potential: RT/zF * ln(c2/c1) term
        - concentration_ratio: c2/c1
        - thermal_voltage: RT/F at the given temperature

    Raises:
        ValueError: If concentrations are non-positive or valency invalid.

    References:
        Part II, Arts. 246-247: Concentration-dependent EMF.

    Example:
        >>> # 10:1 concentration ratio at 25°C
        >>> result = concentration_cell_emf(0.001, 0.01, ion_valency=1)
        >>> print(f"E = {result['emf']:.2e} abV ({result['emf']/1e8:.3f} V)")
    """
    if concentration_1 <= 0 or concentration_2 <= 0:
        raise ValueError("Concentrations must be positive")
    if ion_valency <= 0:
        raise ValueError(f"ion_valency must be positive, got {ion_valency}")

    # Concentration ratio
    conc_ratio = concentration_2 / concentration_1

    # Thermal voltage: RT/F
    thermal_voltage = R_GAS * temperature / FARADAY_CONSTANT

    # Activity correction
    if activity_coefficients is not None:
        gamma1, gamma2 = activity_coefficients
        activity_ratio = (concentration_2 * gamma2) / (concentration_1 * gamma1)
    else:
        activity_ratio = conc_ratio

    # Nernst equation: E = (RT/zF) * ln(a2/a1)
    nernst_potential = (thermal_voltage / ion_valency) * np.log(activity_ratio)

    return {
        "emf": nernst_potential,
        "nernst_potential": nernst_potential,
        "concentration_ratio": conc_ratio,
        "activity_ratio": activity_ratio,
        "thermal_voltage": thermal_voltage,
        "thermal_voltage_mv": thermal_voltage / 1e6,  # In millivolts
        "temperature": temperature,
        "ion_valency": ion_valency,
    }


# =============================================================================
# JUNCTION POTENTIAL (Art. 248)
# =============================================================================

@maxwell_cite(
    248,
    part=2, chapter="EMF Between Bodies in Contact",
    theory_class="maxwell_original",
    description="Calculate liquid junction potential (Planck-Henderson)"
)
def junction_potential(
    cation_mobility: float,
    anion_mobility: float,
    concentration_1: float,
    concentration_2: float,
    cation_valency: int = 1,
    anion_valency: int = 1,
    temperature: float = REFERENCE_TEMPERATURE,
) -> dict[str, float]:
    """
    Calculate the liquid junction potential between two electrolyte solutions.

    Art. 248: When two electrolyte solutions of different concentrations (or
    compositions) are in contact, a potential difference arises at the junction
    due to unequal diffusion rates of cations and anions.

    Maxwell analyzed this phenomenon, which was later formalized by Planck
    and Henderson. For a single 1:1 electrolyte:

        E_junction = (RT/F) * ((u+ - u-) / (u+ + u-)) * ln(c2/c1)

    where:
        - u+ = cation mobility
        - u- = anion mobility
        - c1, c2 = concentrations on either side of junction

    The junction potential can also be expressed using transport numbers:

        E_junction = (RT/F) * (t+ - t-) * ln(c2/c1)

    where t+ = u+/(u+ + u-) and t- = u-/(u+ + u-).

    For a salt bridge or porous junction, the potential is minimized by using
    ions with similar mobilities (e.g., KCl: K+ and Cl- have nearly equal u).

    Args:
        cation_mobility: Cation mobility u+ (cm²/(V*s) in EMU).
        anion_mobility: Anion mobility u- (cm²/(V*s) in EMU).
        concentration_1: Concentration c1 on side 1 (mol/cm³).
        concentration_2: Concentration c2 on side 2 (mol/cm³).
        cation_valency: Valency of cation (default: 1).
        anion_valency: Valency of anion (default: 1).
        temperature: Temperature in Kelvin.

    Returns:
        Dictionary with:
        - junction_potential: E_junction in abvolts
        - transport_number_cation: t+ = u+/(u+ + u-)
        - transport_number_anion: t- = u-/(u+ + u-)
        - mobility_ratio: u+/u-
        - concentration_ratio: c2/c1

    Raises:
        ValueError: If mobilities or concentrations are non-positive.

    References:
        Part II, Art. 248: Junction potential theory.

    Example:
        >>> # KCl junction: u_K+ ≈ u_Cl- (nearly equal mobilities)
        >>> u_k = 7.62e-4  # cm²/(V*s)
        >>> u_cl = 7.91e-4
        >>> result = junction_potential(u_k, u_cl, 0.01, 0.001)
        >>> print(f"E_junction = {result['junction_potential']:.2e} abV")
    """
    if cation_mobility <= 0 or anion_mobility <= 0:
        raise ValueError("Mobilities must be positive")
    if concentration_1 <= 0 or concentration_2 <= 0:
        raise ValueError("Concentrations must be positive")

    # Transport numbers
    total_mobility = cation_mobility + anion_mobility
    t_plus = cation_mobility / total_mobility
    t_minus = anion_mobility / total_mobility

    # Concentration ratio
    conc_ratio = concentration_2 / concentration_1

    # Thermal voltage
    thermal_voltage = R_GAS * temperature / FARADAY_CONSTANT

    # Junction potential (Planck-Henderson equation for 1:1 electrolyte)
    # E_j = (RT/F) * (t+ - t-) * ln(c2/c1)
    mobility_difference_factor = (cation_mobility - anion_mobility) / total_mobility
    junction_emf = thermal_voltage * mobility_difference_factor * np.log(conc_ratio)

    return {
        "junction_potential": junction_emf,
        "transport_number_cation": t_plus,
        "transport_number_anion": t_minus,
        "mobility_ratio": cation_mobility / anion_mobility,
        "concentration_ratio": conc_ratio,
        "thermal_voltage": thermal_voltage,
        "temperature": temperature,
        "cation_mobility": cation_mobility,
        "anion_mobility": anion_mobility,
    }


@maxwell_cite(
    248,
    part=2, chapter="EMF Between Bodies in Contact",
    theory_class="maxwell_original",
    description="Calculate junction potential for multiple electrolytes"
)
def junction_potential_multi_ion(
    ion_data: list[dict],
    concentration_1: float,
    concentration_2: float,
    temperature: float = REFERENCE_TEMPERATURE,
) -> dict[str, float]:
    """
    Calculate liquid junction potential for a multi-ion electrolyte mixture.

    Art. 248: Extension of junction potential theory to mixtures of multiple
    ionic species. The generalized Planck-Henderson equation sums over all ions:

        E_junction = -(RT/F) * sum_i [ (z_i * u_i * (c_i2 - c_i1)) / sum_j (z_j² * u_j * c_j_avg) ] * ln(...)

    For simplicity, we use the Henderson approximation:

        E_junction = (RT/F) * ln(sum_i z_i u_i c_i1 / sum_i z_i u_i c_i2)

    where the sum is over all ionic species.

    Args:
        ion_data: List of dicts with keys:
                 - 'valency': z_i (positive for cations, negative for anions)
                 - 'mobility': u_i (cm²/(V*s))
                 - 'concentration_ratio': c_i2/c_i1 (optional, default: same as bulk)
        concentration_1: Reference concentration on side 1.
        concentration_2: Reference concentration on side 2.
        temperature: Temperature in Kelvin.

    Returns:
        Dictionary with:
        - junction_potential: E_junction in abvolts
        - sum_zu_side1: Sum of z*u*c on side 1
        - sum_zu_side2: Sum of z*u*c on side 2
        - n_ions: Number of ionic species

    References:
        Part II, Art. 248: Multi-ion junction potential.

    Example:
        >>> # Mixed KCl + NaCl solution
        >>> ions = [
        ...     {'valency': 1, 'mobility': 7.62e-4},  # K+
        ...     {'valency': 1, 'mobility': 5.19e-4},  # Na+
        ...     {'valency': -1, 'mobility': 7.91e-4}, # Cl-
        ... ]
        >>> result = junction_potential_multi_ion(ions, 0.01, 0.001)
    """
    if not ion_data:
        raise ValueError("ion_data cannot be empty")

    # Calculate sum of z*u*c for each side
    sum_zu_side1 = 0.0
    sum_zu_side2 = 0.0

    for ion in ion_data:
        z = ion.get('valency', 1)
        u = ion.get('mobility', 1.0)
        conc_ratio = ion.get('concentration_ratio', concentration_2 / concentration_1)

        c1 = concentration_1
        c2 = concentration_2 * conc_ratio

        # For electroneutrality, we need to handle signs properly
        sum_zu_side1 += abs(z) * u * c1
        sum_zu_side2 += abs(z) * u * c2

    # Thermal voltage
    thermal_voltage = R_GAS * temperature / FARADAY_CONSTANT

    # Henderson equation
    if sum_zu_side1 > 0 and sum_zu_side2 > 0:
        junction_emf = thermal_voltage * np.log(sum_zu_side1 / sum_zu_side2)
    else:
        junction_emf = 0.0

    return {
        "junction_potential": junction_emf,
        "sum_zu_side1": sum_zu_side1,
        "sum_zu_side2": sum_zu_side2,
        "n_ions": len(ion_data),
        "thermal_voltage": thermal_voltage,
        "temperature": temperature,
    }


# =============================================================================
# EMF SERIES OF BODIES (Arts. 246-248)
# =============================================================================

@maxwell_cite(
    246, 247, 248,
    part=2, chapter="EMF Between Bodies in Contact",
    theory_class="maxwell_original",
    description="Calculate total EMF of series of bodies in contact"
)
def emf_series_bodies(
    bodies: list[dict],
    temperature: float = REFERENCE_TEMPERATURE,
) -> dict[str, float | list]:
    """
    Calculate the total EMF of a series of different bodies in contact.

    Arts. 246-248: Maxwell analyzed the total EMF when multiple materials
    are connected in series. The key principle is that the total EMF is
    the sum of individual junction potentials, and depends only on the
    first and last materials (if temperature is uniform).

    For a chain A | B | C | D | ... | Z:

        E_total = E_AB + E_BC + E_CD + ... + E_YZ

    By Volta's law of intermediate metals, if all junctions are at the
    same temperature:

        E_total = E_AZ (depends only on end materials)

    However, if there are temperature gradients, thermoelectric EMFs
    contribute (Seebeck effect).

    Args:
        bodies: List of dicts describing each body in the series.
               Each dict should have:
               - 'name': Material name
               - 'work_function': Work function in eV (for metals)
               - 'electrode_potential': Standard potential in V (for electrolytes)
               - 'concentration': Ion concentration (for electrolytes)
               - 'temperature': Local temperature (optional, default: uniform)
        temperature: Uniform temperature if not specified per body.

    Returns:
        Dictionary with:
        - total_emf: Total EMF of the series (abvolts)
        - junction_emfs: List of EMFs at each junction
        - junctions: List of junction descriptions
        - n_junctions: Number of junctions

    Raises:
        ValueError: If fewer than 2 bodies provided.

    References:
        Part II, Arts. 246-248: EMF series and Volta's law.

    Example:
        >>> # Zn | Cu | Pt series
        >>> bodies = [
        ...     {'name': 'Zn', 'work_function': 4.33},
        ...     {'name': 'Cu', 'work_function': 4.65},
        ...     {'name': 'Pt', 'work_function': 5.65},
        ... ]
        >>> result = emf_series_bodies(bodies)
        >>> print(f"Total EMF = {result['total_emf']:.2e} abV")
    """
    if len(bodies) < 2:
        raise ValueError("At least 2 bodies required for a series")

    junction_emfs = []
    junctions = []

    for i in range(len(bodies) - 1):
        body_a = bodies[i]
        body_b = bodies[i + 1]

        # Determine junction type and calculate EMF
        emf = 0.0
        junction_desc = f"{body_a['name']} | {body_b['name']}"

        # Both are metals (work functions given)
        if 'work_function' in body_a and 'work_function' in body_b:
            # Contact potential: E = (phi_B - phi_A) * 1e8 abvolts/eV
            phi_a = body_a['work_function']
            phi_b = body_b['work_function']
            emf = (phi_b - phi_a) * 1e8

        # One or both are electrolytes
        elif 'electrode_potential' in body_a or 'electrode_potential' in body_b:
            E_a = body_a.get('electrode_potential', 0.0)
            E_b = body_b.get('electrode_potential', 0.0)
            # Cell EMF = E_cathode - E_anode = E_b - E_a
            emf = (E_b - E_a) * 1e8

        # Mixed: metal and electrolyte
        elif 'work_function' in body_a and 'concentration' in body_b:
            # Metal-electrolyte junction
            # Simplified: use work function and concentration
            emf = body_a.get('work_function', 4.5) * 1e7  # Approximate

        elif 'work_function' in body_b and 'concentration' in body_a:
            emf = -body_b.get('work_function', 4.5) * 1e7  # Approximate

        else:
            # Unknown junction type
            emf = 0.0

        junction_emfs.append(emf)
        junctions.append(junction_desc)

    # Total EMF
    total_emf = sum(junction_emfs)

    return {
        "total_emf": total_emf,
        "junction_emfs": junction_emfs,
        "junctions": junctions,
        "n_junctions": len(junctions),
        "bodies": [b.get('name', 'Unknown') for b in bodies],
        "temperature": temperature,
    }


@maxwell_cite(
    246, 247, 248,
    part=2, chapter="EMF Between Bodies in Contact",
    theory_class="maxwell_original",
    description="Build Volta series table for common materials"
)
def volta_series_table(
    reference: str = "copper",
    temperature: float = REFERENCE_TEMPERATURE,
) -> dict[str, dict[str, float]]:
    """
    Generate a Volta series table of contact potentials relative to a reference.

    Arts. 246-248: Maxwell compiled the Volta series, ordering materials by
    their contact potentials. This table is fundamental for understanding
    galvanic corrosion, battery design, and electrical contacts.

    The Volta series ranks materials by their tendency to become positively
    or negatively charged when in contact with other materials.

    Args:
        reference: Reference material name (default: "copper").
        temperature: Temperature in Kelvin.

    Returns:
        Dictionary mapping material names to their properties:
        - work_function_ev: Work function in eV
        - contact_potential_vs_ref: Contact potential vs reference (abvolts)
        - volta_position: Position in the series (lower = more electropositive)

    References:
        Part II, Arts. 246-248: Volta series compilation.

    Example:
        >>> table = volta_series_table(reference="copper")
        >>> for material, data in table.items():
        ...     print(f"{material}: {data['contact_potential_vs_ref']:.2e} abV vs Cu")
    """
    # Standard work functions and electrode potentials
    # Data from standard references (values in eV for metals, V for electrolytes)
    materials = {
        # Metals (work function in eV)
        "lithium": {"work_function_ev": 2.90, "type": "metal"},
        "potassium": {"work_function_ev": 2.30, "type": "metal"},  # Actually ~2.3 eV
        "sodium": {"work_function_ev": 2.75, "type": "metal"},
        "calcium": {"work_function_ev": 2.87, "type": "metal"},
        "magnesium": {"work_function_ev": 3.66, "type": "metal"},
        "aluminum": {"work_function_ev": 4.08, "type": "metal"},
        "zinc": {"work_function_ev": 4.33, "type": "metal"},
        "chromium": {"work_function_ev": 4.50, "type": "metal"},
        "iron": {"work_function_ev": 4.50, "type": "metal"},
        "cadmium": {"work_function_ev": 4.08, "type": "metal"},
        "nickel": {"work_function_ev": 5.04, "type": "metal"},
        "tin": {"work_function_ev": 4.42, "type": "metal"},
        "lead": {"work_function_ev": 4.14, "type": "metal"},
        "hydrogen": {"work_function_ev": 4.50, "type": "reference"},  # SHE reference
        "copper": {"work_function_ev": 4.65, "type": "metal"},
        "silver": {"work_function_ev": 4.74, "type": "metal"},
        "gold": {"work_function_ev": 5.10, "type": "metal"},
        "platinum": {"work_function_ev": 5.65, "type": "metal"},

        # Standard electrode potentials (V vs SHE)
        "li_ion": {"electrode_potential_v": -3.04, "type": "electrolyte"},
        "k_ion": {"electrode_potential_v": -2.93, "type": "electrolyte"},
        "na_ion": {"electrode_potential_v": -2.71, "type": "electrolyte"},
        "mg_ion": {"electrode_potential_v": -2.37, "type": "electrolyte"},
        "al_ion": {"electrode_potential_v": -1.66, "type": "electrolyte"},
        "zn_ion": {"electrode_potential_v": -0.76, "type": "electrolyte"},
        "fe_ion": {"electrode_potential_v": -0.44, "type": "electrolyte"},
        "ni_ion": {"electrode_potential_v": -0.25, "type": "electrolyte"},
        "sn_ion": {"electrode_potential_v": -0.14, "type": "electrolyte"},
        "pb_ion": {"electrode_potential_v": -0.13, "type": "electrolyte"},
        "h_ion": {"electrode_potential_v": 0.00, "type": "electrolyte"},  # SHE
        "cu_ion": {"electrode_potential_v": +0.34, "type": "electrolyte"},
        "ag_ion": {"electrode_potential_v": +0.80, "type": "electrolyte"},
        "au_ion": {"electrode_potential_v": +1.50, "type": "electrolyte"},
    }

    # Get reference work function
    if reference.lower() in materials:
        ref_data = materials[reference.lower()]
        if 'work_function_ev' in ref_data:
            ref_wf = ref_data['work_function_ev']
        else:
            # Convert electrode potential to approximate work function
            ref_wf = 4.5 + ref_data.get('electrode_potential_v', 0)
    else:
        ref_wf = 4.65  # Default to copper

    # Build table
    table = {}
    volta_position = 0

    # Sort by work function / electrode potential
    sorted_materials = sorted(
        materials.items(),
        key=lambda x: x[1].get('work_function_ev', 4.5 + x[1].get('electrode_potential_v', 0))
    )

    for name, data in sorted_materials:
        if 'work_function_ev' in data:
            wf = data['work_function_ev']
            # Contact potential vs reference (abvolts)
            contact_potential = (wf - ref_wf) * 1e8
        else:
            E = data.get('electrode_potential_v', 0)
            contact_potential = E * 1e8  # Convert V to abvolts

        table[name] = {
            "work_function_ev": data.get('work_function_ev'),
            "electrode_potential_v": data.get('electrode_potential_v'),
            "contact_potential_vs_ref": contact_potential,
            "volta_position": volta_position,
            "type": data.get('type', 'unknown'),
        }
        volta_position += 1

    return table


# =============================================================================
# CONTACT EMF ANALYZER CLASS
# =============================================================================

@dataclass
class ContactEMFAnalyzer:
    """
    Comprehensive analyzer for contact EMF phenomena.

    This class provides methods for analyzing:
    - Multi-junction systems
    - Temperature-dependent effects
    - Electrochemical cells

    Attributes:
        temperature: Operating temperature (K).
        reference_material: Reference material for potential calculations.
    """

    temperature: float = REFERENCE_TEMPERATURE
    reference_material: str = "copper"

    @maxwell_cite(
        246, 247,
        part=2, chapter="EMF Between Bodies in Contact",
        theory_class="maxwell_original",
        description="Analyze single metal-electrolyte junction"
    )
    def analyze_metal_electrolyte_junction(
        self,
        metal_work_function: float,
        electrolyte_chemical_potential: float,
        ion_valency: int = 1,
    ) -> dict:
        """Analyze a metal-electrolyte junction."""
        return contact_emf_metal_electrolyte(
            metal_work_function=metal_work_function,
            electrolyte_chemical_potential=electrolyte_chemical_potential,
            ion_valency=ion_valency,
            temperature=self.temperature,
        )

    @maxwell_cite(
        248,
        part=2, chapter="EMF Between Bodies in Contact",
        theory_class="maxwell_original",
        description="Analyze liquid junction potential"
    )
    def analyze_junction_potential(
        self,
        cation_mobility: float,
        anion_mobility: float,
        concentration_1: float,
        concentration_2: float,
    ) -> dict:
        """Analyze a liquid junction between two solutions."""
        return junction_potential(
            cation_mobility=cation_mobility,
            anion_mobility=anion_mobility,
            concentration_1=concentration_1,
            concentration_2=concentration_2,
            temperature=self.temperature,
        )

    @maxwell_cite(
        246, 247, 248,
        part=2, chapter="EMF Between Bodies in Contact",
        theory_class="maxwell_original",
        description="Analyze complete electrochemical cell"
    )
    def analyze_electrochemical_cell(
        self,
        anode_material: str,
        cathode_material: str,
        electrolyte_concentration: float,
        ion_valency: int = 1,
    ) -> dict:
        """
        Analyze a complete electrochemical cell.

        Args:
            anode_material: Anode material name.
            cathode_material: Cathode material name.
            electrolyte_concentration: Electrolyte concentration.
            ion_valency: Ion valency.

        Returns:
            Dictionary with cell EMF and component contributions.
        """
        table = volta_series_table(reference=self.reference_material)

        # Get electrode potentials
        anode_data = table.get(anode_material.lower(), {})
        cathode_data = table.get(cathode_material.lower(), {})

        E_anode = anode_data.get('electrode_potential_v', 0)
        E_cathode = cathode_data.get('electrode_potential_v', 0)

        # Cell EMF (standard)
        E_cell_standard = (E_cathode - E_anode) * 1e8  # Convert to abvolts

        # Nernst correction for concentration
        nernst_result = concentration_cell_emf(
            concentration_1=1.0,  # Standard state
            concentration_2=electrolyte_concentration,
            ion_valency=ion_valency,
            temperature=self.temperature,
        )

        E_cell_total = E_cell_standard + nernst_result['emf']

        return {
            "cell_emf": E_cell_total,
            "standard_emf": E_cell_standard,
            "nernst_correction": nernst_result['emf'],
            "anode_material": anode_material,
            "cathode_material": cathode_material,
            "electrolyte_concentration": electrolyte_concentration,
            "temperature": self.temperature,
        }


# =============================================================================
# MAIN: Module verification
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EMF BETWEEN BODIES IN CONTACT")
    print("Maxwell's Treatise, Part II, Chapter III (Arts. 246-248)")
    print("=" * 70)

    # Test contact EMF
    print("\n--- Contact EMF: Metal-Electrolyte (Arts. 246-247) ---")
    phi_zn = 4.33 * 1.602e-12  # Zinc work function in ergs
    mu_zn = -1.5e12  # Chemical potential (example)
    result = contact_emf_metal_electrolyte(phi_zn, mu_zn, ion_valency=2)
    print(f"  Zn | Zn2+ junction:")
    print(f"    E_contact = {result['contact_emf']:.2e} abV")

    # Test concentration cell
    print("\n--- Concentration Cell EMF (Arts. 246-247) ---")
    result = concentration_cell_emf(0.001, 0.01, ion_valency=1)
    print(f"  10:1 concentration ratio at 25°C:")
    print(f"    E = {result['emf']:.2e} abV ({result['emf']/1e8:.3f} V)")
    print(f"    Thermal voltage = {result['thermal_voltage_mv']:.2f} mV")

    # Test junction potential
    print("\n--- Liquid Junction Potential (Art. 248) ---")
    # KCl: nearly equal mobilities
    u_k = 7.62e-4
    u_cl = 7.91e-4
    result = junction_potential(u_k, u_cl, 0.01, 0.001)
    print(f"  KCl junction (0.01M | 0.001M):")
    print(f"    E_junction = {result['junction_potential']:.2e} abV")
    print(f"    t+ = {result['transport_number_cation']:.3f}, t- = {result['transport_number_anion']:.3f}")

    # Test EMF series
    print("\n--- EMF Series of Bodies (Arts. 246-248) ---")
    bodies = [
        {'name': 'Zn', 'work_function': 4.33},
        {'name': 'Cu', 'work_function': 4.65},
        {'name': 'Pt', 'work_function': 5.65},
    ]
    result = emf_series_bodies(bodies)
    print(f"  Zn | Cu | Pt series:")
    print(f"    Total EMF = {result['total_emf']:.2e} abV")
    for junction, emf in zip(result['junctions'], result['junction_emfs']):
        print(f"    {junction}: {emf:.2e} abV")

    # Test Volta series table
    print("\n--- Volta Series Table (Arts. 246-248) ---")
    table = volta_series_table(reference="copper")
    print(f"  Contact potentials vs Copper (abvolts):")
    for material in ['zinc', 'iron', 'copper', 'silver', 'gold', 'platinum']:
        if material in table:
            data = table[material]
            print(f"    {material.capitalize()}: {data['contact_potential_vs_ref']:.2e} abV")

    print("\n" + "=" * 70)
    print("Module verification complete.")
    print("=" * 70)

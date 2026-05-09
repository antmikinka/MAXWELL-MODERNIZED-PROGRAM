"""JAX electrolysis -- Part II Electrolysis (Arts. 249-263).

Faraday's laws, ion transport, polarization, and complete electrolysis cell
modelling implemented with JAX pytree support for JIT compilation, automatic
differentiation, and vectorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import jax
import jax.numpy as jnp

from maxwell.config.conventions import maxwell_cite
from maxwell.jax._compat import jax_tree, safe_div, safe_log, safe_sqrt

__all__ = [
    "FaradayLawsJAX",
    "IonTransportJAX",
    "PolarizationJAX",
    "ElectrolysisCellJAX",
    "FARADAY_CONSTANT_JAX",
    "ELEMENTARY_CHARGE_EMU_JAX",
    "AVOGADRO_NUMBER_JAX",
    "R_GAS_CGS_JAX",
    "faraday_first_law_jax",
    "faraday_second_law_jax",
    "electrochemical_equivalent_jax",
    "polarization_emf_jax",
    "decomposition_voltage_jax",
    "ion_migration_velocity_jax",
    "electrolyte_conductivity_jax",
    "kohlrausch_law_jax",
    "concentration_polarization_jax",
    "battery_back_emf_jax",
    "transference_number_jax",
    "verify_electrolysis_jax",
]

# -- Module-level constants (jnp.array float64) -----------------------------------

#: Faraday constant in CGS-EMU (abcoulombs per mole)
FARADAY_CONSTANT_JAX = jnp.array(96485.33212, dtype=jnp.float64)

#: Elementary charge in abcoulombs (EMU)
ELEMENTARY_CHARGE_EMU_JAX = jnp.array(1.602176634e-20, dtype=jnp.float64)

#: Avogadro's number (per mole)
AVOGADRO_NUMBER_JAX = jnp.array(6.02214076e23, dtype=jnp.float64)

#: Gas constant in CGS (erg/(mol*K))
R_GAS_CGS_JAX = jnp.array(8.314462618e7, dtype=jnp.float64)


# -- Data classes -------------------------------------------------------------------


@jax_tree
@dataclass
class FaradayLawsJAX:
    """Faraday's laws of electrolysis. Arts. 249-252.

    Fields:
        faraday_constant: Faraday constant in abcoulombs/mol (CGS-EMU).
    """

    faraday_constant: float = 96485.33212

    def __post_init__(self) -> None:
        self.faraday_constant = jnp.asarray(self.faraday_constant, dtype=jnp.float64)

    def mass_from_charge(
        self, charge: jax.Array, molar_mass: jax.Array, valence: jax.Array
    ) -> jax.Array:
        """Calculate mass from charge: m = Q * M / (n * F)."""
        return self._mass_from_charge_jit(
            charge, molar_mass, valence, self.faraday_constant
        )

    def mass_from_current_time(
        self,
        current: jax.Array,
        time: jax.Array,
        molar_mass: jax.Array,
        valence: jax.Array,
    ) -> jax.Array:
        """Calculate mass from current and time: m = I*t*M/(n*F)."""
        return self._mass_from_current_time_jit(
            current, time, molar_mass, valence, self.faraday_constant
        )

    def electrochemical_equivalent(
        self, molar_mass: jax.Array, valence: jax.Array
    ) -> jax.Array:
        """Electrochemical equivalent: Z = M/(n*F)."""
        return self._electrochemical_equivalent_jit(
            molar_mass, valence, self.faraday_constant
        )

    def required_charge(
        self, mass: jax.Array, molar_mass: jax.Array, valence: jax.Array
    ) -> jax.Array:
        """Required charge to deposit mass: Q = m*n*F/M."""
        return self._required_charge_jit(
            mass, molar_mass, valence, self.faraday_constant
        )

    def current_for_mass_time(
        self,
        mass: jax.Array,
        time: jax.Array,
        molar_mass: jax.Array,
        valence: jax.Array,
    ) -> jax.Array:
        """Current needed to deposit mass in given time: I = m*n*F/(M*t)."""
        return self._current_for_mass_time_jit(
            mass, time, molar_mass, valence, self.faraday_constant
        )

    @staticmethod
    @jax.jit
    def _mass_from_charge_jit(
        charge: jax.Array,
        molar_mass: jax.Array,
        valence: jax.Array,
        faraday_constant: jax.Array,
    ) -> jax.Array:
        charge = jnp.asarray(charge, dtype=jnp.float64)
        molar_mass = jnp.asarray(molar_mass, dtype=jnp.float64)
        valence = jnp.asarray(valence, dtype=jnp.float64)
        faraday_constant = jnp.asarray(faraday_constant, dtype=jnp.float64)
        return safe_div(charge * molar_mass, valence * faraday_constant)

    @staticmethod
    @jax.jit
    def _mass_from_current_time_jit(
        current: jax.Array,
        time: jax.Array,
        molar_mass: jax.Array,
        valence: jax.Array,
        faraday_constant: jax.Array,
    ) -> jax.Array:
        current = jnp.asarray(current, dtype=jnp.float64)
        time = jnp.asarray(time, dtype=jnp.float64)
        molar_mass = jnp.asarray(molar_mass, dtype=jnp.float64)
        valence = jnp.asarray(valence, dtype=jnp.float64)
        faraday_constant = jnp.asarray(faraday_constant, dtype=jnp.float64)
        return safe_div(current * time * molar_mass, valence * faraday_constant)

    @staticmethod
    @jax.jit
    def _electrochemical_equivalent_jit(
        molar_mass: jax.Array,
        valence: jax.Array,
        faraday_constant: jax.Array,
    ) -> jax.Array:
        molar_mass = jnp.asarray(molar_mass, dtype=jnp.float64)
        valence = jnp.asarray(valence, dtype=jnp.float64)
        faraday_constant = jnp.asarray(faraday_constant, dtype=jnp.float64)
        return safe_div(molar_mass, valence * faraday_constant)

    @staticmethod
    @jax.jit
    def _required_charge_jit(
        mass: jax.Array,
        molar_mass: jax.Array,
        valence: jax.Array,
        faraday_constant: jax.Array,
    ) -> jax.Array:
        mass = jnp.asarray(mass, dtype=jnp.float64)
        molar_mass = jnp.asarray(molar_mass, dtype=jnp.float64)
        valence = jnp.asarray(valence, dtype=jnp.float64)
        faraday_constant = jnp.asarray(faraday_constant, dtype=jnp.float64)
        return safe_div(mass * valence * faraday_constant, molar_mass)

    @staticmethod
    @jax.jit
    def _current_for_mass_time_jit(
        mass: jax.Array,
        time: jax.Array,
        molar_mass: jax.Array,
        valence: jax.Array,
        faraday_constant: jax.Array,
    ) -> jax.Array:
        mass = jnp.asarray(mass, dtype=jnp.float64)
        time = jnp.asarray(time, dtype=jnp.float64)
        molar_mass = jnp.asarray(molar_mass, dtype=jnp.float64)
        valence = jnp.asarray(valence, dtype=jnp.float64)
        faraday_constant = jnp.asarray(faraday_constant, dtype=jnp.float64)
        return safe_div(mass * valence * faraday_constant, molar_mass * time)


@jax_tree
@dataclass
class IonTransportJAX:
    """Ion migration and transport. Arts. 257-263.

    Fields:
        ion_mobilities: Mobilities of ions, shape (n_ions,), cm^2/(V*s).
        ion_charges: Valence numbers (signed), shape (n_ions,).
    """

    ion_mobilities: jax.Array
    ion_charges: jax.Array

    def __post_init__(self) -> None:
        self.ion_mobilities = jnp.asarray(self.ion_mobilities, dtype=jnp.float64)
        self.ion_charges = jnp.asarray(self.ion_charges, dtype=jnp.float64)

    def migration_velocity(self, electric_field: jax.Array) -> jax.Array:
        """Ion migration velocity: v = u * z * E."""
        return self._migration_velocity_jit(
            self.ion_mobilities, self.ion_charges, electric_field
        )

    def electrolyte_conductivity(self, concentrations: jax.Array) -> jax.Array:
        """Electrolyte conductivity: sigma = F * sum(c * |z| * u)."""
        return self._electrolyte_conductivity_jit(
            concentrations, self.ion_charges, self.ion_mobilities, FARADAY_CONSTANT_JAX
        )

    def transference_numbers(self) -> Dict[str, jax.Array]:
        """Transference numbers: t_i = |z_i|*u_i / sum(|z_j|*u_j)."""
        return self._transference_numbers_jit(self.ion_charges, self.ion_mobilities)

    def limiting_current_density(
        self,
        concentrations: jax.Array,
        diffusion_coeffs: jax.Array,
        layer_thickness: jax.Array,
        charge_numbers: jax.Array,
    ) -> jax.Array:
        """Limiting current density: i_L = |n|*F*D*c/delta."""
        return self._limiting_current_density_jit(
            concentrations,
            diffusion_coeffs,
            layer_thickness,
            charge_numbers,
            FARADAY_CONSTANT_JAX,
        )

    @staticmethod
    @jax.jit
    def _migration_velocity_jit(
        mobilities: jax.Array,
        charges: jax.Array,
        electric_field: jax.Array,
    ) -> jax.Array:
        mobilities = jnp.asarray(mobilities, dtype=jnp.float64)
        charges = jnp.asarray(charges, dtype=jnp.float64)
        electric_field = jnp.asarray(electric_field, dtype=jnp.float64)
        return mobilities * charges * electric_field

    @staticmethod
    @jax.jit
    def _electrolyte_conductivity_jit(
        concentrations: jax.Array,
        charges: jax.Array,
        mobilities: jax.Array,
        faraday_constant: jax.Array,
    ) -> jax.Array:
        concentrations = jnp.asarray(concentrations, dtype=jnp.float64)
        charges = jnp.asarray(charges, dtype=jnp.float64)
        mobilities = jnp.asarray(mobilities, dtype=jnp.float64)
        faraday_constant = jnp.asarray(faraday_constant, dtype=jnp.float64)
        return faraday_constant * jnp.sum(
            concentrations * jnp.abs(charges) * mobilities
        )

    @staticmethod
    @jax.jit
    def _transference_numbers_jit(
        charges: jax.Array,
        mobilities: jax.Array,
    ) -> Dict[str, jax.Array]:
        charges = jnp.asarray(charges, dtype=jnp.float64)
        mobilities = jnp.asarray(mobilities, dtype=jnp.float64)
        contributions = jnp.abs(charges) * mobilities
        total = jnp.sum(contributions)
        t_i = safe_div(contributions, total)
        return {"t_i": t_i, "total_contributions": contributions, "total": total}

    @staticmethod
    @jax.jit
    def _limiting_current_density_jit(
        concentrations: jax.Array,
        diffusion_coeffs: jax.Array,
        layer_thickness: jax.Array,
        charge_numbers: jax.Array,
        faraday_constant: jax.Array,
    ) -> jax.Array:
        concentrations = jnp.asarray(concentrations, dtype=jnp.float64)
        diffusion_coeffs = jnp.asarray(diffusion_coeffs, dtype=jnp.float64)
        layer_thickness = jnp.asarray(layer_thickness, dtype=jnp.float64)
        charge_numbers = jnp.asarray(charge_numbers, dtype=jnp.float64)
        faraday_constant = jnp.asarray(faraday_constant, dtype=jnp.float64)
        return safe_div(
            jnp.abs(charge_numbers)
            * faraday_constant
            * diffusion_coeffs
            * concentrations,
            layer_thickness,
            safe_default=0.0,
        )


@jax_tree
@dataclass
class PolarizationJAX:
    """Polarization EMF and decomposition voltage. Arts. 253-256.

    Fields:
        reversible_emf: Reversible EMF in abvolts.
        exchange_current_density: Exchange current density in abA/cm^2.
        transfer_coefficient: Charge transfer coefficient (default: 0.5).
        temperature: Temperature in Kelvin (default: 298.15).
    """

    reversible_emf: float
    exchange_current_density: float
    transfer_coefficient: float = 0.5
    temperature: float = 298.15

    def __post_init__(self) -> None:
        self.reversible_emf = jnp.asarray(self.reversible_emf, dtype=jnp.float64)
        self.exchange_current_density = jnp.asarray(
            self.exchange_current_density, dtype=jnp.float64
        )
        self.transfer_coefficient = jnp.asarray(
            self.transfer_coefficient, dtype=jnp.float64
        )
        self.temperature = jnp.asarray(self.temperature, dtype=jnp.float64)

    def activation_overpotential(self, current_density: jax.Array) -> jax.Array:
        """Activation overpotential: eta = (RT/F) * asinh(j/(2*j0))."""
        return self._activation_overpotential_jit(
            current_density,
            self.exchange_current_density,
            self.transfer_coefficient,
            self.temperature,
            R_GAS_CGS_JAX,
            FARADAY_CONSTANT_JAX,
        )

    def concentration_overpotential(
        self,
        bulk_conc: jax.Array,
        surface_conc: jax.Array,
        diffusion_coeff: jax.Array,
        diffusion_thickness: jax.Array,
        current_density: jax.Array,
        charge_number: jax.Array,
    ) -> jax.Array:
        """Concentration overpotential from mass transport limitation."""
        return self._concentration_overpotential_jit(
            bulk_conc,
            surface_conc,
            diffusion_coeff,
            diffusion_thickness,
            current_density,
            charge_number,
            self.temperature,
            R_GAS_CGS_JAX,
            FARADAY_CONSTANT_JAX,
        )

    def decomposition_voltage(
        self,
        anode_overpotential: jax.Array,
        cathode_overpotential: jax.Array,
        ohmic_drop: jax.Array,
    ) -> jax.Array:
        """Decomposition voltage: E_decomp = E_rev + eta_a + |eta_c| + IR."""
        return self._decomposition_voltage_jit(
            self.reversible_emf, anode_overpotential, cathode_overpotential, ohmic_drop
        )

    def total_polarization_emf(self, current_density: jax.Array) -> jax.Array:
        """Total polarization EMF: E_rev + activation overpotential."""
        eta_act = self.activation_overpotential(current_density)
        return self.reversible_emf + eta_act

    @staticmethod
    @jax.jit
    def _activation_overpotential_jit(
        current_density: jax.Array,
        exchange_current_density: jax.Array,
        transfer_coefficient: jax.Array,
        temperature: jax.Array,
        r_gas: jax.Array,
        faraday_constant: jax.Array,
    ) -> jax.Array:
        current_density = jnp.asarray(current_density, dtype=jnp.float64)
        exchange_current_density = jnp.asarray(
            exchange_current_density, dtype=jnp.float64
        )
        transfer_coefficient = jnp.asarray(transfer_coefficient, dtype=jnp.float64)
        temperature = jnp.asarray(temperature, dtype=jnp.float64)
        r_gas = jnp.asarray(r_gas, dtype=jnp.float64)
        faraday_constant = jnp.asarray(faraday_constant, dtype=jnp.float64)
        thermal_voltage = safe_div(r_gas * temperature, faraday_constant)
        ratio = safe_div(current_density, 2.0 * exchange_current_density)
        # Use asinh with safe guard for zero
        asinh_val = jnp.arcsinh(ratio)
        return safe_div(thermal_voltage * asinh_val, transfer_coefficient)

    @staticmethod
    @jax.jit
    def _concentration_overpotential_jit(
        bulk_conc: jax.Array,
        surface_conc: jax.Array,
        diffusion_coeff: jax.Array,
        diffusion_thickness: jax.Array,
        current_density: jax.Array,
        charge_number: jax.Array,
        temperature: jax.Array,
        r_gas: jax.Array,
        faraday_constant: jax.Array,
    ) -> jax.Array:
        bulk_conc = jnp.asarray(bulk_conc, dtype=jnp.float64)
        surface_conc = jnp.asarray(surface_conc, dtype=jnp.float64)
        diffusion_coeff = jnp.asarray(diffusion_coeff, dtype=jnp.float64)
        diffusion_thickness = jnp.asarray(diffusion_thickness, dtype=jnp.float64)
        current_density = jnp.asarray(current_density, dtype=jnp.float64)
        charge_number = jnp.asarray(charge_number, dtype=jnp.float64)
        temperature = jnp.asarray(temperature, dtype=jnp.float64)
        r_gas = jnp.asarray(r_gas, dtype=jnp.float64)
        faraday_constant = jnp.asarray(faraday_constant, dtype=jnp.float64)

        thermal_voltage = safe_div(r_gas * temperature, faraday_constant)
        abs_z = jnp.abs(charge_number)

        # Limiting current: i_L = |n|*F*D*c_bulk/delta
        i_limiting = safe_div(
            abs_z * faraday_constant * diffusion_coeff * bulk_conc, diffusion_thickness
        )

        # Use limiting current form when valid
        ratio = safe_div(current_density, i_limiting)
        log_term_limiting = safe_log(1.0 - ratio)

        # Direct concentration ratio form
        log_term_direct = safe_log(safe_div(surface_conc, bulk_conc))

        # Choose based on whether we're below limiting current
        use_limiting = (
            (i_limiting > 0) & (current_density < i_limiting) & (bulk_conc > 0)
        )
        log_term = jnp.where(use_limiting, log_term_limiting, log_term_direct)

        return safe_div(thermal_voltage * log_term, abs_z)

    @staticmethod
    @jax.jit
    def _decomposition_voltage_jit(
        reversible_emf: jax.Array,
        anode_overpotential: jax.Array,
        cathode_overpotential: jax.Array,
        ohmic_drop: jax.Array,
    ) -> jax.Array:
        reversible_emf = jnp.asarray(reversible_emf, dtype=jnp.float64)
        anode_overpotential = jnp.asarray(anode_overpotential, dtype=jnp.float64)
        cathode_overpotential = jnp.asarray(cathode_overpotential, dtype=jnp.float64)
        ohmic_drop = jnp.asarray(ohmic_drop, dtype=jnp.float64)
        return (
            reversible_emf
            + anode_overpotential
            + jnp.abs(cathode_overpotential)
            + ohmic_drop
        )


@jax_tree
@dataclass
class ElectrolysisCellJAX:
    """Complete electrolysis cell model. Arts. 249-263.

    Fields:
        electrode_area: Electrode area in cm^2.
        electrode_spacing: Distance between electrodes in cm.
        electrolyte_conductivity: Conductivity in abmho/cm.
        molar_mass: Molar mass of deposited substance in g/mol.
        valence: Valence of deposited ion.
        reversible_emf: Reversible EMF in abvolts.
        temperature: Temperature in Kelvin (default: 298.15).
    """

    electrode_area: float
    electrode_spacing: float
    electrolyte_conductivity: float
    molar_mass: float
    valence: float
    reversible_emf: float
    temperature: float = 298.15

    def __post_init__(self) -> None:
        self.electrode_area = jnp.asarray(self.electrode_area, dtype=jnp.float64)
        self.electrode_spacing = jnp.asarray(self.electrode_spacing, dtype=jnp.float64)
        self.electrolyte_conductivity = jnp.asarray(
            self.electrolyte_conductivity, dtype=jnp.float64
        )
        self.molar_mass = jnp.asarray(self.molar_mass, dtype=jnp.float64)
        self.valence = jnp.asarray(self.valence, dtype=jnp.float64)
        self.reversible_emf = jnp.asarray(self.reversible_emf, dtype=jnp.float64)
        self.temperature = jnp.asarray(self.temperature, dtype=jnp.float64)

    def cell_resistance(self) -> jax.Array:
        """Cell resistance: R = d / (sigma * A)."""
        return self._cell_resistance_jit(
            self.electrode_spacing, self.electrolyte_conductivity, self.electrode_area
        )

    def mass_deposited(self, current: jax.Array, time: jax.Array) -> jax.Array:
        """Mass deposited: m = I*t*M/(n*F)."""
        return self._mass_deposited_jit(
            current, time, self.molar_mass, self.valence, FARADAY_CONSTANT_JAX
        )

    def required_voltage(self, current: jax.Array) -> jax.Array:
        """Required voltage: E_rev + IR + overpotential."""
        return self._required_voltage_jit(
            current,
            self.reversible_emf,
            self.electrode_spacing,
            self.electrolyte_conductivity,
            self.electrode_area,
            R_GAS_CGS_JAX,
            FARADAY_CONSTANT_JAX,
            self.temperature,
        )

    def energy_per_gram(self, current: jax.Array) -> jax.Array:
        """Energy to deposit 1 gram: E = voltage * charge_per_gram."""
        return self._energy_per_gram_jit(
            current,
            self.reversible_emf,
            self.electrode_spacing,
            self.electrolyte_conductivity,
            self.electrode_area,
            self.molar_mass,
            self.valence,
            R_GAS_CGS_JAX,
            FARADAY_CONSTANT_JAX,
            self.temperature,
        )

    def analyze(self, current: jax.Array, time: jax.Array) -> Dict[str, Any]:
        """Comprehensive analysis of electrolysis cell operation."""
        return self._analyze_jit(
            current,
            time,
            self.electrode_area,
            self.electrode_spacing,
            self.electrolyte_conductivity,
            self.molar_mass,
            self.valence,
            self.reversible_emf,
            self.temperature,
            R_GAS_CGS_JAX,
            FARADAY_CONSTANT_JAX,
        )

    @staticmethod
    @jax.jit
    def _cell_resistance_jit(
        spacing: jax.Array,
        conductivity: jax.Array,
        area: jax.Array,
    ) -> jax.Array:
        spacing = jnp.asarray(spacing, dtype=jnp.float64)
        conductivity = jnp.asarray(conductivity, dtype=jnp.float64)
        area = jnp.asarray(area, dtype=jnp.float64)
        return safe_div(spacing, conductivity * area)

    @staticmethod
    @jax.jit
    def _mass_deposited_jit(
        current: jax.Array,
        time: jax.Array,
        molar_mass: jax.Array,
        valence: jax.Array,
        faraday_constant: jax.Array,
    ) -> jax.Array:
        current = jnp.asarray(current, dtype=jnp.float64)
        time = jnp.asarray(time, dtype=jnp.float64)
        molar_mass = jnp.asarray(molar_mass, dtype=jnp.float64)
        valence = jnp.asarray(valence, dtype=jnp.float64)
        faraday_constant = jnp.asarray(faraday_constant, dtype=jnp.float64)
        return safe_div(current * time * molar_mass, valence * faraday_constant)

    @staticmethod
    @jax.jit
    def _required_voltage_jit(
        current: jax.Array,
        reversible_emf: jax.Array,
        spacing: jax.Array,
        conductivity: jax.Array,
        area: jax.Array,
        r_gas: jax.Array,
        faraday_constant: jax.Array,
        temperature: jax.Array,
    ) -> jax.Array:
        current = jnp.asarray(current, dtype=jnp.float64)
        reversible_emf = jnp.asarray(reversible_emf, dtype=jnp.float64)
        spacing = jnp.asarray(spacing, dtype=jnp.float64)
        conductivity = jnp.asarray(conductivity, dtype=jnp.float64)
        area = jnp.asarray(area, dtype=jnp.float64)
        r_gas = jnp.asarray(r_gas, dtype=jnp.float64)
        faraday_constant = jnp.asarray(faraday_constant, dtype=jnp.float64)
        temperature = jnp.asarray(temperature, dtype=jnp.float64)

        # IR drop
        R = safe_div(spacing, conductivity * area)
        ir_drop = current * R

        # Simplified activation overpotential (assume j0=1e-6, alpha=0.5)
        j0 = jnp.array(1e-6, dtype=jnp.float64)
        alpha = jnp.array(0.5, dtype=jnp.float64)
        current_density = safe_div(current, area)
        thermal_voltage = safe_div(r_gas * temperature, faraday_constant)
        ratio = safe_div(current_density, 2.0 * j0)
        eta_act = safe_div(thermal_voltage * jnp.arcsinh(ratio), alpha)

        return reversible_emf + ir_drop + eta_act

    @staticmethod
    @jax.jit
    def _energy_per_gram_jit(
        current: jax.Array,
        reversible_emf: jax.Array,
        spacing: jax.Array,
        conductivity: jax.Array,
        area: jax.Array,
        molar_mass: jax.Array,
        valence: jax.Array,
        r_gas: jax.Array,
        faraday_constant: jax.Array,
        temperature: jax.Array,
    ) -> jax.Array:
        current = jnp.asarray(current, dtype=jnp.float64)
        reversible_emf = jnp.asarray(reversible_emf, dtype=jnp.float64)
        spacing = jnp.asarray(spacing, dtype=jnp.float64)
        conductivity = jnp.asarray(conductivity, dtype=jnp.float64)
        area = jnp.asarray(area, dtype=jnp.float64)
        molar_mass = jnp.asarray(molar_mass, dtype=jnp.float64)
        valence = jnp.asarray(valence, dtype=jnp.float64)
        r_gas = jnp.asarray(r_gas, dtype=jnp.float64)
        faraday_constant = jnp.asarray(faraday_constant, dtype=jnp.float64)
        temperature = jnp.asarray(temperature, dtype=jnp.float64)

        # Voltage
        R = safe_div(spacing, conductivity * area)
        ir_drop = current * R
        j0 = jnp.array(1e-6, dtype=jnp.float64)
        alpha = jnp.array(0.5, dtype=jnp.float64)
        current_density = safe_div(current, area)
        thermal_voltage = safe_div(r_gas * temperature, faraday_constant)
        ratio = safe_div(current_density, 2.0 * j0)
        eta_act = safe_div(thermal_voltage * jnp.arcsinh(ratio), alpha)
        voltage = reversible_emf + ir_drop + eta_act

        # Charge needed to deposit 1 gram: Q = 1*n*F/M
        charge_per_gram = safe_div(valence * faraday_constant, molar_mass)

        return voltage * charge_per_gram

    @staticmethod
    @jax.jit
    def _analyze_jit(
        current: jax.Array,
        time: jax.Array,
        area: jax.Array,
        spacing: jax.Array,
        conductivity: jax.Array,
        molar_mass: jax.Array,
        valence: jax.Array,
        reversible_emf: jax.Array,
        temperature: jax.Array,
        r_gas: jax.Array,
        faraday_constant: jax.Array,
    ) -> Dict[str, Any]:
        current = jnp.asarray(current, dtype=jnp.float64)
        time = jnp.asarray(time, dtype=jnp.float64)
        area = jnp.asarray(area, dtype=jnp.float64)
        spacing = jnp.asarray(spacing, dtype=jnp.float64)
        conductivity = jnp.asarray(conductivity, dtype=jnp.float64)
        molar_mass = jnp.asarray(molar_mass, dtype=jnp.float64)
        valence = jnp.asarray(valence, dtype=jnp.float64)
        reversible_emf = jnp.asarray(reversible_emf, dtype=jnp.float64)
        temperature = jnp.asarray(temperature, dtype=jnp.float64)
        r_gas = jnp.asarray(r_gas, dtype=jnp.float64)
        faraday_constant = jnp.asarray(faraday_constant, dtype=jnp.float64)

        # Cell resistance
        R = safe_div(spacing, conductivity * area)

        # Mass deposited
        mass = safe_div(current * time * molar_mass, valence * faraday_constant)

        # Charge passed
        charge = current * time

        # IR drop
        ir_drop = current * R

        # Overpotential
        j0 = jnp.array(1e-6, dtype=jnp.float64)
        alpha = jnp.array(0.5, dtype=jnp.float64)
        current_density = safe_div(current, area)
        thermal_voltage = safe_div(r_gas * temperature, faraday_constant)
        ratio = safe_div(current_density, 2.0 * j0)
        eta_act = safe_div(thermal_voltage * jnp.arcsinh(ratio), alpha)

        # Required voltage
        voltage = reversible_emf + ir_drop + eta_act

        # Energy
        energy = voltage * charge
        energy_per_gram = safe_div(energy, mass)
        power = voltage * current

        return {
            "mass_deposited": mass,
            "charge_passed": charge,
            "cell_resistance": R,
            "ir_drop": ir_drop,
            "overpotential": eta_act,
            "required_voltage": voltage,
            "energy_consumed": energy,
            "energy_per_gram": energy_per_gram,
            "power": power,
        }


# -- Standalone functions -------------------------------------------------------------


@maxwell_cite(
    249,
    250,
    part=2,
    chapter="Electrolysis",
    description="Faraday's first law: mass = I * t * Z",
)
def faraday_first_law_jax(
    current: jax.Array,
    time: jax.Array,
    Z: jax.Array,
) -> jax.Array:
    """Faraday's first law of electrolysis. Arts. 249-250.

    m = I * t * Z

    Args:
        current: Current in abamperes.
        time: Time in seconds.
        Z: Electrochemical equivalent in g/abC.

    Returns:
        Mass deposited in grams.
    """
    current = jnp.asarray(current, dtype=jnp.float64)
    time = jnp.asarray(time, dtype=jnp.float64)
    Z = jnp.asarray(Z, dtype=jnp.float64)
    return current * time * Z


@maxwell_cite(
    251,
    252,
    part=2,
    chapter="Electrolysis",
    description="Faraday's second law with molar mass and valence",
)
def faraday_second_law_jax(
    current: jax.Array,
    time: jax.Array,
    molar_mass: jax.Array,
    valence: jax.Array,
) -> jax.Array:
    """Faraday's second law of electrolysis. Arts. 251-252.

    m = I * t * M / (n * F)

    Args:
        current: Current in abamperes.
        time: Time in seconds.
        molar_mass: Molar mass in g/mol.
        valence: Valence (number of electrons).

    Returns:
        Mass deposited in grams.
    """
    current = jnp.asarray(current, dtype=jnp.float64)
    time = jnp.asarray(time, dtype=jnp.float64)
    molar_mass = jnp.asarray(molar_mass, dtype=jnp.float64)
    valence = jnp.asarray(valence, dtype=jnp.float64)
    return safe_div(current * time * molar_mass, valence * FARADAY_CONSTANT_JAX)


@maxwell_cite(
    251,
    part=2,
    chapter="Electrolysis",
    description="Electrochemical equivalent: Z = M/(n*F)",
)
def electrochemical_equivalent_jax(
    molar_mass: jax.Array,
    valence: jax.Array,
) -> jax.Array:
    """Electrochemical equivalent. Art. 251.

    Z = M / (n * F)

    Args:
        molar_mass: Molar mass in g/mol.
        valence: Valence.

    Returns:
        Electrochemical equivalent in g/abC.
    """
    molar_mass = jnp.asarray(molar_mass, dtype=jnp.float64)
    valence = jnp.asarray(valence, dtype=jnp.float64)
    return safe_div(molar_mass, valence * FARADAY_CONSTANT_JAX)


@maxwell_cite(
    253,
    254,
    part=2,
    chapter="Electrolysis",
    description="Polarization EMF including activation overpotential",
)
def polarization_emf_jax(
    reversible_potential: jax.Array,
    current_density: jax.Array,
    exchange_current_density: jax.Array,
    transfer_coefficient: jax.Array,
    temperature: jax.Array,
) -> jax.Array:
    """Total polarization EMF. Arts. 253-254.

    E_pol = E_rev + (RT/F) * asinh(j/(2*j0)) / alpha

    Args:
        reversible_potential: Reversible potential in abvolts.
        current_density: Current density in abA/cm^2.
        exchange_current_density: Exchange current density in abA/cm^2.
        transfer_coefficient: Transfer coefficient.
        temperature: Temperature in K.

    Returns:
        Total polarization EMF in abvolts.
    """
    reversible_potential = jnp.asarray(reversible_potential, dtype=jnp.float64)
    current_density = jnp.asarray(current_density, dtype=jnp.float64)
    exchange_current_density = jnp.asarray(exchange_current_density, dtype=jnp.float64)
    transfer_coefficient = jnp.asarray(transfer_coefficient, dtype=jnp.float64)
    temperature = jnp.asarray(temperature, dtype=jnp.float64)

    thermal_voltage = safe_div(R_GAS_CGS_JAX * temperature, FARADAY_CONSTANT_JAX)
    ratio = safe_div(current_density, 2.0 * exchange_current_density)
    eta_act = safe_div(thermal_voltage * jnp.arcsinh(ratio), transfer_coefficient)
    return reversible_potential + eta_act


@maxwell_cite(
    255,
    256,
    part=2,
    chapter="Electrolysis",
    description="Decomposition voltage for electrolysis",
)
def decomposition_voltage_jax(
    reversible_emf: jax.Array,
    anode_overpotential: jax.Array,
    cathode_overpotential: jax.Array,
    ohmic_drop: jax.Array,
) -> jax.Array:
    """Decomposition voltage. Arts. 255-256.

    V_decomp = E_rev + eta_a + |eta_c| + IR

    Args:
        reversible_emf: Reversible EMF in abvolts.
        anode_overpotential: Anode overpotential in abvolts.
        cathode_overpotential: Cathode overpotential in abvolts.
        ohmic_drop: Ohmic drop in abvolts.

    Returns:
        Decomposition voltage in abvolts.
    """
    reversible_emf = jnp.asarray(reversible_emf, dtype=jnp.float64)
    anode_overpotential = jnp.asarray(anode_overpotential, dtype=jnp.float64)
    cathode_overpotential = jnp.asarray(cathode_overpotential, dtype=jnp.float64)
    ohmic_drop = jnp.asarray(ohmic_drop, dtype=jnp.float64)
    return (
        reversible_emf
        + anode_overpotential
        + jnp.abs(cathode_overpotential)
        + ohmic_drop
    )


@maxwell_cite(
    257,
    258,
    259,
    part=2,
    chapter="Electrolysis",
    description="Ion migration velocity in electric field",
)
def ion_migration_velocity_jax(
    ion_mobility: jax.Array,
    electric_field: jax.Array,
    charge_number: jax.Array,
) -> jax.Array:
    """Ion migration velocity. Arts. 257-259.

    v = u * z * E

    Args:
        ion_mobility: Ion mobility in cm^2/(abV*s).
        electric_field: Electric field in abV/cm.
        charge_number: Charge number of the ion.

    Returns:
        Migration velocity in cm/s.
    """
    ion_mobility = jnp.asarray(ion_mobility, dtype=jnp.float64)
    electric_field = jnp.asarray(electric_field, dtype=jnp.float64)
    charge_number = jnp.asarray(charge_number, dtype=jnp.float64)
    return ion_mobility * charge_number * electric_field


@maxwell_cite(
    260,
    261,
    part=2,
    chapter="Electrolysis",
    description="Electrolyte conductivity from ion properties",
)
def electrolyte_conductivity_jax(
    concentrations: jax.Array,
    charge_numbers: jax.Array,
    mobilities: jax.Array,
) -> jax.Array:
    """Electrolyte conductivity. Arts. 260-261.

    sigma = F * sum(c_i * |z_i| * u_i)

    Args:
        concentrations: Ion concentrations (mol/cm^3).
        charge_numbers: Ion charge numbers.
        mobilities: Ion mobilities (cm^2/(abV*s)).

    Returns:
        Conductivity in abmho/cm.
    """
    concentrations = jnp.asarray(concentrations, dtype=jnp.float64)
    charge_numbers = jnp.asarray(charge_numbers, dtype=jnp.float64)
    mobilities = jnp.asarray(mobilities, dtype=jnp.float64)
    return FARADAY_CONSTANT_JAX * jnp.sum(
        concentrations * jnp.abs(charge_numbers) * mobilities
    )


@maxwell_cite(
    262,
    263,
    part=2,
    chapter="Electrolysis",
    description="Kohlrausch's law of independent migration",
)
def kohlrausch_law_jax(
    limiting_molar_conductivity: jax.Array,
    concentration: jax.Array,
    kohlrausch_coeff: jax.Array,
) -> jax.Array:
    """Kohlrausch's law. Arts. 262-263.

    Lambda_m = Lambda_m^0 - K * sqrt(c)

    Args:
        limiting_molar_conductivity: Lambda_m^0 in abmho*cm^2/mol.
        concentration: Concentration in mol/cm^3.
        kohlrausch_coeff: Kohlrausch coefficient K.

    Returns:
        Molar conductivity in abmho*cm^2/mol.
    """
    limiting_molar_conductivity = jnp.asarray(
        limiting_molar_conductivity, dtype=jnp.float64
    )
    concentration = jnp.asarray(concentration, dtype=jnp.float64)
    kohlrausch_coeff = jnp.asarray(kohlrausch_coeff, dtype=jnp.float64)
    sqrt_c = safe_sqrt(concentration)
    return limiting_molar_conductivity - kohlrausch_coeff * sqrt_c


@maxwell_cite(
    260,
    261,
    262,
    part=2,
    chapter="Electrolysis",
    description="Concentration polarization overpotential",
)
def concentration_polarization_jax(
    bulk_conc: jax.Array,
    surface_conc: jax.Array,
    diffusion_coeff: jax.Array,
    diffusion_thickness: jax.Array,
    current_density: jax.Array,
    charge_number: jax.Array,
    temperature: jax.Array,
) -> jax.Array:
    """Concentration polarization. Arts. 260-262.

    eta_conc = (RT/nF) * ln(c_surface/c_bulk) or (RT/nF) * ln(1 - i/i_L)

    Args:
        bulk_conc: Bulk concentration in mol/cm^3.
        surface_conc: Surface concentration in mol/cm^3.
        diffusion_coeff: Diffusion coefficient in cm^2/s.
        diffusion_thickness: Diffusion layer thickness in cm.
        current_density: Current density in abA/cm^2.
        charge_number: Charge number.
        temperature: Temperature in K.

    Returns:
        Concentration overpotential in abvolts.
    """
    bulk_conc = jnp.asarray(bulk_conc, dtype=jnp.float64)
    surface_conc = jnp.asarray(surface_conc, dtype=jnp.float64)
    diffusion_coeff = jnp.asarray(diffusion_coeff, dtype=jnp.float64)
    diffusion_thickness = jnp.asarray(diffusion_thickness, dtype=jnp.float64)
    current_density = jnp.asarray(current_density, dtype=jnp.float64)
    charge_number = jnp.asarray(charge_number, dtype=jnp.float64)
    temperature = jnp.asarray(temperature, dtype=jnp.float64)

    thermal_voltage = safe_div(R_GAS_CGS_JAX * temperature, FARADAY_CONSTANT_JAX)
    abs_z = jnp.abs(charge_number)

    # Limiting current density
    i_limiting = safe_div(
        abs_z * FARADAY_CONSTANT_JAX * diffusion_coeff * bulk_conc, diffusion_thickness
    )

    # Two forms of log term
    ratio = safe_div(current_density, i_limiting)
    log_term_limiting = safe_log(1.0 - ratio)
    log_term_direct = safe_log(safe_div(surface_conc, bulk_conc))

    # Choose based on conditions
    use_limiting = (i_limiting > 0) & (current_density < i_limiting) & (bulk_conc > 0)
    log_term = jnp.where(use_limiting, log_term_limiting, log_term_direct)

    return safe_div(thermal_voltage * log_term, abs_z)


@maxwell_cite(
    255,
    256,
    257,
    258,
    part=2,
    chapter="Electrolysis",
    description="Back EMF in a voltaic battery",
)
def battery_back_emf_jax(
    reversible_emf: jax.Array,
    internal_resistance: jax.Array,
    current: jax.Array,
    polarization_coeff: jax.Array,
) -> jax.Array:
    """Battery back EMF and terminal voltage. Arts. 255-258.

    V_terminal = E_rev - I*R - k*I

    Args:
        reversible_emf: Reversible EMF in abvolts.
        internal_resistance: Internal resistance in abohms.
        current: Current in abamperes.
        polarization_coeff: Polarization coefficient in abohms.

    Returns:
        Terminal voltage in abvolts.
    """
    reversible_emf = jnp.asarray(reversible_emf, dtype=jnp.float64)
    internal_resistance = jnp.asarray(internal_resistance, dtype=jnp.float64)
    current = jnp.asarray(current, dtype=jnp.float64)
    polarization_coeff = jnp.asarray(polarization_coeff, dtype=jnp.float64)
    return reversible_emf - current * internal_resistance - polarization_coeff * current


@maxwell_cite(
    257,
    258,
    259,
    part=2,
    chapter="Electrolysis",
    description="Transference numbers from ionic conductivities",
)
def transference_number_jax(
    lambda_cation: jax.Array,
    lambda_anion: jax.Array,
) -> Dict[str, jax.Array]:
    """Transference numbers. Arts. 257-259.

    t_+ = lambda_+ / (lambda_+ + lambda_-)
    t_- = lambda_- / (lambda_+ + lambda_-)

    Args:
        lambda_cation: Limiting ionic conductivity of cation.
        lambda_anion: Limiting ionic conductivity of anion.

    Returns:
        Dictionary with t_cation, t_anion, Lambda_0.
    """
    lambda_cation = jnp.asarray(lambda_cation, dtype=jnp.float64)
    lambda_anion = jnp.asarray(lambda_anion, dtype=jnp.float64)
    Lambda_0 = lambda_cation + lambda_anion
    t_cation = safe_div(lambda_cation, Lambda_0)
    t_anion = safe_div(lambda_anion, Lambda_0)
    return {"t_cation": t_cation, "t_anion": t_anion, "Lambda_0": Lambda_0}


@maxwell_cite(
    249,
    250,
    251,
    252,
    253,
    254,
    255,
    256,
    257,
    258,
    259,
    260,
    261,
    262,
    263,
    part=2,
    chapter="Electrolysis",
    description="Verify electrolysis relations",
)
def verify_electrolysis_jax(
    tol: float = 1e-10,
) -> Dict[str, Any]:
    """Verify electrolysis consistency. Arts. 249-263.

    Checks:
    1. Faraday's first and second law consistency
    2. Mass-charge roundtrip
    3. Transference number sum
    4. Decomposition voltage composition

    Args:
        tol: Tolerance for verification.

    Returns:
        Dictionary with verification results.
    """
    # Test 1: Faraday's laws consistency
    I = jnp.array(1.0, dtype=jnp.float64)
    t = jnp.array(100.0, dtype=jnp.float64)
    M = jnp.array(107.87, dtype=jnp.float64)  # Silver
    n = jnp.array(1.0, dtype=jnp.float64)

    # Via first law (with Z)
    Z = electrochemical_equivalent_jax(M, n)
    m_first = faraday_first_law_jax(I, t, Z)

    # Via second law
    m_second = faraday_second_law_jax(I, t, M, n)

    first_law_ok = jnp.abs(m_first - m_second) < tol

    # Test 2: Mass-charge roundtrip
    Q = I * t
    mass = faraday_second_law_jax(I, t, M, n)
    Q_recovered = FaradayLawsJAX._required_charge_jit(mass, M, n, FARADAY_CONSTANT_JAX)
    roundtrip_ok = jnp.abs(Q - Q_recovered) < tol

    # Test 3: Transference numbers sum to 1
    lambda_cu = jnp.array(54.0, dtype=jnp.float64)
    lambda_so4 = jnp.array(80.0, dtype=jnp.float64)
    t_numbers = transference_number_jax(lambda_cu, lambda_so4)
    t_sum = t_numbers["t_cation"] + t_numbers["t_anion"]
    transference_ok = jnp.abs(t_sum - 1.0) < tol

    # Test 4: Decomposition voltage consistency
    E_rev = jnp.array(1.23e8, dtype=jnp.float64)
    eta_a = jnp.array(0.4e8, dtype=jnp.float64)
    eta_c = jnp.array(-0.1e8, dtype=jnp.float64)
    ir = jnp.array(0.05e8, dtype=jnp.float64)
    V_decomp = decomposition_voltage_jax(E_rev, eta_a, eta_c, ir)
    expected_decomp = E_rev + eta_a + jnp.abs(eta_c) + ir
    decomp_ok = jnp.abs(V_decomp - expected_decomp) < tol

    verified = bool(first_law_ok & roundtrip_ok & transference_ok & decomp_ok)

    return {
        "first_law_ok": bool(first_law_ok),
        "roundtrip_ok": bool(roundtrip_ok),
        "transference_ok": bool(transference_ok),
        "decomposition_ok": bool(decomp_ok),
        "m_first": float(m_first),
        "m_second": float(m_second),
        "Q_recovered": float(Q_recovered),
        "t_sum": float(t_sum),
        "V_decomp": float(V_decomp),
        "verified": verified,
    }

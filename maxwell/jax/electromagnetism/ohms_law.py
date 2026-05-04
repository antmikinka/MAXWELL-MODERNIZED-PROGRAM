"""JAX Ohm's law -- Part II Electrokinematics (Arts. 230-280).

Ohm's law, resistance, conductivity, and power dissipation implemented
with JAX pytree support for JIT, autodiff, and vectorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import jax
import jax.numpy as jnp

from maxwell.config.conventions import maxwell_cite
from maxwell.jax._compat import jax_tree, safe_div

__all__ = [
    "OhmsLawJAX",
    "ResistanceJAX",
    "ConductivityJAX",
    "PowerDissipationJAX",
    "calc_voltage_jax",
    "calc_current_jax",
    "calc_resistance_jax",
    "calc_conductance_jax",
    "calc_resistivity_jax",
    "calc_conductivity_jax",
    "series_resistance_jax",
    "parallel_resistance_jax",
    "temperature_corrected_resistance_jax",
    "calc_power_from_IV_jax",
    "calc_power_from_I2R_jax",
    "calc_power_from_V2R_jax",
    "verify_ohms_law_jax",
    "analyze_ohms_law_jax",
]


# -- Data classes -------------------------------------------------------------------

@jax_tree
@dataclass
class OhmsLawJAX:
    """Ohm's law calculator (JAX-compatible pytree).

    Art. 230-280: The fundamental relationship V = I * R between voltage,
    current, and resistance in electrical circuits.

    Fields:
        voltage: Voltage in volts (V).
        current: Current in amperes (A).
        resistance: Resistance in ohms (R).
    """

    voltage: float = 0.0
    current: float = 0.0
    resistance: float = 0.0

    def __post_init__(self) -> None:
        self.voltage = jnp.asarray(self.voltage, dtype=jnp.float64)
        self.current = jnp.asarray(self.current, dtype=jnp.float64)
        self.resistance = jnp.asarray(self.resistance, dtype=jnp.float64)

    @property
    def computed_voltage(self) -> jax.Array:
        """V = I * R."""
        return self._voltage_jit(self.current, self.resistance)

    @property
    def computed_current(self) -> jax.Array:
        """I = V / R."""
        return self._current_jit(self.voltage, self.resistance)

    @property
    def computed_resistance(self) -> jax.Array:
        """R = V / I."""
        return self._resistance_jit(self.voltage, self.current)

    @property
    def conductance(self) -> jax.Array:
        """G = 1 / R."""
        return safe_div(jnp.array(1.0, dtype=jnp.float64), self.resistance)

    @property
    def power(self) -> jax.Array:
        """P = V * I."""
        return self.voltage * self.current

    def voltage_from(self, I: float, R: float) -> jax.Array:
        """Calculate V = I * R."""
        return self._voltage_jit(I, R)

    def current_from(self, V: float, R: float) -> jax.Array:
        """Calculate I = V / R."""
        return self._current_jit(V, R)

    def resistance_from(self, V: float, I: float) -> jax.Array:
        """Calculate R = V / I."""
        return self._resistance_jit(V, I)

    @staticmethod
    @jax.jit
    def _voltage_jit(I: float, R: float) -> jax.Array:
        """V = I * R."""
        I = jnp.asarray(I, dtype=jnp.float64)
        R = jnp.asarray(R, dtype=jnp.float64)
        return I * R

    @staticmethod
    @jax.jit
    def _current_jit(V: float, R: float) -> jax.Array:
        """I = V / R."""
        V = jnp.asarray(V, dtype=jnp.float64)
        R = jnp.asarray(R, dtype=jnp.float64)
        return safe_div(V, R)

    @staticmethod
    @jax.jit
    def _resistance_jit(V: float, I: float) -> jax.Array:
        """R = V / I."""
        V = jnp.asarray(V, dtype=jnp.float64)
        I = jnp.asarray(I, dtype=jnp.float64)
        return safe_div(V, I)


@jax_tree
@dataclass
class ResistanceJAX:
    """Resistance calculator with temperature correction (JAX-compatible pytree).

    Art. 244-250: Resistance depends on material properties, geometry,
    and temperature. R(T) = R0 * (1 + alpha * (T - T0)).

    Fields:
        base_resistance: Base resistance at reference temperature (ohms).
        temperature_coefficient: Temperature coefficient alpha (per degree C).
    """

    base_resistance: float = 0.0
    temperature_coefficient: float = 0.004

    def __post_init__(self) -> None:
        self.base_resistance = jnp.asarray(self.base_resistance, dtype=jnp.float64)
        self.temperature_coefficient = jnp.asarray(self.temperature_coefficient, dtype=jnp.float64)

    def series_combine(self, resistances: jax.Array) -> jax.Array:
        """Total resistance in series: R_total = sum(R_i)."""
        return self._series_jit(resistances)

    def parallel_combine(self, resistances: jax.Array) -> jax.Array:
        """Total resistance in parallel: 1/R_total = sum(1/R_i)."""
        return self._parallel_jit(resistances)

    def at_temperature(self, T: float, ref_temp: float = 20.0) -> jax.Array:
        """Temperature-corrected resistance: R(T) = R0 * (1 + alpha * (T - T0))."""
        return self._temp_correct_jit(self.base_resistance, self.temperature_coefficient, T, ref_temp)

    @staticmethod
    @jax.jit
    def _series_jit(resistances: jax.Array) -> jax.Array:
        """R_total = sum(R_i)."""
        resistances = jnp.asarray(resistances, dtype=jnp.float64)
        return jnp.sum(resistances)

    @staticmethod
    @jax.jit
    def _parallel_jit(resistances: jax.Array) -> jax.Array:
        """R_total = 1 / sum(1/R_i)."""
        resistances = jnp.asarray(resistances, dtype=jnp.float64)
        inv_sum = jnp.sum(safe_div(jnp.array(1.0, dtype=jnp.float64), resistances))
        return safe_div(jnp.array(1.0, dtype=jnp.float64), inv_sum)

    @staticmethod
    @jax.jit
    def _temp_correct_jit(R0: float, alpha: float, T: float, T0: float) -> jax.Array:
        """R(T) = R0 * (1 + alpha * (T - T0))."""
        R0 = jnp.asarray(R0, dtype=jnp.float64)
        alpha = jnp.asarray(alpha, dtype=jnp.float64)
        T = jnp.asarray(T, dtype=jnp.float64)
        T0 = jnp.asarray(T0, dtype=jnp.float64)
        return R0 * (1.0 + alpha * (T - T0))


@jax_tree
@dataclass
class ConductivityJAX:
    """Conductivity and resistivity converter (JAX-compatible pytree).

    Art. 251-260: Conductivity sigma is the reciprocal of resistivity rho.
    Current density J = sigma * E, electric field E = J / sigma.

    Fields:
        conductivity: Electrical conductivity sigma (S/m).
    """

    conductivity: float = 0.0

    def __post_init__(self) -> None:
        self.conductivity = jnp.asarray(self.conductivity, dtype=jnp.float64)

    @property
    def resistivity(self) -> jax.Array:
        """rho = 1 / sigma."""
        return safe_div(jnp.array(1.0, dtype=jnp.float64), self.conductivity)

    def current_density(self, E: jax.Array) -> jax.Array:
        """J = sigma * E."""
        return self._current_density_jit(self.conductivity, E)

    def electric_field(self, J: jax.Array) -> jax.Array:
        """E = J / sigma."""
        return self._electric_field_jit(J, self.conductivity)

    @classmethod
    def from_resistivity(cls, rho: float) -> "ConductivityJAX":
        """Create from resistivity: sigma = 1 / rho."""
        sigma = cls._conductivity_from_resistivity_jit(rho)
        return cls(conductivity=float(sigma))

    @staticmethod
    @jax.jit
    def _conductivity_from_resistivity_jit(rho: float) -> jax.Array:
        """sigma = 1 / rho."""
        rho = jnp.asarray(rho, dtype=jnp.float64)
        return safe_div(jnp.array(1.0, dtype=jnp.float64), rho)

    @staticmethod
    @jax.jit
    def _resistivity_from_conductivity_jit(sigma: float) -> jax.Array:
        """rho = 1 / sigma."""
        sigma = jnp.asarray(sigma, dtype=jnp.float64)
        return safe_div(jnp.array(1.0, dtype=jnp.float64), sigma)

    @staticmethod
    @jax.jit
    def _current_density_jit(sigma: float, E: jax.Array) -> jax.Array:
        """J = sigma * E."""
        sigma = jnp.asarray(sigma, dtype=jnp.float64)
        E = jnp.asarray(E, dtype=jnp.float64)
        return sigma * E

    @staticmethod
    @jax.jit
    def _electric_field_jit(J: jax.Array, sigma: float) -> jax.Array:
        """E = J / sigma."""
        J = jnp.asarray(J, dtype=jnp.float64)
        sigma = jnp.asarray(sigma, dtype=jnp.float64)
        return safe_div(J, sigma)


@jax_tree
@dataclass
class PowerDissipationJAX:
    """Power dissipation calculator (JAX-compatible pytree).

    Art. 261-270: Joule heating P = I^2 * R = V^2 / R = V * I.
    Energy dissipated as heat in a resistive element.

    Fields:
        resistance: Resistance in ohms.
    """

    resistance: float = 0.0

    def __post_init__(self) -> None:
        self.resistance = jnp.asarray(self.resistance, dtype=jnp.float64)

    def from_current(self, I: float) -> jax.Array:
        """P = I^2 * R."""
        return self._i2r_jit(I, self.resistance)

    def from_voltage(self, V: float) -> jax.Array:
        """P = V^2 / R."""
        return self._v2r_jit(V, self.resistance)

    def from_IV(self, V: float, I: float) -> jax.Array:
        """P = V * I."""
        return self._iv_jit(V, I)

    @staticmethod
    @jax.jit
    def _i2r_jit(I: float, R: float) -> jax.Array:
        """P = I^2 * R."""
        I = jnp.asarray(I, dtype=jnp.float64)
        R = jnp.asarray(R, dtype=jnp.float64)
        return I ** 2 * R

    @staticmethod
    @jax.jit
    def _v2r_jit(V: float, R: float) -> jax.Array:
        """P = V^2 / R."""
        V = jnp.asarray(V, dtype=jnp.float64)
        R = jnp.asarray(R, dtype=jnp.float64)
        return safe_div(V ** 2, R)

    @staticmethod
    @jax.jit
    def _iv_jit(V: float, I: float) -> jax.Array:
        """P = V * I."""
        V = jnp.asarray(V, dtype=jnp.float64)
        I = jnp.asarray(I, dtype=jnp.float64)
        return V * I


# -- Standalone functions -------------------------------------------------------------

@maxwell_cite(230, part=2, chapter="Electrokinematics", description="Ohm's law: V = I * R")
def calc_voltage_jax(I: float, R: float) -> jax.Array:
    """Calculate voltage from current and resistance. Art. 230.

    V = I * R
    """
    return OhmsLawJAX._voltage_jit(I, R)


@maxwell_cite(230, part=2, chapter="Electrokinematics", description="Ohm's law: I = V / R")
def calc_current_jax(V: float, R: float) -> jax.Array:
    """Calculate current from voltage and resistance. Art. 230.

    I = V / R
    """
    V_arr = jnp.asarray(V, dtype=jnp.float64)
    R_arr = jnp.asarray(R, dtype=jnp.float64)
    return safe_div(V_arr, R_arr)


@maxwell_cite(230, part=2, chapter="Electrokinematics", description="Ohm's law: R = V / I")
def calc_resistance_jax(V: float, I: float) -> jax.Array:
    """Calculate resistance from voltage and current. Art. 230.

    R = V / I
    """
    V_arr = jnp.asarray(V, dtype=jnp.float64)
    I_arr = jnp.asarray(I, dtype=jnp.float64)
    return safe_div(V_arr, I_arr)


@maxwell_cite(244, part=2, chapter="Conduction and Resistance", description="Conductance G = 1/R")
def calc_conductance_jax(R: float) -> jax.Array:
    """Calculate conductance from resistance. Art. 244.

    G = 1 / R
    """
    R_arr = jnp.asarray(R, dtype=jnp.float64)
    return safe_div(jnp.array(1.0, dtype=jnp.float64), R_arr)


@maxwell_cite(251, part=2, chapter="Conductivity", description="Resistivity rho = 1/sigma")
def calc_resistivity_jax(sigma: float) -> jax.Array:
    """Calculate resistivity from conductivity. Art. 251.

    rho = 1 / sigma
    """
    sigma_arr = jnp.asarray(sigma, dtype=jnp.float64)
    return safe_div(jnp.array(1.0, dtype=jnp.float64), sigma_arr)


@maxwell_cite(251, part=2, chapter="Conductivity", description="Conductivity sigma = 1/rho")
def calc_conductivity_jax(rho: float) -> jax.Array:
    """Calculate conductivity from resistivity. Art. 251.

    sigma = 1 / rho
    """
    rho_arr = jnp.asarray(rho, dtype=jnp.float64)
    return safe_div(jnp.array(1.0, dtype=jnp.float64), rho_arr)


@maxwell_cite(245, part=2, chapter="Series Resistance", description="Series resistance: R_total = sum(R_i)")
def series_resistance_jax(resistances: jax.Array) -> jax.Array:
    """Calculate total resistance for series connection. Art. 245.

    R_total = sum(R_i)
    """
    return ResistanceJAX._series_jit(resistances)


@maxwell_cite(246, part=2, chapter="Parallel Resistance", description="Parallel resistance: 1/R_total = sum(1/R_i)")
def parallel_resistance_jax(resistances: jax.Array) -> jax.Array:
    """Calculate total resistance for parallel connection. Art. 246.

    1 / R_total = sum(1 / R_i)
    """
    return ResistanceJAX._parallel_jit(resistances)


@maxwell_cite(250, part=2, chapter="Temperature Dependence", description="Temperature-corrected resistance")
def temperature_corrected_resistance_jax(
    R0: float, alpha: float, T: float, T0: float = 20.0
) -> jax.Array:
    """Calculate temperature-corrected resistance. Art. 250.

    R(T) = R0 * (1 + alpha * (T - T0))
    """
    return ResistanceJAX._temp_correct_jit(R0, alpha, T, T0)


@maxwell_cite(261, part=2, chapter="Power Dissipation", description="Power from voltage and current")
def calc_power_from_IV_jax(V: float, I: float) -> jax.Array:
    """Calculate power from voltage and current. Art. 261.

    P = V * I
    """
    return PowerDissipationJAX._iv_jit(V, I)


@maxwell_cite(262, part=2, chapter="Joule Heating", description="Power from current squared times resistance")
def calc_power_from_I2R_jax(I: float, R: float) -> jax.Array:
    """Calculate power from current and resistance (Joule heating). Art. 262.

    P = I^2 * R
    """
    return PowerDissipationJAX._i2r_jit(I, R)


@maxwell_cite(263, part=2, chapter="Power Dissipation", description="Power from voltage squared over resistance")
def calc_power_from_V2R_jax(V: float, R: float) -> jax.Array:
    """Calculate power from voltage and resistance. Art. 263.

    P = V^2 / R
    """
    return PowerDissipationJAX._v2r_jit(V, R)


@maxwell_cite(230, 244, 261, 262, 263, part=2, chapter="Ohm's Law Verification", description="Verify Ohm's law consistency")
def verify_ohms_law_jax(
    V: float = 10.0,
    I: float = 2.0,
    R: float = 5.0,
    tolerance: float = 1e-10,
) -> Dict[str, Any]:
    """Verify Ohm's law consistency across all formulations. Arts. 230, 244, 261-263.

    Checks that V = IR, I = V/R, R = V/I, and power formulas agree.
    """
    V_arr = jnp.asarray(V, dtype=jnp.float64)
    I_arr = jnp.asarray(I, dtype=jnp.float64)
    R_arr = jnp.asarray(R, dtype=jnp.float64)

    V_from_IR = calc_voltage_jax(I, R)
    I_from_VR = calc_current_jax(V, R)
    R_from_VI = calc_resistance_jax(V, I)

    power_IV = calc_power_from_IV_jax(V, I)
    power_I2R = calc_power_from_I2R_jax(I, R)
    power_V2R = calc_power_from_V2R_jax(V, R)

    V_close = jnp.abs(V_from_IR - V_arr) < tolerance
    I_close = jnp.abs(I_from_VR - I_arr) < tolerance
    R_close = jnp.abs(R_from_VI - R_arr) < tolerance
    power_close = (jnp.abs(power_IV - power_I2R) < tolerance) & (jnp.abs(power_IV - power_V2R) < tolerance)

    verified = V_close & I_close & R_close & power_close

    return {
        "V_from_IR": V_from_IR,
        "I_from_VR": I_from_VR,
        "R_from_VI": R_from_VI,
        "power_IV": power_IV,
        "power_I2R": power_I2R,
        "power_V2R": power_V2R,
        "verified": verified,
    }


@maxwell_cite(230, 244, 251, 261, part=2, chapter="Ohm's Law Analysis", description="Comprehensive Ohm's law analysis")
def analyze_ohms_law_jax(
    voltage: Optional[float] = None,
    current: Optional[float] = None,
    resistance: Optional[float] = None,
    conductivity: Optional[float] = None,
) -> Dict[str, Any]:
    """Comprehensive Ohm's law analysis. Arts. 230, 244, 251, 261.

    Computes all available values from the provided subset of parameters.
    """
    result: Dict[str, Any] = {}

    if voltage is not None and current is not None:
        result["resistance"] = calc_resistance_jax(voltage, current)
        result["power_IV"] = calc_power_from_IV_jax(voltage, current)
        result["power_I2R"] = calc_power_from_I2R_jax(current, float(result["resistance"]))
        result["power_V2R"] = calc_power_from_V2R_jax(voltage, float(result["resistance"]))

    if voltage is not None and resistance is not None:
        result["current"] = calc_current_jax(voltage, resistance)
        result["conductance"] = calc_conductance_jax(resistance)

    if current is not None and resistance is not None:
        result["voltage"] = calc_voltage_jax(current, resistance)
        result["power_I2R"] = calc_power_from_I2R_jax(current, resistance)

    if conductivity is not None:
        result["resistivity"] = calc_resistivity_jax(conductivity)

    return result

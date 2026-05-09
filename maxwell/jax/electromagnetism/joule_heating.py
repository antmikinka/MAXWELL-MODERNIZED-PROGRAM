"""JAX Joule heating and substance resistance -- Part II (Arts. 351-370).

Joule heating (Arts. 351-358): energy dissipation in conductors, heat
generation, Joule's law P = I^2 * R.

Resistance of substances (Arts. 359-370): temperature dependence of
resistivity, geometry-based resistance calculations.

Implemented with JAX pytree support for JIT compilation, automatic
differentiation, and vectorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import jax
import jax.numpy as jnp

from maxwell.config.conventions import maxwell_cite
from maxwell.jax._compat import jax_tree, safe_div, safe_sqrt

__all__ = [
    "JouleHeatingJAX",
    "HeatDissipationJAX",
    "SubstanceResistanceJAX",
    "joule_heating_power_jax",
    "joule_energy_dissipated_jax",
    "joule_power_density_jax",
    "joule_temperature_rise_jax",
    "joule_heating_from_voltage_jax",
    "cooling_rate_jax",
    "steady_state_temperature_jax",
    "substance_resistivity_at_temp_jax",
    "substance_resistance_jax",
    "verify_joule_heating_jax",
    "analyze_joule_heating_jax",
]


# -- Data classes -------------------------------------------------------------------


@jax_tree
@dataclass
class JouleHeatingJAX:
    """Joule heating: P = I^2 * R energy dissipation as heat. Arts. 351-358.

    Fields:
        resistance: Resistance in abohms.
    """

    resistance: float = 0.0

    def __post_init__(self) -> None:
        self.resistance = jnp.asarray(self.resistance, dtype=jnp.float64)

    def power(self, current: jax.Array) -> jax.Array:
        """P = I^2 * R (erg/s)."""
        return self._power_jit(current, self.resistance)

    def energy_dissipated(self, current: jax.Array, time: jax.Array) -> jax.Array:
        """E = I^2 * R * t (erg)."""
        return self._energy_jit(current, self.resistance, time)

    def power_density(
        self, current_density: jax.Array, resistivity: jax.Array
    ) -> jax.Array:
        """p = J^2 * rho (erg/s/cm^3)."""
        return self._power_density_jit(current_density, resistivity)

    def temperature_rise(
        self,
        current: jax.Array,
        time: jax.Array,
        mass: jax.Array,
        specific_heat: jax.Array,
    ) -> jax.Array:
        """dT = E / (m * c) = I^2 * R * t / (m * c)."""
        return self._temp_rise_jit(current, self.resistance, time, mass, specific_heat)

    def from_voltage(self, voltage: jax.Array) -> jax.Array:
        """P = V^2 / R (erg/s)."""
        return self._from_voltage_jit(voltage, self.resistance)

    @staticmethod
    @jax.jit
    def _power_jit(I: jax.Array, R: jax.Array) -> jax.Array:
        I = jnp.asarray(I, dtype=jnp.float64)
        R = jnp.asarray(R, dtype=jnp.float64)
        return I**2 * R

    @staticmethod
    @jax.jit
    def _energy_jit(I: jax.Array, R: jax.Array, t: jax.Array) -> jax.Array:
        I = jnp.asarray(I, dtype=jnp.float64)
        R = jnp.asarray(R, dtype=jnp.float64)
        t = jnp.asarray(t, dtype=jnp.float64)
        return I**2 * R * t

    @staticmethod
    @jax.jit
    def _power_density_jit(J: jax.Array, rho: jax.Array) -> jax.Array:
        J = jnp.asarray(J, dtype=jnp.float64)
        rho = jnp.asarray(rho, dtype=jnp.float64)
        return J**2 * rho

    @staticmethod
    @jax.jit
    def _temp_rise_jit(
        I: jax.Array, R: jax.Array, t: jax.Array, m: jax.Array, c: jax.Array
    ) -> jax.Array:
        I = jnp.asarray(I, dtype=jnp.float64)
        R = jnp.asarray(R, dtype=jnp.float64)
        t = jnp.asarray(t, dtype=jnp.float64)
        m = jnp.asarray(m, dtype=jnp.float64)
        c = jnp.asarray(c, dtype=jnp.float64)
        energy = I**2 * R * t
        return safe_div(energy, m * c)

    @staticmethod
    @jax.jit
    def _from_voltage_jit(V: jax.Array, R: jax.Array) -> jax.Array:
        V = jnp.asarray(V, dtype=jnp.float64)
        R = jnp.asarray(R, dtype=jnp.float64)
        return safe_div(V**2, R)


@jax_tree
@dataclass
class HeatDissipationJAX:
    """Heat dissipation in conductors. Arts. 351-358.

    Fields:
        specific_heat: Specific heat capacity in erg/(g*K).
        mass: Mass of conductor in g.
        thermal_conductivity: Thermal conductivity in erg/(s*cm*K).
    """

    specific_heat: float = 0.0
    mass: float = 0.0
    thermal_conductivity: float = 0.0

    def __post_init__(self) -> None:
        self.specific_heat = jnp.asarray(self.specific_heat, dtype=jnp.float64)
        self.mass = jnp.asarray(self.mass, dtype=jnp.float64)
        self.thermal_conductivity = jnp.asarray(
            self.thermal_conductivity, dtype=jnp.float64
        )

    def temperature_from_energy(self, energy: jax.Array) -> jax.Array:
        """dT = E / (m * c)."""
        return self._temp_from_energy_jit(energy, self.mass, self.specific_heat)

    def cooling_rate(
        self,
        surface_area: jax.Array,
        temp_diff: jax.Array,
        heat_transfer_coeff: jax.Array,
    ) -> jax.Array:
        """dQ/dt = h * A * dT (erg/s)."""
        return self._cooling_rate_jit(surface_area, temp_diff, heat_transfer_coeff)

    def steady_state_temperature(
        self,
        power_input: jax.Array,
        ambient_temp: jax.Array,
        surface_area: jax.Array,
        h_coeff: jax.Array,
    ) -> jax.Array:
        """T_ss = T_amb + P / (h * A)."""
        return self._steady_state_jit(power_input, ambient_temp, surface_area, h_coeff)

    def transient_temperature(
        self,
        power_input: jax.Array,
        time: jax.Array,
        ambient_temp: jax.Array,
        surface_area: jax.Array,
        h_coeff: jax.Array,
    ) -> jax.Array:
        """T(t) = T_amb + dT_ss * (1 - exp(-t/tau)).

        tau = m*c / (h*A), dT_ss = P/(h*A).
        """
        return self._transient_jit(
            power_input,
            time,
            ambient_temp,
            surface_area,
            h_coeff,
            self.mass,
            self.specific_heat,
        )

    @staticmethod
    @jax.jit
    def _temp_from_energy_jit(E: jax.Array, m: jax.Array, c: jax.Array) -> jax.Array:
        E = jnp.asarray(E, dtype=jnp.float64)
        m = jnp.asarray(m, dtype=jnp.float64)
        c = jnp.asarray(c, dtype=jnp.float64)
        return safe_div(E, m * c)

    @staticmethod
    @jax.jit
    def _cooling_rate_jit(A: jax.Array, dT: jax.Array, h: jax.Array) -> jax.Array:
        A = jnp.asarray(A, dtype=jnp.float64)
        dT = jnp.asarray(dT, dtype=jnp.float64)
        h = jnp.asarray(h, dtype=jnp.float64)
        return h * A * dT

    @staticmethod
    @jax.jit
    def _steady_state_jit(
        P: jax.Array, T_amb: jax.Array, A: jax.Array, h: jax.Array
    ) -> jax.Array:
        P = jnp.asarray(P, dtype=jnp.float64)
        T_amb = jnp.asarray(T_amb, dtype=jnp.float64)
        A = jnp.asarray(A, dtype=jnp.float64)
        h = jnp.asarray(h, dtype=jnp.float64)
        dT_ss = safe_div(P, h * A)
        return T_amb + dT_ss

    @staticmethod
    @jax.jit
    def _transient_jit(
        P: jax.Array,
        t: jax.Array,
        T_amb: jax.Array,
        A: jax.Array,
        h: jax.Array,
        m: jax.Array,
        c: jax.Array,
    ) -> jax.Array:
        P = jnp.asarray(P, dtype=jnp.float64)
        t = jnp.asarray(t, dtype=jnp.float64)
        T_amb = jnp.asarray(T_amb, dtype=jnp.float64)
        A = jnp.asarray(A, dtype=jnp.float64)
        h = jnp.asarray(h, dtype=jnp.float64)
        m = jnp.asarray(m, dtype=jnp.float64)
        c = jnp.asarray(c, dtype=jnp.float64)

        # Thermal time constant: tau = m*c / (h*A)
        hA = h * A
        tau = safe_div(m * c, hA)

        # Steady-state temp rise: dT_ss = P / (h*A)
        dT_ss = safe_div(P, hA)

        # T(t) = T_amb + dT_ss * (1 - exp(-t/tau))
        exponent = safe_div(-t, tau)
        return T_amb + dT_ss * (1.0 - jnp.exp(exponent))


@jax_tree
@dataclass
class SubstanceResistanceJAX:
    """Resistance of substances at given temperature. Arts. 359-370.

    Fields:
        base_resistivity: Resistivity rho_0 in abohm*cm at reference temp.
        temperature_coefficient: Temperature coefficient alpha per degree C.
        reference_temp: Reference temperature in C (default: 20.0).
    """

    base_resistivity: float = 0.0
    temperature_coefficient: float = 0.0
    reference_temp: float = 20.0

    def __post_init__(self) -> None:
        self.base_resistivity = jnp.asarray(self.base_resistivity, dtype=jnp.float64)
        self.temperature_coefficient = jnp.asarray(
            self.temperature_coefficient, dtype=jnp.float64
        )
        self.reference_temp = jnp.asarray(self.reference_temp, dtype=jnp.float64)

    def at_temperature(self, temp: jax.Array) -> jax.Array:
        """rho(T) = rho_0 * (1 + alpha*(T - T0))."""
        return self._at_temp_jit(
            self.base_resistivity,
            self.temperature_coefficient,
            temp,
            self.reference_temp,
        )

    def resistance_from_geometry(
        self, length: jax.Array, cross_section_area: jax.Array, temp: jax.Array
    ) -> jax.Array:
        """R = rho(T) * L / A."""
        return self._r_from_geom_jit(
            self.base_resistivity,
            self.temperature_coefficient,
            self.reference_temp,
            length,
            cross_section_area,
            temp,
        )

    def compare_substances(
        self,
        substances_resistivities: jax.Array,
        substances_alphas: jax.Array,
        temp: jax.Array,
        length: jax.Array,
        cross_section_area: jax.Array,
    ) -> jax.Array:
        """Compare resistances of multiple substances at a given temp."""
        return self._compare_jit(
            substances_resistivities,
            substances_alphas,
            self.reference_temp,
            temp,
            length,
            cross_section_area,
        )

    @staticmethod
    @jax.jit
    def _at_temp_jit(
        rho_0: jax.Array, alpha: jax.Array, T: jax.Array, T0: jax.Array
    ) -> jax.Array:
        rho_0 = jnp.asarray(rho_0, dtype=jnp.float64)
        alpha = jnp.asarray(alpha, dtype=jnp.float64)
        T = jnp.asarray(T, dtype=jnp.float64)
        T0 = jnp.asarray(T0, dtype=jnp.float64)
        return rho_0 * (1.0 + alpha * (T - T0))

    @staticmethod
    @jax.jit
    def _r_from_geom_jit(
        rho_0: jax.Array,
        alpha: jax.Array,
        T0: jax.Array,
        L: jax.Array,
        A: jax.Array,
        T: jax.Array,
    ) -> jax.Array:
        rho_0 = jnp.asarray(rho_0, dtype=jnp.float64)
        alpha = jnp.asarray(alpha, dtype=jnp.float64)
        T0 = jnp.asarray(T0, dtype=jnp.float64)
        L = jnp.asarray(L, dtype=jnp.float64)
        A = jnp.asarray(A, dtype=jnp.float64)
        T = jnp.asarray(T, dtype=jnp.float64)
        rho_T = rho_0 * (1.0 + alpha * (T - T0))
        return safe_div(rho_T * L, A)

    @staticmethod
    @jax.jit
    def _compare_jit(
        rhos: jax.Array,
        alphas: jax.Array,
        T0: jax.Array,
        T: jax.Array,
        L: jax.Array,
        A: jax.Array,
    ) -> jax.Array:
        rhos = jnp.asarray(rhos, dtype=jnp.float64)
        alphas = jnp.asarray(alphas, dtype=jnp.float64)
        T0 = jnp.asarray(T0, dtype=jnp.float64)
        T = jnp.asarray(T, dtype=jnp.float64)
        L = jnp.asarray(L, dtype=jnp.float64)
        A = jnp.asarray(A, dtype=jnp.float64)
        rho_T = rhos * (1.0 + alphas * (T - T0))
        return safe_div(rho_T * L, A)


# -- Standalone functions -------------------------------------------------------------


@maxwell_cite(
    351,
    352,
    part=2,
    chapter="Electrokinematics",
    description="Joule heating power: P = I^2 * R",
)
def joule_heating_power_jax(
    current: jax.Array,
    resistance: jax.Array,
) -> jax.Array:
    """Joule heating power. Arts. 351-352.

    P = I^2 * R

    Args:
        current: Current in abamperes.
        resistance: Resistance in abohms.

    Returns:
        Power dissipated in erg/s.
    """
    current = jnp.asarray(current, dtype=jnp.float64)
    resistance = jnp.asarray(resistance, dtype=jnp.float64)
    return current**2 * resistance


@maxwell_cite(
    351,
    352,
    part=2,
    chapter="Electrokinematics",
    description="Joule energy dissipated: E = I^2 * R * t",
)
def joule_energy_dissipated_jax(
    current: jax.Array,
    resistance: jax.Array,
    time: jax.Array,
) -> jax.Array:
    """Joule energy dissipated. Arts. 351-352.

    E = I^2 * R * t

    Args:
        current: Current in abamperes.
        resistance: Resistance in abohms.
        time: Time in seconds.

    Returns:
        Energy dissipated in erg.
    """
    current = jnp.asarray(current, dtype=jnp.float64)
    resistance = jnp.asarray(resistance, dtype=jnp.float64)
    time = jnp.asarray(time, dtype=jnp.float64)
    return current**2 * resistance * time


@maxwell_cite(
    353,
    354,
    part=2,
    chapter="Electrokinematics",
    description="Joule power density: p = J^2 * rho",
)
def joule_power_density_jax(
    current_density: jax.Array,
    resistivity: jax.Array,
) -> jax.Array:
    """Joule power density. Arts. 353-354.

    p = J^2 * rho

    Args:
        current_density: Current density in abA/cm^2.
        resistivity: Resistivity in abohm*cm.

    Returns:
        Power density in erg/s/cm^3.
    """
    current_density = jnp.asarray(current_density, dtype=jnp.float64)
    resistivity = jnp.asarray(resistivity, dtype=jnp.float64)
    return current_density**2 * resistivity


@maxwell_cite(
    355,
    356,
    part=2,
    chapter="Electrokinematics",
    description="Temperature rise from Joule heating: dT = I^2*R*t/(m*c)",
)
def joule_temperature_rise_jax(
    current: jax.Array,
    resistance: jax.Array,
    time: jax.Array,
    mass: jax.Array,
    specific_heat: jax.Array,
) -> jax.Array:
    """Temperature rise from Joule heating. Arts. 355-356.

    dT = I^2 * R * t / (m * c)

    Args:
        current: Current in abamperes.
        resistance: Resistance in abohms.
        time: Time in seconds.
        mass: Mass of conductor in g.
        specific_heat: Specific heat capacity in erg/(g*K).

    Returns:
        Temperature rise in K.
    """
    current = jnp.asarray(current, dtype=jnp.float64)
    resistance = jnp.asarray(resistance, dtype=jnp.float64)
    time = jnp.asarray(time, dtype=jnp.float64)
    mass = jnp.asarray(mass, dtype=jnp.float64)
    specific_heat = jnp.asarray(specific_heat, dtype=jnp.float64)
    energy = current**2 * resistance * time
    return safe_div(energy, mass * specific_heat)


@maxwell_cite(
    351,
    352,
    part=2,
    chapter="Electrokinematics",
    description="Joule heating from voltage: P = V^2 / R",
)
def joule_heating_from_voltage_jax(
    voltage: jax.Array,
    resistance: jax.Array,
) -> jax.Array:
    """Joule heating power from voltage. Arts. 351-352.

    P = V^2 / R

    Args:
        voltage: Voltage in abvolts.
        resistance: Resistance in abohms.

    Returns:
        Power dissipated in erg/s.
    """
    voltage = jnp.asarray(voltage, dtype=jnp.float64)
    resistance = jnp.asarray(resistance, dtype=jnp.float64)
    return safe_div(voltage**2, resistance)


@maxwell_cite(
    357,
    358,
    part=2,
    chapter="Electrokinematics",
    description="Cooling rate: dQ/dt = h * A * dT",
)
def cooling_rate_jax(
    surface_area: jax.Array,
    temp_diff: jax.Array,
    heat_transfer_coeff: jax.Array,
) -> jax.Array:
    """Cooling rate (Newton's law of cooling). Arts. 357-358.

    dQ/dt = h * A * dT

    Args:
        surface_area: Surface area in cm^2.
        temp_diff: Temperature difference in K.
        heat_transfer_coeff: Heat transfer coefficient in erg/(s*cm^2*K).

    Returns:
        Cooling rate in erg/s.
    """
    surface_area = jnp.asarray(surface_area, dtype=jnp.float64)
    temp_diff = jnp.asarray(temp_diff, dtype=jnp.float64)
    heat_transfer_coeff = jnp.asarray(heat_transfer_coeff, dtype=jnp.float64)
    return heat_transfer_coeff * surface_area * temp_diff


@maxwell_cite(
    357,
    358,
    part=2,
    chapter="Electrokinematics",
    description="Steady state temperature: T_ss = T_amb + P/(h*A)",
)
def steady_state_temperature_jax(
    power: jax.Array,
    ambient_temp: jax.Array,
    surface_area: jax.Array,
    heat_transfer_coeff: jax.Array,
) -> jax.Array:
    """Steady-state temperature. Arts. 357-358.

    T_ss = T_amb + P / (h * A)

    Args:
        power: Power input in erg/s.
        ambient_temp: Ambient temperature in K or C.
        surface_area: Surface area in cm^2.
        heat_transfer_coeff: Heat transfer coefficient in erg/(s*cm^2*K).

    Returns:
        Steady-state temperature in same units as ambient_temp.
    """
    power = jnp.asarray(power, dtype=jnp.float64)
    ambient_temp = jnp.asarray(ambient_temp, dtype=jnp.float64)
    surface_area = jnp.asarray(surface_area, dtype=jnp.float64)
    heat_transfer_coeff = jnp.asarray(heat_transfer_coeff, dtype=jnp.float64)
    dT_ss = safe_div(power, heat_transfer_coeff * surface_area)
    return ambient_temp + dT_ss


@maxwell_cite(
    359,
    360,
    part=2,
    chapter="Electrokinematics",
    description="Substance resistivity at temperature",
)
def substance_resistivity_at_temp_jax(
    rho_0: jax.Array,
    alpha: jax.Array,
    temp: jax.Array,
    ref_temp: jax.Array = 20.0,
) -> jax.Array:
    """Temperature-corrected resistivity. Arts. 359-360.

    rho(T) = rho_0 * (1 + alpha * (T - T0))

    Args:
        rho_0: Base resistivity at reference temp in abohm*cm.
        alpha: Temperature coefficient per degree C.
        temp: Temperature in C.
        ref_temp: Reference temperature in C (default: 20.0).

    Returns:
        Resistivity at the given temperature in abohm*cm.
    """
    rho_0 = jnp.asarray(rho_0, dtype=jnp.float64)
    alpha = jnp.asarray(alpha, dtype=jnp.float64)
    temp = jnp.asarray(temp, dtype=jnp.float64)
    ref_temp = jnp.asarray(ref_temp, dtype=jnp.float64)
    return rho_0 * (1.0 + alpha * (temp - ref_temp))


@maxwell_cite(
    361,
    362,
    part=2,
    chapter="Electrokinematics",
    description="Resistance from geometry: R = rho * L / A",
)
def substance_resistance_jax(
    rho: jax.Array,
    length: jax.Array,
    area: jax.Array,
) -> jax.Array:
    """Resistance from resistivity and geometry. Arts. 361-362.

    R = rho * L / A

    Args:
        rho: Resistivity in abohm*cm.
        length: Length in cm.
        area: Cross-sectional area in cm^2.

    Returns:
        Resistance in abohms.
    """
    rho = jnp.asarray(rho, dtype=jnp.float64)
    length = jnp.asarray(length, dtype=jnp.float64)
    area = jnp.asarray(area, dtype=jnp.float64)
    return safe_div(rho * length, area)


@maxwell_cite(
    351,
    352,
    353,
    354,
    355,
    356,
    part=2,
    chapter="Electrokinematics",
    description="Verify Joule heating relations",
)
def verify_joule_heating_jax(
    tol: float = 1e-10,
) -> Dict[str, Any]:
    """Verify Joule heating consistency. Arts. 351-356.

    Checks:
    1. P = I^2*R vs P = V^2/R consistency (via V = I*R)
    2. Energy = P * t
    3. Power density integration: P = p * Volume
    4. Temperature rise from energy

    Args:
        tol: Tolerance for verification.

    Returns:
        Dictionary with verification results.
    """
    # Test parameters
    I = jnp.array(2.0, dtype=jnp.float64)  # 2 abamperes
    R = jnp.array(5.0, dtype=jnp.float64)  # 5 abohms
    t = jnp.array(10.0, dtype=jnp.float64)  # 10 seconds
    V = I * R  # 10 abvolts

    # 1. Power formula consistency: I^2*R == V^2/R
    P_I2R = joule_heating_power_jax(I, R)
    P_V2R = joule_heating_from_voltage_jax(V, R)
    power_consistent = jnp.abs(P_I2R - P_V2R) < tol

    # 2. Energy = P * t
    E = joule_energy_dissipated_jax(I, R, t)
    E_expected = P_I2R * t
    energy_consistent = jnp.abs(E - E_expected) < tol

    # 3. Power density: for uniform J, P = J^2 * rho * Volume
    #    With I=2, A=1 -> J=2, R=5, L=1, A=1 -> rho=R*A/L=5
    J = jnp.array(2.0, dtype=jnp.float64)
    rho = jnp.array(5.0, dtype=jnp.float64)
    volume = jnp.array(1.0, dtype=jnp.float64)
    p = joule_power_density_jax(J, rho)
    P_from_density = p * volume
    density_consistent = jnp.abs(P_from_density - P_I2R) < tol

    # 4. Temperature rise: dT = E / (m*c)
    m = jnp.array(10.0, dtype=jnp.float64)  # 10 g
    c = jnp.array(4.18e7, dtype=jnp.float64)  # water ~4.18 J/(g*K) = 4.18e7 erg/(g*K)
    dT = joule_temperature_rise_jax(I, R, t, m, c)
    dT_expected = E / (m * c)
    temp_consistent = jnp.abs(dT - dT_expected) < tol

    verified = bool(
        power_consistent & energy_consistent & density_consistent & temp_consistent
    )

    return {
        "P_I2R": float(P_I2R),
        "P_V2R": float(P_V2R),
        "power_consistent": bool(power_consistent),
        "E": float(E),
        "E_expected": float(E_expected),
        "energy_consistent": bool(energy_consistent),
        "P_from_density": float(P_from_density),
        "density_consistent": bool(density_consistent),
        "dT": float(dT),
        "dT_expected": float(dT_expected),
        "temp_consistent": bool(temp_consistent),
        "verified": verified,
    }


@maxwell_cite(
    351,
    352,
    353,
    354,
    355,
    356,
    357,
    358,
    part=2,
    chapter="Electrokinematics",
    description="Complete Joule heating analysis",
)
def analyze_joule_heating_jax(
    current: float = 1.0,
    resistance: float = 1.0,
    time: float = 1.0,
    mass: float = 1.0,
    specific_heat: float = 4.18e7,
    voltage: float = None,
    surface_area: float = 1.0,
    ambient_temp: float = 293.15,
    heat_transfer_coeff: float = 1.0e5,
    rho_0: float = 1.7e-6,
    alpha: float = 0.00393,
    length: float = 100.0,
    cross_section_area: float = 0.01,
    operating_temp: float = 20.0,
) -> Dict[str, Any]:
    """Comprehensive Joule heating analysis. Arts. 351-358.

    Computes all relevant quantities from a given set of parameters.

    Args:
        current: Current in abamperes.
        resistance: Resistance in abohms.
        time: Time in seconds.
        mass: Mass of conductor in g.
        specific_heat: Specific heat in erg/(g*K).
        voltage: Voltage in abvolts (if None, computed from I*R).
        surface_area: Surface area in cm^2.
        ambient_temp: Ambient temperature in K.
        heat_transfer_coeff: Heat transfer coefficient in erg/(s*cm^2*K).
        rho_0: Base resistivity at reference temp in abohm*cm.
        alpha: Temperature coefficient per degree C.
        length: Conductor length in cm.
        cross_section_area: Cross-sectional area in cm^2.
        operating_temp: Operating temperature in C.

    Returns:
        Dictionary with complete analysis results.
    """
    I = jnp.array(current, dtype=jnp.float64)
    R = jnp.array(resistance, dtype=jnp.float64)
    t = jnp.array(time, dtype=jnp.float64)
    m = jnp.array(mass, dtype=jnp.float64)
    c = jnp.array(specific_heat, dtype=jnp.float64)

    if voltage is None:
        V = I * R
    else:
        V = jnp.array(voltage, dtype=jnp.float64)

    # Joule heating
    P = joule_heating_power_jax(I, R)
    P_from_V = joule_heating_from_voltage_jax(V, R)
    E = joule_energy_dissipated_jax(I, R, t)
    dT = joule_temperature_rise_jax(I, R, t, m, c)

    # Thermal
    A = jnp.array(surface_area, dtype=jnp.float64)
    T_amb = jnp.array(ambient_temp, dtype=jnp.float64)
    h = jnp.array(heat_transfer_coeff, dtype=jnp.float64)
    T_ss = steady_state_temperature_jax(P, T_amb, A, h)
    cooling = cooling_rate_jax(A, T_ss - T_amb, h)

    # Substance
    rho_T = substance_resistivity_at_temp_jax(
        jnp.array(rho_0, dtype=jnp.float64),
        jnp.array(alpha, dtype=jnp.float64),
        jnp.array(operating_temp, dtype=jnp.float64),
    )
    L = jnp.array(length, dtype=jnp.float64)
    A_cs = jnp.array(cross_section_area, dtype=jnp.float64)
    R_geom = substance_resistance_jax(rho_T, L, A_cs)

    return {
        "current_abA": float(I),
        "resistance_abohm": float(R),
        "voltage_abV": float(V),
        "power_erg_s": float(P),
        "power_from_voltage_erg_s": float(P_from_V),
        "energy_erg": float(E),
        "temperature_rise_K": float(dT),
        "steady_state_temp_K": float(T_ss),
        "cooling_rate_erg_s": float(cooling),
        "resistivity_at_temp": float(rho_T),
        "resistance_from_geometry": float(R_geom),
    }

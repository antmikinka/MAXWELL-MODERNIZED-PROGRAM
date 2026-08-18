"""
Conduction in Dielectric Media — Maxwell's Part II, Chapter X (Arts. 325-334).

This module implements Maxwell's theory of conduction in dielectric media:

1. **Dielectric Conduction** (Arts. 325-328): Small but finite conductivity in insulators
   - Real dielectrics have small but non-zero conductivity
   - Leakage current through insulating materials

2. **Absorption/Soakage** (Arts. 329-331): Dielectric absorption phenomena
   - Time-dependent polarization and charge storage
   - Residual charge after discharge
   - Voltage recovery after open circuit

3. **Composite Dielectrics** (Arts. 332-334): Layered and composite materials
   - Multi-layer dielectric conduction
   - Interface effects and boundary conditions
   - Effective conductivity of heterogeneous dielectrics

Maxwell's key insight: Real dielectrics exhibit both capacitive (displacement)
and conductive (leakage) behavior, with time-dependent absorption effects
due to slow polarization mechanisms.

CGS-EMU units are used throughout, following Maxwell's conventions:
    - Electric field: abvolts/cm
    - Current density: abamperes/cm²
    - Conductivity: siemens/cm (abΩ⁻¹ cm⁻¹)
    - Permittivity: dimensionless (relative to vacuum)

Category: A (maxwell_original) — Maxwell's theory of dielectric conduction.

References:
    Part II, Chapter X: Conduction in Dielectric Media (Arts. 325-334).
    Part II, Chapter VI: Electrolysis (Arts. 236-263) for ionic conduction.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import wraps
from typing import Callable, Optional

import numpy as np

from maxwell.config.constants import CONST, C
from maxwell.meta.citation import maxwell_cite

# =============================================================================
# DIELECTRIC CONDUCTIVITY (Arts. 325-326)
# =============================================================================


@maxwell_cite(
    325,
    326,
    part=2,
    chapter="Conduction in Dielectric Media",
    theory_class="maxwell_original",
    description="Finite conductivity of insulating materials",
)
def dielectric_conductivity(
    material: str = None,
    permittivity: float = None,
    loss_tangent: float = None,
    frequency: float = None,
    temperature: float = 293.15,
) -> dict[str, float]:
    """
    Calculate or lookup the conductivity of a dielectric material.

    Arts. 325-326: Maxwell recognized that even the best insulators have
    small but finite conductivity, allowing leakage current to flow.

    The conductivity of a dielectric can be expressed as:

        sigma_diel = omega * epsilon * tan(delta)

    where:
        - omega = 2 * pi * frequency (angular frequency)
        - epsilon = epsilon_0 * epsilon_r (absolute permittivity)
        - tan(delta) = loss tangent (dissipation factor)

    For DC conditions, the volume resistivity rho_v gives:

        sigma_diel = 1 / rho_v

    Maxwell noted that dielectric conductivity depends on:
        - Material composition and purity
        - Temperature (increases with T)
        - Frequency (for AC)
        - Moisture content and contamination

    Args:
        material: Optional material name for lookup (e.g., "glass", "mica").
        permittivity: Relative permittivity epsilon_r (dimensionless).
        loss_tangent: Loss tangent tan(delta) (dimensionless).
        frequency: Frequency in Hz (for AC conductivity).
        temperature: Temperature in Kelvin (default: 293.15 K = 20°C).

    Returns:
        Dictionary with:
        - conductivity: DC or AC conductivity (siemens/cm)
        - resistivity: Volume resistivity (abohm·cm)
        - loss_conductivity: AC loss component (siemens/cm)
        - frequency: Applied frequency (Hz)
        - temperature: Temperature (K)
        - material: Material name if provided

    Raises:
        ValueError: If insufficient parameters provided for calculation.

    References:
        Part II, Art. 325: Dielectric conduction theory.
        Part II, Art. 326: Specific inductive capacity and conductivity.

    Example:
        >>> # Glass at 60 Hz
        >>> result = dielectric_conductivity(
        ...     permittivity=5.0,
        ...     loss_tangent=0.001,
        ...     frequency=60.0
        ... )
        >>> print(f"sigma = {result['conductivity']:.2e} S/cm")
    """
    # Default material properties (representative values)
    material_properties = {
        "glass": {"epsilon_r": 5.0, "tan_delta": 0.001, "rho_v": 1e10},
        "mica": {"epsilon_r": 6.0, "tan_delta": 0.0001, "rho_v": 1e12},
        "quartz": {"epsilon_r": 4.5, "tan_delta": 0.0001, "rho_v": 1e14},
        "paraffin": {"epsilon_r": 2.2, "tan_delta": 0.0002, "rho_v": 1e15},
        "ebonite": {"epsilon_r": 2.7, "tan_delta": 0.002, "rho_v": 1e13},
        "gutta_percha": {"epsilon_r": 2.5, "tan_delta": 0.005, "rho_v": 1e11},
        "shellac": {"epsilon_r": 3.0, "tan_delta": 0.01, "rho_v": 1e12},
        "air": {"epsilon_r": 1.0006, "tan_delta": 1e-10, "rho_v": 1e18},
    }

    result = {
        "frequency": frequency,
        "temperature": temperature,
        "material": material,
    }

    # Lookup material properties
    if material and material.lower() in material_properties:
        props = material_properties[material.lower()]
        if permittivity is None:
            permittivity = props["epsilon_r"]
        if loss_tangent is None:
            loss_tangent = props["tan_delta"]
        if "rho_v" in props:
            result["resistivity_dc"] = props["rho_v"]

    # Validate inputs
    if permittivity is None:
        permittivity = 1.0  # Default to vacuum
        result["warning"] = "Permittivity not specified, using epsilon_r = 1.0"

    # DC conductivity from resistivity
    if "resistivity_dc" in result:
        sigma_dc = 1.0 / result["resistivity_dc"]
    elif loss_tangent is not None and frequency is not None:
        # AC conductivity from loss tangent
        omega = 2 * np.pi * frequency
        # In CGS-EMU, epsilon_0 = 1/(c^2) where c is speed of light in cm/s
        epsilon_0_emu = 1.0 / (C**2)
        epsilon = epsilon_0_emu * permittivity
        sigma_ac = omega * epsilon * loss_tangent
        sigma_dc = sigma_ac
    else:
        # Default very low conductivity for good insulator
        sigma_dc = 1e-15
        result["note"] = "Default conductivity for ideal insulator"

    result["conductivity"] = sigma_dc
    result["resistivity"] = 1.0 / sigma_dc if sigma_dc > 0 else float("inf")

    if frequency is not None and loss_tangent is not None:
        omega = 2 * np.pi * frequency
        epsilon_0_emu = 1.0 / (C**2)
        epsilon = epsilon_0_emu * permittivity
        result["loss_conductivity"] = omega * epsilon * loss_tangent
        result["angular_frequency"] = omega
        result["absolute_permittivity"] = epsilon

    return result


# =============================================================================
# LEAKAGE CURRENT DENSITY (Arts. 327-328)
# =============================================================================


@maxwell_cite(
    327,
    328,
    part=2,
    chapter="Conduction in Dielectric Media",
    theory_class="maxwell_original",
    description="Leakage current through dielectric under electric field",
)
def leakage_current_density(
    electric_field: np.ndarray,
    conductivity: float,
    permittivity: float = None,
) -> dict[str, np.ndarray | float]:
    """
    Calculate leakage current density through a dielectric material.

    Arts. 327-328: Maxwell showed that in a real dielectric, the total
    current density has two components:

        J_total = J_conduction + J_displacement

    The leakage (conduction) current follows Ohm's law:

        J_leak = sigma_diel * E

    where sigma_diel is the small but finite conductivity of the insulator.

    Maxwell noted that for steady (DC) fields, only the leakage current
    persists, while for AC fields both components contribute.

    The ratio of conduction to displacement current is:

        |J_leak| / |J_disp| = sigma_diel / (omega * epsilon)
                            = tan(delta)  (loss tangent)

    Args:
        electric_field: Electric field vector E (abvolts/cm).
        conductivity: Dielectric conductivity sigma_diel (siemens/cm).
        permittivity: Optional absolute permittivity for displacement current.

    Returns:
        Dictionary with:
        - leakage_current: J_leak vector (abamperes/cm²)
        - leakage_magnitude: |J_leak| (abamperes/cm²)
        - electric_field: Input E field
        - conductivity: Input conductivity
        - displacement_current: J_disp if permittivity provided (frequency-dependent)
        - loss_ratio: |J_leak|/|J_disp| (equals tan delta)

    Raises:
        ValueError: If conductivity is negative.

    References:
        Part II, Art. 327: Leakage current theory.
        Part II, Art. 328: Relation to electric induction.

    Example:
        >>> # Glass insulator, E = 1000 abV/cm, sigma = 1e-12 S/cm
        >>> E = np.array([1000, 0, 0])
        >>> result = leakage_current_density(E, conductivity=1e-12)
        >>> print(f"J_leak = {result['leakage_current']} abA/cm²")
        >>> print(f"|J_leak| = {result['leakage_magnitude']:.2e} abA/cm²")
    """
    electric_field = np.asarray(electric_field, dtype=np.float64)

    if conductivity < 0:
        raise ValueError(f"Conductivity must be non-negative, got {conductivity}")

    # Leakage current: J_leak = sigma * E
    leakage_current = conductivity * electric_field
    leakage_magnitude = np.linalg.norm(leakage_current)

    result = {
        "leakage_current": leakage_current,
        "leakage_magnitude": leakage_magnitude,
        "electric_field": electric_field,
        "conductivity": conductivity,
    }

    # Calculate displacement current if permittivity and frequency provided
    if permittivity is not None:
        # For AC: J_disp = epsilon * dE/dt = omega * epsilon * E (phasor magnitude)
        # The ratio |J_leak|/|J_disp| = sigma/(omega*epsilon) = tan(delta)
        result["permittivity"] = permittivity

    return result


# =============================================================================
# DIELECTRIC ABSORPTION (Arts. 329-330)
# =============================================================================


@maxwell_cite(
    329,
    330,
    part=2,
    chapter="Conduction in Dielectric Media",
    theory_class="maxwell_original",
    description="Time-dependent dielectric absorption (soakage)",
)
def dielectric_absorption(
    voltage: float,
    capacitance: float,
    absorption_time: float,
    absorption_constants: list[float] = None,
    initial_charge: float = None,
) -> dict[str, float]:
    """
    Model dielectric absorption (soakage) — time-dependent polarization.

    Arts. 329-330: Maxwell described the phenomenon of dielectric absorption,
    where a dielectric continues to absorb charge over time after a voltage
    is applied, and releases it slowly after discharge.

    The absorption is modeled as a sum of exponential processes with
    different time constants (absorption constants):

        Q_abs(t) = Q_0 * sum_i [ a_i * (1 - exp(-t/tau_i)) ]

    where:
        - Q_0 = C * V is the nominal stored charge
        - a_i are absorption coefficients (sum to < 1)
        - tau_i are absorption time constants

    For a single absorption process:

        Q_abs(t) = Q_0 * a * (1 - exp(-t/tau))

    Maxwell called this "electric soakage" by analogy with liquid absorption
    in a porous material.

    Args:
        voltage: Applied voltage V (abvolts).
        capacitance: Geometric capacitance C (abfarads).
        absorption_time: Time t since voltage application (seconds).
        absorption_constants: List of (a_i, tau_i) tuples.
                           If None, uses default single process.
        initial_charge: Optional initial absorbed charge.

    Returns:
        Dictionary with:
        - nominal_charge: Q_0 = C * V (abfarads)
        - absorbed_charge: Q_abs(t) additional absorbed charge
        - total_charge: Q_0 + Q_abs(t) total stored charge
        - absorption_ratio: Q_abs / Q_0 (fraction absorbed)
        - time: Time since voltage application
        - time_constants: Absorption time constants used

    References:
        Part II, Art. 329: Dielectric absorption theory.
        Part II, Art. 330: Time-dependent polarization.

    Example:
        >>> # Capacitor with absorption: C = 1 abF, V = 100 abV
        >>> result = dielectric_absorption(
        ...     voltage=100,
        ...     capacitance=1.0,
        ...     absorption_time=10.0,
        ...     absorption_constants=[(0.05, 5.0)]  # 5% absorption, tau=5s
        ... )
        >>> print(f"Q_absorbed = {result['absorbed_charge']:.4f} abC")
        >>> print(f"Absorption ratio = {result['absorption_ratio']:.4f}")
    """
    # Nominal charge
    nominal_charge = capacitance * voltage

    # Default absorption constants if not provided
    # Typical values: 1-10% absorption with time constants 1-100 seconds
    if absorption_constants is None:
        absorption_constants = [(0.05, 10.0)]  # 5% absorption, tau = 10s

    # Calculate absorbed charge
    absorbed_charge = 0.0
    for a_i, tau_i in absorption_constants:
        absorbed_charge += (
            nominal_charge * a_i * (1.0 - np.exp(-absorption_time / tau_i))
        )

    if initial_charge is not None:
        absorbed_charge += initial_charge

    total_charge = nominal_charge + absorbed_charge
    absorption_ratio = absorbed_charge / nominal_charge if nominal_charge > 0 else 0.0

    return {
        "nominal_charge": nominal_charge,
        "absorbed_charge": absorbed_charge,
        "total_charge": total_charge,
        "absorption_ratio": absorption_ratio,
        "time": absorption_time,
        "time_constants": [(a, t) for a, t in absorption_constants],
        "voltage": voltage,
        "capacitance": capacitance,
    }


@maxwell_cite(
    329,
    330,
    part=2,
    chapter="Conduction in Dielectric Media",
    theory_class="maxwell_original",
    description="Absorption current decay after voltage step",
)
def absorption_current(
    voltage: float,
    capacitance: float,
    time: float,
    absorption_time: float = None,
    absorption_constants: list[tuple[float, float]] = None,
) -> dict[str, float]:
    """
    Calculate absorption current as a function of time.

    Arts. 329-330: When a voltage is suddenly applied to a dielectric,
    the absorption current decays exponentially as the dielectric
    becomes polarized:

        I_abs(t) = I_0 * sum_i [ (a_i/tau_i) * exp(-t/tau_i) ]

    For a single absorption process:

        I_abs(t) = (V * C * a / tau) * exp(-t/tau)
                 = I_0 * exp(-t/tau)

    where I_0 = V * C * a / tau is the initial absorption current.

    Maxwell observed that this current can persist for minutes or
    hours in some materials, gradually decreasing as the dielectric
    approaches full polarization.

    Args:
        voltage: Applied voltage V (abvolts).
        capacitance: Geometric capacitance C (abfarads).
        time: Time t since voltage application (seconds).
        absorption_time: Deprecated, use 'time' instead.
        absorption_constants: List of (a_i, tau_i) tuples.
                           If None, uses default single process.

    Returns:
        Dictionary with:
        - absorption_current: I_abs(t) at the given time (abamperes)
        - initial_current: I_0 at t=0 (abamperes)
        - time: Time since voltage application
        - time_constant: Dominant absorption time constant
        - current_ratio: I(t)/I_0 (decay fraction)

    References:
        Part II, Art. 329: Absorption current theory.
        Part II, Art. 330: Exponential decay model.

    Example:
        >>> # Absorption current after 5 seconds
        >>> result = absorption_current(
        ...     voltage=100,
        ...     capacitance=1.0,
        ...     time=5.0,
        ...     absorption_constants=[(0.05, 10.0)]
        ... )
        >>> print(f"I_abs(5s) = {result['absorption_current']:.6f} abA")
        >>> print(f"I_0 = {result['initial_current']:.6f} abA")
    """
    # Handle deprecated parameter
    if absorption_time is not None and time is None:
        time = absorption_time

    if time is None:
        raise ValueError("time parameter is required")

    # Default absorption constants
    if absorption_constants is None:
        absorption_constants = [(0.05, 10.0)]  # 5% absorption, tau = 10s

    # Calculate absorption current
    I_0 = 0.0
    I_t = 0.0

    for a_i, tau_i in absorption_constants:
        I_0_i = voltage * capacitance * a_i / tau_i
        I_0 += I_0_i
        I_t += I_0_i * np.exp(-time / tau_i)

    current_ratio = I_t / I_0 if I_0 > 0 else 0.0

    # Dominant time constant (longest)
    dominant_tau = max(tau_i for _, tau_i in absorption_constants)

    return {
        "absorption_current": I_t,
        "initial_current": I_0,
        "time": time,
        "time_constant": dominant_tau,
        "current_ratio": current_ratio,
        "voltage": voltage,
        "capacitance": capacitance,
    }


# =============================================================================
# RESIDUAL CHARGE (Art. 331)
# =============================================================================


@maxwell_cite(
    331,
    part=2,
    chapter="Conduction in Dielectric Media",
    theory_class="maxwell_original",
    description="Residual charge after capacitor discharge",
)
def residual_charge(
    initial_voltage: float,
    capacitance: float,
    discharge_time: float,
    absorption_constants: list[tuple[float, float]] = None,
    discharge_complete: bool = True,
) -> dict[str, float]:
    """
    Calculate residual charge remaining after discharging a capacitor.

    Art. 331: Maxwell explained the phenomenon of residual charge:
    after a capacitor is discharged through a low resistance, a small
    charge reappears on the plates after some time. This is due to
    the slow release of absorbed charge.

    After discharge at t=0, the residual charge grows as:

        Q_residual(t) = Q_absorbed * (1 - exp(-t/tau))

    where Q_absorbed is the charge that was absorbed during charging.

    For multiple absorption processes:

        Q_residual(t) = sum_i [ Q_0 * a_i * exp(-t_discharge/tau_i) * (1 - exp(-t/tau_i)) ]

    where t_discharge is the time the capacitor was charged before discharge.

    Args:
        initial_voltage: Voltage V before discharge (abvolts).
        capacitance: Capacitance C (abfarads).
        discharge_time: Time t since discharge (seconds).
        absorption_constants: List of (a_i, tau_i) tuples.
        discharge_complete: If True, assume complete discharge of main charge.

    Returns:
        Dictionary with:
        - residual_charge: Q_residual at the given time (abfarads)
        - residual_voltage: V_residual = Q/C (abvolts)
        - initial_absorbed_charge: Charge absorbed before discharge
        - discharge_time: Time since discharge
        - recovery_fraction: Q_residual / Q_absorbed

    Raises:
        ValueError: If capacitance is not positive.

    References:
        Part II, Art. 331: Residual charge phenomenon.

    Example:
        >>> # After discharging a 1 abF capacitor initially at 100 abV
        >>> result = residual_charge(
        ...     initial_voltage=100,
        ...     capacitance=1.0,
        ...     discharge_time=30.0,
        ...     absorption_constants=[(0.05, 10.0)]
        ... )
        >>> print(f"Q_residual = {result['residual_charge']:.4f} abC")
        >>> print(f"V_residual = {result['residual_voltage']:.4f} abV")
    """
    if capacitance <= 0:
        raise ValueError(f"Capacitance must be positive, got {capacitance}")

    # Default absorption constants
    if absorption_constants is None:
        absorption_constants = [(0.05, 10.0)]

    # Assume capacitor was charged long enough for full absorption
    Q_0 = capacitance * initial_voltage

    # Calculate residual charge from each absorption process
    Q_residual = 0.0
    Q_absorbed_total = 0.0

    for a_i, tau_i in absorption_constants:
        Q_abs_i = Q_0 * a_i  # Absorbed charge for this process
        Q_absorbed_total += Q_abs_i
        # After discharge, absorbed charge slowly leaks back
        Q_residual += Q_abs_i * (1.0 - np.exp(-discharge_time / tau_i))

    if not discharge_complete:
        # If discharge incomplete, some main charge also remains
        pass  # Simplified model assumes complete discharge

    residual_voltage = Q_residual / capacitance
    recovery_fraction = Q_residual / Q_absorbed_total if Q_absorbed_total > 0 else 0.0

    return {
        "residual_charge": Q_residual,
        "residual_voltage": residual_voltage,
        "initial_absorbed_charge": Q_absorbed_total,
        "discharge_time": discharge_time,
        "recovery_fraction": recovery_fraction,
        "initial_voltage": initial_voltage,
        "capacitance": capacitance,
    }


@maxwell_cite(
    331,
    part=2,
    chapter="Conduction in Dielectric Media",
    theory_class="maxwell_original",
    description="Voltage recovery after open circuit",
)
def residual_charge_recovery(
    initial_voltage: float,
    capacitance: float,
    open_circuit_time: float,
    absorption_constants: list[tuple[float, float]] = None,
    charge_time: float = None,
) -> dict[str, float]:
    """
    Model voltage recovery after a capacitor is left open-circuit.

    Art. 331: After a capacitor is charged and then disconnected (open
    circuit), the terminal voltage initially drops due to absorption,
    but if discharged briefly and left open, the voltage recovers as
    absorbed charge redistributes.

    For a capacitor charged for time t_charge, discharged briefly,
    then left open for time t_recovery:

        V_recovery(t) = V_initial * sum_i [ a_i * exp(-t_charge/tau_i) * (1 - exp(-t/tau_i)) ]

    The recovered voltage is proportional to the released absorbed charge.

    Maxwell used this phenomenon to demonstrate the reality of dielectric
    absorption and distinguish it from simple leakage.

    Args:
        initial_voltage: Initial charging voltage V_0 (abvolts).
        capacitance: Capacitance C (abfarads).
        open_circuit_time: Time t since open circuit / discharge (seconds).
        absorption_constants: List of (a_i, tau_i) tuples.
        charge_time: Time capacitor was charged before discharge.
                    If None, assumes long charge time (full absorption).

    Returns:
        Dictionary with:
        - recovered_voltage: V_recovery at the given time (abvolts)
        - recovery_fraction: V_recovery / V_initial
        - open_circuit_time: Time since open circuit
        - time_constants: Absorption time constants
        - peak_recovery_voltage: Maximum recoverable voltage

    References:
        Part II, Art. 331: Voltage recovery phenomenon.

    Example:
        >>> # Voltage recovery after 60 seconds open circuit
        >>> result = residual_charge_recovery(
        ...     initial_voltage=100,
        ...     capacitance=1.0,
        ...     open_circuit_time=60.0,
        ...     absorption_constants=[(0.05, 10.0)],
        ...     charge_time=100.0
        ... )
        >>> print(f"V_recovered = {result['recovered_voltage']:.4f} abV")
        >>> print(f"Recovery fraction = {result['recovery_fraction']:.4f}")
    """
    # Default absorption constants
    if absorption_constants is None:
        absorption_constants = [(0.05, 10.0)]

    # Charge time factor (accounts for incomplete absorption during charging)
    V_recovery = 0.0
    V_peak = 0.0

    for a_i, tau_i in absorption_constants:
        if charge_time is not None:
            charge_factor = np.exp(-charge_time / tau_i)
        else:
            charge_factor = 1.0  # Assume full absorption

        # Recovery grows as (1 - exp(-t/tau))
        recovery_factor = 1.0 - np.exp(-open_circuit_time / tau_i)

        V_recovery += initial_voltage * a_i * charge_factor * recovery_factor
        V_peak += initial_voltage * a_i * charge_factor  # Max possible recovery

    recovery_fraction = V_recovery / initial_voltage if initial_voltage > 0 else 0.0
    peak_recovery_fraction = V_peak / initial_voltage if initial_voltage > 0 else 0.0

    return {
        "recovered_voltage": V_recovery,
        "recovery_fraction": recovery_fraction,
        "open_circuit_time": open_circuit_time,
        "time_constants": [(a, t) for a, t in absorption_constants],
        "peak_recovery_voltage": V_peak,
        "peak_recovery_fraction": peak_recovery_fraction,
        "initial_voltage": initial_voltage,
        "capacitance": capacitance,
    }


# =============================================================================
# LAYERED DIELECTRICS (Arts. 332-333)
# =============================================================================


@maxwell_cite(
    332,
    333,
    part=2,
    chapter="Conduction in Dielectric Media",
    theory_class="maxwell_original",
    description="Multi-layer dielectric with conduction and absorption",
)
def layered_dielectric(
    layer_thicknesses: list[float],
    layer_conductivities: list[float],
    layer_permittivities: list[float],
    applied_voltage: float = None,
    applied_field: float = None,
) -> dict[str, np.ndarray | float]:
    """
    Analyze conduction and field distribution in a layered dielectric.

    Arts. 332-333: Maxwell analyzed composite dielectrics consisting of
    layers of different materials. For N layers in series:

    Under DC (steady state):
        - Current density J is continuous across all layers
        - Field in layer i: E_i = J / sigma_i
        - Voltage drop: V_i = E_i * d_i

    Under AC or transient:
        - Displacement current also contributes
        - Interface charge accumulates: sigma_interface = epsilon_0*(epsilon_i*E_i - epsilon_j*E_j)

    For steady DC with applied voltage V:
        J = V / sum_i (d_i / sigma_i)
        E_i = J / sigma_i

    The field is stronger in layers with lower conductivity.

    Args:
        layer_thicknesses: List of layer thicknesses d_i (cm).
        layer_conductivities: List of conductivities sigma_i (siemens/cm).
        layer_permittivities: List of relative permittivities epsilon_i.
        applied_voltage: Total voltage across stack (abvolts).
        applied_field: Alternative: applied electric field (abvolts/cm).

    Returns:
        Dictionary with:
        - current_density: J (abamperes/cm²)
        - field_per_layer: E_i in each layer (abvolts/cm)
        - voltage_per_layer: V_i across each layer (abvolts)
        - total_thickness: Sum of layer thicknesses
        - effective_conductivity: sigma_eff of the stack
        - interface_charges: Charge at each interface (if permittivities given)

    Raises:
        ValueError: If neither voltage nor field specified, or arrays mismatched.

    References:
        Part II, Art. 332: Layered dielectric theory.
        Part II, Art. 333: Interface boundary conditions.

    Example:
        >>> # Two-layer dielectric: glass (0.1cm) + mica (0.2cm)
        >>> result = layered_dielectric(
        ...     layer_thicknesses=[0.1, 0.2],
        ...     layer_conductivities=[1e-12, 1e-14],
        ...     layer_permittivities=[5.0, 6.0],
        ...     applied_voltage=1000
        ... )
        >>> print(f"J = {result['current_density']:.2e} abA/cm²")
        >>> print(f"E_glass = {result['field_per_layer'][0]:.2f} abV/cm")
        >>> print(f"E_mica = {result['field_per_layer'][1]:.2f} abV/cm")
    """
    # Validate inputs
    n = len(layer_thicknesses)
    if len(layer_conductivities) != n or len(layer_permittivities) != n:
        raise ValueError("All layer arrays must have same length")

    if applied_voltage is None and applied_field is None:
        raise ValueError("Either applied_voltage or applied_field must be specified")

    layer_thicknesses = np.asarray(layer_thicknesses, dtype=np.float64)
    layer_conductivities = np.asarray(layer_conductivities, dtype=np.float64)
    layer_permittivities = np.asarray(layer_permittivities, dtype=np.float64)

    total_thickness = np.sum(layer_thicknesses)

    # Determine applied field
    if applied_voltage is not None:
        # Calculate current density from total voltage
        # V = sum(E_i * d_i) = J * sum(d_i / sigma_i)
        resistance_area = np.sum(layer_thicknesses / layer_conductivities)
        current_density = applied_voltage / resistance_area
    else:
        current_density = (
            applied_field * layer_conductivities[0]
        )  # Not quite right for multi-layer

    # Field in each layer: E_i = J / sigma_i
    field_per_layer = current_density / layer_conductivities

    # Voltage drop across each layer
    voltage_per_layer = field_per_layer * layer_thicknesses

    # Effective conductivity of stack (series combination)
    effective_conductivity = total_thickness / resistance_area

    # Interface charges (from discontinuity in D = epsilon * E)
    interface_charges = []
    epsilon_0_emu = 1.0 / (C**2)
    for i in range(n - 1):
        D_i = epsilon_0_emu * layer_permittivities[i] * field_per_layer[i]
        D_ip1 = epsilon_0_emu * layer_permittivities[i + 1] * field_per_layer[i + 1]
        sigma_interface = D_ip1 - D_i  # Surface charge density
        interface_charges.append(sigma_interface)

    # Verify total voltage
    total_voltage = np.sum(voltage_per_layer)

    return {
        "current_density": current_density,
        "field_per_layer": field_per_layer,
        "voltage_per_layer": voltage_per_layer,
        "total_thickness": total_thickness,
        "effective_conductivity": effective_conductivity,
        "interface_charges": np.array(interface_charges),
        "total_voltage": total_voltage,
        "n_layers": n,
    }


# =============================================================================
# COMPOSITE DIELECTRIC CONDUCTIVITY (Art. 334)
# =============================================================================


@maxwell_cite(
    334,
    part=2,
    chapter="Conduction in Dielectric Media",
    theory_class="maxwell_original",
    description="Effective conductivity of heterogeneous dielectric",
)
def composite_dielectric_conductivity(
    matrix_conductivity: float,
    matrix_permittivity: float,
    inclusion_conductivity: float,
    inclusion_permittivity: float,
    volume_fraction: float,
    inclusion_shape: str = "sphere",
) -> dict[str, float]:
    """
    Calculate effective conductivity of a composite dielectric.

    Art. 334: Maxwell derived the effective conductivity of a heterogeneous
    dielectric consisting of inclusions in a continuous matrix.

    For spherical inclusions at low volume fraction (Maxwell-Garnett formula):

        sigma_eff = sigma_m * [2*(1-f)*sigma_m + (1+2f)*sigma_i] / [(2+f)*sigma_m + (1-f)*sigma_i]

    where:
        - sigma_m = matrix conductivity
        - sigma_i = inclusion conductivity
        - f = volume fraction of inclusions

    For dilute suspensions (f << 1):

        sigma_eff ≈ sigma_m * [1 + 3f * (sigma_i - sigma_m)/(sigma_i + 2*sigma_m)]

    Maxwell also derived formulas for other inclusion shapes:
        - Spheres: depolarization factor N = 1/3
        - Needle (parallel): N = 0
        - Disk (perpendicular): N = 1

    Args:
        matrix_conductivity: Conductivity of matrix sigma_m (siemens/cm).
        matrix_permittivity: Permittivity of matrix epsilon_m.
        inclusion_conductivity: Conductivity of inclusions sigma_i.
        inclusion_permittivity: Permittivity of inclusions epsilon_i.
        volume_fraction: Volume fraction f of inclusions (0 to 1).
        inclusion_shape: Shape of inclusions. Options:
                        - "sphere": Spherical inclusions (default)
                        - "needle": Needle-like inclusions (parallel)
                        - "disk": Disk-like inclusions (perpendicular)
                        - "random": Randomly oriented ellipsoids

    Returns:
        Dictionary with:
        - effective_conductivity: sigma_eff (siemens/cm)
        - effective_permittivity: epsilon_eff (from Maxwell's mixture formula)
        - volume_fraction: Input volume fraction
        - conductivity_ratio: sigma_i / sigma_m
        - enhancement_factor: sigma_eff / sigma_m

    Raises:
        ValueError: If volume fraction out of range.

    References:
        Part II, Art. 334: Composite dielectric theory.
        Maxwell-Garnett effective medium theory.

    Example:
        >>> # Spherical inclusions (f=0.2) in dielectric matrix
        >>> result = composite_dielectric_conductivity(
        ...     matrix_conductivity=1e-14,
        ...     matrix_permittivity=2.0,
        ...     inclusion_conductivity=1e-10,
        ...     inclusion_permittivity=10.0,
        ...     volume_fraction=0.2,
        ...     inclusion_shape="sphere"
        ... )
        >>> print(f"sigma_eff = {result['effective_conductivity']:.2e} S/cm")
        >>> print(f"Enhancement = {result['enhancement_factor']:.1f}x")
    """
    if not 0 <= volume_fraction <= 1:
        raise ValueError(
            f"Volume fraction must be between 0 and 1, got {volume_fraction}"
        )

    # Conductivity ratio
    cond_ratio = (
        inclusion_conductivity / matrix_conductivity
        if matrix_conductivity > 0
        else float("inf")
    )

    # Maxwell-Garnett formula for spherical inclusions
    if inclusion_shape == "sphere":
        # Full Maxwell-Garnett formula
        numerator = (
            2 * (1 - volume_fraction) * matrix_conductivity
            + (1 + 2 * volume_fraction) * inclusion_conductivity
        )
        denominator = (2 + volume_fraction) * matrix_conductivity + (
            1 - volume_fraction
        ) * inclusion_conductivity

        if abs(denominator) > 1e-15:
            effective_conductivity = matrix_conductivity * numerator / denominator
        else:
            effective_conductivity = inclusion_conductivity  # Limit case

    elif inclusion_shape == "needle":
        # Needle parallel to field: simple parallel combination
        effective_conductivity = (
            1 - volume_fraction
        ) * matrix_conductivity + volume_fraction * inclusion_conductivity

    elif inclusion_shape == "disk":
        # Disk perpendicular to field: series combination
        inv_sigma_eff = (
            1 - volume_fraction
        ) / matrix_conductivity + volume_fraction / inclusion_conductivity
        effective_conductivity = 1.0 / inv_sigma_eff if inv_sigma_eff > 0 else 0.0

    elif inclusion_shape == "random":
        # Randomly oriented ellipsoids (average over orientations)
        # Uses Bruggeman symmetric formula
        if matrix_conductivity > 0 and inclusion_conductivity > 0:
            # Solve: f*(sigma_i - sigma_eff)/(sigma_i + 2*sigma_eff) + (1-f)*(sigma_m - sigma_eff)/(sigma_m + 2*sigma_eff) = 0
            # This gives the Bruggeman effective conductivity
            a = matrix_conductivity
            b = inclusion_conductivity
            f = volume_fraction

            # Quadratic solution
            A = 2
            B = a + b - 3 * f * (b - a) - 2 * a
            C = -a * b

            discriminant = B**2 - 4 * A * C
            if discriminant >= 0:
                sigma_eff1 = (-B + np.sqrt(discriminant)) / (2 * A)
                sigma_eff2 = (-B - np.sqrt(discriminant)) / (2 * A)
                effective_conductivity = max(sigma_eff1, sigma_eff2)
            else:
                effective_conductivity = matrix_conductivity  # Fallback
        else:
            effective_conductivity = matrix_conductivity

    else:
        raise ValueError(f"Unknown inclusion_shape: {inclusion_shape}")

    # Effective permittivity (same formula structure)
    perm_num = (
        2 * (1 - volume_fraction) * matrix_permittivity
        + (1 + 2 * volume_fraction) * inclusion_permittivity
    )
    perm_den = (2 + volume_fraction) * matrix_permittivity + (
        1 - volume_fraction
    ) * inclusion_permittivity
    effective_permittivity = (
        matrix_permittivity * perm_num / perm_den
        if abs(perm_den) > 1e-15
        else inclusion_permittivity
    )

    enhancement_factor = (
        effective_conductivity / matrix_conductivity
        if matrix_conductivity > 0
        else float("inf")
    )

    return {
        "effective_conductivity": effective_conductivity,
        "effective_permittivity": effective_permittivity,
        "volume_fraction": volume_fraction,
        "conductivity_ratio": cond_ratio,
        "enhancement_factor": enhancement_factor,
        "matrix_conductivity": matrix_conductivity,
        "inclusion_conductivity": inclusion_conductivity,
        "inclusion_shape": inclusion_shape,
    }


# =============================================================================
# DIELECTRIC-CONDUCTOR CLASS
# =============================================================================


@dataclass
class DielectricConductor:
    """
    Model a real dielectric with both leakage and absorption.

    This class combines:
        - Geometric capacitance C (ideal dielectric behavior)
        - Leakage resistance R (finite conductivity)
        - Absorption elements (time-dependent polarization)

    The equivalent circuit is:
        C in parallel with R, with additional RC branches for absorption.

    Attributes:
        capacitance: Geometric capacitance (abfarads).
        leakage_conductance: DC leakage G_leak (siemens).
        absorption_branches: List of (G_abs, C_abs) for absorption.
        temperature: Operating temperature (K).
    """

    capacitance: float
    leakage_conductance: float = 0.0
    absorption_branches: list[tuple[float, float]] = field(default_factory=list)
    temperature: float = 293.15

    @maxwell_cite(
        325,
        326,
        327,
        328,
        329,
        330,
        331,
        part=2,
        chapter="Conduction in Dielectric Media",
        theory_class="maxwell_original",
        description="Initialize real dielectric model",
    )
    def __post_init__(self):
        """Validate and initialize the dielectric model."""
        if self.capacitance <= 0:
            raise ValueError(f"Capacitance must be positive, got {self.capacitance}")
        if self.leakage_conductance < 0:
            raise ValueError(f"Leakage conductance must be non-negative")

        # Default absorption: single branch with 5% absorption, tau=10s
        if not self.absorption_branches:
            # G_abs and C_abs such that tau = C_abs/G_abs = 10s
            # and G_abs/G_leak represents absorption fraction
            self.absorption_branches = [
                (self.leakage_conductance * 0.05, self.capacitance * 0.05)
            ]

    @maxwell_cite(
        327,
        328,
        part=2,
        chapter="Conduction in Dielectric Media",
        theory_class="maxwell_original",
        description="Calculate steady-state leakage current",
    )
    def leakage_current(self, voltage: float) -> float:
        """
        Calculate DC leakage current at given voltage.

        Args:
            voltage: Applied voltage (abvolts).

        Returns:
            Leakage current I_leak = G_leak * V (abamperes).
        """
        return self.leakage_conductance * voltage

    @maxwell_cite(
        329,
        330,
        part=2,
        chapter="Conduction in Dielectric Media",
        theory_class="maxwell_original",
        description="Calculate absorption current at time t",
    )
    def absorption_current(self, voltage: float, time: float) -> float:
        """
        Calculate time-dependent absorption current.

        Args:
            voltage: Applied voltage (abvolts).
            time: Time since voltage application (seconds).

        Returns:
            Total absorption current I_abs(t) (abamperes).
        """
        I_abs = 0.0
        for G_abs, C_abs in self.absorption_branches:
            tau = C_abs / G_abs if G_abs > 0 else float("inf")
            I_abs += (voltage * G_abs) * np.exp(-time / tau)
        return I_abs

    @maxwell_cite(
        331,
        part=2,
        chapter="Conduction in Dielectric Media",
        theory_class="maxwell_original",
        description="Calculate residual charge after discharge",
    )
    def residual_charge_after_discharge(
        self,
        charge_voltage: float,
        charge_time: float,
        discharge_time: float,
    ) -> float:
        """
        Calculate residual charge after charging and discharging.

        Args:
            charge_voltage: Voltage during charging (abvolts).
            charge_time: Duration of charging (seconds).
            discharge_time: Time since discharge (seconds).

        Returns:
            Residual charge Q_residual (abfarads).
        """
        Q_residual = 0.0
        for G_abs, C_abs in self.absorption_branches:
            tau = C_abs / G_abs if G_abs > 0 else float("inf")
            # Charge absorbed during charging
            Q_abs = charge_voltage * C_abs * (1 - np.exp(-charge_time / tau))
            # Fraction remaining after discharge
            Q_residual += Q_abs * np.exp(-discharge_time / tau)
        return Q_residual

    @maxwell_cite(
        325,
        326,
        327,
        328,
        329,
        330,
        331,
        part=2,
        chapter="Conduction in Dielectric Media",
        theory_class="maxwell_original",
        description="Full time-domain response to voltage step",
    )
    def step_response(
        self,
        voltage: float,
        times: np.ndarray = None,
    ) -> dict[str, np.ndarray | float]:
        """
        Calculate complete time-domain response to a voltage step.

        Args:
            voltage: Step voltage magnitude (abvolts).
            times: Array of times for evaluation (seconds).

        Returns:
            Dictionary with:
            - times: Evaluation times
            - total_current: I_total(t) = I_leak + I_abs + I_cap
            - leakage_current: I_leak (constant)
            - absorption_current: I_abs(t)
            - displacement_current: I_cap(t) (impulse at t=0)
            - stored_charge: Q(t) = C*V + Q_abs(t)
        """
        if times is None:
            times = np.logspace(-3, 3, 100)  # 1ms to 1000s

        times = np.asarray(times)
        n_times = len(times)

        # Leakage current (constant)
        I_leak = np.full(n_times, self.leakage_current(voltage))

        # Absorption current (decaying)
        I_abs = np.zeros(n_times)
        Q_abs = np.zeros(n_times)
        for G_abs, C_abs in self.absorption_branches:
            tau = C_abs / G_abs if G_abs > 0 else float("inf")
            I_abs += (voltage * G_abs) * np.exp(-times / tau)
            Q_abs += voltage * C_abs * (1 - np.exp(-times / tau))

        # Total current (excluding displacement impulse at t=0)
        I_total = I_leak + I_abs

        # Total stored charge
        Q_total = self.capacitance * voltage + Q_abs

        return {
            "times": times,
            "total_current": I_total,
            "leakage_current": I_leak,
            "absorption_current": I_abs,
            "stored_charge": Q_total,
            "absorbed_charge": Q_abs,
            "voltage": voltage,
        }

    @maxwell_cite(
        325,
        326,
        327,
        328,
        329,
        330,
        331,
        part=2,
        chapter="Conduction in Dielectric Media",
        theory_class="maxwell_original",
        description="Extract equivalent circuit parameters",
    )
    def equivalent_circuit(self) -> dict[str, float]:
        """
        Return equivalent circuit parameters.

        Returns:
            Dictionary with:
            - C: Main capacitance (abfarads)
            - R_leak: Leakage resistance (abohms)
            - absorption_branches: List of (R_abs, C_abs) tuples
            - time_constants: List of tau = R*C for each branch
        """
        R_leak = (
            1.0 / self.leakage_conductance
            if self.leakage_conductance > 0
            else float("inf")
        )

        abs_branches = []
        time_constants = []
        for G_abs, C_abs in self.absorption_branches:
            R_abs = 1.0 / G_abs if G_abs > 0 else float("inf")
            tau = R_abs * C_abs
            abs_branches.append((R_abs, C_abs))
            time_constants.append(tau)

        return {
            "C": self.capacitance,
            "R_leak": R_leak,
            "absorption_branches": abs_branches,
            "time_constants": time_constants,
            "temperature": self.temperature,
        }


# =============================================================================
# MAIN: Module verification
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("CONDUCTION IN DIELECTRIC MEDIA")
    print("Maxwell's Treatise, Part II, Chapter X (Arts. 325-334)")
    print("=" * 70)

    # Test dielectric conductivity
    print("\n--- Dielectric Conductivity (Arts. 325-326) ---")
    result = dielectric_conductivity(material="glass", frequency=60.0)
    print(f"  Glass at 60 Hz:")
    print(f"    sigma = {result['conductivity']:.2e} S/cm")
    print(f"    rho = {result['resistivity']:.2e} abohm·cm")

    # Test leakage current
    print("\n--- Leakage Current (Arts. 327-328) ---")
    E = np.array([1000.0, 0.0, 0.0])
    result = leakage_current_density(E, conductivity=1e-12)
    print(f"  E = {E[0]} abV/cm, sigma = 1e-12 S/cm")
    print(f"    J_leak = {result['leakage_current']} abA/cm²")
    print(f"    |J_leak| = {result['leakage_magnitude']:.2e} abA/cm²")

    # Test dielectric absorption
    print("\n--- Dielectric Absorption (Arts. 329-330) ---")
    result = dielectric_absorption(
        voltage=100,
        capacitance=1.0,
        absorption_time=10.0,
        absorption_constants=[(0.05, 5.0), (0.03, 30.0)],
    )
    print(f"  C = 1 abF, V = 100 abV, t = 10 s")
    print(f"    Q_nominal = {result['nominal_charge']} abC")
    print(f"    Q_absorbed = {result['absorbed_charge']:.4f} abC")
    print(f"    Absorption ratio = {result['absorption_ratio']:.4f}")

    # Test absorption current
    print("\n--- Absorption Current (Arts. 329-330) ---")
    result = absorption_current(
        voltage=100, capacitance=1.0, time=5.0, absorption_constants=[(0.05, 10.0)]
    )
    print(f"  t = 5 s:")
    print(f"    I_abs = {result['absorption_current']:.6f} abA")
    print(f"    I_0 = {result['initial_current']:.6f} abA")
    print(f"    Decay ratio = {result['current_ratio']:.4f}")

    # Test residual charge
    print("\n--- Residual Charge (Art. 331) ---")
    result = residual_charge(
        initial_voltage=100,
        capacitance=1.0,
        discharge_time=30.0,
        absorption_constants=[(0.05, 10.0)],
    )
    print(f"  After 30 s discharge:")
    print(f"    Q_residual = {result['residual_charge']:.4f} abC")
    print(f"    V_residual = {result['residual_voltage']:.4f} abV")

    # Test voltage recovery
    print("\n--- Voltage Recovery (Art. 331) ---")
    result = residual_charge_recovery(
        initial_voltage=100,
        capacitance=1.0,
        open_circuit_time=60.0,
        absorption_constants=[(0.05, 10.0)],
        charge_time=100.0,
    )
    print(f"  After 60 s open circuit:")
    print(f"    V_recovered = {result['recovered_voltage']:.4f} abV")
    print(f"    Recovery fraction = {result['recovery_fraction']:.4f}")

    # Test layered dielectric
    print("\n--- Layered Dielectric (Arts. 332-333) ---")
    result = layered_dielectric(
        layer_thicknesses=[0.1, 0.2],
        layer_conductivities=[1e-12, 1e-14],
        layer_permittivities=[5.0, 6.0],
        applied_voltage=1000,
    )
    print(f"  Two-layer: d1=0.1cm (sigma=1e-12), d2=0.2cm (sigma=1e-14)")
    print(f"    J = {result['current_density']:.2e} abA/cm²")
    print(f"    E1 = {result['field_per_layer'][0]:.2e} abV/cm")
    print(f"    E2 = {result['field_per_layer'][1]:.2e} abV/cm")
    print(f"    sigma_eff = {result['effective_conductivity']:.2e} S/cm")

    # Test composite dielectric
    print("\n--- Composite Dielectric (Art. 334) ---")
    result = composite_dielectric_conductivity(
        matrix_conductivity=1e-14,
        matrix_permittivity=2.0,
        inclusion_conductivity=1e-10,
        inclusion_permittivity=10.0,
        volume_fraction=0.2,
        inclusion_shape="sphere",
    )
    print(f"  Spherical inclusions (f=0.2) in matrix:")
    print(f"    sigma_eff = {result['effective_conductivity']:.2e} S/cm")
    print(f"    Enhancement = {result['enhancement_factor']:.1f}x")

    # Test DielectricConductor class
    print("\n--- DielectricConductor Class ---")
    diel = DielectricConductor(
        capacitance=1.0, leakage_conductance=1e-12, absorption_branches=[(5e-14, 5e-13)]
    )
    print(f"  C = 1 abF, G_leak = 1e-12 S")
    print(f"  Leakage at 100 abV: I = {diel.leakage_current(100):.2e} abA")
    print(f"  Absorption at t=10s: I = {diel.absorption_current(100, 10):.2e} abA")
    response = diel.step_response(100, times=np.array([0.1, 1.0, 10.0, 100.0]))
    print(f"  Step response:")
    for t, I in zip(response["times"], response["total_current"]):
        print(f"    t={t:.1f}s: I={I:.2e} abA")

    print("\n" + "=" * 70)
    print("Module verification complete.")
    print("=" * 70)

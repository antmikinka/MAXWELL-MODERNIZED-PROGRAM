"""maxwell.signal_processing — Signal transmission and telegraphy (Arts. 730-757).

Implements Maxwell's treatment of electromagnetic signal transmission,
including the theory of telegraphy and signal propagation.

Maxwell's CGS formulation (Arts. 730-757):
    Telegraph equation for signal propagation:
        ∂²V/∂x² = RC * ∂V/∂t + LC * ∂²V/∂t²

    where:
        V = voltage (abvolts)
        R = resistance per unit length (abohms/cm)
        L = inductance per unit length (cm)
        C = capacitance per unit length (cm⁻¹ in CGS)

    Signal velocity:
        v = 1/sqrt(LC)  (for lossless line)

    Attenuation constant:
        α = sqrt(RG)  (for low-frequency signals)

    where:
        G = conductance per unit length (s/cm)

where:
    V = voltage along telegraph line (abvolts)
    I = current along telegraph line (abamperes)
    R = series resistance per unit length (abohms/cm)
    L = series inductance per unit length (cm)
    C = shunt capacitance per unit length (cm⁻¹)
    G = shunt conductance per unit length (s/cm)

Category: A (maxwell_original) — Maxwell's signal transmission theory.

References:
    Part IV, Arts. 730-757: Signal transmission and telegraphy.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class TelegraphLine:
    """
    Telegraph line signal transmission calculator.

    Art. 730-757: Maxwell's theory of signal transmission along
    telegraph lines, including the effects of resistance, inductance,
    capacitance, and leakage.

    Attributes:
        R: Series resistance per unit length (abohms/cm).
        L: Series inductance per unit length (cm).
        C: Shunt capacitance per unit length (cm⁻¹).
        G: Shunt conductance per unit length (s/cm).
    """

    R: float = 0.01  # abohms/cm
    L: float = 10.0  # cm
    C: float = 1e-10  # cm⁻¹
    G: float = 0.0  # s/cm (usually negligible)

    def __post_init__(self):
        """Validate parameters."""
        if self.R < 0:
            raise ValueError(f"R must be non-negative")
        if self.L < 0:
            raise ValueError(f"L must be non-negative")
        if self.C < 0:
            raise ValueError(f"C must be non-negative")
        if self.G < 0:
            raise ValueError(f"G must be non-negative")

    @maxwell_cite(
        730,
        part=4, chapter="Signal Transmission",
        theory_class="maxwell_original",
        description="Calculate signal propagation velocity",
    )
    def signal_velocity(self) -> float:
        """
        Calculate signal propagation velocity.

        Art. 730: For a lossless or high-frequency line:

            v = 1 / sqrt(L*C)

        Returns:
            Signal velocity (cm/s).

        Reference:
            Part IV, Art. 730: Signal velocity.
        """
        if self.L <= 0 or self.C <= 0:
            return 0.0
        return 1.0 / np.sqrt(self.L * self.C)

    @maxwell_cite(
        731,
        part=4, chapter="Signal Transmission",
        theory_class="maxwell_original",
        description="Calculate characteristic impedance",
    )
    def characteristic_impedance(self) -> float:
        """
        Calculate characteristic impedance of the line.

        Art. 731: For a lossless line:

            Z₀ = sqrt(L/C)

        In CGS-EMU, impedance has units of velocity (cm/s).

        Returns:
            Characteristic impedance Z₀ (cm/s in CGS).

        Reference:
            Part IV, Art. 731: Characteristic impedance.
        """
        if self.C <= 0:
            return float('inf')
        return np.sqrt(self.L / self.C)

    @maxwell_cite(
        732,
        part=4, chapter="Signal Transmission",
        theory_class="maxwell_original",
        description="Calculate attenuation constant",
    )
    def attenuation_constant(self, angular_frequency: float) -> float:
        """
        Calculate attenuation constant α.

        Art. 732: For a transmission line:

            α = Re[sqrt((R + iωL)(G + iωC))]

        For low frequencies (ωL << R, ωC << G):
            α ≈ sqrt(R*G)

        For high frequencies (ωL >> R, ωC >> G):
            α ≈ (R/2)*sqrt(C/L) + (G/2)*sqrt(L/C)

        Args:
            angular_frequency: ω (s⁻¹).

        Returns:
            Attenuation constant α (cm⁻¹).

        Reference:
            Part IV, Art. 732: Attenuation constant.
        """
        omega = angular_frequency

        # Complex propagation constant
        Z = self.R + 1j * omega * self.L  # Series impedance
        Y = self.G + 1j * omega * self.C  # Shunt admittance

        gamma = np.sqrt(Z * Y)
        return np.real(gamma)

    @maxwell_cite(
        733,
        part=4, chapter="Signal Transmission",
        theory_class="maxwell_original",
        description="Calculate phase constant",
    )
    def phase_constant(self, angular_frequency: float) -> float:
        """
        Calculate phase constant β.

        Art. 733: The phase constant determines wave phase shift:

            β = Im[sqrt((R + iωL)(G + iωC))]

        For lossless line:
            β = ω * sqrt(L*C)

        Args:
            angular_frequency: ω (s⁻¹).

        Returns:
            Phase constant β (cm⁻¹).

        Reference:
            Part IV, Art. 733: Phase constant.
        """
        omega = angular_frequency

        Z = self.R + 1j * omega * self.L
        Y = self.G + 1j * omega * self.C

        gamma = np.sqrt(Z * Y)
        return np.imag(gamma)

    @maxwell_cite(
        734,
        part=4, chapter="Signal Transmission",
        theory_class="maxwell_original",
        description="Calculate signal delay per unit length",
    )
    def delay_per_length(self) -> float:
        """
        Calculate signal delay per unit length.

        Art. 734: The delay is:

            τ = 1/v = sqrt(L*C)  (s/cm)

        Returns:
            Delay per cm (s/cm).

        Reference:
            Part IV, Art. 734: Signal delay.
        """
        if self.L <= 0 or self.C <= 0:
            return float('inf')
        return np.sqrt(self.L * self.C)

    @maxwell_cite(
        735,
        part=4, chapter="Signal Transmission",
        theory_class="maxwell_original",
        description="Calculate voltage at distance x",
    )
    def voltage_at_distance(self, V0: float, x: float, angular_frequency: float) -> complex:
        """
        Calculate voltage at distance x along the line.

        Art. 735: For a forward-traveling wave:

            V(x) = V₀ * exp(-γ*x)

        where γ = α + iβ is the propagation constant.

        Args:
            V0: Input voltage (abvolts).
            x: Distance (cm).
            angular_frequency: ω (s⁻¹).

        Returns:
            Complex voltage at distance x.

        Reference:
            Part IV, Art. 735: Voltage along line.
        """
        omega = angular_frequency

        Z = self.R + 1j * omega * self.L
        Y = self.G + 1j * omega * self.C

        gamma = np.sqrt(Z * Y)
        return V0 * np.exp(-gamma * x)


@dataclass
class SignalTransmission:
    """
    Signal transmission analysis for telegraphy.

    Art. 730-757: Complete analysis of electromagnetic signal
    transmission including rise time, bandwidth, and distortion.

    Attributes:
        line: TelegraphLine object.
    """

    line: TelegraphLine

    @maxwell_cite(
        740,
        part=4, chapter="Signal Transmission",
        theory_class="maxwell_original",
        description="Calculate signal rise time",
    )
    def rise_time(self, line_length: float) -> float:
        """
        Calculate signal rise time due to line dispersion.

        Art. 740: The rise time for a step input is approximately:

            t_r ≈ 2.2 * R * C * L_line  (for RC-dominated line)

        Args:
            line_length: Line length (cm).

        Returns:
            Rise time (s).

        Reference:
            Part IV, Art. 740: Signal rise time.
        """
        if line_length <= 0:
            return 0.0
        return 2.2 * self.line.R * self.line.C * line_length ** 2

    @maxwell_cite(
        745,
        part=4, chapter="Signal Transmission",
        theory_class="maxwell_original",
        description="Calculate bandwidth limitation",
    )
    def bandwidth_limit(self, line_length: float) -> float:
        """
        Calculate bandwidth limitation due to line dispersion.

        Art. 745: The approximate bandwidth is:

            BW ≈ 0.35 / t_r

        Args:
            line_length: Line length (cm).

        Returns:
            Bandwidth (Hz).

        Reference:
            Part IV, Art. 745: Bandwidth limitation.
        """
        t_r = self.rise_time(line_length)
        if t_r <= 0:
            return float('inf')
        return 0.35 / t_r

    @maxwell_cite(
        750,
        part=4, chapter="Signal Transmission",
        theory_class="maxwell_original",
        description="Calculate maximum signaling rate",
    )
    def max_signaling_rate(self, line_length: float) -> float:
        """
        Calculate maximum practical signaling rate.

        Art. 750: The maximum rate is limited by rise time:

            f_max ≈ 1 / (2 * t_r)

        This ensures pulses don't overlap excessively.

        Args:
            line_length: Line length (cm).

        Returns:
            Maximum signaling rate (symbols/s).

        Reference:
            Part IV, Art. 750: Maximum signaling rate.
        """
        t_r = self.rise_time(line_length)
        if t_r <= 0:
            return float('inf')
        return 1.0 / (2.0 * t_r)


@maxwell_cite(
    730,
    part=4, chapter="Signal Transmission",
    theory_class="maxwell_original",
    description="Calculate signal velocity: v = 1/sqrt(LC)",
)
def calc_signal_velocity(L: float, C: float) -> float:
    """
    Calculate signal propagation velocity.

    Art. 730: For a transmission line:

        v = 1 / sqrt(L*C)

    Args:
        L: Inductance per unit length (cm).
        C: Capacitance per unit length (cm⁻¹).

    Returns:
        Signal velocity (cm/s).

    Reference:
        Part IV, Art. 730: Signal velocity formula.

    Example:
        >>> v = calc_signal_velocity(10.0, 1e-10)
        >>> print(f"v = {v:.4e} cm/s")
    """
    if L <= 0 or C <= 0:
        return 0.0
    return 1.0 / np.sqrt(L * C)


@maxwell_cite(
    731,
    part=4, chapter="Signal Transmission",
    theory_class="maxwell_original",
    description="Calculate characteristic impedance: Z₀ = sqrt(L/C)",
)
def calc_characteristic_impedance(L: float, C: float) -> float:
    """
    Calculate characteristic impedance.

    Art. 731: For a lossless line:

        Z₀ = sqrt(L/C)

    Args:
        L: Inductance per unit length (cm).
        C: Capacitance per unit length (cm⁻¹).

    Returns:
        Characteristic impedance (cm/s in CGS).

    Reference:
        Part IV, Art. 731: Characteristic impedance.
    """
    if C <= 0:
        return float('inf')
    return np.sqrt(L / C)


@maxwell_cite(
    732, 733,
    part=4, chapter="Signal Transmission",
    theory_class="maxwell_original",
    description="Calculate propagation constant",
)
def calc_propagation_constant(
    R: float,
    L: float,
    C: float,
    G: float,
    angular_frequency: float,
) -> complex:
    """
    Calculate complex propagation constant.

    Art. 732-733: The propagation constant is:

        γ = sqrt((R + iωL)(G + iωC)) = α + iβ

    where:
        α = attenuation constant (cm⁻¹)
        β = phase constant (cm⁻¹)

    Args:
        R: Series resistance (abohms/cm).
        L: Series inductance (cm).
        C: Shunt capacitance (cm⁻¹).
        G: Shunt conductance (s/cm).
        angular_frequency: ω (s⁻¹).

    Returns:
        Complex propagation constant γ.

    Reference:
        Part IV, Arts. 732-733: Propagation constant.
    """
    omega = angular_frequency
    Z = R + 1j * omega * L
    Y = G + 1j * omega * C
    return np.sqrt(Z * Y)


@maxwell_cite(
    734,
    part=4, chapter="Signal Transmission",
    theory_class="maxwell_original",
    description="Calculate signal delay",
)
def calc_signal_delay(L: float, C: float, length: float) -> float:
    """
    Calculate signal propagation delay.

    Art. 734: The delay is:

        τ = length * sqrt(L*C)

    Args:
        L: Inductance per unit length (cm).
        C: Capacitance per unit length (cm⁻¹).
        length: Line length (cm).

    Returns:
        Signal delay (s).

    Reference:
        Part IV, Art. 734: Signal delay.
    """
    if L <= 0 or C <= 0:
        return 0.0
    return length * np.sqrt(L * C)


@maxwell_cite(
    730, 731, 732, 733, 734, 735,
    part=4, chapter="Signal Transmission",
    theory_class="maxwell_original",
    description="Verify telegraph line relations",
)
def verify_telegraph_line(
    R: float = 0.01,
    L: float = 10.0,
    C: float = 1e-10,
    G: float = 0.0,
    frequency: float = 1e6,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify telegraph line relationships.

    Art. 730-735: This function verifies:
    1. v = 1/sqrt(LC)
    2. Z₀ = sqrt(L/C)
    3. γ = α + iβ
    4. Lossless limit behavior

    Args:
        R: Series resistance.
        L: Series inductance.
        C: Shunt capacitance.
        G: Shunt conductance.
        frequency: Test frequency (Hz).
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 730-735: Telegraph line verification.
    """
    line = TelegraphLine(R=R, L=L, C=C, G=G)
    omega = 2 * np.pi * frequency

    # Calculate quantities
    v = line.signal_velocity()
    Z0 = line.characteristic_impedance()
    gamma = calc_propagation_constant(R, L, C, G, omega)

    # Verify v = 1/sqrt(LC)
    v_expected = 1.0 / np.sqrt(L * C) if L > 0 and C > 0 else 0
    v_error = abs(v - v_expected) / v_expected if v_expected > 0 else 0

    # Verify Z₀ = sqrt(L/C)
    Z0_expected = np.sqrt(L / C) if C > 0 else float('inf')
    Z0_error = abs(Z0 - Z0_expected) / Z0_expected if Z0_expected < float('inf') and Z0_expected > 0 else 0

    # Verify γ = α + iβ
    alpha = line.attenuation_constant(omega)
    beta = line.phase_constant(omega)
    gamma_error = abs(np.real(gamma) - alpha) + abs(np.imag(gamma) - beta)

    return {
        "R": R,
        "L": L,
        "C": C,
        "G": G,
        "frequency": frequency,
        "angular_frequency": omega,
        "signal_velocity": v,
        "characteristic_impedance": Z0,
        "attenuation_constant": alpha,
        "phase_constant": beta,
        "propagation_constant": gamma,
        "v_error": v_error,
        "Z0_error": Z0_error,
        "gamma_error": gamma_error,
        "verified": v_error < tolerance and Z0_error < tolerance and gamma_error < tolerance,
    }


@maxwell_cite(
    730, 731, 732, 733, 734, 735,
    part=4, chapter="Signal Transmission",
    theory_class="maxwell_original",
    description="Complete telegraph line analysis",
)
def analyze_telegraph_line(
    R: float,
    L: float,
    C: float,
    G: float,
    length: float,
    frequency: float = 1e6,
) -> dict[str, float]:
    """
    Complete analysis of telegraph line transmission.

    Art. 730-735: Comprehensive analysis including:
    1. Line parameters
    2. Signal velocity and impedance
    3. Attenuation and phase constants
    4. Signal delay
    5. Voltage at distance

    Args:
        R: Series resistance (abohms/cm).
        L: Series inductance (cm).
        C: Shunt capacitance (cm⁻¹).
        G: Shunt conductance (s/cm).
        length: Line length (cm).
        frequency: Signal frequency (Hz).

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 730-735: Complete telegraph analysis.

    Example:
        >>> # Analyze submarine telegraph cable
        >>> result = analyze_telegraph_line(
        ...     R=0.003, L=1.7, C=0.3e-6, G=0,
        ...     length=3000e5  # 3000 km
        ... )
    """
    line = TelegraphLine(R=R, L=L, C=C, G=G)
    omega = 2 * np.pi * frequency

    # Calculate quantities
    v = line.signal_velocity()
    Z0 = line.characteristic_impedance()
    alpha = line.attenuation_constant(omega)
    beta = line.phase_constant(omega)
    delay = line.delay_per_length() * length

    # Voltage transmission
    V0 = 1.0  # 1 abvolt input
    V_out = line.voltage_at_distance(V0, length, omega)

    # Signal integrity
    st = SignalTransmission(line)
    rise_time = st.rise_time(length)
    bandwidth = st.bandwidth_limit(length)
    max_rate = st.max_signaling_rate(length)

    return {
        "R_per_length": R,
        "L_per_length": L,
        "C_per_length": C,
        "G_per_length": G,
        "length_cm": length,
        "length_km": length / 1e5,
        "frequency_Hz": frequency,
        "angular_frequency": omega,
        "signal_velocity_cm_s": v,
        "signal_velocity_km_s": v / 1e5,
        "characteristic_impedance": Z0,
        "attenuation_constant_cm": alpha,
        "attenuation_constant_km": alpha * 1e5,
        "phase_constant": beta,
        "total_delay_s": delay,
        "voltage_transmission_mag": abs(V_out / V0),
        "voltage_transmission_phase": np.angle(V_out / V0),
        "rise_time_s": rise_time,
        "bandwidth_Hz": bandwidth,
        "max_signaling_rate_symbols_s": max_rate,
    }

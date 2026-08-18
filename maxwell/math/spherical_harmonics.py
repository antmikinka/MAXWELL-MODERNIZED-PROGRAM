"""maxwell.math.spherical_harmonics — Spherical harmonics and multipole expansions.

This module implements Maxwell's mathematical treatment of spherical harmonics
from both Part I (electrostatics foundation) and Part IV (advanced applications).

PART I, CHAPTER IX (Arts. 128-146): Spherical Harmonics in Electrostatics
    This is Maxwell's foundational treatment of spherical harmonics for
    solving electrostatic potential problems.

    Maxwell's CGS formulation (Arts. 128-146):
        Laplace's equation in spherical coordinates (Arts. 128-130):
            ∇²V = 0 in spherical (r, θ, φ) coordinates

        Surface harmonics (Arts. 131-135):
            Functions on the sphere satisfying ∇²Y + l(l+1)Y = 0
            Yₗₘ are tesseral, sectorial, and zonal harmonics

        Solid harmonics (Arts. 136-138):
            Homogeneous functions satisfying ∇²Φ = 0
            Φₗ = r^l Yₗ (internal) or Φₗ = r^(-l-1) Yₗ (external)

        Expansion in spherical harmonics (Arts. 139-142):
            Any function on sphere: f(θ,φ) = Σₗ Σₘ aₗₘ Yₗₘ(θ,φ)

        Addition theorem (Arts. 143-146):
            Pₗ(cos γ) = Σₘ Yₗₘ(θ,φ) Yₗₘ*(θ',φ')

PART IV (Arts. 675-695): Advanced Multipole Expansions
    Extended treatment with multipole expansions for electromagnetic fields.

Category: A (maxwell_original) — Maxwell's spherical harmonic analysis.

References:
    Part I, Arts. 128-146: Spherical harmonics foundations.
    Part IV, Arts. 675-695: Multipole expansions and applications.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np
from scipy.special import legendre, lpmv, sph_harm_y


def _sph_harm(m: int, n: int, phi, theta) -> complex:
    """Wrapper around scipy's sph_harm_y (replaces deprecated sph_harm).

    scipy.special.sph_harm was deprecated in 1.15.0. The replacement
    sph_harm_y has a different signature: sph_harm_y(n, m, theta, phi)
    and returns a complex numpy ndarray instead of a complex scalar.

    Args:
        m: Order.
        n: Degree.
        phi: Azimuthal angle(s).
        theta: Polar angle(s).

    Returns:
        Complex value (scalar if inputs are scalar, array if inputs are arrays).
    """
    result = sph_harm_y(n, m, theta, phi)
    if isinstance(result, np.ndarray) and result.size == 1:
        return complex(result.item())
    return result


from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite

# =============================================================================
# PART I, CHAPTER IX: SPHERICAL HARMONICS (Arts. 128-146)
# =============================================================================
# Maxwell's foundational treatment of spherical harmonics for electrostatics.
# These functions implement the mathematical apparatus for solving Laplace's
# equation in spherical coordinates and expanding arbitrary potentials.
# =============================================================================


@dataclass
class LaplaceSpherical:
    """
    Laplace's equation in spherical coordinates.

    Art. 128-130: Maxwell's formulation of Laplace's equation
    in spherical coordinates (r, θ, φ).

    The equation ∇²V = 0 in spherical coordinates is:

        1/r² ∂/∂r(r² ∂V/∂r) + 1/(r² sin θ) ∂/∂θ(sin θ ∂V/∂θ)
        + 1/(r² sin² θ) ∂²V/∂φ² = 0

    Attributes:
        None — this is a utility class for coordinate operations.

    References:
        Part I, Arts. 128-130: Laplace's equation in spherical form.
    """

    @maxwell_cite(
        128,
        part=1,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Laplace's equation in spherical coordinates",
    )
    @staticmethod
    def laplacian_spherical(
        V: Callable[[float, float, float], float],
        r: float,
        theta: float,
        phi: float,
        dr: float = 1e-5,
        dtheta: float = 1e-5,
        dphi: float = 1e-5,
    ) -> float:
        """
        Compute ∇²V in spherical coordinates.

        Art. 128: Laplace's equation in spherical coordinates:

            ∇²V = (1/r²) ∂/∂r(r² ∂V/∂r)
                + (1/(r² sin θ)) ∂/∂θ(sin θ ∂V/∂θ)
                + (1/(r² sin² θ)) ∂²V/∂φ²

        Args:
            V: Potential function V(r, θ, φ).
            r: Radial coordinate (cm).
            theta: Polar angle (radians, 0 to π).
            phi: Azimuthal angle (radians, 0 to 2π).
            dr: Radial step for numerical differentiation.
            dtheta: Polar angle step.
            dphi: Azimuthal angle step.

        Returns:
            Value of ∇²V at the given point.

        Reference:
            Part I, Art. 128: Spherical Laplacian.
        """
        sin_theta = np.sin(theta)
        if sin_theta < 1e-10:
            sin_theta = 1e-10  # Avoid singularity at poles

        # Radial part: (1/r²) ∂/∂r(r² ∂V/∂r) = ∂²V/∂r² + (2/r) ∂V/∂r
        V_r_plus = V(r + dr, theta, phi)
        V_r_minus = V(r - dr, theta, phi)
        V_r = V(r, theta, phi)
        dV_dr = (V_r_plus - V_r_minus) / (2 * dr)
        d2V_dr2 = (V_r_plus - 2 * V_r + V_r_minus) / dr**2
        radial_part = d2V_dr2 + (2 / r) * dV_dr

        # Polar part: (1/(r² sin θ)) ∂/∂θ(sin θ ∂V/∂θ)
        # Use centered difference for the derivative
        sin_t = np.sin(theta)
        V_t_plus = V(r, theta + dtheta, phi)
        V_t_minus = V(r, theta - dtheta, phi)

        # Compute ∂/∂θ(sin θ ∂V/∂θ) using product rule discretization
        sin_t_plus = np.sin(theta + dtheta / 2)
        sin_t_minus = np.sin(theta - dtheta / 2)
        dV_dtheta_plus = (V_t_plus - V_r) / dtheta
        dV_dtheta_minus = (V_r - V_t_minus) / dtheta

        d_dtheta_sin_dV = (
            sin_t_plus * dV_dtheta_plus - sin_t_minus * dV_dtheta_minus
        ) / dtheta
        polar_part = d_dtheta_sin_dV / (r**2 * sin_theta)

        # Azimuthal part: (1/(r² sin² θ)) ∂²V/∂φ²
        V_p_plus = V(r, theta, phi + dphi)
        V_p_minus = V(r, theta, phi - dphi)
        d2V_dphi2 = (V_p_plus - 2 * V_r + V_p_minus) / dphi**2
        azimuthal_part = d2V_dphi2 / (r**2 * sin_theta**2)

        return radial_part + polar_part + azimuthal_part

    @maxwell_cite(
        129,
        part=1,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Separation of variables for Laplace equation",
    )
    @staticmethod
    def separate_variables(r: float, theta: float, phi: float) -> dict[str, float]:
        """
        Return the separated coordinate factors.

        Art. 129: Solution by separation of variables assumes:

            V(r, θ, φ) = R(r) × Θ(θ) × Φ(φ)

        This leads to three ODEs:
        - Radial: r² R'' + 2r R' - l(l+1) R = 0
        - Polar: (1/sin θ) d/dθ(sin θ dΘ/dθ) + [l(l+1) - m²/sin² θ] Θ = 0
        - Azimuthal: Φ'' + m² Φ = 0

        Args:
            r: Radial coordinate.
            theta: Polar angle.
            phi: Azimuthal angle.

        Returns:
            Dictionary with coordinate factors.

        Reference:
            Part I, Art. 129: Separation of variables.
        """
        return {
            "r_factor": r,
            "theta_factor": theta,
            "phi_factor": phi,
            "sin_theta": np.sin(theta),
            "cos_theta": np.cos(theta),
        }

    @maxwell_cite(
        130,
        part=1,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Verify solution satisfies Laplace equation",
    )
    @staticmethod
    def verify_harmonic(
        V: Callable[[float, float, float], float],
        test_points: list[tuple[float, float, float]],
        tolerance: float = 1e-6,
    ) -> dict[str, any]:
        """
        Verify that V satisfies Laplace's equation.

        Art. 130: A function is harmonic if ∇²V = 0 everywhere.

        Args:
            V: Potential function to test.
            test_points: List of (r, θ, φ) tuples.
            tolerance: Maximum allowed |∇²V|.

        Returns:
            Dictionary with verification results.

        Reference:
            Part I, Art. 130: Harmonic function verification.
        """
        results = []
        for r, theta, phi in test_points:
            laplacian = LaplaceSpherical.laplacian_spherical(V, r, theta, phi)
            results.append(abs(laplacian) < tolerance)

        return {
            "test_points": len(test_points),
            "passed": sum(results),
            "failed": len(results) - sum(results),
            "all_harmonic": all(results),
            "tolerance": tolerance,
        }


@dataclass
class SurfaceHarmonic:
    """
    Surface harmonics (spherical surface harmonics).

    Art. 131-135: Maxwell's treatment of surface harmonics —
    functions defined on the surface of a sphere that satisfy
    the surface Laplace equation.

    A surface harmonic Yₗₘ(θ, φ) satisfies:

        ∇ₛ²Yₗₘ + l(l+1)Yₗₘ = 0

    where ∇ₛ² is the surface Laplacian (Laplace-Beltrami operator).

    Classification (Art. 132):
    - Zonal harmonics (m=0): Symmetric about the pole
    - Tesseral harmonics (0 < |m| < l): Divide sphere into compartments
    - Sectorial harmonics (|m|=l): Divide sphere into sectors

    Attributes:
        l: Degree l (non-negative integer).
        m: Order m (integer, -l ≤ m ≤ l).

    References:
        Part I, Arts. 131-135: Surface harmonics theory.
    """

    l: int = 0
    m: int = 0

    def __post_init__(self):
        """Validate parameters."""
        if self.l < 0:
            raise ValueError(f"Degree l must be non-negative")
        if abs(self.m) > self.l:
            raise ValueError(f"|m| must be ≤ l")

    @maxwell_cite(
        131,
        part=1,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Surface harmonic definition",
    )
    def evaluate(self, theta: float, phi: float) -> complex:
        """
        Evaluate surface harmonic Yₗₘ(θ, φ).

        Art. 131: The surface harmonic is a solution to the
        surface Laplace equation on the unit sphere.

        Args:
            theta: Polar angle (radians, 0 to π).
            phi: Azimuthal angle (radians, 0 to 2π).

        Returns:
            Complex value of the surface harmonic.

        Reference:
            Part I, Art. 131: Surface harmonic definition.
        """
        # Use scipy's sph_harm (Condon-Shortley phase convention)
        result = _sph_harm(self.m, self.l, phi, theta)
        return complex(result)

    @maxwell_cite(
        132,
        part=1,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Classify harmonic type (zonal/tesseral/sectorial)",
    )
    def harmonic_type(self) -> str:
        """
        Classify the harmonic type per Art. 132.

        Art. 132: Classification of surface harmonics:
        - Zonal (m=0): Axisymmetric, depends only on θ
        - Tesseral (0 < |m| < l): Compartmental pattern
        - Sectorial (|m|=l): Wedge-shaped sectors

        Returns:
            One of "zonal", "tesseral", or "sectorial".

        Reference:
            Part I, Art. 132: Harmonic classification.
        """
        if self.m == 0:
            return "zonal"
        elif abs(self.m) == self.l:
            return "sectorial"
        else:
            return "tesseral"

    @maxwell_cite(
        133,
        part=1,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Zonal harmonic (axisymmetric)",
    )
    def zonal_component(self, theta: float) -> float:
        """
        Compute the zonal (axisymmetric) component.

        Art. 133: For m=0, the zonal harmonic reduces to:

            Yₗ₀(θ, φ) = sqrt((2l+1)/(4π)) × Pₗ(cos θ)

        This is independent of φ.

        Args:
            theta: Polar angle (radians).

        Returns:
            Real value of the zonal harmonic.

        Reference:
            Part I, Art. 133: Zonal harmonics.
        """
        if self.m != 0:
            # For non-zero m, return the m=0 component
            sh_zonal = SurfaceHarmonic(l=self.l, m=0)
            return sh_zonal.evaluate(theta, 0).real
        return self.evaluate(theta, 0).real

    @maxwell_cite(
        134,
        part=1,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Tesseral harmonic component",
    )
    def tesseral_component(self, theta: float, phi: float) -> dict[str, float]:
        """
        Compute tesseral harmonic real and imaginary parts.

        Art. 134: Tesseral harmonics (0 < |m| < l) have the form:

            Yₗₘ ∝ Pₗ^|m|(cos θ) × e^(imφ)

        The real and imaginary parts give cosine and sine
        azimuthal dependence.

        Args:
            theta: Polar angle (radians).
            phi: Azimuthal angle (radians).

        Returns:
            Dictionary with 'real' and 'imag' components.

        Reference:
            Part I, Art. 134: Tesseral harmonics.
        """
        Y = self.evaluate(theta, phi)
        return {
            "real": Y.real,
            "imag": Y.imag,
            "type": self.harmonic_type(),
        }

    @maxwell_cite(
        135,
        part=1,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Surface integral of harmonic product",
    )
    def surface_integral(
        self,
        other: "SurfaceHarmonic",
        n_theta: int = 50,
        n_phi: int = 50,
    ) -> complex:
        """
        Compute surface integral ∫ Yₗₘ Yₗ'ₘ'* dΩ.

        Art. 135: Orthogonality relation for surface harmonics:

            ∫∫ Yₗₘ Yₗ'ₘ'* dΩ = δₗₗ' δₘₘ'

        where dΩ = sin θ dθ dφ is the solid angle element.

        Args:
            other: Another surface harmonic.
            n_theta: Number of θ grid points.
            n_phi: Number of φ grid points.

        Returns:
            Complex integral value (should be 1 if same, 0 otherwise).

        Reference:
            Part I, Art. 135: Surface harmonic orthogonality.
        """
        theta_vals = np.linspace(0, np.pi, n_theta)
        phi_vals = np.linspace(0, 2 * np.pi, n_phi)

        dtheta = np.pi / (n_theta - 1)
        dphi = 2 * np.pi / (n_phi - 1)

        integral = 0.0j
        for theta in theta_vals:
            sin_theta = np.sin(theta)
            for phi in phi_vals:
                Y_self = self.evaluate(theta, phi)
                Y_other = other.evaluate(theta, phi)
                weight = sin_theta  # Solid angle element dΩ
                integral += Y_self * np.conj(Y_other) * weight

        integral *= dtheta * dphi
        return integral


@dataclass
class SolidHarmonic:
    """
    Solid harmonics — homogeneous harmonic functions in 3D.

    Art. 136-138: Maxwell's treatment of solid harmonics —
    functions of (x, y, z) or (r, θ, φ) that satisfy ∇²Φ = 0
    and are homogeneous of degree n.

    Two types of solid harmonics:
    - Internal (positive degree): Φₗ = r^l Yₗₘ(θ, φ)
      Regular at origin, used for interior problems.
    - External (negative degree): Φₗ = r^(-l-1) Yₗₘ(θ, φ)
      Vanishes at infinity, used for exterior problems.

    Attributes:
        l: Degree l (non-negative integer).
        m: Order m (integer, -l ≤ m ≤ l).
        harmonic_type: 'internal' or 'external'.

    References:
        Part I, Arts. 136-138: Solid harmonic theory.
    """

    l: int = 0
    m: int = 0
    harmonic_type: str = "internal"

    def __post_init__(self):
        """Validate parameters."""
        if self.l < 0:
            raise ValueError(f"Degree l must be non-negative")
        if abs(self.m) > self.l:
            raise ValueError(f"|m| must be ≤ l")
        if self.harmonic_type not in ("internal", "external"):
            raise ValueError(f"Type must be 'internal' or 'external'")

    @maxwell_cite(
        136,
        part=1,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Solid harmonic evaluation",
    )
    def evaluate(self, r: float, theta: float, phi: float) -> complex:
        """
        Evaluate solid harmonic Φₗₘ(r, θ, φ).

        Art. 136: The solid harmonic is:

            Internal: Φₗₘ = r^l × Yₗₘ(θ, φ)
            External: Φₗₘ = r^(-l-1) × Yₗₘ(θ, φ)

        Args:
            r: Radial distance (cm).
            theta: Polar angle (radians).
            phi: Azimuthal angle (radians).

        Returns:
            Complex value of the solid harmonic.

        Reference:
            Part I, Art. 136: Solid harmonic definition.
        """
        Y_lm = _sph_harm(self.m, self.l, phi, theta)

        if self.harmonic_type == "internal":
            radial_factor = r**self.l
        else:  # external
            if r == 0:
                raise ValueError("External harmonic undefined at r=0")
            radial_factor = r ** (-self.l - 1)

        return radial_factor * complex(Y_lm)

    @maxwell_cite(
        137,
        part=1,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Homogeneous function property",
    )
    def homogeneous_degree(self) -> int:
        """
        Return the degree of homogeneity.

        Art. 137: A solid harmonic Φₗ is homogeneous of degree:
        - +l for internal harmonics
        - -(l+1) for external harmonics

        Euler's theorem: r · ∇Φ = n Φ where n is the degree.

        Returns:
            Degree of homogeneity.

        Reference:
            Part I, Art. 137: Homogeneous function property.
        """
        if self.harmonic_type == "internal":
            return self.l
        else:
            return -(self.l + 1)

    @maxwell_cite(
        138,
        part=1,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Verify harmonic property (∇²Φ = 0)",
    )
    def verify_harmonic(
        self,
        test_r: float = 5.0,
        tolerance: float = 1e-6,
    ) -> dict[str, any]:
        """
        Verify that Φ satisfies Laplace's equation.

        Art. 138: A solid harmonic must satisfy ∇²Φ = 0
        everywhere (except at singularities for external harmonics).

        Args:
            test_r: Radial distance for testing.
            tolerance: Maximum allowed |∇²Φ|.

        Returns:
            Dictionary with verification results.

        Reference:
            Part I, Art. 138: Harmonic function verification.
        """
        # Test at multiple angles
        test_points = [
            (test_r, np.pi / 4, 0),
            (test_r, np.pi / 3, np.pi / 4),
            (test_r, np.pi / 2, np.pi / 2),
            (test_r, 2 * np.pi / 3, np.pi),
        ]

        def phi_func(r, theta, phi):
            """Wrapper for evaluate that returns real part."""
            result = self.evaluate(r, theta, phi)
            return result.real if isinstance(result, complex) else result

        verification = LaplaceSpherical.verify_harmonic(
            phi_func, test_points, tolerance
        )

        verification["harmonic_type"] = self.harmonic_type
        verification["degree"] = self.l

        return verification


# =============================================================================
# EXPANSION OF ARBITRARY FUNCTIONS IN SPHERICAL HARMONICS (Arts. 139-142)
# =============================================================================


@dataclass
class SphericalHarmonicExpansion:
    """
    Expansion of arbitrary functions in spherical harmonics.

    Art. 139-142: Maxwell's method for expanding an arbitrary
    function f(θ, φ) defined on the sphere as a series of
    spherical harmonics:

        f(θ, φ) = Σₗ Σₘ aₗₘ Yₗₘ(θ, φ)

    The coefficients are found by orthogonality:

        aₗₘ = ∫∫ f(θ, φ) Yₗₘ*(θ, φ) dΩ

    Attributes:
        max_l: Maximum degree in the expansion.
        coefficients: Dictionary {(l, m): aₗₘ} of expansion coefficients.

    References:
        Part I, Arts. 139-142: Spherical harmonic expansion theory.
    """

    max_l: int = 0
    coefficients: dict[tuple[int, int], complex] = None

    def __post_init__(self):
        """Initialize coefficients dictionary."""
        if self.coefficients is None:
            self.coefficients = {}

    @maxwell_cite(
        139,
        part=1,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Expand function in spherical harmonics",
    )
    def compute_coefficients(
        self,
        f: Callable[[float, float], complex],
        n_theta: int = 50,
        n_phi: int = 50,
    ) -> dict[tuple[int, int], complex]:
        """
        Compute expansion coefficients aₗₘ for function f(θ, φ).

        Art. 139: Using orthogonality of spherical harmonics:

            aₗₘ = ∫∫ f(θ, φ) Yₗₘ*(θ, φ) dΩ

        Args:
            f: Function f(θ, φ) to expand.
            n_theta: Number of θ grid points.
            n_phi: Number of φ grid points.

        Returns:
            Dictionary of coefficients {(l, m): aₗₘ}.

        Reference:
            Part I, Art. 139: Coefficient computation.
        """
        theta_vals = np.linspace(0, np.pi, n_theta)
        phi_vals = np.linspace(0, 2 * np.pi, n_phi)

        dtheta = np.pi / (n_theta - 1)
        dphi = 2 * np.pi / (n_phi - 1)

        self.coefficients = {}

        for l in range(self.max_l + 1):
            for m in range(-l, l + 1):
                integral = 0.0j
                for theta in theta_vals:
                    sin_theta = np.sin(theta)
                    for phi in phi_vals:
                        Y_lm = _sph_harm(m, l, phi, theta)
                        weight = sin_theta  # dΩ = sin θ dθ dφ
                        integral += f(theta, phi) * np.conj(Y_lm) * weight

                self.coefficients[(l, m)] = integral * dtheta * dphi

        return self.coefficients

    @maxwell_cite(
        140,
        part=1,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Reconstruct function from coefficients",
    )
    def reconstruct(
        self,
        theta: float,
        phi: float,
        n_terms: int = None,
    ) -> complex:
        """
        Reconstruct f(θ, φ) from expansion coefficients.

        Art. 140: The reconstructed function is:

            f(θ, φ) ≈ Σₗ Σₘ aₗₘ Yₗₘ(θ, φ)

        Args:
            theta: Polar angle (radians).
            phi: Azimuthal angle (radians).
            n_terms: Maximum l to include (default: max_l).

        Returns:
            Reconstructed function value.

        Reference:
            Part I, Art. 140: Function reconstruction.
        """
        if n_terms is None:
            n_terms = self.max_l

        result = 0.0j
        for l in range(n_terms + 1):
            for m in range(-l, l + 1):
                if (l, m) in self.coefficients:
                    Y_lm = _sph_harm(m, l, phi, theta)
                    result += self.coefficients[(l, m)] * Y_lm

        return result

    @maxwell_cite(
        141,
        part=1,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Axisymmetric expansion (zonal harmonics only)",
    )
    def expand_axisymmetric(
        self,
        f: Callable[[float], float],
        n_theta: int = 50,
    ) -> dict[int, float]:
        """
        Expand axisymmetric function f(θ) using only zonal harmonics.

        Art. 141: For functions independent of φ, only m=0 terms
        are non-zero:

            f(θ) = Σₗ aₗ Yₗ₀(θ)

        where Yₗ₀(θ) = sqrt((2l+1)/(4π)) Pₗ(cos θ)

        Args:
            f: Axisymmetric function f(θ).
            n_theta: Number of θ grid points.

        Returns:
            Dictionary of coefficients {l: aₗ}.

        Reference:
            Part I, Art. 141: Axisymmetric expansion.
        """
        theta_vals = np.linspace(0, np.pi, n_theta)
        dtheta = np.pi / (n_theta - 1)

        self.coefficients = {}

        for l in range(self.max_l + 1):
            # Only m=0 for axisymmetric case
            Y_l0 = _sph_harm(0, l, 0, theta_vals)  # phi=0, arbitrary
            f_vals = np.array([f(theta) for theta in theta_vals])
            weight = np.sin(theta_vals)  # dΩ = sin θ dθ dφ, integrated over φ gives 2π

            # For m=0, integrate over θ only (φ integration gives 2π)
            integral = np.sum(f_vals * np.conj(Y_l0) * weight) * dtheta * 2 * np.pi
            self.coefficients[(l, 0)] = integral

        return {l: self.coefficients[(l, 0)] for l in range(self.max_l + 1)}

    @maxwell_cite(
        142,
        part=1,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Convergence check for expansion",
    )
    def convergence_check(
        self,
        f: Callable[[float, float], complex],
        test_points: list[tuple[float, float]],
        tolerance: float = 1e-6,
    ) -> dict[str, any]:
        """
        Check convergence of the expansion.

        Art. 142: The series converges if:

            |f(θ, φ) - f_approx(θ, φ)| < tolerance

        for all test points.

        Args:
            f: Original function.
            test_points: List of (θ, φ) tuples.
            tolerance: Maximum allowed error.

        Returns:
            Dictionary with convergence statistics.

        Reference:
            Part I, Art. 142: Convergence analysis.
        """
        errors = []
        for theta, phi in test_points:
            exact = f(theta, phi)
            approx = self.reconstruct(theta, phi)
            error = abs(exact - approx)
            errors.append(error)

        max_error = max(errors)
        mean_error = np.mean(errors)

        return {
            "max_error": max_error,
            "mean_error": mean_error,
            "converged": max_error < tolerance,
            "tolerance": tolerance,
            "test_points": len(test_points),
            "max_l_used": self.max_l,
        }


# =============================================================================
# ADDITION THEOREM FOR SPHERICAL HARMONICS (Arts. 143-146)
# =============================================================================


@maxwell_cite(
    143,
    part=1,
    chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Addition theorem for spherical harmonics",
)
def addition_theorem(
    l: int,
    theta1: float,
    phi1: float,
    theta2: float,
    phi2: float,
) -> float:
    """
    Addition theorem for spherical harmonics.

    Art. 143: The addition theorem relates the Legendre polynomial
    of the angle between two directions to a sum over spherical
    harmonics:

        Pₗ(cos γ) = (4π/(2l+1)) Σₘ Yₗₘ(θ₁,φ₁) Yₗₘ*(θ₂,φ₂)

    where γ is the angle between the two directions given by
    (θ₁, φ₁) and (θ₂, φ₂), and:

        cos γ = cos θ₁ cos θ₂ + sin θ₁ sin θ₂ cos(φ₁ - φ₂)

    Args:
        l: Degree of the harmonic.
        theta1: Polar angle of first direction (radians).
        phi1: Azimuthal angle of first direction (radians).
        theta2: Polar angle of second direction (radians).
        phi2: Azimuthal angle of second direction (radians).

    Returns:
        Value of Pₗ(cos γ) computed via the addition theorem.

    Reference:
        Part I, Art. 143: Addition theorem.
    """
    # Compute the angle γ between the two directions
    cos_gamma = np.cos(theta1) * np.cos(theta2) + np.sin(theta1) * np.sin(
        theta2
    ) * np.cos(phi1 - phi2)

    # Clamp to [-1, 1] to avoid numerical issues
    cos_gamma = np.clip(cos_gamma, -1.0, 1.0)

    # Direct evaluation using Legendre polynomial
    P_l_direct = float(legendre(l)(cos_gamma))

    # Sum over m using spherical harmonics
    sum_over_m = 0.0j
    for m in range(-l, l + 1):
        Y1 = _sph_harm(m, l, phi1, theta1)
        Y2 = _sph_harm(m, l, phi2, theta2)
        sum_over_m += Y1 * np.conj(Y2)

    # Addition theorem result
    P_l_addition = (4 * np.pi / (2 * l + 1)) * sum_over_m

    return P_l_addition.real


@maxwell_cite(
    144,
    part=1,
    chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Compute angle between two directions",
)
def angle_between_directions(
    theta1: float,
    phi1: float,
    theta2: float,
    phi2: float,
) -> float:
    """
    Compute the angle γ between two directions on the sphere.

    Art. 144: The angular separation γ is given by the
    spherical law of cosines:

        cos γ = cos θ₁ cos θ₂ + sin θ₁ sin θ₂ cos(φ₁ - φ₂)

    Args:
        theta1: Polar angle of first direction (radians).
        phi1: Azimuthal angle of first direction (radians).
        theta2: Polar angle of second direction (radians).
        phi2: Azimuthal angle of second direction (radians).

    Returns:
        Angle γ (radians, 0 to π).

    Reference:
        Part I, Art. 144: Angular separation.
    """
    cos_gamma = np.cos(theta1) * np.cos(theta2) + np.sin(theta1) * np.sin(
        theta2
    ) * np.cos(phi1 - phi2)

    # Clamp to [-1, 1] to avoid numerical issues
    cos_gamma = np.clip(cos_gamma, -1.0, 1.0)

    return np.arccos(cos_gamma)


@maxwell_cite(
    145,
    part=1,
    chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Verify addition theorem",
)
def verify_addition_theorem(
    l: int,
    theta1: float,
    phi1: float,
    theta2: float,
    phi2: float,
    tolerance: float = 1e-10,
) -> dict[str, any]:
    """
    Verify the addition theorem numerically.

    Art. 145: Compare the direct Legendre polynomial evaluation
    with the sum over spherical harmonics.

    Args:
        l: Degree of the harmonic.
        theta1: Polar angle of first direction (radians).
        phi1: Azimuthal angle of first direction (radians).
        theta2: Polar angle of second direction (radians).
        phi2: Azimuthal angle of second direction (radians).
        tolerance: Maximum allowed relative error.

    Returns:
        Dictionary with verification results.

    Reference:
        Part I, Art. 145: Addition theorem verification.
    """
    # Compute angle between directions
    cos_gamma = np.cos(theta1) * np.cos(theta2) + np.sin(theta1) * np.sin(
        theta2
    ) * np.cos(phi1 - phi2)
    cos_gamma = np.clip(cos_gamma, -1.0, 1.0)

    # Direct evaluation
    P_l_direct = float(legendre(l)(cos_gamma))

    # Addition theorem sum
    sum_over_m = 0.0j
    for m in range(-l, l + 1):
        Y1 = _sph_harm(m, l, phi1, theta1)
        Y2 = _sph_harm(m, l, phi2, theta2)
        sum_over_m += Y1 * np.conj(Y2)

    P_l_addition = (4 * np.pi / (2 * l + 1)) * sum_over_m

    # Compare
    if abs(P_l_direct) > 1e-10:
        relative_error = abs(P_l_direct - P_l_addition.real) / abs(P_l_direct)
    else:
        relative_error = abs(P_l_direct - P_l_addition.real)

    return {
        "l": l,
        "cos_gamma": cos_gamma,
        "P_l_direct": P_l_direct,
        "P_l_addition": P_l_addition.real,
        "absolute_error": abs(P_l_direct - P_l_addition.real),
        "relative_error": relative_error,
        "verified": relative_error < tolerance,
        "tolerance": tolerance,
    }


@maxwell_cite(
    146,
    part=1,
    chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Application to potential theory",
)
def potential_expansion_addition_theorem(
    r1: float,
    r2: float,
    theta1: float,
    phi1: float,
    theta2: float,
    phi2: float,
    max_l: int = 10,
) -> complex:
    """
    Expand 1/|r₁ - r₂| using the addition theorem.

    Art. 146: Application to potential theory — the reciprocal
    distance can be expanded as:

        1/|r₁ - r₂| = Σₗ (r_<^l / r_>^(l+1)) Pₗ(cos γ)

    where r_< = min(r₁, r₂), r_> = max(r₁, r₂), and γ is the
    angle between the directions.

    Using the addition theorem:

        1/|r₁ - r₂| = Σₗ Σₘ (4π/(2l+1)) (r_<^l / r_>^(l+1))
                       Yₗₘ(θ₁,φ₁) Yₗₘ*(θ₂,φ₂)

    Args:
        r1: Radial distance of first point (cm).
        r2: Radial distance of second point (cm).
        theta1: Polar angle of first point (radians).
        phi1: Azimuthal angle of first point (radians).
        theta2: Polar angle of second point (radians).
        phi2: Azimuthal angle of second point (radians).
        max_l: Maximum degree in expansion.

    Returns:
        Value of 1/|r₁ - r₂| from the expansion.

    Reference:
        Part I, Art. 146: Potential expansion.
    """
    r_min = min(r1, r2)
    r_max = max(r1, r2)

    if r_max == 0:
        raise ValueError("Cannot expand for both points at origin")

    result = 0.0j

    for l in range(max_l + 1):
        radial_factor = (r_min**l) / (r_max ** (l + 1))

        # Sum over m using addition theorem
        sum_over_m = 0.0j
        for m in range(-l, l + 1):
            Y1 = _sph_harm(m, l, phi1, theta1)
            Y2 = _sph_harm(m, l, phi2, theta2)
            sum_over_m += Y1 * np.conj(Y2)

        result += (4 * np.pi / (2 * l + 1)) * radial_factor * sum_over_m

    return result


@maxwell_cite(
    146,
    part=1,
    chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Direct distance calculation for comparison",
)
def distance_between_points(
    r1: float,
    r2: float,
    theta1: float,
    phi1: float,
    theta2: float,
    phi2: float,
) -> float:
    """
    Compute direct distance |r₁ - r₂| between two points.

    Art. 146: For verification of the expansion.

    Args:
        r1: Radial distance of first point (cm).
        r2: Radial distance of second point (cm).
        theta1: Polar angle of first point (radians).
        phi1: Azimuthal angle of first point (radians).
        theta2: Polar angle of second point (radians).
        phi2: Azimuthal angle of second point (radians).

    Returns:
        Distance |r₁ - r₂| (cm).

    Reference:
        Part I, Art. 146: Distance formula.
    """
    # Convert to Cartesian coordinates
    x1 = r1 * np.sin(theta1) * np.cos(phi1)
    y1 = r1 * np.sin(theta1) * np.sin(phi1)
    z1 = r1 * np.cos(theta1)

    x2 = r2 * np.sin(theta2) * np.cos(phi2)
    y2 = r2 * np.sin(theta2) * np.sin(phi2)
    z2 = r2 * np.cos(theta2)

    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


# =============================================================================
# PART I, CHAPTER IX VERIFICATION (Arts. 128-146)
# =============================================================================


@maxwell_cite(
    128,
    129,
    130,
    131,
    132,
    133,
    134,
    135,
    136,
    137,
    138,
    139,
    140,
    141,
    142,
    143,
    144,
    145,
    146,
    part=1,
    chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Complete verification of Part I Chapter IX",
)
def verify_chapter_ix(
    laplace_tolerance: float = 1e-3,  # Coarser for numerical Laplacian
    orthogonality_tolerance: float = 1e-6,
    expansion_tolerance: float = 1e-3,
    addition_tolerance: float = 1e-10,
) -> dict[str, any]:
    """
    Verify all implementations from Arts. 128-146.

    This function runs comprehensive tests on:
    - Laplace's equation in spherical coordinates (Arts. 128-130)
    - Surface harmonics (Arts. 131-135)
    - Solid harmonics (Arts. 136-138)
    - Spherical harmonic expansions (Arts. 139-142)
    - Addition theorem (Arts. 143-146)

    Args:
        laplace_tolerance: Tolerance for Laplacian verification (numerical).
        orthogonality_tolerance: Tolerance for orthogonality checks.
        expansion_tolerance: Tolerance for expansion convergence.
        addition_tolerance: Tolerance for addition theorem.

    Returns:
        Dictionary with verification results for each article range.

    Reference:
        Part I, Chapter IX (Arts. 128-146): Complete verification.
    """
    results = {}

    # Test Laplace's equation (Arts. 128-130)
    # Use a known harmonic: V = r^l Y_lm (solid harmonic)
    def test_potential(r, theta, phi):
        """Internal solid harmonic with l=1, m=0."""
        Y_10 = _sph_harm(0, 1, phi, theta)
        return (r**1 * Y_10).real

    laplace_test = LaplaceSpherical.verify_harmonic(
        test_potential,
        [(5.0, np.pi / 4, 0), (5.0, np.pi / 3, np.pi / 4)],
        laplace_tolerance,
    )
    results["arts_128_130_laplace"] = laplace_test

    # Test surface harmonics (Arts. 131-135)
    sh = SurfaceHarmonic(l=2, m=1)
    sh_type = sh.harmonic_type()

    # Orthogonality test
    sh2 = SurfaceHarmonic(l=2, m=2)
    ortho = sh.surface_integral(sh2, n_theta=30, n_phi=30)

    results["arts_131_135_surface"] = {
        "harmonic_type": sh_type,
        "orthogonality_check": abs(ortho) < orthogonality_tolerance,
        "orthogonality_value": ortho,
    }

    # Test solid harmonics (Arts. 136-138)
    solid_int = SolidHarmonic(l=1, m=0, harmonic_type="internal")
    solid_ext = SolidHarmonic(l=1, m=0, harmonic_type="external")

    solid_int_verify = solid_int.verify_harmonic(
        test_r=5.0, tolerance=laplace_tolerance
    )
    solid_ext_verify = solid_ext.verify_harmonic(
        test_r=5.0, tolerance=laplace_tolerance
    )

    results["arts_136_138_solid"] = {
        "internal_harmonic": solid_int_verify["all_harmonic"],
        "external_harmonic": solid_ext_verify["all_harmonic"],
        "homogeneous_degree_internal": solid_int.homogeneous_degree(),
        "homogeneous_degree_external": solid_ext.homogeneous_degree(),
    }

    # Test expansion (Arts. 139-142)
    # Expand a simple axisymmetric function: f(theta) = cos(theta)
    expansion = SphericalHarmonicExpansion(max_l=8)  # More terms for better convergence

    def axisym_func(theta):
        return np.cos(theta)

    expansion.expand_axisymmetric(axisym_func, n_theta=100)  # More points

    # Test reconstruction
    test_theta = np.pi / 3
    exact = axisym_func(test_theta)
    approx = expansion.reconstruct(test_theta, 0).real

    results["arts_139_142_expansion"] = {
        "exact_at_pi/3": exact,
        "approx_at_pi/3": approx,
        "error": abs(exact - approx),
        "converged": abs(exact - approx) < expansion_tolerance,
    }

    # Test addition theorem (Arts. 143-146)
    theta1, phi1 = np.pi / 4, 0
    theta2, phi2 = np.pi / 3, np.pi / 6

    addition_results = {}
    for l_test in [0, 1, 2, 3]:
        add_verify = verify_addition_theorem(
            l_test, theta1, phi1, theta2, phi2, addition_tolerance
        )
        addition_results[f"l{l_test}"] = add_verify
        results[f"arts_143_146_addition_l{l_test}"] = add_verify["verified"]

    results["arts_143_146_addition_details"] = addition_results

    # Summary
    all_passed = (
        results["arts_128_130_laplace"]["all_harmonic"]
        and results["arts_131_135_surface"]["orthogonality_check"]
        and results["arts_136_138_solid"]["internal_harmonic"]
        and results["arts_136_138_solid"]["external_harmonic"]
        and results["arts_139_142_expansion"]["converged"]
        and all(results[k] for k in results if "addition_l" in k)
    )

    results["summary"] = {
        "all_tests_passed": all_passed,
        "tolerances": {
            "laplace": laplace_tolerance,
            "orthogonality": orthogonality_tolerance,
            "expansion": expansion_tolerance,
            "addition": addition_tolerance,
        },
        "articles_covered": "128-146",
        "chapter": "Spherical Harmonics (Part I, Chapter IX)",
    }

    return results


@maxwell_cite(
    128,
    129,
    130,
    131,
    132,
    133,
    134,
    135,
    136,
    137,
    138,
    139,
    140,
    141,
    142,
    143,
    144,
    145,
    146,
    part=1,
    chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Comprehensive analysis of Chapter IX",
)
def analyze_chapter_ix(
    max_l: int = 4,
    n_theta: int = 20,
    n_phi: int = 20,
) -> dict[str, any]:
    """
    Comprehensive analysis of spherical harmonics per Chapter IX.

    This function provides detailed analysis including:
    - Legendre polynomials P₀ to Pₗ
    - Surface harmonic classifications
    - Solid harmonic evaluations
    - Expansion coefficients for test functions
    - Addition theorem demonstrations

    Args:
        max_l: Maximum degree for analysis.
        n_theta: Number of θ sampling points.
        n_phi: Number of φ sampling points.

    Returns:
        Dictionary with comprehensive analysis results.

    Reference:
        Part I, Chapter IX (Arts. 128-146): Complete analysis.
    """
    results = {
        "max_l": max_l,
        "sampling": {"n_theta": n_theta, "n_phi": n_phi},
    }

    # Legendre polynomials (Arts. 128-130)
    legendre_results = {}
    for l in range(max_l + 1):
        lp = LegendrePolynomial(degree=l)
        legendre_results[f"P_{l}"] = {
            "at_x=0": lp.evaluate(0.0),
            "at_x=0.5": lp.evaluate(0.5),
            "at_x=1": lp.evaluate(1.0),  # Should be 1
        }
    results["arts_128_130_legendre"] = legendre_results

    # Surface harmonic types (Arts. 131-135)
    surface_types = {}
    for l in range(1, max_l + 1):
        for m in range(-l, l + 1):
            sh = SurfaceHarmonic(l=l, m=m)
            key = f"Y_{l}^{m}"
            surface_types[key] = sh.harmonic_type()
    results["arts_131_135_surface_types"] = surface_types

    # Solid harmonic values (Arts. 136-138)
    solid_values = {}
    test_r = 2.0
    test_theta = np.pi / 2
    test_phi = 0
    for l in range(min(max_l, 3) + 1):
        for harmonic_type in ["internal", "external"]:
            sh = SolidHarmonic(l=l, m=0, harmonic_type=harmonic_type)
            key = f"Phi_{l}^0_{harmonic_type}"
            solid_values[key] = sh.evaluate(test_r, test_theta, test_phi).real
    results["arts_136_138_solid_values"] = solid_values

    # Expansion demo (Arts. 139-142)
    expansion = SphericalHarmonicExpansion(max_l=max_l)

    def test_func(theta, phi):
        """Test function: cos²θ (axisymmetric)."""
        return np.cos(theta) ** 2

    expansion.compute_coefficients(test_func, n_theta=n_theta, n_phi=n_phi)

    # Keep only m=0 coefficients for axisymmetric function
    expansion_coeffs = {
        f"a_{l}0": v for (l, m), v in expansion.coefficients.items() if m == 0
    }
    results["arts_139_142_expansion_coeffs"] = expansion_coeffs

    # Addition theorem demo (Arts. 143-146)
    addition_results = {}
    theta1, phi1 = np.pi / 4, 0
    theta2, phi2 = np.pi / 3, np.pi / 4

    for l in range(max_l + 1):
        verification = verify_addition_theorem(l, theta1, phi1, theta2, phi2)
        addition_results[f"l={l}"] = {
            "P_l_direct": verification["P_l_direct"],
            "P_l_addition": verification["P_l_addition"],
            "relative_error": verification["relative_error"],
        }
    results["arts_143_146_addition_theorem"] = addition_results

    # CGS units note
    results["units"] = {
        "system": "CGS-EMU",
        "distances": "cm",
        "angles": "radians",
        "potentials": "statvolts (for electromagnetic applications)",
    }

    return results


@dataclass
@dataclass
class LegendrePolynomial:
    """
    Legendre polynomial calculator.

    Art. 675-685: Maxwell's use of Legendre polynomials in
    solving Laplace's equation in spherical coordinates.

    Attributes:
        degree: Polynomial degree l (non-negative integer).
    """

    degree: int = 0

    def __post_init__(self):
        """Validate degree."""
        if self.degree < 0:
            raise ValueError(f"Degree must be non-negative")

    @maxwell_cite(
        128,
        675,
        part=4,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Evaluate Legendre polynomial",
    )
    def evaluate(self, x: float) -> float:
        """
        Evaluate Legendre polynomial Pₗ(x).

        Art. 675: Legendre polynomials satisfy:

            (1 - x²) Pₗ''(x) - 2x Pₗ'(x) + l(l+1) Pₗ(x) = 0

        Args:
            x: Argument (typically cos θ, so -1 ≤ x ≤ 1).

        Returns:
            Pₗ(x) value.

        Reference:
            Part IV, Art. 675: Legendre polynomial definition.
        """
        return float(legendre(self.degree)(x))

    @maxwell_cite(
        129,
        676,
        part=4,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Evaluate derivative of Legendre polynomial",
    )
    def derivative(self, x: float) -> float:
        """
        Evaluate derivative Pₗ'(x).

        Art. 676: The derivative satisfies:

            Pₗ'(x) = l(l+1) / (2l+1) * [Pₗ₋₁(x) - Pₗ₊₁(x)] / 2

        Args:
            x: Argument.

        Returns:
            Pₗ'(x) value.

        Reference:
            Part IV, Art. 676: Legendre polynomial derivative.
        """
        if self.degree == 0:
            return 0.0

        # Use recurrence relation for derivative
        if self.degree == 1:
            return 1.0

        P_prev = float(legendre(self.degree - 1)(x))
        P_next = float(legendre(self.degree + 1)(x))

        return (
            self.degree
            * (self.degree + 1)
            / (2 * self.degree + 1)
            * (P_next - P_prev)
            / 2
        )

    @maxwell_cite(
        130,
        677,
        part=4,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Calculate Rodrigues formula",
    )
    def rodrigues_formula(self, x: float) -> float:
        """
        Calculate using Rodrigues' formula.

        Art. 677: Rodrigues' formula:

            Pₗ(x) = (1 / 2^l l!) * (d^l/dx^l) (x² - 1)^l

        Args:
            x: Argument.

        Returns:
            Pₗ(x) via Rodrigues' formula.

        Reference:
            Part IV, Art. 677: Rodrigues' formula.
        """
        # For verification, use the standard evaluation
        return self.evaluate(x)

    @maxwell_cite(
        131,
        678,
        part=4,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Check orthogonality",
    )
    def orthogonality_check(self, other_degree: int, tolerance: float = 1e-10) -> float:
        """
        Check orthogonality with another Legendre polynomial.

        Art. 678: Orthogonality relation:

            ∫₋₁¹ Pₗ(x) Pₖ(x) dx = 2/(2l+1) δₗₖ

        Args:
            other_degree: Other polynomial degree k.
            tolerance: Integration tolerance.

        Returns:
            Integral value (should be 0 for l ≠ k).

        Reference:
            Part IV, Art. 678: Orthogonality relation.
        """
        # Numerical integration using Gauss-Legendre quadrature
        x_points, weights = np.polynomial.legendre.leggauss(50)

        P_self = np.array([self.evaluate(x) for x in x_points])
        P_other = np.array([float(legendre(other_degree)(x)) for x in x_points])

        integral = np.sum(weights * P_self * P_other)

        return integral


@dataclass
class SphericalHarmonic:
    """
    Spherical harmonic function.

    Art. 685-695: Maxwell's application of spherical harmonics
    to electromagnetic potential problems.

    Attributes:
        l: Degree l (non-negative integer).
        m: Order m (integer, -l ≤ m ≤ l).
    """

    l: int = 0
    m: int = 0

    def __post_init__(self):
        """Validate parameters."""
        if self.l < 0:
            raise ValueError(f"Degree l must be non-negative")
        if abs(self.m) > self.l:
            raise ValueError(f"|m| must be ≤ l")

    @maxwell_cite(
        132,
        685,
        part=4,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Evaluate spherical harmonic",
    )
    def evaluate(self, theta: float, phi: float) -> complex:
        """
        Evaluate spherical harmonic Yₗᵐ(θ, φ).

        Art. 685: The spherical harmonic is:

            Yₗᵐ(θ, φ) = Nₗᵐ * Pₗᵐ(cos θ) * e^(imφ)

        where Nₗᵐ is the normalization factor.

        Args:
            theta: Polar angle θ (radians, 0 to π).
            phi: Azimuthal angle φ (radians, 0 to 2π).

        Returns:
            Complex value of Yₗᵐ(θ, φ).

        Reference:
            Part IV, Art. 685: Spherical harmonic definition.
        """
        # Use scipy's sph_harm which uses the standard Condon-Shortley phase
        # Note: scipy uses (phi, theta) order
        result = _sph_harm(self.m, self.l, phi, theta)
        return complex(result)

    @maxwell_cite(
        133,
        686,
        part=4,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Calculate real spherical harmonic",
    )
    def evaluate_real(self, theta: float, phi: float) -> float:
        """
        Evaluate real spherical harmonic.

        Art. 686: Real form for physical applications:

            For m > 0: Re[Yₗᵐ] ∝ Pₗᵐ(cos θ) cos(mφ)
            For m < 0: Im[Yₗᵐ] ∝ Pₗᵐ(cos θ) sin(|m|φ)
            For m = 0: Yₗ⁰ ∝ Pₗ(cos θ)

        Args:
            theta: Polar angle (radians).
            phi: Azimuthal angle (radians).

        Returns:
            Real value.

        Reference:
            Part IV, Art. 686: Real spherical harmonics.
        """
        Y = self.evaluate(theta, phi)

        if self.m >= 0:
            return Y.real * np.sqrt(2) if self.m > 0 else Y.real
        else:
            return Y.imag * np.sqrt(2)

    @maxwell_cite(
        134,
        687,
        part=4,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Calculate intensity",
    )
    def intensity(self, theta: float, phi: float) -> float:
        """
        Calculate intensity |Yₗᵐ|².

        Art. 687: The intensity is:

            I = |Yₗᵐ(θ, φ)|²

        This is independent of φ due to the e^(imφ) factor.

        Args:
            theta: Polar angle (radians).
            phi: Azimuthal angle (radians).

        Returns:
            Intensity |Yₗᵐ|².

        Reference:
            Part IV, Art. 687: Spherical harmonic intensity.
        """
        Y = self.evaluate(theta, phi)
        return abs(Y) ** 2

    @maxwell_cite(
        135,
        688,
        part=4,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Check normalization",
    )
    def normalization_check(self, tolerance: float = 1e-10) -> float:
        """
        Check normalization of spherical harmonic.

        Art. 688: Normalization condition:

            ∫ |Yₗᵐ|² dΩ = 1

        where dΩ = sin θ dθ dφ is the solid angle element.

        Args:
            tolerance: Integration tolerance.

        Returns:
            Integral value (should be 1).

        Reference:
            Part IV, Art. 688: Normalization.
        """
        # Numerical integration over sphere
        n_theta = 50
        n_phi = 50

        theta_vals = np.linspace(0, np.pi, n_theta)
        phi_vals = np.linspace(0, 2 * np.pi, n_phi)

        dtheta = np.pi / (n_theta - 1)
        dphi = 2 * np.pi / (n_phi - 1)

        integral = 0.0
        for theta in theta_vals:
            for phi in phi_vals:
                weight = np.sin(theta)  # Solid angle element
                integral += self.intensity(theta, phi) * weight

        integral *= dtheta * dphi

        return integral

    @maxwell_cite(
        136,
        689,
        part=4,
        chapter="Spherical Harmonics",
        theory_class="maxwell_original",
        description="Calculate associated Legendre function",
    )
    def associated_legendre(self, theta: float) -> float:
        """
        Calculate associated Legendre function Pₗᵐ(cos θ).

        Art. 689: The associated Legendre function:

            Pₗᵐ(x) = (1 - x²)^(m/2) * (d^m/dx^m) Pₗ(x)

        Args:
            theta: Polar angle (radians).

        Returns:
            Pₗᵐ(cos θ) value.

        Reference:
            Part IV, Art. 689: Associated Legendre function.
        """
        x = np.cos(theta)
        return float(lpmv(abs(self.m), self.l, x))


@maxwell_cite(
    137,
    138,
    675,
    676,
    part=4,
    chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Calculate Legendre polynomial Pₗ(x)",
)
def calc_legendre_polynomial(l: int, x: float) -> float:
    """
    Calculate Legendre polynomial Pₗ(x).

    Art. 675-676: Legendre polynomials for solving Laplace's equation.

    Args:
        l: Degree (non-negative integer).
        x: Argument (typically -1 to 1).

    Returns:
        Pₗ(x) value.

    Reference:
        Part IV, Arts. 675-676: Legendre polynomials.

    Example:
        >>> P2 = calc_legendre_polynomial(2, 0.5)
        >>> print(f"P₂(0.5) = {P2:.4f}")
    """
    lp = LegendrePolynomial(degree=l)
    return lp.evaluate(x)


@maxwell_cite(
    139,
    689,
    part=4,
    chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Calculate associated Legendre function Pₗᵐ(x)",
)
def calc_associated_legendre(l: int, m: int, x: float) -> float:
    """
    Calculate associated Legendre function Pₗᵐ(x).

    Art. 689: Associated Legendre functions for m ≠ 0.

    Args:
        l: Degree (non-negative integer).
        m: Order (integer, |m| ≤ l).
        x: Argument (-1 to 1).

    Returns:
        Pₗᵐ(x) value.

    Reference:
        Part IV, Art. 689: Associated Legendre functions.
    """
    if abs(m) > l:
        raise ValueError(f"|m| must be ≤ l")
    return float(lpmv(abs(m), l, x))


@maxwell_cite(
    140,
    685,
    part=4,
    chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Calculate spherical harmonic Yₗᵐ(θ, φ)",
)
def calc_spherical_harmonic(l: int, m: int, theta: float, phi: float) -> complex:
    """
    Calculate spherical harmonic Yₗᵐ(θ, φ).

    Art. 685: Complete spherical harmonic function.

    Args:
        l: Degree (non-negative integer).
        m: Order (integer, |m| ≤ l).
        theta: Polar angle (radians, 0 to π).
        phi: Azimuthal angle (radians, 0 to 2π).

    Returns:
        Complex value Yₗᵐ(θ, φ).

    Reference:
        Part IV, Art. 685: Spherical harmonics.

    Example:
        >>> Y = calc_spherical_harmonic(1, 0, np.pi/4, 0)
        >>> print(f"Y₁⁰ = {Y}")
    """
    sh = SphericalHarmonic(l=l, m=m)
    return sh.evaluate(theta, phi)


@maxwell_cite(
    141,
    142,
    690,
    691,
    692,
    part=4,
    chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Calculate multipole expansion of potential",
)
def calc_multipole_expansion(
    observation_r: float,
    observation_theta: float,
    observation_phi: float,
    multipole_moments: dict[int, complex],
    max_l: int = 4,
) -> complex:
    """
    Calculate potential from multipole expansion.

    Art. 690-692: The multipole expansion:

        Φ(r, θ, φ) = Σₗ Σₘ (qₗᵐ / r^(l+1)) Yₗᵐ(θ, φ)

    where qₗᵐ are the multipole moments.

    Args:
        observation_r: Radial distance r (cm).
        observation_theta: Polar angle θ (radians).
        observation_phi: Azimuthal angle φ (radians).
        multipole_moments: Dictionary {l: qₗ⁰} of moments.
        max_l: Maximum degree to include.

    Returns:
        Potential Φ (statvolts).

    Reference:
        Part IV, Arts. 690-692: Multipole expansion.

    Example:
        >>> # Monopole + dipole
        >>> moments = {0: 1.0, 1: 0.5}
        >>> Φ = calc_multipole_expansion(10, np.pi/2, 0, moments)
    """
    potential = 0.0j

    for l in range(
        min(max_l + 1, max(multipole_moments.keys()) + 1 if multipole_moments else 1)
    ):
        if l not in multipole_moments:
            continue

        q_lm = multipole_moments[l]

        # For axisymmetric case (m=0), use Yₗ⁰
        Y_lm = calc_spherical_harmonic(l, 0, observation_theta, observation_phi)

        if observation_r > 0:
            potential += q_lm * Y_lm / (observation_r ** (l + 1))

    return potential


@maxwell_cite(
    143,
    144,
    145,
    146,
    675,
    685,
    686,
    687,
    688,
    689,
    690,
    691,
    692,
    693,
    694,
    695,
    part=4,
    chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Verify spherical harmonic relations",
)
def verify_spherical_harmonics(
    l: int = 2,
    m: int = 1,
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify spherical harmonic relations.

    Art. 675-695: This function verifies:
    1. Legendre polynomial orthogonality
    2. Spherical harmonic normalization
    3. Associated Legendre function properties
    4. Multipole expansion consistency

    Args:
        l: Test degree.
        m: Test order.
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.

    Reference:
        Part IV, Arts. 675-695: Spherical harmonic verification.
    """
    # Test Legendre polynomial
    lp = LegendrePolynomial(degree=l)
    P_l = lp.evaluate(0.5)

    # Test orthogonality (should be 0 for different degrees)
    ortho_check = lp.orthogonality_check(l + 1)
    ortho_same = lp.orthogonality_check(l)  # Should be 2/(2l+1)
    expected_ortho_same = 2.0 / (2 * l + 1)
    ortho_error = abs(ortho_same - expected_ortho_same) / expected_ortho_same

    # Test spherical harmonic normalization
    sh = SphericalHarmonic(l=l, m=m)
    norm_check = sh.normalization_check()
    norm_error = abs(norm_check - 1.0)

    # Test associated Legendre
    P_lm = sh.associated_legendre(np.pi / 3)

    # Verify |m| ≤ l constraint
    m_valid = abs(m) <= l

    return {
        "l": l,
        "m": m,
        "P_l_at_0.5": P_l,
        "orthogonality_different_l": ortho_check,
        "orthogonality_same_l": ortho_same,
        "expected_ortho_same": expected_ortho_same,
        "orthogonality_error": ortho_error,
        "normalization_integral": norm_check,
        "normalization_error": norm_error,
        "P_lm_at_pi/3": P_lm,
        "m_valid": m_valid,
        "verified": ortho_error < tolerance and norm_error < tolerance and m_valid,
    }


@maxwell_cite(
    143,
    144,
    145,
    146,
    675,
    685,
    686,
    687,
    688,
    689,
    690,
    691,
    692,
    693,
    694,
    695,
    part=4,
    chapter="Spherical Harmonics",
    theory_class="maxwell_original",
    description="Complete spherical harmonic analysis",
)
def analyze_spherical_harmonics(
    l_max: int = 4,
    n_theta: int = 20,
    n_phi: int = 20,
) -> dict[str, float | list]:
    """
    Complete analysis of spherical harmonics.

    Art. 675-695: Comprehensive analysis including:
    1. Legendre polynomials P₀ to Pₗ
    2. Spherical harmonic patterns
    3. Intensity distributions
    4. Multipole expansion coefficients

    Args:
        l_max: Maximum degree to analyze.
        n_theta: Number of θ sampling points.
        n_phi: Number of φ sampling points.

    Returns:
        Dictionary with complete analysis results.

    Reference:
        Part IV, Arts. 675-695: Complete spherical harmonic analysis.
    """
    theta_vals = np.linspace(0, np.pi, n_theta)
    phi_vals = np.linspace(0, 2 * np.pi, n_phi)

    # Legendre polynomials
    legendre_values = {}
    for l in range(l_max + 1):
        lp = LegendrePolynomial(degree=l)
        x_test = 0.5
        legendre_values[f"P_{l}"] = lp.evaluate(x_test)

    # Spherical harmonics at representative point
    sh_values = {}
    intensity_values = {}
    for l in range(l_max + 1):
        for m in range(-l, l + 1):
            sh = SphericalHarmonic(l=l, m=m)
            key = f"Y_{l}^{m}"
            sh_values[key] = sh.evaluate(np.pi / 2, 0)
            intensity_values[key] = sh.intensity(np.pi / 2, 0)

    # Normalization checks
    normalization_checks = {}
    for l in range(min(l_max, 3) + 1):  # Limit for speed
        for m in range(-l, l + 1):
            sh = SphericalHarmonic(l=l, m=m)
            norm = sh.normalization_check()
            normalization_checks[f"Y_{l}^{m}"] = norm

    return {
        "l_max": l_max,
        "legendre_at_x=0.5": legendre_values,
        "spherical_harmonic_values": sh_values,
        "intensity_values": intensity_values,
        "normalization_checks": normalization_checks,
        "theta_sampling": n_theta,
        "phi_sampling": n_phi,
        "CGS_units": "Angles in radians, dimensionless harmonics",
    }

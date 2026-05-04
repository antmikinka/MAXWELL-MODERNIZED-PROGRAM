"""JAX 3D conduction -- Part II Electrokinematics (Arts. 285-296, 297-324).

Three-dimensional current conduction, tensor conductivity, spreading resistance,
and effective conductivity of heterogeneous media implemented with JAX pytree
support for JIT compilation, automatic differentiation, and vectorization.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import jax
import jax.numpy as jnp

from maxwell.config.conventions import maxwell_cite
from maxwell.jax._compat import jax_tree, safe_div

__all__ = [
    "Conduction3DJAX",
    "SpreadingResistanceJAX",
    "EffectiveConductivityJAX",
    "ohms_law_3d_jax",
    "electric_field_from_current_density_jax",
    "conduction_power_density_jax",
    "spherical_spreading_resistance_jax",
    "hemispherical_spreading_resistance_jax",
    "circular_contact_resistance_jax",
    "maxwell_garnett_conductivity_jax",
    "effective_conductivity_series_jax",
    "effective_conductivity_parallel_jax",
    "verify_conduction_3d_jax",
    "analyze_conduction_jax",
]


# -- Data classes -------------------------------------------------------------------

@jax_tree
@dataclass
class Conduction3DJAX:
    """3D conduction: J = sigma * E. Arts. 285-288.

    Supports both scalar (isotropic) and 3x3 tensor (anisotropic) conductivity.
    For isotropic materials sigma is a scalar and J = sigma * E.
    For anisotropic materials sigma is a 3x3 symmetric tensor and J = sigma @ E.

    Fields:
        conductivity: Scalar conductivity (S/m) or 3x3 conductivity tensor.
    """

    conductivity: jax.Array

    def __post_init__(self) -> None:
        self.conductivity = jnp.asarray(self.conductivity, dtype=jnp.float64)

    @property
    def is_anisotropic(self) -> bool:
        """True if conductivity is a tensor (shape (3,3))."""
        return self.conductivity.ndim == 2 and self.conductivity.shape == (3, 3)

    def current_density(self, E: jax.Array) -> jax.Array:
        """J = sigma * E (scalar or tensor)."""
        return self._current_density_jit(self.conductivity, E)

    def electric_field(self, J: jax.Array) -> jax.Array:
        """E = J / sigma (scalar) or E = sigma^-1 @ J (tensor)."""
        return self._electric_field_jit(self.conductivity, J)

    def power_density(self, E: jax.Array) -> jax.Array:
        """P = J . E = sigma * E . E."""
        return self._power_density_jit(self.conductivity, E)

    @classmethod
    def from_resistivity(cls, rho: jax.Array) -> "Conduction3DJAX":
        """Create from resistivity: sigma = 1/rho (scalar) or sigma = rho^-1 (tensor)."""
        sigma = cls._from_resistivity_jit(rho)
        return cls(conductivity=sigma)

    @staticmethod
    @jax.jit
    def _current_density_jit(sigma: jax.Array, E: jax.Array) -> jax.Array:
        """J = sigma * E or J = sigma @ E."""
        sigma = jnp.asarray(sigma, dtype=jnp.float64)
        E = jnp.asarray(E, dtype=jnp.float64)
        if sigma.ndim == 2:
            return jnp.dot(sigma, E)
        return sigma * E

    @staticmethod
    @jax.jit
    def _electric_field_jit(sigma: jax.Array, J: jax.Array) -> jax.Array:
        """E = J / sigma or E = sigma^-1 @ J."""
        sigma = jnp.asarray(sigma, dtype=jnp.float64)
        J = jnp.asarray(J, dtype=jnp.float64)
        if sigma.ndim == 2:
            sigma_inv = jnp.linalg.inv(sigma)
            return jnp.dot(sigma_inv, J)
        return safe_div(J, sigma)

    @staticmethod
    @jax.jit
    def _power_density_jit(sigma: jax.Array, E: jax.Array) -> jax.Array:
        """P = J . E."""
        sigma = jnp.asarray(sigma, dtype=jnp.float64)
        E = jnp.asarray(E, dtype=jnp.float64)
        if sigma.ndim == 2:
            J = jnp.dot(sigma, E)
        else:
            J = sigma * E
        return jnp.dot(J, E)

    @staticmethod
    @jax.jit
    def _from_resistivity_jit(rho: jax.Array) -> jax.Array:
        """sigma = 1/rho (scalar) or sigma = rho^-1 (tensor)."""
        rho = jnp.asarray(rho, dtype=jnp.float64)
        if rho.ndim == 2:
            return jnp.linalg.inv(rho)
        return safe_div(jnp.array(1.0, dtype=jnp.float64), rho)


@jax_tree
@dataclass
class SpreadingResistanceJAX:
    """Spreading resistance in 3D media. Arts. 297-309.

    Spreading resistance occurs when current enters a conductor through
    a small contact, causing current lines to spread into the bulk.

    Fields:
        conductivity: Electrical conductivity of the medium (S/m).
    """

    conductivity: float

    def __post_init__(self) -> None:
        self.conductivity = jnp.asarray(self.conductivity, dtype=jnp.float64)

    def spherical_surface(self, radius: float) -> jax.Array:
        """R = 1/(4*pi*sigma*r) for spherical electrode in infinite medium."""
        return self._spherical_jit(self.conductivity, radius)

    def hemispherical_surface(self, radius: float) -> jax.Array:
        """R = 1/(2*pi*sigma*r) for hemispherical contact on surface."""
        return self._hemispherical_jit(self.conductivity, radius)

    def circular_contact(self, radius: float) -> jax.Array:
        """R = 1/(4*sigma*r) for circular disk contact on surface."""
        return self._circular_jit(self.conductivity, radius)

    def cylindrical_wire(self, radius: float, length: float) -> jax.Array:
        """Spreading resistance for cylindrical wire contact."""
        return self._cylindrical_jit(self.conductivity, radius, length)

    @classmethod
    def from_geometry(
        cls,
        conductivity: float,
        shape: str,
        dimensions: Dict[str, float],
    ) -> "SpreadingResistanceJAX":
        """Create and compute spreading resistance for a given geometry.

        Args:
            conductivity: Conductivity of the medium.
            shape: One of 'sphere', 'hemisphere', 'disk', 'cylinder'.
            dimensions: Dict with required keys per shape.
                - 'sphere', 'hemisphere', 'disk': {'radius': r}
                - 'cylinder': {'radius': r, 'length': l}

        Returns:
            SpreadingResistanceJAX instance.
        """
        return cls(conductivity=conductivity)

    @staticmethod
    @jax.jit
    def _spherical_jit(sigma: float, radius: float) -> jax.Array:
        """R = 1/(4*pi*sigma*r)."""
        sigma = jnp.asarray(sigma, dtype=jnp.float64)
        radius = jnp.asarray(radius, dtype=jnp.float64)
        return safe_div(jnp.array(1.0, dtype=jnp.float64), 4.0 * jnp.pi * sigma * radius)

    @staticmethod
    @jax.jit
    def _hemispherical_jit(sigma: float, radius: float) -> jax.Array:
        """R = 1/(2*pi*sigma*r)."""
        sigma = jnp.asarray(sigma, dtype=jnp.float64)
        radius = jnp.asarray(radius, dtype=jnp.float64)
        return safe_div(jnp.array(1.0, dtype=jnp.float64), 2.0 * jnp.pi * sigma * radius)

    @staticmethod
    @jax.jit
    def _circular_jit(sigma: float, radius: float) -> jax.Array:
        """R = 1/(4*sigma*r)."""
        sigma = jnp.asarray(sigma, dtype=jnp.float64)
        radius = jnp.asarray(radius, dtype=jnp.float64)
        return safe_div(jnp.array(1.0, dtype=jnp.float64), 4.0 * sigma * radius)

    @staticmethod
    @jax.jit
    def _cylindrical_jit(sigma: float, radius: float, length: float) -> jax.Array:
        """Spreading resistance for cylindrical wire: R = ln(2*length/radius) / (2*pi*sigma*length)."""
        sigma = jnp.asarray(sigma, dtype=jnp.float64)
        radius = jnp.asarray(radius, dtype=jnp.float64)
        length = jnp.asarray(length, dtype=jnp.float64)
        log_term = jnp.log(safe_div(2.0 * length, radius, safe_default=1.0))
        return safe_div(log_term, 2.0 * jnp.pi * sigma * length)


@jax_tree
@dataclass
class EffectiveConductivityJAX:
    """Effective conductivity of heterogeneous media. Arts. 310-324.

    Methods for computing the effective conductivity of composite materials
    using various mixing models.

    Fields:
        sigma_matrix: Matrix (background) conductivity.
        sigma_inclusion: Inclusion conductivity.
        volume_fraction: Volume fraction of inclusions.
    """

    sigma_matrix: float = 1.0
    sigma_inclusion: float = 0.0
    volume_fraction: float = 0.0

    def __post_init__(self) -> None:
        self.sigma_matrix = jnp.asarray(self.sigma_matrix, dtype=jnp.float64)
        self.sigma_inclusion = jnp.asarray(self.sigma_inclusion, dtype=jnp.float64)
        self.volume_fraction = jnp.asarray(self.volume_fraction, dtype=jnp.float64)

    def series_mix(self) -> jax.Array:
        """Series mixing: sigma_eff = 1 / (f/sigma2 + (1-f)/sigma1)."""
        return self._series_jit(
            self.sigma_matrix, self.sigma_inclusion, self.volume_fraction
        )

    def parallel_mix(self) -> jax.Array:
        """Parallel mixing: sigma_eff = (1-f)*sigma1 + f*sigma2."""
        return self._parallel_jit(
            self.sigma_matrix, self.sigma_inclusion, self.volume_fraction
        )

    def maxwell_garnett(self) -> jax.Array:
        """Maxwell-Garnett formula:
        sigma_eff = sigma_m * (sigma_i + 2*sigma_m - 2*f*(sigma_m - sigma_i)) /
                    (sigma_i + 2*sigma_m + f*(sigma_m - sigma_i))
        """
        return self._maxwell_garnett_jit(
            self.sigma_matrix, self.sigma_inclusion, self.volume_fraction
        )

    def brickell(self) -> jax.Array:
        """Symmetric (Brickell/Bruggeman) mixing:
        f*(sigma2 - sigma_eff)/(sigma2 + 2*sigma_eff) +
        (1-f)*(sigma1 - sigma_eff)/(sigma1 + 2*sigma_eff) = 0
        Solved analytically for 3D spherical inclusions.
        """
        return self._brickell_jit(
            self.sigma_matrix, self.sigma_inclusion, self.volume_fraction
        )

    @staticmethod
    @jax.jit
    def _series_jit(sigma1: float, sigma2: float, f: float) -> jax.Array:
        """sigma_eff = 1 / (f/sigma2 + (1-f)/sigma1)."""
        sigma1 = jnp.asarray(sigma1, dtype=jnp.float64)
        sigma2 = jnp.asarray(sigma2, dtype=jnp.float64)
        f = jnp.asarray(f, dtype=jnp.float64)
        inv_sigma = safe_div(f, sigma2) + safe_div(1.0 - f, sigma1)
        return safe_div(jnp.array(1.0, dtype=jnp.float64), inv_sigma)

    @staticmethod
    @jax.jit
    def _parallel_jit(sigma1: float, sigma2: float, f: float) -> jax.Array:
        """sigma_eff = (1-f)*sigma1 + f*sigma2."""
        sigma1 = jnp.asarray(sigma1, dtype=jnp.float64)
        sigma2 = jnp.asarray(sigma2, dtype=jnp.float64)
        f = jnp.asarray(f, dtype=jnp.float64)
        return (1.0 - f) * sigma1 + f * sigma2

    @staticmethod
    @jax.jit
    def _maxwell_garnett_jit(sigma_m: float, sigma_i: float, f: float) -> jax.Array:
        """Maxwell-Garnett effective conductivity."""
        sigma_m = jnp.asarray(sigma_m, dtype=jnp.float64)
        sigma_i = jnp.asarray(sigma_i, dtype=jnp.float64)
        f = jnp.asarray(f, dtype=jnp.float64)
        numerator = sigma_i + 2.0 * sigma_m - 2.0 * f * (sigma_m - sigma_i)
        denominator = sigma_i + 2.0 * sigma_m + f * (sigma_m - sigma_i)
        return sigma_m * safe_div(numerator, denominator)

    @staticmethod
    @jax.jit
    def _brickell_jit(sigma1: float, sigma2: float, f: float) -> jax.Array:
        """Brickell/Bruggeman symmetric effective medium approximation.

        Analytical solution for 3D spherical inclusions:
        sigma_eff = (1/4) * (B + sqrt(B^2 + 8*sigma1*sigma2))
        where B = (3*f - 1)*sigma2 + (2 - 3*f)*sigma1
        """
        sigma1 = jnp.asarray(sigma1, dtype=jnp.float64)
        sigma2 = jnp.asarray(sigma2, dtype=jnp.float64)
        f = jnp.asarray(f, dtype=jnp.float64)
        B = (3.0 * f - 1.0) * sigma2 + (2.0 - 3.0 * f) * sigma1
        return 0.25 * (B + jnp.sqrt(B ** 2 + 8.0 * sigma1 * sigma2))


# -- Standalone functions -------------------------------------------------------------

@maxwell_cite(285, 286, part=2, chapter="Conduction in Three Dimensions",
              description="3D Ohm's law: J = sigma * E")
def ohms_law_3d_jax(
    E: jax.Array,
    sigma: jax.Array,
) -> jax.Array:
    """Calculate current density from electric field. Arts. 285-286.

    J = sigma * E  (scalar sigma)
    J = sigma @ E  (tensor sigma)

    Args:
        E: Electric field vector, shape (3,) or (..., 3).
        sigma: Conductivity (scalar or 3x3 tensor).

    Returns:
        Current density J, same shape as E.
    """
    return Conduction3DJAX._current_density_jit(sigma, E)


@maxwell_cite(285, 286, part=2, chapter="Conduction in Three Dimensions",
              description="Inverse 3D Ohm's law: E = J / sigma")
def electric_field_from_current_density_jax(
    J: jax.Array,
    sigma: jax.Array,
) -> jax.Array:
    """Calculate electric field from current density. Arts. 285-286.

    E = J / sigma  (scalar sigma)
    E = sigma^-1 @ J  (tensor sigma)

    Args:
        J: Current density vector, shape (3,) or (..., 3).
        sigma: Conductivity (scalar or 3x3 tensor).

    Returns:
        Electric field E, same shape as J.
    """
    return Conduction3DJAX._electric_field_jit(sigma, J)


@maxwell_cite(285, 286, part=2, chapter="Conduction in Three Dimensions",
              description="Conduction power density: P = J . E")
def conduction_power_density_jax(
    E: jax.Array,
    sigma: jax.Array,
) -> jax.Array:
    """Calculate power density from electric field. Arts. 285-286.

    P = J . E = sigma * E . E

    Args:
        E: Electric field vector, shape (3,).
        sigma: Conductivity (scalar or 3x3 tensor).

    Returns:
        Power density scalar.
    """
    return Conduction3DJAX._power_density_jit(sigma, E)


@maxwell_cite(297, 298, part=2, chapter="Spreading Resistance",
              description="Spherical spreading resistance")
def spherical_spreading_resistance_jax(
    sigma: float,
    radius: float,
) -> jax.Array:
    """Spherical spreading resistance. Arts. 297-298.

    R = 1 / (4 * pi * sigma * r)

    Args:
        sigma: Conductivity of the medium.
        radius: Radius of spherical electrode.

    Returns:
        Spreading resistance.
    """
    return SpreadingResistanceJAX._spherical_jit(sigma, radius)


@maxwell_cite(299, 300, part=2, chapter="Spreading Resistance",
              description="Hemispherical spreading resistance")
def hemispherical_spreading_resistance_jax(
    sigma: float,
    radius: float,
) -> jax.Array:
    """Hemispherical spreading resistance. Arts. 299-300.

    R = 1 / (2 * pi * sigma * r)

    Args:
        sigma: Conductivity of the medium.
        radius: Radius of hemispherical contact.

    Returns:
        Spreading resistance.
    """
    return SpreadingResistanceJAX._hemispherical_jit(sigma, radius)


@maxwell_cite(301, 302, part=2, chapter="Spreading Resistance",
              description="Circular contact resistance")
def circular_contact_resistance_jax(
    sigma: float,
    radius: float,
) -> jax.Array:
    """Circular contact resistance. Arts. 301-302.

    R = 1 / (4 * sigma * r)

    Args:
        sigma: Conductivity of the medium.
        radius: Radius of circular contact.

    Returns:
        Contact resistance.
    """
    return SpreadingResistanceJAX._circular_jit(sigma, radius)


@maxwell_cite(310, 311, 312, part=2, chapter="Effective Conductivity",
              description="Maxwell-Garnett effective medium formula")
def maxwell_garnett_conductivity_jax(
    sigma_m: float,
    sigma_i: float,
    vol_frac: float,
) -> jax.Array:
    """Maxwell-Garnett effective conductivity. Arts. 310-312.

    sigma_eff = sigma_m * (sigma_i + 2*sigma_m - 2*f*(sigma_m - sigma_i)) /
                (sigma_i + 2*sigma_m + f*(sigma_m - sigma_i))

    Args:
        sigma_m: Matrix (background) conductivity.
        sigma_i: Inclusion conductivity.
        vol_frac: Volume fraction of inclusions.

    Returns:
        Effective conductivity.
    """
    return EffectiveConductivityJAX._maxwell_garnett_jit(sigma_m, sigma_i, vol_frac)


@maxwell_cite(310, part=2, chapter="Effective Conductivity",
              description="Series mixing effective conductivity")
def effective_conductivity_series_jax(
    sigma1: float,
    sigma2: float,
    f: float,
) -> jax.Array:
    """Effective conductivity for series mixing. Art. 310.

    sigma_eff = 1 / (f/sigma2 + (1-f)/sigma1)

    Args:
        sigma1: Conductivity of material 1.
        sigma2: Conductivity of material 2.
        f: Volume fraction of material 2.

    Returns:
        Effective conductivity.
    """
    return EffectiveConductivityJAX._series_jit(sigma1, sigma2, f)


@maxwell_cite(310, part=2, chapter="Effective Conductivity",
              description="Parallel mixing effective conductivity")
def effective_conductivity_parallel_jax(
    sigma1: float,
    sigma2: float,
    f: float,
) -> jax.Array:
    """Effective conductivity for parallel mixing. Art. 310.

    sigma_eff = (1-f)*sigma1 + f*sigma2

    Args:
        sigma1: Conductivity of material 1.
        sigma2: Conductivity of material 2.
        f: Volume fraction of material 2.

    Returns:
        Effective conductivity.
    """
    return EffectiveConductivityJAX._parallel_jit(sigma1, sigma2, f)


@maxwell_cite(285, 286, 287, 288, part=2, chapter="Conduction in Three Dimensions",
              description="Verify 3D conduction relations")
def verify_conduction_3d_jax(
    E: jax.Array = jnp.array([1.0, 0.0, 0.0]),
    sigma: jax.Array = jnp.array(1.0),
    tol: float = 1e-10,
) -> Dict[str, Any]:
    """Verify 3D conduction consistency. Arts. 285-288.

    Checks that J = sigma*E, E = J/sigma, and power density are consistent.

    Args:
        E: Electric field vector.
        sigma: Conductivity (scalar or tensor).
        tol: Tolerance for verification.

    Returns:
        Dictionary with verification results.
    """
    E = jnp.asarray(E, dtype=jnp.float64)
    sigma = jnp.asarray(sigma, dtype=jnp.float64)

    J = ohms_law_3d_jax(E, sigma)
    E_recovered = electric_field_from_current_density_jax(J, sigma)
    P_direct = conduction_power_density_jax(E, sigma)
    P_from_JE = jnp.dot(J, E)

    E_close = jnp.max(jnp.abs(E_recovered - E)) < tol
    P_close = jnp.abs(P_direct - P_from_JE) < tol

    verified = bool(E_close & P_close)

    return {
        "J": J,
        "E_recovered": E_recovered,
        "E_error": jnp.max(jnp.abs(E_recovered - E)),
        "P_direct": P_direct,
        "P_from_JE": P_from_JE,
        "P_error": jnp.abs(P_direct - P_from_JE),
        "E_roundtrip_ok": bool(E_close),
        "P_consistent": bool(P_close),
        "verified": verified,
    }


@maxwell_cite(285, 286, 297, 298, 299, 300, 310, 311, 312, part=2,
              chapter="Conduction in Three Dimensions",
              description="Comprehensive 3D conduction analysis")
def analyze_conduction_jax(
    E: jax.Array,
    sigma: jax.Array,
    geometry: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Comprehensive 3D conduction analysis. Arts. 285-286, 297-300, 310-312.

    Args:
        E: Electric field vector.
        sigma: Conductivity (scalar or tensor).
        geometry: Optional dict with spreading resistance parameters.
            {'type': 'sphere'|'hemisphere'|'disk'|'cylinder',
             'radius': r, 'length': l (cylinder only)}

    Returns:
        Dictionary with J, power density, and optionally spreading resistance.
    """
    E = jnp.asarray(E, dtype=jnp.float64)
    sigma = jnp.asarray(sigma, dtype=jnp.float64)

    J = ohms_law_3d_jax(E, sigma)
    P = conduction_power_density_jax(E, sigma)
    J_mag = jnp.linalg.norm(J)

    result: Dict[str, Any] = {
        "current_density": J,
        "current_magnitude": J_mag,
        "power_density": P,
        "electric_field": E,
    }

    if geometry is not None:
        gtype = geometry.get("type", "sphere")
        radius = geometry.get("radius", 1.0)
        if gtype == "sphere":
            result["spreading_resistance"] = spherical_spreading_resistance_jax(
                float(sigma) if sigma.ndim == 0 else 1.0, radius
            )
        elif gtype == "hemisphere":
            result["spreading_resistance"] = hemispherical_spreading_resistance_jax(
                float(sigma) if sigma.ndim == 0 else 1.0, radius
            )
        elif gtype == "disk":
            result["spreading_resistance"] = circular_contact_resistance_jax(
                float(sigma) if sigma.ndim == 0 else 1.0, radius
            )
        elif gtype == "cylinder":
            length = geometry.get("length", 1.0)
            sr = SpreadingResistanceJAX(
                conductivity=float(sigma) if sigma.ndim == 0 else 1.0
            )
            result["spreading_resistance"] = sr.cylindrical_wire(radius, length)

    # Anisotropy info
    if sigma.ndim == 2:
        eigenvalues = jnp.linalg.eigvalsh(sigma)
        result["is_anisotropic"] = True
        result["principal_conductivities"] = eigenvalues
        result["anisotropy_ratio"] = safe_div(
            jnp.max(eigenvalues), jnp.min(eigenvalues), safe_default=1.0
        )
    else:
        result["is_anisotropic"] = False

    return result

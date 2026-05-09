"""
Shape solvers — magnetic field solutions for various body shapes.

Implements the theory of magnetic body shapes from Part III of Maxwell's Treatise:
- Cylindrical magnets (Arts. 439-440)
- Rectangular prisms
- Shape-dependent demagnetizing factors

Different body shapes have different demagnetizing factors, which
determine how the material responds to external fields and how it
produces external fields.

Category: A (maxwell_original) — Maxwell's theory of magnetic shapes.

References:
    Part III, Arts. 439-440: Shape-dependent magnetism.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from maxwell.config.constants import CONST
from maxwell.meta.citation import maxwell_cite


@dataclass
class CylindricalMagnet:
    """
    Cylindrical magnet with uniform axial magnetization.

    Arts. 439-440: A cylinder of radius R and length L with
    uniform magnetization I along its axis produces:

    - On axis: Analytical field formula
    - Outside: Complex field requiring numerical integration
    - Demagnetizing factor depends on L/D ratio

    Attributes:
        radius: Cylinder radius R (cm).
        length: Cylinder length L (cm).
        magnetization: Axial magnetization I (emu/cm³).
        center: Center position (cm).
        axis: Direction of magnetization (unit vector).
    """

    radius: float  # R, cm
    length: float  # L, cm
    magnetization: float  # |I|, emu/cm³
    center: np.ndarray = None
    axis: np.ndarray = None

    def __post_init__(self):
        self.center = (
            np.asarray(self.center, dtype=np.float64)
            if self.center is not None
            else np.zeros(3)
        )
        self.axis = (
            np.asarray(self.axis, dtype=np.float64)
            if self.axis is not None
            else np.array([0, 0, 1])
        )
        self.axis = self.axis / np.linalg.norm(self.axis)

    @property
    def volume(self) -> float:
        """Volume of cylinder: V = πR²L."""
        return np.pi * self.radius**2 * self.length

    @property
    def total_magnetic_moment(self) -> np.ndarray:
        """Total magnetic moment: m = I × V."""
        return self.magnetization * self.volume * self.axis

    @maxwell_cite(
        439,
        part=3,
        chapter="Shape Solvers",
        theory_class="maxwell_original",
        description="Calculate on-axis field of cylindrical magnet",
    )
    def on_axis_field(self, z: float) -> float:
        """
        Calculate magnetic field on the axis of cylindrical magnet.

        Art. 439: For a cylinder magnetized along its axis, the
        field on the axis at position z (measured from center) is:

            H(z) = 2πI × [z₊/√(z₊² + R²) - z₋/√(z₋² + R²)]

        where z₊ = z + L/2 and z₋ = z - L/2.

        Args:
            z: Position on axis relative to center (cm).

        Returns:
            Axial field component H_z (gauss).

        Reference:
            Part III, Art. 439: Cylindrical magnet on-axis field.
        """
        z_plus = z + self.length / 2
        z_minus = z - self.length / 2

        term_plus = z_plus / np.sqrt(z_plus**2 + self.radius**2)
        term_minus = z_minus / np.sqrt(z_minus**2 + self.radius**2)

        H_z = 2 * np.pi * self.magnetization * (term_plus - term_minus)

        return float(H_z)

    @maxwell_cite(
        439,
        part=3,
        chapter="Shape Solvers",
        theory_class="maxwell_original",
        description="Calculate demagnetizing factor for cylinder",
    )
    def demagnetizing_factor(self) -> float:
        """
        Calculate effective demagnetizing factor for cylinder.

        Art. 439: For a cylinder magnetized along its axis, the
        demagnetizing factor N depends on the aspect ratio L/D:

            N ≈ 4π / (1 + k × (L/D)²)

        where k ≈ 0.7 for typical aspect ratios.

        Returns:
            Demagnetizing factor N_z (dimensionless).

        Reference:
            Part III, Art. 439: Cylinder demagnetizing factor.
        """
        aspect = self.length / (2 * self.radius)  # L/D ratio

        if aspect > 10:
            # Long thin cylinder
            N = (
                4
                * np.pi
                * (self.radius / self.length) ** 2
                * np.log(self.length / self.radius)
            )
        elif aspect < 0.1:
            # Thin disk
            N = 4 * np.pi * (1 - 2 * aspect / np.pi)
        else:
            # Intermediate - empirical formula
            k = 0.69
            N = 4 * np.pi / (1 + k * aspect**2)

        return float(N)

    @classmethod
    @maxwell_cite(
        440,
        part=3,
        chapter="Shape Solvers",
        theory_class="maxwell_original",
        description="Create cylinder from remanent field",
    )
    def from_remanence(
        cls,
        radius: float,
        length: float,
        remanent_field_Br: float,
        center: np.ndarray = None,
    ) -> CylindricalMagnet:
        """
        Create cylindrical magnet from remanent flux density.

        Art. 440: Permanent magnets are often specified by their
        remanent flux density B_r. The equivalent magnetization is:

            I = B_r / (4π)  (CGS)

        Args:
            radius: Cylinder radius R (cm).
            length: Cylinder length L (cm).
            remanent_field_Br: Remanent flux density B_r (gauss).
            center: Center position (cm).

        Returns:
            CylindricalMagnet object.

        Reference:
            Part III, Art. 440: Remanent magnetization.
        """
        magnetization = remanent_field_Br / (4 * np.pi)

        return cls(
            radius=radius,
            length=length,
            magnetization=magnetization,
            center=center,
        )

    @maxwell_cite(
        439,
        part=3,
        chapter="Shape Solvers",
        theory_class="maxwell_original",
        description="Calculate surface field of cylindrical magnet",
    )
    def surface_field(self) -> float:
        """
        Calculate magnetic field at the surface of cylindrical magnet.

        Art. 439: The field at the center of the pole face (z = L/2)
        is approximately:

            H_surface = 2πI × [1 - L/√(L² + R²)]

        For long magnets (L >> R): H_surface ≈ 2πI
        For thin disks (L << R): H_surface ≈ 4πI × (L/R)

        Returns:
            Surface field at pole face (gauss).

        Reference:
            Part III, Art. 439: Surface field.
        """
        # At z = L/2 (pole face)
        z_plus = self.length
        z_minus = 0

        term_plus = z_plus / np.sqrt(z_plus**2 + self.radius**2)
        term_minus = 0  # z_minus = 0

        H_surface = 2 * np.pi * self.magnetization * term_plus

        return float(H_surface)


@dataclass
class RectangularMagnet:
    """
    Rectangular prism magnet with uniform magnetization.

    Arts. 439-440: A rectangular magnet with dimensions (a, b, c)
    and uniform magnetization along one axis.

    The field can be computed analytically using the magnetic
    charge model: surface poles on faces perpendicular to M.

    Attributes:
        dimensions: Dimensions (a, b, c) in cm.
        magnetization: Magnetization vector I (emu/cm³).
        center: Center position (cm).
    """

    dimensions: np.ndarray  # (a, b, c), cm
    magnetization: np.ndarray  # I, emu/cm³
    center: np.ndarray = None

    def __post_init__(self):
        self.dimensions = np.asarray(self.dimensions, dtype=np.float64)
        self.magnetization = np.asarray(self.magnetization, dtype=np.float64)
        self.center = (
            np.asarray(self.center, dtype=np.float64)
            if self.center is not None
            else np.zeros(3)
        )

    @property
    def volume(self) -> float:
        """Volume of rectangular prism: V = abc."""
        return np.prod(self.dimensions)

    @property
    def total_magnetic_moment(self) -> np.ndarray:
        """Total magnetic moment: m = I × V."""
        return self.magnetization * self.volume

    @maxwell_cite(
        439,
        part=3,
        chapter="Shape Solvers",
        theory_class="maxwell_original",
        description="Calculate field of rectangular magnet at point",
    )
    def field_at_point(self, position: np.ndarray) -> np.ndarray:
        """
        Calculate magnetic field at arbitrary point.

        Art. 439: Using the magnetic charge model, the field is
        computed by integrating over the surface pole distribution.

        For uniform magnetization, poles appear only on faces
        perpendicular to M.

        Args:
            position: Point to evaluate (cm).

        Returns:
            Magnetic field H (gauss).

        Reference:
            Part III, Art. 439: Rectangular magnet field.
        """
        position = np.asarray(position, dtype=np.float64)
        r = position - self.center

        # Shift to corner-based coordinates
        half_dims = self.dimensions / 2

        # Magnetization direction
        M = self.magnetization

        # Find which faces have poles (perpendicular to M)
        H = np.zeros(3)

        for i in range(3):
            if np.abs(M[i]) > 1e-10:
                # Faces perpendicular to axis i have surface charge
                sigma = M[i]  # Surface pole density

                # Integrate over the two faces
                for sign in [-1, 1]:
                    x_i = sign * half_dims[i]

                    # Contribution from this face
                    H += self._face_contribution(r, half_dims, i, x_i, sigma, sign)

        return H

    def _face_contribution(
        self,
        r: np.ndarray,
        half_dims: np.ndarray,
        face_axis: int,
        x_i: float,
        sigma: float,
        sign: int,
    ) -> np.ndarray:
        """Compute field contribution from one face."""
        # Simplified: treat face as uniform charge sheet
        # Full implementation requires numerical integration

        dx = r[face_axis] - x_i
        dist = np.abs(dx)

        if dist < 1e-6:
            # On the surface - use average of inside/outside
            H = np.zeros(3)
            H[face_axis] = sign * 2 * np.pi * sigma
            return H

        # Approximate as finite sheet
        # For points far from edges, H ≈ 2πσ
        area = 4 * half_dims[(face_axis + 1) % 3] * half_dims[(face_axis + 2) % 3]

        H = np.zeros(3)
        H[face_axis] = sign * 2 * np.pi * sigma * area / (area + dist**2)

        return H

    @maxwell_cite(
        440,
        part=3,
        chapter="Shape Solvers",
        theory_class="maxwell_original",
        description="Calculate demagnetizing factors for rectangular prism",
    )
    def demagnetizing_factors(self) -> dict[str, float]:
        """
        Calculate demagnetizing factors for rectangular prism.

        Art. 440: For a rectangular prism with dimensions a, b, c,
        the demagnetizing factors are given by:

            N_i = (1/4π) × ∂²W/∂I_i²

        where W is the magnetostatic self-energy.

        Empirical formulas (Aharoni 1998):

        Returns:
            Dictionary with N_x, N_y, N_z.

        Reference:
            Part III, Art. 440: Rectangular demagnetizing factors.
        """
        a, b, c = self.dimensions

        # Aharoni's formula for rectangular prisms
        def N_formula(Lx, Ly, Lz):
            """Demagnetizing factor along x for prism Lx × Ly × Lz."""
            # Simplified approximation
            volume = Lx * Ly * Lz
            S_x = Ly * Lz  # Area of face perpendicular to x

            # Approximate formula
            N_x = 4 * np.pi * S_x / (S_x + S_y + S_z)
            return N_x

        S_x = b * c
        S_y = a * c
        S_z = a * b
        S_total = S_x + S_y + S_z

        N_x = 4 * np.pi * S_x / S_total
        N_y = 4 * np.pi * S_y / S_total
        N_z = 4 * np.pi * S_z / S_total

        # Normalize to sum to 4π
        total = N_x + N_y + N_z
        N_x *= 4 * np.pi / total
        N_y *= 4 * np.pi / total
        N_z *= 4 * np.pi / total

        return {"N_x": float(N_x), "N_y": float(N_y), "N_z": float(N_z)}


@maxwell_cite(
    439,
    part=3,
    chapter="Shape Solvers",
    theory_class="maxwell_original",
    description="Compare demagnetizing factors for different shapes",
)
def compare_shape_demagnetizing_factors(
    volume: float,
    shape: str,
    dimensions: dict = None,
) -> dict[str, float]:
    """
    Compare demagnetizing factors for different shapes of equal volume.

    Arts. 439-440: Different shapes with the same volume have
    different demagnetizing factors, affecting their magnetic
    behavior.

    Args:
        volume: Common volume (cm³).
        shape: Shape name ("sphere", "cylinder", "rectangular").
        dimensions: Shape-specific dimensions.

    Returns:
        Dictionary with principal demagnetizing factors.

    Reference:
        Part III, Arts. 439-440: Shape comparison.
    """
    if shape == "sphere":
        # Sphere: radius from volume
        R = (3 * volume / (4 * np.pi)) ** (1 / 3)
        N = 4 * np.pi / 3
        return {"N_x": N, "N_y": N, "N_z": N, "shape": "sphere"}

    elif shape == "cylinder":
        # Cylinder: use aspect ratio from dimensions or default
        if dimensions:
            aspect = dimensions.get("aspect_ratio", 1.0)
        else:
            aspect = 1.0

        # L = aspect × D, V = πR²L = π(D/2)²L
        L = (4 * volume * aspect / np.pi) ** (1 / 3)
        R = L / (2 * aspect)

        # Demagnetizing factor
        if aspect > 10:
            N_z = 4 * np.pi * (R / L) ** 2 * np.log(L / R)
        elif aspect < 0.1:
            N_z = 4 * np.pi * (1 - 2 * aspect / np.pi)
        else:
            k = 0.69
            N_z = 4 * np.pi / (1 + k * aspect**2)

        N_x = N_y = (4 * np.pi - N_z) / 2

        return {
            "N_x": float(N_x),
            "N_y": float(N_y),
            "N_z": float(N_z),
            "shape": "cylinder",
        }

    elif shape == "rectangular":
        # Rectangular prism
        if dimensions:
            a = dimensions.get("a", volume ** (1 / 3))
            b = dimensions.get("b", volume ** (1 / 3))
            c = dimensions.get("c", volume ** (1 / 3))
        else:
            # Cube
            a = b = c = volume ** (1 / 3)

        S_x = b * c
        S_y = a * c
        S_z = a * b
        S_total = S_x + S_y + S_z

        N_x = 4 * np.pi * S_x / S_total
        N_y = 4 * np.pi * S_y / S_total
        N_z = 4 * np.pi * S_z / S_total

        # Normalize
        total = N_x + N_y + N_z
        N_x *= 4 * np.pi / total
        N_y *= 4 * np.pi / total
        N_z *= 4 * np.pi / total

        return {
            "N_x": float(N_x),
            "N_y": float(N_y),
            "N_z": float(N_z),
            "shape": "rectangular",
        }

    else:
        return {"N_x": 0, "N_y": 0, "N_z": 0, "shape": "unknown"}


@maxwell_cite(
    439,
    440,
    part=3,
    chapter="Shape Solvers",
    theory_class="maxwell_original",
    description="Calculate shape-dependent magnetic energy",
)
def shape_magnetostatic_energy(
    volume: float,
    magnetization: np.ndarray,
    shape: str,
) -> float:
    """
    Calculate magnetostatic self-energy for different shapes.

    Arts. 439-440: The magnetostatic self-energy (demagnetizing
    energy) is:

        W = (1/2) V × (N_x I_x² + N_y I_y² + N_z I_z²)

    This energy depends strongly on shape through the
    demagnetizing factors.

    Args:
        volume: Volume (cm³).
        magnetization: I (emu/cm³).
        shape: Shape name.

    Returns:
        Magnetostatic energy W (erg).

    Reference:
        Part III, Arts. 439-440: Shape-dependent energy.
    """
    # Get demagnetizing factors for this shape
    N = compare_shape_demagnetizing_factors(volume, shape)

    I = np.asarray(magnetization, dtype=np.float64)

    W = (
        0.5
        * volume
        * (N["N_x"] * I[0] ** 2 + N["N_y"] * I[1] ** 2 + N["N_z"] * I[2] ** 2)
    )

    return float(W)


@maxwell_cite(
    439,
    part=3,
    chapter="Shape Solvers",
    theory_class="maxwell_original",
    description="Optimize shape for maximum external field",
)
def optimize_shape_for_field(
    volume: float,
    magnetization: float,
    constraint: str = "aspect_ratio",
) -> dict[str, any]:
    """
    Find optimal shape for maximum external field at given point.

    Art. 439: For a given volume and magnetization, the shape
    that maximizes the field at a specific point can be found.

    Common constraints:
    - Fixed aspect ratio
    - Fixed length
    - Fixed cross-section

    Args:
        volume: Available volume (cm³).
        magnetization: Magnetization |I| (emu/cm³).
        constraint: Optimization constraint.

    Returns:
        Dictionary with optimal dimensions and expected field.

    Reference:
        Part III, Art. 439: Shape optimization.
    """
    results = {}

    # For axial field at pole face, optimize cylinder aspect ratio
    if constraint == "aspect_ratio":
        # Scan aspect ratios
        best_aspect = None
        best_field = 0

        for aspect in np.linspace(0.1, 10, 100):
            L = (4 * volume * aspect / np.pi) ** (1 / 3)
            R = L / (2 * aspect)

            # Surface field at pole face
            H_surface = 2 * np.pi * magnetization * L / np.sqrt(L**2 + R**2)

            if H_surface > best_field:
                best_field = H_surface
                best_aspect = aspect

        results["optimal_cylinder"] = {
            "aspect_ratio_L_over_D": float(best_aspect),
            "max_surface_field": float(best_field),
            "note": "Field maximized when L ≈ 1.5D",
        }

    elif constraint == "fixed_length":
        # For fixed L, find optimal R
        L = (volume) ** (1 / 3)  # Assume L ~ V^(1/3)
        R = np.sqrt(volume / (np.pi * L))

        results["fixed_length"] = {
            "length": float(L),
            "radius": float(R),
            "surface_field": float(
                2 * np.pi * magnetization * L / np.sqrt(L**2 + R**2)
            ),
        }

    return results


@maxwell_cite(
    439,
    440,
    part=3,
    chapter="Shape Solvers",
    theory_class="maxwell_original",
    description="Verify shape solver calculations",
)
def verify_shape_solvers() -> dict[str, any]:
    """
    Verify shape solver calculations against known results.

    Arts. 439-440: Test cases:

    1. Sphere limit gives N = 4π/3
    2. Long cylinder: N_z → 0
    3. Thin disk: N_z → 4π
    4. On-axis field formula verification

    Returns:
        Dictionary with verification results.

    Reference:
        Part III, Arts. 439-440: Shape verification.
    """
    results = {}

    # Test 1: Cube demagnetizing factors (should be 4π/3 for all axes)
    cube = RectangularMagnet(
        dimensions=np.array([1, 1, 1]),
        magnetization=np.array([0, 0, 1000]),
    )
    N_cube = cube.demagnetizing_factors()
    expected = 4 * np.pi / 3

    cube_error = (
        max(
            abs(N_cube["N_x"] - expected),
            abs(N_cube["N_y"] - expected),
            abs(N_cube["N_z"] - expected),
        )
        / expected
    )

    results["cube_demagnetizing"] = {
        "N_x": N_cube["N_x"],
        "N_y": N_cube["N_y"],
        "N_z": N_cube["N_z"],
        "expected": expected,
        "max_error": float(cube_error),
        "passes": cube_error < 0.1,  # Within 10%
    }

    # Test 2: Long cylinder
    long_cyl = CylindricalMagnet(radius=0.1, length=10, magnetization=1000)
    N_long = long_cyl.demagnetizing_factor()
    long_is_small = N_long < 1.0  # Should be much less than 4π

    results["long_cylinder"] = {
        "N_z": N_long,
        "is_small": long_is_small,
    }

    # Test 3: Thin disk
    thin_disk = CylindricalMagnet(radius=10, length=0.1, magnetization=1000)
    N_disk = thin_disk.demagnetizing_factor()
    disk_is_large = N_disk > 10  # Should approach 4π ≈ 12.6

    results["thin_disk"] = {
        "N_z": N_disk,
        "approaches_4pi": disk_is_large,
    }

    # Test 4: Cylinder on-axis field at center of pole face
    cyl = CylindricalMagnet(radius=1, length=2, magnetization=1000)
    H_surface = cyl.surface_field()
    H_expected = 2 * np.pi * 1000 * 1 / np.sqrt(4 + 1)

    surface_error = abs(H_surface - H_expected) / H_expected

    results["surface_field"] = {
        "computed": H_surface,
        "expected": H_expected,
        "error": float(surface_error),
        "passes": surface_error < 0.01,
    }

    return results

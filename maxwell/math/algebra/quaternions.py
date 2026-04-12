"""maxwell.math.algebra.quaternions — Quaternion algebra (Art. 522).

Implements Maxwell's use of quaternion algebra for electromagnetic
field representation. Maxwell was one of the first to use quaternions
in physics, predating modern vector notation.

Maxwell's CGS formulation (Art. 522):
    A quaternion q has the form:

        q = w + i*x + j*y + k*z

    where w is the scalar part and (x, y, z) is the vector part.

    Quaternion multiplication (Hamilton product):
        q1 * q2 = (w1*w2 - x1*x2 - y1*y2 - z1*z2)
                + i*(w1*x2 + x1*w2 + y1*z2 - z1*y2)
                + j*(w1*y2 - x1*z2 + y1*w2 + z1*x2)
                + k*(w1*z2 + x1*y2 - y1*x2 + z1*w2)

    Maxwell used quaternions to represent:
    - The operator nabla = i*d/dx + j*d/dy + k*d/dz
    - The combination of scalar and vector potentials
    - Field rotations and transformations

where:
    q = quaternion (dimensionless)
    i, j, k = quaternion units (i^2 = j^2 = k^2 = ijk = -1)

Category: A (maxwell_original) — Maxwell's quaternion algebra.

References:
    Part IV, Art. 522: Quaternion notation in electromagnetism.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from maxwell.meta.citation import maxwell_cite
from maxwell.config.constants import CONST


@dataclass
class Quaternion:
    """
    Quaternion representation for electromagnetic calculations.

    Art. 522: Maxwell used quaternions to unify scalar and vector
    operations. A quaternion q = w + xi + yj + zk can represent:
    - The electromagnetic potential (w = phi, (x,y,z) = A)
    - Field rotations and transformations
    - The nabla operator combined with scalar operations

    Attributes:
        w: Scalar part.
        x: i component.
        y: j component.
        z: k component.
    """

    w: float = 0.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @classmethod
    def from_vector(cls, vector: np.ndarray, scalar: float = 0.0) -> "Quaternion":
        """Create quaternion from scalar and vector parts."""
        v = np.asarray(vector, dtype=np.float64)
        return cls(scalar, v[0], v[1], v[2])

    def to_vector(self) -> np.ndarray:
        """Extract vector part as numpy array."""
        return np.array([self.x, self.y, self.z])

    def scalar_part(self) -> float:
        """Return scalar (real) part."""
        return self.w

    def vector_part(self) -> np.ndarray:
        """Return vector (imaginary) part."""
        return self.to_vector()

    @maxwell_cite(
        522,
        part=4, chapter="Quaternion Algebra",
        theory_class="maxwell_original",
        description="Calculate quaternion conjugate",
    )
    def conjugate(self) -> "Quaternion":
        """
        Calculate quaternion conjugate.

        Art. 522: The conjugate of q = w + xi + yj + zk is:

            q* = w - xi - yj - zk

        Returns:
            Conjugate quaternion.
        """
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    @maxwell_cite(
        522,
        part=4, chapter="Quaternion Algebra",
        theory_class="maxwell_original",
        description="Calculate quaternion norm",
    )
    def norm(self) -> float:
        """
        Calculate quaternion norm (magnitude).

        Art. 522: The norm is:

            |q| = sqrt(w^2 + x^2 + y^2 + z^2)

        Returns:
            Norm (dimensionless).
        """
        return np.sqrt(self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2)

    @maxwell_cite(
        522,
        part=4, chapter="Quaternion Algebra",
        theory_class="maxwell_original",
        description="Calculate quaternion product",
    )
    def multiply(self, other: "Quaternion") -> "Quaternion":
        """
        Calculate Hamilton product of two quaternions.

        Art. 522: The quaternion product (Hamilton product):

            q1 * q2 = (w1*w2 - v1.v2) + (w1*v2 + w2*v1 + v1 x v2)

        where v1, v2 are the vector parts.

        Args:
            other: Right operand.

        Returns:
            Product quaternion.
        """
        v1 = self.to_vector()
        v2 = other.to_vector()

        w_new = self.w * other.w - np.dot(v1, v2)
        v_new = self.w * v2 + other.w * v1 + np.cross(v1, v2)

        return Quaternion(w_new, v_new[0], v_new[1], v_new[2])

    def __mul__(self, other: "Quaternion") -> "Quaternion":
        return self.multiply(other)

    def __add__(self, other: "Quaternion") -> "Quaternion":
        return Quaternion(
            self.w + other.w,
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other: "Quaternion") -> "Quaternion":
        return Quaternion(
            self.w - other.w,
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __repr__(self) -> str:
        return f"Quaternion({self.w}, {self.x}i, {self.y}j, {self.z}k)"


@maxwell_cite(
    522,
    part=4, chapter="Quaternion Algebra",
    theory_class="maxwell_original",
    description="Calculate quaternion product",
)
def calc_quaternion_product(
    q1_w: float, q1_x: float, q1_y: float, q1_z: float,
    q2_w: float, q2_x: float, q2_y: float, q2_z: float,
) -> tuple[float, float, float, float]:
    """
    Calculate Hamilton product of two quaternions.

    Art. 522: The product (w1 + v1)(w2 + v2) = (w1*w2 - v1.v2) + (w1*v2 + w2*v1 + v1 x v2)

    Args:
        q1_w, q1_x, q1_y, q1_z: First quaternion components.
        q2_w, q2_x, q2_y, q2_z: Second quaternion components.

    Returns:
        Tuple (w, x, y, z) of product.
    """
    v1 = np.array([q1_x, q1_y, q1_z])
    v2 = np.array([q2_x, q2_y, q2_z])

    w = q1_w * q2_w - np.dot(v1, v2)
    v = q1_w * v2 + q2_w * v1 + np.cross(v1, v2)

    return (w, v[0], v[1], v[2])


@maxwell_cite(
    522,
    part=4, chapter="Quaternion Algebra",
    theory_class="maxwell_original",
    description="Calculate quaternion norm",
)
def calc_quaternion_norm(w: float, x: float, y: float, z: float) -> float:
    """
    Calculate quaternion norm.

    Art. 522: |q| = sqrt(w^2 + x^2 + y^2 + z^2)

    Args:
        w, x, y, z: Quaternion components.

    Returns:
        Norm (dimensionless).
    """
    return np.sqrt(w ** 2 + x ** 2 + y ** 2 + z ** 2)


@maxwell_cite(
    522,
    part=4, chapter="Quaternion Algebra",
    theory_class="maxwell_original",
    description="Rotate vector using quaternion",
)
def rotate_vector(
    vector: np.ndarray,
    axis: np.ndarray,
    angle: float,
) -> np.ndarray:
    """
    Rotate a vector using quaternion rotation.

    Art. 522: A rotation by angle theta about axis n is represented by:

        q = cos(theta/2) + sin(theta/2) * (n_x*i + n_y*j + n_z*k)

    The rotated vector is: v' = q * v * q^{-1}

    Args:
        vector: Vector to rotate.
        axis: Rotation axis (unit vector).
        angle: Rotation angle (radians).

    Returns:
        Rotated vector.
    """
    vector = np.asarray(vector, dtype=np.float64)
    axis = np.asarray(axis, dtype=np.float64)
    axis_norm = np.linalg.norm(axis)
    if axis_norm > 0:
        axis = axis / axis_norm

    half_angle = angle / 2.0
    cos_half = np.cos(half_angle)
    sin_half = np.sin(half_angle)

    # Rotation quaternion
    q = Quaternion(cos_half, sin_half * axis[0], sin_half * axis[1], sin_half * axis[2])
    q_inv = q.conjugate()  # For unit quaternion, conjugate = inverse

    # Vector as pure quaternion
    v_q = Quaternion(0, vector[0], vector[1], vector[2])

    # Rotate: v' = q * v * q^{-1}
    result = q.multiply(v_q).multiply(q_inv)

    return result.to_vector()


@maxwell_cite(
    522,
    part=4, chapter="Quaternion Algebra",
    theory_class="maxwell_original",
    description="Create quaternion from electromagnetic potentials",
)
def quaternion_from_potentials(
    scalar_potential: float,
    vector_potential: np.ndarray,
) -> Quaternion:
    """
    Create quaternion from electromagnetic potentials.

    Art. 522: Maxwell represented the electromagnetic potential
    as a quaternion with the scalar potential as the real part
    and the vector potential as the imaginary part:

        Q = phi + A_x*i + A_y*j + A_z*k

    Args:
        scalar_potential: Electric scalar potential phi (statvolts).
        vector_potential: Magnetic vector potential A (gauss*cm).

    Returns:
        Electromagnetic potential quaternion.
    """
    vector_potential = np.asarray(vector_potential, dtype=np.float64)
    return Quaternion(
        scalar_potential,
        vector_potential[0],
        vector_potential[1],
        vector_potential[2],
    )


@maxwell_cite(
    522,
    part=4, chapter="Quaternion Algebra",
    theory_class="maxwell_original",
    description="Create quaternion from electromagnetic fields",
)
def quaternion_from_fields(
    E_field: np.ndarray,
    B_field: np.ndarray,
) -> Quaternion:
    """
    Create quaternion from electromagnetic fields.

    Art. 522: The electromagnetic field can be represented as a
    quaternion combining E and B fields.

    Args:
        E_field: Electric field (statvolts/cm).
        B_field: Magnetic field (gauss).

    Returns:
        Field quaternion (scalar = 0, vector = E + i*B representation).
    """
    E_field = np.asarray(E_field, dtype=np.float64)
    B_field = np.asarray(B_field, dtype=np.float64)

    # Maxwell's representation: field = E + i*c*B (complex quaternion)
    # For real quaternions, we use E as vector part
    E_mag = np.linalg.norm(E_field)
    B_mag = np.linalg.norm(B_field)

    return Quaternion(
        0.0,  # No scalar part for pure field
        E_field[0] + CONST.C * B_field[0],
        E_field[1] + CONST.C * B_field[1],
        E_field[2] + CONST.C * B_field[2],
    )


@maxwell_cite(
    522,
    part=4, chapter="Quaternion Algebra",
    theory_class="maxwell_original",
    description="Verify quaternion algebra properties",
)
def verify_quaternion_properties(
    tolerance: float = 1e-10,
) -> dict[str, float | bool]:
    """
    Verify quaternion algebra properties.

    Art. 522: This function verifies:
    1. Non-commutativity: q1*q2 != q2*q1 (in general)
    2. Norm multiplication: |q1*q2| = |q1|*|q2|
    3. Associativity: (q1*q2)*q3 = q1*(q2*q3)
    4. Conjugate norm: |q*| = |q|

    Args:
        tolerance: Numerical tolerance.

    Returns:
        Dictionary with verification results.
    """
    q1 = Quaternion(1, 2, 3, 4)
    q2 = Quaternion(5, 6, 7, 8)

    # Non-commutativity
    p1 = q1.multiply(q2)
    p2 = q2.multiply(q1)
    noncommutative = bool(
        np.linalg.norm(p1.to_vector() - p2.to_vector()) > tolerance
        or abs(p1.w - p2.w) > tolerance
    )

    # Norm multiplication
    norm_product = (q1 * q2).norm()
    product_norms = q1.norm() * q2.norm()
    norm_error = abs(norm_product - product_norms) / product_norms if product_norms > 1e-15 else abs(norm_product)

    # Associativity
    q3 = Quaternion(9, 10, 11, 12)
    left = (q1 * q2) * q3
    right = q1 * (q2 * q3)
    assoc_error = abs(left.w - right.w) + np.linalg.norm(left.to_vector() - right.to_vector())

    # Conjugate norm
    q1_conj = q1.conjugate()
    conj_norm_error = abs(q1_conj.norm() - q1.norm())

    # Rotation preserves vector length
    v = np.array([1.0, 0.0, 0.0])
    v_rotated = rotate_vector(v, np.array([0, 0, 1]), np.pi / 2)
    rotation_error = abs(np.linalg.norm(v_rotated) - np.linalg.norm(v))

    # Expected: rotation by 90 deg about z: (1,0,0) -> (0,1,0)
    expected = np.array([0.0, 1.0, 0.0])
    rotation_accuracy = np.linalg.norm(v_rotated - expected)

    return {
        "noncommutative": noncommutative,
        "norm_multiplication_error": norm_error,
        "associativity_error": assoc_error,
        "conjugate_norm_error": conj_norm_error,
        "rotation_length_error": rotation_error,
        "rotation_accuracy": rotation_accuracy,
        "norm_multiplication_verified": bool(norm_error < tolerance),
        "associativity_verified": bool(assoc_error < tolerance),
        "conjugate_norm_verified": bool(conj_norm_error < tolerance),
        "rotation_verified": bool(rotation_error < tolerance and rotation_accuracy < tolerance),
        "all_verified": bool(
            noncommutative
            and norm_error < tolerance
            and assoc_error < tolerance
            and conj_norm_error < tolerance
            and rotation_error < tolerance
        ),
    }


@maxwell_cite(
    522,
    part=4, chapter="Quaternion Algebra",
    theory_class="maxwell_original",
    description="Complete quaternion analysis",
)
def analyze_quaternion_algebra(
    test_quaternions: list[Quaternion] = None,
) -> dict[str, float | np.ndarray | list]:
    """
    Complete analysis of quaternion algebra.

    Art. 522: Comprehensive analysis including:
    1. Quaternion properties (norm, conjugate)
    2. Product verification
    3. Rotation demonstration
    4. Electromagnetic potential representation

    Args:
        test_quaternions: Quaternions for analysis.

    Returns:
        Dictionary with complete analysis results.
    """
    if test_quaternions is None:
        test_quaternions = [
            Quaternion(1, 0, 0, 0),  # Pure scalar
            Quaternion(0, 1, 0, 0),  # Pure i
            Quaternion(1, 1, 1, 1),  # Mixed
            Quaternion(0, 1, 2, 3),  # Pure vector
        ]

    results = {
        "quaternions": test_quaternions,
    }

    norms = []
    conjugates = []

    for q in test_quaternions:
        norms.append(q.norm())
        conjugates.append(q.conjugate())

    results["norms"] = norms
    results["conjugates"] = conjugates

    # Demonstrate rotation
    v = np.array([1.0, 0.0, 0.0])
    rotations = []
    for angle in [0, np.pi / 4, np.pi / 2, np.pi]:
        v_rot = rotate_vector(v, np.array([0, 0, 1]), angle)
        rotations.append(v_rot)

    results["rotation_demonstration"] = {
        "original_vector": v,
        "rotation_axis": np.array([0, 0, 1]),
        "angles": [0, np.pi / 4, np.pi / 2, np.pi],
        "rotated_vectors": rotations,
    }

    return results

"""Qualifying G3 tests for Arts. 667-669 (current-sheet boundary conditions).

Bundle A of the Wave-7 PHYSICUS share: the implementations in
``maxwell/electromagnetism/current_sheets/boundary_conditions.py`` carried
zero article-marked tests.  These tests pin the article-specific
computations against oracles INDEPENDENT of the code under test:

* Art. 667 (normal B continuity): hand-derived vector decomposition
  goldens plus a div B = 0 pillbox limit -- for a source-free dipole
  field the normal-component difference across the interface tends to
  zero with first-order convergence as the two sample points coalesce
  (a calculus oracle independent of the module).
* Art. 668 (normal D jump = 4 pi sigma): the Gauss-law pillbox solution
  of an infinite charged sheet, E = +/- 2 pi sigma on the two sides.
* Art. 669 (eps2 E2n - eps1 E1n = 4 pi sigma): a full dielectric-
  interface field solution constructed from the analytic boundary laws
  and verified end-to-end by ``verify_boundary_conditions``.

All asserts are numeric with stated tolerances (REQ-T rubric; lint R10);
goldens live in ``tests/articles/reference_values.json`` with
provenance.  The PARKING-LOT annotations for Arts. 663-666 (Wave-6
adjudication; defect D-34 parked) are untouched by this bundle.

Run: PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_articles_boundary_conditions_667_669.py -q
"""

from __future__ import annotations

import numpy as np
import pytest
from articles import ref_value, tolerance_of

from maxwell.electromagnetism.current_sheets.boundary_conditions import (
    BoundaryConditionAnalyzer,
    ElectromagneticBoundary,
    calc_normal_B_continuity,
    calc_normal_D_discontinuity,
    verify_boundary_conditions,
)

TIGHT = 1e-12


def _dipole_B(point: np.ndarray) -> np.ndarray:
    """Unit z-directed magnetic dipole field at the origin (CGS-Gaussian).

    Independent oracle field: B = (3 (m . r_hat) r_hat - m) / r^3 with
    m = z_hat.  It is divergence-free away from the origin, so the
    normal component across any source-free plane is continuous in the
    pillbox limit (hand-derived from the standard dipole solution).
    """
    r = np.asarray(point, dtype=np.float64)
    radius = np.linalg.norm(r)
    r_hat = r / radius
    m = np.array([0.0, 0.0, 1.0])
    return (3.0 * np.dot(m, r_hat) * r_hat - m) / radius**3


# ── Art. 667 — normal B is continuous across any boundary ──────────────────


@pytest.mark.article(667)
def test_art667_normal_B_continuity_hand_decomposition():
    """Art. 667: with B1 = (3, 4, 5), B2 = (-6, 2, 5), normal z-hat the
    normal components are both 5 (difference 0) while the tangential
    parts (3, 4, 0) and (-6, 2, 0) are unrestricted -- norms 5 and
    sqrt(40).  Golden: hand-derived vector decomposition.
    """
    B1 = np.array([3.0, 4.0, 5.0])
    B2 = np.array([-6.0, 2.0, 5.0])
    n = np.array([0.0, 0.0, 1.0])

    result = calc_normal_B_continuity(B1, B2, n)
    assert result["B1_normal_magnitude"] == pytest.approx(5.0, rel=TIGHT)
    assert result["B2_normal_magnitude"] == pytest.approx(5.0, rel=TIGHT)
    assert result["difference"] == pytest.approx(
        ref_value(667, "normal_B_continuous_difference"),
        **tolerance_of(667, "normal_B_continuous_difference"),
    )
    assert bool(result["continuous"]) is True
    assert np.linalg.norm(result["B1_tangential"]) == pytest.approx(5.0, rel=TIGHT)
    assert np.linalg.norm(result["B2_tangential"]) == pytest.approx(
        ref_value(667, "normal_B_tangential2_norm"),
        **tolerance_of(667, "normal_B_tangential2_norm"),
    )

    # The analyzer wrapper must reproduce the identical numbers.
    analyzer = BoundaryConditionAnalyzer(ElectromagneticBoundary(normal=n))
    wrapped = analyzer.check_normal_B(B1, B2)
    assert wrapped["difference"] == pytest.approx(result["difference"], abs=1e-15)
    assert wrapped["B2_normal_magnitude"] == pytest.approx(5.0, rel=TIGHT)


@pytest.mark.article(667)
def test_art667_normal_B_pillbox_limit_first_order_convergence():
    """Art. 667 pillbox oracle (independent of the module): the dipole
    field is divergence-free away from the origin, so sampling its
    normal component at heights +/- h/2 around the plane z = 2 must give
    a difference tending to zero as h -> 0 with first order (ratio of
    successive differences -> 2).  The continuity asserted by Art. 667
    is exactly this h -> 0 limit.
    """
    n = np.array([0.0, 0.0, 1.0])
    xy = np.array([0.3, 0.4])
    z_plane = 2.0

    def difference_at(h: float) -> float:
        B1 = _dipole_B(np.array([xy[0], xy[1], z_plane - 0.5 * h]))
        B2 = _dipole_B(np.array([xy[0], xy[1], z_plane + 0.5 * h]))
        return calc_normal_B_continuity(B1, B2, n)["difference"]

    d_coarse = difference_at(1e-1)
    d_fine = difference_at(5e-2)
    # Non-degenerate sampling point: the normal component genuinely varies.
    assert abs(d_coarse) > 1e-9
    assert abs(d_fine) > 1e-11
    # First-order convergence to the continuous limit: ratio -> 2.
    # provenance: Taylor expansion of a smooth source-free field; the
    # O(h^2) remainder at h/z = 0.05 keeps the ratio within 1% of 2.
    assert abs(d_coarse) / abs(d_fine) == pytest.approx(2.0, rel=1e-2)
    assert abs(d_fine) < abs(d_coarse)


# ── Art. 668 — normal D jumps by 4 pi sigma (Gauss pillbox) ────────────────


@pytest.mark.article(668)
def test_art668_normal_D_jump_gauss_sheet_oracle():
    """Art. 668: an infinite sheet sigma = 2.5 statC/cm^2 in vacuum is
    the Gauss-law pillbox oracle -- E = +/- 2 pi sigma on the two sides,
    independently derived, so D2n - D1n must equal 4 pi sigma = 10 pi and
    the inferred charge must return sigma exactly.
    """
    sigma = 2.5  # statcoulombs/cm^2
    n = np.array([0.0, 0.0, 1.0])
    D_below = np.array([0.0, 0.0, -2.0 * np.pi * sigma])
    D_above = np.array([0.0, 0.0, 2.0 * np.pi * sigma])

    result = calc_normal_D_discontinuity(D_below, D_above, n, surface_charge=sigma)
    assert result["difference"] == pytest.approx(
        ref_value(668, "normal_D_jump_gauss_sheet"),
        **tolerance_of(668, "normal_D_jump_gauss_sheet"),
    )
    assert result["expected_jump"] == pytest.approx(4.0 * np.pi * sigma, rel=TIGHT)
    assert result["inferred_charge"] == pytest.approx(
        ref_value(668, "gauss_sheet_inferred_charge"),
        **tolerance_of(668, "gauss_sheet_inferred_charge"),
    )
    assert bool(result["gauss_satisfied"]) is True


# ── Art. 669 — dielectric interface: eps2 E2n - eps1 E1n = 4 pi sigma ──────


@pytest.mark.article(668)
@pytest.mark.article(669)
def test_art669_charged_dielectric_interface_full_solution():
    """Art. 669: hand-constructed analytic solution of a charged
    dielectric interface (eps1 = 2, eps2 = 5, sigma_s = 3 statC/cm^2,
    tangential E continuous, B fully continuous, no surface current):
    E2n = (eps1 E1n + 4 pi sigma_s)/eps2.  All four boundary conditions
    hold by construction; the module must verify them and report the D
    jump 4 pi sigma_s = 12 pi.
    """
    eps1, eps2, sigma_s = 2.0, 5.0, 3.0
    E1n = 1.5
    E2n = (eps1 * E1n + 4.0 * np.pi * sigma_s) / eps2  # hand-derived
    boundary = ElectromagneticBoundary(
        normal=np.array([0.0, 0.0, 1.0]),
        epsilon1=eps1,
        epsilon2=eps2,
        mu1=1.0,
        mu2=1.0,
        sigma_s=sigma_s,
        current_s=np.zeros(2),
    )
    E1 = np.array([7.0, -2.0, E1n])
    E2 = np.array([7.0, -2.0, E2n])
    B = np.array([1.0, -4.0, 6.0])

    # The constructed normal field matches its hand-derived golden.
    assert E2n == pytest.approx(
        ref_value(669, "charged_interface_E2n"),
        **tolerance_of(669, "charged_interface_E2n"),
    )

    result = verify_boundary_conditions(boundary, E1, B, E2, B)
    assert result["normal_D"]["difference"] == pytest.approx(
        ref_value(669, "charged_interface_D_jump"),
        **tolerance_of(669, "charged_interface_D_jump"),
    )
    assert result["normal_D"]["expected_jump"] == pytest.approx(
        4.0 * np.pi * sigma_s, rel=TIGHT
    )
    assert result["tangential_E"]["discontinuity_magnitude"] == pytest.approx(
        0.0, abs=1e-12
    )
    assert result["normal_B"]["difference"] == pytest.approx(0.0, abs=1e-12)
    assert bool(result["all_satisfied"]) is True


@pytest.mark.article(669)
def test_art669_uncharged_dielectric_refraction_identity():
    """Art. 669 uncharged limit (hand-derived): with sigma_s = 0 the
    condition reduces to eps1 E1n = eps2 E2n (normal D continuous) while
    tangential E stays continuous -- the standard dielectric refraction
    law.  eps1 = 2, eps2 = 3, E1n = 3 forces E2n = 2 exactly.
    """
    boundary = ElectromagneticBoundary.dielectric_interface(2.0, 3.0)
    E1 = np.array([1.0, -0.5, 3.0])
    E2 = np.array([1.0, -0.5, 2.0])
    B = np.array([0.2, 0.7, 1.3])

    result = verify_boundary_conditions(boundary, E1, B, E2, B)
    # D normal: 2*3 = 3*2 = 6 on both sides, jump zero.
    assert result["normal_D"]["difference"] == pytest.approx(0.0, abs=1e-12)
    assert result["normal_D"]["D1_normal_magnitude"] == pytest.approx(6.0, rel=TIGHT)
    assert result["normal_D"]["D2_normal_magnitude"] == pytest.approx(6.0, rel=TIGHT)
    assert bool(result["normal_D"]["gauss_satisfied"]) is True
    assert result["tangential_E"]["discontinuity_magnitude"] == pytest.approx(
        0.0, abs=1e-12
    )
    assert result["normal_B"]["difference"] == pytest.approx(0.0, abs=1e-12)
    assert bool(result["all_satisfied"]) is True

---
type: certification-record
artifact: article_certifications_667_866
gate: G4-prep (Wave 8b, examiner recommendation R1 companion)
date: 2026-08-22
generator: scripts/build_article_certifications.py (machine-derived from article_ledger.json + article_evidence_report.json + reference_values.json)
collab_reviewed: true
---

# Article Certification Records — Arts. 667–866 (Part IV, Ch XII–XXIII)

**Certifier:** SCRIBA (documentation-and-certification persona). 
**State certified:** Wave-7 / G3-close, the certified baseline of the independent fresh-context G3 gate review (`docs/reports/G3_GATE_REVIEW_2026-08-21.md`, verdict **PASS**, 2026-08-22). 
**Regenerated:** 2026-08-22 by `scripts/build_article_certifications.py` from the three machine artifacts listed in §Provenance. No number in this file is hand-entered.

> **Scope of this record.** Per-article certification of the 200 articles 667–866 at tier **T3 (machine-evidenced)**. This record does **not** contain page verdicts or formula-sheet adjudications: those are the human-adjudicated G1 items still pending (Stage-2 §4.3 G1 exit criteria; G3 gate review §9; Stage-5 §8), and T4/spine promotion explicitly awaits the human page-verdict session plus REQ-X SymPy verifiers. Nothing here pre-judges them.

## Certification criteria (as applied)

Tier ladder and Definition of Done: Stage-1 §4 (REQ-F/REQ-M/REQ-V/REQ-T, "REQ-F + REQ-M + REQ-V + REQ-T satisfied ⇒ T3 ('ensured')"), Stage-2 §5.4 (T2→T3 certified by QUALITAS, implementer ≠ certifier), Stage-3 §6. For each article below, the machine evidence is:

| Criterion | Machine evidence cited per article |
|---|---|
| **REQ-F** — article-specific computation | `article_ledger.json` citation(s): module :: function bound to the article by `@maxwell_cite` |
| **REQ-T** — passing article-marked test | `article_evidence_report.json` evidence list (`pytest.mark.article(N)`; suite 2312 passed / 0 failed at G3) |
| **REQ-V** — reference value | `tests/articles/reference_values.json` entry where present (Ref column); otherwise the qualifying tests assert hand-derived goldens / independent oracles (G3 gate review §4, 12 sampled files, 0 theater) — flagged honestly, not overstated |
| **REQ-M** — formula fidelity | Spot-checked equation-by-equation for 10 articles by the G3 examiner (§3, all **Real**); wave-level QA + defect closures for the rest; full formula-sheet sign-off is the pending G1 human item and is **not** claimed here |
| No open ≤S2 defect | Defects column: 5 S1 closed G2-exit, 5 S2 closed Wave 7 (G3 §5), 4 S3 carried as non-blocking (G3 §6); **0 open S1/S2 in scope** |

**Honesty note on REQ-V.** All 200 of the 200 articles carry entries in the central reference store (254 in-scope values; 0 empty provenance fields). The Wave-9 builder (`scripts/build_reference_store_wave9.py`) derives every Wave-9 entry independently of the maxwell package (provenance Classes 2–5); the G4-pre audit re-derived 8 sampled pins to agreement (`docs/reports/G4_PRE_AUDIT_2026-08-22.md` §2 W9a). REQ-V store coverage in scope is complete.

Column legend — **Impls**: `module::function` citation pairs from the ledger (`maxwell/` prefix elided); **Cites**: ledger `cite_count`; **Tests**: count of qualifying `pytest.mark.article(N)` tests (full nodeids in the appendix); **Ref**: reference-store entry present, with value count; **Defects**: closed/carried defect annotations with source, or `none`; **Tier**: verdict.

Scanner note — `math/spherical_harmonics.py::<unknown>` entries are the ledger's stacked-decorator attribution misses (scanner warning class; 37 warnings total, 15 in this file — `article_ledger_summary.md`, G3 gate review §1.3). They are not phantom citations: the G3 examiner resolved the affected functions in source (e.g. Art 690 → `calc_multipole_expansion`, G3 §3) and coverage counting is unaffected.

---

## Chapter IV.XII — Ch XII: Current-Sheets (Arts. 667–674)

8 articles · 31 qualifying marked tests · 8/8 with reference-store entries.

| Art | Impls (module::function) | Cites | Tests | Ref | Defects | Tier |
|-----|--------------------------|-------|-------|-----|---------|------|
| 667 | `electromagnetism/current_sheets/boundary_conditions.py::calc_normal_B_continuity`<br>`electromagnetism/current_sheets/boundary_conditions.py::check_normal_B`<br>`electromagnetism/current_sheets/boundary_conditions.py::dielectric_interface`<br>`electromagnetism/current_sheets/boundary_conditions.py::verify_all`<br>`electromagnetism/current_sheets/boundary_conditions.py::verify_boundary_conditions`<br>`verification/sympy_verify.py::verify_normal_B_continuous`<br>`verification/sympy_verify.py::verify_surface_current_jump` | 7 | 8 | yes (2) | none | **T3** |
| 668 | `electromagnetism/current_sheets/boundary_conditions.py::calc_normal_D_discontinuity`<br>`electromagnetism/current_sheets/boundary_conditions.py::check_normal_D`<br>`electromagnetism/current_sheets/boundary_conditions.py::dielectric_interface`<br>`electromagnetism/current_sheets/boundary_conditions.py::verify_all`<br>`electromagnetism/current_sheets/boundary_conditions.py::verify_boundary_conditions`<br>`verification/sympy_verify.py::verify_solenoid_inductance_structure` | 6 | 5 | yes (2) | none | **T3** |
| 669 | `electromagnetism/current_sheets/boundary_conditions.py::calc_normal_D_discontinuity`<br>`electromagnetism/current_sheets/boundary_conditions.py::check_normal_D`<br>`electromagnetism/current_sheets/boundary_conditions.py::dielectric_interface`<br>`electromagnetism/current_sheets/boundary_conditions.py::verify_all`<br>`electromagnetism/current_sheets/boundary_conditions.py::verify_boundary_conditions`<br>`verification/sympy_verify.py::verify_sheet_potential_discontinuity` | 6 | 5 | yes (2) | none | **T3** |
| 670 | `electromagnetism/components/circular_coils.py::analyze_circular_coil`<br>`electromagnetism/components/circular_coils.py::calc_coil_on_axis`<br>`electromagnetism/components/circular_coils.py::center_field`<br>`electromagnetism/components/circular_coils.py::field_at`<br>`electromagnetism/components/circular_coils.py::verify_coil_field`<br>`electromagnetism/current_sheets/boundary_conditions.py::calc_tangential_H_discontinuity`<br>`electromagnetism/current_sheets/boundary_conditions.py::check_tangential_H`<br>`electromagnetism/current_sheets/boundary_conditions.py::conducting_surface`<br>`electromagnetism/current_sheets/boundary_conditions.py::dielectric_interface`<br>`electromagnetism/current_sheets/boundary_conditions.py::verify_all`<br>`electromagnetism/current_sheets/boundary_conditions.py::verify_boundary_conditions`<br>`verification/sympy_verify.py::verify_cylindrical_sheet_field` | 12 | 4 | yes (1) | S3-2 carried — docstring reads abamperes, code carries CONST.C; doc-only, pinned rel 1e-13; non-blocking | **T3** |
| 671 | `electromagnetism/components/circular_coils.py::analyze_circular_coil`<br>`electromagnetism/components/circular_coils.py::calc_coil_on_axis`<br>`electromagnetism/components/circular_coils.py::center_field`<br>`electromagnetism/components/circular_coils.py::verify_coil_field`<br>`electromagnetism/current_sheets/boundary_conditions.py::calc_tangential_H_discontinuity`<br>`electromagnetism/current_sheets/boundary_conditions.py::check_tangential_H`<br>`electromagnetism/current_sheets/boundary_conditions.py::conducting_surface`<br>`electromagnetism/current_sheets/boundary_conditions.py::dielectric_interface`<br>`electromagnetism/current_sheets/boundary_conditions.py::verify_all`<br>`electromagnetism/current_sheets/boundary_conditions.py::verify_boundary_conditions`<br>`verification/sympy_verify.py::verify_sheet_toroidal_zero_exterior` | 11 | 4 | yes (1) | S3-2 carried — docstring reads abamperes, code carries CONST.C; doc-only, pinned rel 1e-13; non-blocking | **T3** |
| 672 | `electromagnetism/components/circular_coils.py::analyze_circular_coil`<br>`electromagnetism/components/circular_coils.py::calc_coil_on_axis`<br>`electromagnetism/components/circular_coils.py::verify_coil_field`<br>`electromagnetism/current_sheets/boundary_conditions.py::analyze_moving_boundary`<br>`electromagnetism/current_sheets/boundary_conditions.py::calc_moving_boundary_conditions` | 5 | 1 | yes (1) | S3-2 carried — docstring reads abamperes, code carries CONST.C; doc-only, pinned rel 1e-13; non-blocking | **T3** |
| 673 | `electromagnetism/components/circular_coils.py::analyze_circular_coil`<br>`electromagnetism/components/circular_coils.py::calc_coil_off_axis`<br>`electromagnetism/current_sheets/boundary_conditions.py::analyze_moving_boundary`<br>`electromagnetism/current_sheets/boundary_conditions.py::calc_moving_boundary_conditions` | 4 | 2 | yes (1) | CLOSED D-14 — S2, closed Wave 7: truncated elliptic series deleted, Landen/AGM routing; +D-29 neg-parameter K<br>S3-2 carried — docstring reads abamperes, code carries CONST.C; doc-only, pinned rel 1e-13; non-blocking | **T3** |
| 674 | `electromagnetism/components/circular_coils.py::analyze_circular_coil`<br>`electromagnetism/components/circular_coils.py::calc_coil_off_axis`<br>`electromagnetism/current_sheets/boundary_conditions.py::calc_boundary_energy_flux`<br>`electromagnetism/current_sheets/boundary_conditions.py::energy_flux` | 4 | 2 | yes (1) | CLOSED D-14 — S2, closed Wave 7: truncated elliptic series deleted, Landen/AGM routing; +D-29 neg-parameter K<br>S3-2 carried — docstring reads abamperes, code carries CONST.C; doc-only, pinned rel 1e-13; non-blocking | **T3** |

## Chapter IV.XIII — Ch XIII: Parallel Currents (Arts. 675–693)

19 articles · 58 qualifying marked tests · 19/19 with reference-store entries.

| Art | Impls (module::function) | Cites | Tests | Ref | Defects | Tier |
|-----|--------------------------|-------|-------|-----|---------|------|
| 675 | `electromagnetism/components/circular_coils.py::analyze_circular_coil`<br>`electromagnetism/components/circular_coils.py::calc_coil_off_axis`<br>`electromagnetism/components/solenoids.py::analyze_solenoid`<br>`electromagnetism/components/solenoids.py::calc_solenoid_field`<br>`electromagnetism/components/solenoids.py::center_field`<br>`electromagnetism/components/solenoids.py::field_at`<br>`electromagnetism/components/solenoids.py::verify_solenoid_field`<br>`math/spherical_harmonics.py::<unknown>`<br>`verification/sympy_verify.py::verify_legendre_orthogonality`<br>`verification/sympy_verify.py::verify_legendre_parity`<br>`verification/sympy_verify.py::verify_legendre_recurrence`<br>`verification/sympy_verify.py::verify_legendre_value_at_one` | 15 | 15 | yes (1) | CLOSED D-14 — S2, closed Wave 7: truncated elliptic series deleted, Landen/AGM routing; +D-29 neg-parameter K<br>S3-2 carried — docstring reads abamperes, code carries CONST.C; doc-only, pinned rel 1e-13; non-blocking | **T3** |
| 676 | `electromagnetism/components/circular_coils.py::analyze_circular_coil`<br>`electromagnetism/components/circular_coils.py::calc_double_coil_field`<br>`electromagnetism/components/circular_coils.py::verify_helmholtz_uniformity`<br>`electromagnetism/components/solenoids.py::analyze_solenoid`<br>`electromagnetism/components/solenoids.py::calc_solenoid_field`<br>`electromagnetism/components/solenoids.py::verify_solenoid_field`<br>`math/spherical_harmonics.py::<unknown>`<br>`verification/sympy_verify.py::verify_Y00_normalization`<br>`verification/sympy_verify.py::verify_addition_theorem_p1`<br>`verification/sympy_verify.py::verify_legendre_generating_function` | 11 | 10 | yes (1) | S3-2 carried — docstring reads abamperes, code carries CONST.C; doc-only, pinned rel 1e-13; non-blocking | **T3** |
| 677 | `electromagnetism/components/circular_coils.py::analyze_circular_coil`<br>`electromagnetism/components/circular_coils.py::calc_double_coil_field`<br>`electromagnetism/components/circular_coils.py::verify_helmholtz_uniformity`<br>`electromagnetism/components/solenoids.py::analyze_solenoid`<br>`electromagnetism/components/solenoids.py::calc_infinite_solenoid_field`<br>`electromagnetism/components/solenoids.py::infinite_field`<br>`electromagnetism/components/solenoids.py::verify_solenoid_field`<br>`math/spherical_harmonics.py::<unknown>`<br>`verification/sympy_verify.py::verify_legendre_differential_equation`<br>`verification/sympy_verify.py::verify_zonal_harmonic_laplace` | 10 | 7 | yes (1) | S3-2 carried — docstring reads abamperes, code carries CONST.C; doc-only, pinned rel 1e-13; non-blocking | **T3** |
| 678 | `electromagnetism/components/circular_coils.py::calc_coaxial_coil_pair`<br>`electromagnetism/components/solenoids.py::analyze_solenoid`<br>`electromagnetism/components/solenoids.py::calc_infinite_solenoid_field`<br>`math/spherical_harmonics.py::<unknown>` | 4 | 1 | yes (1) | S3-2 carried — docstring reads abamperes, code carries CONST.C; doc-only, pinned rel 1e-13; non-blocking | **T3** |
| 679 | `electromagnetism/components/circular_coils.py::calc_coaxial_coil_pair`<br>`electromagnetism/components/solenoids.py::analyze_solenoid`<br>`electromagnetism/components/solenoids.py::calc_helmholtz_center` | 3 | 1 | yes (1) | S3-2 carried — docstring reads abamperes, code carries CONST.C; doc-only, pinned rel 1e-13; non-blocking | **T3** |
| 680 | `electromagnetism/components/cylinders.py::analyze_cylindrical_conductor`<br>`electromagnetism/components/cylinders.py::calc_cylindrical_field`<br>`electromagnetism/components/cylinders.py::field_at`<br>`electromagnetism/components/cylinders.py::verify_cylindrical_field`<br>`electromagnetism/components/solenoids.py::analyze_solenoid`<br>`electromagnetism/components/solenoids.py::calc_helmholtz_center` | 6 | 2 | yes (1) | none | **T3** |
| 681 | `electromagnetism/components/cylinders.py::analyze_cylindrical_conductor`<br>`electromagnetism/components/cylinders.py::calc_cylindrical_field`<br>`electromagnetism/components/cylinders.py::verify_cylindrical_field`<br>`electromagnetism/components/solenoids.py::analyze_solenoid`<br>`electromagnetism/components/solenoids.py::calc_helmholtz_center` | 5 | 1 | yes (1) | none | **T3** |
| 682 | `electromagnetism/components/cylinders.py::analyze_cylindrical_conductor`<br>`electromagnetism/components/cylinders.py::calc_hollow_cylinder_field`<br>`electromagnetism/components/cylinders.py::verify_cylindrical_field`<br>`electromagnetism/components/solenoids.py::calc_helmholtz_uniformity` | 4 | 2 | yes (1) | none | **T3** |
| 683 | `electromagnetism/components/cylinders.py::analyze_cylindrical_conductor`<br>`electromagnetism/components/cylinders.py::calc_hollow_cylinder_field`<br>`electromagnetism/components/cylinders.py::verify_cylindrical_field`<br>`electromagnetism/components/solenoids.py::calc_helmholtz_uniformity` | 4 | 2 | yes (1) | none | **T3** |
| 684 | `electromagnetism/components/cylinders.py::analyze_cylindrical_conductor`<br>`electromagnetism/components/cylinders.py::calc_wire_self_inductance` | 2 | 1 | yes (1) | none | **T3** |
| 685 | `electromagnetism/components/cylinders.py::analyze_cylindrical_conductor`<br>`electromagnetism/components/cylinders.py::calc_wire_self_inductance`<br>`math/spherical_harmonics.py::<unknown>` | 6 | 2 | yes (1) | none | **T3** |
| 686 | `electromagnetism/components/cylinders.py::calc_cylinder_vector_potential`<br>`electromagnetism/components/cylinders.py::vector_potential_at`<br>`math/spherical_harmonics.py::<unknown>` | 5 | 2 | yes (1) | none | **T3** |
| 687 | `electromagnetism/components/cylinders.py::calc_cylinder_vector_potential`<br>`math/spherical_harmonics.py::<unknown>` | 4 | 1 | yes (1) | none | **T3** |
| 688 | `math/spherical_harmonics.py::<unknown>` | 3 | 1 | yes (1) | S3-3 carried (normalization_check 50/49 endpoint overcount; theorem pinned rel 1e-12; non-blocking) | **T3** |
| 689 | `math/spherical_harmonics.py::<unknown>` | 4 | 2 | yes (2) | none | **T3** |
| 690 | `math/spherical_harmonics.py::<unknown>` | 3 | 1 | yes (1) | none | **T3** |
| 691 | `math/geometry/gmd.py::analyze_gmd`<br>`math/geometry/gmd.py::calc_gmd_parallel_wires`<br>`math/geometry/gmd.py::calc_gmd_points`<br>`math/geometry/gmd.py::calc_inductance_from_gmd`<br>`math/geometry/gmd.py::calc_self_gmd_circle`<br>`math/geometry/gmd.py::calc_self_gmd_rectangle`<br>`math/geometry/gmd.py::gmd_to`<br>`math/geometry/gmd.py::self_gmd`<br>`math/geometry/gmd.py::verify_gmd_relations`<br>`math/spherical_harmonics.py::<unknown>` | 12 | 1 | yes (1) | none | **T3** |
| 692 | `math/geometry/gmd.py::analyze_gmd`<br>`math/geometry/gmd.py::calc_gmd_coaxial_circles`<br>`math/geometry/gmd.py::calc_gmd_parallel_wires`<br>`math/geometry/gmd.py::calc_gmd_points`<br>`math/geometry/gmd.py::calc_inductance_from_gmd`<br>`math/geometry/gmd.py::calc_self_gmd_circle`<br>`math/geometry/gmd.py::calc_self_gmd_rectangle`<br>`math/geometry/gmd.py::gmd_to`<br>`math/geometry/gmd.py::verify_gmd_relations`<br>`math/spherical_harmonics.py::<unknown>` | 12 | 2 | yes (2) | none | **T3** |
| 693 | `math/geometry/gmd.py::analyze_gmd`<br>`math/geometry/gmd.py::calc_gmd_coaxial_circles`<br>`math/geometry/gmd.py::calc_gmd_parallel_wires`<br>`math/geometry/gmd.py::calc_gmd_points`<br>`math/geometry/gmd.py::calc_inductance_from_gmd`<br>`math/geometry/gmd.py::verify_gmd_relations`<br>`math/spherical_harmonics.py::<unknown>` | 8 | 4 | yes (1) | none | **T3** |

## Chapter IV.XIV — Ch XIV: Circular Currents (Arts. 694–706)

13 articles · 62 qualifying marked tests · 13/13 with reference-store entries.

| Art | Impls (module::function) | Cites | Tests | Ref | Defects | Tier |
|-----|--------------------------|-------|-------|-----|---------|------|
| 694 | `math/spherical_harmonics.py::calc_vector_potential_circular_current`<br>`verification/sympy_verify.py::verify_circular_current_center_field`<br>`verification/sympy_verify.py::verify_loop_axial_field_integral`<br>`verification/sympy_verify.py::verify_loop_far_field_dipole_limit`<br>`verification/sympy_verify.py::verify_mutual_inductance_neumann_symmetry` | 5 | 14 | yes (1) | none | **T3** |
| 695 | `math/spherical_harmonics.py::calc_magnetic_shell_potential_circular_current` | 1 | 2 | yes (1) | none | **T3** |
| 696 | `math/elliptic_integrals.py::analyze_elliptic_integrals`<br>`math/elliptic_integrals.py::calc_complete_elliptic_integral_first_kind`<br>`math/elliptic_integrals.py::calc_complete_elliptic_k_parameter`<br>`math/elliptic_integrals.py::calc_elliptic_integral_first_kind`<br>`math/elliptic_integrals.py::first_kind`<br>`math/elliptic_integrals.py::verify_elliptic_integrals`<br>`verification/sympy_verify.py::verify_elliptic_K_AGM_identity`<br>`verification/sympy_verify.py::verify_vector_potential_loop_structure` | 8 | 9 | yes (2) | none | **T3** |
| 697 | `electromagnetism/forces/coil_forces.py::analyze_coil_forces`<br>`electromagnetism/forces/coil_forces.py::calc_coaxial_coil_force`<br>`electromagnetism/forces/coil_forces.py::calc_coil_system_energy`<br>`electromagnetism/forces/coil_forces.py::calc_solenoid_force`<br>`electromagnetism/forces/coil_forces.py::verify_coil_forces`<br>`math/elliptic_integrals.py::analyze_elliptic_integrals`<br>`math/elliptic_integrals.py::calc_complete_elliptic_e_parameter`<br>`math/elliptic_integrals.py::calc_complete_elliptic_integral_second_kind`<br>`math/elliptic_integrals.py::calc_elliptic_integral_second_kind`<br>`math/elliptic_integrals.py::second_kind`<br>`math/elliptic_integrals.py::verify_elliptic_integrals` | 11 | 3 | yes (2) | none | **T3** |
| 698 | `electromagnetism/forces/coil_forces.py::analyze_coil_forces`<br>`electromagnetism/forces/coil_forces.py::calc_coaxial_coil_force`<br>`electromagnetism/forces/coil_forces.py::calc_coil_system_energy`<br>`electromagnetism/forces/coil_forces.py::calc_coil_torque`<br>`electromagnetism/forces/coil_forces.py::verify_coil_forces`<br>`math/elliptic_integrals.py::analyze_elliptic_integrals`<br>`math/elliptic_integrals.py::calc_elliptic_integral_third_kind`<br>`math/elliptic_integrals.py::third_kind`<br>`math/elliptic_integrals.py::verify_elliptic_integrals` | 9 | 1 | yes (1) | none | **T3** |
| 699 | `electromagnetism/forces/coil_forces.py::analyze_coil_forces`<br>`electromagnetism/forces/coil_forces.py::calc_coil_system_energy`<br>`electromagnetism/forces/coil_forces.py::calc_coil_torque`<br>`electromagnetism/forces/coil_forces.py::verify_coil_forces`<br>`math/elliptic_integrals.py::analyze_elliptic_integrals`<br>`math/elliptic_integrals.py::jacobian_functions`<br>`math/elliptic_integrals.py::verify_elliptic_integrals`<br>`verification/sympy_verify.py::verify_loop_axial_field_integral` | 8 | 1 | yes (1) | none | **T3** |
| 700 | `math/elliptic_integrals.py::analyze_elliptic_integrals`<br>`math/elliptic_integrals.py::landen_transformation`<br>`math/elliptic_integrals.py::verify_elliptic_integrals` | 3 | 1 | yes (1) | none | **T3** |
| 701 | `math/elliptic_integrals.py::analyze_elliptic_integrals`<br>`math/elliptic_integrals.py::complementary_modulus`<br>`math/elliptic_integrals.py::verify_elliptic_integrals` | 3 | 1 | yes (1) | none | **T3** |
| 702 | `electromagnetism/vis/circular_fields.py::analyze_circular_fields`<br>`electromagnetism/vis/circular_fields.py::calc_flux_through_circle`<br>`electromagnetism/vis/circular_fields.py::calc_stream_function`<br>`electromagnetism/vis/circular_fields.py::generate_field_lines`<br>`electromagnetism/vis/circular_fields.py::trace_field_line`<br>`electromagnetism/vis/circular_fields.py::verify_field_lines`<br>`math/elliptic_integrals.py::analyze_elliptic_integrals`<br>`math/elliptic_integrals.py::calc_complete_elliptic_e_parameter`<br>`math/elliptic_integrals.py::calc_complete_elliptic_k_parameter`<br>`math/elliptic_integrals.py::verify_elliptic_integrals` | 10 | 3 | yes (1) | CLOSED D-02 — S1, closed G2-exit: A_phi off-axis | **T3** |
| 703 | `math/elliptic_integrals.py::analyze_elliptic_integrals`<br>`math/elliptic_integrals.py::verify_elliptic_integrals`<br>`verification/sympy_verify.py::verify_elliptic_E_small_k_series`<br>`verification/sympy_verify.py::verify_elliptic_K_AGM_identity`<br>`verification/sympy_verify.py::verify_elliptic_K_small_k_series`<br>`verification/sympy_verify.py::verify_elliptic_legendre_relation` | 6 | 10 | yes (1) | none | **T3** |
| 704 | `math/elliptic_integrals.py::analyze_elliptic_integrals`<br>`math/elliptic_integrals.py::verify_elliptic_integrals`<br>`verification/sympy_verify.py::verify_elliptic_E_derivative_identity`<br>`verification/sympy_verify.py::verify_elliptic_K_derivative_identity`<br>`verification/sympy_verify.py::verify_elliptic_legendre_relation` | 5 | 7 | yes (1) | none | **T3** |
| 705 | `math/elliptic_integrals.py::analyze_elliptic_integrals`<br>`math/elliptic_integrals.py::verify_elliptic_integrals`<br>`verification/sympy_verify.py::verify_elliptic_landen_descent` | 3 | 4 | yes (1) | none | **T3** |
| 706 | `electromagnetism/optimization/coil_design.py::calc_gauss_optimal_coil`<br>`electromagnetism/optimization/coil_design.py::calc_max_inductance_design`<br>`electromagnetism/optimization/coil_design.py::calc_optimal_coil_mean_radius`<br>`electromagnetism/optimization/coil_design.py::calc_optimal_mean_radius_to_gmd_ratio`<br>`electromagnetism/optimization/coil_design.py::calc_self_inductance_circular_coil`<br>`electromagnetism/optimization/coil_design.py::calc_square_channel_optimal_coil`<br>`verification/sympy_verify.py::verify_circular_current_center_field` | 7 | 6 | yes (4) | none | **T3** |

## Chapter IV.XV — Ch XV: Electromagnetic Instruments (Arts. 707–729)

23 articles · 30 qualifying marked tests · 23/23 with reference-store entries.

| Art | Impls (module::function) | Cites | Tests | Ref | Defects | Tier |
|-----|--------------------------|-------|-------|-----|---------|------|
| 707 | `instruments/galvanometers.py::_compute_coil_constant` | 1 | 2 | yes (1) | CLOSED D-16 — S2, closed Wave 7: Gaussian-CGS CONST.C convention | **T3** |
| 708 | `instruments/galvanometers.py::design_standard_coil` | 1 | 1 | yes (1) | CLOSED D-16 — S2, closed Wave 7: Gaussian-CGS CONST.C convention | **T3** |
| 709 | `instruments/galvanometers.py::calc_field_at_center`<br>`instruments/galvanometers.py::calc_galvanometer_response` | 2 | 3 | yes (1) | CLOSED D-15 — S2, closed Wave 7: implicit torsion torque balance<br>CLOSED D-16 — S2, closed Wave 7: Gaussian-CGS CONST.C convention | **T3** |
| 710 | `instruments/galvanometers.py::current_from_deflection`<br>`instruments/galvanometers.py::current_from_rotation`<br>`instruments/galvanometers.py::deflection_from_current` | 3 | 1 | yes (1) | none | **T3** |
| 711 | `instruments/galvanometers.py::measure_current` | 1 | 1 | yes (1) | none | **T3** |
| 712 | `instruments/galvanometers.py::apply_gaugain_suspension` | 1 | 1 | yes (1) | none | **T3** |
| 713 | `instruments/helmholtz.py::field_at_center`<br>`instruments/helmholtz.py::field_on_axis`<br>`instruments/helmholtz.py::uniformity_region` | 3 | 4 | yes (3) | S3-1 carried — EMU pocket, documented convention island with stated bridge; non-blocking | **T3** |
| 714 | `instruments/galvanometers.py::combined_coil_constant`<br>`instruments/galvanometers.py::measure_current` | 2 | 1 | yes (1) | none | **T3** |
| 715 | `instruments/galvanometers.py::combined_coil_constant`<br>`instruments/galvanometers.py::measure_current` | 2 | 1 | yes (1) | none | **T3** |
| 716 | `instruments/optimization/sensitivity.py::optimize_galvanometer_wire` | 1 | 2 | yes (1) | S3-1 carried — EMU pocket, documented convention island with stated bridge; non-blocking | **T3** |
| 717 | `instruments/galvanometers.py::design_sensitive_galvanometer` | 1 | 1 | yes (1) | none | **T3** |
| 718 | `instruments/optimization/sensitivity.py::optimize_galvanometer_sensitivity` | 1 | 1 | yes (1) | S3-1 carried — EMU pocket, documented convention island with stated bridge; non-blocking | **T3** |
| 719 | `instruments/optimization/sensitivity.py::apply_sensitivity_wire_law` | 1 | 1 | yes (1) | S3-1 carried — EMU pocket, documented convention island with stated bridge; non-blocking | **T3** |
| 720 | `instruments/galvanometers.py::calc_uniform_wire_sensitivity`<br>`instruments/galvanometers.py::measure_current`<br>`instruments/galvanometers.py::sensitivity` | 3 | 1 | yes (1) | none | **T3** |
| 721 | `instruments/suspended_coil.py::equilibrium_deflection`<br>`instruments/suspended_coil.py::magnetic_moment`<br>`instruments/suspended_coil.py::torque` | 3 | 1 | yes (1) | S3-1 carried — EMU pocket, documented convention island with stated bridge; non-blocking | **T3** |
| 722 | `instruments/suspended_coil.py::measure_current`<br>`instruments/suspended_coil.py::sensitivity` | 2 | 1 | yes (1) | S3-1 carried — EMU pocket, documented convention island with stated bridge; non-blocking | **T3** |
| 723 | `instruments/suspended_coil.py::determine_magnetic_force` | 1 | 1 | yes (1) | S3-1 carried — EMU pocket, documented convention island with stated bridge; non-blocking | **T3** |
| 724 | `instruments/suspended_coil.py::measure_current_both_methods` | 1 | 1 | yes (1) | S3-1 carried — EMU pocket, documented convention island with stated bridge; non-blocking | **T3** |
| 725 | `instruments/dynamometers.py::equilibrium_deflection`<br>`instruments/dynamometers.py::measure_current`<br>`instruments/dynamometers.py::torque`<br>`instruments/dynamometers.py::verify_force_proportional_to_I_squared` | 4 | 1 | yes (1) | S3-1 carried — EMU pocket, documented convention island with stated bridge; non-blocking | **T3** |
| 726 | `instruments/dynamometers.py::balancing_mass`<br>`instruments/dynamometers.py::force`<br>`instruments/dynamometers.py::measure_current` | 3 | 1 | yes (1) | S3-1 carried — EMU pocket, documented convention island with stated bridge; non-blocking | **T3** |
| 727 | `instruments/dynamometers.py::calc_solenoid_suction` | 1 | 1 | yes (1) | S3-1 carried — EMU pocket, documented convention island with stated bridge; non-blocking | **T3** |
| 728 | `instruments/suspended_coil.py::calc_uniform_normal_force` | 1 | 1 | yes (1) | S3-1 carried — EMU pocket, documented convention island with stated bridge; non-blocking | **T3** |
| 729 | `instruments/dynamometers.py::measure_current_from_torsion`<br>`instruments/dynamometers.py::torsion_angle` | 2 | 1 | yes (1) | S3-1 carried — EMU pocket, documented convention island with stated bridge; non-blocking | **T3** |

## Chapter IV.XVI — Ch XVI: Observations (Arts. 730–751)

22 articles · 28 qualifying marked tests · 22/22 with reference-store entries.

| Art | Impls (module::function) | Cites | Tests | Ref | Defects | Tier |
|-----|--------------------------|-------|-------|-----|---------|------|
| 730 | `signal_processing/telegraphy.py::analyze_telegraph_line`<br>`signal_processing/telegraphy.py::calc_signal_velocity`<br>`signal_processing/telegraphy.py::signal_velocity`<br>`signal_processing/telegraphy.py::verify_telegraph_line` | 4 | 1 | yes (1) | none | **T3** |
| 731 | `signal_processing/telegraphy.py::analyze_telegraph_line`<br>`signal_processing/telegraphy.py::calc_characteristic_impedance`<br>`signal_processing/telegraphy.py::characteristic_impedance`<br>`signal_processing/telegraphy.py::verify_telegraph_line` | 4 | 1 | yes (1) | none | **T3** |
| 732 | `signal_processing/telegraphy.py::analyze_telegraph_line`<br>`signal_processing/telegraphy.py::attenuation_constant`<br>`signal_processing/telegraphy.py::calc_propagation_constant`<br>`signal_processing/telegraphy.py::verify_telegraph_line` | 4 | 1 | yes (1) | none | **T3** |
| 733 | `signal_processing/telegraphy.py::analyze_telegraph_line`<br>`signal_processing/telegraphy.py::calc_propagation_constant`<br>`signal_processing/telegraphy.py::phase_constant`<br>`signal_processing/telegraphy.py::verify_telegraph_line` | 4 | 1 | yes (1) | none | **T3** |
| 734 | `signal_processing/telegraphy.py::analyze_telegraph_line`<br>`signal_processing/telegraphy.py::calc_signal_delay`<br>`signal_processing/telegraphy.py::delay_per_length`<br>`signal_processing/telegraphy.py::verify_telegraph_line` | 4 | 1 | yes (1) | none | **T3** |
| 735 | `signal_processing/telegraphy.py::analyze_telegraph_line`<br>`signal_processing/telegraphy.py::verify_telegraph_line`<br>`signal_processing/telegraphy.py::voltage_at_distance` | 3 | 1 | yes (1) | none | **T3** |
| 736 | `electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::coil_field_at_center`<br>`electromagnetism/measurements/galvanometers_extended.py::current_from_deflection`<br>`electromagnetism/measurements/galvanometers_extended.py::deflection_from_current`<br>`electromagnetism/measurements/galvanometers_extended.py::tangent_galvanometer` | 5 | 1 | yes (1) | none | **T3** |
| 737 | `electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::coil_field_at_center`<br>`electromagnetism/measurements/galvanometers_extended.py::current_from_deflection`<br>`electromagnetism/measurements/galvanometers_extended.py::deflection_from_current`<br>`electromagnetism/measurements/galvanometers_extended.py::tangent_galvanometer` | 5 | 1 | yes (1) | none | **T3** |
| 738 | `electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::coil_field_at_center`<br>`electromagnetism/measurements/galvanometers_extended.py::tangent_galvanometer` | 3 | 1 | yes (1) | none | **T3** |
| 739 | `electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::current_from_deflection`<br>`electromagnetism/measurements/galvanometers_extended.py::deflection_from_current`<br>`electromagnetism/measurements/galvanometers_extended.py::sine_galvanometer` | 4 | 1 | yes (1) | none | **T3** |
| 740 | `signal_processing/observation_methods.py::calc_elongation_ratio`<br>`signal_processing/observation_methods.py::calc_small_arc_vibration_time`<br>`signal_processing/observation_methods.py::calc_vibration_time_at_amplitude` | 3 | 3 | yes (1) | none | **T3** |
| 741 | `electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::current_from_deflection`<br>`electromagnetism/measurements/galvanometers_extended.py::field_at_center`<br>`electromagnetism/measurements/galvanometers_extended.py::helmholtz_galvanometer` | 4 | 1 | yes (1) | none | **T3** |
| 742 | `electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::current_from_deflection`<br>`electromagnetism/measurements/galvanometers_extended.py::field_at_center`<br>`electromagnetism/measurements/galvanometers_extended.py::helmholtz_galvanometer` | 4 | 1 | yes (1) | none | **T3** |
| 743 | `electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::current_from_deflection`<br>`electromagnetism/measurements/galvanometers_extended.py::field_at_center`<br>`electromagnetism/measurements/galvanometers_extended.py::helmholtz_galvanometer` | 4 | 1 | yes (1) | none | **T3** |
| 744 | `electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::wattmeter` | 2 | 1 | yes (1) | none | **T3** |
| 745 | `signal_processing/observation_methods.py::calc_first_swing_deflection` | 1 | 3 | yes (1) | none | **T3** |
| 746 | `electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::wattmeter` | 2 | 1 | yes (1) | none | **T3** |
| 747 | `electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::electrodynamometer`<br>`electromagnetism/measurements/galvanometers_extended.py::equilibrium_deflection`<br>`electromagnetism/measurements/galvanometers_extended.py::torque` | 4 | 1 | yes (1) | none | **T3** |
| 748 | `electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::electrodynamometer`<br>`electromagnetism/measurements/galvanometers_extended.py::equilibrium_deflection`<br>`electromagnetism/measurements/galvanometers_extended.py::torque` | 4 | 1 | yes (1) | none | **T3** |
| 749 | `electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::electrodynamometer`<br>`electromagnetism/measurements/galvanometers_extended.py::equilibrium_deflection`<br>`electromagnetism/measurements/galvanometers_extended.py::torque` | 4 | 1 | yes (1) | none | **T3** |
| 750 | `signal_processing/observation_methods.py::calc_recoil_charge_product`<br>`signal_processing/observation_methods.py::calc_recoil_coefficient`<br>`signal_processing/observation_methods.py::calc_recoil_damping`<br>`signal_processing/observation_methods.py::calc_recoil_elongations` | 4 | 3 | yes (2) | none | **T3** |
| 751 | `electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::current_weigher` | 2 | 1 | yes (2) | CLOSED D-05 — S1, closed G2-exit: current-weigher EMU | **T3** |

## Chapter IV.XVII — Ch XVII: Coil Comparison (Arts. 752–757)

6 articles · 29 qualifying marked tests · 6/6 with reference-store entries.

| Art | Impls (module::function) | Cites | Tests | Ref | Defects | Tier |
|-----|--------------------------|-------|-------|-----|---------|------|
| 752 | `electromagnetism/coil_comparison/coil_comparison.py::calc_comparison_advantage`<br>`electromagnetism/coil_comparison/coil_comparison.py::calc_standard_coil_g1`<br>`electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::current_weigher`<br>`verification/sympy_verify.py::verify_coil_comparison_modulus` | 5 | 6 | yes (2) | CLOSED D-05 — S1, closed G2-exit: current-weigher EMU | **T3** |
| 753 | `electromagnetism/coil_comparison/coil_comparison.py::deflection_residual`<br>`electromagnetism/coil_comparison/coil_comparison.py::determine_g1_by_null`<br>`electromagnetism/coil_comparison/coil_comparison.py::determine_g1_by_shunt`<br>`electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::current_weigher` | 5 | 3 | yes (3) | CLOSED D-05 — S1, closed G2-exit: current-weigher EMU | **T3** |
| 754 | `electromagnetism/coil_comparison/coil_comparison.py::axis_field_series`<br>`electromagnetism/coil_comparison/coil_comparison.py::calc_g3_correction`<br>`electromagnetism/coil_comparison/coil_comparison.py::determine_small_coil_moment`<br>`electromagnetism/measurements/galvanometers_extended.py::analyze_galvanometers`<br>`electromagnetism/measurements/galvanometers_extended.py::current_weigher` | 5 | 4 | yes (2) | CLOSED D-05 — S1, closed G2-exit: current-weigher EMU<br>S3-4 carried (O(u^3) truncation is Maxwell's own series; bounded against exact all-orders field; non-blocking) | **T3** |
| 755 | `electromagnetism/coil_comparison/coil_comparison.py::compare_mutual_by_null`<br>`electromagnetism/coil_comparison/coil_comparison.py::full_null_residual`<br>`electromagnetism/coil_comparison/coil_comparison.py::integral_induction_current`<br>`electromagnetism/coil_comparison/coil_comparison.py::standard_pair_mutual_inductance`<br>`verification/sympy_verify.py::verify_coil_comparison_modulus`<br>`verification/sympy_verify.py::verify_dM_dd_dipole_relation`<br>`verification/sympy_verify.py::verify_mutual_inductance_far_limit`<br>`verification/sympy_verify.py::verify_mutual_inductance_neumann_symmetry` | 8 | 11 | yes (4) | none | **T3** |
| 756 | `electromagnetism/coil_comparison/coil_comparison.py::self_induction_from_mutual`<br>`electromagnetism/coil_comparison/coil_comparison.py::self_induction_from_mutual_with_w`<br>`electromagnetism/coil_comparison/coil_comparison.py::steady_balance_residual`<br>`verification/sympy_verify.py::verify_dM_dd_dipole_relation`<br>`verification/sympy_verify.py::verify_mutual_inductance_far_limit` | 5 | 3 | yes (3) | none | **T3** |
| 757 | `electromagnetism/coil_comparison/coil_comparison.py::compare_self_inductions`<br>`electromagnetism/coil_comparison/coil_comparison.py::self_induction_ratio_from_bridge` | 2 | 2 | yes (1) | none | **T3** |

## Chapter IV.XVIII — Ch XVIII: Resistance Unit (Arts. 758–767)

10 articles · 47 qualifying marked tests · 10/10 with reference-store entries.

| Art | Impls (module::function) | Cites | Tests | Ref | Defects | Tier |
|-----|--------------------------|-------|-------|-----|---------|------|
| 758 | `calibration/absolute_resistance.py::analyze_absolute_resistance`<br>`calibration/absolute_resistance.py::calc_absolute_resistance_recoil`<br>`calibration/absolute_resistance.py::recoil_method`<br>`calibration/absolute_resistance.py::verify_absolute_resistance`<br>`verification/sympy_verify.py::verify_wheatstone_balance` | 5 | 6 | yes (3) | none | **T3** |
| 759 | `calibration/absolute_resistance.py::analyze_absolute_resistance`<br>`calibration/absolute_resistance.py::calc_absolute_resistance_lenz`<br>`calibration/absolute_resistance.py::lenz_method`<br>`calibration/absolute_resistance.py::verify_absolute_resistance`<br>`verification/sympy_verify.py::verify_capacitor_energy`<br>`verification/sympy_verify.py::verify_rc_discharge_ode`<br>`verification/sympy_verify.py::verify_rc_time_constant` | 7 | 10 | yes (1) | none | **T3** |
| 760 | `calibration/absolute_resistance.py::analyze_absolute_resistance`<br>`calibration/absolute_resistance.py::calc_absolute_resistance_lenz`<br>`calibration/absolute_resistance.py::lenz_method`<br>`calibration/absolute_resistance.py::verify_absolute_resistance`<br>`verification/sympy_verify.py::verify_ballistic_throw_charge` | 5 | 5 | yes (1) | none | **T3** |
| 761 | `calibration/absolute_resistance.py::analyze_absolute_resistance`<br>`calibration/absolute_resistance.py::calc_absolute_resistance_rotating_coil`<br>`calibration/absolute_resistance.py::rotating_coil_method`<br>`calibration/absolute_resistance.py::verify_absolute_resistance`<br>`verification/sympy_verify.py::verify_recoil_method_structure` | 5 | 6 | yes (1) | none | **T3** |
| 762 | `calibration/absolute_resistance.py::analyze_absolute_resistance`<br>`calibration/absolute_resistance.py::calc_absolute_resistance_joule`<br>`calibration/absolute_resistance.py::energy_dissipation_method`<br>`calibration/absolute_resistance.py::verify_absolute_resistance` | 4 | 5 | yes (3) | none | **T3** |
| 763 | `calibration/absolute_resistance.py::analyze_absolute_resistance`<br>`calibration/absolute_resistance.py::calc_temperature_corrected_resistance`<br>`calibration/absolute_resistance.py::resistance_at_temperature`<br>`calibration/absolute_resistance.py::verify_absolute_resistance`<br>`verification/sympy_verify.py::verify_resistance_emu_velocity_dimension` | 5 | 6 | yes (2) | none | **T3** |
| 764 | `calibration/absolute_resistance.py::analyze_absolute_resistance`<br>`calibration/absolute_resistance.py::calc_solenoid_self_inductance`<br>`calibration/absolute_resistance.py::self_inductance`<br>`calibration/absolute_resistance.py::verify_absolute_resistance` | 4 | 3 | yes (1) | none | **T3** |
| 765 | `calibration/absolute_resistance.py::calc_absolute_resistance_capacitor_discharge` | 1 | 2 | yes (1) | none | **T3** |
| 766 | `calibration/absolute_resistance.py::calc_recoil_damping_correction` | 1 | 2 | yes (1) | none | **T3** |
| 767 | `calibration/absolute_resistance.py::analyze_absolute_resistance`<br>`calibration/absolute_resistance.py::verify_absolute_resistance` | 2 | 2 | yes (2) | none | **T3** |

## Chapter IV.XIX — Ch XIX: ESU vs EMU (Arts. 768–780)

13 articles · 37 qualifying marked tests · 13/13 with reference-store entries.

| Art | Impls (module::function) | Cites | Tests | Ref | Defects | Tier |
|-----|--------------------------|-------|-------|-----|---------|------|
| 768 | `experiments/ratio_v/theory.py::historical_v_anchor`<br>`experiments/ratio_v/theory.py::motivate_ratio_investigation` | 2 | 1 | yes (1) | none | **T3** |
| 769 | `experiments/ratio_v/theory.py::calculate_ratio`<br>`experiments/ratio_v/theory.py::derive_unit_ratio_dimension`<br>`experiments/ratio_v/theory.py::prove_ratio_is_velocity`<br>`experiments/ratio_v/theory.py::verify_equals_c` | 4 | 4 | yes (1) | none | **T3** |
| 770 | `experiments/ratio_v/theory.py::calc_convection_current`<br>`experiments/ratio_v/theory.py::v_from_convection_field` | 2 | 1 | yes (1) | none | **T3** |
| 771 | `core/units/dimensions.py::calc_unit_ratio`<br>`core/units/dimensions.py::convert_emu_to_esu`<br>`core/units/dimensions.py::convert_esu_to_emu`<br>`core/units/dimensions.py::get_practical_unit_conversions`<br>`core/units/dimensions.py::verify_speed_of_light_relationship`<br>`experiments/ratio_v/condensers.py::calculate_v`<br>`experiments/ratio_v/condensers.py::capacity_parallel`<br>`experiments/ratio_v/condensers.py::capacity_series`<br>`experiments/ratio_v/condensers.py::convert_capacity`<br>`experiments/ratio_v/condensers.py::deviation_from_c`<br>`experiments/ratio_v/condensers.py::method_weber_kohlrausch`<br>`experiments/ratio_v/condensers.py::sphere_capacity_esu` | 12 | 3 | yes (1) | none | **T3** |
| 772 | `core/units/dimensions.py::calc_unit_ratio`<br>`core/units/dimensions.py::convert_emu_to_esu`<br>`core/units/dimensions.py::convert_esu_to_emu`<br>`core/units/dimensions.py::get_practical_unit_conversions`<br>`core/units/dimensions.py::verify_speed_of_light_relationship`<br>`experiments/ratio_v/condensers.py::convert_capacity`<br>`experiments/ratio_v/condensers.py::method_thomson_electrometer`<br>`verification/sympy_verify.py::verify_esu_emu_charge_ratio_c` | 8 | 5 | yes (1) | none | **T3** |
| 773 | `core/units/dimensions.py::calc_unit_ratio`<br>`core/units/dimensions.py::get_practical_unit_conversions`<br>`core/units/dimensions.py::verify_speed_of_light_relationship`<br>`experiments/ratio_v/combined.py::method_maxwell_combined`<br>`experiments/ratio_v/condensers.py::convert_capacity`<br>`verification/sympy_verify.py::verify_esu_emu_resistance_ratio_c2` | 6 | 6 | yes (1) | none | **T3** |
| 774 | `experiments/ratio_v/condensers.py::method_jenkin`<br>`verification/sympy_verify.py::verify_capacitance_esu_length_dimension` | 2 | 5 | yes (1) | none | **T3** |
| 775 | `experiments/ratio_v/combined.py::method_intermittent_current`<br>`experiments/ratio_v/theory.py::historical_v_anchor` | 2 | 2 | yes (1) | none | **T3** |
| 776 | `experiments/ratio_v/combined.py::method_condenser_wippe` | 1 | 2 | yes (1) | none | **T3** |
| 777 | `experiments/ratio_v/combined.py::apply_rapid_action_correction`<br>`experiments/ratio_v/combined.py::rapid_action_charge_fraction` | 2 | 2 | yes (1) | CLOSED D-03 — S1, closed G2-exit: Art 777 correction | **T3** |
| 778 | `experiments/ratio_v/combined.py::compare_capacity_inductance` | 1 | 2 | yes (1) | none | **T3** |
| 779 | `experiments/ratio_v/combined.py::combine_coil_condenser` | 1 | 2 | yes (1) | none | **T3** |
| 780 | `experiments/ratio_v/theory.py::compare_resistance_systems` | 1 | 2 | yes (1) | none | **T3** |

## Chapter IV.XX — Ch XX: EM Theory of Light (Arts. 781–805)

25 articles · 61 qualifying marked tests · 25/25 with reference-store entries.

| Art | Impls (module::function) | Cites | Tests | Ref | Defects | Tier |
|-----|--------------------------|-------|-------|-----|---------|------|
| 781 | `core/units/dimensions.py::verify_speed_of_light_relationship`<br>`electromagnetism/waves/wave_equation.py::calc_wave_impedance`<br>`electromagnetism/waves/wave_equation.py::derive_wave_equation`<br>`electromagnetism/waves/wave_equation.py::from_frequency`<br>`electromagnetism/waves/wave_equation.py::impedance`<br>`electromagnetism/waves/wave_equation.py::verify_wave_equation`<br>`electromagnetism/waves/wave_equation.py::wave_parameters`<br>`optics/wave_equation.py::from_E_k_omega` | 8 | 1 | yes (1) | none | **T3** |
| 782 | `electromagnetism/waves/wave_equation.py::calc_wave_impedance`<br>`electromagnetism/waves/wave_equation.py::from_frequency`<br>`electromagnetism/waves/wave_equation.py::impedance`<br>`electromagnetism/waves/wave_equation.py::verify_wave_equation`<br>`optics/wave_equation.py::from_E_k_omega` | 5 | 1 | yes (1) | none | **T3** |
| 783 | `electromagnetism/waves/wave_equation.py::calc_wave_equation_3d`<br>`electromagnetism/waves/wave_equation.py::plane_wave`<br>`electromagnetism/waves/wave_equation.py::verify_wave_equation`<br>`optics/wave_equation.py::derive_wave_equation`<br>`optics/wave_equation.py::derive_wave_equation_from_maxwell`<br>`optics/wave_equation.py::from_E_k_omega`<br>`optics/wave_equation.py::from_parameters`<br>`optics/wave_equation.py::verify_light_is_em_wave`<br>`optics/wave_equation.py::verify_speed_equals_c`<br>`verification/sympy_verify.py::verify_medium_wave_velocity` | 10 | 5 | yes (1) | none | **T3** |
| 784 | `electromagnetism/waves/wave_equation.py::calc_wave_equation_3d`<br>`electromagnetism/waves/wave_equation.py::plane_wave`<br>`electromagnetism/waves/wave_equation.py::verify_wave_equation`<br>`optics/wave_equation.py::calc_wave_speed`<br>`optics/wave_equation.py::from_E_k_omega`<br>`optics/wave_equation.py::from_parameters`<br>`optics/wave_equation.py::verify_light_is_em_wave`<br>`optics/wave_equation.py::verify_speed_equals_c`<br>`optics/wave_equation.py::wave_speed_calc` | 9 | 2 | yes (1) | none | **T3** |
| 785 | `electromagnetism/waves/wave_equation.py::calc_wave_speed`<br>`electromagnetism/waves/wave_equation.py::verify_wave_equation`<br>`electromagnetism/waves/wave_equation.py::wave_speed`<br>`optics/wave_equation.py::analyze`<br>`optics/wave_equation.py::analyze_wave`<br>`optics/wave_equation.py::calc_plane_wave_E`<br>`optics/wave_equation.py::create_plane_wave`<br>`optics/wave_equation.py::evaluate`<br>`optics/wave_equation.py::from_E_k_omega`<br>`optics/wave_equation.py::from_parameters`<br>`verification/sympy_verify.py::verify_plane_wave_E_cB`<br>`verification/sympy_verify.py::verify_wave_transversality` | 14 | 7 | yes (2) | none | **T3** |
| 786 | `electromagnetism/waves/plane_wave.py::analyze`<br>`electromagnetism/waves/plane_wave.py::fields`<br>`electromagnetism/waves/plane_wave.py::fields_at`<br>`electromagnetism/waves/plane_wave.py::linearly_polarized`<br>`optics/velocity.py::E_B_ratio`<br>`optics/velocity.py::analyze_wave_velocity`<br>`optics/velocity.py::calc_E_B_ratio`<br>`optics/velocity.py::calc_permittivity_from_refractive_index`<br>`optics/velocity.py::calc_refractive_index`<br>`optics/velocity.py::calc_wave_velocity`<br>`optics/velocity.py::calc_wavelength_in_medium`<br>`optics/velocity.py::refractive_index`<br>`optics/velocity.py::velocity`<br>`optics/velocity.py::verify_maxwell_velocity`<br>`optics/velocity.py::wavelength`<br>`optics/wave_equation.py::analyze`<br>`optics/wave_equation.py::analyze_wave`<br>`optics/wave_equation.py::calc_plane_wave_B_from_E`<br>`optics/wave_equation.py::create_plane_wave`<br>`optics/wave_equation.py::from_E_k_omega`<br>`optics/wave_equation.py::verify_transversality`<br>`optics/wave_equation.py::verify_transverse` | 22 | 2 | yes (1) | none | **T3** |
| 787 | `electromagnetism/waves/plane_wave.py::analyze`<br>`electromagnetism/waves/plane_wave.py::linearly_polarized`<br>`electromagnetism/waves/plane_wave.py::verify_transversality`<br>`electromagnetism/waves/plane_wave.py::verify_transverse`<br>`optics/velocity.py::E_B_ratio`<br>`optics/velocity.py::analyze_wave_velocity`<br>`optics/velocity.py::calc_E_B_ratio`<br>`optics/velocity.py::calc_wave_number`<br>`optics/velocity.py::calc_wave_velocity`<br>`optics/velocity.py::velocity`<br>`optics/velocity.py::verify_maxwell_velocity`<br>`optics/velocity.py::wave_number`<br>`optics/wave_equation.py::analyze`<br>`optics/wave_equation.py::analyze_wave`<br>`optics/wave_equation.py::calc_plane_wave_B_from_E`<br>`optics/wave_equation.py::create_plane_wave`<br>`optics/wave_equation.py::from_E_k_omega`<br>`verification/sympy_verify.py::verify_dispersion_relation`<br>`verification/sympy_verify.py::verify_plane_wave_dalembert`<br>`verification/sympy_verify.py::verify_wave_equation_1d` | 20 | 8 | yes (1) | none | **T3** |
| 788 | `electromagnetism/waves/plane_wave.py::analyze`<br>`electromagnetism/waves/plane_wave.py::calc_EB_relationship`<br>`electromagnetism/waves/plane_wave.py::circularly_polarized`<br>`electromagnetism/waves/plane_wave.py::verify_EB`<br>`optics/constants.py::analyze_optical_constants`<br>`optics/constants.py::calc_dielectric_from_refractive`<br>`optics/constants.py::calc_refractive_from_dielectric`<br>`optics/constants.py::calc_refractive_index_from_EM`<br>`optics/constants.py::classify_spectral_region`<br>`optics/constants.py::dielectric_from_refractive`<br>`optics/constants.py::get_optical_constants`<br>`optics/constants.py::refractive_from_dielectric`<br>`optics/constants.py::specific_inductive_capacity`<br>`optics/constants.py::verify_optical_constants`<br>`optics/constants.py::wave_velocity`<br>`optics/wave_equation.py::analyze`<br>`optics/wave_equation.py::analyze_wave`<br>`optics/wave_equation.py::calc_poynting_vector`<br>`optics/wave_equation.py::calc_wave_intensity`<br>`optics/wave_equation.py::intensity`<br>`optics/wave_equation.py::poynting_vector`<br>`verification/sympy_verify.py::verify_plane_wave_poynting` | 24 | 5 | yes (1) | none | **T3** |
| 789 | `electromagnetism/waves/plane_wave.py::analyze`<br>`electromagnetism/waves/plane_wave.py::calc_poynting_vector`<br>`electromagnetism/waves/plane_wave.py::circularly_polarized`<br>`electromagnetism/waves/plane_wave.py::energy_flux`<br>`optics/constants.py::analyze_optical_constants`<br>`optics/constants.py::calc_dispersion`<br>`optics/constants.py::calc_optical_path_difference`<br>`optics/constants.py::calc_refractive_index_from_EM`<br>`optics/constants.py::classify_spectral_region`<br>`optics/constants.py::optical_path_length`<br>`optics/constants.py::verify_optical_constants`<br>`optics/wave_equation.py::analyze`<br>`optics/wave_equation.py::analyze_wave`<br>`optics/wave_equation.py::calc_energy_density`<br>`optics/wave_equation.py::calc_wave_intensity`<br>`optics/wave_equation.py::energy_density`<br>`optics/wave_equation.py::intensity` | 19 | 1 | yes (1) | none | **T3** |
| 790 | `electromagnetism/waves/plane_wave.py::analyze`<br>`electromagnetism/waves/plane_wave.py::calc_poynting_vector`<br>`electromagnetism/waves/plane_wave.py::energy_flux`<br>`optics/constants.py::analyze_optical_constants`<br>`optics/constants.py::calc_frequency_from_wavelength`<br>`optics/constants.py::calc_wavelength_from_frequency`<br>`optics/constants.py::classify_spectral_region`<br>`optics/constants.py::verify_optical_constants`<br>`optics/constants.py::wavelength_in_material`<br>`optics/plane_waves.py::E_field`<br>`optics/plane_waves.py::verify_transverse_condition`<br>`optics/plane_waves.py::verify_wave_equation`<br>`optics/wave_equation.py::analyze`<br>`optics/wave_equation.py::analyze_wave`<br>`optics/wave_equation.py::calc_wavelength` | 15 | 1 | yes (1) | none | **T3** |
| 791 | `electromagnetism/waves/polarization.py::analyze`<br>`electromagnetism/waves/polarization.py::analyze_polarization`<br>`electromagnetism/waves/polarization.py::linear`<br>`electromagnetism/waves/polarization.py::polarization_type`<br>`optics/plane_waves.py::B_field`<br>`optics/plane_waves.py::calc_B_from_E`<br>`optics/radiation_pressure.py::analyze_radiation_pressure`<br>`optics/radiation_pressure.py::calc_energy_density_from_intensity`<br>`optics/radiation_pressure.py::calc_pressure_from_intensity`<br>`optics/radiation_pressure.py::calc_radiation_force`<br>`optics/radiation_pressure.py::calc_radiation_momentum`<br>`optics/radiation_pressure.py::calc_radiation_pressure_from_E`<br>`optics/radiation_pressure.py::pressure_absorption`<br>`optics/radiation_pressure.py::verify_radiation_pressure`<br>`vis/em_wave_propagation.py::calc_em_wave`<br>`vis/em_wave_propagation.py::plot_em_wave_propagation`<br>`vis/em_wave_propagation.py::plot_wave_snapshot_3d` | 17 | 2 | yes (2) | none | **T3** |
| 792 | `electromagnetism/waves/polarization.py::analyze`<br>`electromagnetism/waves/polarization.py::analyze_polarization`<br>`electromagnetism/waves/polarization.py::circular`<br>`electromagnetism/waves/polarization.py::handedness`<br>`optics/plane_waves.py::calc_poynting_vector`<br>`optics/radiation_pressure.py::analyze_radiation_pressure`<br>`optics/radiation_pressure.py::calc_radiation_pressure`<br>`optics/radiation_pressure.py::calc_radiation_pressure_reflection`<br>`optics/radiation_pressure.py::pressure_reflection`<br>`optics/radiation_pressure.py::verify_radiation_pressure` | 10 | 2 | yes (1) | none | **T3** |
| 793 | `electromagnetism/waves/polarization.py::analyze`<br>`electromagnetism/waves/polarization.py::analyze_polarization`<br>`electromagnetism/waves/polarization.py::elliptical`<br>`electromagnetism/waves/polarization.py::handedness`<br>`optics/radiation_pressure.py::analyze_radiation_pressure`<br>`optics/radiation_pressure.py::calc_radiation_pressure_oblique`<br>`optics/radiation_pressure.py::verify_radiation_pressure` | 7 | 2 | yes (1) | none | **T3** |
| 794 | `electromagnetism/waves/polarization.py::Jones`<br>`electromagnetism/waves/polarization.py::Stokes`<br>`electromagnetism/waves/polarization.py::analyze`<br>`electromagnetism/waves/polarization.py::analyze_polarization`<br>`electromagnetism/waves/polarization.py::calc_Stokes_parameters`<br>`electromagnetism/waves/polarization.py::decompose`<br>`electromagnetism/waves/polarization.py::decompose_polarization`<br>`electromagnetism/waves/polarization.py::ellipse`<br>`electromagnetism/waves/polarization.py::ellipse_parameters`<br>`optics/crystals.py::calc_refraction_angle`<br>`optics/radiation_pressure.py::analyze_radiation_pressure`<br>`optics/radiation_pressure.py::calc_radiation_force`<br>`optics/radiation_pressure.py::calc_radiation_momentum`<br>`optics/radiation_pressure.py::calc_radiation_pressure_from_E`<br>`optics/radiation_pressure.py::force_on_area`<br>`optics/radiation_pressure.py::verify_radiation_pressure` | 16 | 3 | yes (1) | none | **T3** |
| 795 | `electromagnetism/waves/polarization.py::Jones_linear_polarizer`<br>`electromagnetism/waves/polarization.py::Jones_wave_plate`<br>`electromagnetism/waves/polarization.py::analyze`<br>`electromagnetism/waves/polarization.py::analyze_polarization`<br>`electromagnetism/waves/polarization.py::decompose`<br>`electromagnetism/waves/polarization.py::decompose_polarization`<br>`electromagnetism/waves/polarization.py::transform`<br>`electromagnetism/waves/polarization.py::transform_polarization`<br>`optics/metals.py::analyze_metallic_reflection`<br>`optics/metals.py::calc_fresnel_reflection_metal`<br>`optics/metals.py::get_metal_constants`<br>`optics/metals.py::reflection_perpendicular`<br>`optics/metals.py::verify_metallic_reflection` | 13 | 1 | yes (1) | none | **T3** |
| 796 | `optics/metals.py::analyze_metallic_reflection`<br>`optics/metals.py::calc_fresnel_reflection_metal`<br>`optics/metals.py::reflection_parallel`<br>`optics/metals.py::verify_metallic_reflection` | 4 | 1 | yes (1) | none | **T3** |
| 797 | `optics/metals.py::analyze_metallic_reflection`<br>`optics/metals.py::calc_metal_reflectance_normal`<br>`optics/metals.py::calc_metal_reflectivity`<br>`optics/metals.py::reflectance`<br>`optics/metals.py::reflectivity`<br>`optics/metals.py::verify_metallic_reflection` | 6 | 1 | yes (1) | none | **T3** |
| 798 | `optics/metals.py::analyze_metallic_reflection`<br>`optics/metals.py::calc_skin_depth`<br>`optics/metals.py::calc_skin_depth_from_kappa`<br>`optics/metals.py::check_transparency`<br>`optics/metals.py::skin_depth`<br>`optics/metals.py::verify_metallic_reflection` | 7 | 2 | yes (1) | none | **T3** |
| 799 | `optics/metals.py::absorption_coefficient`<br>`optics/metals.py::analyze_metallic_reflection`<br>`optics/metals.py::calc_absorption_coefficient`<br>`optics/metals.py::calc_absorption_coefficient_from_kappa`<br>`optics/metals.py::verify_metallic_reflection` | 5 | 1 | yes (1) | none | **T3** |
| 800 | `optics/metals.py::analyze_metallic_reflection`<br>`optics/metals.py::normal_reflectance`<br>`optics/metals.py::verify_metallic_reflection` | 3 | 2 | yes (1) | none | **T3** |
| 801 | `optics/diffusion.py::calc_diffusion_time`<br>`optics/diffusion.py::skin_depth_60hz`<br>`optics/plane_waves.py::analyze_plane_wave_polarization`<br>`optics/plane_waves.py::calc_polarized_wave_intensity`<br>`optics/plane_waves.py::circular_polarization`<br>`optics/plane_waves.py::elliptical_polarization`<br>`optics/plane_waves.py::linear_polarization`<br>`optics/plane_waves.py::polarization_type`<br>`optics/plane_waves.py::verify_polarization_relations` | 9 | 2 | yes (1) | CLOSED D-01 — S1, closed G2-exit: diffusion 4pi/c^2 | **T3** |
| 802 | `optics/diffusion.py::calc_diffusion_length`<br>`optics/plane_waves.py::analyze_plane_wave_polarization`<br>`optics/plane_waves.py::calc_polarization_ellipse`<br>`optics/plane_waves.py::electric_field`<br>`optics/plane_waves.py::magnetic_field`<br>`optics/plane_waves.py::verify_polarization_relations` | 6 | 2 | yes (1) | CLOSED D-01 — S1, closed G2-exit: diffusion 4pi/c^2 | **T3** |
| 803 | `optics/diffusion.py::verify_diffusion_equation`<br>`optics/plane_waves.py::analyze_plane_wave_polarization`<br>`optics/plane_waves.py::calc_fringe_visibility`<br>`optics/plane_waves.py::calc_wave_interference`<br>`optics/plane_waves.py::stokes_parameters`<br>`optics/plane_waves.py::verify_polarization_relations` | 6 | 2 | yes (4) | CLOSED D-01 — S1, closed G2-exit: diffusion 4pi/c^2 | **T3** |
| 804 | `optics/crystals.py::analyze_crystal_optics`<br>`optics/crystals.py::calc_birefringence`<br>`optics/crystals.py::calc_retardation_waves`<br>`optics/crystals.py::calc_velocity_difference`<br>`optics/crystals.py::effective_index_at_angle`<br>`optics/crystals.py::get_crystal_constants`<br>`optics/crystals.py::half_wave_thickness`<br>`optics/crystals.py::ordinary_velocity`<br>`optics/crystals.py::path_difference`<br>`optics/crystals.py::quarter_wave_thickness`<br>`optics/crystals.py::retardation`<br>`optics/crystals.py::verify_crystal_optics`<br>`optics/diffusion.py::calc_field_at_depth`<br>`optics/diffusion.py::field_at_depth` | 14 | 2 | yes (1) | none | **T3** |
| 805 | `optics/crystals.py::analyze_crystal_optics`<br>`optics/crystals.py::calc_birefringence`<br>`optics/crystals.py::calc_effective_index`<br>`optics/crystals.py::calc_velocity_difference`<br>`optics/crystals.py::effective_index_at_angle`<br>`optics/crystals.py::extraordinary_velocity`<br>`optics/crystals.py::retardation`<br>`optics/crystals.py::verify_crystal_optics` | 8 | 3 | yes (1) | none | **T3** |

## Chapter IV.XXI — Ch XXI: Magnetic Action on Light (Arts. 806–831)

26 articles · 43 qualifying marked tests · 26/26 with reference-store entries.

| Art | Impls (module::function) | Cites | Tests | Ref | Defects | Tier |
|-----|--------------------------|-------|-------|-----|---------|------|
| 806 | `magneto_optics/rotation.py::measure_rotation_by_analyser` | 1 | 1 | yes (1) | none | **T3** |
| 807 | `magneto_optics/rotation.py::B_field_from_rotation`<br>`magneto_optics/rotation.py::rotation_angle` | 2 | 1 | yes (1) | none | **T3** |
| 808 | `magneto_optics/rotation.py::establish_rotation_laws`<br>`verification/sympy_verify.py::verify_circular_birefringence_rotation` | 2 | 4 | yes (1) | none | **T3** |
| 809 | `magneto_optics/rotation.py::apply_verdet_negative_rotation`<br>`magneto_optics/rotation.py::compare_materials`<br>`magneto_optics/rotation.py::get_verdet`<br>`magneto_optics/rotation.py::get_verdet_rad` | 4 | 2 | yes (1) | none | **T3** |
| 810 | `magneto_optics/rotation.py::model_natural_rotation`<br>`magneto_optics/rotation.py::round_trip_rotation` | 2 | 1 | yes (1) | none | **T3** |
| 811 | `magneto_optics/circular_polarization.py::perform_kinematic_analysis` | 1 | 2 | yes (1) | none | **T3** |
| 812 | `magneto_optics/circular_polarization.py::calc_circular_velocity_split` | 1 | 3 | yes (2) | CLOSED D-04 — S1, closed G2-exit: Delta n identity | **T3** |
| 813 | `magneto_optics/circular_polarization.py::electric_field`<br>`magneto_optics/circular_polarization.py::velocity`<br>`verification/sympy_verify.py::verify_verdet_path_linearity` | 3 | 4 | yes (1) | none | **T3** |
| 814 | `magneto_optics/circular_polarization.py::calc_natural_velocity_split` | 1 | 1 | yes (1) | none | **T3** |
| 815 | `magneto_optics/circular_polarization.py::calc_magnetic_velocity_split` | 1 | 1 | yes (1) | none | **T3** |
| 816 | `magneto_optics/circular_polarization.py::define_light_vector` | 1 | 1 | yes (1) | none | **T3** |
| 817 | `magneto_optics/circular_polarization.py::derive_circular_kinematics` | 1 | 1 | yes (1) | none | **T3** |
| 818 | `magneto_optics/energy_analysis.py::calc_medium_energy` | 1 | 1 | yes (1) | none | **T3** |
| 819 | `magneto_optics/energy_analysis.py::calc_propagation_quadratic`<br>`magneto_optics/energy_analysis.py::derive_propagation_condition`<br>`magneto_optics/energy_analysis.py::quadratic_coupling_coefficient` | 3 | 2 | yes (5) | none | **T3** |
| 820 | `magneto_optics/energy_analysis.py::prove_real_rotation_required` | 1 | 1 | yes (1) | none | **T3** |
| 821 | `magneto_optics/energy_analysis.py::summarize_magneto_optic_results` | 1 | 1 | yes (1) | none | **T3** |
| 822 | `vis/molecular_vortices.py::calc_magnetic_field_from_vortices`<br>`vis/molecular_vortices.py::calc_vortex_lattice`<br>`vis/molecular_vortices.py::plot_molecular_vortices`<br>`vis/molecular_vortices.py::plot_vortex_3d_surface`<br>`vortex_engine/vortex_lattice.py::add_vortex`<br>`vortex_engine/vortex_lattice.py::angular_momentum`<br>`vortex_engine/vortex_lattice.py::kinetic_energy`<br>`vortex_engine/vortex_lattice.py::magnetic_field_equivalent`<br>`vortex_engine/vortex_lattice.py::total_angular_momentum`<br>`vortex_engine/vortex_lattice.py::total_kinetic_energy`<br>`vortex_engine/vortex_lattice.py::total_magnetic_field`<br>`vortex_engine/vortex_lattice.py::verify_vortex_gear_condition` | 12 | 1 | yes (2) | none | **T3** |
| 823 | `vortex_engine/helmholtz_law.py::apply_helmholtz_vortex_law`<br>`vortex_engine/helmholtz_law.py::calc_vortex_stretching` | 2 | 1 | yes (1) | none | **T3** |
| 824 | `vortex_engine/kinetic_energy.py::calc_disturbed_vortex_energy`<br>`vortex_engine/kinetic_energy.py::calc_vortex_angular_velocity` | 2 | 2 | yes (3) | CLOSED D-22 — S2, closed Wave 7: vortex energy dimensional homogeneity | **T3** |
| 825 | `vortex_engine/kinetic_energy.py::express_vortex_current_velocity` | 1 | 2 | yes (3) | CLOSED D-22 — S2, closed Wave 7: vortex energy dimensional homogeneity | **T3** |
| 826 | `vortex_engine/kinetic_energy.py::calc_plane_wave_vortex_energy` | 1 | 3 | yes (4) | CLOSED D-22 — S2, closed Wave 7: vortex energy dimensional homogeneity | **T3** |
| 827 | `vortex_engine/equations_of_motion.py::derive_vortex_equations_of_motion` | 1 | 1 | yes (1) | none | **T3** |
| 828 | `vortex_engine/equations_of_motion.py::calc_vortex_circular_velocity`<br>`vortex_engine/equations_of_motion.py::solve_plane_wave` | 2 | 2 | yes (1) | none | **T3** |
| 829 | `vortex_engine/magnetic_rotation.py::derive_magnetic_rotation`<br>`vortex_engine/magnetic_rotation.py::rotation_coefficient` | 2 | 1 | yes (1) | none | **T3** |
| 830 | `vortex_engine/magnetic_rotation.py::compare_verdet_data`<br>`vortex_engine/magnetic_rotation.py::verdet_inverse_square_analysis` | 2 | 2 | yes (5) | none | **T3** |
| 831 | `vortex_engine/vortex_lattice.py::append_mechanical_theory_notes` | 1 | 1 | yes (1) | none | **T3** |

## Chapter IV.XXII — Ch XXII: Molecular Currents (Arts. 832–845)

14 articles · 30 qualifying marked tests · 14/14 with reference-store entries.

| Art | Impls (module::function) | Cites | Tests | Ref | Defects | Tier |
|-----|--------------------------|-------|-------|-----|---------|------|
| 832 | `molecular/amperes_theory.py::analyze_amperes_theory`<br>`molecular/amperes_theory.py::calc_molecular_moment`<br>`molecular/amperes_theory.py::magnetic_moment`<br>`molecular/amperes_theory.py::verify_amperes_theory` | 4 | 1 | yes (1) | none | **T3** |
| 833 | `molecular/amperes_theory.py::analyze_amperes_theory`<br>`molecular/amperes_theory.py::calc_molecular_field`<br>`molecular/amperes_theory.py::magnetic_field_at`<br>`molecular/amperes_theory.py::verify_amperes_theory`<br>`verification/sympy_verify.py::verify_dipole_vector_potential`<br>`verification/sympy_verify.py::verify_div_B_dipole_zero`<br>`verification/sympy_verify.py::verify_loop_far_field_dipole_limit` | 7 | 8 | yes (1) | none | **T3** |
| 834 | `molecular/amperes_theory.py::vector_potential_at` | 1 | 1 | yes (1) | none | **T3** |
| 835 | `molecular/amperes_theory.py::analyze_amperes_theory`<br>`molecular/amperes_theory.py::magnetization`<br>`molecular/amperes_theory.py::verify_amperes_theory` | 3 | 1 | yes (1) | none | **T3** |
| 836 | `molecular/amperes_theory.py::analyze_amperes_theory`<br>`molecular/amperes_theory.py::susceptibility` | 2 | 2 | yes (1) | none | **T3** |
| 837 | `molecular/amperes_theory.py::bound_current_density` | 1 | 2 | yes (1) | none | **T3** |
| 838 | `molecular/amperes_theory.py::total_magnetic_moment` | 1 | 2 | yes (1) | none | **T3** |
| 839 | `molecular/amperes_theory.py::bound_surface_current` | 1 | 1 | yes (1) | none | **T3** |
| 840 | `molecular/amperes_theory.py::sphere_center_field_rings`<br>`molecular/amperes_theory.py::sphere_interior_field` | 2 | 2 | yes (1) | none | **T3** |
| 841 | `molecular/webers_theory.py::analyze_webers_theory`<br>`molecular/webers_theory.py::calc_weber_force`<br>`molecular/webers_theory.py::force`<br>`molecular/webers_theory.py::verify_webers_theory`<br>`molecular/webers_theory.py::weber_force` | 6 | 2 | yes (1) | CLOSED D-12 — S2, closed Wave 7: Weber convention — register scope 841-845, G3 section 5 cluster 846-853 | **T3** |
| 842 | `molecular/webers_theory.py::analyze_webers_theory`<br>`molecular/webers_theory.py::calc_weber_potential`<br>`molecular/webers_theory.py::potential_energy`<br>`molecular/webers_theory.py::verify_webers_theory`<br>`molecular/webers_theory.py::weber_potential` | 5 | 1 | yes (1) | CLOSED D-12 — S2, closed Wave 7: Weber convention — register scope 841-845, G3 section 5 cluster 846-853 | **T3** |
| 843 | `molecular/competing_theories.py::analyze_webers_theory`<br>`molecular/webers_theory.py::analyze_webers_theory`<br>`molecular/webers_theory.py::coulomb_limit`<br>`molecular/webers_theory.py::verify_webers_theory` | 4 | 1 | yes (1) | CLOSED D-12 — S2, closed Wave 7: Weber convention — register scope 841-845, G3 section 5 cluster 846-853 | **T3** |
| 844 | `molecular/webers_theory.py::analyze_webers_theory`<br>`molecular/webers_theory.py::velocity_correction_factor`<br>`molecular/webers_theory.py::verify_webers_theory` | 3 | 1 | yes (1) | CLOSED D-12 — S2, closed Wave 7: Weber convention — register scope 841-845, G3 section 5 cluster 846-853 | **T3** |
| 845 | `molecular/webers_theory.py::acceleration_correction_factor` | 1 | 5 | yes (2) | CLOSED D-12 — S2, closed Wave 7: Weber convention — register scope 841-845, G3 section 5 cluster 846-853 | **T3** |

## Chapter IV.XXIII — Ch XXIII: Action at Distance (Arts. 846–866)

21 articles · 45 qualifying marked tests · 21/21 with reference-store entries.

| Art | Impls (module::function) | Cites | Tests | Ref | Defects | Tier |
|-----|--------------------------|-------|-------|-----|---------|------|
| 846 | `molecular/competing_theories.py::analyze_webers_theory`<br>`molecular/webers_theory.py::ampere_wire_force_recovery`<br>`molecular/webers_theory.py::force_between_current_elements`<br>`verification/sympy_verify.py::verify_weber_coulomb_limit`<br>`verification/sympy_verify.py::verify_weber_velocity_structure` | 5 | 8 | yes (1) | CLOSED D-12 — S2, closed Wave 7: Weber convention — register scope 841-845, G3 section 5 cluster 846-853 | **T3** |
| 847 | `molecular/webers_theory.py::induced_emf`<br>`verification/sympy_verify.py::verify_weber_coulomb_limit`<br>`verification/sympy_verify.py::verify_weber_potential_energy_identity` | 3 | 4 | yes (3) | CLOSED D-12 — S2, closed Wave 7: Weber convention — register scope 841-845, G3 section 5 cluster 846-853 | **T3** |
| 848 | `molecular/webers_theory.py::weber_constant` | 1 | 1 | yes (1) | CLOSED D-12 — S2, closed Wave 7: Weber convention — register scope 841-845, G3 section 5 cluster 846-853 | **T3** |
| 849 | `molecular/competing_theories.py::analyze_webers_theory`<br>`molecular/webers_theory.py::critical_velocity` | 2 | 1 | yes (1) | CLOSED D-12 — S2, closed Wave 7: Weber convention — register scope 841-845, G3 section 5 cluster 846-853 | **T3** |
| 850 | `molecular/competing_theories.py::analyze_webers_theory`<br>`molecular/webers_theory.py::weber_energy_conservation_residual` | 2 | 1 | yes (1) | CLOSED D-12 — S2, closed Wave 7: Weber convention — register scope 841-845, G3 section 5 cluster 846-853 | **T3** |
| 851 | `molecular/neumanns_theory.py::calc_neumann_potential`<br>`molecular/neumanns_theory.py::vector_potential_at`<br>`verification/sympy_verify.py::verify_ampere_force_symmetry`<br>`verification/sympy_verify.py::verify_ampere_parallel_attraction` | 4 | 7 | yes (1) | CLOSED D-12 — S2, closed Wave 7: Weber convention — register scope 841-845, G3 section 5 cluster 846-853 | **T3** |
| 852 | `molecular/neumanns_theory.py::analyze_neumanns_theory`<br>`molecular/neumanns_theory.py::magnetic_flux_through`<br>`molecular/neumanns_theory.py::mutual_potential_energy`<br>`molecular/neumanns_theory.py::potential_energy`<br>`molecular/neumanns_theory.py::verify_neumanns_theory`<br>`verification/sympy_verify.py::verify_ampere_newton_third_law` | 6 | 4 | yes (1) | CLOSED D-12 — S2, closed Wave 7: Weber convention — register scope 841-845, G3 section 5 cluster 846-853 | **T3** |
| 853 | `molecular/competing_theories.py::analyze_neumanns_theory`<br>`molecular/neumanns_theory.py::analyze_neumanns_theory`<br>`molecular/neumanns_theory.py::calc_mutual_inductance_neumann`<br>`molecular/neumanns_theory.py::maxwell_mutual_inductance_closed_form`<br>`molecular/neumanns_theory.py::mutual_inductance`<br>`molecular/neumanns_theory.py::mutual_inductance_loops`<br>`molecular/neumanns_theory.py::neumann_mutual_inductance`<br>`molecular/neumanns_theory.py::verify_neumanns_theory` | 8 | 1 | yes (1) | CLOSED D-12 — S2, closed Wave 7: Weber convention — register scope 841-845, G3 section 5 cluster 846-853 | **T3** |
| 854 | `molecular/neumanns_theory.py::analyze_neumanns_theory`<br>`molecular/neumanns_theory.py::circular_loop_inductance`<br>`molecular/neumanns_theory.py::self_inductance`<br>`molecular/neumanns_theory.py::verify_neumanns_theory` | 4 | 1 | yes (1) | none | **T3** |
| 855 | `molecular/neumanns_theory.py::induced_emf` | 1 | 1 | yes (1) | none | **T3** |
| 856 | `molecular/competing_theories.py::analyze_neumanns_theory`<br>`molecular/neumanns_theory.py::neumann_reciprocity_residual`<br>`molecular/neumanns_theory.py::verify_neumanns_theory` | 3 | 1 | yes (1) | none | **T3** |
| 857 | `molecular/competing_theories.py::analyze_neumanns_theory`<br>`molecular/neumanns_theory.py::neumann_far_field_residual`<br>`theories/failure_modes.py::analyze_action_at_distance_failure`<br>`theories/failure_modes.py::analyze_failure_modes`<br>`theories/failure_modes.py::analyze_weber_failure`<br>`theories/failure_modes.py::verify_maxwell_supremacy` | 6 | 1 | yes (1) | none | **T3** |
| 858 | `molecular/neumanns_theory.py::motional_emf_coaxial`<br>`theories/failure_modes.py::analyze_action_at_distance_failure`<br>`theories/failure_modes.py::analyze_failure_modes`<br>`theories/failure_modes.py::analyze_mechanical_ether_failure`<br>`theories/failure_modes.py::analyze_weber_failure`<br>`theories/failure_modes.py::verify_maxwell_supremacy` | 6 | 1 | yes (1) | none | **T3** |
| 859 | `molecular/competing_theories.py::analyze_amperes_theory`<br>`molecular/competing_theories.py::characteristics`<br>`molecular/competing_theories.py::compare_electromagnetic_theories`<br>`molecular/competing_theories.py::compare_theories`<br>`molecular/competing_theories.py::diamagnetic_response`<br>`theories/failure_modes.py::analyze_failure_modes`<br>`theories/failure_modes.py::analyze_mechanical_ether_failure`<br>`theories/failure_modes.py::verify_maxwell_supremacy` | 8 | 1 | yes (1) | none | **T3** |
| 860 | `molecular/competing_theories.py::analyze_amperes_theory`<br>`molecular/competing_theories.py::compare_electromagnetic_theories`<br>`molecular/competing_theories.py::compare_theories`<br>`molecular/competing_theories.py::computed_residuals`<br>`molecular/competing_theories.py::diamagnetic_response` | 5 | 2 | yes (1) | none | **T3** |
| 861 | `molecular/competing_theories.py::analyze_theory_differences`<br>`molecular/competing_theories.py::compare_theories`<br>`molecular/competing_theories.py::computed_checks` | 3 | 2 | yes (1) | none | **T3** |
| 862 | `molecular/competing_theories.py::analyze_theory_differences`<br>`molecular/competing_theories.py::compare_all`<br>`molecular/competing_theories.py::compare_theories`<br>`molecular/competing_theories.py::synthesize_theory_comparison` | 5 | 1 | yes (1) | none | **T3** |
| 863 | `molecular/competing_theories.py::verify_theory_consistency` | 1 | 1 | yes (1) | none | **T3** |
| 864 | `molecular/competing_theories.py::verify_theory_consistency` | 1 | 1 | yes (1) | none | **T3** |
| 865 | `molecular/competing_theories.py::maxwell_advantages`<br>`philosophy/medium_check.py::analyze_theory_completeness`<br>`philosophy/medium_check.py::calc_reflection_coefficient`<br>`philosophy/medium_check.py::calc_wave_properties`<br>`philosophy/medium_check.py::verify_maxwell_relation`<br>`philosophy/medium_check.py::verify_wave_speed` | 6 | 2 | yes (1) | none | **T3** |
| 866 | `molecular/competing_theories.py::maxwell_advantages`<br>`molecular/competing_theories.py::synthesize_theory_comparison`<br>`philosophy/medium_check.py::analyze_theory_completeness`<br>`philosophy/medium_check.py::calc_reflection_coefficient`<br>`philosophy/medium_check.py::calc_wave_properties`<br>`philosophy/medium_check.py::verify_maxwell_relation`<br>`philosophy/medium_check.py::verify_wave_speed` | 7 | 3 | yes (1) | none | **T3** |

---

## Appendix A — Qualifying tests per article (verbatim from `article_evidence_report.json`)

Artifact `generated: 2026-08-22T15:15:23.968575+00:00` (authoritative full-suite emission; source: `article_evidence_report.json`; the G3-era revision is G3 gate review §1.2/§7.3). 501 marked-test entries over 200 articles; 481 distinct test nodeids (tests may qualify several articles when marked for each).

### IV.XII Ch XII: Current-Sheets

- **Art. 667** (8):
  - `tests/test_articles_boundary_conditions_667_669.py::test_art667_normal_B_continuity_hand_decomposition`
  - `tests/test_articles_boundary_conditions_667_669.py::test_art667_normal_B_pillbox_limit_first_order_convergence`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_surface_current_jump]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_normal_B_continuous]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_surface_current_jump]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_normal_B_continuous]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_surface_current_jump]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_normal_B_continuous]`
- **Art. 668** (5):
  - `tests/test_articles_boundary_conditions_667_669.py::test_art668_normal_D_jump_gauss_sheet_oracle`
  - `tests/test_articles_boundary_conditions_667_669.py::test_art669_charged_dielectric_interface_full_solution`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_solenoid_inductance_structure]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_solenoid_inductance_structure]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_solenoid_inductance_structure]`
- **Art. 669** (5):
  - `tests/test_articles_boundary_conditions_667_669.py::test_art669_charged_dielectric_interface_full_solution`
  - `tests/test_articles_boundary_conditions_667_669.py::test_art669_uncharged_dielectric_refraction_identity`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_sheet_potential_discontinuity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_sheet_potential_discontinuity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_sheet_potential_discontinuity]`
- **Art. 670** (4):
  - `tests/test_articles_math_spine_691_706.py::test_on_axis_formula_center_and_dipole`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_cylindrical_sheet_field]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_cylindrical_sheet_field]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_cylindrical_sheet_field]`
- **Art. 671** (4):
  - `tests/test_articles_math_spine_691_706.py::test_on_axis_formula_center_and_dipole`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_sheet_toroidal_zero_exterior]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_sheet_toroidal_zero_exterior]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_sheet_toroidal_zero_exterior]`
- **Art. 672** (1):
  - `tests/test_articles_math_spine_691_706.py::test_on_axis_formula_center_and_dipole`
- **Art. 673** (2):
  - `tests/test_articles_math_spine_691_706.py::test_off_axis_matches_biot_savart_oracle`
  - `tests/test_articles_math_spine_691_706.py::test_off_axis_reduces_to_on_axis_continuously`
- **Art. 674** (2):
  - `tests/test_articles_math_spine_691_706.py::test_off_axis_matches_biot_savart_oracle`
  - `tests/test_articles_math_spine_691_706.py::test_off_axis_far_field_dipole_pattern`

### IV.XIII Ch XIII: Parallel Currents

- **Art. 675** (15):
  - `tests/test_articles_math_spine_691_706.py::test_off_axis_matches_biot_savart_oracle`
  - `tests/test_articles_math_spine_691_706.py::test_off_axis_far_field_dipole_pattern`
  - `tests/test_articles_math_spine_691_706.py::test_spherical_harmonics_citation_split_keeps_part4_winning`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_legendre_value_at_one]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_legendre_parity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_legendre_recurrence]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_legendre_orthogonality]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_legendre_value_at_one]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_legendre_parity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_legendre_recurrence]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_legendre_orthogonality]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_legendre_value_at_one]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_legendre_parity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_legendre_recurrence]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_legendre_orthogonality]`
- **Art. 676** (10):
  - `tests/test_articles_math_spine_691_706.py::test_helmholtz_superposition_and_uniformity`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_legendre_generating_function]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_addition_theorem_p1]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_Y00_normalization]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_legendre_generating_function]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_addition_theorem_p1]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_Y00_normalization]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_legendre_generating_function]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_addition_theorem_p1]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_Y00_normalization]`
- **Art. 677** (7):
  - `tests/test_articles_math_spine_691_706.py::test_helmholtz_superposition_and_uniformity`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_zonal_harmonic_laplace]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_legendre_differential_equation]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_zonal_harmonic_laplace]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_legendre_differential_equation]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_zonal_harmonic_laplace]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_legendre_differential_equation]`
- **Art. 678** (1):
  - `tests/test_articles_math_spine_691_706.py::test_coaxial_pair_antisymmetry`
- **Art. 679** (1):
  - `tests/test_articles_math_spine_691_706.py::test_coaxial_pair_antisymmetry`
- **Art. 680** (2):
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art680_solid_cylinder_exterior_vs_volume_biot_savart`
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art680_helmholtz_center_coefficient`
- **Art. 681** (1):
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art681_inside_field_surface_invariant_and_continuity`
- **Art. 682** (2):
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art682_hollow_cylinder_cavity_zero_and_wall_oracle`
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art682_helmholtz_uniformity_profile_vs_quadrature`
- **Art. 683** (2):
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art683_hollow_exterior_and_ampere_wall_values`
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art683_helmholtz_axial_uniformity_fourth_order`
- **Art. 684** (1):
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art684_wire_inductance_from_flux_and_energy_quadrature`
- **Art. 685** (2):
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art685_spherical_harmonic_vs_closed_forms`
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art685_wire_inductance_radius_independence`
- **Art. 686** (2):
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art686_real_harmonics_vs_closed_forms`
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art686_vector_potential_matches_ampere_field_integral`
- **Art. 687** (1):
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art687_intensity_closed_form_and_phi_independence`
- **Art. 688** (1):
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art688_normalization_theorem_and_code_band`
- **Art. 689** (2):
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art689_associated_legendre_closed_forms_and_goldens`
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art689_associated_legendre_orthogonality_integrals`
- **Art. 690** (1):
  - `tests/test_articles_cylinders_harmonics_680_690.py::test_art690_zonal_multipole_expansion_closed_forms`
- **Art. 691** (1):
  - `tests/test_articles_math_spine_691_706.py::test_self_gmd_circle_exact`
- **Art. 692** (2):
  - `tests/test_articles_math_spine_691_706.py::test_self_gmd_rectangle_square_and_thin_strip`
  - `tests/test_articles_math_spine_691_706.py::test_gmd_coaxial_rings_closed_form`
- **Art. 693** (4):
  - `tests/test_articles_math_spine_691_706.py::test_gmd_parallel_wires_disjoint_sections_exact`
  - `tests/test_articles_math_spine_691_706.py::test_gmd_parallel_wires_overlap_vs_tensor_quadrature`
  - `tests/test_articles_math_spine_691_706.py::test_gmd_coaxial_rings_closed_form`
  - `tests/test_articles_math_spine_691_706.py::test_inductance_gmd_correction_self_consistent`

### IV.XIV Ch XIV: Circular Currents

- **Art. 694** (14):
  - `tests/test_articles_c1_meta_closure.py::test_art694_vector_potential_series_vs_independent_oracles`
  - `tests/test_articles_c1_meta_closure.py::test_art694_vector_potential_citation_and_domain_guard`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_circular_current_center_field]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_loop_axial_field_integral]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_loop_far_field_dipole_limit]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_mutual_inductance_neumann_symmetry]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_circular_current_center_field]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_loop_axial_field_integral]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_loop_far_field_dipole_limit]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_mutual_inductance_neumann_symmetry]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_circular_current_center_field]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_loop_axial_field_integral]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_loop_far_field_dipole_limit]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_mutual_inductance_neumann_symmetry]`
- **Art. 695** (2):
  - `tests/test_articles_c1_meta_closure.py::test_art695_magnetic_shell_potential_vs_independent_oracles`
  - `tests/test_articles_c1_meta_closure.py::test_art695_shell_potential_citation_and_domain_guard`
- **Art. 696** (9):
  - `tests/test_articles_math_spine_691_706.py::test_K_E_golden_values_tight`
  - `tests/test_articles_math_spine_691_706.py::test_K_E_cross_check_carlson_grid`
  - `tests/test_articles_math_spine_691_706.py::test_legendre_relation`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_elliptic_K_AGM_identity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_vector_potential_loop_structure]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_elliptic_K_AGM_identity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_vector_potential_loop_structure]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_elliptic_K_AGM_identity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_vector_potential_loop_structure]`
- **Art. 697** (3):
  - `tests/test_articles_math_spine_691_706.py::test_K_E_golden_values_tight`
  - `tests/test_articles_math_spine_691_706.py::test_K_E_cross_check_carlson_grid`
  - `tests/test_articles_math_spine_691_706.py::test_legendre_relation`
- **Art. 698** (1):
  - `tests/test_articles_math_spine_691_706.py::test_third_kind_reduces_to_first_kind`
- **Art. 699** (1):
  - `tests/test_articles_math_spine_691_706.py::test_jacobian_identities`
- **Art. 700** (1):
  - `tests/test_articles_math_spine_691_706.py::test_landen_identity_full_loop`
- **Art. 701** (1):
  - `tests/test_articles_math_spine_691_706.py::test_complementary_modulus_and_parameter_convention`
- **Art. 702** (3):
  - `tests/test_articles_math_spine_691_706.py::test_negative_parameter_imaginary_modulus_transform`
  - `tests/test_articles_math_spine_691_706.py::test_complementary_modulus_and_parameter_convention`
  - `tests/test_defects_s1.py::test_regression_D02_art702_near_axis_psi_and_curl`
- **Art. 703** (10):
  - `tests/test_articles_math_spine_691_706.py::test_verify_and_analyze_elliptic_relations`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_elliptic_legendre_relation]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_elliptic_K_small_k_series]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_elliptic_E_small_k_series]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_elliptic_legendre_relation]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_elliptic_K_small_k_series]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_elliptic_E_small_k_series]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_elliptic_legendre_relation]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_elliptic_K_small_k_series]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_elliptic_E_small_k_series]`
- **Art. 704** (7):
  - `tests/test_articles_math_spine_691_706.py::test_verify_and_analyze_elliptic_relations`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_elliptic_K_derivative_identity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_elliptic_E_derivative_identity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_elliptic_K_derivative_identity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_elliptic_E_derivative_identity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_elliptic_K_derivative_identity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_elliptic_E_derivative_identity]`
- **Art. 705** (4):
  - `tests/test_articles_math_spine_691_706.py::test_verify_and_analyze_elliptic_relations`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_elliptic_landen_descent]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_elliptic_landen_descent]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_elliptic_landen_descent]`
- **Art. 706** (6):
  - `tests/test_article_706_coil_design.py::test_art_706_gauss_optimal_coil_golden`
  - `tests/test_article_706_coil_design.py::test_art_706_optimal_winding_proportion_golden`
  - `tests/test_article_706_coil_design.py::test_art_706_disk_self_gmd_golden`
  - `tests/test_article_706_coil_design.py::test_art_706_fd_stationarity_of_inductance`
  - `tests/test_article_706_coil_design.py::test_art_706_max_inductance_design_and_identity`
  - `tests/test_article_706_coil_design.py::test_art_706_square_channel_matches_quadrature_and_printed_ratio`

### IV.XV Ch XV: Electromagnetic Instruments

- **Art. 707** (2):
  - `tests/test_articles_instruments_707_729.py::test_art_707_coil_constant_golden_and_limit`
  - `tests/test_articles_instruments_707_729.py::test_art_707_709_center_field_matches_biot_savart_oracle`
- **Art. 708** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_708_design_standard_coil_self_consistent`
- **Art. 709** (3):
  - `tests/test_articles_instruments_707_729.py::test_art_707_709_center_field_matches_biot_savart_oracle`
  - `tests/test_articles_instruments_707_729.py::test_art_709_tangent_law_zero_torsion`
  - `tests/test_articles_instruments_707_729.py::test_art_709_torsion_balance_residual_and_independent_root`
- **Art. 710** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_710_tangent_sine_equivalence_at_zero`
- **Art. 711** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_711_single_coil_tangent_measurement`
- **Art. 712** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_712_gaugain_offset_and_field_oracle`
- **Art. 713** (4):
  - `tests/test_articles_instruments_707_729.py::test_art_713_helmholtz_center_field_golden_and_oracle`
  - `tests/test_articles_instruments_707_729.py::test_art_713_helmholtz_uniformity_condition_spacing_equals_radius`
  - `tests/test_articles_instruments_707_729.py::test_art_713_helmholtz_field_flatness_over_center_region`
  - `tests/test_articles_instruments_707_729.py::test_art_713_helmholtz_far_field_dipole_limit`
- **Art. 714** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_714_four_coil_constant_is_sum_and_oracle`
- **Art. 715** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_715_three_coil_constant_is_sum`
- **Art. 716** (2):
  - `tests/test_articles_instruments_707_729.py::test_art_716_wire_dimensions_match_prescribed_resistance`
  - `tests/test_articles_instruments_707_729.py::test_art_716_gaussian_agreement_galvanometers_vs_circular_coils`
- **Art. 717** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_717_sensitive_design_uses_full_wire_and_reports_merit`
- **Art. 718** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_718_greatest_sensibility_at_matched_resistance`
- **Art. 719** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_719_wire_thickness_grows_with_radius`
- **Art. 720** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_720_uniform_wire_sensitivity_is_g_over_h`
- **Art. 721** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_721_suspended_coil_moment_and_torque_balance`
- **Art. 722** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_722_thomson_sensitive_coil_sensitivity_and_round_trip`
- **Art. 723** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_723_determine_magnetic_force_from_deflection`
- **Art. 724** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_724_combined_instrument_two_readings_agree`
- **Art. 725** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_725_weber_dynamometer_square_law_and_equilibrium`
- **Art. 726** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_726_joule_weigher_force_and_balancing_mass`
- **Art. 727** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_727_solenoid_suction_golden_and_work_identity`
- **Art. 728** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_728_uniform_field_max_torque_matches_coil_torque`
- **Art. 729** (1):
  - `tests/test_articles_instruments_707_729.py::test_art_729_torsion_dynamometer_angle_and_inversion`

### IV.XVI Ch XVI: Observations

- **Art. 730** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_730_signal_velocity`
- **Art. 731** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_731_characteristic_impedance`
- **Art. 732** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_732_attenuation_constant`
- **Art. 733** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_733_phase_constant`
- **Art. 734** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_734_signal_delay`
- **Art. 735** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_735_voltage_at_distance`
- **Art. 736** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_736_tangent_current_from_deflection`
- **Art. 737** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_737_tangent_deflection_from_current`
- **Art. 738** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_738_coil_field_at_center`
- **Art. 739** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_739_sine_galvanometer`
- **Art. 740** (3):
  - `tests/test_articles_ch16_wave7_740_745_750.py::test_art_740_vibration_time_amplitude_law`
  - `tests/test_articles_ch16_wave7_740_745_750.py::test_art_740_small_arc_time_golden_and_sum_oracle`
  - `tests/test_articles_ch16_wave7_740_745_750.py::test_art_740_limits_zero_kappa_and_undamped`
- **Art. 741** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_741_helmholtz_field_and_uniformity`
- **Art. 742** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_742_helmholtz_factor`
- **Art. 743** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_743_helmholtz_current_from_deflection`
- **Art. 744** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_744_wattmeter_true_power`
- **Art. 745** (3):
  - `tests/test_articles_ch16_wave7_740_745_750.py::test_art_745_first_swing_golden`
  - `tests/test_articles_ch16_wave7_740_745_750.py::test_art_745_damped_oscillator_rk4_oracle`
  - `tests/test_articles_ch16_wave7_740_745_750.py::test_art_745_undamped_limit_is_midpoint`
- **Art. 746** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_746_wattmeter_reactive_and_phase`
- **Art. 747** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_747_electrodynamometer_torque`
- **Art. 748** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_748_equilibrium_deflection`
- **Art. 749** (1):
  - `tests/test_articles_ch16_observations_730_750.py::test_art_749_series_square_law_and_product_invariance`
- **Art. 750** (3):
  - `tests/test_articles_ch16_wave7_740_745_750.py::test_art_750_elongation_chain_rational_goldens`
  - `tests/test_articles_ch16_wave7_740_745_750.py::test_art_750_recoil_coefficient_forms_and_limits`
  - `tests/test_articles_ch16_wave7_740_745_750.py::test_art_750_kicked_oscillator_ode_oracle`
- **Art. 751** (1):
  - `tests/test_defects_s1.py::test_regression_D05_art751_force_equals_I2_dMdx`

### IV.XVII Ch XVII: Coil Comparison

- **Art. 752** (6):
  - `tests/test_articles_coil_comparison_752_757.py::test_752_standard_coil_g1_matches_independent_section_quadrature`
  - `tests/test_articles_coil_comparison_752_757.py::test_752_thin_ring_limit_matches_biot_savart_line_integral`
  - `tests/test_articles_coil_comparison_752_757.py::test_752_comparison_advantage_computed_from_errors`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_coil_comparison_modulus]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_coil_comparison_modulus]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_coil_comparison_modulus]`
- **Art. 753** (3):
  - `tests/test_articles_coil_comparison_752_757.py::test_753_null_determination_golden`
  - `tests/test_articles_coil_comparison_752_757.py::test_753_shunt_determination_golden`
  - `tests/test_articles_coil_comparison_752_757.py::test_753_deflection_equation_residual`
- **Art. 754** (4):
  - `tests/test_articles_coil_comparison_752_757.py::test_754_axis_series_reproduces_exact_loop_field`
  - `tests/test_articles_coil_comparison_752_757.py::test_754_g3_of_thin_loop_golden`
  - `tests/test_articles_coil_comparison_752_757.py::test_754_moment_inversion_is_exact_for_truncated_series`
  - `tests/test_articles_coil_comparison_752_757.py::test_754_end_to_end_null_against_exact_loop_field`
- **Art. 755** (11):
  - `tests/test_articles_coil_comparison_752_757.py::test_755_standard_pair_matches_independent_neumann_quadrature`
  - `tests/test_articles_coil_comparison_752_757.py::test_755_asymmetric_pair_and_reciprocity`
  - `tests/test_articles_coil_comparison_752_757.py::test_755_far_field_dipole_asymptotic`
  - `tests/test_articles_coil_comparison_752_757.py::test_755_integral_induction_current_golden_and_null`
  - `tests/test_articles_coil_comparison_752_757.py::test_755_null_ratio_and_full_null_condition`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_mutual_inductance_far_limit]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_dM_dd_dipole_relation]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_mutual_inductance_far_limit]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_dM_dd_dipole_relation]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_mutual_inductance_far_limit]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_dM_dd_dipole_relation]`
- **Art. 756** (3):
  - `tests/test_articles_coil_comparison_752_757.py::test_756_self_induction_from_mutual_golden`
  - `tests/test_articles_coil_comparison_752_757.py::test_756_third_method_with_shunt_w_golden`
  - `tests/test_articles_coil_comparison_752_757.py::test_756_steady_balance_residual`
- **Art. 757** (2):
  - `tests/test_articles_coil_comparison_752_757.py::test_757_double_balance_residuals_and_ratio`
  - `tests/test_articles_coil_comparison_752_757.py::test_757_off_balance_residuals_hand_computed`

### IV.XVIII Ch XVIII: Resistance Unit

- **Art. 758** (6):
  - `tests/test_articles_absolute_resistance_758_764.py::test_art758_recoil_resistance_hand_golden`
  - `tests/test_articles_absolute_resistance_758_764.py::test_art758_recoil_velocity_dimension_exponents_measured`
  - `tests/test_articles_absolute_resistance_758_764.py::test_art758_recoil_identity_with_art766_decrement`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_wheatstone_balance]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_wheatstone_balance]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_wheatstone_balance]`
- **Art. 759** (10):
  - `tests/test_lint_remediation_last200.py::TestAbsoluteResistanceIndependence::test_no_heat_reports_cross_check_not_performed`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_rc_discharge_ode]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_rc_time_constant]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_capacitor_energy]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_rc_discharge_ode]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_rc_time_constant]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_capacitor_energy]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_rc_discharge_ode]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_rc_time_constant]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_capacitor_energy]`
- **Art. 760** (5):
  - `tests/test_articles_absolute_resistance_758_764.py::test_art760_lenz_resistance_hand_golden`
  - `tests/test_articles_absolute_resistance_758_764.py::test_art760_lenz_resistance_from_independent_faraday_emf`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_ballistic_throw_charge]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_ballistic_throw_charge]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_ballistic_throw_charge]`
- **Art. 761** (6):
  - `tests/test_articles_absolute_resistance_758_764.py::test_art761_rotating_coil_resistance_hand_golden`
  - `tests/test_articles_absolute_resistance_758_764.py::test_art761_rotating_coil_matches_independent_faraday_oracle`
  - `tests/test_articles_absolute_resistance_758_764.py::test_art761_rotating_coil_known_series_subtraction`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_recoil_method_structure]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_recoil_method_structure]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_recoil_method_structure]`
- **Art. 762** (5):
  - `tests/test_lint_remediation_last200.py::TestAbsoluteResistanceIndependence::test_verify_absolute_resistance_independence`
  - `tests/test_lint_remediation_last200.py::TestAbsoluteResistanceIndependence::test_calorimetric_cross_check_consistent_heat_passes`
  - `tests/test_lint_remediation_last200.py::TestAbsoluteResistanceIndependence::test_known_bad_heat_flips_verdict`
  - `tests/test_lint_remediation_last200.py::TestAnalyzeAbsoluteResistanceHonesty::test_no_heat_average_uses_existing_determinations_only`
  - `tests/test_lint_remediation_last200.py::TestAnalyzeAbsoluteResistanceHonesty::test_independent_heat_enters_average`
- **Art. 763** (6):
  - `tests/test_articles_absolute_resistance_758_764.py::test_art763_copper_temperature_correction_hand_golden`
  - `tests/test_articles_absolute_resistance_758_764.py::test_art763_german_silver_coil_material_table_golden`
  - `tests/test_articles_absolute_resistance_758_764.py::test_art763_affine_law_identities_hand_derived`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_resistance_emu_velocity_dimension]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_resistance_emu_velocity_dimension]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_resistance_emu_velocity_dimension]`
- **Art. 764** (3):
  - `tests/test_articles_absolute_resistance_758_764.py::test_art764_solenoid_inductance_hand_golden`
  - `tests/test_articles_absolute_resistance_758_764.py::test_art764_oracle_self_check_ring_mutual_limits`
  - `tests/test_articles_absolute_resistance_758_764.py::test_art764_solenoid_inductance_neumann_sheet_oracle`
- **Art. 765** (2):
  - `tests/test_articles_c1_meta_closure.py::test_art765_capacitor_discharge_resistance_vs_ode_oracle`
  - `tests/test_articles_c1_meta_closure.py::test_art765_capacitor_discharge_citation_and_guards`
- **Art. 766** (2):
  - `tests/test_articles_c1_meta_closure.py::test_art766_recoil_damping_correction_vs_oscillator_oracle`
  - `tests/test_articles_c1_meta_closure.py::test_art766_recoil_damping_correction_citation_and_guards`
- **Art. 767** (2):
  - `tests/test_lint_remediation_last200.py::TestVelocityDimensionCheck::test_velocity_dimensions_exponents_computed`
  - `tests/test_lint_remediation_last200.py::TestVelocityDimensionCheck::test_degenerate_measurement_fails_dimension_check`

### IV.XIX Ch XIX: ESU vs EMU

- **Art. 768** (1):
  - `tests/test_articles_ratio_v_768_780.py::test_art_768_motivation_quantitative_anchor`
- **Art. 769** (4):
  - `tests/test_articles_ratio_v_768_780.py::test_art_769_dimensional_derivation_from_force_laws`
  - `tests/test_articles_ratio_v_768_780.py::test_art_769_sympy_symbolic_derivation`
  - `tests/test_articles_ratio_v_768_780.py::test_art_769_unit_ratio_experiment_all_quantities`
  - `tests/test_articles_ratio_v_768_780.py::test_art_769_dimensional_check_v_cm_s`
- **Art. 770** (1):
  - `tests/test_articles_ratio_v_768_780.py::test_art_770_convection_current_geometry_and_field`
- **Art. 771** (3):
  - `tests/test_articles_ratio_v_768_780.py::test_art_771_weber_kohlrausch_reduction`
  - `tests/test_articles_ratio_v_768_780.py::test_art_771_series_parallel_identities_both_systems`
  - `tests/test_articles_ratio_v_768_780.py::test_ch19_v_anchor_maxwell_parameters[art771-weber-kohlrausch]`
- **Art. 772** (5):
  - `tests/test_articles_ratio_v_768_780.py::test_art_772_thomson_emf_ratio`
  - `tests/test_articles_ratio_v_768_780.py::test_ch19_v_anchor_maxwell_parameters[art772-thomson]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_esu_emu_charge_ratio_c]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_esu_emu_charge_ratio_c]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_esu_emu_charge_ratio_c]`
- **Art. 773** (6):
  - `tests/test_articles_ratio_v_768_780.py::test_art_773_maxwell_combined_cross_routes`
  - `tests/test_articles_ratio_v_768_780.py::test_art_773_cross_method_agreement`
  - `tests/test_articles_ratio_v_768_780.py::test_ch19_v_anchor_maxwell_parameters[art773-maxwell-combined]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_esu_emu_resistance_ratio_c2]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_esu_emu_resistance_ratio_c2]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_esu_emu_resistance_ratio_c2]`
- **Art. 774** (5):
  - `tests/test_articles_ratio_v_768_780.py::test_art_774_jenkin_intermittent_discharge`
  - `tests/test_articles_ratio_v_768_780.py::test_ch19_v_anchor_maxwell_parameters[art774-jenkin]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_capacitance_esu_length_dimension]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_capacitance_esu_length_dimension]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_capacitance_esu_length_dimension]`
- **Art. 775** (2):
  - `tests/test_articles_ratio_v_768_780.py::test_art_775_intermittent_current`
  - `tests/test_articles_ratio_v_768_780.py::test_ch19_v_anchor_maxwell_parameters[art775-intermittent-current]`
- **Art. 776** (2):
  - `tests/test_articles_ratio_v_768_780.py::test_art_776_condenser_wippe_balance`
  - `tests/test_articles_ratio_v_768_780.py::test_ch19_v_anchor_maxwell_parameters[art776-condenser-wippe]`
- **Art. 777** (2):
  - `tests/test_articles_ratio_v_768_780.py::test_art_777_rapid_action_correction_contract`
  - `tests/test_defects_s1.py::test_regression_D03_art777_correction_halves_v`
- **Art. 778** (2):
  - `tests/test_articles_ratio_v_768_780.py::test_art_778_lc_resonance_velocity`
  - `tests/test_articles_ratio_v_768_780.py::test_ch19_v_anchor_maxwell_parameters[art778-lc-resonance]`
- **Art. 779** (2):
  - `tests/test_articles_ratio_v_768_780.py::test_art_779_coil_condenser_period`
  - `tests/test_articles_ratio_v_768_780.py::test_ch19_v_anchor_maxwell_parameters[art779-coil-condenser]`
- **Art. 780** (2):
  - `tests/test_articles_ratio_v_768_780.py::test_art_780_resistance_ratio_direction`
  - `tests/test_articles_ratio_v_768_780.py::test_ch19_v_anchor_maxwell_parameters[art780-resistance]`

### IV.XX Ch XX: EM Theory of Light

- **Art. 781** (1):
  - `tests/test_articles_optics_781_805.py::TestWaveEquation781to785::test_781_vacuum_dispersion_relation`
- **Art. 782** (1):
  - `tests/test_articles_optics_781_805.py::TestWaveEquation781to785::test_782_wave_satisfies_maxwell_equations`
- **Art. 783** (5):
  - `tests/test_articles_optics_781_805.py::TestWaveEquation781to785::test_783_vacuum_speed_identity_from_emu_constants`
  - `tests/test_articles_optics_781_805.py::TestWaveEquation781to785::test_783_vacuum_wave_speed_equals_c`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_medium_wave_velocity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_medium_wave_velocity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_medium_wave_velocity]`
- **Art. 784** (2):
  - `tests/test_articles_optics_781_805.py::TestWaveEquation781to785::test_784_medium_wave_speed`
  - `tests/test_articles_optics_781_805.py::TestWaveEquation781to785::test_784_dispersionless_vacuum_and_medium`
- **Art. 785** (7):
  - `tests/test_articles_optics_781_805.py::TestWaveEquation781to785::test_785_plane_wave_fields_golden`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_plane_wave_E_cB]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_wave_transversality]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_plane_wave_E_cB]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_wave_transversality]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_plane_wave_E_cB]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_wave_transversality]`
- **Art. 786** (2):
  - `tests/test_articles_optics_781_805.py::TestPlaneWaveProperties786to790::test_786_transversality_k_dot_E`
  - `tests/test_articles_optics_781_805.py::TestPlaneWaveProperties786to790::test_786_transversality_full_wave`
- **Art. 787** (8):
  - `tests/test_articles_optics_781_805.py::TestPlaneWaveProperties786to790::test_787_E_over_B_equals_c`
  - `tests/test_articles_optics_781_805.py::TestPlaneWaveProperties786to790::test_787_E_B_ratio_in_medium`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_plane_wave_dalembert]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_dispersion_relation]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_plane_wave_dalembert]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_dispersion_relation]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_plane_wave_dalembert]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_dispersion_relation]`
- **Art. 788** (5):
  - `tests/test_articles_optics_781_805.py::TestPlaneWaveProperties786to790::test_788_poynting_vector_golden`
  - `tests/test_articles_optics_781_805.py::TestPlaneWaveProperties786to790::test_788_intensity_golden`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_plane_wave_poynting]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_plane_wave_poynting]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_plane_wave_poynting]`
- **Art. 789** (1):
  - `tests/test_articles_optics_781_805.py::TestPlaneWaveProperties786to790::test_789_energy_density_golden`
- **Art. 790** (1):
  - `tests/test_articles_optics_781_805.py::TestPlaneWaveProperties786to790::test_790_wavelength_frequency_relations`
- **Art. 791** (2):
  - `tests/test_articles_optics_781_805.py::TestPolarization791to795::test_791_linear_polarization_malus`
  - `tests/test_articles_optics_781_805.py::TestRadiationPressure791to794::test_791_radiation_pressure_absorber_golden`
- **Art. 792** (2):
  - `tests/test_articles_optics_781_805.py::TestPolarization791to795::test_792_circular_polarization_stokes`
  - `tests/test_articles_optics_781_805.py::TestRadiationPressure791to794::test_792_radiation_pressure_reflector_golden`
- **Art. 793** (2):
  - `tests/test_articles_optics_781_805.py::TestPolarization791to795::test_793_elliptical_polarization_stokes_identity`
  - `tests/test_articles_optics_781_805.py::TestRadiationPressure791to794::test_793_radiation_pressure_oblique_golden`
- **Art. 794** (3):
  - `tests/test_articles_optics_781_805.py::TestPolarization791to795::test_794_half_wave_plate_flips_polarization`
  - `tests/test_articles_optics_781_805.py::TestPolarization791to795::test_794_snell_refraction_golden`
  - `tests/test_articles_optics_781_805.py::TestRadiationPressure791to794::test_794_radiation_force_and_momentum_golden`
- **Art. 795** (1):
  - `tests/test_articles_optics_781_805.py::TestPolarization791to795::test_795_quarter_wave_plate_makes_circular`
- **Art. 796** (1):
  - `tests/test_articles_optics_781_805.py::TestMetalOptics795to800::test_796_fresnel_normal_incidence_equality`
- **Art. 797** (1):
  - `tests/test_articles_optics_781_805.py::TestMetalOptics795to800::test_797_normal_reflectance_golden`
- **Art. 798** (2):
  - `tests/test_articles_optics_781_805.py::TestMetalOptics795to800::test_798_skin_depth_conductivity_golden`
  - `tests/test_articles_optics_781_805.py::TestMetalOptics795to800::test_798_skin_depth_limit_behavior`
- **Art. 799** (1):
  - `tests/test_articles_optics_781_805.py::TestMetalOptics795to800::test_799_absorption_coefficient_identities`
- **Art. 800** (2):
  - `tests/test_articles_optics_781_805.py::TestMetalOptics795to800::test_800_hagen_rubens_against_fresnel_oracle`
  - `tests/test_articles_optics_781_805.py::TestMetalOptics795to800::test_800_hagen_rubens_limit_behavior`
- **Art. 801** (2):
  - `tests/test_articles_optics_781_805.py::TestPolarizationStates801to803::test_801_polarization_classification`
  - `tests/test_defects_s1.py::test_regression_D01_art801_diffusion_time_copper_and_roundtrip`
- **Art. 802** (2):
  - `tests/test_articles_optics_781_805.py::TestPolarizationStates801to803::test_802_polarization_ellipse_limits`
  - `tests/test_defects_s1.py::test_regression_D01_art801_diffusion_time_copper_and_roundtrip`
- **Art. 803** (2):
  - `tests/test_articles_optics_781_805.py::TestPolarizationStates801to803::test_803_stokes_completeness_identity`
  - `tests/test_articles_optics_781_805.py::TestPolarizationStates801to803::test_803_interference_limits_and_visibility`
- **Art. 804** (2):
  - `tests/test_articles_optics_781_805.py::TestCrystalOptics804to805::test_804_ordinary_extraordinary_velocities`
  - `tests/test_articles_optics_781_805.py::TestCrystalOptics804to805::test_804_wave_plate_thickness_round_trip`
- **Art. 805** (3):
  - `tests/test_articles_optics_781_805.py::TestCrystalOptics804to805::test_805_uniaxial_index_identities`
  - `tests/test_articles_optics_781_805.py::TestCrystalOptics804to805::test_805_fresnel_normal_equation`
  - `tests/test_articles_optics_781_805.py::TestCrystalOptics804to805::test_805_crystal_sign_and_velocity_ordering`

### IV.XXI Ch XXI: Magnetic Action on Light

- **Art. 806** (1):
  - `tests/test_articles_magneto_optics_vortex.py::test_art806_rotation_measured_by_analyser_difference`
- **Art. 807** (1):
  - `tests/test_articles_magneto_optics_vortex.py::test_art807_theta_equals_VBL_and_inversion`
- **Art. 808** (4):
  - `tests/test_articles_magneto_optics_vortex.py::test_art808_rotation_follows_resolved_part_of_force`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_circular_birefringence_rotation]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_circular_birefringence_rotation]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_circular_birefringence_rotation]`
- **Art. 809** (2):
  - `tests/test_articles_magneto_optics_vortex.py::test_art809_ferromagnetic_rotation_is_negative_of_diamagnetic`
  - `tests/test_articles_magneto_optics_vortex.py::test_art809_verdet_table_units_and_ratios`
- **Art. 810** (1):
  - `tests/test_articles_magneto_optics_vortex.py::test_art810_biot_law_and_round_trip_reciprocity`
- **Art. 811** (2):
  - `tests/test_articles_magneto_optics_vortex.py::test_art811_rotation_is_half_phase_difference`
  - `tests/test_articles_magneto_optics_vortex.py::test_art812_index_split_and_closed_loop_with_811`
- **Art. 812** (3):
  - `tests/test_articles_magneto_optics_vortex.py::test_art812_index_split_and_closed_loop_with_811`
  - `tests/test_articles_magneto_optics_vortex.py::test_art815_magnetic_split_consistent_with_art812`
  - `tests/test_defects_s1.py::test_regression_D04_art812_delta_n_identity`
- **Art. 813** (4):
  - `tests/test_articles_magneto_optics_vortex.py::test_art813_circular_ray_constant_magnitude_transverse`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_verdet_path_linearity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_verdet_path_linearity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_verdet_path_linearity]`
- **Art. 814** (1):
  - `tests/test_articles_magneto_optics_vortex.py::test_art814_natural_split_delta_v_formula`
- **Art. 815** (1):
  - `tests/test_articles_magneto_optics_vortex.py::test_art815_magnetic_split_consistent_with_art812`
- **Art. 816** (1):
  - `tests/test_articles_magneto_optics_vortex.py::test_art816_light_vector_is_transverse_projection`
- **Art. 817** (1):
  - `tests/test_articles_magneto_optics_vortex.py::test_art817_kinematics_equations_and_conventions`
- **Art. 818** (1):
  - `tests/test_articles_magneto_optics_vortex.py::test_art818_energy_labels_potential_electric_kinetic_magnetic`
- **Art. 819** (2):
  - `tests/test_articles_magneto_optics_vortex.py::test_art819_quadratic_roots_and_coupling_eq8`
  - `tests/test_articles_magneto_optics_vortex.py::test_art819_medium_propagation_condition_and_split`
- **Art. 820** (1):
  - `tests/test_articles_magneto_optics_vortex.py::test_art820_round_trip_discriminant_detects_real_rotation`
- **Art. 821** (1):
  - `tests/test_articles_magneto_optics_vortex.py::test_art821_summary_is_fully_derived_and_consistent`
- **Art. 822** (1):
  - `tests/test_articles_magneto_optics_vortex.py::test_art822_vortex_energy_momentum_and_gear_condition`
- **Art. 823** (1):
  - `tests/test_articles_magneto_optics_vortex.py::test_art823_helmholtz_variation_and_strength_ratio`
- **Art. 824** (2):
  - `tests/test_articles_magneto_optics_vortex.py::test_art824_angular_velocity_is_half_curl_and_coupling_term`
  - `tests/test_defect_d22_dimensional_consistency.py::test_d22_art824_coupling_term_has_energy_density_dimensions`
- **Art. 825** (2):
  - `tests/test_articles_magneto_optics_vortex.py::test_art825_coupling_in_terms_of_current_and_velocity`
  - `tests/test_defect_d22_dimensional_consistency.py::test_d22_art825_current_velocity_term_has_energy_density_dimensions`
- **Art. 826** (3):
  - `tests/test_articles_magneto_optics_vortex.py::test_art826_plane_wave_energy_reduces_to_art828_eq15`
  - `tests/test_defect_d22_dimensional_consistency.py::test_d22_plane_wave_energy_density_has_energy_density_dimensions`
  - `tests/test_defect_d22_dimensional_consistency.py::test_d22_circular_ray_energy_phase_independent_identity`
- **Art. 827** (1):
  - `tests/test_articles_magneto_optics_vortex.py::test_art827_equation_of_motion_residual_vanishes_at_roots`
- **Art. 828** (2):
  - `tests/test_articles_magneto_optics_vortex.py::test_art826_plane_wave_energy_reduces_to_art828_eq15`
  - `tests/test_articles_magneto_optics_vortex.py::test_art828_circular_velocities_and_vieta_identities`
- **Art. 829** (1):
  - `tests/test_articles_magneto_optics_vortex.py::test_art829_rotation_formula_eq26_and_denominator`
- **Art. 830** (2):
  - `tests/test_articles_magneto_optics_vortex.py::test_art830_verdet_table_golden_and_laws`
  - `tests/test_articles_magneto_optics_vortex.py::test_art830_inverse_square_laws_from_verdet_data`
- **Art. 831** (1):
  - `tests/test_articles_magneto_optics_vortex.py::test_art831_mechanical_theory_summary_computed`

### IV.XXII Ch XXII: Molecular Currents

- **Art. 832** (1):
  - `tests/test_articles_molecular_832_866.py::test_art832_molecular_moment_is_ia_over_c`
- **Art. 833** (8):
  - `tests/test_articles_molecular_832_866.py::test_art833_dipole_field_matches_biot_savart_on_axis`
  - `tests/test_articles_molecular_832_866.py::test_art833_dipole_field_equator`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_div_B_dipole_zero]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_dipole_vector_potential]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_div_B_dipole_zero]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_dipole_vector_potential]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_div_B_dipole_zero]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_dipole_vector_potential]`
- **Art. 834** (1):
  - `tests/test_articles_molecular_832_866.py::test_art834_loop_equals_dipole_off_axis`
- **Art. 835** (1):
  - `tests/test_articles_molecular_832_866.py::test_art835_magnetization_density_golden`
- **Art. 836** (2):
  - `tests/test_articles_molecular_832_866.py::test_art836_curie_law_codata_golden`
  - `tests/test_articles_molecular_832_866.py::test_art836_curie_halving_and_field_independence`
- **Art. 837** (2):
  - `tests/test_articles_molecular_832_866.py::test_art837_uniform_magnetization_has_no_bound_current`
  - `tests/test_articles_molecular_832_866.py::test_art837_bound_current_is_c_curl_M_golden`
- **Art. 838** (2):
  - `tests/test_articles_molecular_832_866.py::test_art838_total_moment_uniform_golden`
  - `tests/test_articles_molecular_832_866.py::test_art838_total_moment_linear_field_golden`
- **Art. 839** (1):
  - `tests/test_articles_molecular_832_866.py::test_art839_surface_current_golden_cross_product`
- **Art. 840** (2):
  - `tests/test_articles_molecular_832_866.py::test_art840_sphere_center_field_rings_golden`
  - `tests/test_articles_molecular_832_866.py::test_art840_sphere_interior_field_biot_savart_golden`
- **Art. 841** (2):
  - `tests/test_articles_molecular_832_866.py::test_art841_weber_static_limit_is_coulomb`
  - `tests/test_articles_molecular_832_866.py::test_art841_acceleration_term_golden`
- **Art. 842** (1):
  - `tests/test_articles_molecular_832_866.py::test_art842_weber_potential_golden`
- **Art. 843** (1):
  - `tests/test_articles_molecular_832_866.py::test_art843_coulomb_limit_residual_is_zero`
- **Art. 844** (1):
  - `tests/test_articles_molecular_832_866.py::test_art844_velocity_factor_golden_at_point_one_c`
- **Art. 845** (5):
  - `tests/test_articles_molecular_832_866.py::test_art845_acceleration_factor_golden`
  - `tests/test_defect_d12_weber_pin.py::test_d12_velocity_squared_coefficient_pin`
  - `tests/test_defect_d12_weber_pin.py::test_d12_acceleration_coefficient_pin`
  - `tests/test_defect_d12_weber_pin.py::test_d12_both_implementation_sites_one_convention`
  - `tests/test_defect_d12_weber_pin.py::test_d12_equivalence_with_weber_1846_c_w_form`

### IV.XXIII Ch XXIII: Action at Distance

- **Art. 846** (8):
  - `tests/test_articles_molecular_832_866.py::test_art846_wire_force_vs_finite_closed_form`
  - `tests/test_articles_molecular_832_866.py::test_art846_antiparallel_currents_repel`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_weber_coulomb_limit]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_weber_velocity_structure]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_weber_coulomb_limit]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_weber_velocity_structure]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_weber_coulomb_limit]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_weber_velocity_structure]`
- **Art. 847** (4):
  - `tests/test_articles_molecular_832_866.py::test_art847_induced_emf_goldens_and_lenz_sign`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_weber_potential_energy_identity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_weber_potential_energy_identity]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_weber_potential_energy_identity]`
- **Art. 848** (1):
  - `tests/test_articles_molecular_832_866.py::test_art848_weber_constant_is_sqrt2_c`
- **Art. 849** (1):
  - `tests/test_articles_molecular_832_866.py::test_art849_critical_velocity_and_force_sign_flip`
- **Art. 850** (1):
  - `tests/test_articles_molecular_832_866.py::test_art850_weber_energy_conservation_residual`
- **Art. 851** (7):
  - `tests/test_articles_molecular_832_866.py::test_art851_vector_potential_axisymmetry_and_far_dipole`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_ampere_force_symmetry]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_ampere_parallel_attraction]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_ampere_force_symmetry]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_ampere_parallel_attraction]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_ampere_force_symmetry]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_ampere_parallel_attraction]`
- **Art. 852** (4):
  - `tests/test_articles_molecular_832_866.py::test_art852_flux_equals_MI`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_verdict_passes[verify_ampere_newton_third_law]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_result_contract[verify_ampere_newton_third_law]`
  - `tests/test_sympy_spine_wave8.py::TestWave8VerifiersPass::test_citation_matches_marker[verify_ampere_newton_third_law]`
- **Art. 853** (1):
  - `tests/test_articles_molecular_832_866.py::test_art853_neumann_quadrature_matches_elliptic_closed_form`
- **Art. 854** (1):
  - `tests/test_articles_molecular_832_866.py::test_art854_self_inductance_golden_formula`
- **Art. 855** (1):
  - `tests/test_articles_molecular_832_866.py::test_art855_induced_emf_neumann_sign_and_golden`
- **Art. 856** (1):
  - `tests/test_articles_molecular_832_866.py::test_art856_reciprocity_with_unequal_discretizations`
- **Art. 857** (1):
  - `tests/test_articles_molecular_832_866.py::test_art857_far_field_dipole_limit`
- **Art. 858** (1):
  - `tests/test_articles_molecular_832_866.py::test_art858_motional_emf_matches_dipole_oracle`
- **Art. 859** (1):
  - `tests/test_articles_molecular_832_866.py::test_art859_compare_theories_structure_and_required_flags`
- **Art. 860** (2):
  - `tests/test_articles_molecular_832_866.py::test_art860_residuals_are_finite_small_and_honest`
  - `tests/test_articles_molecular_832_866.py::test_art860_dipole_residual_independently_zero`
- **Art. 861** (2):
  - `tests/test_articles_molecular_832_866.py::test_art861_checks_are_boolean_and_self_consistent`
  - `tests/test_articles_molecular_832_866.py::test_art861_weber_checks_include_critical_velocity_sign_flip`
- **Art. 862** (1):
  - `tests/test_articles_molecular_832_866.py::test_art862_compare_all_and_synthesis_best_theory`
- **Art. 863** (1):
  - `tests/test_articles_molecular_832_866.py::test_art863_verify_theory_consistency_computed_for_all_theories`
- **Art. 864** (1):
  - `tests/test_articles_molecular_832_866.py::test_art864_differences_and_cross_comparison_computed`
- **Art. 865** (2):
  - `tests/test_articles_molecular_832_866.py::test_art865_wave_speed_and_impedance_goldens`
  - `tests/test_articles_molecular_832_866.py::test_art865_reflection_coefficient_golden`
- **Art. 866** (3):
  - `tests/test_articles_molecular_832_866.py::test_art866_default_dataset_verifies_with_provenance`
  - `tests/test_articles_molecular_832_866.py::test_art866_honesty_wrong_water_datum_flips_the_verdict`
  - `tests/test_articles_molecular_832_866.py::test_art866_wave_speed_check_and_completeness_are_computed`

---

## Summary statistics

### By chapter

| Chapter | Title | Articles | Marked tests | Ref-store articles |
|---------|-------|----------|--------------|--------------------|
| IV.XII | Ch XII: Current-Sheets | 8 | 31 | 8 |
| IV.XIII | Ch XIII: Parallel Currents | 19 | 58 | 19 |
| IV.XIV | Ch XIV: Circular Currents | 13 | 62 | 13 |
| IV.XV | Ch XV: Electromagnetic Instruments | 23 | 30 | 23 |
| IV.XVI | Ch XVI: Observations | 22 | 28 | 22 |
| IV.XVII | Ch XVII: Coil Comparison | 6 | 29 | 6 |
| IV.XVIII | Ch XVIII: Resistance Unit | 10 | 47 | 10 |
| IV.XIX | Ch XIX: ESU vs EMU | 13 | 37 | 13 |
| IV.XX | Ch XX: EM Theory of Light | 25 | 61 | 25 |
| IV.XXI | Ch XXI: Magnetic Action on Light | 26 | 43 | 26 |
| IV.XXII | Ch XXII: Molecular Currents | 14 | 30 | 14 |
| IV.XXIII | Ch XXIII: Action at Distance | 21 | 45 | 21 |
| **Total** | | **200** | **501** | **200** |

### Headline counts

- Articles certified: **200** (all of 667–866; matches `article_evidence_report.json` `articles_covered: 200`, `articles_missing: []`).
- Qualifying article-marked tests: **501** (= `total_marked_tests`).
- Reference-store coverage in scope: **200/200 articles** (254 in-scope values; store-wide 202 article keys / 256 values, incl. out-of-scope Arts 624, 625 (legacy, consumed by `test_lint_remediation_last200.py`; G4-pre audit finding F4); 0 empty provenance fields).
- Ledger citations for the 200 articles: **944** of 3867 total (ledger: 866 articles, 0 zero-citation).
- Suite at certified baseline: **2312 passed, 0 failed, 0 errors, 0 xfailed** (G3 gate review §1.1, reproduced twice by the independent examiner). This is the Wave-7/G3-close historical baseline; Waves 8–9 subsequently added guard/battery tests on top of it. Live suite counts are tracked in `docs/LAST200_STAGE5_AGENT_ORCHESTRATION.md` §7 and were independently re-run by the G4-pre audit (`docs/reports/G4_PRE_AUDIT_2026-08-22.md`).
- Defect state in scope: **0 open S1/S2** (5 S1 closed G2-exit; D-12/D-14/D-15/D-16/D-22 closed Wave 7, G3 §5); 4 S3 residuals carried as non-blocking (G3 §6).

### Implementer ≠ certifier

These records were authored by **SCRIBA** from machine evidence only (ledger, evidence report, reference store, G3 gate review). SCRIBA implemented none of the certified code and none of the qualifying tests; implementation was performed by the Wave 1–7 persona agents and certified at T2→T3 by QUALITAS under the separation-of-duties rule (Stage-2 §5.4, Stage-5 §5). The upcoming **G4 adjudication will be a fresh-context review** with final HUMAN acceptance authority (Stage-2 §4.3); this document is an input to that review, not a verdict of it.

## Provenance (artifacts cited, with their own timestamps)

| Artifact | Role | Internal timestamp/identifier |
|----------|------|-------------------------------|
| `docs/reports/article_ledger.json` (+ `article_ledger_summary.md`) | REQ-F citations module::function, chapter map, cite counts | Regenerated post-Wave-9 by `scripts/build_article_ledger.py` (2026-08-22, G4-pre audit finding F1 remediation); the G3-era revision was independently rebuilt by the G3 examiner (G3 §1.3) |
| `docs/reports/article_evidence_report.json` | REQ-T qualifying tests | `generated: 2026-08-22T15:15:23.968575+00:00`, `gate_G3: PASS` (G3 examiner run 2, §1.2/§7.3). Source used: `article_evidence_report.json` (live report is re-emitted per pytest run and can be a partial-run product, G3 §7.3; the frozen G3 baseline preserves the authoritative full-suite artifact) |
| `tests/articles/reference_values.json` | REQ-V reference values | 202 article keys / 256 values / 0 empty provenance (`validate_store()` green; G3 §4; Wave-9 expansion 71→200 in-scope; G4-pre §2 W9a) |
| `python check_coverage.py` (re-run by SCRIBA 2026-08-22) | chapter boundaries, 866/866 total | Ch XVII 752–757 (6), Ch XVIII 758–767 (10); P0 boundary fix holds |
| `docs/reports/G3_GATE_REVIEW_2026-08-21.md` | certified baseline: suite 2312/0/0/0, S2 closures, S3 rulings, theater scan | Independent fresh-context examiner, verdict PASS |
| Defect sources | annotations | Stage-3 register (`LAST200_STAGE3_QUALITY_REVIEW.md`), `S1_CERTIFICATION_2026-08-21.md`, Stage-5 §6, G3 §5–6 |

## Regeneration

```bash
python scripts/build_article_certifications.py
```

Re-run after any gate to re-emit this file from current artifact truth. The script fails loudly if the three artifacts disagree internally.

---

*Generated 2026-08-22 by SCRIBA (Wave 8b) via `scripts/build_article_certifications.py`. Certified baseline: G3 close, verdict PASS. T4/page verdicts/formula sheets intentionally absent — pending the human G1 adjudication session.*

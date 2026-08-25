"""Build docs/POTENTIALS_EQUIPOTENTIALS_PAGE_MAP.pdf — full inventory report."""
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "POTENTIALS_EQUIPOTENTIALS_PAGE_MAP.pdf"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title="Maxwell Potentials and Equipotentials — Equations, Code, and Page Numbers",
        author="Maxwell Modernization Project",
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontSize=16,
            spaceAfter=8,
            leading=20,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSub",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.HexColor("#333333"),
            spaceAfter=6,
            leading=13,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1c",
            parent=styles["Heading1"],
            fontSize=13,
            spaceBefore=14,
            spaceAfter=6,
            textColor=colors.HexColor("#1a2744"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            spaceAfter=4,
            alignment=TA_JUSTIFY,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Cell",
            parent=styles["Normal"],
            fontSize=7.5,
            leading=9.5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Note",
            parent=styles["Normal"],
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#444444"),
            leftIndent=6,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeBlock",
            parent=styles["Code"],
            fontSize=7.5,
            leading=9,
            backColor=colors.HexColor("#f4f4f4"),
            leftIndent=4,
            rightIndent=4,
            spaceBefore=4,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Hdr",
            parent=styles["Normal"],
            fontSize=7.5,
            leading=9.5,
            textColor=colors.white,
            fontName="Helvetica-Bold",
        )
    )

    def p(text: str, style: str = "Body") -> Paragraph:
        return Paragraph(text, styles[style])

    def cell(text: str) -> Paragraph:
        return Paragraph(text.replace("\n", "<br/>"), styles["Cell"])

    def table(headers: list[str], rows: list[list[str]], widths: list[float]) -> Table:
        data = [[Paragraph(h, styles["Hdr"]) for h in headers]]
        for row in rows:
            data.append([cell(c) for c in row])
        t = Table(data, colWidths=widths, repeatRows=1)
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a2744")),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#aaaaaa")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, colors.HexColor("#f0f4f8")],
                    ),
                    ("LEFTPADDING", (0, 0), (-1, -1), 3),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )
        return t

    story: list = []

    # Cover
    story.append(p("Maxwell Modernization Project", "CoverSub"))
    story.append(p("Potentials &amp; Equipotentials", "CoverTitle"))
    story.append(
        p(
            "Calculations, Equations, Product Modules, and Treatise Page Numbers",
            "CoverSub",
        )
    )
    story.append(
        p(
            "Full inventory: electric scalar potential V, equipotential surfaces, "
            "magnetic scalar potential, magnetic vector potential A, conduction/EMF "
            "potential language, product code paths, and OCR page IDs from the "
            "MAXWELL-MODERNIZED-PROGRAM product and page verifier catalog."
        )
    )
    story.append(
        p(
            "<b>Page numbering:</b> <font face='Courier'>v1-pNNN</font> = Volume I "
            "OCR/PDF page NNN; <font face='Courier'>v2-pNNN</font> = Volume II. "
            "These match <font face='Courier'>page_NNN.png</font> photos and the "
            "page verifier catalog "
            "(<font face='Courier'>volume_*_direct_result.json</font>).",
            "Note",
        )
    )
    story.append(
        p(
            "Product root: <font face='Courier'>MAXWELL-MODERNIZED-PROGRAM/maxwell/</font>. "
            "Generated for human verification and documentation.",
            "Note",
        )
    )
    story.append(Spacer(1, 8))

    # 1
    story.append(p("1. The big picture — types of potential", "H1c"))
    story.append(
        p(
            "In Maxwell's <i>Treatise</i> (and in the product package) there are several "
            "different potentials. Equipotential means a surface of constant scalar "
            "electric potential (and the geometry of those surfaces)."
        )
    )
    story.append(
        table(
            ["Kind", "Symbol", "What it is", "Where in Treatise"],
            [
                [
                    "Electric (scalar) potential",
                    "V or psi",
                    "Work per unit charge; E = -grad V",
                    "Vol I, Part I",
                ],
                [
                    "Equipotential surface",
                    "V = const",
                    "Surface of constant V; E perpendicular to it",
                    "Vol I (Art. 46 + forms of surfaces)",
                ],
                [
                    "Magnetic scalar potential",
                    "Omega",
                    "Magnetostatics (current-free regions)",
                    "Vol II, Part III",
                ],
                [
                    "Magnetic vector potential",
                    "A",
                    "B = curl A",
                    "Vol II, Arts. ~405-406+",
                ],
                [
                    "Contact / voltaic / EMF potential",
                    "EMF, contact V",
                    "Chemistry/contact electricity, not Laplace theory",
                    "Vol I, Part II",
                ],
                [
                    "Competing theories",
                    "Weber / Neumann",
                    "Historical alternatives",
                    "Late Vol II",
                ],
            ],
            [1.55 * inch, 0.9 * inch, 2.5 * inch, 2.15 * inch],
        )
    )
    story.append(Spacer(1, 10))

    # 2
    story.append(p("2. Core electric potential equations", "H1c"))
    story.append(
        p(
            "Main electrostatic potential calculations under "
            "<font face='Courier'>maxwell.core.potential</font>, "
            "<font face='Courier'>maxwell.core.field</font>, and supporting math. "
            "Units in product: <b>CGS-ESU</b> (statvolt, esu, cm)."
        )
    )
    story.append(
        table(
            ["Concept", "Equation (CGS)", "Articles", "OCR pages", "Product"],
            [
                [
                    "Potential / EMF unit",
                    "units of potential",
                    "22-23",
                    "v1-p057, v1-p060",
                    "core.measurement.potential_unit",
                ],
                [
                    "EMF as potential difference",
                    "work / unit charge along path",
                    "45",
                    "v1-p083",
                    "electromotive_force_potential",
                ],
                [
                    "Equipotential surface",
                    "V=const; E perp surface",
                    "46",
                    "v1-p084",
                    "core.field.EquipotentialSurface",
                ],
                [
                    "Line of force (related)",
                    "dx/Ex = dy/Ey = dz/Ez",
                    "47",
                    "v1-p086",
                    "core.field.LineOfForce",
                ],
                [
                    "Line integral of intensity",
                    "integral E · dl",
                    "69",
                    "v1-p111",
                    "line_integral (+ JAX)",
                ],
                [
                    "Definition of V",
                    "work bringing unit + charge from infinity",
                    "70",
                    "v1-p112",
                    "ElectricPotential, potential_difference",
                ],
                [
                    "Point charge",
                    "V = q / r",
                    "70",
                    "v1-p112",
                    "ElectricPotential.from_point_charge",
                ],
                [
                    "Field from potential",
                    "E = -grad V",
                    "71",
                    "v1-p113",
                    "field_from_potential (+ JAX)",
                ],
                [
                    "Conductor equipotential",
                    "V constant on/in conductor",
                    "72",
                    "v1-p113",
                    "ElectricPotential.conductor_surface",
                ],
                [
                    "Superposition",
                    "V = sum q_i/r_i",
                    "73",
                    "v1-p115",
                    "ElectricPotential.from_charges",
                ],
                [
                    "Laplace (no charge)",
                    "nabla^2 V = 0",
                    "77",
                    "v1-p124",
                    "laplace_equation, solve_laplace",
                ],
                [
                    "Poisson (with charge)",
                    "nabla^2 V = -4 pi rho",
                    "77",
                    "v1-p124",
                    "poisson_equation, solve_poisson",
                ],
                [
                    "Boundary conditions",
                    "cont. V; jump in dV/dn",
                    "78",
                    "(no OCR marker)",
                    "boundary_condition_*",
                ],
                [
                    "Mean-value of potential",
                    "sphere average",
                    "83",
                    "(no OCR marker)",
                    "potential_mean_value",
                ],
                [
                    "Energy via potentials",
                    "system energy",
                    "85-88, 91-92",
                    "v1-p140+",
                    "system_energy, general_theorems.*",
                ],
                [
                    "Potential of distribution",
                    "integral form",
                    "100-101",
                    "(no OCR marker for 100)",
                    "potential_from_charge_distribution",
                ],
                [
                    "Uniqueness",
                    "solution unique under BCs",
                    "102",
                    "(no OCR marker)",
                    "uniqueness_theorem",
                ],
            ],
            [1.25 * inch, 1.35 * inch, 0.85 * inch, 1.35 * inch, 2.3 * inch],
        )
    )
    story.append(
        p(
            "<b>Operators used with these:</b> gradient, divergence, laplacian in "
            "<font face='Courier'>maxwell.math.vector_operators</font>; partials in "
            "<font face='Courier'>math.derivatives</font>; integrals in "
            "<font face='Courier'>math.calculus_calculator</font>.",
            "Note",
        )
    )

    # 3
    story.append(p("3. Equipotentials — yes, that is the name", "H1c"))
    story.append(
        p(
            "Maxwell's language: <b>equipotential surfaces</b> (and forms of those surfaces "
            "together with lines of force). An equipotential is a surface at every point of "
            "which the potential is the same; the electric field is everywhere perpendicular "
            "to an equipotential surface (Art. 46)."
        )
    )
    story.append(
        table(
            ["Topic", "Articles", "OCR pages", "Product"],
            [
                [
                    "Early viz / related phenomena cites",
                    "16-19 (vis module labeling)",
                    "v1-p049, 051, 052, 053",
                    "vis.equipotential.plot_*; examples/02_equipotential_surfaces.py",
                ],
                [
                    "Definition of equipotential surface",
                    "46",
                    "v1-p084",
                    "EquipotentialSurface",
                ],
                [
                    "Equilibrium points / saddle structure",
                    "112-115",
                    "v1-p204, 205, 207…",
                    "equilibrium_points, saddle_point_analysis",
                ],
                [
                    "Generate equipotential surface V=const",
                    "117-119",
                    "v1-p212-215",
                    "equipotential_surface",
                ],
                [
                    "Surface charge / curvature on equipotentials",
                    "119-121",
                    "v1-p214-216",
                    "surface_charge_density, surface_curvature",
                ],
                [
                    "Field lines perp equipotentials",
                    "122-123",
                    "v1-p217-218",
                    "field_line_tracing",
                ],
                [
                    "Isolated sphere / concentric / coaxial V",
                    "124, 126, 127",
                    "v1-p221, 225, 226",
                    "isolated_sphere, concentric_spheres, coaxial_cylinders",
                ],
                [
                    "Confocal ellipsoid / hyperboloid equipotentials",
                    "147-156",
                    "v1-p267-280",
                    "confocal_ellipsoid_potential, confocal_hyperboloid, …",
                ],
            ],
            [1.9 * inch, 1.35 * inch, 1.55 * inch, 2.3 * inch],
        )
    )
    story.append(p("<b>Example to run:</b>"))
    story.append(
        Preformatted(
            "python examples/02_equipotential_surfaces.py\n"
            "# -> examples/output/equipotential.png",
            styles["CodeBlock"],
        )
    )

    # 4
    story.append(p("4. Method of images (potential near conductors)", "H1c"))
    story.append(
        table(
            ["Case", "Articles", "Pages", "Function"],
            [
                ["Plane", "171-173", "v1-p301, 303, 305", "image_point_charge_plane"],
                ["Sphere", "174-176", "v1-p307, 308, 311", "image_point_charge_sphere"],
                ["System analysis", "181", "v1-p314", "image_system_analysis"],
            ],
            [1.4 * inch, 1.2 * inch, 2.0 * inch, 2.5 * inch],
        )
    )
    story.append(Spacer(1, 8))

    # 5
    story.append(p("5. Magnetic scalar potential and vector potential (Vol II)", "H1c"))
    story.append(
        table(
            ["Topic", "Equation / idea", "Articles", "Pages", "Product"],
            [
                [
                    "Magnetic element potential",
                    "dOmega from magnet element",
                    "385-386",
                    "v2-p036, 037",
                    "physics.potentials.calc_element_potential, calc_finite_potential",
                ],
                [
                    "Vector potential",
                    "B = curl A",
                    "405",
                    "v2-p056",
                    "calc_B_from_vector_potential, gauge, magnetization to A",
                ],
                [
                    "Relate scalar / vector A",
                    "relation Omega to A",
                    "406",
                    "v2-p057",
                    "relate_scalar_vector_potential, vector_potential_uniform_field",
                ],
                [
                    "Loop / shell",
                    "solid angle to A; jump of Omega",
                    "421-422",
                    "v2-p069, 070",
                    "vector_potential_closed_curve, magnetic_shell_potential_jump",
                ],
                [
                    "Current-sheet / shell",
                    "shell potential, sheet A",
                    "648-651",
                    "v2-p313-314",
                    "calc_magnetic_shell_potential, calc_sheet_vector_potential",
                ],
                [
                    "Cylinder A",
                    "A inside cylindrical conductor",
                    "686-687",
                    "v2-p345",
                    "calc_cylinder_vector_potential",
                ],
            ],
            [1.35 * inch, 1.45 * inch, 0.85 * inch, 1.15 * inch, 2.3 * inch],
        )
    )
    story.append(
        p(
            "Also: <font face='Courier'>maxwell/electromagnetism/potentials/</font> "
            "(surfaces, multivalued, mutual_energy, directrix) and "
            "<font face='Courier'>vis/helicoidal_potentials.py</font> for advanced "
            "geometry / visualization.",
            "Note",
        )
    )

    # 6
    story.append(p("6. Potential in conduction / EMF (not Laplace)", "H1c"))
    story.append(
        p(
            "Maxwell also uses potential language for contact electricity and current flow. "
            "These are not the same as solving Laplace/Poisson for electrostatic V, but they "
            "appear in the product under potential-related names."
        )
    )
    story.append(
        table(
            ["Topic", "Articles", "Pages", "Product"],
            [
                [
                    "Contact / voltaic EMF",
                    "246-272 band",
                    "v1-p402-429",
                    "emf.*, emf_bodies.*, contact_potential",
                ],
                [
                    "Point source / dipole in 3D conductor",
                    "293-294",
                    "v1-p449-450",
                    "point_source_potential, dipole_potential",
                ],
                [
                    "Potential on resistive plane",
                    "307-309",
                    "v1-p464-467",
                    "potential_distribution_plane",
                ],
                [
                    "Network voltages (Kirchhoff)",
                    "275-280",
                    "v1-p434-438",
                    "network_solver.*",
                ],
            ],
            [2.0 * inch, 1.3 * inch, 1.5 * inch, 2.3 * inch],
        )
    )

    # 7
    story.append(p("7. Instruments that measure potential", "H1c"))
    story.append(
        p(
            "Electrometers, attracted disk, torsion balance — Arts. <b>210-228</b>, pages "
            "<b>v1-p355 … v1-p384</b> "
            "(<font face='Courier'>electrostatics.instruments.*</font>)."
        )
    )

    # 8
    story.append(p("8. How this shows up in the calculator UI", "H1c"))
    story.append(
        table(
            ["Calculator mode", "Potential-related content"],
            [
                [
                    "Equation Calculator",
                    "Sets involving A, E from potentials, energy (catalog Sets A-H, etc.)",
                ],
                [
                    "Derivatives",
                    "Partial V / gradient / Hessian (Laplace-related)",
                ],
                [
                    "Integrals",
                    "Volume integrals for charge to potential / energy style calcs",
                ],
                [
                    "Theorems",
                    "Divergence / Stokes / Green (potential theory backbone)",
                ],
            ],
            [1.8 * inch, 5.3 * inch],
        )
    )
    story.append(
        p(
            "The Streamlit calculator does <b>not</b> yet expose every ElectricPotential / "
            "equipotential / image-charge API as a dedicated UI page — those are mainly "
            "Python API + examples + vis. Launch: "
            "<font face='Courier'>streamlit run maxwell/calculator_ui.py "
            "--server.port 8502</font>.",
            "Note",
        )
    )

    # 9
    story.append(p("9. Page join gaps (OCR did not mark the article)", "H1c"))
    story.append(
        p(
            "These have product code but no page_* in the OCR index right now: "
            "<b>78, 83, 85, 100, 102</b> (and possibly neighbors). You can still open nearby "
            "pages (e.g. 77 → <b>v1-p124</b>, 86 → <b>v1-p140</b>) in the page verifier; a "
            "class-C style fix would attach markers later."
        )
    )

    # 10
    story.append(p("10. High-value pages to open in the page verifier", "H1c"))
    story.append(
        table(
            ["Page ID", "Why"],
            [
                [
                    "v1-p049-053",
                    "Early equipotential / force-line material + vis cites",
                ],
                [
                    "v1-p083-086",
                    "EMF potential, equipotential Art. 46, lines of force",
                ],
                [
                    "v1-p111-115",
                    "Line integral, V definition, E = -grad V, conductors, superposition",
                ],
                ["v1-p124", "Laplace / Poisson"],
                ["v1-p140+", "Energy"],
                [
                    "v1-p204-226",
                    "Equilibrium + equipotential surface generators",
                ],
                ["v1-p267-280", "Confocal equipotentials"],
                ["v1-p301-314", "Method of images"],
                ["v2-p036-037", "Magnetic element potential"],
                ["v2-p056-057", "Vector potential A"],
                ["v2-p069-070", "Loop / magnetic shell potential"],
            ],
            [1.6 * inch, 5.5 * inch],
        )
    )
    story.append(
        p(
            "In the HTML page verifier: Jump = article number (e.g. 112) or page id "
            "(e.g. v1-p212), or function search for "
            "<font face='Courier'>field_from_potential</font> / "
            "<font face='Courier'>equipotential_surface</font>. Server: "
            "<font face='Courier'>python run_page_verifier.py</font> → "
            "http://127.0.0.1:8765/",
            "Note",
        )
    )

    # 11
    story.append(p("11. Key product modules (file paths)", "H1c"))
    story.append(
        table(
            ["Module path", "Role"],
            [
                [
                    "maxwell/core/potential.py",
                    "ElectricPotential, Laplace, Poisson, BC, energy",
                ],
                [
                    "maxwell/core/field.py",
                    "EquipotentialSurface, LineOfForce, field_from_potential, line_integral",
                ],
                [
                    "maxwell/vis/equipotential.py",
                    "2D equipotential contour plots",
                ],
                [
                    "maxwell/electrostatics/equilibrium_surfaces.py",
                    "equipotential_surface generator, field lines, spheres/cylinders",
                ],
                [
                    "maxwell/electrostatics/confocal_surfaces.py",
                    "Confocal equipotentials / ellipsoidal Laplace",
                ],
                [
                    "maxwell/electrostatics/electric_images.py",
                    "Method of images potentials",
                ],
                [
                    "maxwell/electrostatics/general_theorems.py",
                    "Energy, Green reciprocity, uniqueness, potential from charge",
                ],
                [
                    "maxwell/math/potential_theorems.py",
                    "Flux, Gauss surface, mean value, EMF defs",
                ],
                [
                    "maxwell/calculus/vector_potential.py",
                    "Magnetic vector potential A",
                ],
                [
                    "maxwell/calculus/cyclic.py",
                    "Loop A via solid angle; magnetic shell jump",
                ],
                [
                    "maxwell/physics/potentials.py",
                    "Magnetic element / finite magnet potential",
                ],
                [
                    "maxwell/electromagnetism/potentials/*",
                    "Advanced EM potential surfaces / multivalued / energy",
                ],
                ["maxwell/jax/…", "JAX ports of potential/field helpers"],
            ],
            [2.6 * inch, 4.5 * inch],
        )
    )

    # 12
    story.append(p("12. Bottom line", "H1c"))
    story.append(
        p(
            "• <b>Potentials</b> in this project = mainly scalar electric V, equipotentials "
            "V=const, then magnetic scalar Omega and vector A, plus conduction/EMF "
            "potential language."
        )
    )
    story.append(
        p(
            "• <b>Equipotentials</b> are first-class: Art. 46 (definition), Arts. 117+ "
            "(forms/surfaces), confocal 147+, plus vis/equipotential."
        )
    )
    story.append(
        p(
            "• <b>Page numbers</b> are from the OCR catalog join (article markers to volume "
            "PDF pages). A few articles still lack page markers (78, 83, 85, 100, 102)."
        )
    )
    story.append(
        p(
            "• Treatise structure reminder: <b>2 volumes</b> (books), <b>4 scientific "
            "parts</b> (I-IV), continuous article numbers ~27-866 for the body of the work."
        )
    )
    story.append(Spacer(1, 12))
    story.append(
        p(
            "Document source: product code inventory + page_verifier citation/page index + "
            "Maxwell Treatise structure. Not a substitute for the original 1873/Third "
            "Edition text. Full response packaged as PDF per user request.",
            "Note",
        )
    )

    doc.build(story)
    print(f"WROTE {OUT.resolve()}")


if __name__ == "__main__":
    main()

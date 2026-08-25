"""Build docs/POTENTIALS_VALUE_MAP.pdf — where potentials matter most."""
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
OUT = ROOT / "docs" / "POTENTIALS_VALUE_MAP.pdf"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title="Where Maxwell Potentials Are Most Valuable",
        author="Maxwell Modernization Project",
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontSize=15,
            spaceAfter=8,
            leading=19,
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
            fontSize=12,
            spaceBefore=12,
            spaceAfter=5,
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
            fontSize=7,
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

    story.append(p("Maxwell Modernization Project", "CoverSub"))
    story.append(p("Where Potentials Are Most Valuable", "CoverTitle"))
    story.append(
        p(
            "Topology · Material Science · Nanotech · Wormhole Analogues · Dimensional Travel Claims",
            "CoverSub",
        )
    )
    story.append(
        p(
            "Strategic map: where electrostatic / magnetic potentials (V, equipotentials, "
            "vector potential A) create the most leverage — and where claims go beyond "
            "classical Maxwell theory. Companion to "
            "<font face='Courier'>POTENTIALS_EQUIPOTENTIALS_PAGE_MAP.pdf</font>."
        )
    )
    story.append(
        p(
            "<b>Honest frame:</b> Your stack is verified classical EM (Treatise-linked). "
            "That is infrastructure for materials and nanotech. It is <b>not</b> a spacetime "
            "wormhole or dimensional-travel engine. Metamaterial EM analogues are the only "
            "legitimate wormhole-adjacent research language.",
            "Note",
        )
    )
    story.append(Spacer(1, 6))

    # Ranked
    story.append(p("1. Ranked value (Clear Thought)", "H1c"))
    story.append(
        table(
            ["Rank", "Domain", "How valuable are potentials?", "Fit to maxwell package"],
            [
                [
                    "1",
                    "Material science",
                    "Highest near-term engineering impact",
                    "Dielectrics, conductors, BC on V, energy, images",
                ],
                [
                    "2",
                    "Nanotech / plasmonics",
                    "Extremely high (extreme E = -grad V)",
                    "Tip/gap fields, sensors, light-matter EM",
                ],
                [
                    "3",
                    "EM topology (flux, equipotentials, cloaks)",
                    "High as design language",
                    "Equipotentials, shells, A, field-line geometry",
                ],
                [
                    "4",
                    "Quantum / A topology (Aharonov-Bohm)",
                    "Deep; needs quantum layer beyond pure 1873 UI",
                    "Vector potential A is the classical bridge",
                ],
                [
                    "5",
                    "Wormholes / dimensional travel",
                    "Not from classical V alone",
                    "Only EM/metamaterial analogues, clearly labeled",
                ],
            ],
            [0.45 * inch, 1.55 * inch, 2.4 * inch, 2.7 * inch],
        )
    )
    story.append(Spacer(1, 8))

    # Materials
    story.append(p("2. Material science — best home for the potential stack", "H1c"))
    story.append(
        p(
            "Here potentials are not optional; they are the continuum description of "
            "electrostatic and magnetic materials problems."
        )
    )
    story.append(
        table(
            ["Physics", "Why it matters", "Treatise / product hooks"],
            [
                [
                    "Dielectrics / K",
                    "D ~ K E; interface jumps in normal dV/dn",
                    "Art. 77-78 band; dielectrics modules",
                ],
                [
                    "Conductors",
                    "Entire conductor is equipotential; charge on surface",
                    "Art. 72; EquipotentialSurface; equilibrium surfaces",
                ],
                [
                    "Energy / force on bodies",
                    "Forces from energy at fixed V or fixed charge",
                    "Arts. ~86-94 energy theorems",
                ],
                [
                    "Method of images",
                    "Potentials of charges near material boundaries",
                    "Arts. 171-176; electric_images",
                ],
                [
                    "Magnetics / materials",
                    "B, H, M; magnetic potentials / shells",
                    "Part III; vector potential A Arts. 405+",
                ],
            ],
            [1.4 * inch, 2.7 * inch, 3.0 * inch],
        )
    )
    story.append(
        p(
            "<b>Value:</b> capacitors, insulation, coatings, magnetic soft materials, sensors, "
            "electrometers — anything where boundary-value problems for V or A decide performance. "
            "This is where a page-verified, pip-installable Maxwell library is most defensible as "
            "advanced-tech infrastructure.",
            "Note",
        )
    )

    # Nano
    story.append(p("3. Nanotech — where gradients of potential dominate", "H1c"))
    story.append(
        p(
            "At the nanoscale, fields are huge even for modest voltages: "
            "E ~ Delta V / nanometer. Nanotech is not new wormhole physics; it is Maxwell potential "
            "theory under extreme geometry."
        )
    )
    story.append(
        table(
            ["Area", "Role of potential", "Reality check"],
            [
                [
                    "Tip / gap fields",
                    "Corona, field emission, AFM/STM intuition",
                    "Continuum model still starts from V; treatise has sharp-point language",
                ],
                [
                    "Plasmonics",
                    "EM response of metal nanostructures; enhanced E",
                    "Sensing, photothermal, catalysis — modern optics + Maxwell EM",
                ],
                [
                    "Nano-assembly / electrokinetics",
                    "Applied fields move/assemble particles",
                    "Direct use of potentials/fields in process design",
                ],
                [
                    "Molecular junctions",
                    "Potential landscape between electrodes",
                    "Continuum V + atomistic hybrid; your solvers are continuum side",
                ],
            ],
            [1.5 * inch, 2.6 * inch, 3.0 * inch],
        )
    )
    story.append(
        p(
            "Equipotentials around tips, gaps, and particles are the design language. "
            "Your vis.equipotential and E = -grad V tools map directly here.",
            "Note",
        )
    )

    # Topology
    story.append(p("4. Topology — which topology?", "H1c"))
    story.append(p("<b>A. Topology of the electromagnetic field (real, high value)</b>"))
    story.append(
        p(
            "• Equipotential surfaces = level sets of V.<br/>"
            "• Field lines / flux tubes = connectivity of E and B.<br/>"
            "• Vector potential A = flux topology (circulation, solid angle, magnetic shells; "
            "Arts. ~405-422).<br/>"
            "• Multivalued magnetic potential around currents = classical topological subtlety.<br/>"
            "<b>Value:</b> coils, shields, return-flux paths, field uniformity, instruments."
        )
    )
    story.append(p("<b>B. Topology of spacetime (wormholes, extra dimensions)</b>"))
    story.append(
        p(
            "General relativity / quantum gravity — not electrostatic V = q/r. "
            "Classical potentials do not open dimensional travel or traversable spacetime wormholes."
        )
    )
    story.append(p("<b>C. Analogue topology in the lab (interesting middle ground)</b>"))
    story.append(
        p(
            "Researchers have built electromagnetic / magnetic wormholes using metamaterials: "
            "devices that make fields appear to connect two regions while hiding the tunnel — "
            "changing effective EM topology, not spacetime. Lab magnetic wormholes (field appears "
            "elsewhere as if from an isolated monopole; tunnel magnetically erased) are "
            "<b>analogies</b>, not stargates. Theoretical work also discusses EM wormholes from "
            "metamaterials that act as wormholes with respect to Maxwell's equations."
        )
    )
    story.append(
        p(
            "<b>Honest research frame:</b> Can we design materials/structures whose EM potentials "
            "and fields implement non-trivial effective topology? — Not: Does Maxwell electrostatic "
            "potential implement dimensional travel?",
            "Note",
        )
    )

    # Wormholes
    story.append(p("5. Wormholes and dimensional travel — honest split", "H1c"))
    story.append(
        table(
            ["Claim", "Supported by Maxwell potentials?"],
            [
                [
                    "Traversable spacetime wormhole (Morris-Thorne-type)",
                    "No — needs GR + usually exotic stress-energy",
                ],
                [
                    "Quantum teleportation of states",
                    "Different physics (quantum info); not Treatise V",
                ],
                [
                    "EM / magnetic wormhole (metamaterial)",
                    "Yes as analogue — Maxwell equations + materials engineering",
                ],
                [
                    "Dimensional travel",
                    "Not a consequence of classical potential theory",
                ],
            ],
            [3.2 * inch, 3.9 * inch],
        )
    )
    story.append(
        p(
            "Wormhole papers that study EM fields in a wormhole metric assume GR first; "
            "Maxwell is a field on the geometry, not the generator of the tunnel. "
            "Sci-fi product claims would undermine the verified classical-EM brand. "
            "Metamaterial / effective-geometry EM design is legitimate frontier language.",
            "Note",
        )
    )

    # Vector potential
    story.append(p("6. Vector potential A — topology + quantum bridge", "H1c"))
    story.append(
        p(
            "Maxwell's A (Vol II ~405+) is not only bookkeeping: classically it encodes "
            "induction, gauges, and flux through loops; quantum mechanically the "
            "Aharonov-Bohm effect shows measurable phase from A even where B = 0. "
            "<b>Value ranking for A:</b> magnets and inductors first; flux topology second; "
            "quantum devices / interferometry third (needs a quantum layer on top of classical A)."
        )
    )

    # Map
    story.append(p("7. Practical value map for this product", "H1c"))
    story.append(
        Preformatted(
            """
                    +-------------------------------+
                    | Verified V, equipotentials    |
                    | Poisson/Laplace, images       |
                    | A, shells, energy             |
                    +---------------+---------------+
                                    |
        +---------------------------+---------------------------+
        v                           v                           v
  MATERIAL SCIENCE            NANO / PLASMONICS           EM TOPOLOGY DESIGN
  dielectrics, BC             tip fields, sensors         equipotentials,
  conductors, energy          gaps, assembly              flux tubes, A, cloaks
        |                           |                           |
        +---------------------------+-------------+-------------+
                                                  v
                              OPTIONAL RESEARCH (clearly labeled)
                         metamaterial EM "wormholes" / analogues
                              NOT dimensional travel
""".strip(
                "\n"
            ),
            styles["CodeBlock"],
        )
    )
    story.append(
        table(
            ["Your modules", "Natural customers"],
            [
                [
                    "core.potential, Poisson/Laplace",
                    "Continuum materials modeling",
                ],
                [
                    "EquipotentialSurface, equilibrium_surfaces, vis.equipotential",
                    "Electrode / insulation / nano-electrode design and viz",
                ],
                [
                    "Images, confocal",
                    "Conductor-charge problems, geometry",
                ],
                [
                    "vector_potential, cyclic shells",
                    "Magnetic topology, coils, shells",
                ],
                [
                    "page_verifier",
                    "Trust that equations match the book",
                ],
            ],
            [3.2 * inch, 3.9 * inch],
        )
    )

    # Bottom line
    story.append(p("8. Bottom line", "H1c"))
    story.append(
        p(
            "1. <b>Most valuable:</b> material science and nanotech — boundary-value problems "
            "for potential and its gradient."
        )
    )
    story.append(
        p(
            "2. <b>Topology that pays off:</b> equipotential and magnetic-flux topology (design), "
            "not spacetime topology."
        )
    )
    story.append(
        p(
            "3. <b>Wormholes:</b> only EM analogues / metamaterials are in-scope for Maxwell-based "
            "tech; literal wormholes / dimensional travel are out of scope for this physics."
        )
    )
    story.append(
        p(
            "4. <b>Comparative advantage:</b> free, page-verified classical implementation of V, "
            "equipotentials, and A — once-hidden Treatise math as usable infrastructure."
        )
    )
    story.append(
        p(
            "5. <b>Honest slogan:</b> Potential theory as the design language of matter and "
            "fields — from bulk dielectrics to nanometer gaps — with optional metamaterial "
            "topology research."
        )
    )
    story.append(Spacer(1, 10))
    story.append(
        p(
            "Related: <font face='Courier'>docs/POTENTIALS_EQUIPOTENTIALS_PAGE_MAP.pdf</font> "
            "(equations, articles, OCR page IDs). Regenerate this file: "
            "<font face='Courier'>python scripts/build_potentials_value_pdf.py</font>.",
            "Note",
        )
    )
    story.append(
        p(
            "Not a substitute for peer-reviewed GR, QFT, or experimental metamaterial literature. "
            "Classical Maxwell potentials remain foundational for materials and nano regardless.",
            "Note",
        )
    )

    doc.build(story)
    print(f"WROTE {OUT.resolve()}")


if __name__ == "__main__":
    main()

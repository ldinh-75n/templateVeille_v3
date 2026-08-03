from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from models import RapportVeille


def _echapper(texte: str) -> str:
    """
    Échappe les caractères spéciaux XML avant insertion dans un Paragraph
    reportlab (qui interprète un sous-ensemble de balises HTML/XML).
    """
    return (
        texte.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _construire_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()

    return {
        "titre": ParagraphStyle(
            "TitreRapport",
            parent=base["Title"],
        ),
        "sous_titre": ParagraphStyle(
            "SousTitreRapport",
            parent=base["Normal"],
            textColor=HexColor("#666666"),
            spaceAfter=18,
        ),
        "titre_article": ParagraphStyle(
            "TitreArticle",
            parent=base["Heading2"],
            spaceBefore=6,
            spaceAfter=4,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=base["Normal"],
            textColor=HexColor("#555555"),
            spaceAfter=8,
            alignment=TA_LEFT,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base["Heading4"],
            spaceBefore=6,
            spaceAfter=2,
        ),
        "corps": ParagraphStyle(
            "Corps",
            parent=base["Normal"],
            spaceAfter=8,
            leading=15,
        ),
        "lien": ParagraphStyle(
            "Lien",
            parent=base["Normal"],
            textColor=HexColor("#1a73e8"),
            spaceBefore=4,
        ),
    }


def generer_pdf_depuis_rapport(
    rapport: RapportVeille,
    chemin_pdf: str = "outputs/rapport_veille.pdf",
) -> str:
    """
    Génère un PDF proprement mis en page à partir du rapport structuré
    (titres, gras, retours à la ligne automatiques, liens cliquables).
    """

    Path("outputs").mkdir(exist_ok=True)
    styles = _construire_styles()

    elements = [
        Paragraph(_echapper(rapport.titre), styles["titre"]),
        Paragraph(
            f"Généré le {rapport.date_generation.strftime('%d/%m/%Y à %H:%M')}",
            styles["sous_titre"],
        ),
    ]

    for resume in rapport.resumes:
        elements.append(Paragraph(_echapper(resume.titre), styles["titre_article"]))
        elements.append(
            Paragraph(
                f"<b>Source :</b> {_echapper(resume.source)}"
                f" &nbsp;•&nbsp; <b>Score :</b> {resume.score_pertinence}/10",
                styles["meta"],
            )
        )

        elements.append(Paragraph("Résumé", styles["section"]))
        elements.append(Paragraph(_echapper(resume.resume), styles["corps"]))

        elements.append(Paragraph("Impact pour la SID/DNSI", styles["section"]))
        elements.append(Paragraph(_echapper(resume.impact), styles["corps"]))

        if resume.tags:
            tags = ", ".join(_echapper(tag) for tag in resume.tags)
            elements.append(Paragraph(f"<b>Tags :</b> {tags}", styles["corps"]))

        elements.append(
            Paragraph(
                f'<link href="{resume.url}">🔗 Lire l\'article</link>',
                styles["lien"],
            )
        )

        elements.append(
            HRFlowable(
                width="100%",
                thickness=0.5,
                color=HexColor("#dddddd"),
                spaceBefore=12,
                spaceAfter=12,
            )
        )

    document = SimpleDocTemplate(
        chemin_pdf,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    document.build(elements)

    return chemin_pdf

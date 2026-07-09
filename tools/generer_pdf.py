from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generer_pdf_depuis_markdown(
    chemin_markdown: str = "outputs/rapport_veille.md",
    chemin_pdf: str = "outputs/rapport_veille.pdf",
) -> str:
    """
    Génère un PDF simple à partir du rapport Markdown.
    """

    texte = Path(chemin_markdown).read_text(encoding="utf-8")

    Path("outputs").mkdir(exist_ok=True)

    document = canvas.Canvas(chemin_pdf, pagesize=A4)
    largeur, hauteur = A4

    position_y = hauteur - 50

    for ligne in texte.splitlines():
        if position_y < 50:
            document.showPage()
            position_y = hauteur - 50

        document.drawString(50, position_y, ligne[:110])
        position_y -= 16

    document.save()

    return chemin_pdf
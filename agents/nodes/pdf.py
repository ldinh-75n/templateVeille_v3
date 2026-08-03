from agents.state import EtatAgent
from tools.generer_pdf import generer_pdf_depuis_markdown


def noeud_pdf(etat: EtatAgent) -> EtatAgent:
    """
    Génère le rapport PDF.
    """

    etat.journal_execution.append("Génération du rapport PDF.")

    chemin_markdown = etat.metadonnees.get(
        "chemin_rapport_markdown", "outputs/rapport_veille.md"
    )
    chemin_pdf = generer_pdf_depuis_markdown(chemin_markdown=chemin_markdown)
    etat.metadonnees["chemin_rapport_pdf"] = chemin_pdf

    return etat
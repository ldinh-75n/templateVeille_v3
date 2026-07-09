from agents.state import EtatAgent
from tools.generer_rapport import generer_rapport_markdown


def noeud_rapport(etat: EtatAgent) -> EtatAgent:
    """
    Génère le rapport Markdown final.
    """

    etat.journal_execution.append("Génération du rapport Markdown.")

    etat.rapport = generer_rapport_markdown(etat.resumes)
    etat.metadonnees["chemin_rapport_markdown"] = "outputs/rapport_veille.md"

    return etat
from agents.state import EtatAgent
from tools.resumer_articles import resumer_articles


def noeud_resume(etat: EtatAgent) -> EtatAgent:
    """
    Résume les articles sélectionnés.
    """

    etat.journal_execution.append("Résumé des articles sélectionnés.")

    etat.resumes = resumer_articles(etat.articles_selectionnes)

    etat.metadonnees["nombre_resumes_generes"] = len(etat.resumes)

    return etat
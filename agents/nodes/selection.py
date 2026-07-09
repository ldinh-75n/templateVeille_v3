from agents.state import EtatAgent
from tools.selectionner_articles import selectionner_articles


def noeud_selection(etat: EtatAgent) -> EtatAgent:
    """
    Sélectionne les articles les plus pertinents pour la veille.
    """

    etat.journal_execution.append("Sélection des articles pertinents.")

    etat.articles_selectionnes = selectionner_articles(
        etat.articles_collectes
    )

    etat.metadonnees["nombre_articles_selectionnes"] = len(
        etat.articles_selectionnes
    )

    return etat
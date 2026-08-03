from agents.state import EtatAgent
from tools.collecter_articles import collecter_articles
from tools.stocker_articles import enregistrer_articles


def noeud_collecte(etat: EtatAgent) -> EtatAgent:
    """
    Collecte les articles depuis les sources choisies par le planificateur.
    """

    etat.journal_execution.append("Collecte des articles.")

    etat.articles_collectes = collecter_articles(
        sources_a_utiliser=etat.sources_a_utiliser,
        limite_par_source=etat.limite_par_source,
    )

    enregistrer_articles(etat.articles_collectes)

    etat.metadonnees["nombre_articles_collectes"] = len(
        etat.articles_collectes
    )

    return etat
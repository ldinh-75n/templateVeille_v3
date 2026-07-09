from agents.state import EtatAgent
from tools.dedoublonner_articles import dedoublonner_articles


def noeud_deduplication(etat: EtatAgent) -> EtatAgent:
    """
    Déduplique les articles collectés.
    """

    etat.journal_execution.append("Déduplication des articles.")

    nombre_avant = len(etat.articles_collectes)

    etat.articles_collectes = dedoublonner_articles(
        etat.articles_collectes
    )

    nombre_apres = len(etat.articles_collectes)

    etat.metadonnees["nombre_articles_avant_deduplication"] = nombre_avant
    etat.metadonnees["nombre_articles_apres_deduplication"] = nombre_apres

    return etat
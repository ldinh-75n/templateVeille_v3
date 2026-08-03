from agents.state import EtatAgent
from tools.charger_memoire import charger_memoire, sauvegarder_memoire


def noeud_charger_memoire(etat: EtatAgent) -> EtatAgent:
    """
    Charge la mémoire de veille précédente.
    """

    etat.journal_execution.append("Chargement de la mémoire.")
    etat.memoire = charger_memoire()
    etat.metadonnees["memoire_chargee"] = True

    return etat


def noeud_sauvegarder_memoire(etat: EtatAgent) -> EtatAgent:
    """
    Sauvegarde les URLs des articles traités.
    """

    etat.journal_execution.append("Sauvegarde de la mémoire.")

    urls = set(etat.memoire.get("urls_deja_vues", []))

    for article in etat.articles_collectes:
        urls.add(str(article.url))

    etat.memoire["urls_deja_vues"] = sorted(urls)
    sauvegarder_memoire(etat.memoire)
    etat.metadonnees["memoire_sauvegardee"] = True

    return etat
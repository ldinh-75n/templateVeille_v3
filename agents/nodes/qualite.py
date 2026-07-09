from agents.state import EtatAgent


def noeud_qualite(etat: EtatAgent) -> EtatAgent:
    """
    Vérifie rapidement si la veille produite est exploitable.
    """

    etat.journal_execution.append("Contrôle qualité de la veille.")

    if not etat.resumes:
        etat.erreurs.append("Aucun résumé généré.")

    etat.metadonnees["controle_qualite_ok"] = len(etat.erreurs) == 0

    return etat
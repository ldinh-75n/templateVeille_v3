from agents.state import EtatAgent


def noeud_demarrage(etat: EtatAgent) -> EtatAgent:
    """
    Initialise l'exécution de la veille.
    """

    etat.journal_execution.append("Démarrage de la veille.")

    return etat
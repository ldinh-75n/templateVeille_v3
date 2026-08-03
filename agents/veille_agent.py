from agents.graph import construire_graphe
from agents.state import EtatAgent


class VeilleAgent:
    """
    Point d'entrée principal de l'application.

    Cette classe masque les détails de LangGraph au reste de l'application.
    """

    def __init__(self):
        self.graphe = construire_graphe()

    def executer(self) -> EtatAgent:
        """
        Lance une exécution complète de la veille
        et retourne toujours un EtatAgent.
        """

        etat_initial = EtatAgent()

        resultat = self.graphe.invoke(etat_initial)

        if isinstance(resultat, EtatAgent):
            return resultat

        return EtatAgent.model_validate(resultat)
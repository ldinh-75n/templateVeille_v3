from agents.actions import ActionAgent
from agents.state import EtatAgent


def noeud_planificateur(etat: EtatAgent) -> EtatAgent:
    """
    Décide de la prochaine étape nécessaire pour produire une veille complète.
    """

    etat.journal_execution.append("Planification de la mission.")

    if not etat.sources_a_utiliser:
        etat.sources_a_utiliser = [
            "mistral",
            "huggingface",
            "xdaforums",
            "machinelearningmastery",
        ]

    if not etat.articles_collectes:
        etat.prochaine_action = ActionAgent.COLLECTER

    elif "nombre_articles_apres_deduplication" not in etat.metadonnees:
        etat.prochaine_action = ActionAgent.DEDOUBLER

    elif not etat.articles_selectionnes:
        etat.prochaine_action = ActionAgent.SELECTIONNER

    elif not etat.resumes:
        etat.prochaine_action = ActionAgent.RESUMER

    elif etat.rapport is None:
        etat.prochaine_action = ActionAgent.GENERER_RAPPORT

    else:
        etat.prochaine_action = ActionAgent.TERMINER

    return etat
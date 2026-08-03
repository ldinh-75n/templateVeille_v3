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
            "openai",
            "blogia",
        ]

    if "memoire_chargee" not in etat.metadonnees:
        etat.prochaine_action = ActionAgent.CHARGER_MEMOIRE

    elif "nombre_articles_collectes" not in etat.metadonnees:
        etat.prochaine_action = ActionAgent.COLLECTER

    elif "nombre_articles_apres_deduplication" not in etat.metadonnees:
        etat.prochaine_action = ActionAgent.DEDOUBLER

    elif "nombre_articles_selectionnes" not in etat.metadonnees:
        etat.prochaine_action = ActionAgent.SELECTIONNER

    elif "nombre_resumes_generes" not in etat.metadonnees:
        etat.prochaine_action = ActionAgent.RESUMER

    elif "controle_qualite_ok" not in etat.metadonnees:
        etat.prochaine_action = ActionAgent.CONTROLE_QUALITE

    elif etat.rapport is None:
        etat.prochaine_action = ActionAgent.GENERER_RAPPORT

    elif "chemin_rapport_pdf" not in etat.metadonnees:
        etat.prochaine_action = ActionAgent.GENERER_PDF

    elif "memoire_sauvegardee" not in etat.metadonnees:
        etat.prochaine_action = ActionAgent.SAUVEGARDER_MEMOIRE

    else:
        etat.prochaine_action = ActionAgent.TERMINER

    return etat
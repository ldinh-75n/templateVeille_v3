from agents.state import EtatAgent
from tools.envoyer_email import envoyer_email_veille


def noeud_email(etat: EtatAgent) -> EtatAgent:
    """
    Simule l'envoi du rapport de veille par email.
    """

    etat.journal_execution.append("Préparation de l'envoi email.")

    succes = envoyer_email_veille(
        destinataires=[],
        chemin_markdown=etat.metadonnees.get("chemin_rapport_markdown"),
        chemin_pdf=etat.metadonnees.get("chemin_rapport_pdf"),
    )

    etat.metadonnees["email_envoye"] = succes

    return etat
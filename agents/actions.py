from enum import StrEnum


class ActionAgent(StrEnum):
    """
    Liste des actions que l'agent peut exécuter.
    """

    COLLECTER = "collecter"
    DEDOUBLER = "dedoubler"
    SELECTIONNER = "selectionner"
    RESUMER = "resumer"
    GENERER_RAPPORT = "generer_rapport"
    ENVOYER_EMAIL = "envoyer_email"
    TERMINER = "terminer"
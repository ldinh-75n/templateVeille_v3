from enum import StrEnum


class ActionAgent(StrEnum):
    """
    Liste des actions que l'agent peut exécuter.
    """

    CHARGER_MEMOIRE = "charger_memoire"
    COLLECTER = "collecter"
    DEDOUBLER = "dedoubler"
    SELECTIONNER = "selectionner"
    RESUMER = "resumer"
    CONTROLE_QUALITE = "controle_qualite"
    GENERER_RAPPORT = "generer_rapport"
    GENERER_PDF = "generer_pdf"
    SAUVEGARDER_MEMOIRE = "sauvegarder_memoire"
    TERMINER = "terminer"
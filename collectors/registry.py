from collectors.base import CollecteurBase
from collectors.huggingface import CollecteurHuggingFace
from collectors.mistral import CollecteurMistral


# Registre central de tous les collecteurs disponibles.
#
# Pour ajouter une nouvelle source, il suffit de :
# 1. créer un nouveau collecteur dans collectors/
# 2. l'enregistrer ici
COLLECTEURS: dict[str, CollecteurBase] = {
    "mistral": CollecteurMistral(),
    "huggingface": CollecteurHuggingFace(),
}


def obtenir_collecteur(nom: str) -> CollecteurBase | None:
    """
    Retourne le collecteur associé à une source.

    Parameters
    ----------
    nom : str
        Nom technique de la source.

    Returns
    -------
    CollecteurBase | None
        Le collecteur correspondant ou None si la source n'existe pas.
    """
    return COLLECTEURS.get(nom)
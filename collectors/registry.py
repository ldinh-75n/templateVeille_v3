from collectors.base import CollecteurBase
from collectors.blogia import CollecteurBlogIA
from collectors.huggingface import CollecteurHuggingFace
from collectors.machinelearningmastery import CollecteurMachineLearningMastery
from collectors.mistral import CollecteurMistral
from collectors.openai import CollecteurOpenAI
from collectors.xdaforums import CollecteurXdaForums


# Registre central de tous les collecteurs disponibles.
#
# Pour ajouter une nouvelle source, il suffit de :
# 1. créer un nouveau collecteur dans collectors/
# 2. l'enregistrer ici
COLLECTEURS: dict[str, CollecteurBase] = {
    "mistral": CollecteurMistral(),
    "huggingface": CollecteurHuggingFace(),
    "xdaforums": CollecteurXdaForums(),
    "machinelearningmastery": CollecteurMachineLearningMastery(),
    "openai": CollecteurOpenAI(),
    "blogia": CollecteurBlogIA(),
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
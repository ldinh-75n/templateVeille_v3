from collectors.registry import obtenir_collecteur
from models import Article


def collecter_articles(
    sources_a_utiliser: list[str],
    limite_par_source: int = 5,
) -> list[Article]:
    """
    Collecte des articles depuis les sources demandées.
    """

    articles_collectes: list[Article] = []

    for nom_source in sources_a_utiliser:
        collecteur = obtenir_collecteur(nom_source)

        if collecteur is None:
            print(f"[WARNING] Aucun collecteur trouvé pour '{nom_source}'.")
            continue

        try:
            articles = collecteur.collecter(limite=limite_par_source)
            articles_collectes.extend(articles)

        except Exception as erreur:
            print(f"[ERROR] {nom_source} : {erreur}")

    return articles_collectes
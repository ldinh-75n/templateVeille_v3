from collectors.registry import obtenir_collecteur
from models import Article
from tools.stocker_articles import charger_urls_existantes


def collecter_articles(
    sources_a_utiliser: list[str],
    limite_par_source: int = 5,
) -> list[Article]:
    """
    Collecte des articles depuis les sources demandées.

    Les URLs déjà présentes dans le stockage (voir tools.stocker_articles)
    sont ignorées pour éviter de re-scraper des articles déjà connus.
    """

    articles_collectes: list[Article] = []
    urls_deja_connues = charger_urls_existantes()

    for nom_source in sources_a_utiliser:
        collecteur = obtenir_collecteur(nom_source)

        if collecteur is None:
            print(f"[WARNING] Aucun collecteur trouvé pour '{nom_source}'.")
            continue

        collecteur.definir_urls_a_ignorer(urls_deja_connues)

        try:
            articles = collecteur.collecter(limite=limite_par_source)
            articles_collectes.extend(articles)

        except Exception as erreur:
            print(f"[ERROR] {nom_source} : {erreur}")

    return articles_collectes
from models import Article


def dedoublonner_articles(articles: list[Article]) -> list[Article]:
    """
    Supprime les doublons d'articles à partir de leur URL.

    Le premier article rencontré est conservé.
    """

    articles_uniques: list[Article] = []
    urls_deja_vues: set[str] = set()

    for article in articles:
        url_normalisee = str(article.url).rstrip("/")

        if url_normalisee in urls_deja_vues:
            continue

        urls_deja_vues.add(url_normalisee)
        articles_uniques.append(article)

    return articles_uniques
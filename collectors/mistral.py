from collectors.base import CollecteurBase
from models import Article


class CollecteurMistral(CollecteurBase):
    """
    Collecteur dédié aux actualités Mistral AI.
    """

    def collecter(self, limite: int = 5) -> list[Article]:
        nom_source = "Mistral AI"
        theme = "LLM, modèles français, agents IA"
        url_base = "https://mistral.ai"
        url_actualites = "https://mistral.ai/news/"

        soup = self.obtenir_soup(url_actualites)

        articles: list[Article] = []
        urls_deja_vues: set[str] = set()

        for lien in soup.find_all("a", href=True):
            href = lien["href"]

            if "/news/" not in href:
                continue

            url = href if href.startswith("http") else url_base + href

            if url in urls_deja_vues or url.rstrip("/") == url_actualites.rstrip("/"):
                continue

            titre = lien.get_text(" ", strip=True)

            if not titre:
                continue

            urls_deja_vues.add(url)

            articles.append(
                Article(
                    titre=titre,
                    url=url,
                    source=nom_source,
                    theme=theme,
                    contenu=self.extraire_contenu_article(url),
                )
            )

            if len(articles) >= limite:
                break

        return articles
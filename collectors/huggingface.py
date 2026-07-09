from collectors.base import CollecteurBase
from models import Article


class CollecteurHuggingFace(CollecteurBase):
    """
    Collecteur dédié au blog Hugging Face.
    """

    def collecter(self, limite: int = 5) -> list[Article]:
        nom_source = "Hugging Face"
        theme = "Open source, modèles IA, datasets, agents"
        url_base = "https://huggingface.co"
        url_blog = "https://huggingface.co/blog"

        soup = self.obtenir_soup(url_blog)

        articles: list[Article] = []
        urls_deja_vues: set[str] = set()

        chemins_bloques = {
            "/blog",
            "/blog/",
            "/blog/community",
            "/blog/leaderboards",
            "/blog/open-source",
        }

        for lien in soup.find_all("a", href=True):
            href = lien["href"]

            if not href.startswith("/blog/"):
                continue

            if href in chemins_bloques:
                continue

            if len(href.strip("/").split("/")) < 2:
                continue

            url = url_base + href

            if url in urls_deja_vues or url.rstrip("/") == url_blog.rstrip("/"):
                continue

            titre = lien.get_text(" ", strip=True)

            if not titre or len(titre) < 10 or titre.lower() == "view all":
                continue

            urls_deja_vues.add(url)

            contenu = self.extraire_contenu_article(url)

            if len(contenu) < 500:
                continue

            articles.append(
                Article(
                    titre=titre,
                    url=url,
                    source=nom_source,
                    theme=theme,
                    contenu=contenu,
                )
            )

            if len(articles) >= limite:
                break

        return articles
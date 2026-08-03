from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from collectors.base import CollecteurBase
from config import JOURS_MAX_ANCIENNETE
from models import Article


class CollecteurHuggingFace(CollecteurBase):
    """
    Collecteur dédié au blog Hugging Face.
    """

    def extraire_date_publication(self, soup: BeautifulSoup) -> datetime | None:
        """
        Extrait la date de publication depuis la page d'un article.

        Sur huggingface.co/blog, la date est portée par une balise
        <time datetime="2026-07-27T10:15:03">.
        """
        balise_time = soup.find("time", attrs={"datetime": True})

        if balise_time is None:
            return None

        try:
            return datetime.fromisoformat(balise_time["datetime"]).replace(
                tzinfo=None
            )
        except ValueError:
            return None

    def collecter(self) -> list[Article]:
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

            if url in self.urls_a_ignorer:
                continue

            titre = lien.get_text(" ", strip=True)

            if not titre or len(titre) < 10 or titre.lower() == "view all":
                continue

            urls_deja_vues.add(url)

            soup_article = self.obtenir_soup(url)
            date_publication = self.extraire_date_publication(soup_article)
            date_limite = datetime.now() - timedelta(days=JOURS_MAX_ANCIENNETE)

            if date_publication is None or date_publication < date_limite:
                continue

            contenu = self.extraire_contenu_depuis_soup(soup_article)

            if len(contenu) < 500:
                continue

            articles.append(
                Article(
                    titre=titre,
                    url=url,
                    source=nom_source,
                    theme=theme,
                    contenu=contenu,
                    date_publication=date_publication,
                )
            )

        return articles
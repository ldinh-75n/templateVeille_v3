from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from collectors.base import CollecteurBase
from config import JOURS_MAX_ANCIENNETE
from models import Article


class CollecteurBlogIA(CollecteurBase):
    """
    Collecteur dédié au blog IA (blog-ia.com).
    """

    def extraire_date_publication(self, soup: BeautifulSoup) -> datetime | None:
        """
        Extrait la date de publication depuis la page d'un article.

        WordPress expose la date via
        <meta property="article:published_time" content="2026-07-25T08:41:53+00:00">.
        """
        balise_meta = soup.find("meta", property="article:published_time")

        if balise_meta is None or not balise_meta.get("content"):
            return None

        try:
            return datetime.fromisoformat(balise_meta["content"]).replace(
                tzinfo=None
            )
        except ValueError:
            return None

    def collecter(self, limite: int = 5) -> list[Article]:
        nom_source = "Blog IA"
        theme = "IA grand public, outils IA, guides pratiques"
        url_blog = "https://blog-ia.com/blog/"

        soup = self.obtenir_soup(url_blog)

        articles: list[Article] = []
        urls_deja_vues: set[str] = set()
        date_limite = datetime.now() - timedelta(days=JOURS_MAX_ANCIENNETE)

        for balise_article in soup.find_all("article"):
            lien = balise_article.find("a", href=True)

            if lien is None:
                continue

            url = lien["href"].strip()

            if url in urls_deja_vues:
                continue

            if url in self.urls_a_ignorer:
                continue

            titre_balise = balise_article.find(["h1", "h2", "h3"])
            titre = (
                titre_balise.get_text(" ", strip=True)
                if titre_balise is not None
                else lien.get_text(" ", strip=True)
            )

            if not titre or len(titre) < 10:
                continue

            urls_deja_vues.add(url)

            try:
                soup_article = self.obtenir_soup(url)
            except Exception:
                continue

            date_publication = self.extraire_date_publication(soup_article)

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

            if len(articles) >= limite:
                break

        return articles

from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from collectors.base import CollecteurBase
from config import JOURS_MAX_ANCIENNETE
from models import Article


class CollecteurMachineLearningMastery(CollecteurBase):
    """
    Collecteur dédié au blog Machine Learning Mastery.
    """

    def extraire_date_publication(self, soup: BeautifulSoup) -> datetime | None:
        """
        Extrait la date de publication depuis la page d'un article.

        WordPress expose la date via
        <meta property="article:published_time" content="2026-07-30T14:31:51+00:00">.
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

    def collecter(self) -> list[Article]:
        nom_source = "Machine Learning Mastery"
        theme = "Tutoriels ML, LLM, agents IA, bonnes pratiques"
        url_base = "https://machinelearningmastery.com"
        url_blog = "https://machinelearningmastery.com/blog/"

        soup = self.obtenir_soup(url_blog)

        # Chemins non pertinents (catégories, auteurs, pagination, pages utilitaires).
        segments_bloques = {
            "blog",
            "category",
            "author",
            "tag",
            "page",
            "about",
            "contact",
            "products",
            "newsletter",
            "rss-feed",
            "feed",
            "sitemap",
            "disclaimer",
            "privacy",
            "terms",
        }

        articles: list[Article] = []
        urls_deja_vues: set[str] = set()

        # Les titres d'articles sont exposés dans des balises <h2><a href="...">.
        for titre_balise in soup.find_all(["h2", "h3"]):
            lien = titre_balise.find("a", href=True)

            if lien is None:
                continue

            href = lien["href"].strip()

            if not href.startswith(url_base):
                continue

            # Attendu : https://machinelearningmastery.com/<slug>/
            chemin = href[len(url_base):].strip("/")

            if not chemin or "/" in chemin:
                continue

            if chemin in segments_bloques:
                continue

            url = f"{url_base}/{chemin}/"

            if url in urls_deja_vues:
                continue

            if url in self.urls_a_ignorer:
                continue

            titre = lien.get_text(" ", strip=True)

            if not titre or len(titre) < 10:
                continue

            urls_deja_vues.add(url)

            try:
                soup_article = self.obtenir_soup(url)
            except Exception:
                continue

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

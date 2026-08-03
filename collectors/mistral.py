from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from collectors.base import CollecteurBase
from config import JOURS_MAX_ANCIENNETE
from models import Article


class CollecteurMistral(CollecteurBase):
    """
    Collecteur dédié aux actualités Mistral AI.
    """

    def extraire_date_publication(self, soup: BeautifulSoup) -> datetime | None:
        """
        Extrait la date de publication depuis la page d'un article.

        Sur mistral.ai, la date apparaît sous le titre dans un
        <p class="text-body-small"> au format "March 23, 2026".
        """
        for paragraphe in soup.find_all("p", class_="text-body-small"):
            texte = paragraphe.get_text(strip=True)

            try:
                return datetime.strptime(texte, "%B %d, %Y")
            except ValueError:
                continue

        return None

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

            if url in self.urls_a_ignorer:
                continue

            titre = lien.get_text(" ", strip=True)

            if not titre:
                continue

            urls_deja_vues.add(url)

            soup_article = self.obtenir_soup(url)
            date_publication = self.extraire_date_publication(soup_article)

            date_limite = datetime.now() - timedelta(days=JOURS_MAX_ANCIENNETE)

            if date_publication is None or date_publication < date_limite:
                continue

            articles.append(
                Article(
                    titre=titre,
                    url=url,
                    source=nom_source,
                    theme=theme,
                    contenu=self.extraire_contenu_depuis_soup(soup_article),
                    date_publication=date_publication,
                )
            )

            if len(articles) >= limite:
                break

        return articles
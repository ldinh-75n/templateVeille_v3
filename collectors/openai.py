from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from curl_cffi import requests as creq

from collectors.base import CollecteurBase
from config import JOURS_MAX_ANCIENNETE
from models import Article


class CollecteurOpenAI(CollecteurBase):
    """
    Collecteur dédié aux actualités OpenAI.

    openai.com est protégé par une protection anti-bot (Cloudflare) qui
    bloque les requêtes `requests` classiques. On utilise curl_cffi qui
    imite le fingerprint TLS d'un vrai navigateur pour contourner cette
    protection, comme pour le collecteur XDA Forums.
    """

    _IMPERSONATE = "chrome124"

    def obtenir_soup(self, url: str) -> BeautifulSoup:
        reponse = creq.get(url, impersonate=self._IMPERSONATE, timeout=20)
        reponse.raise_for_status()
        return BeautifulSoup(reponse.text, "html.parser")

    def collecter(self) -> list[Article]:
        nom_source = "OpenAI"
        theme = "LLM, agents IA, recherche, produits OpenAI"
        url_base = "https://openai.com"
        url_actualites = "https://openai.com/news/"

        soup = self.obtenir_soup(url_actualites)

        articles: list[Article] = []
        urls_deja_vues: set[str] = set()
        date_limite = datetime.now() - timedelta(days=JOURS_MAX_ANCIENNETE)

        for lien in soup.find_all("a", href=True):
            href = lien["href"]

            if not href.startswith("/index/"):
                continue

            url = url_base + href

            if url in urls_deja_vues:
                continue

            if url in self.urls_a_ignorer:
                continue

            # La date de publication est déjà présente dans la carte de
            # la liste, sous forme de <time datetime="...">.
            balise_time = lien.find("time", attrs={"datetime": True})

            if balise_time is None:
                continue

            try:
                date_publication = datetime.fromisoformat(
                    balise_time["datetime"]
                ).replace(tzinfo=None)
            except ValueError:
                continue

            if date_publication < date_limite:
                continue

            balise_titre = lien.find(class_="text-h5")
            titre = (
                balise_titre.get_text(" ", strip=True)
                if balise_titre is not None
                else lien.get_text(" ", strip=True)
            )

            if not titre:
                continue

            urls_deja_vues.add(url)

            try:
                contenu = self.extraire_contenu_article(url)
            except Exception:
                continue

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

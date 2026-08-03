import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from curl_cffi import requests as creq

from collectors.base import CollecteurBase
from config import JOURS_MAX_ANCIENNETE
from models import Article


class CollecteurXdaForums(CollecteurBase):
    """
    Collecteur dédié au forum XDA « Artificial Intelligence (AI) general discussion ».

    XDA est protégé par BunnyCDN Bunny Shield (challenge TLS/JS).
    On utilise curl_cffi qui imite le fingerprint TLS d'un vrai navigateur
    pour contourner cette protection.
    """

    # Un fil de discussion XDA a une URL de la forme /t/slug-du-fil.NUMERO/
    _MOTIF_FIL = re.compile(r"^/t/[a-z0-9][a-z0-9\-]*\.\d+/?$")

    _IMPERSONATE = "chrome124"

    def obtenir_soup(self, url: str) -> BeautifulSoup:
        reponse = creq.get(url, impersonate=self._IMPERSONATE, timeout=20)
        reponse.raise_for_status()
        return BeautifulSoup(reponse.text, "html.parser")

    def extraire_contenu_article(self, url: str) -> str:
        """
        Extrait le contenu du premier post d'un fil XenForo.
        """
        soup = self.obtenir_soup(url)

        return self.extraire_contenu_depuis_soup(soup)

    def extraire_contenu_depuis_soup(self, soup: BeautifulSoup) -> str:
        """
        Extrait le contenu du premier post d'un fil XenForo à partir
        d'un objet BeautifulSoup déjà chargé.

        Les messages XDA sont dans des div `.bbWrapper` ; on prend le premier
        (le message d'ouverture du fil) et on récupère son texte brut.
        """
        message = soup.find("div", class_="bbWrapper")

        if message is None:
            # Repli sur la logique générique de la classe de base.
            return super().extraire_contenu_depuis_soup(soup)

        for balise in message(["script", "style", "blockquote"]):
            balise.decompose()

        texte = message.get_text(" ", strip=True)
        return texte[:4000]

    def extraire_date_publication(self, soup: BeautifulSoup) -> datetime | None:
        """
        Extrait la date de publication du premier post d'un fil XenForo.

        Le premier post porte une balise <time itemprop="datePublished" datetime="...">.
        """
        balise_time = soup.find("time", itemprop="datePublished")

        if balise_time is None or not balise_time.get("datetime"):
            return None

        try:
            return datetime.fromisoformat(balise_time["datetime"]).replace(
                tzinfo=None
            )
        except ValueError:
            return None

    def collecter(self) -> list[Article]:
        nom_source = "XDA Forums (AI)"
        theme = "IA sur mobile, LLM locaux, discussions communautaires"
        url_base = "https://xdaforums.com"
        url_forum = (
            "https://xdaforums.com/f/"
            "artificial-intelligence-ai-general-discussion.12757/"
        )

        soup = self.obtenir_soup(url_forum)

        articles: list[Article] = []
        urls_deja_vues: set[str] = set()

        # XenForo : les fils épinglés (règles, méta) sont dans un groupe séparé
        # `structItemContainer-group--sticky` — on ne prend que les fils normaux.
        for fil in soup.select("div.js-threadList div.structItem--thread"):
            titre_div = fil.select_one("div.structItem-title")
            if titre_div is None:
                continue

            lien_titre = titre_div.find(
                "a",
                href=lambda h: h is not None and self._MOTIF_FIL.match(h),
            )
            if lien_titre is None:
                continue

            titre = lien_titre.get_text(" ", strip=True)
            if not titre or len(titre) < 10:
                continue

            href = lien_titre["href"].strip()
            url = url_base + href.rstrip("/") + "/"

            if url in urls_deja_vues:
                continue

            if url in self.urls_a_ignorer:
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

            if len(contenu) < 300:
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

import re

from bs4 import BeautifulSoup
from curl_cffi import requests as creq

from collectors.base import CollecteurBase
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

        Les messages XDA sont dans des div `.bbWrapper` ; on prend le premier
        (le message d'ouverture du fil) et on récupère son texte brut.
        """
        soup = self.obtenir_soup(url)

        message = soup.find("div", class_="bbWrapper")

        if message is None:
            # Repli sur la logique générique de la classe de base.
            return super().extraire_contenu_article(url)

        for balise in message(["script", "style", "blockquote"]):
            balise.decompose()

        texte = message.get_text(" ", strip=True)
        return texte[:4000]

    def collecter(self, limite: int = 5) -> list[Article]:
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

            urls_deja_vues.add(url)

            try:
                contenu = self.extraire_contenu_article(url)
            except Exception:
                continue

            if len(contenu) < 300:
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

from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from models import Article


class CollecteurBase(ABC):
    """
    Classe abstraite commune à tous les collecteurs de sources.

    Elle fournit les méthodes techniques partagées :
    récupération HTML, parsing BeautifulSoup et extraction du texte utile.
    """

    @abstractmethod
    def collecter(self, limite: int = 5) -> list[Article]:
        """
        Collecte les articles d'une source donnée.
        """
        pass

    def obtenir_soup(self, url: str) -> BeautifulSoup:
        """
        Télécharge une page HTML et retourne un objet BeautifulSoup.
        """
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        }
        reponse = requests.get(url, timeout=10, headers=headers)
        reponse.raise_for_status()

        return BeautifulSoup(reponse.text, "html.parser")

    def extraire_contenu_article(self, url: str) -> str:
        """
        Extrait le contenu textuel principal d'un article.
        """
        soup = self.obtenir_soup(url)

        for balise in soup(["nav", "header", "footer", "script", "style"]):
            balise.decompose()

        contenu_principal = soup.find("main") or soup
        paragraphes = contenu_principal.find_all(["h1", "h2", "h3", "p"])

        texte = " ".join(
            paragraphe.get_text(" ", strip=True)
            for paragraphe in paragraphes
            if len(paragraphe.get_text(" ", strip=True)) > 40
        )

        return texte[:4000]
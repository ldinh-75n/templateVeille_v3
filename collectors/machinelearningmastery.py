from collectors.base import CollecteurBase
from models import Article


class CollecteurMachineLearningMastery(CollecteurBase):
    """
    Collecteur dédié au blog Machine Learning Mastery.
    """

    def collecter(self, limite: int = 5) -> list[Article]:
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

            titre = lien.get_text(" ", strip=True)

            if not titre or len(titre) < 10:
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
                )
            )

            if len(articles) >= limite:
                break

        return articles

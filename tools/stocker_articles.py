import csv
from datetime import datetime
from pathlib import Path

from models import Article, ArticleSelectionne


CHEMIN_CSV = Path("outputs/articles_collectes.csv")

COLONNES = [
    "url",
    "titre",
    "source",
    "theme",
    "date_publication",
    "date_collecte",
    "score_pertinence",
]


def charger_urls_existantes() -> set[str]:
    """
    Retourne l'ensemble des URLs déjà stockées dans le CSV.
    """

    if not CHEMIN_CSV.exists():
        return set()

    with open(CHEMIN_CSV, newline="", encoding="utf-8") as fichier:
        lecteur = csv.DictReader(fichier)
        return {ligne["url"] for ligne in lecteur}


def enregistrer_articles(articles: list[Article]) -> None:
    """
    Ajoute les nouveaux articles collectés au CSV (sans doublonner les URLs).
    """

    urls_existantes = charger_urls_existantes()

    nouveaux_articles = [
        article for article in articles if str(article.url) not in urls_existantes
    ]

    if not nouveaux_articles:
        return

    CHEMIN_CSV.parent.mkdir(exist_ok=True)
    fichier_existe = CHEMIN_CSV.exists()

    with open(CHEMIN_CSV, "a", newline="", encoding="utf-8") as fichier:
        ecrivain = csv.DictWriter(fichier, fieldnames=COLONNES)

        if not fichier_existe:
            ecrivain.writeheader()

        for article in nouveaux_articles:
            ecrivain.writerow(
                {
                    "url": str(article.url),
                    "titre": article.titre,
                    "source": article.source,
                    "theme": article.theme,
                    "date_publication": (
                        article.date_publication.isoformat()
                        if article.date_publication
                        else ""
                    ),
                    "date_collecte": datetime.now().isoformat(),
                    "score_pertinence": "",
                }
            )


def mettre_a_jour_scores(articles_selectionnes: list[ArticleSelectionne]) -> None:
    """
    Renseigne le score de pertinence des articles sélectionnés dans le CSV.
    """

    if not CHEMIN_CSV.exists() or not articles_selectionnes:
        return

    scores_par_url = {
        str(article.url): article.score_pertinence
        for article in articles_selectionnes
    }

    with open(CHEMIN_CSV, newline="", encoding="utf-8") as fichier:
        lecteur = csv.DictReader(fichier)
        lignes = list(lecteur)

    for ligne in lignes:
        if ligne["url"] in scores_par_url:
            ligne["score_pertinence"] = scores_par_url[ligne["url"]]

    with open(CHEMIN_CSV, "w", newline="", encoding="utf-8") as fichier:
        ecrivain = csv.DictWriter(fichier, fieldnames=COLONNES)
        ecrivain.writeheader()
        ecrivain.writerows(lignes)

from langchain_core.messages import HumanMessage, SystemMessage

from config import SCORE_MINIMAL_PERTINENCE
from llm import get_llm
from models import Article, ArticleSelectionne, ScorePertinence


def calculer_score_article(article: Article) -> int:
    """
    Évalue la pertinence d'un article pour l'équipe SID/DNSI.
    """

    prompt_systeme = """
            Tu travailles pour une équipe SID/DNSI qui construit une veille IA interne.

            Évalue l'intérêt de l'article pour une équipe qui travaille sur :
            - LLM open source
            - RAG
            - agents IA
            - serving de modèles avec vLLM
            - sécurité IA
            - outils développeurs IA
            - architecture de plateforme IA
            - IA pour le secteur public ou l'agriculture

            Attribue une note de pertinence entre 0 et 10.
            """

    llm_structure = get_llm(
        temperature=0.1
    ).with_structured_output(ScorePertinence)

    resultat = llm_structure.invoke(
        [
            SystemMessage(content=prompt_systeme),
            HumanMessage(
                content=(
                    f"Titre : {article.titre}\n\n"
                    f"Contenu : {article.contenu[:3000]}"
                )
            ),
        ]
    )

    return resultat.score


def selectionner_articles(
    articles: list[Article],
) -> list[ArticleSelectionne]:
    """
    Sélectionne les articles dont le score dépasse le seuil minimal.
    """

    articles_selectionnes: list[ArticleSelectionne] = []

    for article in articles:
        score = calculer_score_article(article)

        print(f"Score {score}/10 : {article.titre}")

        if score >= SCORE_MINIMAL_PERTINENCE:
            articles_selectionnes.append(
                ArticleSelectionne(
                    **article.model_dump(),
                    score_pertinence=score,
                )
            )

    return articles_selectionnes
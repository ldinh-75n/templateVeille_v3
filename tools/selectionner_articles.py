from langchain_core.messages import HumanMessage, SystemMessage

from config import SCORE_MINIMAL_PERTINENCE
from llm import get_llm
from models import Article, ArticleSelectionne, ScorePertinence


def calculer_score_article(article: Article) -> int:
    """
    Évalue la pertinence d'un article pour l'équipe SID/DNSI.
    """

    prompt_systeme = """
            Tu travailles au sein de la SID (Système d'Information Décisionnelle),
            une équipe de la DNSI (Direction Nationale du Système d'Information)
            des Chambres d'agriculture France.

            Ton équipe développe des applications d'IA générative pour des besoins
            internes :
            - recherche documentaire et RAG (retrieval augmented generation) sur
              des documents et données internes
            - génération automatique d'images, de vidéos et de documents
            - interrogation en langage naturel de données business (BI, requêtes
              sur les bases de données internes)
            - agents IA et automatisation de tâches

            Le but de cette veille est de ne pas passer à côté des technologies,
            outils, techniques ou retours d'expérience qui permettraient de mieux
            construire, opérer ou faire évoluer ces applications internes.

            Évalue la pertinence de l'article UNIQUEMENT par rapport à ces cas
            d'usage concrets. Sois exigeant :
            - 8 à 10 : l'article apporte une technique, un outil, un modèle ou un
              retour d'expérience directement réutilisable pour du RAG, de la
              génération de contenu (image/vidéo/document), de l'interrogation de
              données ou des agents IA internes
            - 4 à 7 : l'article concerne l'IA générative de façon plus générale
              mais reste exploitable indirectement (nouveau modèle LLM/multimodal,
              avancée en serving, sécurité IA ou outillage développeur IA)
            - 0 à 3 : actualité IA grand public, lancement produit sans rapport
              avec ces cas d'usage, ou contenu trop éloigné (IA dans le
              divertissement, discussions communautaires génériques, etc.)

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
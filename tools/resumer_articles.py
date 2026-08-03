from langchain_core.messages import HumanMessage, SystemMessage

from llm import get_llm
from models import ArticleSelectionne, ResumeArticle, ResultatResume


def resumer_articles(
    articles: list[ArticleSelectionne],
) -> list[ResumeArticle]:
    """
    Génère un résumé en français pour chaque article sélectionné.
    """

    llm_structure = get_llm(
        temperature=0.2
    ).with_structured_output(ResultatResume)

    resumes: list[ResumeArticle] = []

    prompt_systeme = """
        Tu rédiges une veille technologique pour l'équipe SID (Système
        d'Information Décisionnelle) de la DNSI (Direction Nationale du
        Système d'Information) des Chambres d'agriculture France.

        Cette équipe développe des applications d'IA générative internes :
        recherche documentaire et RAG, génération automatique d'images, de
        vidéos et de documents, interrogation en langage naturel de données
        business, et agents IA.

        Pour chaque article :
        - résume en français, de façon factuelle et concise
        - explique concrètement en quoi cette technologie, cet outil ou cette
          pratique peut aider l'équipe dans ses projets de RAG, de génération
          de contenu, d'interrogation de données ou d'agents IA (pas un impact
          générique du type "l'IA progresse")
        - propose quelques tags courts en lien avec ces cas d'usage
        """

    for article in articles:
        resultat = llm_structure.invoke(
            [
                SystemMessage(content=prompt_systeme),
                HumanMessage(
                    content=(
                        f"Titre : {article.titre}\n\n"
                        f"Source : {article.source}\n\n"
                        f"Contenu : {article.contenu[:4000]}"
                    )
                ),
            ]
        )

        resumes.append(
            ResumeArticle(
                titre=article.titre,
                url=article.url,
                source=article.source,
                theme=article.theme,
                score_pertinence=article.score_pertinence,
                resume=resultat.resume,
                impact=resultat.impact,
                tags=resultat.tags,
            )
        )

    return resumes
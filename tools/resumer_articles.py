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
Tu rédiges une veille IA professionnelle pour une équipe SID/DNSI.

Pour chaque article :
- résume en français
- explique l'impact concret pour une équipe data/IA/SI
- propose quelques tags courts
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
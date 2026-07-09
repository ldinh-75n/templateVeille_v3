from pathlib import Path

from models import RapportVeille, ResumeArticle


def generer_rapport_markdown(
    resumes: list[ResumeArticle],
    chemin_sortie: str = "outputs/rapport_veille.md",
) -> RapportVeille:
    """
    Génère un rapport Markdown à partir des résumés sélectionnés.
    """

    rapport = RapportVeille(
        titre="Veille IA SID/DNSI",
        resumes=resumes,
    )

    lignes: list[str] = [
        f"# {rapport.titre}",
        "",
        f"_Généré le {rapport.date_generation.strftime('%d/%m/%Y à %H:%M')}_",
        "",
    ]

    for resume in resumes:
        lignes.extend(
            [
                f"## {resume.titre}",
                "",
                f"**Source :** {resume.source}",
                "",
                f"**Score :** {resume.score_pertinence}/10",
                "",
                "### Résumé",
                resume.resume,
                "",
                "### Impact pour la SID/DNSI",
                resume.impact,
                "",
                f"**Tags :** {', '.join(resume.tags)}",
                "",
                f"[Lire l'article]({resume.url})",
                "",
                "---",
                "",
            ]
        )

    Path("outputs").mkdir(exist_ok=True)
    Path(chemin_sortie).write_text("\n".join(lignes), encoding="utf-8")

    return rapport
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class SourceVeille(BaseModel):
    """
    Représente une source de veille activable par l'agent.
    """

    nom: str
    url: HttpUrl
    theme: str
    active: bool = True


class Article(BaseModel):
    """
    Représente un article collecté depuis une source externe.
    """

    titre: str
    url: HttpUrl
    source: str
    theme: str
    contenu: str
    date_publication: Optional[datetime] = None


class ArticleSelectionne(Article):
    """
    Article retenu après évaluation de sa pertinence.
    """

    score_pertinence: int = Field(ge=0, le=10)


class ScorePertinence(BaseModel):
    """
    Résultat structuré renvoyé par le LLM lors de l'évaluation d'un article.
    """

    score: int = Field(ge=0, le=10)


class ResultatResume(BaseModel):
    """
    Résultat structuré renvoyé par le LLM lors du résumé d'un article.
    """

    resume: str
    impact: str
    tags: list[str] = Field(default_factory=list)


class ResumeArticle(BaseModel):
    """
    Résumé final enrichi d'un article sélectionné.
    """

    titre: str
    url: HttpUrl
    source: str
    theme: str
    score_pertinence: int = Field(ge=0, le=10)
    resume: str
    impact: str
    tags: list[str] = Field(default_factory=list)


class RapportVeille(BaseModel):
    """
    Rapport final généré par l'agent de veille.
    """

    titre: str
    langue: str = "fr"
    date_generation: datetime = Field(default_factory=datetime.now)
    resumes: list[ResumeArticle] = Field(default_factory=list)
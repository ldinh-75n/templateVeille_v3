from typing import Any

from pydantic import BaseModel, Field

from models import (
    Article,
    ArticleSelectionne,
    ResumeArticle,
    RapportVeille,
)


class EtatAgent(BaseModel):
    """
    Représente l'état partagé de l'agent de veille.

    Cet objet est transmis entre tous les nœuds LangGraph.
    Chaque nœud lit une partie de l'état, exécute sa responsabilité,
    puis enrichit l'état avec ses résultats.
    """

    # Mission demandée à l'agent.
    mission: str = "Effectuer une veille IA"

    # Planification de l'exécution.
    sources_a_utiliser: list[str] = Field(default_factory=list)
    prochaine_action: str | None = None

    # Articles collectés et sélectionnés.
    articles_collectes: list[Article] = Field(default_factory=list)
    articles_selectionnes: list[ArticleSelectionne] = Field(default_factory=list)

    # Résultats produits par l'agent.
    resumes: list[ResumeArticle] = Field(default_factory=list)
    rapport: RapportVeille | None = None

    # Mémoire de l'agent : historique, articles déjà vus, préférences, etc.
    memoire: dict[str, Any] = Field(default_factory=dict)

    # Observabilité : suivi de l'exécution et erreurs non bloquantes.
    journal_execution: list[str] = Field(default_factory=list)
    erreurs: list[str] = Field(default_factory=list)

    # Métadonnées techniques : durée, statistiques, configuration utilisée, etc.
    metadonnees: dict[str, Any] = Field(default_factory=dict)
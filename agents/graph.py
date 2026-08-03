from langgraph.graph import END, START, StateGraph

from agents.actions import ActionAgent
from agents.nodes.collecte import noeud_collecte
from agents.nodes.deduplication import noeud_deduplication
from agents.nodes.memoire import noeud_charger_memoire, noeud_sauvegarder_memoire
from agents.nodes.pdf import noeud_pdf
from agents.nodes.planificateur import noeud_planificateur
from agents.nodes.qualite import noeud_qualite
from agents.nodes.rapport import noeud_rapport
from agents.nodes.resume import noeud_resume
from agents.nodes.selection import noeud_selection
from agents.state import EtatAgent


def choisir_prochaine_etape(etat: EtatAgent) -> str:
    """
    Retourne le nom du prochain nœud à exécuter.
    """

    return etat.prochaine_action


def construire_graphe():
    """
    Construit le graphe fonctionnel de veille.
    """

    graphe = StateGraph(EtatAgent)

    graphe.add_node("planificateur", noeud_planificateur)
    graphe.add_node("charger_memoire", noeud_charger_memoire)
    graphe.add_node("collecter", noeud_collecte)
    graphe.add_node("dedoubler", noeud_deduplication)
    graphe.add_node("selectionner", noeud_selection)
    graphe.add_node("resumer", noeud_resume)
    graphe.add_node("controle_qualite", noeud_qualite)
    graphe.add_node("generer_rapport", noeud_rapport)
    graphe.add_node("generer_pdf", noeud_pdf)
    graphe.add_node("sauvegarder_memoire", noeud_sauvegarder_memoire)

    graphe.add_edge(START, "planificateur")

    graphe.add_conditional_edges(
        "planificateur",
        choisir_prochaine_etape,
        {
            ActionAgent.CHARGER_MEMOIRE: "charger_memoire",
            ActionAgent.COLLECTER: "collecter",
            ActionAgent.DEDOUBLER: "dedoubler",
            ActionAgent.SELECTIONNER: "selectionner",
            ActionAgent.RESUMER: "resumer",
            ActionAgent.CONTROLE_QUALITE: "controle_qualite",
            ActionAgent.GENERER_RAPPORT: "generer_rapport",
            ActionAgent.GENERER_PDF: "generer_pdf",
            ActionAgent.SAUVEGARDER_MEMOIRE: "sauvegarder_memoire",
            ActionAgent.TERMINER: END,
        },
    )

    graphe.add_edge("charger_memoire", "planificateur")
    graphe.add_edge("collecter", "planificateur")
    graphe.add_edge("dedoubler", "planificateur")
    graphe.add_edge("selectionner", "planificateur")
    graphe.add_edge("resumer", "planificateur")
    graphe.add_edge("controle_qualite", "planificateur")
    graphe.add_edge("generer_rapport", "planificateur")
    graphe.add_edge("generer_pdf", "planificateur")
    graphe.add_edge("sauvegarder_memoire", "planificateur")

    return graphe.compile()
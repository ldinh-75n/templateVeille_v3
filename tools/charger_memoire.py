import json
from pathlib import Path


CHEMIN_MEMOIRE = Path("outputs/memoire_veille.json")


def charger_memoire() -> dict:
    """
    Charge la mémoire persistante de l'agent.
    """

    if not CHEMIN_MEMOIRE.exists():
        return {"urls_deja_vues": []}

    return json.loads(CHEMIN_MEMOIRE.read_text(encoding="utf-8"))


def sauvegarder_memoire(memoire: dict) -> None:
    """
    Sauvegarde la mémoire persistante de l'agent.
    """

    Path("outputs").mkdir(exist_ok=True)
    CHEMIN_MEMOIRE.write_text(
        json.dumps(memoire, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
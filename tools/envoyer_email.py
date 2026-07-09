def envoyer_email_veille(
    destinataires: list[str],
    chemin_markdown: str,
    chemin_pdf: str | None = None,
) -> bool:
    """
    Prépare l'envoi de la veille par email.

    Pour l'instant, cette fonction est un placeholder.
    L'intégration SMTP ou Microsoft Graph sera ajoutée ensuite.
    """

    print("[INFO] Envoi email simulé.")
    print(f"[INFO] Destinataires : {destinataires}")
    print(f"[INFO] Markdown : {chemin_markdown}")
    print(f"[INFO] PDF : {chemin_pdf}")

    return True
from pathlib import Path

import streamlit as st

from agents.veille_agent import VeilleAgent
from tools.envoyer_email import envoyer_email_veille
from tools.generer_pdf import generer_pdf_depuis_markdown


st.set_page_config(
    page_title="Veille IA SID/DNSI V2",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Veille IA SID/DNSI - Version 2")

with st.sidebar:
    st.header("Configuration")

    limite = st.slider(
        "Nombre d'articles par source",
        min_value=1,
        max_value=10,
        value=3,
    )

    generer_pdf = st.checkbox(
        "Générer aussi un PDF",
        value=False,
    )

    envoyer_email = st.checkbox(
        "Envoyer la veille par email",
        value=False,
    )

    destinataires = ""

    if envoyer_email:
        destinataires = st.text_input(
            "Destinataires email",
            placeholder="prenom.nom@example.fr, autre@example.fr",
        )

    lancer = st.button(
        "🚀 Générer la veille",
        use_container_width=True,
    )


if lancer:
    with st.spinner("Collecte, sélection et résumé en cours..."):
        agent = VeilleAgent()
        etat = agent.executer(
            limite_par_source=limite,
        )

    st.success(
        f"{len(etat.resumes)} article(s) retenu(s)"
    )

    st.subheader("Journal d'exécution")
    st.write(etat.journal_execution)

    st.subheader("Métadonnées")
    st.json(etat.metadonnees)

    for article in etat.resumes:
        with st.container(border=True):
            col1, col2 = st.columns([5, 1])

            with col1:
                st.subheader(article.titre)
                st.caption(article.source)

            with col2:
                st.metric("Score", f"{article.score_pertinence}/10")

            st.markdown("### 📝 Résumé")
            st.write(article.resume)

            st.markdown("### 💡 Intérêt pour la SID/DNSI")
            st.write(article.impact)

            if article.tags:
                st.markdown(
                    "**Tags :** " + " • ".join(article.tags)
                )

            st.markdown(
                f"[🔗 Lire l'article]({article.url})"
            )

    chemin_markdown = etat.metadonnees.get(
        "chemin_rapport_markdown",
        "outputs/rapport_veille.md",
    )

    if Path(chemin_markdown).exists():
        with open(chemin_markdown, "rb") as fichier:
            st.download_button(
                label="📥 Télécharger le rapport Markdown",
                data=fichier,
                file_name="rapport_veille.md",
                mime="text/markdown",
                use_container_width=True,
            )

    if generer_pdf:
        chemin_pdf = generer_pdf_depuis_markdown(
            chemin_markdown=chemin_markdown,
            chemin_pdf="outputs/rapport_veille.pdf",
        )

        with open(chemin_pdf, "rb") as fichier:
            st.download_button(
                label="📄 Télécharger le rapport PDF",
                data=fichier,
                file_name="rapport_veille.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

    if envoyer_email:
        liste_destinataires = [
            email.strip()
            for email in destinataires.split(",")
            if email.strip()
        ]

        if not liste_destinataires:
            st.warning("Aucun destinataire renseigné.")
        else:
            chemin_pdf = "outputs/rapport_veille.pdf" if generer_pdf else None

            succes = envoyer_email_veille(
                destinataires=liste_destinataires,
                chemin_markdown=chemin_markdown,
                chemin_pdf=chemin_pdf,
            )

            if succes:
                st.success("Email préparé / envoyé avec succès.")
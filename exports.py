import os
import io
import pandas as pd
import streamlit as st
from gcp import get_storage_client
from google.cloud.exceptions import NotFound
from google.cloud import storage
import footer

from Data_cleaning.clean_adh import clean_adh_data
from Data_cleaning.clean_euros_players import clean_euros_players
from Data_cleaning.clean_evo_jj import clean_evo_jj


from utils import display_icon


def upload_to_bucket(file, folder_name):
    client, bucket = get_storage_client()

    # Construire le nom de fichier complet avec le préfixe du dossier.
    filename = os.path.join(folder_name, file.name)

    # Télécharge le fichier dans le bucket.
    blob = bucket.blob(filename)
    blob.upload_from_file(file, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    print(f"File {file.name} uploaded to {filename}.")



def save_final_dataframe(df, export_name):
    # Initialisation de la barre de progression
    progress = st.progress(0)
    st.title(f"Sauvegarde des données pour l'export {export_name} en cours, merci de patienter...")

    progress.progress(25)

    # Convertir le DataFrame directement en un objet BytesIO pour éviter de le sauvegarder localement
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    progress.progress(50)

    # Créer un objet de fichier semblable avec le contenu du BytesIO et le nom souhaité
    final_file = type('', (object,), {'name': f'{export_name}_df_finale.xlsx', 'read': output.read, 'seek': output.seek, 'tell': output.tell})()

    progress.progress(75)

    # Réinitialisez la position à 0 pour être sûr
    final_file.seek(0)

    # Téléchargez ce "fichier" dans le bucket
    upload_to_bucket(final_file, "DF_FINALE")
    progress.progress(100)
    st.title(f"Sauvegarde des données pour l'export {export_name} terminée...")

def main():
    # Charger le contenu du fichier CSS
    with open('style.css', 'r') as css_file:
        css = css_file.read()

    # Afficher le contenu CSS dans la page Streamlit
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    #########################################################################
    #########################################################################

    # Afficher l'icône pour la page "Exports" avec le titre personnalisé
    display_icon("Exports", "Exportations des fichiers")

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

    with col2:
        # Upload pour EVO_JJ
        evo_jj_file = st.file_uploader("Choisissez un fichier EVO_JJ (.xls)", type=["xls"])
        if evo_jj_file:
            upload_to_bucket(evo_jj_file, "EVO_JJ")
            evo_jj_df = clean_evo_jj()
            save_final_dataframe(evo_jj_df, "EVO_JJ")
            # st.success(f"Fichier {evo_jj_file.name} téléchargé avec succès dans le dossier EVO_JJ.")

        # Upload pour ADH
        adh_file = st.file_uploader("Choisissez un fichier ADH (.xls)", type=["xls"])
        if adh_file:
            upload_to_bucket(adh_file, "ADH")
            adh_df = clean_adh_data()
            save_final_dataframe(adh_df, "ADH")
            # st.success(f"Fichier {adh_file.name} téléchargé avec succès dans le dossier ADH.")

        # Upload pour EUROS_PLAYERS
        euros_players_file = st.file_uploader("Choisissez un fichier EUROS_PLAYERS (.xls)", type=["xls"])
        if euros_players_file:
            upload_to_bucket(euros_players_file, "EUROS_PLAYERS")
            euros_players_df = clean_euros_players()
            save_final_dataframe(euros_players_df, "EUROS_PLAYERS")
            # st.success(f"Fichier {euros_players_file.name} téléchargé avec succès dans le dossier EUROS_PLAYERS.")



    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    footer.display()

if __name__ == "__main__":
    main()

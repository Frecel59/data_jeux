# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io

# Importation des fonctions personnalisées depuis d'autres fichiers Python
from gcp import get_storage_client
import footer
from utils import display_icon



# Fonction pour formater une date en français
def format_date_in_french(date):
    # Liste des noms de mois en français
    mois = [
        'janvier',
        'février',
        'mars',
        'avril',
        'mai',
        'juin',
        'juillet',
        'août',
        'septembre',
        'octobre',
        'novembre',
        'décembre']

    # Formater la date au format "jour mois année"
    return f"{date.day} {mois[date.month - 1]} {date.year}"

# Fonction principale
def main():
    # Charger le contenu du fichier CSS
    with open('style.css', 'r') as css_file:
        css = css_file.read()

    # Afficher le contenu CSS dans la page Streamlit
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    #########################################################################
    #########################################################################

    # Afficher l'icône pour la page avec le titre personnalisé
    display_icon("Analyses N-1", "Analyses d'une période vs période N-1")

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    #########################################################################
    ############# CHAMPS INPUT POUR LE CHOIX DE LA PERIODE ##################
    #########################################################################
    # Début de la section pour le bilan en fonction des jours et services

    def get_df_from_gcp():
        client, bucket = get_storage_client()

        # Chemin vers votre fichier dans le bucket
        blob_path = "DF_FINALE/EVO_JJ_df_finale.xlsx"
        blob = bucket.blob(blob_path)

        # Téléchargez le fichier dans un objet en mémoire
        in_memory_file = io.BytesIO()
        blob.download_to_file(in_memory_file)
        in_memory_file.seek(0)

        # Lisez le fichier Excel dans un DataFrame
        df = pd.read_excel(in_memory_file)

        return df

    # Appeler la fonction get_df_from_gcp pour obtenir les données
    EVO_JJ_df_finale = get_df_from_gcp()

    ##########################################################################

        # Créer une mise en page en colonnes pour la période N et N-1
    col_N, col_N_1 = st.columns(2)

    # Période N
    with col_N:
        st.markdown(f'<p class="period-text">Choississez une période N</p>', \
            unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([0.1, 0.4, 0.4, 0.1])

        with col2:
            # Date de départ pour la période N
            start_date_a = st.date_input("Date de départ", datetime((EVO_JJ_df_finale["date"] \
                .max()).year - 1, 11, 1), key="start_date_input_a", \
                    format="DD/MM/YYYY")
            formatted_start_date_a = format_date_in_french(start_date_a)

        with col3:
            # Date de fin pour la période N
            end_date_a = st.date_input("Date de fin", EVO_JJ_df_finale["date"].max(), \
                key="end_date_input_a", format="DD/MM/YYYY")
            formatted_end_date_a = format_date_in_french(end_date_a)

    # Période N-1
    with col_N_1:
        st.markdown(f'<p class="period-text">Choississez une période N-1</p>', \
            unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([0.1, 0.4, 0.4, 0.1])

        with col2:
            # Date de départ pour la période N-1
            start_date_a2 = st.date_input("Date de départ",
                datetime((EVO_JJ_df_finale["date"].max()).year - 1, 11, 1) - timedelta(days=365),
                key="start_date_input_a2",
                format="DD/MM/YYYY")
            formatted_start_date_a2 = format_date_in_french(start_date_a2)

        with col3:
            # Date de fin pour la période N-1
            end_date_a2 = st.date_input("Date de fin", EVO_JJ_df_finale["date"].max() - \
                timedelta(days=365), key="end_date_input_a2", format="DD/MM/YYYY")
            formatted_end_date_a2 = format_date_in_french(end_date_a2)


    st.markdown("<hr/>", unsafe_allow_html=True)
    footer.display()





if __name__ == "__main__":
    main()

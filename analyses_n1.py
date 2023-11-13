# Importation des bibliothèques nécessaires
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io
from datetime import datetime, timedelta

# Importation des fonctions personnalisées depuis d'autres fichiers Python
from gcp import get_storage_client
import footer
from utils import display_icon
from Results_df.adh import results_adh
from Results_df.evo_jj import results_evo_jj
from Results_df.euros_pp import results_euros_pp



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

def get_df_from_gcp(file_name):
    client, bucket = get_storage_client()

    # Chemin vers votre fichier dans le bucket
    blob_path = f"DF_FINALE/{file_name}"
    blob = bucket.blob(blob_path)

    # Téléchargez le fichier dans un objet en mémoire
    in_memory_file = io.BytesIO()
    blob.download_to_file(in_memory_file)
    in_memory_file.seek(0)

    # Lisez le fichier Excel dans un DataFrame
    df = pd.read_excel(in_memory_file)

    return df

 # Fonction pour obtenir le jour de la semaine le plus proche un an avant
def get_nearest_weekday(date_N, target_weekday):
    # Soustrayez un an de la date de départ de la période N
    previous_year_date = date_N - timedelta(days=365)
    # Trouvez le jour de la semaine pour cette date
    current_weekday = previous_year_date.weekday()

    # Calculez la différence de jours entre le jour cible et le jour actuel
    day_difference = (target_weekday - current_weekday) % 7
    # Ajoutez la différence de jours à la date précédente
    nearest_weekday_date = previous_year_date + timedelta(days=day_difference)

    return nearest_weekday_date

# Fonction principale
def main():
    # Charger le contenu du fichier CSS
    with open('style.css', 'r') as css_file:
        css = css_file.read()

    # Afficher le contenu CSS dans la page Streamlit
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    # Afficher l'icône pour la page avec le titre personnalisé
    display_icon("Analyses N-1", "Analyses de 2 périodes")

    # Utiliser le séparateur horizontal avec la classe CSS personnalisée
    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)

    # Ajouter dans le menu des options
    st.sidebar.title("Options")
    genre = st.sidebar.radio(
        "Quel type d'analyse ?",
        ["***Date***", "***Jour***"],
        format_func=lambda x: f"***De {x.lower()} à {x.lower()}***"
    )


    #########################################################################
    ############# CHAMPS INPUT POUR LE CHOIX DE LA PERIODE ##################
    #########################################################################
    # Appeler la fonction get_df_from_gcp avec le nom spécifique de chaque fichier
    EVO_JJ_df_finale = get_df_from_gcp("EVO_JJ_df_finale.xlsx")
    ADH_df_finale = get_df_from_gcp("ADH_df_finale.xlsx")
    EUROS_PLAYERS_df = get_df_from_gcp("EUROS_PLAYERS_df_finale.xlsx")




    # Champs des dates
    col_N, col_N_1 = st.columns(2)

    with col_N:
        st.markdown(f'<p class="period-text">Choississez une période</p>', unsafe_allow_html=True)

        col_N_start, col_N_end = st.columns(2)
        with col_N_start:
            start_date_a = st.date_input("***Date de départ***", datetime((EVO_JJ_df_finale["date"].max()).year - 1, 11, 1), key="start_date_input_a", format="DD/MM/YYYY")
        with col_N_end:
            end_date_a = st.date_input("***Date de fin***", EVO_JJ_df_finale["date"].max(), key="end_date_input_a", format="DD/MM/YYYY")

    with col_N_1:
        st.markdown(f'<p class="period-text">Période de comparaison</p>', unsafe_allow_html=True)

        col_N_1_start, col_N_1_end = st.columns(2)
        with col_N_1_start:
            if genre == '***Date***':
                start_date_a2 = st.date_input("Date de départ", (start_date_a - timedelta(days=365)), key="start_date_input_a2", format="DD/MM/YYYY")
            elif genre == '***Jour***':
                start_date_a2 = st.date_input("Date de départ", get_nearest_weekday(start_date_a, start_date_a.weekday()), key="start_date_input_a2", format="DD/MM/YYYY")

        with col_N_1_end:
            if genre == '***Date***':
                end_date_a2 = st.date_input("Date de départ", (end_date_a - timedelta(days=365)), key="end_date_input_a2", format="DD/MM/YYYY")
            elif genre == '***Jour***':
                end_date_a2 = st.date_input("Date de fin", start_date_a2 + (end_date_a - start_date_a), key="end_date_input_a2", format="DD/MM/YYYY")


    start_date_a = pd.to_datetime(start_date_a)
    end_date_a = pd.to_datetime(end_date_a)
    start_date_a2 = pd.to_datetime(start_date_a2)
    end_date_a2 = pd.to_datetime(end_date_a2)


    result_evo_jj, result_evo_jj_1 = results_evo_jj(EVO_JJ_df_finale, start_date_a, end_date_a, start_date_a2, end_date_a2)

    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)
    col1_bilan, col2_bilan, col3_bilan = st.columns([0.2, 0.6, 0.2])

    with col2_bilan:
        st.markdown(f'<p class="period-text">EVO JJ</p>', unsafe_allow_html=True)
        st.table(result_evo_jj_1)


    result_df, result_df1 = results_adh(ADH_df_finale, start_date_a, end_date_a, start_date_a2, end_date_a2)
    result_euros_pp, result_euros_pp1 = results_euros_pp(EUROS_PLAYERS_df, start_date_a, end_date_a, start_date_a2, end_date_a2)

    st.markdown('<hr class="custom-separator">', unsafe_allow_html=True)
    col1_bilan, col2_bilan, col3_bilan = st.columns([0.2, 0.6, 0.2])

    with col2_bilan:
        st.markdown(f'<p class="period-text">Players Plus</p>', unsafe_allow_html=True)
        # st.table(result_df1)
        # st.table(result_euros_pp1)

        # Concaténer les deux DataFrames verticalement
        result_combined = pd.concat([result_df1, result_euros_pp1], ignore_index=False)

        # Afficher la table combinée
        st.table(result_combined)





    st.markdown("<hr/>", unsafe_allow_html=True)
    footer.display()





if __name__ == "__main__":
    main()

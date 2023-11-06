import pandas as pd
from dotenv import load_dotenv
from gcp import get_storage_client


load_dotenv() # Charger les variables d'environnement à partir du fichier .env

def concatenate_evo_jj():
    # Chemin vers le dossier contenant les fichiers XLSX dans le bucket
    blob_directory = "EVO_JJ/"

    client, bucket = get_storage_client()

    # Liste des fichiers XLS dans le répertoire spécifié
    blobs = bucket.list_blobs(prefix=blob_directory)

    # Initialisation du dataframe pour stocker les données concaténées
    concatenated_df = pd.DataFrame()

    # Boucle pour lire chaque fichier XLS et les concaténer
    for blob in blobs:
        # Télécharger le contenu du blob en tant qu'objets bytes
        blob_data = blob.download_as_bytes()

        # Vérifier si le fichier est vide avant de le lire
        if len(blob_data) > 0:
            df = pd.read_excel(blob_data)

            # Concaténation avec le dataframe principal
            concatenated_df = pd.concat([concatenated_df, df], ignore_index=True)

    return concatenated_df


def clean_evo_jj():

    # Appeler la fonction pour concaténer les données ADH
    df = concatenate_evo_jj()

    # Supprimer les lignes en doublon
    df = df.drop_duplicates()

    # Suppression des lignes avec une date exploitation vide
    df.dropna(subset=['Jour Semaine'], inplace=True)

    # Remplacer les , par un .
    replace_point = ['PBJ Total', 'PBJ MAS', 'PBJ JT']
    for col in replace_point:
        df[col] = df[col].replace(',', '.')
    df = df.replace('', '', regex=True)

    # Trouver les colonnes contenant un pourcentage (%) ou 'N-1'
    colonnes_a_supprimer = [col for col in df.columns if '%' in col or 'N-1' in col]

    # Supprimer les colonnes sélectionnées
    df = df.drop(columns=colonnes_a_supprimer)

    # Afficher le DataFrame modifié
    df.head()

    # Transformer des colonnes en float
    cols_to_convert = ['Fréq. totale', 'Fréq. tot. ident.', 'PBJ Total', 'PBJ MAS', 'PBJ JT']
    df[cols_to_convert] = df[cols_to_convert].astype(float)

    # Classer par ordre de date
    df = df.sort_values(by='Date')

    # Renommer les colonnes
    df_date = df.rename(columns={
        'Jour Semaine': 'jour',
        'Date': 'date',
        'Fréq. totale': 'freq_tot',
        'Fréq. tot. ident.': 'freq_tot_id',
        'PBJ Total': 'pbj_tot',
        'PBJ MAS': 'pbj_mas',
        'PBJ JT': 'pbj_jt'
    })

    # Suppression des lignes avec une date vide
    df_date.dropna(subset=['date'], inplace=True)

    # Conversion de la colonne 'Date' en datetime
    df_date['date'] = pd.to_datetime(df_date['date'], format='%d/%m/%Y')

    # Tri des données par date croissante
    df_evo_jj = df_date.sort_values(by='date')


    return df_evo_jj







if __name__ == '__main__':
    # Appeler la fonction pour concaténer les données ADH
    print(clean_evo_jj().info())

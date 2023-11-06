import pandas as pd
from dotenv import load_dotenv
from gcp import get_storage_client

load_dotenv() # Charger les variables d'environnement à partir du fichier .env

def concatenate_euros_players():
    # Chemin vers le dossier contenant les fichiers XLSX dans le bucket
    blob_directory = "EUROS_PLAYERS/"

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


def clean_euros_players():

    # Appeler la fonction pour concaténer les données ADH
    df = concatenate_euros_players()

    # Supprimer les lignes en doublon
    df = df.drop_duplicates()

    # Conversion de la colonne 'Date' en datetime
    df['Date exploitation'] = pd.to_datetime(df['Date exploitation'], format='%d/%m/%Y')

    # Tri des données par date croissante
    df = df.sort_values(by='Date exploitation')

    # Suppression des lignes avec une date exploitation vide
    df.dropna(subset=['Date exploitation'], inplace=True)

    # Remplacer toutes les virgules par des points dans la colonne
    df['euros Players gagnés'] = df['euros Players gagnés'].astype(str).str.replace(',', '.')
    df['euros Players restants'] = df['euros Players restants'].astype(str).str.replace(',', '.')

    # Transformer des colonnes en float
    df['euros Players gagnés'] = df['euros Players gagnés'].astype(float)
    df['euros Players restants'] = df['euros Players restants'].astype(float)

    # Ajout d'une colonne BURN
    df['burn'] = df['euros Players gagnés'] - df['euros Players restants']

    # Renommer les colonnes restantes
    df = df.rename(columns={
    "Date exploitation": "date",
    "euros Players gagnés": "earn",
    "euros Players restants": "euros_players_rest",
    "Zone": "zone"
    })

    # Remplacement des valeurs manquantes dans Zone
    df['zone'] = df['zone'].fillna('NC')

    return df






if __name__ == '__main__':
    # Appeler la fonction pour concaténer les données ADH
    print(clean_euros_players().info())

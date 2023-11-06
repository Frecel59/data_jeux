import pandas as pd
from dotenv import load_dotenv
from gcp import get_storage_client


load_dotenv() # Charger les variables d'environnement à partir du fichier .env

def concatenate_adh_data():
    # Chemin vers le dossier contenant les fichiers XLSX dans le bucket
    blob_directory = "ADH/"

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


def clean_adh_data():

    # Appeler la fonction pour concaténer les données ADH
    df = concatenate_adh_data()

    # Supprimer les lignes en doublon
    df = df.drop_duplicates()

    # Création d'un masque booléen pour sélectionner les lignes à conserver
    mask = df['Type'] != ' Total'

    # Suppression des lignes correspondant à 'Total' dans la colonne 'Type'
    df = df[mask]

    # Supprimer les colonnes "Type" et "Site"
    df = df.drop(["Type", "Site"], axis=1)

    # Renommer les colonnes restantes
    df = df.rename(columns={
        "Date": "date",
        "Sexe": "Genre",
        "Nb nouvelles adhésions": "new_adh"
    })


    return df







if __name__ == '__main__':
    # Appeler la fonction pour concaténer les données ADH
    print(clean_adh_data().info())

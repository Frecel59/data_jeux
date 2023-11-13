import pandas as pd


def get_value_from_result(df, gender):
    if len(df) > 0:
        return df[df['Genre'] == gender]['new_adh'].values[0]
    else:
        return 0

def results_adh(df, date_start, date_end, date_start_n_1_obj, date_end_n_1_obj):

    ########### Période N ###########
    # Filtrer le DataFrame en fonction des dates
    dataframe = df[(df['date'] >= date_start) & (df['date'] <= date_end)]

    # Somme du nbr d'adhésion sur la période
    result_encartage = dataframe.new_adh.sum()

    # Dataframe de répartition homme / femme
    result_genre = dataframe.groupby('Genre').agg({'new_adh': 'sum'}).reset_index()
    result_genre['proportion'] = result_genre['new_adh'] / result_genre['new_adh'].sum() * 100

    # Nbr d'ahésion par F et H pour la période N
    f_value = get_value_from_result(result_genre, 'F')
    m_value = get_value_from_result(result_genre, 'M')


    # ########### Période N-1 ###########
    dataframe_n_1 = df[(df['date'] >= date_start_n_1_obj) & (df['date'] <= date_end_n_1_obj)]

    # Somme du nbr d'adhésion sur la période
    result_encartage_n_1 = dataframe_n_1.new_adh.sum()

    # Dataframe de répartition homme / femme
    result_genre_n_1 = dataframe_n_1.groupby('Genre').agg({'new_adh': 'sum'}).reset_index()
    result_genre_n_1['proportion'] = result_genre_n_1['new_adh'] / result_genre_n_1['new_adh'].sum() * 100

    # Nbr d'ahésion par F et H pour la période N-1
    f_value_n_1 = get_value_from_result(result_genre_n_1, 'F')
    m_value_n_1 = get_value_from_result(result_genre_n_1, 'M')


    ########### Evolution ###########
    evolution_encartage = ((result_encartage - result_encartage_n_1) / result_encartage_n_1) * 100 if result_encartage_n_1 != 0 else 0

    # Vérification pour éviter la division par zéro
    evolution_f_value = ((f_value - f_value_n_1) / f_value_n_1) * 100 if f_value_n_1 != 0 else 0
    evolution_m_value = ((m_value - m_value_n_1) / m_value_n_1) * 100 if m_value_n_1 != 0 else 0




    # Créer un DataFrame avec les résultats
    result_df = pd.DataFrame({
        'Catégorie': ["Nbr d'encartages", 'Femmes', 'Hommes'],
        'N': [result_encartage, f_value, m_value],
        'N-1': [result_encartage_n_1, f_value_n_1, m_value_n_1],
        'Variation': [evolution_encartage, evolution_f_value, evolution_m_value],

    })



    # Supprimer l'index par défaut du DataFrame
    result_df1 = result_df.set_index('Catégorie')

    def format_percent(value):
        if isinstance(value, (int, float)):
            return f"{value:,.2f}%".replace(",", " ").replace(".", ",")
        else:
            return value

    # Appliquez 'format_percent' à chaque cellule de la colonne 'Variation (%)'.
    result_df1['Variation'] = result_df1['Variation'].map(format_percent)


    # Appliquer le formatage ici
    def format_numbers(value, integer_only=False):
        if isinstance(value, (int, float)):
            if isinstance(value, float) and value.is_integer() and not integer_only:
                return f"{value:,.0f}".replace(",", " ")
            else:
                return f"{value:,.0f}".replace(",", " ")
        else:
            return value


    # Pour chaque colonne, appliquez 'format_numbers' à chaque cellule de la colonne.
    for col in ['N', 'N-1']:
        result_df1[col] = result_df1[col].map(lambda x: format_numbers(x, integer_only=True))


    return result_df, result_df1

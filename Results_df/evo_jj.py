import pandas as pd


def results_evo_jj(df, date_start, date_end, date_start_n_1_obj, date_end_n_1_obj):

    ########### Période N ###########
    # Filtrer le DataFrame en fonction des dates
    # Filtrer le DataFrame en fonction des dates
    dataframe = df[(df['date'] >= date_start) & (df['date'] <= date_end)]

    # Calculer la somme de chaque colonne
    sum_freq_tot = dataframe['freq_tot'].sum()
    sum_freq_tot_id = dataframe['freq_tot_id'].sum()
    sum_pbj_tot = dataframe['pbj_tot'].sum()
    sum_pbj_mas = dataframe['pbj_mas'].sum()
    sum_pbj_jt = dataframe['pbj_jt'].sum()

    # sum_freq_tot = "{:,.0f}".format(filtre_evo_jj['freq_tot'].sum()).replace(",", " ")
    # sum_freq_tot_id = "{:,.0f}".format(filtre_evo_jj['freq_tot_id'].sum()).replace(",", " ")
    # sum_pbj_tot = "{:,.2f}".format(filtre_evo_jj['pbj_tot'].sum()).replace(",", " ")
    # sum_pbj_mas = "{:,.2f}".format(filtre_evo_jj['pbj_mas'].sum()).replace(",", " ")
    # sum_pbj_jt = "{:,.2f}".format(filtre_evo_jj['pbj_jt'].sum()).replace(",", " ")


    ########### Période N-1 ###########
    # Filtrer le DataFrame en fonction des dates
    dataframe_n_1 = df[(df['date'] >= date_start_n_1_obj) & (df['date'] <= date_end_n_1_obj)]

    # Calculer la somme de chaque colonne
    sum_freq_tot_n_1 = dataframe_n_1['freq_tot'].sum()
    sum_freq_tot_id_n_1 = dataframe_n_1['freq_tot_id'].sum()
    sum_pbj_tot_n_1 = dataframe_n_1['pbj_tot'].sum()
    sum_pbj_mas_n_1 = dataframe_n_1['pbj_mas'].sum()
    sum_pbj_jt_n_1 = dataframe_n_1['pbj_jt'].sum()

    # sum_freq_tot_n_1 = "{:,.0f}".format(filtre_evo_jj_n_1['freq_tot'].sum()).replace(",", " ")
    # sum_freq_tot_id_n_1 = "{:,.0f}".format(filtre_evo_jj_n_1['freq_tot_id'].sum()).replace(",", " ")
    # sum_pbj_tot_n_1 = "{:,.2f}".format(filtre_evo_jj_n_1['pbj_tot'].sum()).replace(",", " ")
    # sum_pbj_mas_n_1 = "{:,.2f}".format(filtre_evo_jj_n_1['pbj_mas'].sum()).replace(",", " ")
    # sum_pbj_jt_n_1 = "{:,.2f}".format(filtre_evo_jj_n_1['pbj_jt'].sum()).replace(",", " ")


    ########### Evolution JJ ###########
    evolution_freq_tot = ((sum_freq_tot - sum_freq_tot_n_1) / sum_freq_tot_n_1) * 100 if sum_freq_tot_n_1 != 0 else 0
    evolution_freq_tot_id = ((sum_freq_tot_id - sum_freq_tot_id_n_1) / sum_freq_tot_id_n_1) * 100 if sum_freq_tot_id_n_1 != 0 else 0
    evolution_pbj_tot = ((sum_pbj_tot - sum_pbj_tot_n_1) / sum_pbj_tot_n_1) * 100 if sum_pbj_tot_n_1 != 0 else 0
    evolution_pbj_mas = ((sum_pbj_mas - sum_pbj_mas_n_1) / sum_pbj_mas_n_1) * 100 if sum_pbj_mas_n_1 != 0 else 0
    evolution_pbj_jt = ((sum_pbj_jt - sum_pbj_jt_n_1) / sum_pbj_jt_n_1) * 100 if sum_pbj_jt_n_1 != 0 else 0

    # Créer un DataFrame avec les résultats
    result_df = pd.DataFrame({
        'Catégorie': ["Fréq total", 'Freq total id', 'PBJ tot', 'PBJ MAS', 'PBJ JT'],
        'N': [sum_freq_tot, sum_freq_tot_id, sum_pbj_tot, sum_pbj_mas, sum_pbj_jt],
        'N-1': [sum_freq_tot_n_1, sum_freq_tot_id_n_1, sum_pbj_tot_n_1, sum_pbj_mas_n_1, sum_pbj_jt_n_1],
        'Variation': [evolution_freq_tot, evolution_freq_tot_id, evolution_pbj_tot, evolution_pbj_mas, evolution_pbj_jt],

    })

    result_evo_jj = result_df
    # Supprimer l'index par défaut du DataFrame
    result_evo_jj1 = result_evo_jj.set_index('Catégorie')

    def format_percent(value):
        if isinstance(value, (int, float)):
            return f"{value:,.2f}%".replace(",", " ").replace(".", ",")
        else:
            return value

    # Appliquez 'format_percent' à chaque cellule de la colonne 'Variation (%)'.
    result_evo_jj1['Variation'] = result_evo_jj1['Variation'].map(format_percent)


    # Appliquer le formatage ici
    def format_numbers(value):
        if isinstance(value, (int, float)):
            if value.is_integer():
                return f"{value:,.0f}".replace(",", " ")
            else:
                return f"{value:,.2f}".replace(",", " ").replace(".", ",")
        else:
            return value

    # Pour chaque colonne, appliquez 'format_numbers' à chaque cellule de la colonne.
    for col in ['N', 'N-1']:
        result_evo_jj1[col] = result_evo_jj1[col].map(format_numbers)



    return result_evo_jj, result_evo_jj1

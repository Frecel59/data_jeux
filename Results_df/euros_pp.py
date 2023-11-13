import pandas as pd


def results_euros_pp(df, date_start, date_end, date_start_n_1_obj, date_end_n_1_obj):


    ########### Période N ###########
    # Filtrer le DataFrame en fonction des dates
    dataframe = df[(df['date'] >= date_start) & (df['date'] <= date_end)]

    df_groupby_euros_players = dataframe.groupby('zone')\
        .agg({'earn': 'sum', 'euros_players_rest': 'sum', 'burn': 'sum'\
            }).reset_index()

    df_groupby_euros_players = df_groupby_euros_players.groupby('zone')\
        .agg({'earn': 'sum', 'euros_players_rest': 'sum', 'burn': 'sum'\
            }).reset_index()
    df_groupby_euros_players[['earn', 'euros_players_rest', 'burn']] = \
        df_groupby_euros_players[['earn', 'euros_players_rest', 'burn']]\
            .apply(lambda x: x.apply('{:,.2f}'.format).str.replace\
                (',', ' '))

    # Afficher le total earn arrondie
    df_groupby_euros_players['earn'] = df_groupby_euros_players['earn']\
        .str.replace(' ', '').astype(float)
    total_earn = df_groupby_euros_players['earn'].sum()
    # total_earn_formatted = "{:,.2f}".format(total_earn).replace(",", " ")

    # Afficher le total brun arrondie
    df_groupby_euros_players['burn'] = df_groupby_euros_players['burn']\
        .str.replace(' ', '').astype(float)
    total_burn = df_groupby_euros_players['burn'].sum()
    # total_burn_formatted = "{:,.2f}".format(total_burn).replace(",", " ")

    ########### Période N-1 ###########
    # Filtrer le DataFrame en fonction des dates
    dataframe_n_1 = df[(df['date'] >= date_start_n_1_obj) & (df['date'] <= date_end_n_1_obj)]

    df_groupby_euros_players_n_1 = dataframe_n_1.groupby('zone')\
        .agg({'earn': 'sum', 'euros_players_rest': 'sum', 'burn': 'sum'\
            }).reset_index()

    df_groupby_euros_players_n_1 = df_groupby_euros_players_n_1.groupby('zone')\
        .agg({'earn': 'sum', 'euros_players_rest': 'sum', 'burn': 'sum'\
            }).reset_index()
    df_groupby_euros_players_n_1[['earn', 'euros_players_rest', 'burn']] = \
        df_groupby_euros_players_n_1[['earn', 'euros_players_rest', 'burn']]\
            .apply(lambda x: x.apply('{:,.2f}'.format).str.replace\
                (',', ' '))

    # Afficher le total earn arrondie
    df_groupby_euros_players_n_1['earn'] = df_groupby_euros_players_n_1['earn']\
        .str.replace(' ', '').astype(float)
    total_earn_n_1 = df_groupby_euros_players_n_1['earn'].sum()

    evolution_earn = ((total_earn - total_earn_n_1) / total_earn_n_1) * 100 if total_earn_n_1 != 0 else 0

    # total_earn_n_1_formatted = "{:,.2f}".format(total_earn_n_1).replace(",", " ")

    # Afficher le total brun arrondie
    df_groupby_euros_players_n_1['burn'] = df_groupby_euros_players_n_1['burn']\
        .str.replace(' ', '').astype(float)
    total_burn_n_1 = df_groupby_euros_players_n_1['burn'].sum()

    evolution_burn = ((total_burn - total_burn_n_1) / total_burn_n_1) * 100 if total_burn_n_1 != 0 else 0

    # total_burn_n_1_formatted = "{:,.2f}".format(total_burn_n_1).replace(",", " ")


    # Créer un DataFrame avec les résultats
    result_euros_pp = pd.DataFrame({
        'Catégorie': ["Earn", 'Burn'],
        'N': [total_earn, total_burn],
        'N-1': [total_earn_n_1, total_burn_n_1],
        'Variation': [evolution_earn, evolution_burn],

    })

    # Supprimer l'index par défaut du DataFrame
    result_euros_pp_1 = result_euros_pp.set_index('Catégorie')


    def format_percent(value):
        if isinstance(value, (int, float)):
            return f"{value:,.2f}%".replace(",", " ").replace(".", ",")
        else:
            return value

    # Appliquez 'format_percent' à chaque cellule de la colonne 'Variation (%)'.
    result_euros_pp_1['Variation'] = result_euros_pp_1['Variation'].map(format_percent)


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
        result_euros_pp_1[col] = result_euros_pp_1[col].map(format_numbers)


    return result_euros_pp, result_euros_pp_1

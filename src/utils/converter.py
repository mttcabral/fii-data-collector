import pandas as pd
import json

"""
# This file holds all logic related to conversion (e.g. file A -> B)
"""


def html_table_to_json(html_content):
    # pd.read_html return a list of DataFrames, in the html code "table_ifix"
    # there is just one table, so the slicing after the command is to pass
    # the dataframe instead of a list with just one DataFrame
    df_table_ifix = pd.read_html(html_content, decimal=',', thousands='.')[0]

    # Dropping undesired columns
    df_table_ifix = df_table_ifix.drop(
        columns=["Ação", "Tipo", "Qtde. Teórica"]
    )

    # Dropping undesired rows
    number_of_rows = df_table_ifix.shape[0]
    rows_to_drop = [(number_of_rows-1), (number_of_rows-2)]
    df_table_ifix = df_table_ifix.drop(rows_to_drop)

    # Removing '11' after every id
    df_table_ifix['Código'] = df_table_ifix['Código'].str[0:4]

    # DataFrame to dict
    dict_table_ifix = df_table_ifix.set_index(
        "Código").to_dict()['Part. (%)']

    # Writing the dict as JSON
    with open('data/FII_id_and_participation.json', 'w') as file:
        json.dump(dict_table_ifix, file)

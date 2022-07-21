from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import pandas as pd


"""
# This method will write a JSON file, where the key will be the
# 'FII' code, and the value the closing quotation of that 'FII'
"""


def scrape_closing_quotation():

    fii_closing_quotation_dict = {}
    fii_code_list = get_fii_code_list()
    # Must be MM/YYYY
    date = '05/2022'

    # Setting up browser
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    # The B3's stores the closing quotation in the following url
    base_url = 'https://bvmf.bmfbovespa.com.br/SIG/FormConsultaMercVista.asp?strTipoResumo=RES_MERC_VISTA&strSocEmissora={fii_name}&strDtReferencia={date}&strIdioma=P&intCodNivel=2&intCodCtrl=160'  # noqa: E501

    for x in range(len(fii_code_list)):
        # By using a placeholder, the bot can search for the
        # desired 'FII' at the desired date
        url = base_url.format(fii_name=fii_code_list[x], date=date)

        # Accessing formatted url
        browser.get(url)

        try:
            # Wait until the table loads
            WebDriverWait(browser, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="tblResDiario"]/tbody/tr[2]/td/table/tbody')))  # noqa: E501
        except:
            print("bot2: Table not found!")

        """
        # In B3's site there is a table containing the closing quotation, it
        # is stored in the 'desired_row' and 'desired_column'
        """

        # Getting the number of rows in the table
        number_of_rows = len(browser.find_elements(
            By.XPATH, '//*[@id="tblResDiario"]/tbody/tr[2]/td/table/tbody/tr'))

        # Taking the XPATH for the penultimate row, i.e. the row
        # containing  the closing quotation of that 'FII', it
        # is done by taking the number of rows in the
        # table, subtracting 1, and assign the row index to that number
        desired_row_xpath = '//*[@id="tblResDiario"]/tbody/tr[2]/td/table/tbody/tr[{penultimate_row}]'.format(  # noqa: E501
            penultimate_row=(number_of_rows-1))

        number_of_columns = len(browser.find_elements(
            By.XPATH, (desired_row_xpath+'/td')))

        # Taking the XPATH for the last column of 'desired_row'
        desired_column_xpath = (
            desired_row_xpath+'/td[{last_column}]').format(last_column=(number_of_columns))  # noqa: E501

        # Scraping the text contained in the 'desired_row' and 'desired_column'
        closing_quotation = browser.find_element(
            By.XPATH, desired_column_xpath).get_attribute("innerText")

        # The 'FII' of name 'x' have a 'closing_quotation'
        fii_closing_quotation_dict[fii_code_list[x]] = closing_quotation

    browser.quit()

    # Writing the dict as JSON
    with open('data/FII_closing_quotation.json', 'w') as file:
        json.dump(fii_closing_quotation_dict, file)


def get_fii_code_list():
    with open('data/table_ifix.html', 'r') as file:
        table_ifix = file.read()
        file.close()

    # pd.read_html return a list of DataFrames, in the html code "table_ifix"
    # there is just one table, so the slicing after the command is to pass
    # the dataframe instead of a list with just one DataFrame
    df_table_ifix = pd.read_html(table_ifix)[0]

    # Dropping undesired columns
    df_table_ifix = df_table_ifix.drop(
        columns=["Ação", "Part. (%)", "Tipo", "Qtde. Teórica"]
    )

    # Dropping undesired rows
    number_of_rows = df_table_ifix.shape[0]
    rows_to_drop = [(number_of_rows-1), (number_of_rows-2)]
    df_table_ifix = df_table_ifix.drop(rows_to_drop)

    fii_code_list = []

    for x in range(0, len(df_table_ifix.values.tolist())):
        fii_code_list.append(df_table_ifix.values.tolist()[x][0][0:4])

    return fii_code_list

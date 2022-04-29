import time

from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd


def scraping_html():
    """
    This bot is made to collect ID and percentage participation of IFIX from B3's site by
    using HTML code
    """

    url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/theorical/IFIX?language=pt-br'

    # Defining Firefox's options
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    # Browser access the url and refresh it
    browser.get(url)
    # Wait until the browser opens
    time.sleep(5)
    browser.refresh()

    # Wait until the page loads completely before select an option
    time.sleep(3)

    # By default the table is set to 20 elements per page, by using this command, selenium
    # set 120 elements per page, which means that there is just 1 page to scrape
    select_element = browser.find_element(By.XPATH, '//*[@id="selectPage"]')
    select_object = Select(select_element)

    # Try to select the last option, if any exception occurs, then select the "120 elements per page" option
    try:
        all_available_options = select_object.options
        index_of_last_option = (len(all_available_options) - 1)
        select_object.select_by_index(index_of_last_option)
    except:
        select_object.select_by_visible_text('120')

    # Find the table
    table = browser.find_element(By.TAG_NAME, "table")

    # Get the HTML code of the table
    html_content = table.get_attribute('outerHTML')

    # Wait until the whole process ends before exiting the browser
    time.sleep(5)

    browser.quit()

    soup = BeautifulSoup(html_content, 'html.parser')

    table_ifix = soup.find()

    with open("/home/mats/Desktop/table_ifix.html", "w") as file:
        file.write(str(table_ifix))


def html_table_to_dataframe():
    with open("../../../Desktop/table_ifix.html", "r") as file:
        table_ifix = file.read()
        file.close()

    # pd.read_html return a list of DataFrames, in the html code "table_ifix" there is just
    # one table, so the slicing after the command is to pass the dataframe instead of a list with
    # just one DataFrame
    df_table_ifix = pd.read_html(table_ifix)[0]

    df_table_ifix = df_table_ifix.drop(columns=["Ação", "Part. (%)", "Tipo", "Qtde. Teórica"])
    df_table_ifix = df_table_ifix.drop([103, 104])

    code_list_of_REIT = []

    for x in range(0, len(df_table_ifix.values.tolist())):
        code_list_of_REIT.append(df_table_ifix.values.tolist()[x][0][0:4])

    print(code_list_of_REIT)
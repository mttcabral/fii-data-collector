import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.by import By


def scraping_html():
    # This bot is made to collect ID and percentage participation
    # of IFIX from B3's site by using HTML code

    url = "https://sistemaswebb3-listados.b3.com.br/indexPage/theorical/IFIX?language=pt-br"

    # Setting up browser
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    # Accessing url
    browser.get(url)
    # Wait until the browser opens
    time.sleep(5)
    # Refreshing the page
    browser.refresh()

    # Wait until the page loads completely before select an option
    time.sleep(3)

    # By default the table is set to 20 elements per page, by
    # using this command, selenium set 120 elements per page, which
    # means that there is just 1 page to scrape
    select_element = browser.find_element(By.XPATH, '//*[@id="selectPage"]')
    select_object = Select(select_element)

    # Try to select the last option, if any exception occurs, then
    # select the "120 elements per page" option
    try:
        all_available_options = select_object.options
        index_of_last_option = len(all_available_options) - 1
        select_object.select_by_index(index_of_last_option)
    except:
        select_object.select_by_visible_text("120")

    # Find the table
    table = browser.find_element(By.TAG_NAME, "table")

    # Get the HTML code of the table
    html_content = table.get_attribute("outerHTML")

    # Wait until the whole process ends before exiting the browser
    time.sleep(5)

    browser.quit()

    soup = BeautifulSoup(html_content, "html.parser")

    table_ifix = soup.find()

    with open("table_ifix.html", "w") as file:
        file.write(str(table_ifix))


def html_table_to_dataframe():
    with open("table_ifix.html", "r") as file:
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

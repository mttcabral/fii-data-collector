from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import json

from date import get_period
from utils import converter, get_fii_id_list

"""
# This file holds all scraping-related logic
"""


def scrape_id_and_participation():
    """
    # Function task: scrape the ID and participation (in %)
    # of each 'FII' (from B3's site) and save it as a HTML file
    """

    url = "https://sistemaswebb3-listados.b3.com.br/indexPage/theorical/IFIX?language=pt-br"  # noqa: E501

    # Setting up browser
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    # Accessing url and refreshing the page
    browser.get(url)
    browser.refresh()

    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="divContainerIframeB3"]/div/div[1]/form/div[3]/div/table/tbody')))  # noqa: E501
    except:
        try:
            browser.refresh()
            WebDriverWait(browser, 20).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="divContainerIframeB3"]/div/div[1]/form/div[3]/div/table/tbody')))  # noqa: E501
        except:
            print("scrape_id_and_participation(): Table not found!")

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

    browser.quit()

    # Output to JSON file
    converter.html_table_to_json(html_content)


def scrape_closing_quotation():
    """
    # Function task: scrape the closing quotation and
    # save it in a JSON file, where the key is the 'FII'
    # ID, and the value is the closing quotation of that 'FII'
    """

    fii_closing_quotation_dict = {}
    fii_id_list = get_fii_id_list.get_fii_id_list()
    # Must be MM/YYYY
    date = '07/2022'

    # Setting up browser
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    # The B3's stores the closing quotation in the following url
    base_url = 'https://bvmf.bmfbovespa.com.br/SIG/FormConsultaMercVista.asp?strTipoResumo=RES_MERC_VISTA&strSocEmissora={fii_name}&strDtReferencia={date}&strIdioma=P&intCodNivel=2&intCodCtrl=160'  # noqa: E501

    for x in range(len(fii_id_list)):
        # By using a placeholder, the bot can search for the
        # desired 'FII' at the desired date
        url = base_url.format(fii_name=fii_id_list[x], date=date)

        # Accessing formatted url
        browser.get(url)

        try:
            # Wait until the table loads
            WebDriverWait(browser, 10).until(EC.presence_of_element_located(
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
        fii_closing_quotation_dict[fii_id_list[x]] = float(
            closing_quotation.replace(',', '.'))

    browser.quit()

    # Writing the dict as JSON
    with open('data/FII_closing_quotation.json', 'w') as file:
        json.dump(fii_closing_quotation_dict, file)


def scrape_proceeds(fii, from_date, to_date):
    """
    # Function task: scrape the proceeds
    # Note: The translation (Portuguese (provento) -> English  (proceeds))
    # might not be very accurate
    #
    # The main logic is from Pedro Lucas Paulino
    # GitHub link: https://github.com/PLPaulino
    """

    print(f"\nFII: {fii}")

    option = Options()
    option.headless = True
    browser = webdriver.Firefox(options=option)

    # Changing date format from dd/mm/yyyy to yyyy/mm/dd
    from_date = from_date.split(
        '/')[2] + '-' + from_date.split('/')[1] + '-' + from_date.split('/')[0]
    to_date = to_date.split(
        '/')[2] + '-' + to_date.split('/')[1] + '-' + to_date.split('/')[0]

    url = f'https://sistemasweb.b3.com.br/PlantaoNoticias/Noticias/ListarTitulosNoticias?agencia=18&palavra={fii}&dataInicial={from_date}&dataFinal={to_date}'
    browser.get(url)

    # The place where the proceeds can be found is called "Notícias"
    # (B3's nomenclature) where "Notícias" (Portuguese) means "News" (English)
    news_json = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body")))
    html_json = news_json.get_attribute('outerHTML')
    soup_json = BeautifulSoup(html_json, 'html.parser')

    dict_news = json.loads(soup_json.text)

    news_credentials = []
    identifier = "Aviso aos Cotistas"

    # List of news containing the identifier
    desired_news = (list(filter(lambda dict: identifier in str(
        dict['NwsMsg']['headline']), dict_news)))

    # The desired_news is the one containing "N"
    # at the end
    for x in range(len(desired_news)):
        if (desired_news[x]['NwsMsg']['headline'][-2] == 'N'):
            id_news = desired_news[x]['NwsMsg']['id']
            date_news = desired_news[x]['NwsMsg']['dateTime']
            break

    news_credentials.append(id_news)
    news_credentials.append(date_news)

    # Applying the 'news_credentials' to get the correct url
    url = f'https://sistemasweb.b3.com.br/PlantaoNoticias/Noticias/Detail?idNoticia={news_credentials[0]}&agencia=18&dataNoticia={news_credentials[1]}'
    browser.get(url)

    # The link for the table is inside <pre> (HTML Tag)
    pre_tag = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "conteudoDetalhe")))
    pre_tag_html = pre_tag.get_attribute('outerHTML')
    soup_pre_tag = BeautifulSoup(pre_tag_html, 'html.parser')

    # Collecting all links inside <pre> tag
    for a_tag in soup_pre_tag.findAll('a'):
        links = str(a_tag['href']).split('=')
        id_table = links[1]

    url_table = 'https://fnet.bmfbovespa.com.br/fnet/publico/exibirDocumento?id=' + \
        id_table+'&#toolbar=0'

    browser.get(url_table)

    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/table[2]')))

    table = browser.find_element(By.XPATH, '/html/body/table[2]')
    table_html = table.get_attribute('outerHTML')
    soup_table = BeautifulSoup(table_html, 'html.parser')

    # Scraping the data inside the table
    data = []
    for span in soup_table.findAll('span', class_='dado-valores'):
        data.append(span.text)

    proceeds = data[5].replace(',', '.')
    proceeds = {fii: proceeds}

    return proceeds


def bot3():
    period = get_period()
    from_date = period[0]
    to_date = period[1]

    fii = get_fii_id_list.get_fii_id_list()[2]
    dados_bot1 = scrape_proceeds(fii, from_date, to_date)

    print(dados_bot1)

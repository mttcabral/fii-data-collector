from bot2 import get_fii_code_list
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from date import get_period
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

"""
# This bot will collect the proceeds
# Note: The translation (Portuguese (provento) -> English  (proceeds)) might
# not be very accurate
#
# The main logic is from Pedro Lucas Paulino
# GitHub link: https://github.com/PLPaulino
"""


def scrape_proceeds(fii, from_date, to_date):

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

    fii = get_fii_code_list()[2]
    dados_bot1 = scrape_proceeds(fii, from_date, to_date)

    print(dados_bot1)


bot3()

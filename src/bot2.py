from bot1 import html_table_to_dataframe
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def collect_dividend_yield():
    fii_code_list = html_table_to_dataframe()
    test_date = '01/2022'

    url = 'https://bvmf.bmfbovespa.com.br/SIG/FormConsultaMercVista.asp?strTipoResumo=RES_MERC_VISTA&strSocEmissora={fii_name}&strDtReferencia={date}&strIdioma=P&intCodNivel=2&intCodCtrl=160'
    url = url.format(fii_name=fii_code_list[0], date=test_date)

    # Setting up browser
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    # Accessing url
    browser.get(url)

    # Code for test purposes
    value = browser.find_element(
        By.XPATH, '/html/body/table[3]/tbody/tr/td/table/tbody/tr/td/table[1]/tbody/tr[2]/td/table/tbody/tr[23]/td[12]')

    print(value.get_attribute('outerHTML'))

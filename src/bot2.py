from bot1 import html_table_to_dataframe
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def collect_closing_quotation():
    # This method will return a dictionary, where the key will be the
    # 'FII' code, and the value the closing quotation of that 'FII'

    fii_closing_quotation_dict = {}
    fii_code_list = html_table_to_dataframe()
    # Must be MM/YYYY
    date = '05/2022'

    # Setting up browser
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    # The B3's stores the closing quotation in the following url
    url = 'https://bvmf.bmfbovespa.com.br/SIG/FormConsultaMercVista.asp?strTipoResumo=RES_MERC_VISTA&strSocEmissora={fii_name}&strDtReferencia={date}&strIdioma=P&intCodNivel=2&intCodCtrl=160'

    # -------------------------------------------------------------------------------
    # By using a placeholder, the bot can search for the
    # desired 'FII' at the desired date
    url = url.format(fii_name=fii_code_list[0], date=date)

    # Accessing formatted url
    browser.get(url)

    try:
        value = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="tblResDiario"]/tbody/tr[2]/td/table'))
        )
    except:
        print("Error!")

    # Code for test purposes

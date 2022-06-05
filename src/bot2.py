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

    # By using a placeholder, the bot can search for the
    # desired 'FII' at the desired date
    url = url.format(fii_name=fii_code_list[0], date=date)

    # Accessing formatted url
    browser.get(url)

    try:
        # Wait until the table loads
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="tblResDiario"]/tbody/tr[2]/td/table/tbody')))

        # Getting all the rows contained in the table
        rows = browser.find_elements(
            By.XPATH, '//*[@id="tblResDiario"]/tbody/tr[2]/td/table/tbody/tr')
    except:
        print("Error!")

    # Taking the penultimate row, i.e. the row containing the closing
    # quotation of that 'FII', it is done by taking the number of rows in the
    # table, subtracting 1, and assign the row index to that number
    xpath = '//*[@id="tblResDiario"]/tbody/tr[2]/td/table/tbody/tr[{penultimate_row}]'
    xpath = xpath.format(penultimate_row=(len(rows)-1))

    desired_row = browser.find_element(By.XPATH, xpath)

    print(desired_row.get_attribute("outerHTML"))

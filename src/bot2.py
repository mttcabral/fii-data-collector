from bot1 import html_table_to_dataframe
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_closing_quotation():
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
    base_url = 'https://bvmf.bmfbovespa.com.br/SIG/FormConsultaMercVista.asp?strTipoResumo=RES_MERC_VISTA&strSocEmissora={fii_name}&strDtReferencia={date}&strIdioma=P&intCodNivel=2&intCodCtrl=160'

    for x in range(len(fii_code_list)):
        if(x != 0):
            print('\n\n')
        print('length of FII code list: '+str(len(fii_code_list)))
        print('FII name: '+fii_code_list[x])
        print('FII list: ', fii_code_list)
        print('x: '+str(x))

        # By using a placeholder, the bot can search for the
        # desired 'FII' at the desired date
        url = base_url.format(fii_name=fii_code_list[x], date=date)

        print('\n'+url)

        # Accessing formatted url
        browser.get(url)

        try:
            # Wait until the table loads
            WebDriverWait(browser, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="tblResDiario"]/tbody/tr[2]/td/table/tbody')))
        except:
            print("bot2: Table not found!")

        # Getting all the rows contained in the table
        rows = browser.find_elements(
            By.XPATH, '//*[@id="tblResDiario"]/tbody/tr[2]/td/table/tbody/tr')

        # Taking the penultimate row, i.e. the row containing the closing
        # quotation of that 'FII', it is done by taking the number of rows in the
        # table, subtracting 1, and assign the row index to that number
        desired_row_xpath = '//*[@id="tblResDiario"]/tbody/tr[2]/td/table/tbody/tr[{penultimate_row}]'
        desired_row_xpath = desired_row_xpath.format(
            penultimate_row=(len(rows)-1))

        desired_row = browser.find_element(By.XPATH, desired_row_xpath)

        columns = browser.find_elements(By.XPATH, (desired_row_xpath+'/td'))

        desired_column_xpath = desired_row_xpath+'/td[{last_column}]'
        desired_column_xpath = desired_column_xpath.format(
            last_column=(len(columns)))

        desired_column = browser.find_element(By.XPATH, desired_column_xpath)

        closing_quotation = desired_column.get_attribute("innerText")

        # browser.quit()

        fii_closing_quotation_dict[fii_code_list[x]] = closing_quotation

        print(fii_closing_quotation_dict)

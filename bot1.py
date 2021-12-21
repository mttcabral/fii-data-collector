import time

from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.by import By


def scraping_html():
    """
    This bot is made to collect ID and percentage participation of IFIX from B3's site by
    using HTML code
    """

    url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/theorical/IFIX?language=pt-br'

    # Defining Firefox's options
    options = Options()
    options.headless = False
    browser = webdriver.Firefox(options=options)

    # Browser access the url and refresh it
    browser.get(url)
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

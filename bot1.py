# This bot is made to collect ID and percentage participation of IFIX from B3's site

from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By


def scraping_csv_file():
    url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/day/IFIX?language=pt-br'

    options = Options()
    options.headless = False
    browser = webdriver.Firefox(options=options)

    browser.get(url)

    # Downloading the CSV file
    browser.find_element(By.XPATH,'//*[@id="divContainerIframeB3"]/div/div[2]/app-menu-portfolio/div/ul/li[1]/a').click()
    browser.find_element(By.XPATH,'//*[@id="divContainerIframeB3"]/div/div[1]/form/div[3]/div/div[2]/div/div/div[1]/div[2]/p/a').click()
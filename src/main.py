from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

import scraper
from utils import dir_handler

if __name__ == '__main__':
    dir_handler.create_data_dir()

    # Setting up browser
    options = Options()
    options.headless = False
    browser = webdriver.Firefox(
        options=options, executable_path=GeckoDriverManager().install())

    scraper.scrape_id_and_participation(browser)
    scraper.scrape_closing_quotation(browser)
    scraper.scrape_proceeds(browser)

    browser.quit()

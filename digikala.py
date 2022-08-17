from base_scraper import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import config
import pandas as pd


class digi(ScrapperSelenium):

    def __init__(self, h_url, db_name=None, con=None):
        super(digi, self).__init__()
        self.website = h_url
        # self.db = DBHandler(db_name, con)

    def fetch_product_page(self, symbol):
        sleep_time = 2
        self.driver.get(self.website.format(s=symbol))

    def sort_in_order(self,order):
        btn = self.fetch_element(By.XPATH, config.symbol_to_search[order])
        self.driver.execute_script("arguments[0].click();", btn)
        page_in_order = self.fetch_element(By.XPATH, config.most_visited_btn)

    def products_details(self):
        pass


    def insert_page_to_db(self, tbl, table):
        tbl = tbl.split('\n')
        for line in tbl:
            if line[0] != '0':
                line = line.replace('/', '-')
                line = line.replace(',', '').split(' ')
                row = f'{line[0]},{line[2]},{line[1]},{line[3]},\'{line[6]}\',\'{line[7]}\''
                self.db.insert_row(table, row)



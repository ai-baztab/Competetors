from base_scraper import *
from selenium.webdriver.common.by import By
from base_db import DBHandler
import time
import config
import pandas as pd


class digi(ScrapperSelenium):

    def __init__(self, h_url, db_name=None, con=None):
        super(digi, self).__init__()
        self.website = h_url
        # self.db = DBHandler(db_name, con)

    def search_for(self, symbol):
        sleep_time = 2
        self.driver.get(self.website.format(s=symbol))
        most_visited_btn_order = self.fetch_element(By.XPATH, config.most_visited_btn)
        most_sold_btn_order = self.fetch_element(By.XPATH, config.most_sold_btn)
        self.driver.execute_script("arguments[0].click();", most_visited_btn_order)
        proucts = self.fetch_element(By.XPATH, config.most_visited_btn)
    def items(self, symbol, date_from, date_to):
        sleep_time = 2
        self.driver.get(self.website.format(s=symbol))
        date_from_id = config.date_from_id
        date_to_id = config.date_to_id
        price_list_id = config.price_list_id
        dt = self.fetch_element(By.ID, date_from_id)
        dt.send_keys(date_from)
        self.fetch_element(By.ID, date_to_id).send_keys(date_to)
        paginate_buttons = self.fetch_element(By.ID, config.btns_id)
        next_btn = self.fetch_element(By.ID, config.btn_next)
        list_of_buttons_str = paginate_buttons.text
        total_pages = self.total_pages(list_of_buttons_str)
        self.db.create_table(config.table_name, config.create_command)
        for i in range(total_pages):
            table = self.fetch_element(By.ID, price_list_id)
            table_str = table.text
            self.insert_page_to_db(table_str, config.table_name)
            try:
                self.driver.execute_script("arguments[0].click();", next_btn)
            except:
                next_btn = self.fetch_element(By.ID, config.btn_next)
                self.driver.execute_script("arguments[0].click();", next_btn)
                sleep_time += 1
            time.sleep(sleep_time)
            next_btn = self.fetch_element(By.ID, config.btn_next)

    @staticmethod
    def total_pages(string):
        next_btn = string.index('بعدی')
        etc_str = string.index('…') + 1
        return int(string[etc_str:next_btn])

    def insert_page_to_db(self, tbl, table):
        tbl = tbl.split('\n')
        for line in tbl:
            if line[0] != '0':
                line = line.replace('/', '-')
                line = line.replace(',', '').split(' ')
                row = f'{line[0]},{line[2]},{line[1]},{line[3]},\'{line[6]}\',\'{line[7]}\''
                self.db.insert_row(table, row)

    def show_table(self, table):
        df = self.db.sql_to_df(table)
        df.datee = pd.to_datetime(df.datee)
        df = df.set_index('datee')
        df = df.drop('datef', axis=1)
        df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close"},
                  inplace=True)
        df = df.iloc[::-1]
        ap = mlp.make_addplot(df['Close'])
        mlp.plot(
            df,
            type='candle',
            addplot=ap
        )

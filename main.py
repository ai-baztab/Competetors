import config
from digikala import digi
import psycopg2
import config

if __name__ == '__main__':

    # conn = psycopg2.connect(database='tgu', user='postgres', password='1372', host='127.0.0.1', port='5432')
    # conn.autocommit = True
    selenium = digi(config.url, None, None)
    selenium.historical_data_wrapper(config.symbol_to_search, config.from_date, config.to_date)
    selenium.show_table(config.table_name)
    print("final")


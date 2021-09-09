from oddsbook.sqlitedb import SqliteDB
import time as timer
from oddsbook import booker
from oddsbook import scraper

def run(driver_path:str = './chromedriver.exe', lang:str='ch', delay: int = 3):

    hkjc_scraper = scraper.HKJCScraper(driver_path, lang, delay)
    scrapers = (hkjc_scraper.scrap_homedrawaway, hkjc_scraper.scrap_handicap, hkjc_scraper.scrap_hilo, hkjc_scraper.scrap_cornerhilo)
    sqlitedb = SqliteDB()

    for s in scrapers:
        odds = s()
        if odds:
            sqlitedb.add_all(odds)
            print(odds)
            booker.populatebook(odds)


import argparse
import logging
from datetime import datetime

parser = argparse.ArgumentParser(description=r"Scrapping Odds infomation and populating to OddsBook.xlsx")
parser.add_argument('-i', '--interval', type=int, default=0, help=r"Minutes of interval for updating odds after each run.")
parser.add_argument('-d', '--delay', type=int, default=3, help=r"Seconds of delay on webscraping.")
parser.add_argument('-l', '--lang', type=str, default='ch', help=r"Language of webpage to parse.")
parser.add_argument('--webdriver', type=str, default='./chromedriver.exe', help=r"Path of the webdriver executable.")
parser.add_argument('--debug', action='store_true', help=r"Log debug message.")
argv = parser.parse_args()

if __name__ == "__main__":

    logging.basicConfig(filename='oddsbook.log', filemode='w', level=logging.DEBUG if argv.debug else logging.INFO)

    while True:
        logging.info(f"Start Running at {datetime.now()}")
        logging.debug(argv)
        try:
            run(argv.webdriver, argv.lang, argv.delay)
            logging.info("Run Successful!")
            if argv.interval > 0: break
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
        finally:
            timer.sleep(argv.interval * 60)
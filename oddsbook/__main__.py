import time as timer
from oddsbook import booker
from oddsbook import scraper

def run(delay: int = 3, driver_path:str = './chromedriver.exe'):

    hkjc_scraper = scraper.HKJCScraper(driver_path)
    scrapers = (hkjc_scraper.scrap_homedrawaway, hkjc_scraper.scrap_handicap, hkjc_scraper.scrap_hilo, hkjc_scraper.scrap_cornerhilo)
    
    for s in scrapers:
        odds = s()
        booker.populatebook(odds)

import argparse
import logging
from datetime import datetime

parser = argparse.ArgumentParser(description=r"Scrapping Odds infomation and populating to OddsBook.xlsx")
parser.add_argument('-i', '--interval', type=int, default=0, help=r"Minutes of interval for updating odds after each run.")
parser.add_argument('-d', '--delay', type=int, default=3, help=r"Seconds of delay on webscraping.")
parser.add_argument('--webdriver', type=str, default='./chromedriver.exe')
parser.add_argument('--debug', action='store_true', help=r"Log debug message.")
argv = parser.parse_args()

if __name__ == "__main__":

    logging.basicConfig(filename='oddsbook.log', filemode='w', level=logging.DEBUG if argv.debug else logging.INFO)

    if argv.interval <= 0:
        run(argv.delay, argv.webdriver)
    else:
        while True:
            logging.info(f"Start Running at {datetime.now()}")
            logging.debug(argv)
            try:
                run(argv.delay, argv.webdriver)
                logging.info("Run Successful!")
            except Exception as e:
                logging.error("Exception occurred", exc_info=True)
            finally:
                timer.sleep(argv.interval * 60)
                
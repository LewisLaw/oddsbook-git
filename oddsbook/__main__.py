import time as timer
from oddsbook import booker
from oddsbook import hkjc_scraper

def run(delay: int = 3):

    scrapers = (hkjc_scraper.scrap_homedrawaway, hkjc_scraper.scrap_handicap, hkjc_scraper.scrap_hilo, hkjc_scraper.scrap_cornerhilo)
    
    for s in scrapers:
        odds = s(delay=delay)
        booker.populatebook(odds)

import argparse
import logging
from datetime import datetime

parser = argparse.ArgumentParser(description=r"Scrapping Odds infomation and populating to OddsBook.xlsx")
parser.add_argument('-i', '--interval', type=int, default=0, help=r"Minutes of interval for updating odds after each run.")
parser.add_argument('-d', '--delay', type=int, default=3, help=r"Seconds of delay on webscraping.")
parser.add_argument('--debug', action='store_true', help=r"Log debug message.")
argv = parser.parse_args()

if __name__ == "__main__":

    print(argv)
    logging.basicConfig(filename='oddsbook.log', filemode='a', level=logging.DEBUG if argv.debug else logging.INFO)

    if argv.interval <= 0:
        run(argv.delay)
    else:
        while True:
            logging.info(f"Start Running at {datetime.now()}")
            try:
                run(argv.delay)
                logging.info("Run Successful!")
            except Exception as e:
                logging.error("Exception occurred", exc_info=True)
            finally:
                timer.sleep(argv.interval * 60)
                
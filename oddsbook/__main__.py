import time as timer
from oddsbook import booker
from oddsbook import hkjc_scraper

def run(delay: int = 3):

    scrapers = (hkjc_scraper.scrap_homedrawaway, hkjc_scraper.scrap_handicap, hkjc_scraper.scrap_hilo, hkjc_scraper.scrap_cornerhilo)
    
    for s in scrapers:
        odds = s(delay=delay)
        booker.populatebook(odds)

import argparse

parser = argparse.ArgumentParser(description=r"Scrapping Odds infomation and populating to OddsBook.xlsx")
parser.add_argument('--interval', default=0, help=r"Minutes of interval for updating odds after each run.")
parser.add_argument('--delay', default=3, help=r"Seconds of delay on webscraping.")
argv = parser.parse_args()

if __name__ == "__main__":
    
    interval = int(argv.interval)
    delay = int(argv.delay)

    if interval <= 0:
        run(delay)
    else:
        while True:
            run(delay)
            timer.sleep(interval * 60)
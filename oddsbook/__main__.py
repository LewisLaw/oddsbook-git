import sched
import time as timer
from oddsbook import booker
from oddsbook import hkjc_scraper

def run():

    scrapers = (hkjc_scraper.scrap_homedrawaway, hkjc_scraper.scrap_handicap)
    
    for s in scrapers:
        odds = s()
        booker.populatebook(odds)

def main():
    run()

if __name__ == "__main__":
    main()
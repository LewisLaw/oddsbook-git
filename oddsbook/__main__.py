from sqlalchemy import sql
from oddsbook.sqlitedb import SqliteDB
import time as timer
from oddsbook import booker
from oddsbook import scraper
from oddsbook import models

def run(driver_path:str = './chromedriver.exe', lang:str='ch', delay: int = 3):

    tgbot_logger = logging.getLogger('telegramBot')

    hkjc_scraper = scraper.HKJCScraper(driver_path, lang, delay)
    scrapers = (hkjc_scraper.scrap_homedrawaway, hkjc_scraper.scrap_handicap, hkjc_scraper.scrap_hilo, hkjc_scraper.scrap_cornerhilo)
    sqlitedb = SqliteDB()

    for s in scrapers:
        odds = s()
        if odds:
            booker.populatebook(odds)
            sqlitedb.add_all(odds)
    
    for oddstype in (models.Odds_HomeDrawAway, models.Odds_Handicap, models.Odds_HiLo, models.Odds_CornerHiLo):
        oddstype_str = booker.ODDSTYPE_CONFIG[oddstype.__name__]['columnheader']
        
        new_matches = sqlitedb.get_new_matches(oddstype)
        for m in new_matches:
            msg = f"新增賽事{oddstype_str} @ {m.source}: {m.date:%b-%d} {m.teams}"
            if oddstype == models.Odds_HomeDrawAway:
                msg += f"主: {m.home} 客: {m.away} 和: {m.draw}"
            elif oddstype == models.Odds_Handicap:
                msg += f"讓: {m.handicap} 主: {m.home} 客: {m.away}"
            elif oddstype in (models.Odds_HiLo, models.Odds_CornerHiLo):
                msg += f"球: {m.line} 大: {m.hi} 細: {m.lo}"
            tgbot_logger.info(msg)
        
        updated_odds = sqlitedb.get_updated_odds(oddstype)
        for m in updated_odds:
            msg = f"賠率變動{oddstype_str} @ {m.source}: {m.date:%b-%d} {m.teams}"
            if oddstype == models.Odds_HomeDrawAway:
                msg += f"主: {m.home} 客: {m.away} 和: {m.draw}"
            elif oddstype == models.Odds_Handicap:
                msg += f"讓: {m.handicap} 主: {m.home} 客: {m.away}"
            elif oddstype in (models.Odds_HiLo, models.Odds_CornerHiLo):
                msg += f"球: {m.line} 大: {m.hi} 細: {m.lo}"
            tgbot_logger.info(msg)

import argparse
import logging
import logging.config
from datetime import datetime

parser = argparse.ArgumentParser(description=r"Scrapping Odds infomation and populating to OddsBook.xlsx")
parser.add_argument('-i', '--interval', type=int, default=0, help=r"Minutes of interval for updating odds after each run.")
parser.add_argument('-d', '--delay', type=int, default=3, help=r"Seconds of delay on webscraping.")
parser.add_argument('-l', '--lang', type=str, default='ch', help=r"Language of webpage to parse.")
parser.add_argument('--webdriver', type=str, default='./chromedriver.exe', help=r"Path of the webdriver executable.")
parser.add_argument('--debug', action='store_true', help=r"Log debug message.")
argv = parser.parse_args()

if __name__ == "__main__":

    logging.config.fileConfig(fname='./oddsbook/logging.conf', disable_existing_loggers=False)
    #logging.basicConfig(filename='oddsbook.log', filemode='w', level=logging.DEBUG if argv.debug else logging.INFO)
    logger = logging.getLogger(__name__)

    while True:
        logging.info(f"Start Running at {datetime.now()}")
        logging.debug(argv)
        try:
            run(argv.webdriver, argv.lang, argv.delay)
            logging.info("Run Successful!")
            if argv.interval <= 0: break
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
        finally:
            timer.sleep(argv.interval * 60)
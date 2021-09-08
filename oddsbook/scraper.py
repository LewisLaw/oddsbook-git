from abc import abstractclassmethod
from selenium import webdriver
from .hkjc_scraper import HKJCScraperFuncs

class Scraper:
    def __init__(self, driver_path:str) -> None:
        self.browser = browser_selector(driver_path)
    def __del__(self) -> None:
        try:
            self.browser.close()
        except AttributeError:
            pass


class HKJCScraper(Scraper):
    def __init__(self, driver_path: str) -> None:
        super().__init__(driver_path)
        funcs = HKJCScraperFuncs(self.browser)
        self.scrap_homedrawaway = funcs.scrap_homedrawaway
        self.scrap_handicap = funcs.scrap_handicap
        self.scrap_hilo = funcs.scrap_hilo
        self.scrap_cornerhilo = funcs.scrap_cornerhilo


class UnsupportedWebdriver(Exception):
    def __init__(self, driver_path:str) -> None:
        self.message = f"Webdriver specified in path {driver_path} not supported."
        super().__init__(self.message)


def browser_selector(driver_path:str) -> webdriver:
    if 'chromedriver' in (path:=driver_path.lower()):
        driver = webdriver.Chrome
    elif 'geckodriver' in path:
        driver = webdriver.Firefox
    elif 'edgedriver' in path:
        driver = webdriver.Edge
    elif 'safari' in path:
        driver = webdriver.Safari
    else:
        raise UnsupportedWebdriver(driver_path)
    return driver(driver_path)
from typing import Callable, Iterable, Tuple
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import date, datetime, timedelta
from .models import Odds, Odds_CornerHiLo, Odds_Handicap, Odds_HiLo, Odds_HomeDrawAway
import re

NEXT = {
    'en' : 'NEXT',
    'ch' : '下頁'
}

WEEKDAY_MAP = {
    'en': {
        'MON': 0,
        'TUE': 1,
        'WED': 2,
        'THU': 3,
        'FRI': 4,
        'SAT': 5,
        'SUN': 6
    }, 
    'ch': {
        '星期一': 0,
        '星期二': 1,
        '星期三': 2,
        '星期四': 3,
        '星期五': 4,
        '星期六': 5,
        '星期日': 6
    }
}

class HKJCScraperFuncs:
    
    def __init__(self, browser:webdriver, lang:str = 'ch', delay:int = 3) -> None:
        self.browser = browser
        self.lang = lang
        self.delay = delay

    def scrap_homedrawaway(self) -> Tuple[Odds_HomeDrawAway]: 
        return self.scrap(f"https://bet.hkjc.com/football/index.aspx?lang={self.lang}", self.parse_homedrawaway)

    def scrap_handicap(self) -> Tuple[Odds_Handicap]:
        return self.scrap(f"https://bet.hkjc.com/football/odds/odds_hdc.aspx?lang={self.lang}", self.parse_handicap)

    def scrap_hilo(self) -> Tuple[Odds_HiLo]:
        return self.scrap(f"https://bet.hkjc.com/football/odds/odds_hil.aspx?lang={self.lang}", self.parse_hilo)

    def scrap_cornerhilo(self) -> Tuple[Odds_CornerHiLo]:
        return self.scrap(f"https://bet.hkjc.com/football/odds/odds_chl.aspx?lang={self.lang}", self.parse_hilo, {'oddshilotype': Odds_CornerHiLo})

    def scrap(self, url: str, matchparser: Callable, matchparserparam: dict = {}) -> Tuple[Odds]:

        self.browser.get(url)

        oddslist = tuple()

        while(True):
            tables = WebDriverWait(self.browser, self.delay).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "couponTable")))

            update_time = datetime.now().replace(second=0, microsecond=0)

            matches = []
            for t in tables:
                matches += t.find_elements_by_css_selector("div.couponRow.rAlt0")
                matches += t.find_elements_by_css_selector("div.couponRow.rAlt1")

            for m in matches:
                try:
                    o = matchparser(m, update_time=update_time, **matchparserparam)
                    oddslist += o if isinstance(o, Iterable) else (o, )
                except:
                    pass

            next_btn = self.browser.find_elements_by_xpath(f"//*[text()='{NEXT[self.lang]}']")

            if next_btn:
                next_btn[0].click()
            else:
                break
            
        return oddslist


    def parse_homedrawaway(self, match_element, update_time:datetime) -> Odds_HomeDrawAway:
        
        wkday = match_element.find_element_by_class_name("cday").get_attribute("innerText")[:3]
        match_date=date.today() + timedelta(days = -1 if (wkdiff:=WEEKDAY_MAP[self.lang][wkday] - date.today().weekday()) == 6 else wkdiff if wkdiff >= -1 else wkdiff + 7)
        teams = match_element.find_element_by_class_name("cteams").find_element_by_tag_name("a").get_attribute("text")
        oddsVal = match_element.find_elements_by_class_name("oddsVal")
        home = oddsVal[0].get_attribute("innerText")
        draw = oddsVal[1].get_attribute("innerText")
        away = oddsVal[2].get_attribute("innerText")

        return Odds_HomeDrawAway(source='hkjc', date=match_date, teams=teams, home=home, draw=draw, away=away, update_time=update_time)


    def parse_handicap(self, match_element, update_time:datetime) -> Odds_Handicap:
        
        wkday = match_element.find_element_by_class_name("cday").get_attribute("innerText")[:3]
        match_date=date.today() + timedelta(days = -1 if (wkdiff:=WEEKDAY_MAP[self.lang][wkday] - date.today().weekday()) == 6 else wkdiff if wkdiff >= -1 else wkdiff + 7)
        cteams = match_element.find_element_by_class_name("cteams").find_element_by_tag_name("a").get_attribute("text")
        teams = ''.join(re.match("^(.*)\[.*\](\s.*\s)(.*)\[.*\]$", cteams).groups())
        handicap = r'||'.join(re.match("^.*(\[.*\])\s.*\s.*(\[.*\])$", cteams).groups())
        oddsVal = match_element.find_elements_by_class_name("oddsVal")
        home = oddsVal[0].get_attribute("innerText")
        away = oddsVal[1].get_attribute("innerText")

        return Odds_Handicap(source='hkjc', date=match_date, teams=teams, home=home, away=away, handicap=handicap, update_time=update_time)


    def parse_hilo(self, match_element, update_time:datetime, oddshilotype = Odds_HiLo) -> Odds_HiLo:
        
        wkday = match_element.find_element_by_class_name("cday").get_attribute("innerText")[:3]
        match_date=date.today() + timedelta(days = -1 if (wkdiff:=WEEKDAY_MAP[self.lang][wkday] - date.today().weekday()) == 6 else wkdiff if wkdiff >= -1 else wkdiff + 7)
        teams = match_element.find_element_by_class_name("cteams").find_element_by_tag_name("a").get_attribute("text")
        cline = match_element.find_element_by_class_name("cline")
        lines = cline.find_elements_by_xpath("div[contains(@class,'LineRow')]") 
        codds = match_element.find_elements_by_xpath("div[@class='codds']")
        his = codds[0].find_elements_by_xpath("div[contains(@class,'LineRow')]")
        los = codds[1].find_elements_by_xpath("div[contains(@class,'LineRow')]")

        odds_list = tuple()
        for ln, h, l in zip(lines, his, los):
            line = ln.get_attribute("innerText")
            hi = h.get_attribute("innerText")
            lo = l.get_attribute("innerText")
            odds_list += (oddshilotype(source='hkjc', date=match_date, teams=teams, line=line, hi=hi, lo=lo, update_time=update_time), )
        
        return odds_list
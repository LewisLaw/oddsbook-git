from typing import Iterable
import xlwings as xw
from .models import Odds

ODDSTYPE_CONFIG = {
    'Odds_HomeDrawAway': {
        'columnheader': '全場主客和',
        'attributes': ['update_time', 'home', 'draw', 'away']
    },
    'Odds_Handicap': {
        'columnheader': '全場讓球',
        'attributes': ['update_time', 'handicap', 'home', 'away']
    },
    'Odds_HiLo': {
        'columnheader': '全場入球大細',
        'attributes': ['update_time', 'line', 'hi', 'lo']
    },
    'Odds_CornerHiLo': {
        'columnheader': '全場角球大細',
        'attributes': ['update_time', 'line', 'hi', 'lo']
    }
}


def populatebook(oddslist: Iterable):
#def populatematch(odds: Odds):

    wb = xw.Book("./oddsbook.xlsx")
    shtnames = [sht.name for sht in wb.sheets if sht != "TEMPLATE"]
    
    with wb.app.properties(screen_updating = False):
        for odds in oddslist:
            oddstype = type(odds).__name__
            oddsconfig = ODDSTYPE_CONFIG[oddstype]

            shtname = f"{odds.date:%y%m%d}_{odds.teams}"[:31]

            if shtname not in shtnames:
                template_sht = wb.sheets['TEMPLATE']
                odds_sht = template_sht.copy(before=template_sht, name=shtname)
                shtnames += [shtname]
            else:
                odds_sht = wb.sheets[shtname]

            start_col = odds_sht.range(oddsconfig['columnheader']).column
            last_row = odds_sht.range((1, start_col)).end('down').row
            odds_sht.range((last_row + 1, start_col)).value = [odds.__dict__.get(a) for a in oddsconfig['attributes']]
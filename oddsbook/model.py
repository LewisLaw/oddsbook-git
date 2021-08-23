from dataclasses import dataclass
import datetime

@dataclass
class Odds():
    date: datetime.date
    teams: str
    update_time: datetime.datetime

@dataclass
class Odds_HomeDrawAway(Odds):
    home: float
    away: float
    draw: float

@dataclass
class Odds_Handicap(Odds):
    home: float
    away: float
    handicap: str

@dataclass
class Odds_HiLo(Odds):
    line: str
    hi: float
    lo: float

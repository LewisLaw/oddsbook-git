from dataclasses import dataclass
import datetime

@dataclass
class Odds():
    date: datetime.date
    teams: str
    home: float
    away: float
    update_time: datetime.datetime

@dataclass
class Odds_HomeDrawAway(Odds):
    draw: float

@dataclass
class Odds_Handicap(Odds):
    handicap: str
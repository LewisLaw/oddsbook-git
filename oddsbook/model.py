from dataclasses import dataclass, field
from sqlalchemy import Column, String, Date, DateTime, Float
import datetime

@dataclass
class Odds():
    source: str = field(
        metadata={
            'sa': Column(String)
        }
    )
    date: datetime.date = field(
        metadata={
            'sa': Column(Date)
        }
    )
    teams: str = field(
        metadata={
            'sa': Column(String(37))
        }
    )
    update_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime)
        }
    )

@dataclass
class Odds_HomeDrawAway(Odds):
    __tablename__ = "Odds_HomeDrawAway"
    __sa_dataclass_metadata_key__ = "sa"
    home: float = field(
        metadata={
            'sa': Column(Float)
        }
    )
    away: float= field(
        metadata={
            'sa': Column(Float)
        }
    )
    draw: float= field(
        metadata={
            'sa': Column(Float)
        }
    )

@dataclass
class Odds_Handicap(Odds):
    __tablename__ = "Odds_Handicap"
    __sa_dataclass_metadata_key__ = "sa"
    handicap: str= field(
        metadata={
            'sa': Column(String)
        }
    )
    home: float= field(
        metadata={
            'sa': Column(Float)
        }
    )
    away: float= field(
        metadata={
            'sa': Column(Float)
        }
    )

@dataclass
class Odds_HiLo(Odds):
    __tablename__ = "Odds_HiLo"
    __sa_dataclass_metadata_key__ = "sa"
    line: str= field(
        metadata={
            'sa': Column(String)
        }
    )
    hi: float= field(
        metadata={
            'sa': Column(Float)
        }
    )
    lo: float= field(
        metadata={
            'sa': Column(Float)
        }
    )

@dataclass
class Odds_CornerHiLo(Odds_HiLo):
    __tablename__ = "Odds_CornerHiLo"
    __sa_dataclass_metadata_key__ = "sa"
    pass
from dataclasses import dataclass, field
from sqlalchemy import create_engine, Column, String, Date, DateTime, Float
from sqlalchemy.orm import registry
import datetime

mapper_registry = registry()
Base = mapper_registry.generate_base()

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
            'sa': Column(String)
        }
    )
    update_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime)
        }
    )

@mapper_registry.mapped
@dataclass
class Odds_HomeDrawAway(Odds):
    __tablename__ = "Odds_HomeDrawAway"
    __sa_dataclass_metadata_key__ = "sa"
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
            'sa': Column(String, primary_key=True)
        }
    )
    update_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime, primary_key=True)
        }
    )
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

@mapper_registry.mapped
@dataclass
class Odds_Handicap(Odds):
    __tablename__ = "Odds_Handicap"
    __sa_dataclass_metadata_key__ = "sa"
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
            'sa': Column(String, primary_key=True)
        }
    )
    update_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime, primary_key=True)
        }
    )
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

@mapper_registry.mapped
@dataclass
class Odds_HiLo(Odds):
    __tablename__ = "Odds_HiLo"
    __sa_dataclass_metadata_key__ = "sa"
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
            'sa': Column(String, primary_key=True)
        }
    )
    update_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime, primary_key=True)
        }
    )
    line: str= field(
        metadata={
            'sa': Column(String, primary_key=True)
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

@mapper_registry.mapped
@dataclass
class Odds_CornerHiLo(Odds):
    __tablename__ = "Odds_CornerHiLo"
    __sa_dataclass_metadata_key__ = "sa"
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
            'sa': Column(String, primary_key=True)
        }
    )
    update_time: datetime.datetime = field(
        metadata={
            'sa': Column(DateTime, primary_key=True)
        }
    )
    line: str= field(
        metadata={
            'sa': Column(String, primary_key=True)
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

engine = create_engine(r'sqlite:///./oddsdb.sqlite')
Base.metadata.create_all(engine)
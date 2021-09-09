import os
from typing import Tuple
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, base
from . import models

class SqliteDB:
    def __init__(self, dbpath:str = './oddsdb.sqlite') -> None:
        self.dbpath = os.path.abspath(dbpath)
        self.engine = create_engine(f'sqlite:///{self.dbpath}')
        models.Base.metadata.create_all(self.engine)
        self.sessionfactory = sessionmaker(bind=self.engine)
    
    def add_all(self, odds:Tuple[models.Odds]) -> None:
        print(odds)
        s = self.sessionfactory()
        s.add_all(odds)
        s.commit()

        
    def check_new(self, oddstype:str = 'Odds_HomeDrawAway') -> Tuple:
        s = self.sessionfactory()
        if oddstype == 'Odds_HomeDrawAway':
            oddsmodel = models.Odds_HomeDrawAway
        elif oddstype == 'Odds_Handicap':
            oddsmodel = models.Odds_Handicap
        elif oddstype == 'Odds_HiLo':
            oddsmodel = models.Odds_HiLo
        elif oddstype == 'Odds_CornerHiLo':
            oddsmodel = models.Odds_CornerHiLo
        else:
            raise UnsupportedOddsModel
        latest_update_time = s.query(func.max(oddsmodel.update_time)).scalar()
        result = s.query(oddsmodel, func.count(oddsmodel.teams)).group_by(oddsmodel.teams)
        if result:
            return tuple(r[0] for r in result if (r[1] == 1 and r[0].update_time == latest_update_time))
        return tuple()

class UnsupportedOddsModel(Exception):
    pass

if __name__ == '__main__':
    db = SqliteDB()
    db.check_new()
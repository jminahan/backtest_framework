##imports -- python libraries
import logging
import pandas as pd

##imports mongointerfce
from utils.src.mongointerface.mongointerface import MongoInterface

#import models
from models.conf.Symbol import Symbol

class SymbolMongoInterface:

    @staticmethod
    def getByTicker(ticker) -> Symbol:
        """
        docstring
        """
        return Symbol.objects(ticker=ticker)[0]

    @staticmethod
    def getSymbols() -> [Symbol]:
        return Symbol.objects

    @staticmethod
    def getSymbolsDF() -> pd.DataFrame:
        return pd.DataFrame.from_records([s.to_dict()] for s in Symbol.objects)
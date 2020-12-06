##imports -- python libraries
import logging

##imports mongointerfce
from utils.src.mongointerface.mongointerface import MongoInterface

#import models
from models.conf.Symbol import Symbol

class SymbolMongoInterface:

    mongoInterface = None

    def __init__(self, mongoInterface : MongoInterface):
        logging.debug("Symbol Mongo Interface initialized")
        self.mongoInterface = mongoInterface

    def getByTicker(self, ticker) -> Symbol:
        """
        docstring
        """
        return Symbol.objects(ticker=ticker)[0]

    def getSymbols(self) -> [Symbol]:
        return Symbol.objects
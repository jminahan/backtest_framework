import logging
from abc import ABC, abstractmethod
import datetime
from pandas import DataFrame
from DataEngine.DataAdapters.BaseAdapter.BaseAdapter import BaseAdapter as DataEngineAdapter
from Domain.OrderModels.Contract import Contract
from Domain.OrderModels.Order import Order
from Domain.OrderModels.OrderStatus import OrderStatus

class BaseAdapter(ABC):

    dataEngineAdapter : DataEngineAdapter
    dayOfMarket : DataFrame
    date : datetime.datetime
    universe : [str]

    def __init__(self, dataAdapter : DataEngineAdapter, date : datetime.datetime, universe : [str]):
        logging.debug("Base Adapter Initializer Called")
        self.dataEngineAdapter = dataAdapter
        self.date = date
        self.universe = universe

    @abstractmethod
    def ingestDataForToday(self, date : datetime.datetime) -> None:
        logging.error("Error, Base Adapter Method not overriden")

    @abstractmethod
    def ingestDataForToday(self, date : datetime.datetime, dfData : DataFrame):
        logging.error("Error, Base Adapter Method not overriden")

    @abstractmethod
    def getData(self) -> DataFrame:
        logging.error("Error, Base Adapter Method not overriden")

    @abstractmethod
    def getCurrentDate(self) -> datetime.datetime:
        logging.error("Error, Base Adapter Method not overriden")

    @abstractmethod
    def placeOrder(self, contract : Contract, order : Order) -> OrderStatus:
        logging.error("Error, Base Adapter Method not overriden")

    @abstractmethod
    def getHistoricMarketData(self, dateStart : datetime.datetime, dateEnd : datetime.datetime) -> DataFrame:
        logging.error("Error, Base Adapter Method not overriden")

    @abstractmethod
    def getCorporateInfos(self):
        logging.error("Error, Base Adapter Method not overriden")

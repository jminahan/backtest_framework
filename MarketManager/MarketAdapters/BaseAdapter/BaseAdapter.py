import logging
from abc import ABC, abstractmethod
import datetime
from pandas import DataFrame
from DataEngine.DataAdapters.BaseAdapter.BaseAdapter import BaseAdapter as DataEngineAdapter

class BaseAdapter(ABC):

    dataEngineAdapter : DataEngineAdapter
    dayOfMarket : DataFrame
    date : datetime.datetime

    def __init__(self, dataAdapter : DataEngineAdapter, date : datetime.datetime):
        logging.debug("Base Adapter Initializer Called")
        self.dataEngineAdapter = dataAdapter
        self.date = date

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
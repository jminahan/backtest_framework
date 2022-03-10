import datetime
from MarketManager.MarketAdapters.BaseAdapter.BaseAdapter import BaseAdapter
from pandas import DataFrame
from DataEngine.DataAdapters.BaseAdapter.BaseAdapter import BaseAdapter as DataEngineAdapter
import datetime

class MongoAdapter(BaseAdapter):
    
    def __init__(self, dataEngine : DataEngineAdapter, date : datetime.datetime):
        self.super(dataEngine, date)
        self.ingestDataForCurrentDate(date)

    def fetchDataForCurrentDate(self, date : datetime.datetime) -> None:
        self.ingestDataForToday(super().dataEngineAdapter.getDataForDate(date))

    def ingestDataForToday(self, date: datetime.datetime, dfData: DataFrame) -> None:
        super().dayOfMarket = super().dataEngineAdapter.getDataForDate(date)

    def getData(self, date: datetime.datetime) -> DataFrame:
        return super().dayOfMarket

    def getCurrentDate(self) -> datetime.datetime:
        return super().date
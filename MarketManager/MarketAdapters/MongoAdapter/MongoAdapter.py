from Domain.EquityCorporateData import EquityCorporateData
from Domain.OrderModels.OrderStatus import OrderStatus, OrderStatuses
import datetime
from MarketManager.MarketAdapters.BaseAdapter.BaseAdapter import BaseAdapter
from pandas import DataFrame
from DataEngine.DataAdapters.BaseAdapter.BaseAdapter import BaseAdapter as DataEngineAdapter
import datetime
from Domain.OrderModels.Contract import Contract
from Domain.OrderModels.Order import Order
from Domain.OrderModels.OrderStatus import OrderStatuses, OrderStatus
from Domain.EquityCorporateData import EquityCorporateData

class MongoAdapter(BaseAdapter):
    
    def __init__(self, dataEngine : DataEngineAdapter, date : datetime.datetime, universe : [str]):
        self.super(dataEngine, date, universe)
        self.ingestDataForCurrentDate(date)

    def fetchDataForCurrentDate(self, date : datetime.datetime) -> None:
        self.ingestDataForToday(super().dataEngineAdapter.getDataForDate(date))

    def ingestDataForToday(self, date: datetime.datetime) -> None:
        super().dayOfMarket = super().dataEngineAdapter.getDataForDate(date, self.universe)

    def getCurrentMarketData(self) -> DataFrame:
        return super().dayOfMarket

    def getHistoricMarketData(self, dateStart : datetime.datetime, dateEnd : datetime.datetime) -> DataFrame:
        if(super().date < dateStart or super().date < dateEnd):
            raise Exception("Attempting to access out of time data")
            
        return super().dataEngineAdapter.getDataForDateRange(dateStart, dateEnd, self.universe)

    def getCurrentDate(self) -> datetime.datetime:
        return super().date

    def placeOrder(self, contract: Contract, order: Order) -> OrderStatus:
        instrumentDf = super().dayOfMarket.loc(super().dayOfMarket["ticker" == contract.symbol])
        if(instrumentDf is not None):
            return OrderStatus(
                cost=instrumentDf["Close"][0] * order.total_quantity,
                status = OrderStatuses.FILLED)
        else:
            return OrderStatus(
                cost=0,
                status=OrderStatuses.UNFILLED
            )

    def getCorporateInfos(self) -> [EquityCorporateData]:
        return super().dataEngineAdapter.getCorporateInfos(self.universe)
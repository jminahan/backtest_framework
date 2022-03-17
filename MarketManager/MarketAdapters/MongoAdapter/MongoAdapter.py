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
        super().__init__(dataEngine, date, universe)
        self.fetchDataForCurrentDate(date)

    def fetchDataForCurrentDate(self, date : datetime.datetime) -> None:
        self.ingestDataForToday(self.dataEngineAdapter.getDataForDate(date, self.universe))

    def ingestDataForToday(self, incoming_data : DataFrame) -> None:
        self.dayOfMarket = incoming_data

    def getCurrentMarketData(self) -> DataFrame:
        return self.dayOfMarket

    def getData(self) -> DataFrame:
        return self.getCurrentMarketData()

    def getHistoricMarketData(self, dateStart : datetime.datetime, dateEnd : datetime.datetime) -> DataFrame:
        if(self.date < dateStart or self.date < dateEnd):
            raise Exception("Attempting to access out of time data")
            
        return self.dataEngineAdapter.getDataForDateRange(dateStart, dateEnd, self.universe)

    def getCurrentDate(self) -> datetime.datetime:
        return self.date

    def placeOrder(self, contract: Contract, order: Order) -> OrderStatus:
        instrumentDf = self.dayOfMarket.loc[self.dayOfMarket["ticker"] == contract.symbol]
        if(instrumentDf is not None):
            return OrderStatus(
                cost=instrumentDf["Open"][0] * order.total_quantity,
                status = OrderStatuses.FILLED,
                contract = contract,
                order = order)
        else:
            return OrderStatus(
                cost=0,
                status=OrderStatuses.UNFILLED,
                contract = contract,
                order = order
            )

    def getCorporateInfos(self) -> [EquityCorporateData]:
        return self.dataEngineAdapter.getCorporateInfos(self.universe)
from Domain.OrderModels.OrderStatus import OrderStatus
from Domain.DTO.MarketManagerConfigDTO import MarketManagerConfigDTO
import logging
from Domain.DTO.MarketManagerConfigDTO import MarketManagerConfigDTO, AdapterType
from MarketManager.MarketAdapters.BaseAdapter.BaseAdapter import BaseAdapter
from MarketManager.MarketAdapters.MongoAdapter.MongoAdapter import MongoAdapter
from DataEngine.DataAdapters.BaseAdapter.BaseAdapter import BaseAdapter as DataEngineAdapter
import datetime
from Domain.OrderModels.Order import Order
from Domain.OrderModels.Contract import Contract

class MarketManager():
    entityName : str = "MarketManager"

    config : MarketManagerConfigDTO
    adapter : BaseAdapter
    dataEngineAdapter : DataEngineAdapter

    def __init__(self, marketManagerConfigDTO : MarketManagerConfigDTO, 
                    dataEngineAdapter : DataEngineAdapter,
                    date : datetime.datetime,
                    universe : [str]):
        logging.info("Data Engine Initialized")
        marketManagerConfigDTO.validate()
        self.config = marketManagerConfigDTO
        self.universe = universe
        self.adapter = self.initializeAdapter(dataEngineAdapter, date)

    def initializeAdapter(self, dataEngineAdapter : DataEngineAdapter, date : datetime.datetime) -> BaseAdapter:
        if(self.config.adapterType == AdapterType.MONGO):
            return MongoAdapter(dataEngineAdapter, date=date, universe =self.universe)
        else:
            logging.error("Attempted to use unsupported {} adapter type, {}", self.entityName, self.config.adapterType);
            return Exception()

    def placeOrder(self, order : Order, contract : Contract, callback) -> OrderStatus:
        callback(self.adapter.placeOrder(order, contract))

    def getCurrentData(self):
            return self.adapter.getData()
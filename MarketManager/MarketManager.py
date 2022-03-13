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

def MarketManager():
    config : MarketManagerConfigDTO
    adapter : BaseAdapter
    dataEngineAdapter : DataEngineAdapter

    def __init__(self, marketManagerConfigDTO : MarketManagerConfigDTO, 
                    dataEngineAdapter : DataEngineAdapter,
                    date : datetime.datetime):
        logging.info("Data Engine Initialized")
        marketManagerConfigDTO.validate()
        self.config = marketManagerConfigDTO
        self.adapter = self.initializeAdapter(dataEngineAdapter, date)

    def initializeAdapter(self, dataEngineAdapter : DataEngineAdapter) -> BaseAdapter:
        if(self.config.adapterType == AdapterType.MONGO):
            return MongoAdapter(dataEngineAdapter)

    def placeOrder(self, order : Order, contract : Contract) -> OrderStatus:
        return self.adapter.placeOrder(order, contract)
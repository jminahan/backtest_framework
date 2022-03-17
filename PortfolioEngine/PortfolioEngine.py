from cmath import log
from datetime import datetime
from time import sleep

from sympy import threaded
from AccountantManager.AccountantManager import AccountantManager
from PortfolioEngine.Components.Portfolio import Portfolio
from sys import executable
from boto import config
from Domain.DTO.PortfolioEngineConfigDTO import PortfolioEngineConfigDTO
from PortfolioEngine.Components.TransactionCostModel.TransactionCostModelComponent import TransactionCostModelComponent
from PortfolioEngine.Components.PortfolioBalancer.PortfolioBalancerComponent import PortfolioBalancerComponent
from PortfolioEngine.Components.AlphaModel.AlphaModelComponent import AlphaModelComponent
from MarketManager.MarketManager import MarketManager
from PortfolioEngine.Adapters.BaseAdapter.BaseAdapter import BaseAdapter
from PortfolioEngine.Adapters.MongoAdapter.MongoAdapter import MongoAdapter
from Domain.DTO.PortfolioEngineConfigDTO import AdapterType
from threading import Timer, current_thread
from Domain.OrderModels.Contract import Contract
from Domain.OrderModels.Order import Order
from Domain.OrderModels.OrderStatus import OrderStatus
import logging
from Domain.OrderModels.TradeInfo import TradeInfo


class PortfolioEngine():

    universe : [str]
    alphaModel : AlphaModelComponent
    portfolioBalancer : PortfolioBalancerComponent
    transactionCostModel : TransactionCostModelComponent
    adapter : BaseAdapter
    market : MarketManager
    accountant : AccountantManager

    def __init__(self, universe : [str], configs : PortfolioEngineConfigDTO, market : MarketManager, accountant : AccountantManager):
        self.universe = universe
        self.configs = configs
        self.market = market
        self.accountant = accountant
        self.initializeComponents(configs)

    def registerMarketManager(self, market : MarketManager) -> None:
        self.market = market

    def registerAccountantManager(self, accountant : AccountantManager) -> None:
        self.accountant = accountant

    def initializeComponents(self, configs : PortfolioEngineConfigDTO):
        self.adapter = self.initializeAdapter(configs)
        self.adapter.initializeCurrentPortfolio()

        self.alphaModel = AlphaModelComponent(configs.alphaModelConfigs, self)
        self.portfolioBalancer = PortfolioBalancerComponent(configs.portfolioBalancerConfigs, self)
        self.transactionCostModel = TransactionCostModelComponent(configs.transactionModelConfigs, self)

    def initializeAdapter(self, configs : PortfolioEngineConfigDTO):
        if(self.configs.adapterType == AdapterType.MONGO):
            return MongoAdapter()

    def getCurrentPortfolio(self) -> Portfolio:
        return self.adapter.getCurrentPortfolio()

    def execute(self):
        self.executeTradeSchedule(self.getOrderSchedules())

    def getOrderSchedules(self) -> dict:
        indicators = self.alphaModel.collectIndicators()
        targetPortfolio = self.portfolioBalancer.getBalancedPortfolio(indicators)
        orderSchedule = self.transactionCostModel.getTradeSchedule(self.getCurrentPortfolio(), targetPortfolio, self.market.getCurrentData(), self.accountant.getFreeCapital())
        return orderSchedule

    def executeTradeSchedule(self, orderSchedule : dict) -> None:
        """
            orderSchedule should look like:
            {
                "t1": [ti1, ti2,...],
                "t2": [ti3, ti4,...]
            }

            tx should be able to be casted to a date time
            ti are trade infos, and should have all the information necessary to request execution of a trade from the MarketManager
        """
        for key, value in orderSchedule.items():
            for o in value:
                t = Timer(interval=(datetime.strptime(key, "YYYY-MM-DDTHH:MM:SS") - datetime.now()).total_seconds(), function=self.executeTrade, args=([o.tojson()]))
                t.start()

    def executeTrade(self, tradeinfo : dict) -> None:
        logging.info("in trade execution")
        trade = TradeInfo.fromjson(tradeinfo)
        os : OrderStatus = self.market.placeOrder(trade.contract,trade.order,self.executeTradeCallBack)

    def executeTradeCallBack(self, oStatus : OrderStatus):
        logging.info("In call back")
        self.accountant.adjustFreeCapital(oStatus.cost)
        self.adapter.executeTradeCallBack(oStatus)

    def getMarket(self) -> MarketManager:
        return self.market
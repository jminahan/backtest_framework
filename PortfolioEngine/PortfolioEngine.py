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
from Domain.OrderModels.TradeInfo import TradeInfoplaceOrder


class PortfolioEngine():

    universe : [str]
    alphaModel : AlphaModelComponent
    portfolioBalancer : PortfolioBalancerComponent
    transactionCostModel : TransactionCostModelComponent
    adapter : BaseAdapter
    market : MarketManager
    accountant : AccountantManager

    def __init__(self, universe : [str], configs : PortfolioEngineConfigDTO):
        self.universe = universe
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
        if(self.config.adapterType == AdapterType.MONGO):
            return MongoAdapter()

    def getCurrentPortfolio(self) -> Portfolio:
        self.adapter.getCurrentPortfolio()

    def execute(self):
        self.executeTradeSchedule(self.getOrderSchedules())

    def getOrderSchedules(self) -> dict:
        indicators = self.alphaModel.collectIndicators()
        targetPortfolio = self.portfolioBalancer.getBalancedPortfolio(indicators)
        orderSchedule = self.transactionCostModel.getOrderSchedule(self.getCurrentPortfolio(), targetPortfolio)

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
        for key, value in orderSchedule:
            for o in value:
                t = Timer(interval=key, function=self.executeOrder, args=(o))


    def executeTrade(self, trade : TradeInfo) -> None:
        os : OrderStatus = self.market.placeOrder(trade.order, trade.contract)
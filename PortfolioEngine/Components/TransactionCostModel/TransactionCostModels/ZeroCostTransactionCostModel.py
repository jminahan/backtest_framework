from datetime import datetime
from Domain.OrderModels.TradeInfo import TradeInfo
from PortfolioEngine.Components.TransactionCostModel.TransactionCostModels.BaseTransactionCostModel import BaseTransactionCostModel
from PortfolioEngine.Components.Portfolio import Portfolio
from Domain.OrderModels.Order import Order, OrderActions, OrderTypes
from Domain.OrderModels.Contract import Contract, ContractCurrencies, ContractExchanges, ContractPrimaryExchanges, ContractSecurityTypes

class ZeroCostTransactionCostModel(BaseTransactionCostModel):
    def __init__(self):
        pass

    def getTradeSchedule(self, oldPortfolio: Portfolio, newPortfolio: Portfolio) -> dict:
        portDiff = super().calculatePortfolioDifferences(oldPortfolio, newPortfolio)
        for t in portDiff:
            newTrade = self.generateTrades(t, portDiff[t])
            executionTime = datetime.today()

    def generateTrades(self, ticker : str, amt : float) -> TradeInfo:
        """
            Params:
                amt can be + or -, + buy, - sell
                ticker = "AAPL", "A", etc
            Returns:
                a single TradeComponent object filled with order and contract
        """
        o = Order()
        if (amt > 0):
            o.total_quantity = amt
            o.action = OrderActions.BUY
            o.order_type = OrderTypes.MKT

        if (amt < 0):
            o.total_quantity = -1 * amt
            o.action = OrderActions.SELL
            o.order_type = OrderTypes.MKT

        c = Contract()
        c.symbol = ticker
        c.currency = ContractCurrencies.USD
        c.prim_exchange = ContractPrimaryExchanges.NASDAQ
        c.sec_type = ContractSecurityTypes.STOCK
        c.exchange = ContractExchanges.SMART

        tc = TradeInfo()
        tc.order = o
        tc.contract = c

        return tc


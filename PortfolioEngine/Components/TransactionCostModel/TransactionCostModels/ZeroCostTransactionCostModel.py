from datetime import datetime, timedelta
from Domain.OrderModels.TradeInfo import TradeInfo
from PortfolioEngine.Components.TransactionCostModel.TransactionCostModels.BaseTransactionCostModel import BaseTransactionCostModel
from PortfolioEngine.Components.Portfolio import Portfolio
from Domain.OrderModels.Order import Order, OrderActions, OrderTypes
from Domain.OrderModels.Contract import Contract, ContractCurrencies, ContractExchanges, ContractPrimaryExchanges, ContractSecurityTypes
from pandas import DataFrame

class ZeroCostTransactionCostModel(BaseTransactionCostModel):
    def __init__(self):
        pass

    def getTradeSchedule(self, oldPortfolio: Portfolio, newPortfolio: Portfolio, dayDF : DataFrame, freeCapital : float) -> dict:
        portDiff = super().calculatePortfolioDifferences(oldPortfolio, newPortfolio, oldPortfolio.getCapital(dayDF=dayDF, freeCapital = freeCapital))
        retDict = {}
        newTrades = []
        for t in portDiff:
            newTrades.append(self.generateTrades(t, portDiff[t]))
        executionTime = datetime.today() + timedelta(seconds=15)
        retDict[executionTime.strftime("YYYY-MM-DDTHH:MM:SS")] = newTrades

        return retDict


    def generateTrades(self, ticker : str, amt : float) -> TradeInfo:
        """
            Params:
                amt can be + or -, + buy, - sell
                ticker = "AAPL", "A", etc
            Returns:
                a single TradeComponent object filled with order and contract
        """
        if (amt > 0):
            o = Order(total_quantity = amt,
                        action = OrderActions.BUY,
                        order_type = OrderTypes.MKT)

        if (amt < 0):
            o = Order(total_quantity = -1 * amt,
                        action = OrderActions.SELL,
                        order_type = OrderTypes.MKT)

        c = Contract(symbol = ticker, currency = ContractCurrencies.USD,
                                prim_exchange = ContractPrimaryExchanges.NASDAQ,
                                sec_type = ContractSecurityTypes.STOCK,
                                exchange = ContractExchanges.SMART)

        tc = TradeInfo(order = o,
                    contract = c)

        return tc


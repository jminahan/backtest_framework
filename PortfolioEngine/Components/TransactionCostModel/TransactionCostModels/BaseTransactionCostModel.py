from PortfolioEngine.Components.Portfolio import Portfolio
from abc import ABC, abstractmethod
import logging
from pandas import DataFrame

class BaseTransactionCostModel(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def getTradeSchedule(self, oldPortfolio : Portfolio, newPortfolio : Portfolio, dayDF : DataFrame, freeCapital : float) -> dict:
        logging.error("Error, unfilled abstract method")

    def calculatePortfolioDifferences(self, oldPortfolio : Portfolio, newPortfolio : Portfolio, totalCapital : int) -> dict:
        """
            Params:
                Old portfolio - existing asset allocations
                new portfolio - calculated as newly balanced portfolio given updated conditions

            returns:
                a dict in the following form:
                    { "ticker 1" : 20,
                       "ticker 2" : -2
                    }

                This is to be interpreted as "for the old portfolio to become the new portfolio, buy 20 ticker 1, and sell 2 ticker 2"
        """
        tickers = []
        tickers.extend(key for key in oldPortfolio.tickerAmounts.keys())
        tickers.extend(key for key in newPortfolio.tickerAmounts.keys())

        tickerChanges = {}

        for t in tickers:
            tickerChanges[t] = newPortfolio.getAllocation(t) - oldPortfolio.getAllocation(t)

        return tickerChanges
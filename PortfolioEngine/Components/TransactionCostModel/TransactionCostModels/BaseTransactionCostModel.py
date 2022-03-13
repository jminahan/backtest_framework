from PortfolioEngine.Components.Portfolio import Portfolio
from abc import ABC, abstractmethod
import logging

class BaseTransactionCostModel(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def getTradeSchedule(self, oldPortfolio : Portfolio, newPortfolio : Portfolio) -> dict:
        logging.error("Error, unfilled abstract method")\

    def calculatePortfolioDifferences(self, oldPortfolio : Portfolio, newPortfolio : Portfolio) -> dict:
        tickers = set()
        tickers.add(oldPortfolio.tickerDistr.keys)
        tickers.add(newPortfolio.tickerDistr.keys)

        tickerChanges = {}

        for t in tickers:
            tickerChanges[t] = newPortfolio.tickerDistr[t] - oldPortfolio.tickerDistr[t]
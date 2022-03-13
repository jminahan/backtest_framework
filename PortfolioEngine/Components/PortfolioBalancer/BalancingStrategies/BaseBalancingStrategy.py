from PortfolioEngine.Components.Portfolio import Portfolio
from pandas import DataFrame
from PortfolioEngine.Components.Indicator import Indicator
from abc import ABC, abstractmethod
import logging

class BaseBalancingStrategy(ABC):
    def __init__(self, currentPortfolio : Portfolio):
        self.currentPortfolio : Portfolio = currentPortfolio

    @abstractmethod
    def generateBalancedPortfolio(self, indics : [Indicator], DayDF: DataFrame, freeCapital : float) -> Portfolio:
        """
            params
                indics : a collection of indicators
                dayDF : dataframe of current market conditions
                freeCapital : free capital to allocate

            return
                a single target portfolio

            Useful to remember that an indicator is a distribution of asset allocation
            a portfolio is a set of quantities per asset.

            Also useful to remember that you can get all capital (allocated and free) given a DayDF, currentProfile, and freeCapital

            this means that this method must to two things:
                create a balanced distribution of tickers according to this balancing strategies rules
                convert that distribution of tickers to asset amounts to convert it to a portfolio
        """
        logging.error("Error, unimplemented method")
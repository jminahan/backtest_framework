from matplotlib import ticker
from PortfolioEngine.Components.PortfolioBalancer.BalancingStrategies.BaseBalancingStrategy import BaseBalancingStrategy
from PortfolioEngine.Components.Indicator import Indicator
from PortfolioEngine.Components.Portfolio import Portfolio
from pandas import DataFrame
import logging

class EvenSplitBalancingStrategy(BaseBalancingStrategy):
    def __init__(self, currentPortfolio : Portfolio):
        super().__init__(currentPortfolio)
        logging.error(currentPortfolio)

    def generateBalancedPortfolio(self, indics : [Indicator], dayDF : DataFrame, freeCapital : float) -> Portfolio:
        """
            params
                indics : a collection of indicators
                dayDF : a dataframe for the current market conditions

            return
                a single target portfolio

            Useful to remember that an indicator is a distribution of asset allocation
            a portfolio is a set of quantities per asset

            this means that this method must to two things:
                create a balanced distribution of tickers according to this balancing strategies rules
                convert that distribution of tickers to asset amounts to convert it to a portfolio
        """
        tickers = []
        tickerProportions = {}

        for i in indics:
            tickers.extend(key for key, value in i.indicators.items())

        tickers = set(tickers)

        for t in tickers:
            tickerProportions[t] = 0

        for i in indics:
            for t in i.indicators:
                tickerProportions[t] += i.indicators[t]

        for t in tickerProportions:
            tickerProportions[t] = tickerProportions[t]/len(indics)

        capitalToAllocate = self.currentPortfolio.getCapital(freeCapital = freeCapital, dayDF=dayDF)
        
        for t in tickerProportions:
            tickerProportions[t] = tickerProportions[t] * capitalToAllocate

        for t in tickerProportions:
            price = dayDF.loc[dayDF["ticker"] == t]["Open"]
            tickerProportions[t] = int(tickerProportions[t] / price)

        p = Portfolio()
        p.tickerAmounts = tickerProportions
        return p
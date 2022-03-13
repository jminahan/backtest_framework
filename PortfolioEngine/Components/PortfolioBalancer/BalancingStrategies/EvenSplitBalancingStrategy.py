from PortfolioEngine.Components.PortfolioBalancer.BalancingStrategies.BaseBalancingStrategy import BaseBalancingStrategy
from PortfolioEngine.Components.Indicator import Indicator
from PortfolioEngine.Components.Portfolio import Portfolio
from pandas import DataFrame

class EvenSplitBalancingStrategy(BaseBalancingStrategy):
    def __init__(self, currentPortfolio : Portfolio):
        super(currentPortfolio)

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
        tickers = set()
        tickerProportions = {}

        for i in indics:
            tickers.add(i.indicators.keys())

        for t in tickers:
            tickerProportions[t] = 0

        for i in indics:
            for t in i.indicators:
                tickerProportions[t] += i.indicators[t]

        for t in tickerProportions:
            tickerProportions[t] = tickerProportions[t]/len(indics)

        capitalToAllocate = self.currentPortfolio.getCapital(freeCapital = freeCapital, dayDF=dayDF)
        
        for t in tickerProportions:
            tickerProportions[t] = tickerProportions * capitalToAllocate

        for t in tickerProportions:
            price = dayDF.loc[dayDF["tickers"] == t]["Open"]
            tickerProportions[t] = int(tickerProportions / price)

        p = Portfolio()
        p.tickerAmounts = tickerProportions
        return p
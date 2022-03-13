from PortfolioEngine.Components.PortfolioBalancer.BalancingStrategies.BaseBalancingStrategy import BaseBalancingStrategy
from PortfolioEngine.Components.Indicator import Indicator
from PortfolioEngine.Components.Portfolio import Portfolio

class EvenSplitBalancingStrategy(BaseBalancingStrategy):
    def __init__(self):
        pass

    def generateBalancedPortfolio(self, indics : [Indicator]) -> Portfolio:
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

        p = Portfolio()
        p.tickerDistr = tickerProportions
        return p
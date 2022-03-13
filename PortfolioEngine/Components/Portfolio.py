from h11 import Data
from pandas import DataFrame

class Portfolio():
    """
        tickerDistr is based on percent of asset allocation
        so if:
            tickerDistr = {"AAPL" : .5, "AMZN" : .2. "GOOG": .3}
            50 percent of your portfolio is apple, 20 percent amazon, 30 percent google
    """
    tickerAmounts : dict
    def __init__(self):
        pass

    def getAllocatedCapital(self, dayDF : DataFrame, freeCapital : float = 0) -> float:
        allocationOfCapital : float = 0
        tickersInDay : DataFrame = dayDF["tickers"]
        for t in self.tickerAmounts:
            if(t in tickersInDay):
                tickerAmount = dayDF.loc[dayDF["tickers"]==t]["Open"] * self.tickerAmounts[t]
                allocationOfCapital += tickerAmount
            else:
                raise Exception ("Ticker of Portfolio not found in DataFrame")

        allocationOfCapital += freeCapital
        return allocationOfCapital

    def getCapital(self, dayDF : DataFrame, freeCapital : float) -> float:
        allocationOfCapital : float = 0
        tickersInDay : DataFrame = dayDF["tickers"]
        for t in self.tickerAmounts:
            if(t in tickersInDay):
                tickerAmount = dayDF.loc[dayDF["tickers"]==t]["Open"] * self.tickerAmounts[t]
                allocationOfCapital += tickerAmount
            else:
                raise Exception ("Ticker of Portfolio not found in DataFrame")

        allocationOfCapital += freeCapital
        return allocationOfCapital


    def tickerDistrAllocatedCapital(self, dayDF : DateFrame, freeCapital : float = 0) -> dict:
        """
            This method should give the distribution of allocated capital according
            current market conditions

            if self.tickerAmounts = {"AAPL": 50, "AMZN" : 10}
            and the current market conditions by a given data frame say that AAPL is 10/usd a share and AMZN is 20 usd/share

            the returned distribution is

            {"AAPL" : .71, "AMZN" : .29}

        """
        allocationOfCapital : float = 0
        tickerDistr : dict = {}
        tickersInDay : DataFrame = dayDF["tickers"]
        for t in self.tickerAmounts:
            if(t in tickersInDay):
                tickerAmount = dayDF.loc[dayDF["tickers"]==t]["Open"] * self.tickerAmounts[t]
                tickerDistr[t] = tickerAmount
                allocationOfCapital += tickerAmount
            else:
                raise Exception ("Ticker of Portfolio not found in DataFrame")

        allocationOfCapital += freeCapital
        for t in tickerDistr:
            tickerDistr[t] = tickerDistr[t] / allocationOfCapital

        return tickerDistr
        

    def tickerDistrWithFreeCapital(self, dayDF : DataFrame, freeCapital : float) -> dict:
        """
            This method is similar to tickerDistrAllocatedCapital, except it takes into account free capital
            meaning this will return the same as tickerDistrAllocatedCapital if you have no free capital
        """
        return self.tickerDistrAllocatedCapital(dayDF, freeCapital)
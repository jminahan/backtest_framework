###
#   Build YahooHistoricalData Model objects
###

## imports -- external
import logging
import pandas as pd

##imports -- models
from models.YahooHistoricalData import YahooHistoricalData
from models.conf.Symbol import Symbol
import datetime

class SymbolBuilder():

    def __init__(self):
        logging.debug("in Symbol Model Builder")

    def buildFromHand(self, ticker,
                            lastupdate,
                            commonCompanyName,
                            ipoDateTime,
                            industry, 
                            sector,
                            country,
                            market_cap) -> Symbol:
        return self.build(
            ticker = ticker,
            yHistoricalData = None,
            lastUpdate = lastupdate,
            commonCompanyName = commonCompanyName,
            ipoYear = ipoDateTime,
            industry = industry,
            sector = sector,
            country = country,
            marketCap = market_cap
        )

    def buildFromNasdaqDf(self, nasdaqDf : pd.DataFrame) -> [Symbol]:
        returnArray = []
        for index, row in nasdaqDf.iterrows():
            ##todo there has to be a better way
            if(pd.notna(row["Symbol"]) and 
                pd.notna(row["Name"]) and
                pd.notna(row["Market Cap"]) and
                pd.notna(row["Country"]) and 
                pd.notna(row["IPO Year"]) and
                pd.notna(row["Sector"]) and
                pd.notna(row["Industry"])):
                returnArray.append(
                    self.build(
                        ticker = row["Symbol"],
                        yHistoricalData = None,
                        lastUpdate = datetime.datetime.now(),
                        commonCompanyName = row["Name"],
                        ipoYear = row["IPO Year"],
                        industry = row["Industry"],
                        sector = row["Sector"],
                        country = row["Country"],
                        marketCap = row["Market Cap"]
                    )
                )

        return returnArray

    def build(self, ticker : str, 
                yHistoricalData : YahooHistoricalData,
                lastUpdate : datetime.datetime,
                commonCompanyName : str,
                ipoYear : datetime.datetime,
                industry : str,
                sector : str,
                country : str,
                marketCap : float) -> Symbol:
        """
        Takes inputs to generate a Symbol model object
        """
        return Symbol(
                ticker = ticker,
                yHistoricalData = yHistoricalData,
                lastUpdate = lastUpdate,
                commonCompanyName = commonCompanyName,
                ipoYear = datetime.datetime(int(ipoYear), 1, 1),
                industry = industry,
                sector = sector,
                country = country,
                marketCap = marketCap
        )
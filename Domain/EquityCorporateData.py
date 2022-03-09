from matplotlib import ticker
from mongoengine import Document, StringField, DateField
from sympy import E
from .BuildEnumMethods import BuildEnumMethods
import pandas as pd
import datetime


class EquityCorporateData(Document):
    ticker : StringField = StringField(required=True)
    commonCompanyName : StringField = StringField(required=True)
    ipoYear : DateField = DateField(required=True)
    industry : StringField = StringField(required=True)
    sector : StringField= StringField(required=True)
    country : StringField = StringField(required=True)

    def to_dict(self):
        """
        EquityCorporateData to dict
        """
        return {
            "ticker" : self.ticker,
            "commonCompanyName": self.commonCompanyName,
            "ipoYear" : self.ipoYear,
            "industry" : self.industry,
            "sector": self.sector,
            "country" : self.country,
        }

    @staticmethod
    def build(method : BuildEnumMethods, **kwargs) :
        if(method == BuildEnumMethods.MANUAL):
            return EquityCorporateData.manualBuild(kwargs)
        elif(method == BuildEnumMethods.DICT):
            return EquityCorporateData.dictbuild(kwargs)
        elif(method == BuildEnumMethods.DF):
            return EquityCorporateData.dfBuild(kwargs["DF"])

    @staticmethod
    def dfBuild(nasdaqDf : pd.DataFrame):
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
                    EquityCorporateData.build(method=BuildEnumMethods.MANUAL,
                        ticker = row["Symbol"],
                        yHistoricalData = None,
                        lastUpdate = datetime.datetime.now(),
                        commonCompanyName = row["Name"],
                        ipoYear = str(int(row["IPO Year"])) + "-01-01",
                        industry = row["Industry"],
                        sector = row["Sector"],
                        country = row["Country"],
                        marketCap = row["Market Cap"]
                    )
                )

        return returnArray

    def manualBuild(kwargs):
        equity = EquityCorporateData()
        equity.ticker = kwargs["ticker"]
        equity.commonCompanyName = kwargs["commonCompanyName"]
        equity.ipoYear = kwargs["ipoYear"]
        equity.industry = kwargs["industry"]
        equity.sector = kwargs["sector"]
        equity.country = kwargs["country"]

        if(equity.ticker is None or
            equity.commonCompanyName is None or
            equity.ipoYear is None or
            equity.industry is None or
            equity.sector is None or
            equity.country is None):
            raise Exception("Missing fields in an EquityCorporateData object Manual Build Method")

        return equity

    @staticmethod
    def dictBuild(kwargs):

        equity = EquityCorporateData()
        
        equity.ticker = kwargs["dict"]["ticker"]
        equity.commonCompanyName = kwargs["dict"]["commonCompanyName"]
        equity.ipoYear = kwargs["dict"]["ipoYear"]
        equity.industry = kwargs["dict"]["industry"]
        equity.sector = kwargs["dict"]["sector"]
        equity.country = kwargs["dict"]["country"]

        if(equity.ticker is None or
            equity.commonCompanyName is None or
            equity.ipoYear is None or
            equity.industry is None or
            equity.sector is None or
            equity.country is None):
            raise Exception("Missing fields in an EquityCorporateData object Dict Build Method")
        return equity

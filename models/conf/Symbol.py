from mongoengine import *
from models.YahooHistoricalData import YahooHistoricalData

class Symbol(Document):
    ticker = StringField(required=True)
    yHistoricalData = ReferenceField(YahooHistoricalData)
    lastUpdate = DateTimeField(required=True)
    commonCompanyName = StringField(required=True)
    ipoYear = DateTimeField(required=True)
    industry = StringField(required=True)
    sector = StringField(required=True)
    country = StringField(required=True)
    marketCap = FloatField(required=True)

    def to_dict(self):
        """
        docstring
        """
        return {
            "ticker" : self.ticker,
            "lastUpdate" : self.lastUpdate,
            "commonCompanyName": self.commonCompanyName,
            "ipoYear" : self.ipoYear,
            "industry" : self.industry,
            "sector": self.sector,
            "country" : self.country,
            "marketCap" : self.marketCap
        }


    # def __str__(self):
    #     return """
    #     { 
    #         \"ticker\" : {},
    #         \"yHistoricalData\" : {},
    #         \"lastUpdate\" : {},
    #         \"commonCompanyName\" : {},
    #         \"ipoYear\" : {},
    #         \"industry\" : {},
    #         \"sector\" : {},
    #         \"country\" : {},
    #         \"marketCap\" : {}
    #     }
    #     """.format(
    #         self.ticker,
    #         self.yHistoricalData,
    #         self.lastUpdate,
    #         self.commonCompanyName,
    #         self.ipoYear,
    #         self.industry,
    #         self.sector,
    #         self.country,
    #         self.marketCap
    #     )
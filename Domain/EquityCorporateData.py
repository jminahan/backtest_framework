from matplotlib import ticker
from mongoengine import Document, StringField, DateTimeField
from .BuildEnumMethods import BuildEnumMethods

class EquityCorporateData(Document):
    ticker : StringField = StringField(required=True)
    commonCompanyName : StringField = StringField(required=True)
    ipoYear : DateTimeField = DateTimeField(required=True)
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

    def build(self, method : BuildEnumMethods, **kwargs):
        if(method == BuildEnumMethods.MANUAL):
            self.manualBuild(kwargs)
        elif(method == BuildEnumMethods.DICT):
            self.dictbuild(kwargs)

    def manualBuild(self, kwargs):
        self.ticker = kwargs["ticker"]
        self.commonCompanyName = kwargs["commonCompanyName"]
        self.ipoYear = kwargs["ipoYear"]
        self.industry = kwargs["industry"]
        self.sector = kwargs["sector"]
        self.country = kwargs["country"]

        if(self.ticker is None or
            self.commonCompanyName is None or
            self.ipoYear is None or
            self.industry is None or
            self.sector is None or
            self.country is None):
            raise Exception("Missing fields in an EquityCorporateData object Manual Build Method")

    def dictBuild(self, **kwargs):
        self.ticker = kwargs["dict"]["ticker"]
        self.commonCompanyName = kwargs["dict"]["commonCompanyName"]
        self.ipoYear = kwargs["dict"]["ipoYear"]
        self.industry = kwargs["dict"]["industry"]
        self.sector = kwargs["dict"]["sector"]
        self.country = kwargs["dict"]["country"]

        if(self.ticker is None or
            self.commonCompanyName is None or
            self.ipoYear is None or
            self.industry is None or
            self.sector is None or
            self.country is None):
            raise Exception("Missing fields in an EquityCorporateData object Dict Build Method")

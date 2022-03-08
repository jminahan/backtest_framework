from mongoengine import Document, StringField, DateTimeField

class EquityCorporateData(Document):
    ticker = StringField(required=True)
    commonCompanyName = StringField(required=True)
    ipoYear = DateTimeField(required=True)
    industry = StringField(required=True)
    sector = StringField(required=True)
    country = StringField(required=True)

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

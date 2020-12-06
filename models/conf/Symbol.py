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
from mongoengine import *
from .DataFrameField import DataFrameField
class YahooHistoricalData(Document):
    historicalData = DataFrameField(required=True)
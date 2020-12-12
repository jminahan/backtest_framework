from mongoengine import *
from .DataFrameField import DataFrameField
class YahooHistoricalData(Document):
    historicalData = DataFrameField(required=True)

    def to_dict(self, ):
        """
        Historical data to dict
        """
        return {
            "historicalData" : self.historicalData
        }
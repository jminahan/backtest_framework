from mongoengine import Document, ReferenceField
from .DataFrameField import DataFrameField
from .EquityCorporateData import EquityCorporateData

class HistoricalData(Document):
    historicalData = DataFrameField(required=True)
    associatedEquity = ReferenceField(EquityCorporateData)


    def to_dict(self, ):
        """
        Historical data to dict
        """
        return {
            "associatedEquity" : self.associatedEquity.primary_key,
            "historicalData" : self.historicalData
        }
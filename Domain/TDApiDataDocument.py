from mongoengine import Document, ReferenceField
from .DataFrameField import DataFrameField
from .EquityCorporateData import EquityCorporateData

class TdApiDataDocument(Document):
    dataDump = DataFrameField(required=True)
    associatedEquity = ReferenceField(EquityCorporateData)


    def to_dict(self, ):
        """
        Historical data to dict, used pretty much exclusively in the td ameritrade scrape script
        """
        return {
            "associatedEquity" : self.associatedEquity.primary_key,
            "dataDump" : self.dataDump
        }
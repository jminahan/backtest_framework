from enum import Enum

class MarketManagerConfigDTO():
    def __init__(self, data):
        if(data is not None) :
            self.adapterType = data["adapterType"];
        else:
            self.adapterType = None

    def validate(self):
        if(self.adapterType == None):
            raise Exception("Invalid DataEngineConfigDTO data")

    @staticmethod
    def fromjson(jsonDict : dict):
        retConfig = MarketManagerConfigDTO(None)
        ##AdapterType
        if(jsonDict["adapterType"] == "MONGO"):
            retConfig.adapterType = AdapterType.MONGO
        elif(jsonDict["adapterType"] == "PAPER"):
            retConfig.adapterType = AdapterType.MONGO
        elif(jsonDict["adapterType"] == "LIVE"):
            retConfig.adapterType = AdapterType.MONGO
        else:
            raise Exception("Adapter Type Argument not found valid")
        return retConfig

class AdapterType(Enum):
    MONGO = "MONGO"
    PAPER = "PAPER"
    LIVE = "LIVE"

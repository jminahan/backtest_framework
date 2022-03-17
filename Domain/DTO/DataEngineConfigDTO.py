from enum import Enum

class DataEngineConfigDTO():
    def __init__(self, data):
        if(data is not None):
            self.adapterType = data["adapterType"];
        else:
            self.adapterType = None

    def validate(self):
        if(self.adapterType == None):
            raise Exception("Invalid DataEngineConfigDTO data")

    @staticmethod
    def fromjson(jsonData : dict):
        ac = DataEngineConfigDTO(None)
        if(jsonData["adapterType"] == "MONGO"):
            ac.adapterType = AdapterType.MONGO
        if(jsonData["adapterType"] == "PAPER"):
            ac.adapterType = AdapterType.PAPER
        if(jsonData["adapterType"] == "LIVE"):
            ac.adapterType = AdapterType.LIVE

        return ac

class AdapterType(Enum):
    MONGO = "MONGO"
    PAPER = "PAPER"
    LIVE = "LIVE"

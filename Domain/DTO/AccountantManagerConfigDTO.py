from enum import Enum

class AccountantManagerConfigDTO():
    def __init__(self, data):
        self.adapterType = data["adapterType"];

    def validate(self):
        if(self.adapterType == None):
            raise Exception("Invalid DataEngineConfigDTO data")

class AdapterType(Enum):
    MONGO = "MONGO"
    PAPER = "PAPER"
    LIVE = "LIVE"

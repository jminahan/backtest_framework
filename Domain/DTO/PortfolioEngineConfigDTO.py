from enum import Enum

"""

{
    "AlphaModel" : {
        "Strategies" : [AlphaModelStrategiesDTOEnum.BUYALL, ...]
        },

    "PortfolioBalancer" : {
        "Strategies" : PortfolioBalancerStrategiesDTOEnum.EVENSPLIT
        }

    "TransactionCostModel" : TransactionCostModelStrategyDTOEnum.DUMMY

    "adapterType" : AdapterTypes.MONGO

}


"""

class PortfolioEngineConfigDTO():
    def __init__(self, data):
        self.alphaModelConfigs = AlphaModelConfigDTO(data)
        self.portfolioBalancerConfigs = PortfolioBalancerConfigDTO(data)
        self.transactionModelConfigs = TransactionCostModelConfigDTO(data)
        self.adapterType = data["adapterType"]

    def validate(self):
        if(self.adapterType == None):
            raise Exception("Invalid DataEngineConfigDTO data")

class AlphaModelConfigDTO():
    def __init__(self, data):
        self.strategies = data["AlphaModel"]["Strategies"]

class PortfolioBalancerConfigDTO():
    def __init__(self, data):
        self.strategy = data["PortfolioBalancer"]

class TransactionCostModelConfigDTO():
    def __init__(self, data):
        self.strategy = data["TransactionCostModel"]


class AlphaModelStrategiesDTOEnum(Enum):
    BUYALL = "BUYALL"

class PortfolioBalancerStrategiesDTOEnum(Enum):
    EVENSPLIT = "EVENSPLIT"

class TransactionCostModelStrategyDTOEnum(Enum):
    ZEROCOST = "ZEROCOST"

class AdapterType(Enum):
    MONGO = "MONGO"
    PAPER = "PAPER"
    LIVE = "LIVE"

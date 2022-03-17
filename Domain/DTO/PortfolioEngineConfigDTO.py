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
        if(data is not None):
            self.alphaModelConfigs = AlphaModelConfigDTO(data)
            self.portfolioBalancerConfigs = PortfolioBalancerConfigDTO(data)
            self.transactionModelConfigs = TransactionCostModelConfigDTO(data)
            self.adapterType = data["adapterType"]
        else:
            self.alphaModelConfigs = None
            self.portfolioBalancerConfigs = None
            self.transactionModelConfigs = None
            self.adapterType = None

    def validate(self):
        if(self.adapterType == None):
            raise Exception("Invalid DataEngineConfigDTO data")

    @staticmethod
    def fromjson(jsonDict : dict):
        retConfig = PortfolioEngineConfigDTO(None)
        retConfig.alphaModelConfigs = AlphaModelConfigDTO.fromjson(jsonDict)
        retConfig.portfolioBalancerConfigs = PortfolioBalancerConfigDTO.fromjson(jsonDict)
        retConfig.transactionModelConfigs = TransactionCostModelConfigDTO.fromjson(jsonDict)
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

class AlphaModelConfigDTO():
    def __init__(self, data):
        if(data is not None):
            self.strategies = data["AlphaModel"]["Strategies"]
        else:
            self.strategies = None


    @staticmethod
    def fromjson(data):
        strats = []
        retConfig = AlphaModelConfigDTO(None)
        if("BUYALL" in data["AlphaModel"]["Strategies"]):
            strats.append(AlphaModelStrategiesDTOEnum.BUYALL)

        retConfig.strategies = strats
        return retConfig

class PortfolioBalancerConfigDTO():
    def __init__(self, data):
        if(data is not None):
            self.strategy = data["PortfolioBalancer"]
        else:
            self.strategy = None

    @staticmethod
    def fromjson(data):
        retConfig = PortfolioBalancerConfigDTO(None)
        if(data["PortfolioBalancer"] == "EVENSPLIT"):
            retConfig.strategy = PortfolioBalancerStrategiesDTOEnum.EVENSPLIT

        return retConfig

class TransactionCostModelConfigDTO():
    def __init__(self, data):
        if(data is not None):
            self.strategy = data["TransactionCostModel"]
        else:
            self.strategy = None

    @staticmethod
    def fromjson(data):
        retConfig = PortfolioBalancerConfigDTO(None)
        if(data["TransactionCostModel"] == "ZEROCOST"):
            retConfig.strategy = TransactionCostModelStrategyDTOEnum.ZEROCOST

        return retConfig


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

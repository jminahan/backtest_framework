from PortfolioEngine.Components.TransactionCostModel.TransactionCostModels.ZeroCostTransactionCostModel import ZeroCostTransactionCostModel
from PortfolioEngine.Components.TransactionCostModel.TransactionCostModels.BaseTransactionCostModel import BaseTransactionCostModel
from Domain.DTO.PortfolioEngineConfigDTO import TransactionCostModelConfigDTO, TransactionCostModelStrategyDTOEnum
from PortfolioEngine.Components.Portfolio import Portfolio
from pandas import DataFrame

class TransactionCostModelComponent():
    costModel : BaseTransactionCostModel

    def __init__(self, configs : TransactionCostModelConfigDTO, engineRef):
        self.engineRef = engineRef
        self.initialize(configs)

    def initialize(self, configs : TransactionCostModelConfigDTO):
        if(configs.strategy is TransactionCostModelStrategyDTOEnum.ZEROCOST):
            self.costModel = ZeroCostTransactionCostModel()

    def getTradeSchedule(self, oldPortfolio : Portfolio, newPortfolio : Portfolio, dayDF : DataFrame, freeCapital : float) -> dict:
        return self.costModel.getTradeSchedule(oldPortfolio, newPortfolio, dayDF, freeCapital)
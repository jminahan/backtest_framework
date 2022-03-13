from PortfolioEngine.Components.TransactionCostModel.TransactionCostModels.ZeroCostTransactionCostModel import ZeroCostTransactionCostModel
from PortfolioEngine.Components.TransactionCostModel.TransactionCostModels.BaseTransactionCostModel import BaseTransactionCostModel
from Domain.DTO.PortfolioEngineConfigDTO import TransactionCostModelConfigDTO, TransactionCostModelStrategyDTOEnum
from PortfolioEngine.PortfolioEngine import PortfolioEngine
from PortfolioEngine.Components.Portfolio import Portfolio


class TransactionCostModelComponent():
    engineRef : PortfolioEngine
    costModel : BaseTransactionCostModel

    def __init__(self, configs : TransactionCostModelConfigDTO, engineRef : PortfolioEngine):
        self.engineRef = engineRef
        self.initialize(configs)

    def initialize(self, configs : TransactionCostModelConfigDTO):
        if(configs.strategy is TransactionCostModelStrategyDTOEnum.ZEROCOST):
            self.costModel = ZeroCostTransactionCostModel()

    def getTradeSchedule(self, oldPortfolio : Portfolio, newPortfolio : Portfolio):
        self.costModel.getTradeSchedule(oldPortfolio, newPortfolio)
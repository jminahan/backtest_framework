from PortfolioEngine.Components.Portfolio import Portfolio
from PortfolioEngine.Components.PortfolioBalancer.BalancingStrategies.EvenSplitBalancingStrategy import EvenSplitBalancingStrategy
from PortfolioEngine.Components.PortfolioBalancer.BalancingStrategies.BaseBalancingStrategy import BaseBalancingStrategy
from PortfolioEngine.PortfolioEngine import PortfolioEngine
from Domain.DTO.PortfolioEngineConfigDTO import PortfolioBalancerConfigDTO, PortfolioBalancerStrategiesDTOEnum


class PortfolioBalancerComponent():
    engineRef : PortfolioEngine
    balanceMethod : BaseBalancingStrategy

    def __init__(self, configs : PortfolioBalancerConfigDTO, engineRef : PortfolioEngine):
        self.engineRef = engineRef
        self.initialize(configs)

    def initialize(self, configs : PortfolioBalancerConfigDTO):
        if(configs.strategy is PortfolioBalancerStrategiesDTOEnum.EVENSPLIT):
            self.balanceMethod = EvenSplitBalancingStrategy()

    def getBalancedPortfolio(self, indics: [Indicator]) -> Portfolio:
        return self.balanceMethod.generateBalancedPortfolio(indics, self.engineRef.accountant.getFreeCapital())
from PortfolioEngine.Components.Portfolio import Portfolio
from PortfolioEngine.Components.PortfolioBalancer.BalancingStrategies.EvenSplitBalancingStrategy import EvenSplitBalancingStrategy
from PortfolioEngine.Components.PortfolioBalancer.BalancingStrategies.BaseBalancingStrategy import BaseBalancingStrategy
from Domain.DTO.PortfolioEngineConfigDTO import PortfolioBalancerConfigDTO, PortfolioBalancerStrategiesDTOEnum
from PortfolioEngine.Components.Indicator import Indicator
import logging


class PortfolioBalancerComponent():
    balanceMethod : BaseBalancingStrategy

    def __init__(self, configs : PortfolioBalancerConfigDTO, engineRef):
        self.engineRef = engineRef
        self.initialize(configs)

    def initialize(self, configs : PortfolioBalancerConfigDTO):
        if(configs.strategy is PortfolioBalancerStrategiesDTOEnum.EVENSPLIT):
            self.balanceMethod = EvenSplitBalancingStrategy(currentPortfolio=self.engineRef.getCurrentPortfolio())

    def getBalancedPortfolio(self, indics: [Indicator]) -> Portfolio:
        return self.balanceMethod.generateBalancedPortfolio(indics,self.engineRef.getMarket().getCurrentData(), self.engineRef.accountant.adapter.getFreeCapital())
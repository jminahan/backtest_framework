from PortfolioEngine.Components.Indicator import Indicator
from PortfolioEngine.Components.AlphaModel.Strategies.BuyAllStrategy import BuyAllStrategy
from PortfolioEngine.Components.AlphaModel.Strategies.BaseStrategy import BaseStrategy
from Domain.DTO.PortfolioEngineConfigDTO import AlphaModelConfigDTO, AlphaModelStrategiesDTOEnum



from PortfolioEngine.Components.AlphaModel.Strategies.BaseStrategy import BaseStrategy

class AlphaModelComponent():
    strategies : [BaseStrategy] = []

    def __init__(self, configs : AlphaModelConfigDTO, engineRef):
        self.engineRef = engineRef
        self.initialize(configs)

    def initialize(self, configs : AlphaModelConfigDTO):
        self.initializeStrategies(configs.strategies)

    def initializeStrategies(self, stratNames : AlphaModelStrategiesDTOEnum) -> None:
        todayDate = self.engineRef.market.adapter.getCurrentDate()

        if(AlphaModelStrategiesDTOEnum.BUYALL in stratNames):
            self.strategies.append(BuyAllStrategy())

    def collectIndicators(self) -> [Indicator]:
        retIndics = []
        for i in self.strategies:
            indic : Indicator = i.collectIndicator(self.engineRef.market.adapter.getCurrentMarketData())
            indic.validateIndicator()
            retIndics.append(indic)

        return retIndics
            
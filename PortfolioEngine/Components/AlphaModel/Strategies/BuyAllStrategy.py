from PortfolioEngine.Components.Indicator import Indicator
from PortfolioEngine.Components.AlphaModel.Strategies.BaseStrategy import BaseStrategy
from pandas import DataFrame

class BuyAllStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()

    def collectIndicator(self, dataDF: DataFrame) -> Indicator:
        indic = Indicator()

        distribute = 100 / dataDF.__len__
        for key in dataDF["ticker"]:
            indic.indicators[key] = distribute
        
        return indic
    
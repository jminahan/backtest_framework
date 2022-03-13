from abc import ABC, abstractmethod
from pandas import DataFrame
from PortfolioEngine.Components.Indicator import Indicator
import logging

class BaseStrategy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def collectIndicator(self, dataDF : DataFrame) -> Indicator:
        logging.error("Method not filled out in BaseStrategy")
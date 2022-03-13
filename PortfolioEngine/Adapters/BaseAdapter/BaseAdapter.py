from abc import ABC, abstractmethod
import logging
from PortfolioEngine.Components.Portfolio import Portfolio

class BaseAdapter(ABC):
    currentPortfolio : Portfolio

    def __init__(self):
        pass

    @abstractmethod
    def initializeCurrentPortfolio(self):
        logging.error("Unimplemented Method")

    @abstractmethod
    def savePortfolio(self):
        logging.error("Unimplemented method")

    def getCurrentPortfolio(self) -> Portfolio:
        return self.currentPortfolio
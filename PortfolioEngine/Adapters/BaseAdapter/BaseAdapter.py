import os
from Domain.OrderModels.OrderStatus import OrderStatus
from abc import ABC, abstractmethod
import logging
from PortfolioEngine.Components.Portfolio import Portfolio

class BaseAdapter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def initializeCurrentPortfolio(self):
        logging.error("Unimplemented Method")

    @abstractmethod
    def savePortfolio(self):
        logging.error("Unimplemented method")

    @abstractmethod
    def executeTradeCallBack(self, oStatus : OrderStatus):
        logging.error("Unimplemented method")


    @abstractmethod
    def getCurrentPortfolio(self) -> Portfolio:
        logging.error("Unimplemented method")

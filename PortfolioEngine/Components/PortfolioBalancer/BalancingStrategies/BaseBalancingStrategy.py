from abc import ABC, abstractmethod
import logging

class BaseBalancingStrategy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generateBalancedPortfolio(self):
        logging.error("Error, unimplemented method")
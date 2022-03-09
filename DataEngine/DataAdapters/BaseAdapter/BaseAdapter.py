import logging
from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    def __init__(self):
        logging.debug("Base Adapter Initializer Called")

    @abstractmethod
    def getCurrentData():
        logging.error("Error, Base Adapter Method not overriden")
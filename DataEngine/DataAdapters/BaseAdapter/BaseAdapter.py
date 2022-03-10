import logging
from abc import ABC, abstractmethod
import datetime

class BaseAdapter(ABC):
    def __init__(self):
        logging.debug("Base Adapter Initializer Called")

    @abstractmethod
    def getDataForDate(date : datetime.datetime):
        logging.error("Error, Base Adapter Method not overriden")
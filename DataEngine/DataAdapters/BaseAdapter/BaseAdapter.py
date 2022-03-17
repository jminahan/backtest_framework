import logging
from abc import ABC, abstractmethod
import datetime
from Domain.EquityCorporateData import EquityCorporateData

class BaseAdapter(ABC):
    def __init__(self):
        logging.debug("Base Adapter Initializer Called")

    @abstractmethod
    def getDataForDate(self, date : datetime.datetime, universe : [str]):
        logging.error("Error, Base Adapter Method not overriden")

    @abstractmethod
    def getDataForDateRange(self, startDate: datetime.datetime, endDate : datetime.datetime):
        logging.error("Error, Base Adapter Method not overriden")

    @abstractmethod
    def getCorporateInfos(self, universe : [str]) -> [EquityCorporateData]:
        logging.error("Error, Base Adapter Method not overriden")

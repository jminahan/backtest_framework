import logging

from sim.TimeSlice import TimeSlice
from sim.Trade import Trade
class Strategy():

    title = None
    def __init__(self, title : str):
        logging.debug("Super Strategy Initialized")
        self.title = title

    def getTradeSignals(self, currentTimeSlice : TimeSlice) -> [Trade]:
        """
        This method when implemented will take in a time slice and see if any trades should
        be performed
        """
        raise NotImplementedError
    
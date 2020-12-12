from strategies.Strategy import Strategy
from sim.Sim import Sim
from sim.TimeSlice import TimeSlice
import utils.consts as consts
from sim.Trader import Trader
from sim.Trade import Trade
"""
This strategy will buy stocks on the first trading day
of the sim and sell them all on the last day

each stock will be equally cash weighted
"""
class BuyAndHoldSpecific(Strategy):
    sim = None
    title = None
    ticker = None

    """
    This strategy will buy all of one stock on opening day
    and close all of one stock on closing day
    """
    def __init__(self,ticker : str, 
                    title : str):
        self.title = title
        self.ticker = ticker

    '''
    should return a dict in the form of:
        {
            ticker : signal
        }

        where ticker is in the universe and signal is
        between -1 and 1.  This will then be rebalanced by trader
        that owns this strategy
    '''
    def getTradeSignals(self, currentTimeSlice : TimeSlice):
        retSignals = []
        if(currentTimeSlice.currentTime == self.sim.startDate):
            retSignals.append({self.ticker : 1.0})
        elif(currentTimeSlice.currentTime == self.sim.endDate):
            retSignals.append({self.ticker : -1.0})
        return retSignals
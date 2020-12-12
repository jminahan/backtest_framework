from strategies.Strategy import Strategy
from sim.Sim import Sim
from sim.TimeSlice import TimeSlice
import utils.consts as consts
from sim.Trader import Trader
from sim.Trade import Trade
"""
This strategy will buy stocks on the first trading day
of the sim and sell them all on the last day

each stock will be equally weighted
"""
class BuyAndHold(Strategy):
    sim = None
    title = None
    def __init__(self, title : str):
        self.title = title

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
            ##First day of sim, buy
            for i in self.sim.tickerList:
                retSignals.append({i : 1.0/self.sim.tickerList})
        elif(currentTimeSlice.currentTime == self.sim.endDate):
            for i in self.sim.tickerList:
                retSignals.append({i : -1.0/self.sim.tickerList})
        return retSignals
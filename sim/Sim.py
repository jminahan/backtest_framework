from sim.TimeSlice import TimeSlice
import datetime
from sim.Trader import Trader
from sim.Broker import Broker
"""
The primary sim
"""
class Sim():
    ## Stepping through the TimeSlices will be like progressing through time
        ## objective : avoid look ahead bias
    timeSlices : [TimeSlice] = []
    traders : [Trader] = []
    broker : Broker = None

    startDate : datetime.datetime = None
    endDate : datetime.datetime = None
    tickerList : [str] = None
    def __init__(self, tickerList : [str],
                    startDate : datetime.datetime,
                    endDate : datetime.datetime,
                    listOfStrategies,
                    interval : str = "1d"):
        """
        tickerList : the tickers you want to be presented as an asset to trade
        startDate : datetime of start date
        endDate : datetime of end date
        interval : str of interval - currently only support 1d
        """
        self.startDate = startDate
        self.endDate = endDate
        self.tickerList = tickerList

        self.initTimeSlices(tickerList, startDate, endDate, interval)
        self.initTraders(listOfStrategies)
        self.broker = Broker(self.timeSlices[0], self.traders)

    def run(self, callBack):
        for i in self.timeSlices:
            self.broker.setTimeSlice(i)
            for t in self.traders:
                callBack(i, self.broker, t)

    def initTraders(self, listOfStrategies):
        for i in listOfStrategies:
            newTrader = Trader(i)
            self.traders.append(newTrader)
            i.trader = newTrader
            i.sim = self

    def initTimeSlices(self, tickerList : [str],
                            startDate : datetime.datetime,
                            endDate : datetime.datetime,
                            interval : str = "1d"):
        """
        init time slices
        """
        deltaTimeSlices = endDate - startDate

        for i in range(deltaTimeSlices.days + 1):
            iterDateTime = startDate + datetime.timedelta(i)
            newTimeSlice = TimeSlice(tickerList, startDate, iterDateTime)
            self.timeSlices.append(newTimeSlice)        
    
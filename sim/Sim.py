from sim.TimeSlice import TimeSlice
import datetime
from sim.Trader import Trader
from sim.Broker import Broker
from models.conf.Symbol import Symbol

"""
The primary sim
"""
class Sim():
    ## Stepping through the TimeSlices will be like progressing through time
    timeSlices : [TimeSlice] = []
    traders : [Trader] = []
    broker : Broker = None

    startDate : datetime.datetime = None
    endDate : datetime.datetime = None
    tickerList : [str] = None

    def __init__(self, tickerList : [str],
                    startDate : datetime.datetime,
                    endDate : datetime.datetime,
                    listOfTradersProfiles,
                    interval : str = "1d"):
        """
        tickerList : the tickers you want to be presented as an asset to trade
        startDate : datetime of start date
        endDate : datetime of end date
        listOfTradersProfiles : comes in the form of [{strategy : allocation}]
        interval : str of interval - currently only support 1d
        """
        self.startDate = startDate
        self.endDate = endDate
        self.tickerList = tickerList

        self.initTimeSlices(tickerList, startDate, endDate, interval)
        self.initTraders(listOfTradersProfiles)
        self.broker = Broker(self.timeSlices[0], self.traders)

    def run(self, callBack):
        for i in self.timeSlices:
            self.broker.setTimeSlice(i)
            self.broker.addressQueue()
            for t in self.traders:
                callBack(i, self.broker, t)
                t.updateStats(self.broker)
        for t in self.traders:
            t.finalUpdateStats()

    '''
    initialize traders with listOfTradersProfiles parameter
    also pass each strategy in each dict the sim (used to 
    reference broker for values))
    '''
    def initTraders(self, listOfTradersProfiles):
        for i in listOfTradersProfiles:
            newTrader = Trader(i)
            self.traders.append(newTrader)
            newTrader.sim = self
            for t in i.keys():
                t.sim = self

    '''
    Init time slices
    loads historical data into each time slice
    between start and end time
    '''
    def initTimeSlices(self, tickerList : [str],
                            startDate : datetime.datetime,
                            endDate : datetime.datetime,
                            interval : str = "1d"):

        deltaTimeSlices = endDate - startDate

        ##Generate ticker list dict
        tickerListDict = self.generateTickerListDict(tickerList)

        for i in range(deltaTimeSlices.days + 1):
            iterDateTime = startDate + datetime.timedelta(i)
            if(i == 0):
                newTimeSlice = TimeSlice(tickerListDict, startDate, iterDateTime, None)
            else:
                newTimeSlice = TimeSlice(tickerListDict, startDate, iterDateTime, self.timeSlices[-1])
            self.timeSlices.append(newTimeSlice)        

    '''
    helper method to pull historical data once instead
    of on every time slice
    '''
    def generateTickerListDict(self, tickerList : [str]):
        returnDict = {}

        for i in tickerList:
            assetSymbol = Symbol.objects(ticker=i)[0]
            data = assetSymbol.yHistoricalData.historicalData
            returnDict[i] = {
                "Symbol" : assetSymbol,
                "HistoricalData" : data
            }

        return returnDict
    
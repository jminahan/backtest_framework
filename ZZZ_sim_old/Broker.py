from sim.TimeSlice import TimeSlice
import utils.consts as consts
from sim.Trade import Trade
from sim.Trader import Trader
from sim.Asset import Asset
from utils.src.sim.SimUtils import SimUtils

'''
This class acts kind of as the gateway to info for
a trader in a current time slice
'''
class Broker():

    ## current time slice - updated by sim
    currentTimeSlice : TimeSlice = None

    ##list of traders
    traders : [Trader] = []

    ##trade queue in case a trade is placed on
    ## a non-trading day
    tradeQueue : {} = {}

    '''
    initialize values of params
    '''
    def __init__(self, initTimeSlice : TimeSlice, traders : [Trader]) :
        self.currentTimeSlice = initTimeSlice
        self.traders = traders
        self.initTradeQueues(traders)

    ##initialize trade queues as 1 per trader
    def initTradeQueues(self, traders : [Trader]):
        for trader in traders:
            self.tradeQueue[trader] = []

    ##progress broker to next step
    def setTimeSlice(self, newTimeSlice : TimeSlice):
        self.currentTimeSlice = newTimeSlice

    def takeTrade(self, trade : Trade, trader: Trader):
        ##make sure the trades and traders of trades are valid
            ## aka not asking for an asset that does exist
            ##     or not traded from a trader that doesn't exist
        self.verifyTrade(trade)
        self.verifyTrader(trader)

        #if today is a trading day
        if(SimUtils.isTradingDay(self.currentTimeSlice)):
            ##handle trade
            if(trade.tradeAction == consts.TRADE_BUY):
                self.buy(trade, trader)
            elif(trade.tradeAction == consts.TRADE_SELL):
                self.sell(trade, trader)
        # if today is not a trading day
        else:
            self.tradeQueue[trader].append(trade)
            
    '''
    for each trade, call take trade
    '''
    def takeTrades(self, trades : [Trade], trader : Trader):
        for i in trades:
            self.takeTrade(i, trader)

    ##Make sure the trade is okay
    def verifyTrade(self, trade: Trade):
        assert(trade.ticker in self.currentTimeSlice.assets.keys())

    ##Make sure the trader is okay
    def verifyTrader(self, trader : Trader):
        assert(trader in self.traders)
    
    ##What to do on a buy trade
    def buy(self, trade : Trade, trader : Trader):
        ticker : str = trade.ticker
        costToTrade : float = self.getCurrentAssetPrice(ticker, self.currentTimeSlice) * trade.amt

        if(costToTrade > trader.cash):
            trade.modToCash(trader.cash)
        
        trader.cash = trader.cash - (trade.amt * self.getCurrentAssetPrice(ticker, self.currentTimeSlice))
        if(ticker in trader.positions.keys() != None):
            trader.positions[ticker] = trader.positions[ticker] + trade.amt
        else:
            trader.positions[ticker] = trade.amt

    #what to do on a sell trade
    def sell(self, trade : Trade,trader : Trader):
        ticker : str = trade.ticker
        asset : Asset = self.currentTimeSlice.assets[ticker]
        
        if(ticker in trader.positions.keys() and
                trader.positions[ticker] < trade.amt):
            trade.modToPosition(trader.positions[ticker])
        
        trader.cash = trader.cash + (trade.amt * self.getCurrentAssetPrice(ticker, self.currentTimeSlice))
        trader.positions[ticker] -= trade.amt

    #Get an tickers current price
    def getCurrentAssetPrice(self, ticker : str, timeSliceToUse : TimeSlice):
        if(SimUtils.isTradingDay(timeSliceToUse)):
            return timeSliceToUse.assets[ticker].historicalData.loc[timeSliceToUse.getKeyString()]["Close"]
        elif(timeSliceToUse.prevTimeSlice):
            return self.getCurrentAssetPrice(ticker, timeSliceToUse.prevTimeSlice)
        else:
            raise Exception("Started on a not trading day")

    '''
    called on a trading day after a non-trading day

    If theres trades, address in order that they arrived
    '''
    def addressQueue(self):
        if(SimUtils.isTradingDay(self.currentTimeSlice)):
            for trader in self.tradeQueue.keys():
                for trade in self.tradeQueue[trader]:
                    self.takeTrade(trade, trader)
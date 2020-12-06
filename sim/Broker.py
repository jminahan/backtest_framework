from sim.TimeSlice import TimeSlice
import utils.consts as consts
from sim.Trade import Trade
from sim.Trader import Trader
from sim.Asset import Asset

class Broker():

    currentTimeSlice : TimeSlice = None
    traders : [Trader] = []

    def __init__(self, initTimeSlice : TimeSlice, traders : [Trader]) :
        self.currentTimeSlice = initTimeSlice
        self.traders = traders

    def setTimeSlice(self, newTimeSlice : TimeSlice):
        self.currentTimeSlice = newTimeSlice

    def takeTrade(self, trade : Trade, trader: Trader):
        self.verifyTrade(trade)
        self.verifyTrader(trader)
        if(trade.tradeAction == consts.TRADE_BUY):
            self.buy(trade, trader)
        elif(trade.tradeAction == consts.TRADE_SELL):
            self.sell(trade, trader)

    def takeTrades(self, trader : Trader, trades : [Trade]):
        self.verifyTrader(trader)
        for i in trades:
            self.verifyTrade(i)
            if(i.tradeAction == consts.TRADE_BUY):
                self.buy(trader, i)
            elif(i.tradeAction == consts.TRADE_SELL):
                self.sell(trader, i)

    def verifyTrade(self, trade: Trade):
        assert(trade.ticker in self.currentTimeSlice.assets.keys())

    def verifyTrader(self, trader : Trader):
        assert(trader in self.traders)
    
    def buy(self, trader : Trader, trade : Trade):
        ticker : str = trade.ticker
        asset : Asset = self.currentTimeSlice.assets[ticker]
        costToTrade : float = asset.historicalData.loc[self.currentTimeSlice.getKeyString()]["Close"] * trade.amt

        if(costToTrade > trader.cash):
            trade.modToCash(trader.cash)
        
        trader.cash = trader.cash - (trade.amt * asset.historicalData.loc[self.currentTimeSlice.getKeyString()]["Close"])
        if(ticker in trader.positions.keys() != None):
            trader.positions[ticker] = trader.positions[ticker] + trade.amt
        else:
            trader.positions[ticker] = trade.amt

    def sell(self, trader : Trader,trade : Trade):
        ticker : str = trade.ticker
        asset : Asset = self.currentTimeSlice.assets[ticker]
        
        if(ticker in trader.positions.keys() and
                trader.positions[ticker] < trade.amt):
            trade.modToPosition(trader.positions[ticker])

        trader.cash = trader.cash + (trade.amt * asset.historicalData.loc[self.currentTimeSlice.getKeyString()]["Close"])
        trader.positions[ticker] = trade.amt
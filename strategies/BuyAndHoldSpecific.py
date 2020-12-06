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
    trader : Trader = None

    def __init__(self,ticker : str, 
                    title : str):
        self.title = title
        self.ticker = ticker

    def getTradeSignals(self, currentTimeSlice : TimeSlice):
        retSignals = []
        if(currentTimeSlice.currentTime == self.sim.startDate):
            retSignals.append(self.generateBuySignal(currentTimeSlice))
        elif(currentTimeSlice.currentTime == self.sim.endDate):
            sellSignal = self.generateSellSignal()
            if(sellSignal):
                retSignals.append(sellSignal)
        return retSignals

    def generateBuySignal(self,currentTimeSlice : TimeSlice):
        closeValueOfStock = currentTimeSlice.assets[self.ticker].historicalData.loc[currentTimeSlice.getKeyString()]["Close"]
        amt = self.trader.cash // closeValueOfStock
        return Trade(consts.TRADE_BUY, self.ticker, amt)

    def generateSellSignal(self):
        amt = self.trader.positions[self.ticker]
        if(amt):
            return Trade(consts.TRADE_SELL, self.ticker, amt)
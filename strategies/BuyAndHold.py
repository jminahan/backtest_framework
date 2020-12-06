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
class BuyAndHold(Strategy):
    sim = None
    title = None
    trader : Trader = None
    def __init__(self, title : str):
        self.title = title

    def getTradeSignals(self, currentTimeSlice : TimeSlice):
        retSignals = []
        if(currentTimeSlice.currentTime == self.sim.startDate):
            ##First day of sim, buy
            cashPerTrade = self.trader.cash // len(self.sim.tickerList)
            for i in self.sim.tickerList:
                retSignals.append(self.generateBuySignal(cashPerTrade, i, currentTimeSlice))
        elif(currentTimeSlice.currentTime == self.sim.endDate):
            for i in self.sim.tickerList:
                sellSignal = self.generateSellSignal(i, self.trader)
                if(sellSignal):
                    retSignals.append(sellSignal)
        return retSignals

    def generateBuySignal(self, cashPerTrade : int,
                                ticker : str,
                                currentTimeSlice : TimeSlice):
        closeValueOfStock = currentTimeSlice.assets[ticker].historicalData.loc[currentTimeSlice.getKeyString()]["Close"]
        amt = cashPerTrade // closeValueOfStock
        return Trade(consts.TRADE_BUY, ticker, amt)

    def generateSellSignal(self, ticker : str):
        amt = self.trader.positions[ticker]
        if(amt):
            return Trade(consts.TRADE_SELL, ticker, amt)
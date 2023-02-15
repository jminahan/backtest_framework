from strategies.Strategy import Strategy
from sim.TraderStats import TraderStats
from sim.TimeSlice import TimeSlice
import utils.consts as consts
from sim.Trade import Trade

'''
This class is used to simulate what a trader with a given
set of strategies @ a specific allocation would trade at
'''
class Trader():
    
    ##Instance of trader stats : used to keep a
    ##  timeslice log of performance and actions
    stats : TraderStats = None

    ##A dict in the form of Strategy : allocation
    ## where allocation is percent risk of portfolio
    strategies : {} = {}
    
    '''
    Init method
        params:
            strategies - list of strategy objects
            lever - unused TODO
    '''
    def __init__(self, 
                strategiesAndAllocations : [{}],
                leverage : int = 1):
        self.strategies = strategiesAndAllocations
        self.stats = TraderStats()
        self.positions = {}
        self.cash = 100000

    '''
    Update stats according to broker
    '''
    def updateStats(self, broker):
        self.updatePortfolioValue(broker)

    '''
    TODO
    '''
    def finalUpdateStats(self):
        pass
    
    '''
    Get the signals from each strategy then rebalance portfolio
    according to allocation of strategies.values()
    '''
    def getTradeRequests(self, currentTimeSlice : TimeSlice):
        strengths_by_strat = {}

        for strategy in self.strategies.keys():
            strengths_by_strat[strategy] = strategy.getTradeSignals(currentTimeSlice)

        targetPortfolio = self.rebalanceWeights(strengths_by_strat)
        trades = self.genTrades(targetPortfolio)

        return trades

    def genTrades(self, targetPortfolio):
        trades = []
        for i in self.positions.keys():
            if i in targetPortfolio.keys():
                targetPortfolio[i] = targetPortfolio[i] - self.positions[i]

        for i in targetPortfolio.keys():
            if(targetPortfolio[i] > 0):
                trades.append(Trade(
                    consts.TRADE_BUY,
                    i,
                    targetPortfolio[i]
                ))
            else:
                trades.append(Trade(
                    consts.TRADE_SELL,
                    i,
                    targetPortfolio[i]
                ))

        return trades

    '''
    Generate trades according to the following
    (sum of strategy values * allocation) -> buy stocks up to cash weighting of that
    TODO this is currently cash weighted, not risk weighted
    '''
    def rebalanceWeights(self, strengths_by_strat):
        rebalancedWeights = {}
        for strat in strengths_by_strat.keys():
            weights = strengths_by_strat[strat]
            total_strength_of_strat = self.sum(strengths_by_strat[strat])

            for t in strengths_by_strat[strat]:
                ticker = list(t.keys())[0]
                strength = t[ticker]

                portfolioPerTicker = self.genAbsolutePortfolioAmount(strength, ticker, strat)
                if(ticker not in rebalancedWeights.keys()):
                    rebalancedWeights[ticker] = portfolioPerTicker
                else:
                    rebalancedWeights[ticker] += portfolioPerTicker
        return rebalancedWeights

    def genAbsolutePortfolioAmount(self, strength, ticker, strat):
        strength_by_allocation = strength * self.strategies[strat]
        currentAssetCost = self.sim.broker.getCurrentAssetPrice(ticker, self.sim.broker.currentTimeSlice)
        numToBuySellOfTicker = (self.getPortfolioValue(self.sim.broker) * strength_by_allocation) // currentAssetCost
        return numToBuySellOfTicker
    '''
    Gets value of portfolio (positions + cash)
    at current time slice
    '''
    def updatePortfolioValue(self, broker):
        portfolioValue = 0
        portfolioValue += self.cash
        for i in self.positions.keys():
            portfolioValue += broker.getCurrentAssetPrice(i, broker.currentTimeSlice) * self.positions[i]
        self.stats.portfolioValueByTimeSlice[broker.currentTimeSlice] = portfolioValue

    def getPortfolioValue(self, broker):
        portfolioValue = 0
        portfolioValue += self.cash
        for i in self.positions.keys():
            portfolioValue += broker.getCurrentAssetPrice(i, broker.currentTimeSlice) * self.positions[i]

        return portfolioValue


    '''
    TODO should this be a util?
    '''
    def sum(self, list_values):
        total = 0.0
        for i in list_values:
            for strength in i.values():
                total = total + strength
        return total
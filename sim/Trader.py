from strategies.Strategy import Strategy
from sim.TraderStats import TraderStats

class Trader():
    strat : Strategy = None
    stats : TraderStats = None
    
    def __init__(self, strategy : Strategy):
        self.strat = strategy
        self.stats = TraderStats()
        self.positions = {}
        self.cash = 100000

    def updateStats(self, broker):
        self.updatePortfolioValue(broker)

    def finalUpdateStats(self):
        pass

    def updatePortfolioValue(self, broker):
        portfolioValue = 0
        portfolioValue += self.cash
        for i in self.positions.keys():
            portfolioValue += broker.getCurrentAssetPrice(i, broker.currentTimeSlice) * self.positions[i]
        self.stats.portfolioValueByTimeSlice[broker.currentTimeSlice] = portfolioValue
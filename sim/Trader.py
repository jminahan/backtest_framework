from strategies.Strategy import Strategy

class Trader():
    positions = {}
    cash = 100000.0
    strat : Strategy = None
    
    def __init__(self, strategy : Strategy):
        self.strat = strategy
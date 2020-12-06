import utils.consts as consts

class Trade():
    tradeAction : str = None
    ticker : str = None
    amt : str = None

    def __init__(self, tradeAction : str, ticker : str, amt : int):
        self.verifyInputs(tradeAction, ticker, amt)
        self.tradeAction = tradeAction
        self.ticker = ticker
        self.amt = amt

    def verifyInputs(self, tradeAction, ticker, amt):
        assert(tradeAction in consts.VALID_TRADE_TYPES)

    def modToCash(self, cash : float, cost: float):
        self.amt = cash // cost

    def modToPosition(self, positionAmount : int):
        self.amt = positionAmount
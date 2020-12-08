import pandas as pd

class Finops():
    def __init__(self):
        pass

    @staticmethod
    def calculateAlpha(dfStrat : pd.DataFrame, dfBenchMark : pd.DataFrame):
        returns = (dfStrat["Close"][-1] - dfStrat["Close"][1]) / dfStrat["Close"][1]
        returnsBenchmark (dfBechMark["Close"][-1] - dfBenchMark["Close"][1]) / dfStrat["Close"][1]

        return returns - returnsBenchmark

    @staticmethod
    def calculateSharpe(dfStrat: pd.DataFrame, dfBenchmark : pd.DataFrame):
        """
        The dfstrat should be running value of how much the portfolio was worth
        via Trader states
        """

        ##NOTE: TODO we are assuming the risk free rate is inconsequential
        ##  I'm not sure this is a fair assumption

        dfStratMovement = Finops.priceToPctChange(dfStrat)
        dfBenchmarkMovement = Finops.priceToPctChange(dfBenchmark)
        dfExcessReturns : pd.DataFrame = dfStratMovement - dfBenchmarkMovement
        excessReturnStdDev = dfExcessReturns.std(0)
        returns = (dfStrat["Close"][-1] - dfStrat["Close"][1]) / dfStrat["Close"][1]

        return returns/(excessReturnsStdDev["Close"])

    @staticmethod
    def calculateBeta(dfStrat : pd.DataFrame, dfBenchMark : pd.DataFrame) -> float:
        """
        the dfStrat should be a running value of how much the portfolio was worth via TraderStats
        same with dfBenchMark
        """
        dfStratMovement = Finops.priceToPctChange(dfStrat)
        dfBenchMarkMovement = Finops.priceToPctChange(dfBenchMark)
        corr = dfStratMovement["Close"].corr(dfBenchMarkMovement["Close"])
        stdDevStrat = dfStratMovement["Close"].std()
        stdDevBench = dfBenchMarkMovement["Close"].std()

        return corr * (stdDevStrat/stdDevBench)

    @staticmethod
    def priceToPctChange(df : pd.DataFrame, header : [str] = ["Close"]) -> pd.DataFrame:
        '''
        take a df and a header to convert to returns

        defaults to Close,
        but can pass in something like "Open"
        up to the user at that point to make sure it works
        '''
        returnDF = (df[header] - df[header].shift(1))/df[header].shift(1)
        return returnDF

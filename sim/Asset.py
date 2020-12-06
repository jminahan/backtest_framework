import pandas as pd

"""
An asset as it exists in a TimeSlice

For example, this shoudl capture all of AAPL on 12/1/2020
Including all its history
"""
class Asset():

    historicalData : pd.DataFrame = None
    def __init__(self, historicalData : pd.DataFrame):
        self.historicalData = historicalData

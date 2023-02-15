###
#   Build YahooHistoricalData Model objects
###

## imports -- external
import logging
import pandas as pd

##imports -- models
from models.YahooHistoricalData import YahooHistoricalData

class YahooHistoricalDataBuilder():

    def __init__(self):
        logging.debug("in YahooHistoricalData Model Builder")


    def build(self, df : pd.DataFrame) -> YahooHistoricalData:
        """
        Takes a df

        and outputs a YahooHistoricalData
        """
        return YahooHistoricalData(
            historicalData=df
        )
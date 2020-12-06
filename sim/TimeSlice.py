from sim.Asset import Asset
import datetime
from models.conf.Symbol import Symbol

"""
This will be what the world was like on a day
"""
class TimeSlice():

    assets = {}
    currentTime = None

    def __init__(self, tickerList : [str], 
                    universeStartTime : datetime.datetime,
                    currentTime : datetime.datetime):
        self.currentTime = currentTime
        self.initAssets(tickerList, universeStartTime, currentTime)

    def initAssets(self, tickerList : [str], startTime : datetime.datetime, currentTime : datetime.datetime):
        """
        Initialize assets of this time slice
        """
        for i in tickerList:
            assetSymbol : Symbol = Symbol.objects(ticker=i)[0]
            startTimeKey : str = startTime.strftime("%Y-%m-%d")
            currentTimeKey : str = currentTime.strftime("%Y-%m-%d")
            assetTimeSliceHistoricalData = assetSymbol.yHistoricalData.historicalData.set_index("Date").loc[startTimeKey :currentTimeKey]
            iterAsset = Asset(assetTimeSliceHistoricalData)
            self.assets[i] = iterAsset

    def getKeyString(self) -> str:
        return self.currentTime.strftime("%Y-%m-%d")
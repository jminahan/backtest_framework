from sim.Asset import Asset
import datetime
from models.conf.Symbol import Symbol

"""
This will be what the world was like on a day
"""
class TimeSlice():

    assets = {}
    currentTime = None
    prevTimeSlice = None

    def __init__(self, tickerListDict : {}, 
                    universeStartTime : datetime.datetime,
                    currentTime : datetime.datetime,
                    prevTimeSlice):
        self.currentTime = currentTime
        self.initAssets(tickerListDict, universeStartTime, currentTime)
        self.prevTimeSlice = prevTimeSlice

    def initAssets(self, tickerListDict : {}, startTime : datetime.datetime, currentTime : datetime.datetime):
        """
        Initialize assets of this time slice
        """
        for i in tickerListDict.keys():
            startTimeKey : str = startTime.strftime("%Y-%m-%d")
            currentTimeKey : str = currentTime.strftime("%Y-%m-%d")
            assetTimeSliceHistoricalData = tickerListDict[i]["HistoricalData"].set_index("Date").loc[startTimeKey :currentTimeKey]
            iterAsset = Asset(assetTimeSliceHistoricalData)
            self.assets[i] = iterAsset

    def getKeyString(self) -> str:
        return self.currentTime.strftime("%Y-%m-%d")
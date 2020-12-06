####
#   Yahoo Finance Utils
####

#imports
import logging
import requests
import datetime

class YahooUtils():

    def __init__(self):
        logging.debug("Yahoo Utils Initialized")

    def getTickerHistoricalPrice(self, symbol, startDate, endDate, interval="1d") -> str:
        """
        Takes a:
            symbol :: "AAPL"
            startDate :: datetime.datetime(2020, 1, 1)
            endDate :: datetime.datetime(2020, 1, 1)
            interval :: in range of [1d]

        Pulls a link like this one:

        https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1575411457&period2=1607033857&interval=1d&events=history&includeAdjustedClose=true

        and returns a pandas df
        """
        urlString = self.queryBuilder(symbol, startDate, endDate, interval)
        reqObj = self.performRequest(urlString)
        self.isRequestOkay(reqObj, symbol)
        return reqObj.content
    def isRequestOkay(self, requestObj : requests.Request, ticker : str):
        """
        Takes a:
            request object

        and performs checks to make sure its what we want
        """
        if(requestObj.status_code == 200):
            pass
        else:
            logging.debug("Ticker : [{}] has status code {}".format(ticker, requestObj.status_code))

    def performRequest(self, urlString : str) -> requests.Request:
        """
        Takes a:
            urlString :: https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1575411457&period2=1607033857&interval=1d&events=history&includeAdjustedClose=true

        and returns
            a request object
        """
        return requests.get(urlString)

    def queryBuilder(self, symbol :str, startDate : datetime.datetime, endDate : datetime.datetime, interval:str) -> str:
        """
        Takes a:
            symbol :: "AAPL"
            startDate :: datetime.datetime(2020, 1, 1)
            endDate :: datetime.datetime(2020, 1, 1)
            interval :: in range of [1d]

        and returns a string like below:
            https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1575411457&period2=1607033857&interval=1d&events=history&includeAdjustedClose=true

        """

        #TODO fix this to go from datetime to seconds
        secondsStart = startDate
        secondsEnd = endDate
        return "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval={}&events=history&includeAdjustedClose=true".format(
            symbol, secondsStart, secondsEnd, interval
        )
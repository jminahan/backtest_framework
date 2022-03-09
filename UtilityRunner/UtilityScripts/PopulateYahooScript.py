from operator import eq
from .UtilityScriptBase import UtilityScriptBase
import logging
from .Exceptions.ArgNotFoundException import ArgNotFoundException
import json
import logging
import requests
import datetime
from Domain.EquityCorporateData import EquityCorporateData
from mongoengine import connect
from Domain.HistoricalData import HistoricalData
import pandas
from io import StringIO

class PopulateYahooScript(UtilityScriptBase):
    def __init__(self):
        UtilityScriptBase.__init__( self )
        logging.debug("In Example Utility Script")
        ##Change Description
        self.description = "This to populate the mongo db with Yahoo Historical Data script"

        ##Init args
        self.args["DB_CONNECTION"] = None
        self.args["DB_HOST"] = None
        self.args["DB_PORT"] = None
        self.args["DEFAULT_YAHOO_HISTORICAL_START_DATE"] = None
        self.args["DEFAULT_YAHOO_HISTORICAL_END_DATE"] = None
        self.args["outputFile"] = None

        self.tickerOutputs = {"200":[], "404":[],"443":[]}



    def run(self):
        logging.debug("Attemptign to run Populate Yahoo Script")
        self.queryArg("DB_CONNECTION", self.args, "What DB Connection?\nValue: \t")
        self.queryArg("DB_HOST", self.args, "What DB Host?\nValue: \t")
        self.queryArg("DB_PORT", self.args, "What DB Port?\nValue: \t")
        self.queryArg("DEFAULT_YAHOO_HISTORICAL_START_DATE", self.args, "What Start date?\nValue: \t")
        self.queryArg("DEFAULT_YAHOO_HISTORICAL_END_DATE", self.args, "What end date?\nValue: \t")
        self.queryArg("outputFile", self.args, "What output file?\nValue: \t")
        logging.debug("args successfully set")

        connect(self.args["DB_CONNECTION"], host=self.args["DB_HOST"], port=int(self.args["DB_PORT"]))
        logging.debug("Connected to DB")
        listOfEquitys = self.getEquityObjects()
        logging.debug("List of equity objects with : " + str(len(listOfEquitys)) + " retrieved")

        for equity in listOfEquitys:
            associatedHistorical = self.getAssociatedHistorical(equity)
            if(associatedHistorical is None):
                logging.debug("associatedHistorical for equity : " + equity.ticker + " is none, attempting to populate")
                yhDataStr = self.getTickerHistoricalPrice(
                    symbol = equity.ticker,
                    startDate = self.args["DEFAULT_YAHOO_HISTORICAL_START_DATE"],
                    endDate = self.args["DEFAULT_YAHOO_HISTORICAL_END_DATE"]
                )
                logging.debug("yhDataStr for equity : " + equity.ticker + " successfully retrieved")

                yhDataDF = self.stringcsvToDf(yhDataStr)
                yhdataDoc = self.buildHistoricalData(
                    yhDataDF,
                    equity
                )
                logging.debug("yhdataDoc for equity : " + yhdataDoc.associatedEquity.ticker + " successfully created")

                yhdataDoc.save()

                logging.debug("yhdataDoc has been saved")
        f = open(self.args["outputFile"], "w")
        json.dump(self.tickerOutputs, f)
        f.close()


    def runWithArgFile(self, argFile):
        self.parseArgFile(argFile)
        self.validateArgs()
        self.run()

    def parseArgFile(self, argFile):
        f = open(argFile)
        data = json.load(f)
        for i in data:
            self.args[i] = data[i]

    def validateArgs(self):
        if(self.args["DB_CONNECTION"] == None):
            raise ArgNotFoundException("DB_CONNECTION")
        if(self.args["DB_PORT"] == None):
            raise ArgNotFoundException("DB_PORT")
        if(self.args["DB_HOST"] == None):
            raise ArgNotFoundException("DB_HOST")

    ##### Utils

    def getTickerHistoricalPrice(self, symbol, startDate, endDate, interval="1d") -> str:
        """
        Takes a:
            symbol :: "AAPL"
            startDate :: datetime.datetime(2020, 1, 1)
            endDate :: datetime.datetime(2020, 1, 1)
            interval :: in range of [1d]

        Pulls a link like this one:
        https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1615248000&period2=1646784000&interval=1d&events=history&includeAdjustedClose=true    
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
            self.tickerOutputs["200"].append(ticker)
        elif(requestObj.status_code == 404):
            self.tickerOutputs["404"].append(ticker)
            logging.warn("Identified probably a delisted equity")
        else:
            self.tickerOutputs["443"].append(ticker)
            logging.debug("Ticker : [{}] has status code {}".format(ticker, requestObj.status_code))

    def performRequest(self, urlString : str) -> requests.Request:
        """
        Takes a:
            urlString :: https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1575411457&period2=1607033857&interval=1d&events=history&includeAdjustedClose=true

        and returns
            a request object
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        return requests.get(urlString, headers=headers)

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

        secondsStart = startDate
        secondsEnd = endDate
        return "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval={}&events=history&includeAdjustedClose=true".format(
            symbol, secondsStart, secondsEnd, interval
        )

    def getEquityObjects(self) -> [EquityCorporateData]:
        return EquityCorporateData.objects

    def getAssociatedHistorical(self, associatedEquityObj : EquityCorporateData):
        return HistoricalData.objects(associatedEquity=associatedEquityObj).first()

    def stringcsvToDf(self,
                        stringCSV : str,
                        delim : str = ",") -> pandas.DataFrame:
        """
        takes a string and returns a dataframe from it
        """
        return pandas.read_csv(StringIO(stringCSV.decode("utf-8")), delim)

    def buildHistoricalData(self, df : pandas.DataFrame, equity : EquityCorporateData) -> HistoricalData:
        """
        Takes a df

        and outputs a YahooHistoricalData
        """
        return HistoricalData(
            associatedEquity=equity,
            historicalData=df
        )
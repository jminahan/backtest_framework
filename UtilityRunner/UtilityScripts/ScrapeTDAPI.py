from operator import eq
from time import sleep
from .UtilityScriptBase import UtilityScriptBase
import logging
from .Exceptions.ArgNotFoundException import ArgNotFoundException
import json
import logging
import requests
import datetime
from Domain.EquityCorporateData import EquityCorporateData
from mongoengine import connect
import pandas
from io import StringIO
from Domain.TDApiDataDocument import TdApiDataDocument

class ScrapeTdApi(UtilityScriptBase):
    def __init__(self):
        UtilityScriptBase.__init__( self )
        logging.debug("In TD API Script")
        ##Change Description
        self.description = "This to populate the mongo db with data from the TD API (L1 + L2?)"

        ##Init args
        self.args["DB_CONNECTION"] = None
        self.args["DB_HOST"] = None
        self.args["DB_PORT"] = None
        self.args["DEFAULT_TD_HISTORICAL_START_DATE"] = None
        self.args["DEFAULT_TD_HISTORICAL_END_DATE"] = None
        self.args["outputFile"] = None
        self.args["API_KEY"] = None

        self.tickerOutputs = {"200":[], "404":[],"443":[]}



    def run(self):
        logging.debug("Attemptign to run TD Script")
        self.queryArg("DB_CONNECTION", self.args, "What DB Connection?\nValue: \t")
        self.queryArg("DB_HOST", self.args, "What DB Host?\nValue: \t")
        self.queryArg("DB_PORT", self.args, "What DB Port?\nValue: \t")
        self.queryArg("DEFAULT_TD_HISTORICAL_START_DATE", self.args, "What Start date?\nValue: \t")
        self.queryArg("DEFAULT_TD_HISTORICAL_END_DATE", self.args, "What end date?\nValue: \t")
        self.queryArg("outputFile", self.args, "What output file?\nValue: \t")
        self.queryArg("API_KEY", self.args, "What API_KEY?\nValue: \t")
        logging.debug("args successfully set")

        connect(self.args["DB_CONNECTION"], host=self.args["DB_HOST"], port=int(self.args["DB_PORT"]))
        logging.debug("Connected to DB")
        listOfEquitys = self.getEquityObjects()
        logging.debug("List of equity objects with : " + str(len(listOfEquitys)) + " retrieved")

        for equity in listOfEquitys:
            associatedHistorical = self.getAssociatedTdApiDataDocument(equity)
            if(associatedHistorical is None):
                logging.debug("associatedHistorical for equity : " + equity.ticker + " is none, attempting to populate")
                tdDataStr = self.getTickerTdData(
                    symbol = equity.ticker,
                    startDate = self.args["DEFAULT_TD_HISTORICAL_START_DATE"],
                    endDate = self.args["DEFAULT_TD_HISTORICAL_END_DATE"]
                )
                logging.debug("tdDataStr for equity : " + equity.ticker + " successfully retrieved")

                tdDataDf = self.stringcsvToDf(json.loads(tdDataStr))
                tdDataDoc = self.buildTdData(
                    tdDataDf,
                    equity
                )
                logging.debug("tdDataDoc for equity : " + tdDataDoc.associatedEquity.ticker + " successfully created")
                tdDataDoc.save()
                sleep(1)

                logging.debug("tdDataDoc has been saved")
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

    def getTickerTdData(self, symbol, startDate, endDate, interval="1d") -> str:
        """
        Takes a:

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
        https://api.tdameritrade.com/v1/marketdata/A/pricehistory?apikey=HAR7XXUTOYYSXAKGMGWZKPT4L09CUSWT&frequencyType=minute&frequency=30&endDate=1645140011000&startDate=1643757611000

        """

        millisecondsStart = startDate
        millisecondsEnd = endDate
        frequencyType = "minute"
        frequency = "30"
        apiKey = self.args["API_KEY"]
        return "https://api.tdameritrade.com/v1/marketdata/{}/pricehistory?apikey={}&frequencyType={}&frequency={}&endDate={}&startDate={}".format(
            symbol, apiKey, frequencyType, frequency, millisecondsStart, millisecondsStart
        )

    def getEquityObjects(self) -> [EquityCorporateData]:
        return EquityCorporateData.objects

    def getAssociatedTdApiDataDocument(self, associatedEquityObj : EquityCorporateData):
        return TdApiDataDocument.objects(associatedEquity=associatedEquityObj).first()

    def stringcsvToDf(self,
                        data : dict,
                        delim : str = ",") -> pandas.DataFrame:
        """
        takes a string and returns a dataframe from it
        """
        return pandas.DataFrame.from_dict(data)

    def buildTdData(self, df : pandas.DataFrame, equity : EquityCorporateData) -> TdApiDataDocument:
        """
        Takes a df

        and outputs a TdApiDataDocument
        """
        return TdApiDataDocument(
            associatedEquity=equity,
            dataDump=df
        )
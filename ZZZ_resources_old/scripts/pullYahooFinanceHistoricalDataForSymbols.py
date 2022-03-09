from utils.src.pandasinterface.pandasinterface import PandasInterface
from utils.src.modelbuilder.YahoHistoricalDataBuilder import YahooHistoricalDataBuilder;
from utils.src.mongointerface.mongointerface import MongoInterface
from utils.src.mongointerface.modelutils.SymbolMongoInterface import SymbolMongoInterface
from utils.src.web.yahoo import YahooUtils
from models.conf.Symbol import Symbol
import utils.consts as consts
from resources.scripts.Script import Script
import datetime
from models.DataFrameField import DataFrameField
import logging

class PullYahooFinancialHistoricalDataForSymbols(Script):
    def __init__(self):
        logging.debug("In PullYahooFinancialHistoricalDataForSymbols Script")

    @staticmethod
    def run():
        params = {
            consts.DB_CONNECTION_FIELD : consts.DB_CONNECTION,
            consts.DB_CONNECTION_HOST_FIELD : consts.DB_CONNECTION_HOST,
            consts.DB_CONNECTION_PORT_FIELD : consts.DB_CONNECTION_PORT
        }

        pdInterface = PandasInterface()
        yahooHistoricalDataBuilder = YahooHistoricalDataBuilder()
        monInterface = MongoInterface(params)
        symbolMongoInterface = SymbolMongoInterface(monInterface)
        yahooUtils = YahooUtils()

        listOfSymbols : [Symbol] = symbolMongoInterface.getSymbols()

        for symbol in listOfSymbols:
            if(symbol.yHistoricalData is None):
                yhDataStr = yahooUtils.getTickerHistoricalPrice(
                    symbol = symbol.ticker,
                    startDate = consts.DEFAULT_YAHOO_HISTORICAL_START_DATE,
                    endDate = consts.DEFAULT_YAHOO_HISTORICAL_END_DATE
                )
                yhDataDF = pdInterface.stringcsvToDf(yhDataStr)
                yhdataDoc = yahooHistoricalDataBuilder.build(
                    yhDataDF
                )
                monInterface.saveDocument(yhdataDoc)
                symbol.yHistoricalData = yhdataDoc
                symbol.lastUpdate = datetime.datetime.today()
                symbol.save()
            elif(symbol.lastUpdate.strftime("%Y%m%d") != datetime.datetime.today().strftime("%Y%m%d")):
                secondsStart = consts.DEFAULT_YAHOO_HISTORICAL_START_DATE
                secondsEnd = consts.DEFAULT_YAHOO_HISTORICAL_END_DATE

                ##Get yh data doc max
                yhDataStr = yahooUtils.getTickerHistoricalPrice(
                    symbol = symbol.ticker,
                    startDate = consts.DEFAULT_YAHOO_HISTORICAL_START_DATE,
                    endDate = consts.DEFAULT_YAHOO_HISTORICAL_END_DATE
                )
                
                yhDataDF = pdInterface.stringcsvToDf(yhDataStr)
                yhdataDoc = yahooHistoricalDataBuilder.build(
                    yhDataDF
                )

                monInterface.saveDocument(yhdataDoc)

                ##delete old doc of yhistorical data
                oldDoc = symbol.yHistoricalData
                oldDoc.delete()

                #update symbol
                symbol.yHistoricalData = yhdataDoc
                symbol.lastUpdate = datetime.datetime.today()
                symbol.save()

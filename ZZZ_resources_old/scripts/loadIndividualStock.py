from utils.src.pandasinterface.pandasinterface import PandasInterface
from utils.src.modelbuilder.SymbolBuilder import SymbolBuilder;
from utils.src.mongointerface.mongointerface import MongoInterface
import utils.consts as consts
from resources.scripts.Script import Script
import datetime
from utils.src.web.yahoo import YahooUtils
from utils.src.modelbuilder.YahoHistoricalDataBuilder import YahooHistoricalDataBuilder


class LoadIndividualStocks(Script):
    def __init__(self):
        logging.debug("In LoadNasdaqScreenerSymbol Script")
    
    @staticmethod
    def run():
        ##local consts
        TICKER = "ticker"
        YHISTORICALDAT = "yHistoricalData"
        LAST_UPDATE = "lastUpdate"
        COMMON_COMPANY_NAME = "commonCompanyName"
        IPO_YEAR = "ipoYear"
        INDUSTRY = "industry"
        SECTOR = "sector"
        COUNTRY = "country"
        MARKET_CAP = "marketCap"

        params = {
            consts.DB_CONNECTION_FIELD : consts.DB_CONNECTION,
            consts.DB_CONNECTION_HOST_FIELD : consts.DB_CONNECTION_HOST,
            consts.DB_CONNECTION_PORT_FIELD : consts.DB_CONNECTION_PORT
        }

        stocks = {
            "SPY" : {
                TICKER: "SPY",
                LAST_UPDATE: datetime.datetime.now(),
                COMMON_COMPANY_NAME: "SPDR S&P 500 ETF Trust (SPY)",
                IPO_YEAR: 1993,
                INDUSTRY : "ETF",
                SECTOR : "ETF",
                COUNTRY : "N/A",
                MARKET_CAP : -1.0
            }
        }

        pdInterface = PandasInterface()
        symbolBuilder = SymbolBuilder()
        monInterface = MongoInterface(params)
        yahooUtils = YahooUtils()
        yahooHistoricalDataBuilder = YahooHistoricalDataBuilder()
        for i in stocks:
            symbol = symbolBuilder.buildFromHand(
                stocks[i][TICKER],
                stocks[i][LAST_UPDATE],
                stocks[i][COMMON_COMPANY_NAME],
                stocks[i][IPO_YEAR],
                stocks[i][INDUSTRY],
                stocks[i][SECTOR],
                stocks[i][COUNTRY],
                stocks[i][MARKET_CAP]
            )
            yhDataStr = yahooUtils.getTickerHistoricalPrice(
                symbol = stocks[i][TICKER],
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

from utils.src.pandasinterface.pandasinterface import PandasInterface
from utils.src.modelbuilder.SymbolBuilder import SymbolBuilder;
from utils.src.mongointerface.mongointerface import MongoInterface
import utils.consts as consts
from resources.scripts.Script import Script


class LoadNasdaqScreenerSymbols(Script):
    def __init__(self):
        logging.debug("In LoadNasdaqScreenerSymbol Script")

    params = {
        consts.DB_CONNECTION_FIELD : consts.DB_CONNECTION,
        consts.DB_CONNECTION_HOST_FIELD : consts.DB_CONNECTION_HOST,
        consts.DB_CONNECTION_PORT_FIELD : consts.DB_CONNECTION_PORT
    }
    
    @staticmethod
    def run():
        pdInterface = PandasInterface()
        symbolBuilder = SymbolBuilder()
        monInterface = MongoInterface(params)
        nasdaqDF = pdInterface.fileToDf("resources/nasdaq_screener.csv")
        symbols = symbolBuilder.buildFromNasdaqDf(nasdaqDF)
        monInterface.saveDocuments(symbols)
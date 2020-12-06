import logging
from utils.src.mongointerface.modelutils.SymbolMongoInterface import SymbolMongoInterface
from utils.src.mongointerface.mongointerface import MongoInterface
from utils.src.pandasinterface.pandasinterface import PandasInterface
from models.conf.Symbol import Symbol
from models.YahooHistoricalData import YahooHistoricalData
from resources.scripts.Script import Script
import utils.consts as consts
import matplotlib.pyplot as plt
from utils.src.plot.PresetGraphs.SimpleLinePlot import SimpleLinePlot
from utils.src.finops.Finops import Finops

class PlotTest(Script):
    def __init__(self):
        logging.debug("In Plot Test")

    @staticmethod 
    def run():
        params = {
            consts.DB_CONNECTION_FIELD : consts.DB_CONNECTION,
            consts.DB_CONNECTION_HOST_FIELD : consts.DB_CONNECTION_HOST,
            consts.DB_CONNECTION_PORT_FIELD : consts.DB_CONNECTION_PORT
        }

        pdInterface = PandasInterface()
        monInterface = MongoInterface(params)
        symbolMongoInterface = SymbolMongoInterface(monInterface)
        simpleLinePlot = SimpleLinePlot()
        aaplSymbol = symbolMongoInterface.getByTicker("AAPL")
        df = aaplSymbol.yHistoricalData.historicalData[["Date", "Close", "Open"]].set_index("Date")
        returns = Finops.priceToPctChange(df, ["Close"])
        simpleLinePlot.buildPlot(returns)
        simpleLinePlot.show()
        


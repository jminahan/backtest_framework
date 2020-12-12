##python libraries
import logging
import datetime

##import utils
import utils.consts as consts

##import web utils
from utils.src.web.yahoo import YahooUtils

##import pandas utils
from utils.src.pandasinterface.pandasinterface import PandasInterface


###Builders
from utils.src.modelbuilder.SymbolBuilder import SymbolBuilder;
from utils.src.modelbuilder.YahoHistoricalDataBuilder import YahooHistoricalDataBuilder

##mongo interface
from utils.src.mongointerface.mongointerface import MongoInterface
from utils.src.mongointerface.modelutils.SymbolMongoInterface import SymbolMongoInterface

#scripts
from resources.scripts.Script import Script
from resources.scripts.loadNasdaqScreenerSymbols import LoadNasdaqScreenerSymbols
from resources.scripts.pullYahooFinanceHistoricalDataForSymbols import PullYahooFinancialHistoricalDataForSymbols
from resources.scripts.plotTest import PlotTest
from resources.scripts.loadIndividualStock import LoadIndividualStocks

##sim
from sim.Sim import Sim
from sim.TimeSlice import TimeSlice
from sim.Trader import Trader
from sim.Broker import Broker
from sim.Trade import Trade

##Strategies
from strategies.BuyAndHold import BuyAndHold
from strategies.BuyAndHoldSpecific import BuyAndHoldSpecific
from strategies.Strategy import Strategy

##finops utils
from utils.src.finops.Finops import Finops
class Main(Script):

    def __init__(self):
        logging.debug("Initialized Main Main")

        ##the below can be thought of as "ensuring the environment is correct"
        self.initializeConfigurationOptions()
        self.initializeLocalVars()
        self.runScripts()

    def run(self):
        """
        Run implentation of super script
        """
        self.sim.run(self.timeStepResponse)
        print(Finops.calculateSharpe(dfStrat=self.sim.traders[1].stats.portfolioValueByTimeSliceAsDf(),
                                        dfBenchmark=self.sim.traders[0].stats.portfolioValueByTimeSliceAsDf()))

    def timeStepResponse(self, currentTimeSlice : TimeSlice,
                            broker : Broker,
                            trader : Trader):
        """
        This is passed as a callback in run
        and is called once per trader per timestep
        """
        broker.takeTrades(trader.getTradeRequests(currentTimeSlice), trader)

    def initializeConfigurationOptions(self):
        self.params = {
                consts.DB_CONNECTION_FIELD : consts.DB_CONNECTION,
                consts.DB_CONNECTION_HOST_FIELD : consts.DB_CONNECTION_HOST,
                consts.DB_CONNECTION_PORT_FIELD : consts.DB_CONNECTION_PORT,
                consts.SIM_PARAMS_FIELD : {
                    consts.SIM_PARAMS_TICKER_LIST_FIELD : consts.SIM_PARAMS_TICKER_LIST,
                    consts.SIM_PARAMS_START_DATE_FIELD : consts.SIM_PARAMS_START_DATE,
                    consts.SIM_PARAMS_END_DATE_FIELD : consts.SIM_PARAMS_END_DATE
                }
        }

        self.scripts = {
            LoadNasdaqScreenerSymbols : False,
            PullYahooFinancialHistoricalDataForSymbols : False,
            PlotTest : False,
            LoadIndividualStocks : True
        }

    def initializeLocalVars(self):
        """
        Used to initialize things like Pandas Interface, YahooUtils, etc
        """
        self.yutils = YahooUtils()
        self.pdInterface = PandasInterface()
        self.yhDataBuilder = YahooHistoricalDataBuilder()
        self.symbolBuilder = SymbolBuilder()
        self.monInterface = MongoInterface(self.params)
        self.symbolMongoInterface = SymbolMongoInterface()

        self.strategies  =  [
                                        {BuyAndHoldSpecific("AAPL", consts.BUY_AND_HOLD_SPECIFIC_TITLE): .5,
                                            BuyAndHoldSpecific("SPY", consts.BUY_AND_HOLD_SPECIFIC_TITLE): .5},
                                        {BuyAndHoldSpecific("AAPL", consts.BUY_AND_HOLD_SPECIFIC_TITLE) : .5,
                                            BuyAndHoldSpecific("SPY", consts.BUY_AND_HOLD_SPECIFIC_TITLE) : .5}
                                        ]

        self.sim = Sim(
            self.params[consts.SIM_PARAMS_FIELD][consts.SIM_PARAMS_TICKER_LIST_FIELD],
            self.params[consts.SIM_PARAMS_FIELD][consts.SIM_PARAMS_START_DATE_FIELD],
            self.params[consts.SIM_PARAMS_FIELD][consts.SIM_PARAMS_END_DATE_FIELD],
            self.strategies
        )

    def runScripts(self):
        for i in self.scripts:
            if(self.scripts[i]):
                i.run()



# AAPLhistorical = yutils.getTickerHistoricalPrice("AAPL", "1575411457", "1607033857")
# AAPLdf = pdInterface.stringcsvToDf(AAPLhistorical)
# yahoohistoricaldatamodel = yhDataBuilder.build(AAPLdf)
# monInterface.saveDocument(yahoohistoricaldatamodel)

Main().run()
logging.debug("Completed main.py")
print("EXIT")
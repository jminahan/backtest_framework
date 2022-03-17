from UtilityRunner.UtilityScripts.UtilityScriptBase import UtilityScriptBase
import logging
from PortfolioEngine.PortfolioEngine import PortfolioEngine
from MarketManager.MarketManager import MarketManager
from DataEngine.DataEngine import DataEngine
from AccountantManager.AccountantManager import AccountantManager
from UtilityRunner.UtilityScripts.Exceptions.ArgNotFoundException import ArgNotFoundException
import json
from Domain.DTO.DataEngineConfigDTO import DataEngineConfigDTO
from Domain.DTO.MarketManagerConfigDTO import MarketManagerConfigDTO
from Domain.DTO.AccountantManagerConfigDTO import AccountantManagerConfigDTO
from Domain.DTO.PortfolioEngineConfigDTO import PortfolioEngineConfigDTO


class RunComponentScript(UtilityScriptBase):
    def __init__(self):
        UtilityScriptBase.__init__( self )
        logging.info("in Component runner")
        self.description = "Runs all Components and places orders"

        self.args["DATA_ENGINE_CONFIGS"] = None
        self.args["MARKET_MANAGER_CONFIGS"] = None
        self.args["ACCOUNTANT_MANAGER_CONFIGS"] = None
        self.args["PORTFOLIO_ENGINE_CONFIGS"] = None
        self.args["DATE"] = None
        self.args["UNIVERSE"] = None

    def runWithArgFile(self, argFile):
        self.parseArgFile(argFile)
        self.validateArgs()
        self.run()

    def run(self):
        logging.info("In run of RunComponentScript")
        self.validateArgs()

        dataEngine = DataEngine(DataEngineConfigDTO.fromjson(self.args["DATA_ENGINE_CONFIGS"]))
        marketManager = MarketManager(MarketManagerConfigDTO.fromjson(self.args["MARKET_MANAGER_CONFIGS"]), dataEngine.adapter, self.args["DATE"], self.args["UNIVERSE"])
        accountantManager = AccountantManager(AccountantManagerConfigDTO.fromjson(self.args["ACCOUNTANT_MANAGER_CONFIGS"]))
        portfolioEngine = PortfolioEngine(self.args["UNIVERSE"], PortfolioEngineConfigDTO.fromjson(self.args["PORTFOLIO_ENGINE_CONFIGS"]), marketManager, accountantManager)

        portfolioEngine.execute()


    def validateArgs(self):
        if(self.args["DATA_ENGINE_CONFIGS"] == None):
            raise ArgNotFoundException("DATA_ENGINE_CONFIGS")
        if(self.args["MARKET_MANAGER_CONFIGS"] == None):
            raise ArgNotFoundException("MARKET_MANAGER_CONFIGS")
        if(self.args["ACCOUNTANT_MANAGER_CONFIGS"] == None):
            raise ArgNotFoundException("ACCOUNTANT_MANAGER_CONFIGS")
        if(self.args["PORTFOLIO_ENGINE_CONFIGS"] == None):
            raise ArgNotFoundException("PORTFOLIO_ENGINE_CONFIGS")
        if(self.args["DATE"] == None):
            raise ArgNotFoundException("DATE")
        if(self.args["UNIVERSE"] == None):
            raise ArgNotFoundException("UNIVERSE")

    def parseArgFile(self, argFile):
        f = open(argFile)
        data = json.load(f)
        for i in data:
            self.args[i] = data[i]
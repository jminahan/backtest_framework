from Domain.BuildEnumMethods import BuildEnumMethods
from .UtilityScriptBase import UtilityScriptBase
import logging
from .Exceptions.ArgNotFoundException import ArgNotFoundException
import json
from mongoengine import connect
import pandas
from Domain.EquityCorporateData import EquityCorporateData


class LoadNasdaqTickers(UtilityScriptBase):
    def __init__(self):
        UtilityScriptBase.__init__( self )
        logging.debug("In Nasdaq Utility Script")
        ##Change Description
        self.description = "Loads tickers from nasdaq csv"

        ##Init args
        self.args["DB_CONNECTION"] = None
        self.args["DB_HOST"] = None
        self.args["DB_PORT"] = None
        self.args["pathToCsv"] = None

    def run(self):
        logging.debug("Prompting for value")
        self.queryArg("pathToCsv", self.args, "What is the path to the nasdaq csv??\nValue: \t")
        self.queryArg("DB_CONNECTION", self.args, "What DB Connection?\nValue: \t")
        self.queryArg("DB_HOST", self.args, "What DB Host?\nValue: \t")
        self.queryArg("DB_PORT", self.args, "What DB Port?\nValue: \t")
        connect(self.args["DB_CONNECTION"], host=self.args["DB_HOST"], port=int(self.args["DB_PORT"]))
        nasdaqDF = self.fileToDf(self.args["pathToCsv"])
        equities = EquityCorporateData.build(BuildEnumMethods.DF, DF=nasdaqDF)
        equitiesInSystem = self.getEquityObjects()
        for i in equities:
            i.save()


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
        if(self.args["pathToCsv"] == None):
            raise ArgNotFoundException("pathToCsv")
        if(self.args["DB_CONNECTION"] == None):
            raise ArgNotFoundException("DB_CONNECTION")
        if(self.args["DB_PORT"] == None):
            raise ArgNotFoundException("DB_PORT")
        if(self.args["DB_HOST"] == None):
            raise ArgNotFoundException("DB_HOST")

    def fileToDf(self, filePath : str) -> pandas.DataFrame:
        return pandas.read_csv(filePath)            

    def getEquityObjects(self) -> [EquityCorporateData]:
        return EquityCorporateData.objects
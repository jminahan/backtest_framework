from .UtilityScriptBase import UtilityScriptBase
import logging
from .Exceptions.ArgNotFoundException import ArgNotFoundException
import json

class ExampleUtilityScript(UtilityScriptBase):
    def __init__(self):
        UtilityScriptBase.__init__( self )
        logging.debug("In Example Utility Script")
        ##Change Description
        self.description = "This is the description of the example script"

        ##Init args
        self.args["retVal"] = None

    def run(self):
        logging.debug("Prompting for value")
        self.queryArg("retVal", self.args, "What Value do you want to multiply by 3?\nValue: \t")
        logging.debug("The returned value will be " + str(int(self.args["retVal"]) * 3))
        return int(self.args["retVal"]) * 3

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
        if(self.args["retVal"] == None):
            raise ArgNotFoundException("retVal")

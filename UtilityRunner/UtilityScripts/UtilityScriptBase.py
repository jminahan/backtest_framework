import logging
from abc import ABC, abstractmethod


class UtilityScriptBase(ABC):
    def __init__(self):
        """
            description is a human readable description
        """
        self.description = "A Base Utility Script Description"
        self.args = {}

    @abstractmethod
    def run(self):
        logging.error("ERROR: A Utility script was called without an implemented abstract method")

    @abstractmethod
    def runWithArgFile(self, argFile):
        logging.error("ERROR: A Utility Script Was Called without an implemented abstract method")

    @abstractmethod
    def parseArgFile(self, argFile):
        logging.error("ERROR: A Utility Script Was Called without an implemented abstract method")

    @abstractmethod
    def validateArgs(self):
        logging.error("ERROR: A Utility Script Was Called without an implemented abstract method")

    def queryArg(self, argToFill, existArgs, message):
        if(argToFill in existArgs and existArgs[argToFill] is not None):
            return

        existArgs[argToFill] = input(message)

    def getDescription(self):
        return self.description

####
#
####

##imports -- external libraries
from mongoengine import *
import logging

##imports models

##import utils
import utils.consts as consts

class MongoInterface():

    requiredParams = [consts.DB_CONNECTION_FIELD,
                        consts.DB_CONNECTION_HOST_FIELD,
                        consts.DB_CONNECTION_PORT_FIELD]

    def __init__(self, params : dict):

        logging.debug("In MongoInterface")
        self.verifyParams(params)
        logging.debug("Params dict verified")
        self.connect(params)
        logging.debug("connected to mongodb, ready to interact")

    def saveDocument(self, doc : Document):
        """
        takes a document and saves it to a connected database
        """
        doc.save()

    def saveDocuments(self, documents : [Document]):
        """
        takes a list of documents and saves it to a connected database
        """
        for i in documents:
            self.saveDocument(i)

    def verifyParams(self, paramsDict : dict):
        """
        asserts characteristics of interface params
        """
        keys = paramsDict.keys()
        for i in self.requiredParams:
            assert(i in keys);

    def connect(self, params):
        connect(params[consts.DB_CONNECTION_FIELD], 
                        host=params[consts.DB_CONNECTION_HOST_FIELD], 
                        port=params[consts.DB_CONNECTION_PORT_FIELD])

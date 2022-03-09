from ..BaseAdapter.BaseAdapter import BaseAdapter
import logging
from mongoengine import connect as meConnect
from mongoengine import Document

class MongoConfig():
    DB_CONNECTION = "test"
    DB_CONNECTION_HOST = "localhost"
    DB_CONNECTION_PORT = 27017

class MongoAdapter(BaseAdapter):
    config : MongoConfig = MongoConfig()

    def __init__(self):
        logging.info("Mongo Adapter Initialized")
        self.connect()
        logging.info("Connection Attempting")


    def getCurrentData():
        pass

    def connect(self):
        meConnect(self.config.DB_CONNECTION, 
                        host=self.config.DB_CONNECTION_HOST, 
                        port=self.config.DB_CONNECTION_PORT)

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

    def removeDocument(self, doc : Document):
        doc.delete()
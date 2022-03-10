from tokenize import String

import pandas
from ..BaseAdapter.BaseAdapter import BaseAdapter
import logging
from mongoengine import connect as meConnect
from mongoengine import Document
import datetime
from Domain.EquityCorporateData import EquityCorporateData
from Domain.HistoricalData import HistoricalData

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

    def getCorporateInfo(self, universe: String) -> EquityCorporateData:
        """
            description:
                get a single corporate data

            params:
                a string ticker interested in

            returns:
                an equityCorporateData
        """
        return EquityCorporateData.objects(ticker=universe).first()


    def getCorporateInfos(self, universe : [String]) -> [EquityCorporateData]:
        """
            description:
                get multiple corporate datas

            params:
                list of string tickers you're interested in
            
            returns:
                a list of EquityCorporateData
        """
        return EquityCorporateData.objects(ticker__in=universe)


    def getDataForDate(self, date : datetime.datetime, universe : [String]) :
        """
            params:
                date you are intereste in received values for
                list of string tickers you are interested in
        """
        dayDf = pandas.DataFrame()
        equityObjects = self.getCorporateInfos(universe)
        for equity in equityObjects:
            historicalForEquity : HistoricalData = HistoricalData.objects(associatedEquity=equity).first()
            if(historicalForEquity is not None):
                historicalPriceDataFrame = historicalForEquity.historicalData
                dayDf = dayDf.append(historicalPriceDataFrame.set_index("Date").loc[date])
        dayDf["ticker"] = universe
        return dayDf
        

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
from Domain.BuildEnumMethods import BuildEnumMethods
from PortfolioEngine.Adapters.BaseAdapter.BaseAdapter import BaseAdapter
import logging
from PortfolioEngine.Components.Portfolio import Portfolio
from mongoengine import connect as meConnect
from Domain.PortfolioDocument import PortfolioDocument


class MongoConfig():
    DB_CONNECTION = "test"
    DB_CONNECTION_HOST = "localhost"
    DB_CONNECTION_PORT = 27017
    PROFILE = "default"

class MongoAdapter(BaseAdapter):
    config : MongoConfig = MongoConfig()

    def __init__(self):
        self.initializeCurrentPortfolio()

    def initializeCurrentPortfolio(self):
        self.connect()
        super().currentPortfolio = PortfolioDocument.objects(name = self.config.PROFILE).first().toPortfolio()

    def savePortfolio(self):
        doc = PortfolioDocument.build(method=BuildEnumMethods.MANUAL, tickerDistr = super().currentPortfolio.tickerDistr, name = self.config.PROFILE)
        potentialExisting : PortfolioDocument= PortfolioDocument.objects(name = self.config.PROFILE).first()
        if(potentialExisting is not None):
            potentialExisting.delete()
        doc.save()


    def connect(self):
        meConnect(self.config.DB_CONNECTION, 
                        host=self.config.DB_CONNECTION_HOST, 
                        port=self.config.DB_CONNECTION_PORT)

    
    def getCurrentPortfolio(self) -> Portfolio:
        return super().getCurrentPortfolio()
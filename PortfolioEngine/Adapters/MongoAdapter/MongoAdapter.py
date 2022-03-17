from Domain.OrderModels.OrderStatus import OrderStatus
from Domain.OrderModels.Order import Order
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
    currentPortfolio : Portfolio

    def __init__(self):
        self.initializeCurrentPortfolio()

    def initializeCurrentPortfolio(self):
        self.connect()
        try:
            portfolioDoc =  PortfolioDocument.objects(name = self.config.PROFILE).first()
            self.currentPortfolio = Portfolio()
            self.currentPortfolio.deepCopy(portfolioDoc)
            logging.info("Initialized currentPortfolio via DB")
        except:
            self.currentPortfolio = Portfolio()
            logging.info("Initialized currentPortfolio via manual building")


    def savePortfolio(self):
        doc = PortfolioDocument.build(method=BuildEnumMethods.MANUAL, tickerDistr = self.currentPortfolio.tickerAmounts, name = self.config.PROFILE)
        potentialExisting = None
        try:
            potentialExisting : PortfolioDocument= PortfolioDocument.objects(name = self.config.PROFILE).first()
        except:
            logging.warn("No existing portfolio document found")
        if(potentialExisting is not None):
            potentialExisting.delete()
        doc.save()


    def connect(self):
        meConnect(self.config.DB_CONNECTION, 
                        host=self.config.DB_CONNECTION_HOST, 
                        port=self.config.DB_CONNECTION_PORT)

    
    def getCurrentPortfolio(self) -> Portfolio:
        return self.currentPortfolio

    def executeTradeCallBack(self, oStatus : OrderStatus):
        c = oStatus.contract
        ticker = c.symbol
        amt = oStatus.order.total_quantity
        port = self.getCurrentPortfolio()
        port.tickerAmounts[ticker] = amt
        self.savePortfolio()
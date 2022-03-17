from mongoengine import Document, DictField, StringField
from Domain.BuildEnumMethods import BuildEnumMethods
from PortfolioEngine.Components.Portfolio import Portfolio


class PortfolioDocument(Document):
    tickerDistr = DictField(required=True)
    name = StringField(required=True, unique=True)

    @staticmethod
    def build(method : BuildEnumMethods, **kwargs) :
        if(method == BuildEnumMethods.MANUAL):
            return PortfolioDocument.manualBuild(kwargs)
        elif(method == BuildEnumMethods.DICT):
            return PortfolioDocument.dictbuild(kwargs)
        else:
            raise Exception("Unknown build enum method for PortfolioDocument : " + method)

    @staticmethod
    def dictBuild(kwargs):
        doc = PortfolioDocument()
        doc.tickerDistr = kwargs["dict"]["tickerDistr"]
        doc.name = kwargs["dict"]["name"]
        return doc

    @staticmethod
    def manualBuild(kwargs):
        doc = PortfolioDocument()
        doc.tickerDistr = kwargs["tickerDistr"]
        doc.name = kwargs["name"]
        return doc
        

    def toPortfolio(self) -> Portfolio:
        port = Portfolio()
        port.tickerAmounts = self.tickerDistr

        return port
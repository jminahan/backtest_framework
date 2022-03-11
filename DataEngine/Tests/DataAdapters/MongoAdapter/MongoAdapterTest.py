from DataEngine.DataAdapters.MongoAdapter.MongoAdapter import MongoAdapter
from Domain.EquityCorporateData import EquityCorporateData
from Domain.BuildEnumMethods import BuildEnumMethods
from datetime import date


ma : MongoAdapter = MongoAdapter()

testEquity = EquityCorporateData().build(
        method = BuildEnumMethods.MANUAL,
        ticker="test",
        commonCompanyName = "test",
        ipoYear = date.today(),
        industry = "test",
        sector = "test",
        country = "test"
)

def testConnect():
    assert(1 == 1)

def testSaveEquityCorporateDataDocument():
    ma.saveDocument(testEquity)

def testRemoveEquityCorporateDataDocument():
    ma.removeDocument(testEquity)

def getDataForDate():
    """
        This test assumes you have a fully loaded database

        Or at least a database with the following ticker in it with some data for that date
    """
    retDf = ma.getDataForDate("2020-01-30", ["AAPL", "A"])
    assert(retDf.loc[retDf["ticker"] == "AAPL"]["Close"][0] == 84.379997)

def getDataForDates():
    """
        This test assumes you have a fully loaded database

        Or at least a database with the following ticker in it with some data for that date
    """
    retDf = ma.getDataForDateRange("2020-01-01", "2020-01-30", ["AAPL", "A"])
    assert(retDf.loc[retDf["ticker"] == "AAPL"]["Open"][2] == 73.447502)

testConnect()
testSaveEquityCorporateDataDocument()
testRemoveEquityCorporateDataDocument()
getDataForDate()
getDataForDates()
from ....DataAdapters.MongoAdapter.MongoAdapter import MongoAdapter
from .....Domain.EquityCorporateData import EquityCorporateData
from .....Domain.BuildEnumMethods import BuildEnumMethods
from datetime import date


ma : MongoAdapter = MongoAdapter()

testEquity = EquityCorporateData()
testEquity.build(
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

testConnect()
testSaveEquityCorporateDataDocument()
testRemoveEquityCorporateDataDocument()
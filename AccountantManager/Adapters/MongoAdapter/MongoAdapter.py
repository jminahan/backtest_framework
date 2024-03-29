from AccountantManager.Adapters.BaseAdapter.BaseAdapter import BaseAdapter

class DefaultProfile():
    INITIAL_FREE_CAPITAL : int = 10000

class MongoAdapter(BaseAdapter):
    def __init__(self):
        super().__init__()
        self.initializeProfile()

    def initializeProfile(self):
        self.freeCapital = DefaultProfile().INITIAL_FREE_CAPITAL
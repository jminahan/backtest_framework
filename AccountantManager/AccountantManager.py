from Domain.DTO.AccountantManagerConfigDTO import AccountantManagerConfigDTO, AdapterType
from AccountantManager.Adapters.BaseAdapter.BaseAdapter import BaseAdapter
from AccountantManager.Adapters.MongoAdapter.MongoAdapter import MongoAdapter

class AccountantManager():
    adapter : BaseAdapter
    def __init__(self, configs : AccountantManagerConfigDTO):
        self.initializeAdapter(configs)

    def initializeAdapter(self, config : AccountantManagerConfigDTO):
        if(config.adapterType == AdapterType.MONGO):
            self.adapter = MongoAdapter()

    def getFreeCapital(self) -> float:
        return self.adapter.getFreeCapital()

    def adjustFreeCapital(self, change : float):
        return self.adapter.adjustFreeCapital(change)
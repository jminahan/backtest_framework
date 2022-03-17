from DataEngine.DataAdapters.MongoAdapter.MongoAdapter import MongoAdapter
import logging
from Domain.DTO.DataEngineConfigDTO import DataEngineConfigDTO, AdapterType
from DataEngine.DataAdapters.BaseAdapter.BaseAdapter import BaseAdapter

class DataEngine():
    config : DataEngineConfigDTO
    adapter : BaseAdapter

    def __init__(self, dataEngineConfigDTO : DataEngineConfigDTO):
        logging.info("Data Engine Initialized")
        dataEngineConfigDTO.validate()
        self.config = dataEngineConfigDTO
        self.adapter = self.initializeAdapter()

    def initializeAdapter(self) -> BaseAdapter:
        if(self.config.adapterType == AdapterType.MONGO):
            return MongoAdapter()
from DataEngine.DataAdapters.MongoAdapter.MongoAdapter import MongoAdapter
import logging
from domain.DTO.DataEngineConfigDTO import DataEngineConfigDTO, AdapterType
from .DataAdapters.BaseAdapter.BaseAdapter import BaseAdapter

def DataEngine():
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
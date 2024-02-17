from Housing.exception import HousingException
from Housing.logger import logging
import sys

from Housing.components.DataIngestion import DataIngestion
from Housing.config.configuration import Configuration
from Housing.entity.config_entity import DataIngestionConfig
from Housing.entity.artifact_entity import DataIngestionArtifact

class Pipeline:
    def __init__(self,config:Configuration=Configuration())->None:

        try:
            self.config=config

        except Exception as e:
            raise HousingException(e,sys) from e
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion=DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()

        except Exception as e:
            raise HousingException(e,sys) from e
        




"""
try:

except Exception as e:
raise HousingException(e,sys) from e
"""
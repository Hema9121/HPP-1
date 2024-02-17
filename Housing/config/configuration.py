from Housing.constant import *
from Housing.exception import HousingException
import sys
from Housing.entity.config_entity import *
from Housing.utils.util import read_yaml_file
from Housing.logger import logging

class Configuration():
    def __init__(self,
        config_file_path:str=CONFIG_FILE_PATH,
        time_stamp:str=CURRENT_TIME_STAMP
        )->None:

        try:
            self.config_info=read_yaml_file(file_path=config_file_path)
            self.time_stamp=time_stamp
            self.training_pipeline_config=self.get_training_pipeline_config()
        except Exception as e:
            raise HousingException(e,sys) from e
    
    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            training_pipeline_config=self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir=os.path.join(ROOT_DIR,training_pipeline_config[TRAINING_PIPELINE_NAME],
                                      training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_NAME])
            
            training_pipeline_config=TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"training pipeline config :{training_pipeline_config}")
            return training_pipeline_config
            
        except Exception as e:
            raise HousingException(e,sys) from e
        

    def get_data_ingestion_config(self)->DataIngestionConfig:
        
        try:
            artifact_dir=self.training_pipeline_config.artifact_dir

            data_ingestion_config=self.config_info[DATA_INGESTION_CONFIG_KEY]

            data_ingestion_artifact_dir=os.path.join(artifact_dir,DATA_INGESTION_ARTIFACT_DIR_NAME,
                                                     self.time_stamp)
            
            dataset_download_url=data_ingestion_config[DATA_INGESTION_DOWNLOAD_URL_KEY]

            tgz_download_dir=os.path.join(data_ingestion_artifact_dir,
                                          data_ingestion_config[DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY])
            
            raw_data_dir=os.path.join(data_ingestion_artifact_dir,
                                      data_ingestion_config[DATA_INGESTION_RAW_DATA_DIR_KEY])
            
            ingested_dir=os.path.join(data_ingestion_artifact_dir,
                                      data_ingestion_config[DATA_INGESTION_INGESTED_DIR_KEY])
            
            data_ingestion_train_dir=os.path.join(ingested_dir,
                                                  data_ingestion_config[DATA_INGESTION_INGESTED_TRAIN_DIR_KEY])
            
            data_ingestion_test_dir=os.path.join(ingested_dir,
                                                 data_ingestion_config[DATA_INGESTION_INGESTED_TEST_DIR_KEY])
            
            data_ingestion_config=DataIngestionConfig(dataset_download_url=dataset_download_url,
                                                      raw_data_dir=raw_data_dir,
                                                      tgz_download_dir=tgz_download_dir,
                                                      ingested_test_dir=data_ingestion_test_dir,
                                                      ingested_train_dir=data_ingestion_train_dir)
            logging.info(f"data ingestion config : {data_ingestion_config}")
            return data_ingestion_config

        except Exception as e:
            raise HousingException(e,sys) from e
    

#    def get_data_validation_config(self):

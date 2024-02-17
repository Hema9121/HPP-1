from Housing.entity.config_entity import DataIngestionConfig
from Housing.entity.artifact_entity import DataIngestionArtifact
import os
import sys
from Housing.exception import HousingException
from Housing.logger import logging
from six.moves import urllib
import tarfile
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
import numpy as np



class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'**'*20}data ingestion log started{'**'*20}")
            self.data_ingestion_config=data_ingestion_config

        except Exception as e:
            raise HousingException(e,sys) from e
        
    def download_date(self)->str:
        try:

            dataset_download_url=self.data_ingestion_config.dataset_download_url

            tgz_download_dir=self.data_ingestion_config.tgz_download_dir
            os.makedirs(tgz_download_dir,exist_ok=True)

            housing_file_name=os.path.basename(dataset_download_url)

            tgz_file_path=os.path.join(tgz_download_dir,housing_file_name)

            logging.info(f"downloading the housing data from url {dataset_download_url} to the file path {tgz_file_path}")
            urllib.request.urlretrieve(dataset_download_url,tgz_file_path)
            logging.info(f"downloaded the Housing data to the path {tgz_file_path}")

            return tgz_file_path
        except Exception as e:
            raise HousingException(e,sys) from e
        
    
    def extract_tgz_file(self,tgz_file_path:str)->str:
        try:
            raw_data_dir=self.data_ingestion_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)
            logging.info(f"extracting the tgz file {tgz_file_path} to the dir {raw_data_dir}")
            with tarfile.open(tgz_file_path) as file:
                file.extractall(path=raw_data_dir)
            logging.info("extraction completed !")
            return raw_data_dir

        except Exception as e:
            raise HousingException(e,sys) from e
    
    def split_data_as_train_test(self)->DataIngestionArtifact:

        try:
            #ingested_dir=os.path.dirname(self.data_ingestion_config.ingested_test_dir)
            #os.makedirs(ingested_dir,exist_ok=True)
            raw_data_dir=self.data_ingestion_config.raw_data_dir
            file_name=os.listdir(raw_data_dir)[0]

            raw_housing_file_path=os.path.join(raw_data_dir,file_name)

            logging.info(f"Reading csv file: [{raw_housing_file_path}]")
            housing_data=pd.read_csv(raw_housing_file_path)
            housing_data["income_cat"] = pd.cut(
                housing_data["median_income"],
                bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1,2,3,4,5]
            )

            split=StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)

            logging.info(f"splitting the raw housing data {raw_housing_file_path} into train and test data")

            train_set=None
            test_set=None

            for train_index,test_index in split.split(housing_data,housing_data["income_cat"]):
                train_set=housing_data.loc[train_index].drop(["income_cat"],axis=1)
                test_set=housing_data.loc[test_index].drop(["income_cat"],axis=1)
            
            train_file_path=os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)
            test_file_path=os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)

            if train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"train dataset file : {train_file_path}")
                train_set.to_csv(train_file_path,index=False)

            if test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                logging.info(f"test dataset file : {test_file_path}")
                test_set.to_csv(test_file_path,index=False)
            
            data_ingestion_artifact=DataIngestionArtifact(is_ingested=True,message=f"data ingestion completed successfully",train_file_path=train_file_path,test_file_path=test_file_path)

            logging.info(f"data ingestion artifact : {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise HousingException(e,sys) from e
    
    def initiate_data_ingestion(self,)->DataIngestionArtifact:
        try:
            tgz_file_path=self.download_date()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()

        except Exception as e:
            raise HousingException(e,sys) from e


    def __del__(self):
        logging.info(f"{'**'*20} data ingestion log completed!{'**'*20}")




from Housing.exception import HousingException
from Housing.logger import logging

import os,sys

from Housing.constant import *
from Housing.entity.config_entity import DataValidationConfig
from Housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from Housing.config.configuration import Configuration

import pandas as pd
import json
#
from evidently.report import Report
from evidently.metrics import *
from evidently.metric_preset import DataDriftPreset

#
#from evidently.model_profile import Profile
#from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab



class DataValidation:

    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifact:DataIngestionArtifact)->None:
        try:
            logging.info(f"{'**'*20}data validation log started{'**'*20}")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact

        except Exception as e:
            raise HousingException(e,sys) from e

    def get_train_test_data(self):
        try:
            train_df=pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df=pd.read_csv(self.data_ingestion_artifact.test_file_path)

            return train_df,test_df

        except Exception as e:
            raise HousingException(e,sys) from e
    
    def is_train_test_available(self)->bool:
        try:
            logging.info(f"checking if the train and test data is available!")
            is_train_file_exist=False
            is_test_file_exists=False

            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            is_train_file_exist=os.path.exists(train_file_path)
            is_test_file_exists=os.path.exists(test_file_path)
            
            is_available=is_train_file_exist and is_test_file_exists

            logging.info(f"Is train and test file exists?-> {is_available}")
            if not is_available:
                logging.info(f"train file and test file is not present!")
                message=f"the train file {train_file_path} and test file {train_file_path} does not exist"
                raise Exception(message)
            
            return is_available

        except Exception as e:
            raise HousingException(e,sys) from e

    def validate_dataset_schema(self)->bool:
        try:
            validation_status=False
            
            #Assigment validate training and testing dataset using schema file
            #1. Number of Column
            #2. Check the value of ocean proximity 
            # acceptable values     <1H OCEAN
            # INLAND
            # ISLAND
            # NEAR BAY
            # NEAR OCEAN
            #3. Check column names

            validation_status=True

            return validation_status

        except Exception as e:
            raise HousingException(e,sys) from e

    def get_save_data_drift_report(self):
        try:
            train_df,test_df=self.get_train_test_data()
            report = Report(metrics=[DataDriftPreset(),])

            report.run(reference_data=train_df, current_data=test_df)
            report.as_dict()
            report=json.loads(report.json())

            """profile=Profile(sections=[DataDriftProfileSection()])
            train_df,test_df=self.get_train_test_data()
            profile.calculate(train_df,test_df)
            report=json.loads(profile.json())"""

            report_file_path=self.data_validation_config.report_file_path
            report_dir=os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,"w") as f:
                json.dump(report, f,indent=6)
            return report

        except Exception as e:
            raise HousingException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard=Dashboard(tabs=[DataDriftTab()])
            train_df,test_df=self.get_train_test_data()
            dashboard.calculate(train_df,test_df)

            report_page_file_path=self.data_validation_config.report_page_file_path
            report_page_dir=os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)

        except Exception as e:
            raise HousingException(e,sys) from e

    def is_data_drift_found(self)->bool:
        try:
            report=self.get_save_data_drift_report()
            self.save_data_drift_report_page()

            return True
        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            self.is_train_test_available()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact=DataValidationArtifact(is_validated=True,message=f"data validation performed successfully!",
                                                            schema_file_path=self.data_validation_config.schema_file_path,
                                                            report_file_path=self.data_validation_config.report_file_path,
                                                            report_page_file_path=self.data_validation_config.report_page_file_path)
            logging.info(f"data validation artifact : {data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise HousingException(e,sys) from e
    
    def __del__(self):
        logging.info(f"{'**'*20}data validation ended !{'**'*20}")

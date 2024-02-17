import os
from datetime import datetime


def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

CURRENT_TIME_STAMP=get_current_time_stamp()

ROOT_DIR=os.getcwd()
#print(root_dir)
CONFIG_DIR="config"
CONFIG_FILE_NAME="config.yaml"
CONFIG_FILE_PATH=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

#training pipeline config
TRAINING_PIPELINE_CONFIG_KEY="training_pipeline_config"
TRAINING_PIPELINE_NAME="pipeline_name"
TRAINING_PIPELINE_ARTIFACT_DIR_NAME="artifact_dir"

#data ingestion config
DATA_INGESTION_CONFIG_KEY="data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR_NAME="DATA INGESTION"
DATA_INGESTION_DOWNLOAD_URL_KEY="dataset_download_url"
DATA_INGESTION_RAW_DATA_DIR_KEY="raw_data_dir"
DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY="tgz_download_dir"
DATA_INGESTION_INGESTED_DIR_KEY="ingested_dir"
DATA_INGESTION_INGESTED_TRAIN_DIR_KEY="ingested_train_dir"
DATA_INGESTION_INGESTED_TEST_DIR_KEY="ingested_test_dir"

#data validation config
DATA_VALIDATION_CONFIG_KEY="data_validation_config"
DATA_VALIDATION_ARTIFACT_DIR="DATA VALIDATION"
DATA_VALIDATION_SCHEMA_DIR_KEY="schema_dir"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY="schema_file_name"
DATA_VALIDATION_REPORT_FILE_NAME_KEY="report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY="report_page_file_name"

#data transformation config
DATA_TRANSFORMATION_CONFIG_KEY="data_transformation_config"
DATA_TRANSFORMATION_ARTIFACT_DIR="DATA TRANSFORMATION"
DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY="transformed_dir"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY="transformed_train_dir"
DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY="transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY="preprocessing_dir"
DATA_TRANSFORMATION_PREPROCESSED_OBJ_FILE_NAME_KEY="preprocessed_object_file_name"
DATA_TRANSFORMATION_ADD_BEDROOM_PER_ROOM_KEY="add_bedroom_per_room"

NUMERICAL_COLUMNS_KEY="numerical_columns"
CATEGORICAL_COLUMNS_KEY="categorical_columns"
TARGET_COLUMN_KEY="target_columns"
DATASET_SCHEMA_COLUMNS_KEY=  "columns"

COLUMN_TOTAL_ROOMS_KEY = "total_rooms"
COLUMN_POPULATION_KEY = "population"
COLUMN_HOUSEHOLDS_KEY = "households"
COLUMN_TOTAL_BEDROOM_KEY = "total_bedrooms"
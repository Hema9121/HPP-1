from collections import namedtuple

#data ingestion config
DataIngestionConfig=namedtuple("DataIngestionConfig",["dataset_download_url","raw_data_dir","tgz_download_dir","ingested_train_dir","ingested_test_dir"])

#data validation config
DataValidationConfig=namedtuple("DataValidationConfig",["schema_file_path","report_file_path","report_page_file_path"])

#data transformation config
DataTransformationConfig=namedtuple("DataTransformationConfig",["add_bedroom_per_room","transformed_train_dir","transformed_test_dir","preprocessed_object_file_name"])

#



#training pipeline config
TrainingPipelineConfig=namedtuple("TrainingPipelineConfig",["artifact_dir"])



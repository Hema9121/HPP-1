from collections import namedtuple

#data ingestion config
DataIngestionConfig=namedtuple("DataIngestionConfig",["dataset_download_url","raw_data_dir","tgz_download_dir","ingested_train_dir","ingested_test_dir"])

#training pipeline config
TrainingPipelineConfig=namedtuple("TrainingPipelineConfig",["artifact_dir"])

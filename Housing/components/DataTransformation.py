import os,sys
from Housing.logger import logging
from Housing.exception import HousingException
from Housing.config.configuration import Configuration
from Housing.entity.artifact_entity import DataTransformationArtifact,DataIngestionArtifact,DataValidationArtifact
from Housing.entity.config_entity import DataTransformationConfig
from Housing.constant import *
from Housing.utils.util import load_data,read_yaml_file,save_numpy_array_data,save_object

from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
import numpy as np






class FeatureGenerator(BaseEstimator,TransformerMixin):
    def __init__(self,
              add_bedrooms_per_room=True,
              columns=None,
              total_rooms_ix=3,
              population_ix=5,
              households_ix=6,
              total_bedrooms_ix=4):
        try:
            self.columns=columns
            if self.columns is not None:
                total_rooms_ix = self.columns.index(COLUMN_TOTAL_ROOMS_KEY)
                population_ix = self.columns.index(COLUMN_POPULATION_KEY)
                households_ix = self.columns.index(COLUMN_HOUSEHOLDS_KEY)
                total_bedrooms_ix = self.columns.index(COLUMN_TOTAL_BEDROOM_KEY)
            self.add_bedrooms_per_room=add_bedrooms_per_room
            self.total_rooms_ix =total_rooms_ix
            self.population_ix=population_ix
            self.households_ix=households_ix
            self.total_bedrooms_ix=total_bedrooms_ix

        except Exception as e:
            raise HousingException(e,sys) from e
        
    def fit(self,X,y=None):
        return self
    
    def transform(self,X,y=None):
        try:
            room_per_household = X[:, self.total_rooms_ix] / \
                                 X[:, self.households_ix]
            population_per_household = X[:, self.population_ix] / \
                                       X[:, self.households_ix]
            if self.add_bedrooms_per_room:
                bedrooms_per_room = X[:, self.total_bedrooms_ix] / \
                                    X[:, self.total_rooms_ix]
                generated_feature = np.c_[
                    X, room_per_household, population_per_household, bedrooms_per_room]
            else:
                generated_feature = np.c_[
                    X, room_per_household, population_per_household]

            return generated_feature

        except Exception as e:
            raise HousingException(e,sys) from e




class DataTransformation:
    def __init__(self,
               data_transformation_config: DataTransformationConfig,
               data_ingestion_artifact: DataIngestionArtifact,
               data_validation_artifact: DataValidationArtifact):
        try:
            logging.info(f"{'**'*20}data transformation log started ! {'**'*20}")
            self.data_transformation_config=data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact

        except Exception as e:
            raise HousingException(e,sys) from e
        
    def get_data_transformer_obj(self)->ColumnTransformer:
        try:
            schema_file_path=self.data_validation_artifact.schema_file_path
            dataset_schema=read_yaml_file(file_path=schema_file_path)

            num_columns=dataset_schema[NUMERICAL_COLUMNS_KEY]
            cat_columns=dataset_schema[CATEGORICAL_COLUMNS_KEY]

            num_pipeline=Pipeline(steps=[("imputer",SimpleImputer(strategy='median')),
                                         ("feature_generator",FeatureGenerator(add_bedrooms_per_room=self.data_transformation_config.add_bedroom_per_room,
                                                                               columns=num_columns)),
                                        ("scaler",StandardScaler())
                                        ])
            
            cat_pipeline=Pipeline(steps=[("imputer",SimpleImputer(strategy='most_frequent')),
                                         ("encoder",OneHotEncoder()),
                                         ("scaler",StandardScaler(with_mean=False))
                                        ])
            
            preprocessing=ColumnTransformer([("num_pipelene",num_pipeline,num_columns),
                                             ("cat_pipeline",cat_pipeline,cat_columns),
                                            ])
            return preprocessing

        except Exception as e:
            raise HousingException(e,sys) from e

            

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info(f"{'**'*20}loading the train and test data set for transformation !{'**'*20}")
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            schema_file_path=self.data_validation_artifact.schema_file_path

            train_df=load_data(schema_file_path=schema_file_path,data_file_path=train_file_path)
            test_df=load_data(schema_file_path=schema_file_path,data_file_path=test_file_path)
            dataset_schema=read_yaml_file(file_path=schema_file_path)
            target_column=dataset_schema[TARGET_COLUMN_KEY]

            logging.info(f"loading the preprocessing objest ! ")
            preprocessing_obj=self.get_data_transformer_obj()
            
            logging.info(f"splitting the target column from the train and test data")
            input_train_df=train_df.drop(columns=target_column,axis=1)
            target_train_df=train_df[target_column]

            input_test_df=test_df.drop(columns=target_column,axis=1)
            target_test_df=test_df[target_column]

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
            input_train_arr=preprocessing_obj.fit_transform(input_train_df)
            input_test_arr=preprocessing_obj.transform(input_test_df)

            train_arr=np.c_[input_train_arr,np.array(target_train_df)]
            test_arr=np.c_[input_test_arr,np.array(target_test_df)]

            transformed_train_dir=self.data_transformation_config.transformed_train_dir
            transformed_test_dir=self.data_transformation_config.transformed_test_dir

            train_file_name=os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_name=os.path.basename(test_file_path).replace(".csv",".npz")

            transformed_train_file_path=os.path.join(transformed_train_dir,train_file_name)
            transformed_test_file_path=os.path.join(transformed_test_dir,test_file_name)

            logging.info(f"Saving transformed training and testing array.")
            save_numpy_array_data(array=train_arr,file_path=transformed_train_file_path)
            save_numpy_array_data(array=test_arr,file_path=transformed_test_file_path)

            preprocessed_obj_file_path=self.data_transformation_config.preprocessed_object_file_name
            save_object(file_path=preprocessed_obj_file_path,obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(is_transformed=True,
            message="Data transformation successfull.",
            transformed_train_file_path=transformed_train_file_path,
            transformed_test_file_path=transformed_test_file_path,
            preprocessed_obj_file_path=preprocessed_obj_file_path)

            logging.info(f"Data transformationa artifact: {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise HousingException(e,sys) from e


    def __del__(self):
        logging.info(f"{'**'*20}data transformation log completed ! {'**'*20}")



import yaml
from Housing.exception import HousingException
from Housing.constant import *
import sys,os
import numpy as np
import pandas as pd
import dill

def write_yaml_file(file_path:str,data:dict=None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise HousingException(e,sys) from e
    
def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise HousingException(e,sys) from e
    
def load_numpy_array_data(file_path:str):
    try:
        with open(file_path,"rb") as f:
            return np.load(f)
    except Exception as e:
        raise HousingException(e,sys) from e
    
def save_numpy_array_data(array:np.array,file_path:str):
    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path, 'wb') as f:
            return np.save(f,array)
    except Exception as e:
        raise HousingException(e,sys) from e
    
def load_data(schema_file_path:str,data_file_path:str,)->pd.DataFrame:
    try:
        data_schema=read_yaml_file(schema_file_path)
        data=pd.read_csv(data_file_path)
        schema=data_schema[DATASET_SCHEMA_COLUMNS_KEY]

        for column in data.columns:
            if column in list(schema.keys()):
                data[column].astype(schema[column])
            else:
                message=f"{column} not in schema."
                raise Exception(message)
        return data

    except Exception as e:
        raise HousingException(e,sys) from e
    
def save_object(file_path:str,obj):
    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,"wb") as f:
            return dill.dump(obj=obj,file=f)
        
    except Exception as e:
        raise HousingException(e,sys) from e
    
def load_object(file_path:str):
    try:
        with open(file_path,"rb") as f:
            return dill.load(f)
    except Exception as e:
        raise HousingException(e,sys) from e
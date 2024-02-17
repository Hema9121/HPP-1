import yaml
from Housing.exception import HousingException
import sys


def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise HousingException(e,sys) from e
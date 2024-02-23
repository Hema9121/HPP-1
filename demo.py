from Housing.pipeline.pipeline import Pipeline
from Housing.exception import HousingException
from Housing.logger import logging
import sys,os
from Housing.config.configuration import Configuration



def main():
    try:
        config_path = os.path.join("config","config.yaml")
        logging.info("testing")
        pipeline=Pipeline(Configuration(config_file_path=config_path))
        pipeline.start()
        logging.info("testing completed")
    except Exception as e:
        raise HousingException(e,sys) from e
    
if __name__=="__main__":
    main()
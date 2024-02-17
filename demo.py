from Housing.pipeline.pipeline import Pipeline
from Housing.exception import HousingException
from Housing.logger import logging
import sys

def main():
    try:
        logging.info("testing data ingestion")
        pipeline=Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        raise HousingException(e,sys) from e
    
if __name__=="__main__":
    main()
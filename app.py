from flask import Flask
from Housing.logger import logging
from Housing.exception import HousingException
import sys

app=Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
#    try:
#        raise Exception("testing the exception!")
#    except Exception as e:
#        housing=HousingException(e,sys)
#       logging.info(housing.error_message)
#        logging.info("we are testing logging module!!!!")
    return "hello world!!!!"

if __name__=="__main__":
    app.run(debug=True)
from flask import Flask
from Housing.logger import logging


app=Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    logging.info("we are testing logging module!!!!")
    return "hello world!!!!"

if __name__=="__main__":
    app.run(debug=True)
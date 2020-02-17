import os
import requests, json
from flask import Flask
from flask import request
from flask import make_response
import pandas as pd
import numpy as np
import csv
# flask app should start in global layout
# enter your api key here
app = Flask(__name__)
def query(query1):
    api_key = 'AIzaSyAxE1mDEd-cebw9260kMrGPzqaC-cxCUAw'
# url variable store url
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
# The text string on which to search
    query = query1
# get method of requests module
# return response object
    r = requests.get(url + 'query=' + query +'&key=' + api_key)
# json method of response object convert
#  json format data into python format data
    x = r.json()
# now x contains list of nested dictionaries
# we know dictionary contain key value pair
# store the value of result key in variable y
    y = x['results']
    loc=[]
# keep looping upto lenght of y
    for i in range(len(y)):
    # Print value corresponding to the
    # 'name' key at the ith index of y
        print(y[i]['name'])
        loc.append(y[i]['name'])
    return loc

#dialogflow connection
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#colleges in Thane/Palghar
def makeWebhookResult(req):
    if req.get("queryResult").get("action") != "location":
        return{}
    result = req.get("queryResult")
    #data =json.loads(result)
    parameters = result.get("parameters")
    query1=result.get("queryText")
    locations = parameters.get("locations")
    co=query(query1)
    speech = "heres the result from maps " + str(co)
    print("response:")
    print(speech)
    return {
        #"speech": speech,
        #"text":speech,
        #"fulfillmentMessages":speech,
        "fulfillmentText":speech,
        #"displayText": speech,
        "source": "Student_Counsellor"
    }
if __name__ == '__main__':
    port = int(os.getenv('PORT',80))
    print("starting app on port %d" %(port))
    app.run(debug=True, port=port, host='0.0.0.0')
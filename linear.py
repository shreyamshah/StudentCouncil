import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
import json
import os
from flask import Flask
from flask import request
from flask import make_response
import csv
# flask app should start in global layout
app = Flask(__name__)
#%matplotlib inline
# Function to get data
def get_data(file_name,caste1):
    data = pd.read_csv('linear1.csv')
    x_parameter = []
    y_parameter = []
    cutoff=caste1
    print(cutoff)
    for year ,general, sc,st,obc in zip(data['year'],data['general'],data['sc'],data['st'],data['obc']):
        x_parameter.append([float(year)])
        if cutoff=="['general']":
            y_parameter.append([float(general)])
        elif cutoff == "['obc']":
                y_parameter.append([float(obc)])
        elif cutoff == "['sc']":
                y_parameter.append([float(sc)])
        elif cutoff == "['st']":
                y_parameter.append([float(st)])
    return x_parameter, y_parameter
#x,y = get_data('linear.csv')
#print (x)
#print (y)
# Function for Fitting data to Linear model
def linear_model_main(X_parameters,Y_parameters,predict_value):

    # Create linear regression object
    regr = linear_model.LinearRegression()
    regr.fit(X_parameters, Y_parameters)
    predict_outcome = regr.predict(predict_value)
    predictions = {}
    predictions['intercept'] = regr.intercept_
    predictions['coefficient'] = regr.coef_
    predictions['predicted_value'] = predict_outcome
    return predictions
#x,y = get_data('linear.csv')
def linear(caste,year):
    predict_value = [[float(year)]]
    caste1=str(caste)
    x,y=get_data('linear1.csv',caste1)
    print(x)
    print(y)
    result = linear_model_main(x,y,predict_value)
    print ("Intercept value " , result['intercept'])
    print ("coefficient" , result['coefficient'])
    print ("Predicted value: ",result['predicted_value'])
    return result['predicted_value']
'''caste=input("enter caste")
year=input("enter year")
li=linear(caste,year)
print(li)'''

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


def makeWebhookResult(req):
    if req.get("queryResult").get("action") != "cast":
        return{}
    result = req.get("queryResult")
    #data =json.loads(result)
    parameters = result.get("parameters")
    caste = parameters.get("caste")
    print(caste)
    year= parameters.get("year")
    co=linear(caste,year)
    speech = "The cutoff for "+str(caste)+ "is" + str(co)
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

#what will be the cutoff
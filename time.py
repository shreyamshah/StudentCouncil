import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
import json
import os
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from flask import Flask
from flask import request
from flask import make_response
import csv
# flask app should start in global layout
app = Flask(__name__)






def classify(s1,m1,s2,m2):
    data = pd.read_csv('appti.csv')
    X = data[['s1', 'm1', 's2', 'm2']]
    y = data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    exp = [[s1,m1,s2,m2]]
    dept_idx = clf.predict(exp)[0]
    exp1 = data.dept[dept_idx]
    return exp1


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
    s1 = parameters.get("s1")
    print(s1)
    m1 = parameters.get("m1")
    print(m1)
    s2 = parameters.get("s2")
    print(s1)
    m2 = parameters.get("m2")
    print(m2)
    co=classify(s1,m1,s2,m2)
    speech = "The department is " + str(co)
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
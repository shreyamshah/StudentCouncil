import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
import matplotlib.pyplot as plt
import json
import os
from flask import Flask
from flask import request
from flask import make_response
import csv
# flask app should start in global layout
app = Flask(__name__)
#%matplotlib inline
def random(cutoff1,cutoff2, stream):
    train=pd.read_csv('collegelist1.csv')
    cutoff1=int(cutoff1)
    cutoff2 = int(cutoff2)
    #if cutoff1<cutoff2:
        #temp=cutoff1
        #cutoff1=cutoff2
        #cutoff2=temp
    if stream == "computer" or "computer engineering" or "computer science" or "computer science and engineering":
        st=0
    elif stream =="electronics" or "electronics engineering":
        st=1
    elif stream == "extc" or "electrical and telecommunications":
        st=2
    elif stream == 'civil' or 'civil engineering':
        st=3
    elif stream == "mechanical" or "mechanical engineering":
        st=3
    print(st)
    with open('random.csv','w',newline='') as f:
        thewriter = csv.writer(f)
        thewriter.writerow(['Sr.No.','cutoff','Merit' ,'choice_code','Institute','stream','Exam (JEE/MHT- CET)','Type','Seat Type'])
        while cutoff1<=cutoff2:
            thewriter.writerow(['',str(cutoff1),'','','',str(st),'','',''])
            cutoff1=cutoff1+1
    train.head()
    factor=pd.factorize(train['stream'])
    train.stream =factor[0]
    definitions=factor[1]
    print(train.stream.head())
    print(definitions)
    test=pd.read_csv('random.csv')
#   def data_cleaning (train):
#     train["cutoff"]=train["cutoff"].fillna(train["cutoff"].median())
#     train["stream"]=train["stream"].fillna(train["stream"].median())
#
#     train.loc[train["stream"]=="Computer","stream"]=0
#     train.loc[train["stream"]=="Electronics","stream"]=1
#     train.loc[train["stream"]=="EXTC","stream"]==2
#     train.loc[train["stream"]=="Civil","stream"]=3
#     train.loc[train["stream"]=="Mechanical","stream"]=4
#     return train
# train=data_cleaning(train)
    predictor_vars=["stream","cutoff"]
    x,y=train[predictor_vars],train.Institute
    modelRandom = RandomForestClassifier(n_estimators=100,max_depth=30,random_state=2)
    modelRandomCV = cross_validate(modelRandom,x,y,cv=5)
    print(modelRandomCV)
    #plt.plot(modelRandomCV,"p")
    #print(mean(modelRandomCV))
    modelRandom.fit(x,y)
    predictions1 = modelRandom.predict(test[predictor_vars])
    print(predictions1)
#    with open('random.csv', 'rb') as inp, open('random.csv', 'wb') as out:
#        writer = csv.writer(out)
#        for row in csv.reader(inp):
#            if row[2] != "0":
#                writer.writerow(row)
    return predictions1


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
    if req.get("queryResult").get("action") != "random":
        return{}
    result = req.get("queryResult")
    #data =json.loads(result)
    parameters = result.get("parameters")
    cutoff1 = parameters.get("cutoff1")
    cutoff2= parameters.get("cutoff2")
    stream = parameters.get("stream")
    co=random(cutoff1,cutoff2,stream)
    speech = "heres the result " + str(co)
    print("response:")
    print(speech)
    tp = open("percentage.txt", "r+")
    tp.truncate(0)
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

#to invoke the app talk to my test app```
#what is the cutoff for sc for 2019```
#70 to 80 computer engineering college or can be used in different ways as well```
#for maps "colleges in Mumbai City"


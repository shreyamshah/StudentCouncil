import numpy as np
import pandas as pd
df = pd.read_csv("collegelist1.csv")
print(df.head())
for col in df.columns :
   df[col] = pd.get_dummies(df[col])
print(df.head())
#X and Y
X = df.ix[:,df.columns !='cutoff']
y = df.ix[:,df.columns == 'Institute']
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3, random_state=30)
from sklearn.ensemble import RandomForestClassifier
rclf = RandomForestClassifier()
rclf.fit(X_train,y_train)
from sklearn.metrics import accuracy_score,recall_score,confusion_matrix
y_pred = rclf.predict(X_test)
print(len(X_test))
print("accuracy is:")
print(accuracy_score(y_test,y_pred))
print(recall_score(y_test,y_pred))
print(confusion_matrix(y_test,y_pred))


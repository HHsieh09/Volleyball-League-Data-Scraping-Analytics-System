import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
#from sklearn.model_selection import train_test_split
from sklearn.model_selection import LeaveOneOut, cross_val_score
from sklearn.metrics import classification_report

train_data = pd.read_csv("ETL_files/ML_Training_Data.csv")

libero_data = train_data[train_data["eng_position"]=="Libero"]

libero_men = libero_data[libero_data["DIVISION"]=="Mens Division"]
print(libero_men)

libero_men = libero_men[["receive_percentage","dig_percentage","set_percentage","national_team"]].fillna(0)

X = libero_men[["receive_percentage","dig_percentage","set_percentage"]]
y = libero_men["national_team"]

#X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

libero_model = RandomForestClassifier(random_state=42)
#libero_model.fit(X_train, y_train)

loocv = LeaveOneOut()
scores = cross_val_score(libero_model, X, y, cv=loocv, scoring="accuracy")

#print("Libero Model Analysis:", classification_report(y_test, libero_model.predict(X_test)))
print("LOOCV 每輪準確率:", scores)
print("LOOCV 平均準確率: {:.2f}".format(np.mean(scores)))

libero_model.fit(X,y)

joblib.dump(libero_model, "ml/libero_model_men.pkl")
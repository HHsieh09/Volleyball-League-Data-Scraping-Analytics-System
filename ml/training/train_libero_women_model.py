import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

train_data = pd.read_csv("ETL_files/ML_Training_Data.csv")

libero_data = train_data[train_data["eng_position"]=="Libero"]
print(libero_data)

libero_women = libero_data[libero_data["DIVISION"]=="Womens Division"]
print(libero_women)

libero_women = libero_women[["receive_percentage","dig_percentage","set_percentage","national_team"]].fillna(0)

X = libero_women[["receive_percentage","dig_percentage","set_percentage"]]
y = libero_women[["national_team"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

libero_model = RandomForestClassifier()
libero_model.fit(X_train, y_train)

print("Libero Model Analysis:", classification_report(y_test, libero_model.predict(X_test)))

joblib.dump(libero_model, "ml/libero_model_women.pkl")
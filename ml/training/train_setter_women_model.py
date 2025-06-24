import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

train_data = pd.read_csv("ETL_files/ML_Player_National.csv")

setter_data = train_data[train_data["eng_position"]=="Setter"]
print(setter_data)

setter_women = setter_data[setter_data["DIVISION"]=="Womens Division"]
print(setter_women)

setter_women = setter_women[["set_percentage","dig_percentage","receive_percentage","total_point_score","national_team"]].fillna(0)

X = setter_women[["set_percentage","dig_percentage","receive_percentage","total_point_score"]]
y = setter_women[["national_team"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

setter_model = RandomForestClassifier()
setter_model.fit(X_train, y_train)

print("Libero Model Analysis:", classification_report(y_test, setter_model.predict(X_test)))

joblib.dump(setter_model, "ml/setter_model_men.pkl")
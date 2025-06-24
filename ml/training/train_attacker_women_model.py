import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
import matplotlib.pyplot as plt


train_data = pd.read_csv("ETL_files/ML_Training_Data.csv")

attacker_data = train_data[~train_data["eng_position"].isin(["Libero","Setter"])]
print(attacker_data)

attacker_women = attacker_data[attacker_data["DIVISION"]=="Womens Division"]
print(attacker_women)

attacker_women = attacker_women[["attack_percentage", "block_total", "serve_percentage", "total_point_score","receive_percentage","dig_percentage","set_percentage","national_team"]].fillna(0)

X = attacker_women[["attack_percentage", "block_total", "serve_percentage", "total_point_score","receive_percentage","dig_percentage","set_percentage"]]
y = attacker_women["national_team"]

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

attacker_model = RandomForestClassifier()
attacker_model.fit(X_train.values, y_train.values)

print("Attacker Model Analysis:", classification_report(y_test.values, attacker_model.predict(X_test.values)))

ConfusionMatrixDisplay.from_estimator(attacker_model, X_test.values, y_test.values)
plt.title("Confusion Matrix - Attacker (Women)")
plt.show()

indicators_importance = attacker_model.feature_importances_
feature_names = X.columns
importance_df = pd.DataFrame({"Feature": feature_names, "Importance": indicators_importance})
print(importance_df.sort_values("Importance", ascending=False))

joblib.dump(attacker_model, "ml/attacker_model_women.pkl")
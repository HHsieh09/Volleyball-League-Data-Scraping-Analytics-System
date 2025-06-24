import joblib
import pandas as pd

attacker_model_men = joblib.load("ml/model/attacker_model_men.pkl")
attacker_model_women = joblib.load("ml/model/attacker_model_women.pkl")

candidates = pd.read_csv("ETL_files/ML_Player_Candidates.csv")
print(candidates.head())

attacker_candidates = candidates[~candidates["eng_position"].isin(["Setter","Libero"])].fillna(0)
attacker_candidates = attacker_candidates[~attacker_candidates["name"].str.fullmatch(r"[A-Za-z\s\.\-']+")]
print(attacker_candidates.head())

indicators = ["attack_percentage", "block_total", "serve_percentage", "total_point_score","receive_percentage","dig_percentage","set_percentage"]

men_results = []
women_results = []

for _, row in attacker_candidates.iterrows():
    name = row["name"]
    division = row["DIVISION"]
    position = row["eng_position"]

    try:
        if division == "Mens Division":
            X = row[indicators].values.reshape(1,-1)
            probability = attacker_model_men.predict_proba(X)[0][1]
            men_results.append({"name":name, "division":division, "position":position, "probability":probability})
        else:
            X = row[indicators].values.reshape(1,-1)
            probability = attacker_model_women.predict_proba(X)[0][1]
            women_results.append({"name":name, "division":division, "position":position, "probability":probability})
    except Exception as e:
        print(f"{name}: causing errors - {e}")

men_top10 = pd.DataFrame(men_results).sort_values(by="probability", ascending=False).head(10)
women_top10 = pd.DataFrame(women_results).sort_values(by="probability", ascending=False).head(10)

men_top10.to_csv("ml/recommendation_result/top10_potential_nat_attacker_men.csv")
women_top10.to_csv("ml/recommendation_result/top10_potential_nat_attacker_women.csv")
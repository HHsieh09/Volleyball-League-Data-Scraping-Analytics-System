from volleyballdata.database.clients import get_mysql_volleyballdata_conn
from sqlalchemy import MetaData
from fastapi import FastAPI
import pandas as pd
import joblib
import numpy as np

app = FastAPI()

@app.get("/")
def read_root():
    return {"Welcome":"to this project"}

@app.get("/matches")
def get_matches(match_cup_id: str):
    sql = f"""SELECT * FROM Matches WHERE match_cup_id = '{match_cup_id}'"""
    conn = get_mysql_volleyballdata_conn()
    df = pd.read_sql(sql, con=conn.connection)
    return {"data": df.to_dict("records")}

@app.get("/match_score")
def get_match_score(
    match_cup_id: str = "",
):
    sql = f"""SELECT * FROM Match_Score
                WHERE match_cup_id = '{match_cup_id}'"""
    conn = get_mysql_volleyballdata_conn()
    data_df = pd.read_sql(sql,con=conn.connection)
    data_dict = data_df.to_dict("records")
    return{"data": data_dict}

@app.get("/referee")
def get_referee(match_cup_id: str):
    sql = f"""SELECT * FROM Match_Referee WHERE match_cup_id = '{match_cup_id}'"""
    conn = get_mysql_volleyballdata_conn()
    df = pd.read_sql(sql, con=conn.connection)
    return {"data": df.to_dict("records")}

@app.get("/coach")
def get_coach(match_cup_id: str):
    sql = f"""SELECT * FROM Match_Coach WHERE match_cup_id = '{match_cup_id}'"""
    conn = get_mysql_volleyballdata_conn()
    df = pd.read_sql(sql, con=conn.connection)
    return {"data": df.to_dict("records")}

@app.get("/player_stats")
def get_player_stats(match_cup_id: str):
    sql = f"""SELECT * FROM Player_Stats WHERE match_cup_id = '{match_cup_id}'"""
    conn = get_mysql_volleyballdata_conn()
    df = pd.read_sql(sql, con=conn.connection)
    return {"data": df.to_dict("records")}


attacker_model_men = joblib.load("ml/model/attacker_model_men.pkl")
attacker_model_women = joblib.load("ml/model/attacker_model_women.pkl")

@app.get("/predict_male_player")
def predict_male_player(
    name: str,
    attack_percentage: float,
    block_total: float,
    serve_percentage: float,
    total_point_score: float,
    receive_percentage: float,
    dig_percentage: float,
    set_percentage: float,
):
    indicators = np.array([[attack_percentage, block_total, serve_percentage,
                          total_point_score, receive_percentage, dig_percentage,
                          set_percentage]])
    prediction = attacker_model_men.predict(indicators)[0]
    return {"name": name, "predicted_label": prediction}

@app.get("/predict_female_player")
def predict_female_player(
    name: str,
    attack_percentage: float,
    block_total: float,
    serve_percentage: float,
    total_point_score: float,
    receive_percentage: float,
    dig_percentage: float,
    set_percentage: float,
):
    indicators = np.array([[attack_percentage, block_total, serve_percentage,
                          total_point_score, receive_percentage, dig_percentage,
                          set_percentage]])
    prediction = attacker_model_men.predict(indicators)[0]
    return {"name": name, "predicted_label": prediction}
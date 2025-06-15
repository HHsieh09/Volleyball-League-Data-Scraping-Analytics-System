from volleyballdata.database.clients import get_mysql_volleyballdata_conn
from sqlalchemy import MetaData
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello":"World"}

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
from volleyballdata.database.clients import get_mysql_volleyballdata_conn
from sqlalchemy import MetaData
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.get("/volleyball_data")
def volleyball_data(
    match_cup_id: str = "",
):
    sql = f"""SELECT * FROM Match_Score
                WHERE match_cup_id = '{match_cup_id}'"""
    conn = get_mysql_volleyballdata_conn()
    data_df = pd.read_sql(sql,con=conn.connection)
    data_dict = data_df.to_dict("records")
    return{"data": data_dict}

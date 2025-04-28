import pandas as pd
from datetime import datetime, time
from pydantic import BaseModel, validator

########### Define class for further data type verification ###########

class Match(BaseModel):
    group: str
    week: int
    arena: str
    index: str
    date: datetime
    time: time
    duration: time
    match_type: str

    """Convert to correct data type"""
    @validator("date", pre=True)
    def convert_date(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y/%m/%d") 
        return value

    @validator("time", "duration", pre=True)
    def convert_time(cls, value):
        if isinstance(value, str):
            return time.fromisoformat(value) 
        return value

class Match_Score(BaseModel):
    team: str
    set1: int
    set2: int
    set3: int
    set4: int
    set5: int

    @validator("set1","set2","set3","set4","set5", pre=True)
    def convert_set(cls, value):
        if isinstance(value, str):
            return int(value)
        return value

class Referee(BaseModel):
    first_referee: str
    second_referee: str

class Coach(BaseModel):
    team: str
    head_coach: str
    assistant_coach1: str
    assistant_coach2: str

class Player(BaseModel):
    team: str
    number: int
    name: str
    position: str
    attack_point: int
    attack_total:int
    block_point: int
    serve_point: int
    serve_total: int
    receive_nice: int
    receive_total: int
    dig_nice: int
    dig_total: int
    set_nice: int
    set_total: int
    total_points: int

    @validator("number","attack_point","attack_total","block_point","serve_point","serve_total",
               "receive_nice","receive_total","dig_nice","dig_total","set_nice","set_total","total_points")
    def convert_stats(cls,value):
        if value in (None, "", " "):
            return 0
        if isinstance(value,str):
            return int(value)
        return value


#######################################################################

    

################ Define functions for validation ################

"""Check the match information"""
def check_match_schema(df: pd.DataFrame,) -> pd.DataFrame:
    df_dict = df.to_dict("records")
    #for dd in df_dict:
    #    dd['date'] = datetime.strptime(dd['date','%Y/%m/%d'])
    df_schema = [ Match(**dd).__dict__ for dd in df_dict]
    df = pd.DataFrame(df_schema)
    return df

"""Check the match score information"""
def check_match_score_schema(df: pd.DataFrame,) -> pd.DataFrame:
    df_dict = df.to_dict("records")
    df_schema = [ Match_Score(**dd).__dict__ for dd in df_dict]
    df = pd.DataFrame(df_schema)
    return df

"""Check the referee information"""
def check_referee_schema(df: pd.DataFrame,) -> pd.DataFrame:
    df_dict = df.to_dict("records")
    df_schema = [ Referee(**dd).__dict__ for dd in df_dict]
    df = pd.DataFrame(df_schema)
    return df

"""Check the coach information"""
def check_coach_schema(df: pd.DataFrame,) -> pd.DataFrame:
    df_dict = df.to_dict("records")
    df_schema = [ Coach(**dd).__dict__ for dd in df_dict]
    df = pd.DataFrame(df_schema)
    return df

"""Check the player information"""
def check_player_schema(df: pd.DataFrame,) -> pd.DataFrame:
    df_dict = df.to_dict("records")
    df_schema = [ Player(**dd).__dict__ for dd in df_dict]
    df = pd.DataFrame(df_schema)
    return df

#################################################################
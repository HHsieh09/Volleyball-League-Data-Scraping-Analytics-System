import re
import sys

import requests
import pandas as pd
from sqlalchemy import text
from bs4 import BeautifulSoup
from datetime import datetime, time
from volleyballdata.router import Router
from pydantic import BaseModel, validator
from urllib.parse import urlparse, parse_qs

################ Define functions for crawlers ################

def get_cupid(url):
    parse_url = urlparse(url)

    #Get the elements after ? in URL
    urlelement = parse_qs(parse_url.query)

    #Get the cupid from the URL
    cupid = urlelement.get('CupID')

    if cupid:
        return int(cupid[0])
    else:
        ("N/A")    

###############################################################

################ Define functions for crawlers ################

"""Parameter of request header to mimic the browser sending request"""
def tvl_header():
    return {
        "Accept": "/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,zh-TW;q=0.9,zh;q=0.8",
        "Connection": "keep-alive",
        "Host": "114.35.229.141",
        "Refer": "http://114.35.229.141/Match.aspx?CupID=20",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

"""Gather match information"""
def scrape_match(url: str,) -> pd.DataFrame:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    match_info = soup.find('h3').get_text(strip=True)

    """Group the capturing information into groups"""
    match_org = re.search(r'(.*?) 第(\d+)週\((.*?)\)\s+編號：(\d+)\s+\((\d+)月(\d+)日\s+(\d+:\d+)\)\s+歷時\s+(\d+:\d+)', match_info)

    if match_org:
        group = match_org.group(1).strip()
        week = match_org.group(2).strip()
        arena = match_org.group(3).strip()
        index = match_org.group(4).strip()
        month = match_org.group(5).zfill(2)
        day = match_org.group(6).zfill(2)
        month_int = int(month)
        year = 2024 if month_int >= 10 else 2025
        date = f"{year}/{month}/{day}"
        time = match_org.group(7).strip()
        duration = match_org.group(8).strip()

        match_dict = {
            "group": group,
            "week": week,
            "arena": arena,
            "index": index,
            "date": date,
            "time": time,
            "duration": duration,
        }

        match_df = pd.DataFrame([match_dict])

        print(match_df)
        return match_df

"""Gather match score information"""
def scrape_match_score(url: str,) -> pd.DataFrame:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    match_table = soup.find('div',class_="MatchResult").find('table')
    match_rows = match_table.find_all('tr')

    match_score_info = []
    for row in match_rows:
        col = row.find_all('td')
        if col:
            """Get the team name"""
            team_name_dirty = col[0].find_all('a')[-1]
            team_name = team_name_dirty.get_text(strip=True)

            """Get match socres data"""
            set_scores = [coll.get_text(strip=True) for coll in col[1:6]]

            match_score_info.append({
                "team": team_name,
                "set1":set_scores[0],
                "set2":set_scores[1],
                "set3":set_scores[2],
                "set4":set_scores[3],
                "set5":set_scores[4],
            })

    match_score_df = pd.DataFrame(match_score_info)
    
    return match_score_df

"""Gather referee score information"""
def scrape_ref(url: str,):
    response = requests.get(url)
    #Since the website wrongly programmed HTML, which has a </td> before </th>, thus using lxml
    soup = BeautifulSoup(response.text, 'lxml')

    ref_table = soup.find('th',string="第一裁判").find_parent('table')
    ref_rows = ref_table.find_all('tr')

    #Get referee data
    ref_data = {}
    for row in ref_rows:
        ref_type = row.find('th').get_text(strip=True)
        #Since the website wrongly programmed HTML, which has a </td> before </th>, thus using the following code to correctly extract the data
        td = row.find_all('td')
        if td:
            ref_name = td[0].get_text(strip=True)  # First <td> should contain name
        else:
            ref_name = "N/A"  # If no <td> found, fallback to "N/A"

        ref_data[ref_type] = ref_name


    ref_df = pd.DataFrame([ref_data])
    ref_df_rename = ref_df.rename(columns={"第一裁判":"first_referee","第二裁判":"second_referee"})

    return ref_df_rename

"""Gather coach information"""
def scrape_coach(url: str,) -> pd.DataFrame:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all('h3')
    data_eliminate_first = data[-2:]
    coach_data = []
    for row in data_eliminate_first:
        raw_coach = row.get_text(strip=True)

        team, coaches = raw_coach.split('：')
        coach = coaches.split('、')

        coach_data.append({
            "team": team,
            "head_coach":coach[0],
            "assistant_coach1":coach[1],
            "assistant_coach2":coach[2],
        })

    coach_df = pd.DataFrame(coach_data)

    return coach_df

"""Gather player information"""
def scrape_player(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    team_headers = soup.find_all('h3')[-2:]
    team_name = [team.text.split('：')[0].strip() for team in team_headers]

    team_table = soup.find_all('div',{'class':'TableFormat_1'})
    eliminate_first_two = team_table[-2:]

    player_data = []

    """To get the team of the players and their stats in each game"""
    for team, fake_table in zip(team_name, eliminate_first_two):
        tables = fake_table.find_all('table')

        for table in tables:
            player_rows = table.find_all('tr')[2:-1]
            for player in player_rows:
                data = player.find_all('td')

                player_stat = {
                    "team": team,
                    "number": data[0].string.strip(),
                    "name": data[1].string.strip(),
                    "position": data[2].string.strip(),
                    "attack_point": data[3].string.strip(),
                    "attack_total": data[4].string.strip(),
                    "block_point": data[5].string.strip(),
                    "serve_point": data[6].string.strip(),
                    "serve_total": data[7].string.strip(),
                    "receive_nice": data[8].string.strip(),
                    "receive_total": data[9].string.strip(),
                    "dig_nice": data[10].string.strip(),
                    "dig_total": data[11].string.strip(),
                    "set_nice": data[12].string.strip(),
                    "set_total": data[13].string.strip(),
                    "total_points": data[14].string.strip(),
                }

                player_data.append(player_stat)

    player_df = pd.DataFrame(player_data)

    return player_df
###############################################################

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

################ Define functions for inserting data into database ################

router = Router()

"""Insert match data into mysql"""
def insert_match(match_df, cup):
    db_conn = router.mysql_volleyball_conn

    query = text("""
    INSERT IGNORE INTO Matches (match_cup_id, match_id, tournament_id, match_date, match_time, arena, duration)
    VALUES (:match_cup_id, :match_id, :tournament_id, :match_date, :match_time, :arena, :duration)
    """)

    row = match_df.iloc[0]

    paras = {
    "match_cup_id": f"{row['index']}_{cup}",
    "match_id": row["index"],
    "tournament_id": cup,
    "match_date": row["date"],
    "match_time": row["time"],
    "arena": row["arena"],
    "duration": row["duration"],
    }

    db_conn.execute(query, paras)

    db_conn.commit()
    db_conn.close()

"""Insert match score data into mysql"""
def insert_match_score(match_score_df, match_cup_id):
    db_conn = router.mysql_volleyball_conn

    query = text("""
    INSERT IGNORE INTO Match_Score (match_cup_id, match_team, set1, set2, set3, set4, set5)
    VALUES (:match_cup_id, :match_team, :set1, :set2, :set3, :set4, :set5)
    """)

    for row in match_score_df.to_dict(orient='records'):
        paras = {
        "match_cup_id": match_cup_id,
        "match_team": row['team'],
        "set1": row["set1"],
        "set2": row["set2"],
        "set3": row["set3"],
        "set4": row["set4"],
        "set5": row["set5"]
        }
        db_conn.execute(query, (paras))


    db_conn.commit()
    db_conn.close()

def insert_referee(ref_df, match_cup_id):
    db_conn = router.mysql_volleyball_conn

    query = text("""
    INSERT IGNORE INTO Match_Referee (match_cup_id, first_referee, second_referee)
    VALUES (:match_cup_id, :first_referee, :second_referee)
    """)

    for row in ref_df.to_dict(orient="records"): 
        paras = {
        "match_cup_id": match_cup_id,
        "first_referee": row['first_referee'],
        "second_referee": row['second_referee'],
        }
        # Insert match-referee relationship
        db_conn.execute(query, paras)

    db_conn.commit()
    db_conn.close()

def insert_coach(coach_df, match_cup_id):
    db_conn = router.mysql_volleyball_conn

    query = text("""
    INSERT IGNORE INTO Match_Coach (match_cup_id, team, head_coach, assistant_coach1, assistant_coach2)
    VALUES (:match_cup_id, :team, :head_coach, :assistant_coach1, :assistant_coach2)
    """)

    for row in coach_df.to_dict(orient="records"):
        paras = {
        "match_cup_id": match_cup_id,
        "team": row["team"],
        "head_coach": row["head_coach"],
        "assistant_coach1": row["assistant_coach1"],
        "assistant_coach2": row["assistant_coach2"],
        }
        db_conn.execute(query, paras)

    db_conn.commit()
    db_conn.close()

"""
def insert_player(player_df):
    db_conn = router.mysql_volleyball_conn

    query = "    INSERT INTO Player (player_name, player_number, position)    VALUES (%s, %s, %s)    "

    for row in player_df.to_dict(orient="records"):
        db_conn.execute(query, (row["name"], row["number"], row["position"]))

    db_conn.commit()
    db_conn.close()
"""

def insert_player_stats(player_df, match_cup_id):
    db_conn = router.mysql_volleyball_conn

    query = text("""
    INSERT IGNORE INTO Player_Stats (match_cup_id, team, number, name, position, attack_point, attack_total, block_point, serve_point, serve_total, receive_nice, receive_total, dig_nice, dig_total, set_nice, set_total, total_points)
    VALUES (:match_cup_id, :team, :number, :name, :position, :attack_point, :attack_total, :block_point, :serve_point, :serve_total, :receive_nice, :receive_total, :dig_nice, :dig_total, :set_nice, :set_total, :total_points)
    """)

    for row in player_df.to_dict(orient="records"):
        paras = {
        "match_cup_id": match_cup_id,
        "team": row["team"],
        "number": row["number"],
        "name": row["name"],
        "position": row["position"],
        "attack_point": row["attack_point"],
        "attack_total": row["attack_total"],
        "block_point": row["block_point"],
        "serve_point": row["serve_point"],
        "serve_total": row["serve_total"],
        "receive_nice": row["receive_nice"],
        "receive_total": row["receive_total"],
        "dig_nice": row["dig_nice"],
        "dig_total": row["dig_total"],
        "set_nice": row["set_nice"],
        "set_total": row["set_total"],
        "total_points": row["total_points"],
        }
        db_conn.execute(query,paras)

    db_conn.commit()
    db_conn.close()

###################################################################################

################ Define functions to start the program ################

def start(url):
    cup = get_cupid(url)

    match_df = scrape_match(url)
    match_df = check_match_schema(match_df.copy())
    insert_match(match_df,cup)

    match_score_df = scrape_match_score(url)
    match_score_df = check_match_score_schema(match_score_df.copy())
    match_cup_id = str(match_df.iloc[0]["index"]) + "_" + str(cup)
    insert_match_score(match_score_df,match_cup_id)

    ref_df = scrape_ref(url)
    ref_df = check_referee_schema(ref_df)
    insert_referee(ref_df,match_cup_id)

    coach_df = scrape_coach(url)
    coach_df = check_coach_schema(coach_df.copy())
    insert_coach(coach_df,match_cup_id)

    player_df = scrape_player(url)
    player_df = check_player_schema(player_df.copy())
    insert_player_stats(player_df,match_cup_id)

    print(f"Data in {cup} has successfully proceeded")


#######################################################################

########### Define class for further data type verification ###########

class Match(BaseModel):
    group: str
    week: int
    arena: str
    index: int
    date: datetime
    time: time
    duration: time

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
    number: str
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

    @validator("attack_point","attack_total","block_point","serve_point","serve_total",
               "receive_nice","receive_total","dig_nice","dig_total","set_nice","set_total","total_points")
    def convert_stats(cls,value):
        if isinstance(value,str):
            return int(value)
        return value


#######################################################################


if __name__ == '__main__':
    url = 'http://114.35.229.141/_handler/Match.ashx?CupID=20&MatchID=1&SetNum=0'
    start(url)



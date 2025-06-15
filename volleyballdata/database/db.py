from sqlalchemy import text
from volleyballdata.database.router import Router

################ Define functions for inserting data into database ################

def get_router():
    return Router()


"""Insert match data into mysql"""
def insert_match(match_df, cup, matchid):
    router = get_router()
    db_conn = router.mysql_volleyball_conn

    query = text("""
    INSERT IGNORE INTO Matches (match_cup_id, match_id, tournament_id, match_date, match_time, arena, duration, match_type)
    VALUES (:match_cup_id, :match_id, :tournament_id, :match_date, :match_time, :arena, :duration, :match_type)
    """)

    row = match_df.iloc[0]

    paras = {
    "match_cup_id": f"{matchid}_{cup}",
    "match_id": row["index"],
    "tournament_id": cup,
    "match_date": row["date"],
    "match_time": row["time"],
    "arena": row["arena"],
    "duration": row["duration"],
    "match_type": row["match_type"],
    }

    db_conn.execute(query, paras)

    db_conn.commit()
    db_conn.close()

"""Insert match score data into mysql"""
def insert_match_score(match_score_df, match_cup_id):
    router = get_router()
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
    router = get_router()
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
    router = get_router()
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
    router = get_router()
    db_conn = router.mysql_volleyball_conn

    query = "    INSERT INTO Player (player_name, player_number, position)    VALUES (%s, %s, %s)    "

    for row in player_df.to_dict(orient="records"):
        db_conn.execute(query, (row["name"], row["number"], row["position"]))

    db_conn.commit()
    db_conn.close()
"""

def insert_player_stats(player_df, match_cup_id):
    router = get_router()
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
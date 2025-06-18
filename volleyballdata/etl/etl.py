import pandas as pd
from sqlalchemy import create_engine, engine
from volleyballdata.config import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER


'''Connection Setting'''
def get_mysql_volleyballdata_conn(database: str ="volleyballdb") -> engine.base.Connection:
    """
    user: user
    password: test
    host: localhost
    port: 3306
    database: volleyballdb
    """
    #address = "mysql+pymysql://user:test@host.docker.internal:3306/volleyballdb"
    address = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD})"
    f"{MYSQL_HOST}:{MYSQL_PORT}/{database}"
    )
    engine = create_engine(address)
    
    connect = engine.connect()
    return connect




sql = f"SELECT * FROM Matches"
try:
    with get_mysql_volleyballdata_conn() as conn:
        result = pd.read_sql(sql,con=conn.connection)
        print(result.head())
except Exception as e:
    print(f"Database connection error:{e}")

'''Transform'''
sql = f"""SELECT match_cup_id, 
        tournament_id, 
        SUBSTRING_INDEX(match_cup_id,'_',1) MATCH_ID,
        match_date,
        YEAR(match_date) YEAR,
        MONTH(match_date) MONTH,
        DAY(match_date) DAY,
        match_time,
        arena,
        CASE 
            WHEN arena = '臺灣體育大學體育館' THEN 'Taichung City'
            WHEN arena = '臺灣大學綜合體育館' THEN 'Taipei City'
            WHEN arena = '屏東縣立體育館' THEN 'Pingtung County'
            WHEN arena = '新竹縣體育館' THEN 'Hsinchu County County'
            WHEN arena = '臺北市立大學體育館' THEN 'Taipei City'
            WHEN arena = '成功大學體育館' THEN 'Tainan City'
            WHEN arena = '彰化師範大學體育館' THEN 'Changhua County'
            WHEN arena = '輔仁大學中美堂' THEN 'New Taipei City'
            WHEN arena = '鳳山體育館' THEN 'Kaohsiung City'
            WHEN arena = '新莊體育館' THEN 'New Taipei City'
            WHEN arena = '桃園體育館' THEN 'Taoyuan City'
            WHEN arena = '雲林縣立體育館' THEN 'Yunlin County'
            WHEN arena = '國北教大體育館' THEN 'Taipei City'
            WHEN arena = '中原大學體育館' THEN 'Taoyuan City'
            WHEN arena = '嘉義市港坪體育館' THEN 'Chiayi City'
            WHEN arena = '苗栗巨蛋體育館' THEN 'Miaoli County'
            WHEN arena = '雲科大體育館' THEN 'Yunlin County'
            WHEN arena = '彰化縣立體育館' THEN 'Changhua County'
            WHEN arena = '花蓮小巨蛋體育館' THEN 'Hualien County'
            ELSE 'UNKNOWN'
        END AS CITY,
        duration,
        match_type,
        CASE 
            WHEN match_type = '常規賽' THEN 'Regular'
            WHEN match_type = '挑戰賽' THEN 'Qualifier'
            WHEN match_type = '季後賽' THEN 'Playoffs'
        END AS ENG_MATCH_TYPE,
        `group`,
        CASE
            WHEN `group` = '男子組' THEN 'Mens Division'
            WHEN `group` = '女子組' THEN 'Womens Division'
        END AS ENG_GROUP
        FROM `Matches` 
"""
try:
    with get_mysql_volleyballdata_conn() as conn:
        result = pd.read_sql(sql,con=conn.connection)
        print(result.head())
        result.to_csv("Matches.csv", index=False, encoding='utf-8-sig')
except Exception as e:
    print(f"Database connection error:{e}")

sql = f"""SELECT match_coach_id, 
        match_cup_id, 
        team, 
        CASE
            WHEN team = '台電公司' THEN '台電男排'
            WHEN team = 'MIZUNO' THEN '雲林Mizuno'
            WHEN team = '中國人纖' THEN '新北中纖'
            WHEN team = 'conti' THEN '臺北Conti'
            WHEN team = '桃園台灣產險' THEN '桃園臺產'
            WHEN team = '桃園臺灣產險' THEN '桃園臺產'
            WHEN team = '長力男排' THEN '臺中長力'
            WHEN team = '屏東台電' THEN '台電男排'
            WHEN team = '桃園臺產隼鷹' THEN '桃園臺產'
            WHEN team = '愛山林' THEN '愛山林建設'
            WHEN team = '高雄台電' THEN '台電女排'
            WHEN team = '連莊' THEN '連莊排球隊'
            WHEN team = '雲林美津濃' THEN '雲林Mizuno'
            ELSE team
        END AS COR_TEAM,
        CASE
            WHEN team = '國訓中心' THEN 'Kaohsiung City'
            WHEN team = '桃園石易' THEN 'Taoyuan City'
            WHEN team = '台電公司' THEN 'Pingtung County'
            WHEN team = 'MIZUNO' THEN 'Yunlin County'
            WHEN team = '長力男排' THEN 'Taichung City'
            WHEN team = 'ATTACKLINE' THEN 'Taipei City'
            WHEN team = '匯竑國際' THEN 'New Taipei City'
            WHEN team = '中國人纖' THEN 'New Taipei City'
            WHEN team = 'conti' THEN 'Taipei City'
            WHEN team = '極速超跑' THEN 'Kaohsiung City'
            WHEN team = '雲林Mizuno' THEN 'Yunlin County' 
            WHEN team = '桃園台灣產險' THEN 'Taoyuan City' 
            WHEN team = '愛山林' THEN 'New Taipei City'
            WHEN team = '臺北鯨華' THEN 'Taipei City'
            WHEN team = '臺中長力' THEN 'Taichung City'
            WHEN team = '桃園臺產' THEN 'Taoyuan City'
            WHEN team = '台電男排' THEN 'Pingtung County'
            WHEN team = '台電女排' THEN 'Taoyuan City'
            WHEN team = '桃園臺產隼鷹' THEN 'Taoyuan City'
            WHEN team = '屏東台電' THEN 'Pingtung County'
            WHEN team = '臺中太陽神' THEN 'Taichung City'
            WHEN team = '愛山林建設' THEN 'New Taipei City'
            WHEN team = '高雄台電' THEN 'Taoyuan City'
            WHEN team = '桃園臺灣產險' THEN 'Taoyuan City'
            WHEN team = '連莊' THEN 'Taichung City'
            WHEN team = '新北中纖' THEN 'New Taipei City'
            WHEN team = '臺北Conti' THEN 'Taipei City'
            WHEN team = '連莊排球隊' THEN 'Taichung City' 
            WHEN team = '彰化三大有線' THEN 'Changhua County' 
            WHEN team = '雲林美津濃' THEN 'Yunlin County'
            WHEN team = '凱撒飯店連鎖' THEN 'New Taipei City'
            WHEN team = '義力營造' THEN 'New Taipei City'
        END AS TEAM_CITY,
        head_coach, 
        assistant_coach1, 
        assistant_coach2 
        FROM `Match_Coach`
"""
try:
    with get_mysql_volleyballdata_conn() as conn:
        result = pd.read_sql(sql,con=conn.connection)
        print(result.head())
        result.to_csv("Match_Coach.csv", index=False, encoding='utf-8-sig')
except Exception as e:
    print(f"Database connection error:{e}")

sql = f"""SELECT score_id, 
        match_cup_id, 
        match_team, 
        CASE
            WHEN match_team = '台電公司' THEN '台電男排'
            WHEN match_team = 'MIZUNO' THEN '雲林Mizuno'
            WHEN match_team = '中國人纖' THEN '新北中纖'
            WHEN match_team = 'conti' THEN '臺北Conti'
            WHEN match_team = '桃園台灣產險' THEN '桃園臺產'
            WHEN match_team = '桃園臺灣產險' THEN '桃園臺產'
            WHEN match_team = '長力男排' THEN '臺中長力'
            WHEN match_team = '屏東台電' THEN '台電男排'
            WHEN match_team = '桃園臺產隼鷹' THEN '桃園臺產'
            WHEN match_team = '愛山林' THEN '愛山林建設'
            WHEN match_team = '高雄台電' THEN '台電女排'
            WHEN match_team = '連莊' THEN '連莊排球隊'
            WHEN match_team = '雲林美津濃' THEN '雲林Mizuno'
            ELSE match_team
        END AS COR_TEAM,
        CASE
            WHEN match_team = '國訓中心' THEN 'Kaohsiung City'
            WHEN match_team = '桃園石易' THEN 'Taoyuan City'
            WHEN match_team = '台電公司' THEN 'Pingtung County'
            WHEN match_team = 'MIZUNO' THEN 'Yunlin County'
            WHEN match_team = '長力男排' THEN 'Taichung City'
            WHEN match_team = 'ATTACKLINE' THEN 'Taipei City'
            WHEN match_team = '匯竑國際' THEN 'New Taipei City'
            WHEN match_team = '中國人纖' THEN 'New Taipei City'
            WHEN match_team = 'conti' THEN 'Taipei City'
            WHEN match_team = '極速超跑' THEN 'Kaohsiung City'
            WHEN match_team = '雲林Mizuno' THEN 'Yunlin County' 
            WHEN match_team = '桃園台灣產險' THEN 'Taoyuan City' 
            WHEN match_team = '愛山林' THEN 'New Taipei City'
            WHEN match_team = '臺北鯨華' THEN 'Taipei City'
            WHEN match_team = '臺中長力' THEN 'Taichung City'
            WHEN match_team = '桃園臺產' THEN 'Taoyuan City'
            WHEN match_team = '台電男排' THEN 'Pingtung County'
            WHEN match_team = '台電女排' THEN 'Taoyuan City'
            WHEN match_team = '桃園臺產隼鷹' THEN 'Taoyuan City'
            WHEN match_team = '屏東台電' THEN 'Pingtung County'
            WHEN match_team = '臺中太陽神' THEN 'Taichung City'
            WHEN match_team = '愛山林建設' THEN 'New Taipei City'
            WHEN match_team = '高雄台電' THEN 'Taoyuan City'
            WHEN match_team = '桃園臺灣產險' THEN 'Taoyuan City'
            WHEN match_team = '連莊' THEN 'Taichung City'
            WHEN match_team = '新北中纖' THEN 'New Taipei City'
            WHEN match_team = '臺北Conti' THEN 'Taipei City'
            WHEN match_team = '連莊排球隊' THEN 'Taichung City' 
            WHEN match_team = '彰化三大有線' THEN 'Changhua County' 
            WHEN match_team = '雲林美津濃' THEN 'Yunlin County'
            WHEN match_team = '凱撒飯店連鎖' THEN 'New Taipei City'
            WHEN match_team = '義力營造' THEN 'New Taipei City'
        END AS TEAM_CITY,
        set1,
        set2,
        set3,
        set4,
        set5,
        is_winner
        FROM `Match_Score`
"""
try:
    with get_mysql_volleyballdata_conn() as conn:
        result = pd.read_sql(sql,con=conn.connection)
        print(result.head())
        result.to_csv("Match_Score.csv", index=False, encoding='utf-8-sig')
except Exception as e:
    print(f"Database connection error:{e}")


sql = f"""SELECT stat_id, 
        match_cup_id, 
        team, 
        CASE
            WHEN team = '台電公司' THEN '台電男排'
            WHEN team = 'MIZUNO' THEN '雲林Mizuno'
            WHEN team = '中國人纖' THEN '新北中纖'
            WHEN team = 'conti' THEN '臺北Conti'
            WHEN team = '桃園台灣產險' THEN '桃園臺產'
            WHEN team = '桃園臺灣產險' THEN '桃園臺產'
            WHEN team = '長力男排' THEN '臺中長力'
            WHEN team = '屏東台電' THEN '台電男排'
            WHEN team = '桃園臺產隼鷹' THEN '桃園臺產'
            WHEN team = '愛山林' THEN '愛山林建設'
            WHEN team = '高雄台電' THEN '台電女排'
            WHEN team = '連莊' THEN '連莊排球隊'
            WHEN team = '雲林美津濃' THEN '雲林Mizuno'
            ELSE team
        END AS COR_TEAM,
        CASE
            WHEN team = '國訓中心' THEN 'Kaohsiung City'
            WHEN team = '桃園石易' THEN 'Taoyuan City'
            WHEN team = '台電公司' THEN 'Pingtung County'
            WHEN team = 'MIZUNO' THEN 'Yunlin County'
            WHEN team = '長力男排' THEN 'Taichung City'
            WHEN team = 'ATTACKLINE' THEN 'Taipei City'
            WHEN team = '匯竑國際' THEN 'New Taipei City'
            WHEN team = '中國人纖' THEN 'New Taipei City'
            WHEN team = 'conti' THEN 'Taipei City'
            WHEN team = '極速超跑' THEN 'Kaohsiung City'
            WHEN team = '雲林Mizuno' THEN 'Yunlin County' 
            WHEN team = '桃園台灣產險' THEN 'Taoyuan City' 
            WHEN team = '愛山林' THEN 'New Taipei City'
            WHEN team = '臺北鯨華' THEN 'Taipei City'
            WHEN team = '臺中長力' THEN 'Taichung City'
            WHEN team = '桃園臺產' THEN 'Taoyuan City'
            WHEN team = '台電男排' THEN 'Pingtung County'
            WHEN team = '台電女排' THEN 'Taoyuan City'
            WHEN team = '桃園臺產隼鷹' THEN 'Taoyuan City'
            WHEN team = '屏東台電' THEN 'Pingtung County'
            WHEN team = '臺中太陽神' THEN 'Taichung City'
            WHEN team = '愛山林建設' THEN 'New Taipei City'
            WHEN team = '高雄台電' THEN 'Taoyuan City'
            WHEN team = '桃園臺灣產險' THEN 'Taoyuan City'
            WHEN team = '連莊' THEN 'Taichung City'
            WHEN team = '新北中纖' THEN 'New Taipei City'
            WHEN team = '臺北Conti' THEN 'Taipei City'
            WHEN team = '連莊排球隊' THEN 'Taichung City' 
            WHEN team = '彰化三大有線' THEN 'Changhua County' 
            WHEN team = '雲林美津濃' THEN 'Yunlin County'
            WHEN team = '凱撒飯店連鎖' THEN 'New Taipei City'
            WHEN team = '義力營造' THEN 'New Taipei City'
        END AS TEAM_CITY,
        number,
        name,
        position,
        CASE
            WHEN position = '攔中' THEN 'Middle Blocker'
            WHEN position = '舉球' THEN 'Setter'
            WHEN position = '長攻' THEN 'Outside Hitter'
            WHEN position = '自由' THEN 'Libero'
            WHEN position = '對角' THEN 'Opposite Hitter'
        END AS ENG_POSITION,
        attack_point,
        attack_total,
        block_point,
        serve_point,
        serve_total,
        receive_nice,
        receive_total,
        dig_nice,
        dig_total,
        set_nice,
        set_total,
        total_points
        FROM `Player_Stats`
"""
try:
    with get_mysql_volleyballdata_conn() as conn:
        result = pd.read_sql(sql,con=conn.connection)
        print(result.head())
        result.to_csv("Player_Stats.csv", index=False, encoding='utf-8-sig')
except Exception as e:
    print(f"Database connection error:{e}")


sql = f"""SELECT match_referee_id, 
        match_cup_id, 
        first_referee, 
        second_referee
        FROM `Match_Referee`
    """

try:
    with get_mysql_volleyballdata_conn() as conn:
        result = pd.read_sql(sql,con=conn.connection)
        print(result.head())
        result.to_csv("Match_Referee.csv", index=False, encoding='utf-8-sig')
except Exception as e:
    print(f"Database connection error:{e}")

'''
if __name__ == "__main__":
'''
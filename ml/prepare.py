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
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{database}"
    )
    engine = create_engine(address)
    
    connect = engine.connect()
    return connect

sql = """SELECT p.name,
        pr.eng_position, 
        CASE WHEN team = '國訓中心' THEN 'Mens Division' 
            WHEN team = '桃園石易' THEN 'Mens Division' 
            WHEN team = '台電公司' THEN 'Mens Division' 
            WHEN team = 'MIZUNO' THEN 'Mens Division' 
            WHEN team = '長力男排' THEN 'Mens Division' 
            WHEN team = 'ATTACKLINE' THEN 'Womens Division' 
            WHEN team = '匯竑國際' THEN 'Womens Division' 
            WHEN team = '中國人纖' THEN 'Womens Division' 
            WHEN team = 'conti' THEN 'Mens Division' 
            WHEN team = '極速超跑' THEN 'Womens Division' 
            WHEN team = '雲林Mizuno' THEN 'Mens Division' 
            WHEN team = '桃園台灣產險' THEN 'Mens Division' 
            WHEN team = '愛山林' THEN 'Womens Division' 
            WHEN team = '臺北鯨華' THEN 'Womens Division' 
            WHEN team = '臺中長力' THEN 'Mens Division' 
            WHEN team = '桃園臺產' THEN 'Mens Division' 
            WHEN team = '台電男排' THEN 'Mens Division' 
            WHEN team = '台電女排' THEN 'Womens Division' 
            WHEN team = '桃園臺產隼鷹' THEN 'Mens Division' 
            WHEN team = '屏東台電' THEN 'Mens Division' 
            WHEN team = '臺中太陽神' THEN 'Mens Division' 
            WHEN team = '愛山林建設' THEN 'Womens Division' 
            WHEN team = '高雄台電' THEN 'Womens Division' 
            WHEN team = '桃園臺灣產險' THEN 'Mens Division' 
            WHEN team = '連莊' THEN 'Mens Division' 
            WHEN team = '新北中纖' THEN 'Womens Division' 
            WHEN team = '臺北Conti' THEN 'Mens Division' 
            WHEN team = '連莊排球隊' THEN 'Mens Division' 
            WHEN team = '彰化三大有線' THEN 'Mens Division' 
            WHEN team = '雲林美津濃' THEN 'Mens Division' 
            WHEN team = '凱撒飯店連鎖' THEN 'Womens Division' 
            WHEN team = '義力營造' THEN 'Womens Division' 
        END AS DIVISION, 
        sum(attack_point)/sum(attack_total), 
        sum(block_point), 
        sum(serve_point)/sum(serve_total), 
        sum(receive_nice)/sum(receive_total), 
        sum(dig_nice)/sum(dig_total), 
        sum(set_nice)/sum(set_total), 
        sum(total_points), 
        pr.national_team 
        FROM `Player_Stats` p 
        JOIN Players pr on p.name = pr.name 
        WHERE pr.national_team = 1 
        GROUP BY p.name, pr.eng_position, DIVISION, pr.national_team
"""
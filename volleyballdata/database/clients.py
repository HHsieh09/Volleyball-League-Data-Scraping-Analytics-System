from sqlalchemy import create_engine, engine
from volleyballdata.config import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT, MYSQL_USER

def get_mysql_volleyballdata_conn() -> engine.base.Connection:
    """
    user: user
    password: test
    host: localhost
    port: 3306
    database: volleyballdb
    """
    #address = "mysql+pymysql://user:test@host.docker.internal:3306/volleyballdb"
    address = (
    f"mysql+pymysql://{MYSQL_DATA_USER}:{MYSQL_DATA_PASSWORD}"
    f"@{MYSQL_DATA_HOST}:{MYSQL_DATA_PORT}/{MYSQL_DATA_DATABASE}"
    )
    engine = create_engine(address)
    
    connect = engine.connect()
    return connect
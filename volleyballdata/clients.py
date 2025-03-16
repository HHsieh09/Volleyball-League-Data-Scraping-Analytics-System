from sqlalchemy import create_engine, engine

def get_mysql_volleyballdata_conn() -> engine.base.Connection:
    """
    user: user
    password: test
    host: localhost
    port: 3306
    database: volleyballdb
    """
    address = "mysql+pymysql://user:test@host.docker.internal:3306/volleyballdb"
    engine = create_engine(address)
    
    connect = engine.connect()
    return connect
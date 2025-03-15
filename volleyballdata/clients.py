from sqlalchemy import create_engine, engine

def get_mysql_volleyballdata_conn() -> engine.base.Connection:
    """
    user: root
    password: test
    host: localhost
    port: 3306
    database: volleyballdb
    """
    address = "mysql+pymysql://root:test@localhost/volleyballdb"
    engine = create_engine(address)
    connect = engine.connect()
    return connect
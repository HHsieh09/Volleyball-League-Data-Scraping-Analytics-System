import os
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from sqlalchemy.engine import Connection
from unittest.mock import patch, MagicMock
from api.main import app, get_mysql_volleyballdata_conn

load_dotenv(dotenv_path=".env.test", override=True)

client = TestClient(app)

def test_env_check():
    print("MYSQL_HOST = ", os.getenv("MYSQL_HOST"))
    assert os.getenv("MYSQL_HOST") == "127.0.0.1"


#def test_get_mysql_volleyballdata_conn():
#    conn = (get_mysql_volleyballdata_conn())
#    assert isinstance (conn, Connection)

@patch("volleyballdata.database.clients.get_mysql_volleyballdata_conn")
def test_get_mysql_volleyballdata_conn(mock_conn):
    mock_db = MagicMock()
    mock_conn.return_value = mock_db
    assert mock_conn() is not None
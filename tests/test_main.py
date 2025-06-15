import os
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from sqlalchemy import engine
from api.main import app, get_mysql_volleyballdata_conn

load_dotenv(dotenv_path=".env.test", override=True)

client = TestClient(app)

def test_env_check():
    print("MYSQL_HOST = ", os.getenv("MYSQL_HOST"))
    assert os.getenv("MYSQL_HOST") == "127.0.0.1"

def test_get_mysql_volleyballdata_conn():
    conn = (get_mysql_volleyballdata_conn())
    assert isinstance (conn, engine.Connection)
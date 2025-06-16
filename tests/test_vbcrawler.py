from volleyballdata.crawler.vbcrawler import (
    is_valid_match,
    get_cupid,
    get_matchid,
    fetch_html,
    scrape_match,
    scrape_match_score,
    scrape_ref,
    scrape_coach,
    scrape_player,
    )
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import pandas as pd

global soup_html
global soup_lxml

url = 'http://114.35.229.141/_handler/Match.ashx?CupID=20&MatchID=1&SetNum=0'

with open("tests/sample_html.html","r",encoding="utf-8") as f:
    html = f.read()
    soup_html = BeautifulSoup(html, "html.parser")
    soup_lxml = BeautifulSoup(html, "lxml")


def test_is_valid_match():
    expected = True
    result = is_valid_match(url)
    assert result == expected

def test_get_cupid():
    expected = 20
    result = get_cupid(url)
    assert result == expected

def test_get_matchid():
    expected = 1
    result = get_matchid(url)
    assert result == expected

@patch("volleyballdata.database.clients.get_mysql_volleyballdata_conn")
def test_scrape_match(mock_db_conn):
    fake_conn = MagicMock()
    fake_conn.execute.return_value = None
    mock_db_conn.return_value = fake_conn

    expected_data = {
        "group": ["女子組"],
        "week": ["1"],
        "arena": ["成功大學體育館"],
        "index": ["1"],
        "date": ["2024/10/19"],
        "time": ["13:00"],
        "duration": ["01:58"],
        "match_type": ["常規賽"],
    }
    expected_df = pd.DataFrame(expected_data)

    actual_df = scrape_match(soup_html, url)

    pd.testing.assert_frame_equal(actual_df, expected_df)

@patch("volleyballdata.database.clients.get_mysql_volleyballdata_conn")
def test_scrape_match_score(mock_db_conn):
    fake_conn = MagicMock()
    fake_conn.execute.return_value = None
    mock_db_conn.return_value = fake_conn

    expected_df = pd.DataFrame([
    {
        "team": "臺北鯨華",
        "set1": "20",
        "set2": "25",
        "set3": "25",
        "set4": "25",
        "set5": "00",
    },
    {
        "team": "高雄台電",
        "set1": "25",
        "set2": "17",
        "set3": "18",
        "set4": "21",
        "set5": "00",
    },
    ])

    actual_df = scrape_match_score(soup_html)

    pd.testing.assert_frame_equal(actual_df,expected_df)

@patch("volleyballdata.database.clients.get_mysql_volleyballdata_conn")
def test_scrape_ref(mock_db_conn):
    fake_conn = MagicMock()
    fake_conn.execute.return_value = None
    mock_db_conn.return_value = fake_conn

    expected_df = pd.DataFrame([
    {"first_referee": "王啟瑞",
    "second_referee": "張志豪",}
    ])

    actual_df = scrape_ref(soup_lxml)
    pd.testing.assert_frame_equal(actual_df,expected_df)

@patch("volleyballdata.database.clients.get_mysql_volleyballdata_conn")
def test_scrape_coach(mock_db_conn):
    fake_conn = MagicMock()
    fake_conn.execute.return_value = None
    mock_db_conn.return_value = fake_conn

    expected_df = pd.DataFrame([
        {
            "team": "臺北鯨華",
            "head_coach": "鄧衍敏",
            "assistant_coach1": "詹詠鈞",
            "assistant_coach2": "張芷瑄",
        },
        {
            "team": "高雄台電",
            "head_coach": "張秝芸",
            "assistant_coach1": "姚承杉",
            "assistant_coach2": "王前鑌",
        },
    ])

    actual_df = scrape_coach(soup_html)
    pd.testing.assert_frame_equal(actual_df,expected_df)

@patch("volleyballdata.database.clients.get_mysql_volleyballdata_conn")
def test_scrape_player(mock_db_conn):
    fake_conn = MagicMock()
    fake_conn.execute.return_value = None
    mock_db_conn.return_value = fake_conn

    expected_df = pd.DataFrame([
        {
            "team": "臺北鯨華",
            "number": "1",
            "name": "林良黛",
            "position": "長攻",
            "attack_point": "10",
            "attack_total": "27",
            "block_point": "0",
            "serve_point": "0",
            "serve_total": "22",
            "receive_nice": "17",
            "receive_total": "32",
            "dig_nice": "6",
            "dig_total": "12",
            "set_nice": "0",
            "set_total": "0",
            "total_points": "10",
        },
    ])

    player_df = scrape_player(soup_lxml)
    actual_df = player_df.iloc[0:1].reset_index(drop=True)

    pd.testing.assert_frame_equal(actual_df,expected_df)

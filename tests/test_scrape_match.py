from volleyballdata.crawler.vbcrawler import fetch_html,scrape_match
from unittest.mock import patch, MagicMock
import pandas as pd

url = 'http://114.35.229.141/_handler/Match.ashx?CupID=20&MatchID=1&SetNum=0'

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

    soup_html = fetch_html(url)
    actual_df = scrape_match(soup_html,url)

    pd.testing.assert_frame_equal(actual_df, expected_df)
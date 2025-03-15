from volleyballdata import scrape_match
import pandas as pd

url = 'http://114.35.229.141/_handler/Match.ashx?CupID=20&MatchID=1&SetNum=0'

def test_scrape_match():
    expected_data = {
        "group": ["女子組"],
        "week": ["1"],
        "arena": ["成功大學體育館"],
        "index": ["1"],
        "date": ["2024/10/19"],
        "time": ["13:00"],
        "duration": ["01:58"],
    }
    expected_df = pd.DataFrame(expected_data)
    actual_df = scrape_match(url)

    pd.testing.assert_frame_equal(actual_df, expected_df)

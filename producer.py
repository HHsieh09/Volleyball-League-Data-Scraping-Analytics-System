from volleyballdata.tasks.tasks import crawler_match
from volleyballdata.crawler.vbcrawler import is_valid_match
 
# 發送任務有兩種方式
# 1.
#13-20
cupids = list(range(13, 21))  # 13 ~ 20
max_match_id = 300  # 假設最多 300，實測後調整

for cup in cupids:
    for match in range(1, max_match_id):
        url = f'http://114.35.229.141/_handler/Match.ashx?CupID={cup}&MatchID={match}&SetNum=0'
        if is_valid_match(url):
            crawler_match.delay(url)
# 2.
# task = crawler.s(x=0)
# task.apply_async()
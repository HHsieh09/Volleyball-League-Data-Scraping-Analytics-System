from volleyballdata.tasks.tasks import crawler_match
from volleyballdata.crawler.vbcrawler import is_valid_match


def send_tasks():
    # 發送任務有兩種方式
    # 1.
    #13-20
    cupids = list(range(13, 17))  # 13 ~ 20

    for cup in cupids:
        print(f"Scan Cup ID: {cup}")
        match_id = 1
        max_match_id = 300

        while match_id <=  max_match_id:
            url = f'http://114.35.229.141/_handler/Match.ashx?CupID={cup}&MatchID={match_id}&SetNum=0'

            if is_valid_match(url):
                crawler_match.apply_async(args=[url], queue=f'cup_{cup}')
                print(f"Send Successfully: {url}")
            else:
                print(f"Failed Sending ●∩●: {url}")

            match_id += 1

        '''
        for match in range(1, max_match_id):
            url = f'http://114.35.229.141/_handler/Match.ashx?CupID={cup}&MatchID={match}&SetNum=0'
        '''
    # 2.
    # task = crawler.s(x=0)
    # task.apply_async()

if __name__ == "__main__":
    send_tasks()
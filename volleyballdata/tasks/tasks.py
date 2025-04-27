from volleyballdata.crawler.vbcrawler import start
from volleyballdata.tasks.worker import app

@app.task(queue='default')
def crawler_match(url: str):
    start(url)
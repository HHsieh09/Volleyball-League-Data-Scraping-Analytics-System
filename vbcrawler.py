import re
import sys
import time
import datetime

import requests
import pandas as pd
from loguru import logger
from bs4 import BeautifulSoup
from pydantic import BaseModel 

"""Parameter of request header to mimic the browser sending request"""
def tvl_header():
    return {
        "Accept": "/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,zh-TW;q=0.9,zh;q=0.8",
        "Connection": "keep-alive",
        "Host": "114.35.229.141",
        "Refer": "http://114.35.229.141/Match.aspx?CupID=20",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

"""Gather the Match Information"""
def scrape_match(url: str,) -> pd.DataFrame:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    match_info = soup.find('h3').get_text(strip=True)

    """Group the capturing information into groups"""
    match_org = re.search(r'(.*?) 第(\d+)週\((.*?)\)\s+編號：(\d+)\s+\((\d+)月(\d+)日\s+(\d+:\d+)\)\s+歷時\s+(\d+:\d+)', match_info)

    if match_org:
        group = match_org.group(1).strip()
        week = match_org.group(2).strip()
        arena = match_org.group(3).strip()
        index = match_org.group(4).strip()
        month = match_org.group(5).zfill(2)
        day = match_org.group(6).zfill(2)
        month_int = int(month)
        year = 2024 if month_int >= 10 else 2025
        date = f"{year}/{month}/{day}"
        time = match_org.group(7).strip()
        duration = match_org.group(8).strip()

        match_dict = {
            "group": group,
            "week": week,
            "arena": arena,
            "index": index,
            "date": date,
            "time": time,
            "duration": duration,
        }

        match_df = pd.DataFrame([match_dict])
        print(match_df)

        return match_df


def scrape_match_score(url: str,) -> pd.DataFrame:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    match_table = soup.find('div',class_="MatchResult").find('table')
    match_rows = match_table.find_all('tr')

    match_score_info = []
    for row in match_rows:
        col = row.find_all('td')
        if col:
            """Get the team name"""
            team_name_dirty = col[0].find_all('a')[-1]
            team_name = team_name_dirty.get_text(strip=True)

            """Get match socres data"""
            set_scores = [coll.get_text(strip=True) for coll in col[1:6]]

            match_score_info.append({
                "team": team_name,
                "set1":set_scores[0],
                "set2":set_scores[1],
                "set3":set_scores[2],
                "set4":set_scores[3],
                "set5":set_scores[4],
            })

    match_score_df = pd.DataFrame(match_score_info)
    
    print(match_score_df)
    return match_score_df


def scrape_ref(url: str,):
    response = requests.get(url)
    #Since the website wrongly programmed HTML, which has a </td> before </th>, thus using lxml
    soup = BeautifulSoup(response.text, 'lxml')

    ref_table = soup.find('th',string="第一裁判").find_parent('table')
    ref_rows = ref_table.find_all('tr')

    #Get referee data
    ref_data = {}
    for row in ref_rows:
        ref_type = row.find('th').get_text(strip=True)
        #Since the website wrongly programmed HTML, which has a </td> before </th>, thus using the following code to correctly extract the data
        td = row.find_all('td')
        if td:
            ref_name = td[0].get_text(strip=True)  # First <td> should contain name
        else:
            ref_name = "N/A"  # If no <td> found, fallback to "N/A"

        ref_data[ref_type] = ref_name


    ref_df = pd.DataFrame([ref_data])

    print(ref_df)
    return ref_df

        
def scrape_coach(url: str,) -> pd.DataFrame:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all('h3')
    data_eliminate_first = data[-2:]
    coach_data = []
    for row in data_eliminate_first:
        raw_coach = row.get_text(strip=True)

        team, coaches = raw_coach.split('：')
        coach = coaches.split('、')

        coach_data.append({
            "team": team,
            "head_coach":coach[0],
            "assistant_coach1":coach[1],
            "assistant_coach2":coach[2],
        })

    coach_df = pd.DataFrame(coach_data)
    print(coach_df)
    return coach_df

def scrape_player(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    team_headers = soup.find_all('h3')[-2:]
    team_name = [team.text.split('：')[0].strip() for team in team_headers]

    team_table = soup.find_all('div',{'class':'TableFormat_1'})
    eliminate_first_two = team_table[-2:]

    player_data = []

    for team, fake_table in zip(team_name, eliminate_first_two):
        tables = fake_table.find_all('table')

        for table in tables:
            player_rows = table.find_all('tr')[2:-1]
            for player in player_rows:
                data = player.find_all('td')

                player_stat = {
                    "team": team,
                    "number": data[0].string.strip(),
                    "name": data[1].string.strip(),
                    "position": data[2].string.strip(),
                    "attack_point": data[3].string.strip(),
                    "attack_total": data[4].string.strip(),
                    "block_point": data[5].string.strip(),
                    "serve_point": data[6].string.strip(),
                    "serve_total": data[7].string.strip(),
                    "receive_nice": data[8].string.strip(),
                    "receive_total": data[9].string.strip(),
                    "dig_nice": data[10].string.strip(),
                    "dig_total": data[11].string.strip(),
                    "set_nice": data[12].string.strip(),
                    "set_total": data[13].string.strip(),
                    "total_points": data[14].string.strip(),
                }

                player_data.append(player_stat)

    player_df = pd.DataFrame(player_data)

    print(player_df)
    return player_df

if __name__ == '__main__':
    url = 'http://114.35.229.141/_handler/Match.ashx?CupID=20&MatchID=1&SetNum=0'
    scrape_player(url)

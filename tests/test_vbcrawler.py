import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from volleyballdata.schema.dataset import check_match_schema, check_coach_schema, check_match_score_schema, check_player_schema, check_referee_schema
from volleyballdata.database.db import insert_coach, insert_match, insert_match_score, insert_player_stats, insert_referee 
from urllib.parse import urlparse, parse_qs

################ Define functions for verifying match url is valid ################

def is_valid_match(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        h3 = soup.find('h3')
        if not h3:
            return False
        if "編號" not in h3.text:
            return False
        return True
    except Exception:
        return False

###############################################################

################ Define functions for crawlers ################

def get_cupid(url):
    parse_url = urlparse(url)

    #Get the elements after ? in URL
    urlelement = parse_qs(parse_url.query)

    #Get the cupid from the URL
    cupid = urlelement.get('CupID')
    

    if cupid:
        return int(cupid[0])
    else:
        ("N/A")


def get_matchid(url):
    parse_url = urlparse(url)
    urlelement = parse_qs(parse_url.query)

    matchid = urlelement.get('MatchID')

    if matchid:
        return int(matchid[0])
    else:
        ("N/A")    

###############################################################

################ Define functions for crawlers ################

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

"""Gather match information"""
def scrape_match(url: str,) -> pd.DataFrame:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    match_info = soup.find('h3').get_text(strip=True)

    """Group the capturing information into groups"""
    match_org = re.search(r'(.*?) 第(\d+)週\((.*?)\)\s+編號：(.+?)\s+\((\d+)月(\d+)日\s+(\d+:\d+)\)\s+歷時\s+(\d+:\d+)', match_info)
    match_special = re.search(r'(.*?)\s+(挑戰賽|季後賽)?\((.*?)\)\s+編號：(.+?)\s+\((\d+)月(\d+)日\s+(\d+:\d+)\)\s+歷時\s+(\d+:\d+)', match_info)

    cupidyear = get_cupid(url)

    if match_org:
        group = match_org.group(1).strip()
        week = match_org.group(2).strip()
        arena = match_org.group(3).strip()
        index = match_org.group(4).strip()
        month = match_org.group(5).zfill(2)
        day = match_org.group(6).zfill(2)
        month_int = int(month)
        year = 2004+cupidyear if month_int >= 10 else 2005+cupidyear
        date = f"{year}/{month}/{day}"
        time = match_org.group(7).strip()
        duration = match_org.group(8).strip()
        match_type = "常規賽"

    elif match_special:
        group = match_special.group(1).strip()
        match_type = match_special.group(2) or "Unknown"
        week = "0"
        arena = match_special.group(3).strip()
        index = match_special.group(4).strip()
        month = match_special.group(5).zfill(2)
        day = match_special.group(6).zfill(2)
        month_int = int(month)
        year = 2024 if month_int >= 10 else 2025
        date = f"{year}/{month}/{day}"
        time = match_special.group(7).strip()
        duration = match_special.group(8).strip()

    match_dict = {
        "group": group,
        "week": week,
        "arena": arena,
        "index": index,
        "date": date,
        "time": time,
        "duration": duration,
        "match_type": match_type,
    }

    match_df = pd.DataFrame([match_dict])

    print(match_df)
    return match_df

"""Gather match score information"""
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
    
    return match_score_df

"""Gather referee score information"""
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
    ref_df_rename = ref_df.rename(columns={"第一裁判":"first_referee","第二裁判":"second_referee"})

    return ref_df_rename

"""Gather coach information"""
def scrape_coach(url: str,) -> pd.DataFrame:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all('h3')
    data_eliminate_first = data[-2:]
    coach_data = []
    for row in data_eliminate_first:
        raw_coach = row.get_text(strip=True)

        team, coaches = raw_coach.split('：')
        coach_list = coaches.split('、')

        coach_data.append({
            "team": team,
            "head_coach":coach_list[0] if len(coach_list) > 0 else "N/A",
            "assistant_coach1":coach_list[1] if len(coach_list) > 1 else "N/A",
            "assistant_coach2":coach_list[2] if len(coach_list) > 2 else "N/A",
        })

    coach_df = pd.DataFrame(coach_data)

    return coach_df

"""Gather player information"""
def scrape_player(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    team_headers = soup.find_all('h3')[-2:]
    team_name = [team.text.split('：')[0].strip() for team in team_headers]

    team_table = soup.find_all('div',{'class':'TableFormat_1'})
    eliminate_first_two = team_table[-2:]

    player_data = []

    """To get the team of the players and their stats in each game"""
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

    return player_df
###############################################################


################ Define functions to start the program ################

def start(url):
    cup = get_cupid(url)
    match = get_matchid(url)

    match_df = scrape_match(url)
    match_df = check_match_schema(match_df.copy())
    insert_match(match_df,cup,match)

    match_score_df = scrape_match_score(url)
    match_score_df = check_match_score_schema(match_score_df.copy())
    match_cup_id = str(match_df.iloc[0]["index"]) + "_" + str(cup)
    insert_match_score(match_score_df,match_cup_id)

    ref_df = scrape_ref(url)
    ref_df = check_referee_schema(ref_df)
    insert_referee(ref_df,match_cup_id)

    coach_df = scrape_coach(url)
    coach_df = check_coach_schema(coach_df.copy())
    insert_coach(coach_df,match_cup_id)

    player_df = scrape_player(url)
    player_df = check_player_schema(player_df.copy())
    insert_player_stats(player_df,match_cup_id)

    print(f"Data in {cup} has successfully proceeded")


#######################################################################




if __name__ == '__main__':
    for match_id in range(1,2):
        url = f'http://114.35.229.141/_handler/Match.ashx?CupID=16&MatchID={match_id}&SetNum=0'
        '''
        if is_valid_match(url):
            player_df = scrape_player(url)
            player_df = check_player_schema(player_df.copy())
            print(player_df)
        '''
        '''
        match = get_matchid(url)
        print(match)
        '''
        if is_valid_match(url):
            match_df = scrape_match(url)
            match_df = check_match_schema(match_df.copy())
            print(match_df)
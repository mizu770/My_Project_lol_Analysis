import requests
import pandas as pd
import time
import numpy as np
from ast import literal_eval

api_key = "RGAPI-eaccd64a-3244-4435-8f03-5742962812ce"
#sohwan = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" +'hide on bush' +'?api_key=' + api_key
#r = requests.get(sohwan)
#r.json()['id'] #소환사의 고유 id

#tier_url = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/" + r.json()['id'] +'?api_key=' + api_key
#r2 = requests.get(tier_url)
#r2.json()

CHALLENGER='https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key='+api_key

r = requests.get(CHALLENGER)

league_df = pd.DataFrame(r.json())
print(league_df)

league_df.reset_index(inplace=True)#수집한 챌린저데이터 index정리
league_entries_df = pd.DataFrame(dict(league_df['entries'])).T #dict구조로 되어 있는 entries컬럼 풀어주기
league_df = pd.concat([league_df, league_entries_df], axis=1) #열끼리 결합

league_df = league_df.drop(['index', 'queue', 'name', 'leagueId', 'entries', 'rank'], axis=1)
league_df.info()
league_df.to_csv('챌린저.csv',index=False,encoding = 'cp949')#중간저장

for i in range(len(league_df)):
    try:
        sohwan = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + league_df['summonerName'].iloc[
            i] + '?api_key=' + api_key
        r = requests.get(sohwan)

        while r.status_code == 429:
            time.sleep(5)
            sohwan = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + league_df['summonerName'].iloc[
                i] + '?api_key=' + api_key
            r = requests.get(sohwan)

        account_id = r.json()['accountId']
        league_df.iloc[i, -1] = account_id

    except:
        pass

league_df.to_csv('챌린저2.csv',index=False,encoding = 'cp949')#중간저장

league_df3 = league_df

league_df3.rename(columns={'hotStreak':'account_id'},inplace=True)
print(league_df3['account_id'])
league_df3.loc[league_df3['account_id'] == 'False','account_id'] = np.nan
league_df3.loc[league_df3['account_id'] == 'True','account_id'] = np.nan
print(league_df3['account_id'])
league_df3 = league_df3.dropna()
print(league_df3['account_id'].isnull().sum().sum())
match_info_df = pd.DataFrame()
season = str(13)
for i in range(len(league_df3)):
    try:
        match0 = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + league_df3['account_id'].iloc[
            i] + '?season=' + season + '&api_key=' + api_key
        r = requests.get(match0)

        while r.status_code == 429:
            time.sleep(5)
            match0 = 'https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/' + league_df3['account_id'].iloc[
                i] + '?season=' + season + '&api_key=' + api_key
            r = requests.get(match0)

        match_info_df = pd.concat([match_info_df, pd.DataFrame(r.json()['matches'])])

    except:
        print(i)
match_info_df.to_csv('챌린저3.csv',index=False,encoding = 'cp949')#중간저장
match_info_df2 = match_info_df
match_info_df2 = match_info_df2.drop_duplicates(['gameId'], keep="first")
match_fin = pd.DataFrame()
for i in range(len(match_info_df2)):

    api_url = 'https://kr.api.riotgames.com/lol/match/v4/matches/' + str(
        match_info_df2['gameId'].iloc[i]) + '?api_key=' + api_key
    r = requests.get(api_url)

    if r.status_code == 200:  # response가 정상이면 바로 맨 밑으로 이동하여 정상적으로 코드 실행
        pass

    elif r.status_code == 429:
        print('api cost full : infinite loop start')
        print('loop location : ', i)
        start_time = time.time()

        while True:  # 429error가 끝날 때까지 무한 루프
            if r.status_code == 429:

                print('try 10 second wait time')
                time.sleep(10)

                r = requests.get(api_url)
                print(r.status_code)

            elif r.status_code == 200:  # 다시 response 200이면 loop escape
                print('total wait time : ', time.time() - start_time)
                print('recovery api cost')
                break

    elif r.status_code == 503:  # 잠시 서비스를 이용하지 못하는 에러
        print('service available error')
        start_time = time.time()

        while True:
            if r.status_code == 503 or r.status_code == 429:

                print('try 10 second wait time')
                time.sleep(10)

                r = requests.get(api_url)
                print(r.status_code)

            elif r.status_code == 200:  # 똑같이 response가 정상이면 loop escape
                print('total error wait time : ', time.time() - start_time)
                print('recovery api cost')
                break
    elif r.status_code == 403:  # api갱신이 필요
        print('403 you need api renewal')
        print('break')
        break

    # 위의 예외처리 코드를 거쳐서 내려왔을 때 해당 코드가 실행될 수 있도록 작성
    mat = pd.DataFrame(list(r.json().values()), index=list(r.json().keys())).T
    match_fin = pd.concat([match_fin, mat])
match_fin.to_csv('중간저장용.csv',index=False,encoding='cp949')

data = match_fin
a_ls = list(data['teams'])
# team1
team1_df = pd.DataFrame()
for i in range(len(a_ls)):
    try:
        b = a_ls[i].find('}]},')
        e = literal_eval(a_ls[i][1:b + 3])
        e.pop('bans')
        team1 = pd.DataFrame(list(e.values()), index=list(e.keys())).T
        team1_df = team1_df.append(team1)
    except:
        pass

team1_df.index = range(len(team1_df))
team1_df.to_csv('team1.csv',encoding='cp949')

# team2
team2_df = pd.DataFrame()
for i in range(len(a_ls)):
    try:
        b = a_ls[i].find('}]},')
        f = b + 5
        g = literal_eval(a_ls[i][f:-1])
        g.pop('bans')
        team2 = pd.DataFrame(list(g.values()), index=list(g.keys())).T
        team2_df = team2_df.append(team2)
    except:
        pass

team2_df.index = range(len(team2_df))
team2_df.to_csv('team2.csv',encoding='cp949')
# 컬럼으로 풀어준 team1과 team2와 duration의 데이터를 합쳐준다.
data_team = pd.concat([team1_df, team2_df, data[['gameDuration']]], axis=1)
data_team.to_csv('챌린저 최종.csv',index=False,encoding='cp949')
data_team.to_csv('챌린저 최종2.csv',index=False,encoding='utf-8')
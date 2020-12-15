import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rc('font',family='Malgun Gothic')
game_df = pd.read_csv('최종.csv',encoding='cp949')
team1 = pd.read_csv('team1.csv',encoding='cp949',index_col=0)
team2 = pd.read_csv('team2.csv',encoding='cp949',index_col=0)

print(game_df.head())

for i in range(len(team1)):
    wf_valid = team1['win'].iloc[i]
    if team2['win'].iloc[i] != wf_valid:
        pass
    else:
        print(str(i)+'행 데이터 정합성 문제')

game_df['game_time'] = game_df['gameDuration'] / 60

g1 = game_df[game_df['game_time']>=30].sort_values('win')
g2 = game_df[game_df['game_time']>=40].sort_values('win')
g3 = game_df[game_df['game_time']<30].sort_values('win')
g4 = game_df[game_df['game_time']<20].sort_values('win')


def first_time_ratio(target, variable):
    global g1, g2, g3, g4

    fig = plt.figure(figsize=(20, 20))
    fig.suptitle('게임 시간대별 승리 팀과 패배팀의 ' + variable + '비율', size=30)
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)

    ax1.set_title('GameTime < 20 minute', size=20)
    ax2.set_title('GameTime < 30 minute', size=20)
    ax3.set_title('GameTime > 30 minute', size=20)
    ax4.set_title('GameTime > 40 minute', size=20)

    sns.pointplot(target, variable, data=g4, ax=ax1)
    sns.pointplot(target, variable, data=g3, ax=ax2)
    sns.pointplot(target, variable, data=g1, ax=ax3)
    sns.pointplot(target, variable, data=g2, ax=ax4)
    plt.show()

first_time_ratio('win','firstBlood')
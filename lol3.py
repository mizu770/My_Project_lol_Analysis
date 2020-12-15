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

tf_mapping = {True : 1, False : 0}
bool_column = game_df.select_dtypes('bool').columns.tolist()

for i in bool_column :
    game_df[i] = game_df[i].map(tf_mapping)

wl_mapping = {"Win":"Win","Fail":"Lose"}
game_df['win'] = game_df['win'].map(wl_mapping)

game_df[game_df['win'] == 'Win'].describe()[['towerKills','inhibitorKills','baronKills','dragonKills']]
print(game_df[game_df['win'] == 'Win'].describe()[['towerKills','inhibitorKills','baronKills','dragonKills']])
game_df[game_df['win'] == 'Lose'].describe()[['towerKills','inhibitorKills','baronKills','dragonKills']]
print(game_df[game_df['win'] == 'Lose'].describe()[['towerKills','inhibitorKills','baronKills','dragonKills']])

def first_valid_visualize(df,target,variable):
    sns.factorplot(target,variable,data=df)
    plt.title(variable+' 변수의 승리확률')
    #plt.xticks(df[target])
    plt.show()

first_valid_visualize(game_df,'win','firstBlood')

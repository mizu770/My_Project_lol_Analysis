import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

#분석을 위해서 상대편데이터는 제외하고 한 쪽팀 정보만 저장한 csv 불러오기
team1 = pd.read_csv('tema1.csv',encoding='cp949')

team1 = team1.dropna(axis=0) #데이터 결측치 제거

data2 = team1[list(team1.columns)[2:]] # 타켓 데이터를 제외한 나머지 데이터

# 데이터의 종속변수(승/패)말고 first로 시작하는 변수들은 T/F 값을 가지고 있어 해당 변수들을 인코딩
# 인코딩 방법으로는 ONE HOT ENCODING와 Labeling을 하는 방법이 있는데 저는 라벨링 방법으로 변수를 인코딩
for i in range(0,6):
    le = LabelEncoder()
    y = list(data2.iloc[:,i])

    le.fit(y)
    y2 = le.transform(y)

    data2.iloc[:,i] = y2

# 종속 변수 라벨링
dict_win2 = {"Win": 0, "Fail": 1}

team1['win'].map(dict_win2).tolist()

# train 과 test 0.75와 0.25 비율로 나눔
X_train, X_test, y_train, y_test = train_test_split(data2,np.array(team1['win'].map(dict_win2).tolist()),test_size=0.25,
                                                    stratify=np.array(team1['win'].map(dict_win2).tolist()),random_state=123456)
# Random forest 학습
rf = RandomForestClassifier(n_estimators=100,oob_score=True, random_state=123456)
rf.fit(X_train, y_train) # 소환사 코드를 float으로 변환

predicted = rf.predict(X_test)
accuracy = accuracy_score(y_test,predicted)

#oob_score = out of bag score로써 예측이 얼마나 정확한가에 대한 추정치입니다.
print(f'Out-of-bag score estimate: {rf.oob_score_:.3}')
print(f'Mean accuracy score: {accuracy:.3}')


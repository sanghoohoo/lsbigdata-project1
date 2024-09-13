# 필요한 패키지 불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

np.random.seed(20240911) 

## 필요한 데이터 불러오기
titanic_train=pd.read_csv("./data/spaceship-titanic/train.csv")
titanic_test=pd.read_csv("./data/spaceship-titanic/test.csv")
sub_df=pd.read_csv("./data/spaceship-titanic/sample_submission.csv")

titanic_train
titanic_test
sub_df

titanic_train.dtypes

titanic_train.isna().sum()
titanic_test.isna().sum()

## NaN 채우기
# 각 숫치형 변수는 평균 채우기
# 각 범주형 변수는 Unknown 채우기

## 숫자형 채우기
quantitative = titanic_train.select_dtypes(include = [int, float])
quantitative.isna().sum()
quant_selected = quantitative.columns[quantitative.isna().sum() > 0]

for col in quant_selected:
    titanic_train[col].fillna(titanic_train[col].mean(), inplace=True)
titanic_train[quant_selected].isna().sum()

## 범주형 채우기
qualitative = titanic_train.select_dtypes(include = [object])
qualitative.isna().sum()
qual_selected = qualitative.columns[qualitative.isna().sum() > 0]

for col in qual_selected:
    titanic_train[col].fillna("unknown", inplace=True)
titanic_train[qual_selected].isna().sum()


# test 데이터 채우기
## 숫자형 채우기
quantitative = titanic_test.select_dtypes(include = [int, float])
quantitative.isna().sum()
quant_selected = quantitative.columns[quantitative.isna().sum() > 0]

for col in quant_selected:
    titanic_test[col].fillna(titanic_train[col].mean(), inplace=True)
titanic_test[quant_selected].isna().sum()

## 범주형 채우기
qualitative = titanic_test.select_dtypes(include = [object])
qualitative.isna().sum()
qual_selected = qualitative.columns[qualitative.isna().sum() > 0]

for col in qual_selected:
    titanic_test[col].fillna("unknown", inplace=True)
titanic_test[qual_selected].isna().sum()


# 통합 df 만들기 + 더미코딩
titanic_train_x=titanic_train.drop(['Transported','PassengerId'],axis=1)
titanic_test=titanic_test.drop('PassengerId',axis=1)

df = pd.concat([titanic_train_x, titanic_test], ignore_index=True)
# df.info()
df = pd.get_dummies(
    df,
    columns= df.select_dtypes(include=[object]).columns,
    drop_first=True
    )
df

# train / test 데이터셋
train_n = len(titanic_train)
train_x=df.iloc[:train_n,]
test_x=df.iloc[train_n:,]

train_y=titanic_train["Transported"]

train_x.columns
test_x.columns

# 표준화
num_features = train_x.select_dtypes(include = [int, float]).columns

scaler = StandardScaler()
train_x[num_features] = scaler.fit_transform(train_x[num_features])
test_x[num_features] = scaler.transform(test_x[num_features])

# 로지스틱 회귀 모델
from sklearn.linear_model import LogisticRegression

log_model = LogisticRegression(max_iter=1000, random_state=20240911)
log_model.fit(train_x, train_y)

# 랜덤 포레스트 분류 모델
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

rf_model = RandomForestClassifier(random_state=20240911, n_estimators=100)
best_rf_model=rf_model.fit(train_x, train_y)

# 스택킹을 위한 예측값 생성
y1_hat = best_rf_model.predict_proba(train_x)[:, 1]
y2_hat = log_model.predict_proba(train_x)[:, 1]

train_x_stack = pd.DataFrame({
    'y1': y1_hat,
    'y2': y2_hat
})

# test 데이터에 대해서도 예측
pred_y_rf = best_rf_model.predict_proba(test_x)[:, 1]
pred_y_log = log_model.predict_proba(test_x)[:, 1]

test_x_stack = pd.DataFrame({
    'y1': pred_y_rf,
    'y2': pred_y_log
})

# 메타모델: GradientBoostingClassifier 사용
from sklearn.ensemble import GradientBoostingClassifier
blender_gbc = GradientBoostingClassifier(
    n_estimators=100, learning_rate=0.1, max_depth=10, random_state=20240911
)
blender_gbc.fit(train_x_stack, train_y)

# test 데이터셋에 대한 최종 예측
pred_y = blender_gbc.predict_proba(test_x_stack)[:, 1]

# 예측 결과를 0.5 기준으로 'True' 또는 'False'로 변환
sub_df["Transported"] = (pred_y >= 0.5).astype(bool)

# 결과 저장
sub_df.to_csv("./data/spaceship-titanic/sample_submission_stacking.csv", index=False)

# 필요한 패키지 불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

## 필요한 데이터 불러오기
house_train=pd.read_csv("./data/houseprice/train.csv")
house_test=pd.read_csv("./data/houseprice/test.csv")
sub_df=pd.read_csv("./data/houseprice/sample_submission.csv")

## NaN 채우기
# 각 숫치형 변수는 평균 채우기
# 각 범주형 변수는 Unknown 채우기
house_train.isna().sum()
house_test.isna().sum()

## 숫자형 채우기
quantitative = house_train.select_dtypes(include = [int, float])
quantitative.isna().sum()
quant_selected = quantitative.columns[quantitative.isna().sum() > 0]

for col in quant_selected:
    house_train[col].fillna(house_train[col].mean(), inplace=True)
house_train[quant_selected].isna().sum()

## 범주형 채우기
qualitative = house_train.select_dtypes(include = [object])
qualitative.isna().sum()
qual_selected = qualitative.columns[qualitative.isna().sum() > 0]

for col in qual_selected:
    house_train[col].fillna(house_test[col].mode()[0], inplace=True)
house_train[qual_selected].isna().sum()

house_train.shape
house_test.shape
train_n=len(house_train)

## 숫자형 채우기
quantitative = house_test.select_dtypes(include = [int, float])
quantitative.isna().sum()
quant_selected = quantitative.columns[quantitative.isna().sum() > 0]

for col in quant_selected:
    house_test[col].fillna(house_test[col].mean(), inplace=True)
house_test[quant_selected].isna().sum()

## 범주형 채우기
qualitative = house_test.select_dtypes(include = [object])
qualitative.isna().sum()
qual_selected = qualitative.columns[qualitative.isna().sum() > 0]

for col in qual_selected:
    house_test[col].fillna(house_test[col].mode()[0], inplace=True)
house_test[qual_selected].isna().sum()

# 통합 df 만들기 + 더미코딩
# house_test.select_dtypes(include=[int, float])

df = pd.concat([house_train, house_test], ignore_index=True)
# df.info()
df = pd.get_dummies(
    df,
    columns= df.select_dtypes(include=[object]).columns,
    drop_first=True
    )
df

# train / test 데이터셋
train_df=df.iloc[:train_n,]
test_df=df.iloc[train_n:,]

## train
train_x=train_df.drop("SalePrice", axis=1)
train_y=train_df["SalePrice"]

## test
test_x=test_df.drop("SalePrice", axis=1)

# # 표준화
# scaler = StandardScaler()
# train_x_scaled = scaler.fit_transform(train_x)
# test_x_scaled = scaler.transform(test_x)

# # 정규화된 데이터를 DataFrame으로 변환
# train_x = pd.DataFrame(train_x_scaled, columns=train_x.columns)
# test_x= pd.DataFrame(test_x_scaled, columns=test_x.columns)

# dct 모델 생성
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV

model = DecisionTreeRegressor(random_state=42)
param_grid={
    'max_depth': np.arange(10, 30, 1),
    'min_samples_split': np.arange(30, 50, 1)
}

grid_search=GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    scoring='neg_mean_squared_error',
    cv=5
)

grid_search.fit(train_x,train_y)

grid_search.best_params_
grid_search.cv_results_
score_dct=-grid_search.best_score_
best_model_dct=grid_search.best_estimator_

# Lasso 모델 생성
from sklearn.linear_model import Lasso
model = Lasso()
param_grid={
    'alpha': np.arange(118, 120, 0.1),
}

grid_search=GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    scoring='neg_mean_squared_error',
    cv=5
)

grid_search.fit(train_x,train_y)

grid_search.best_params_
grid_search.cv_results_
score_lasso=-grid_search.best_score_
best_model_lasso=grid_search.best_estimator_

# Bagging

pred_y_lasso = best_model_lasso.predict(test_x)
pred_y_dct = best_model_dct.predict(test_x)

# 가중치는 성능에 반비례하게 설정 (1/score)
weight_lasso = 1 / score_lasso
weight_dct = 1 / score_dct

# 가중치의 합으로 정규화
total_weight = weight_lasso + weight_dct
weight_lasso /= total_weight
weight_dct /= total_weight

# 가중치를 적용한 예측 (Bagging)
pred_y_ensemble = weight_lasso * pred_y_lasso + weight_dct * pred_y_dct

# SalePrice 바꿔치기
sub_df["SalePrice"] = pred_y_ensemble
sub_df

# csv 파일로 내보내기
sub_df.to_csv("./data/houseprice/sample_submission_ensemble.csv", index=False)
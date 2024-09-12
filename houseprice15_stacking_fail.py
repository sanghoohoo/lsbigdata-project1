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

## train데이터 NaN 채우기
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
    house_train[col].fillna('unknown', inplace=True)
house_train[qual_selected].isna().sum()

house_train.shape
house_test.shape
train_n=len(house_train)

# test데이터 nan 채우기
## 숫자형 채우기
quantitative = house_test.select_dtypes(include = [int, float])
quantitative.isna().sum()
quant_selected = quantitative.columns[quantitative.isna().sum() > 0]

for col in quant_selected:
    house_test[col].fillna(house_train[col].mean(), inplace=True)
house_test[quant_selected].isna().sum()

## 범주형 채우기
qualitative = house_test.select_dtypes(include = [object])
qualitative.isna().sum()
qual_selected = qualitative.columns[qualitative.isna().sum() > 0]

for col in qual_selected:
    house_test[col].fillna('unknown', inplace=True)
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

## 이상치 탐색
train_df=train_df.query("GrLivArea <= 4500")

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

np.random.seed(20270911)

# randforest 모델 생성
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

model = RandomForestRegressor(n_estimators=100, max_features=None)

param_grid={
    'max_depth': [11],#np.arange(10, 15, 1), #11
    'min_samples_split': [5],#np.arange(4, 10, 1), # 5
    'min_samples_leaf': [1]#np.arange(1, 3, 1) #1
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
best_model_rf=grid_search.best_estimator_

# Elasticnet 모델 생성
from sklearn.linear_model import ElasticNet
model = ElasticNet()

param_grid={
    'alpha': [65.3],#np.arange(65, 67, 0.1),  #65.3
    'l1_ratio': [1]#np.arange(0.9, 1, 0.01)
}

grid_search=GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    scoring='neg_mean_squared_error',
    cv=5
)

grid_search.fit(train_x,train_y)

grid_search.best_params_
best_model_eln=grid_search.best_estimator_

# stacking

y1_hat = best_model_eln.predict(train_x)
y2_hat = best_model_rf.predict(train_x)

train_x_stack=pd.DataFrame({
    'y1':y1_hat,
    'y2':y2_hat
})

# 블렌더 모델 생성
from sklearn.linear_model import ElasticNet
model = ElasticNet()

param_grid={
    'alpha': np.arange(0, 10, 0.1),
    'l1_ratio': np.arange(0, 1, 0.1)
}

grid_search=GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    scoring='neg_mean_squared_error',
    cv=5
)

grid_search.fit(train_x_stack,train_y)

grid_search.best_params_
blender_model=grid_search.best_estimator_

pred_y_eln = best_model_eln.predict(test_x)
pred_y_rf = best_model_rf.predict(test_x)

test_x_stack=pd.DataFrame({
    'y1':pred_y_eln,
    'y2':pred_y_rf
})

pred_y=blender_model.predict(test_x_stack)

sub_df["SalePrice"] = pred_y

# csv 파일로 내보내기
sub_df.to_csv("./data/houseprice/sample_submission_rf_eln.csv", index=False)
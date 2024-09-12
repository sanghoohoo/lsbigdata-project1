# 필요한 패키지 불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

np.random.seed(20240911) 

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
    house_train[col].fillna("unknown", inplace=True)
house_train[qual_selected].isna().sum()


# test 데이터 채우기
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
    house_test[col].fillna("unknown", inplace=True)
house_test[qual_selected].isna().sum()


house_train.shape
house_test.shape
train_n=len(house_train)

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

# ## 이상치 탐색
# train_df=train_df.query("GrLivArea <= 4500")

## train
train_x=train_df.drop("SalePrice", axis=1)
train_y=train_df["SalePrice"]

## test
test_x=test_df.drop("SalePrice", axis=1)

# 표준화
from sklearn.preprocessing import StandardScaler
num_features = house_test.select_dtypes(include = [int, float]).columns

scaler = StandardScaler()
train_x[num_features] = scaler.fit_transform(train_x[num_features])
test_x[num_features] = scaler.transform(test_x[num_features])

# xg부스트 모델 생성
import xgboost as xgb
from sklearn.model_selection import GridSearchCV

xgb_model = xgb.XGBRegressor(random_state=20240911)

param_grid = {
    'n_estimators': [100, 200],
    'learning_rate': [0.05, 0.1, 0.2],
    'max_depth': [3, 4, 5]
}

grid_search = GridSearchCV(
    estimator=xgb_model,
    param_grid=param_grid,
    scoring='neg_mean_squared_error',
    cv=5
)

grid_search.fit(train_x, train_y)

best_params = grid_search.best_params_
best_xgb_model = grid_search.best_estimator_

# rf 모델 생성
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(random_state=20240911, n_estimators=100, max_features=None)

param_grid={
    'max_depth': [25],
    'min_samples_split': [3]
}

grid_search=GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    scoring='neg_mean_squared_error',
    cv=5
)

grid_search.fit(train_x,train_y)
grid_search.best_params_
best_rf_model=grid_search.best_estimator_

# 신경망 모델
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
nn_model = Sequential()
nn_model.add(Dense(128, input_dim=train_x.shape[1], activation='relu'))
nn_model.add(Dense(64, activation='relu'))
nn_model.add(Dense(32, activation='relu'))
nn_model.add(Dense(1))

nn_model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

history = nn_model.fit(train_x, train_y, epochs=200, batch_size=32, validation_split=0.1, verbose=1)


# 서포트 벡터 머신
from sklearn.svm import SVR
svr_model = SVR(kernel='rbf')
svr_model.fit(train_x, train_y)

# Lasso 모델
from sklearn.linear_model import Lasso
lasso_model = Lasso(alpha=119.9)
lasso_model.fit(train_x, train_y)

# 스택킹
y1_hat = best_xgb_model.predict(train_x)
y2_hat = best_rf_model.predict(train_x)
y3_hat = nn_model.predict(train_x).flatten()
y4_hat = svr_model.predict(train_x)
y5_hat = lasso_model.predict(train_x)

train_x_stack = pd.DataFrame({
    'y1': y1_hat,
    'y2': y2_hat,
    'y3': y3_hat,
    'y4': y4_hat,
    'y5': y5_hat
})

pred_y_xgb = best_xgb_model.predict(test_x)
pred_y_rf = best_rf_model.predict(test_x)
pred_y_nn = nn_model.predict(test_x).flatten()
pred_y_svr = svr_model.predict(test_x)
pred_y_lasso = lasso_model.predict(test_x)

test_x_stack = pd.DataFrame({
    'y1': pred_y_xgb,
    'y2': pred_y_rf,
    'y3': pred_y_nn,
    'y4': pred_y_svr,
    'y5': pred_y_lasso
})

# 블렌더
from sklearn.ensemble import GradientBoostingRegressor
blender_gbr = GradientBoostingRegressor(
    n_estimators=100, learning_rate=0.1, max_depth=3, random_state=20240911
)
blender_gbr.fit(train_x_stack, train_y)

# 최종 예측
pred_y = blender_gbr.predict(test_x_stack)

# SalePrice 바꿔치기
sub_df["SalePrice"] = pred_y
sub_df

# # csv 파일로 내보내기
sub_df.to_csv("./data/houseprice/sample_submission_stack6.csv", index=False)

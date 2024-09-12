# 필요한 패키지 불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

np.random.seed(20240911) 

# 데이터 불러오기
house_train = pd.read_csv("./data/houseprice/train.csv")
house_test = pd.read_csv("./data/houseprice/test.csv")
sub_df = pd.read_csv("./data/houseprice/sample_submission.csv")

# NaN 채우기
quantitative = house_train.select_dtypes(include=[int, float])
quantitative.isna().sum()
quant_selected = quantitative.columns[quantitative.isna().sum() > 0]

for col in quant_selected:
    house_train[col].fillna(house_train[col].mean(), inplace=True)
house_train[quant_selected].isna().sum()

qualitative = house_train.select_dtypes(include=[object])
qualitative.isna().sum()
qual_selected = qualitative.columns[qualitative.isna().sum() > 0]

for col in qual_selected:
    house_train[col].fillna("unknown", inplace=True)
house_train[qual_selected].isna().sum()

# test 데이터 채우기
quantitative = house_test.select_dtypes(include=[int, float])
quantitative.isna().sum()
quant_selected = quantitative.columns[quantitative.isna().sum() > 0]

for col in quant_selected:
    house_test[col].fillna(house_train[col].mean(), inplace=True)
house_test[quant_selected].isna().sum()

qualitative = house_test.select_dtypes(include=[object])
qualitative.isna().sum()
qual_selected = qualitative.columns[qualitative.isna().sum() > 0]

for col in qual_selected:
    house_test[col].fillna("unknown", inplace=True)
house_test[qual_selected].isna().sum()

# 통합 df 만들기 + 더미코딩
df = pd.concat([house_train, house_test], ignore_index=True)
df = pd.get_dummies(df, columns=df.select_dtypes(include=[object]).columns, drop_first=True)

# train / test 데이터셋
train_n = len(house_train)
train_df = df.iloc[:train_n,]
test_df = df.iloc[train_n:,]

# 이상치 탐색
train_df = train_df.query("GrLivArea <= 4500")

# train
train_x = train_df.drop("SalePrice", axis=1)
train_y = train_df["SalePrice"]

# test
test_x = test_df.drop("SalePrice", axis=1)

# 표준화
num_features = house_test.select_dtypes(include = [int, float]).columns

scaler = StandardScaler()
train_x[num_features] = scaler.fit_transform(train_x[num_features])
test_x[num_features] = scaler.transform(test_x[num_features])

# 신경망 모델 정의
model = Sequential()
model.add(Dense(128, input_dim=train_x.shape[1], activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))

# 모델 컴파일
model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

# 모델 학습
history = model.fit(train_x, train_y, epochs=200, batch_size=32, validation_split=0.1, verbose=1)

# 학습 과정 시각화
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='validation loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

# 예측
pred_y = model.predict(test_x).flatten()

# SalePrice 바꿔치기
sub_df["SalePrice"] = pred_y
sub_df

# csv 파일로 내보내기
sub_df.to_csv("./data/houseprice/sample_submission_nn.csv", index=False)

import optuna
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

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

## train
train_x=train_df.drop("SalePrice", axis=1)
train_y=train_df["SalePrice"]

## test
test_x=test_df.drop("SalePrice", axis=1)

# Optuna 최적화 함수 정의
def objective(trial):
    # 하이퍼파라미터 샘플링
    encoding_dim = trial.suggest_int('encoding_dim', 32, 128)
    epochs = trial.suggest_int('epochs', 10, 100)
    batch_size = trial.suggest_int('batch_size', 16, 128)
    alpha = trial.suggest_loguniform('alpha', 1e-4, 1e2)

    # 오토인코더 모델 정의
    input_dim = train_x.shape[1]
    input_layer = Input(shape=(input_dim,))
    encoded = Dense(encoding_dim, activation='relu')(input_layer)
    decoded = Dense(input_dim, activation='sigmoid')(encoded)
    autoencoder = Model(inputs=input_layer, outputs=decoded)

    # 오토인코더 컴파일
    autoencoder.compile(optimizer='adam', loss='mean_squared_error')

    # 오토인코더 학습
    autoencoder.fit(train_x, train_x, epochs=epochs, batch_size=batch_size, shuffle=True, validation_split=0.2, verbose=0)

    # 인코더 모델 생성
    encoder = Model(inputs=input_layer, outputs=encoded)
    train_x_encoded = encoder.predict(train_x)

    # Lasso 모델 학습
    from sklearn.linear_model import Lasso
    lasso_model = Lasso(alpha=alpha)
    lasso_model.fit(train_x_encoded, train_y)

    # 성능 평가 (RMSE)
    pred_y = lasso_model.predict(train_x_encoded)
    from sklearn.metrics import mean_squared_error
    rmse = np.sqrt(mean_squared_error(train_y, pred_y))
    
    return rmse

# Optuna 스터디 생성 및 최적화 수행
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=50)

# 최적의 하이퍼파라미터 확인
best_trial = study.best_trial
print('Best trial RMSE:', best_trial.value)
print('Best trial parameters:', best_trial.params)

# 최적 하이퍼파라미터로 최종 모델 학습
encoding_dim = best_trial.params['encoding_dim']
epochs = best_trial.params['epochs']
batch_size = best_trial.params['batch_size']
alpha = best_trial.params['alpha']

# 오토인코더 모델 재학습
input_dim = train_x.shape[1]
input_layer = Input(shape=(input_dim,))
encoded = Dense(encoding_dim, activation='relu')(input_layer)
decoded = Dense(input_dim, activation='sigmoid')(encoded)
autoencoder = Model(inputs=input_layer, outputs=decoded)
autoencoder.compile(optimizer='adam', loss='mean_squared_error')
autoencoder.fit(train_x, train_x, epochs=epochs, batch_size=batch_size, shuffle=True, validation_split=0.2, verbose=0)

# 인코더 모델 생성
encoder = Model(inputs=input_layer, outputs=encoded)
train_x_encoded = encoder.predict(train_x)
test_x_encoded = encoder.predict(test_x)

# Lasso 모델 재학습
from sklearn.linear_model import Lasso
lasso_model = Lasso(alpha=alpha)
lasso_model.fit(train_x_encoded, train_y)

# 최종 예측
pred_y = lasso_model.predict(test_x_encoded)

# 결과 저장
sub_df["SalePrice"] = pred_y
sub_df.to_csv("./data/houseprice/sample_submission_autoencoder_optuna.csv", index=False)

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import mean_squared_error, confusion_matrix, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
import optuna

np.random.seed(20240911)

## 필요한 데이터 불러오기
df = pd.read_csv("./data/week1.csv")

df.info()
df.isna().sum()

df_good = df.iloc[:470000,]
df_bad = df.iloc[470000:,]

# 피처와 라벨 분리 (Y를 제외한 모든 컬럼을 피처로 사용)
X_good = df_good.drop(columns=['Y']).values
X_bad = df_bad.drop(columns=['Y']).values

# 데이터 정규화
scaler = StandardScaler()
X_good_scaled = scaler.fit_transform(X_good)

# Optuna 목적 함수 정의
def objective(trial):
    input_dim = X_good.shape[1]
    
    # 하이퍼파라미터 설정
    encoding_dim = trial.suggest_int('encoding_dim', 16, 64)  # 잠재 공간 차원
    epochs = trial.suggest_int('epochs', 10, 100)  # 에포크 수
    batch_size = trial.suggest_int('batch_size', 32, 512)  # 배치 크기

    # 오토인코더 모델 구축
    autoencoder = Sequential()
    autoencoder.add(Dense(64, activation='relu', input_shape=(input_dim,)))
    autoencoder.add(Dense(encoding_dim, activation='relu'))
    autoencoder.add(Dense(64, activation='relu'))
    autoencoder.add(Dense(input_dim, activation='sigmoid'))  # 출력층

    # 모델 컴파일
    autoencoder.compile(optimizer='adam', loss='mean_squared_error')

    # 모델 학습
    autoencoder.fit(X_good_scaled, X_good_scaled, 
                    epochs=epochs, 
                    batch_size=batch_size, 
                    shuffle=True, 
                    validation_split=0.2, 
                    verbose=0)  # verbose=0으로 설정하여 출력을 생략

    # 재구성 오류 계산
    X_good_reconstructed = autoencoder.predict(X_good_scaled)
    mse_good = np.mean(np.power(X_good_scaled - X_good_reconstructed, 2), axis=1)

    # MSE 임계값 설정
    threshold = np.mean(mse_good) + 3 * np.std(mse_good)

    # 이상치 탐지
    outliers_good = mse_good > threshold
    
    # F1 스코어를 사용하여 성능 평가
    y_true = np.zeros(len(X_good))  # 모든 데이터는 정상
    y_pred = outliers_good.astype(int)  # 예측 결과

    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    return f1  # F1 스코어를 반환

# Optuna 최적화
study = optuna.create_study(direction='maximize')  # F1 스코어 최대화를 목표로 설정
study.optimize(objective, n_trials=50)  # 50회의 실험

# 최적의 하이퍼파라미터 출력
print("Best hyperparameters:", study.best_params)
print("Best F1 score:", study.best_value)

# F1 Score 및 Confusion Matrix 확인
best_params = study.best_params

# 최적 하이퍼파라미터로 모델 재훈련
input_dim = X_good.shape[1]
autoencoder = Sequential()
autoencoder.add(Dense(64, activation='relu', input_shape=(input_dim,)))
autoencoder.add(Dense(best_params['encoding_dim'], activation='relu'))
autoencoder.add(Dense(64, activation='relu'))
autoencoder.add(Dense(input_dim, activation='sigmoid'))  # 출력층

# 모델 컴파일 및 학습
autoencoder.compile(optimizer='adam', loss='mean_squared_error')
autoencoder.fit(X_good_scaled, X_good_scaled, 
                epochs=best_params['epochs'], 
                batch_size=best_params['batch_size'], 
                shuffle=True, 
                validation_split=0.2, 
                verbose=0)

# 불량 데이터에 대한 재구성 오류 계산
X_bad_scaled = scaler.transform(X_bad)  # 불량 데이터 정규화
X_bad_reconstructed = autoencoder.predict(X_bad_scaled)

# 불량 데이터의 재구성 오류 계산
mse_bad = np.mean(np.power(X_bad_scaled - X_bad_reconstructed, 2), axis=1)

# MSE 임계값 설정
threshold = np.mean(mse_good) + 3 * np.std(mse_good)

# 이상치 탐지
outliers_bad = mse_bad > threshold
y_true_bad = np.ones(len(X_bad))  # 모든 불량 데이터는 1
y_pred_bad = outliers_bad.astype(int)  # 예측 결과

# 혼동 행렬
cm_bad = confusion_matrix(y_true_bad, y_pred_bad)
print("Confusion Matrix for Bad Data:\n", cm_bad)

# 정밀도, 재현율, F1 Score 계산
precision_bad = precision_score(y_true_bad, y_pred_bad)
recall_bad = recall_score(y_true_bad, y_pred_bad)
f1_bad = f1_score(y_true_bad, y_pred_bad)

print("Precision for Bad Data:", precision_bad)
print("Recall for Bad Data:", recall_bad)
print("F1 Score for Bad Data:", f1_bad)

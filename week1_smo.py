import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

np.random.seed(20240911)

# 필요한 데이터 불러오기
df = pd.read_csv("./data/week1.csv")

df.info()
df.isna().sum()


470000/527000
df_good = df.iloc[:470000, ]
df_bad = df.iloc[470000:, ]

# 피처와 라벨 분리 (Y를 제외한 모든 컬럼을 피처로 사용)
X_good = df_good.drop(columns=['Y']).values
X_bad = df_bad.drop(columns=['Y']).values

# 데이터 정규화
scaler = StandardScaler()
X_good_scaled = scaler.fit_transform(X_good)
X_bad_scaled = scaler.transform(X_bad)  # 불량 데이터 정규화

# 레이블 생성 (정상 클래스: 0, 불량 클래스: 1)
y_good = np.zeros(len(X_good_scaled))  # 정상 데이터 레이블
y_bad = np.ones(len(X_bad_scaled))      # 불량 데이터 레이블

# SMOTE를 정상 데이터에 적용하기
X_resampled, y_resampled = SMOTE(sampling_strategy='auto', random_state=42).fit_resample(X_good_scaled, y_good)

# 불량 데이터와 재샘플링된 정상 데이터를 결합
X_combined = np.vstack((X_resampled, X_bad_scaled))
y_combined = np.hstack((y_resampled, y_bad))

# 하이퍼파라미터 설정
encoding_dim = 32  # 잠재 공간 차원
epochs = 50  # 에포크 수
batch_size = 256  # 배치 크기

# 오토인코더 모델 구축
input_dim = X_combined.shape[1]  # 입력 차원
autoencoder = Sequential()
autoencoder.add(Dense(64, activation='relu', input_shape=(input_dim,)))
autoencoder.add(Dense(encoding_dim, activation='relu'))
autoencoder.add(Dense(64, activation='relu'))
autoencoder.add(Dense(input_dim, activation='sigmoid'))  # 출력층

# 모델 컴파일
autoencoder.compile(optimizer='adam', loss='mean_squared_error')

# 모델 학습
autoencoder.fit(X_combined, X_combined,
                epochs=epochs,
                batch_size=batch_size,
                shuffle=True,
                validation_split=0.2,
                verbose=1)  # verbose=1로 설정하여 출력을 확인

# 재구성 오류 계산
X_combined_reconstructed = autoencoder.predict(X_combined)

# 재구성 오류 계산
mse_combined = np.mean(np.power(X_combined - X_combined_reconstructed, 2), axis=1)

# MSE 임계값 설정
threshold = np.mean(mse_combined) + 3 * np.std(mse_combined)

# 이상치 탐지
outliers_combined = mse_combined > threshold

# 혼동 행렬 및 평가
y_pred = outliers_combined.astype(int)  # 예측 결과
cm = confusion_matrix(y_combined, y_pred)
print("Confusion Matrix:\n", cm)

# 정밀도, 재현율, F1 Score
precision = precision_score(y_combined, y_pred)
recall = recall_score(y_combined, y_pred)
f1 = f1_score(y_combined, y_pred)

print("Precision:", precision)
print("Recall:", recall)
print(" :", f1)

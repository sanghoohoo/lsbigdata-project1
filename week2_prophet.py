import pandas as pd
from prophet import Prophet
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

# 데이터 불러오기 및 전처리
df = pd.read_csv("data/data_week2.csv", encoding='cp949')
df = df.rename(columns={'num': '건물번호', 'date_time': '날짜', '전력사용량(kWh)': '전력사용량', 
                        '기온(°C)': '기온', '풍속(m/s)': '풍속', '습도(%)': '습도', 
                        '강수량(mm)': '강수량', '일조(hr)': '일조'})
df['날짜'] = pd.to_datetime(df['날짜'])

# 파생변수 추가
df['시간_sin'] = np.sin(2 * np.pi * df['날짜'].dt.hour / 24)
df['시간_cos'] = np.cos(2 * np.pi * df['날짜'].dt.hour / 24)

# Prophet에 맞게 데이터 준비
df_prophet = df[['날짜', '전력사용량', '기온', '풍속', '습도', '강수량', '일조', '시간_sin', '시간_cos']]
df_prophet = df_prophet.rename(columns={'날짜': 'ds', '전력사용량': 'y'})

# 학습 데이터와 예측할 마지막 이틀 데이터 구분
last_2days_df = df_prophet[df_prophet['ds'] >= (df_prophet['ds'].max() - pd.Timedelta(days=2))]
train_df = df_prophet[df_prophet['ds'] < last_2days_df['ds'].min()]

# Prophet 모델 초기화
model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=True, stan_backend='CMDSTANPY')

# 외부 변수 추가
for col in ['기온', '풍속', '습도', '강수량', '일조', '시간_sin', '시간_cos']:
    model.add_regressor(col)

# 모델 학습
model.fit(train_df)

# 마지막 이틀 예측할 데이터프레임 생성
future = last_2days_df[['ds', '기온', '풍속', '습도', '강수량', '일조', '시간_sin', '시간_cos']]

# 예측 수행
forecast = model.predict(future)

# 급증 기준 설정 (예: 과거 중앙값 대비 30% 증가)
train_df['중앙값'] = train_df['y'].rolling(window=24*7, min_periods=1).median()
median_last = train_df['중앙값'].iloc[-1]
forecast['급증_예측'] = (forecast['yhat'] > median_last * 1.3).astype(int)

# 실제 값과 예측 값 비교
actual = last_2days_df['y'].values
predicted = forecast['급증_예측'].values

# 평가 지표 계산
print("Confusion Matrix:\n", confusion_matrix(actual > median_last * 1.3, predicted))
print("\nClassification Report:\n", classification_report(actual > median_last * 1.3, predicted))

# 예측 결과 시각화
plt.figure(figsize=(10, 6))
plt.plot(train_df['ds'], train_df['y'], label='실제 전력사용량')
plt.plot(forecast['ds'], forecast['yhat'], label='예측 전력사용량')
plt.scatter(forecast.loc[forecast['급증_예측'] == 1, 'ds'], 
            forecast.loc[forecast['급증_예측'] == 1, 'yhat'], 
            color='red', label='급증 예측', marker='x')
plt.xlabel('날짜')
plt.ylabel('전력 사용량 (kWh)')
plt.legend()
plt.title('전력 사용량 예측 및 급증 여부')
plt.show()


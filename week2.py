import numpy as np
import pandas as pd

np.random.seed(42)

## 필요한 데이터 불러오기
df = pd.read_csv("./data/data_week2.csv", encoding='cp949')
df
df.describe()
df.info()
df = df.rename(columns = {'num' : '건물번호', 'date_time' : '날짜' , '전력사용량(kWh)' : '전력사용량' , '기온(°C)':'기온', '풍속(m/s)' :'풍속'  , '습도(%)':'습도' , '강수량(mm)':'강수량', '일조(hr)' : '일조'  })

df_1 = group1 = df[(df['비전기냉방설비운영']==1) & (df['태양광보유']==1)]
df_1

df_1 = df_1.groupby('날짜').agg({'전력사용량': 'mean'}).reset_index()
plt.plot(df_1['날짜'], df_1['전력사용량'],  label='전력사용량')

# 전력사용량 그래프
df = df.groupby('날짜').agg({'전력사용량': 'mean'}).reset_index()
import matplotlib.pyplot as plt
df['날짜']=pd.to_datetime(df['날짜'])
plt.plot(df['날짜'], df['전력사용량'],  label='전력사용량')

df1 = df[df['건물번호']==1]
df2 = df[df['건물번호']==2]
df.columns

plt.figure(figsize=(20,18))
# plt.plot(df1['날짜'], df1['전력사용량'],  label='전력사용량')


plt.plot(df['전력사용량(kWh)'],  label='전력사용량(kWh)')


# # 7시간 이동평균
# df['7_hr_SMA'] = df['전력사용량(kWh)'].rolling(window=300).mean()
# df
# plt.plot(df['7_hr_SMA'], label='7_hr_SMA')

df['전력사용량(kWh)'].mean()

# 변화량
df['hourly_diff'] = df['전력사용량(kWh)'].diff()
plt.plot(df['hourly_diff'], label='hourly_diff')
df['hourly_diff'].describe()

# 변화량 퍼센트로
df['hourly_diff_percent'] = (df['hourly_diff'] / df['전력사용량(kWh)'].shift(1)) * 100
plt.plot(df['hourly_diff_percent'], label='hourly_diff_percent')

df['hourly_diff_percent'].describe()

## 급증 조건
# # 임의로 지정
# threshold_rate = 20  # 예시: 변화율 20% 이상
# threshold_value = 100  # 예시: 절대값 100kWh 이상

# # 급증 상황 판별
# df['is_surge'] = ((df['hourly_diff_percent'] > threshold_rate) & 
#                   (df['전력사용량(kWh)'].abs() > threshold_value))


# Z-score 사용
df['z_scores'] = (df['전력사용량(kWh)'] - df['전력사용량(kWh)'].mean()) / np.std(df['전력사용량(kWh)'])
plt.plot(df['z_scores'], label='z_scores')

# Z-score 기준 설정 (예: 2)
threshold_z_score = 2
threshold_rate = 30

df['is_surge'] = ((df['hourly_diff_percent'] > threshold_rate) & 
                  (df['z_scores'] > threshold_z_score))

(df['z_scores'] > threshold_z_score).value_counts()
df['is_surge'].value_counts()

# 그래프 그리기
plt.figure(figsize=(14, 7))
plt.plot(df['전력사용량(kWh)'], label='전력 사용량 (kWh)', color='blue')

# 급증 상황 표시
plt.scatter(df.index[df['is_surge']], df['전력사용량(kWh)'][df['is_surge']], 
            color='red', label='급증 상황', marker='o', s=100)



#def plot_gain_chart(y_true, y_scores):
#     # 예측 확률에 따라 데이터 정렬
#     data = pd.DataFrame({'y_true': y_true, 'y_scores': y_scores})
#     data = data.sort_values(by='y_scores', ascending=False).reset_index(drop=True)

#     # 누적 true positive 비율 계산
#     data['cumulative_gain'] = data['y_true'].cumsum() / data['y_true'].sum()
#     data['cumulative_percentage'] = (data.index + 1) / len(data)

#     # Gain Chart 그리기
#     plt.figure(figsize=(10, 6))
#     plt.plot(data['cumulative_percentage'], data['cumulative_gain'], label="Model Gain", color="blue")
#     plt.plot([0, 1], [0, 1], label="Random Model", linestyle="--", color="gray")
#     plt.xlabel("Percentage of Sample")
#     plt.ylabel("Cumulative Gain")
#     plt.title("Gain Chart")
#     plt.legend()
#     plt.grid(True)
#     plt.show()

# # 함수 호출
# plot_gain_chart(y_true, y_scores)

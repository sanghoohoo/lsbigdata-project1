import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from xgboost import XGBClassifier
from sklearn.metrics import f1_score, confusion_matrix
from tslearn.clustering import TimeSeriesKMeans
from tslearn.preprocessing import TimeSeriesScalerMeanVariance

np.random.seed(42)

## 필요한 데이터 불러오기
df = pd.read_csv("./data/data_week2.csv", encoding='cp949')

# 컬럼명 바꾸기
df = df.rename(columns = {'num' : '건물번호', 'date_time' : '날짜' , '전력사용량(kWh)' : '전력사용량' , '기온(°C)':'기온', '풍속(m/s)' :'풍속'  , '습도(%)':'습도' , '강수량(mm)':'강수량', '일조(hr)' : '일조'  })
len(df.query("전력사용량==0"))

# 데이터 자료형 바꾸기
df['날짜'] = pd.to_datetime(df['날짜'])
df['비전기냉방설비운영'] = df['비전기냉방설비운영'].astype('boolean')
df['태양광보유'] = df['태양광보유'].astype('boolean')

# 인코딩
df['년'] = df['날짜'].dt.year
df['월'] = df['날짜'].dt.month
df['일'] = df['날짜'].dt.day
df['요일'] = df['날짜'].dt.dayofweek  # 0: 월요일, 6: 일요일
df['시'] = df['날짜'].dt.hour
df['시간_sin'] = np.sin(2 * np.pi * df['시'] / 24)
df['시간_cos'] = np.cos(2 * np.pi * df['시'] / 24)
df.drop('시', axis=1, inplace=True)  # '시' 칼럼 제거
# df['주말'] = df['요일'].apply(lambda x: 1 if x >= 5 else 0)  # 주말: 1, 평일: 0

# 3개 행씩 묶어 평균 계산
df_avg = df.groupby(df.index // 3).mean(numeric_only=True)
df_avg['날짜'] = df.groupby(df.index // 3)['날짜'].first().values

# 군집화
buildings = df_avg['건물번호'].unique()
series_data = [df_avg[df_avg['건물번호'] == bld]['전력사용량'].values for bld in buildings]

scaler = TimeSeriesScalerMeanVariance()
series_data_scaled = scaler.fit_transform(series_data)

n_clusters = 5  # 원하는 군집 수 지정
dtw_kmeans = TimeSeriesKMeans(n_clusters=n_clusters, metric="dtw", random_state=42)
labels = dtw_kmeans.fit_predict(series_data_scaled)

result_df = pd.DataFrame({'건물번호': buildings, '군집': labels})
df_avg = df_avg.merge(result_df[['건물번호', '군집']], on='건물번호', how='left')

# 군집화 결과 시각화
for cluster_num in range(n_clusters):
    plt.figure(figsize=(10, 6))
    plt.title(f'Cluster {cluster_num} 전력사용량 패턴')
    for i, building in enumerate(buildings):
        if labels[i] == cluster_num:
            plt.plot(series_data[i], label=f'건물 {building}')
    plt.xlabel('시간')
    plt.ylabel('전력사용량')
    plt.legend(loc='upper right')
    plt.show()


# 군집 번호에 따른 데이터 반환 함수
def cluster(cluster_label):
    # 지정된 군집 번호로 필터링
    df_cluster = df_avg.query(f'군집 == {cluster_label}')

    # 이전 4개의 동일 요일, 시간대 전력 사용량의 중앙값을 구해 새로운 열에 추가
    median_series = (
        df_cluster.groupby(['건물번호','요일', '시간_sin'])['전력사용량'] # 건물번호 추가?
        .apply(lambda x: x.shift().rolling(window=4, min_periods=1).median())
    )

    median_df = pd.DataFrame({'index' : median_series.index.get_level_values(3),
                               '전력중앙값' : median_series.values})

    df_cluster = pd.merge(df_cluster, median_df, how='left', left_index=True, right_on='index')
    df_cluster.set_index('index', inplace=True)

    # 변화율 계산하여 새로운 칼럼 추가
    df_cluster['변화율'] = ((df_cluster['전력사용량'] - df_cluster['전력중앙값']) / df_cluster['전력중앙값']) * 100

    df_cluster = df_cluster.dropna()

    # 급증 기준: 동일 요일 동 시간대 4개의 중앙값 대비 증가율 30% 초과
    df_cluster['급증'] = df_cluster['변화율'] > 30

    # 전역 변수로 할당 (원하는 경우)
    globals()[f'df_{cluster_label}'] = df_cluster

# 군집별 급증 갯수와 건물 수 계산
surge = []
for i in range(5):
    cluster(i)
    df_n = globals()[f'df_{i}']
    surge_count = df_n['급증'].sum()
    building_count = df_avg.query(f'군집 == {i}')['건물번호'].nunique()  # 해당 군집의 건물 수 계산
    surge.append({'군집': i, '급증갯수': surge_count, '건물갯수': building_count, '비율': surge_count / building_count if building_count > 0 else 0})

# 결과를 데이터프레임으로 변환
surge_df = pd.DataFrame(surge)
surge_df.sort_values(by='급증갯수', ascending=False, inplace=True)
surge_df

# 결과를 데이터프레임으로 변환
surge_df = pd.DataFrame(surge)
surge_df.sort_values(by='급증갯수',ascending=False)

# 모델
def train_and_evaluate_xgb(df):
    # 데이터 전처리: 학습에 필요 없는 컬럼 제거
    df = df.drop(['군집', '전력사용량', '비전기냉방설비운영', '태양광보유', '년', '날짜', '전력중앙값', '변화율'], axis=1)

    # 학습 및 테스트 데이터셋 분할
    test_df = df[(df['월'] == 8) & (df['일'] >= 17)]
    train_df = df.drop(test_df.index)


    train_x = train_df.drop('급증', axis=1)
    train_y = train_df['급증']
    test_x = test_df.drop('급증', axis=1)
    test_y = test_df['급증']

    # 모델 생성 및 학습
    scale_pos_weight = 7488 / 343
    xgb_clf = XGBClassifier(scale_pos_weight=scale_pos_weight, random_state=42)
    xgb_clf.fit(train_x, train_y)

    # 예측
    pred_y = xgb_clf.predict(test_x)

    # 성능 평가
    f1 = f1_score(test_y, pred_y)
    cm = confusion_matrix(test_y, pred_y)

    print("Confusion Matrix:\n", cm)

train_and_evaluate_xgb(df_0)
train_and_evaluate_xgb(df_1)
train_and_evaluate_xgb(df_2)
train_and_evaluate_xgb(df_3)





df_3[(df['월'] == 8) & (df['일'] == 23)]['급증'].sum()

# 데이터 전처리: 학습에 필요 없는 컬럼 제거
df = df_3.drop(['군집', '전력사용량', '비전기냉방설비운영', '태양광보유', '년', '날짜', '전력중앙값', '변화율'], axis=1)

# 학습 및 테스트 데이터셋 분할
test_df = df[(df['월'] == 8) & (df['일'] >= 19)]
train_df = df.drop(test_df.index)
# train_df = df[(df['월'] < 8) | ((df['월'] == 8) & (df['일'] < 21))]

train_x = train_df.drop('급증', axis=1)
train_y = train_df['급증']
test_x = test_df.drop('급증', axis=1)
test_y = test_df['급증']

# 모델 생성 및 학습
scale_pos_weight = 7488 / 343
xgb_clf = XGBClassifier(scale_pos_weight=scale_pos_weight, random_state=42)
xgb_clf.fit(train_x, train_y)

# 예측
pred_y = xgb_clf.predict(test_x)

# 성능 평가
f1 = f1_score(test_y, pred_y)
cm = confusion_matrix(test_y, pred_y)

print("Confusion Matrix:\n", cm)


df[(df['월'] == 8) & (df['일'] == 21)]['급증'].sum()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from xgboost import XGBClassifier
from sklearn.metrics import f1_score, confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import GridSearchCV
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

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
df['주말'] = df['요일'].apply(lambda x: 1 if x >= 5 else 0)  # 주말: 1, 평일: 0

# 3개 행씩 묶어 평균 계산
df_avg = df.groupby(df.index // 3).mean(numeric_only=True)
df_avg['날짜'] = df.groupby(df.index // 3)['날짜'].first().values
    
# 건물 번호에 따른 데이터 반환 함수
def building(n):
    # 지정된 건물 번호로 필터링
    df_n = df_avg.query(f'건물번호 == {n}')

    # 이전 4개의 동일 요일, 시간대 전력 사용량의 중앙값을 구해 새로운 열에 추가
    median_series = (
        df_n.groupby(['요일', '시간_sin'])['전력사용량']
        .apply(lambda x: x.shift().rolling(window=4, min_periods=1).median())
    )

    median_df = pd.DataFrame({'index' : median_series.index.get_level_values(2),
                        '전력중앙값' : median_series.values})

    df_n = pd.merge(df_n, median_df, how='left', left_index=True, right_on='index')
    df_n.set_index('index', inplace=True)


    # 변화율 계산하여 새로운 칼럼 추가
    df_n['변화율'] = ((df_n['전력사용량'] - df_n['전력중앙값']) / df_n['전력중앙값']) * 100

    df_n = df_n.dropna()

    # # 정규화
    # transformed_variable, lambda_value = stats.boxcox(df_n['변화율'] + 1)
    # df_n['변화율정규화'] = (transformed_variable-transformed_variable.mean())/transformed_variable.std()

    # 급증 기준: 동일 요일 동 시간대 4개의 중앙값 대비 증가율 30% 초과
    df_n['급증'] = df_n['변화율'] > 30

    # 전역 변수로 할당
    globals()[f'df_{n}'] = df_n

# 빌딩 1부터 60까지의 급증 갯수 계산
surge = []
for i in range(1, 61):
    building(i)
    df_n = globals()[f'df_{i}']
    surge_count = df_n['급증'].sum()
    surge.append({'건물번호': i, '급증갯수': surge_count})

# 결과를 데이터프레임으로 변환
surge_df = pd.DataFrame(surge)
surge_df.sort_values(by='급증갯수',ascending=False)

df_4['주말'].sum()

def train_and_evaluate_xgb(df):
    # 데이터 전처리: 학습에 필요 없는 컬럼 제거
    df = df.drop(['날짜','건물번호', '전력사용량', '비전기냉방설비운영', '태양광보유', '년', '날짜', '전력중앙값', '변화율'], axis=1)

    # 학습 및 테스트 데이터셋 분할
    test_df = df[(df['월'] == 8) & (df['일'] >= 17)]
    train_df = df.drop(test_df.index)

    train_x = train_df.drop('급증', axis=1)
    train_y = train_df['급증']
    test_x = test_df.drop('급증', axis=1)
    test_y = test_df['급증']

    # 모델 생성 및 학습
    scale_pos_weight = train_y.shape[0] / train_y.sum()
    xgb_clf = XGBClassifier(random_state=42)
    xgb_clf.fit(train_x, train_y)

    # 예측
    pred_y = xgb_clf.predict(test_x)

    # 성능 평가
    f1 = f1_score(test_y, pred_y)
    cm = confusion_matrix(test_y, pred_y)

    print("Confusion Matrix:\n", cm)

train_and_evaluate_xgb(df_4)
train_and_evaluate_xgb(df_30)
train_and_evaluate_xgb(df_19)
train_and_evaluate_xgb(df_59)


df_4[(df_4['월'] == 8) & (df_4['일'] >= 17)]['급증'].sum() # 건물 4 -> 12 급증
df_30[(df_30['월'] == 8) & (df_30['일'] >= 17)]['급증'].sum()  # 건물 30 -> 0 급증
df_19[(df_19['월'] == 8) & (df_19['일'] >= 17)]['급증'].sum() # 건물 19 -> 21 급증
df_59[(df_59['월'] == 8) & (df_59['일'] >= 17)]['급증'].sum()  # 건물 59 -> 7 급증

df_4['급증'].sum()


df_4 = df_4.drop(['날짜','건물번호', '전력사용량', '비전기냉방설비운영', '태양광보유', '년', '날짜', '전력중앙값', '변화율'], axis=1)

# 학습 및 테스트 데이터셋 분할
test_df_4 = df_4[(df_4['월'] == 8) & (df_4['일'] >= 17)]
train_df_4 = df_4.drop(test_df_4.index)

train_x = train_df_4.drop('급증', axis=1)
train_y = train_df_4['급증']
test_x = test_df_4.drop('급증', axis=1)
test_y = test_df_4['급증']

# 모델 생성 및 학습
scale_pos_weight = train_y.shape[0] / train_y.sum()
xgb_clf = XGBClassifier(random_state=42)
xgb_clf.fit(train_x, train_y)

prob_y = xgb_clf.predict_proba(test_x)[:, 1]  # 양성 클래스의 확률

# # 이득도표
# from sklearn.metrics import precision_recall_curve, roc_curve, f1_score
# precision, recall, thresholds_pr = precision_recall_curve(test_y, prob_y)
# fpr, tpr, thresholds_roc = roc_curve(test_y, prob_y)

# # F1 점수 계산
# f1_scores = [f1_score(test_y, prob_y >= thresh) for thresh in thresholds_pr]

# # 이득도표 그리기
# plt.figure(figsize=(12, 8))

# # Precision-Recall 커브
# plt.subplot(2, 2, 1)
# plt.plot(thresholds_pr, precision[:-1], label="Precision", color="b")
# plt.plot(thresholds_pr, recall[:-1], label="Recall", color="g")
# plt.xlabel("Threshold")
# plt.ylabel("Score")
# plt.title("Precision-Recall Curve")
# plt.legend()

# # F1 Score 커브
# plt.subplot(2, 2, 2)
# plt.plot(thresholds_pr, f1_scores, label="F1 Score", color="r")
# plt.xlabel("Threshold")
# plt.ylabel("F1 Score")
# plt.title("F1 Score vs. Threshold")

# # ROC 커브 (TPR, FPR)
# plt.subplot(2, 2, 3)
# plt.plot(fpr, tpr, label="ROC Curve", color="purple")
# plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
# plt.xlabel("False Positive Rate")
# plt.ylabel("True Positive Rate")
# plt.title("ROC Curve")
# plt.legend()

# # 이득도표
# gains = np.cumsum(tpr - fpr)
# plt.subplot(2, 2, 4)
# plt.plot(thresholds_roc, gains, label="Gain", color="brown")
# plt.xlabel("Threshold")
# plt.ylabel("Cumulative Gain")
# plt.title("Gain Chart")
# plt.legend()

# plt.tight_layout()
# plt.show()


# ROC 곡선 및 임계값, precision, recall 계산
from sklearn.metrics import f1_score, confusion_matrix, roc_curve, auc, precision_score, recall_score
thresholds = np.arange(0, 1.1, 0.01)
results = []

for threshold in thresholds:
    pred_y_threshold = (prob_y >= threshold).astype(int)  # 각 임계값에 따른 예측
    tn, fp, fn, tp = confusion_matrix(test_y, pred_y_threshold).ravel()

    precision = precision_score(test_y, pred_y_threshold)
    recall = recall_score(test_y, pred_y_threshold)

    results.append({
        'Threshold': threshold,
        'Predicted Positive N': tp,
        'Actual Positive N': tp + fn,
        'Precision': precision,
        'Recall': recall,
        'Cumulative Probability': prob_y[pred_y_threshold == 1].sum()
    })

# 결과 DataFrame 생성
results_df = pd.DataFrame(results)
results_df

# 임계값 선정
threshold = 0.01  # 원하는 임계값으로 설정
pred_y = (prob_y >= threshold).astype(int)
confusion_matrix(test_y, pred_y)
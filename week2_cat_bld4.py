import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import f1_score, confusion_matrix
from catboost import CatBoostClassifier
from sklearn.metrics import precision_recall_curve, roc_curve, f1_score, confusion_matrix, auc, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit

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

# 파생변수 추가
df['주말'] = df['요일'].apply(lambda x: 1 if x >= 5 else 0)  # 주말: 1, 평일: 0
df['기온_1시간전'] = df['기온'].shift(1)  # 1시간 전 기온
df['기온_24시간전'] = df['기온'].shift(24)  # 24시간 전 기온
df['기온_3시간평균'] = df['기온'].rolling(window=3).mean()  # 최근 3시간 평균
df['기온_24시간평균'] = df['기온'].rolling(window=24).mean()  # 최근 24시간 평균
df['풍속_24시간평균'] = df['풍속'].rolling(window=24).mean()  # 최근 24시간 평균
df['강수량_24시간평균'] = df['강수량'].rolling(window=24).mean()  # 최근 24시간 평균
df["체감온도"]=13.12 + 0.6215 *df["기온"] -11.37*(df["풍속"]**0.16) + 0.3965*df["기온"]*(df["풍속"]**0.16)
df["불쾌지수"]=0.81 *df["기온"]+ 0.01*df["습도"] *(0.99*df["기온"]-14.3)+46.3

# 건물 번호에 따른 데이터 반환 함수
def building(n):
    # 지정된 건물 번호로 필터링
    df_n = df.query(f'건물번호 == {n}')

    # 이전 4개의 동일 요일, 시간대 전력 사용량의 중앙값을 구해 새로운 열에 추가
    median_series = (
        df_n.groupby(['요일', '시'])['전력사용량']
        .apply(lambda x: x.shift().rolling(window=4, min_periods=1).median())
    )

    median_df = pd.DataFrame({'index' : median_series.index.get_level_values(2),
                        '전력중앙값' : median_series.values})

    df_n = pd.merge(df_n, median_df, how='left', left_index=True, right_on='index')
    df_n.set_index('index', inplace=True)


    # 변화율 계산하여 새로운 칼럼 추가
    df_n['변화율'] = ((df_n['전력사용량'] - df_n['전력중앙값']) / df_n['전력중앙값']) * 100

    df_n = df_n.dropna()

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
surge_df.sort_values(by='급증갯수',ascending=False).reset_index().drop('index',axis=1)

np.random.seed(42)

# df_59에서 급증 갯수가 3개 이상인 날짜 필터링
# df_true_counts = df_59[df_59['급증']].groupby(df_59['날짜'].dt.date).size()
# days_with_three_or_more_true = df_true_counts[df_true_counts >= 3]

# 데이터 전처리: 학습에 필요 없는 컬럼 제거
## df_1 ~ df_60 선택
df = df_59.drop(['날짜', '시', '일조', '건물번호', '전력사용량', '비전기냉방설비운영', '태양광보유', '년', '날짜', '전력중앙값', '변화율'], axis=1)
# 학습 및 테스트 데이터셋 분할
# 6, 7일
# test_df = df[(df['월'] == 8) & ((df['일'] == 6)|(df['일'] == 7))]
# train_df = df[(df['월'] < 8) | ((df['월'] == 8) & (df['일'] < 6))]

# 7, 8
# test_df = df[(df['월'] == 8) & ((df['일'] == 7)|(df['일'] == 8))]
# train_df = df[(df['월'] < 8) | ((df['월'] == 8) & (df['일'] < 7))]

# 18, 19일
# test_df = df[(df['월'] == 8) & ((df['일'] == 18)|(df['일'] == 19))]
# train_df = df[(df['월'] < 8) | ((df['월'] == 8) & (df['일'] < 18))]

# 19, 20일
test_df = df[(df['월'] == 8) & ((df['일'] == 19)|(df['일'] == 20))]
train_df = df[(df['월'] < 8) | ((df['월'] == 8) & (df['일'] < 19))]

# 20, 21일
# test_df = df[(df['월'] == 8) & ((df['일'] == 20)|(df['일'] == 21))]
# train_df = df[(df['월'] < 8) | ((df['월'] == 8) & (df['일'] < 20))]

# 22, 23일
# test_df = df[(df['월'] == 8) & ((df['일'] == 22)|(df['일'] == 23))]
# train_df = df[(df['월'] < 8) | ((df['월'] == 8) & (df['일'] < 22))]

# 23, 24일
# test_df = df[(df['월'] == 8) & (df['일'] >= 23)]
# train_df = df.drop(test_df.index)

# 특징 변수와 타겟 변수 분리
X_train = train_df.drop('급증', axis=1).values
y_train = train_df['급증'].values
X_test = test_df.drop('급증', axis=1).values
y_test = test_df['급증'].values

# 그리드서치
# TimeSeriesSplit 객체 생성
tscv = TimeSeriesSplit(n_splits=5)
# Grid Search에 사용할 파라미터 범위 정의
param_grid = {
    'iterations': [1000,2000,3000,4000,5000]
}

scale_pos_weight = (len(y_test) - y_test.sum()) / y_test.sum()
catboost_clf = CatBoostClassifier(scale_pos_weight=scale_pos_weight, learning_rate=0.1, depth=6, eval_metric='AUC', random_seed=42, verbose=0)

grid_search = GridSearchCV(estimator=catboost_clf, param_grid=param_grid, 
                           scoring='roc_auc', cv=tscv, n_jobs=-1)

grid_search.fit(X_train, y_train)

grid_search.best_params_
catboost_clf = grid_search.best_estimator_

# 예측 및 평가
prob_y = catboost_clf.predict_proba(X_test)[:, 1]  # 양성 클래스의 확률

# 임계값 목록 생성
thresholds = np.arange(0, 1.1, 0.1)
results = []

roc_auc = roc_auc_score(y_test, prob_y)
for threshold in thresholds:
    pred_y_threshold = (prob_y >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, pred_y_threshold).ravel()
    
    precision = precision_score(y_test, pred_y_threshold)
    recall = recall_score(y_test, pred_y_threshold)
    f1 = f1_score(y_test, pred_y_threshold)  # F1 Score 계산
    fpr = fp / (fp + tn)
    
    # 결과 저장
    results.append({
        'Threshold': threshold,
        'Predicted Positive N': tp,
        'Actual Positive N': tp + fn,
        'Predicted Negative N': tn,
        'Actual Negative N': tn + fp,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1,
        'FPR': fpr,
        'ROC AUC': roc_auc 
    })

# 결과 DataFrame 생성
results_df = pd.DataFrame(results)
results_df
# =============================================================

# 임계값 선정
threshold = 0.3
pred_y = (prob_y >= threshold).astype(int)
confusion_matrix(y_test, pred_y)

pred_y

df_plot=df_59  #####

pred_df = pd.DataFrame({
    '날짜': df_plot[(df_plot['월'] == 8) & ((df_plot['일'] == 19)|(df_plot['일'] == 20))]['날짜'],
    '예측급증': pred_y,
    '실제급증': df_plot[(df_plot['월'] == 20) & ((df_plot['일'] == 19)|(df_plot['일'] == 20))]['급증']
})

## 그래프
import seaborn as sns


time_df = df_plot[(df_plot['월'] == 8) & ((df_plot['일'] == 19)|(df_plot['일'] == 20))]
highlight = pred_df['예측급증']
highlight2 = time_df['급증']
plt.figure(figsize=(10,7))
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
sns.lineplot(data=time_df , x='날짜', y='전력사용량', color='black')
#sns.scatterplot(data=time_df , x='날짜', y='전력사용량' ,color='black')
plt.fill_between(pred_df['날짜'], time_df['전력사용량'],where=highlight, color='red', alpha=0.5, label='급증 구간')
plt.fill_between(pred_df['날짜'], time_df['전력사용량'],where=highlight2, color='blue', alpha=0.5, label='급증 구간')
monthly_ticks = pd.date_range(start=pred_df['날짜'].min(), end=pred_df['날짜'].max(), freq='D')
# 날짜와 요일을 함께 표시
tick_labels = [f"{date.strftime('%Y-%m-%d')}\n{date.strftime('%a')}" for date in monthly_ticks]
plt.xticks(monthly_ticks, tick_labels)

##






# 이득도표
precision, recall, thresholds_pr = precision_recall_curve(y_test, prob_y)
fpr, tpr, thresholds_roc = roc_curve(y_test, prob_y)

# F1 점수 계산
f1_scores = [f1_score(y_test, prob_y >= thresh) for thresh in thresholds_pr]

# 이득도표 그리기
plt.figure(figsize=(12, 8))

# Precision-Recall 커브
plt.subplot(2, 2, 1)
plt.plot(thresholds_pr, precision[:-1], label="Precision", color="b")
plt.plot(thresholds_pr, recall[:-1], label="Recall", color="g")
plt.xlabel("Threshold")
plt.ylabel("Score")
plt.title("Precision-Recall Curve")
plt.legend()

# F1 Score 커브
plt.subplot(2, 2, 2)
plt.plot(thresholds_pr, f1_scores, label="F1 Score", color="r")
plt.xlabel("Threshold")
plt.ylabel("F1 Score")
plt.title("F1 Score vs. Threshold")

# ROC 커브 (TPR, FPR)
plt.subplot(2, 2, 3)
plt.plot(fpr, tpr, label="ROC Curve", color="purple")
plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()

# 이득도표
gains = np.cumsum(tpr - fpr)
plt.subplot(2, 2, 4)
plt.plot(thresholds_roc, gains, label="Gain", color="brown")
plt.xlabel("Threshold")
plt.ylabel("Cumulative Gain")
plt.title("Gain Chart")
plt.legend()

plt.tight_layout()
plt.show()


# 피처 중요도 가져오기
feature_importances = catboost_clf.get_feature_importance()

# 피처 이름
feature_names = train_df.drop('급증', axis=1).columns

# 변수 중요도 데이터프레임 생성
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': feature_importances
})

# 중요도 기준으로 내림차순 정렬
importance_df = importance_df.sort_values(by='Importance')

# 피처 중요도 시각화
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.figure(figsize=(10, 6))
plt.barh(importance_df['Feature'], importance_df['Importance'])
plt.xlabel('Importance')
plt.title('Feature Importance')
plt.show()

# 정렬된 변수 중요도 데이터프레임 출력
importance_df

importance_df['Feature'].values.shape
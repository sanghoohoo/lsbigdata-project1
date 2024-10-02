import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from sklearn.metrics import f1_score, confusion_matrix
from imblearn.metrics import geometric_mean_score
import shap

# 데이터 로드
df = pd.read_csv("./data/week1.csv")
## 전처리
df.corr()  # 상관계수 확인
df = df.drop(columns=['X4', 'X13', 'X18', 'X19', 'X20'])  # 불필요한 열 제거

X = df.drop("Y", axis=1)
y = df['Y']

# train/test 셋 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # StandardScaler 적용
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# Polynomial Features 적용 (차수는 2로 설정)
poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# SMOTE 적용
smote = SMOTE(sampling_strategy=0.3)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_poly, y_train)

# # scale_pos_weight 계산
# neg_count = (y_train == 0).sum()  # Negative Class Count
# pos_count = (y_train == 1).sum()  # Positive Class Count
# scale_pos_weight = neg_count / pos_count

# XGBoost 분류기
xgb_clf = XGBClassifier(
    # random_state=42, 
    use_label_encoder=False, 
    eval_metric='logloss', 
    # scale_pos_weight=scale_pos_weight  # scale_pos_weight 설정
)
xgb_clf.fit(X_train_resampled, y_train_resampled)

# 예측
y_pred = xgb_clf.predict(X_test_poly)

# 성능 평가
f1 = f1_score(y_test, y_pred)
print(f"F1 Score: {f1}")
gmean = geometric_mean_score(y_test, y_pred)
print(f"G-Mean: {gmean}")

# # Confusion Matrix 출력
# conf_matrix = confusion_matrix(y_test, y_pred)
# print("Confusion Matrix:")
# print(conf_matrix)

# # SHAP 분석
# explainer = shap.TreeExplainer(xgb_clf)  # TreeExplainer 사용
# shap_values = explainer.shap_values(X_test_poly)  # SHAP 값 계산

# # 변수 중요도 플롯
# shap.summary_plot(shap_values, X_test_poly)

# # 클래스 비율 확인
# print("Before SMOTE:")
# print(y_train.value_counts(normalize=True))

# print("\nAfter SMOTE:")
# print(y_train_resampled.value_counts(normalize=True))
# XGBoost: 클래스 가중치를 조정할 수 있어 불균형 데이터에 효과적으로 대응하며, 높은 예측 성능을 제공

# Logistic Regression: 해석이 용이하고 빠른 속도로 모델을 구축할 수 있으며, 클래스 가중치를 설정하여 불균형 문제를 완화할 수 있음

# LightGBM: 대규모 데이터셋을 처리할 수 있는 능력이 뛰어나고, 불균형 데이터에서 빠른 학습 속도를 제공

# RandomForest: 랜덤 샘플링 기법을 활용하여 과적합을 방지하고, 불균형 데이터에서도 안정적인 성능을 유지


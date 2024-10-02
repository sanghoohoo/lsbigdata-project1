import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from imblearn.over_sampling import SMOTE

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
smote = SMOTE(sampling_strategy=0.3, random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_poly, y_train)

# 로지스틱 회귀 (class_weight 옵션 추가)
from sklearn.linear_model import LogisticRegression
log_reg = LogisticRegression(random_state=42)#, class_weight='balanced')  # 또는 {0: 가중치0, 1: 가중치1} 형태로 직접 지정 가능
log_reg.fit(X_train_resampled, y_train_resampled)

# 예측
y_pred = log_reg.predict(X_test_poly)  # 변환된 다항식 데이터 사용

# 성능 평가
from sklearn.metrics import f1_score, confusion_matrix, roc_auc_score, roc_curve
from imblearn.metrics import geometric_mean_score
f1 = f1_score(y_test, y_pred)
print(f"F1 Score: {f1}")
gmean = geometric_mean_score(y_test, y_pred)
print(f"G-Mean: {gmean}")
# AUC 계산
auc = roc_auc_score(y_test, y_pred_proba)
print(f"AUC: {auc}")

# Confusion Matrix 출력
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

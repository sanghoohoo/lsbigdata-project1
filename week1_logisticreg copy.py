import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE

# 데이터 로드
df = pd.read_csv("./data/week1.csv")

# 불필요한 열 제거
df = df.drop(columns=['X4', 'X13', 'X18', 'X19', 'X20'])

X = df.drop("Y", axis=1)
y = df['Y']

# train/test 셋 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # StandardScaler 적용
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# PCA 적용
pca = PCA(n_components=5, random_state=42)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

# SMOTE 적용 (클래스 불균형 처리)
smote = SMOTE(sampling_strategy=0.3, random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_pca, y_train)

# 로지스틱 회귀
from sklearn.linear_model import LogisticRegression
log_reg = LogisticRegression(random_state=42)#, class_weight='balanced')
log_reg.fit(X_train_resampled, y_train_resampled)

# 예측
y_pred = log_reg.predict(X_test_pca)
y_pred_proba = log_reg.predict_proba(X_test_pca)[:, 1]  # 긍정 클래스 확률

# 성능 평가
from sklearn.metrics import f1_score, confusion_matrix, roc_auc_score
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

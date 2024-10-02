import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from sklearn.metrics import f1_score
from imblearn.metrics import geometric_mean_score
import shap

# 데이터 로드
df = pd.read_csv("./data/week1.csv")

# 불필요한 열 제거
df = df.drop(columns=['X4', 'X13', 'X18', 'X19', 'X20'])

X = df.drop("Y", axis=1)
y = df['Y']

# train/test 셋 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Polynomial Features 적용 (차수는 2로 설정) 후 데이터프레임으로 변환
poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# 변환된 특징들의 이름 생성
poly_feature_names = poly.get_feature_names_out(X_train.columns)

# 데이터프레임으로 변환
X_train_poly_df = pd.DataFrame(X_train_poly, columns=poly_feature_names)
X_test_poly_df = pd.DataFrame(X_test_poly, columns=poly_feature_names)

# SMOTE 적용
smote = SMOTE(sampling_strategy=0.3)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_poly_df, y_train)

# XGBoost 분류기
xgb_clf = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
xgb_clf.fit(X_train_resampled, y_train_resampled)

# 예측
y_pred = xgb_clf.predict(X_test_poly_df)

# 성능 평가
f1 = f1_score(y_test, y_pred)
print(f"F1 Score: {f1}")
gmean = geometric_mean_score(y_test, y_pred)
print(f"G-Mean: {gmean}")

# SHAP 분석
explainer = shap.TreeExplainer(xgb_clf)
shap_values = explainer.shap_values(X_test_poly_df)

# 변수 중요도 플롯
shap.summary_plot(shap_values, X_test_poly_df)

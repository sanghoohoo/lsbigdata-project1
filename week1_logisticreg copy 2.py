import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from imblearn.over_sampling import SMOTE
from lightgbm import LGBMClassifier
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

# Polynomial Features 적용 (차수는 2로 설정)
poly = PolynomialFeatures(degree=2, include_bias=False)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Polynomial Features에 맞는 새로운 컬럼명 생성
original_columns = X.columns
poly_feature_names = poly.get_feature_names_out(original_columns)

# 데이터프레임으로 변환 (다항 특성 적용 후)
X_train_poly_df = pd.DataFrame(X_train_poly, columns=poly_feature_names)
X_test_poly_df = pd.DataFrame(X_test_poly, columns=poly_feature_names)

# StandardScaler 적용 (정규화)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_poly_df)
X_test_scaled = scaler.transform(X_test_poly_df)

# 데이터프레임으로 변환 (정규화 후 데이터프레임 유지)
X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=poly_feature_names)
X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=poly_feature_names)

# SMOTE 적용
smote = SMOTE(sampling_strategy=0.3, random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled_df, y_train)

# LightGBM 분류기
lgb_clf = LGBMClassifier(
    random_state=42, 
    objective='binary',
    eval_metric='logloss'
)
lgb_clf.fit(X_train_resampled, y_train_resampled)

# 예측
y_pred = lgb_clf.predict(X_test_scaled_df)

# 성능 평가
f1 = f1_score(y_test, y_pred)
print(f"F1 Score: {f1}")
gmean = geometric_mean_score(y_test, y_pred)
print(f"G-Mean: {gmean}")

# Confusion Matrix 출력
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

# SHAP 분석
explainer = shap.TreeExplainer(lgb_clf)  # TreeExplainer 사용
shap_values = explainer.shap_values(X_test_scaled_df)  # SHAP 값 계산

# 변수 중요도 플롯
shap.summary_plot(shap_values, X_test_scaled_df)

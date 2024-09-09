import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, uniform
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.model_selection import cross_val_score, KFold
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import make_scorer, mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler

## 필요한 데이터 불러오기
berry_train=pd.read_csv("./data/blueberry/train.csv")
berry_test=pd.read_csv("./data/blueberry/test.csv")
sub_df=pd.read_csv("./data/blueberry/sample_submission.csv")

berry_train.isna().sum()
berry_test.isna().sum()

berry_train.info()

## train
X=berry_train.drop(["yield", "id"], axis=1)
y=berry_train["yield"]
berry_test=berry_test.drop(["id"], axis=1)

# 표준화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
test_X_scaled=scaler.transform(berry_test)

# 정규화된 데이터를 DataFrame으로 변환
X = pd.DataFrame(X_scaled, columns=X.columns)
test_X= pd.DataFrame(test_X_scaled, columns=berry_test.columns)

# 다항 특징 추가
polynomial_transformer=PolynomialFeatures(degree=3, include_bias=False)

polynomial_features=polynomial_transformer.fit_transform(X.values)
features=polynomial_transformer.get_feature_names_out(X.columns)
X=pd.DataFrame(polynomial_features,columns=features)

polynomial_features=polynomial_transformer.fit_transform(test_X.values)
features=polynomial_transformer.get_feature_names_out(test_X.columns)
test_X=pd.DataFrame(polynomial_features,columns=features)

list(X.columns)


# dct 모델 생성
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV

model = DecisionTreeRegressor(random_state=42)
param_grid={
    'max_depth': np.arange(0, 100, 10),
    'min_samples_split': np.arange(0, 100, 10)
}

grid_search=GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    scoring='neg_mean_absolute_error',
    cv=5
)

grid_search.fit(X,y)

grid_search.best_params_
grid_search.cv_results_
score_dct=-grid_search.best_score_
best_model_dct=grid_search.best_estimator_

# Lasso 모델 생성
from sklearn.linear_model import Lasso
model = Lasso()
param_grid={
    'alpha': np.arange(2.8, 3, 0.1),
}

grid_search=GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    scoring='neg_mean_absolute_error',
    cv=5
)

grid_search.fit(X,y)

grid_search.best_params_
grid_search.cv_results_
score_lasso=-grid_search.best_score_
best_model_lasso=grid_search.best_estimator_

# Bagging

pred_y_lasso = best_model_lasso.predict(test_X)
pred_y_dct = best_model_dct.predict(test_X)

# 가중치는 성능에 반비례하게 설정 (1/score)
weight_lasso = 1 / score_lasso
weight_dct = 1 / score_dct

# 가중치의 합으로 정규화
total_weight = weight_lasso + weight_dct
weight_lasso /= total_weight
weight_dct /= total_weight

# 가중치를 적용한 예측 (Bagging)
pred_y_ensemble = weight_lasso * pred_y_lasso + weight_dct * pred_y_dct

# yield 바꿔치기
sub_df["yield"] = pred_y
sub_df

# csv 파일로 내보내기
sub_df.to_csv("./data/blueberry/sample_submission_scaled.csv", index=False)
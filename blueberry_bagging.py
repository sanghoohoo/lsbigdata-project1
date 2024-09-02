import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, uniform
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score, KFold
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import make_scorer, mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor

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
polynomial_transformer=PolynomialFeatures(degree=2, include_bias=False)

polynomial_features=polynomial_transformer.fit_transform(X.values)
features=polynomial_transformer.get_feature_names_out(X.columns)
X=pd.DataFrame(polynomial_features,columns=features)

polynomial_features=polynomial_transformer.fit_transform(test_X.values)
features=polynomial_transformer.get_feature_names_out(test_X.columns)
test_X=pd.DataFrame(polynomial_features,columns=features)

list(X.columns)
####### lasso alpha
# 교차 검증 설정
kf = KFold(n_splits=20, shuffle=True, random_state=2024)

def mae(model):
    score = -cross_val_score(model, X, y, cv = kf,
                                     n_jobs = -1, scoring = "neg_mean_absolute_error").mean()
    return(score)

# 각 알파 값에 대한 교차 검증 점수 저장
alpha_values = np.arange(2, 4, 1)
mean_scores = np.zeros(len(alpha_values))

k=0
for alpha in alpha_values:
    lasso = Lasso(alpha=alpha)
    mean_scores[k] = mae(lasso)
    k += 1

# 결과를 DataFrame으로 저장
df = pd.DataFrame({
    'lambda': alpha_values,
    'validation_error': mean_scores
})

# 최적의 alpha 값 찾기
optimal_alpha = df['lambda'][np.argmin(df['validation_error'])]
print("Optimal lambda:", optimal_alpha)

# 결과 시각화
plt.plot(df['lambda'], df['validation_error'], label='Validation Error', color='red')
plt.xlabel('Lambda')
plt.ylabel('Mean Squared Error')
plt.legend()
plt.title('Lasso Regression Train vs Validation Error')
plt.show()


####### knn k
# 각 n_neighbors 값에 대한 교차 검증 점수 저장
knn_neighbors_values = np.arange(1, 31)
knn_mean_scores = np.zeros(len(knn_neighbors_values))

k = 0
for n_neighbors in knn_neighbors_values:
    knn = KNeighborsRegressor(n_neighbors=n_neighbors)
    knn_mean_scores[k] = mae(knn)
    k += 1

# 최적의 n_neighbors 값 찾기
optimal_knn_neighbors = knn_neighbors_values[np.argmin(knn_mean_scores)]
print("Optimal KNN n_neighbors:", optimal_knn_neighbors)


# 결과 시각화
plt.plot(knn_neighbors_values, knn_mean_scores, label='Validation Error', color='green')
plt.xlabel('Number of Neighbors')
plt.ylabel('Mean Absolute Error')
plt.legend()
plt.title('KNN Train vs Validation Error')
plt.show()


####ridge
# 각 알파 값에 대한 교차 검증 점수 저장
ridge_alpha_values = np.logspace(-3, 3, 10)  # Ridge의 alpha 값 범위
ridge_mean_scores = np.zeros(len(ridge_alpha_values))

k = 0
for alpha in ridge_alpha_values:
    ridge = Ridge(alpha=alpha)
    ridge_mean_scores[k] = mae(ridge)
    k += 1

# 최적의 alpha 값 찾기
optimal_ridge_alpha = ridge_alpha_values[np.argmin(ridge_mean_scores)]
print("Optimal Ridge alpha:", optimal_ridge_alpha)

# 결과 시각화
plt.plot(ridge_alpha_values, ridge_mean_scores, label='Validation Error', color='blue')
plt.xscale('log')
plt.xlabel('Alpha')
plt.ylabel('Mean Absolute Error')
plt.legend()
plt.title('Ridge Regression Train vs Validation Error')
plt.show()


### model

# Lasso모델 학습
lasso_model= Lasso(alpha=2.9)
lasso_model.fit(X, y)  # 자동으로 기울기, 절편 값을 구해줌
lasso_pred_y=lasso_model.predict(test_X) # test 셋에 대한 집값

# Ridge 모델 학습
ridge_model = Ridge(46.4)
ridge_model.fit(X, y)
ridge_pred_y = ridge_model.predict(test_X)

# KNN 모델 학습
knn_model = KNeighborsRegressor(15)
knn_model.fit(X, y)
knn_pred_y = knn_model.predict(test_X)

# 선형회귀 모델 학습
lin_model = LinearRegression()
lin_model.fit(X, y)
lin_pred_y = lin_model.predict(test_X)


mae(lasso_model)
mae(ridge_model)
mae(knn_model)
mae(lin_model)

# 배깅: Ridge와 KNN 예측의 평균을 최종 예측으로 사용
final_pred_y = (lasso_pred_y*(1/363) + ridge_pred_y*(1/389) + knn_pred_y*(1/433)) / ((1/363)+(1/389)+(1/433))

# 결과 저장
sub_df["yield"] = final_pred_y
sub_df.to_csv("./data/blueberry/sample_submission_bagging.csv", index=False)



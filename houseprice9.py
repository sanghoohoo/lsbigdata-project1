
# 필요한 패키지 불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

## 필요한 데이터 불러오기
house_train=pd.read_csv("./data/houseprice/train.csv")
house_test=pd.read_csv("./data/houseprice/test.csv")
sub_df=pd.read_csv("./data/houseprice/sample_submission.csv")

#### 범주형 데이터 더미코딩
house_train['Neighborhood'].unique()

neighborhood_dummies = pd.get_dummies(
    house_train['Neighborhood'],
    drop_first=True)
neighborhood_dummies.columns


x = pd.concat([house_train[["GrLivArea", "GarageArea"]], neighborhood_dummies], axis=1)
y = house_train["SalePrice"]

# 선형 회귀 모델 생성
model = LinearRegression()

# 모델 학습
model.fit(x, y)  # 자동으로 기울기, 절편 값을 구해줌

# 회귀 직선의 기울기와 절편
model.coef_      # 기울기 a
model.intercept_ # 절편 b


neighborhood_dummies_test = pd.get_dummies(
    house_test['Neighborhood'],
    drop_first=True)
    
test_x = pd.concat([house_test[["GrLivArea", "GarageArea"]],
                    neighborhood_dummies_test], axis=1)

# 결측치 확인
test_x.isna().sum()
test_x=test_x.fillna(house_test["GarageArea"].mean())

pred_y=model.predict(test_x) # test 셋에 대한 집값
pred_y

# SalePrice 바꿔치기
sub_df["SalePrice"] = pred_y
sub_df

# csv 파일로 내보내기
sub_df.to_csv("./data/houseprice/sample_submission17.csv", index=False)

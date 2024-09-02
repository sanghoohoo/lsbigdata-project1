# 원하는 변수를 사용해서 회귀모델을 만들고, 제출할것!
# 원하는 변수 2개
# 회귀모델을 통한 집값 예측

# 필요한 패키지 불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

## 필요한 데이터 불러오기
house_train=pd.read_csv("./data/houseprice/train.csv")
house_test=pd.read_csv("./data/houseprice/test.csv")
sub_df=pd.read_csv("./data/houseprice/sample_submission.csv")

house_train.isna().sum()
house_test.isna().sum()

# for i in house_train.select_dtypes(include=[int,float]).columns:
#     house_train[f'{i}']=house_train.fillna(house_train[f'{i}'].mean())

# for i in house_train.select_dtypes(include=[object]).columns:
#     house_train[f'{i}']=house_train.fillna('unknown')

## 숫자형 채우기
quantitative = house_train.select_dtypes(include = [int, float])
quantitative.isna().sum()
quant_selected = quantitative.columns[quantitative.isna().sum() > 0]

for col in quant_selected:
    house_train[col].fillna(house_train[col].mean(), inplace=True)
house_train[quant_selected].isna().sum()

## 범주형 채우기
qualitative = house_train.select_dtypes(include = [object])
qualitative.isna().sum()
qual_selected = qualitative.columns[qualitative.isna().sum() > 0]

for col in qual_selected:
    house_train[col].fillna("unknown", inplace=True)
house_train[qual_selected].isna().sum()
###

house_train.shape
house_test.shape

house_train.isna().sum().sum()

df=pd.concat([house_train, house_test],ignore_index=True)
df

df.info()

df = pd.get_dummies(
    df,
    columns=df.select_dtypes(include=[object]).columns,
    drop_first=True
    )


train_df = df.iloc[:1460,]
train_df

test_df = df.iloc[1460:,]

# validation 셋 (모의고사 셋) 만들기
np.random.seed(42)
val_index=np.random.choice(np.arange(1460), size=438, replace=False)

valid_df=train_df.loc[val_index] # 30%
train_df=train_df.drop(val_index) # 70%


train_x = train_df.drop('SalePrice', axis=1)
train_y = train_df["SalePrice"]

valid_x = valid_df.drop('SalePrice', axis=1)
valid_y = valid_df["SalePrice"]

## test
test_x = test_df.drop('SalePrice', axis=1)

model = LinearRegression()

model.fit(train_x, train_y)

y_hat=model.predict(valid_x)

np.sqrt(np.mean((valid_y - y_hat)**2))

## test 셋 결측치 채우기
test_x["GrLivArea"].isna().sum()
test_x["GarageArea"].isna().sum()
test_x=test_x.fillna(house_test["GarageArea"].mean())

# 테스트 데이터 집값 예측
pred_y=model.predict(test_x) # test 셋에 대한 집값
pred_y

# SalePrice 바꿔치기
sub_df["SalePrice"] = pred_y
sub_df

# csv 파일로 내보내기
# sub_df.to_csv("./data/houseprice/sample_submission18.csv", index=False)
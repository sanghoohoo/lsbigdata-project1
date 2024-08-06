import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

house_train = pd.read_csv("data/houseprice/train.csv")
house_test = pd.read_csv("data/houseprice/test.csv")
sub_df=pd.read_csv("./data/houseprice/sample_submission.csv")


# house_train 에서 수치형 변수만 x에 저장
house_train.info()
x = house_train.select_dtypes(include=[int, float])
x.info()

# 필요없는 칼럼 제거 (ID, SalePrice)
x = x.iloc[:,1:-1]
y = house_train['SalePrice']

# train 결측치 제거
x.isna().sum()

x['LotFrontage'].describe()
x['MasVnrArea'].describe()
x['GarageYrBlt'].describe()

# x['LotFrontage'] = x['LotFrontage'].fillna(x['LotFrontage'].mean())
# x['GarageYrBlt'] = x['GarageYrBlt'].fillna(x['GarageYrBlt'].mean())
# x['MasVnrArea'] = x['MasVnrArea'].fillna(0)

# fill_values = {
#     'LotFrontage' : x['LotFrontage'].mean(),
#     'GarageYrBlt' : x['GarageYrBlt'].mean(), #mode()[0]
#     'MasVnrArea' : x['MasVnrArea'].mode()[0]
# }
# x = x.fillna(value=fill_values)
x = x.fillna(x.mean())


# 모델 학습
model = LinearRegression()
model.fit(x, y)

model.coef_
model.intercept_

# test 결측치 제거
test_x = house_test.select_dtypes(include=[int, float]).iloc[:,1:]
test_x
test_x.isna().sum()

test_x[['BsmtFinSF1','BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF']].describe()
test_x['GarageYrBlt'].describe()

# fill_values2 = {
#     'LotFrontage' : test_x['LotFrontage'].mean(),
#     'GarageYrBlt' : test_x['GarageYrBlt'].mean(), #mode()[0]
#     'MasVnrArea' : test_x['MasVnrArea'].mode()[0]
# }
# test_x = test_x.fillna(value=fill_values2)
#test_x = test_x.fillna(0)
test_x = test_x.fillna(test_x.mean())

# test_x['BsmtFinSF1'] = test_x['BsmtFinSF1'].fillna(0)
# test_x['BsmtFinSF2'] = test_x['BsmtFinSF2'].fillna(0)
# test_x['BsmtUnfSF'] = test_x['BsmtUnfSF'].fillna(0)
# test_x['TotalBsmtSF'] = test_x['TotalBsmtSF'].fillna(0)
# test_x['GarageCars'] = test_x['GarageCars'].fillna(0)
# test_x['GarageArea'] = test_x['GarageArea'].fillna(0)
# test_x['BsmtFullBath'] = test_x['BsmtFullBath'].fillna(0)
# test_x['BsmtHalfBath'] = test_x['BsmtHalfBath'].fillna(0)
# test_x['LotFrontage'] = test_x['LotFrontage'].fillna(test_x['LotFrontage'].mean())
# test_x['GarageYrBlt'] = test_x['GarageYrBlt'].fillna(test_x['GarageYrBlt'].mean())
# test_x['MasVnrArea'] = test_x['MasVnrArea'].fillna(0)
test_x.isna().sum()

pred_y = model.predict(test_x) # test 셋에 대한 집값
pred_y

sub_df['SalePrice'] = pred_y
#sub_df.to_csv("data/houseprice/sample_submission16.csv", index = False)

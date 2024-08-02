import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

house_train = pd.read_csv("data/houseprice/train.csv")
house_test = pd.read_csv("data/houseprice/test.csv")
sub_df=pd.read_csv("./data/houseprice/sample_submission.csv")

#이상치 제거
house_train = house_train.query('GrLivArea<=4500')

x = house_train[['GrLivArea']]
y = house_train['SalePrice']

model = LinearRegression()

model.fit(x, y)

model.coef_ # 기울기 a
model.intercept_ # 절편 b
slope = model.coef_[0]
intercept = model.intercept_
print(f"기울기 (slope): {slope}")
print(f"절편 (intercept): {intercept}")

test_x = house_test[['GrLivArea']]
test_x

pred_y = model.predict(test_x) # test 셋에 대한 집값
pred_y

plt.scatter(x, y, color='blue', label='data')
plt.plot(test_x, pred_y, color='red', label='regression line')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim([0,5000])
plt.ylim([0,900000])
plt.legend()
plt.show()
plt.clf()

sub_df['SalePrice'] = pred_y
#sub_df.to_csv("data/houseprice/sample_submission10.csv", index = False)



import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
x = np.linspace(-10,10,100)
a=1
b=0
y=a*x+b
plt.plot(x,y, color = 'blue')
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')
plt.axis('equal')
plt.xlim(-5,5)
plt.ylim(-5,5)
plt.show()
plt.clf()

house_train = pd.read_csv("data/houseprice/train.csv")
my_df=house_train[['BedroomAbvGr','SalePrice']]
my_df['SalePrice']=my_df['SalePrice']/1000

##
plt.scatter(x=my_df['BedroomAbvGr'], y=my_df['SalePrice'])

x = np.linspace(0,8,100)
a=12
b=170
y=a*x+b

plt.plot(x,y, color = 'blue')
plt.show()
plt.clf()

house_test = pd.read_csv("data/houseprice/test.csv")
house_test['SalePrice']=(12*house_test['BedroomAbvGr']+170)*1000
house_test

sub_df=pd.read_csv("./data/houseprice/sample_submission.csv")
sub_df['SalePrice'] = house_test['SalePrice']
sub_df.to_csv("data/houseprice/sample_submission5.csv", index = False)

a=12
b=170

y_hat=(a*house_train['BedroomAbvGr']+b)*1000
y=house_train['SalePrice']
np.abs(y - y_hat).sum()



## 선형회귀 사용해서 구하기

x = house_train[['BedroomAbvGr']]
y = house_train['SalePrice']/1000

# 선형 회귀 모델 생성
model = LinearRegression()

# 모델 학습
model.fit(x, y)  # 자동으로 기울기, 절편 값을 구해줌 (model에 저장됨)

# 회귀 직선의 기울기와 절편
model.coef_ # 기울기 a
model.intercept_ # 절편 b
slope = model.coef_[0]
intercept = model.intercept_
print(f"기울기 (slope): {slope}")
print(f"절편 (intercept): {intercept}")

# 예측값 계산
y_pred = model.predict(x) # 회귀 직선에 x값 대입

# 데이터와 회귀 직선 시각화
plt.scatter(x, y, color='blue', label='data')
plt.plot(x, y_pred, color='red', label='regression line')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
plt.clf()

#abs값으로 했을 때 a=16 b=117

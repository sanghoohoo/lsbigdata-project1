import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import uniform
from sklearn.linear_model import LinearRegression

# 20차 모델 성능을 알아보자능
np.random.seed(2024)
x = uniform.rvs(size=30, loc=-4, scale=8)
y = np.sin(x) + norm.rvs(size=30, loc=0, scale=0.3)

import pandas as pd
df = pd.DataFrame({
    "y" : y,
    "x" : x
})
df

train_df = df.loc[:19]
train_df

for i in range(2, 21):
    train_df[f"x{i}"] = train_df["x"] ** i
    
# 'x' 열을 포함하여 'x2'부터 'x20'까지 선택.
train_x = train_df[["x"] + [f"x{i}" for i in range(2, 21)]]
train_y = train_df["y"]

valid_df = df.loc[20:]
valid_df

for i in range(2, 21):
    valid_df[f"x{i}"] = valid_df["x"] ** i

# 'x' 열을 포함하여 'x2'부터 'x20'까지 선택.
valid_x = valid_df[["x"] + [f"x{i}" for i in range(2, 21)]]
valid_x
valid_y = valid_df["y"]
valid_y

from sklearn.linear_model import Lasso

val_result=np.repeat(0.0, 100)
tr_result=np.repeat(0.0, 100)

for i in np.arange(0, 100):
    model= Lasso(alpha=i*0.01)
    model.fit(train_x, train_y)

    # 모델 성능
    y_hat_train = model.predict(train_x)
    y_hat_val = model.predict(valid_x)

    perf_train=sum((train_df["y"] - y_hat_train)**2)
    perf_val=sum((valid_df["y"] - y_hat_val)**2)
    tr_result[i]=perf_train
    val_result[i]=perf_val

tr_result
val_result

import seaborn as sns

df = pd.DataFrame({
    'l':np.arange(0,1,0.01),
    'tr':tr_result,
    'val':val_result
})

# sns.scatterplot(data=df,x='l',y='tr', color='blue')
# sns.scatterplot(data=df,x='l',y='val', color='red')
# plt.xlim(0,0.4)

val_result[3]
np.min(val_result)
np.argmin(val_result)
#alpha를 0.03으로 선택

model=Lasso(0.03)
model.fit(train_x,train_y)
model.coef_
model.intercept_

train_x

# lasso회귀 valid set에 얼마나 적합하는지 보자
k = np.arange(-4, 4, 0.01)
df_k = pd.DataFrame({
    'x': k
    })
for i in range(2,21) :
    df_k[f'x{i}'] = df_k['x']**i
plt.scatter(valid_df['x'], valid_df['y'], color='blue')
reg_line = model.predict(df_k)
plt.plot(k, reg_line, color="red")
plt.show()



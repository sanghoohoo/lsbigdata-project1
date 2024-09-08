import pandas as np
import numpy as np
from palmerpenguins import load_penguins

penguins=load_penguins()
penguins.head()

df=penguins.dropna()
df=df[['bill_length_mm','bill_depth_mm']]
df=df.rename(columns={'bill_length_mm':'y',
                   'bill_depth_mm':'x'})
df

# x=15기준으로 나눴을 떄 데이터포인트 몇개씩?
n1=df.query("x < 15").shape[0]
n2=df.query("x >= 15").shape[0]

# 1,2번 그룹 얼마로 예측?
y_hat1=df.query("x < 15").mean()[0]
y_hat2=df.query("x >= 15").mean()[0]

# 각 그룹 mse
mse1=np.mean((df.query("x<15")["y"]- y_hat1)**2)
mse2=np.mean((df.query("x >= 15")["y"]- y_hat2)**2)

# x=15 의 mse 가중평균?
(mse1*n1+mse2*n2)/(n1+n2) #29.23


## x=20일때
n1=df.query("x < 20").shape[0]
n2=df.query("x >= 20").shape[0]

y_hat1=df.query("x < 20").mean()[0]
y_hat2=df.query("x >= 20").mean()[0]

mse1=np.mean((df.query("x<20")["y"]- y_hat1)**2)
mse2=np.mean((df.query("x >= 20")["y"]- y_hat2)**2)

(mse1*n1+mse2*n2)/(n1+n2) #29.73

## 원래
np.mean((df["y"]- df["y"].mean())**2) #29.81

29.81-29.73


## 기준값 x를 넣으면 mse값이 나오는 함수
def my_mse(x):
    n1=df.query(f"x < {x}").shape[0]
    n2=df.query(f"x >= {x}").shape[0]

    y_hat1=df.query(f"x < {x}").mean()[0]
    y_hat2=df.query(f"x >= {x}").mean()[0]

    mse1=np.mean((df.query(f"x<{x}")["y"]- y_hat1)**2)
    mse2=np.mean((df.query(f"x >= {x}")["y"]- y_hat2)**2)

    return (mse1*n1+mse2*n2)/(n1+n2)


df["x"].min()
df["x"].max()

## 13.2~21.4
x_values=np.arange(13.2, 21.4, 0.01)
x_values.shape
result=np.repeat(0.0, 820)
for i in range(820):
    result[i]=my_mse(x_values[i])

result.min()
x_values[np.argmin(result)] #16.4

## 13.2~16.4
df2=df.query("x<=16.4")

def my_mse2(x):
    n1=df2.query(f"x < {x}").shape[0]
    n2=df2.query(f"x >= {x}").shape[0]

    y_hat1=df2.query(f"x < {x}").mean()[0]
    y_hat2=df2.query(f"x >= {x}").mean()[0]

    mse1=np.mean((df2.query(f"x<{x}")["y"]- y_hat1)**2)
    mse2=np.mean((df2.query(f"x >= {x}")["y"]- y_hat2)**2)

    return (mse1*n1+mse2*n2)/(n1+n2)

x_values=np.arange(13.2, 16.39, 0.01)
x_values.shape
result=np.repeat(0.0, 320)
for i in range(320):
    result[i]=my_mse2(x_values[i])

result.min()
x_values[np.argmin(result)] #14.0

##16.4~21.4
df3=df.query("x>=16.4")

def my_mse3(x):
    n1=df3.query(f"x < {x}").shape[0]
    n2=df3.query(f"x >= {x}").shape[0]

    y_hat1=df3.query(f"x < {x}").mean()[0]
    y_hat2=df3.query(f"x >= {x}").mean()[0]

    mse1=np.mean((df3.query(f"x<{x}")["y"]- y_hat1)**2)
    mse2=np.mean((df3.query(f"x >= {x}")["y"]- y_hat2)**2)

    return (mse1*n1+mse2*n2)/(n1+n2)

x_values=np.arange(16.41, 21.4, 0.01)
x_values.shape
result=np.repeat(0.0, 499)
for i in range(499):
    result[i]=my_mse3(x_values[i])

result.min()
x_values[np.argmin(result)] #19.4

# 평행선 그리기
import matplotlib.pyplot as plt
df.plot(kind='scatter', x='x', y='y')

thresholds=[14.1,16.4,19.4]
df['group']=np.digitize(df['x'], thresholds)
y_mean=df.groupby('group').mean()['y']
y_mean

# plt.plot([df['x'].min(), 14.1], [y_mean[0],y_mean[0]], color='red')
# plt.plot([14.1, 16.4], [y_mean[1], y_mean[1]], color='red')
# plt.plot([16.4, 19.4], [y_mean[2], y_mean[2]], color='red')
# plt.plot([19.4, df['x'].max()], [y_mean[3], y_mean[3]], color='red')

k1=np.linspace(13, 14.01, 100)
k2=np.linspace(14.01, 16.42, 100)
k3=np.linspace(16.42, 19.4, 100)
k4=np.linspace(19.4, 22, 100)

plt.plot(k1, np.repeat(y_mean[0],100), color="red")
plt.plot(k2, np.repeat(y_mean[1],100), color="red")
plt.plot(k3, np.repeat(y_mean[2],100), color="red")
plt.plot(k4, np.repeat(y_mean[3],100), color="red")
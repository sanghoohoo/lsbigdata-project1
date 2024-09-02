import matplotlib.pyplot as plt
import numpy as np

# x, y의 값을 정의합니다 (-1에서 7까지)
beta0 = np.linspace(-15, 15, 400)
beta1 = np.linspace(-15, 15, 400)
beta0, beta1 = np.meshgrid(beta0, beta1)

# 함수 f(x, y)를 계산합니다.
z = (1-(beta0+beta1))**2 + (4-(beta0+2*beta1))**2 + (1.5-(beta0+3*beta1))**2 + (5-(beta0+4*beta1))**2

# 등고선 그래프를 그립니다.
plt.figure()
cp = plt.contour(beta0, beta1, z, levels=50)  # levels는 등고선의 개수를 조절합니다.
plt.colorbar(cp)  # 등고선 레벨 값에 대한 컬러바를 추가합니다.

# f(beta0, beta1) = (1-(beta0+beta1))**2 + (4-(beta0+2*beta1))**2 + (1.5-(beta0+3*beta1))**2 + (5-(beta0+4*beta1))**@
beta0 = 10
beta1 = 10
delta = 0.01
plt.scatter(beta0, beta1, color = 'red', s=2)
for i in range(1000):
    gradient_beta0 = 8*beta0 + 20*beta1 -23
    gradient_beta1 = 20*beta0 + 60*beta1 -67
    beta0, beta1 = np.array([beta0, beta1]) - delta * np.array([gradient_beta0, gradient_beta1])
    plt.scatter(beta0, beta1, color = 'red', s=2)
print('beta0:', round(beta0,2),', beta1:', round(beta1,2))


# 모델 fit으로 베타 구하기
import pandas as pd
from sklearn.linear_model import LinearRegression

df=pd.DataFrame({
    'x': np.array([1, 2, 3, 4]),
    'y': np.array([1, 4, 1.5, 5])
})
model = LinearRegression()
model.fit(df[['x']], df['y'])

model.intercept_
model.coef_
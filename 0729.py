import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

old_seat=np.arange(1,29)

np.random.seed(20240729)

new_seat=np.random.choice(old_seat, 28, replace=False)

result=pd.DataFrame(
    {'old_seat' : old_seat,
     'new_seat' : new_seat}
)

#result.to_csv('result.csv')

x=np.linspace(0,8,2)
y=2*x
plt.plot(x, y, color='black')
plt.scatter(x, y, color='red', zorder=5, s=3)
plt.show()
plt.clf()

x=np.linspace(-8,8,100)
y=x**2
plt.plot(x, y, color='black')
#plt.scatter(x, y, color='red', zorder=5, s=3)
plt.xlim(-10, 10)
plt.ylim(0, 40)
plt.gca().set_aspect('equal', adjustable='box')
#plt.axis('equal')
plt.show()
plt.clf()

from scipy.stats import norm

x=np.array([79.1, 68.8, 62.0, 74.4, 71.0, 60.6, 98.5, 86.4, 73.0, 40.8,
            61.2, 68.7, 61.6, 67.7, 61.7, 66.8])
x.mean()
len(x)

z_005=norm.ppf(0.95, loc=0, scale=1)
z_005

#신뢰구간
x.mean() + z_005 * 6/np.sqrt(16)
x.mean() - z_005 * 6/np.sqrt(16)

# 데이터로부터 E[X^2] 구하기
x=norm.rvs(loc=3, scale=5, size=100000)
np.mean(x**2)
#sum(x**2) / (len(x)-1)

np.mean((x-x**2)/(2*x))

np.random.seed(20240729)
x=norm.rvs(loc=3, scale=5, size=100000)
x_bar=np.mean(x)
s_2=sum((x - x_bar)**2) / (100000-1)
s_2

np.var(x, ddof=1) # n-1으로 나눈 값 (표본 분산)
np.var(x, ddof=0) # n으로 나눈 값

# n-1 vs. n
x=norm.rvs(loc=3, scale=5, size=20)
np.var(x)
np.var(x, ddof=1)

import numpy as np
import pandas as pd
from scipy.stats import uniform
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

uniform.rvs(loc=2, scale=4, size=1)

k=np.linspace(0, 8,100)
y= uniform.pdf(k, loc=2, scale=4)
plt.plot(k, y, color='black')
plt.show()
plt.clf()

uniform.cdf(3.25, loc=2, scale=4)

uniform.cdf(8.39, loc=2, scale=4)-uniform.cdf(5, loc=2, scale=4)

uniform.ppf(0.93, loc=2, scale=4)

# 신뢰구간(표본 20개 뽑고 표본평균 계산)
x=uniform.rvs(loc=2, scale=4, size=20000, random_state=42)
x=x.reshape(1000,20)
x.shape
blue_x=x.mean(axis=1)

sns.histplot(blue_x, stat='density')
plt.show()

# X bar ~ N(4, 1.333)

uniform.var(loc=2, scale=4)
uniform.expect(loc=2, scale=4)

xmin, xmax = (blue_x.min(), blue_x.max())
x_values=np.linspace(xmin,xmax,100)
pdf_values= norm.pdf(x_values, loc=4, scale=np.sqrt(1.3333333/20))
plt.plot(x_values, pdf_values, color='red', linewidth=2)
plt.show()
plt.clf()


# plot the normal distribution pdf
x_values=np.linspace(3,5,100)
pdf_values= norm.pdf(x_values, loc=4, scale=np.sqrt(1.3333333/20))
plt.plot(x_values, pdf_values, color='red', linewidth=2)
# 기대값 표현
plt.axvline(4, color='green', linestyle='--', linewidth=2)
# 표본평균(파란벽돌) 점찍기
blue_x=uniform.rvs(loc=2, scale=4, size=20).mean()
a=blue_x+0.665 #(2.57*표준편차 --> 99%커버  /  1.96*표준편차 --> 95%커버)
b=blue_x-0.665 #(2.57*표준편차)
plt.scatter(blue_x, 0.002, color='blue', zorder=10, s=10)
plt.axvline(x=a, color='blue', linestyle='--', linewidth=1)
plt.axvline(x=b, color='blue', linestyle='--', linewidth=1)

plt.show()
plt.clf()


a=norm.ppf(0.025, loc=4, scale=np.sqrt(1.3333333/20))
b=norm.ppf(0.975, loc=4, scale=np.sqrt(1.3333333/20))
a
b

(4-a)/(np.sqrt(1.3333333/20)) #표준편차의 1.96배

a=norm.ppf(0.005, loc=4, scale=np.sqrt(1.3333333/20))
b=norm.ppf(0.995, loc=4, scale=np.sqrt(1.3333333/20))


a
b
4-a
4-b


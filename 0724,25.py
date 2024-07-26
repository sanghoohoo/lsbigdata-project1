from scipy.stats import bernoulli
#확률질량함수(pmf)
#확률변수가 갖는 값에 해당하는 확률을 저장하고 있는 함수
#bernoulli.pmf(k,p)
bernoulli.pmf(1,0.3)
bernoulli.pmf(0,0.3)

# 이항분포 X~(X= k | n , p)
# n : 베르누이 확률변수 더한 갯수
# 1이 나올 확률
# binom.pmf(k, n, p)

from scipy.stats import binom
binom.pmf(0, n = 2, p=0.3)
binom.pmf(1, n = 2, p=0.3)
binom.pmf(2, n = 2, p=0.3)


result=[binom.pmf(x, n=30, p=0.3) for x in range(31)]
result
for i in range(31):
    binom.pmf(i, n = 30, p=0.3)
    
import math
math.factorial(54)/(math.factorial(26)*math.factorial(54-26))
math.comb(54,26)

import numpy as np
np.cumprod(np.arange(1,55))[-1]/\
(np.cumprod(np.arange(1,27))[-1]*np.cumprod(np.arange(1,29))[-1])

logf_54=sum(np.log(np.arange(1,55)))
logf_26=sum(np.log(np.arange(1,27)))
logf_28=sum(np.log(np.arange(1,29)))

np.exp(logf_54-(logf_26+logf_28))

math.comb(2,0)*0.3**0*(1-0.3)**2
math.comb(2,1)*0.3**1*(1-0.3)**1
math.comb(2,2)*0.3**2*(1-0.3)**0

#pmf(probability math function: 확률질량함수)
binom.pmf(0, 2, 0.3)
binom.pmf(1, 2, 0.3)
binom.pmf(2, 2, 0.3)

binom.pmf(4, 10, 0.36)
binom.pmf(np.arange(5), 10, 0.36).sum()
binom.pmf(np.arange(3,9), 10, 0.36).sum()

#X~B(30, 0.2)
#(X<4 25<=X) 방법 1
a=binom.pmf(np.arange(4), 30, 0.2).sum()
b=binom.pmf(np.arange(25,31), 30, 0.2).sum()
a+b
#(X<4 25<=X) 방법 2, 1에서 (4<=X<25)의 확률을 뺌
1-binom.pmf(np.arange(4,25), 30, 0.2).sum()

# rvs 함수 (random variates sample) : 표본 추출 함수
# X ~ Bernoulli(p=0.3)
bernoulli.rvs(0.3)+bernoulli.rvs(0.3)
binom.rvs(n=2, p=0.3, size=1)
binom.rvs(n=30, p=0.26, size=30)

30*0.26

import matplotlib.pyplot as plt

x=np.arange(31)
B=binom.pmf(x, 30, 0.26)
plt.bar(x,B)
plt.show()
plt.clf()

import seaborn as sns

sns.barplot(x=x,y=B)
plt.xticks(size=5)
plt.show()
plt.clf()

import pandas as pd

df = pd.DataFrame({'x':x, 'prob':B})
df
sns.barplot(data=df, x='x', y='prob')
plt.xticks(size=5)
plt.show()
plt.clf()

# cdf: cumulative dist. function
# (누적확률분포 함수)
#F_X(x) = P(X <= x)
binom.cdf(4, n=30, p=0.26)

binom.cdf(18, n=30, p=0.26)-binom.cdf(4, n=30, p=0.26)
binom.cdf(19, n=30, p=0.26)-binom.cdf(13, n=30, p=0.26)


x_1=binom.rvs(n=30, p=0.26, size=10)

x=np.arange(31)
prob_x=binom.pmf(x, 30, 0.26)
sns.barplot(prob_x, color='skyblue')
plt.xticks(size=5)
plt.show()
plt.scatter(x_1, np.repeat(0.002, 10), color='orange', zorder=5, s=3)
plt.axvline(7.8, color='lavender', linestyle='--', linewidth=2)
plt.show()
plt.clf()


binom.ppf(0.5, n=30, p=0.26)
binom.cdf(7, n=30, p=0.26)

binom.ppf(0.7, n=30, p=0.26)
binom.cdf(8, n=30, p=0.26)

1/np.sqrt(2*math.pi)

from scipy.stats import norm
#(x, loc=mu평균, scale=sigma표준편차)
norm.pdf(0, loc=0, scale=1)

norm.pdf(5, loc=3, scale=4)

# 정규분포 pdf 그리기
k=np.linspace(-5,5,100)
y= norm.pdf(k, loc=0, scale=1)

plt.plot(k, y, color='black')
plt.show()
plt.clf()


# mu (loc)
k=np.linspace(-5,5,100)
y= norm.pdf(k, loc=3, scale=1)

plt.plot(k, y, color='black')
plt.show()
plt.clf()


# sigma (scale)
k=np.linspace(-5,5,100)
y= norm.pdf(k, loc=0, scale=1)
y2= norm.pdf(k, loc=0, scale=2)
y3= norm.pdf(k, loc=0, scale=0.5)
plt.plot(k, y, color='black')
plt.plot(k, y2, color='blue')
plt.plot(k, y3, color='red')
plt.show()
plt.clf()

norm.cdf(100, loc=0, scale=1)
norm.cdf(0.54, loc=0, scale=1)-norm.cdf(-2, loc=0, scale=1)
norm.cdf(1, loc=0, scale=1)+norm.cdf(-3, loc=0, scale=1)

# X ~ N(3, 5^2)
# P(3 < X < 5) =? 15.54%
norm.cdf(5, loc=3, scale=5)-norm.cdf(3, loc=3, scale=5)

x=norm.rvs(loc=3, scale=5, size=1000)
sum((3<x) & (x<5))/1000

x=norm.rvs(loc=0, scale=1, size=1000)
np.mean(x<0)

x=norm.rvs(loc=3, scale=2, size=1000)
x
sns.histplot(x, stat='density', color='skyblue')

xmin, xmax = (x.min(), x.max())
k=np.linspace(xmin,xmax,100)
y= norm.pdf(k, loc=3, scale=2)
plt.plot(k, y, color='purple')
plt.show()
plt.clf()



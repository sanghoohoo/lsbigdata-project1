from scipy.stats import norm
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

x = norm.ppf(0.25,3,7)
z = norm.ppf(0.25,0,1)
x
3+z*7

norm.cdf(5, loc=3, scale=7)
norm.cdf(2/7, loc=0, scale=1)

# plot the normal distribution PDF
z=norm.rvs(0,1,size=1000)
sns.histplot(z, stat='density', color='grey')
zmin, zmax = (z.min(), z.max())
z_values=np.linspace(zmin,zmax,100)
pdf_values= norm.pdf(z_values, loc=0, scale=1)
plt.plot(z_values, pdf_values, color='red', linewidth=2)
plt.show()
plt.clf()

# X~N(3,2) 그래프 겹쳐 그리기
z=norm.rvs(0,1,size=1000)
x=z*np.sqrt(2) + 3
sns.histplot(z, stat='density', color='grey')
sns.histplot(x, stat="density", color="green")
zmin, xmax = (z.min(), x.max())
z_values = np.linspace(zmin, xmax, 500)
pdf_values = norm.pdf(z_values, loc=0, scale=1)
pdf_values2 = norm.pdf(z_values, loc=3, scale=np.sqrt(2))
plt.plot(z_values, pdf_values, color='red', linewidth=2)
plt.plot(z_values, pdf_values2, color='blue', linewidth=2)

plt.show()
plt.clf()

# X~N(5,3^2)일때 Z=(X-5)/3가 표준정규분포를 따른다는 것을 보이기
x=norm.rvs(5,3,size=1000)
z=(x-5)/3
sns.histplot(x, stat='density', color='grey')
sns.histplot(z, stat="density", color="green")
zmin, xmax = (z.min(), x.max())
z_values = np.linspace(zmin, xmax, 500)
pdf_values = norm.pdf(z_values, loc=0, scale=1)
plt.plot(z_values, pdf_values, color='red', linewidth=2)

plt.show()
plt.clf()

#
var_x=np.var(norm.rvs(5,3,size=20), ddof=1)
var_x
std_x=np.sqrt(var_x)
std_x

x=norm.rvs(5,3,size=1000)
z=(x-5)/std_x
sns.histplot(z, stat='density', color='grey')

zmin, zmax = (z.min(), z.max())
z_values=np.linspace(zmin,zmax,100)
pdf_values= norm.pdf(z_values, loc=0, scale=1)
plt.plot(z_values, pdf_values, color='red', linewidth=2)

plt.show()
plt.clf()

# t분포
# X~t(df)
# 자유도가 4인 t분포의 pdf를 그려보세요
from scipy.stats import t

t_values=np.linspace(-4,4,100)
pdf_values= t.pdf(t_values, df=5)
plt.plot(t_values, pdf_values, color='red', linewidth=2)

#표준정규분포 겹치기
z_values=np.linspace(-4,4,100)
pdf_values2= norm.pdf(z_values, loc=0, scale=1)
plt.plot(z_values, pdf_values2, color='black', linewidth=2)

#자유도가 낮을 경우 t분포의 꼬리가 길게 나타남
#(fat tale, 극단값이 더 많이 나타남)
#자유도가 커질수록 표준정규분포에 가까워짐

plt.show()
plt.clf()

#X ~ ?(mu, sigma^2)
#X bar ~ N(mu, sigma^2/n)
#X bar ~= t(x_bar, s^2/n) 자유도가 n-1인 t분포
x=norm.rvs(loc=15, scale=3, size=16, random_state=42)
x
x_bar=x.mean()
n=len(x)

#df. (degree of freedom)
#모분산을 모를 때:모평균에 대한 95% 신뢰구간을 구해보자
x_bar + t.ppf(0.975, df=n-1) * np.std(x, ddof=1)/np.sqrt(n)
x_bar - t.ppf(0.975, df=n-1) * np.std(x, ddof=1)/np.sqrt(n)

#모분산(3^2)을 알 때:모평균에 대한 95% 신뢰구간을 구해보자
x_bar + norm.ppf(0.975, loc=0, scale=1) * 3/np.sqrt(n)
x_bar - norm.ppf(0.975, loc=0, scale=1) * 3/np.sqrt(n)



import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

x=np.linspace(0,100,400)
y=2*x+3

# np.random.seed(20240805)
obs_x=np.random.choice(np.arange(100),20)
epsilon_i=norm.rvs(loc=0, scale=100, size=20)

obs_y=2 * obs_x + 3 + epsilon_i

plt.plot(x,y, color = 'k')
plt.scatter(obs_x,obs_y, color='blue', s=3)

obs_x=obs_x.reshape(-1,1)

model = LinearRegression()
model.fit(obs_x, obs_y)

a=model.coef_[0]
b=model.intercept_

y_reg = a * x + b
plt.plot(x,y_reg, color = 'red')

plt.xlim(0,100)
plt.ylim(0,300)
plt.show()
plt.clf()

import statsmodels.api as sm

obs_x = sm.add_constant(obs_x)
model = sm.OLS(obs_y,obs_x).fit()
print(model.summary())



1-norm.cdf(18, loc = 10, scale = 1.96)
1-norm.cdf(4.08, loc = 0, scale = 1)


## 신형 자동차의 에너지 소비효율 등급 (p.57)

# H_0 : mu>=16
# H_A : mu<16

eff=np.array([15.078, 15.752, 15.549, 15.56, 16.098, 13.277, 15.462, 16.116, 15.214, 16.93, 14.118, 14.927,
15.382, 16.709, 16.804])

x_bar=eff.mean()
s=np.std(eff, ddof=1)
n=len(eff)

t=(x_bar-16)/(s/np.sqrt(n))
p_val = norm.cdf(-1.85, loc=0, scale=1)

from scipy.stats import t

z_0025 = t.ppf(0.975, df=n-1)

l_ci = x_bar - z_0025 * s/np.sqrt(n)
r_ci = x_bar + z_0025 * s/np.sqrt(n)
l_ci
r_ci

import numpy as np
#Q1
x=np.arange(2,13)
P_x=np.array([1,2,3,4,5,6,5,4,3,2,1])/36
E=sum(x*P_x)
var=sum(((x-E)**2)*P_x)
E,var

#Q2
E2=2*E+3
std2=np.sqrt(4*var)
E2,std2

# X~N(30, 4^2)
# P(X > 24)
from scipy.stats import norm
1-norm.cdf(24, loc=30, scale=4)

# 표본 8개를 뽑아서 표본평균 X_bar
# P (28 < X_bar < 29.7)
norm.cdf(29.7, loc=30, scale=4/np.sqrt(8))-norm.cdf(28, loc=30, scale=4/np.sqrt(8))




# 자유도 7인 카이제곱분포 확률밀도함수 그리기
from scipy.stats import chi2
import matplotlib.pyplot as plt
k = np.linspace(-2, 40, 1000)
y = chi2.pdf(k, df=7)
plt.plot(k, y, color="black")

## 독립성 검정
# 귀무가설: 두 변수 독립
# 대립가설: 두 변수 독립 x
mat_a=np.array([14,4,0,10]).reshape(2,2)
mat_a

from scipy.stats import chi2_contingency

chi2, p, df, expected = chi2_contingency(mat_a, correction=False)
chi2.round(3) # 검정통계량
p # p-value
((mat_a-expected)**2/expected).sum()

# 유의수준 0.05 이라면,
# p값이 0.05보다 작으므로, 귀무가설을 기각
# 즉, 두 변수는 독립 아니다
from scipy.stats import chi2
p=1-chi2.cdf(15.556, df=1)
p


# 귀무가설 : 두 도시에서의 음료 선호도가 동일하다.
# 대립가설 : 두 도시에서의 음료 선호도가 동일하지 않다.
mat_b=np.array([50,30,20,45,35,20]).reshape(2,3)
mat_b

chi2, p, df, expected = chi2_contingency(mat_b, correction=False)
chi2.round(3) # 검정통계량
p.round(4) # p-value
expected
# 귀무가설 기각하지 못함
import numpy as np
from scipy.stats import chi2
from scipy.stats import chi2_contingency

# 통계교재 p.112
# 귀무가설 : 정당 지지와 핸드폰 사용 유무는 독립이다.
# 대립가설 : 정당 지지와 핸드폰 사용 유무는 독립이 아니다.
mat=np.array([49,47,15,27,32,30]).reshape(3,2)
mat
chi2, p, df, expected = chi2_contingency(mat, correction=False)
expected
chi2.round(3) # 검정통계량
p.round(4) # p-value
# 유의수준 0.05보다 p값이 크므로, 귀무가설을 기각할 수 없다.

from scipy.stats import chisquare
import numpy as np
observed = np.array([13, 23, 24, 20, 27, 18, 15])
expected = np.repeat(20, 7)
statistic, p_value = chisquare(observed, f_exp=expected)
print("Test statistic: ", statistic.round(3))
## Test statistic: 7.6
print("p-value: ", p_value.round(3))
## p-value: 0.269

# 지역별 후보 지지율
# 귀무가설: 후보 A의 지지에 있어서 선거구 간의 차이는 없다
# 대립가설: 후보 A의 지지에 있어서 선거구 간의 차이가 있다
mat_b = np.array([[176, 124], [193, 107], [159, 141]])
mat_b
chi2, p, df, expected = chi2_contingency(mat_b, correction=False)
expected
chi2.round(3) # 검정통계량
p.round(4) # p-value 귀무가설 기각, 차이가 있다.


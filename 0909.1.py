import numpy as np
import pandas as pd
import statsmodels.api as sm


## 문제 1.
# 데이터를 로드하고, 로지스틱 회귀모델을 적합하고, 회귀 표를 작성하세요.
df = pd.read_csv('data/leukemia_remission.txt', sep='\t')
df
df.columns
df.dtypes

model = sm.formula.logit("REMISS ~ CELL + SMEAR + INFIL + LI + BLAST + TEMP", data=df).fit()

print(model.summary())


## 문제 2.
# 해당 모델은 통계적으로 유의한가요? 그 이유를 검정통계량를 사용해서 설명하시오.
from scipy.stats import chi2
p_val=1-chi2.cdf(-2*(-17.186 + 10.797), df=6)
p_val
#p-value: 0.04669995098322843 이므로 유의수준 0.05보다 작다 --> 유의함


## 문제 3.
# 유의수준이 0.2를 기준으로 통계적으로 유의한 변수는 몇개이며, 어느 변수 인가요?
from scipy.stats import norm
(1-norm.cdf(30.8301/52.135))*2 # cell 0.5542850639621408
(1-norm.cdf(24.6863/61.526))*2 # smear 0.6882481267876992
(norm.cdf(-24.9745/65.281))*2 # infil 0.702039210194285
(1-norm.cdf(4.3605/2.658))*2 # li 0.10089726232517515 < 0.2
(norm.cdf(-0.0115/2.266))*2 # blast 0.9959507356304004 
(norm.cdf(-100.1734/77.753))*2 # temp 0.19762271242612317 < 0.2
# 유의수준 0.2를 기준으로 통계적으로 유의한 변수는 2개, 유의한 변수는 LI(0.101), TEMP(0.198)이다.


## 문제 4. 다음 환자에 대한 오즈는 얼마인가요?
# CELL (골수의 세포성): 65%
# SMEAR (골수편의 백혈구 비율): 45%
# INFIL (골수의 백혈병 세포 침투 비율): 55%
# LI (골수 백혈병 세포의 라벨링 인덱스): 1.2
# BLAST (말초혈액의 백혈병 세포 수): 1.1세포/μL
# TEMP (치료 시작 전 최고 체온): 0.9
log_odds = 64.2581 + 30.8301 * 0.65 + 24.6863 * 0.45 - 24.9745 * 0.55 + 4.3605 * 1.2 - 0.0115 * 1.1 - 100.1734 * 0.9
odds = np.exp(log_odds)
odds # 0.03817459641135519


## 문제 5.
# 위 환자의 혈액에서 백혈병 세포가 관측되지 않은 확률은 얼마인가요?
p_hat = odds / (odds + 1)
p_hat # 0.03677088280074742


## 문제 6. 
# TEMP 변수의 계수는 얼마이며, 해당 계수를 사용해서 TEMP 변수가 백혈병 치료에 대한 영향을 설명하시오.
# -100.1734
np.exp(-100.1734)*100 
# temp가 1 증가할때 REMISS에 대한 오즈가 3.1278444454718354e-42[%] 로 감소한다. 즉 백혈병 세포가 관측될 확률이 증가한다.


## 문제 7. CELL 변수의 99% 오즈비에 대한 신뢰구간을 구하시오.
z = norm.ppf(0.995,0,1)
r_ci = np.exp(30.8301 + z * 52.135)
l_ci = np.exp(30.8301 - z * 52.135)
l_ci, r_ci


## 문제 8. 주어진 데이터에 대하여 로지스틱 회귀 모델의 예측 확률을 구한 후, 50% 이상인 경우 1로 처리하여, 혼동 행렬를 구하시오.
df_x=df.drop(["REMISS"], axis=1)
df_y=df["REMISS"]

y_pred = model.predict(df_x).round().astype(int)

from sklearn.metrics import confusion_matrix
conf_mat=confusion_matrix(y_true=df_y, 
                          y_pred=y_pred,
                          labels=[1, 0])
conf_mat


## 문제 9. 해당 모델의 Accuracy는 얼마인가요?
(conf_mat[0][0]+conf_mat[1][1])/conf_mat.sum() # 0.7407407407407407


## 문제 10. 해당 모델의 F1 Score를 구하세요.
precision=conf_mat[0][0]/(conf_mat[0][0]+conf_mat[1][0])
recall=conf_mat[0][0]/(conf_mat[0][0]+conf_mat[0][1])

f1=2/((1/precision)+(1/recall))
f1 # 0.5882352941176471
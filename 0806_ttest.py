import numpy as np
import pandas as pd
from scipy.stats import ttest_1samp

tab3 = pd.read_csv('data/tab3.csv')
tab3

# tab1 = tab3.iloc[:,:-1]
# tab1['id']=np.arange(1,13)
# tab1

tab1 = pd.DataFrame({'id': np.arange(1,13),
                     'score' : tab3['score']})
tab1
                     
tab2 = pd.DataFrame({'id': np.arange(1,13),
                     'score' : tab3['score'],
                     'gender' : ['female']*7 + ['male']*5})
tab2


## 1표본 t검정
# 귀무가설 vs. 대립가설
# H_0 : mu = 0 vs. H_A : mu != 10
from scipy.stats import ttest_1samp
result = ttest_1samp(tab1['score'], popmean=10, alternative='two-sided')
result[0] # t 검정통계량
result[1] # 유의확률 p-value
result.df
ci = result.confidence_interval(confidence_level=0.95)
ci[0]
ci[1]
# 유의확률 0.0648이 유의수준 0.05보다 크므로 귀무가설을 기각하지 못한다.

## 2표본 t 검정 - 분산 같고, 다를 때
# 분산 같은 경우 : 독립 2표본 t검정
# 분산 다른 경우 : 웰치스 t검정
# 귀무가설 vs. 대립가설
# H_0 : mu_m = mu_f vs. H_A : mu_m > mu_f
#유의수준 1%로 설정, 두 그룹 분산 같다고 가정한다.

# male = tab2.query("gender=='male'")
# female = tab2.query("gender=='female'")
male = tab2[tab2['gender'] == 'male']
female = tab2[tab2['gender'] == 'female']

# alternative='less'의 의미는 대립가설이 첫번째 입력 그룹의 평균이
# 두번째 입력 그룹 평균보다 작다고 설정된 경우를 나타냄
from scipy.stats import ttest_ind
result = ttest_ind(female['score'], male['score'],
                   equal_var=True, alternative='less')
# result = ttest_ind(male['score'], female['score'],
#                    equal_var=True, alternative='greater')
result


## 대응표본 t검정 (짝지을 수 있는 표본)
# H_0 : mu_before = mu_after vs. H_A : mu_after > mu_before
# H_0 : mu_d = 0 vs. H_A : mu_d > 0
# mu_d = mu_after - mu_before
tab3
tab3_data = tab3.pivot_table(index='id', columns='group', values='score')
tab3_data
#
tab3.pivot(index='id', columns='group', values='score')
pd.melt(tab3_data)
tab3_data.melt(id_vars='id', value_vars=['before','after'], var_name='group', value_name='score')

tab3_data['score_diff'] = tab3_data['after'] - tab3_data['before']
test3_data = tab3_data[['score_diff']]
test3_data

from scipy.stats import ttest_1samp
result = ttest_1samp(test3_data['score_diff'], popmean=0, alternative='greater')
result

# 연습1
df = pd.DataFrame({'id':[1,2,3],
                   'A':[10,20,30],
                   'B':[40,50,60]})
df
df_long=df.melt(id_vars='id', value_vars=['A','B'], var_name='group', value_name='score')
pd.melt(df)


df_long.pivot_table(index='id', columns='group', values='score')

# 연습2
import seaborn as sns
tips = sns.load_dataset('tips')
tips
tips.pivot(columns='day', values='tip').reset_index()
tips_new=tips.reset_index(drop=False)\
        .pivot_table(index=['index'],columns=['day'], values='tip').reset_index()
tips_drop=tips.drop(columns=['day','tip'])
pd.concat([tips_new, tips_drop], axis=1).drop(columns='index')


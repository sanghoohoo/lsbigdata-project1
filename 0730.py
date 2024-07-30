import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 9.1
raw_welfare = pd.read_spss('data/Koweps_hpwc14_2019_beta2.sav')
welfare=raw_welfare.copy()
welfare.shape
welfare.info()
welfare.describe()

welfare = welfare.rename(
    columns = {'h14_g3' : 'sex',
               'h14_g4' : 'birth',
               'h14_g10' : 'marriage_type',
               'h14_g11' : 'religion',
               'p1402_8aq1' : 'income',
               'h14_eco9' : 'code_job',
               'h14_reg7' : 'code_religion',}
)

welfare = welfare[['sex','birth', 'marriage_type', 'religion',
                   'income', 'code_job', 'code_religion']]
                   
welfare.shape

# 9.2
welfare['sex'].dtypes
welfare['sex'].value_counts()
welfare['sex']=np.where(welfare['sex']==9, np.nan, welfare['sex'])
welfare['sex'].isna().sum()
welfare['sex']=np.where(welfare['sex']==1, 'male', 'female')
welfare['sex'].value_counts()

sns.countplot(data=welfare, x='sex', hue='sex')
plt.show()
plt.clf()

welfare['income'].dtypes
welfare['income'].describe()
sns.histplot(data=welfare, x='income')
plt.show()
plt.clf()

welfare['income'].isna().sum()
welfare['income']=np.where(welfare['income']==9999, np.nan, welfare['income'])

sex_income = welfare.dropna(subset = 'income')\
                    .groupby('sex', as_index = False)\
                    .agg(mean_income = ('income', 'mean'))
sex_income

sns.barplot(data = sex_income, x = 'sex', y = 'mean_income', hue = 'sex')
plt.show()
plt.clf()
# 숙제
# 위 그래프에서 각 성별 95% 신뢰구간 계산 후 그리기, 위아래 검정색 막대기로 표시

# 9.3
welfare['birth'].dtypes
welfare['birth'].describe()
sns.histplot(data = welfare, x = 'birth')
plt.show()
plt.clf()
welfare['birth'].describe()


welfare['birth'].isna().sum()
welfare['birth']=np.where(welfare['birth']==9999, np.nan, welfare['birth'])

welfare = welfare.assign(age=2019-welfare['birth']+1)
welfare['age'].describe()
sns.histplot(data=welfare, x='age')
plt.show()
plt.clf()

age_income = welfare.dropna(subset='income')\
                    .groupby('age')\
                    .agg(mean_income = ('income','mean'))
age_income.head()

sns.lineplot(data=age_income, x='age', y='mean_income')
plt.show()
plt.clf()

sum(welfare['income']==0)

my_df=welfare.assign(income_na=welfare['income'].isna())\
            .groupby('age', as_index=False).agg(n=('income_na','sum'))
sns.barplot(data = my_df, x='age', y='n')
plt.xticks(size=2, rotation=45)
plt.show()
plt.clf()

# 9.4
welfare['age'].head()
welfare=welfare.assign(ageg=np.where(welfare['age']<30, 'young',
                            np.where(welfare['age']<=59, 'middle', 'old')))
                            
welfare['ageg'].value_counts()
sns.countplot(data=welfare, x='ageg', hue= 'ageg')
plt.show()
plt.clf()

ageg_income = welfare.dropna(subset='income')\
                     .groupby('ageg', as_index=False)\
                     .agg(mean_income=('income','mean'))
sns.barplot(data=ageg_income, x='ageg', y='mean_income',
            order=['young', 'middle', 'old'], hue='ageg')
plt.show()
plt.clf()

#/09/ 10 19/ 20 29 /30 39
welfare['age'].max()

bins=np.array([0,9,19,29,39,49,59,69,79,89,99,109,119])
welfare['ages']=pd.cut(welfare['age'], bins,
                       labels=(np.arange(12)*10).astype(str)+['s'])
                       
ages_income = welfare.groupby('ages', as_index=False)\
                     .agg(mean_income=('income','mean'))
sns.barplot(data=ages_income, x='ages', y='mean_income', hue='ages')
plt.xticks(size=7)
plt.show()
plt.clf()

# 9.5
sex_income = welfare.dropna(subset = 'income')\
                    .groupby(['ageg', 'sex'], as_index=False)\
                    .agg(mean_income = ('income','mean'))
sex_income
sns.barplot(data=sex_income, x='ageg', y='mean_income', hue='sex',
            order=['young', 'middle', 'old'])
plt.show()
plt.clf()

# 판다스 데이터 프레임을 다룰 때, 변수의 타입이 카테고리로 설정되어 있는 경우,
# groupby + .agg 콤보 안먹힘.
# 그래서 object 타입으로 변경해준 후 수행
welfare['ages']=welfare['ages'].astype('object')
sex_income2 = welfare.dropna(subset = 'income')\
                     .groupby(['ages', 'sex'], as_index=False)\
                     .agg(mean_income = ('income','mean'))
sex_income2
sns.barplot(data=sex_income2, x='ages', y='mean_income', hue='sex')
plt.show()
plt.clf()

#각 연령대별 성별 상위 4% 수입
sex_income3 = welfare.dropna(subset = 'income')\
                     .groupby(['ages', 'sex'], as_index=False)\
                     .agg(top4per_income = ('income',lambda x: np.quantile(x, q=0.96)))sex_income3
sns.barplot(data=sex_income3, x='ages', y='top4per_income', hue='ages')
plt.show()
plt.clf()

#사용자 정의 함수 사용하는 방법
#def top_4_percentile(x):
#    return np.quantile(x, 0.96)
#custom_top4per_income = welfare.groupby(['ages', 'sex'], as_index=False)\
                               .agg(top4per_income=('income', top_4_percentile))

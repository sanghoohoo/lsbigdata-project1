import pandas as pd
import numpy as np
data=pd.read_csv('data/fire.csv')
print(data.columns)
data_2020 = data[['행정구역별'] + data.filter(like='2020').columns.tolist()]
data_2020
data_2020.columns = data_2020.iloc[0]
data_2020 = data_2020[1:]
data_2020 = data_2020.reset_index(drop=True)
data_2020
data_2020_pop = data_2020.iloc[:, 0:4]
data_2020_pop
data_2020_pop['사망 (명)'] = pd.to_numeric(data_2020_pop['사망 (명)'])
data_2020_pop['부상 (명)'] = pd.to_numeric(data_2020_pop['부상 (명)'])
data_2020_pop['건수 (건)'] = pd.to_numeric(data_2020_pop['건수 (건)'])
data_2020_pop.info()
pop=data_2020_pop

# 변수명 변경
pop = pop.rename(columns = {"건수 (건)" : "건수"})
pop = pop.rename(columns = {"사망 (명)" : "사망자수"})
pop = pop.rename(columns = {"부상 (명)" : "부상자수"})

# 인명 피해
pop["total"] = pop["사망자수"] + pop["부상자수"]
pop.head()

# 위험도 추가
count_mean = 38659/17  #평균
pop["위험도"] = np.where(pop["건수"] >= count_mean, "dan", "saf")
pop.head()

# 빈도 막대 그래프
pop["위험도"].value_counts().plot.bar(rot=0) #rot=0 : 축 이름 수평
plt.show()

# 시도별 인명피해 그래프
pop["total"].plot.bar(rot = 0)
plt.show()

plt.clf()


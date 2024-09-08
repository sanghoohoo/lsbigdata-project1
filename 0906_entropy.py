import pandas as pd
import numpy as np
from palmerpenguins import load_penguins
import seaborn as sns
import matplotlib.pyplot as plt

penguins = load_penguins()
penguins.head()

# 펭귄 분류 문제
# y: 펭귄의 종류
# x1: bill_length_mm (부리 길이) 
# x2: bill_depth_mm (부리 깊이)

df=penguins.dropna()
df=df[["species", "bill_length_mm", "bill_depth_mm"]]
df=df.rename(columns={
    'species': 'y',
    'bill_length_mm': 'x1',
    'bill_depth_mm': 'x2'})
df

sns.scatterplot(data = df, x = 'x1', y = 'x2', hue = "y")
plt.axvline(x = 45)

# Q. 나누기 전 현재의 엔트로피?
# Q. 45로 나눴을때, 엔트로피 평균은 얼마인가요?
# 입력값이 벡터 -> 엔트로피!
p_i=df['y'].value_counts() / len(df['y'])
entropy_curr=-sum(p_i * np.log2(p_i))

# x1=45 기준으로 나눈 후, 평균 엔트로피 구하기!
# x1=45 기준으로 나눴을때, 데이터포인트가 몇개 씩 나뉘나요?
n1=df.query("x1 < 45").shape[0]  # 1번 그룹
n2=df.query("x1 >= 45").shape[0] # 2번 그룹

# 1번 그룹은 어떤 종류로 예측하나요?
# 2번 그룹은 어떤 종류로 예측하나요?
y_hat1=df.query("x1 < 45")['y'].mode()
y_hat2=df.query("x1 >= 45")['y'].mode()

# 각 그룹 엔트로피는 얼마 인가요?
p_1=df.query("x1 < 45")['y'].value_counts() / len(df.query("x1 < 45")['y'])
entropy1=-sum(p_1 * np.log2(p_1))

p_2=df.query("x1 >= 45")['y'].value_counts() / len(df.query("x1 >= 45")['y'])
entropy2=-sum(p_2 * np.log2(p_2))

entropy_x145=(n1 * entropy1 + n2 * entropy2)/(n1 + n2)
entropy_x145

###
# 엔트로피 구해주는 함수
def my_entropy(x):
    n1=df.query(f"x1 < {x}").shape[0]  # 1번 그룹
    n2=df.query(f"x1 >= {x}").shape[0] # 2번 그룹

    p_1=df.query(f"x1 < {x}")['y'].value_counts() / len(df.query(f"x1 < {x}")['y'])
    entropy1=-sum(p_1 * np.log2(p_1))

    p_2=df.query(f"x1 >= {x}")['y'].value_counts() / len(df.query(f"x1 >= {x}")['y'])
    entropy2=-sum(p_2 * np.log2(p_2))

    entropy_x1=(n1 * entropy1 + n2 * entropy2)/(n1 + n2)
    return entropy_x1

# 최적 기준값
x_values=df['x1'].unique()
x_values.shape[0]
result=np.repeat(0.0, 163)
for i in range(163):
    result[i]=my_entropy(x_values[i])

result.min() # 0.8042691471139144
x_values[np.argmin(result)] #42.4

# 최적 기준값
x_values=np.arange(df['x1'].min(), df['x1'].max(), 0.1)
x_values.shape[0]
result=np.repeat(0.0, 275)
for i in range(275):
    result[i]=my_entropy(x_values[i])

result.min() # 0.8042691471139144
x_values[np.argmin(result)] #42.300000000000146 -->42.4
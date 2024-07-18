import numpy as np
import pandas as pd

a = np.array([1, 2, 3, 4])
b = np.array([1, 2])

a = np.array([1.0, 2.0, 3.0])
b = 2.0
a * b

a.shape
b.shape

type(a)
type(b)

a+b

matrix = np.array([[ 0.0, 0.0, 0.0],
[10.0, 10.0, 10.0],
[20.0, 20.0, 20.0],
[30.0, 30.0, 30.0]])
matrix.shape
vector = np.array([1.0, 2.0, 3.0, 4.0]).reshape(4,1)
vector
vector.shape
result = matrix + vector
print("브로드캐스팅 결과:\n", result)

np.random.seed(2024)
a= np.random.randint(1,21,10)
a

a[1]
a[2:5]
a[-2]
a[::2]
a[1:6:2]

a=np.arange(3,1001)
a
a[::3].sum()

a[[0,2,4]]
np.delete(a,1)
np.delete(a,[1,3])

a
a > 3
a[a > 3]
b = a[a > 3]
print(b)

np.random.seed(2024)
a= np.random.randint(1,10000,5)
a
a>2000
a<5000
(a>2000)&(a<5000)
a[(a>2000)&(a<5000)]

import pydataset

df=pydataset.data('mtcars')
np_df=np.array(df['mpg'])
df
np_df

n=(np_df>=15)&(np_df<=25)
n.sum()

(np_df>=np_df.mean()).sum()

np.random.seed(2024)
a= np.random.randint(1,10000,5)
b= np.array(['A','B','C','F','W'])
a[(a>2000)&(a<5000)]
b[(a>2000)&(a<5000)]

model_names=np.array(df.index)
model_names[(np_df>=np_df.mean())]
model_names[(np_df<np_df.mean())]
model_names[n]

a[a>3000]=3000
a

np.random.seed(2024)
a= np.random.randint(1,100,10)
a
np.where(a<50)

np.random.seed(2024)
a= np.random.randint(1,26346,1000)
a

b=np.where(a>10000)
b
my_index=b[0][49]
my_index
a[my_index]

b=np.where(a<500)
b
my_index=b[0][-1]
my_index
a[my_index]

a=np.array([20,np.nan,13,24,309])
a
a+3
np.mean(a)
np.nanmean(a)
np.nan_to_num(a, nan=0)

a=None
b=np.nan
a
b
b+1
a+1
a=np.array([20,np.nan,13,24,309])
np.isnan(a)

a_flitered=a[~np.isnan(a)]
a_flitered

import numpy as np
str_vec = np.array(["사과", "배", "수박", "참외"])
str_vec
str_vec[[0, 2]]

mix_vec = np.array(["사과", 12, "수박", "참외"], dtype=str)
mix_vec

combined_vec = np.concatenate((str_vec, mix_vec))
combined_vec

col_stacked=np.column_stack((np.arange(1,5),np.arange(12,16)))
col_stacked
row_stacked = np.vstack((np.arange(1, 5), np.arange(12, 16)))
row_stacked

vec1 = np.arange(1, 5)
vec2 = np.arange(12, 18)
vec1 = np.resize(vec1, len(vec2))
vec1

uneven_stacked = np.column_stack((vec1, vec2))
uneven_stacked
uneven_stacked1 = np.vstack((vec1, vec2))
uneven_stacked1

a = np.array([1, 2, 3, 4, 5])
a+5

a = np.array([12, 21, 35, 48, 5])
a
a[0::2]

a = np.array([1, 2, 3, 2, 4, 5, 4, 6])
a
np.unique(a)

a = np.array([21, 31, 58])
b = np.array([24, 44, 67])
a
b
c=np.empty(6)
c
c[0::2]=a
c[1::2]=b
c

import pandas as pd
import numpy as np
df=pd.DataFrame({'name':['김지훈','이유진','박동현','김민지'],
                 'english':[90,80,60,70],
                 'math':[50,60,100,20]})
df
type(df)
type(df["name"])

df['english'].sum()

fruits=pd.DataFrame({
    '제품':['사과','딸기','수박'],
    '가격':[1800,1500,3000],
    '판매량':[24,38,13]})
fruits
fruits['가격'].mean()
fruits['판매량'].mean()

df_exam=pd.read_excel('data/excel_exam.xlsx')
df_exam

sum(df_exam['english'])/20
sum(df_exam['science'])/20

df_exam.shape
df_exam.size
len(df_exam)

df_exam['math']
df_exam['english']
df_exam['science']
df_exam['total']=df_exam['math']+df_exam['english']+df_exam['science']
df_exam['mean']=df_exam['total']/3
df_exam

df_exam[(df_exam['math']>50)&(df_exam['english']>50)]

mean_math=df_exam['math'].mean()
mean_eng=df_exam['english'].mean()

df_exam[(df_exam['math']>mean_math)&(df_exam['english']<mean_eng)]
df_nc3=df_exam[df_exam['nclass']==3]
df_nc3[['math','english','science']]
df_nc3

df_exam[0:10:2]

df_exam.sort_values('math',ascending=False)

#84p 115p 130p

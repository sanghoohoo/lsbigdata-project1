import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

exam=pd.read_csv('data/exam.csv')
exam.head(10)
exam.tail(10)
exam.shape
exam.info()
exam.describe()

type(exam)
var=[1,2,3]
type(var)

exam2=exam.copy()
exam2
exam2=exam2.rename(columns={'nclass':'class'})
exam2
exam2['total']=exam2['math']+exam2['english']+exam2['science']
exam2.head()
exam2['test']=np.where(exam2['total']>=200,'pass','fail')
exam2

count_test=exam2['test'].value_counts()
count_test.plot.bar(rot=0)
plt.show()
plt.clf()

exam2['test2']=np.where(exam2['total']>=200,'A',
               np.where(exam2['total']>=100,'B','C'))
exam2

exam2['test2'].isin(['A','C'])

mpg=pd.read_csv('data/mpg.csv')
mpg['size']=np.where(mpg['category'].isin(['compact','subcompact','2seater']),'small','large')
mpg
mpg['size'].value_counts()
a=np.random.choice(np.arange(1,21),10,False)
a


exam
exam.query('nclass==1')
exam[exam['nclass']==1]

exam.query('math>50')
exam.query('math<50')
exam.query('english>=50')
exam.query('english<=80')
exam.query('nclass==2 & math>=50')
exam.query('nclass in [1,3,5]')
exam[exam['nclass'].isin([1,3,5])]

exam.query('nclass not in [1,3,5]')
exam[~exam['nclass'].isin([1,3,5])]

exam['nclass']
exam[['nclass']]
exam[['id','nclass']]

exam.query('nclass==1')\
[['math','english']]\
.head()

exam.sort_values('math',ascending=False)
exam.sort_values(['nclass','english'],ascending=[True,False])

exam=exam.assign(
    total=exam['math']+exam['english']+exam['science'],
    mean=(exam['math']+exam['english']+exam['science'])/3
    )
exam.sort_values('total')

exam=pd.read_csv('data/exam.csv')
exam2=exam.assign(
    total= lambda x: x['math']+x['english']+x['science'],
    mean= lambda x: x['total']/3
    )
exam2

exam2.agg(mean_math=('math','mean'))
exam2.groupby('nclass').agg(mean_math=('math','mean'))
exam2.groupby('nclass').agg(
    mean_math=('math','mean'),
    mean_english=('english','mean'),
    mean_science=('science','mean'))

mpg=pd.read_csv('data/mpg.csv')
mpg
mpg.query('category=="suv"')\
    .assign(total=(mpg['hwy']+mpg['cty'])/2)\
    .groupby('manufacturer')\
    .agg(mean_tot=('total','mean'))\
    .sort_values('mean_tot',ascending=False)\
    .head()

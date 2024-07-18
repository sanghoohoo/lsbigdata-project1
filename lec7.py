import pandas as pd
import numpy as np

test1=pd.DataFrame({'id':[1,2,3,4,5],
                    'midterm':[60,80,70,90,85]})
                    
test2=pd.DataFrame({'id':[1,2,3,40,5],
                    'midterm':[70,83,65,95,80]})
                    
test1
test2

total=pd.merge(test1,test2,how='left', on='id')
total

total=pd.merge(test1,test2,how='right', on='id')
total

total=pd.merge(test1,test2,how='inner', on='id')
total

total=pd.merge(test1,test2,how='outer', on='id')
total

exam=pd.read_csv('data/exam.csv')
name=pd.DataFrame({'nclass':[1,2,3,4,5],
                   'techer':['kim','lee','park','choi','jung']})
name

exam_new=pd.merge(exam,name,how='left',on='nclass')
exam_new

score1=pd.DataFrame({'id':[1,2,3,4,5],
                    'score':[60,80,70,90,85]})
                    
score2=pd.DataFrame({'id':[6,7,8,9,10],
                    'score':[70,83,65,95,80]})
                    
score_all=pd.concat([score1,score2])
score_all

pd.concat([test1,test2],axis=1)


#Ch.7
df=pd.DataFrame({'sex':['M','F',np.nan,'M','F'],
                 'score':[5,4,3,4,np.nan]})
df
pd.isna(df)

#결측치 제거하기
df.dropna(subset=['score','sex'])
df.dropna()

#데이터 프레임 location을 사용한 인덱싱
exam.loc[[2,7,14],['math']]=np.nan
exam

exam['math'].mean()
exam['math']=exam['math'].fillna(55)
exam

exam['math'].isna().sum()


#수학점수가 50점 이하인 학생들 점수 50점으로 상향조정
exam.loc[exam['math']<=50,'math']=50
exam.iloc[exam['english']>=90,3]=90
exam
#수학점수가 50점 이하인 학생들 점수 -로 변경
exam=pd.read_csv('data/exam.csv')
exam.loc[exam['math']<=50,'math']='-'
exam
#-를 평균으로 변경
exam.loc[exam['math']=='-','math']=np.nan
exam['math']=exam['math'].fillna(exam['math'].mean())
exam

exam.loc[exam['math']=='-','math']=np.nan
exam['math']=np.where(exam['math'==np.nan,exam['math'].mean(),exam['math']])
exam

vector=np.nanmean(np.array([np.nan if x=='-' else float(x) for x in exam['math']]))
vector


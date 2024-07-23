import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
mpg=pd.read_csv('data/mpg.csv')
mpg.shape

sns.scatterplot(data=mpg,
                x='displ', y='hwy')
plt.show()
plt.clf()

sns.scatterplot(data=mpg,
                x='displ', y='hwy',
                hue='drv')\
                .set(xlim=[3,6], ylim=[10,30])
plt.show()
plt.clf()

df_mpg=mpg.groupby('drv', as_index=False)\
    .agg(mean_hwy=('hwy','mean'))

df_mpg
sns.barplot(data=df_mpg.sort_values('mean_hwy',ascending= False),
    x='drv', y='mean_hwy', hue='drv')
plt.show()
plt.clf()

df_mpg_2=mpg.groupby('drv', as_index=False)\
    .agg(count_drv=('drv','count'))
df_mpg_2
sns.barplot(data=df_mpg_2.sort_values('count_drv',ascending= False),
    x='drv', y='count_drv', hue='drv')
plt.show()
plt.clf()

sns.countplot(data=mpg, x='drv')
plt.show()
plt.clf()


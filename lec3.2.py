import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.metrics as met

var=['a','a','b','c']
sns.countplot(x=var)
plt.show()

df=sns.load_dataset('titanic')
df
sns.countplot(data=df, x='sex',hue='sex')
plt.show()

sns.countplot(data=df, y='class', hue='alive')
plt.show()
plt.clf()

sklearn.metrics.accuracy_score()
from sklearn import metrics
metrics.accuracy_score()

met.accuracy_score()



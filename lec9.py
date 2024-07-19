#E[x]
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sum(np.arange(4)*np.array([1,2,2,1])/6)

data=np.random.rand(1000)
plt.hist(data,bins=30,alpha=0.7,color='blue')
plt.title('Histogram of Numpy vector')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
plt.clf()

data1=np.random.rand(50000).reshape(-1,5).mean(axis=1)
#data1=np.random.rand(10000,5).mean(axis=1)
plt.hist(data1,bins=30,alpha=0.7,color='blue')
plt.title('Histogram of Numpy vector')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
plt.clf()

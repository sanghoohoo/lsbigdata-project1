import matplotlib.pyplot as plt
import numpy as np

k=2
x=np.linspace(-4,8,100)
y= (x-2)**2+1
plt.plot(x, y, color='black')
# y= 4*x -11
# plt.plot(x, y, color='red')

l_slope=2*k-4
f_k=(k-2)**2+1
l_intercept=f_k-l_slope*k

line_y=l_slope*x + l_intercept
plt.plot(x, line_y, color='red')

plt.xlim(-4,8)
plt.ylim(0,15)



x=10
lstep=np.arange(100, 0, -1)*0.01

for i in range(100):
    x=x-lstep[i]*(2*x)

x

x=9
y=2
lstep=np.arange(100, 0, -1)*0.1

for i in range(100):
    x=x-lstep[i]*(2*x-6)
    y=y-lstep[i]*(2*y-8)

x
y


beta0=10
beta1=10
lstep=0.01

for i in range(1000):
    beta0=beta0-lstep*(8*beta0+20*beta1-23)
    beta1=beta1-lstep*(20*beta0+60*beta1-67)

round(beta0, 2), round(beta1, 2)
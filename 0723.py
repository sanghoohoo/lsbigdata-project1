import numpy as np

np.arange(33).sum()/33

np.unique((np.arange(33)-16)**2)

sum(np.unique((np.arange(33)-16)**2)*2/33)

x=np.arange(33)
sum(x)/33
sum((x-16)*1/33)
(x-16)**2

np.unique((x-16)**2)*(2/33)
sum(np.unique((x-16)**2)*(2/33))

#E[X^2]
sum(x**2*(1/33))

#Var(X)=E[X^2]-(E[X])^2
sum(x**2*(1/33))-16**2

x=np.arange(4)
x
pro_x=np.array([1/6,2/6,2/6,1/6])
pro_x

#기대값
Ex=sum(x*pro_x)
Exx=sum(x**2*pro_x)

#분산
Exx-Ex**2

sum((x-Ex)**2 *pro_x)

x=np.arange(99)
x
pro_x=np.concatenate([np.arange(1, 51), np.arange(49, 0, -1)])/2500
pro_x
Ex=sum(x*pro_x)
Exx=sum(x**2*pro_x)

Exx-Ex**2

sum((x-Ex)**2 *pro_x)

y=np.arange(0,7,2) #np.arange(4)*2
y
pro_y=np.array([1/6,2/6,2/6,1/6])
Ey=sum(y*pro_y)
Eyy=sum(y**2*pro_y)

Eyy-Ey**2

sum((y-Ey)**2 *pro_y)



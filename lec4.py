a=[1,2,3]
b=a
a[1]=4
a
b

id(a)
id(b)
 b=a.copy()
id(b) 

import math
x=4
math.sqrt(x)
math.exp(5)
math.log(10,10)
math.factorial(5)
math.sin(math.radians(90))
math.cos(math.radians(180))
math.tan(math.radians(45))

def normal_pdf(x, mu, sigma):
sqrt_two_pi = math.sqrt(2 * math.pi)
factor = 1 / (sigma * sqrt_two_pi)
return factor * math.exp(-0.5 * ((x - mu) / sigma) ** 2)

def my_normal_pdf(x,mu,sigma):
  part_1=(sigma*math.sqrt(2*math.pi))**-1
  part_2=math.exp(-(x-mu)**2/2*sigma**2)
  return part_1*part_2

my_normal_pdf(3,3,1)


def my_f(x,y,z):
  return (x**2+math.sqrt(y)+math.sin(z))*math.exp(x)
my_f(2,9,math.pi/2)

def my_g(x):
  return math.cos(x)+math.sin(x)*math.exp(x)
my_g(math.pi)


import numpy as np
a = np.array([1, 2, 3, 4, 5])
b = np.array(["apple", "banana", "orange"])
c = np.array([True, False, True, True])

a
type(a)
a[3]
a[2:]
a[1:4]

b=np.empty(3)
b 
b[0]=1
b[1]=4
b[2]=10
b

vec1=np.arange(100)
vec1

vec1=np.arange(1,100.1,0.5)
vec1

l_space1=np.linspace(0,1,5)
l_space1

l_space2=np.linspace(0,1,5, endpoint=False)
l_space2

vec1=np.array([0,1,2,3,4])
np.repeat(3,5)
np.repeat(vec1,5)
vec2=np.arange(-100,1)
vec2 

np.repeat(vec1,3)
np.tile(vec1,3)
vec1/3
vec1+vec1

max(vec1)
sum(vec1)

odd=np.arange(1,35673,2)
odd
sum(odd)

len(odd)
odd.shape

b = np.array([[1, 2, 3], [4, 5, 6]])
len(b)
b.shape

a=np.array([1,2])
b=np.array([1,2,3,4])
a+b

np.tile(a,2)+b

b==3

(np.arange(1,35672)%7==3).sum()


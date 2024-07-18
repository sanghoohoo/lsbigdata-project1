import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


matrix = np.vstack((np.arange(1, 5),
np.arange(12, 16)))
matrix
print("행렬:\n", matrix)

np.zeros(5)
np.zeros([5,4])

np.arange(1,7).reshape(2,3)
np.arange(1,7).reshape(2,-1)

np.random.seed(2024)
a= np.random.randint(0,100,50).reshape((5,10))
a

np.arange(1,21).reshape((4,5),order='f')
np.arange(1,21).reshape((4,5),order='c')

mat_a=np.arange(1,21).reshape((4,5),order='f')
mat_a

mat_a[0,0]
mat_a[1,1]
mat_a[2,3]
mat_a[:2,3]
mat_a[1:3,1:4]

mat_a[3,::2]
mat_a[1::2,:]

mat_b=np.arange(1,101).reshape((20,-1))
mat_b
mat_b[1::2,:]

mat_b[[1,4,6,14],]

x=np.arange(1,11).reshape((5,2))*2
x[[True,True,False,False,True],0]
mat_b[:,1].reshape((-1,1))
mat_b[:,(1,)]

mat_b[mat_b[:,1]%7==0,:]

mat_b[mat_b[:,1]>50,:]
mat_b.iloc[]

np.random.seed(2024)
img1 = np.random.rand(3, 3)
print("이미지 행렬 img1:\n", img1)
plt.imshow(img1, cmap='gray', interpolation='nearest')
plt.colorbar()
plt.show()
plt.clf()

a=np.array([[9,9,9,9,9,9,9,9,9,9],
            [9,9,0,0,0,0,0,0,9,9],
            [9,9,7,7,7,7,7,7,9,9],
            [9,9,7,0,7,7,0,7,9,9],
            [9,7,7,7,7,7,7,7,7,9],
            [9,9,7,0,7,7,0,7,9,9],
            [9,9,7,7,0,0,7,7,9,9],
            [9,9,7,7,7,7,7,7,9,9],
            [9,9,9,9,7,7,9,9,9,9],
            [9,9,3,3,7,7,3,3,9,9],
            [9,9,3,3,3,3,3,3,9,9],
            [9,9,3,3,3,3,3,3,9,9]])
            
            
a=a/9
plt.imshow(a, cmap='gray', interpolation='nearest')
plt.axis('off')
plt.show()
plt.clf()

b=np.array([[0,0,0,0,0,0,0,0,0,0],
            [0,9,9,0,0,0,0,9,9,0],
            [0,0,9,9,9,9,9,9,0,0],
            [0,9,9,3,9,9,3,9,9,0],
            [0,9,9,9,9,9,9,9,9,0],
            [0,9,9,3,3,3,3,9,9,0],
            [0,0,9,9,9,9,9,9,0,0],
            [0,0,9,9,9,9,9,9,9,0],
            [0,0,9,9,9,9,9,9,0,0],
            [0,0,9,9,0,0,9,9,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,7,7,7,7,0,0,0],
            [0,0,7,7,7,7,7,7,0,0],
            [0,0,0,0,0,0,0,0,0,0]
         ])
b=b/9
plt.imshow(b, cmap='gray', interpolation='nearest')
plt.axis('off')
plt.show()
plt.clf()

import urllib.request
img_url = "https://bit.ly/3ErnM2Q"
urllib.request.urlretrieve(img_url, "jelly.png")

#!pip install imageio
import imageio
jelly = imageio.imread("jelly.png")
print("이미지 클래스:", type(jelly))
print("이미지 차원:", jelly.shape)
print("이미지 첫 4x4 픽셀, 첫 번째 채널:\n", jelly[:4, :4, 0])

plt.imshow(jelly)
plt.imshow(jelly[:,:,0].transpose())
plt.imshow(jelly[:,:,0])
plt.imshow(jelly[:,:,1])
plt.imshow(jelly[:,:,2])
plt.imshow(jelly[:,:,3])
plt.axis('off')
plt.show()
plt.clf()

mat1 = np.arange(1, 7).reshape(2, 3)
mat2 = np.arange(7, 13).reshape(2, 3)

my_array = np.array([mat1, mat2])
my_array
my_array.shape

my_array2 = np.array([my_array, my_array])
my_array2
my_array2.shape

first_slice = my_array[0, :, :]
print("첫 번째 2차원 배열:\n", first_slice)

filtered_array = my_array[:, :, :-1]
print("세 번째 요소를 제외한 배열:\n", filtered_array)

filtered_array2 = my_array[:, :,[0,2]]
print(filtered_array2)

filtered_array3 = my_array[:, 0,:]
print(filtered_array3)

filtered_array4 = my_array[0, 1,1:]
print(filtered_array4)

mat_x = np.arange(1, 101).reshape((5,5,4))
mat_x

a=np.array([[1,2,3],[4,5,6]])
a.sum()
a.sum(axis=1)
a.sum(axis=0)
a.mean()
a.mean(axis=0)
a.mean(axis=1)

mat_b=np.random.randint(1,100,50).reshape((5,-1))
mat_b

mat_b.max()
mat_b.max(axis=0)
mat_b.max(axis=1)

a.cumsum()
mat_b.cumsum()
mat_b.cumsum(axis=0)
mat_b.cumsum(axis=1)
mat_b

mat_b.cumprod()
a.cumprod()

mat_b.flatten()

d = np.array([1, 2, 3, 4, 5])
print("클립된 배열:", d.clip(2, 4))


np.random.rand()


def X(n):
    return np.random.rand(n)
X(1)

#베르누이 확률변수 모수:P
def Y(n,p):
    x=np.random.rand(n)
    return np.where(x<p,1,0)

Y(100000000,0.5).mean()

p=np.array([0.2,0.5,0.3])
def Z(n,p):
    x=np.random.rand(n)
    p_cumsum=p.cumsum()
    return np.where(x<p_cumsum[0],0,
           np.where(x<p_cumsum[1],1,2))
np.bincount(Z(100000,p))/100000

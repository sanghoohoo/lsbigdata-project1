import numpy as np

# 벡터 * 벡터 (내적)
a = np.arange(1,4)
b = np.array([3,6,9])

a.dot(b)

# 행렬 * 행렬
a = np.array([1,2,3,4]).reshape((2,2), order='F')
b = np.array([5,6,7,8]).reshape((2,2), order='F')

a.dot(b)
a@b #똑같다

# Q1
a = np.array([1,2,1,0,2,3]).reshape(2,3)
b = np.array([1,0,-1,1,2,3]).reshape(3,2)
a@b

# Q2
np.eye(3)
a = np.array([3,5,7,
              2,4,9,
              3,1,0]).reshape(3,3)
# np.array([[3,5,7],
#           [2,4,9],
#           [3,1,0]])
a @ np.eye(3)
np.eye(3) @ a

a.transpose()



b = a[:,:2]
b.transpose()

# 회귀분석 데이터행렬
x = np.array([13,15,
              12,14,
              10,11,
              5,6]).reshape(4,2)
vec1 = np.repeat(1,4).reshape(4,1)
matX = np.hstack((vec1, x))

beta_vec = np.array([2,0,1]).reshape(3,1)
matX @ beta_vec

y = np.array([20,19,20,12]).reshape(4,1)
(y - matX @ beta_vec).transpose() @ (y - matX @ beta_vec)

# 역행렬
np.array([1,5,3,4]).reshape(2,2) @ ((-1/11) * np.array([4,-5,-3,1]).reshape(2,2))

a = np.array([-4,-6,2,5,-1,3,-2,4,-3]).reshape(3,3)
np.linalg.det(a)
a_inv = np.linalg.inv(a)
np.round(a @ a_inv)

# 역행렬 존재하지 않는 경우 (선형종속)
b = np.array([1,2,3,2,4,6,3,5,7]).reshape(3,3)
# np.linalg.inv(b)
np.linalg.det(b)

## 벡터 형태로 베타 구하기
XtX_inv = np.linalg.inv((matX.transpose() @ matX))
XtY = matX.transpose() @ y
beta_hat = XtX_inv @ XtY
beta_hat

## model.fit으로 베타 구하기
from sklearn.linear_model import LinearRegression
model = LinearRegression()

model.fit(x, y)
model.coef_
model.intercept_

## minimize로 베타 구하기
from scipy.optimize import minimize

def line_perform(beta):
    beta=np.array(beta).reshape(3,1)
    a=(y - matX @ beta)
    return (a.transpose() @ a)

line_perform([8.55769312, 5.96153998, -4.38461679])

# 초기 추정값
initial_guess = [0, 0, 0]

# 최소값 찾기
result = minimize(line_perform, initial_guess)

# 결과 출력
print("최소값:", result.fun)
print("최소값을 갖는 x 값:", result.x)

## minimize로 라쏘 베타 구하기 (lambda=3)
def line_perform_lasso(beta):
    beta=np.array(beta).reshape(3,1)
    a=(y - matX @ beta)
    return (a.transpose() @ a) + 3*np.abs(beta).sum()

line_perform_lasso([8.55769312, 5.96153998, -4.38461679])

# 초기 추정값
initial_guess = [0, 0, 0]

# 최소값 찾기
result_lasso = minimize(line_perform_lasso, initial_guess)

# 결과 출력
print("최소값:", result_lasso.fun)
print("최소값을 갖는 x 값:", result_lasso.x)

## minimize로 ridge 베타 구하기
def line_perform_ridge(beta):
    beta=np.array(beta).reshape(3,1)
    a=(y - matX @ beta)
    return (a.transpose() @ a) + 3*(beta**2).sum()

line_perform_ridge([8.55769312, 5.96153998, -4.38461679])

# 초기 추정값
initial_guess = [0, 0, 0]

# 최소값 찾기
result_ridge = minimize(line_perform_ridge, initial_guess)

# 결과 출력
print("최소값:", result_ridge.fun)
print("최소값을 갖는 x 값:", result_ridge.x)
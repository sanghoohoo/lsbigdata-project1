# y=x^2+3의 최소값이 나오는 입력값 구하기
from scipy.optimize import minimize

def my_f(x):
    return x**2+3  # 0에서 최소값 3

my_f(3)

# 최소값을 찾아주는 함수
# 초기 추정값
initial_guess = [10]

# 최소값 찾기
result = minimize(my_f, initial_guess)

# 결과 출력
print("최소값:", result.fun)
print("최소값을 갖는 x 값:", result.x)

def my_f2(x):
    return x[0]**2+x[1]**2+3

my_f2([1,3])
initial_guess = [0,0]
result = minimize(my_f2, initial_guess)
print("최소값:", result.fun)
print("최소값을 갖는 위치:", result.x)

def my_f3(x):
    return (x[0]-1)**2+(x[1]-2)**2+(x[2]-4)**2+7

my_f3([1,1,1])
initial_guess = [0,0,0]
result = minimize(my_f3, initial_guess)
print("최소값:", result.fun)
print("최소값을 갖는 위치:", result.x)

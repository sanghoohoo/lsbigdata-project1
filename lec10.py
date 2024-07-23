import numpy as np
import pandas as pd

fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "apple", 3.5, True]
print("과일 리스트:", fruits)
print("숫자 리스트:", numbers)
print("혼합 리스트:", mixed)

empty_list1 = []
empty_list2 = list()
print("빈 리스트 1:", empty_list1)
print("빈 리스트 2:", empty_list2)

numbers = [1, 2, 3, 4, 5]
range_list = list(range(5))
print("숫자 리스트:", numbers)
print("range() 함수로 생성한 리스트:", range_list)

range_list[3]='LS빅데이터스쿨'
range_list

range_list[1]=['1st','2nd','3rd']
range_list

range_list[1][2]

#리스트 내포 (list comprehention)
#대괄호로 싸여져있다 => 리스트다.
squares = [x**2 for x in range(10)]
print("제곱 리스트:", squares)

my_squares = [x**3 for x in [3,5,2,15]] #시리즈
my_squares

my_squares2 = [x**3 for x in np.array([3,5,2,15])] #넘파이어레이
my_squares2

exam=pd.read_csv('data/exam.csv')
exam['math']
my_squares3 = [x**3 for x in exam['math']] #판다스시리즈
my_squares3

3+2
'안녕'+'하세요'
'안녕'*3

list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined_list = list1 + list2
print("연결된 리스트:", combined_list)

numbers = [1, 2, 3]
repeated_list = numbers * 3
print("반복된 리스트:", repeated_list)


numbers = [5, 2, 3]
repeated_list = [x for x in numbers for _ in range(3)]
print("각 원소별 반복된 리스트:", repeated_list)

#for 루프 문법
#for i in 범위:
#   작동방식

for x in [4,1,2,3]:
    print(x)
    
for x in numbers:
    for y in range(4):
        print(x)
    
e_list=[]
e_list=[x for x in range(2,21,2)]

mylist=[]
for i in [1,2,3]:
    mylist.append(i*2)
mylist

mylist=[0]*10
for i in range(10):
    mylist[i]=2*(i+1)
mylist


mylist_b=[2,4,6,80,10,12,24,35,23,20]
mylist=[0]*10
for i in range(10):
    mylist[i]=mylist_b[i]
mylist

mylist_b=[2,4,6,80,10,12,24,35,23,20]
mylist=[0]*5
for i in range(5):
    mylist[i]=mylist_b[2*i]
mylist

newlist=[i*2 for i in range(1,11)]
newlist

mylist=[]
for i in range(1,11):
    mylist.append(i*2)
mylist

for i in [0,1]:
    for j in [4,5,6]:
        print(i)

numbers = [5, 2, 3]
repeated_list = [x for x in numbers for _ in range(3)]
print(repeated_list)

for i in numbers:
    for _ in range(3):
        print(i)

fruits = ["apple", "banana", "cherry"]
"banana" in fruits
"grape" in fruits

mylist=[]
for x in fruits:
    mylist.append(x=='banana')
mylist

fruits_np=np.array(fruits)
int(np.where(fruits_np=='banana')[0][0])

fruits.reverse()
fruits

fruits.append('pineapple')
fruits
fruits.reverse()
fruits
fruits.insert(2, 'test')
fruits

fruits.remove('test')
fruits

# 넘파이 배열 생성
fruits = np.array(["apple", "banana", "cherry", "apple", "pineapple"])
# 제거할 항목 리스트
items_to_remove = np.array(["banana", "apple"])
# 불리언 마스크 생성
mask = ~np.isin(fruits, items_to_remove)
# 불리언 마스크를 사용하여 항목 제거
filtered_fruits = fruits[mask]
print("remove() 후 배열:", filtered_fruits)




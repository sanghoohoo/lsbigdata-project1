x=15.34
print(x,"는",type(x),"형식입니다.",sep=' ')

a = "Hello, world!"
b = 'python programming'
type(a)

print('''나는
바보다''')

greeting = "안녕" + " " + "파이썬!"
print("결합 된 문자열:", greeting)

laugh = "하" * 3
print("반복 문자열:", laugh)

fruits = ['apple', 'banana', 'cherry']
fruits
type(fruits)
numbers=[1,2,3]
type(numbers)

mixed_list=[1,'hello',[1,2,3]]
mixed_list
type(mixed_list)

a=(10,20,30)
b_int=(42)
b_tp=(42,)
type(a)
type(b_int)
type(b_tp)

a[0]
a[1]
a[2]

a_list=[10,20,30,40,50]
a_tp=(10,20,30,40,50)
a_list[1]
a_tp[1]
a_list[1]=25
a_tp[1]=25
a_list[1]
a_tp[1:]
a_tp[1:3]
a_list[1:]
a_list[1:3]

def min_max(numbers):
  return min(numbers), max(numbers)

min_max([1,2,3,4,5]
type(min_max([1,2,3,4,5])

person={'name':'Sanghoo',
        'age':(24,25),
        'city':['Seongnam','Daegu']}
print('안상후',person)

person.get('name')
person.get('age')
person.get('city')
person.get('age')[1]
Sanhoo_age=person.get('age')
Sanhoo_age[1]

fruits = {'apple', 'banana', 'cherry', 'apple'}
print("Fruits set:", fruits)
type(fruits)
empty_set=set()
empty_set
empty_set.add('apple')
empty_set.add('apple')
empty_set.add('banana')
empty_set
empty_set.remove('banana')
empty_set.discard('banana')
empty_set.remove('banana')

other_fruits = {'berry', 'cherry'}
union_fruits=fruits.union(other_fruits)
intersection_fruits=fruits.intersection(other_fruits)
print("Union of fruits:", union_fruits)
print("Intersection of fruits:", intersection_fruits)

p=True
type(p)

is_active = True
is_greater = 10 > 5 
is_equal = (10 == 5)
print("Is active:", is_active)
print("Is 10 greater than 5?:", is_greater)
print("Is 10 equal to 5?:", is_equal)

a=3
if(a==2): print('a는 2와 같습니다')
else: print('a는 2와 같지 않습니다')

num=123
str_num=str(num)
str_num
type(str_num)

flt_num=float(num)
flt_num
type(flt_num)


set_example = {'a', 'b', 'c'}
dict_from_set = {key: True for key in set_example}
print("Dictionary from set:", dict_from_set)


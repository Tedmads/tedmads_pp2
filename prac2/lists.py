list1=["Madina", "banana", "cherry"]
list2=[1, 5, 7, 9, 3]
list3=[True, False, False]
list1.extend(list2)
print(list1)

list1=["Madina", "banana", "cherry"]
list2=[1, 5, 7, 9, 3]
list3=[True, False, False]
list1.extend(list2)
list1.pop(1)
print(list1)
del list1[0]
print(list1)
list1.clear()
print(list1)

fruits=["apple", "banana", "cherry", "kiwi", "mango"]
newlist=[]
for x in fruits:
  if "a" in x:
    newlist.append(x)
print(newlist)

madina=[x for x in range(10) if x < 5]
print(madina)

fruits=["apple", "banana", "cherry", "kiwi", "mango"]
newlis=[x.upper() for x in fruits]
print(newlist)
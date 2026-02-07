tuple1=("a", "b" , "c")
tuple2=(1, 2, 3)
tuple3=tuple1 + tuple2
print(tuple3)

thistuple=("apple", "banana", "cherry")
for x in thistuple:
  print(x)

thistuple=("apple", "banana", "cherry")
for i in range(len(thistuple)):
  print(thistuple[i])

thistuple=("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
print(thistuple[-4:-1]) #not include the last item

thistuple=("apple", "banana", "cherry")
if "apple" in thistuple:
  print("Yes, 'apple' is in the fruits tuple")
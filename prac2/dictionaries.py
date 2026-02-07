thisdict={
  "brand":"Ford",
  "model":"Mustang",
  "year":1964
}
if "model" in thisdict:
  print("Yes, 'model' is one of the keys in the thisdict dictionary")

thisdict={
  "brand":"Ford",
  "model":"Mustang",
  "year":1964
}
thisdict["year"]=2018

thisdict={
  "brand":"Ford",
  "model":"Mustang",
  "year":1964
}
thisdict.update({"year":2020})

thisdict={
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
for x in thisdict:
  print(x)

  thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
mydict=dict(thisdict)
print(mydict)
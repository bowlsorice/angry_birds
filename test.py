loop = [3,2,1,"a","b","c"]
for each in loop:
    print(each)
    if each == "a":
        loop.remove(each)
print(loop)

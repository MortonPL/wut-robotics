def tuplemul(tup, num):
    return tuple(x * num for x in tup)

def tuplediv(tup, num):
    return tuple(x / num for x in tup)



array = [(1, 1, 1)] * 10
y = (0,0,0)
x = (1,1,1)

print(x+y)

for x in array:
    y = (y[0] + x[0], y[1] + x[1], y[2] + x[2])

print(y)

print(len(array))




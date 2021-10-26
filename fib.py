
a = 1
b = 1
for _ in range(100):
    c = a + b
    a = b
    b = c
    print(c)
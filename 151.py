m = 0
for i in range(2, 81):
    if i != 3:
        m += 1 / i ** 2
print(m)
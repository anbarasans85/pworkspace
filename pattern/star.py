n = 140
print ''
for i in range(0, n):
    for j in range(0, n-i-1):
        print '',
    for k in range(0, i+1):
        print '*',
    print ''
for i in range(n, 0, -1):
    for j in range(0, n-i+1):
        print '',
    for l in range(0, i-1):
        print '*',
    print ''

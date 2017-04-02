def for_print(n):
    k = 1
    i = 1
    while 1:
        for j in range(0, k):
            print i,
            i += 1
            if i > n:
                return
        k += 1
        print ''

input_n = 12
for_print(input_n)

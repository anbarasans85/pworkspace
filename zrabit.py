def isoverlap(l1, l2):
    # Below works because l1 (list of list) is sorted.
    flag = 0
    for item in l1:
        if not (item[0] < l2[0] and item[1] <= l2[0]) or (item[0] >= l2[1] and item[1] > l2[1]):
            flag = 1
        else:
            flag = 2
    if flag == 0 or flag == 2:
        return False
    else:
        return True


def meetings(input_list):
    # Save input list index and difference
    d1 = [(i, item[1] - item[0]) for i, item in enumerate(input_list)]
    # Sort based on difference
    d2 = sorted(d1, key=lambda t: t[1])
    r1 = list()
    for item in d2:
        if not isoverlap(r1, input_list[item[0]]):
            r1.append(input_list[item[0]])
    return r1


e1 = [[0, 5], [0, 1], [0, 2], [1, 2], [2, 3], [3, 5], [4, 5], [2, 3]]
# e1 = [[0, 1], [1, 2], [2, 3], [3, 5], [4, 5]]
# e1 = [[0, 1000000], [42, 43], [0, 1000000], [42, 43]]
# e1 = [[0, 1], [0, 2], [0, 3], [0, 4]]
result = meetings(e1)
print('Result')
print(result)
print(len(result))

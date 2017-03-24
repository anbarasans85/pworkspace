
input_list1 = [1, 1, 3, 3, 4, 4, 8, 10, 10, 11, 11]
input_list2 = [1, 3, 3, 4, 4, 8, 8, 10, 10]
input_list3 = [1, 1, 3, 4, 4, 8, 8]
input_list4 = [1, 1, 2, 3, 3, 4, 4, 8, 8]
input_list5 = [1, 1, 2, 2, 3, 4, 4, 8, 8]
input_list6 = [1, 1, 2, 2, 3, 3, 4, 8, 8]
input_list7 = [1, 1, 3, 3, 4, 4, 8, 8, 10, 10, 11]


def binary_twice(input_list):
    low = 0
    high = len(input_list) - 1
    while low <= high:
        mid = (low + high) / 2
        if high - low == 2:
            if input_list[mid] == input_list[low]:
                return input_list[high]
            else:
                return input_list[low]
        if low == high:
            return input_list[low]
        if input_list[mid] == input_list[mid - 1] and ((high - mid) % 2 != 0):
            low = mid + 1
        elif input_list[mid] == input_list[mid - 1] and ((high - mid) % 2 == 0):
            high = mid - 2
        elif input_list[mid] == input_list[mid + 1] and ((high - mid) % 2 == 0):
            low = mid + 2
        elif input_list[mid] == input_list[mid + 1] and ((high - mid) % 2 != 0):
            high = mid - 1
        else:
            return input_list[mid]


print binary_twice(input_list7)

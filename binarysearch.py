
input_list1 = [1, 2, 3, 4, 5, 6, 7]


def binary_search(input_list, se):
    low = 0
    high = len(input_list) - 1
    while low <= high:
        mid = (low + high)/2
        if input_list[mid] == se:
            return mid
        elif input_list[mid] < se:
            low = mid + 1
        elif input_list[mid] > se:
            high = mid - 1
    return -1


print binary_search(input_list1, 2)

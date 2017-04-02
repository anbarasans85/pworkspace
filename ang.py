# set 1: stop tops pots spot opts post
# set 2: stops spots posts

def get_count(input_string):
    result = dict()
    for i in range(0, len(input_string)):
        if input_string[i] in result:
            result[input_string[i]] += 1
        else:
            result[input_string[i]] = 1
    return result


def anagram_check(input_s1, input_s2):
    s1_result = get_count(input_s1)
    s2_result = get_count(input_s2)
    if s1_result == s2_result:
        return True
    else:
        return False


print anagram_check('stops', 'opts')


input_list = ["abc", "ef", "bca", "d", "cab", "fe"]


result_dict = dict()
i = 0
while len(input_list) > 0:
    witem = input_list[i]
    check_flag = 0
    j = i+1
    while j < len(input_list):
        if anagram_check(witem, input_list[j]):
            check_flag = 1
            try:
                result_dict[witem] =  result_dict[witem] + ' ' + input_list[j]
            except KeyError:
                result_dict[witem] = input_list[j]
            input_list.remove(input_list[j])
        else:
            j += 1
    if check_flag == 0:
        result_dict[witem] = ''
    input_list.remove(witem)
    i += 1
    if i >= len(input_list):
        i = 0

print('Result::')
for ritem in result_dict.keys():
    print('{0} {1}'.format(ritem, result_dict[ritem]))

def search_forward(data, starting_index, search_range):
    if starting_index == len(data)-1:
        return []
    return convolution(data[starting_index+1:], search_range)


def search_backward(data, starting_index, search_range):
    if starting_index == 0:
        return []
    return convolution(data[:starting_index], search_range)


def convolution(data, search_range):
    if search_range>len(data):
        search_range = len(data)
    result = []
    for i in range(1, search_range+1):
        convolution_helper(i, data, result)
    return result


def convolution_helper(window_size, data, result):
    for i in range(len(data) - window_size + 1):
        result.append(' '.join(data[i:i + window_size]))

s = 'I am really good at computer science'
s_list = s.split()
print(search_backward(s_list, 3, 12))

def new_search_forward(data, starting_index):
    if starting_index == len(data)-1:
        return []
    fragments = []
    for index in range(starting_index + 1, len(data)):
        fragments.append(" ".join(data[starting_index + 1:index + 1]))
    return fragments

s = 'I am really good at computer science'
s_list = s.split()
print(new_search_forward(s_list, 3))

def new_search_backward(data, starting_index):
    if starting_index == 0:
        return []
    fragments = []
    for index in range(1, starting_index + 1):
        fragments.append(" ".join(data[starting_index - index:starting_index]))
    return fragments

s = 'I am really good at computer science'
s_list = s.split()
print(new_search_backward(s_list, 3))

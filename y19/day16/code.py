from util import get_fname

fname = get_fname(__file__)


def phase(num_array, pattern_cache):
    # pattern cache to be array of patterns based on number,
    # repeated to num_array's length
    new_array = []
    for i, num in enumerate(num_array):
        new_pattern = [*pattern_cache[i]]
        new_num = sum([r*new_pattern[i] for i, r in enumerate(num_array)])
        new_array.append(new_num)
    new_array = [abs(x) % 10 for x in new_array]
    return new_array


def generate_cache(num_array, pattern):
    pattern_cache = []
    data_len = len(num_array)
    tens = [10**i for i in range(8)]
    for i in range(len(num_array)):
        if i in tens:
            print(i)
        this_pattern = []
        reps = i + 1
        for j in pattern:
            this_pattern.extend([j]*reps)
        this_pattern = this_pattern * (data_len // (len(pattern)*reps) + 1)
        pattern_cache.append(this_pattern[1:data_len + 1])
    return pattern_cache


def combine_digits(num_array):
    len_array = len(num_array)
    return sum(
        (10**(len_array-1-i))*num
        for i, num in enumerate(num_array[:len_array])
    )


def solve_pt1():
    with open(fname) as f:
        data = [int(x) for x in f.read()]
    pattern = [0, 1, 0, -1]

    pattern_cache = generate_cache(data, pattern)
    for i in range(100):
        data = phase(data, pattern_cache)
    print("".join(str(x) for x in data[:8]))


def solve_pt2():
    with open(fname) as f:
        data = [int(x) for x in f.read()] * 10000
    offset = combine_digits(data[:7])

    for i in range(100):
        for j in range(len(data)-2, len(data)//2, -1):
            curr_sum = data[j] + data[j+1]
            if curr_sum >= 10:
                curr_sum -= 10
            data[j] = curr_sum
    print(combine_digits(data[offset:offset+8]))

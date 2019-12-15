# a number meets the criteria for pt1 if it both has at least 1 double digit and if all digits are in increasing order
# a number meets pt 2 criteria if double digits are not part of a bigger set
from collections import Counter


data = [128392, 643281]


def solve_pt1():
    # slow, but quick to write
    meets_criteria = 0
    for num in range(data[0], data[1] + 1):
        str_num = str(num)

        # check for increasing order
        if "".join(sorted(str_num)) != str_num:
            continue

        # check for double digits
        if len(set(str_num)) == len(str_num):
            continue

        meets_criteria += 1

    print(meets_criteria)


def solve_pt2():
    meets_criteria = 0
    for num in range(data[0], data[1] + 1):
        str_num = str(num)

        # check for increasing order
        if "".join(sorted(str_num)) != str_num:
            continue

        # check for double (MAX) digits
        c = Counter(str_num)
        reps = {r[1]: None for r in c.most_common()}
        if 2 not in reps:
            continue

        meets_criteria += 1

    print(meets_criteria)

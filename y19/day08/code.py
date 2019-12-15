from collections import Counter
from util import get_fname

fname = get_fname(__file__)


def solve_pt1():
    with open(fname) as f:
        data = f.read()

    pixels = 25 * 6
    first = True
    num_0s = None
    mult_result = None
    for i in range(len(data[::pixels])):
        layer = data[i * pixels: (i+1) * pixels]
        c = Counter(layer)

        if first:
            num_0s = c['0']
            mult_result = c['1'] * c['2']
            first = False
        elif c['0'] < num_0s:
            num_0s = c['0']
            mult_result = c['1'] * c['2']
    print(mult_result)


def solve_pt2():
    with open(fname) as f:
        data = f.read()

    pixels = 25 * 6

    first = True
    top_layer = None

    for i in range(len(data[::pixels])):
        layer = [*data[i * pixels: (i+1) * pixels]]

        if first:
            top_layer = layer
            first = False
        else:
            for j, cell in enumerate(top_layer):
                if cell == '2':
                    top_layer[j] = layer[j]

    for i in range(6):
        row = top_layer[i*25:(i+1)*25]
        conv_row = ['*' if cell == '1' else ' ' for cell in row]
        print(" ".join(conv_row))
